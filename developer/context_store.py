"""Small, offline reference design; not a production memory service."""
from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json


@dataclass(frozen=True)
class Memory:
    id: str
    text: str
    kind: str
    source: str
    owner: str
    domain: str
    status: str = "current"
    depends_on: tuple[str, ...] = ()
    check: str = "not independently checked"


class Store:
    def __init__(self):
        self.records = {}

    def add(self, record):
        if record.id in self.records:
            raise ValueError("ID already exists; corrections need a new ID")
        if record.kind not in {"preference", "report", "evidence", "inference"}:
            raise ValueError("unknown kind")
        if record.status != "current" or not all(
            isinstance(x, str) and x.strip()
            for x in (record.id, record.text, record.source, record.owner, record.domain)
        ):
            raise ValueError("new records need explicit provenance and scope")
        for dependency in record.depends_on:
            parent = self.records[dependency]
            if (parent.owner, parent.domain) != (record.owner, record.domain):
                raise ValueError("cross-scope dependency")
            if parent.status != "current":
                raise ValueError("dependency is not current")
        self.records[record.id] = record

    def context(self, owner, domain, ids):
        """Caller supplies an allowlist; never search outside its authorized scope."""
        selected = []
        for record_id in dict.fromkeys(ids):
            record = self.records[record_id]
            if (record.owner, record.domain) != (owner, domain):
                raise PermissionError("record outside authorized scope")
            if record.status != "current":
                raise ValueError("record needs correction or review")
            selected.append(asdict(record))
        payload = {"owner": owner, "domain": domain, "records": selected}
        encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
        return {**payload, "sha256": sha256(encoded).hexdigest()}

    def correct(self, old_id, replacement):
        """Keep old provenance, block its derivatives, accept a new source record."""
        old = self.records[old_id]
        if old.status != "current":
            raise ValueError("only a current record can be corrected")
        if (replacement.owner, replacement.domain) != (old.owner, old.domain):
            raise ValueError("correction changed scope")
        affected = {old_id}
        while True:
            next_ids = {
                r.id for r in self.records.values()
                if set(r.depends_on) & affected
            }
            expanded = affected | next_ids
            if expanded == affected:
                break
            affected = expanded
        if set(replacement.depends_on) & affected:
            raise ValueError("replacement depends on the obsolete conclusion")
        self.add(replacement)  # Validate before changing existing state.
        self.records[old_id] = replace(old, status="superseded")
        for record_id in affected - {old_id}:
            self.records[record_id] = replace(
                self.records[record_id], status="needs_review"
            )
        return sorted(affected)


def demo():
    store = Store()
    store.add(Memory("m1", "Release tests passed", "report", "message:118", "alice", "release"))
    store.add(Memory("s1", "Release is ready", "inference", "summary:9", "alice", "release", depends_on=("m1",)))
    store.add(Memory("r1", "Proceed with release", "inference", "recommendation:2", "alice", "release", depends_on=("s1",)))
    store.add(Memory("p1", "Prefer quiet hotels", "preference", "message:42", "alice", "travel"))
    affected = store.correct("m1", Memory("m2", "Two release tests failed", "evidence", "test-log:build-42", "alice", "release", check="inspected build-42 test output"))
    return store, affected


if __name__ == "__main__":
    store, affected = demo()
    print(json.dumps({"affected": affected, "manifest": store.context("alice", "release", ["m2"])}, indent=2))
