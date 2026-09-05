# Extracted Paper

<!-- source_page: 1 -->

第 31 卷第 1 期
数学的实践与认识
V o l131 N o 11
2001 年 1 月
J an. 2001
M A TH EM A T ICS IN PRA CT ICE AND TH EO R Y

经比较, 两组结果相近, 说明能够减少波源和接收器.

6

对模型的评价

本文所阐述的模型是以探测山体空洞为目标, 广泛地应用于对山体、坝体、隧洞等某些
内部空洞定位. 问题 2 的解答, 拓宽了本模型的应用范围. 对于特殊的坝体、山体等, 利用本
模型的不等距设置波源和接收器, 同样能测出空洞的位置, 因而具有很强的实用性.

流

参考文献:
南京地区工科院校数学协会建模工业数学讨论班. 数学建模与实验. 河海大学出版社, 1996.

[2]

朱道元. 数学建模精品案例. 东南大学出版社, 1999.

[3]

中国数学协会. 数学的实践与认识. 1998.

[4]

庄天戈. CT 原理与算法. 上海交通大学出版社, 1992.

研

交

[1]

：
科

The O ptim iza tion Solution M ethod in Survey
of the Vacan t Hole
L IAN X iang 2hua,

YAN G Sheng 2m ing, Q IN Kun

Abstract:

210097)

号

(N an jing N o rm a l U n iversity, N an jing

In th is p ap er, w e d iscu ss the po sition p rob lem of the vacan t ho le in su rvey fo r

公
众

m oun ta in, land, tunnel and so on. B y sim p lifica tion, cu tting a p iece of p lane dom a in, w e
estab lish the m odel on the system of linea r equa tion. W e so lved com p letely the po sition p rob lem

空洞探测问题及有关情况

微

信

of the vacan t ho le.

关 信,

韩洁平

( 东北电力学院, 吉林

摘要:

132012)

本文对 2000 网易杯全国大学生数学建模竞赛 ( 大专组)D 题的背景、模型、算法及评阅情况作了简

单介绍.

1

题目产生的背景
本题目来源于吉林丰满水电站水库大坝的检测与维修.
这种类型的大坝每隔一定时间就需进行较全面的维修. 为此, 首先就要对坝的内部结
© 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.

http://www.cnki.net

<!-- source_page: 2 -->

1期

关

信等: 空洞探测问题及有关情况

125

构有清楚的了解, 以便进行有效的维修.
丰满大坝前些年进行一次较全面的维修. 维修前的基础工作是对大坝进行检测, 通过
检测了解大坝的内部的可能的缺陷情况. 丰满坝的检测应用的就是弹性波断层技术. 通过
检测, 获得了大量的数据; 对数据进行处理, 才能得到大坝的有关情况; 由于数据量大, 要由
计算机完成处理. 这样就必须要有符合实际的模型和有效的算法.

2

流

基于上述背景, 简化后给出了一个二维空间探测问题. 为了不造成计算上的困难, 给定
的数据量很少.

模型与算法

网格化
连结波源与其相对应的接收器, 用这样形成的两组与边平行的平行线将给定区域划分
成网格. 每个小矩形 ( 此题是小正方形) 称为一个单元. 使每个单元与一个变量相对应, 若

交

2. 1

：
科

研

单元位于空洞部分, 其取值为 1, 否则取值 0.
设一边上的波源为 m 个, 另一边上的波源为 n 个, 于是得到单元为 (m - 1) ( n - 1) 个, 所
对应的变量也是 (m - 1) ( n - 1) 个, 记为 x 1 , x 2 , …, x (m - 1) (n- 1).
计算精度由网络所决定, 即由波源与接收器的数量与分布所决定.
2. 2 将给定数据转化为相应的通过空洞部分的总长度
计算有关系数和常数项
令 A = ( a ij ) m 1×n1 , m 1 = m (m - 1) + n ( n - 1) , n 1 = (m - 1) ( n - 1).
a ij 的值为联结波源与接收器的直线被相应单元截得的线段长.
令 b= ( b1 , b2 , …, bm 1 ) T , m 1 = m (m - 1) + n ( n - 1)

号

2. 3

公
众

令 x = ( x 1 , x 2 , …, x n 1 ) T , n 1 = (m - 1) ( n - 1)
于是得
Ax = b

( 2)

信

通常 ( 1) 式为超定方程组, 应用最小二乘法, 得
m inJ ( x ) = (A x - b) T (A x - b)
( 2) 式即为“0- 1”
规划问题.
(
)
问题 2 可通过法方程求解.

( 1)

答卷与评阅情况

微

3

有少数答卷将所给问题归结为“0- 1”
规划.
有相当数量的答卷是用排除法 ( 或称剔除法) 求解的. 针对此问题的特殊情况, 此方法
是有效的, 也是较简单的; 但有一定的局限性, 而不具备较普遍的适用性.
答卷能将问题用数学语言表述清楚, 符合题目要求, 结果正确, 即认定基本合格.
评阅时, 特别注意创造性. 答卷若有一定的创造性, 对一些枝节性的毛病与不足就适当
地放宽, 以鼓励创造性.

© 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.

http://www.cnki.net

<!-- source_page: 3 -->

第 31 卷第 1 期
数学的实践与认识
V o l131 N o 11
2001 年 1 月
J an. 2001
M A TH EM A T ICS IN PRA CT ICE AND TH EO R Y

The Prohlem on Survey ing of the Vacan t
Holes and the Relevan t M a tters
HAN J ie 2p ing

(N o rthea stern E lectric Pow er In stitu te,

In th is p ap er the backg round, m odel, a lgo rithm and som e comm en ts in judg ing of

研

the p robem D in the CUM CM 2000 a re in troduced sim p ly.

讯

：
科

简

132012)

交

Abstract:

J ilin

流

GU AN X in,

号

第七届全国数学建模教学与应用会议论文集
将在本刊今年第 5 期发表

公
众

第七届全国数学建模教学与应用会议于 2000 年 8 月 17 日至 20 日在郑州举行, 来自全国 27 省 ( 市、自
治区) 205 所院校的代表 283 人出席会议. 这次会议是在教育部高教司和中国工业与应用数学学会的领导
下, 由全国大学生数学建模竞赛组委会和中国工业与应用数学学会数学模型专业委员会组织、由中国人民
解放军信息工程大学承办的, 中科院院士、中国数学会副理事长丁伟岳教授出席了会议.
这次会议是 1986 年第一届会议以来出席人数最多的一次, 特别是 30 岁左右的年轻人占大部分, 而且

信

第一次有中学教师参加, 充分显示出我国从事数学建模教学与应用的队伍在不断壮大
从 1989 年, 特别是 1994 年以来, 在教育部的领导和指导下, 我国数学建模教学与应用活动取得很大

微

成绩, 具体表现在: 参加过国内外数学建模竞赛的大学生超过四万人, 通过赛前准备、竞赛三天的拼搏和赛
后继续三个阶段的努力, 他们的能力普遍获得很大提高; 培养出一大批年轻教师; 推动了数学教学改革; 推
动了中学生数学知识应用活动; 为进一步发展我国的应用数学事业提出了许多值得思考的问题. 这次会议
也是为明年将在我国召开的第十届国际数学建模教学与应用会议作准备.
四天的会议安排了多项大会报告和分组报告. 这些报告经整理后将以论文形式在本刊 2001 年第 5 期
发表. 分为“数学建模与数学教育”
、
“ 数学建模教学与竞赛”
、
“ 数学建模应用”
、
“ 数学建模方法”等专栏.

© 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.

http://www.cnki.net

