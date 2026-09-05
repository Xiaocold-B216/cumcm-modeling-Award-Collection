# Knowledge Card

## Basic Information

- Paper ID: CUMCM-2017-B-006
- Year: 2017
- Problem: B

## Evidence-based Content

The following excerpt is copied deterministically from the generated paper body; no method or conclusion is inferred beyond this source evidence.

> 摘要 在“拍照赚钱”的新自助式服务模式下，用户可领取 app 上的任务，成功执行 便可赚取标定的酬金。在这种模式下，如何合理定价从而获取最高收益成为了系 统运营的核心。本文针对题中所给的数据信息进行数
> 据挖掘，设计了一套较为合 理的定价及任务打包算法。 问题一中，我们首先猜测了可能影响任务定价的因素，包括：任务周围的用 户限额总量、任务周围的用户密度、任务的离群程度等。我们量化以上可能的影 响因素，
> 并以该因素为自变量以定价为因变量回归分析，通过拟合度来判断该因 素是否对定价有决定作用。我们随机抽取 70%的数据进行回归训练，结果表明， 任务的定价与周围用户的限额总量、周围用户的平均距离、自身的离
> 群程度关系 密切。利用剩余的 30%数据分别对以上回归方程进行检验，用均方残差偏移程度 来评价方程的可靠性。根据三个因素，对于成功执行的任务与未成功执行的任务 分别进行回归分析，并对比其回归函数图像，
> 发现任务未完成的主要原因是用户 没考虑自身限额对定价的影响，其余两个因素相对次要。 问题二中，我们建立了多目标优化模型，其中目标函数为总定价和成功率。 对问题一中的完成与未完成的任务，我们可以分别拟合
> 出其定价曲面，位于这两 个曲面之间的区间即为合理定价区间。除了问题一中三个因素外，任务成功率还 受到周围用户的信誉、预订任务时间等变量的影响。根据已有的数据回归分析， 得到成功率的综合评价函数。基于合
> 理定价区间的约束，我们分别对定价最优方 案与成功率最优方案进行求解，经过我们的算法优化之后，与原方案相比，我们 可以在同样的平均成功率的前提下将定价总额降低 2.9%；我们也可以用同样的 定价总额将平
> 均成功率提高 9.4%。 问题三中，我们建立基于改进的 DBSCAN 算法的打包方案。确定打包的核 心目的是改善预期成功率较小任务的执行情况。我们引入了任务的得分半径和用 户得分半径两个参数对原算法中

## Evidence

- Evidence granularity: page
- Source pages represented: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45

## G11 Repair Evidence

This block records deterministic repair provenance only; no semantic claim is inferred.

- Repair stage: G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR
- Repair attempt: 20260905T045418589698Z_557724fba657
- Route categories: MARKER_ONLY_DIAGNOSTIC_OCR_REUSE
- Repaired source pages: 33, 36, 38, 39, 43
- Preserved legitimate noncontent pages: none
- Candidate paper artifact SHA-256: 86823A24C555358151351AD2FF144E44AD8B71CC3FC0019FD16EC32F79BA75E9
- Source binding: PASS
