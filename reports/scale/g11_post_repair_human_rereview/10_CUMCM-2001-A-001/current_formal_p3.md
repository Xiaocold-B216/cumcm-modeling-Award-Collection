# Current Formal Excerpt — CUMCM-2001-A-001 — source page 3

- Current body: `derived/scale/papers/CUMCM-2001-A-001/paper.md`
- Current body SHA256: `25E382CD5CE4F99D69F070B726A4A72EB33EDE0E295075941C1F42856F80AC3E`
- Current page segment SHA256: `FCE591C93A86CACD679D19072BEB9AF2C4C376C36C00386F899F991DCE49D8C9`
- Extraction method: `STRICT_SOURCE_PAGE_MARKER_BOUNDARY`
- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`
- Repair page audit: `catalog/scale/g11_multi_route_formal_repair_pages.csv`

The block between the delimiters below is copied from the current `paper.md` substring. No human wording, OCR, rendering, or extraction was added in this stage.

<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->
<!-- source_page: 3 -->

维普资讯 http://www.cqvip.com

建 横专 辑

血 管切 片 的三 维重 建

图 １

图 ２

１） 题 目 中截 面 边 界 上 的 点 的 坐 标 是 从 图象 中 读 取 的 ，
这 些 数 据 是 经 过 离 散 化 的 ，因 而边
界 曲线 并 不 光 滑 ，
无 法 精 确 作 出 边 界 曲线 在 任 一 点 处 的 切线 。
十这样 的点 。

为了克服 第一个 困难 ，
我 们 设 计 出下 面 的 算法 一 ：

流

２） 定 理 只给 出 了截 面 上 的点 在 中轴 线 上 的 必 要 条 件 ，所 以 在 一 片 截 面 上 可 能 会 出 现 多

交

先 把 每 张取 定 的藏 面 图 中所 有 点 编 号 ，
根 据 编 号 将 图 的 边 界 点 划 分 为 上 弧 、下 弧 。对 于 上
弧 上 固定 的 一 点 ｎ ，
求 出该 点 到 下 弧 上 点 ６，的 距 离 ｄ 令 ｄ

ｍｉ
ｎｄｌ
】Ｄ 当

ｉ取 遍 上 弧 中每 一

研

点，
并得 到其对 应最短 距离 ｄ ，
令 Ｄ ＝ｍａｘ
ｄ ，则 Ｄ 为 由该 截 面 所 确 定 的管 道 直 径 。
为 了 克 服 第 二 个 困难 ，
我 们设计 的算法二 ：
该 截 面 与 中 轴 线 的交 点 。
具体 求解过 程如下 ：

：
科

对 可 能 为 球 心 的 ”个 点 ０（１≤ ≤ ），
把 ｃ 中到 其 余 ｎ一１个 点 的距 离 之 和 最 小 的 点作 为

Ｓｔ
ｅｐ１．对 于 １００张 截 面 图 ，
用 ＶＣ＋ ＋编 程 读 出每 张 图 的 边 界 点 。将 边 界 曲线 分 为 上 弧 、
下弧 。

号

Ｓｔ
ｅ
ｐ２．由 ｚ：９９截 面 图 象 用 算 法 一 计 算 出直 径 ＤＣ
９
９
）以及 中轴 线 ｃ 被 平 面 ｚ＝９９截 得 的

众

点 ｃ（’（ ， ）。得 到 Ｄ（）：５９ １３
５
４ｐｉ
ｘｅ
ｉ
。
并确定 出取 到直径 的端点 尸｛’（１
ｚ｛ ， ｛ ），
尸ｌ （
－
ｚ ，
ｙｌ’），
取中点得 ｃ 。满足上述条件的点可能不止一个 ，
我们利用算法二求出
ｃ（
９
９）， 其 坐 标 为 ｃ（
’
’（１５，一１
８８）。

Ｓｔ
ｅ
ｐ３．设当 ｚ＝ｉ时已经求出Ｃ 和 尸ｉ’
（ｆ
“，

），
尸 （－
ｚ ，

），由于相邻两个截

公

面之 间 的距 离 很 小 ，
从 而 ｃｃＩ１在 截 面 ｚ＝ ｉ上 的 投 影 和 Ｃ“）
的距离很 小 ，
故 在 ｚ＝ ｉ一１的 截

面上分别 以 尸｛ （ ｛
”， ｝ ），
尸｛
’（ ｛
“， ｉ ）为 圆心 ，
３０
ｐｉ
ｘｅ
ｌ为半径作圆与

‘
ｉ交 出弧段

信

ｓ｝ ，
ｓ； 。利用算法一求 出坐标 ｃ（
’ 和直径 Ｄ（ ）
。依照上面的做法 ，
依次对 ｚ＝９
８，
ｚ＝

９７，
…．
－ｚ＝０截 面 进 行 计 算 ，
得 到 Ｄｃ ，以及 中轴 线 与 备 平 面 的 交 点 的 坐 标 Ｃ“ （ｚ， ），（ｉ＝

微

０，１，
…… ，
９８）

‘
Ｓｔ
ｅ
ｐ４．我 们 最 后 根 据 Ｄ¨ （０≤ ｉ≤ ９９）
求 出直 径 的 平 均 值 为 ５９ １２３８ｐｉ
ｘｅｌ
，
从 而 Ｒ ＝２９．

５６１９ｐｉ
ｘｅｌ。

Ｓｔ
ｅ
ｐ５．对 于 计 算 得 到 的 １００个 中轴 线 上 的点 ，
我 们 用 Ｍ ａｔ
ｈｅｍａｔ
ｉ
ｃａ软 件 对 其 进 行 拟 台 ，
从
而 得 到 管 遭 中轴 线 的 拟 合 曲线 方 程 。
（１）折线 连 接

由于 管 道 长 度 很 短 ，
故 得 到 的 １００个 点 彼 此 间 的排 列 很 紧 密 ，因 而 我 们 可

以用 折 线 连 接 的方 法 得 出 中轴 线 的近 似 曲 线 。对 此 曲线 分 别 向 ＸＯＹ，ＹＯＺ，ＸＯＺ平 面 作 投
<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->
