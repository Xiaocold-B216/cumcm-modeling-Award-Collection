# 一个给足球队排名次的方法——B题

- 年份：1993
- 角色：award_paper
- 状态：partially_parsed / key_content_verified / complete
- 题号：B
- 模型：ahp_pairwise_judgment_matrix、perron_frobenius_eigenvector_ranking、chi_square_reliability
- 方案谱系：lineage_cumcm_1993_b_football_ranking

## 人工核验摘要

{
  "problem_and_subproblems": [
    "从赛果构造判断矩阵",
    "用主特征向量排名",
    "处理缺赛和残缺数据",
    "估计可依赖程度"
  ],
  "data_types": [
    "比赛网络",
    "比分与多场赛果",
    "缺失和矛盾数据"
  ],
  "mathematical_essence": "非负矩阵主特征向量排序与图连通性。",
  "data_preprocessing": [
    "把比分和多场结果映射为相对强度a_ij",
    "可约性检查",
    "构造辅助矩阵处理残缺"
  ],
  "baseline_models": [
    "积分排序"
  ],
  "core_models": [
    "AHP判断矩阵",
    "Perron–Frobenius主特征向量",
    "χ²可依赖度"
  ],
  "parameter_sources": [
    "赛果表",
    "经验比分权重",
    "σ²=1/2的简化估计"
  ],
  "validation_methods": [
    "保序性证明",
    "残缺处理命题",
    "扰动稳定性",
    "χ²可靠度"
  ],
  "important_results": [
    "排名T7,T3,T1,T9,T2,T10,T8,T12,T6,T5,T11,T4",
    "数据可依赖度约65%",
    "运行时间小于1秒"
  ],
  "abstract_structure": "模型—数据充分性—可靠度—名次—理论性质和推广。",
  "section_structure": [
    "问题分析",
    "模型和算法",
    "理论分析",
    "运行结果",
    "优缺点"
  ],
  "innovation_expression": "把排名反馈、残缺数据和可靠度统一进特征向量框架。",
  "strengths": [
    "能处理平局、缺赛和不一致",
    "理论性质与数值排名对应"
  ],
  "limitations": [
    "算法较复杂且依赖计算机",
    "比分映射和σ²=1/2具有经验性",
    "未研究近乎可约矩阵的排序稳定性"
  ],
  "reproducibility_level": "medium"
}

> 完整正文只保存在忽略缓存。
