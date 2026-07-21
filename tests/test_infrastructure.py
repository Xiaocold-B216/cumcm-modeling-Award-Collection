import json
import unittest
from pathlib import Path

from scripts import build_index as bi


ROOT = Path(__file__).resolve().parents[1]


class InfrastructureTests(unittest.TestCase):
    def test_versions_and_baseline(self):
        self.assertEqual(bi.SCHEMA_VERSION, "1.4.1")
        self.assertEqual(bi.PARSER_VERSION, "0.5.1")
        self.assertEqual(bi.SOURCE_BASELINE, "a042ecf898feaba6fc81d543a10e0188db8b2b12")

    def test_year_and_role_classification(self):
        self.assertEqual(bi.extract_year("1995年数学建模/论文.pdf"), 1995)
        self.assertEqual(bi.classify_role("1995优秀论文/飞行管理问题答卷评述.pdf")[0], "expert_commentary")
        self.assertEqual(bi.classify_role("1998年数学建模国赛真题+优秀论文/1998年赛题/A题.pdf")[0], "problem_statement")
        self.assertEqual(
            bi.classify_role("1998年数学建模国赛真题+优秀论文/1998年优秀论文/1998A：投资收益和风险.pdf")[0],
            "award_paper",
        )
        self.assertEqual(bi.classify_role("冶炼车间最优调度模型的检验.pdf")[:2],
                         ("solution_summary", "validation_summary"))

    def test_candidate_pdf_excludes_administrative_and_attachment_pdfs(self):
        self.assertTrue(bi.candidate_pdf("2010年/2010年优秀论文/A001.pdf"))
        self.assertFalse(bi.candidate_pdf("2015年/赛题/D题附件2.pdf"))
        self.assertFalse(bi.candidate_pdf("2017年/全国大学生数学建模竞赛论文格式规范.pdf"))

    def test_unknown_is_never_absent_or_eligible(self):
        rows = bi.feature_records("短文本", ["短文本"], "scanned_or_no_text", "award_paper")
        self.assertTrue(rows)
        self.assertTrue(all(r["value_status"] == "unknown" for r in rows))
        self.assertTrue(all(not r["eligible_for_statistics"] for r in rows))

    def test_automatic_keyword_features_never_claim_absence_or_enter_denominator(self):
        rows = bi.feature_records("摘要 结论 " * 300, ["摘要 结论 " * 300], "native_text", "award_paper")
        self.assertNotIn("absent", {r["value_status"] for r in rows})
        self.assertTrue(all(not r["eligible_for_statistics"] for r in rows))

    def test_core_object_and_relation_enums_are_separate(self):
        self.assertIn("contains", bi.RELATION_TYPES)
        self.assertIn("continuation_of", bi.RELATION_TYPES)
        self.assertNotIn("carrier_document", bi.ROLES)
        self.assertEqual(bi.FIELD_STATUSES, {"present", "absent", "unknown", "not_applicable"})

    def test_source_verification_and_baseline_count(self):
        check = bi.verify_source()
        self.assertEqual(check["original_source_modifications"], 0)
        self.assertEqual(len(bi.baseline_entries()), 3614)

    def test_unicode_baseline_paths_are_real_checkout_paths(self):
        entries = bi.baseline_entries()
        chinese = next(row for row in entries if "1992年" in row["relative_path"])
        self.assertFalse(chinese["relative_path"].startswith('"'))
        self.assertTrue((ROOT / chinese["relative_path"]).exists())

    def test_schema_files_are_readable(self):
        bi.ensure_dirs()
        bi.write_schema_files()
        schema = json.loads((ROOT / "schema/logical_document.schema.json").read_text(encoding="utf-8"))
        self.assertIn("document_subtype", schema["required"])
        self.assertEqual(schema["schema_version"], "1.4.1")

    def test_schema_manifest_is_idempotent(self):
        bi.ensure_dirs()
        bi.write_schema_files()
        manifest = ROOT / "analysis-index/00_control/schema_version_manifest.json"
        first = manifest.read_bytes()
        bi.write_schema_files()
        self.assertEqual(first, manifest.read_bytes())


if __name__ == "__main__":
    unittest.main()
