# 蛋白质氨基酸的组合问题

- 年份：1992
- 角色：award_paper
- 状态：partially_parsed / key_content_verified / complete
- 题号：B
- 核心模型：nonnegative_integer_equation、constrained_enumeration、models_A_to_F
- 方案谱系：lineage_cumcm_1992_b_amino_acid

## 人工核验摘要

{
  "problem_and_subproblems": [
    "求非负整数方程的全部解",
    "利用化学信息缩小解空间",
    "分别设计有/无微机方案"
  ],
  "data_types": [
    "整数",
    "氨基酸分子量",
    "元素组成约束"
  ],
  "mathematical_essence": "一元总量约束下的高维非负整数可行解枚举。",
  "data_preprocessing": [
    "合并等分子量氨基酸",
    "减去已知必含成分",
    "按元素组成减少变量"
  ],
  "baseline_models": [
    "18变量非负整数方程"
  ],
  "core_models": [
    "加入C/N/O/H守恒的模型A",
    "利用已知氨基酸集合的模型B/C",
    "0-1简化模型D",
    "仪器信息模型E/F"
  ],
  "parameter_sources": [
    "题给18种分子量",
    "文献中的元素组成",
    "经验含氮比例15%—17%"
  ],
  "validation_methods": [
    "多组X的解数和运行时间对比",
    "不同约束模型的并列表格"
  ],
  "important_results": [
    "X=1000时一般模型有28268解",
    "加入含氮约束后降为10954解",
    "模型F在可获得比例信息时可给出唯一解"
  ],
  "abstract_structure": "问题—一般模型规模—模型A至F—测试—全文结构。",
  "section_structure": [
    "问题提出与分析",
    "假设和符号",
    "一般模型",
    "改进模型A—F",
    "改进方向",
    "误差与优缺点"
  ],
  "innovation_expression": "把化学元素守恒、已知组分和仪器信息逐层转化为约束。",
  "strengths": [
    "基线与逐层约束对比清楚",
    "运行时间和解数均有测试"
  ],
  "limitations": [
    "X=1000时改进后解数仍多",
    "部分经验约束可能不真实",
    "未公开程序源代码"
  ],
  "reproducibility_level": "medium"
}

> 仅保存结构化短摘要和页码证据；完整提取正文为本地忽略缓存。
