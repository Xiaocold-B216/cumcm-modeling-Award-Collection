
    # 基于成分数据分析的玻璃制品分析与分类：模型与算法摘要

    ## 建模链条

    - 对缺失值和组成数据零值使用插补/乘法替换，并进行闭合处理。
- 用 Spearman 相关与卡方检验分析风化关联；用 Dirichlet 回归预测风化前组成。
- 对组成数据做 clr 变换，用决策树进行主分类。
- 使用 PLS-DA 与 VIP 识别重要成分，用 K-means/聚类方法确定亚类。
- 使用 Pearson 与 Wilcoxon 检验比较类别相关结构。

    ## 论文报告的主要结果

    - 论文将玻璃主类划分为高钾与铅钡，并进一步给出若干亚类。
- 通过决策树与 PLS-DA 两条路线对未知样本交叉判别。
- 聚类数通过 SSE/轮廓或组间分离图进行选择，正文采用三类亚群方案。

    ## 方法标签

    - 乘法替换与闭合处理（compositional_preprocessing）：处理成分数据零值与总和约束，证据页 4, 5
- Spearman 相关（nonparametric_statistics）：分析风化与属性关系，证据页 6
- 卡方检验（hypothesis_test）：检验类别属性关联，证据页 6
- Dirichlet 回归（compositional_regression）：预测风化前化学成分比例，证据页 8
- clr 变换（compositional_transform）：将组成数据映射到欧氏空间，证据页 11
- 决策树（classification）：划分玻璃主类别和未知样本，证据页 11, 17
- PLS-DA 与 VIP（classification）：识别分类成分并交叉判别，证据页 12, 16
- K-means/聚类分析（clustering）：划分玻璃亚类，证据页 13, 15
- Pearson 与 Wilcoxon 检验（correlation_comparison）：比较类别间相关结构，证据页 18, 19

    ## 复现状态

    本轮未把图片中的代码转写为可执行源码，也未在缺少官方数据附件的情况下伪造运行结果。所有数值均标记为论文自报结果。
