# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
多
第 19 卷 建 模 专辑 工程 数学 学 报 Vol. 19 Supp.
2002.02J3 JOURNAL OF ENGINEERING MATHEMATICS feb- 2002
文章 编号 :1005-3085(2002)05-0041-06
管 切片 的 三 维 重建
血管 切片 的 三 维 重 建  -
人 { Se
柳 海 东 ， 陈 璐 ， 江 浩 = 蛋
指导 教师 : ” 卢 钦 和 2XG
(苏州 大 学 ,苏州 215006) 本
编者 按 :本 文 指出 在 一 定 的 条 件 下 ,血管 中 轴线 与 截面 的 交点 必 沙 在 截面 边界 上 贤 ea 中 点 上 ,过 这 对 点 的 截面
边界 的 两 条 切线 是 相互 平行 的 。 据 此 ,设计 出 相应 的 算法 , 计 算 结 果 比 较 精 卫 o 痊 求 得 中 轴线 的 离散 点 后 进行 了 多
项 式 拟 合 得 到 中 轴线 方程 。 文 章 用 多 种 方法 对 建立 的 模型 进行 三 恰 验 5 这 是 本 文 的 主要 优点 之 一 。
摘 ， 要: 本文 讨论 血管 的 三 维 重建 问题 。 我 们 通过 研究 ,证 明了 以 Filist,
定理 ” 设 C( 纪 是 中 轴线 和 平面 Z= i FIZ2A, BAtEEL, c(i) fd FL AG 户 ( 引 , 户 亿 在 go( 坟 上 的 线段 ,并 且
在 户 (7 , 户 ( 亿 处 知 ( 纪 的 切线 相互 平行 。
根据 定理 ,我 们 找到 利用 求 截面 图 象 边界 曲线 的 平行 切线 方法 找到 中 轴线 和 100 个 截面 的 交点 及 管道 的 直径 59.
1238pixel 。 并 用 这 100 个 交点 的 数据 拟 含 出 中 型 线条
X(1) = - 0.207806 - 0.61030 106455 ¢2- 0.0144935 °
+0.000517774 ¢* - 8.394 41977754047 x10 -55
+6. 133353112035975 何人 2 ) .6673218267444805 X10 007
3 =158.211+ 1.§6595, - 0.266798 * +0. 0141407
NT 65
- 0.0003254 AR 043275597680807 X10 5
- 9.899171274615063 x10 ?14
(0 =
menrmsucp AieT=nur puTERARS | 个 平面 上 的 截面 w' 7 (30 <i <69) ,并 与 原始 截
面 omA0/ <9 角 进 每 比较 ,截面 平均 符合 率 高 达 96. 8024 %。
关键 局 : 切 缚 多 os
2 二 AMS(2000) 65D17 中 图 分 类 号 : 0242.1 文献 标识 码 : A
1 " \
RH
和 so
2 模型 假设
JU 不 考虑 血管 的 弹性 ,将 血管 视 为 一 类 特殊 的 管道 ,其 表面 由 球 心 沿 某 一 曲线 ( 称 为 中
轴线 ) 且 半径 固定 的 球 滚动 包 络 而 成 。
2) 管道 中 轴线 与 每 张 切片 有 且 只 有 一 个 交点 。
3) “切片 间距 以 及 图 象 象 素 的 尺寸 均 为 1 ,可 将 切片 图 象 视 为 平面 图 形 。
沁 。” 中 轴线 充分 光滑 且 它 每 一 点 的 曲率 K( 0 较 小 (有 本 > R, R 为 管道 半径 ) 。
2 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved. http://www.cnkinet

<!-- source_page: 2 -->

[ElimahE
Erie
4 工程 数学 学 报 第 19 郑 oem
3 符号 说 明
pixel 象 素 单 位

c 中 轴线

c 拟 合 出 的 中 轴线

Cr 中 轴线 被 平面 Z- ; 截 得 的 点 的 坐标 (0 <i <99)

0 (x(1) fm) 拟 合 出 的 中 轴线 被 平面 =- ; 截 得 的 点 的 坐标 /0 <i <09)

DO 由 Z- / 截面 图 象 求 得 的 管道 直径 (0 <i <09) <=A_

R 管道 半径 =4isD

s |mawwwn_p 个 )

ke p.

可

H (xf” ") | sam ob HED S9.1  <

oo | mgossy 人 这 |

oo | mamin z- wmEirby

杷 | 7 和 的 地 外 oo

ao 人 拟 合 出 的 z= ; 截面 图 象 的 边界 /0 <i <99)

O
4 问题 分 析 Y4/ / °

这 是 一 个 重建 三 维 图 象 的 问题 ,所 给。 张 截面 图 是 分 别 由 平面 Z-0.Z=1 .wzZ
=99 截 管道 得 到 的 。 i 张 图 片 琶 加 起 来 得 到 管道 在 YXO7 平面 上 的 投影 (如 图
1) in z 的 增 大 而 逐渐 变 小 。

为 了 得 到 血管 重建 的 方法 | 我们 证 明了 下 面 的 定理 。

定理 设 Ce Z= :的 交点 ,那么 存在 以 c(7” 为 中 点 且 端 点 Pf”, 性 7 在
5 用  P 处 go 儿 的 切线 相互 平行 。

定理 的 证 朋 略 。

人 的，onronnnauaraanramao 过 截面 图 象 边界
[ 边界 曲线 的 切线 工 ,过 o fF L) 的 垂 线 与 对 弧 交 于 点 。 如 果 过 5 点 的 切线
证 wa ab 的 中 点 c 可 能 是 中 轴线 和 该 截面 的 交点 ,线段 ac 的 长 度 等 于 管道 的
半径 鼠 ( 见 图 2)

我 们 在 每 个 截面 上 找 出 这 样 的 点 ,并 根据 这 些 c 点 的 坐标 数据 拟 合 出 管道 中 轴线 的 方
程 ,从 而 实现 血管 的 三 维 重 建 。

5 模型 建立 与 求解

根据 上 面 的 分 析 ,理论 上 我 们 可 以 对 每 张 截 面 , 用 上 述 方法 找 出 中 轴线 和 该 截面 的 交点 和
管道 的 半径 。 但 具体 实现 时 会 遇 到 下 述 两 个 问题 :

9 0 hin， mis ctron ubl H Al cnk
模 大

<!-- source_page: 3 -->

回 叶 这
全
建 模 专辑 血管 切片 的 三 维 重建
: . ;
: we
a No
图 1 图 2 二 和 从》
了 ) 题目 中 芝 画 这 站 上 的 点 的 华 标 是 从 图 角 中 读 取 的 .这些 数据 是 经 过 次 (名 从 而 边
界 曲线 并 不 光滑 ,无 法 精确 作出 边界 曲线 在 任 一 点 处 的 切线 。 =
2) eg sun
个 这 样 的 点 。 /
为 了 克服 第 一 个 困难 ,我们 设计 出 下 面 的 算法 一 :
先 把 每 张 取 定 的 截面 图 中 所 有 点 编号 ,根据 编号 将 图 的 边 外 总 划分 为 上 弧 、 下 弧 。 对 于 上
弧 上 固定 的 一 点 w, 求 出 该 点 到 下 弧 上 点 by 的 距离 8 当 ww 取 遍 上 弧 中 每 一
点 ,并 得 到 其 对 应 最 短 距 离 w, 令 D =maxd;, ll "清和 重 所 确定 的 管道 直径 。
为 了 克服 第 二 个 困难 ,我们 设计 的 算法 二
对 可 能 为 球 心 的 半 个 点 cll <i <n) He 中 到 其 余 ”- 1 个 点 的 距离 之 和 最 小 的 点 作为
该 截面 与 中 轴线 的 交点 。 $, V 4 ©
有 具体 求解 过 程 如 下 :
Step1. 对 于 100 张 截面 图 ,用 C++ 纺 程 读 出 每 张 图 的 边界 点 。 将 边界 曲线 分 为 上 弧 、
下 弧 。 _，
Step2. 由 Z= 99 截面 9 DOY 以 及 中 轴线 C 被 平面 Z= 99 截 得 的
点 C09 (x,y) 。 得 到 -DB 镶 =59. 1354pixel, 并 确定 出 取 到 直径 的 端点 PY (x, 9(*),
二 Cf0? 。 满 足 上 述 条 件 的 点 可 能 不 止 一 个 ,我 们 利用 算法 二 求 出
cf09 ,其 坐标 间 c® (15, - 188) 。
si i 时 已 经 求 出 cVR PCxz 人 人) PEY (xz 刀 ,2 光 ,由 于 相 邻 两 个 截
aa ,从 而 c0 7 在 截面 Z= 守 上 的 投影 和 c0 的 距离 很 小 , 故 在 Z=i- 1 的 截
四 汐 2” (人 yy 所) P2Yxz 亿 ,世人 为 圆心 ,30pixel 为 半径 作 圆 与 to 必 交 出 弧 段
本 。 利 用 算法 一 求 出 坐标 C 和 “和 直径 DOY 。 依 照 上 面 的 做 法 ,依次 对 Z=98,Z=
97，' 衬 "Z=0 截面 进行 计算 ,得 到 D4”, 以 及 中 轴线 与 各 平面 的 交点 的 坐标 ¢ (xz , 攻 , (i=
0,1, 98)
Step4. 我 们 最 后 根据 Dr0 <i <99) 求 出 直径 的 平均 值 为 59. 1238pixel ,从 而 R = 29.
5619pixel 。
Step5. 对 于 计算 得 到 的 100 个 中 轴线 上 的 点 ,我 们 用 Mathematica 软件 对 其 进行 拟 合 , 从
而 得 到 管道 中 轴线 的 拟 合 曲线 方程 。
(LU 折线 连接 ”由 于 管道 长 度 很 短 , 故 得 到 的 100 个 点 彼此 间 的 排列 很 紧密 ,因而 我 们 可
以 用 折线 连接 的 方法 得 出 中 轴线 的 近似 曲线 。 对 此 曲线 分 别 向 YXO7Y，y7OZ，XOZ 平 面 作 投
# 工
1994 i c Journal n h H 1 esel

<!-- source_page: 4 -->

ERi
多
44 工程 数学 学 报 第 19 T
影 得 到 三 条 相应 的 投影 曲线 。
(2) 曲线 拟 合 ”把 中 轴线 方程 表示 为 参数 式 C: (xz (0 ,7( , 吃 , 其 中 关 ( 力 ,7( 必 均 是
的 多 项 式 ,z(b = ¢, 3:F Mathematica 中 的 非 线性 拟 合 (Statistics NonlinearFit 对 中 轴线 进
行 多 项 式 拟 合 ,从 而 得 到 拟 合 曲线 C 的 参数 方程 :
x(t) =-0.207806 - 0.610303 ¢ +0. 206455 * - 0.0144935 下
+0.000517774 ¢* - 8.394241977754047 X10 -让
+6.133353112035975 X10 8 15- 1. 6673218267444805 X10- 101
y(t) =158.211+1.86595¢- 0.266798 £+0.0141407 人
- 0.000325412 * +3.043275597680807 X10 ° ¢° o 人 本
- 9.899171274615063 X10- ?1 = 蛋
z(t) =t 全 厂
并 将 拟 合 曲线 和 连接 折线 在 YXO7，7OZ， oaaaeoenjon 中 。
: 八 碎 :
- wE  f 人 YX N
| Ne
XOY 而 - J\ SN 028
图 3
®
4
6 ”模型 检验
我 们 对 所 得 到 的 中 轴线 的 拟 合 曙 线 作 误 凑 分 机 。 分 别 用 下 面 的 三 种 方法 讨论 。
方法 一 和 CUxz(O 7(D , 用 半径
为 R 的 球 球 心 沿 C 滚动 包 络 硬 成 管道 8”。 再 用 平面 Z= 1(1= 30,31……69) 去 截 9 得 到 的
40 张 截面 7” 与 题 读 申 的 对 应 截面 ”比较 ,我 们 称 4” no" 所 的 面积 与 0”Uo' 的 面
各 的 比 为 面 各 重合 :7 放 计 算 可 和 面积 重 合 刘 的 平均 人 为 96. 8024 % ,从 这 40 张 截 面 中
取出 5 张 2=30, 2=40, 2=50, Z=60, Z=69 与 对 应 的 截面 迭 加 ,其 重合 的 情况 如 图 4 所
示 。 (黑色 区 ider 题 设 中 的 对 应 截面 ,灰色 表示 截 9" 所 得 的 区 域 ) 。
二 重心 法 : 对 于 用 多 项 式 拟 合 得 到 的 空间 曲线 C” :Kx (0 ,7 , 坟 , 考 虑 C 与
OO
下 对 于 求 得 的 曲 级 C" 和 半径 R ,用 半径 为 R 的 球 沿 C" 滚 动 包 络 而 成 管道 9” 。 再 用
平面 虽 = ;去 截 8 得 到 40 张 截面 (= 30,31 ……69) ,用 截面 的 边界 点 go' 儿 求 出 每 张 图 的
“重心 给 标 ( 即 所 有 点 的 x 坐标 平均 , y” 坐标 求 平均 ) 。 把 此 “重心 "与 原 截 面 的 边界 ao 的
“重心 * 作 比较 ,计算 它们 之 间 的 距离 , 求 得 平均 偏 移 量 A' = 3. 35722pixel 。
方法 三 ”随机 投 点 检验 法 : 对 于 最 后 得 到 的 拟 合 曲线 C"” , 当 半径 为 R 的 球 沿 着 C "滚动
时 ,用 平面 Z= ;30 <i <69) 去 截 。 考 虑 此 球 通过 平面 Z= 的 过 程 。 设 在  <t 和 总 时 , 球
与 Z=1i 相交, 并 且 当 := 五 及 :=5 时 与 平面 Z=i 相 切 。 把 区 间 /m ,7240 等 分 , 则 第 * 个
分 点 t=s X(P -17240+ 站 ,对 每 个  BRTE 大 时 与 Z= 交 成 一 个 圆 ,由 此 可 以 得 到 240
4 994-200 a Academic Journal Electronic Publishing House. All rights reserved. http://www.cnkinet
模 大

<!-- source_page: 5 -->

ERi
起 让
建 模 专 各 血管 切片 的 三 维 重建
CS N) \
V 7
-从
xf / 所
条
7 <
|
MK- AN
/N
AN
O
4
L- / V 'S
图 4
个 加 .然后 在 这 240 个 国 的 请 妇 了 7200 个 点 ,每 加 周 所 到 的 点 的 数目 与 答 枚 谍
正比 ,然后 把 这 些 点 向 2 六 图 象 @(? 投 点 ,由 此 计算 出 这 些 点 沙 于 o(9 中 的 比例 30 <
1 <659) 。 经 计算 ,其 平均 比例 为 94 % 以 上 。
上 上 二 种 方法 靖 内 下 突 重 建 血 和 的 曲折 维和 和 的 大 的 妆 扫 比 较 - 政 人
可 以 说 明 丰 用 让 起 革 可 行 的 。
\5
7_PIBG—iti
了 术 多 型 实际 上 是 在 综合 考虑 了 编程 的 可 实现 性 和 运算 量 的 大 小 后 ,采用 改进 的 切线 法 来
人
会 更 汶 精 确 ,但 会 增加 运算 量 。
另外 ,我 们 还 可 以 用 收缩 或 扩大 管道 半径 的 方法 来 建立 模型 , 即 对 于 一 个 初始 给 定 的 半径
Ru ,对 每 一 个 截面 图 象 Z= ,判断 这 个 半径 为 Ro 的 圆 是 否 可 以 完全 含 于 截面 图 象 中 。 如 果
每 张 截面 图 象 均 能 完全 覆盖 此 圆 , 则 把 球 半径 Ro 增 大 1/2pixel ,否则 将 Ro 减 小 /2pixel 。 直
到 对 某 一 个 Ro , 当 Ro 增 大 1/2pixel 时 至 少 有 一 个 加 不 能 完全 含 于 所 有 的 截面 图 象 中 , 则 将 这
个 Rn 作为 管道 半径 。 用 这 各 方法 建 模 也 是 比较 合理 的 ,但 计算 量 较 大 ,留待 以 后 进行 具体 计
算 。
2 © 1994-2006 China Academic Jo Electronic Publishing House. All rights rese http e

<!-- source_page: 6 -->

回 叶 这
人
5
46 工程 数学 学 报 第 19 T
参考 文献 :
[1] 杨 钰 , 何 旭 洪 , 赵 吴 彤 等 编著 . Mathematica 应 用 指南 [M]. 人 民 邮 电 出 版 社 ,1999 年 10 月 第 一 版
[2] 苏 步 青 等 编著 . 实用 微分 几何 引 论 [LM] . 北京 :科学 出 版 社 ,1986 年 11 月 版
[3] 谭 浩 强 编著 . C 程序 设计 [M]. 北京 :清华 大 学 出 版 社 ,1991 年 7 月 版
[4] “ 姜 启 源 . 数学 模型 [M] . 高 等 教育 出 版 社 ,2001 年 1 月 版
[5] 白 其 峥 主编 . 数学 建 模 案例 分 析 [M].2001 年 1 月 版
[6] 雷 功 炎 编著 . 数学 模型 讲义 [M].1999 年 4 月 版
Re-construction of Vessel in Taree Dimension _
-从 >
LIDU Hardonz，CHEN Lu，JIANG Hao 全 W
The tutor: LU Qirhe 2XG
(Suzhou University , Suzhou 215006 , P. R，China) H
Abstract : The re - construction of vessel in three dimension will be discussed in this esay. st show the following proposition.
Proposition  Let C be a curve along which the center of a ball moves, oa 本 m the original vessel by the plane Z
=i,and Dof the boundary of of0 <i <99). Let C'” be the intersectionpoint of C with the plane Z=i(0 <i <99) , then
there are a line segment with two end points PP 人， P{”, (PP €dw¥ < <2) such that CT) is the middle point of
the line segment x
Pf P{¥ and two parallel tangent lines which touch 3” only at P{”, P{’respectively (0 <i <99)
On the basis of the proposition shown above , C'* (0 <i <09) and the diameter of the vessel D=59.1238 pixel have been found.
The equation of C is simulated by coordinate data of 100 interséétion points :
X(1) = - 0.207806 - 0 206455 1> £0. 0144935 *
+0.000517774* - 8.394241977754047 X10°¢1°
+6. 133353112035975 X10  p X10°10¢
Y(1) =158.211+ 14 ©0.266798 17 +0.0141407 于
- S Ty X10 -51
- 9.899171274615063 x10- 915
2(1) = ie 下
On the ground of that equation.ythe-simulated vessel in three dimension is figured out , and at the same time , the 40 sections sliced
from the simulated vessel 人 out ,matching the original vessel at the average rate as much as 96. 8024 %.
Key words : % polynomial fit
1do
四  1ntom ts ei seo Ars. mo 医 对
1994-2006 China Academic Journal Electronic Publishing All rights reserve http://ww ki.net

