# Extracted Paper

<!-- source_page: 1 -->

加
第 31 卷 第 1 其 数学 的 实践 与 认识 Vol31 NO 国 =
2001 年 ! 月 MATHEMATICS N PRACTICE AND THEORY Jan_2001
Abstract Asto the problem of the tine needed for an airp lane to start from Beijing, fly over
arctic pole, and reach Detroit, this article discusses how much tine can be saved in the models
that established in the article in comparison w ith the original flight route And it summarizes
selection of the flight route for searching the shortest arc in the surface Discussion is based on
the fact that the shortest arc on surface is geodesic Model 1 is on the assumption that the
Earth is a sphere It can be solved by the relation betw een inner-product and included angle of
two unit vectors Model2 ison the assumption that the Earth is a revolving ellpsoid It can be
solved by the geodesic equation in differential geometry, which turns latitude of theE; into
thatof ellpsoid For the 4pairs of special points, their latitudes or longitudes < 从;
calculate geodesic, so we replace geodesic w ith ellpse arc，and use softwareM an to
obtain the length 74
航程 计算 的 全
N\e
EG S | SS
(复旦 大 学 辐 上 海 400433)
人 os
摘要 : 。 本文 对 飞机 航线 飞行 距离 计 斤 尘 模型 进行 了 概述 , 并 对 2000 年 全 国 大 学 生 数学 建 模 竞赛 的 C
题 答 卷 进行 了 评述
\ =- 一
假定 飞机 保持 飞行 高 席 !j F 且 作 匀速 飞行 , 忽略 起 飞 、 降落 和 地 球 自转 和 公转 的 影响 ，
C 题 可 以 归结 为 求 飞越 通 过 指定 各 点 的 球面 或 旋转 椭 球 面 上 的 短程 线 (或 测 地 线 ) 的 航线 与
飞越 直接 连结 北 训 上 衬 .10 干 米 至 底特律 上 空 10 千 米 的 经 过 北极 圈 的 新 航线 的 时 间 差 又
hr 千 米 /小 时 的 匀速 飞行 , 问题 又 可 归结 为 求 相 应 的 航程 差
CA
1 人
< 隔 直 角 标 系 如 下 : 以 球 心 为 原点 ,= 轴 指 向 北极 ,x 轴 通 过 赤道 上 经 度 为 0 和 180" 的
Tie 二 may 指向 0 y 轴 重 直 于 x 轴 和 = 轴 , 构成 右手 坐标 系
忆 在 半径 一 6381 (TK) 的 球面 上 建立 球面 坐标 系 (9 6 , 由 于 航线 在 北半球 , 我 们 取 9 和
北纬 度 一 致 , 6 和 东经 度 一 致 因此 航线 上 某 处 的 地 理 坐 标 为 , 0), 可 用 以 下 方法 得 到 对 应
的 球面 坐标 (9 9 :
9 广义 /180
. {: IARS
360 - /为 西 经
6= 8 XTX180
应 有
3 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved 1tp.//WWW.CRKi.ne

<!-- source_page: 2 -->

EREE
1 期 谭 永 基 航程 计算 的 数学 模型 Se
x= rcos9qcosQ
y= rcos Psin Q
z=r sin @
若 球面 上 两 点 的 球面 坐标 为 (9 6),，(92 6) , 过 这 两 点 的 短程 线 是 过 这 两 处 的 大 圆 的
劣 圆 弧 ( 即 长 度 较 短 的 一 条 大 圆 弧 )， 从 球 心 指 向 此 两 点 的 矢量 分 别 为
(rcos 9ycos 6.rcos9%sin B, » sin P,i= 1,2
设 它们 的 夹 角 为 w 则 有
cos X= c0s Rcos B cos Peos & + cos 9? sin 6 cos 9 sin e+ KR
从 而 求 得 x 进而 求 得 过 这 两 点 的 航程 7 一 A7
多 数 参赛 队 都 能 正确 计算 航程 , 从 而 获得 节省 时 间 大 约 为 3. 91 小 时 才 结 过 则 主 题目 未
给 出 北京 和 底特律 的 经 纬度 , 有 些 队 对 两 地 的 经 纬度 误差 估计 较 大 ， 5
2 设 地 球 为 旋转 椭 球 的 情形
此 时 , 飞机 的 航线 位 于 方程 为 As
| 6388 2
?= 6388 cos Psin.
= = 6367 “加
的 旋转 椭 球 面 上 , 它 通 过 给 定 地 理 坐 z
标的 各 点 , 在 相 邻 两 点 间 为 上 述 覃 球 O
面 的 短程 线 在 大 地 测量 中 , -点 的 ji 孝 SS
球 坐标 (/, 妨 中 的 地 理 纬度 是 这 样 区
义 的 : 用 通过 该 点 的 子 竺 面 与 [ 球 交
得 一 椭圆 , 过 该 点 作 烛 圆 的 法 线 。 法 线
人
( 见 图 1D. 全 =”
由 于 这 可 机 天 天
二 638glos 9
V 67 sin 9 图 1
si
这- 人 6388 | [ 6367 |
N 6367 cos P | | 6388 sin P
从 tan P= tan 太 ， 9 ul eu]
得 到 我 们 所 需 的 纬度 , 文献 称 为 归 约 纬度
在 一 般 的 有 关 大 地 测量 的 文献 中 均 有 对 地 理 纬度 与 归 约 纬度 之 间 关 系 的 论述 但 有 较
多 答卷 直接 将 地 理 纬度 作为 归 约 纬度 建 模 计算 ” 虽 因 长 短 半 轴 差别 较 小 , 计算 误差 不 算 大 ，
但 作为 精确 的 数学 模型 , 这 种 做 法 是 有 缺陷 的
就 笔者 所 知 , 到 现在 为 止 尚 未 得 到 过 旋转 椭 球 面 上 任意 两 点 的 短程 线 的 解析 表达 式
奔 大 地 测量 学 和 航海 学 的 有 关 文 献 中 采用 个 一 些 有 效 的 近似 公式 如 贝 宕 尔 公式 等 在 参赛

<!-- source_page: 3 -->

E
116 数学 的 实战 与 认识 1 tien
队 中 采用 这 种 方法 也 不 在 少数 其 中 有 些 队 从 求 短程 线 出 发 , 建立 模型 , 经 合理 简化 得 到 相
应 的 计算 公式 , 这 是 可 取 的 ; 另 一 些 队 简单 生硬 地 套用 公式 , 多 少 偏 离 了 数学 建 模 竞 赛 的 宗
旨 和 要 求 , 他 们 的 答卷 不 能 认为 是 优秀 的 答卷
解决 问题 的 另 一 方法 是 建立 问题 的 变 分 模型 这 种 方法 根据 航线 是 短程 线 的 要 求 , 将
过 给 定 两 点 的 曲线 的 长 度 表示 为 依 原 该 曲线 的 参数 方程 的 一 个 泛 函 , 在 满足 该 曲线 落 在 旋
转 椭 球 面 上 的 约束 条 件 下 , 使 该 泛 函 达到 最 小 在 用 Lagrange 匀 子 法 后 得 到 Euler 方程 , 然
后 对 此 方程 用 数值 方法 , 得 到 近似 短程 线 有 几 个 参赛 队 采 用 此 方法 , 并 得 到 Euler 方程 的
表达 式 ”但 因 方 程 较 复 杂 , 未 能 最 终 求 出 数值 解 A
还 有 一 个 方法 就 是 用 微分 几何 知识 直接 获得 顶 球 面 上 短程 线 应 满足 的 微 pe
微分 方程 表达 式 得 到 弧 长 计算 公式 , 并 用 数值 积分 法 求 得 短程 线 的 近似 长 度 \eaet 参赛 队
建立 了 这 样 的 模型 , 得 到 了 结果 人
一 种 比较 直观 的 方法 就 是 直接 搜索 法 , 即 在 椭 球 面 上 过 给 负 中 Earasn
长 度 最 短 的 一 条 作为 短程 线 的 近似 Se 惧 分 , 需要 将 9 和
进行 剖 分 , 这 就 将 问题 化 为 一 个 离散 的 优化 问题 , 可 以 采用 优 和 的 邓 法 求解 在 本 期 发 表 的
优秀 论文 中 有 一 篇 采用 了 在 一 类 椭 球 面 上 过 给 定 两 点 的 曲线 中 进行 搜索 的 方法
较 多 的 答卷 直接 将 地 球 作为 球 的 结果 移植 到 从 光志 蔷 央 球 的 情形 , 简单 地 认为 “过 机 于
面 上 给 定 两 点 的 短程 线 即 为 过 此 两 点 和 地 心 的 平面 与 粳 球面 交 线 的 劣 弧 ( 两 点 间 较 短 的 一
条 ) ” 这 一 结论 是 错误 的 , 有 时 会 导致 很 大 的 误差
数学 软件 M athem atica 的 程序 库 中 有 驱 近 似 测 地 线 的 函数 , 利用 这 一 函数 不 难 求 出 各
点 之 间 的 航程 有 个 别 参赛 队 没 有 建 3 给 适 的 数学 模型 直接 调用 这 一 函数 , 得 到 近似 的 结
果 , 不 能 视 作 好 的 答案 区 A
TR 条 作为 他 证 和 评价 自己 模型 的 手段 之 一 , 这 是 很 值得 称道 的
Math aa odeling for D istance Calculation
4 v of Airline
g)
下 4 TAN Yong-ji
¥y (Fudan University, Shanghai 400433)
长
N.... The sketch of the mathematicalmodeling for the Calcalation of the distance covered
by an airline is discribed Some comments to the answer paper for the problem C of 2000 China
undergraduateM CM are given
3

