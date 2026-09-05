# Current Formal Excerpt — CUMCM-1999-B-003 — source page 3

- Current body: `derived/scale/papers/CUMCM-1999-B-003/paper.md`
- Current body SHA256: `5AF0061C03FA255BA04B35F28021E9090E4CDF772FF87BCB7E617B6A4A634CF9`
- Current page segment SHA256: `287E7614BB939A5263DF25A1DBAC7664F0B1C78CA9CA410682D53ED6D406337C`
- Extraction method: `STRICT_SOURCE_PAGE_MARKER_BOUNDARY`
- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`
- Repair page audit: `catalog/scale/g11_multi_route_formal_repair_pages.csv`

The block between the delimiters below is copied from the current `paper.md` substring. No human wording, OCR, rendering, or extraction was added in this stage.

<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->
<!-- source_page: 3 -->

1期

徐胜阳等: 钻井布局

57

旧井及其映射点的方位

：
科

图1

研

交

流

边界问题 图 2 中, 由粗线围成的区域为映射区, 与其内部的细线围成环状区域, 其宽
度为 Ε. 由旧井方位 P 1 与 P 2 映射而成的两点 P 31 与 P 32 分别分布在映射区两条对边的附
近, 与对应边的距离均不超过给定误差 Ε, 它们可能同时成为可利用点. 如果直接用 Ε—邻域
在映射区穷举, 则不可能同时容纳这两点. 为了不漏掉可能的最优解, 下面给出边界问题的
解决方法.

图2

边界问题示意图

412

公
众

号

如图 2, 网格的右、上两条边附近有区域 A , B , C , 将这些区域及其上的所有点分别复制
到对应区域 A 3 , A 3 , C 3 . 为了易于编制程序, 将左上角与右下角区域也补齐, 形成一个边长
为 1+ Ε的扩大的正方形搜索区域, 那么原有的点与点之间的关系将全部反映到映射后的网
格上, 从而解决了边界问题, 得到了完善的算法. 在计算机上求解得出, 在第一象限内, 距原
点最近的网格结点, 相对于原点的横向偏移为 0. 4, 纵向偏移为 0. 5, 可利用点为第 2, 4, 5,
10 点.

微

信

问题二: 无方向约束的求解问题
显然, 问题一是问题二的特殊情况. 下面探讨无方向约束下的求解问题. 为了方便研究,
在约定中给定了三种坐标系 S 、S 1、S 2.
我们所关心的是源点坐标系 S 1 与网格坐标系 S 2 之间的相互关系. 如图 4, 令源点坐标

图3

三个坐标系

图4

最优解下网格的覆盖方式
<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->
