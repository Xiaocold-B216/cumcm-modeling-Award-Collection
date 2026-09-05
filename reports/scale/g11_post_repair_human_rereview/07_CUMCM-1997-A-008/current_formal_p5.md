# Current Formal Excerpt — CUMCM-1997-A-008 — source page 5

- Current body: `derived/scale/papers/CUMCM-1997-A-008/paper.md`
- Current body SHA256: `B222A793AF8346A5E568837E9D9BC95B69DBC29AFA500759EE26E9CAD53AAB66`
- Current page segment SHA256: `8764CD4B090805ABCCEDB9F4D1D9A1F1CB5ABD21A2E74B6A35CD52EDD3BF75A3`
- Extraction method: `STRICT_SOURCE_PAGE_MARKER_BOUNDARY`
- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`
- Repair page audit: `catalog/scale/g11_multi_route_formal_repair_pages.csv`

The block between the delimiters below is copied from the current `paper.md` substring. No human wording, OCR, rendering, or extraction was added in this stage.

<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->
<!-- source_page: 5 -->

数

学

劝 由蒙待卡洛 法模拟 产 生

把

,

二,

计算统计量
拟 合优度 ,

与

践

二

。
、 ’

、一

实

认

卷

识

个样本值
并使 , 全
’ 个 区 间 并判断样本落在 各 区 间的频数
、
。
,
,
。
‘
二
其中 为正 态分布
二 在第 个 区 间 内的理论概率 ,

的

的 可能取值 范围分 成

,

的

。‘,

,

‘,

,

‘

,

一 、

孟

通过 计算 我 们得 到 ,
,

,

,

这说 明我们用正 态分布 州 。 弓 来近似
,

,

的实际分布是 可靠 的

。

模拟的误 差
。

,

我 们用 蒙特卡洛 法模拟 , 的分布 时使用 的样本个数是

与成批 生产 的 产量 一致 但是计算机
模 拟 的统计量必 然有 一定 的波动性 我们对 同样一 组标定值和 等级进 行多次模拟 发 现 目标 函 数 的波
动程 度在
元左 右 因 此 我 们的模 型所给 出 的精度顶多也 只 能达 到 这个值
,

,

,

,

流

参数选择分两 步 走 的有效性

若 同时对标定值和 容差等级求最优解 则计算复杂度过大 为此 我们采用 了两步走 的近似 方法
第一 步 使各零件都取最低容差 等级 求 出各零件标定值的最优 解 梯度法
,

,

,

求容差 等级的最 优解 遍 历

作为对 比 在 线性 模 型 中 我 们 同 时考虑 标定值和 容差 等级 也用梯度法 求得 极值
这 和 分两步走 的结果
元非常接 近 这说 明了我们的分两步 策略是 十分有效 的
,

,

,

,

,

、

、 讨

论

的另一 种理 解

：
科

质量损失 ,

,

结果为

研

元

交

第二 步 固定标定值

,

有些产 品参数 离 目标值越近 越好 甚 至于突破人 为 的等级限制 即 。 , 随 , 连续 变 化 而 不 是如
,

,

二。 , 一‘

所述 的阶梯 函 数 一种 可能的情况 是 。

假设

·

”,

其中 “二

,

·,

,

此时 “ 二

了

、

侧,一

。

·

“

这正是我 们前 面 提 出 的第二 个 目标 函 数 以这种解释求 得的 目标函 数最优解
局 部 最优解和 全 局 最优 解

我 们的模型 给 出的都是局 部 的最优解 区域内的极 值

如果多取几 个初 始值求极值 的话

号

最 优解 但是

,

达 到最优解
优缺点分析

我 们给 出的都是局 部 的最优解

,

,

信

兀

、

并 不能保证 它就是 间题 的全局最 优解
,

微

盛 昭瀚
徐士 良
陈希孺

,

,

这 使得 我们给出的总 费用精度有限

参 考 文 献
,

严颖 成世学 运 筹学随机模型
、

‘

同时也给出了 非常接近 最优解的结果

由于 进行 蒙特卡洛方法模拟 的次数 有 限
·

,

中国人 民大学出版社 北 京

曹忻 最优化方法基本教程
,

,

,

东南 大学 出版社 南京
,

,

常用算法 程 序曳 清华大学 出版社 北京
概率论与数理 统计

,

,

从而提高 了运算速 度 ,

,

线性模 型 在 一般 的情况下也 能 给出 比较理想 的结果 ,
分 两步 走的策略有效地 简化 了 问题

这 不一定就是 目标 函 数在 整个 区 域内的

可 以尽可能 缩 小 我们的结果与最优解的差距 甚 至

,

线性模型避免 了蒙特卡 洛法所 需 的大量模 拟

公
众

·

,

,

中国科技大学出版社 合肥
,

,

,

,

,

误差 为 士
<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->
