#!/usr/bin/env python3
"""Persist the page-by-page visual review of the 1997 corpus."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.apply_manual_review_1992 import fstats, read_jsonl, stable, write_json, write_jsonl

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
DOCS = AI / "02_documents"
CARDS = DOCS / "cards"
REL = AI / "04_relations"
CAT = AI / "05_catalogs"
REPORTS = AI / "07_reports/yearly"
QUALITY = AI / "08_quality"
FIELDS = ["abstract", "model_assumptions", "symbol_definitions", "model_validation",
          "sensitivity_analysis", "error_analysis", "final_solution",
          "final_answer_summary_table", "flowchart", "visualization", "references",
          "appendix", "code_description"]


def paper(key, title, problem, fragment, pages, models, algorithms, evidence,
          present, absent, essence):
    return dict(key=key, title=title, role="award_paper", subtype="none", problem=problem,
                fragment=fragment, pages=pages, models=models, algorithms=algorithms,
                evidence=evidence, present=present, absent=absent,
                content={"mathematical_essence": essence}, authors=[])


COMMON_PRESENT = ["abstract", "model_assumptions", "symbol_definitions", "final_solution",
                  "references"]
COMMON_ABSENT = ["final_answer_summary_table", "flowchart", "appendix", "code_description"]
SPECS = [
paper("a1", "关于零件参数问题的建模", "A", "关于零件参数问题", 5,
      ["robust_parameter_design", "probabilistic_tolerance_model"],
      ["numerical_integration", "parameter_search"],
      [(1, "摘要与符号", "model", "把零件成本和产品损失统一为期望费用", "expected-cost model"),
       (3, "计算方法", "algorithm", "采用Mathematica计算概率积分并搜索参数", "numerical probability integration"),
       (4, "结果表", "result", "给出设计参数、成本和质量指标", "parameter plan reported"),
       (5, "程序框图", "flowchart", "给出两类参数计算框图", "calculation workflow")],
      COMMON_PRESENT + ["model_validation", "flowchart", "visualization"], COMMON_ABSENT,
      "以参数偏离造成的产品损失概率与零件成本之和为目标选择标称值和容差。"),
paper("a2", "零件参数的优化设计", "A", "参数的优化设计", 5,
      ["nonlinear_programming", "quality_loss_model"], ["orthogonal_design", "sensitivity_analysis"],
      [(1, "摘要", "model", "建立零件参数优化设计模型", "nonlinear quality-cost optimization"),
       (3, "试验设计", "table", "以正交表比较参数组合", "orthogonal design"),
       (4, "稳定性分析", "validation", "分析参数摄动后的方案稳定性", "stability checked"),
       (5, "结论", "result", "给出推荐标称值和容差", "recommended parameters")],
      COMMON_PRESENT + ["model_validation", "sensitivity_analysis", "visualization"], COMMON_ABSENT,
      "用非线性质量损失与生产成本联合目标进行参数优化，并以正交试验和扰动检验方案。"),
paper("a3", "零件参数设计的动态规划模型", "A", "动态规划模型", 5,
      ["dynamic_programming", "probabilistic_quality_loss"], ["stagewise_optimization", "simulation"],
      [(1, "摘要", "model", "把多零件参数选择写成动态规划", "dynamic programming formulation"),
       (2, "误差传播", "formula", "用偏导数近似输出方差", "variance propagation"),
       (4, "模拟结果", "figure", "用分布图和表格检验设计", "simulation validation"),
       (5, "评价", "validation", "讨论模型的优点、局限和敏感因素", "model evaluated")],
      COMMON_PRESENT + ["model_validation", "sensitivity_analysis", "error_analysis", "visualization"], COMMON_ABSENT + ["flowchart"],
      "将零件等级和容差作为阶段决策，以期望质量损失与生产成本之和最小为目标递推。"),
paper("a4", "零件参数设计的数学模型", "A", "设计的数学模型", 4,
      ["probabilistic_tolerance_model", "nonlinear_optimization"], ["lagrange_multiplier", "numerical_search"],
      [(1, "摘要", "model", "用正态误差传播建立零件参数模型", "normal-error propagation"),
       (2, "模型建立", "formula", "建立期望损失与成本目标函数", "expected loss objective"),
       (3, "求解", "algorithm", "比较解析近似和数值优化", "optimization methods compared"),
       (4, "评价", "validation", "讨论误差近似及模型适用条件", "approximation limitations")],
      COMMON_PRESENT + ["model_validation", "error_analysis"], COMMON_ABSENT + ["flowchart", "visualization"],
      "用一阶误差传播和分段质量损失构造目标函数，优化各零件均值与标准差。"),
paper("a5", "零件的参数设计（1）", "A", "参数设计(1)", 5,
      ["stochastic_programming", "tolerance_allocation"], ["normal_approximation", "nonlinear_optimization"],
      [(1, "摘要", "model", "在随机误差下分配零件容差", "stochastic tolerance allocation"),
       (3, "随机模型", "formula", "由正态分布计算产品合格概率", "probability of conformity"),
       (4, "结果表", "result", "比较多种设计的期望费用", "designs compared"),
       (5, "模型评价", "validation", "说明随机模型假设和不足", "assumptions evaluated")],
      COMMON_PRESENT + ["model_validation", "visualization"], COMMON_ABSENT + ["flowchart"],
      "把产品超差概率转化为期望损失，并在生产成本约束下分配零件容差。"),
paper("a6", "零件的参数设计（2）", "A", "参数设计(2)", 4,
      ["monte_carlo_simulation", "simulated_annealing"], ["monte_carlo", "simulated_annealing"],
      [(1, "摘要", "model", "用Monte Carlo模拟输出分布", "Monte Carlo quality model"),
       (2, "分布检验", "figure", "直方图检验产品参数近似正态", "distribution checked"),
       (3, "优化模型", "formula", "最小化生产成本与产品损失", "joint cost objective"),
       (4, "算法", "algorithm", "给出模拟退火步骤和数值方案", "simulated annealing solution")],
      COMMON_PRESENT + ["model_validation", "sensitivity_analysis", "visualization"], COMMON_ABSENT + ["flowchart"],
      "用Monte Carlo传播零件随机误差，再以模拟退火搜索离散等级和连续标称参数。"),
paper("a7", "零件的参数设计（3）", "A", "参数设计(3)", 8,
      ["stochastic_optimization", "response_surface_approximation"], ["mathematica", "iterative_search"],
      [(1, "摘要", "model", "建立随机参数设计模型", "stochastic parameter design"),
       (4, "计算表", "table", "列出随机试验和目标函数值", "simulation table"),
       (7, "数值方案", "result", "给出多组零件等级和参数", "candidate plans"),
       (8, "模型评价", "validation", "总结方法合理性并列出改进方向", "model evaluated")],
      COMMON_PRESENT + ["model_validation", "sensitivity_analysis", "visualization"], COMMON_ABSENT + ["flowchart"],
      "以随机模拟近似产品输出分布，对零件等级、均值和标准差联合寻优。"),
paper("a8", "零件的参数设计（4）", "A", "参数设计（4）", 6,
      ["chance_constrained_programming", "robust_parameter_design"], ["normal_approximation", "scenario_comparison"],
      [(1, "摘要", "model", "构造带概率约束的参数设计模型", "chance-constrained design"),
       (3, "优化模型", "formula", "最小化期望生产成本和废品损失", "expected total cost"),
       (4, "结果曲线", "figure", "比较多个方案随参数变化的费用", "scenario curves"),
       (6, "结论", "result", "给出零件等级组合和参数方案", "design plan reported")],
      COMMON_PRESENT + ["model_validation", "sensitivity_analysis", "visualization"], COMMON_ABSENT + ["flowchart"],
      "以产品质量概率约束限制失效率，并最小化零件生产成本和产品损失。"),
paper("b1", "切割次序的优化", "B", "切割次序的优化", 5,
      ["sequencing_optimization", "cutting_cost_model"], ["heuristic_search", "simulation"],
      [(1, "摘要", "model", "建立长方体多面切割次序费用模型", "cutting sequence cost"),
       (2, "算法", "algorithm", "逐步交换切割次序并比较费用", "sequence improvement"),
       (4, "结果表", "result", "比较不同尺寸和刀具下的最优次序", "optimal sequences compared"),
       (5, "评价", "validation", "用算例说明算法有效范围", "algorithm checked")],
      COMMON_PRESENT + ["model_validation", "visualization"], COMMON_ABSENT + ["flowchart"],
      "把每次换刀、转面和进给费用累加为序列目标，以交换搜索确定低费用切割次序。"),
paper("b2", "截断切割中的最优排列问题", "B", "最优排列问题", 3,
      ["dynamic_programming", "permutation_optimization"], ["dynamic_programming", "dominance_pruning"],
      [(1, "开篇", "model", "将截断切割抽象为排列问题", "permutation model"),
       (1, "递推式", "formula", "建立阶段费用函数递推", "dynamic recursion"),
       (2, "支配准则", "algorithm", "用交换不增费用关系删减排列", "dominance pruning"),
       (3, "结论", "result", "给出适用于一般长方体的排列方法", "ordering method")],
      ["model_assumptions", "symbol_definitions", "model_validation", "final_solution", "references"], COMMON_ABSENT + ["abstract", "flowchart", "visualization"],
      "将六次切割写为有限排列并利用阶段递推和支配准则减少组合搜索。"),
paper("b3", "截断切割优化模型", "B", "截断切割优化模型", 6,
      ["integer_programming", "cutting_sequence_model"], ["branch_and_bound", "enumeration"],
      [(1, "摘要", "model", "建立0-1切割次序模型", "binary sequencing model"),
       (3, "整数规划", "formula", "以0-1变量表示切割状态", "integer formulation"),
       (5, "方案表", "result", "列出尺寸情形下的最优刀序和费用", "optimal plan table"),
       (6, "检验", "validation", "用图解和算例核验最优次序", "solution verified")],
      COMMON_PRESENT + ["model_validation", "visualization"], COMMON_ABSENT + ["flowchart"],
      "用0-1变量描述各方向和切面的先后关系，以加工费用最小建立整数规划。"),
paper("b4", "截断切割的最优方案", "B", "截断切割的最优方案", 6,
      ["graph_search", "cutting_sequence_model"], ["theorem_based_pruning", "enumeration"],
      [(1, "摘要", "model", "按切面关系构造最优切割方案", "cutting-order optimization"),
       (3, "定理", "formula", "证明相邻切割交换的费用判据", "exchange theorem"),
       (5, "算法", "algorithm", "依定理枚举并剪枝切割序列", "pruned enumeration"),
       (6, "结果表", "result", "报告最小费用方案", "minimum-cost plan")],
      COMMON_PRESENT + ["model_validation", "visualization"], COMMON_ABSENT + ["flowchart"],
      "从相邻操作交换准则推导切割顺序的偏序关系，再枚举满足偏序的最小费用方案。"),
paper("b5", "最优切割次序模型", "B", "最优切割次序模型", 7,
      ["state_space_model", "dynamic_programming"], ["shortest_path", "numerical_validation"],
      [(1, "摘要", "model", "以状态空间表示切割过程", "state-space cutting model"),
       (3, "状态转移", "formula", "定义各切割状态和转移费用", "state transition"),
       (6, "数值结果", "table", "列出不同条件下的最优费用", "cost results"),
       (7, "模型评价", "validation", "比较理论判据和数值方案", "model evaluated")],
      COMMON_PRESENT + ["model_validation", "visualization"], COMMON_ABSENT + ["flowchart"],
      "将工件姿态与已切割面作为状态，把切割次序问题转化为状态图最短路。"),
paper("b6", "最小费用切割策略", "B", "最小费用切割策略", 6,
      ["fuzzy_decision", "cutting_cost_model"], ["heuristic_enumeration", "fuzzy_comprehensive_evaluation"],
      [(1, "摘要", "model", "建立最小费用切割策略", "minimum-cost strategy"),
       (3, "策略图", "figure", "以线段示意切割次序", "sequence diagram"),
       (4, "模糊评价", "validation", "用模糊评价比较实用性", "fuzzy evaluation"),
       (6, "结果表", "result", "比较三类工件的推荐方案", "recommended strategies")],
      COMMON_PRESENT + ["model_validation", "visualization"], COMMON_ABSENT + ["flowchart"],
      "枚举可行切割次序并按加工费选择最小值，再用模糊评价衡量工程适用性。"),
paper("b7", "长方体材料截断切割的优化设计", "B", "长方体材料", 6,
      ["geometric_optimization", "cutting_sequence_model"], ["dynamic_programming", "case_analysis"],
      [(1, "摘要", "model", "从长方体几何建立截断切割模型", "geometric cutting model"),
       (3, "递推方法", "algorithm", "用动态规划比较子问题", "dynamic programming"),
       (5, "误差分析", "validation", "分析参数变化对切割费用的影响", "cost sensitivity"),
       (6, "结果表", "result", "给出刀具选择和最优次序", "tool and sequence plan")],
      COMMON_PRESENT + ["model_validation", "sensitivity_analysis", "error_analysis", "visualization"], COMMON_ABSENT + ["flowchart"],
      "从工件尺寸、刀具方向和进给路径计算费用，以动态规划选择刀具和切割次序。"),
]

SPECS += [
 dict(key="ac", title="“零件的参数设计”模型和评述", role="expert_commentary", subtype="none",
      problem="A", fragment="模型和评述", pages=4, models=[], algorithms=[], present=[], absent=[], authors=["姜启源"],
      evidence=[(1,"标题与引言","review","对1997年A题建模与答卷进行模型化评述","commentary identity"),
                (2,"基本模型","model","给出期望质量损失和零件成本的参考模型","reference formulation"),
                (4,"方案评述","review","比较解析近似、数值积分和Monte Carlo的适用条件","method criteria")],
      content={"review_findings":["质量损失必须用概率而非仅看均值","零件误差独立和正态分布需说明依据","近似模型应以Monte Carlo或数值积分复核","参数优化需区分离散等级与连续标称值"]}),
 dict(key="errata", title="勘误：数学建模工作中的疏忽", role="other_related", subtype="editorial_note",
      problem="A", fragment="参数设计(3)", pages=1, models=[], algorithms=[], present=[], absent=[], authors=[],
      evidence=[(8,"分隔线后","boundary","参考文献后出现独立“勘误”标题和另一文章文字","separate editorial note")],
      content={"note":"刊物勘误，位于《零件的参数设计（3）》末页下部，不属于参赛论文正文。"}),
 dict(key="pa", title="1997年A题：零件的参数设计", role="problem_statement", subtype="none",
      problem="A", fragment="国赛赛题", pages=1, models=[], algorithms=[], present=[], absent=[], authors=[],
      evidence=[(1,"题面","title","A题 零件的参数设计","canonical A problem"),
                (1,"任务","constraint","给出七个零件参数、质量等级、成本和产品损失函数","parameter design task")],
      content={"subproblems":["设计零件标称值、容差和等级","比较所提方案与原方案"],"outputs":["参数设计方案","总费用及质量指标"]}),
 dict(key="pb", title="1997年B题：截断切割", role="problem_statement", subtype="none",
      problem="B", fragment="国赛赛题", pages=1, models=[], algorithms=[], present=[], absent=[], authors=[],
      evidence=[(2,"题面","title","B题 截断切割","canonical B problem"),
                (2,"任务","constraint","比较不同切割次序并设计一般优化模型","cutting-order task")],
      content={"subproblems":["计算给定次序费用","寻找最优次序","推广一般情形"],"outputs":["最优切割次序与费用"]}),
]

for s in SPECS:
    s["id"] = stable("logical_", 1997, s["title"], s["role"])
    s["problem_id"] = f"problem_cumcm_1997_{s['problem'].lower()}"
    s["lineage"] = stable("lineage_cumcm_1997_", s["problem"], s["title"]) if s["role"] == "award_paper" else None


def eligibility(role):
    out = {k: "excluded" for k in ["award_paper_patterns", "reviewer_feedback", "problem_analysis",
                                    "validation_patterns", "visualization_patterns"]}
    if role == "award_paper": out["award_paper_patterns"] = out["visualization_patterns"] = "included"
    elif role == "expert_commentary": out["reviewer_feedback"] = "included"
    elif role == "problem_statement": out["problem_analysis"] = "included"
    return out


def main():
    with (DOCS / "1997_carrier_manifest.csv").open(encoding="utf-8-sig", newline="") as fh:
        carrier_rows = list(csv.DictReader(fh))

    def carrier(fragment):
        found = [r["carrier_document_id"] for r in carrier_rows if fragment in r["filename"]]
        if len(found) != 1:
            raise SystemExit(f"carrier lookup {fragment!r}: {found}")
        return found[0]

    carriers = {s["key"]: carrier(s["fragment"]) for s in SPECS}
    carriers["errata"] = carriers["a7"]
    carriers["pb"] = carriers["pa"]
    width, height, split_y = 595.22, 842.0, 548
    docs, segments, representations = [], [], []
    old_auto = {d["logical_document_id"] for d in read_jsonl(DOCS / "logical_documents_1997.jsonl")}
    reviewed = {s["id"] for s in SPECS}
    all_docs = [d for d in read_jsonl(DOCS / "logical_documents.jsonl") if int(d.get("year", 0)) != 1997]

    for order, s in enumerate(SPECS, 1):
        did, cid = s["id"], carriers[s["key"]]
        page_range = list(range(1, s["pages"] + 1))
        if s["key"] == "errata": page_range = [8]
        if s["key"] == "pb": page_range = [2]
        sids = []
        for page in page_range:
            box = [0, 0, width, height]
            if s["key"] == "a7" and page == 8: box = [0, 0, width, split_y]
            if s["key"] == "errata": box = [0, split_y, width, height]
            sid = stable("segment_", did, cid, page, *box, "manual-1997")
            sids.append(sid)
            segments.append({"segment_id": sid, "carrier_document_id": cid,
                "logical_document_id": did, "page": page, "include_bbox": box, "exclude_bbox": [],
                "normalized_bbox": [round(box[0]/width,6), round(box[1]/height,6), round(box[2]/width,6), round(box[3]/height,6)],
                "page_width": width, "page_height": height, "page_rotation": 0,
                "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
                "reason": "manually verified article region", "segmentation_status": "segmented" if s["key"] in {"a7","errata"} else "not_required",
                "manually_verified": True, "manual_overrides": True})
        rid = stable("representation_", did, cid)
        representations.append({"representation_id": rid, "logical_document_id": did,
            "carrier_document_id": cid, "segment_ids": sids, "page_coverage": page_range,
            "completeness": "complete", "visual_quality": "native_text" if s["role"] == "problem_statement" else "good_scan",
            "text_layer_quality": "native_text_reviewed" if s["role"] == "problem_statement" else "scan_visual_only",
            "table_quality": "verified_key_tables", "formula_quality": "verified_key_formulas",
            "page_order_quality": "verified", "contamination_level": "cropped_adjacent_content" if s["key"] in {"a7","errata"} else "none_detected",
            "preferred_representation": True, "preference_reason": "only complete manually reviewed representation",
            "manual_overrides": True})
        vals = {f: ("unknown", []) for f in FIELDS}
        if s["role"] == "award_paper":
            for f in s["absent"]: vals[f] = ("absent", page_range)
            # A verified presence wins when a reusable common absence is overridden.
            for f in s["present"]: vals[f] = ("present", page_range)
        elif s["role"] in {"problem_statement", "other_related"}:
            vals = {f: ("not_applicable", []) for f in FIELDS}
        aelig = {"metadata_statistics"}
        if s["role"] == "award_paper": aelig |= {"structure_statistics", "model_statistics", "algorithm_statistics", "visualization_statistics", "result_pattern_statistics"}
        elif s["role"] == "expert_commentary": aelig.add("reviewer_feedback_statistics")
        elif s["role"] == "problem_statement": aelig.add("problem_analysis")
        doc = {"logical_document_id": did, "entity_type": "logical_document", "year": 1997,
            "article_order": order, "title": s["title"], "authors": s["authors"],
            "document_role": s["role"], "document_subtype": s["subtype"], "problem_code": s["problem"],
            "problem_id": s["problem_id"], "solution_lineage_id": s["lineage"],
            "carrier_document_ids": [cid], "segment_ids": sids, "page_count": len(page_range),
            "parse_status": "parsed" if s["role"] == "problem_statement" else "partially_parsed",
            "evidence_status": "verified" if s["role"] in {"problem_statement","other_related"} else "key_content_verified",
            "segmentation_status": "segmented" if s["key"] in {"a7","errata"} else "not_required",
            "completeness_status": "complete", "corpus_status": "included" if s["role"] != "other_related" else "excluded",
            "representation_quality": "manually_reviewed",
            "role_classification": {"predicted_role": s["role"], "confidence": 1.0,
                "classification_basis": ["title", "document_structure", "visual_review", "article_boundaries"],
                "conflicting_signals": [], "manually_verified": True},
            "corpus_eligibility": eligibility(s["role"]), "analysis_eligibility": sorted(aelig),
            "feature_statistics": fstats(s["role"], vals), "models": s["models"], "algorithms": s["algorithms"],
            "content_analysis": s["content"], "manual_overrides": True,
            "manual_reviewed_at": "2026-07-22T01:20:00Z"}
        docs.append(doc)
        folder = CARDS / did
        write_json(folder / "metadata.json", doc)
        write_json(folder / "page_map.json", {"logical_document_id": did, "page_number_basis": "carrier local, 1-based",
            "representation_id": rid, "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
            "pages": [{"page": x["page"], "width": width, "height": height, "rotation": 0,
                       "valid_bbox": x["include_bbox"], "excluded_bbox": [], "segment_id": x["segment_id"],
                       "carrier_document_id": cid, "manually_verified": True}
                      for x in segments if x["logical_document_id"] == did]})
        write_jsonl(folder / "evidence.jsonl", [{"logical_document_id": did,
            "paper_id": did if s["role"] == "award_paper" else None, "source_page": p,
            "source_section": sec, "source_bbox": [0,0,width,height], "evidence_type": typ,
            "text_excerpt": text, "normalized_claim": claim, "confidence": .97,
            "extraction_method": "manual_visual_review", "manual_review_required": False}
            for p, sec, typ, text, claim in s["evidence"]])
        (folder / "document_card.md").write_text(
            f"# {s['title']}\n\n- 年份：1997\n- 角色：{s['role']}\n- subtype：{s['subtype']}\n"
            f"- 状态：{doc['parse_status']} / {doc['evidence_status']} / complete\n- 题号：{s['problem']}\n"
            f"- 模型：{'、'.join(s['models']) or '不适用'}\n\n## 人工核验摘要\n\n"
            f"{json.dumps(s['content'], ensure_ascii=False, indent=2)}\n\n> 扫描全文不公开；短证据见 evidence.jsonl。\n", encoding="utf-8")
        (folder / "review_record.md").write_text("# Review record\n\n" +
            f"- logical_document_id: `{did}`\n" + "".join(f"- {x}: verified\n" for x in
            ["标题和身份", "文章边界", "摘要或开篇", "核心模型或评议对象", "关键公式", "关键表格或图", "最终结论", "重要数字", "题面和方案关系"]) +
            "- manually_verified: true\n", encoding="utf-8")
        (folder / "extracted_text.md").write_text("# 本地提取缓存\n\n扫描件未执行全篇中文OCR；短证据见 evidence.jsonl。\n", encoding="utf-8")

    write_jsonl(DOCS / "logical_documents_1997.jsonl", docs)
    write_jsonl(DOCS / "logical_documents.jsonl", sorted(all_docs + docs, key=lambda d: (int(d.get("year", 0)), d["logical_document_id"])))
    write_jsonl(DOCS / "page_segments_1997.jsonl", segments)
    write_jsonl(DOCS / "representations_1997.jsonl", representations)
    compact = ["logical_document_id", "title", "document_role", "document_subtype", "problem_code", "problem_id", "solution_lineage_id", "parse_status", "evidence_status", "segmentation_status", "completeness_status", "page_count"]
    with (DOCS / "1997_logical_document_compact.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=compact, lineterminator="\n"); writer.writeheader()
        writer.writerows([{k: d.get(k) for k in compact} for d in docs])
    absorptions = [r for r in read_jsonl(DOCS / "carrier_absorptions.jsonl") if int(r.get("year", 0)) != 1997]
    for row in carrier_rows:
        absorptions.append({"year": 1997, "carrier_document_id": row["carrier_document_id"],
            "logical_document_ids": [d["logical_document_id"] for d in docs if row["carrier_document_id"] in d["carrier_document_ids"]],
            "reason": "manual carrier-to-logical mapping; article boundary retained where applicable",
            "manually_verified": True, "manual_overrides": True})
    write_jsonl(DOCS / "carrier_absorptions.jsonl", absorptions)
    write_jsonl(DOCS / "carrier_absorptions_1997.jsonl", [r for r in absorptions if int(r.get("year", 0)) == 1997])
    boundary = {"boundary_id": stable("boundary_", carriers["a7"], 8, split_y),
        "carrier_document_id": carriers["a7"], "before_page": 8, "after_page": 8,
        "same_page_boundary": True, "boundary_y": split_y, "boundary_bbox": [0, split_y, width, height],
        "normalized_bbox": [0, round(split_y/height,6), 1, 1], "page_width": width, "page_height": height,
        "page_rotation": 0, "evidence": "award paper references end above asterisk divider; separate errata heading begins below",
        "confidence": .99, "manually_verified": True, "manual_overrides": True}
    write_jsonl(DOCS / "article_boundaries_1997.jsonl", [boundary])
    write_jsonl(DOCS / "orphan_segments_1997.jsonl", [])

    relations = [r for r in read_jsonl(REL / "document_relations.jsonl") if int(r.get("year", 0)) != 1997]
    def rel(src, tgt, typ, ev):
        relations.append({"relation_id": stable("relation_", src, tgt, typ), "source_document_id": src,
            "target_document_id": tgt, "relation_type": typ, "evidence": ev, "confidence": .98,
            "verified_by": "manual_visual_review", "status": "verified", "year": 1997, "manual_overrides": True})
    for s in SPECS:
        rel(carriers[s["key"]], s["id"], "contains", "verified title and page region")
        if s["role"] == "award_paper": rel(s["id"], s["problem_id"], "answers_problem", "variables, constraints and requested output correspond to statement")
        elif s["role"] == "expert_commentary": rel(s["id"], s["problem_id"], "comments_on", "text explicitly reviews problem models and solution approaches")
        elif s["key"] == "errata": rel(s["id"], next(x["id"] for x in SPECS if x["key"] == "a7"), "adjacent_to", "same carrier page, below asterisk divider after references")
    write_jsonl(REL / "document_relations.jsonl", relations)
    write_jsonl(REL / "document_relations_1997.jsonl", [r for r in relations if int(r.get("year", 0)) == 1997])
    lineages = [l for l in read_jsonl(REL / "solution_lineages.jsonl") if int(l.get("contest_year", 0) or 0) != 1997]
    for s in [x for x in SPECS if x["role"] == "award_paper"]:
        lineages.append({"lineage_id": s["lineage"], "contest_year": 1997, "problem_code": s["problem"],
            "primary_paper": s["id"], "paper_representations": [next(r["representation_id"] for r in representations if r["logical_document_id"] == s["id"])],
            "commentaries": [x["id"] for x in SPECS if x["role"] == "expert_commentary" and x["problem"] == s["problem"]],
            "problem_statement": [x["id"] for x in SPECS if x["role"] == "problem_statement" and x["problem"] == s["problem"]],
            "validation_summaries": [], "partial_segments": [], "unresolved_members": [],
            "canonical_solution_description": ", ".join(s["models"]), "status": "verified", "manual_overrides": True})
    write_jsonl(REL / "solution_lineages.jsonl", lineages)
    write_jsonl(REL / "solution_lineages_1997.jsonl", [l for l in lineages if int(l.get("contest_year", 0) or 0) == 1997])

    feedback = [r for r in read_jsonl(CAT / "reviewer_feedback_catalog.jsonl") if int(r.get("year", 0) or 0) != 1997]
    commentary = next(s for s in SPECS if s["key"] == "ac")
    for i, (dim, text, improve, page) in enumerate([
        ("loss_definition", "产品质量损失应按概率和损失函数计算，不能只比较均值。", "将超差概率与损失金额统一到目标函数。", 1),
        ("assumption_validity", "独立正态误差是一项需说明来源的假设。", "用数据或敏感性分析检验分布与独立性。", 2),
        ("approximation_validation", "一阶误差传播可能在强非线性区失准。", "以数值积分或Monte Carlo复核。", 3),
        ("mixed_decision_variables", "质量等级离散而标称值连续。", "使用混合优化并清楚说明取整规则。", 4)]):
        feedback.append({"feedback_id": stable("feedback_", 1997, i, dim), "year": 1997,
            "commentary_id": commentary["id"], "problem_id": commentary["problem_id"], "solution_lineage_id": None,
            "review_dimension": dim, "praised_or_criticized": "criterion", "normalized_feedback": text,
            "recommended_improvement": improve, "severity": "major", "source_page": page,
            "source_bbox": [], "evidence_status": "verified"})
    write_jsonl(CAT / "reviewer_feedback_catalog.jsonl", feedback)
    write_jsonl(CAT / "reviewer_feedback_catalog_1997.jsonl", [r for r in feedback if int(r.get("year", 0) or 0) == 1997])
    vis = []
    for key, page, chart, purpose in [("a1",5,"flowchart","parameter calculation workflow"),
        ("a2",3,"result_table","compare orthogonal designs"),("a3",4,"distribution_plot","validate simulated output"),
        ("a5",4,"result_table","compare designs"),("a6",2,"histogram","check output distribution"),
        ("a7",4,"result_table","show simulated costs"),("a8",4,"line_chart","compare parameter scenarios"),
        ("b1",4,"result_table","compare cutting sequences"),("b3",6,"line_chart","verify cost model"),
        ("b4",6,"result_table","report minimum-cost plan"),("b5",6,"line_chart","show cost threshold"),
        ("b6",3,"sequence_diagram","show cutting order"),("b7",5,"result_table","report tool and sequence")]:
        s = next(x for x in SPECS if x["key"] == key)
        vis.append({"logical_document_id": s["id"], "figure_or_table_id": stable("visual_", s["id"], page, chart),
            "page": page, "bbox": f"[0,0,{width},{height}]", "chart_type": chart, "purpose": purpose,
            "supports_question": s["problem"], "supports_claim": purpose, "effective": "yes",
            "reusable_pattern": chart, "evidence_status": "verified",
            "representation_id": next(r["representation_id"] for r in representations if r["logical_document_id"] == s["id"])})
    with (CAT / "visualization_catalog_1997.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(vis[0]), lineterminator="\n"); writer.writeheader(); writer.writerows(vis)
    write_jsonl(QUALITY / "unresolved/1997_manual_review_queue.jsonl", [])
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "1997_report.md").write_text("""# 1997年人工核验报告

- 物理PDF载体17；逻辑文档19；参赛论文15（A题8、B题7）；专家评述1；题面逻辑文档2；其他相关短文1；unique problem 2；方案谱系15。
- 题面A、B各占独立物理页；《零件的参数设计（3）》第8页在参考文献后的星号分隔线下另含“勘误”，已拆成 `other_related/editorial_note`，不进入论文统计。
- 18个正文或题面逻辑文档及1个勘误逻辑文档均有首选表示；未发现重复表示、缺页或未保全的orphan。
- 扫描文章保持 `partially_parsed + key_content_verified`；原生题面为 `parsed + verified`。

A题以概率质量损失、误差传播、随机/混合优化、动态规划、Monte Carlo和模拟退火为主。B题以排列优化、动态规划、状态空间、交换判据、整数规划和工程费用比较为主。以上仅为1997年已核验样本的描述性观察。
""", encoding="utf-8")
    (REPORTS / "1997_data_quality.md").write_text("""# 1997数据质量

| 项目 | 结果 |
|---|---|
| carrier coverage | 17/17 |
| logical documents | 19/19角色和边界人工确认 |
| unique award papers | 15 |
| unique problems | 2 |
| representations | 19，均为首选唯一表示 |
| same-page boundary | A题第（3）篇第8页，y=548 PDF point |
| missing/orphan | 0/0；分隔线后勘误已升级为独立逻辑文档 |
| OCR | 未执行全篇中文OCR；关键证据视觉核验 |

未确认字段保持unknown，不进入present/absent分母；勘误不进入参赛论文统计。
""", encoding="utf-8")
    for did in old_auto - reviewed:
        folder = CARDS / did
        if folder.exists():
            for name in ["document_card.md", "metadata.json", "extracted_text.md", "page_map.json", "evidence.jsonl", "review_record.md"]:
                path = folder / name
                if path.exists(): path.unlink()
            if not any(folder.iterdir()): folder.rmdir()
    print(json.dumps({"status": "applied_manual_review", "year": 1997,
                      "logical_documents": len(docs), "representations": len(representations),
                      "same_page_boundaries": 1}, ensure_ascii=False))


if __name__ == "__main__":
    main()
