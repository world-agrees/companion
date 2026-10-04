"""Offline SQLite demonstration of correction that survives process restarts.

Trusted application code supplies identity, source labels, and dependency links.
This is not an authorization system, a truth detector, or a production service.
"""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory

from context_store import Memory, Store


class DurableStore:
    """Persist Store's rules inside one SQLite transaction per mutation."""
    def __init__(self, path):
        self.path = str(path)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )

    @staticmethod
    def _load(connection):
        store = Store()
        for record_id, payload in connection.execute("SELECT id, payload FROM records"):
            data = json.loads(payload)
            data["depends_on"] = tuple(data["depends_on"])
            record = Memory(**data)
            if record.id != record_id:
                raise ValueError("record ID disagrees with stored key")
            store.records[record_id] = record
        return store

    def _mutate(self, operation):
        with sqlite3.connect(self.path) as connection:
            # Reserve the writer before reading, so two writers cannot correct
            # different stale snapshots and overwrite one another's changes.
            connection.execute("BEGIN IMMEDIATE")
            store = self._load(connection)
            result = operation(store)  # A validation exception rolls back.
            for record in store.records.values():
                connection.execute(
                    "INSERT OR REPLACE INTO records(id, payload) VALUES (?, ?)",
                    (record.id, json.dumps(asdict(record), sort_keys=True)),
                )
            return result

    def add(self, record):
        return self._mutate(lambda store: store.add(record))

    def correct(self, old_id, replacement):
        return self._mutate(lambda store: store.correct(old_id, replacement))

    def context(self, owner, domain, ids):
        with sqlite3.connect(self.path) as connection:
            return self._load(connection).context(owner, domain, ids)

    def current_context(self, owner, domain):
        """Select only current records in the requested scope, not relevance."""
        with sqlite3.connect(self.path) as connection:
            store = self._load(connection)
            ids = sorted(
                record.id for record in store.records.values()
                if (record.owner, record.domain, record.status) == (owner, domain, "current")
            )
            return store.context(owner, domain, ids)

    def statuses(self):
        with sqlite3.connect(self.path) as connection:
            return {key: record.status for key, record in self._load(connection).records.items()}


def phase(name, path):
    store = DurableStore(path)
    if name == "seed":
        store.add(Memory("m1", "Release tests passed", "report", "synthetic message:118", "alice", "release"))
        store.add(Memory("s1", "Release is ready", "inference", "synthetic summary:9", "alice", "release", depends_on=("m1",)))
        store.add(Memory("r1", "Proceed with release", "inference", "synthetic recommendation:2", "alice", "release", depends_on=("s1",)))
        store.add(Memory("p1", "Prefer quiet hotels", "preference", "synthetic message:42", "alice", "travel"))
        return {"phase": name, "release": store.current_context("alice", "release")}
    if name == "correct":
        affected = store.correct("m1", Memory(
            "m2", "Two release tests failed", "evidence", "synthetic test-log:build-42",
            "alice", "release", check="example assumes a human inspected build-42",
        ))
        return {"phase": name, "affected": affected, "statuses": store.statuses()}
    return {
        "phase": name,
        "release": store.current_context("alice", "release"),
        "travel": store.current_context("alice", "travel"),
        "statuses": store.statuses(),
    }


def demo():
    # Each phase is a distinct process. The database, not a Python object,
    # carries the correction forward. The temporary files are then removed.
    script = str(Path(__file__).resolve())
    with TemporaryDirectory(prefix="world-agrees-memory-") as directory:
        database = str(Path(directory) / "demonstration.sqlite")
        results = []
        for name in ("seed", "correct", "read"):
            completed = subprocess.run(
                [sys.executable, script, "--phase", name, "--db", database],
                check=True, text=True, capture_output=True,
            )
            results.append(json.loads(completed.stdout))
        return {"demonstration_only": True, "separate_processes": 3, "phases": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("seed", "correct", "read"))
    parser.add_argument("--db", help="Use only a disposable demonstration database")
    args = parser.parse_args()
    if bool(args.phase) != bool(args.db):
        parser.error("--phase and --db must be supplied together")
    print(json.dumps(phase(args.phase, args.db) if args.phase else demo(), indent=2))
