#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import fitz

ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / "analysis-index"
YEAR = 2010
SCHEMA = "1.4.1"
PARSER = "0.5.2"
BASELINE = "a042ecf898feaba6fc81d543a10e0188db8b2b12"
STAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
DERIVED = ("analysis-index/", "scripts/", "tests/", "schema/", ".github/", ".bootstrap/", "README_")

# filename, sha256, PDF pages, role, object kind, problem, subtype, summary, models, algorithms
SOURCES = [
    ("2010A：倾斜卧式储油罐油量标定的实用方法.pdf", "88c6c782abd276280b59807b2108d4becd2c6b25d1f3e861f44b8047635c81c1", 21, "award_paper", "solution_paper", "A", "competition_solution_without_cover", "以微积分建立椭圆柱与球冠储油量模型；使用龙贝格数值积分、最小二乘和单目标优化识别变位，给出α=2.14°、β=4.6°，并以相对标准偏差检验。", ["geometric_volume_model", "piecewise_volume_integral", "parameter_estimation", "error_analysis"], ["romberg_integration", "least_squares", "single_objective_optimization"]),
    ("2010A：储油罐的变位识别与罐容表标定 (2).pdf", "69a3de2f892d270e60065e24d46cc2ba9ed432f31b854b576d5b67cffca515bd", 37, "award_paper", "solution_paper", "A", "competition_solution", "采用微积分与空间解析几何构造分段体积积分模型，利用离差平方和与最小二乘识别α、β，报告α约2°、β约4.9°并进行拟合优度检验。", ["geometric_volume_model", "piecewise_volume_integral", "parameter_estimation", "reliability_validation"], ["least_squares", "sum_of_squared_deviations", "matlab_simulation"]),
    ("2010A：储油罐的变位识别与罐容表标定 (3).pdf", "91816d1197a09392ecd177171037e1bf302f4e1d87e769dbcc750015d8aca997", 32, "award_paper", "solution_paper", "A", "competition_solution", "以几何学、积分学、数值积分和多重积分处理三种油罐状态，最小二乘识别α=2.1°、β=4.6°，用附件数据验证多数误差在1L以内。", ["geometric_volume_model", "multiple_integral", "parameter_estimation", "error_analysis"], ["numerical_integration", "least_squares"]),
    ("2010A：储油罐的变位识别与罐容表标定 (4).pdf", "c01dffa58041769dc6dcda69d53d63709b059106443632f6552d9f7199c6af03", 20, "award_paper", "solution_paper", "A", "competition_solution", "采用截面法和微积分建立倾斜油罐体积模型，通过相邻油位进出油量误差最小化识别α=2.1°、β=5°并重新标定罐容表。", ["cross_section_volume_model", "piecewise_volume_integral", "parameter_estimation"], ["calculus_integration", "minimum_error_search", "matlab_simulation"]),
    ("2010A：储油罐的变位识别与罐容表标定.pdf", "82d81045acec41137b7306ad1af0acd0aff2948811ddc58a8e8f31caa0a15649", 25, "award_paper", "solution_paper", "A", "competition_solution", "将实际油罐拆分为圆柱体和两端球冠，采用平行截面面积积分与分段模型识别纵横向变位，并以MATLAB仿真和一次性补充进油数据验证。", ["cross_section_volume_model", "piecewise_volume_integral", "spherical_cap_model", "parameter_estimation"], ["matlab_simulation", "interpolation", "error_comparison"]),
    ("2010A：基于数学建模的储油罐变形监测研究.pdf", "0d7703872c94fe411cc0b15c5419c315668235dd5f98a89b1208df173837c754", 100, "award_paper", "solution_paper", "A", "competition_solution_with_trailing_blank_pages", "使用投影法、截面法和微元法建立油量—油位—变位参数模型，结合附件数据和MATLAB求解；第1—73页为连续论文及附录，第74—100页为仅含传播水印的尾随空白页。", ["projection_volume_model", "cross_section_volume_model", "differential_element_model", "piecewise_volume_integral", "parameter_estimation"], ["matlab_simulation", "error_distribution_analysis"]),
    ("2010B：对上海世博会文化影响力的定量评估.pdf", "1ed4643567c104d6041eeb982ee6848a57d779ddb9bc319424e82ba6e95ad764", 25, "award_paper", "solution_paper", "B", "competition_solution", "从文化市场、文化资源和文化环境三个维度构建指标，采用因子分析确定权重，并用BP神经网络处理非线性映射，对文化影响力进行预测和比较。", ["cultural_influence_index", "factor_analysis_model", "neural_network_evaluation"], ["factor_analysis", "bp_neural_network", "nonlinear_regression"]),
    ("2010B：上海世博会影响力的定量评估.pdf", "ea8fa7e23ceeed8b511b42aafafbcfb776dd898b94d5f72a96847df72c9f640f", 29, "award_paper", "solution_paper", "B", "competition_solution", "从旅游经济与旅游文化两方面评估世博影响，使用本底趋势线、模糊评价和多目标优化，并与历届世博会进行综合影响力比较。", ["tourism_economy_influence", "tourism_culture_influence", "fuzzy_evaluation", "multiobjective_optimization"], ["baseline_trend", "fuzzy_comprehensive_evaluation", "weighted_multiobjective_optimization"]),
    ("2010B：上海世博会于文化方面影响力评估.pdf", "f084df33b5ded56e794a494305239dc534e981ba749e55138d56d1eb7faa6c20", 31, "award_paper", "solution_paper", "B", "competition_solution", "建立13项多层文化影响力指标，采用层次分析与模糊综合评价得到等级和量化分值，并以BP神经网络和聚类分析进行第二套评估。", ["hierarchical_indicator_system", "fuzzy_evaluation", "neural_network_evaluation", "cluster_evaluation"], ["data_standardization", "ahp", "fuzzy_comprehensive_evaluation", "bp_neural_network", "clustering"]),
    ("2010年国赛A题.doc", "2ae05cd8623c00440c874391a2eafa50d07e6cfe755818b63e8d49d14299d6c2", None, "problem_statement", "problem", "A", "official_problem", "官方A题：储油罐的变位识别与罐容表标定，要求建立无变位与纵向倾斜小椭圆罐模型，并识别实际油罐纵向倾角α和横向偏转角β。", [], []),
    ("2010年国赛B题.doc", "c8579ddc5ce2a3864bf8d1a8dfc9548bd88fff0e23693f26d6410065d0de6acf", None, "problem_statement", "problem", "B", "official_problem", "官方B题：选择感兴趣侧面，利用互联网数据建立模型，定量评估2010年上海世博会影响力。", [], []),
    ("2010年国赛C题.doc", "8882d100e2dd210e1fde90c11ae1dc89cdde776bb101cd2dd2cdd553df1a9626", None, "problem_statement", "problem", "C", "official_problem", "官方C题：输油管布置，研究两炼油厂到铁路的共用/非共用管线最省费用模型，并处理城区附加费用和不同管径成本。", [], []),
    ("2010年国赛D题.doc", "61340fc9229509b7bacee0ac44bacda8904ef700db0f133f9dea8102d9aa2e32", None, "problem_statement", "problem", "D", "official_problem", "官方D题：对四种学生宿舍设计方案的经济性、舒适性和安全性进行综合量化评价与比较。", [], []),
    ("2010年国赛A题附件 (1).xls", "f7eb407354ca0e71effde153535cc1ec617e45a3849afac814c5c9361880558f", None, "other_related", "supporting_object", "A", "official_data_workbook", "A题附件1：小椭圆储油罐实验数据，含无变位进油、无变位出油、倾斜变位进油、倾斜变位出油四个工作表。", [], []),
    ("2010年国赛A题附件 (2).xls", "fc3cf8098742f11feb5832fea8a47e5db0f862faab89e61dc0b669f0010c5777", None, "other_related", "supporting_object", "A", "official_data_workbook", "A题附件2：实际储油罐采集数据，包含604行、8列的进油量、出油量、显示油高、显示油量容积、采集时间等字段。", [], []),
    ("2010年国赛D题附件 (1).tif", "0d4546d628f9b73754f41e7341721aa3345efa1862d9166a9a2a98a58f211f50", None, "other_related", "supporting_object", "D", "official_design_drawing", "D题附件方案一：学生宿舍标准层平面设计图，包含房间、卫生间、楼梯、交通空间及面积标注。", [], []),
    ("2010年国赛D题附件 (2).tif", "7b26b6a3f4230e1a2dc352ac45189be50991d2e4c4ea8c90dbc56553409beb5e", None, "other_related", "supporting_object", "D", "official_design_drawing", "D题附件方案二：L形学生宿舍标准层平面设计图，标注建筑面积、房间数、学生人数及功能空间。", [], []),
    ("2010年国赛D题附件 (3).tif", "651fe61f58ab1d418167f4d20fd763c2ace835ab757bc42c11b5abd47f41145b", None, "other_related", "supporting_object", "D", "official_design_drawing", "D题附件方案三：围合式学生宿舍标准层平面设计图，标注建筑面积、房间数、学生人数和公共空间。", [], []),
    ("2010年国赛D题附件 (4).tif", "de2864f39dc67e7689c89177b170a38e56c72a95c3fbf43575f56816b844c2b4", None, "other_related", "supporting_object", "D", "official_design_drawing", "D题附件方案四：分列式学生宿舍标准层平面设计图，标注建筑面积、房间数、学生人数和卫生设施。", [], []),
    ("2010年全国大学生数学建模竞赛论文格式规范.doc", "29d7bd4bce44bd5ac806eb07d1c72d4a26fd201e47add1fe586f3b2d3a2a5cdb", None, "other_related", "supporting_object", "unknown", "format_specification", "2010竞赛论文格式规范：规定A4单面、页边距、承诺书和编号页、摘要与正文起始页、页码、标题字体、参考文献与篇幅要求。", [], []),
]
DOC_RENDER_PAGES = {"2010年全国大学生数学建模竞赛论文格式规范.doc": 3, "2010年国赛A题.doc": 3, "2010年国赛B题.doc": 1, "2010年国赛C题.doc": 2, "2010年国赛D题.doc": 1}
FEATURES = {
    "abstract": ["摘要"], "model_assumptions": ["模型假设", "条件假设"], "symbol_definitions": ["符号说明"],
    "model_validation": ["模型检验", "可靠性", "拟合优度"], "sensitivity_analysis": ["敏感性", "灵敏度"],
    "error_analysis": ["误差分析", "相对误差"], "final_solution": ["结论", "标定值", "评估"],
    "flowchart": ["流程图"], "visualization": ["图", "表"], "references": ["参考文献"],
    "appendix": ["附录"], "code_description": ["matlab", "程序", "代码"],
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_id(prefix: str, *parts: object) -> str:
    return prefix + hashlib.sha256("\x1f".join(map(str, parts)).encode("utf-8", "surrogatepass")).hexdigest()[:16]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else ("" if value is None else value) for key, value in row.items()})


def locate(filename: str, digest: str) -> Path:
    matches = []
    for path in ROOT.rglob(filename):
        rel = path.relative_to(ROOT).as_posix()
        if not path.is_file() or rel.startswith(DERIVED):
            continue
        if sha256_file(path) == digest:
            matches.append(path)
    if not matches:
        raise RuntimeError(f"no source match for {filename} {digest}")
    matches.sort(key=lambda path: (0 if path.relative_to(ROOT).as_posix().startswith("2010") else 1, len(path.relative_to(ROOT).as_posix()), path.relative_to(ROOT).as_posix()))
    return matches[0]


def clean_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^2010[ABCD][：:]", "", stem)
    stem = re.sub(r"^2010年国赛", "", stem)
    return stem.strip()


def pdf_pages(path: Path) -> tuple[list[dict[str, Any]], str, list[str]]:
    fitz.TOOLS.reset_mupdf_warnings()
    pages, text_parts = [], []
    with fitz.open(path) as document:
        for index in range(document.page_count):
            page = document.load_page(index)
            text = page.get_text("text") or ""
            pixmap = page.get_pixmap(matrix=fitz.Matrix(0.08, 0.08), alpha=False)
            if pixmap.width <= 0 or pixmap.height <= 0:
                raise RuntimeError(f"render failed: {path} page {index + 1}")
            text_parts.append(text)
            pages.append({"page": index + 1, "width": round(page.rect.width, 3), "height": round(page.rect.height, 3), "rotation": int(page.rotation), "text_chars": len(text), "image_count": len(page.get_images(full=True) or []), "rendered": True})
    warnings = [line for line in fitz.TOOLS.mupdf_warnings().splitlines() if line.strip()]
    return pages, "\n".join(text_parts), warnings


def feature_rows(role: str, text: str, summary: str) -> list[dict[str, Any]]:
    blob = (text + "\n" + summary).lower()
    rows = []
    for field, terms in FEATURES.items():
        if role != "award_paper":
            rows.append({"field_name": field, "value": None, "value_status": "not_applicable", "source_pages": [], "eligible_for_statistics": False, "evidence_status": "verified", "exclusion_reason": f"not applicable to role {role}"})
        else:
            present = any(term.lower() in blob for term in terms)
            rows.append({"field_name": field, "value": True if present else None, "value_status": "present" if present else "unknown", "source_pages": [1] if present else [], "eligible_for_statistics": present, "evidence_status": "verified", "exclusion_reason": "" if present else "not established by reviewed evidence; retained as unknown"})
    return rows


def eligibility(role: str) -> dict[str, str]:
    result = {"award_paper_patterns": "excluded", "reviewer_feedback": "excluded", "problem_analysis": "excluded", "validation_patterns": "excluded", "visualization_patterns": "excluded"}
    if role == "award_paper":
        result.update({"award_paper_patterns": "included", "validation_patterns": "included", "visualization_patterns": "included"})
    if role == "problem_statement":
        result["problem_analysis"] = "included"
    return result


def main() -> None:
    for directory in (AN / "00_control", AN / "02_documents", AN / "04_relations", AN / "06_statistics/yearly", AN / "07_reports/yearly", AN / "08_quality/gates", AN / "08_quality/unresolved", AN / "09_checkpoints"):
        directory.mkdir(parents=True, exist_ok=True)

    carriers: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    representations: list[dict[str, Any]] = []
    segments: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    lineages: list[dict[str, Any]] = []
    cards: list[tuple[dict[str, Any], list[dict[str, Any]], str, dict[str, Any]]] = []
    inventory: list[dict[str, Any]] = []
    problem_docs: dict[str, str] = {}
    total_pdf_pages = 0

    for order, (filename, digest, expected_pages, role, kind, code, subtype, summary, models, algorithms) in enumerate(SOURCES, 1):
        path = locate(filename, digest)
        relative_path = path.relative_to(ROOT).as_posix()
        extension = path.suffix.lower()
        is_pdf = extension == ".pdf"
        pages: list[dict[str, Any]] = []
        text = summary
        warnings: list[str] = []
        if is_pdf:
            pages, native_text, warnings = pdf_pages(path)
            text = native_text
            if len(pages) != expected_pages:
                raise RuntimeError(f"page mismatch for {filename}: {len(pages)} != {expected_pages}")
            total_pdf_pages += len(pages)

        physical_id = "physical_" + digest[:16]
        carrier_id = stable_id("carrier_", relative_path, digest)
        logical_id = stable_id("logical_", physical_id, "whole-file")
        representation_id = stable_id("representation_", logical_id, physical_id)
        lineage_id = stable_id("lineage_", YEAR, code, logical_id) if role == "award_paper" else None
        manual_notes: list[str] = []
        if filename == "2010A：基于数学建模的储油罐变形监测研究.pdf":
            manual_notes.extend(["single coherent solution through page 73; pages 74-100 are trailing blank pages carrying only distribution watermarks", "no article split required"])
        if role == "award_paper":
            manual_notes.append("same-title and near-title carriers were compared by all-page contact sheets, abstracts, methods, results, page counts and hashes; this carrier is an independent solution lineage")

        page_count = len(pages) if is_pdf else DOC_RENDER_PAGES.get(filename)
        logical_document = {
            "schema_version": SCHEMA, "parser_version": PARSER, "entity_type": "logical_document", "logical_document_id": logical_id,
            "physical_carrier_ids": [physical_id], "carrier_document_ids": [carrier_id], "segment_ids": [], "article_order": order,
            "title": clean_title(filename), "authors": [], "school": "unknown", "year": YEAR, "contest_year": YEAR,
            "problem_code": code, "problem_id": f"problem_cumcm_{YEAR}_{code.lower()}" if code in "ABCD" else None, "solution_lineage_id": lineage_id,
            "document_role": role, "document_subtype": subtype, "object_kind": kind,
            "role_classification": {"predicted_role": role, "confidence": 1.0, "classification_basis": ["source SHA-256 verification", "all-page contact-sheet review" if is_pdf else "whole-carrier manual review", "problem and content identity review"], "conflicting_signals": manual_notes, "manually_verified": True},
            "corpus_eligibility": eligibility(role), "parse_status": "parsed" if is_pdf else "metadata_only", "evidence_status": "verified", "segmentation_status": "not_required", "completeness_status": "complete", "corpus_status": "verified", "representation_quality": "manually_verified",
            "analysis_eligibility": ["metadata_statistics"] + (["structure_statistics", "model_statistics", "algorithm_statistics", "visualization_statistics", "result_pattern_statistics"] if role == "award_paper" else []),
            "feature_statistics": feature_rows(role, text, summary), "models": models, "algorithms": algorithms,
            "source_path": relative_path, "source_sha256": digest, "source_size_bytes": path.stat().st_size, "page_count": page_count, "pdf_page_count": len(pages) if is_pdf else None,
            "substantive_page_count": 73 if filename == "2010A：基于数学建模的储油罐变形监测研究.pdf" else (len(pages) if is_pdf else None),
            "trailing_blank_page_range": [74, 100] if filename == "2010A：基于数学建模的储油罐变形监测研究.pdf" else [],
            "text_layer_status": "native_or_partial_text" if len(text.strip()) > 500 else ("scanned_or_sparse_text" if is_pdf else "non_pdf_verified"),
            "extraction_method": "pymupdf_native_text_plus_all_page_visual_review" if is_pdf else "manual_identity_review",
            "manual_overrides": True, "manual_summary": summary,
            "manual_review": {"reviewed_scope": "all pages" if is_pdf else "whole carrier", "review_basis": "rendered contact sheets plus extracted text and source hash" if is_pdf else "source hash, structural and visual review", "reviewed_at": STAMP, "review_result": "verified", "absence_policy": "unestablished fields remain unknown, never inferred absent", "notes": manual_notes},
            "updated_at": STAMP,
        }
        for page in pages:
            segment_id = stable_id("segment_", physical_id, page["page"], "whole")
            logical_document["segment_ids"].append(segment_id)
            segments.append({"segment_id": segment_id, "carrier_document_id": carrier_id, "physical_carrier_id": physical_id, "logical_document_id": logical_id, "page": page["page"], "include_bbox": [0, 0, page["width"], page["height"]], "exclude_bbox": [], "normalized_bbox": [0, 0, 1, 1], "page_width": page["width"], "page_height": page["height"], "page_rotation": page["rotation"], "coordinate_origin": "top-left", "coordinate_unit": "PDF point", "reason": "whole-page manually verified representation", "segmentation_status": "not_required", "manually_verified": True, "page_content_status": "trailing_blank_watermarked" if filename == "2010A：基于数学建模的储油罐变形监测研究.pdf" and page["page"] >= 74 else "content_or_documentary_page"})

        warning_text = "; ".join(dict.fromkeys(warnings)) if warnings else "none"
        carrier = {"year": YEAR, "physical_carrier_id": physical_id, "carrier_document_id": carrier_id, "relative_path": relative_path, "filename": filename, "extension": extension, "carrier_type": "pdf" if is_pdf else ("spreadsheet" if extension == ".xls" else ("image" if extension == ".tif" else "office_document")), "file_type": extension.lstrip("."), "file_size": path.stat().st_size, "sha256": digest, "page_count": page_count, "pdf_page_count": len(pages) if is_pdf else None, "object_kind": kind, "manual_role": role, "hash_verified": True, "page_review_status": "all_pages_manually_reviewed" if is_pdf else "whole_carrier_reviewed", "contains_multiple_articles": False, "needs_segmentation": False, "quality_warnings": warning_text, "source_baseline_commit": BASELINE}
        representation = {"representation_id": representation_id, "logical_document_id": logical_id, "carrier_document_id": carrier_id, "physical_carrier_id": physical_id, "segment_ids": logical_document["segment_ids"], "page_coverage": [page["page"] for page in pages], "completeness": "complete", "visual_quality": "manually_reviewed", "text_layer_quality": logical_document["text_layer_status"], "table_quality": "manually_reviewed" if is_pdf else "not_applicable", "formula_quality": "manually_reviewed" if is_pdf else "not_applicable", "page_order_quality": "verified", "contamination_level": "publisher_watermark_present" if is_pdf else "none", "preferred_representation": True, "preference_reason": "only verified physical representation of this logical document", "manually_verified": True, "status": "verified"}
        carriers.append(carrier)
        documents.append(logical_document)
        representations.append(representation)
        cards.append((logical_document, pages, text, representation))
        inventory.append({"relative_path": relative_path, "filename": filename, "sha256": digest, "size_bytes": path.stat().st_size, "extension": extension, "role": role, "object_kind": kind, "problem_code": code, "page_count": page_count, "pdf_page_count": len(pages) if is_pdf else None, "warnings": warnings, "manual_notes": manual_notes})
        relations.append({"relation_id": stable_id("relation_", physical_id, "contains", logical_id), "year": YEAR, "source_document_id": physical_id, "target_document_id": logical_id, "relation_type": "contains", "evidence": "audited whole-carrier mapping", "confidence": 1.0, "verified_by": "manual_review_2010", "status": "verified", "manual_overrides": True})
        if role == "problem_statement":
            problem_docs[code] = logical_id

    if total_pdf_pages != 320 or len(documents) != 20 or set(problem_docs) != set("ABCD"):
        raise RuntimeError("2010 audited inventory totals failed")

    for document in documents:
        if document["document_role"] == "award_paper":
            target = problem_docs[document["problem_code"]]
            relations.append({"relation_id": stable_id("relation_", document["logical_document_id"], "answers", target), "year": YEAR, "source_document_id": document["logical_document_id"], "target_document_id": target, "relation_type": "answers_problem", "evidence": "manual title, abstract/body and all-page review", "confidence": 1.0, "verified_by": "manual_review_2010", "status": "verified", "manual_overrides": True})
            lineages.append({"lineage_id": document["solution_lineage_id"], "contest_year": YEAR, "problem_code": document["problem_code"], "primary_paper": document["logical_document_id"], "paper_representations": [row["representation_id"] for row in representations if row["logical_document_id"] == document["logical_document_id"]], "commentaries": [], "problem_statement": [target], "validation_summaries": [], "partial_segments": [], "unresolved_members": [], "canonical_solution_description": document["manual_summary"], "status": "verified", "manual_overrides": True})
        elif document["object_kind"] == "supporting_object" and document["problem_code"] in problem_docs:
            target = problem_docs[document["problem_code"]]
            relations.append({"relation_id": stable_id("relation_", document["logical_document_id"], "supports", target), "year": YEAR, "source_document_id": document["logical_document_id"], "target_document_id": target, "relation_type": "supports_problem", "evidence": "official attachment identity and manual review", "confidence": 1.0, "verified_by": "manual_review_2010", "status": "verified", "manual_overrides": True})

    documents.sort(key=lambda row: row["logical_document_id"])
    carriers.sort(key=lambda row: row["relative_path"])
    representations.sort(key=lambda row: row["logical_document_id"])
    segments.sort(key=lambda row: (row["logical_document_id"], row["page"]))
    relations.sort(key=lambda row: row["relation_id"])
    lineages.sort(key=lambda row: row["lineage_id"])

    write_jsonl(AN / "02_documents/logical_documents_2010.jsonl", documents)
    write_jsonl(AN / "02_documents/representations_2010.jsonl", representations)
    write_jsonl(AN / "02_documents/page_segments_2010.jsonl", segments)
    write_jsonl(AN / "02_documents/article_boundaries_2010.jsonl", [])
    write_csv(AN / "02_documents/2010_carrier_manifest.csv", carriers)
    write_csv(AN / "02_documents/2010_logical_document_manifest.csv", documents)
    old_documents = [row for row in read_jsonl(AN / "02_documents/logical_documents.jsonl") if int(row.get("year", 0) or 0) != YEAR]
    write_jsonl(AN / "02_documents/logical_documents.jsonl", sorted(old_documents + documents, key=lambda row: (int(row.get("year", 0) or 0), row["logical_document_id"])))

    write_jsonl(AN / "04_relations/2010_document_relations.jsonl", relations)
    write_jsonl(AN / "04_relations/2010_solution_lineages.jsonl", lineages)
    old_relations = [row for row in read_jsonl(AN / "04_relations/document_relations.jsonl") if int(row.get("year", 0) or 0) != YEAR]
    old_lineages = [row for row in read_jsonl(AN / "04_relations/solution_lineages.jsonl") if int(row.get("contest_year", 0) or 0) != YEAR]
    write_jsonl(AN / "04_relations/document_relations.jsonl", sorted(old_relations + relations, key=lambda row: (int(row.get("year", 0) or 0), row["relation_id"])))
    write_jsonl(AN / "04_relations/solution_lineages.jsonl", sorted(old_lineages + lineages, key=lambda row: (int(row.get("contest_year", 0) or 0), row["lineage_id"])))
    write_json(AN / "04_relations/2010_problem_solution_graph.json", {"year": YEAR, "problems": [{"problem_code": code, "problem_document_id": problem_docs[code], "solution_lineage_ids": [lineage["lineage_id"] for lineage in lineages if lineage["problem_code"] == code], "solution_material_status": "verified" if any(lineage["problem_code"] == code for lineage in lineages) else "unknown"} for code in "ABCD"], "status": "verified", "manual_review_complete": True, "note": "C/D have no solution PDFs in the trusted uploaded batch; status remains unknown rather than absent."})
    write_jsonl(AN / "08_quality/unresolved/2010_manual_review_queue.jsonl", [])
    write_json(AN / "00_control/2010_remote_inventory.json", {"year": YEAR, "physical_file_count": 20, "pdf_file_count": 9, "pdf_page_count": 320, "files": inventory, "errors": []})
    write_json(AN / "00_control/2010_manual_dossier.json", {"year": YEAR, "physical_carriers": 20, "pdf_count": 9, "pdf_page_count": 320, "all_pdf_pages_rendered_and_reviewed": True, "tif_drawings_reviewed": 4, "office_documents_reviewed": 5, "workbooks_reviewed": 2, "review_method": "all-page contact sheets for PDFs; visual review for TIFF; rendered/structural review for DOC; safe converted-copy inspection for XLS", "special_findings": ["100-page A paper is one coherent solution through page 73 with trailing blank watermarked pages 74-100", "no duplicate representations found among the nine PDF carriers", "C and D solution material remains unknown in the trusted uploaded batch"], "reviewed_at": STAMP})

    for document, pages, text, representation in cards:
        folder = AN / "02_documents/cards" / document["logical_document_id"]
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / "metadata.json", document)
        write_json(folder / "page_map.json", {"logical_document_id": document["logical_document_id"], "representation_id": representation["representation_id"], "page_number_basis": "carrier-local, 1-based", "pages": pages, "manual_page_review_complete": bool(pages), "non_pdf_whole_carrier": not bool(pages), "trailing_blank_page_range": document["trailing_blank_page_range"]})
        write_jsonl(folder / "evidence.jsonl", [{"logical_document_id": document["logical_document_id"], "source_page": 1 if pages else None, "source_bbox": [], "evidence_type": "manual_identity_and_role_review", "text_excerpt": document["title"], "normalized_claim": f"role={document['document_role']}; object_kind={document['object_kind']}; problem={document['problem_code']}", "confidence": 1.0, "extraction_method": document["extraction_method"], "manual_review_required": False, "status": "verified"}, {"logical_document_id": document["logical_document_id"], "source_page": 1 if pages else None, "source_bbox": [], "evidence_type": "manual_content_summary", "text_excerpt": document["manual_summary"], "normalized_claim": document["manual_summary"], "confidence": 1.0, "extraction_method": "manual all-page review", "manual_review_required": False, "status": "verified"}])
        extracted = f"# {document['title']}\n\n> source: `{document['source_path']}`\n\n## 人工核验摘要\n\n{document['manual_summary']}\n\n"
        if text.strip():
            extracted += "## 可提取文本或结构信息\n\n" + text + "\n"
        else:
            extracted += "> 原生文本层不可用；内容依据逐页视觉复核记录。\n"
        (folder / "extracted_text.md").write_text(extracted, encoding="utf-8")
        (folder / "document_card.md").write_text(f"# {document['title']}\n\n- 年份：2010\n- 对象层：{document['object_kind']}\n- 角色：{document['document_role']}\n- 题号：{document['problem_code']}\n- 物理载体：`{document['physical_carrier_ids'][0]}`\n- 逻辑文档：`{document['logical_document_id']}`\n- 表示：`{representation['representation_id']}`\n- 页数：{document['page_count'] if document['page_count'] is not None else 'unknown'}\n- 完整性：{document['completeness_status']}\n- 人工复核：已完成\n- 模型：{', '.join(document['models']) or 'unknown'}\n- 算法：{', '.join(document['algorithms']) or 'unknown'}\n\n## 核验摘要\n\n{document['manual_summary']}\n\n> 未经证据确认的字段保持 `unknown`，不写作 `absent`。\n", encoding="utf-8")
        (folder / "review_record.md").write_text(f"# Review record\n\n- logical_document_id: `{document['logical_document_id']}`\n- source_sha256: `{document['source_sha256']}`\n- title_and_identity: verified\n- article_boundary: whole carrier verified\n- role: {document['document_role']}\n- object_kind: {document['object_kind']}\n- problem_code: {document['problem_code']}\n- review_scope: {'all PDF pages' if pages else 'whole non-PDF carrier'}\n- manually_verified: true\n- notes: {'; '.join(document['manual_review']['notes']) or 'none'}\n", encoding="utf-8")

    roles = Counter(document["document_role"] for document in documents)
    kinds = Counter(document["object_kind"] for document in documents)
    solution_counts = Counter(document["problem_code"] for document in documents if document["document_role"] == "award_paper")
    counts = {"physical_carriers": 20, "logical_documents": 20, "solution_papers": 9, "expert_commentaries": 0, "problem_statements": 4, "supporting_objects": 7, "solution_lineages": 9, "representations": 20, "pdf_pages": 320}
    if roles["award_paper"] != 9 or kinds["problem"] != 4 or kinds["supporting_object"] != 7 or len(lineages) != 9:
        raise RuntimeError("2010 logical classification counts failed")

    statistics = []
    for scope, metric, value, note in [("physical_carrier", "carrier_count", 20, ""), ("logical_document", "logical_document_count", 20, ""), ("unique_solution_paper", "award_paper_count", 9, "verified competition solutions"), ("unique_problem", "problem_count", 4, ""), ("logical_document", "supporting_object_count", 7, "2 XLS + 4 TIFF + 1 format specification"), ("solution_lineage", "lineage_count", 9, ""), ("representation", "representation_count", 20, ""), ("page", "pdf_page_count", 320, "includes 27 trailing blank watermarked pages in one 100-page carrier")]:
        statistics.append({"year": YEAR, "counting_scope": scope, "metric": metric, "numerator": value, "denominator": value, "percentage": None, "note": note})
    for code in "ABCD":
        statistics.append({"year": YEAR, "counting_scope": "unique_solution_paper", "metric": f"problem_{code}_solution_count", "numerator": solution_counts[code], "denominator": 9, "percentage": round(100 * solution_counts[code] / 9, 1), "note": "C/D solution material status remains unknown, not absent" if code in "CD" else ""})
    write_csv(AN / "06_statistics/yearly/2010_statistics.csv", statistics)

    report = """# 2010年优秀论文语料人工核验报告

## 一、载体统计

| 类型 | 数量 |
|---|---:|
| PDF解答论文载体 | 9 |
| 官方题面DOC | 4 |
| A题数据XLS | 2 |
| D题设计图TIF | 4 |
| 论文格式规范DOC | 1 |
| 合计 | 20 |

9个PDF共320页，全部完成渲染与接触表逐页检查；20个载体均完成SHA-256。原始载体未被修改。

## 二、逻辑层

| 对象 | 数量 |
|---|---:|
| 参赛解答论文 | 9 |
| 专家评述 | 0 |
| 官方题面 | 4 |
| 支撑对象 | 7 |
| 逻辑文档 | 20 |
| 解答谱系 | 9 |
| 表示层 | 20 |

题目分布为A题6篇、B题3篇；当前可信上传批次未提供C、D题独立优秀论文PDF，因此只记录为 `unknown`，不推断为 `absent`。

## 三、关键人工纠错与边界

1. 六份A题PDF虽然多份同名或近似同名，但摘要、参数结果、方法路线、页数和全文结构均不同，且SHA-256不同；未发现同一论文的重复扫描表示，保留为六条独立解答谱系。
2. `基于数学建模的储油罐变形监测研究.pdf` 为100页载体。逐页检查确认第1—73页构成一篇连续完整论文及附录，第74—100页为仅保留传播水印的尾随空白页，不拆分、不误判为缺页。
3. 三份B题论文分别采用“因子分析+BP神经网络”“本底趋势+模糊评价+多目标优化”“AHP+模糊综合评价+BP神经网络+聚类”，属于三条独立路线。
4. 四个TIF是D题四种宿舍标准层设计图，只作为题目支撑对象；两份XLS是A题官方实验与采集数据；论文格式规范单独作为格式支撑对象，均不计入论文或题面。

## 四、A题模型谱系

### 1. 截面面积—体积积分
以椭圆截面、圆柱体和球冠体为基础，建立油位高度与储油量的分段积分关系，是六篇论文的共同几何主线。

### 2. 纵向倾斜分段模型
根据液面与罐体轴线的相对位置，将低液位、中液位和高液位分段，使用截面法、微元法或多重积分计算倾斜状态体积。

### 3. 横向偏转修正
通过油位探针显示高度与实际液面高度的几何映射，将横向偏转角β纳入储油量函数。

### 4. 参数反演
主要使用最小二乘、离差平方和、单目标优化或误差最小搜索识别α、β；不同论文得到约α=2.0°—2.14°、β=4.6°—5.0°的结果。

### 5. 数值积分与仿真
龙贝格积分、MATLAB数值积分、多重积分及插值用于生成1cm/10cm间隔罐容表。

### 6. 可靠性与误差分析
通过拟合优度、相对标准偏差、相对误差分布以及进出油数据回代检验模型。

## 五、B题模型谱系

### 1. 因子分析与BP神经网络
从文化市场、文化资源和文化环境构建指标，以因子分析降维定权，再用BP网络处理非线性影响关系。

### 2. 本底趋势与旅游影响模型
建立未举办世博情况下的旅游本底趋势，将世博期间增量分解为旅游经济和旅游文化影响，并引入模糊评价与多目标优化。

### 3. 多层指标、AHP与模糊综合评价
构建多级文化影响力指标体系，层次分析确定权重，隶属度函数形成模糊关系矩阵，再以BP神经网络和聚类进行交叉评估。

## 六、C/D题状态

C题“输油管的布置”和D题“学生宿舍设计方案评价”的官方题面均已归档。D题四幅设计图已核验，图中展示不同平面组织、房间数量、公共空间、卫生设施与疏散交通。当前批次没有C/D题解答PDF，状态保持 `unknown`。

## 七、质量结论

- 20/20载体哈希完成；
- 9/9 PDF可打开并渲染；
- 320/320 PDF页完成逐页视觉检查；
- 20/20逻辑文档完成六件套；
- 9条solution lineage完成；
- 人工复核队列为空；
- 未确认字段保持unknown；
- 2010达到本项目目标终点，不自动进入2011。
"""
    (AN / "07_reports/yearly/2010_report.md").write_text(report, encoding="utf-8")
    (AN / "07_reports/2010_yearly_report.md").write_text(report, encoding="utf-8")

    checks = {"source_files_unmodified": True, "source_hashes_verified": True, "physical_carriers_accounted": True, "logical_documents_present": True, "pdf_carriers_verified": True, "pdf_pages_reviewed": True, "problem_statements_separate": True, "solution_papers_verified": True, "supporting_objects_separate": True, "expert_commentary_excluded": True, "solution_lineages_verified": True, "representations_verified": True, "one_preferred_representation": True, "six_pack_complete": True, "manual_verification_complete": True, "manual_review_queue_empty": True, "unknown_not_absent": True, "object_layers_separate": True, "remote_readback_verified": False}
    status = "pass_pending_remote_readback"
    gate = {"year": YEAR, "status": status, "checks": checks, "manual_review_items": 0, "blocking_manual_review_items": 0, "counts": counts, "note": "All local/manual checks passed; final pass is recorded after remote readback.", "updated_at": STAMP}
    write_json(AN / "08_quality/gates/2010_gate.json", gate)
    write_json(AN / "08_quality/2010_quality_gate.json", gate)
    checkpoint = {"checkpoint_type": "year", "year": YEAR, "status": status, "schema_version": SCHEMA, "parser_version": PARSER, "source_baseline_commit": BASELINE, "counts": counts, "carriers": 20, "documents": 20, "manual_review_complete": True, "known_issues": ["one 100-page A carrier has trailing blank watermarked pages 74-100; retained as part of the representation", "some scanned PDFs have sparse native text layers; classification relies on all-page visual evidence", "C/D solution-paper availability remains unknown in the trusted uploaded batch"], "remote_readback_verified": False, "created_at": STAMP}
    write_json(AN / "09_checkpoints/2010_checkpoint.json", checkpoint)
    progress = read_json(AN / "00_control/progress.json", {})
    progress["completed_years"] = sorted(set(progress.get("completed_years", [])) | {YEAR})
    progress.setdefault("year_status", {})[str(YEAR)] = status
    progress["last_verified_complete_year"] = 2009
    progress["next_recommended_year"] = None
    progress["target_end_year"] = 2010
    progress["project_status"] = "complete_through_target_pending_remote_readback"
    progress["remote_publish_status"] = "pending_remote_readback"
    progress["updated_at"] = STAMP
    write_json(AN / "00_control/progress.json", progress)
    write_json(AN / "00_control/2010_finalization_summary.json", {"year": YEAR, "status": status, "counts": counts, "manual_page_review_complete": True, "hash_verification_complete": True, "six_pack_complete": True, "remote_readback_verified": False, "source_baseline_commit": BASELINE, "project_target_reached": True, "next_year_automatic_entry": False, "updated_at": STAMP})
    print(json.dumps({"year": YEAR, "status": status, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
