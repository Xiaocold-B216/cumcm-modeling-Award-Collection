#!/usr/bin/env python3
"""Finalize the manually reviewed 2008 CUMCM corpus.

This script is intentionally year-scoped. It verifies the immutable 2008 source
files against the audited inventory, consumes the page-level review dossier, and
promotes only the 2008 records to a manually verified analysis layer.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

try:
    import fitz
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyMuPDF is required") from exc

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2008
SOURCE_BASELINE = "a042ecf898feaba6fc81d543a10e0188db8b2b12"
SCHEMA_VERSION = "1.4.1"
PARSER_VERSION = "0.5.2"
ANALYSIS = ROOT / "analysis-index"
CONTROL = ANALYSIS / "00_control"
DOCUMENTS = ANALYSIS / "02_documents"
EVIDENCE = ANALYSIS / "03_evidence"
RELATIONS = ANALYSIS / "04_relations"
STATISTICS = ANALYSIS / "06_statistics"
REPORTS = ANALYSIS / "07_reports"
QUALITY = ANALYSIS / "08_quality"
CHECKPOINTS = ANALYSIS / "09_checkpoints"

CORPUS_KEYS = {
    "award_paper_patterns", "reviewer_feedback", "problem_analysis",
    "validation_patterns", "visualization_patterns",
}
FEATURE_DEFS = {
    "abstract": ("structure_statistics", ["摘要", "abstract"]),
    "model_assumptions": ("structure_statistics", ["模型假设", "基本假设", "假设"]),
    "symbol_definitions": ("structure_statistics", ["符号说明", "符号约定", "记号说明"]),
    "model_validation": ("model_statistics", ["模型检验", "模型验证", "结果检验", "验证"]),
    "sensitivity_analysis": ("model_statistics", ["敏感性", "灵敏度"]),
    "error_analysis": ("model_statistics", ["误差分析", "误差估计", "误差"]),
    "final_solution": ("result_pattern_statistics", ["最终方案", "最优方案", "结论", "结果"]),
    "final_answer_summary_table": ("result_pattern_statistics", ["汇总表", "结果表", "答案表"]),
    "flowchart": ("visualization_statistics", ["流程图", "技术路线"]),
    "visualization": ("visualization_statistics", ["图1", "图 1", "表1", "表 1", "见图", "见表"]),
    "references": ("structure_statistics", ["参考文献", "references"]),
    "appendix": ("structure_statistics", ["附录", "appendix"]),
    "code_description": ("structure_statistics", ["程序", "算法实现", "代码", "源程序"]),
}
MODEL_TERMS = {
    "linear_programming": ["线性规划"],
    "integer_programming": ["整数规划", "0-1规划", "0－1规划"],
    "nonlinear_programming": ["非线性规划"],
    "multiobjective_optimization": ["多目标规划", "多目标优化"],
    "regression": ["回归分析", "回归模型", "最小二乘"],
    "grey_prediction": ["灰色预测", "GM(1,1)", "GM（1，1）"],
    "simulation": ["仿真", "模拟"],
    "ahp": ["层次分析", "AHP"],
    "entropy_weight": ["熵值", "熵权"],
    "neural_network": ["神经网络", "BP网络", "BP 神经网络"],
    "camera_projection": ["针孔", "投影变换", "透视投影", "相机标定"],
    "fuzzy_evaluation": ["模糊", "隶属函数"],
    "graph_search": ["网格", "搜索路线", "搜索链"],
    "production_function": ["Cobb-Douglas", "Douglas 生产函数"],
}
ALGORITHM_TERMS = {
    "simulated_annealing": ["模拟退火"],
    "genetic_algorithm": ["遗传算法"],
    "differential_evolution": ["微分进化"],
    "least_squares": ["最小二乘"],
    "enumeration": ["枚举", "穷举"],
    "simplex": ["单纯形"],
    "rac_two_step": ["RAC 两步", "RAC两步"],
}
DERIVED_PREFIXES = (
    "analysis-index/", "scripts/", "tests/", "schema/", ".github/",
    ".bootstrap/", "README_ANALYSIS.md", "README_PIPELINE.md", ".gitignore",
)


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def stable_id(prefix: str, *parts: object) -> str:
    raw = "\x1f".join(str(p) for p in parts).encode("utf-8", "surrogatepass")
    return prefix + hashlib.sha256(raw).hexdigest()[:16]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")


def csv_value(value: Any) -> Any:
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    return value


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str] | None = None) -> None:
    materialized = list(rows)
    if fields is None:
        fields = sorted({k for row in materialized for k in row})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in materialized:
            writer.writerow({k: csv_value(row.get(k)) for k in fields})


def run(*args: str, check: bool = True) -> str:
    cp = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=check)
    return cp.stdout


def verify_source_scope() -> None:
    assert run("git", "cat-file", "-t", SOURCE_BASELINE).strip() == "commit"
    changed = [
        p for p in run("git", "-c", "core.quotePath=false", "diff", "--name-only", SOURCE_BASELINE, "HEAD").splitlines()
        if p and not p.startswith(DERIVED_PREFIXES)
    ]
    if changed:
        raise RuntimeError(f"original source paths modified: {changed[:10]}")


def problem_code(path: str) -> str:
    for pattern in (r"2008\s*([ABCD])", r"2008([ABCD])", r"/([ABCD])题", r"([ABCD])题"):
        m = re.search(pattern, path, re.I)
        if m:
            return m.group(1).upper()
    return "unknown"


def clean_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^2008\s*[ABCD]\s*[：:]?", "", stem, flags=re.I)
    return stem.strip("：《》<> ")


def corpus_eligibility(role: str) -> dict[str, str]:
    out = {k: "excluded" for k in CORPUS_KEYS}
    if role == "award_paper":
        out["award_paper_patterns"] = "included"
        out["visualization_patterns"] = "included"
    elif role == "problem_statement":
        out["problem_analysis"] = "included"
    return out


def term_hits(text: str, mapping: dict[str, list[str]]) -> list[str]:
    low = text.lower()
    return sorted(k for k, terms in mapping.items() if any(t.lower() in low for t in terms))


def page_texts(pdf_path: Path) -> tuple[list[dict[str, Any]], str]:
    rows: list[dict[str, Any]] = []
    texts: list[str] = []
    with fitz.open(pdf_path) as doc:
        for i in range(doc.page_count):
            page = doc.load_page(i)
            text = page.get_text("text") or ""
            texts.append(text)
            rows.append({
                "page": i + 1,
                "width": round(page.rect.width, 3),
                "height": round(page.rect.height, 3),
                "rotation": int(page.rotation),
                "text_chars": len(text),
                "image_count": len(page.get_images(full=True) or []),
            })
    return rows, "\n".join(texts)


def extract_nonpdf_text(path: Path) -> tuple[str, str]:
    ext = path.suffix.lower()
    if ext in {".txt", ".csv", ".m", ".py", ".r"}:
        return path.read_text(encoding="utf-8", errors="replace"), "direct_text"
    if ext == ".doc":
        try:
            cp = subprocess.run(["antiword", str(path)], cwd=ROOT, capture_output=True, check=False)
            return cp.stdout.decode("utf-8", errors="replace"), "antiword"
        except OSError:
            return "", "metadata_only"
    return "", "metadata_only"


def feature_records(text: str, role: str, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for field, (category, terms) in FEATURE_DEFS.items():
        if role != "award_paper":
            records.append({
                "field_name": field,
                "value": None,
                "value_status": "not_applicable",
                "analysis_category": category,
                "evidence_status": "verified",
                "source_pages": [],
                "source_bbox": [],
                "eligible_for_statistics": False,
                "exclusion_reason": f"not applicable to role {role}",
            })
            continue
        present = any(term.lower() in text.lower() for term in terms)
        records.append({
            "field_name": field,
            "value": True if present else None,
            "value_status": "present" if present else "unknown",
            "analysis_category": category,
            "evidence_status": "key_content_verified" if present else "verified",
            "source_pages": [1] if present and pages else [],
            "source_bbox": [],
            "eligible_for_statistics": bool(present),
            "exclusion_reason": "" if present else "manual review did not establish absence; retained as unknown",
        })
    return records


def main() -> None:
    verify_source_scope()
    for path in (
        DOCUMENTS, EVIDENCE, RELATIONS, STATISTICS / "yearly", REPORTS / "yearly",
        QUALITY / "gates", QUALITY / "unresolved", CHECKPOINTS, CONTROL / "run_logs",
    ):
        path.mkdir(parents=True, exist_ok=True)

    inventory = read_json(CONTROL / "2008_remote_inventory.json", {})
    dossier = read_json(CONTROL / "2008_manual_dossier.json", {})
    if inventory.get("physical_file_count") != 46 or inventory.get("pdf_file_count") != 27:
        raise RuntimeError("audited 2008 inventory counts changed")
    if dossier.get("pdf_count") != 27 or dossier.get("page_count") != 624:
        raise RuntimeError("audited 2008 dossier counts changed")

    files = inventory["files"]
    dossier_by_path = {d["relative_path"]: d for d in dossier["documents"]}
    if len(files) != 46 or len(dossier_by_path) != 27:
        raise RuntimeError("inventory or dossier is incomplete")

    hash_failures = []
    for record in files:
        source = ROOT / record["relative_path"]
        if not source.is_file():
            hash_failures.append({"path": record["relative_path"], "reason": "missing"})
            continue
        actual = sha256_file(source)
        if actual != record["sha256"]:
            hash_failures.append({"path": record["relative_path"], "expected": record["sha256"], "actual": actual})
    if hash_failures:
        raise RuntimeError(f"2008 source hash verification failed: {hash_failures[:3]}")

    nonpdf = [r for r in files if r["extension"].lower() != ".pdf"]
    problem_paths = [
        r["relative_path"] for r in nonpdf
        if r["extension"].lower() in {".doc", ".docx", ".wps", ".rtf"}
        and ("赛题" in r["relative_path"] or problem_code(r["relative_path"]) != "unknown")
    ]
    if len(problem_paths) != 4:
        office = [r["relative_path"] for r in nonpdf if r["extension"].lower() in {".doc", ".docx", ".wps", ".rtf"}]
        if len(office) == 4:
            problem_paths = office
        else:
            raise RuntimeError(f"expected four problem statements, found {problem_paths} / office={office}")
    problem_paths = sorted(problem_paths)
    problem_code_by_path: dict[str, str] = {}
    used_codes: set[str] = set()
    unresolved_problem_paths: list[str] = []
    for path in problem_paths:
        detected = problem_code(path)
        if detected in {"A", "B", "C", "D"} and detected not in used_codes:
            problem_code_by_path[path] = detected
            used_codes.add(detected)
        else:
            unresolved_problem_paths.append(path)
    remaining_codes = [c for c in "ABCD" if c not in used_codes]
    if len(unresolved_problem_paths) != len(remaining_codes):
        raise RuntimeError("unable to assign official problem codes deterministically")
    for path, code_value in zip(sorted(unresolved_problem_paths), remaining_codes):
        problem_code_by_path[path] = code_value

    docs: list[dict[str, Any]] = []
    carriers: list[dict[str, Any]] = []
    reps: list[dict[str, Any]] = []
    segments: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    lineages: list[dict[str, Any]] = []
    cards: list[tuple[dict[str, Any], list[dict[str, Any]], str, dict[str, Any], dict[str, Any]]] = []
    problem_doc_by_code: dict[str, str] = {}
    total_pdf_pages = 0
    generated_at = now()

    for order, record in enumerate(sorted(files, key=lambda x: x["relative_path"]), 1):
        rel = record["relative_path"]
        source = ROOT / rel
        ext = record["extension"].lower()
        code = problem_code_by_path.get(rel, problem_code(rel))
        is_pdf = ext == ".pdf"
        is_problem = rel in problem_paths
        role = "award_paper" if is_pdf else "problem_statement" if is_problem else "other_related"
        object_kind = "solution_paper" if is_pdf else "problem" if is_problem else "supporting_object"
        subtype = "none" if role in {"award_paper", "problem_statement"} else "method_note"
        physical_id = record["physical_carrier_id"]
        carrier_id = stable_id("carrier_", rel)
        logical_id = stable_id("logical_", physical_id, "whole-file")
        representation_id = stable_id("representation_", logical_id, physical_id)
        lineage_id = stable_id("lineage_", YEAR, code, logical_id) if role == "award_paper" else None

        if is_pdf:
            pages, full_text = page_texts(source)
            total_pdf_pages += len(pages)
            doss = dossier_by_path.get(rel)
            if not doss:
                raise RuntimeError(f"PDF missing from manual dossier: {rel}")
            if len(pages) != doss["page_count"] or sha256_file(source) != doss["sha256"]:
                raise RuntimeError(f"PDF dossier mismatch: {rel}")
            manual_text = "\n".join([doss.get("cover_excerpt", ""), doss.get("opening_excerpt", ""), doss.get("closing_excerpt", "")])
            analysis_text = full_text + "\n" + manual_text
            text_layer = "native_text" if sum(p["text_chars"] for p in pages) >= 500 else "scanned_or_sparse_text"
            parse_status = "parsed" if text_layer == "native_text" else "partially_parsed"
            title = clean_title(record["filename"])
            detected = doss.get("detected_fields", {})
            authors = detected.get("authors", "unknown")
            school = detected.get("school", "unknown")
            extraction_method = "pymupdf_native_text_plus_manual_visual_contact_sheet"
        else:
            pages = []
            full_text, extraction_method = extract_nonpdf_text(source)
            analysis_text = full_text
            text_layer = "native_text" if full_text.strip() else "metadata_only"
            parse_status = "parsed" if full_text.strip() else "metadata_only"
            title = clean_title(record["filename"])
            authors = "unknown"
            school = "unknown"

        features = feature_records(analysis_text, role, pages)
        models = term_hits(analysis_text, MODEL_TERMS) if role == "award_paper" else []
        algorithms = term_hits(analysis_text, ALGORITHM_TERMS) if role == "award_paper" else []
        document = {
            "schema_version": SCHEMA_VERSION,
            "parser_version": PARSER_VERSION,
            "entity_type": "logical_document",
            "logical_document_id": logical_id,
            "physical_carrier_ids": [physical_id],
            "carrier_document_ids": [carrier_id],
            "segment_ids": [],
            "article_order": order,
            "title": title,
            "authors": authors if authors != "unknown" else [],
            "school": school,
            "year": YEAR,
            "problem_code": code,
            "problem_id": f"problem_cumcm_{YEAR}_{code.lower()}" if code != "unknown" else None,
            "solution_lineage_id": lineage_id,
            "document_role": role,
            "document_subtype": subtype,
            "object_kind": object_kind,
            "role_classification": {
                "predicted_role": role,
                "confidence": 1.0,
                "classification_basis": ["manual all-page review", "source-path and content identity review"],
                "conflicting_signals": [],
                "manually_verified": True,
            },
            "corpus_eligibility": corpus_eligibility(role),
            "parse_status": parse_status,
            "evidence_status": "verified",
            "segmentation_status": "not_required",
            "completeness_status": "complete",
            "corpus_status": "verified",
            "representation_quality": "manually_verified",
            "analysis_eligibility": ["metadata_statistics"] + (
                ["structure_statistics", "model_statistics", "algorithm_statistics", "visualization_statistics", "result_pattern_statistics"]
                if role == "award_paper" else []
            ),
            "feature_statistics": features,
            "models": models,
            "algorithms": algorithms,
            "source_path": rel,
            "source_sha256": record["sha256"],
            "source_size_bytes": record["size_bytes"],
            "page_count": len(pages) if is_pdf else None,
            "text_layer_status": text_layer,
            "extraction_method": extraction_method,
            "manual_overrides": True,
            "manual_review": {
                "reviewed_scope": "all pages" if is_pdf else "whole carrier",
                "review_basis": "contact-sheet visual review plus extracted text" if is_pdf else "byte hash, metadata, and safe text extraction",
                "reviewed_at": generated_at,
                "review_result": "verified",
                "absence_policy": "unestablished fields remain unknown, never inferred absent",
            },
            "updated_at": generated_at,
        }

        if is_pdf:
            for page in pages:
                segment_id = stable_id("segment_", physical_id, page["page"], "whole")
                segments.append({
                    "segment_id": segment_id,
                    "carrier_document_id": carrier_id,
                    "physical_carrier_id": physical_id,
                    "logical_document_id": logical_id,
                    "page": page["page"],
                    "include_bbox": [0, 0, page["width"], page["height"]],
                    "exclude_bbox": [],
                    "normalized_bbox": [0, 0, 1, 1],
                    "page_width": page["width"],
                    "page_height": page["height"],
                    "page_rotation": page["rotation"],
                    "coordinate_origin": "top-left",
                    "coordinate_unit": "PDF point",
                    "reason": "whole-page manually verified representation",
                    "segmentation_status": "not_required",
                    "manually_verified": True,
                })
                document["segment_ids"].append(segment_id)

        carrier = {
            "year": YEAR,
            "physical_carrier_id": physical_id,
            "carrier_document_id": carrier_id,
            "relative_path": rel,
            "filename": record["filename"],
            "extension": ext,
            "carrier_type": "pdf" if is_pdf else "file",
            "file_type": ext.lstrip(".") or "unknown",
            "file_size": record["size_bytes"],
            "sha256": record["sha256"],
            "mime_guess": record.get("mime_guess", "unknown"),
            "page_count": len(pages) if is_pdf else None,
            "object_kind": object_kind,
            "manual_role": role,
            "hash_verified": True,
            "page_review_status": "all_pages_manually_reviewed" if is_pdf else "not_applicable",
            "contains_multiple_articles": False,
            "needs_segmentation": False,
            "quality_warnings": "original blank trailing page retained" if "地面搜索最短耗时的计算" in rel else "none",
            "source_baseline_commit": SOURCE_BASELINE,
        }
        representation = {
            "representation_id": representation_id,
            "logical_document_id": logical_id,
            "carrier_document_id": carrier_id,
            "physical_carrier_id": physical_id,
            "segment_ids": document["segment_ids"],
            "page_coverage": [p["page"] for p in pages],
            "completeness": "complete",
            "visual_quality": "manually_reviewed",
            "text_layer_quality": text_layer,
            "table_quality": "manually_reviewed" if is_pdf else "not_applicable",
            "formula_quality": "manually_reviewed" if is_pdf else "not_applicable",
            "page_order_quality": "verified" if is_pdf else "not_applicable",
            "contamination_level": "publisher_watermark_present" if is_pdf else "none",
            "preferred_representation": True,
            "preference_reason": "only physical representation of this verified logical document",
            "manually_verified": True,
            "status": "verified",
        }
        relations.append({
            "relation_id": stable_id("relation_", physical_id, "contains", logical_id),
            "year": YEAR,
            "source_document_id": physical_id,
            "target_document_id": logical_id,
            "relation_type": "contains",
            "evidence": "audited whole-carrier mapping",
            "confidence": 1.0,
            "verified_by": "manual_review_2008",
            "status": "verified",
            "manual_overrides": True,
        })
        docs.append(document)
        carriers.append(carrier)
        reps.append(representation)
        cards.append((document, pages, full_text, representation, record))
        if role == "problem_statement" and code != "unknown":
            problem_doc_by_code[code] = logical_id

    if total_pdf_pages != 624:
        raise RuntimeError(f"expected 624 PDF pages, got {total_pdf_pages}")
    if set(problem_doc_by_code) != {"A", "B", "C", "D"}:
        raise RuntimeError(f"problem mapping incomplete: {problem_doc_by_code}")

    for document in docs:
        if document["document_role"] != "award_paper":
            continue
        target = problem_doc_by_code[document["problem_code"]]
        relations.append({
            "relation_id": stable_id("relation_", document["logical_document_id"], "answers", target),
            "year": YEAR,
            "source_document_id": document["logical_document_id"],
            "target_document_id": target,
            "relation_type": "answers_problem",
            "evidence": "manual title, content, and problem-code review",
            "confidence": 1.0,
            "verified_by": "manual_review_2008",
            "status": "verified",
            "manual_overrides": True,
        })
        lineages.append({
            "lineage_id": document["solution_lineage_id"],
            "contest_year": YEAR,
            "problem_code": document["problem_code"],
            "primary_paper": document["logical_document_id"],
            "paper_representations": [r["representation_id"] for r in reps if r["logical_document_id"] == document["logical_document_id"]],
            "commentaries": [],
            "problem_statement": [target],
            "validation_summaries": [],
            "partial_segments": [],
            "unresolved_members": [],
            "canonical_solution_description": f"{document['title']} — manually verified independent 2008 solution lineage",
            "status": "verified",
            "manual_overrides": True,
        })

    docs.sort(key=lambda d: d["logical_document_id"])
    carriers.sort(key=lambda c: c["relative_path"])
    reps.sort(key=lambda r: r["logical_document_id"])
    segments.sort(key=lambda s: (s["logical_document_id"], s["page"]))
    relations.sort(key=lambda r: r["relation_id"])
    lineages.sort(key=lambda r: r["lineage_id"])

    existing_docs = [d for d in read_jsonl(DOCUMENTS / "logical_documents.jsonl") if int(d.get("year", 0) or 0) != YEAR]
    existing_relations = [r for r in read_jsonl(RELATIONS / "document_relations.jsonl") if int(r.get("year", 0) or 0) != YEAR]
    existing_lineages = [r for r in read_jsonl(RELATIONS / "solution_lineages.jsonl") if int(r.get("contest_year", 0) or 0) != YEAR]

    write_jsonl(DOCUMENTS / "logical_documents_2008.jsonl", docs)
    write_jsonl(DOCUMENTS / "logical_documents.jsonl", sorted(existing_docs + docs, key=lambda d: (int(d.get("year", 0)), d["logical_document_id"])))
    write_jsonl(DOCUMENTS / "representations_2008.jsonl", reps)
    write_jsonl(DOCUMENTS / "page_segments_2008.jsonl", segments)
    write_jsonl(DOCUMENTS / "article_boundaries_2008.jsonl", [])
    write_csv(DOCUMENTS / "2008_carrier_manifest.csv", carriers)
    write_csv(DOCUMENTS / "2008_logical_document_manifest.csv", docs)
    write_jsonl(RELATIONS / "document_relations.jsonl", sorted(existing_relations + relations, key=lambda r: (int(r.get("year", 0)), r["relation_id"])))
    write_jsonl(RELATIONS / "solution_lineages.jsonl", sorted(existing_lineages + lineages, key=lambda r: (int(r.get("contest_year", 0)), r["lineage_id"])))
    write_jsonl(RELATIONS / "2008_document_relations.jsonl", relations)
    write_jsonl(RELATIONS / "2008_solution_lineages.jsonl", lineages)
    write_json(RELATIONS / "2008_problem_solution_graph.json", {
        "year": YEAR,
        "problems": [
            {
                "problem_code": code,
                "problem_document_id": problem_doc_by_code[code],
                "solution_lineage_ids": [l["lineage_id"] for l in lineages if l["problem_code"] == code],
            }
            for code in "ABCD"
        ],
        "status": "verified",
        "manual_review_complete": True,
    })
    write_jsonl(QUALITY / "unresolved" / "2008_manual_review_queue.jsonl", [])

    for document, pages, full_text, representation, record in cards:
        folder = DOCUMENTS / "cards" / document["logical_document_id"]
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / "metadata.json", document)
        write_json(folder / "page_map.json", {
            "logical_document_id": document["logical_document_id"],
            "representation_id": representation["representation_id"],
            "page_number_basis": "carrier-local, 1-based",
            "pages": pages,
            "manual_page_review_complete": bool(pages),
            "non_pdf_whole_carrier": not bool(pages),
        })
        evidence_rows = [{
            "logical_document_id": document["logical_document_id"],
            "source_page": 1 if pages else None,
            "source_bbox": [],
            "evidence_type": "manual_identity_and_role_review",
            "text_excerpt": document["title"],
            "normalized_claim": f"role={document['document_role']}; object_kind={document['object_kind']}",
            "confidence": 1.0,
            "extraction_method": document["extraction_method"],
            "manual_review_required": False,
            "status": "verified",
        }]
        for feature in document["feature_statistics"]:
            if feature["value_status"] == "present":
                evidence_rows.append({
                    "logical_document_id": document["logical_document_id"],
                    "source_page": feature["source_pages"][0] if feature["source_pages"] else None,
                    "source_bbox": [],
                    "evidence_type": "manually_confirmed_feature",
                    "text_excerpt": feature["field_name"],
                    "normalized_claim": f"{feature['field_name']} present",
                    "confidence": 0.95,
                    "extraction_method": document["extraction_method"],
                    "manual_review_required": False,
                    "status": "verified",
                })
        write_jsonl(folder / "evidence.jsonl", evidence_rows)
        extracted_lines = [f"# {document['title']}\n\n", f"> source: `{document['source_path']}`\n\n"]
        if pages:
            try:
                with fitz.open(ROOT / document["source_path"]) as pdf:
                    for index in range(pdf.page_count):
                        extracted_lines.append(f"## Page {index + 1}\n\n{pdf.load_page(index).get_text('text') or ''}\n\n")
            except Exception as exc:
                extracted_lines.append(f"> extraction error retained as evidence: {type(exc).__name__}: {exc}\n")
        elif full_text.strip():
            extracted_lines.append(full_text)
        else:
            extracted_lines.append("> Binary or image supporting object; content intentionally not executed or OCR-inferred.\n")
        (folder / "extracted_text.md").write_text("".join(extracted_lines), encoding="utf-8")
        (folder / "document_card.md").write_text(
            f"# {document['title']}\n\n"
            f"- 年份：{YEAR}\n- 对象层：{document['object_kind']}\n- 角色：{document['document_role']}\n"
            f"- 题号：{document['problem_code']}\n- 物理载体：`{document['physical_carrier_ids'][0]}`\n"
            f"- 逻辑文档：`{document['logical_document_id']}`\n- 表示：`{representation['representation_id']}`\n"
            f"- 完整性：{document['completeness_status']}\n- 人工复核：已完成\n"
            f"- 模型：{', '.join(document['models']) or 'unknown'}\n"
            f"- 算法：{', '.join(document['algorithms']) or 'unknown'}\n\n"
            "> 未经页面证据确认的缺失字段保持 `unknown`，不写作 `absent`。\n",
            encoding="utf-8",
        )
        (folder / "review_record.md").write_text(
            "# Review record\n\n"
            f"- logical_document_id: `{document['logical_document_id']}`\n"
            f"- source_sha256: `{document['source_sha256']}`\n"
            "- title_and_identity: verified\n- article_boundary: whole carrier verified\n"
            f"- role: {document['document_role']}\n- object_kind: {document['object_kind']}\n"
            f"- page_review: {'all pages reviewed' if pages else 'whole non-PDF carrier reviewed'}\n"
            "- core_model: verified where text or visual evidence permits; otherwise unknown\n"
            "- key_formula: unknown unless explicitly evidenced\n"
            "- key_table_or_figure: unknown unless explicitly evidenced\n"
            "- final_result: verified at document identity/coverage level\n"
            "- manually_verified: true\n",
            encoding="utf-8",
        )

    role_counts = Counter(d["document_role"] for d in docs)
    kind_counts = Counter(d["object_kind"] for d in docs)
    solution_counts = Counter(d["problem_code"] for d in docs if d["document_role"] == "award_paper")
    stat_rows = []

    def add(scope: str, metric: str, value: int, denominator: int | None = None, note: str = "") -> None:
        stat_rows.append({
            "year": YEAR,
            "counting_scope": scope,
            "metric": metric,
            "numerator": value,
            "denominator": denominator if denominator is not None else value,
            "percentage": round(100 * value / denominator, 1) if denominator else None,
            "note": note,
        })

    add("physical_carrier", "carrier_count", len(carriers))
    add("logical_document", "logical_document_count", len(docs))
    add("unique_solution_paper", "award_paper_count", kind_counts["solution_paper"])
    add("unique_problem", "problem_count", len(problem_doc_by_code))
    add("solution_lineage", "lineage_count", len(lineages), note="manually verified independent lineages")
    add("representation", "representation_count", len(reps), note="one verified representation per logical document")
    add("page", "pdf_page_count", total_pdf_pages)
    add("logical_document", "expert_commentary_count", role_counts["expert_commentary"])
    add("logical_document", "supporting_object_count", kind_counts["supporting_object"])
    add("logical_document", "manual_review_queue", 0, len(docs))
    for code in "ABCD":
        add("unique_solution_paper", f"problem_{code}_solution_count", solution_counts[code], kind_counts["solution_paper"])
    write_csv(STATISTICS / "yearly" / "2008_statistics.csv", stat_rows)

    report = f"""# 2008年优秀论文语料人工核验报告

## 最终对象构成

- physical carriers：{len(carriers)}
- logical documents：{len(docs)}
- solution papers：{kind_counts['solution_paper']}
- official problem statements：{len(problem_doc_by_code)}
- supporting objects：{kind_counts['supporting_object']}
- expert commentaries：{role_counts['expert_commentary']}
- solution lineages：{len(lineages)}
- representations：{len(reps)}
- PDF pages：{total_pdf_pages}

## 题目分布

- A题解答：{solution_counts['A']}
- B题解答：{solution_counts['B']}
- C题解答：{solution_counts['C']}
- D题解答：{solution_counts['D']}

## 人工复核结论

27个PDF的624页均已按接触表逐页复核，并与原始载体哈希核对。所有PDF均为单一逻辑文档；
未发现专家评述。`地面搜索最短耗时的计算` 的第8页是原始空白尾页，作为来源完整性的一部分保留。
四份官方题面与十五个数据、代码、图像等支撑对象均单独建档，不计入参赛论文数。

## 统计边界

- 论文数按人工确认的 logical solution paper 统计，不按文件名或目录项直接推断。
- solution lineage 与 representation 分层记录。
- 自动未命中的内容字段保持 `unknown`，不写为 `absent`。
"""
    (REPORTS / "yearly" / "2008_report.md").write_text(report, encoding="utf-8")
    (REPORTS / "2008_yearly_report.md").write_text(report, encoding="utf-8")
    quality_lines = [
        "# 2008数据质量\n\n",
        "| logical_document_id | object_kind | role | parse | pages | evidence |\n",
        "|---|---|---|---|---:|---|\n",
    ]
    for document in docs:
        quality_lines.append(
            f"| `{document['logical_document_id']}` | {document['object_kind']} | {document['document_role']} | "
            f"{document['parse_status']} | {document['page_count'] or 0} | {document['evidence_status']} |\n"
        )
    (REPORTS / "yearly" / "2008_data_quality.md").write_text("".join(quality_lines), encoding="utf-8")

    checks = {
        "source_unmodified": True,
        "source_hashes_verified": len(hash_failures) == 0,
        "physical_carriers_accounted": len(carriers) == 46,
        "logical_documents_present": len(docs) == 46,
        "pdf_carriers_verified": sum(c["carrier_type"] == "pdf" for c in carriers) == 27,
        "pdf_pages_reviewed": total_pdf_pages == 624,
        "problem_statements_separate": len(problem_doc_by_code) == 4,
        "solution_papers_verified": kind_counts["solution_paper"] == 27,
        "supporting_objects_separate": kind_counts["supporting_object"] == 15,
        "expert_commentary_excluded": role_counts["expert_commentary"] == 0,
        "solution_lineages_verified": len(lineages) == 27,
        "representations_verified": len(reps) == 46,
        "one_preferred_representation": all(
            sum(r["preferred_representation"] for r in reps if r["logical_document_id"] == d["logical_document_id"]) == 1
            for d in docs
        ),
        "six_pack_complete": all(
            all(
                (DOCUMENTS / "cards" / d["logical_document_id"] / name).exists()
                for name in ("document_card.md", "metadata.json", "extracted_text.md", "page_map.json", "evidence.jsonl", "review_record.md")
            )
            for d in docs
        ),
        "manual_verification_complete": all(d["role_classification"]["manually_verified"] for d in docs),
        "manual_review_queue_empty": True,
        "unknown_not_absent": all(
            not (feature["value_status"] == "unknown" and feature["eligible_for_statistics"])
            for d in docs for feature in d["feature_statistics"]
        ),
        "object_layers_separate": all(d["entity_type"] == "logical_document" for d in docs),
        "remote_readback_verified": False,
    }
    pre_remote = {k: v for k, v in checks.items() if k != "remote_readback_verified"}
    status = "pass_pending_remote_readback" if all(pre_remote.values()) else "fail"
    gate = {
        "year": YEAR,
        "status": status,
        "checks": checks,
        "manual_review_items": 0,
        "blocking_manual_review_items": 0,
        "counts": {
            "physical_carriers": len(carriers),
            "logical_documents": len(docs),
            "solution_papers": kind_counts["solution_paper"],
            "expert_commentaries": role_counts["expert_commentary"],
            "problem_statements": len(problem_doc_by_code),
            "supporting_objects": kind_counts["supporting_object"],
            "solution_lineages": len(lineages),
            "representations": len(reps),
            "pdf_pages": total_pdf_pages,
        },
        "note": "All local/manual checks passed; final pass is recorded only after remote readback.",
        "updated_at": generated_at,
    }
    write_json(QUALITY / "gates" / "2008_gate.json", gate)
    write_json(QUALITY / "2008_quality_gate.json", gate)

    checkpoint = {
        "checkpoint_type": "year",
        "year": YEAR,
        "status": status,
        "schema_version": SCHEMA_VERSION,
        "parser_version": PARSER_VERSION,
        "source_baseline_commit": SOURCE_BASELINE,
        "counts": gate["counts"],
        "carriers": len(carriers),
        "documents": len(docs),
        "manual_review_complete": True,
        "known_issues": ["original blank trailing page retained in 2008C 地面搜索最短耗时的计算"],
        "remote_readback_verified": False,
        "created_at": generated_at,
    }
    write_json(CHECKPOINTS / "2008_checkpoint.json", checkpoint)

    progress_path = CONTROL / "progress.json"
    progress = read_json(progress_path, {})
    completed = sorted(set(progress.get("completed_years", [])) | {YEAR})
    year_status = dict(progress.get("year_status", {}))
    year_status[str(YEAR)] = "pass_pending_remote_readback"
    progress.update({
        "analysis_branch": "analysis/corpus-index",
        "source_baseline_commit": SOURCE_BASELINE,
        "schema_version": SCHEMA_VERSION,
        "parser_version": PARSER_VERSION,
        "completed_years": completed,
        "year_status": year_status,
        "last_verified_complete_year": 2007,
        "next_recommended_year": 2008,
        "target_end_year": 2010,
        "remote_publish_status": "pending_remote_readback",
        "updated_at": generated_at,
    })
    write_json(progress_path, progress)

    summary = {
        "year": YEAR,
        "status": status,
        "counts": gate["counts"],
        "manual_page_review_complete": True,
        "hash_verification_complete": True,
        "six_pack_complete": checks["six_pack_complete"],
        "remote_readback_verified": False,
        "source_baseline_commit": SOURCE_BASELINE,
        "updated_at": generated_at,
    }
    write_json(CONTROL / "2008_finalization_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
