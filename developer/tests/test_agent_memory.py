import json
from pathlib import Path
import sqlite3
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compaction_demo import check_summary, example
from context_store import Memory
from durable_memory import DurableStore, demo, phase


class CompactionTests(unittest.TestCase):
    def test_bad_compaction_loses_attribution_and_promotes_claim(self):
        original, lossy, _ = example()
        problems = check_summary(original, lossy)
        self.assertIn("changed_kind", problems)
        self.assertIn("missing_uncertainty", problems)
        self.assertIn("missing_source_id", problems)

    def test_preserved_summary_keeps_scope_source_and_uncertainty(self):
        original, _, preserved = example()
        self.assertEqual(check_summary(original, preserved), [])
        for field in ("scope", "speaker", "uncertainty"):
            altered = {**preserved, field: "changed"}
            self.assertIn("changed_" + field, check_summary(original, altered))

    def test_correct_metadata_does_not_establish_truth_of_prose(self):
        original, _, preserved = example()
        misleading = {**preserved, "text": "Jordan definitely sabotaged the project."}
        self.assertEqual(check_summary(original, misleading), [])


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "memory.sqlite"
        phase("seed", self.path)

    def test_restart_keeps_correction_and_blocks_derivatives(self):
        phase("correct", self.path)
        restarted = DurableStore(self.path)
        self.assertEqual(restarted.statuses()["m1"], "superseded")
        self.assertEqual(restarted.statuses()["r1"], "needs_review")
        self.assertEqual(restarted.statuses()["s1"], "needs_review")
        records = restarted.current_context("alice", "release")["records"]
        self.assertEqual([record["id"] for record in records], ["m2"])
        for record_id in ("m1", "s1", "r1"):
            with self.assertRaises(ValueError):
                restarted.context("alice", "release", [record_id])

    def test_scope_is_explicit_and_unrelated_preference_survives(self):
        phase("correct", self.path)
        restarted = DurableStore(self.path)
        self.assertEqual(restarted.current_context("alice", "travel")["records"][0]["id"], "p1")
        self.assertEqual(restarted.current_context("bob", "release")["records"], [])
        with self.assertRaises(PermissionError):
            restarted.context("alice", "release", ["p1"])

    def test_failed_correction_does_not_partially_persist(self):
        store = DurableStore(self.path)
        before = store.current_context("alice", "release")
        with self.assertRaises(ValueError):
            store.correct("m1", Memory("bad", "Failed", "evidence", "", "alice", "release"))
        self.assertEqual(DurableStore(self.path).current_context("alice", "release"), before)
        self.assertNotIn("bad", DurableStore(self.path).statuses())

    def test_new_dependency_cannot_use_obsolete_memory(self):
        phase("correct", self.path)
        with self.assertRaises(ValueError):
            DurableStore(self.path).add(Memory("new", "Proceed", "inference", "example:3", "alice", "release", depends_on=("s1",)))

    def test_changed_database_key_is_rejected(self):
        with sqlite3.connect(self.path) as connection:
            value = json.loads(connection.execute("SELECT payload FROM records WHERE id='m1'").fetchone()[0])
            value["id"] = "different-id"
            connection.execute("UPDATE records SET payload=? WHERE id='m1'", (json.dumps(value),))
        with self.assertRaises(ValueError):
            DurableStore(self.path).current_context("alice", "release")

    def test_full_demo_uses_three_fresh_processes(self):
        result = demo()
        self.assertEqual(result["separate_processes"], 3)
        self.assertEqual([phase["phase"] for phase in result["phases"]], ["seed", "correct", "read"])
        self.assertEqual(result["phases"][2]["release"]["records"][0]["id"], "m2")


if __name__ == "__main__":
    unittest.main()
