#!/usr/bin/env python3
"""Apply the visually verified 1993 logical-document and cross-year review."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.apply_manual_review_1992 import (FEATURES, fstats, read_jsonl, stable,
                                               write_json, write_jsonl)

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
DOCS = AI / "02_documents"
CARDS = DOCS / "cards"
REL = AI / "04_relations"
CAT = AI / "05_catalogs"
REPORTS = AI / "07_reports" / "yearly"
QUALITY = AI / "08_quality"

A_PROBLEM = "logical_16bea3dd6cef91b8"
A_PAPER = "logical_e6bf45e93a065728"
B_COMMENTARY = "logical_ddecdd2fd9deb09f"
B_PROBLEM = "logical_a9bca702479e4ac0"
B_PAPER = "logical_c8ba8962d24258a2"
COMBINED = "logical_300e7c6d8d5a51a3"
INTERMOD_1992 = "logical_096f6338555ccb87"


SPECS: dict[str, dict[str, Any]] = {
    A_PROBLEM: {"role": "problem_statement", "title": "1993年A题：非线性交调的频率设计", "authors": [],
        "problem": "A", "problem_id": "problem_cumcm_1993_a", "lineage": None, "parse": "parsed", "evidence": "verified",
        "models": [], "algorithms": [], "content": {"subproblems": ["拟合非线性输入输出函数", "设计满足接收带和SNR约束的三个整数频率", "讨论稳定性"], "inputs": ["9组u-y数据", "A1=25、A2=10、A3=45"], "outputs": ["频率组f1/f2/f3"], "constraints": ["三个频率区间", "接收带±5", "fi±6处SNR>10dB", "频率互不落入接收带"]}},
    A_PAPER: {"role": "award_paper", "title": "非线性交调的频率设计——A题", "authors": ["檀晋轩", "邢毅春", "郝燕"],
        "problem": "A", "problem_id": "problem_cumcm_1993_a", "lineage": "lineage_cumcm_1993_a_intermodulation_frequency_design",
        "parse": "parsed", "evidence": "verified", "models": ["cubic_least_squares_input_output_model", "frequency_constraint_model", "snr_model"],
        "algorithms": ["least_squares", "integer_enumeration", "constraint_screening"],
        "features": {"abstract": ("present", [1]), "model_assumptions": ("present", [2]), "symbol_definitions": ("present", [2, 3]),
            "model_validation": ("present", [4, 5]), "sensitivity_analysis": ("present", [4, 5]), "error_analysis": ("present", [5]),
            "final_solution": ("present", [4, 5]), "final_answer_summary_table": ("absent", list(range(1, 9))),
            "flowchart": ("absent", list(range(1, 9))), "visualization": ("present", [1, 4]),
            "references": ("absent", list(range(1, 9))), "appendix": ("absent", list(range(1, 9))), "code_description": ("present", [4])},
        "content": {"problem_and_subproblems": ["用数据拟合非线性器件", "枚举并筛选频率", "证明解的稳定性与一般性质"],
            "data_types": ["连续输入输出数据", "整数频率", "信号幅值"], "mathematical_essence": "多项式拟合后的交调频率组合与不等式约束筛选。",
            "data_preprocessing": ["最小二乘拟合三次多项式"], "baseline_models": ["二、三阶交调的直接枚举"],
            "core_models": ["三次输入输出模型", "接收带约束", "SNR约束"], "parameter_sources": ["题给u-y数据", "题给幅值和σ=6"],
            "validation_methods": ["系数扰动稳定性", "高次项量级分析", "输入频率微扰分析", "充分必要条件证明"],
            "important_results": ["基本约束得到6组候选", "SNR筛选保留(36,42,55)与(36,49,55)"],
            "abstract_structure": "问题—拟合—算法—稳定性—定理推广。", "section_structure": ["问题提出", "问题分析", "模型假设", "建模求解", "稳定性", "理论归纳"],
            "innovation_expression": "从计算筛选提升为可取频率组的充分必要条件。", "strengths": ["工程约束、计算与定理闭环", "对误差和稳定性作多层分析"],
            "limitations": ["无公开程序源代码", "SNR模型依赖三次多项式近似"], "reproducibility_level": "medium_high"}},
    B_COMMENTARY: {"role": "expert_commentary", "title": "关于“球队排名次问题”的几点评注——B题", "authors": ["蔡大用"],
        "problem": "B", "problem_id": "problem_cumcm_1993_b", "lineage": "lineage_cumcm_1993_b_football_ranking",
        "parse": "partially_parsed", "evidence": "key_content_verified", "models": ["ranking_models", "ahp"], "algorithms": [],
        "content": {"document_purpose": "解释开放排名题背景并归纳评审标准和典型方法。", "review_findings": ["先审假设是否合理", "再审模型是否反映实际且有一般性", "最后审叙述是否清楚", "肯定AHP完整分析", "反对猜测标准答案或只对一组数据有效的算法"], "strengths": ["评审标准明确且可迁移"], "limitations": ["评论多类答卷，不只对应一篇论文"], "reproducibility_level": "not_applicable"}},
    B_PROBLEM: {"role": "problem_statement", "title": "1993年B题：足球队排名次", "authors": [],
        "problem": "B", "problem_id": "problem_cumcm_1993_b", "lineage": None, "parse": "parsed", "evidence": "verified",
        "models": [], "algorithms": [], "content": {"subproblems": ["为12队排名并给出结果", "推广到N队", "讨论可排名的数据条件"], "inputs": ["1988—1989甲级联赛赛果矩阵"], "outputs": ["名次", "一般算法", "数据条件"], "constraints": ["含多场比赛、平局、缺赛和不一致数据"]}},
    B_PAPER: {"role": "award_paper", "title": "一个给足球队排名次的方法——B题", "authors": ["戚立峰", "毛威", "马斌"],
        "problem": "B", "problem_id": "problem_cumcm_1993_b", "lineage": "lineage_cumcm_1993_b_football_ranking",
        "parse": "partially_parsed", "evidence": "key_content_verified", "models": ["ahp_pairwise_judgment_matrix", "perron_frobenius_eigenvector_ranking", "chi_square_reliability"],
        "algorithms": ["power_iteration", "graph_connectivity_check", "ranking_sort"],
        "features": {"abstract": ("present", [1]), "model_assumptions": ("present", [2]), "symbol_definitions": ("present", [2, 3]),
            "model_validation": ("present", [6, 7, 8]), "sensitivity_analysis": ("absent", list(range(1, 10))), "error_analysis": ("present", [7, 8, 9]),
            "final_solution": ("present", [8]), "final_answer_summary_table": ("absent", list(range(1, 10))),
            "flowchart": ("absent", list(range(1, 10))), "visualization": ("present", [9]), "references": ("present", [9]),
            "appendix": ("absent", list(range(1, 10))), "code_description": ("present", [3, 4])},
        "content": {"problem_and_subproblems": ["从赛果构造判断矩阵", "用主特征向量排名", "处理缺赛和残缺数据", "估计可依赖程度"],
            "data_types": ["比赛网络", "比分与多场赛果", "缺失和矛盾数据"], "mathematical_essence": "非负矩阵主特征向量排序与图连通性。",
            "data_preprocessing": ["把比分和多场结果映射为相对强度a_ij", "可约性检查", "构造辅助矩阵处理残缺"],
            "baseline_models": ["积分排序"], "core_models": ["AHP判断矩阵", "Perron–Frobenius主特征向量", "χ²可依赖度"],
            "parameter_sources": ["赛果表", "经验比分权重", "σ²=1/2的简化估计"], "validation_methods": ["保序性证明", "残缺处理命题", "扰动稳定性", "χ²可靠度"],
            "important_results": ["排名T7,T3,T1,T9,T2,T10,T8,T12,T6,T5,T11,T4", "数据可依赖度约65%", "运行时间小于1秒"],
            "abstract_structure": "模型—数据充分性—可靠度—名次—理论性质和推广。", "section_structure": ["问题分析", "模型和算法", "理论分析", "运行结果", "优缺点"],
            "innovation_expression": "把排名反馈、残缺数据和可靠度统一进特征向量框架。", "strengths": ["能处理平局、缺赛和不一致", "理论性质与数值排名对应"],
            "limitations": ["算法较复杂且依赖计算机", "比分映射和σ²=1/2具有经验性", "未研究近乎可约矩阵的排序稳定性"], "reproducibility_level": "medium"}},
}


EVIDENCE: dict[str, list[tuple[int, str, str, str, str, list[float] | None]]] = {
    A_PROBLEM: [(1, "题面", "identity", "A题 非线性交调的频率设计", "身份为A题题面", None), (1, "输入", "input_data", "A1=25，A2=10，A3=45", "给出输入幅值和u-y数据", None), (2, "约束", "problem_requirement", "SNR应大于10分贝", "给出接收带和SNR约束", None)],
    A_PAPER: [(1, "摘要", "identity", "非线性交调的频率设计——A题", "身份为1993 A题参赛论文", None), (2, "模型假设", "assumption", "列出三项模型假设", "忽略外部干扰与四次以上交调", None), (3, "输出函数", "formula", "三次多项式", "最小二乘拟合非线性输入输出关系", None), (4, "算法", "algorithm", "按三个步骤筛选", "枚举整数频率并按接收带和SNR筛选", None), (4, "结果表", "result", "36,42,55；36,49,55", "最终保留两组频率", None), (5, "稳定性分析", "sensitivity", "系数波动范围", "证明系数和频率微扰不改变解", None), (7, "定理1", "theorem", "充分必要条件", "给出解存在的充分必要条件", None)],
    B_COMMENTARY: [(1, "标题", "identity", "球队排名次问题的几点评注", "身份为专家评注", None), (2, "评审标准", "review_feedback", "假设是否合理", "评审首先检查假设", None), (2, "评审标准", "review_feedback", "结果是否合乎实际，而且具有一般性", "评审模型适配与可推广性", None), (2, "例3", "review_feedback", "层次分析法完整地分析并解决", "肯定AHP类完整解答", None), (2, "总结", "review_feedback", "没有唯一的最优方法", "开放题不应猜标准答案", None)],
    B_PROBLEM: [(1, "题面", "identity", "B题 足球队排名次", "身份为B题题面", None), (1, "任务", "problem_requirement", "排出诸队名次", "要求排名、推广与数据条件", None), (1, "数据表", "input_data", "12支球队", "输入为赛果矩阵", None)],
    B_PAPER: [(1, "同页下篇标题", "identity", "一个给足球队排名次的方法——B题", "身份为1993 B题参赛论文", [0, 360, 588, 792]), (1, "摘要", "model", "层次分析法", "核心为AHP排名模型", [0, 360, 588, 792]), (3, "判断矩阵", "formula", "A=(a_ij)", "构造互反判断矩阵", None), (4, "算法", "algorithm", "迭代计算主特征向量", "用幂法求排序向量", None), (7, "模型稳定性", "validation", "特征向量的变动是微小的", "给出扰动稳定性论证", None), (8, "运行结果", "result", "T7,T3,T1,T9,T2,T10,T8,T12,T6,T5,T11,T4", "给出12队最终排名", None), (8, "运行结果", "validation", "可依赖程度为65%", "给出数据可靠度", None), (9, "模型缺点", "limitation", "算法复杂", "作者明确列出复杂度和经验参数缺陷", None)],
}


def corpus(role: str) -> dict[str, str]:
    out = {k: "excluded" for k in ["award_paper_patterns", "reviewer_feedback", "problem_analysis", "validation_patterns", "visualization_patterns"]}
    if role == "award_paper": out["award_paper_patterns"] = out["visualization_patterns"] = "included"
    if role == "expert_commentary": out["reviewer_feedback"] = "included"
    if role == "problem_statement": out["problem_analysis"] = "included"
    return out


def ev(doc_id: str, row: tuple[int, str, str, str, str, list[float] | None]) -> dict[str, Any]:
    p, section, kind, excerpt, claim, bbox = row
    return {"logical_document_id": doc_id, "paper_id": doc_id if SPECS[doc_id]["role"] == "award_paper" else None,
            "source_page": p, "source_section": section, "source_bbox": bbox or [], "evidence_type": kind,
            "text_excerpt": excerpt, "normalized_claim": claim, "confidence": 0.98,
            "extraction_method": "manual_visual_review_with_native_text" if doc_id in {A_PROBLEM, A_PAPER, B_PROBLEM} else "manual_visual_review",
            "manual_review_required": False}


def main() -> None:
    old_docs = {d["logical_document_id"]: d for d in read_jsonl(DOCS / "logical_documents_1993.jsonl")}
    old_reps = {r["logical_document_id"]: r for r in read_jsonl(DOCS / "representations_1993.jsonl")}
    reviewed_ids = {A_PROBLEM, A_PAPER, B_COMMENTARY, B_PROBLEM, B_PAPER}

    def remove_absorbed_candidate_bundle() -> None:
        bundle = CARDS / COMBINED
        for name in ("document_card.md", "metadata.json", "extracted_text.md", "page_map.json",
                     "evidence.jsonl", "review_record.md"):
            path = bundle / name
            if path.exists():
                path.unlink()
        if bundle.exists() and not any(bundle.iterdir()):
            bundle.rmdir()

    def write_year_relation_views() -> None:
        year_relations = [r for r in read_jsonl(REL / "document_relations.jsonl")
                          if int(r.get("year", 0)) == 1993]
        year_lineages = [r for r in read_jsonl(REL / "solution_lineages.jsonl")
                         if int(r.get("contest_year", 0) or 0) == 1993
                         or r.get("lineage_id") == "lineage_intermodulation_frequency_design_unresolved_year"]
        write_jsonl(REL / "document_relations_1993.jsonl", year_relations)
        write_jsonl(REL / "solution_lineages_1993.jsonl", year_lineages)

    if set(old_docs) == reviewed_ids and all(d.get("manual_overrides") for d in old_docs.values()):
        remove_absorbed_candidate_bundle()
        write_year_relation_views()
        print('{"status":"reused_manual_review","year":1993,"logical_documents":5}')
        return
    if set(old_docs) != reviewed_ids | {COMBINED}:
        raise SystemExit("1993 candidate IDs differ from reviewed carrier set")

    combined_carrier = old_docs[COMBINED]["carrier_document_ids"][0]
    absorptions = [r for r in read_jsonl(DOCS / "carrier_absorptions.jsonl") if int(r.get("year", 0)) != 1993]
    absorptions.append({"year": 1993, "carrier_document_id": combined_carrier,
        "logical_document_ids": [A_PROBLEM, B_PROBLEM], "reason": "official A/B combined statement split into canonical problems",
        "manually_verified": True, "manual_overrides": True})
    write_jsonl(DOCS / "carrier_absorptions.jsonl", absorptions)

    maps = {doc_id: json.loads((CARDS / doc_id / "page_map.json").read_text(encoding="utf-8")) for doc_id in old_docs}
    documents: list[dict[str, Any]] = []
    segments: list[dict[str, Any]] = []
    representations: list[dict[str, Any]] = []
    segment_by_doc_carrier: dict[tuple[str, str], list[str]] = {}

    def add_segment(doc_id: str, carrier: str, page: int, w: float, h: float, bbox: list[float], rotation: int = 0) -> str:
        sid = stable("segment_", doc_id, carrier, page, *bbox, "manual-1993")
        segments.append({"segment_id": sid, "carrier_document_id": carrier, "logical_document_id": doc_id,
            "page": page, "include_bbox": bbox, "exclude_bbox": [],
            "normalized_bbox": [round(bbox[0]/w, 6), round(bbox[1]/h, 6), round(bbox[2]/w, 6), round(bbox[3]/h, 6)],
            "page_width": w, "page_height": h, "page_rotation": rotation, "coordinate_origin": "top-left",
            "coordinate_unit": "PDF point", "reason": "manually verified valid article region",
            "segmentation_status": "segmented" if bbox != [0, 0, w, h] else "not_required", "manually_verified": True})
        segment_by_doc_carrier.setdefault((doc_id, carrier), []).append(sid)
        return sid

    # Regular carriers, with B-paper page 1 cropped at the verified same-page boundary.
    for doc_id in [A_PROBLEM, A_PAPER, B_COMMENTARY, B_PROBLEM, B_PAPER]:
        carrier = old_docs[doc_id]["carrier_document_ids"][0]
        for p in maps[doc_id]["pages"]:
            bbox = [0, 360, p["width"], p["height"]] if doc_id == B_PAPER and p["page"] == 1 else [0, 0, p["width"], p["height"]]
            add_segment(doc_id, carrier, p["page"], p["width"], p["height"], bbox, p.get("rotation", 0))
    # Official combined statement: page 1=A, page 2=B.
    for doc_id, page in [(A_PROBLEM, 1), (B_PROBLEM, 2)]:
        p = next(x for x in maps[COMBINED]["pages"] if x["page"] == page)
        add_segment(doc_id, combined_carrier, page, p["width"], p["height"], [0, 0, p["width"], p["height"]], p.get("rotation", 0))

    rep_lookup: dict[tuple[str, str], str] = {}
    for doc_id in [A_PROBLEM, A_PAPER, B_COMMENTARY, B_PROBLEM, B_PAPER]:
        carriers = [old_docs[doc_id]["carrier_document_ids"][0]]
        if doc_id in {A_PROBLEM, B_PROBLEM}: carriers.append(combined_carrier)
        for carrier in carriers:
            rep_id = old_reps[doc_id]["representation_id"] if carrier == old_docs[doc_id]["carrier_document_ids"][0] else stable("representation_", carrier, doc_id)
            rep_lookup[(doc_id, carrier)] = rep_id
            preferred = carrier == combined_carrier if doc_id in {A_PROBLEM, B_PROBLEM} else True
            representations.append({"representation_id": rep_id, "logical_document_id": doc_id, "carrier_document_id": carrier,
                "segment_ids": segment_by_doc_carrier[(doc_id, carrier)],
                "page_coverage": [s["page"] for s in segments if s["segment_id"] in segment_by_doc_carrier[(doc_id, carrier)]],
                "completeness": "complete", "visual_quality": "good", "text_layer_quality": "native_text_reviewed" if doc_id in {A_PROBLEM, A_PAPER, B_PROBLEM} or carrier == combined_carrier else "scan_visual_only",
                "table_quality": "verified_key_tables", "formula_quality": "verified_key_formulas", "page_order_quality": "verified",
                "contamination_level": "cropped_same_page_content" if doc_id == B_PAPER else "none_detected",
                "preferred_representation": preferred,
                "preference_reason": "official combined statement representation" if preferred and doc_id in {A_PROBLEM, B_PROBLEM} else "complete manually verified representation" if preferred else "duplicate standalone statement retained",
                "manual_overrides": True})

    for doc_id, spec in SPECS.items():
        old = old_docs[doc_id]
        carrier_ids = [old["carrier_document_ids"][0]] + ([combined_carrier] if doc_id in {A_PROBLEM, B_PROBLEM} else [])
        all_sids = [s["segment_id"] for s in segments if s["logical_document_id"] == doc_id]
        elig = {"metadata_statistics"}
        if spec["role"] == "award_paper": elig |= {"structure_statistics", "model_statistics", "algorithm_statistics", "visualization_statistics", "result_pattern_statistics"}
        elif spec["role"] == "expert_commentary": elig.add("reviewer_feedback_statistics")
        else: elig.add("problem_analysis")
        doc = {**old, "title": spec["title"], "authors": spec["authors"], "carrier_document_ids": carrier_ids,
            "segment_ids": all_sids, "problem_code": spec["problem"], "problem_id": spec["problem_id"],
            "solution_lineage_id": spec["lineage"], "document_role": spec["role"], "document_subtype": "none",
            "role_classification": {"predicted_role": spec["role"], "confidence": 1.0,
                "classification_basis": ["title", "document_structure", "first_page_text", "visual_review"],
                "conflicting_signals": ["filename says 优秀论文 but content is a problem statement"] if spec["role"] == "problem_statement" else [], "manually_verified": True},
            "corpus_eligibility": corpus(spec["role"]), "parse_status": spec["parse"], "evidence_status": spec["evidence"],
            "segmentation_status": "segmented" if doc_id == B_PAPER or len(carrier_ids) > 1 else "not_required",
            "completeness_status": "complete", "corpus_status": "included", "representation_quality": "manually_reviewed",
            "analysis_eligibility": sorted(elig), "feature_statistics": fstats(spec["role"], spec.get("features", {})),
            "models": spec["models"], "algorithms": spec["algorithms"], "manual_overrides": True,
            "manual_reviewed_at": "2026-07-22T00:00:00Z", "content_analysis": spec["content"],
            "page_count": 1 if doc_id in {A_PROBLEM, B_PROBLEM} else old["page_count"]}
        documents.append(doc)

        folder = CARDS / doc_id
        write_json(folder / "metadata.json", doc)
        preferred = next(r for r in representations if r["logical_document_id"] == doc_id and r["preferred_representation"])
        page_entries = []
        for s in segments:
            if s["segment_id"] in preferred["segment_ids"]:
                page_entries.append({"page": s["page"], "width": s["page_width"], "height": s["page_height"],
                    "rotation": s["page_rotation"], "valid_bbox": s["include_bbox"], "excluded_bbox": s["exclude_bbox"],
                    "segment_id": s["segment_id"], "carrier_document_id": s["carrier_document_id"], "manually_verified": True})
        write_json(folder / "page_map.json", {"logical_document_id": doc_id, "page_number_basis": "carrier-local, 1-based",
            "representation_id": preferred["representation_id"], "coordinate_origin": "top-left", "coordinate_unit": "PDF point", "pages": page_entries})
        write_jsonl(folder / "evidence.jsonl", [ev(doc_id, row) for row in EVIDENCE[doc_id]])
        (folder / "document_card.md").write_text(f"# {spec['title']}\n\n- 年份：1993\n- 角色：{spec['role']}\n- 状态：{spec['parse']} / {spec['evidence']} / complete\n- 题号：{spec['problem']}\n- 模型：{'、'.join(spec['models']) or '不适用'}\n- 方案谱系：{spec['lineage'] or '不适用'}\n\n## 人工核验摘要\n\n{json.dumps(spec['content'], ensure_ascii=False, indent=2)}\n\n> 完整正文只保存在忽略缓存。\n", encoding="utf-8")
        (folder / "review_record.md").write_text("# Review record\n\n" + f"- logical_document_id: `{doc_id}`\n" + "".join(f"- {x}: verified\n" for x in ["标题和身份", "文章边界", "摘要或开篇", "核心模型或评议对象", "关键公式", "关键表格或图", "最终结论", "重要数字", "关联文档关系"]) + "- manually_verified: true\n", encoding="utf-8")

    documents.sort(key=lambda d: d["article_order"])
    write_jsonl(DOCS / "logical_documents_1993.jsonl", documents)
    all_docs = [d for d in read_jsonl(DOCS / "logical_documents.jsonl") if int(d.get("year", 0)) != 1993] + documents
    write_jsonl(DOCS / "logical_documents.jsonl", sorted(all_docs, key=lambda d: (int(d.get("year", 0)), d["logical_document_id"])))
    write_jsonl(DOCS / "page_segments_1993.jsonl", segments)
    write_jsonl(DOCS / "representations_1993.jsonl", representations)
    b_carrier = old_docs[B_PAPER]["carrier_document_ids"][0]
    write_jsonl(DOCS / "article_boundaries_1993.jsonl", [{"boundary_id": stable("boundary_", b_carrier, 1, 360),
        "logical_document_id": B_PAPER, "carrier_document_id": b_carrier, "before_page": 1, "after_page": 1,
        "same_page_boundary": True, "boundary_y": 360, "boundary_bbox": [0, 360, 588, 792],
        "normalized_bbox": [0, 0.454545, 1, 1], "page_width": 588, "page_height": 792, "page_rotation": 0,
        "evidence": "visual transition from intermodulation commentary ending to football-ranking title", "confidence": 0.99,
        "manually_verified": True, "manual_overrides": True}])

    orphans = read_jsonl(DOCS / "orphan_segments.jsonl")
    for item in orphans:
        if item.get("detected_title") == "一个给足球队排名次的方法——B题":
            item.update({"matched_document_id": B_PAPER, "match_status": "matched", "preservation_status": "preserved_and_linked_cross_year"})
    top_orphan = {"segment_id": stable("orphan_", b_carrier, 1, 0, 0, 588, 360), "carrier_document_id": b_carrier,
        "page": 1, "bbox": [0, 0, 588, 360], "normalized_bbox": [0, 0, 1, 0.454545], "page_width": 588, "page_height": 792,
        "page_rotation": 0, "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
        "detected_title": "关于非线性交调的频率设计的评注（结尾）", "probable_role": "expert_commentary",
        "matched_document_id": INTERMOD_1992, "match_status": "matched", "preservation_status": "preserved_and_linked_cross_year",
        "reason_excluded_from_primary_document": "same-page boundary; upper text duplicates commentary ending", "manual_overrides": True}
    orphans = [o for o in orphans if o.get("segment_id") != top_orphan["segment_id"]] + [top_orphan]
    write_jsonl(DOCS / "orphan_segments.jsonl", orphans)

    def relation(source: str, target: str, kind: str, evidence: str, confidence: float = 0.98) -> dict[str, Any]:
        return {"relation_id": stable("relation_", source, kind, target), "year": 1993,
            "source_document_id": source, "target_document_id": target, "relation_type": kind, "evidence": evidence,
            "confidence": confidence, "verified_by": "manual_visual_review", "status": "verified", "manual_overrides": True}
    relations = [r for r in read_jsonl(REL / "document_relations.jsonl") if int(r.get("year", 0)) != 1993]
    for rep in representations:
        relations.append(relation(rep["carrier_document_id"], rep["logical_document_id"], "contains", "verified segment and representation mapping"))
    relations += [
        relation(A_PAPER, A_PROBLEM, "answers_problem", "u-y data, frequency bounds, SNR and reception-band constraints correspond"),
        relation(B_PAPER, B_PROBLEM, "answers_problem", "12-team score matrix and all three tasks correspond"),
        relation(B_COMMENTARY, B_PAPER, "comments_on", "commentary explicitly praises complete AHP treatment", 0.90),
        relation(B_COMMENTARY, B_PAPER, "evaluates_solution", "review criteria address assumptions, generality and clarity", 0.90),
        relation(INTERMOD_1992, A_PAPER, "comments_on", "same cubic model, σ=6 constraints, six candidates and two SNR-surviving triples"),
        relation(INTERMOD_1992, A_PAPER, "evaluates_solution", "commentary discusses stability, theorem and exact two frequency triples"),
        relation(INTERMOD_1992, A_PAPER, "same_solution_lineage", "formula/result correspondence and official 1993 A statement resolve year"),
        relation(top_orphan["segment_id"], INTERMOD_1992, "partial_copy_of", "upper page text duplicates 1992 carrier commentary ending"),
        relation(next(o["segment_id"] for o in orphans if o.get("detected_title") == "一个给足球队排名次的方法——B题"), B_PAPER, "partial_copy_of", "1992 carrier lower-page title, abstract and opening match 1993 paper"),
        relation("lineage_intermodulation_frequency_design_unresolved_year", "lineage_cumcm_1993_a_intermodulation_frequency_design", "resolved_alias", "official 1993 statement plus identical formulas/results resolve contest year"),
        relation(rep_lookup[(A_PROBLEM, old_docs[A_PROBLEM]["carrier_document_ids"][0])], rep_lookup[(A_PROBLEM, combined_carrier)], "duplicate_representation_of", "same A problem tasks and numerical constraints"),
        relation(rep_lookup[(B_PROBLEM, old_docs[B_PROBLEM]["carrier_document_ids"][0])], rep_lookup[(B_PROBLEM, combined_carrier)], "duplicate_representation_of", "same B problem tasks and score matrix"),
    ]
    write_jsonl(REL / "document_relations.jsonl", sorted(relations, key=lambda r: r["relation_id"]))

    lineages = [r for r in read_jsonl(REL / "solution_lineages.jsonl") if int(r.get("contest_year") or 0) != 1993 and r.get("lineage_id") != "lineage_intermodulation_frequency_design_unresolved_year"]
    lineages += [
        {"lineage_id": "lineage_intermodulation_frequency_design_unresolved_year", "contest_year": 0, "carrier_year": 1992,
         "problem_code": "A", "primary_paper": None, "paper_representations": [], "commentaries": [INTERMOD_1992],
         "problem_statement": [], "validation_summaries": [], "partial_segments": [top_orphan["segment_id"]],
         "unresolved_members": [], "canonical_solution_description": "Historical provisional identifier resolved to the canonical 1993 A lineage.",
         "status": "resolved_alias", "resolved_to": "lineage_cumcm_1993_a_intermodulation_frequency_design", "manual_overrides": True},
        {"lineage_id": "lineage_cumcm_1993_a_intermodulation_frequency_design", "contest_year": 1993, "problem_code": "A",
         "primary_paper": A_PAPER, "paper_representations": [rep_lookup[(A_PAPER, old_docs[A_PAPER]["carrier_document_ids"][0])]],
         "commentaries": [INTERMOD_1992], "problem_statement": [A_PROBLEM], "validation_summaries": [],
         "partial_segments": [top_orphan["segment_id"]], "unresolved_members": [],
         "canonical_solution_description": "三次多项式拟合、整数频率枚举、接收带/SNR筛选及稳定性定理。", "status": "verified", "manual_overrides": True},
        {"lineage_id": "lineage_cumcm_1993_b_football_ranking", "contest_year": 1993, "problem_code": "B",
         "primary_paper": B_PAPER, "paper_representations": [rep_lookup[(B_PAPER, b_carrier)]], "commentaries": [B_COMMENTARY],
         "problem_statement": [B_PROBLEM], "validation_summaries": [],
         "partial_segments": [next(o["segment_id"] for o in orphans if o.get("detected_title") == "一个给足球队排名次的方法——B题")],
         "unresolved_members": [], "canonical_solution_description": "以AHP互反判断矩阵的主特征向量排名，并处理残缺数据与可靠度。",
         "status": "verified", "manual_overrides": True}]
    write_jsonl(REL / "solution_lineages.jsonl", lineages)
    write_year_relation_views()

    write_jsonl(QUALITY / "unresolved" / "1993_manual_review_queue.jsonl", [])
    write_jsonl(QUALITY / "unresolved" / "1992_manual_review_queue.jsonl", [])

    feedback = [r for r in read_jsonl(CAT / "reviewer_feedback_catalog.jsonl") if not str(r.get("feedback_id", "")).startswith("feedback_1993_")]
    feedback += [
        {"feedback_id": "feedback_1993_ranking_assumptions", "commentary_id": B_COMMENTARY, "problem_id": "problem_cumcm_1993_b", "solution_lineage_id": "lineage_cumcm_1993_b_football_ranking", "review_dimension": "assumptions", "praised_or_criticized": "criterion", "normalized_feedback": "先判断模型假设是否合理。", "recommended_improvement": "在建模前明确实力、赛果和随机波动假设。", "severity": "major", "source_page": 2, "source_bbox": [], "evidence_status": "verified"},
        {"feedback_id": "feedback_1993_ranking_generality", "commentary_id": B_COMMENTARY, "problem_id": "problem_cumcm_1993_b", "solution_lineage_id": "lineage_cumcm_1993_b_football_ranking", "review_dimension": "generality", "praised_or_criticized": "criterion", "normalized_feedback": "结果要符合实际并具有一般性。", "recommended_improvement": "避免只对给定赛果有效的特制算法。", "severity": "major", "source_page": 2, "source_bbox": [], "evidence_status": "verified"},
        {"feedback_id": "feedback_1993_ranking_ahp", "commentary_id": B_COMMENTARY, "problem_id": "problem_cumcm_1993_b", "solution_lineage_id": "lineage_cumcm_1993_b_football_ranking", "review_dimension": "model_completeness", "praised_or_criticized": "praised", "normalized_feedback": "AHP方案理论分析和因素讨论较完整。", "recommended_improvement": "保留完整证据链而非只给名次。", "severity": "important", "source_page": 2, "source_bbox": [], "evidence_status": "verified"},
    ]
    write_jsonl(CAT / "reviewer_feedback_catalog.jsonl", feedback)

    vis_path = CAT / "visualization_catalog.csv"
    old_vis = []
    if vis_path.exists():
        with vis_path.open(encoding="utf-8-sig", newline="") as fh: old_vis = [r for r in csv.DictReader(fh) if r.get("logical_document_id") not in {A_PAPER, B_PAPER}]
    new_vis = [
        {"logical_document_id": A_PAPER, "figure_or_table_id": "input_output_table", "page": 1, "bbox": "", "chart_type": "table", "purpose": "show nonlinear system data", "supports_question": "A", "supports_claim": "least-squares input", "effective": "yes", "reusable_pattern": "model-input table", "evidence_status": "verified", "representation_id": rep_lookup[(A_PAPER, old_docs[A_PAPER]["carrier_document_ids"][0])]},
        {"logical_document_id": A_PAPER, "figure_or_table_id": "frequency_candidates_table", "page": 4, "bbox": "", "chart_type": "table", "purpose": "show six constraint-feasible triples", "supports_question": "A", "supports_claim": "screening result", "effective": "yes", "reusable_pattern": "candidate solution table", "evidence_status": "verified", "representation_id": rep_lookup[(A_PAPER, old_docs[A_PAPER]["carrier_document_ids"][0])]},
        {"logical_document_id": B_PAPER, "figure_or_table_id": "counterexample_matrices", "page": 9, "bbox": "", "chart_type": "matrix_diagram", "purpose": "show ranking instability under small structural changes", "supports_question": "B", "supports_claim": "model limitation", "effective": "yes", "reusable_pattern": "counterexample matrix pair", "evidence_status": "verified", "representation_id": rep_lookup[(B_PAPER, b_carrier)]},
    ]
    with vis_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(new_vis[0]), lineterminator="\n"); writer.writeheader(); writer.writerows(old_vis + new_vis)

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "1993_report.md").write_text("""# 1993年重建人工核验报告

> 依据相同原始基线重新构建。统计按carrier、logical document、unique problem和solution lineage分开。

## 构成

- 物理载体：6；logical documents：5；representations：7。
- 参赛论文：2；专家评注：1；canonical problem statements：2。
- 题面物理载体：3（A独立、B独立、A/B合卷）；唯一赛题：2。
- 独立解题方案：2。

## 身份纠错与载体归并

“A题优秀论文①”实际为A题题面；“B题优秀论文②”实际为B题题面。官方合卷的两页分别归入同一A/B canonical logical document，保留为第二representation，不重复计算赛题。

## 论文模式（n=2）

A题用最小二乘三次多项式、整数枚举和接收带/SNR筛选，最后由稳定性分析和充分必要条件定理收束。B题用互反判断矩阵、Perron–Frobenius主特征向量、残缺数据处理和χ²可依赖度形成排名证据链。

两篇均有摘要、显式假设、符号定义、模型检验、最终方案和算法说明：2/2（100.0%）。明确最终答案汇总表和流程图均为0/2（0.0%）。

## 跨年谱系结论

1992载体中的非线性交调评注与1993 A题论文在三次输入输出模型、σ=6约束、6组候选和最终两组频率上逐项对应；结合1993官方题面，谱系解析为 `lineage_cumcm_1993_a_intermodulation_frequency_design`。旧unresolved ID保留为resolved alias，不删除历史记录。

1993 B题论文首页上半是该评注末段的局部副本，下半才是足球排名论文；边界为PDF点坐标y=360。1992载体中足球文章开篇片段也已反向匹配到该论文。
""", encoding="utf-8")
    (REPORTS / "1993_data_quality.md").write_text("""# 1993数据质量

| 项目 | 结果 |
|---|---|
| carriers | 6/6有状态 |
| logical documents | 5/5人工核验 |
| representations | 7，两个canonical题面各2个表示 |
| same-page boundaries | 1，B题论文首页y=360 |
| role corrections | 2个“优秀论文”文件纠正为题面；合卷拆成2个题面表示 |
| parsed / verified | A题论文及两个题面 |
| partially_parsed / key_content_verified | B题扫描论文、B题扫描评注 |
| unresolved cross-year lineage | 0，非线性交调谱系已解析 |

扫描件没有完整中文文本层，故即使关键页均视觉核验，也不提升为全文parsed。
""", encoding="utf-8")
    remove_absorbed_candidate_bundle()


if __name__ == "__main__":
    main()
