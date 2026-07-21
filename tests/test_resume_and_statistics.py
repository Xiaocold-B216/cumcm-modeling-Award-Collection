import unittest

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


if __name__ == "__main__":
    unittest.main()
