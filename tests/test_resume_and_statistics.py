import unittest
import json
import csv
from collections import Counter
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
        self.assertIn("manual_year_docs =", source)
        self.assertIn("logical_id in manual_year_docs", source)

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

    def test_1994_carrier_logical_representation_and_lineage_denominators(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index"
        documents = bi.read_jsonl(root / "02_documents/logical_documents_1994.jsonl")
        representations = bi.read_jsonl(root / "02_documents/representations_1994.jsonl")
        self.assertEqual(13, len(documents))
        self.assertEqual(Counter({"award_paper": 9, "expert_commentary": 2, "problem_statement": 2}),
                         Counter(d["document_role"] for d in documents))
        self.assertEqual(26, len(representations))
        self.assertEqual(13, sum(bool(r["preferred_representation"]) for r in representations))
        self.assertEqual(4, len({r["carrier_document_id"] for r in representations}))
        self.assertEqual(9, len(bi.read_jsonl(root / "04_relations/solution_lineages_1994.jsonl")))

    def test_1994_mountain_route_boundary_is_complete_and_orphans_preserved(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index"
        documents = bi.read_jsonl(root / "02_documents/logical_documents_1994.jsonl")
        mountain = next(d for d in documents if d["title"] == "山区公路线路选优方法")
        self.assertEqual("complete", mountain["completeness_status"])
        self.assertIn("1300", json.dumps(mountain["content_analysis"], ensure_ascii=False))
        boundaries = [b for b in bi.read_jsonl(root / "02_documents/article_boundaries_1994.jsonl") if b["same_page_boundary"]]
        self.assertEqual({212, 232}, {b["boundary_y"] for b in boundaries})
        orphans = [o for o in bi.read_jsonl(root / "02_documents/orphan_segments.jsonl") if o.get("year") == 1994]
        self.assertEqual(2, len(orphans))
        self.assertTrue(all("下转第57页" in o["reason_excluded_from_primary_document"] for o in orphans))

    def test_1994_unknown_is_outside_field_specific_denominator(self):
        path = Path(__file__).resolve().parents[1] / "analysis-index/06_statistics/yearly/1994_statistics.csv"
        with path.open(encoding="utf-8-sig", newline="") as fh:
            rows = {r["metric"]: r for r in csv.DictReader(fh)}
        self.assertEqual("4", rows["model_assumptions:unknown"]["numerator"])
        self.assertEqual("5", rows["model_assumptions:present"]["denominator"])
        self.assertEqual("5", rows["model_assumptions:absent"]["denominator"])

    def test_1995_logical_roles_representations_and_missing_segment(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index"
        docs = bi.read_jsonl(root / "02_documents/logical_documents_1995.jsonl")
        self.assertEqual(18, len(docs))
        self.assertEqual(Counter({"award_paper": 13, "expert_commentary": 2,
                                  "problem_statement": 2, "solution_summary": 1}),
                         Counter(d["document_role"] for d in docs))
        reps = bi.read_jsonl(root / "02_documents/representations_1995.jsonl")
        self.assertEqual(30, len(reps))
        self.assertEqual(18, sum(bool(r["preferred_representation"]) for r in reps))
        missing = next(d for d in docs if d["title"] == "天车与冶炼炉的作业调度")
        self.assertEqual("missing_segment", missing["completeness_status"])
        self.assertEqual("content_verified_partial", missing["evidence_status"])
        requests = bi.read_jsonl(root / "02_documents/missing_segment_requests.jsonl")
        self.assertIn("missing_1995_b_scheduling_pages_41_50", {r["request_id"] for r in requests})

    def test_1995_unknown_not_absent_and_field_denominators(self):
        path = Path(__file__).resolve().parents[1] / "analysis-index/06_statistics/yearly/1995_statistics.csv"
        with path.open(encoding="utf-8-sig", newline="") as fh:
            rows = {r["metric"]: r for r in csv.DictReader(fh)}
        self.assertEqual("1", rows["final_solution:unknown"]["numerator"])
        self.assertEqual("12", rows["final_solution:eligible_denominator"]["numerator"])
        self.assertEqual("8", rows["visualization:present"]["numerator"])
        self.assertEqual("12", rows["visualization:eligible_denominator"]["numerator"])
        self.assertEqual("7", rows["model_validation:present"]["numerator"])

    def test_1995_same_page_boundaries_and_orphan_are_preserved(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index"
        boundaries = bi.read_jsonl(root / "02_documents/article_boundaries_1995.jsonl")
        self.assertEqual(15, len(boundaries))
        self.assertEqual(8, sum(bool(b["same_page_boundary"]) for b in boundaries))
        self.assertTrue(all(b["manually_verified"] for b in boundaries))
        orphans = [o for o in bi.read_jsonl(root / "02_documents/orphan_segments.jsonl") if int(o.get("year", 0)) == 1995]
        self.assertEqual(1, len(orphans))
        self.assertEqual("preserved", orphans[0]["preservation_status"])

    def test_1995_validation_summary_uses_subtype_not_new_role(self):
        root = Path(__file__).resolve().parents[1] / "analysis-index"
        docs = bi.read_jsonl(root / "02_documents/logical_documents_1995.jsonl")
        summary = next(d for d in docs if d["document_role"] == "solution_summary")
        self.assertEqual("validation_summary", summary["document_subtype"])
        self.assertEqual("included", summary["corpus_eligibility"]["validation_patterns"])


if __name__ == "__main__":
    unittest.main()
