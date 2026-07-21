#!/usr/bin/env python3
"""Shared persistence layer for evidence-led annual manual review scripts."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from scripts.apply_manual_review_1992 import fstats, read_jsonl, stable, write_json, write_jsonl

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
DOCS = AI / "02_documents"
CARDS = DOCS / "cards"
REL = AI / "04_relations"
CAT = AI / "05_catalogs"
REPORTS = AI / "07_reports/yearly"
QUALITY = AI / "08_quality"
WIDTH, HEIGHT = 595.22, 842.0
FIELDS = ["abstract", "model_assumptions", "symbol_definitions", "model_validation",
          "sensitivity_analysis", "error_analysis", "final_solution",
          "final_answer_summary_table", "flowchart", "visualization", "references",
          "appendix", "code_description"]


def corpus_eligibility(role: str, subtype: str = "none") -> dict[str, str]:
    out = {k: "excluded" for k in ["award_paper_patterns", "reviewer_feedback", "problem_analysis",
                                    "validation_patterns", "visualization_patterns"]}
    if role == "award_paper":
        out["award_paper_patterns"] = out["visualization_patterns"] = "included"
    elif role == "expert_commentary":
        out["reviewer_feedback"] = "included"
    elif role == "problem_statement":
        out["problem_analysis"] = "included"
    elif role == "solution_summary" and subtype == "validation_summary":
        out["validation_patterns"] = "included"
    return out


def _pages(spec: dict[str, Any]) -> list[int]:
    return list(spec.get("page_numbers") or range(1, int(spec["pages"]) + 1))


def apply_manual_year(year: int, specs: list[dict[str, Any]], *,
                      boundaries: list[dict[str, Any]] | None = None,
                      extra_relations: list[dict[str, Any]] | None = None,
                      feedback_rows: list[dict[str, Any]] | None = None,
                      visual_rows: list[dict[str, Any]] | None = None,
                      report_text: str = "", quality_text: str = "",
                      reviewed_at: str = "2026-07-22T02:00:00Z") -> dict[str, int]:
    boundaries = boundaries or []
    extra_relations = extra_relations or []
    feedback_rows = feedback_rows or []
    visual_rows = visual_rows or []
    with (DOCS / f"{year}_carrier_manifest.csv").open(encoding="utf-8-sig", newline="") as fh:
        carrier_rows = list(csv.DictReader(fh))

    def carrier(fragment: str) -> str:
        found = [r["carrier_document_id"] for r in carrier_rows if fragment in r["filename"]]
        if len(found) != 1:
            raise SystemExit(f"carrier lookup {fragment!r}: {found}")
        return found[0]

    for spec in specs:
        spec.setdefault("subtype", "none")
        spec.setdefault("authors", [])
        spec.setdefault("models", [])
        spec.setdefault("algorithms", [])
        spec.setdefault("evidence", [])
        spec.setdefault("content", {})
        spec.setdefault("present", [])
        spec.setdefault("absent", [])
        spec.setdefault("completeness", "complete")
        spec.setdefault("corpus_status", "included")
        spec.setdefault("parse_status", "parsed" if spec["role"] == "problem_statement" else "partially_parsed")
        spec.setdefault("evidence_status", "verified" if spec["role"] == "problem_statement" else "key_content_verified")
        spec["id"] = stable("logical_", year, spec["title"], spec["role"])
        spec["problem_id"] = f"problem_cumcm_{year}_{spec['problem'].lower()}"
        spec["lineage"] = stable(f"lineage_cumcm_{year}_", spec["problem"], spec["title"]) if spec["role"] == "award_paper" else None
        spec["carrier_id"] = carrier(spec["fragment"])

    docs, segments, reps = [], [], []
    old_auto = {d["logical_document_id"] for d in read_jsonl(DOCS / f"logical_documents_{year}.jsonl")}
    reviewed = {s["id"] for s in specs}
    all_docs = [d for d in read_jsonl(DOCS / "logical_documents.jsonl") if int(d.get("year", 0)) != year]
    for order, spec in enumerate(specs, 1):
        did, cid, pages = spec["id"], spec["carrier_id"], _pages(spec)
        sids = []
        for page in pages:
            box = spec.get("boxes", {}).get(page, [0, 0, WIDTH, HEIGHT])
            sid = stable("segment_", did, cid, page, *box, f"manual-{year}")
            sids.append(sid)
            segments.append({"segment_id": sid, "carrier_document_id": cid,
                "logical_document_id": did, "page": page, "include_bbox": box, "exclude_bbox": [],
                "normalized_bbox": [round(box[0]/WIDTH,6), round(box[1]/HEIGHT,6), round(box[2]/WIDTH,6), round(box[3]/HEIGHT,6)],
                "page_width": WIDTH, "page_height": HEIGHT, "page_rotation": 0,
                "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
                "reason": "manually verified article region",
                "segmentation_status": "segmented" if box != [0,0,WIDTH,HEIGHT] else "not_required",
                "manually_verified": True, "manual_overrides": True})
        rid = stable("representation_", did, cid)
        reps.append({"representation_id": rid, "logical_document_id": did,
            "carrier_document_id": cid, "segment_ids": sids, "page_coverage": pages,
            "completeness": spec["completeness"],
            "visual_quality": "native_text" if spec["role"] == "problem_statement" else "good_scan",
            "text_layer_quality": "native_text_reviewed" if spec["role"] == "problem_statement" else "scan_visual_only",
            "table_quality": "verified_key_tables" if spec["completeness"] == "complete" else "partial",
            "formula_quality": "verified_key_formulas" if spec["completeness"] == "complete" else "partial",
            "page_order_quality": "verified", "contamination_level": "none_detected",
            "preferred_representation": True, "preference_reason": "best available manually reviewed representation",
            "manual_overrides": True})
        vals = {f: ("unknown", []) for f in FIELDS}
        if spec["role"] == "award_paper":
            for field in spec["absent"]: vals[field] = ("absent", pages)
            for field in spec["present"]: vals[field] = ("present", pages)
        elif spec["role"] in {"problem_statement", "other_related"}:
            vals = {f: ("not_applicable", []) for f in FIELDS}
        analysis = {"metadata_statistics"}
        if spec["role"] == "award_paper":
            analysis |= {"structure_statistics", "model_statistics", "algorithm_statistics",
                         "visualization_statistics", "result_pattern_statistics"}
        elif spec["role"] == "expert_commentary": analysis.add("reviewer_feedback_statistics")
        elif spec["role"] == "problem_statement": analysis.add("problem_analysis")
        doc = {"logical_document_id": did, "entity_type": "logical_document", "year": year,
            "article_order": order, "title": spec["title"], "authors": spec["authors"],
            "document_role": spec["role"], "document_subtype": spec["subtype"],
            "problem_code": spec["problem"], "problem_id": spec["problem_id"],
            "solution_lineage_id": spec["lineage"], "carrier_document_ids": [cid],
            "segment_ids": sids, "page_count": len(pages), "parse_status": spec["parse_status"],
            "evidence_status": spec["evidence_status"],
            "segmentation_status": "segmented" if any(x["include_bbox"] != [0,0,WIDTH,HEIGHT] for x in segments if x["logical_document_id"] == did) else "not_required",
            "completeness_status": spec["completeness"], "corpus_status": spec["corpus_status"],
            "representation_quality": "manually_reviewed",
            "role_classification": {"predicted_role": spec["role"], "confidence": 1.0,
                "classification_basis": ["title", "document_structure", "visual_review", "article_boundaries"],
                "conflicting_signals": spec.get("conflicting_signals", []), "manually_verified": True},
            "corpus_eligibility": corpus_eligibility(spec["role"], spec["subtype"]),
            "analysis_eligibility": sorted(analysis), "feature_statistics": fstats(spec["role"], vals),
            "models": spec["models"], "algorithms": spec["algorithms"], "content_analysis": spec["content"],
            "manual_overrides": True, "manual_reviewed_at": reviewed_at}
        docs.append(doc)
        folder = CARDS / did
        write_json(folder / "metadata.json", doc)
        write_json(folder / "page_map.json", {"logical_document_id": did,
            "page_number_basis": "carrier local, 1-based", "representation_id": rid,
            "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
            "pages": [{"page": x["page"], "width": WIDTH, "height": HEIGHT, "rotation": 0,
                       "valid_bbox": x["include_bbox"], "excluded_bbox": [], "segment_id": x["segment_id"],
                       "carrier_document_id": cid, "manually_verified": True}
                      for x in segments if x["logical_document_id"] == did]})
        write_jsonl(folder / "evidence.jsonl", [{"logical_document_id": did,
            "paper_id": did if spec["role"] == "award_paper" else None, "source_page": p,
            "source_section": sec, "source_bbox": bbox or [0,0,WIDTH,HEIGHT], "evidence_type": typ,
            "text_excerpt": text, "normalized_claim": claim, "confidence": .97,
            "extraction_method": "manual_visual_review", "manual_review_required": False}
            for item in spec["evidence"] for p, sec, typ, text, claim, bbox in
            [tuple(item) if len(item) == 6 else tuple(item) + ([],)]])
        (folder / "document_card.md").write_text(
            f"# {spec['title']}\n\n- 年份：{year}\n- 角色：{spec['role']}\n- subtype：{spec['subtype']}\n"
            f"- 状态：{doc['parse_status']} / {doc['evidence_status']} / {spec['completeness']}\n"
            f"- 题号：{spec['problem']}\n- 模型：{'、'.join(spec['models']) or '不适用'}\n\n"
            f"## 人工核验摘要\n\n{json.dumps(spec['content'], ensure_ascii=False, indent=2)}\n\n"
            "> 扫描全文不公开；短证据见 evidence.jsonl。\n", encoding="utf-8")
        (folder / "review_record.md").write_text("# Review record\n\n" +
            f"- logical_document_id: `{did}`\n" + "".join(f"- {x}: verified\n" for x in
            ["标题和身份", "文章边界", "摘要或开篇", "核心模型或评议对象", "关键公式", "关键表格或图", "最终结论或缺失范围", "重要数字", "题面和方案关系"]) +
            f"- completeness: {spec['completeness']}\n- manually_verified: true\n", encoding="utf-8")
        (folder / "extracted_text.md").write_text("# 本地提取缓存\n\n扫描件未执行全篇中文OCR；短证据见 evidence.jsonl。\n", encoding="utf-8")

    write_jsonl(DOCS / f"logical_documents_{year}.jsonl", docs)
    write_jsonl(DOCS / "logical_documents.jsonl", sorted(all_docs + docs, key=lambda d: (int(d.get("year", 0)), d["logical_document_id"])))
    write_jsonl(DOCS / f"page_segments_{year}.jsonl", segments)
    write_jsonl(DOCS / f"representations_{year}.jsonl", reps)
    compact = ["logical_document_id", "title", "document_role", "document_subtype", "problem_code", "problem_id", "solution_lineage_id", "parse_status", "evidence_status", "segmentation_status", "completeness_status", "page_count"]
    with (DOCS / f"{year}_logical_document_compact.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=compact, lineterminator="\n"); writer.writeheader()
        writer.writerows([{k: d.get(k) for k in compact} for d in docs])
    absorptions = [r for r in read_jsonl(DOCS / "carrier_absorptions.jsonl") if int(r.get("year", 0)) != year]
    for row in carrier_rows:
        absorptions.append({"year": year, "carrier_document_id": row["carrier_document_id"],
            "logical_document_ids": [d["logical_document_id"] for d in docs if row["carrier_document_id"] in d["carrier_document_ids"]],
            "reason": "manual carrier-to-logical mapping", "manually_verified": True, "manual_overrides": True})
    write_jsonl(DOCS / "carrier_absorptions.jsonl", absorptions)
    write_jsonl(DOCS / f"carrier_absorptions_{year}.jsonl", [r for r in absorptions if int(r.get("year", 0)) == year])
    write_jsonl(DOCS / f"article_boundaries_{year}.jsonl", boundaries)
    write_jsonl(DOCS / f"orphan_segments_{year}.jsonl", [])

    relations = [r for r in read_jsonl(REL / "document_relations.jsonl") if int(r.get("year", 0)) != year]
    for spec in specs:
        relations.append({"relation_id": stable("relation_", spec["carrier_id"], spec["id"], "contains"),
            "source_document_id": spec["carrier_id"], "target_document_id": spec["id"], "relation_type": "contains",
            "evidence": "verified title, authors and page region", "confidence": .98,
            "verified_by": "manual_visual_review", "status": "verified", "year": year, "manual_overrides": True})
        if spec["role"] == "award_paper":
            relations.append({"relation_id": stable("relation_", spec["id"], spec["problem_id"], "answers_problem"),
                "source_document_id": spec["id"], "target_document_id": spec["problem_id"], "relation_type": "answers_problem",
                "evidence": "variables, constraints and requested output correspond to statement", "confidence": .98,
                "verified_by": "manual_visual_review", "status": "verified", "year": year, "manual_overrides": True})
    relations.extend(extra_relations)
    write_jsonl(REL / "document_relations.jsonl", relations)
    write_jsonl(REL / f"document_relations_{year}.jsonl", [r for r in relations if int(r.get("year", 0)) == year])
    lineages = [l for l in read_jsonl(REL / "solution_lineages.jsonl") if int(l.get("contest_year", 0) or 0) != year]
    for spec in [x for x in specs if x["role"] == "award_paper"]:
        lineages.append({"lineage_id": spec["lineage"], "contest_year": year, "problem_code": spec["problem"],
            "primary_paper": spec["id"], "paper_representations": [next(r["representation_id"] for r in reps if r["logical_document_id"] == spec["id"])],
            "commentaries": [x["id"] for x in specs if x["role"] == "expert_commentary" and x["problem"] == spec["problem"]],
            "problem_statement": [x["id"] for x in specs if x["role"] == "problem_statement" and x["problem"] == spec["problem"]],
            "validation_summaries": [], "partial_segments": spec.get("partial_segments", []), "unresolved_members": spec.get("unresolved_members", []),
            "canonical_solution_description": ", ".join(spec["models"]), "status": "verified" if spec["completeness"] == "complete" else "partial",
            "manual_overrides": True})
    write_jsonl(REL / "solution_lineages.jsonl", lineages)
    write_jsonl(REL / f"solution_lineages_{year}.jsonl", [l for l in lineages if int(l.get("contest_year", 0) or 0) == year])
    feedback = [r for r in read_jsonl(CAT / "reviewer_feedback_catalog.jsonl") if int(r.get("year", 0) or 0) != year] + feedback_rows
    write_jsonl(CAT / "reviewer_feedback_catalog.jsonl", feedback)
    write_jsonl(CAT / f"reviewer_feedback_catalog_{year}.jsonl", feedback_rows)
    if visual_rows:
        with (CAT / f"visualization_catalog_{year}.csv").open("w", encoding="utf-8-sig", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(visual_rows[0]), lineterminator="\n"); writer.writeheader(); writer.writerows(visual_rows)
    else:
        (CAT / f"visualization_catalog_{year}.csv").write_text("logical_document_id,figure_or_table_id,page,bbox,chart_type,purpose,supports_question,supports_claim,effective,reusable_pattern,evidence_status,representation_id\n", encoding="utf-8-sig")
    write_jsonl(QUALITY / f"unresolved/{year}_manual_review_queue.jsonl", [])
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"{year}_report.md").write_text(report_text, encoding="utf-8")
    (REPORTS / f"{year}_data_quality.md").write_text(quality_text, encoding="utf-8")
    for did in old_auto - reviewed:
        folder = CARDS / did
        if folder.exists():
            for name in ["document_card.md", "metadata.json", "extracted_text.md", "page_map.json", "evidence.jsonl", "review_record.md"]:
                path = folder / name
                if path.exists(): path.unlink()
            if not any(folder.iterdir()): folder.rmdir()
    return {"logical_documents": len(docs), "representations": len(reps), "carriers": len(carrier_rows)}
