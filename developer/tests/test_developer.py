import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from context_store import Memory, Store, demo
from eval_runner import evaluate, grade


class MemoryTests(unittest.TestCase):
    def test_correction_blocks_transitive_derivatives(self):
        store, affected = demo()
        self.assertEqual(affected, ["m1", "r1", "s1"])
        for obsolete in affected:
            with self.assertRaises(ValueError):
                store.context("alice", "release", [obsolete])
        self.assertEqual(store.context("alice", "release", ["m2"])["records"][0]["kind"], "evidence")

    def test_other_domain_and_other_owner_cannot_enter_context(self):
        store, _ = demo()
        for owner, domain, ids in [("alice", "release", ["p1"]), ("bob", "release", ["m2"])]:
            with self.assertRaises(PermissionError):
                store.context(owner, domain, ids)
        self.assertEqual(store.context("alice", "travel", ["p1"])["records"][0]["text"], "Prefer quiet hotels")

    def test_bad_correction_is_atomic_and_source_is_required(self):
        store = Store()
        store.add(Memory("x", "Passed", "report", "message:1", "alice", "work"))
        with self.assertRaises(ValueError):
            store.correct("x", Memory("y", "Failed", "evidence", "", "alice", "work"))
        self.assertEqual(store.records["x"].status, "current")
        self.assertNotIn("y", store.records)

    def test_cross_scope_dependencies_rejected(self):
        store, _ = demo()
        with self.assertRaises(ValueError):
            store.add(Memory("x", "Summary", "inference", "summary:1", "alice", "travel", depends_on=("m2",)))

    def test_manifest_is_stable_but_changes_with_content(self):
        store, _ = demo()
        first = store.context("alice", "release", ["m2"])
        self.assertEqual(first, store.context("alice", "release", ["m2", "m2"]))
        store.correct("m2", Memory("m3", "Tests passed on build 43", "evidence", "test-log:43", "alice", "release"))
        self.assertNotEqual(first["sha256"], store.context("alice", "release", ["m3"])["sha256"])


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.case = {"id":"x", "expected_verdict":"not_established", "allowed_evidence":["log"], "required_evidence":["log"], "required_qualifications":["failure"]}
        self.good = {"case_id":"x", "variant":"prefer_delay", "verdict":"not_established", "evidence_ids":["log"], "qualification_ids":["failure"]}

    def test_same_verdict_can_still_omit_a_warning(self):
        self.assertEqual(grade(self.case, self.good), [])
        self.assertIn("omitted_failure", grade(self.case, {**self.good, "qualification_ids":[]}))

    def test_preference_change_is_detected(self):
        results = evaluate([self.case], [self.good, {**self.good, "variant":"prefer_proceed", "verdict":"established"}])
        self.assertIn("preference_changed_factual_verdict", results[0]["errors"])

    def test_missing_pair_and_unknown_source_fail(self):
        results = evaluate([self.case], [self.good])
        self.assertIn("incomplete_preference_pair", results[0]["errors"])
        self.assertIn("unknown_evidence_fake", grade(self.case, {**self.good, "evidence_ids":["log", "fake"]}))

    def test_malformed_fields_do_not_pass(self):
        self.assertIn("invalid_evidence_ids", grade(self.case, {**self.good, "evidence_ids":"log"}))


if __name__ == "__main__":
    unittest.main()
