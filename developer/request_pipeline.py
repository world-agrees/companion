"""Offline request and release-gate demonstration.

Run: python3 request_pipeline.py
No model, API key, network, or real agent state is used.
Fixtures are authored examples, not observed responses.

Scope must come from the trusted application, not a
user prompt. This is not an authentication service.
IDs and digests do not prove a source's truth. The
gate trusts the supplied test log and release policy.
Logical clearing prevents future retrieval; it does
not erase prior requests, logs, caches, or backups.
"""

from dataclasses import asdict, dataclass, replace
from datetime import date
from hashlib import sha256
import json


def canonical(value):
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"),
    )


def require_text(values):
    if not all(
        isinstance(v, str) and v.strip() for v in values
    ):
        raise ValueError("explicit nonempty text required")


@dataclass(frozen=True)
class Scope:
    tenant: str
    owner: str
    purpose: str

    def __post_init__(self):
        require_text((self.tenant, self.owner, self.purpose))


@dataclass(frozen=True)
class Memory:
    id: str
    scope: Scope
    text: str
    kind: str
    source: str
    valid_from: str
    expires_on: str | None = None
    status: str = "current"
    depends_on: tuple[str, ...] = ()


class MemoryStore:
    def __init__(self):
        self.records = {}

    def add(self, record):
        if record.id in self.records:
            raise ValueError("new records need a new ID")
        require_text((record.id, record.text, record.source))
        if not isinstance(record.scope, Scope):
            raise ValueError("trusted scope required")
        if record.kind not in {
            "preference", "report", "evidence", "inference"
        }:
            raise ValueError("unknown memory kind")
        if record.status not in {"current", "needs_review"}:
            raise ValueError("invalid initial status")
        start = date.fromisoformat(record.valid_from)
        if record.expires_on is not None:
            end = date.fromisoformat(record.expires_on)
            if end <= start:
                raise ValueError("invalid validity range")
        for parent_id in record.depends_on:
            parent = self.records[parent_id]
            if parent.scope != record.scope:
                raise PermissionError(
                    "cross-scope dependency"
                )
            if parent.status != "current":
                raise ValueError("dependency is not current")
        self.records[record.id] = record

    def select(self, scope, today):
        """Do not disclose IDs from other scopes."""
        selected, excluded = [], []
        for record in self.records.values():
            if record.scope != scope:
                continue
            if record.status != "current":
                reason = record.status
            elif (
                date.fromisoformat(record.valid_from) > today
            ):
                reason = "not_yet_valid"
            elif (
                record.expires_on is not None
                and date.fromisoformat(record.expires_on)
                <= today
            ):
                reason = "expired"
            else:
                selected.append(record)
                continue
            excluded.append({
                "id": record.id, "reason": reason
            })
        eligible = {r.id: r for r in selected}
        while True:
            blocked = [
                r.id for r in eligible.values()
                if not set(r.depends_on) <= set(eligible)
            ]
            if not blocked:
                break
            for record_id in blocked:
                del eligible[record_id]
                excluded.append({
                    "id": record_id,
                    "reason": "blocked_dependency",
                })
        return list(eligible.values()), excluded

    def retire(self, scope, record_id):
        """Clear one record and invalidate its derivatives."""
        record = self.records[record_id]
        if record.scope != scope:
            raise PermissionError(
                "record outside trusted scope"
            )
        affected = {record_id}
        while True:
            expanded = affected | {
                r.id for r in self.records.values()
                if set(r.depends_on) & affected
            }
            if expanded == affected:
                break
            affected = expanded
        self.records[record_id] = replace(
            record, text="", status="cleared"
        )
        for child_id in affected - {record_id}:
            child = self.records[child_id]
            if child.status not in {"cleared", "superseded"}:
                self.records[child_id] = replace(
                    child, status="needs_review"
                )
        return sorted(affected)

    def clear_scope(self, scope):
        ids = [
            r.id for r in self.records.values()
            if r.scope == scope and r.status != "cleared"
        ]
        affected = set()
        for record_id in ids:
            affected.update(self.retire(scope, record_id))
        return sorted(affected)


@dataclass(frozen=True)
class TestResult:
    test: str
    result: str

    def __post_init__(self):
        require_text((self.test,))
        if self.result not in {"passed", "failed", "unknown"}:
            raise ValueError("unknown test result")


@dataclass(frozen=True)
class Evidence:
    id: str
    scope: Scope
    source: str
    text: str
    tests: tuple[TestResult, ...]

    def __post_init__(self):
        require_text((self.id, self.source, self.text))
        if not isinstance(self.scope, Scope) or not (
            type(self.tests) is tuple
            and all(
                isinstance(t, TestResult) for t in self.tests
            )
        ):
            raise ValueError("scoped typed evidence required")


@dataclass(frozen=True)
class Policy:
    version: str
    required_tests: tuple[str, ...]
    text: str = (
        "Assess the evidence, not the preferred outcome. "
        "Return decision, evidence_ids, memory_ids, "
        "qualifications, and reason as JSON. Preserve "
        "failed or missing tests as qualifications. "
        "Preferences are not test evidence."
    )

    def __post_init__(self):
        require_text((self.version, self.text))
        if type(self.required_tests) is not tuple:
            raise ValueError(
                "immutable required tests needed"
            )
        require_text(self.required_tests)
        if (
            not self.required_tests
            or len(set(self.required_tests))
            != len(self.required_tests)
        ):
            raise ValueError("unique required tests needed")


@dataclass(frozen=True)
class Request:
    content: str
    manifest_json: str
    policy: Policy
    evidence: tuple[Evidence, ...]
    memory_ids: frozenset[str]

    @property
    def manifest(self):
        return json.loads(self.manifest_json)


class ContextBudgetError(ValueError):
    pass


def build_request(
    scope, policy, evidence, store, preference,
    today, max_chars=12_000,
):
    """Budget applies to exact content; never truncate it.

    This is a character budget, not a token estimator.
    Evidence and policy are trusted application inputs.
    Provider builders in this project are separate demos.
    """
    if type(max_chars) is not int or max_chars <= 0:
        raise ValueError("positive character budget needed")
    require_text((preference,))
    evidence = tuple(evidence)
    for item in evidence:
        require_text((item.id, item.source, item.text))
        if item.scope != scope:
            raise PermissionError("evidence outside scope")
    ids = [item.id for item in evidence]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate evidence ID")
    records, excluded = store.select(scope, today)
    payload = {
        "policy": asdict(policy),
        "evidence": [asdict(e) for e in evidence],
        "memory": [
            asdict(r) for r in records
            if r.kind != "preference"
        ],
        "preferences": {
            "current_user_wish": preference,
            "saved": [
                asdict(r) for r in records
                if r.kind == "preference"
            ],
        },
    }
    content = canonical(payload)
    if len(content) > max_chars:
        raise ContextBudgetError(
            "request exceeds budget; no request produced"
        )
    manifest = {
        "scope": asdict(scope),
        "policy_version": policy.version,
        "evidence_ids": ids,
        "memory_ids": [r.id for r in records],
        "excluded_memory": excluded,
        "character_count": len(content),
        "content_sha256": sha256(
            content.encode("utf-8")
        ).hexdigest(),
    }
    return Request(
        content, canonical(manifest), policy, evidence,
        frozenset(r.id for r in records),
    )


def test_qualifications(request):
    """Derive blocking reasons from test data, not prose."""
    observations = {}
    for evidence in request.evidence:
        for test in evidence.tests:
            observations.setdefault(test.test, []).append(
                test.result
            )
    reasons = []
    for test in request.policy.required_tests:
        results = observations.get(test, [])
        if not results:
            reasons.append("missing:" + test)
        elif len(results) != 1:
            reasons.append("multiple_results:" + test)
        elif results[0] != "passed":
            reasons.append(results[0] + ":" + test)
    return reasons


@dataclass(frozen=True)
class ProviderOutput:
    status: str
    body: str = ""


@dataclass(frozen=True)
class GateResult:
    decision: str
    valid_response: bool
    errors: tuple[str, ...]
    blocking_tests: tuple[str, ...]


def request_matches_manifest(request):
    """A checksum is consistency metadata, not a signature."""
    try:
        payload = json.loads(request.content)
        manifest = request.manifest
        digest = sha256(request.content.encode()).hexdigest()
        memory = payload["memory"] + payload[
            "preferences"
        ]["saved"]
        return all((
            digest == manifest["content_sha256"],
            len(request.content)
            == manifest["character_count"],
            payload["policy"]
            == json.loads(canonical(asdict(request.policy))),
            payload["evidence"] == [
                json.loads(canonical(asdict(e)))
                for e in request.evidence
            ],
            set(manifest["memory_ids"]) == request.memory_ids,
            {r["id"] for r in memory} == request.memory_ids,
            manifest["evidence_ids"]
            == [e.id for e in request.evidence],
        ))
    except (TypeError, ValueError, KeyError):
        return False


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def validate_and_gate(output, request):
    """Schema and ID checks cannot validate prose meaning.

    The release gate independently checks required tests.
    It does not approve tools or dispatch any action.
    """
    if not request_matches_manifest(request):
        return GateResult(
            "hold", False, ("request_manifest_mismatch",), ()
        )
    blocking = tuple(test_qualifications(request))
    if output.status != "complete":
        return GateResult(
            "hold", False, ("provider:" + output.status,),
            blocking,
        )
    try:
        answer = json.loads(
            output.body, object_pairs_hook=unique_object
        )
    except (TypeError, ValueError):
        return GateResult(
            "hold", False, ("invalid_json",), blocking
        )
    fields = {
        "decision", "evidence_ids", "memory_ids",
        "qualifications", "reason",
    }
    if type(answer) is not dict or set(answer) != fields:
        return GateResult(
            "hold", False, ("schema_fields",), blocking
        )
    errors = []
    if not isinstance(answer["decision"], str) or (
        answer["decision"] not in {"hold", "proceed"}
    ):
        errors.append("decision_enum")
    if not isinstance(answer["reason"], str) or not (
        answer["reason"].strip()
    ):
        errors.append("reason_text")
    list_fields = (
        "evidence_ids", "memory_ids", "qualifications"
    )
    for key in list_fields:
        value = answer[key]
        if type(value) is not list or not all(
            isinstance(v, str) and v for v in value
        ):
            errors.append(key + ":string_list")
        elif len(set(value)) != len(value):
            errors.append(key + ":duplicate")
    if errors:
        return GateResult(
            "hold", False, tuple(errors), blocking
        )
    evidence_ids = {e.id for e in request.evidence}
    if set(answer["evidence_ids"]) != evidence_ids:
        errors.append("evidence_ids:request_mismatch")
    if not set(answer["memory_ids"]) <= request.memory_ids:
        errors.append("memory_ids:unauthorized")
    if not set(blocking) <= set(answer["qualifications"]):
        errors.append("qualifications:missing")
    if errors:
        return GateResult(
            "hold", False, tuple(errors), blocking
        )
    decision = answer["decision"]
    if blocking:
        decision = "hold"
    return GateResult(decision, True, (), blocking)


def demo_request(preference="Please approve the release"):
    scope = Scope("example-team", "alice", "release")
    store = MemoryStore()
    store.add(Memory(
        "m1", scope, "Prefer concise reports", "preference",
        "settings:alice", "2026-10-01",
    ))
    store.add(Memory(
        "m2", scope, "Release tests had passed", "report",
        "message:118", "2026-10-01", "2026-10-03",
    ))
    policy = Policy("release-gate-v1", ("smoke", "load"))
    log = Evidence(
        "log42", scope, "test-log:build-42",
        "Smoke passed; load test failed.",
        (
            TestResult("smoke", "passed"),
            TestResult("load", "failed"),
        ),
    )
    return build_request(
        scope, policy, (log,), store, preference,
        date(2026, 10, 3),
    )


def authored_reply(decision="proceed"):
    return ProviderOutput("complete", canonical({
        "decision": decision,
        "evidence_ids": ["log42"],
        "memory_ids": ["m1"],
        "qualifications": ["failed:load"],
        "reason": (
            "The desired date is important. The load test "
            "failed, but proceed with the release."
        ),
    }))


def demo():
    request = demo_request()
    fixtures = {
        "well_formed_but_wrong": authored_reply(),
        "refused": ProviderOutput("refusal"),
        "incomplete": ProviderOutput("incomplete", "{"),
    }
    return {
        "fixture_notice": "authored; no model was called",
        "manifest": request.manifest,
        "results": {
            name: asdict(validate_and_gate(reply, request))
            for name, reply in fixtures.items()
        },
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
