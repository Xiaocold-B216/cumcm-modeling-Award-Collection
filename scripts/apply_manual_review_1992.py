#!/usr/bin/env python3
"""Apply the visually verified 1992 review without publishing full article text.

This script only writes derived files under analysis-index.  It is idempotent and
keeps stable logical-document/carrier identifiers created by build_index.py.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
DOCS = AI / "02_documents"
CARDS = DOCS / "cards"
REL = AI / "04_relations"
CAT = AI / "05_catalogs"
REPORTS = AI / "07_reports" / "yearly"
QUALITY = AI / "08_quality"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def stable(prefix: str, *parts: Any) -> str:
    return prefix + hashlib.sha256("\x1f".join(map(str, parts)).encode()).hexdigest()[:16]


def evidence(doc_id: str, page: int, section: str, kind: str, excerpt: str, claim: str,
             bbox: list[float] | None = None, confidence: float = 0.98) -> dict[str, Any]:
    return {
        "logical_document_id": doc_id,
        "paper_id": doc_id if SPECS[doc_id]["role"] == "award_paper" else None,
        "source_page": page,
        "source_section": section,
        "source_bbox": bbox or [],
        "evidence_type": kind,
        "text_excerpt": excerpt,
        "normalized_claim": claim,
        "confidence": confidence,
        "extraction_method": "manual_visual_review_with_native_text" if SPECS[doc_id]["text"] else "manual_visual_review",
        "manual_review_required": False,
    }


FEATURES = {
    "abstract": "structure_statistics",
    "model_assumptions": "structure_statistics",
    "symbol_definitions": "structure_statistics",
    "model_validation": "model_statistics",
    "sensitivity_analysis": "model_statistics",
    "error_analysis": "model_statistics",
    "final_solution": "result_pattern_statistics",
    "final_answer_summary_table": "result_pattern_statistics",
    "flowchart": "visualization_statistics",
    "visualization": "visualization_statistics",
    "references": "structure_statistics",
    "appendix": "structure_statistics",
    "code_description": "structure_statistics",
}


def fstats(role: str, values: dict[str, tuple[str, list[int]]]) -> list[dict[str, Any]]:
    rows = []
    for field, category in FEATURES.items():
        if role != "award_paper":
            status, pages = "not_applicable", []
            reason = "award-paper feature is outside this document role"
            eligible = False
            value = None
        else:
            status, pages = values.get(field, ("unknown", []))
            eligible = status in {"present", "absent"}
            value = True if status == "present" else False if status == "absent" else None
            reason = "manually verified from complete valid article region" if eligible else "insufficient evidence"
        rows.append({
            "field_name": field, "value": value, "value_status": status,
            "evidence_status": "verified" if eligible else "content_verified_partial",
            "source_pages": pages, "source_bbox": [], "analysis_category": category,
            "eligible_for_statistics": eligible, "exclusion_reason": "" if eligible else reason,
        })
    return rows


SPECS: dict[str, dict[str, Any]] = {
    "logical_4d1c1c5a662b313f": {
        "key": "d01", "role": "expert_commentary", "title": "关于施肥效果分析问题的评注",
        "authors": ["项可风"], "problem": "A", "problem_id": "problem_cumcm_1992_a",
        "lineage": "lineage_cumcm_1992_a_fertilization", "text": False,
        "parse": "partially_parsed", "evidence": "key_content_verified", "segmentation": "segmented",
        "models": ["experimental_design", "quadratic_regression"], "algorithms": [],
        "content": {
            "document_purpose": "评议施肥题答卷并指出试验设计缺陷。",
            "opening_structure": "阅卷背景—代表性答卷—三个主要问题—改进设计。",
            "review_findings": ["单因素轮换设计不能估计交互作用", "重复试验的区组效应不可忽略", "建议采用15次试验的二次复合设计"],
            "strengths": ["批评直接绑定设计矩阵与可估参数", "给出可执行的改进试验表"],
            "limitations": ["扫描文本层不可用", "主要针对实验设计，未复算代表论文全部回归结果"],
            "reproducibility_level": "medium",
        },
    },
    "logical_b5ebbd7404ae15a9": {
        "key": "d02", "role": "award_paper", "title": "施肥方案对作物、蔬菜的影响",
        "authors": ["喻梅", "金青松", "唐福明"], "problem": "A", "problem_id": "problem_cumcm_1992_a",
        "lineage": "lineage_cumcm_1992_a_fertilization", "text": True,
        "parse": "partially_parsed", "evidence": "key_content_verified", "segmentation": "segmented",
        "models": ["multiple_quadratic_regression", "stepwise_regression", "quadratic_response_surface"],
        "algorithms": ["least_squares_estimation", "stepwise_variable_selection"],
        "features": {
            "abstract": ("present", [1]), "model_assumptions": ("present", [2]),
            "symbol_definitions": ("present", [2]), "model_validation": ("present", [3, 4]),
            "sensitivity_analysis": ("present", [4, 5]), "error_analysis": ("absent", [1, 2, 3, 4, 5, 6]),
            "final_solution": ("present", [1, 4]), "final_answer_summary_table": ("absent", [1, 2, 3, 4, 5, 6]),
            "flowchart": ("absent", [1, 2, 3, 4, 5, 6]), "visualization": ("present", [1, 3, 4]),
            "references": ("present", [6]), "appendix": ("absent", [1, 2, 3, 4, 5, 6]),
            "code_description": ("absent", [1, 2, 3, 4, 5, 6]),
        },
        "content": {
            "problem_and_subproblems": ["建立土豆和生菜产量—N/P/K施肥量关系", "给出最优施肥组合", "评价应用价值并提出改进"],
            "data_types": ["连续数值", "两作物各30组单因素试验数据"],
            "mathematical_essence": "多元二次回归、变量交互与响应面优化。",
            "data_preprocessing": ["中心化与标准化", "用VIF诊断共线性后作相关变换"],
            "baseline_models": ["全回归"], "core_models": ["逐步回归", "二次响应面回归"],
            "parameter_sources": ["试验数据", "SAS/STAT回归估计"],
            "validation_methods": ["VIF", "方差分析F检验", "残差散点检查", "95%预测区间", "决定系数"],
            "important_results": ["土豆N/P/K=292/246/542 kg/ha，预测产量45.18 t/ha", "生菜N/P/K=213/667/427 kg/ha，预测产量23.13 t/ha"],
            "abstract_structure": "对象与模型—统计分析—两作物比较—最优施肥量与产量。",
            "section_structure": ["问题重述", "假设", "模型建立与分析", "应用分析", "优缺点与改进"],
            "innovation_expression": "比较三类回归并把响应面导数用于边际产量和投入组合分析。",
            "strengths": ["模型、检验和应用解释闭环", "给出明确数值方案"],
            "limitations": ["原试验设计不能独立估计全部交互项", "未显式建模区组效应", "无代码或SAS脚本"],
            "reproducibility_level": "medium",
        },
    },
    "logical_096f6338555ccb87": {
        "key": "d03", "role": "expert_commentary", "title": "关于“非线性交调的频率设计”的评注——A题的解答和有关情况",
        "authors": ["谢衷洁"], "problem": "A", "problem_id": None,
        "lineage": "lineage_intermodulation_frequency_design_unresolved_year", "text": True,
        "parse": "parsed", "evidence": "verified", "segmentation": "segmented",
        "models": ["polynomial_input_output_model", "fourier_analysis", "frequency_configuration"],
        "algorithms": ["enumeration_under_frequency_constraints", "snr_screening"],
        "content": {
            "document_purpose": "说明非线性交调题的背景、参考解、稳定性与阅卷观察。",
            "review_findings": ["不能把大量候选完全交给软件而缺少数学分析", "规划模型必须明确目标函数", "工程允许区间不能任意改动", "鼓励数学与工程背景协作"],
            "key_results": ["频率约束得到6组初配", "SNR筛选后保留(36,42,55)与(36,49,55)"],
            "strengths": ["公式推导、工程解释和评审标准结合"],
            "limitations": ["真实竞赛年份须与1993同题文档交叉核验"],
            "reproducibility_level": "medium_high",
        },
    },
    "logical_8b702cd539a61ed3": {
        "key": "d04", "role": "problem_statement", "title": "1992年A题：施肥效果分析",
        "authors": [], "problem": "A", "problem_id": "problem_cumcm_1992_a",
        "lineage": None, "text": True, "parse": "parsed", "evidence": "verified", "segmentation": "not_required",
        "models": [], "algorithms": [],
        "content": {"subproblems": ["分析N/P/K施肥量与土豆、生菜产量关系", "评价应用价值和改进方向"],
                    "inputs": ["两作物的施肥量与产量表"], "outputs": ["关系模型", "应用评价"],
                    "constraints": ["改变一种营养素时另两种保持第7水平"], "data_attachments": "题面内嵌表格"},
    },
    "logical_c246cf980eced8f6": {
        "key": "d05", "role": "problem_statement", "title": "1992年B题：实验数据分解",
        "authors": [], "problem": "B", "problem_id": "problem_cumcm_1992_b",
        "lineage": None, "text": True, "parse": "parsed", "evidence": "verified", "segmentation": "not_required",
        "models": [], "algorithms": [],
        "content": {"subproblems": ["分解给定分子量X为18种氨基酸分子量之和", "分别讨论有无微型计算机", "推广到一般情形"],
                    "inputs": ["18个已知分子量", "正整数X≤1000"], "outputs": ["全部可行组成", "一般模型与方法"],
                    "constraints": ["非负整数个数", "分子量加和等于X"], "data_attachments": "题面内嵌数列"},
    },
    "logical_33abe6eb835f81d8": {
        "key": "d06", "role": "award_paper", "title": "蛋白质氨基酸的组合问题",
        "authors": ["程龙", "张云军", "赵蕊"], "problem": "B", "problem_id": "problem_cumcm_1992_b",
        "lineage": "lineage_cumcm_1992_b_amino_acid", "text": True,
        "parse": "partially_parsed", "evidence": "key_content_verified", "segmentation": "not_required",
        "models": ["nonnegative_integer_equation", "constrained_enumeration", "models_A_to_F"],
        "algorithms": ["depth_first_search", "branch_pruning", "variable_reduction"],
        "features": {
            "abstract": ("present", [1]), "model_assumptions": ("present", [2]),
            "symbol_definitions": ("present", [2]), "model_validation": ("present", [3, 4, 5, 6, 7]),
            "sensitivity_analysis": ("absent", [1, 2, 3, 4, 5, 6, 7, 8, 9]), "error_analysis": ("present", [8]),
            "final_solution": ("present", [7, 8]), "final_answer_summary_table": ("absent", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            "flowchart": ("absent", [1, 2, 3, 4, 5, 6, 7, 8, 9]), "visualization": ("present", [3, 4, 5, 6, 7, 9]),
            "references": ("present", [9]), "appendix": ("present", [9]), "code_description": ("present", [2, 3]),
        },
        "content": {
            "problem_and_subproblems": ["求非负整数方程的全部解", "利用化学信息缩小解空间", "分别设计有/无微机方案"],
            "data_types": ["整数", "氨基酸分子量", "元素组成约束"],
            "mathematical_essence": "一元总量约束下的高维非负整数可行解枚举。",
            "data_preprocessing": ["合并等分子量氨基酸", "减去已知必含成分", "按元素组成减少变量"],
            "baseline_models": ["18变量非负整数方程"], "core_models": ["加入C/N/O/H守恒的模型A", "利用已知氨基酸集合的模型B/C", "0-1简化模型D", "仪器信息模型E/F"],
            "parameter_sources": ["题给18种分子量", "文献中的元素组成", "经验含氮比例15%—17%"],
            "validation_methods": ["多组X的解数和运行时间对比", "不同约束模型的并列表格"],
            "important_results": ["X=1000时一般模型有28268解", "加入含氮约束后降为10954解", "模型F在可获得比例信息时可给出唯一解"],
            "abstract_structure": "问题—一般模型规模—模型A至F—测试—全文结构。",
            "section_structure": ["问题提出与分析", "假设和符号", "一般模型", "改进模型A—F", "改进方向", "误差与优缺点"],
            "innovation_expression": "把化学元素守恒、已知组分和仪器信息逐层转化为约束。",
            "strengths": ["基线与逐层约束对比清楚", "运行时间和解数均有测试"],
            "limitations": ["X=1000时改进后解数仍多", "部分经验约束可能不真实", "未公开程序源代码"],
            "reproducibility_level": "medium",
        },
    },
    "logical_7f58eb5c45b19366": {
        "key": "d07", "role": "expert_commentary", "title": "关于“蛋白质氨基酸的组合问题”的评注",
        "authors": ["韩继业"], "problem": "B", "problem_id": "problem_cumcm_1992_b",
        "lineage": "lineage_cumcm_1992_b_amino_acid", "text": True,
        "parse": "parsed", "evidence": "verified", "segmentation": "not_required",
        "models": ["large_scale_discrete_optimization", "constrained_enumeration"], "algorithms": ["enumeration", "constraint_reduction"],
        "content": {
            "document_purpose": "介绍代表性答卷，并讨论大规模离散问题的约束化求解。",
            "review_findings": ["单纯枚举在X=1000时产生28268个解", "化学约束可减至10954个解", "还需进一步删除无实际意义解", "大规模离散问题应增加充分约束"],
            "visual_evidence": "第2页四幅偏差分析图承接正文并由页末总结说明，属于本评注。",
            "strengths": ["用解空间规模量化方法改进", "把竞赛答卷放入离散优化背景"],
            "limitations": ["评注不是参赛论文，不进入award-paper字段分母"],
            "reproducibility_level": "medium",
        },
    },
}


EVIDENCE_SPECS: dict[str, list[tuple[int, str, str, str, str, list[float] | None]]] = {
    "logical_4d1c1c5a662b313f": [
        (1, "标题与开篇", "identity", "关于施肥效果分析问题的评注", "身份为专家评注", [0, 515, 588, 792]),
        (2, "一、多因素轮换法试验", "review_feedback", "不可能估计交互作用", "指出原设计无法估计交互作用", None),
        (2, "二、区组效应", "review_feedback", "区组效应不可忽视", "指出重复试验外界差异形成区组效应", None),
        (3, "三、试验设计的改进", "table", "15个试验设计点", "给出二次复合设计的15次试验表", None),
        (3, "三、试验设计的改进", "formula", "ΔN=80，ΔP=50，ΔK=100", "给出复合设计步长", None),
    ],
    "logical_b5ebbd7404ae15a9": [
        (1, "摘要", "identity", "施肥方案对作物、蔬菜的影响", "身份为1992 A题参赛论文", None),
        (1, "摘要", "result", "N/P/K为292、246、542", "土豆最优施肥量及预测产量45.18 t/ha", None),
        (1, "摘要", "result", "N/P/K为213、667、427", "生菜最优施肥量及预测产量23.13 t/ha", None),
        (2, "二、假设", "assumption", "各次实验独立", "列出误差正态与观测无误差等显式假设", None),
        (2, "三、模型建立与模型分析", "formula", "多元二次回归模型", "核心模型包含平方项与交互项", None),
        (3, "全回归", "validation", "F检验P值为0.0001", "用F检验、VIF和残差检查模型适度性", None),
        (4, "二次响应面回归", "validation", "R²为95.9%和92.8%", "报告两作物响应面拟合度", None),
        (4, "表3", "table", "因子分析", "表格比较N/P/K影响", None),
        (5, "四、模型的应用分析", "sensitivity", "边际产量方程", "用偏导数分析边际产量与敏感顺序", None),
        (6, "五、模型优缺点与改进", "limitation", "仅考虑了施肥量影响", "作者明确说明遗漏植株密度、气候等因素", [0, 0, 588, 515]),
    ],
    "logical_096f6338555ccb87": [
        (1, "标题与问题背景", "identity", "非线性交调的频率设计", "身份为评注而非参赛论文", None),
        (2, "频率约束下的初步配置", "result", "可以选出满足频率约束的6组解", "频率约束产生6组初配", None),
        (3, "信噪比SNR计算", "formula", "Fourier分析", "用Fourier系数推导交调幅度", None),
        (4, "本题的频率设计", "result", "只有二组：(36,42,55)和(36,49,55)", "SNR筛选保留两组频率", None),
        (5, "答卷印象", "review_feedback", "目标函数没有给出很好的数学表达", "批评只依赖软件和目标函数不清", [0, 0, 607, 360]),
        (5, "同页下篇标题", "boundary", "一个给足球队排名次的方法——B题", "页内切换到另一独立文章", [0, 360, 607, 798]),
    ],
    "logical_8b702cd539a61ed3": [
        (1, "题面", "identity", "1992年题A 施肥效果分析", "身份为A题题面", None),
        (1, "题面表格", "input_data", "土豆与生菜", "输入为两作物N/P/K施肥量和产量表", None),
        (1, "任务", "problem_requirement", "分析施肥量与生产量之间关系", "要求建模并评价应用与改进", None),
    ],
    "logical_c246cf980eced8f6": [
        (1, "题面", "identity", "1992年题B 实验数据分解", "身份为B题题面", None),
        (1, "输入", "input_data", "n=18，X≤1000", "给出18个分子量及整数上界", None),
        (1, "任务", "problem_requirement", "拥有或不拥有微型计算机", "要求分别提出解法并推广", None),
    ],
    "logical_33abe6eb835f81d8": [
        (1, "摘要", "identity", "蛋白质氨基酸的组合问题", "身份为1992 B题参赛论文", None),
        (1, "二、问题的分析", "formula", "Σa_i x_i=X", "问题建模为非负整数方程", None),
        (2, "三、模型假设", "assumption", "列出7项模型假设", "明确假设分子量、氨基酸集合与仪器条件", None),
        (2, "四、最一般的模型", "algorithm", "采用了深度优先算法", "用深度优先枚举解空间", None),
        (3, "表1", "result", "X=1000时有28268个解", "一般模型解空间过大", None),
        (3, "模型A", "formula", "加入元素组成约束", "利用C/N/O/H守恒减少解", None),
        (6, "表4", "table", "解的个数与运行时间", "多组数据对比约束模型", None),
        (7, "模型F", "result", "解是唯一的", "比例信息充分时模型F可得到唯一解", None),
        (8, "模型的误差分析", "error_analysis", "X和a_i的测量误差", "讨论输入测量误差及含氮比例区间", None),
        (9, "模型的缺点", "limitation", "X=1000时给出了28268个解", "明确承认解数仍过多和约束真实性风险", None),
    ],
    "logical_7f58eb5c45b19366": [
        (1, "摘要与开篇", "identity", "关于蛋白质氨基酸的组合问题的评注", "身份为专家评注", None),
        (1, "评议", "review_feedback", "28268个解", "指出无约束枚举规模过大", None),
        (1, "评议", "review_feedback", "从28268减为10954", "肯定元素约束缩小解空间", None),
        (2, "离散数学讨论", "review_feedback", "充分补充的约束条件", "建议用更多有效约束删除无意义解", None),
        (2, "第13—16题图", "figure", "四幅偏差分析图", "图形属于评注并支持稳定性/偏差讨论", None),
        (2, "页末总结", "boundary", "上面给出了七种进行偏差分析的方法", "图后文字承接评注，未发现新文章边界", None),
    ],
}


def corpus(role: str) -> dict[str, str]:
    keys = ["award_paper_patterns", "reviewer_feedback", "problem_analysis", "validation_patterns", "visualization_patterns"]
    out = {key: "excluded" for key in keys}
    if role == "award_paper":
        out["award_paper_patterns"] = out["visualization_patterns"] = "included"
    elif role == "expert_commentary":
        out["reviewer_feedback"] = "included"
    elif role == "problem_statement":
        out["problem_analysis"] = "included"
    return out


def page_dimensions(old_map: dict[str, Any]) -> dict[int, tuple[float, float, int]]:
    return {p["page"]: (p["width"], p["height"], p.get("rotation", 0)) for p in old_map["pages"]}


def main() -> None:
    docs_1992 = {d["logical_document_id"]: d for d in read_jsonl(DOCS / "logical_documents_1992.jsonl")}
    reps_old = {r["logical_document_id"]: r for r in read_jsonl(DOCS / "representations_1992.jsonl")}
    if set(docs_1992) != set(SPECS):
        raise SystemExit(f"1992 logical-document IDs differ: {set(docs_1992) ^ set(SPECS)}")

    new_docs: list[dict[str, Any]] = []
    new_segments: list[dict[str, Any]] = []
    new_reps: list[dict[str, Any]] = []
    new_boundaries: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for doc_id, spec in SPECS.items():
        old = docs_1992[doc_id]
        old_map = json.loads((CARDS / doc_id / "page_map.json").read_text(encoding="utf-8"))
        dims = page_dimensions(old_map)
        page_bboxes: dict[int, list[float]] = {p: [0, 0, w, h] for p, (w, h, _r) in dims.items()}
        exclusions: dict[int, list[float]] = {}
        if spec["key"] == "d01":
            page_bboxes[1] = [0, 515, 588, 792]; exclusions[1] = [0, 0, 588, 515]
        elif spec["key"] == "d02":
            page_bboxes[6] = [0, 0, 588, 515]; exclusions[6] = [0, 515, 588, 792]
        elif spec["key"] == "d03":
            page_bboxes[5] = [0, 0, 607, 360]; exclusions[5] = [0, 360, 607, 798]

        segment_ids = []
        for page in sorted(dims):
            w, h, rotation = dims[page]
            bbox = page_bboxes[page]
            sid = stable("segment_", doc_id, page, *bbox, "manual-1992")
            segment_ids.append(sid)
            new_segments.append({
                "segment_id": sid, "carrier_document_id": old["carrier_document_ids"][0],
                "logical_document_id": doc_id, "page": page, "include_bbox": bbox,
                "exclude_bbox": [exclusions[page]] if page in exclusions else [],
                "normalized_bbox": [round(bbox[0]/w, 6), round(bbox[1]/h, 6), round(bbox[2]/w, 6), round(bbox[3]/h, 6)],
                "page_width": w, "page_height": h, "page_rotation": rotation,
                "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
                "reason": "manually verified valid article region", "segmentation_status": spec["segmentation"],
                "manually_verified": True,
            })
        if exclusions:
            for page, bbox in exclusions.items():
                w, h, rotation = dims[page]
                orphan_id = stable("orphan_", old["carrier_document_ids"][0], page, *bbox)
                match = None
                detected = None
                status = "unmatched_partial"
                probable = "unknown"
                if spec["key"] == "d01":
                    match = "logical_b5ebbd7404ae15a9"; detected = "施肥方案对作物、蔬菜的影响（结尾）"; status = "matched"; probable = "award_paper"
                elif spec["key"] == "d02":
                    match = "logical_4d1c1c5a662b313f"; detected = "关于施肥效果分析问题的评注（开篇）"; status = "matched"; probable = "expert_commentary"
                elif spec["key"] == "d03":
                    detected = "一个给足球队排名次的方法——B题"; probable = "award_paper"
                excluded.append({
                    "segment_id": orphan_id, "carrier_document_id": old["carrier_document_ids"][0],
                    "page": page, "bbox": bbox,
                    "normalized_bbox": [round(bbox[0]/w, 6), round(bbox[1]/h, 6), round(bbox[2]/w, 6), round(bbox[3]/h, 6)],
                    "page_width": w, "page_height": h, "page_rotation": rotation,
                    "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
                    "detected_title": detected, "probable_role": probable, "matched_document_id": match,
                    "match_status": status, "preservation_status": "preserved_metadata_and_bbox",
                    "reason_excluded_from_primary_document": "same-page article boundary verified visually",
                    "manual_overrides": True,
                })

        role = spec["role"]
        analysis_categories = {"metadata_statistics"}
        if role == "award_paper":
            analysis_categories |= {"structure_statistics", "model_statistics", "algorithm_statistics", "visualization_statistics", "result_pattern_statistics"}
        elif role == "expert_commentary":
            analysis_categories.add("reviewer_feedback_statistics")
        elif role == "problem_statement":
            analysis_categories.add("problem_analysis")
        doc = {
            **old, "title": spec["title"], "authors": spec["authors"], "problem_code": spec["problem"],
            "problem_id": spec["problem_id"], "solution_lineage_id": spec["lineage"],
            "document_role": role, "document_subtype": "none",
            "role_classification": {"predicted_role": role, "confidence": 1.0,
                "classification_basis": ["title", "document_structure", "first_page_text", "visual_review"],
                "conflicting_signals": ["filename says 优秀论文 but content is a problem statement"] if role == "problem_statement" else [],
                "manually_verified": True},
            "corpus_eligibility": corpus(role), "parse_status": spec["parse"],
            "evidence_status": spec["evidence"], "segmentation_status": spec["segmentation"],
            "completeness_status": "complete", "corpus_status": "included",
            "representation_quality": "manually_reviewed", "analysis_eligibility": sorted(analysis_categories),
            "feature_statistics": fstats(role, spec.get("features", {})),
            "models": spec["models"], "algorithms": spec["algorithms"], "segment_ids": segment_ids,
            "manual_overrides": True, "manual_reviewed_at": "2026-07-22T00:00:00Z",
            "content_analysis": spec["content"],
        }
        new_docs.append(doc)

        old_rep = reps_old[doc_id]
        new_reps.append({
            **old_rep, "segment_ids": segment_ids, "page_coverage": sorted(dims), "completeness": "complete",
            "visual_quality": "good", "text_layer_quality": "native_text_reviewed" if spec["text"] else "scan_visual_only",
            "table_quality": "verified_key_tables", "formula_quality": "verified_key_formulas",
            "page_order_quality": "verified", "contamination_level": "cropped_same_page_content" if exclusions else "none_detected",
            "preferred_representation": True, "preference_reason": "only complete carrier representation; valid regions manually verified",
            "manual_overrides": True,
        })

        ev_rows = [evidence(doc_id, *row) for row in EVIDENCE_SPECS[doc_id]]
        card_dir = CARDS / doc_id
        write_json(card_dir / "metadata.json", doc)
        page_map = {"logical_document_id": doc_id, "page_number_basis": "carrier-local, 1-based",
                    "representation_id": old_rep["representation_id"], "coordinate_origin": "top-left",
                    "coordinate_unit": "PDF point", "pages": []}
        for page, (w, h, rotation) in sorted(dims.items()):
            source_page = next(p for p in old_map["pages"] if p["page"] == page)
            page_map["pages"].append({**source_page, "valid_bbox": page_bboxes[page],
                                      "excluded_bbox": [exclusions[page]] if page in exclusions else [],
                                      "segment_id": segment_ids[page-1], "manually_verified": True})
        write_json(card_dir / "page_map.json", page_map)
        write_jsonl(card_dir / "evidence.jsonl", ev_rows)
        status_line = f"{doc['parse_status']} / {doc['evidence_status']} / {doc['completeness_status']}"
        model_text = "、".join(spec["models"]) or "不适用"
        (card_dir / "document_card.md").write_text(
            f"# {spec['title']}\n\n- 年份：1992\n- 角色：{role}\n- 状态：{status_line}\n"
            f"- 题号：{spec['problem']}\n- 核心模型：{model_text}\n- 方案谱系：{spec['lineage'] or '不适用'}\n\n"
            "## 人工核验摘要\n\n" + json.dumps(spec["content"], ensure_ascii=False, indent=2) +
            "\n\n> 仅保存结构化短摘要和页码证据；完整提取正文为本地忽略缓存。\n", encoding="utf-8")
        checks = ["标题和身份", "文章边界", "摘要或开篇", "核心模型或评议对象", "关键公式", "关键表格或图", "最终结论", "重要数字"]
        (card_dir / "review_record.md").write_text(
            "# Review record\n\n" + f"- logical_document_id: `{doc_id}`\n- reviewer: manual_visual_review\n"
            + "".join(f"- {item}: verified\n" for item in checks)
            + f"- full_text_status: {'native text plus visual sampling' if spec['text'] else 'visual review; Chinese OCR unavailable'}\n"
            + "- manually_verified: true\n", encoding="utf-8")

    new_docs.sort(key=lambda d: d["article_order"])
    write_jsonl(DOCS / "logical_documents_1992.jsonl", new_docs)
    all_docs = [d for d in read_jsonl(DOCS / "logical_documents.jsonl") if int(d.get("year", 0)) != 1992] + new_docs
    write_jsonl(DOCS / "logical_documents.jsonl", sorted(all_docs, key=lambda d: (int(d.get("year", 0)), d["logical_document_id"])))
    write_jsonl(DOCS / "page_segments_1992.jsonl", new_segments)
    write_jsonl(DOCS / "representations_1992.jsonl", new_reps)

    for doc_id, page, y, before, after in [
        ("logical_4d1c1c5a662b313f", 1, 515, "fertilization paper ending", "fertilization commentary opening"),
        ("logical_b5ebbd7404ae15a9", 6, 515, "fertilization paper ending", "fertilization commentary opening"),
        ("logical_096f6338555ccb87", 5, 360, "intermodulation commentary ending", "football ranking paper opening"),
    ]:
        carrier = docs_1992[doc_id]["carrier_document_ids"][0]
        new_boundaries.append({
            "boundary_id": stable("boundary_", carrier, page, y), "logical_document_id": doc_id,
            "carrier_document_id": carrier, "before_page": page, "after_page": page,
            "same_page_boundary": True, "boundary_y": y,
            "boundary_bbox": [0, y, 588 if doc_id != "logical_096f6338555ccb87" else 607, 792 if doc_id != "logical_096f6338555ccb87" else 798],
            "normalized_bbox": [0, round(y/(792 if doc_id != "logical_096f6338555ccb87" else 798), 6), 1, 1],
            "page_width": 588 if doc_id != "logical_096f6338555ccb87" else 607,
            "page_height": 792 if doc_id != "logical_096f6338555ccb87" else 798,
            "page_rotation": 0, "evidence": f"visual title/layout transition: {before} -> {after}",
            "confidence": 0.99, "manually_verified": True, "manual_overrides": True,
        })
    write_jsonl(DOCS / "article_boundaries_1992.jsonl", new_boundaries)

    existing_orphans = [r for r in read_jsonl(DOCS / "orphan_segments.jsonl")
                        if r.get("carrier_document_id") not in {d["carrier_document_ids"][0] for d in new_docs}]
    write_jsonl(DOCS / "orphan_segments.jsonl", existing_orphans + excluded)

    def relrow(source: str, target: str, kind: str, ev: str, confidence: float = 0.99) -> dict[str, Any]:
        return {"relation_id": stable("relation_", source, kind, target), "year": 1992,
                "source_document_id": source, "target_document_id": target, "relation_type": kind,
                "evidence": ev, "confidence": confidence, "verified_by": "manual_visual_review",
                "status": "verified", "manual_overrides": True}

    relations = [r for r in read_jsonl(REL / "document_relations.jsonl") if int(r.get("year", 0)) != 1992]
    for d in new_docs:
        relations.append(relrow(d["carrier_document_ids"][0], d["logical_document_id"], "contains", "verified page map and valid bbox"))
    relations += [
        relrow("logical_b5ebbd7404ae15a9", "logical_8b702cd539a61ed3", "answers_problem", "A题数据和任务逐项对应"),
        relrow("logical_4d1c1c5a662b313f", "logical_b5ebbd7404ae15a9", "comments_on", "开篇点名该代表性答卷及作者"),
        relrow("logical_4d1c1c5a662b313f", "logical_b5ebbd7404ae15a9", "evaluates_solution", "逐项评价试验设计与回归可估性"),
        relrow("logical_4d1c1c5a662b313f", "logical_b5ebbd7404ae15a9", "same_solution_lineage", "同题且评注明确指向该解答"),
        relrow("logical_33abe6eb835f81d8", "logical_c246cf980eced8f6", "answers_problem", "18种分子量、X≤1000及有无微机任务对应"),
        relrow("logical_7f58eb5c45b19366", "logical_33abe6eb835f81d8", "comments_on", "标题及文中作者/模型内容对应"),
        relrow("logical_7f58eb5c45b19366", "logical_33abe6eb835f81d8", "evaluates_solution", "28268与10954等数值逐项对应"),
        relrow("logical_7f58eb5c45b19366", "logical_33abe6eb835f81d8", "same_solution_lineage", "同题且评注明确评价该模型系列"),
        relrow(excluded[0]["segment_id"], "logical_b5ebbd7404ae15a9", "partial_copy_of", "同一刊物第83页上半内容与论文末页一致"),
        relrow(excluded[1]["segment_id"], "logical_4d1c1c5a662b313f", "partial_copy_of", "同一刊物第83页下半内容与评注首页一致"),
        relrow("logical_b5ebbd7404ae15a9", "logical_4d1c1c5a662b313f", "adjacent_to", "共享刊物第83页并在y=515处分界"),
        relrow("logical_096f6338555ccb87", excluded[2]["segment_id"], "adjacent_to", "刊物第85页在y=360处切换标题"),
    ]
    write_jsonl(REL / "document_relations.jsonl", sorted(relations, key=lambda r: r["relation_id"]))

    old_lineages = [r for r in read_jsonl(REL / "solution_lineages.jsonl") if int(r.get("contest_year") or 0) not in {0, 1992}]
    lineages = [
        {"lineage_id": "lineage_cumcm_1992_a_fertilization", "contest_year": 1992, "problem_code": "A",
         "primary_paper": "logical_b5ebbd7404ae15a9", "paper_representations": [reps_old["logical_b5ebbd7404ae15a9"]["representation_id"]],
         "commentaries": ["logical_4d1c1c5a662b313f"], "problem_statement": ["logical_8b702cd539a61ed3"],
         "validation_summaries": [], "partial_segments": [excluded[0]["segment_id"], excluded[1]["segment_id"]],
         "unresolved_members": [], "canonical_solution_description": "用多元二次回归与响应面确定两作物施肥方案，并由专家评注检视试验设计。",
         "status": "verified", "manual_overrides": True},
        {"lineage_id": "lineage_cumcm_1992_b_amino_acid", "contest_year": 1992, "problem_code": "B",
         "primary_paper": "logical_33abe6eb835f81d8", "paper_representations": [reps_old["logical_33abe6eb835f81d8"]["representation_id"]],
         "commentaries": ["logical_7f58eb5c45b19366"], "problem_statement": ["logical_c246cf980eced8f6"],
         "validation_summaries": [], "partial_segments": [], "unresolved_members": [],
         "canonical_solution_description": "以非负整数方程为基线，逐层加入化学与仪器约束缩小氨基酸组合解空间。",
         "status": "verified", "manual_overrides": True},
        {"lineage_id": "lineage_intermodulation_frequency_design_unresolved_year", "contest_year": 0, "carrier_year": 1992, "problem_code": "A",
         "primary_paper": None, "paper_representations": [], "commentaries": ["logical_096f6338555ccb87"],
         "problem_statement": [], "validation_summaries": [], "partial_segments": [excluded[2]["segment_id"]],
         "unresolved_members": ["logical_096f6338555ccb87"],
         "canonical_solution_description": "非线性交调频率配置与SNR筛选；真实竞赛年份及对应论文待1993交叉核验。",
         "status": "unresolved", "manual_overrides": True},
    ]
    write_jsonl(REL / "solution_lineages.jsonl", old_lineages + lineages)

    CAT.mkdir(parents=True, exist_ok=True)
    feedback = [
        {"feedback_id": "feedback_1992_fertilization_interaction", "commentary_id": "logical_4d1c1c5a662b313f", "problem_id": "problem_cumcm_1992_a", "solution_lineage_id": "lineage_cumcm_1992_a_fertilization", "review_dimension": "experimental_design", "praised_or_criticized": "criticized", "normalized_feedback": "单因素轮换设计不能独立估计交互作用。", "recommended_improvement": "采用可估交互项的二次复合设计。", "severity": "major", "source_page": 2, "source_bbox": [], "evidence_status": "verified"},
        {"feedback_id": "feedback_1992_fertilization_block", "commentary_id": "logical_4d1c1c5a662b313f", "problem_id": "problem_cumcm_1992_a", "solution_lineage_id": "lineage_cumcm_1992_a_fertilization", "review_dimension": "experimental_design", "praised_or_criticized": "criticized", "normalized_feedback": "重复试验存在不可忽略的区组效应。", "recommended_improvement": "在模型中纳入区组效应。", "severity": "major", "source_page": 2, "source_bbox": [], "evidence_status": "verified"},
        {"feedback_id": "feedback_1992_intermodulation_software", "commentary_id": "logical_096f6338555ccb87", "problem_id": None, "solution_lineage_id": "lineage_intermodulation_frequency_design_unresolved_year", "review_dimension": "mathematical_reasoning", "praised_or_criticized": "criticized", "normalized_feedback": "不能用软件穷举替代数学分析。", "recommended_improvement": "先推导约束与筛选结构，再计算候选。", "severity": "major", "source_page": 5, "source_bbox": [0, 0, 607, 360], "evidence_status": "verified"},
        {"feedback_id": "feedback_1992_amino_constraints", "commentary_id": "logical_7f58eb5c45b19366", "problem_id": "problem_cumcm_1992_b", "solution_lineage_id": "lineage_cumcm_1992_b_amino_acid", "review_dimension": "constraint_quality", "praised_or_criticized": "praised", "normalized_feedback": "化学约束显著缩小离散解空间。", "recommended_improvement": "继续增加有物理意义的约束以删除无意义解。", "severity": "important", "source_page": 1, "source_bbox": [], "evidence_status": "verified"},
    ]
    existing_feedback = [r for r in read_jsonl(CAT / "reviewer_feedback_catalog.jsonl") if not str(r.get("feedback_id", "")).startswith("feedback_1992_")]
    write_jsonl(CAT / "reviewer_feedback_catalog.jsonl", existing_feedback + feedback)
    visualization_rows = [
        {"logical_document_id": "logical_b5ebbd7404ae15a9", "figure_or_table_id": "table_1", "page": 1, "bbox": "", "chart_type": "table", "purpose": "show fertilizer-yield input data", "supports_question": "A", "supports_claim": "input data coverage", "effective": "yes", "reusable_pattern": "raw data table", "evidence_status": "verified", "representation_id": reps_old["logical_b5ebbd7404ae15a9"]["representation_id"]},
        {"logical_document_id": "logical_b5ebbd7404ae15a9", "figure_or_table_id": "table_2", "page": 3, "bbox": "", "chart_type": "table", "purpose": "report regression estimates and significance", "supports_question": "A", "supports_claim": "model fit", "effective": "yes", "reusable_pattern": "parameter evidence table", "evidence_status": "verified", "representation_id": reps_old["logical_b5ebbd7404ae15a9"]["representation_id"]},
        {"logical_document_id": "logical_b5ebbd7404ae15a9", "figure_or_table_id": "table_3", "page": 4, "bbox": "", "chart_type": "table", "purpose": "compare factor effects", "supports_question": "A", "supports_claim": "N/P/K influence ranking", "effective": "yes", "reusable_pattern": "ANOVA table", "evidence_status": "verified", "representation_id": reps_old["logical_b5ebbd7404ae15a9"]["representation_id"]},
    ]
    for page, ids in [(3, ["table_1"]), (4, ["table_2"]), (5, ["table_3"]), (6, ["table_4a", "table_4b", "table_4c"]), (7, ["table_5"]), (9, ["appendix_c_table"])]:
        for table_id in ids:
            visualization_rows.append({"logical_document_id": "logical_33abe6eb835f81d8", "figure_or_table_id": table_id, "page": page, "bbox": "", "chart_type": "table", "purpose": "compare solution counts, runtime, or chemical constraints", "supports_question": "B", "supports_claim": "constraint effectiveness", "effective": "yes", "reusable_pattern": "baseline-versus-constrained model table", "evidence_status": "verified", "representation_id": reps_old["logical_33abe6eb835f81d8"]["representation_id"]})
    vis_path = CAT / "visualization_catalog.csv"
    old_vis: list[dict[str, str]] = []
    if vis_path.exists():
        with vis_path.open(encoding="utf-8-sig", newline="") as fh:
            old_vis = [r for r in csv.DictReader(fh) if not r.get("logical_document_id", "").startswith(("logical_b5eb", "logical_33ab"))]
    fieldnames = list(visualization_rows[0])
    with vis_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader(); writer.writerows(old_vis + visualization_rows)

    write_jsonl(QUALITY / "unresolved" / "1992_manual_review_queue.jsonl", [{
        "logical_document_id": "logical_096f6338555ccb87", "carrier_document_id": docs_1992["logical_096f6338555ccb87"]["carrier_document_ids"][0],
        "year": 1992, "reason": "cross-year intermodulation lineage awaits 1993 comparison", "priority": "high",
        "status": "unresolved_cross_year_relation", "does_not_invalidate_1992_content_review": True,
    }])

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "1992_report.md").write_text("""# 1992年重建人工核验报告

> 依据相同原始基线重新构建；不是恢复已丢失工作区。百分比只使用字段独立有效分母。

## 文档构成

- 候选相关载体 / logical documents：7。
- 参赛论文：2/7（28.6%）；专家评注：3/7（42.9%）；题面：2/7（28.6%）。
- 唯一赛题：2；已确认参赛方案谱系：2；另有1条非线性交调跨年谱系待1993核验。

## 参赛论文模式（n=2）

- 两篇均有摘要、显式假设、符号说明、模型检验、最终方案和表格：2/2（100.0%）。
- 灵敏度分析：施肥论文1/2（50.0%）；误差分析：氨基酸论文1/2（50.0%）。
- 最终答案汇总表与流程图：0/2（0.0%）。这里的“无”经有效文章区域逐页核验，不包含相邻文章。
- 施肥论文用全回归—逐步回归—响应面形成模型比较链；氨基酸论文用一般模型—模型A至F形成逐层加约束链。

## 专家评注模式（n=3）

评注重视可估性、约束的现实含义、解空间规模、软件与数学推导的边界，以及模型改进能否实际执行。评注不进入参赛论文的摘要、图表或最终答案比例。

## 页面边界与历史对账

- 施肥论文末页与施肥评注首页是同一刊物第83页的重复载体表示，PDF点坐标 `y=515` 分界。
- 非线性交调评注第5页在 `y=360` 后切换为《一个给足球队排名次的方法——B题》，下部保留为orphan segment。
- 氨基酸评注第2页的四图上下文连续，图后总结仍属本评注；未发现新标题、作者或版式边界。旧日志的“图形污染”判断缺乏证据，列为旧日志可能错误。

## 状态说明

施肥论文与氨基酸论文因公式文本层并非逐式无损，严格保持 `partially_parsed / key_content_verified`；两份短题面和两份原生文本评注可设为 `parsed / verified`。施肥评注无中文文本层，保持部分解析。
""", encoding="utf-8")
    (REPORTS / "1992_data_quality.md").write_text("""# 1992数据质量

| 类别 | 数量 | 说明 |
|---|---:|---|
| logical documents | 7 | 角色与边界均人工核验 |
| parsed / verified | 4 | 两题面、非线性交调评注、氨基酸评注 |
| partially_parsed / key_content_verified | 3 | 施肥评注及两篇参赛论文 |
| 同页边界 | 3 | 施肥共享页两载体、非线性交调末页 |
| 保存的排除区域 | 3 | 2个已匹配局部副本，1个未匹配足球文章片段 |
| 未解决跨年关系 | 1 | 非线性交调真实年份和论文对应待1993 |

扫描文本不可用不会被提升为全文parsed；所有论文字段的present/absent只来自有效区域人工核验。
""", encoding="utf-8")


if __name__ == "__main__":
    main()
