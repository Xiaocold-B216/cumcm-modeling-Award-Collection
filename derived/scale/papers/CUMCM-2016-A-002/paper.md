# Extracted Paper

<!-- source_page: 1 -->

# 基于极值优化的系泊系统设计

## 摘要

本文研究的是利用力学及数学知识进行系泊系统设计分析及优化的综合问题。 第一问中，着重通过静力学理论分析系泊系统的受力，进而确定风速与钢桶和各节钢管的倾斜 角度、锚链形状、浮标的吃水深度和游动区域的关系。 建立平面汇交力系，根据系泊系统在海面平静、风速一定的情况下保持稳定的特点，利用静力 平衡和力矩平衡，分别对浮标、钢管、钢桶和重物球进行静力学分析，得到一系列静力平衡方程和 力矩平衡方程。对于锚链，由于质量均匀分布，我们将其视为悬链线结构。使用微积分方法求出锚 链垂向投影长度与锚链长的关系式。同时计算出使得全部锚链恰离开海床的临界风速。 为了求解上述多元非线性方程组，我们以系泊系统各部件垂向投影长度等于海水深度为目标， 选取浮标出水高度为自变量，在合理范围内采用循环遍历法，得到一组精度较高的解向量。同时， 采用悬链线理论计算锚链垂向投影长度，进而得出另一组解向量。得到相似的结果互为检验。 最终得出临界风速为 21.92m/s。当风速 12m/s 时，钢桶倾斜角度 2.2，钢管倾斜角度由上至下分 别为 1.163，1.175,1.18，1.186。锚链形状：有 6.2525m 长的锚链平躺在海床上，剩余部分为曲线（曲 线方程和图片见正文），浮标的吃水深度为 0.6816m，浮标游动区域为在海面上以锚为中心，半径为

14.676m 的圆；风速 24m/s 时，钢桶倾斜角度 4.584，钢管倾斜角度由上至下分别为 4.435，4.463,4.492，
4.521。锚链形状：锚链底端切线与海床夹角为 4.4，形状为曲线（曲线方程和图片见正文），浮标的 吃水深度为 0.6957m，浮标游动区域为在海面上以锚为中心，半径为 17.7918m 的圆。 第二问中，运用模型一的计算方法初步计算出风速为 36m/s 下系泊系统的各参数，之后求出满 足约束条件的重物球质量的最小值，并计算此种情况下系泊系统的各参数。 在问题一的假设下用模型一求解，得出风速 36m/s 时，钢桶倾斜角度 9.48，钢管倾斜角度由上 至下分别为 9.19，9.24,9.30，9.36。锚链形状：锚链在锚点与海床的夹角为 20.91，剩余部分为曲线 （曲线方程和图片见正文），浮标的吃水深度为 0.7185m，浮标游动区域为在海面上以锚为中心，半 径为 18.8718m 的圆。 以钢桶的倾斜角度不超过 5 度，锚链在锚点与海床的夹角不超过 16 度为约束条件，重物球的质 量为目标函数，运用模型一中的循环遍历法求出满足约束条件的重物球质量的最小值。 最终得出重物球的质量为 2225kg，此时钢桶倾斜角度 4.52，钢管倾斜角度由上至下分别为 4.43，
4.45,4.47，4.49。锚链形状：锚链在锚点与海床的夹角为 15.98，剩余部分为曲线，浮标的吃水深度 为 0.98m，浮标游动区域为在海面上以锚为中心，半径为 18.5437m 的圆。 第三问中，在模型一的力学分析中添加近海水流力，进而确定风速、近海水流速度、锚链型号 与长度、重物球质量与钢桶和各节钢管的倾斜角度、锚链形状、浮标的吃水深度和游动区域的关系。 首先确定优化指标：选定吃水深度、游动区域、钢桶倾斜角为优化指标，用层次分析法确定各 指标的权重系数，对三个指标作归一化处理，得到综合优化指标。优化目标为综合优化指标尽可能 小。对于 5 种不同的锚链型号，我们选择分别穷举比较，接着设计系泊系统设计目标：以极限海况 下系泊系统正常工作为约束条件，以在海况稳定状况下综合优化指标最小为目标函数，建立优化模 型，寻求最优解。求解时采用赋值降元方法将问题化归到求解第二问的方法，较好地简化了求解步 骤，最终得出设计方案。最后列举出在此方案下不同情况时桶和各节钢管的倾斜角度、锚链形状、 浮标的吃水深度和游动区域。 本模型建立中运用 Matlab7.0（图像绘制，方程求解，最优规划），从而使建模过程顺利进行， 使所建模型更加精简。
### 关键词：系泊系统设计 多元非线性方程组 循环遍历法 层次分析法 优化模型

<!-- source_page: 2 -->

# 一、问题重述

本题考察的是利用力学和数学分析手段合理设计系泊系统。

1.根据题给的锚、锚链、钢桶、重物球、钢管、浮标等的相对位置、尺寸、质量等数据和部分
约束条件，假设海水静止，分别确定海面风速为 12m/s 和 24m/s 时钢桶和各节钢管的倾斜角度、锚 链形状、浮标的吃水深度和游动区域。

2. 在问题 1 的假设下，计算海面风速为 36m/s 时钢桶和各节钢管的倾斜角度、锚链形状和浮标
的游动区域。并调节重物球的质量，使得钢桶的倾斜角度不超过 5 度，锚链在锚点与海床的夹角不 超过 16 度。

3.考虑风力、水流力和水深情况，进行系泊系统设计。求出水深介于 16m~20m 之间、海水速度
最大 1.5m/s、风速最大 36m/s 的情况下，钢桶、钢管的倾斜角度、锚链形状、浮标的吃水深度和游 动区域。

# 二、问题分析

本题是以系泊系统设计为背景的力学分析问题。 首先是建立系泊系统静力特性分析模型，为了简化求解过程，在假设条件和海面风速为 12m/s 和 24m/s 的情况下，首先考虑锚链，由于锚链每段相对较短，近似地将其视为整体，取锚链长度为 微元进行积分，得到锚链顶端至海床高度的表达式。然后，分别取钢管、浮标为研究对象设参量进 行力学分析，列出静力学平衡方程。最终得到 26 个有效方程（含 26 个变量），为静定问题，理论上 可解。但由于方程组复杂且非线性，首先对部分方程进行化简，再选取浮标出水高度为枚举变量， 以系泊系统各部分在水中高度之和等于水深为目标，采用遍历法，寻找符合条件的浮标出水高度， 并据此求解出钢桶和各节钢管的倾斜角度、锚链形状、浮标的吃水深度和游动区域。

接着，根据所给数据，计算出风速为 36m/s 时钢桶和各节钢管的倾斜角度、锚链形状、浮标的 吃水深度和游动区域，判断设备是否能够正常工作，若不能，以钢桶的倾斜角度不超过 5 度，锚链 在锚点与海床的夹角不超过 16 度为约束条件，重物球的质量为目标函数，运用模型一中的循环遍历 法求出满足约束条件的重物球质量的最小值。同时解出改变重物球的质量后钢桶和各节钢管的倾斜 角度、锚链形状、浮标的吃水深度和游动区域。

同时考虑近海水流力和风力使得问题由二维上升到三维，极大地增大了分析难度。首先考虑到 系泊系统要满足在极限海况（风速和水流速度最大且同向）能够正常工作这一必要条件。然后考虑 系泊系统的受力，由于水流与风的方向一般不同，系泊系统的形态会比较复杂。为了既保持设计的 可靠性同时又比较容易操作，我们只研究风与海流在同一方向的情况。根据系泊系统设计要求选取 优化指标，用层次分析法确定权重系数，建立综合优化指标。在海况为中值的情况下找到满足极限 海况下系泊系统正常工作约束条件的使得综合优化指标最小的方案，随后选取多组海水深度、风速、 锚链型号和长度、重物球质量，分别求出在此方案下桶和各节钢管的倾斜角度、锚链形状、浮标的 吃水深度和游动区域。

本题的求解过程中，紧密的联系了图形和数据，是当今许多先进技术的基本思路。与此同时， 求解的过程也是典型的抽象模型，数据检验，实际性优化三步走，是典型的利用数学原理解决问题 的案例。

<!-- source_page: 3 -->

# 三、模型假设

1.锚与海床的静摩擦系数足够大；
2.假设未脱地的锚链平躺在海床上；
3.系泊系统内各部件连接处接触良好；
4.风和水流的方向稳定且与海床平行；
5.风倾力矩作用下浮标产生的倾角忽略不计；
6.假设所分析海域处的重力加速度 g=9.8𝑚 ∙ 𝑠
−2 ；

7.重物球主要成分为铬钼铝钢，密度 7.65𝑔 ∙ 𝑐𝑐
−3 ；

8.锚链主要成分为高强度合金钢，密度 7.82 𝑔 ∙ 𝑐𝑐
−3 ；

9.假设题给传输节点示意图中表示的各物体均处于同一竖直平面；
10.不考虑锚链自身的弹性伸长及结构空隙，锚链自重沿锚链方向为常量。
# 四、符号说明

|符号表示|文字说明|
|---|---|
|𝑹 𝒇|浮标系统直径|
|𝐡 𝒇|浮标系统高度|
|h|浮标系统出水高度|
|𝒉 𝒄|浮标吃水深度|
|𝐦 𝒇|浮标质量|
|G|浮标重力|
|𝒍 𝒈|钢管长度|
|𝑹 𝒈|钢管直径|
|𝒎 𝒈|钢管质量|
|𝜽 𝟎|锚链末端切线方向与海床法线的夹角|
|𝒍 𝒕|钢桶长度|
|𝑹 𝒕|钢桶外径|
|𝒎 𝒕|设备和钢桶总质量|
|𝜽 𝒕|钢桶的倾斜角度|
|𝒔 (i=1,2,…,5) 𝒊|i 型电焊锚链长度|
|A|锚链横截面积|
|𝝆 𝒎|锚链密度|
|𝒎 𝒒|重物球质量|
|H|海水深|
|𝝆 𝒔|海水密度|

<!-- source_page: 4 -->

|v|风速|
|---|---|
|𝑭 风|风力|
|𝑭 𝟎|锚对锚链的拉力|
|𝑭 𝟏|钢管对浮标的拉力|
|𝑭 (i=1,2,3,4) 浮𝒊|钢管受到的浮力|
|𝑭 锚|锚链微元的张力|
|𝑭 水桶|钢桶受到的近海水流力|
|y|锚链悬垂长度的垂向投影分量|
|x|锚链悬垂长度的水平投影分量|
|P|锚链单位长度的质量|
|𝛉 (i=1,2,3,4) 𝒊|钢管 / 钢桶上端受力与竖直方向的夹角|
|𝛂 (i=1,2,3,4) 𝒊|钢管倾斜角度|
|s|锚链在海床上部的长度|
|R|浮标底部圆心与锚的水平最大距离|
|g|重力加速度|
|’ 𝐇|水深的模型计算值|
|∆𝐇|题设水深与模型结果的差值|
|realv|使锚链恰不被拖行的风速|
|𝑭 水|近海水流力|

# 五、模型建构

**5.1** 模型一 系泊系统静力特性分析模型
**5.1.1.**模型简介 在平衡状态下用隔离法对系泊系统的各部分进行静力学分析，用微元法计算锚链两端的张力， 同时分别隔离钢管、重物球、浮标进行受力分析。列出方程组，以其中一个方程成立条件为目标， 选取浮标出水深度为变量，采用遍历法求解。
**5.1.2.**模型建立
**5.1.2.1** 浮标的静力学分析： 浮标的结构是长为 2m，底面直径为 2m 的圆柱。在不考虑风浪的情况下浮标受到重力、浮力、 钢管的拉力（认为三力成平面汇交力系），方向均为竖直方向。在第一问中考虑风速，在前述基础上

<!-- source_page: 5 -->

添加 近海 风 荷 载 〈 下 简称 风力 )， 浮 标 受到 重力 、 浮 力 、 钢 管 的 拉力 、 风 力 四 个 力 。 在 静 力 平衡 状态
下 ， 四 力 构成 平面 汇 交 力 系 。 如 下 图 所 示 :
人 d
一 > 1 h
,T ~、 上 海面 |
L___-_ G
本 入
图 1 浮标 系统 受 力图
根据 平面 汇 交 力 系 的 相关 知识 所 ,将 各 力作 用 点 等 效 在 浮标 系统 的 重心 上 ， 以 浮标 系统 重心 为
原点 ， 如 下 图 建立 平面 直角 坐标 系 :
F.
F 风
海面 FA
G
sa/ .
0. .0' 分 别 是 重力 、 浮 为 的 作用 点
图 2 受 力 及 受 力 点 示意 图 图 3 受 力 示意 图
在 x 轴 和 y 轴 方 向 上 分 别 列 出 静 力 学 平衡 方程 :
> 到 =0: Fy —Fsing; =0
> =0: Fy—G-Fcosf; =0
又 :
FF 风 =0.6250% x Reh
Fy = pgn(h; 一 门
得 出
0.625v2 x Rh 六 = Fy sin 6; @
pgr(Rr — h) = Gy; + F, cos6; (2)
实际 情况 中 风 对 浮标 的 作用 效果 还 包括 使 其 倾斜 ， 即 存在 风 倾 力矩 下 的 倾斜 角度 。 由 力矩 的 基
本 定义 可 得 :
M = Fo x ho
其 中 ，Fo 为 迎风 面 所 受 风 力 ，ho 为 迎风 面 中 心 到 水 面 的 竖 直 距离 。 令 动 风 倾 角 为 p， 可 得 风 倾 力 失
5

<!-- source_page: 6 -->

所 做 的 功 :
W = 六 d
| Mdo
0 中 中 max = 57.3°
图 4 动 稳 性 曲线
浮标 在 水 中 的 排水 量 、 重 心 高 度 、 浮 心 移动 距离 等 因素 影响 的 复原 力矩 和 风 倾 角 有 关 。 如 图 所 示 的
动 稳 性 曲线 中 ， 每 一 点 切线 的 斜率 即 风 倾 力矩 。e 取 最 大 值 57.3" 时 ， 数 值 上 M = W。 令 了 为 结构 重
量 ，GM 为 初 稳 性 高 ， 得 到 风 倾 角 6 的 表达 式 :
6 = NLL 57.3°
由 于 风速 、 吃 水 深度 等 条 件 在 一 定 范围 内 时 风 倾 力矩 产生 的 倾角 很 小 ， 浮 标的 抗 风能 力 满足 要 求 ，
风 倾 角 对 浮标 轴线 朝向 的 影响 可 不 考虑 。
5.1.2.2 钢管 的 静 力 学 分 析 :
钢管 部 分 由 四 节 完 全 一 样 的， 长 为 Im， 直径 为 50mm， 质 量 为 10kg 的 圆柱 组 成 。 在 不 考虑 水 中
阻力 等 影响 因素 的 情况 下 ， 每 一 节 钢管 均 收 到 浮力 、 重 力 志 以 及 相 邻 钢管 或 相 邻 浮标 、 锚 链 在 其 几
何 形状 两 端 中 心 施加 的 拉力 。 四 力 在 竖 直 平面 内 成 汇 交 力 系 ， 钢 管 处 于 静 力 平衡 状态 。 第 了 工 节 钢 管
(7=1, 2, 3, 4) 的 受 力 情 况 如 下 图 所 示 :
Pi 个。 E
H
所
1 ya
I
Pu cy
图 5 单 节 钢管 受 力图
在 x 轴 、y 轴 两 个 方向 分 别 列 出 静 力 学 平衡 方程 :
SF =0: F;sinf; —Fi1sinf, =0 3)
了 已 = 0: Fiyycospyy —Frcos6; — Fig — G; =0 (7)
6

<!-- source_page: 7 -->

由 力矩 平衡 得 :
Fi x 3 x sin(ai — 6;) 一 局 ;1 X 3 xsin(gl -al =0 (1D
由 几何 关系 得 :
H; =lcosa; (15)
以 上 四 个 方程 代表 四 节 钢 管 的 四 种 不 同情 况 。
5.1.2.3 钢 桶 和 重 物 球 的 静 力 学 分 析 :
上 接 第 4 节 钢 管 、 内 含水 声 通讯 设备 的 钢 桶 ， 长 为 In、 外 径 为 30cm， 总 质量 为 100kg。 钢 桶 下
接 电焊 错 链 悬挂 重 物 球 ， 使 钢 桶 的 倾斜 角度 〈 钢 桶 与 坚 直线 的 夹 角 ) 尽 可 能 小 。
以 下 讨论 重 物 球 在 海水 中 受到 的 浮力 对 实际 情况 的 影响 。
Fig =pingV
G=mg
m=p-V
4
V =znR?
Wear bal, fi#fe:
/海水
Po = 一 一 .6
洱 p
对 于 重 物 球 材质 的 选择 ， 综 合 考虑 重 物 球 与 钢 桶 的 质量 关系 、 重 物 球 的 密度 及 其 在 海水 中 的 耐
压 耐 腐蚀 性 等 各 因素 。 我 们 首先 假定 为 金 “ 稳 定性 强 且 密度 较 大 ，p = 19.329 .cm 3 )， 代 入 数据 :
1.025
Fii1=To3y G ~00536
倍数 关系 较 大 。 结 合 实际 生产 生活 情况 ， 重 物 球 的 材质 应 为 10Criodl (p = 7.65g .cm -3)。 此 时 ，
R= | 垩 .3 0335m ~ 2.233R
= on'd ~ 0. m= 2. g
1.025
Fizy=5geG~0.134G
符合 要 求 ， 且 Fi ， < Ps 。 因 此 ， 重 物 球 所 受 浮力 不 可 忽略 。
根据 题 意 ， 钢 桶 的 小 角度 偏转 度数 xi 在 5 以 内 ， 受 力 分 析 图 中 不 易 体 现 ， 但 在 方程 分 析 中 不
能 忽略 。 因 此 ， 钢 桶 和 重 物 球 组 成 的 整体 的 静 力 平衡 状态 如 下 图 所 示 :
7

<!-- source_page: 8 -->

## 图 6 钢桶、重物球系统受力图

## 在 x 轴、y 轴两个方向分别列出静力学平衡方程：

∑ 𝐹𝑥= 0：𝐹₅ sin 𝜃₅ − 𝐹 锚 sin 𝜃 锚 = 0 (19)

∑ 𝐹𝑦= 0：𝐹₅ cos 𝜃₅ + 𝐹 浮桶 + 𝐹 浮球 − 𝐺 桶 − 𝐺 球 − 𝐹 锚 cos 𝜃 锚 = 0 (20)

以钢桶质心为参考点，由力矩平衡得：

<u>1 1</u> 𝐹₅ × × sin(𝛼 桶 − 𝜃₄)−𝐹 锚 × × sin 𝜃 锚 − 𝛼 桶 = 0 (21) 2 2

由几何关系得： 𝐻 桶 ＝ cos 𝛼 桶 (22)

**5.1.2.4** 锚链的静力学分析：
【2】 锚链各段长度不大，根据悬链线理论 ，可将锚链看作匀质的线性缆索。

## 取一小段锚链（ds），则可以将锚链悬垂长度的垂向投影分量的微元（dy）用 ds 表示，从锚链

## 底端至上端积分可以得到 y 与 s 的表达式。

## 图 7 锚链受力图 图 8 锚链微元分析图

<!-- source_page: 9 -->

设 ds 与 海 床 的 夹 角 为 p， 则 由 几何 关系 推 得
. Fy
sing = 一 -一
、\ F2yutF2y
进而 得 出
d ds - si d Fon
y = ds ' sin py = ds .一 -一
、\ Flup tF%p

其 中 ，F 节 直 表 示 锚 链 微 元 的 张力 沿 水 平方 向 上 的 分 力 ，F 永 平 表示 锚 链 微 元 的 张力 沿 竖 直方 向 上
的 分 力 。

对 锚 链 进行 静 力 学 分 析 ， 由 锚 链 与 锚 的 接口 处 右 推 ， 锚 链 微 元 的 张力 沿 水 平方 向 上 的 分 力 应 等
于 锚 对 锚 链 的 拉力 驯 ， 锚 链 微 元 受到 重力 和 海水 的 浮力 ， 所 以 错 链 微 元 的 张力 沿 紧 直 方向 上 的 分 力
应 等 于 其 受到 的 重力 与 浮力 的 合力 ， 即 有 :

F jop.=Fy sin 6, = Fy sin , (23)
Fgy =F g c0s 8,.= mgs — pgAs + Fy cos 6y (24)
对 dy 的 表达 式 积分 ， 有
s s s 由
y=|dy=| ds'sinyp = | ds 一 一
为 了 简化 计算 ， 令
a=mg — pgA
b = Fycosb,
c =Fysiné,
as+b
_c. 1 aretan—c—
cost。 C3)
|
Ta Ce ET
(25) 式 可 作为 计算 锚 链 形状 的 依据 。

不 妨 取 题 给 图 示 的 左 端 为 锚 链 末端 。 以 上 分 析 基 于 锚 链 全 长 都 悬 在 海水 中 《没有 任何 部 分 平 躺
在 海 床 上 ) 的 前 提 。 然 而 ， 风 速 小 于 临界 值 时 ， 锚 链 可 分 为 平 躺 在 海 床上 和 基 在 海水 中 两 部 分 ， 前
者 切线 方向 与 海 床 法 线 夹 角 为 60〈 如 下 图 所 示 )。6o 恰 不 为 90" 时 ， 锚 链 不 再 被 拖 行 ， 悬 在 海水 中 的
锚 链 长 度 及 为 错 链 实际 总 长 度 。

9

<!-- source_page: 10 -->

人
关头
平 船 在 海 床 上 悬 在 海水 中 |
图 9 错 链 部 分 拖 地 示意 图
5.1.2.5 各 组 成 部 分 的 关联 性 分 析 ;
海平 面 泽 标
上
| WE 2 f
1
g
| - 钢 桶 。 下 -Le 人 an
|
锚 链 重 物 球
1 了 锁链
| H 海 床
图 10 系统 结构 示意 图
总 长 度 三 浮标 吃水 深度 十 钢管 紧 直 方向 总 长 度 十 钢 桶 竖 直 方向 长 度 十 锚 链 竖 直 方向 总 长 度
即 :
4
2-h + >》 所 +Hy FYy =18 (26)
i=1
5.1.3 模型 求解
初步 判断 临界 风速 realv 取 值 在 10-30m ' s-!+ 范 围 内 。 由 于 9o 和 s 均 为 已 知 量 , 联 立 上 述 (1)~(26)
号 方程 并 缩小 待 求 两 范围 ， 得 到 realv = 21.9200m - s-1 。 以 系 泊 系 统 各 部 件 垂 向 投影 长 度 y 等 于 海
水 深度 为 目标 , 以 浮标 系统 出 水 高 度 h 为 自 变量 , 控制 自 变 量 在 0~2 之 间 。 调 节 自 变量 , 用 MATLAB
软件 ， 使 用 循环 遍历 方法 找到 系 泊 系 统 各 部 件 垂 向 投影 长 度 最 接近 海水 深度 18m 的 解 ， 分 别 讨论 风
速 为 12ms《〈 锚 链 拖 地 )、24m/s《〈 锚 链 不 拖 地 ) 的 情况 。 详 细 结果 如 下 表 所 示 :
EEC
w[|we EEC
al
EEC
10

<!-- source_page: 11 -->

角
a;(=12
E
名 初始 状态 ， 锚 链 与 海 床 夹 角 4.561°;
人 @@ 参 数 方程 表达 式 ，
(©6.253m 长 的 部 分 平 躺 在 海 床 上 ;
@@ 剩 余部 分 的 参数 方程 表达 式 : y = 15.7338 (/(0.0636s + 00798)" + 1
错 链 形状 y = 3.9763(V0.2515s2+1-1) -10032)
x = 3.9763In(,/(0.25155)2 + 1 x =15.7338 [in (V(0.06365 +00798) + 1
+0.2515s) + 0.0636s 十 0.0798)
一 0.4703|
LT  ILL SVNS
表 1 12?7n/s、24?7n/s 风 速 下 系统 部 分 结构 状态
图 1 风速 12m/s 时 锚 链 形状 示意 图 图 12 风速 247/s 时 锚 链 形状 示意 图
5.1.4 模型 检验
在 第 一 问 中 ， 锚 链 实 际 上 由 210 段 链条 连接 而 成 ， 在 模型 的 建立 中 我 们 将 错 链 视 为 悬 链 线 ， 并
采用 微 积分 方法 进行 求解 。
悬 链 线 方程 ;
实际 上 ， 灵 链 线 方程 也 可 以 较 好 地 解决 类 似 的 问题 。 锚 链 垂 向 投影 长 度 y 与 锚 链 水 平 投影 长 度 x
满足 悬 链 线 方程 9:
y = a(cosh @) -1
其 中
11

<!-- source_page: 12 -->

<u>𝑇₀</u> 𝑎 = 𝑃 𝑇₀表示锚链顶端张力的水平分量，由于锚链水平方向受力平衡故可用𝐹₀表示𝑇₀，因𝜃₀较小，此 处近似认为𝑇₀等于𝐹₀。 风速为 12m/s 时锚链有一部分在海床上，风速为 24m/s 时锚链全部浮起，故以风速为 24m/s 时 的数据为基础进行比较。𝑇₀的值等于 941.87N，P 的值等于 68.6N/m。 模型检验： 在同一坐标系中画出模型一和悬链线方程所表示的 y 与 x 的图像：

图 **13** 模型检验图 可以看出，两曲线（下方曲线为模型一算式所得的锚链形状曲线）形状较为接近，y 值分别为

12.3012m（模型一）和 12.5824m（悬链线方程）相差不大，经计算，用悬链线方程方法算得的系泊 系统各参数值与模型一算得的各参数值相差不大。从侧面验证了模型一的合理性和准确性。
**5.2** 模型二 重物球质量优化模型
**5.2.1** 模型一的再应用 采用模型一的计算方法，不考虑钢桶的倾斜角度不超过 5 度、锚链在锚点处与海床的夹角不超 过 16 度这两个约束条件的情况下求解，得出：
风速 36m/s

|钢桶倾斜角𝛼|桶|9.482°|
|---|---|---|
||𝛼₁|9.190°|
|各节钢管倾斜|𝛼₂|9.242°|
|(i =1,2,3,4) 角𝛼 𝑖|𝛼₃ 𝛼₄|9.299° 9.356°|

<!-- source_page: 13 -->

加 D 锚 链 在 锚 点 与 海 床 的 夹 角 为 20.867";
@@ 剩 余部 分 的 参数 方程 表达 式 :
错 链 形状 y = 34.7849(,/(0.0287s + 0.3811)2 + 1 — 1.0702)
x = 34.7849(In(y/(0.0287s + 0.3811)% + 1 + 0.0287s
+0.3811) — 0.6303))
一
表 2 36m/s 风 速 下 系统 部 分 结构 状态
图 14 风速 36mx/s 时 锚 链 形状 示意 图

由 上 土 表 结果 可 知 ,风速 为 36m/s 时 钢 桶 倾斜 角 和 锚 链 在 锚 点 处 与 海 床 的 夹 角 都 超过 了 最 大 限 值 ，
可 见 在 模型 一 的 假设 下 系 泊 系 统 不 能 正常 工作 ， 所 以 需要 通过 调节 系 泊 系 统 的 部 件 对 系 泊 系统 进行
重新 设计 。 根 据 题 意 ， 问 题 二 中 考虑 通过 调节 重 物 球 的 质量 来 达到 系 泊 系统 设计 要 求 。 下 文 给 出 重
物 球 质 量 优化 模型 的 具体 内 容 。
5.2.2 模型 简介

在 模型 一 的 基础 上 对 模型 进行 加 强 ， 以 钢 桶 的 倾斜 角度 不 超过 5 度 、 锚 链 在 锚 点 处 与 海 床 的 来
角 不 超过 16 度 为 约束 条 件 ， 重 物 球 的 质量 为 目标 函数 ， 运 用 模型 一 中 的 循环 遍历 法 求 出 满足 约束 条
件 的 重 物 球 质量 的 最 小 值 。
5.2.3 模型 求解

在 模型 一 的 基础 上 同样 地 对 各 系统 部 件 进行 受 力 分 析 ， 增 加 调节 重 物 球 质量 的 步 又， 逐步 增 大
重 物 球 质量 ， 直 到 满足 钢 桶 的 倾斜 角度 不 超过 5 度 ， 锚 链 在 锚 点 与 海 床 的 夹 角 不 超过 16 度 。 恰 好 满
足 这 两 个 条 件 的 重 物 球 质量 即 为 最 优 的 重 物 球 质量 。

求 得 重 物 球 的 质量 为 2225Skg。 对 应 的 系 泊 系 统 的 各 参数 值 如 下 :

此 时 钢 桶 倾斜 角度 4.52"， 钢 管 倾 斜 角度 由 上 至 下 分 别 为 4.43"，4.45",4.47"，4.49"。 锚 链 形状 :
锚 链 在 锚 点 与 海 床 的 夹 角 为 15.98"， 剩 余部 分 为 曲线 ， 浮 标的 吃水 深度 为 0.98m,， 浮标 游 动 区 域 为 在

13

<!-- source_page: 14 -->

海面 上 以 锚 为 中 心 ， 半 径 为 18.5437m 的 圆 。
锚 链 高 于 海 床 部 分 的 参数 方程 表达 式 :
y =27.5782(V(0.0363s + 0.2863)2 + 1 — 1.04)
x=275782x (ln ({/(0.0363s+0.2863)? + 1+ 0.0363s + 0.2863) — 0.2825))
由 上 表 结 果 可 知 ， 重 物 球 为 2225kg 时 系 泊 系 统 达 到 了 钢 桶 的 倾斜 角度 不 超过 $ 度 、 锚 链 在 锚 点
处 与 海 床 的 夹 角 不 超过 16 度 这 两 个 约束 条 件 。2225ksg 为 比较 合理 的 重 物 球 质量 。
5.2.4 模型 评价
模型 二 在 模型 一 的 基础 上 减少 了 重 物 球 质 量 这 一 已 知 条 件 ， 模 型 的 功能 获得 了 优化 ， 但 重 物 球
质量 的 改变 会 影响 锚 链 脱 地 的 临界 风速 。 所 以 模型 二 在 使 用 前 需要 先 计 算 临 界 风速 这 一 点 需要 注意 。
5.3 模型 三 基于 极 值 优化 的 系 泊 系 统 设计 模型
5.3.1 模型 简介
在 模型 一 、 二 的 基础 上 增加 近海 水 流 力 ， 在 二 维 坐标 中 用 静 力 平衡 和 力矩 平衡 对 模型 一 的 方程
组 进行 补充 。 根 据 系 泊 系 统 设 计 要 求 选取 优化 指标 ， 用 层次 分 析 法 确定 权重 系数 ， 建立 综合 优化 指
标 。 在 海 况 为 中 值 的 情况 下 找到 满足 极限 海 况 下 系 泊 系 统 正常 工作 约束 条 件 的 使 得 综合 优化 指标 最
小 的 方案 ， 选 取 多 组 海水 深度 、 风 速 、 锚 链 型 号 和 长 度 、 重 物 球 质 量 寺 分 别 求 出 在 此 方案 下 桶 和 各
节 钢 管 的 倾斜 角度 、 锚 链 形状 、 浮 标的 吃水 深度 和 游 动 区 域 。
5.3.2 模型 建立
5.3.2.1 综合 优化 指标 的 建立
根据 系 泊 系 统 设 计 使 得 浮标 的 吃水 深度 和 游 动 区 域 及 钢 桶 的 倾斜 角度 尽 可 能 小 的 要 求 ， 初 步 确
定 浮标 吃水 深度 、 游 动 区 域 、 钢 桶 的 倾斜 角度 为 系 泊 系 统 设计 优化 指标 。 如 果 单独 考虑 某 一 个 指标
可 能 可 以 不 断 优 化 ， 但 这 三 项 指标 的 值 相互 存在 关联 ， 如 减 小 钢 桶 的 倾斜 角度 可 能 要 以 增加 浮标 的
吃水 深度 为 代价 ， 因 此 考虑 将 三 个 优化 指标 综合 考虑 。
浮标 能 够 正常 采集 数据 需要 吃水 深度 尽量 小 且 浮标 不 能 沉没 ， 游 动 区 域 则 反映 了 浮标 的 稳定 程
度 ， 钢 桶 倾斜 角 小 于 “也 是 系 泊 系统 正常 工作 的 条 件 。 接 下 来 ， 采 用 层次 分 析 法 汪 ， 根 据 前 两 问 的
计算 及 题目 要 求 ， 我 们 确定 了 钢 桶 的 倾斜 角度 、 浮 标 吃水 深度 、 游 动 区 域 三 个 指标 的 判别 矩阵 A。
工 1
- 1 = -一
5 3
A= | 35 1 3 |
3 = 1
3
采用 规范 列 平均 法 〈 和 法 ) 求 出 各 指标 的 权重 系数 ， 步 又 如 下 :
14

<!-- source_page: 15 -->

矩阵 A 每 一 列 归 一 化 得 到 矩阵 B;
将 矩阵 B 每 一 行 元 素 的 平均 值得 到 一 个 一 列 n 行 的 矩阵 C;
和 矩阵 C 即 为 所 求 权重 向 量 。
求 得 浮标 吃水 深度 、 游 动 区 域 、 钢 桶 的 倾斜 角度 的 权重 系数 分 别 为 0.63，0.26，0.11。
对 浮标 吃水 深度 、 游 动 区 域 、 钢 桶 的 倾斜 角度 三 个 优化 指标 作 归 一 化 处 理 ， 将 处 理 过 的 浮标 吃
水 深度 记 作 心 ， 浮 标 游 动 区 域 记 作 Rs， 钢 桶 倾斜 角度 记 作 6.， 综 合 优化 指标 记 作 y 。
则 :
f=0.63x hs +0.26 X Rg + 0.11 x 6
53.2.2 系 泊 系统 的 静 力 学 分 析
在 考虑 近海 水 流 的 情况 下 ， 重 新 对 浮标 、 钢 管 、 钢 彬 、 锚 链 作 静 力学 分 析 ， 用 平面 汇 交 原理 和
力 抢 平衡 原理 列 出 方程 ， 得 到 方程 组 。 系 泊 系 统 各 部 分 受 力 分 析 图 与 模型 一 分 析 类 似 此 处 省 略 ， 只
给 出 计算 公式 :
浮标 的 静 力 学 分 析 :
在 x 轴 和 y 轴 方 向 上 分 别 列 出 静 力 学 平衡 方程
DE =0: Fy+F,—Fsing =0
> =0: Fy—G—Fcosf; =0
又 :
Fy, = 0.62572 x Rch
Fyy = pgn(hy — h)
Fy =374v2 X Rp x (2 — h)
得 出
0.62502 X Rph + 374v2 X Ry X (2 — h) = Fy sin6, @)
pgr(Rr —h) = Gy; + F cos 6; (2)
钢管 的 静 力 学 分 析 :
在 x 轴 、y 轴 两 个 方向 分 别 列 出 静 力 学 平衡 方程 ;
了 到 =0: Fising;—Fyysinbyyy 一 Phi=0 (3)~(6)
YF, =0: Fiyy c058;1 — Fcos8;— Fipy — G;=0 (7)~(10)
Pii = 374% H; x 0.0502
由 力 抢 平衡 得 :
F; x x sin(ai — 8;) — Fipq X xsin(f, —a)=0  (11)
由 几何 关系 得 :
H; =lcosa; (15)
15

<!-- source_page: 16 -->

以 上 方程 代表 四 节 钢 管 的 四 种 不 同情 况 。
钢 桶 和 重 物 球 的 静 力 学 分 析 :
在 x 轴 、y 轴 两 个 方向 分 别 列 出 静 力 学 平衡 方程 ;
了 肥 =0: Fysins —Fysinfy — Fy=0 19)
了 已 =0: Fy5c0885+ Figp + Fyazp — Gyg — Gyy — Fi cos8y =0 (20)
F ypy = 374 X Hy x 0.372
以 钢 桶 质心 为 参考 点 ， 由 力矩 平衡 得 :
1 1 ，
Fs x  X sin(ay; — 0) = Fyg X 5 x sin (B -ay) =0 (21)
由 几何 关系 得 :
Hy =cosay, (22)
锚 链 的 静 力学 分 析 :
对 锚 链 进行 静 力 学 分 析 ， 由 锚 链 与 锚 的 接口 处 右 推 ， 锚 链 微 元 的 张力 沿 水 平方 向 上 的 分 力 应 等
于 锚 对 锚 链 的 拉力 布 ， 锚 链 微 元 受到 重力 和 海水 的 浮力 ， 所 以 错 链 微 元 的 张力 沿 竖 直方 向 上 的 分 力
应 等 于 其 受到 的 重力 与 浮力 的 合力 ， 即 有 :
F joop =F y sin 8,= Fo sin 6, (23)
Fygy=Fy, cos 8,=mgs — pgAs + Fy cosg (24)
对 dy 的 表达 式 积分 ， 有
s s s Fuew
y=|dy=| ds-sing = | ds 一 一
全 从 外
为 了 简化 计算 ， 仿
a=mg— pgA
b = Fy cos 8,
¢ = Fysinf, — 374 x 0.02(H -> 所 一 (2 一 门 )z2
as+b
了 C - 1 WE
7 cosil wos 5)
二 1 _ i
Ta Ce ET
(25) 式 可 作为 计算 锚 链 形状 的 依据 。
各 组 成 部 分 的 关联 性 分 析 :
4
@2-h+ > Hi + Hyg 十》 和 外 一 18 (26)
i=1
5.3.2.3 极 值 优化 方法
以 风速 、 水 流速 度 、 锚 链 型 号 和 长 度 、 重 物 球 质 量 为 自 变量 ， 但 由 于 自 变量 较 多 且 方 程 组 较 复
16

<!-- source_page: 17 -->

杂 ， 我 们 采用 赋值 降 元 方法 在 风速 为 18m/s， 水 流速 度 为 0.75m/s， 海 水 深 为 18m 的 中 值 海 况 下 对 每
种 系 泊 系 统 进行 计算 ， 以 系 泊 系 统 在 极限 海 况 下 〈 风 速 和 海流 方向 相同 且 达 到 最 大 ， 水 深 为 16m 和
20m 共 两 种 情况 ) 能 够 正常 工作 为 约束 条 件 ， 以 综合 优化 指标 /最 小 为 目标 ， 寻 找 满足 上 述 条 件 的
锚 链 型 号 和 长 度 、 重 物 球 质量 。
5.2.3.4 模型 求解
在 满足 极限 海 况 可 以 正常 工作 的 情况 下 ， 对 每 种 错 链 解 出 一 组 使 得 综合 优化 指标 最 小 的 解 :
ER
一
一 Ta
一
一 am E. ILL
va
表 3 五 种 锚 链 型 号 下 的 最 优 解
得 出 型 号 V 的 锚 链 优化 指标 最 小 ， 效 果 最 优 ， 所 以 选取 这 种 设计 : 锚 链 长 度 20.52m， 型 号 为
V， 重 物 球 质 量 4200kg。 能 够 较 好 的 满足 要 求 。
5.2.3.5 系 泊 系 统 设计 结果 分 析
选取 三 种 海 况 进行 计算 ， 得 出 以 下 结果 :
1. 风 速 27m/s， 水 速 0.75Sm/s， 方 向 同 向 风水 深 20m。
此 时 钢 桶 倾斜 角度 1.5$"， 钢 管 倾斜 角度 由 上 至 下 分 别 为 1.449，1.46"，1.48"，1.50"。 浮 标的 吃
水 深度 为 1.6144m， 浮 标 游 动 区 域 为 在 海面 上 以 锚 为 中 心 ， 半 径 为 10.4201lm 的 圆 。
锚 链 高 于 海 床 部 分 的 参数 方程 表达 式 :
y = 4.7376(/0.044652 + 1 —1)
x = 4.7376 x (InV0.0446s2 + 1 + 0.2111s)
2. 风 速 24m/s， 水 速 Ims， 方 向 同 向 ， 水 深 16m。
此 时 钢 桶 倾斜 角度 2.27"， 钢 管 倾斜 角度 由 上 至 下 分 别 为 2.07"，2.11*，2.14"*，2.17*。 浮 标的 吃
水 深度 为 1.6144m， 浮 标 游 动 区 域 为 在 海面 上 以 锚 为 中 心 ， 半 径 为 12.7424m 的 圆 。
锚 链 高 于 海 床 部 分 的 参数 方程 表达 式 :
y = 6.9747(;/0.0206s% + 1 — 1)
x = 4.7376 X In(/0.0206sZ + 1 + 0.1434s)
3. 风 速 1Sm/s， 水 速 0.Sm/s， 方 向 同 向 ， 水 深 18m。
此 时 钢 桶 倾斜 角度 0.62*， 钢 管 倾 斜 角度 由 上 至 下 分 别 为 0.57"，0.58"，0.59"，0.60"。 浮 标的 吃
水 深度 为 1.6144m， 浮 标 游 动 区 域 为 在 海面 上 以 锚 为 中 心 ， 半 径 为 5.9076m 的 圆 。
锚 链 高 于 海 床 部 分 的 参数 方程 表达 式 :
y = 19065(V0.2751s2 + 1 — 1)
x =1.9065 X (In/0.2751s2 + 1 + 0.5245s)
由 于 篇 幅 有 限 ， 只 选取 一 种 情况 作出 锚 链 形状 图 。
17

<!-- source_page: 18 -->

图 **15** 第 **2** 种情况锚链形状示意图 三种情况下钢桶的倾斜角都较小，浮标游动区域也比较理想，吃水深度较大的原因可能是为了 满足极限海况下系泊系统能够正常工作使得重物球质量较大。

**5.2.3.6** 模型分析与优化 第三问的求解中我们是在系泊系统在极限海况下能够正常工作的前提下设计系泊系统，求出的 结果重物球质量与第一二问相比明显较大，锚链长度明显较长。这与适应极限海况的实际相符合。 当外界环境适中时，由于重物球较重和锚链长度较长，必然会有较长的一段锚链躺在海床上，这样 在一定程度上来看提高了锚链的稳定性。 本题我们主要是从系泊系统能够正常发挥功能考虑，设计的系泊系统可能存在用料较大，费用 较高的缺点。在实际应用中，可以综合考虑这方面的因素，对锚链和重物球的规格做一定的限制， 更好地满足实际应用需求。
# 六、模型评价：

**6.1** 模型一、二：
**6.1.1** 误差分析：
1.在海水静止的情况下，题给传输节点示意图所示的各结构模块也可能不位于同一竖直平面内，连 接处对系统高度和受力情况存在一定影响。
2.锚链自身和其与相邻锚链相连时都有空隙。
3.实际情况下，浮标的风倾角对系统产生的极微弱影响在分析对象不同时显著性可能有差别。
4.重物球和锚链的密度未知，我们根据资料查得的数据可能与实际情况有些偏差。
**6.1.2** 灵敏度分析： 根据模型中的（1）~（26）号方程，以浮标系统出水高度 h 为自变量，利用 MATLAB，使用循 环遍历方法找到系泊系统各部件垂向投影长度最接近海水深度 18m 的情况。将数据保留至小数点后

<!-- source_page: 19 -->

四位，求得 h=0.3184m，此时水深为 17.9940m，与题给条件相差 0.0060m。 改变系统出水高度检验模型灵敏度。取步长为 0.0001，除去求得的最优情况再计算相邻八组数 据，如下表所示：

|h(m)|1.3180|1.3181|1.3182|1.3183|1.3184|1.3185|1.3186|1.3187|1.3188|
|---|---|---|---|---|---|---|---|---|---|
|2- h(m)|0.6820|0.6819|0.6818|0.6817|0.6816|0.6815|0.6814|0.6813|0.6812|
|’ H (m)|18.2005|18.1489|18.0972|18.0456|17.9940|17.9424|17.8908|17.8392|17.7877|
|∆H(m)|0.2005|0.1489|0.0972|0.0456|0.0060|0.0576|0.1092|0.1608|0.2123|

表 **4** 出水高度灵敏度检验 可见在合理自变量范围内 h=0.3184m 为最优解，自变量每改变 0.0001 对待求结果的影响都很大， 模型灵敏度很高，从侧面验证了模型求解的精确性。

**6.2** 模型三：
**6.2.1** 误差分析：
1.在海水流动的情况下，浮标可能受到随时间变化的复杂的力，本模型视近海水流力和风力为恒力 可能会产生一定的误差。
2.海水阻尼可能对系泊系统的受力有一定的影响。
3.锚链自身和其与相邻锚链相连时都有空隙。
4.重物球和锚链的密度未知，我们根据资料查得的数据可能与实际情况有些偏差。
**6.2.2** 模型评价： 本模型建立了综合优化指标，并且在中值海况下寻求最优的设计方案，同时满足系泊系统在极 限海况下的正常工作，总体上是一个较好的设计方案。实际海况较为复杂且系泊系统受力也比较复 杂，作为一个简化模型它不能对复杂海况计算出对应的钢桶、钢管的倾斜角度、锚链形状、浮标的 吃水深度和游动区域，但作为一个设计模型满足了设计的需求，是一个符合设计功能的较为简易的 模型。
# 七、应用拓展

海洋资料浮标系统 此次系泊系统设计及优化综合问题的模型建立与解决有着重要的现实意义。 海洋资料浮标系统指以锚定在海上的观测浮标为主体，以数据采集处理、控制、传输系统为核 心处理环节，以自动化为工作特点，以卫星、调查船、声波探测设备为以海洋水文等为最终直接处 理对象的系统。2016 年初，《自然》杂志阐述的致力于全球气候变化研究的 Argo 计划以一定间距设 立浮标，有效监测并处理实时情况与测得的数据。这要求海洋资料浮标系统在多样化的环境条件下 都有强大的技术支持。但如今系统存在的问题主要包括规模及资料获取量欠佳、监测网点少、稳定

<!-- source_page: 20 -->

||性与可靠性略有不足等方面。||
|---|---|---|
||数的大小的确定，在设备稳定性方面利于海洋资料浮标系统长期可靠性运行。 八、参考文献 [1] 百度百科，平面汇交力系，[http://baike.baidu.com/view/604101.htm](http://baike.baidu.com/view/604101.htm) [3] 吴剑锋，王斌，基于悬链线法的锚链长度的计算，《中国水运月刊》 [4] 郑鹏飞，悬链线状的海洋浮标锚泊系统，《山东科学》|本文着眼全局，考虑海上、海下的多种环境条件下系泊系统各部分的组成、连接方式以及各参 ，2016.9.10 。 [2] 曹宏宇，海洋柱形浮标阻力和运动特性研究，天津大学硕士学位论文，2012.11。 139-139，2013.1。 1-9，1990.02。|
|[5]|%E6%9E%90%E6%B3%95/1672，2016.9.11。|百度百科，层次分析法，[http://baike.baidu.com/item/%E5%B1%82%E6%AC%A1%E5%88%86|](http://baike.baidu.com/item/%E5%B1%82%E6%AC%A1%E5%88%86|)
|||20|

<!-- source_page: 21 -->

# 附录：

以下附件均为 matlab 软件代码。 附件 1 问题一风速 12m/s 时各参数算法 matlab 代码 p=1025; v=12; g=9.8; Mbuoy=1000; Mtube=10; Mdrum=100; Mball=1200; Ltube=1; Dtube=0.05; Ldrum=1; Ddrum=0.3; s=22.05; m=7; Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; Gball=Mball*g; Ffball=Gball/7.46;%7.65/1.025=7.46 realh=100; judge=100;

% h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi)); % realh=0; % theta0=pi/2; % Fwind=2*0.625*h*v*v; % F0=Fwind/sin(theta0); % a=0.87*m*g; % b=F0*cos(theta0); % c=F0*sin(theta0); % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

for h=1:0.0001:1.5 Fwind=2*0.625*h*v*v; Ff=p*g*pi*(2-h); theta1=atan(Fwind/(Ff-Gbuoy)); F1=Fwind/sin(theta1); theta2=atan((F1*sin(theta1))/(F1*cos(theta1)-temp)); F2=F1*sin(theta1)/sin(theta2); theta3=atan((F2*sin(theta2))/(F2*cos(theta2)-temp)); F3=F2*sin(theta2)/sin(theta3); theta4=atan((F3*sin(theta3))/(F3*cos(theta3)-temp)); F4=F3*sin(theta3)/sin(theta4); theta5=atan((F4*sin(theta4))/(F4*cos(theta4)-temp)); F5=F4*sin(theta4)/sin(theta5); thetachain=atan((F5*sin(theta5))/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=F5*sin(theta5)/sin(thetachain); % theta0=atan((Fchain*sin(thetachain))/(Fchain*cos(thetachain)-0.87*m*g*s));%7.81/1.025=7.62 1-1/7.62=0.87 theta0=pi/2; F0=Fchain*sin(thetachain)/sin(theta0);

<!-- source_page: 22 -->

s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; if(judge>abs(18-Hriver)) realh=h; judge=abs(18-Hriver); end end h=realh; Fwind=2*0.625*h*v*v; Ff=p*g*pi*(2-h); theta1=atan(Fwind/(Ff-Gbuoy)); F1=Fwind/sin(theta1); theta2=atan((F1*sin(theta1))/(F1*cos(theta1)-temp)); F2=F1*sin(theta1)/sin(theta2); theta3=atan((F2*sin(theta2))/(F2*cos(theta2)-temp)); F3=F2*sin(theta2)/sin(theta3); theta4=atan((F3*sin(theta3))/(F3*cos(theta3)-temp)); F4=F3*sin(theta3)/sin(theta4); theta5=atan((F4*sin(theta4))/(F4*cos(theta4)-temp)); F5=F4*sin(theta4)/sin(theta5); thetachain=atan((F5*sin(theta5))/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=F5*sin(theta5)/sin(thetachain); % theta0=atan((Fchain*sin(thetachain))/(Fchain*cos(thetachain)-0.87*m*g*s));%7.81/1.025=7.62 1-1/7.62=0.87 theta0=pi/2; F0=Fchain*sin(thetachain)/sin(theta0); s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

coe1=c/a; coe2=b/c; coe3=a/c; y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

<!-- source_page: 23 -->

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+22.05-s+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha);

附件 2 问题一中求解临界风速代码 p=1025; g=9.8; Mbuoy=1000; Mtube=10; Mdrum=100; Mball=1200; Ltube=1; Dtube=0.05; Ldrum=1; Ddrum=0.3; s=22.05; m=7; Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; Gball=Mball*g; Ffball=Gball/7.46;%7.65/1.025=7.46 judge=100; realv=0;

for v=10:0.1:30 h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi)); theta0=pi/2; Fwind=2*0.625*h*v*v; F0=Fwind/sin(theta0); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); if(judge>abs(18-(2-h)-5-y)) judge=abs(18-(2-h)-5-y); realv=v; end end

<!-- source_page: 24 -->

附件 3 问题一、二风速 24m/s 和 36m/s 时各参数算法 matlab 代码（36m/s 时只需将第二行的 v 改为 36） p=1025; v=24; g=9.8; Mbuoy=1000; Mtube=10; Mdrum=100; Mball=1200; Ltube=1; Dtube=0.05; Ldrum=1; Ddrum=0.3; s=22.05; m=7; Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; Gball=Mball*g; Ffball=Gball/7.46;%7.65/1.025=7.46 realh=100; judge=100;

% h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi)); % realh=0; % theta0=pi/2; % Fwind=2*0.625*h*v*v; % F0=Fwind/sin(theta0); % a=0.87*m*g; % b=F0*cos(theta0); % c=F0*sin(theta0); % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

for h=1:0.0001:1.5 Fwind=2*0.625*h*v*v; Ff=p*g*pi*(2-h); theta1=atan(Fwind/(Ff-Gbuoy)); F1=Fwind/sin(theta1); theta2=atan((F1*sin(theta1))/(F1*cos(theta1)-temp)); F2=F1*sin(theta1)/sin(theta2); theta3=atan((F2*sin(theta2))/(F2*cos(theta2)-temp)); F3=F2*sin(theta2)/sin(theta3); theta4=atan((F3*sin(theta3))/(F3*cos(theta3)-temp)); F4=F3*sin(theta3)/sin(theta4); theta5=atan((F4*sin(theta4))/(F4*cos(theta4)-temp)); F5=F4*sin(theta4)/sin(theta5); thetachain=atan((F5*sin(theta5))/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=F5*sin(theta5)/sin(thetachain); theta0=atan((Fchain*sin(thetachain))/(Fchain*cos(thetachain)-0.87*m*g*s));%7.81/1.025=7.62 1-1/7.62=0.87 F0=Fwind/sin(theta0); % theta0=pi/2; % F0=Fchain*sin(thetachain)/sin(theta0);

<!-- source_page: 25 -->

% s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; if(judge>abs(18-Hriver)) realh=h; judge=abs(18-Hriver); end end h=realh; Fwind=2*0.625*h*v*v; Ff=p*g*pi*(2-h); theta1=atan(Fwind/(Ff-Gbuoy)); F1=Fwind/sin(theta1); theta2=atan((F1*sin(theta1))/(F1*cos(theta1)-temp)); F2=F1*sin(theta1)/sin(theta2); theta3=atan((F2*sin(theta2))/(F2*cos(theta2)-temp)); F3=F2*sin(theta2)/sin(theta3); theta4=atan((F3*sin(theta3))/(F3*cos(theta3)-temp)); F4=F3*sin(theta3)/sin(theta4); theta5=atan((F4*sin(theta4))/(F4*cos(theta4)-temp)); F5=F4*sin(theta4)/sin(theta5); thetachain=atan((F5*sin(theta5))/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=F5*sin(theta5)/sin(thetachain); theta0=atan((Fchain*sin(thetachain))/(Fchain*cos(thetachain)-0.87*m*g*s));%7.81/1.025=7.62 1-1/7.62=0.87 F0=Fwind/sin(theta0); % theta0=pi/2; % F0=Fchain*sin(thetachain)/sin(theta0); % s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); coe1=c/a; coe2=b/c; coe3=a/c; y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

<!-- source_page: 26 -->

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+22.05-s+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha);

附件 4 问题二风速 36m/s 调节重物球质量后的代码 p=1025; v=36; g=9.8; Mbuoy=1000; Mtube=10; Mdrum=100; Ltube=1; Dtube=0.05; Ldrum=1; Ddrum=0.3; s=22.05; m=7; Mball=2225 Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; Gball=Mball*g; Ffball=Gball/7.46;%7.65/1.025=7.46 realh=100; judge=100; t=3000; % h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi)); % realh=0; % theta0=pi/2; % Fwind=2*0.625*h*v*v; % F0=Fwind/sin(theta0); % a=0.87*m*g; % b=F0*cos(theta0); % c=F0*sin(theta0); % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

for h=1:0.0001:1.5 Fwind=2*0.625*h*v*v; Ff=p*g*pi*(2-h); theta1=atan(Fwind/(Ff-Gbuoy));

<!-- source_page: 27 -->

F1=Fwind/sin(theta1); theta2=atan((F1*sin(theta1))/(F1*cos(theta1)-temp)); F2=F1*sin(theta1)/sin(theta2); theta3=atan((F2*sin(theta2))/(F2*cos(theta2)-temp)); F3=F2*sin(theta2)/sin(theta3); theta4=atan((F3*sin(theta3))/(F3*cos(theta3)-temp)); F4=F3*sin(theta3)/sin(theta4); theta5=atan((F4*sin(theta4))/(F4*cos(theta4)-temp)); F5=F4*sin(theta4)/sin(theta5); thetachain=atan((F5*sin(theta5))/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=F5*sin(theta5)/sin(thetachain); theta0=atan((Fchain*sin(thetachain))/(Fchain*cos(thetachain)-0.87*m*g*s));%7.81/1.025=7.62 1-1/7.62=0.87 F0=Fwind/sin(theta0); % theta0=pi/2; % F0=Fchain*sin(thetachain)/sin(theta0); % s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; if(judge>abs(18-Hriver)) realh=h; judge=abs(18-Hriver); end end h=realh; Fwind=2*0.625*h*v*v; Ff=p*g*pi*(2-h); theta1=atan(Fwind/(Ff-Gbuoy)); F1=Fwind/sin(theta1); theta2=atan((F1*sin(theta1))/(F1*cos(theta1)-temp)); F2=F1*sin(theta1)/sin(theta2); theta3=atan((F2*sin(theta2))/(F2*cos(theta2)-temp)); F3=F2*sin(theta2)/sin(theta3); theta4=atan((F3*sin(theta3))/(F3*cos(theta3)-temp)); F4=F3*sin(theta3)/sin(theta4); theta5=atan((F4*sin(theta4))/(F4*cos(theta4)-temp)); F5=F4*sin(theta4)/sin(theta5); thetachain=atan((F5*sin(theta5))/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=F5*sin(theta5)/sin(thetachain);

<!-- source_page: 28 -->

theta0=atan((Fchain*sin(thetachain))/(Fchain*cos(thetachain)-0.87*m*g*s));%7.81/1.025=7.62 1-1/7.62=0.87 F0=Fwind/sin(theta0); % theta0=pi/2; % F0=Fchain*sin(thetachain)/sin(theta0); % s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0); % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); coe1=c/a; coe2=b/c; coe3=a/c; y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+22.05-s+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha);

附件 5 问题三极值优化代码 p=1025; Vwind=36; Vwater=1.5; g=9.8; Mbuoy=1000; Mtube=10; Mdrum=100; Ltube=1; Dtube=0.05; Ldrum=1; Ddrum=0.3; Dchain=0.02; Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; judge=100; %数据的初始化，缺少量为水深 H，锚链单位质量 m,锚链长度 s,重物球质量 Mball,吃水深度 2-h m=28.12; H=20; trueh=zeros(3000,0);

<!-- source_page: 29 -->

truetheta0=zeros(3000,0); truealpha=zeros(3000,0); trueMball=zeros(3000,0); trues=zeros(3000,0); trueR=zeros(3000,0); i=1; % s=25; % Mball=2300; for s=10.8:0.18:54 for Mball=1000:100:6000 for h=0:0.01:2 Gball=Mball*g; Ffball=Gball/7.46; Fwind=2*0.625*h*Vwind*Vwind; Fwater=374*2*(2-h)*Vwater*Vwater; Ff=p*g*pi*(2-h); theta1=atan((Fwind+Fwater)/(Ff-Gbuoy)); F1=(Fwind+Fwater)/sin(theta1); Fwtube=374*0.05*Vwater*Vwater; theta2=atan((F1*sin(theta1)+Fwtube)/(F1*cos(theta1)-temp)); F2=(F1*sin(theta1)+Fwtube)/sin(theta2); theta3=atan((F2*sin(theta2)+Fwtube)/(F2*cos(theta2)-temp)); F3=(F2*sin(theta2)+Fwtube)/sin(theta3); theta4=atan((F3*sin(theta3)+Fwtube)/(F3*cos(theta3)-temp)); F4=(F3*sin(theta3)+Fwtube)/sin(theta4); theta5=atan((F4*sin(theta4)+Fwtube)/(F4*cos(theta4)-temp)); F5=(F4*sin(theta4)+Fwtube)/sin(theta5); Fwdrum=374*0.3*Vwater*Vwater; thetachain=atan((F5*sin(theta5)+Fwdrum)/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=(F5*sin(theta5)+Fwdrum)/sin(thetachain); Fwchain=374*Dchain*(H-7+h)*Vwater*Vwater; theta0=atan((Fchain*sin(thetachain)+Fwchain)/(Fchain*cos(thetachain)-0.87*m*g*s)); F0=(Fchain*sin(thetachain)+Fwchain)/sin(theta0); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0)-374*Dchain*(H-5-(2-h))*Vwater*Vwater; y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c)));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; if(judge>abs(H-Hriver)) realh=h; judge=abs(H-Hriver); end

<!-- source_page: 30 -->

end judge=100; h=realh; Ffball=Gball/7.46; Fwind=2*0.625*h*Vwind*Vwind; Fwater=374*2*(2-h)*Vwater*Vwater; Ff=p*g*pi*(2-h); theta1=atan((Fwind+Fwater)/(Ff-Gbuoy)); F1=(Fwind+Fwater)/sin(theta1); Fwtube=374*0.05*Vwater*Vwater; theta2=atan((F1*sin(theta1)+Fwtube)/(F1*cos(theta1)-temp)); F2=(F1*sin(theta1)+Fwtube)/sin(theta2); theta3=atan((F2*sin(theta2)+Fwtube)/(F2*cos(theta2)-temp)); F3=(F2*sin(theta2)+Fwtube)/sin(theta3); theta4=atan((F3*sin(theta3)+Fwtube)/(F3*cos(theta3)-temp)); F4=(F3*sin(theta3)+Fwtube)/sin(theta4); theta5=atan((F4*sin(theta4)+Fwtube)/(F4*cos(theta4)-temp)); F5=(F4*sin(theta4)+Fwtube)/sin(theta5); Fwdrum=374*0.3*Vwater*Vwater; thetachain=atan((F5*sin(theta5)+Fwdrum)/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=(F5*sin(theta5)+Fwdrum)/sin(thetachain); Fwchain=374*0.02*(H-7+h)*Vwater*Vwater; theta0=atan((Fchain*sin(thetachain)+Fwchain)/(Fchain*cos(thetachain)-0.87*m*g*s)); F0=(Fchain*sin(thetachain)+Fwchain)/sin(theta0); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0)-374*0.02*(H-5-(2-h))*Vwater*Vwater; % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); coe1=c/a; coe2=b/c; coe3=a/c; y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha); % if((Alpha<pi)&&(theta0>0)) if((Alpha<(1/36)*pi)&&(theta0>(37/90)*pi)) trueh(i,1)=h; truetheta0(i,1)=theta0; truealpha(i,1)=Alpha; trueMball(i,1)=Mball; trues(i,1)=s;

<!-- source_page: 31 -->

trueR(i,1)=R; i=i+1; end end end

midscore=100; score=zeros(10000,1); Vwind=18; Vwater=0.75; H=18; for i=1:3000 if(trueh(i,1)==0) continue; end Mball=trueMball(i,1); s=trues(i,1); p=1025; g=9.8; Mbuoy=1000; Mdrum=100; Ltube=1; Dtube=0.05; Ldrum=1; Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; Gball=Mball*g; Ffball=Gball/7.46;%7.65/1.025=7.46 h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi));%判断锚链是否拖地 theta0=pi/2; Fwind=2*0.625*h*Vwind*Vwind; Fwater=374*2*(2-h)*Vwater*Vwater; F0=(Fwind+Fwater)/sin(theta0); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0)-374*Dchain*(H-5-(2-h))*Vwater*Vwater; y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); decide=0; if(H-(2-h)-5-y>0) decide=1; end%decide=0 拖地 decide=1 没拖地 if(decide==0) h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi)); Gball=Mball*g; Ffball=Gball/7.46; Fwind=2*0.625*h*Vwind*Vwind; Fwater=374*2*(2-h)*Vwater*Vwater; Ff=p*g*pi*(2-h); theta1=atan((Fwind+Fwater)/(Ff-Gbuoy)); F1=(Fwind+Fwater)/sin(theta1); Fwtube=374*0.05*Vwater*Vwater; theta2=atan((F1*sin(theta1)+Fwtube)/(F1*cos(theta1)-temp));

<!-- source_page: 32 -->

F2=(F1*sin(theta1)+Fwtube)/sin(theta2); theta3=atan((F2*sin(theta2)+Fwtube)/(F2*cos(theta2)-temp)); F3=(F2*sin(theta2)+Fwtube)/sin(theta3); theta4=atan((F3*sin(theta3)+Fwtube)/(F3*cos(theta3)-temp)); F4=(F3*sin(theta3)+Fwtube)/sin(theta4); theta5=atan((F4*sin(theta4)+Fwtube)/(F4*cos(theta4)-temp)); F5=(F4*sin(theta4)+Fwtube)/sin(theta5); Fwdrum=374*0.3*Vwater*Vwater; thetachain=atan((F5*sin(theta5)+Fwdrum)/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=(F5*sin(theta5)+Fwdrum)/sin(thetachain); Fwchain=374*Dchain*(H-7+h)*Vwater*Vwater; % theta0=atan((Fchain*sin(thetachain)+Fwchain)/(Fchain*cos(thetachain)-0.87*m*g*s)); theta0=pi/2; F0=(Fchain*sin(thetachain)+Fwchain)/sin(theta0); s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0)-374*Dchain*(H-5-(2-h))*Vwater*Vwater; % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); coe1=c/a; coe2=b/c; coe3=a/c; y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+trues(i,1)-s+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha); score(i,1)=0.63*0.5*(2-h)+0.26*0.05*R+0.11*Alpha*36/pi; if(midscore>score(i,1)) midscore=score(i,1); record=i; end end if(decide==1) h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*s)/(p*g*pi)); Gball=Mball*g; Ffball=Gball/7.46; Fwind=2*0.625*h*Vwind*Vwind; Fwater=374*2*(2-h)*Vwater*Vwater; Ff=p*g*pi*(2-h); theta1=atan((Fwind+Fwater)/(Ff-Gbuoy)); F1=(Fwind+Fwater)/sin(theta1);

<!-- source_page: 33 -->

Fwtube=374*0.05*Vwater*Vwater; theta2=atan((F1*sin(theta1)+Fwtube)/(F1*cos(theta1)-temp)); F2=(F1*sin(theta1)+Fwtube)/sin(theta2); theta3=atan((F2*sin(theta2)+Fwtube)/(F2*cos(theta2)-temp)); F3=(F2*sin(theta2)+Fwtube)/sin(theta3); theta4=atan((F3*sin(theta3)+Fwtube)/(F3*cos(theta3)-temp)); F4=(F3*sin(theta3)+Fwtube)/sin(theta4); theta5=atan((F4*sin(theta4)+Fwtube)/(F4*cos(theta4)-temp)); F5=(F4*sin(theta4)+Fwtube)/sin(theta5); Fwdrum=374*0.3*Vwater*Vwater; thetachain=atan((F5*sin(theta5)+Fwdrum)/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=(F5*sin(theta5)+Fwdrum)/sin(thetachain); Fwchain=374*Dchain*(H-7+h)*Vwater*Vwater; theta0=atan((Fchain*sin(thetachain)+Fwchain)/(Fchain*cos(thetachain)-0.87*m*g*s)); % theta0=pi/2; F0=(Fchain*sin(thetachain)+Fwchain)/sin(theta0); % s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0)-374*Dchain*(H-5-(2-h))*Vwater*Vwater; % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); coe1=c/a; coe2=b/c; coe3=a/c; y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+trues(i,1)-s+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha); score(i,1)=0.63*0.5*(2-h)+0.26*0.05*R+0.11*Alpha*36/pi; if(midscore>score(i,1)) midscore=score(i,1); record=i; end end end result=zeros(3,1); result(1,1)=trueMball(record,1); result(2,1)=trues(record,1); result(3,1)=score(record,1);

<!-- source_page: 34 -->

附件 6 问题三几种海况分析代码 p=1025; Vwind=15;%变量 Vwater=0.5;%变量 g=9.8; Mbuoy=1000; Mtube=10; Mdrum=100; Ltube=1; Dtube=0.05; Ldrum=1; Ddrum=0.3; Dchain=0.02; Gbuoy=Mbuoy*g; Gtube=Mtube*g; Fftube=p*g*Ltube*pi*0.25*Dtube*Dtube; temp=Gtube-Fftube; Ffdrum=p*g*Ldrum*0.25*pi*Ddrum*Ddrum; Gdrum=Mdrum*g; m=28.12; s=20.52; Mball=4200; Gball=Mball*g; Ffball=Gball/7.46; h=2-((Gbuoy+4*temp+Gdrum+Gball-Ffdrum-Ffball+0.87*m*g*s)/(p*g*pi)); H=18;%变量

Fwind=2*0.625*h*Vwind*Vwind; Fwater=374*2*(2-h)*Vwater*Vwater; Ff=p*g*pi*(2-h); theta1=atan((Fwind+Fwater)/(Ff-Gbuoy)); F1=(Fwind+Fwater)/sin(theta1); Fwtube=374*0.05*Vwater*Vwater; theta2=atan((F1*sin(theta1)+Fwtube)/(F1*cos(theta1)-temp)); F2=(F1*sin(theta1)+Fwtube)/sin(theta2); theta3=atan((F2*sin(theta2)+Fwtube)/(F2*cos(theta2)-temp)); F3=(F2*sin(theta2)+Fwtube)/sin(theta3); theta4=atan((F3*sin(theta3)+Fwtube)/(F3*cos(theta3)-temp)); F4=(F3*sin(theta3)+Fwtube)/sin(theta4); theta5=atan((F4*sin(theta4)+Fwtube)/(F4*cos(theta4)-temp)); F5=(F4*sin(theta4)+Fwtube)/sin(theta5); Fwdrum=374*0.3*Vwater*Vwater; thetachain=atan((F5*sin(theta5)+Fwdrum)/(F5*cos(theta5)+Ffdrum+Ffball-Gball-Gdrum)); Fchain=(F5*sin(theta5)+Fwdrum)/sin(thetachain); Fwchain=374*Dchain*(H-7+h)*Vwater*Vwater; % theta0=atan((Fchain*sin(thetachain)+Fwchain)/(Fchain*cos(thetachain)-0.87*m*g*s)); theta0=pi/2; F0=(Fchain*sin(thetachain)+Fwchain)/sin(theta0); s=(Fchain*cos(thetachain)-F0*cos(theta0))/(0.87*m*g); a=0.87*m*g; b=F0*cos(theta0); c=F0*sin(theta0)-374*Dchain*(H-5-(2-h))*Vwater*Vwater; % y=(c/a)*(1/cos(atan((a*s+b)/c))-1/cos(atan(b/c))); coe1=c/a; coe2=b/c; coe3=a/c;

<!-- source_page: 35 -->

coe4=log(sqrt(coe2.^2+1)+coe2); y=coe1*(sqrt((coe3*s+coe2).^2+1)-sqrt(coe2.^2+1)); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

alpha1=(F2*theta2+F1*theta1)/(F1+F2); alpha2=(F3*theta3+F2*theta2)/(F2+F3); alpha3=(F4*theta4+F3*theta3)/(F3+F4); alpha4=(F5*theta5+F4*theta4)/(F4+F5);

Alpha=acot((F5*cos(theta5)+Fchain*cos(thetachain)+Gball-Ffball)/(F5*sin(theta5)+Fchain*sin(thetachain )));

H1=cos(alpha1); H2=cos(alpha2); H3=cos(alpha3); H4=cos(alpha4); Hdrum=cos(Alpha); Hriver=2-h+H1+H2+H3+H4+Hdrum+y; R=x+sin(alpha1)+sin(alpha2)+sin(alpha3)+sin(alpha4)+sin(Alpha);

## 附件 7 图 11 作图代码

s=0:0.01:6.25 x=s; y=0; plot(x,y); hold on; s=6.26:0.01:22.05 x=3.9763*log(sqrt(0.2515*(s-6.26).^2+1)+0.2515*(s-6.26))+6.26; y=3.9763*(sqrt(0.2515*(s-6.26).^2+1)-1); plot(x,y); set(gca,'xtick',[0:2.5:15]); set(gca,'ytick',[0:2.5:15]); axis([0 ,15 ,0 ,15]);

附件 8 图 12 作图代码 s=0:0.01:22.05; x=15.7338*(log(sqrt((0.0636*s+0.0798).^2+1)+0.0636*s+0.0798)-0.0797); y=15.7338*(sqrt((0.0636*s+0.0798).^2+1)-1.0032); plot(x,y); set(gca,'xtick',[0:2.5:20]); set(gca,'ytick',[0:2.5:15]); axis([0 ,20 ,0 ,15]); x=coe1*(log(sqrt((coe3*s+coe2).^2+1)+coe3*s+coe2)-log(sqrt(coe2.^2+1)+coe2));

附件 9 图 14 作图代码 s=0:0.01:22.05; x=34.7849*(log(sqrt((0.0287*s+0.3811).^2+1)+0.0287*s+0.3811)-0.3724); y=34.7849*(sqrt((0.0287*s+0.3811).^2+1)-1.0702); plot(x,y); set(gca,'xtick',[0:2.5:20]); set(gca,'ytick',[0:2.5:15]); axis([0,20,0,15]);

<!-- source_page: 36 -->

附件 10 图 15 作图代码 s=0:0.01:20.52 x=6.9747*(log(sqrt(0.0206*s.^2+1)+0.1434*s)); y=6.9747*(sqrt(0.0206*s.^2+1)-1); plot(x,y); set(gca,'xtick',[0:2.5:15]); set(gca,'ytick',[0:2.5:13]); axis([0 ,15 ,0 ,13]);
