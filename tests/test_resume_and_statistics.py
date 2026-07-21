import unittest
import json
from pathlib import Path

from scripts import build_index as bi


class ResumeAndStatisticsTests(unittest.TestCase):
    def test_stable_ids_are_deterministic(self):
        self.assertEqual(bi.stable_id("file_", "a.pdf"), bi.stable_id("file_", "a.pdf"))
        self.assertNotEqual(bi.stable_id("file_", "a.pdf"), bi.stable_id("logical_", "a.pdf"))

    def test_problem_ids_do_not_depend_on_carrier_count(self):
        self.assertEqual("problem_cumcm_1998_a", f"problem_cumcm_{1998}_{'A'.lower()}")

    def test_relation_enum_requires_evidence_capable_types(self):
        required = {"comments_on", "evaluates_solution", "same_solution_lineage", "continuation_of"}
        self.assertTrue(required <= bi.RELATION_TYPES)

    def test_analysis_eligibility_dimensions(self):
        self.assertIn("algorithm_statistics", bi.ELIGIBILITY_KEYS)
        self.assertIn("reviewer_feedback_statistics", bi.ELIGIBILITY_KEYS)

    def test_candidate_layers_are_not_completed_years(self):
        root = Path(__file__).resolve().parents[1]
        checkpoint = json.loads(
            (root / "analysis-index/09_checkpoints/summary_checkpoint.json").read_text(encoding="utf-8")
        )
        self.assertEqual([], checkpoint["completed_years"])
        self.assertEqual(list(range(1992, 2011)), checkpoint["candidate_layer_years"])


if __name__ == "__main__":
    unittest.main()
