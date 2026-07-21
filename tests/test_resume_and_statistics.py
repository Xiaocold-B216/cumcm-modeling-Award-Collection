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

    def test_manual_override_preserves_segments_representations_and_bundle(self):
        source = Path("scripts/build_index.py").read_text(encoding="utf-8")
        self.assertIn('if document.get("manual_overrides"):', source)
        self.assertIn("manual_segments =", source)
        self.assertIn("manual_representations =", source)
        self.assertIn("manually reviewed bundle, page map, and evidence are authoritative", source)
        self.assertIn('r.get("manual_overrides")', source)
        self.assertIn("preserve_existing=bool(docs)", source)
        self.assertIn("return old", source)
        self.assertIn('DOCUMENTS / "orphan_segments.jsonl"', source)
        self.assertIn("blocking_queue =", source)
        self.assertIn('DOCUMENTS / "carrier_absorptions.jsonl"', source)
        self.assertIn("represented_carriers =", source)

    def test_1993_combined_problem_carrier_is_absorbed_not_counted_as_document(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index/02_documents"
        documents = bi.read_jsonl(root / "logical_documents_1993.jsonl")
        representations = bi.read_jsonl(root / "representations_1993.jsonl")
        absorptions = [r for r in bi.read_jsonl(root / "carrier_absorptions.jsonl") if r["year"] == 1993]
        self.assertEqual(5, len(documents))
        self.assertEqual(7, len(representations))
        self.assertEqual(1, len(absorptions))
        self.assertNotIn("logical_300e7c6d8d5a51a3", {d["logical_document_id"] for d in documents})
        self.assertFalse((root / "cards/logical_300e7c6d8d5a51a3").exists())
        represented = {r["carrier_document_id"] for r in representations}
        self.assertIn(absorptions[0]["carrier_document_id"], represented)

    def test_1993_same_page_boundary_and_resolved_alias_have_evidence(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index"
        segments = bi.read_jsonl(root / "02_documents/page_segments_1993.jsonl")
        paper_page_one = [s for s in segments if s["logical_document_id"] == "logical_c8ba8962d24258a2" and s["page"] == 1]
        self.assertEqual(1, len(paper_page_one))
        self.assertEqual(360, paper_page_one[0]["include_bbox"][1])
        relations = bi.read_jsonl(root / "04_relations/document_relations.jsonl")
        aliases = [r for r in relations if r["relation_type"] == "resolved_alias" and r["source_document_id"] == "lineage_intermodulation_frequency_design_unresolved_year"]
        self.assertEqual(1, len(aliases))
        self.assertTrue(aliases[0]["evidence"])
        self.assertTrue(bi.read_jsonl(root / "04_relations/document_relations_1993.jsonl"))
        self.assertEqual(3, len(bi.read_jsonl(root / "04_relations/solution_lineages_1993.jsonl")))


if __name__ == "__main__":
    unittest.main()
