# Extracted Paper

<!-- source_page: 1 -->

第 30 卷第 1 期
数学的实践与认识
V o l130 N o 11
2000 年 1 月
J an. 2000
M A TH EM A T ICS IN PRA CT ICE AND TH EO R Y

法需要的仅仅是求关于三个变量的 n 2 个不等式是否有解, 可以用穷举的办法来解决, 不需
要用优化方法来解题.
参考文献:
周承高, 廖

[2]

张培强. 《M A TLAB 语言》
. 中国科技大学出版社, 1995. 11.

园.《优化方法及应用程序设计》
. 中国铁道出版社, 1989.

[3]

刘来福, 曾文艺.《数学模型与数学建模》
. 北京师范大学出版社, 1997, 8.

流

[1]

CH EN Gang,

GU O Cheng 2liang,

交

L oca tion Arrangem en t M odel of D r ill ing W ell
W U T ing 2b in
116024)

研

(D a lian U n iversity of T echno logy, D a lian

T he key idea of th is p ap er is to determ ine the inva rian ts w ith resp ect to coo rd ina te

：
科

Abstract:

tran sfo rm a tion s. Fo r the first p rob lem , the au tho rs find tha t a ll the ′
w ells′can be m oved in to a
sing le g rid, and the d istance from each w ell to the nea rest crunode is a con stan t, therefo r the
question is g rea tly sim p lified. Fo r the second question, since the Euclidean d istance betw een
tw o w ells is con stan t under coo rd ina tes tran sfo rm a tion s, a series of necessa ry cond ition s a re ob 2
ta ined to conclude w hether the a ll g iven w ells can be u sed. Fu rtherm o re, a op tim iza tion m odel

号

is estab lished to get a necessa ry and sufficien t cond ition. T he a rithem etic of the second questino
fits the th ird question a s w ell. W e can u se the sam e m ethod to trea t the th ird question a s in the

微

信

公
众

second one.

钻 井 布 局

徐胜阳, 陈思多, 金 豪
指导教师: 数学建模教练组
( 武汉汽车工业大学, 武汉

编者按:

430070)

本文对前两问的解答采用了正确的穷举算法, 得到了正确的结果. 对问题三的解答有特点: 第

一, 给出了一个好用的充分条件: Π i, j , D ij ≤Ε; 第二, 通过算法给出了求 n 个像点的最小外接圆的方法, 该圆
的半径即可作为判别 n 个源点是否可用的条件. 此处反应出作者们较强的创造性.

摘要:

本文将旧井的利用问题归结为 0- 1 规划问题, 由此建立了目标函数. 提出映射原理, 将旧井的位置

映射到一个单位网格中, 从而大大地简化了模型的求解. 应用映射原理和穷举方法, 求解出有方向约束条件
下的可利用点为 4 个, 经过转化, 推广到无方向约束条件下的可利用问题, 解得 6 个点可利用. 研究了目标成
立的充分条件, 给出了三种特殊情形下的判定方法. 提出了中垂线上的二分逼近法.

<!-- source_page: 2 -->

加
人 风
56 数学 的 实 上 距 与 认识 0 times
1 问题 重 述 ( 咯 )
2 符号 约定

om 为 绝对 坐标 系 , 记 为 8:

+iop， 为 题 设 给 定 的 点 所 在 平面 的 坐标 系 , 记 为 S1

raozy; 为 网 格 所 在 平面 的 坐标 系 , 满足 坐标 轴 与 网 格 上 的 边 平行 , 坐标 原点 与 网 格 上 某
一 结 点 重合 , 记 为 8x _

D 为 P/ 与 P 之 间 的 距离 (天 疡 二 2. 让 -从
3 ”模型 的 建立 一 一

旧 并 要 么 被 利用 , 要 么 被 舍弃 , 这 便 形 成 了 一 种 0- age 标 函数 :

上 第 ?个旧 井 被 利用 Ac J
上. 第; 个旧 井 被 舍弃
我 们 要 寻求 目标 函数 的 最 大 值 , 即 w = za SN

每 个 Z， 都 由 同一 个 激活 函数 mr 确定 2 下 ,D 三 ec 时 有 激活 函数
7(P)= 1 否则 为 4 即 有 冰 值 0e 当 源 点 P, 与 距离 最 近 抽 结 点 的 距离 不 大 于 给 定 误差
时 , 点 忆 被 激活 可 用

由 感 设 ,采用 向 量 的 户 一 范 数 定义 距离 问题 一 为 上 。|| -, 平面 上 的 e- 邻 域 为 边 长 2e
的 正方 形 域 ; 问题 二 为 。 AN
4 模型 求解 4 )

4.1 问题 一 : Ne

引 理 “ 设 有 非 负 实数 司 二 器 覆 数 w ,mw, 则 有 : (e+ wm od 1= (+ mm od 1( 证 略 )

贞 射 原理 ”给 定 边 长 洲 1 单位 的 正方 形 网 格 , 以 其 上 某 结 点 为 原点 建立 直角 坐标 系
Te 并 满足 所 有 点 均 处 于 第 一 象限 根据 上 述 引 理 , 对 应 坐标 系
上 任意 -3 区， 5 在 矩形 区 域 C- 人 :中 有 唯一 的 点 PCorso7)

， 从 0<y< 1
"\s 下 cs 把 所 有 旧 井 的 坐标 乙 ( 以 下 称 为 源 点 ) 映射 到 这 个 矩形 区 域 C 内 ，

SN im O4
] more (以 下 称 为 像 点 ) , 我 们 称 区 域 C 为 映射 区

户 映射 到 忆 ” 后 , 相对 于 包含 它 的 单个 网 格 的 相对 位 置 不 变 , 故 源 点 与 像 点 的 激活 状态
完全 相同 , 即 有 广 (P; ) =/(P) 问题 转化 成 在 映射 区 中 寻找 像 点 P, 分 布 最 为 密集 的 边 长
为 26 的 正方 形 区 域 , 该 区 域内 所 有 像 点 P” 所 对 应 的 源 点 P, 均 在 e 一 邻 域内 可 供 利用

这 种 映射 算法 按 一 个 常数 倍数 减 小 了 时 间 复 杂 度

根据 问题 一 所 设 , 用 | 。| -定义 距离 下 忆 " 的 e 一 邻 域 , 对 包含 所 有 像 点 P” 的 映射 区
C 作 穷 举 , 激活 e 一 邻 域内 的 所 有 像 点 , 以 确定 目标 函数

在 映射 区 内 , 按照 平移 方式 穷 举 , 移动 步 长 为 。 步 长 * 的 选取 要 权衡 复杂 度 与 精度 的
问题, 以 保证 在 不 漏 掉 可 能 的 最 优 解 的 情况 下 使 运算 时 间 最 短
o4 © 1994-200: in demic Journal Electronic Publishing House. All rights reserved. htt nk t

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

<!-- source_page: 4 -->

加 天
58 数学 的 实践 与 认识 0 和
系 $， 的 原点 0， 与 绝对 坐标 系 8 的 原点 O 重合 , 则 $， 可 由 8 绕 原点 0 旋转 6 得 到 令 网 格
坐标 系 8; 的 方向 与 绝对 坐标 系 $ 的 方向 相同 , 则 8* 可 由 S 平移 位 移 量 (v, v) 得 到 这 样 ,从
标 系 $8， 与 S。 之 间 的 相互 关系 便 由 转角 6 与 位 移 量 (uv) 唯一 确定

考虑 到 网 格 由 正方 形 构成 , 转角 6 只 需 变化 rw 便 可 以 穷 举 , 故 可 取 转 角 6 为 网 格 纵 边
或 横 边 与 x 轴 的 正 向 夹 角 , 并 满足 0<O mw2 由 于 假设 网 格 足够 大 , 可 任意 确定 一 网 格 结
点 为 坐标 系 $; 的 原点 0 为 了 方便 , 我 们 取 为 绝对 坐标 系 $ 第 一 象限 上 距 原点 O 最 近 的
点 , 易 证 , 位 移 向 量 (wy) 在 映射 区 C 内

以 相互 独立 的 参数 ww v 作为 状态 分 量 , 得 到 三 维 状态 空间 4 4 HK
中 均 唯一 确定 一 个 目标 函数 值 > (Q w =

令 转角 6 以 足够 小 的 步 长 从 0 到 mw 变化 每 当 转角 6 确 定时, 源 虚 所 三重 经 固定
在 绝对 坐标 系 $ 上 了 , 剩 下 的 工作 便 是 固定 方向 平移 网 格 ， g 此 时 的
工作 与 问题 一 相 比 , 除 e 一 误差 邻 域 是 | 。| ; 定义 距离 下 的 之 外 , 其 它 综 竺 租 同 , 可 以 全 慢
借用 问题 一 算法 , 故 不 效 述 SA

运算 结果 (如 图 4 为 : 夹 角 9- 0.779， oom 作 六 评 利 用 点 为 第 1 6 7, 8
9,11 点 全
4.3 ”问题 三 : 完全 利用 的 问题 DA

所 有 旧 井 均 可 利用 的 充分 条 件 是 : 当 所 有 源 点 区 鞭 角度 w(0<oc rw) 形成 一 个 映射 区
( 称 为 g 一 映射 区 ) 后 , 所 有 像 点 必须 沙 在 一 个 半径 有 过 e 的 圆 ( 即 e 一 邻 域 ) 内 , 即 w= w 并 且
Dy<2¢ 我 们 称 其 为 误差 贺 对 于 完全 利用 间 题 , 可 用 如 下 判 据 作 优先 判 电 :

判 据 -在 o- 映 射 区 内 , 若 村 竹 两 点 间 移 距离 pv> 26 则 ， 口 旧 间 不 能 同时 利用 因
为 相距 D > 26 的 两 点 不 可 能 同时 着 从 加 内

判 据 二 “车 or- 占 射 区 内 任 兽 丙 点 间 后 离 D ,满足 Dvsf 3e 则 有 下 = 几 即 这 ， 个 像
TO

证 明 “如 图 5, 作 误差 同 的 内 接 正三 角形 48C, 边 长
为 | 3 e 分 别 以 估计 为 加 心 作 半径 为 | 3 e 的 圆 ,得 到
0 由 于 映射 区 内 任何 一 点 到 4、

BC 的 上 各 甸 不 过 3 e 必 落 在 区 域 已 中 证 之 人

nesawEn 着 成 锐角 或 直 2
角 志 角形 , 则 其 外 接 圆 是 能 将 三 个 项 点 完全 包围 的 最 小 <
1 里 着 pt 角 三 角形, 则 以 钝 角 的 对 边 为 直径 所 作 的 贺 为
能 格 半 个 顶点 完全 包围 的 所 有 国 中 的 最 小 园 当 最 小 贺 半
径 AS e 时 , 则 六 < w 这 就 是 说 如 果 存在 三 个 点 不 能 同时
在 一 个 误差 圆 中 , 这 时 口 旧 井 就 一 定 不 能 同时 被 利用 图 5 判 撮 二 的 示意 图

有 一 种 更 简洁 的 求 最 小 圆 的 算法 :

中 垂 线 上 的 二 分 逼近 法 “如 图 6, 为 了 在 映射 区 中 找到 能 柳 盖 全 部 像 点 的 最 小 圆 域 , 作
包含 w 个 像 点 的 凸 m On 四 边 形 , 作 其 直径 PO 的 中 重 线 交 多 边 形 于 8,T 从 Pg 与 S7 的
交点 O 出 发 , 在 中 重 线 上 搜索 所 求 圆 的 圆心 , 步骤 如 下 :

1 到 点 0 为 圆心 ,R= loP 上 loo | 为 半径 作 贺
3 © 1994-2008 China A C al Electronic Publish ouse. All sreserved. htt nki.ne

<!-- source_page: 5 -->

说
#2 本
葬
1 其 徐 胜 阳 等 : 钻井 布局 9 en
2 找 出 其 余 普 一 2 个 像 点 到 oO 点 的 最 长 距离 D. #D s
> R, 则 使 圆心 2, 朝 R, 增 大 而 D，, 减 小 的 方向 (向 外 ) 移 至
SO 的 中 点 , 继续 步骤 3; 若 D <r , WR 即 为 所 求 最 小 圆 的 忆
半径 , 结束 ; (下 标 表示 迭代 运算 的 次 数 ,二 1 2, …) D OO
3 找 出 其 余 产 - 2 个 像 点 到 oO, 的 最 长 距离 D,, 若 D，
> RCR= Po), 则 使 圆心 ,向 R, 增 大 的 方向 移动 , 移 至 “ 机 2 Q
万 与 其 向 外 方向 邻接 点 的 中 点 处 ; 若 D,< R,， 则 使 圆心 .
O。 ,向 R, 减少 的 方向 (向 内 ) 移动 , 移 至 0,， 与 其 向 内 方向 T2 居
邻接 点 的 中 点 处 若 D = &。 则 有 R, 即 为 所 求 最 小 贺 的 半 。 图 6 中 皇 线 节 二 让 让
径 , 结束 ; of. AN
4 重复 步 又 3 的 工作 , 直到 p ,- R ,| 科 风 0 为 任 一 给 定 的 充分 和 M19 实数 ) 为 止 , 此 时
R; 即 为 所 求 最 小 圆 的 半径
求 得 唯一 的 包含 wm 边 形 的 最 小 圆 (以 下 称 圆 2 ) 的 半径 6 XS
边界 问题 ”如 图 7,8， 为 非 边界 区 $， 为 边界 区 吧 。 r
区 , 根据 映射 原理 , 对 于 S， 内 的 点 , 对 应 8， 由 一 个 戈 凡 个 同
点 而 在 中 垂 线 上 的 二 分 逼近 法 求 R 的 过 程 中 , 因 0OED/ <26
故 m 个 点 都 在 最 小 圆 2 内 下 面 证 明 结论 一 : 若 o T1 RAEH: 4
部 利用 , 则 圆 O 内 一 定 有 7 个 点 , 且 一 个 源 点 在 圆 2 内 只 对 应
一 个 像 点 O
证 明 ”如 图 8 因 ， 口 井 能 被 人 部 利用, 风 请 0<p ,<2c 处 加
于 边界 区 的 每 个 源 点 对 应 圆 2 内 也 hPRer. 而 任 一 源 点 所 对 应 有
的 两 个 或 三 个 像 点 只 能 有 个 圆 2 中 :得 证 图 7 边界 问题 示意 图
由 结论 一 , 可 利用 中 里 线 二 的 到 分 逼近 法 求解 最 小 圆 的 半
径 将 题 设 的 12 个 源 点 代 入 法 , 判定 R> 6E 即 这 12 个 源 点 不 在 半径 为 e 的 圆 内 ; 而 将 问
题 二 求 出 的 6 个 旧 代 六 算法 中 , 求 得 圆 的 半径 R 科 e 这 与 问题 二 的 最 优 解 相 吻 合 这 样 从 正
反方 本 只 证 沪 全 于 天
o
参考 文献
0
[DA 何 振 辣 Siy 夭 勿 能 一 认 知 科学 中 的 若干 重 大 问题 的 研究 湖南 科学 技术 出 版 社 , 1997
RN 控制 理论 (第 一 册 ) 清华 大 学 出 版 社 , 1978
Well- Drilling Layout
XU Sheng-yang, CHEN Si-duo, JN Hao
(W uhan A utomotive Polytechnic U niversity, W uhan 430070)
Abstract By transfom ing the availability of the originalwells into the 0- 1 progranm ing
24 1994-2008 China mic Journal Electronic Publishing House. All rights re ttp://www.cnki.net

<!-- source_page: 6 -->

第 30 卷第 1 期
数学的实践与认识
V o l130 N o 11
2000 年 1 月
J an. 2000
M A TH EM A T ICS IN PRA CT ICE AND TH EO R Y
p rob lem , the ob jective functiom is bu ilt. W e p resen t the m app ing p rincip le, to m ap the loca tion s of
the o rig ina l w ells in to a un ique un it b lock of the m esh, so a s to sim p lify the so lu tion of the m odel.
U sing the m app ing a lgo rithm and the ergod ic a lgo rithm , w e so lve the p rob lem under the d irection
con stra in t. T hen w e genera lize the a lgo rithm s to the so lu tion w ithou t the d irection con stra in t. W e
stud ied the sufficien t cond ition s and g ive som e criteria of the ava ilab ility on th ree p a rticu la r cond i2

交

钻井布局的数学模型

流

tion s. T he m ethod of b isection on p erp end icu la r a t m idpo in t is p resen ted.

( 南京大学, 南京

210093)

本文对钻井布局问题的研究, 是从全局搜索入手, 逐步深入讨论了各种算法的有效性、适用性和复

：
科

摘要:

研

胡海洋, 陈 建, 陆 鑫
指导教师: 陈 晖, 姚天行

杂性, 得到不同条件下求最多可利用旧井数的较好算法.

对问题 1, 我们给出了全局搜索模型、局部精化模型与图论模型, 讨论了各种算法的可行性和复杂度. 得
到的答案为: 最多可使用 4 口旧井, 井号为 2, 4, 5, 10. 对问题 2, 我们给出了全局搜索、局部精化和旋转矢量
等模型, 并对局部精化模型给出了理论证明, 答案为: 最多可使用 6 口旧井, 井号为 1, 6, 7, 8, 9, 11, 此时的网

号

格逆时针旋转 44. 37 度, 网格原点坐标为 (0. 47, 0. 62).

对问题 3, 给出判断 n 口井是否均可利用的几个充分条件、必要条件和充要条件及其有效算法.

模型假设及符号说明 ( 略)

2

问题分析与模型准备

公
众

1

微

信

如果一个已知点 P i 与某个网络结点 X j 距离不超过给定误差 Ε( 0105 ) 单位, 则认为 P i
处的旧井资料可以利用. 因此, 在棋盘 ( 欧氏) 距离定义下, 可以以 P i 为中心, 2Ε单位为边长
作一个正方形 ( 半径为 Ε的圆). 若网络在平移过程中, 网络中的某个结点 X j 落在以 P i 为中
心的正方形 ( 圆) 内或边上, 可认为 X j 可利用旧井 P i 的相应资料. 同样可以以 X j 为中心, 2Ε
单位为边长作一个正方形 ( 圆). 若网络在平移过程中, P i 落在以 X j 为中心的正方形 ( 圆) 内
或边上, 可认为 X j 可利用旧井 P i 的相应资料. 这两种方法分别对应于网格移动和坐标平
移, 显然它们是等价的. 以下的讨论将不明显区别这两种方法. 为了简化讨论, 引入以下法
则.
映射法则:
将点 i 映射至以 (a , b) , ( a + 1, b+ 1) 为对角顶点的正方形内的点 i′
, i′
[ ix ] + a;
x = ix i′
[ iy ] + b, 其中 [ x ] 为 x 的整数部分.
y = iy 覆盖法则:
将 所有旧井映射至 ( - 1, - 1) , ( 0, 0) ; ( - 1, 0) , ( 0, 1) ; ( 0, - 1) , ( 1, 0) ; ( 0, 0) , ( 1, 1) 为
对角顶点的四个正方形上. 以 2Ε为边长作小正方形, 该正方形形心在以 ( - 015, - 015 ) ,

