import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis-index"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class TestManualFinalization2008(unittest.TestCase):
    def setUp(self):
        self.docs = read_jsonl(ANALYSIS / "02_documents/logical_documents_2008.jsonl")
        self.reps = read_jsonl(ANALYSIS / "02_documents/representations_2008.jsonl")
        self.pages = read_jsonl(ANALYSIS / "02_documents/page_segments_2008.jsonl")
        self.lineages = read_jsonl(ANALYSIS / "04_relations/2008_solution_lineages.jsonl")
        self.gate = read_json(ANALYSIS / "08_quality/gates/2008_gate.json")
        self.checkpoint = read_json(ANALYSIS / "09_checkpoints/2008_checkpoint.json")

    def test_object_counts(self):
        roles = Counter(d["document_role"] for d in self.docs)
        kinds = Counter(d["object_kind"] for d in self.docs)
        self.assertEqual(len(self.docs), 46)
        self.assertEqual(roles["award_paper"], 27)
        self.assertEqual(kinds["solution_paper"], 27)
        self.assertEqual(roles["problem_statement"], 4)
        self.assertEqual(kinds["supporting_object"], 15)
        self.assertEqual(roles["expert_commentary"], 0)
        self.assertEqual(len(self.reps), 46)
        self.assertEqual(len(self.lineages), 27)
        self.assertEqual(len(self.pages), 624)

    def test_six_pack_complete(self):
        names = {
            "document_card.md", "metadata.json", "extracted_text.md",
            "page_map.json", "evidence.jsonl", "review_record.md",
        }
        for doc in self.docs:
            card = ANALYSIS / "02_documents/cards" / doc["logical_document_id"]
            self.assertTrue(card.is_dir(), doc["logical_document_id"])
            self.assertTrue(names.issubset({p.name for p in card.iterdir()}), doc["logical_document_id"])

    def test_manual_and_unknown_policy(self):
        for doc in self.docs:
            self.assertTrue(doc["role_classification"]["manually_verified"])
            self.assertEqual(doc["evidence_status"], "verified")
            for feature in doc["feature_statistics"]:
                self.assertNotEqual(feature["value_status"], "absent")
                if feature["value_status"] == "unknown":
                    self.assertFalse(feature["eligible_for_statistics"])

    def test_gate_and_checkpoint_counts(self):
        expected = {
            "physical_carriers": 46,
            "logical_documents": 46,
            "solution_papers": 27,
            "expert_commentaries": 0,
            "problem_statements": 4,
            "supporting_objects": 15,
            "solution_lineages": 27,
            "representations": 46,
            "pdf_pages": 624,
        }
        self.assertEqual(self.gate["counts"], expected)
        self.assertEqual(self.checkpoint["counts"], expected)
        self.assertIn(self.gate["status"], {"pass_pending_remote_readback", "pass"})
        self.assertIn(self.checkpoint["status"], {"pass_pending_remote_readback", "pass"})

    def test_problem_graph(self):
        graph = read_json(ANALYSIS / "04_relations/2008_problem_solution_graph.json")
        self.assertEqual({row["problem_code"] for row in graph["problems"]}, set("ABCD"))
        self.assertEqual(sum(len(row["solution_lineage_ids"]) for row in graph["problems"]), 27)


if __name__ == "__main__":
    unittest.main()
