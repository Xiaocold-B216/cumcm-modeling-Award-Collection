# 施肥方案对作物、蔬菜的影响

- 年份：1992
- 角色：award_paper
- 状态：partially_parsed / key_content_verified / complete
- 题号：A
- 核心模型：multiple_quadratic_regression、stepwise_regression、quadratic_response_surface
- 方案谱系：lineage_cumcm_1992_a_fertilization

## 人工核验摘要

{
  "problem_and_subproblems": [
    "建立土豆和生菜产量—N/P/K施肥量关系",
    "给出最优施肥组合",
    "评价应用价值并提出改进"
  ],
  "data_types": [
    "连续数值",
    "两作物各30组单因素试验数据"
  ],
  "mathematical_essence": "多元二次回归、变量交互与响应面优化。",
  "data_preprocessing": [
    "中心化与标准化",
    "用VIF诊断共线性后作相关变换"
  ],
  "baseline_models": [
    "全回归"
  ],
  "core_models": [
    "逐步回归",
    "二次响应面回归"
  ],
  "parameter_sources": [
    "试验数据",
    "SAS/STAT回归估计"
  ],
  "validation_methods": [
    "VIF",
    "方差分析F检验",
    "残差散点检查",
    "95%预测区间",
    "决定系数"
  ],
  "important_results": [
    "土豆N/P/K=292/246/542 kg/ha，预测产量45.18 t/ha",
    "生菜N/P/K=213/667/427 kg/ha，预测产量23.13 t/ha"
  ],
  "abstract_structure": "对象与模型—统计分析—两作物比较—最优施肥量与产量。",
  "section_structure": [
    "问题重述",
    "假设",
    "模型建立与分析",
    "应用分析",
    "优缺点与改进"
  ],
  "innovation_expression": "比较三类回归并把响应面导数用于边际产量和投入组合分析。",
  "strengths": [
    "模型、检验和应用解释闭环",
    "给出明确数值方案"
  ],
  "limitations": [
    "原试验设计不能独立估计全部交互项",
    "未显式建模区组效应",
    "无代码或SAS脚本"
  ],
  "reproducibility_level": "medium"
}

> 仅保存结构化短摘要和页码证据；完整提取正文为本地忽略缓存。
