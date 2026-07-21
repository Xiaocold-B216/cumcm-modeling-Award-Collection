#!/usr/bin/env python3
"""Record the page-reviewed 1998 corpus, including the one-page excerpt."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.apply_manual_review_1992 import read_jsonl, stable, write_jsonl
from scripts.manual_review_common import AI, CAT, DOCS, HEIGHT, WIDTH, apply_manual_year

COMMON_PRESENT = ["abstract", "model_assumptions", "symbol_definitions", "final_solution", "references"]
COMMON_ABSENT = ["final_answer_summary_table", "flowchart", "appendix", "code_description"]


def p(key, title, problem, fragment, pages, models, algorithms, evidence, *,
      present=None, absent=None, essence="", use_common=True, **extra):
    out = dict(key=key, title=title, role="award_paper", problem=problem, fragment=fragment,
               pages=pages, models=models, algorithms=algorithms, evidence=evidence,
               present=(COMMON_PRESENT if use_common else []) + (present or []),
               absent=(COMMON_ABSENT if use_common else []) + (absent or []),
               content={"mathematical_essence": essence})
    out.update(extra)
    return out


SPECS = [
p("a1", "一类投资组合问题的建模与分析", "A", "一类投资组合问题", 5,
  ["portfolio_optimization", "piecewise_risk_model"], ["linear_programming", "parametric_analysis"],
  [(1,"摘要","model","以最大单项风险刻画组合风险并讨论多类目标","portfolio risk-return model"),
   (2,"模型建立","formula","分别固定风险或收益构造线性规划","parametric linear programs"),
   (4,"定理与曲线","validation","推导风险阈值变化下收益的分段性质","efficient frontier property"),
   (5,"结论","result","给出投资比例随风险偏好的选择方法","allocation rule")],
  present=["model_validation","visualization"], essence="以总收益、交易费和最大单项风险建立参数化线性规划，刻画风险—收益有效边界。"),
p("a2", "投资收益与风险的优化模型", "A", "收益与风险的优化模型", 2,
  ["multiobjective_portfolio", "portfolio_optimization"], ["weighted_sum", "linear_programming"],
  [(1,"摘要","model","把收益最大和风险最小写成多目标投资模型","multiobjective portfolio"),
   (1,"模型","formula","以权重统一风险和净收益目标","weighted objective"),
   (2,"结论","result","给出不同风险偏好下的投资组合","allocation scenarios")],
  present=["model_validation"], absent=["visualization"], essence="用加权多目标规划平衡净收益与最大风险并扣除交易费用。"),
p("a3", "投资组合与模糊规划模型", "A", "模糊规划模型", 5,
  ["fuzzy_programming", "portfolio_optimization"], ["max_min_membership", "linear_programming"],
  [(1,"摘要","model","用模糊满意度处理收益和风险目标","fuzzy portfolio model"),
   (2,"模糊规划","formula","建立最大最小隶属度模型","max-min membership"),
   (4,"结果表","result","比较不同风险偏好参数下的投资比例","portfolio comparison"),
   (5,"模型评价","validation","讨论模糊规划与单目标模型差异","model comparison")],
  present=["model_validation","visualization"], essence="把最低收益与风险上限模糊化，以最大化最低满意度得到折衷投资组合。"),
p("a4", "投资组合模型", "A", "投资组合模型.pdf", 4,
  ["portfolio_optimization", "minimax_risk"], ["linear_programming", "maple"],
  [(1,"摘要","model","构造固定收益和固定风险两类组合模型","dual portfolio formulations"),
   (2,"风险模型","formula","以各资产风险暴露最大值为风险指标","minimax risk"),
   (4,"计算结果","result","用Maple给出投资比例与净收益","computed allocation")],
  present=["model_validation"], absent=["visualization"], essence="在投资额和交易费约束下分别求固定风险最大收益与固定收益最小风险。"),
p("a5", "资产投资收益与风险模型", "A", "资产投资收益与风险", 6,
  ["portfolio_optimization", "efficient_frontier"], ["linear_programming", "sensitivity_analysis"],
  [(1,"摘要","model","建立资产投资收益与风险模型","risk-return optimization"),
   (3,"数值表","table","计算风险限额变化下的最优组合","parametric results"),
   (4,"曲线","figure","绘制收益与风险参数关系","efficient frontier"),
   (6,"结论","result","按投资者风险承受能力选择组合","risk-preference plan")],
  present=["model_validation","sensitivity_analysis","visualization"], essence="参数化风险限额并求解线性规划，以有效边界支持不同风险偏好。"),
p("a6", "资本市场的最佳投资组合", "A", "资本市场的最佳投资组合", 8,
  ["mean_risk_portfolio", "capital_asset_pricing"], ["random_sampling", "efficient_frontier_analysis"],
  [(1,"摘要","model","从资本市场组合样本分析最佳投资组合","market portfolio analysis"),
   (3,"散点图","figure","展示随机组合在收益—风险平面中的分布","feasible portfolio cloud"),
   (6,"风险曲线","figure","比较不同约束下的风险收益边界","frontier comparison"),
   (8,"结论","validation","讨论模型适用范围与参数敏感性","model evaluated")],
  present=["model_validation","sensitivity_analysis","visualization"], essence="通过组合收益与风险散点、有效边界和市场定价关系选择资本市场组合。"),
p("a7", "风险投资分析", "A", "风险投资分析.pdf", 6,
  ["expected_utility", "portfolio_optimization"], ["linear_programming", "scenario_analysis"],
  [(1,"摘要","model","按收益、风险和交易费分析投资方案","risk investment analysis"),
   (3,"方案计算","formula","建立多种风险定义下的优化模型","alternative risk measures"),
   (5,"结果曲线","figure","比较风险参数与收益的变化","risk-return curve"),
   (6,"模型评价","validation","说明不同风险指标的影响","risk measure evaluation")],
  present=["model_validation","sensitivity_analysis","visualization"], essence="比较最大风险、期望损失等风险指标下的最优投资比例和净收益。"),
p("a8", "风险投资组合的线性规划模型", "A", "线性规划模型", 4,
  ["linear_programming", "portfolio_optimization"], ["matlab", "parametric_linear_programming"],
  [(1,"摘要","model","建立风险投资组合线性规划","linear portfolio model"),
   (2,"规划模型","formula","分别约束风险与收益并计入交易费","constrained portfolio LP"),
   (3,"结果表","result","用MATLAB计算多组风险参数方案","parametric allocations"),
   (4,"结论","validation","用曲线说明风险与收益权衡","trade-off checked")],
  present=["model_validation","sensitivity_analysis","visualization"], essence="把风险上限作为参数，以线性规划求净收益最大组合并分析风险—收益权衡。"),
p("b1", "多旅行商路线的几个问题", "B", "多旅行商路线", 8,
  ["multiple_traveling_salesman", "graph_partition"], ["set_partition", "heuristic_search"],
  [(1,"摘要","model","把灾情巡视归结为多旅行商路线问题","multiple traveling salesman"),
   (3,"路线划分","formula","建立区域划分和各队行程约束","route partition constraints"),
   (7,"图示","figure","用图说明多支巡视队的路线构成","route diagram"),
   (8,"附录结果","result","列出节点间距离和巡视路线","route list")],
  present=["model_validation","visualization"], essence="将公路网络分区并为多支巡视队构造闭合/开放路线，兼顾总里程与均衡性。"),
p("b2", "最佳灾情巡视路线的数学模型", "B", "最佳灾情巡视路线的数学模型", 10,
  ["graph_partition", "route_optimization"], ["shortest_path", "heuristic_balancing"],
  [(1,"摘要","model","建立多队灾情巡视路线模型","disaster inspection routing"),
   (3,"网络图","figure","绘制道路网络和初步分区","network partition"),
   (6,"路线表","result","列出各巡视队路线和里程","route schedule"),
   (10,"评价","validation","比较总里程与队间均衡并讨论算法","route evaluated")],
  present=["model_validation","visualization"], essence="在公路网络上先分区再求每区巡视回路，平衡各队路程并控制最长完成时间。"),
p("b3", "灾情巡视的最佳路线", "B", "灾情巡视的最佳路线.pdf", 5,
  ["integer_programming", "vehicle_routing"], ["branch_and_bound", "local_search"],
  [(1,"摘要","model","以0-1变量建立灾情巡视路线模型","binary routing formulation"),
   (2,"整数规划","formula","约束每条道路被巡视并保持路线连通","route coverage constraints"),
   (4,"路线方案","result","给出多支巡视队的路线与时间","inspection routes"),
   (5,"评价","validation","比较方案并讨论均衡性","route balance checked")],
  present=["model_validation","visualization"], essence="用0-1整数规划覆盖灾区道路，并用启发式搜索获得多队均衡巡视方案。"),
p("b4", "灾情巡视的最佳路线（节选）", "B", "最佳路线_节选_", 1,
  ["heuristic_route_partition"], ["route_construction"],
  [(1,"标题与作者","title","独立作者和“节选”标题表明是另一篇论文的局部载体","distinct partial paper"),
   (1,"摘要与网络图","model","开篇给出巡视网络、分队构想和路线示意","partial route method")],
  present=["abstract","visualization"], absent=[], essence="可确认采用网络分区和路线构造；载体只有开篇一页，后续公式、检验和结果均未知。",
  completeness="missing_end", evidence_status="content_verified_partial", use_common=False,
  unresolved_members=["missing_1998_b_disaster_route_excerpt_continuation"]),
p("b5", "灾情巡视路线寻优模型", "B", "路线寻优模型", 6,
  ["graph_theory", "route_optimization"], ["network_decomposition", "heuristic_search"],
  [(1,"摘要","model","以图论建立灾情巡视路线寻优模型","graph route optimization"),
   (2,"图论模型","formula","定义道路图、回路和队伍负载","graph constraints"),
   (4,"路线图","figure","展示网络分解和各队路线","route visualization"),
   (6,"结果表","result","给出路线、里程和总完成时间","routing plan")],
  present=["model_validation","visualization"], essence="用图的连通分解、回路构造和负载均衡确定多队灾情巡视路线。"),
p("b6", "灾情巡视路线最优解的证明", "B", "最优解的证明", 4,
  ["routing_lower_bound", "optimality_proof"], ["lower_bound", "enumeration"],
  [(1,"摘要","model","针对已有巡视路线给出最优性证明","route optimality proof"),
   (1,"定理","formula","由队伍总里程和最长路线建立下界","routing lower bound"),
   (3,"分类讨论","validation","逐类排除低于候选值的可行方案","case exclusion"),
   (4,"结论","result","证明候选巡视路线达到下界","optimality established")],
  present=["model_validation","visualization"], essence="构造路线长度下界并通过组合分类排除更优方案，从而证明给定解最优。"),
p("b7", "灾情巡视路线的设计", "B", "路线的设计", 7,
  ["graph_partition", "vehicle_routing"], ["hamiltonian_cycle", "heuristic_balancing"],
  [(1,"摘要","model","设计灾情巡视网络分区与路线","inspection route design"),
   (3,"路线构造","algorithm","用Hamilton回路思想构造候选路线","cycle construction"),
   (6,"数值方案","result","给出各队路线、时间和均衡结果","balanced routes"),
   (7,"评价","validation","讨论算法近似性和工程可实施性","method evaluated")],
  present=["model_validation","visualization"], essence="将道路图分区后构造Hamilton型回路，并通过局部调整平衡各巡视队行程。"),
dict(key="pa", title="1998年A题：投资的收益和风险", role="problem_statement", problem="A", fragment="国赛赛题", pages=1,
     evidence=[(1,"题面","title","A题 投资的收益和风险","canonical A problem"),(1,"任务","constraint","在收益、风险和交易费之间选择投资组合","portfolio task")],
     content={"subproblems":["建立风险收益模型","给出不同风险偏好下的投资方案"]}),
dict(key="pb", title="1998年B题：灾情巡视路线", role="problem_statement", problem="B", fragment="国赛赛题", pages=1, page_numbers=[2],
     evidence=[(2,"题面","title","B题 灾情巡视路线","canonical B problem"),(2,"任务","constraint","为多支巡视队设计覆盖道路的最佳路线","routing task")],
     content={"subproblems":["设计分队巡视路线","比较完成时间与路程","处理新增道路情景"]}),
]


def main():
    for s in SPECS:
        s["id"] = stable("logical_", 1998, s["title"], s["role"])
        s["problem_id"] = f"problem_cumcm_1998_{s['problem'].lower()}"
    visuals = []
    for key, page, chart, purpose in [
        ("a1",4,"efficient_frontier","show return versus risk"),("a3",4,"result_table","compare fuzzy portfolios"),
        ("a5",4,"efficient_frontier","show parametric frontier"),("a6",3,"scatter_plot","show feasible portfolios"),
        ("a7",5,"risk_return_curve","compare risk measures"),("a8",4,"risk_return_curve","show LP trade-off"),
        ("b1",7,"route_diagram","show multi-salesman partition"),("b2",3,"map","show road network"),
        ("b3",4,"route_table","report routes"),("b4",1,"map","show partial route plan"),
        ("b5",4,"network_graph","show optimized routes"),("b6",2,"result_table","support optimality proof"),
        ("b7",6,"route_table","report balanced routes")]:
        s = next(x for x in SPECS if x["key"] == key)
        visuals.append({"logical_document_id": s["id"], "figure_or_table_id": stable("visual_", s["id"], page, chart),
            "page": page, "bbox": f"[0,0,{WIDTH},{HEIGHT}]", "chart_type": chart, "purpose": purpose,
            "supports_question": s["problem"], "supports_claim": purpose, "effective": "yes",
            "reusable_pattern": chart, "evidence_status": "verified",
            "representation_id": stable("representation_", s["id"], "carrier-pending")})
    result = apply_manual_year(1998, SPECS, visual_rows=visuals,
        report_text="""# 1998年人工核验报告

- 物理PDF载体16；逻辑文档17；参赛论文15（A题8、B题7）；题面逻辑文档2；unique problem 2；方案谱系15。
- 14篇论文载体完整；《灾情巡视的最佳路线（节选）》作者与同题完整论文不同，是独立论文的一页节选，不是重复表示，状态为 `missing_end + content_verified_partial`。
- 官方A/B题面分别位于同一载体的第1、2页。17个逻辑文档均有一个首选表示；未发现重复表示或相邻文章污染。
- 完整扫描论文保持 `partially_parsed + key_content_verified`；节选未确认字段均为unknown。

A题以线性规划、多目标规划、模糊规划、有效边界和风险偏好参数分析为主。B题以图划分、多旅行商、整数规划、Hamilton回路、路线均衡和最优性下界证明为主。以上仅为1998年已核验样本的描述性观察。
""",
        quality_text="""# 1998数据质量

| 项目 | 结果 |
|---|---|
| carrier coverage | 16/16 |
| logical documents | 17/17角色和边界人工确认 |
| unique award papers | 15（其中1篇仅有节选） |
| unique problems | 2 |
| representations | 17，均为首选唯一表示 |
| missing segment | 1：一页节选缺少后续正文 |
| duplicate/orphan | 0/0 |
| OCR | 未执行全篇中文OCR；关键证据视觉核验 |

节选论文的最终方案、模型检验、参考文献、附录和后续图表保持unknown，不计入present/absent分母。
""")
    # Replace placeholder representation identifiers after carrier resolution.
    reps = {r["logical_document_id"]: r["representation_id"] for r in read_jsonl(DOCS / "representations_1998.jsonl")}
    for row in visuals: row["representation_id"] = reps[row["logical_document_id"]]
    import csv
    with (CAT / "visualization_catalog_1998.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(visuals[0]), lineterminator="\n"); writer.writeheader(); writer.writerows(visuals)
    partial = next(s for s in SPECS if s["key"] == "b4")
    requests = [r for r in read_jsonl(DOCS / "missing_segment_requests.jsonl") if r.get("request_id") != "missing_1998_b_disaster_route_excerpt_continuation"]
    requests.append({"request_id":"missing_1998_b_disaster_route_excerpt_continuation",
        "logical_document_id": partial["id"], "carrier_document_id": next(d["carrier_document_ids"][0] for d in read_jsonl(DOCS / "logical_documents_1998.jsonl") if d["logical_document_id"] == partial["id"]),
        "title":partial["title"], "missing_type":"missing_end", "expected_page_label":"after excerpt page",
        "preceding_text":"one-page excerpt ends during method introduction", "required_content":"remaining model, solution, validation, results and references",
        "search_scope":["full inventory","adjacent years","duplicate carriers","archives and image groups"],
        "candidate_matches":[], "status":"unresolved_missing_segment", "resolution_evidence":[],
        "affected_fields":["model_validation","final_solution","final_answer_summary_table","references","appendix","code_description"],
        "year":1998, "manual_overrides":True})
    write_jsonl(DOCS / "missing_segment_requests.jsonl", requests)
    print(json.dumps({"status":"applied_manual_review","year":1998,**result,"missing_segments":1}, ensure_ascii=False))


if __name__ == "__main__":
    main()
