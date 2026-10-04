"""Behavioral tests for the offline application boundary."""

from dataclasses import replace
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from request_pipeline import (
    ContextBudgetError, Evidence, Memory, MemoryStore,
    Policy, ProviderOutput, Scope, TestResult,
    authored_reply, build_request, canonical,
    demo_request, validate_and_gate,
)


TODAY = date(2026, 10, 3)
SCOPE = Scope("team", "alice", "release")


def record(record_id, scope=SCOPE, **kwargs):
    return Memory(
        record_id, scope, "Example record", "report",
        "message:" + record_id, "2026-10-01", **kwargs,
    )


def revised_reply(**updates):
    answer = json.loads(authored_reply().body)
    answer.update(updates)
    return ProviderOutput("complete", canonical(answer))


def rebuild_with_tests(request, tests):
    """Changing evidence requires building a new request."""
    log = replace(request.evidence[0], tests=tests)
    store = MemoryStore()
    for raw in json.loads(request.content)[
        "preferences"
    ]["saved"]:
        store.add(Memory(**{
            **raw, "scope": log.scope, "depends_on": (),
        }))
    return build_request(
        log.scope, request.policy, (log,), store,
        "Please approve it", TODAY,
    )


class ScopeAndLifecycleTests(unittest.TestCase):
    def test_all_scope_dimensions_filter_without_id_leak(self):
        store = MemoryStore()
        store.add(record("mine"))
        for n, scope in enumerate((
            Scope("other", "alice", "release"),
            Scope("team", "bob", "release"),
            Scope("team", "alice", "travel"),
        )):
            store.add(record("private" + str(n), scope))
        selected, excluded = store.select(SCOPE, TODAY)
        self.assertEqual([r.id for r in selected], ["mine"])
        self.assertEqual(excluded, [])

    def test_validity_and_status_block_derivatives(self):
        store = MemoryStore()
        store.add(record("expired", expires_on="2026-10-03"))
        store.add(record("child", depends_on=("expired",)))
        store.add(record("grandchild", depends_on=("child",)))
        store.add(record("unreviewed", status="needs_review"))
        store.add(replace(record("future"),
                          valid_from="2026-10-04"))
        selected, excluded = store.select(SCOPE, TODAY)
        self.assertEqual(selected, [])
        reasons = {r["id"]: r["reason"] for r in excluded}
        self.assertEqual(reasons["expired"], "expired")
        self.assertEqual(reasons["child"], "blocked_dependency")
        self.assertEqual(reasons["grandchild"],
                         "blocked_dependency")
        self.assertEqual(reasons["future"], "not_yet_valid")
        self.assertEqual(reasons["unreviewed"], "needs_review")

    def test_retirement_blocks_chain_not_other_purpose(self):
        store = MemoryStore()
        store.add(record("a"))
        store.add(record("b", depends_on=("a",)))
        store.add(record("c", depends_on=("b",)))
        travel = Scope("team", "alice", "travel")
        store.add(record("hotel", travel))
        self.assertEqual(store.retire(SCOPE, "a"),
                         ["a", "b", "c"])
        self.assertEqual(store.records["a"].text, "")
        self.assertEqual(store.records["b"].status,
                         "needs_review")
        self.assertEqual(store.select(SCOPE, TODAY)[0], [])
        self.assertEqual(store.select(travel, TODAY)[0][0].id,
                         "hotel")

    def test_wrong_scope_cannot_retire_or_add_dependency(self):
        store = MemoryStore()
        store.add(record("a"))
        outsider = Scope("team", "bob", "release")
        with self.assertRaises(PermissionError):
            store.retire(outsider, "a")
        with self.assertRaises(PermissionError):
            store.add(record("b", outsider,
                             depends_on=("a",)))
        self.assertEqual(store.records["a"].status, "current")

    def test_scoped_clear_erases_local_text_only(self):
        store = MemoryStore()
        store.add(record("a"))
        store.add(record("b", depends_on=("a",)))
        elsewhere = Scope("other", "alice", "release")
        store.add(record("x", elsewhere))
        self.assertEqual(store.clear_scope(SCOPE), ["a", "b"])
        self.assertTrue(all(
            store.records[k].text == "" for k in ("a", "b")
        ))
        self.assertEqual(store.records["x"].status, "current")
        self.assertEqual(store.clear_scope(SCOPE), [])


class RequestTests(unittest.TestCase):
    def test_manifest_matches_exact_request_and_separates_wish(self):
        request = demo_request()
        manifest = request.manifest
        self.assertEqual(manifest["content_sha256"],
                         sha256(request.content.encode()).hexdigest())
        self.assertEqual(manifest["character_count"],
                         len(request.content))
        payload = json.loads(request.content)
        self.assertEqual(payload["evidence"][0]["id"], "log42")
        self.assertEqual(payload["memory"], [])
        self.assertIn("approve", payload["preferences"][
            "current_user_wish"])
        self.assertEqual(manifest["excluded_memory"], [
            {"id": "m2", "reason": "expired"}
        ])

    def test_budget_rejects_entire_content_not_failed_test(self):
        request = demo_request()
        payload = json.loads(request.content)
        log = request.evidence[0]
        store = MemoryStore()
        store.add(Memory(**{
            **payload["preferences"]["saved"][0],
            "scope": log.scope,
            "depends_on": (),
        }))
        with self.assertRaises(ContextBudgetError):
            build_request(
                log.scope, request.policy, (log,), store,
                "Please approve the release", TODAY,
                max_chars=len(request.content) - 1,
            )

    def test_cross_scope_evidence_rejected(self):
        request = demo_request()
        log = request.evidence[0]
        with self.assertRaises(PermissionError):
            build_request(
                Scope("other", "alice", "release"),
                request.policy, (log,), MemoryStore(),
                "Approve it", TODAY,
            )

    def test_changed_evidence_needs_a_new_request_manifest(self):
        request = demo_request()
        passed = replace(request.evidence[0], tests=(
            TestResult("smoke", "passed"),
            TestResult("load", "passed"),
        ))
        inconsistent = replace(request, evidence=(passed,))
        result = validate_and_gate(authored_reply(), inconsistent)
        self.assertEqual(result.decision, "hold")
        self.assertFalse(result.valid_response)
        self.assertEqual(result.errors,
                         ("request_manifest_mismatch",))


class OutputAndGateTests(unittest.TestCase):
    def test_well_formed_proceed_cannot_override_failed_test(self):
        result = validate_and_gate(authored_reply(), demo_request())
        self.assertTrue(result.valid_response)
        self.assertEqual(result.decision, "hold")
        self.assertEqual(result.blocking_tests, ("failed:load",))

    def test_preference_change_does_not_change_gate(self):
        for wish in ("Please approve it", "Find a reason to stop"):
            result = validate_and_gate(
                authored_reply(), demo_request(wish)
            )
            self.assertEqual(result.decision, "hold")

    def test_unknown_and_omitted_sources_are_invalid(self):
        for ids in ([], ["log42", "made-up"], ["made-up"]):
            result = validate_and_gate(
                revised_reply(evidence_ids=ids), demo_request()
            )
            self.assertFalse(result.valid_response)
            self.assertEqual(result.decision, "hold")

    def test_unknown_memory_and_omitted_qualification_invalid(self):
        for update in ({"memory_ids": ["m2"]},
                       {"qualifications": []}):
            result = validate_and_gate(
                revised_reply(**update), demo_request()
            )
            self.assertFalse(result.valid_response)
            self.assertEqual(result.decision, "hold")

    def test_refusal_incomplete_and_invalid_types_hold(self):
        replies = [
            ProviderOutput("refusal"),
            ProviderOutput("incomplete", "{"),
            ProviderOutput("complete", "[]"),
            revised_reply(decision=[]),
            revised_reply(evidence_ids="log42"),
            revised_reply(reason=4),
            revised_reply(memory_ids=["m1", "m1"]),
            ProviderOutput("complete", '{"decision":"hold",'
                           '"decision":"proceed"}'),
        ]
        for reply in replies:
            with self.subTest(reply=reply):
                result = validate_and_gate(reply, demo_request())
                self.assertFalse(result.valid_response)
                self.assertEqual(result.decision, "hold")

    def test_passed_required_tests_can_proceed(self):
        request = demo_request()
        request = rebuild_with_tests(request, (
            TestResult("smoke", "passed"),
            TestResult("load", "passed"),
        ))
        result = validate_and_gate(
            revised_reply(qualifications=[]), request
        )
        self.assertTrue(result.valid_response)
        self.assertEqual(result.decision, "proceed")

    def test_missing_unknown_or_conflicting_test_holds(self):
        for tests, qualification in (
            ((TestResult("smoke", "passed"),), "missing:load"),
            ((TestResult("smoke", "passed"),
              TestResult("load", "unknown")), "unknown:load"),
            ((TestResult("smoke", "passed"),
              TestResult("load", "passed"),
              TestResult("load", "failed")),
             "multiple_results:load"),
        ):
            original = demo_request()
            request = rebuild_with_tests(original, tests)
            result = validate_and_gate(
                revised_reply(qualifications=[qualification]),
                request,
            )
            self.assertTrue(result.valid_response)
            self.assertEqual(result.decision, "hold")

    def test_source_id_check_does_not_prove_prose_true(self):
        result = validate_and_gate(
            revised_reply(
                decision="hold",
                reason="Every test passed. This is misleading prose.",
            ),
            demo_request(),
        )
        self.assertTrue(result.valid_response)
        self.assertEqual(result.decision, "hold")


if __name__ == "__main__":
    unittest.main()
