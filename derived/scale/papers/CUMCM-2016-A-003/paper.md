# Extracted Paper

<!-- source_page: 1 -->

# 论文标题

# 摘要

本文通过受力分析、最小二乘法、非线性规划、变步长搜索算法等方法，建立了系 泊系统状态模型、多目标非线性规划模型对系泊系统的设计问题进行了研究。 针对问题一，首先建立以锚为原点、风向为 x 轴，竖直方向为 z 轴，海床所在平面 为 O-xy 平面，风向所在铅锤面为 O-xz 平面的标准坐标系，从而刻画浮标的游动区域。 其次，为描述系泊系统的状态，通过对该系统的各组成部分进行隔离受力分析，确定了 浮标所受的杆拉力与风速、吃水深度的表达式，以及钢杆、钢桶、锚链倾角的递推关系， 并结合海水深度的几何约束，最终建立了系泊系统状态模型；接着，基于锚链着地现象 的考虑，对着地处的锚链进行了受力分析，从而得到了着地锚链的倾角关系，并结合未 着地的倾角关系以及海水深度的几何约束，建立了系泊系统状态的修正模型；最后，本 文针对复杂多元非线性方程组的求解问题，设计了基于最小二乘法的搜索算法，求解出 了海面风速分别为 12m/s 和 24m/s 时，钢桶和各节钢管的倾斜角度、锚链形状、浮标吃 水深度与游动区域，见图 5.4.3，见表 5.4.2。 针对问题二，首先利用问题一建立的系泊系统状态模型和基于最小二乘法的搜索算 法，对海面风速为 36m/s 时，钢桶与各节钢管的倾斜角度、锚链形状、浮标吃水深度和 游动区域进行了求解见文中 XXX 页，XX 表。其次，针对题目所给出的系泊系统设计要求， 将浮标吃水深度，浮标的游动区域，钢桶的倾角作为优化目标，以各个构件在竖直方向 投影的几何约束作为约束条件，以重物球的配重作为决策变量，建立了多目标非线性规 划模型。接着，采用熵权法对各优化目标分配权重，从而将多目标规划问题转化为单目 标规划问题。最后，利用循环搜索算法对模型进行求解，得到的满足设计要求的配重范 围为 2200 ££ *m* *q* 4100 kg 、最佳配重为 2894*kg* 。 针对问题三，首先基于海水流速与近海风速夹角的考虑，建立了以锚为原点，海水 流速方向为 x 轴, 竖直方向为 z 轴, 海床所在平面为 O-xy 平面, 水流速度所在法平面 为 O-xz 平面的标准坐标系，从而描述浮标的游动区域。其次，根据海水流速与海水深 度的关系，结合“近海水流力”的近似公式，从而得到水流力与海水深度的关系。接着， 对系泊系统进行受力分析，确定了各参数间的关系，进而建立了系泊系统的三维状态模 型。再次，结合问题二对优化目标的分析，以锚链型号，锚链长度，重物球配重作为决 策变量，建立了多目标非线性规划模型。最后，考虑到模型的复杂程度，通过变步长搜 索算法对模型进行求解，结果如表 7.3.2 所示。 本文的特色在于将机理分析与多目标规划相结合，运用熵权法将多目标问题转化为 单目标问题，使得求解结果更加客观。此外，对于解空间较复杂的模型，设计了变步长 搜索算法，在保证了求解的精度的同时，极大地提高了运算的时间复杂程度，为日后系 泊系统的设计的发展提供了参考依据。

## 关键字： 系泊系统设计 机理分析 最小二乘法 变步长搜索算法

<!-- source_page: 2 -->

一、问题重述

近浅海观测网的传输节点由浮标系统、系泊系统和水声通讯系统组成（如图 1 所示）。 某型传输节点的浮标系统可简化为底面直径 2m、高 2m 的圆柱体，浮标的质量为 1000kg。 系泊系统由钢管、钢桶、重物球、电焊锚链和特制的抗拖移锚组成。锚 的质量为 600kg， 锚链选用无档普通链环，近浅海观测网的常用型号及其参数在附表中列出。钢管共 4 节， 每节长度 1m，直径为 50mm，每节钢管的质量为 10kg。要求锚链末端与锚的链接处的 切线方向与海床的夹角不超过 16 度，否则锚会被拖行，致使节点移位丢失。水声通讯 系统安装在一个长 1m、外径 30cm 的密封圆柱形钢桶内，设备和钢桶总质量为 100kg。 钢桶上接第 4 节钢管，下接电焊锚链。钢桶竖直时，水声通讯设备的工作效果最佳。若 钢桶倾斜，则影响设备的工作效果。钢桶的倾斜角度（钢桶与竖直线的夹角）超过 5 度 时，设备的工作效果较差。为了控制钢桶的倾斜角度，钢桶与电焊锚链链接处可悬挂重 物球。系泊系统的设计问题就是确定锚链的型号、长度和重物球的质量，使得浮标的吃 水深度和游动区域及钢桶的倾斜角度尽可能小。 问题 1：某型传输节点选用 II 型电焊锚链 22.05m，选用的重物球的质量为 1200kg。 3 现将该型传输节点布放在水深 18m、海床平坦、海水密度为 1.025×10 kg/m³ 的海域。若 海水静止，分别计算海面风速为 12m/s 和 24m/s 时钢桶和各节钢管的倾斜角度、锚链形 状、浮标的吃水深度和游动区域。 问题 2：在问题 1 的假设下，计算海面风速为 36m/s 时钢桶和各节钢管的倾斜角度、 锚链形状和浮标的游动区域。请调节重物球的质量，使得钢桶的倾斜角度不超过 5 度， 锚链在锚点与海床的夹角不超过 16 度。 问题 3：由于潮汐等因素的影响，布放海域的实测水深介于 16m~20m 之间。布放 点的海水速度最大可达到 1.5m/s、风速最大可达到 36m/s。请给出考虑风力、水流力和 水深情况下的系泊系统设计，分析不同情况下钢桶、钢管的倾斜角度、锚链形状、浮标 的吃水深度和游动区域。

二、问题假设

1. 假设浮标在水面上不存在偏斜；
2. 假设各构件均为刚体，不发生变形；
3. 假设问题三中海水流速随深度呈抛物分布；
4. 假设海水流速方向水平。
三、符号说明

|类型|符号|含义|
|---|---|---|
|上标|a b c|xoy 在 平面 xoz 在 平面 xoy 在 平面|
|下标|i ij,|构件编号 i 构件 对构件 作用量 j|
|变量|F|构件相互作用力|

<!-- source_page: 3 -->

|变量|G|构件重力|
|---|---|---|
||T f q b|构件所受浮力 构件所受水流力 构件倾角 作用力与竖直方向夹角|

四、问题分析

4.1 问题一的分析 问题一要求建立系泊系统内钢桶和各节钢管倾斜角度，锚链形状和浮标吃水深度变 化的数学模型，因此需要对不同结构分别进行受力分析，从而找到题目要求的各个参数 的递推关系，进而构建本问题的非线性方程组。 其次，为了分析各个参数与风速的关系，则需要根据“近海风荷载”的近似公式， 对浮标进行进一步受力分析。 此外，为了求解出海面风速为 12m/s 和 24m/s 时钢桶和各节钢管的倾斜角度、锚链 形状、浮标的吃水深度和游动区域，需要求解之前构建的非线性方程，进而确定各个参 数。考虑到解空间不大，因此本文采用基于最小二乘法的搜索算法进行求解。
4.2 问题二的分析 为了计算海面风速为 36m/s 时，钢桶和各节钢管的倾斜角度，锚链形状和浮标的游 动区域，则只要将海面风速带入模型一进行求解即可。 为了满足钢桶的倾斜角度不超过 5 度，锚链在锚点与海床的夹角不超过 16 度的要 求，需要建立以重物配重为决策变量，海水深度为几何约束条件的多目标非线性规划模 型。由于数据规模不大，本文采用循环搜索算法对模型进行求解。
4.3 问题三的分析 为了分析在海水深度、海水速度，风速变化情况下钢桶、钢管的倾斜角度、锚链形 状、浮标的吃水深度和游动区域，需要依据问题二的思路建立多目标非线性规划模型， 决策变量为锚链型号、锚链长度以及重物配重。

<!-- source_page: 4 -->

五、问题一模型的建立与求解

5.1 模型准备 对于本问，可通过引入决策变量浮标吃水深度*h*，以海面风速和海水深度*H* 在作为 已知条件，借助物理学与力学原理进行机理分析得到系统内在关系，进而求得系泊系统 各状态参数。 首先，本文以锚和锚链的交点为原点，建立空间直角坐标系来讨论系统内部的受力 情况，示意图如下：
图 5.1.1 系统空间坐标系 接着，为了方便表述，我们用 *PP*1~*N*来依次表示系统内部从上到下的 *N* 种构件，由 题中锚链长度除以单个链环的长度可以得到锚链共有 210 个链环，由此得到*N* 的数值： *N* = + + + 1 4 1 210 + = 1 218 各编号代表的具体构件如下表所示： 表 5.1.2 各构件编号

|P 编号 i|i =1|25 ££ i|i = 6|7 ££ i 216|i = 217|
|---|---|---|---|---|---|
|构件类型|浮标|钢管|钢桶|锚链|锚|

5.2 模型建立
5.2.1 系泊系统受力分析 本文假设风向平行于海平面，当风速度不变时，海风方向的变化会使浮标在圆形区 域内运动，并且各方向平衡时系统状态相同。因此，本文在平面内对系统进行受力分析。 （一）浮标的受力 如图 5.2.1 所示，浮标受到速度为*v* 的海风作用在海面上达到平衡，设其吃水深度为 *h*，此时浮标一共受到 4 个力的作用。

<!-- source_page: 5 -->

图 5.2.1 浮标受力示意图

其中*T₁*表示浮标所受浮力大小，方向竖直向上。由阿基米德定律可以得到浮力*T₁*与

吃水深度*h*的关系为

2 p*dh* 1 *Tg* =× r （5-2-1） 1 4

## 式中， r 为海水的密度； d₁ 为浮标底面直径。

## 浮标还受到水平方向的风力 F₀ 的作用，由题中已知关系式可知风力和风速有如下关

系：

ì*F₀₁* =´ 0.625 *S v²* í （5-2-2） =-(*l₁ h d*) îS₁ 1

## 其中 S₁ 为浮标在风向法平面的投影面积，l₁为浮标高度。

浮标下表面与第一节钢管铰接，钢管对浮标作用力的大小用*F* 表示，其与竖直方 2,1 向的夹角为 b₁。此外，物体还受到竖直向下的重力*G₁*。物体受力平衡根据牛顿第一定律

## 有浮标在 xy, 方向的合力为零，即：

ì*F₀*-= *F*2 1，*sin*b₁ 0 í （5-2-3） *T₁*-*F* cos b₁-*G₁* = 0 î 2 1，

对方程组进行求解并分离变量得到钢管对浮标作用力大小*F* 和夹角 b₁表达式为： 2,1

ì2 2 2 25(*l*-*h*) *d v⁴* + 4(rp *g d h*- 4*G*) 1 1 1 1 ï*F* = 2,1 ï 8 í （5-2-4） 2 ïb 5(*l₁₁*-*h d v*) = arctan 1 2 ï 82 *G* + *g*rp*d h* î 11

<!-- source_page: 6 -->

（二）钢管的受力

图 5.2.2 钢管受力示意图

钢管*P* （ 25 ££ *i* ）受力如图 5.2.2 所示，首先对于底面直径为*d* ，轴向高度为*l* 的 *i i i* 圆柱形钢管的浮力由阿基米德定律有

4 p*dl* *ii* *Tg* =× r （5-2-5） *i* 4

物体静止不发生移动由牛顿第一定律有：

ì*FFi*-1,*i*× sin bb*i*-1-*i*+1,*i*× sin*i*= 0 í （5-2-6） *T* + *F* × cos bb-*G*-*F* × cos = 0 î*i i*-1,*i i*-1 *i i*+1,*i i*

求解方程组分离变量得到钢管上下端点作用力递推关系式为： ì *Fi*--1,*i*× sin b*i* 1 = arctan ïb*i* *T* + *F* × cos b-*G* ï*i i*--1,*i i* 1 *i* ï í *Fi*+1,*i*× sin b*i*（5-2-7） *F* = ï *ii* +1, *F* × sin b *i*--1,*i i* 1 ï sin(arctan) ïî *Ti*+ *Fi*--1,*i*× cos b*i* 1-*Gi*

接着，物体不发生转动由力矩平衡定理对钢管下端点取矩有 *l* *i* *F* sin b *l* cosq-*F* cos b *l* sinq + (*G*-*T*) × sinq = 0 （5-2-8） *i*-1,*i i*-1 *i i i*-1,*i i*-1 *i i i i i* 2

对上式进行分离变量得到钢管倾斜角q*i*关于上端点作用力的递推关系式：

*F* sin b *i*--1,*i i* 1 q = arctan （5-2-9） *i*

0.5(*T*-+ *G*) *F* cos b *i i i*--1,*i i* 1
（三）钢桶的受力

## 如图 5.2.3 所示，钢桶静止时共受到 6 个外力作用，其倾斜角度（与竖直方向夹角）

为q₆ ，其上端与钢管 *P₅* 铰接，钢管对钢桶作用力大小为*F* ，倾角为 b₅；下端与锚链链 5,6 环*P₈* 铰接并悬挂一重物球，链环对钢管作用力大小为*F* ，倾角为 b₆ 。 8,6

<!-- source_page: 7 -->

图 5.2.3 钢桶受力示意图

首先，同样由阿基米德定律得到钢桶浮力*T₆* 与重物球浮力*T* 表达式如下： *q*

2 ì p*dl* 66 ï*Tg*6=× r í 4 （5-2-10） ï*T* =× rr *g m* î*q q q*

式中， *dl*66, 分别为钢桶的底面直径和轴向高度；*m*, r 分别为重物球的质量和密度。 *qq* 接着由牛顿第一定律得到钢桶平衡不发生移动时满足如下关系：

ì*FF*5,6sin bb5-=8,6sin60 í （5-2-11） *T₆* + *T* + *F* cos bb-*F* cos-*G₆*-*G* = 0 î*qq* 5,6 5 8,6 6

同样的对方程组进行求解分离变量得到*F* 与 *F* ， b₅与 b₆ 的关系式如下 5,6 8,6

ì *F*5,6sin b₅ = arctan ïb₆ *F* cos b + *T* + *T*-*G*-*G* ï5,6 5 6 *qq* 6 ï í *F*5,6sin b₅ （5-2-12） *F* = ï 8,6 *F* sin b 5,6 5 ï sin(arctan) ïî *F*5,6cos b₅ +*T₆* + *Tqq*-*G₆*-*G*

此外，物体平衡不发生转动还需满足合力矩为零的条件，本文统一选取构件下端中 心点取矩，这里对钢桶下端点取矩满足如下关系： *l* 6 (*T₆*-*G₆*) × sinq₆ + *F* ×*l₆* cos b₅ sinq₆-*F* ×*l₆* sin b₅ cosq₆ = 0 （5-2-13） 5,6 5,6 2

对上式分离变量得到钢桶倾斜角q₆ 的关于*F*, b₅表达式为 5,6

*F* × sin b₅ 5,6 q₆ = arctan （5-2-14）

0.5(*T₆*-*G₆*) +*F* × cos b₅
5,6

（四）锚链的受力

锚链各节链环的受力情况与各节钢管受力情况相似，因此上文中的钢管递推关系式

同样适用于锚链链环。但对于链环浮力的计算，题中只给出了各节链环的质量，体积是

<!-- source_page: 8 -->

[1] 未知的，本文参考题目背景中“采用无档普通链环”查阅资料 得一般链环密度 r ，这 *m* 样链环*P* （ 7 ££216 ）浮力计算公式： *ii*

*T* =× rr *g m* （5-2-15） *i m i*

式中*m* 为链环质量。得到各节链环作用力与倾角递推关系如下： *i*

ì *Fi*--1,*i*× sin b*i* 1 = arctan ïb*i* *T* + *F* × cos b-*G* ï*i i*--1,*i i* 1 *i* ï *F* × sin b *i*+1,*i i* ï*Fii* +1,= *F* × sin b ï *i*--1,*i i* 1 sin(arctan （5-2-16） í *T* + *F* × cos b-*G* *i i*--1,*i i* 1 *i* ï ï *F* sin b *i*--1,*i i* 1 ïq*i*= arctan

0.5(*T*-+ *G*) *F* cos b
ï *i i i*--1,*i i* 1 ï *T* =× rr *g m* î *i m i*

至此，本文通过受力分析得到了系泊系统中各构件作用力与倾角的递推关系。

5.2.2 系泊系统几何约束分析 根据以上受力分析，系泊系统状态由决策变量浮标吃水深度*h*确定，可通过海床深 度约束对其进行求解。
图 5.2.4 构件投影示意图 如图 5.2.4 所示，系统稳定时在海水中各构件在竖直方向上的投影总长度应该等于 海床深度，即 *N* *h*+=å*l* cosq *H* （5-2-17） *ii* *i*=1

由各构件在水平方向上的投影长度进一步得到浮标游动圆半径*r* ： *N* *rl* =åsinq （5-2-18） *ii* *i*=1

综合以上分析得到系泊系统的状态模型总的表述为：

<!-- source_page: 9 -->

ìì 25(*l*-*h*) *d v⁴* + 4(rp *g d h*- 4*G*) ïï*F₂₁*= ïï ïí2 5(*l*-*h d v*) 11 ïïb₁ = arctan ï 82 *G* + *g*rp*d*2*h* ïî11 ï *F* sin b₅ ïì5,6 = arctan ïïb⁶ *F* cos b + *T* + *T*-*G*-*G* ï5,6 5 6 *qq* 6 ï ï *F* sin b ï5,6 5 *F* = ïï 8,6 *F* sin b 5,6 5 ïí sin(arctan) ï ï *F* cos b + *T* + *T*-*G*-*G* 5,6 5 6 *qq* 6 ïï *F* × sin b₅ ïï5,6 = arctan ïïq⁶ 0.5(*T*-+ *G*) *F* × cos b î6 6 5,65 ï í ì *Fi*--1,*i*× sin b*i* 1 ïïb*i*= arctan ïï *Ti*+ *Fi*--1,*i*× cos b*i* 1-*Gi* ïï *F* × sin b ï*i*+1,*i i* ï*Fii* +1,= ïï *Fi*--1,*i*× sin b*i* 1 sin(arctan) ïí *T* + *F* × cos b-*G* *i i*--1,*i i* 1 *i* ïï ïï *F* sin b *i*--1,*i i* 1 ïïq*i*= arctan

0.5(*T*-+ *G*) *F* cos b
ïï *i i i*--1,*i i* 1 ïîï （5-2-19） *i*Î[2,5] È[7, 216]，*i* Î *z* ï *N* ï ï*h*+=å*lii*cosq *H* ï*i*=1 ï*N* ï*rl* =å *ii*sinq î *i*=1

5.3 模型修正 在实际情况中，当风速过小时锚链会提前沉底，导致以上模型对于锚链链环作用力 与倾角的递推关系不再适用，因此本文针对这一情况对模型进行修正。示意图如图 5.3.1 所：
图 5.3.1 完全沉底链环受力图

由图可知，锚链第一个完全沉底的链环共受到 5 个外力作用，分别为重力*G* ，浮力 *i* *T* ，摩擦力*F* ，海床提供的支撑力 *FN* 以及上一个链环的拉力*F* 。 *i f ii*-1, + 在链环处于将要被提起处于临界状态时，其与海床的夹角a ® 0 ，对 *A*点取矩有

<!-- source_page: 10 -->

*l* *i* *MA* = (*T* *i* -*G* *i* ) × cosa + *F* *i*-1,*i* cos b *i*-1 ×*l* *i* cosa -*F* *i*-1,*i* sin b *i*-1 *l* *i* sina （5-3-1）

+ 由于链环不发生转动，故合力矩为零，且a ® 0 ，则 sina ® 0 ，cosa ®1。故有：

*F* *i*--1,*i* × cosb *i* 1 = 0.5(*G* *i* -*T* *i*

) （5-3-2）
进而得到链环*Pi*完全沉底时，上一个链环对其作用力满足如下关系：

*F* *i*--1,*i* × cosb *i* 1 £ 0.5(*G* *i* -*T* *i*

) （5-3-3）
此时，若将*Pi*以上构件看做一个整体，对该整体的浮力和重力作差，则满足

*i*-1

# åTj-= GjFi--1,icos bi 1（5-3-4）

*j*=1

联立上式得到竖直方向受力约束条件为： *i*-1

# åTj-Gj£ 0.5(Gi-Ti) （5-3-5）

*j*=1

综上所述，对模型作出如下修正： *i*-1 l 增加海水中构建竖直方向受力约束：å*T* *j* -*G* *j* £ 0.5(*G* *i* -*T* *i* ) 。 *j*=1 l 更改锚链递推关系式适用范围： 7 ££ *ij*， *j* 表示第一个脱离海床链环的编号。 *j* 216 l 更改浮标游动半径表达式：*r* =+åå*l* *i* sinq *i* *l* *i* 。 *i*=11 *i*= +*j* 至此，针对链环沉底情况对模型修正完毕。

5.4 模型求解 对于系泊系统状态模型的求解，难以直接通过大量状态方程得到定解，所以联立非 线性方程组求定解方法不适用。因此本文采用一种基于最小二乘思想的循环搜索算法对 模型进行求解。
5.4.1 基于最小二乘思想的循环搜索算法 描述系泊系统状态模型中的未知变量包括吃水深度*h*，钢桶，各节钢管以及锚链刚 体的倾斜角度q*i*，由模型的可确定各个倾斜角度q*i*与钢桶吃水深度*h*的递推关系，故倾 斜角度可由钢桶的倾斜角度确定，故风速*v* 确定的情况下，系泊系统的状态可由吃水深 度 *h*一个变量确定。因此将吃水深度*h*为连续变量，故将其离散化进行定步长搜索可对 模型进行求解，具体算法步骤如图 5.4.1 所示：

<!-- source_page: 11 -->

图 5.4.1 搜索算法流程图 图 5.4.1 中，模型 I 为未修正模型。模型 II 为针对锚链提前触底修正后的模型。

5.4.2 算法精度检验 对于定步长的循环搜索算法，误差的主要来源为变量的步长，因此可以通过减小步 长，根据最优解变化幅度来判断步长是否合理。
1 取变量*h*步长没原步长的 ，则算法精度应提高 50 倍，定义相对优化量*q* 为目标 50 函数优化量与理论优化量的比值：

*S*¢(*h*) -*S*(*h*) *q* = 50

-3 通过 matlab 编程计算可得*q* =´ 0.38 10 ，由于长度范围在 0.1 数量级，因此*q* 可以

忽略不计，故目前搜索算法中设置的步长可认为是合理的。

5.4.3 结果分析
33 本文假设锚链和重物球材料为普通铸铁，其密度为 7.8´10 *kg* / *m* ，由此参数求解。

当海面风速为12*ms* / 时，本文通过 matlab 编程对模型进行求解，结果表明此时锚 链出现提前触底的情况，此时各构件倾角与浮标吃水深度如表 5.4.2 所示：

<!-- source_page: 12 -->

表 5.4.2 求解结果

|钢桶倾角|1.2089°|钢管 3 倾角|1.1799°|
|---|---|---|---|
|钢管 1 倾角|1.1641°|钢管 4 倾角|1.1880°|
|钢管 2 倾角|1.1720°|浮标吃水深度|0.6818 m|

由于锚链提前沉底，本文假设沉底锚链完全拉直，得到浮标游动半径为14.7232*m*， 2 22 进而得到游动区域面积为 681*m* ，在 *xoy* 平面表达式为 *xy* +£ 681，单位为 m。此时锚 链从 152 个链环开始触底，沉底链环个数为 59 个，锚链形状及各构件在 *xoz* 坐标平面中 形状如图 5.4.3 所示：

图 5.4.3 锚链形状示意图 图 5.4.5 锚链形状示意图 当海面风速为 24*ms* / 时，求解结果表明此时锚链完全脱离海床没有提前触底。求解 得到系统各参数如表 5.4.4 所示： 表 5.4.4 求解结果

|钢桶倾角|4.5837°|钢管 3 倾角|4.4871°|
|---|---|---|---|
|钢管 1 倾角|4.4294°|钢管 4 倾角|4.4516°|
|钢管 2 倾角|4.458°|浮标吃水深度|0.6959 m|

2 浮标游动半径17.8224*m*得到其游动区域面积为 997.89*m* ，在 *xoy* 平面表达式为 22 *xy* +£ 997.89 ，单位为 m。此时锚链在锚点与海床夹角为 5.7059° ，求解得到锚链形状 如图 5.4.5 所示。

六、问题二模型的建立与求解

6.1 模型准备 本问首先要根据问题一中模型计算海面风速为 36*ms* / 时系统的各状态参数。接着题 目要求通过调节重物球的质量来使钢桶倾角和锚链在锚点与海床的夹角小于给定阈值， 由此可以通过问题一模型计算得到重物球的质量范围。但结合题目背景考虑，本文建立 优化模型，在满足约束范围内搜索重物球的最优质量使得系统达到最优状态。
6.2 系泊系统优化模型的建立 （一）决策变量的确定

<!-- source_page: 13 -->

根据题目要求，本文假设重物球材料不变，确定重物球的质量*m* 为模型的决策变 *q* 量，通过调节*m* 的大小来对目标进行优化。 *q*

（二）目标函数分析

由题目背景可知，要对系泊系统进行优化就要使得浮标的吃水深度和游动区域以及 钢桶的倾斜角度尽可能小。据此本文一共确立如下 3 个优化目标。 l 钢桶的倾斜角度尽可能小：

*F* ×sin b₅ 5,6 min q₆ = arctan

0.5(*T₆*-*G₆*) +*F* × cos b₅
5,6

l 浮标的吃水深度尽可能小： *N* min *h*=*H*-å*l* cosq *ii* *i*=1

l 浮标的在海面上的游动区域为圆形，目标可以转化为浮标的游动半径尽可能小： *N* min *rl* =åsinq *ii* *i*=1

（三）约束条件分析

问题二同样满足问题一的假设，因此优化模型需要满足问题一模型的约束条件。此 外根据题目要求，还需要满足锚链在锚点与海床夹角不超过 16 度： p

- q₂₁₆ £ 16° （6-2-1）
2

## 式中q₂₁₆ 为与锚点相连接的链环与竖直方向的夹角。此外，对于优化目标钢桶的倾

## 角q₆ 还需满足约束：

*F* × sin b₅ 5,6 q₆ = arctan £ °5 （6-2-2）

0.5(*T₆*-*G₆*) +*F* × cos b₅
5,6

综合以上分析，并结合问题一模型中系统中各构件作用力与倾角的递推关系得到系 泊系统的优化模型为：

<!-- source_page: 14 -->

*N* min *h* =-*H*å*l* *ii* cosq *i*=1 *F* 5,6 × sin b₅ min q₆ = arctan

0.5(*T₆*-*G₆*) + *F*
5,6 × cos b₅ *N* min *rl* =å *ii* sinq *i*=1 ìì 25(*l*-*h*) 2 *d v⁴* + 4(rp *g d* 2 *h*- 4*G*) 2 ïï*F₂₁*= 1 1 1 1 ïï 8 ïí 5(*l*-*h d v*) 2 ïïb₁ = arctan 11 2 ïî ï 82 *G* + *g*rp*d h* 11 ï ïì = arctan *F* 5,6 sin b₅ ïïb⁶ *F* cos b + *T* + *T*-*G*-*G* ï ï5,6 5 6 *qq* 6 ïï *F*5,6sin b₅ ïï *F* 8,6 = *F* sin b ïí sin(arctan 5,6 5 ) ï ï *F* cos b + *T* + *T*-*G*-*G* 5,6 5 6 *qq* 6 ïï ïï = arctan *F* 5,6 × sin b₅ ïïq⁶ 0.5(*T*-*G*) + *F* × cos b î6 6 5,6 5 ï *st*. í *F* × sin b ì*i*--1,*i i* 1 ïïb*i*= arctan ïï *Ti*+ *Fi*--1,*i*× cos b*i* 1-*Gi* ïï ï ï*F* = *i*+1,*i i* *F* × sin b *ii* +1, *F* × sin b ïï*i*--1,*i i* 1 ïí sin(arctan) ïï *i i*-1,*i ii*-1 *TF* +× cos b-*G* ïï *F* sin b *i*--1,*i i* 1 ïïq*i*= arctan ïï

0.5(*T* *i* -+ *G* *i* ) *F*
*i*--1,*i* cos b *i* 1 ïîï *i*Î[2,5] È[7, 216]，*i* Î *z* ï ï *N* ï*h*+=å*lii*cosq *H* ï*i*=1 ï*N* ï*rl* =å *ii*sinq （6-2-3） î *i*=1

6.3 模型求解
6.3.1 多目标转化单目标求解 对于三个目标的权重值的确定，基于赋权的可靠性考虑，本文在此选择了主观性相 对较小，能够充分利用数据特征的熵权法。熵权法可以根据各个目标的变异度，利用信 息熵计算出各个目标的客观权重值。信息熵越小，变异程度最大，重要程度越大。期计 算结果为 *A*= 11.46,*B* = 1.5,*C* = 0.05

<!-- source_page: 15 -->

## 接着我们对以上三个目标分别赋以权重 A B C,, ，将多目标优化转化为单目标优化问

题，用*U* 表示总的优化目标： min *U* = *A*×q₆ + *B*× + *h C* × *r*

6.3.2 风速为 36m/s 时系统参数求解 通过 matlab 编程代入风速对问题一模型进行求解，结果表明此时锚链全部浮于水 中，此时各构件倾角与浮标吃水深度如表 6.3.1 所示：
表 6.3.1 求解结果

|钢桶倾角|9.4767°|钢管 3 倾角|9.2935°|
|---|---|---|---|
|钢管 1 倾角|9.1822°|钢管 4 倾角|9.3502°|
|钢管 2 倾角|9.2375°|浮标吃水深度|0.7187 m|

2 得到浮标游动半径为18.8906*m*，进而得到游动区域面积为1121.092*m* ，其在 *xoy*平 22 面表达式为 *xy* +£ 1121.092 。此时锚链在锚点与海床的夹角大小为 21.397°> 16° ，表 明锚点被拖动。锚链在 *xoz* 坐标平面中形状如图 6.3.2 所示：

图 6.3.2 锚链形状示意图

6.3.3 系泊系统优化模型的求解 （一）循环搜索算法求解 Step 1: 根据系泊系统的设计要求求解重物球的质量范围 *mm*
*qq* min ~ max ，令重物的初 始重量值为质量范围下限*m* *q*min ； Step 2: 将重物球最小质量*m* *q* 带入模型一，按照模型一的求解算法求解出并记录此 时的吃水深度*h*，钢桶倾斜角度q₆ ，锚链在锚点与海床夹角 90°-q₂₁₆,浮标游动半径*r* ， 并求解出此时的目标函数值*u* ，并令 min*uu* = ； Step 3: 判断此时的系统状态是否满足 90°-q₂₁₆ £ 16° ，q₆ £° 5 的约束条件，若满足 进入 Step 4,不满足进入 Step 5； Step 4: 若*uu* £ min ，则令 min*uu* = ，并记录*h*，q₆， *r* ，否则 min*u* 保持不变。

<!-- source_page: 16 -->

Step 5: 令 *mm* *qq* =+ 0.5

Step 6: 若 *mm* *qq* £ max ，返回 Step 2，否则结束程序，输出*h*，q₆， *r* 。

（二）结果分析 根据以上算法，本文通过 matlab 编程求解，得到满足题目要求时重物球的质量范围， 并在此范围求得重物球最佳质量，使得系统达到最优状态，结果如表 6.3.3 所示 表 6.3.3 具体结果

|重物球质量范围|重物球最佳质量|浮标吃水深度|浮标游动半径|钢桶倾角|
|---|---|---|---|---|
|2200 ££ m 4100 kg q|2894 kg|1.16 m|18.2831 m|2.9954°|

（三）灵敏度分析 为进一步研究重物球质量变化对每个优化目标的相关性及相关程度，我们对模型进 行灵敏度分析，结果下图所示：

图 6.3.4 重物质量对浮标游动及吃水影响 图 6.3.5 重物质量对钢桶倾角影响

如图 6.3.4 所示随着重物球质量增加，浮标游动半径减小，吃水深度增加，但变化 范围很小，表明重物球质量对二者关系影响较小；由图 6.3.5 可知，钢桶倾角随重物球 质量增加而减小，且相对幅度较大，即重物质量变化对钢桶倾角具有较大影响。

七、问题三模型的建立与求解

7.1 模型准备 与问题一不同，问题三中增加了海水流动这一因素，当海水流动方向与风速方向不 在同一平面时，需要在三维空间中对系统各个构件进行研究。但如果直接在空间坐标系 中对构件进行受力分析，过程繁琐且不方便表述，因此我们将各个构件及其受力投影到 *xoy*,, *xoz yoz* 三个平面内，如图 7.1.1 所示，进而在每个平面内对构件进行受力分析。

<!-- source_page: 17 -->

图 7.1.1 构件投影示意图 此外，为方便表述，本在问题一中符号系统增加上标*abc*,, 来分别构件或力在 *xoy*， *xoz* ， *yoz* 平面内的投影。

7.2 模型建立
7.2.1 系泊系统的水流力分析 （一）水流力函数分析 根据参考文献
[2] 可知，在海域浅水区不同水深的水流速度服从抛物线分布，即： 2 *v* =× *k z* (7-2-1)

## 式中 z 表示离海床的竖直高度。因此，只要给定海面最大水速vmax和海水最大深度

*H* ，就可解得系数*k* ，进而得到随深度变化的水流函数： *v* max 2 *vz* = 2 (7-2-2) *H* 接着，由题中已知海水速度与水流力关系式得到系泊系统水流力函数为： 2 374*Sv* × max 4 *Fz* = 4 (7-2-3) *H*

（二）构件水流力计算

图 7.2.3 投影面微元示意图 由于水流沿 *x* 轴方向，故构件在 *yoz* 平面投影即为在水流法方向面投影。如图 7.2.3 所示，在构件投影中取面积微元 *ds* ，当浮标底面半径为*D*时，根据式(7-2-3)得到对应水 流力为：

<!-- source_page: 18 -->

374*v* max *dF* =× *z Ddz* *H* 对上式积分即可得到浮标受到水流力大小： *Z*2 374*Dv*max 4 *f* = *z dz* （7-2-4） ò*Z* 4 1*H*

7.2.2 系统构件受力分析 为方便分析，本文以锚点为原点，海水流动方向作为 *y* 轴正方向在系泊系统中建立 空间直角坐标系。由于只要确定构件在两个平面内的投影状态就可构件的空间状态，因 此本文下面只在两个投影面对构建进行受力分析。 （一）浮标的受力分析
图 7.2.1 浮标在 *yoz* 面投影 图 7.2.2 浮标在 *xoy* 面投影

## 浮标在 xoz 面投影受力如图 7.2.1 所示，f 表示海水流动力，由牛顿第一定律并结合

式子(5-2-3)可得： *c c c c* ìï*F₀*-*F sin*b₁ + *f₁* = 0 2,1 í*c c c c*（7-2-5） ïî*T₁*-*F*2,1cos b₁-*G₁* = 0

对方程组求解并分离变量得：

|||cc|
|---|---|---|
|c||01|
|1||cc|
|||11|
||cc||
|c|10||

ìb *Ff* + = arctan ï ï *TG*- í （7-2-6） ï *fF* + *F* = 2,1 *c* ï sin b î 1

## 式中上标c 表示在 yoz 平面内。

## 浮标在 xoy 面上投影面受力如图 7.2.2 所示，a₀ 为风速与海水流动方向夹角的余角，

同样由牛顿第一定律得到平衡方程，求解分离变量得到： *a* ìb*aF₀₀* cosa = arctan ï 1 *aa* ï *fF*1+0sina₀ í （7-2-7） *a* ï *aF₀₀* cosa *F* = 2,1 *a* ï sin b î 1

## 同样，式中上标a 表示在 xoy 平面。

<!-- source_page: 19 -->

（二）钢管的受力分析

图 7.2.3 钢管在 *yoz* 面投影 图 7.2.4 钢管在 *xoy* 面投影

*b* 钢管在 *yoz* 平面投影如图 7.2.3 所示， *f* 为等效海水流动力，根据牛顿第一定律得 *i*

到物体受力平衡方程组，对方程组求解分离变量得：

*b b b* ì *Ff* sin b + *b i*--1,*i i* 1 *i* ïb*i*= arctan*b b b b* ï *Fi*--1,*i*cos b*i* 1+-*TiGi* í （7-2-9） *b b b* ï*bFfi*--1,*i*sin b*i* 1+*i* *F* = ï*ii* +1, *b* sin b î *i*

接着对钢管*b*点取矩，平衡不发生转动时其合力矩必为零： *b b b b b b b b b b b* (*T*-*G*)sinq + 2*F* cos b *l*sinq- 2*F* sin b cosq-*f* cosq = 0 (7-2-10) *i i i i*-1,*i i*-1 *i i*-1,*i i*-1 *i i i*

对式（7-2-6）进行分离变量得到钢管与 *z* 轴夹角： *b b b* *Ff* sin b + 0.5 *b i*--1,*i i* 1 *i* q = arctan （7-2-11） *i b b b b*

0.5(*T*-+ *G*) *F* cos b *i i i*--1,*i i* 1
钢管在 *xoy* 平面内投影如图 7.2.4 所示，由与水流方向为*x* 轴正方向，故 由投影定理 水流力在 *xoy* 平面与 *yoz* 平面投影大小相等： *ab* *ff* = （7-2-12） *ii* 同样由钢管静止不发生转动时满足合力为零且合力矩为零得到平衡方程，对方程求 解并分离变量得： *aa* ì *F* sin b *a i*--1,*i i* 1 ïb*i*= arctan*a a a* *fF* + cos b ï*i i*--1,*i i* 1 ï *aa* *F* sin b *a i*--1,*i i* 1 ï = ï*F*2,1 1 í sin b*i*（7-2-13） ï*aa* *F* sin b ï*a i*--1,*i i* 1 = *i a a a* ïq 0.5 *fF* + cos b *i i*--1,*i i* 1 ï ïî25 £ £ *i* ，*i* Î *z*

<!-- source_page: 20 -->

（三）钢桶的受力分析

图 7.2.5 钢桶在 *yoz* 面投影 图 7.2.6 钢桶在 *xoy* 面投影

钢桶及重物球在 *yoz* 平面投影如图 7.2.5 所示，由钢桶静止不发生转动故在 *xz*, 方向

合力为零且合力矩为零（对钢桶下端点取矩），得到平衡方程组： *b b b b b b b b* ì*F* cos bb +*T₆* + *T* +*G₆*-*G*-*F* cos = 0 5,6 5 *qq* 7,6 6 ï*b b b b b* í*F*5,6sin bb5+ *f₅*-*F*7,6sin6= 0 (7-2-14) ï *b b b b b b b b b b b* *F* cos b sinq + (*T*-*G*) sinq-*F* sin b cosq-*f* cosq = 0 î25,6 5 6 6 6 6 5,6 5 6 5 6

对方程组(7-2-10)求解并分离变量得： *b b b* ì

|Ff|sin b₅|+|
|---|---|---|
|5,6||6b|
|b b b b 6|b|qq b b|
|b|b|b|
|5,6|5|5|
|b b|b|b|

*b* 5,6 6 ïb₆ = arctan*b b* *F* cos b₅ +*T₆* + *T*-*G₆*-*G* ï5,6 ï *b* ï*bFf*5,6sin b₅ + í*F*7,6= (7-2-15) sin b₆ ï ï *Ff* sin b + 0.5 *b* ïq₆ = arctan ïî 0.5(*T₆*-+ *G₆*) *F*5,6cos b₅

在*xoy* 平面内，钢桶投影如图 7.2.6 所示，对于海水流动力由式(7-2-8)可得： *ab* *ff* = (7-2-16) 66 同样由钢管静止不发生转动时满足合力为零且合力矩为零得到平衡方程，对方程求 解并分离变量得： *aa* ì *F* sin b₅ *a* 5,6 ïb₆ = arctan*a a a* *fF* + cos b₅ ï6 5,6 ï *aa* ï*aF*5,6sin b₅ í*F*2,1=1(7-2-17) sin b₆ ï ï*aa* *F* sin b *a* 5,6 5 ïq₆ = *a a a* ïî 0.5 *fF*6+5,6cos b₅

<!-- source_page: 21 -->

（四）锚链的受力分析 锚链受力情况与钢管类似，即各节锚链链环同样满足式（7-2-9），（7-2-11），（7-2-13）， 这里不再重复分析。此外，由于链环形状未知，导致在计算链环水流力时无法直接得到 投影面积，因此本文根据其质量与密度将其转化为同体积圆柱体处理，满足： 2 p*dl* *ii* = r *m* *ii* 4

7.2.3 系泊系统设计优化模型 （一）决策变量的确定 综合考虑环境因素以及系统内部构件参数对系泊系统的影响并结合题目背景，本文 选取如下 3 个决策变量以及 4 个环境变量对系泊系统进行研究。

|ì|ì海水深度H||
|---|---|---|
|ï|ï||
|ï|ï海水速度v||
|ï环境变量 í ï|ï海面风速|v|
|ï í|ï î风速与水流方向夹角a₀||
|ï ï|ì重物球质量m||
|ï决策变量 í锚链链环数量|ï|n|
|ï ïî|ïî锚链链环长度|L|

*f*

*q*

（二）目标函数及约束分析 与问题二相同，选取浮标吃水深度，浮标游动半径以及钢桶倾斜角作为优化目标建 立多目标优化模型。同样本问模型需要满足问题二中约束条件，这里不再赘述。

## 综合以上分析，并结合式(6-2-1)， (6-2-2) ，(6-2-3)得到系泊系统设计优化模型为：

<!-- source_page: 22 -->

*N* *bb* min *h* =-*H*å*li*cosaq*i*cos*i* *i*=1 *bb* min q₆ =× arccos(cosq₆ cos b₆) *N* *a* min *rl* =å *ii*cosa *i*=1 ìì *c c c c* *F₀*-*F*2,1*sin*b₁ + *f₁* = 0 ïï *c c*

|c|c||
|---|---|---|
|cc|||
|01|||
|cc|||
|11|||
|c|||
|1 b|b|b|
|i--1,i|i 1|i|
|b|b b|b|
|i--1,i|i 1 i|i|
|b b|b||
|i--1,i i 1|i||
|b ib|b|b|
|i--1,i|i 1|i|
|b|b b|b|
|i|i i--|1,i i 1|
|i--aa 1,i a|i 1||
|i a i-- aa 1,i i 1|1,i i a 1||
|a i|a||
|a ii-1, a|i-1 a||
|i i--1,i|i 1||

ïï*T₁*-*F*2,1cos b₁-*G₁* = 0 ïï ïïíb*c* = arctan *Ff* + ï ï 1 *TG*- ïï *cc* ïï *cfF*10+ *F*2,1= ï sin b ïïî ïì *Ff* sin b + *b* ïïb*i*= arctan ïï *F* cos b +-*TG* ïï ïï *F* *b* = *Ff* sin b + ïï *ii* +1, sin b ïï ïï*bFf* sin b + 0.5 ï qï*i* = arctan ïï

0.5(*T*-+ *G*) *F* cos b
ïï *F* sin b ïí ïb*i* *a* = arctan ïï *fF* + cos b ïï ïï *a* *Fi*--sin b ï ï 2,1 sin b¹ *F* = ï *st*. íï *F* sin b ï *a* = ïïq*i* ï ï

0.5 *fF* + cos b
ïïî *i*Î[2,5] È[7, N]，*i* Î *z* ï *b b b*

|ïì|Ff|sin b|+|
|---|---|---|---|
|b|5,6 b b|5 b|6 qq b b|
||b b|||
|7,6 b|b 6 6 b|b|b|
|b|5,6 b|b b|5 b|

*b* 5,6 5 6 ïïb₆ = arctan *b*

|ïï|F|cos b₅ + T₆ + T|- G₆ - G|
|---|---|---|---|
|ïï ïïF|sin b₅ +|||
|ïï ïï|= Ff sin b|||
|ïï||Ff sin b₅ + 0.5||
|ïïq₆ = arctan ïï ïí ïïb ï ïï ï ïï ïï F ïï ïïï ï q₆ = ïïî|0.5(T₆ -+ = arctan fF F sin b₅ = sin b¹ F 0.5 fF +|G₆ ) F sin b + cos b₅ sin b₅ cos b₅|F cos b₅|
|ï|374Dv|||
|ï f = î|H|z dz||

5,6 *b* 5,6

5,6 *aa* *a* 5,6 5 6 *a a a* 6 5,6 （7-2-18） *aa* *a* 5,6 2,1 6 *aa* *a* 5,6 *a a a* 6 5,6 *Z* 2max 4 ò *Z*

<!-- source_page: 23 -->

7.3 模型求解 由于决策变量增加直接导致问题三模型解空间过大，因此为了保证求解的时效性与 准确性本文采用变步长搜索算法对模型进行求解。
7.3.1 变步长搜索算法 1）连续变量的离散化 模型的决策变量有重物球的配重*m*
*q* ，链环的个数*n* ，链环长度*L* = {*L₁*,*L₂*,*L₃*,*L₄*,*L₅*} ， 需要对其进行全局搜索寻找目标函数的最小值，由于重物球的配重*m* *q* 为连续变量，因 此先将其离散化，进行定步长搜索。 2）变步长搜索算法 由于解空间较大，使用变步长搜索算法对模型进行求解，即先使用较大步长进行全 局搜索，得到近似最优解，在找到的近似最优解附近使用较小步长进行局部搜索寻找目 标函数的最优解。

7.3.2 结果分析 基于以上模型和算法，本文首先将风速和水速定为最大值，且二者方向相同，再次 条件下分别计算海水深度为16*m*、 20*m*时系泊系统最优状态，得到对应参数如表 7.3.1 所示：
表 7.3.1 求解结果

|海水深度|重物配重 m q|链环个数|链环长度|钢桶倾角|浮标吃水深 度|浮标游动半 径|
|---|---|---|---|---|---|---|
|16m|3000kg|140|180mm（型号 V）|4.593°|1.59m|18.61m|
|20m|2950kg|180|180mm（型号 V）|4.959°|1.37m|11.41m|

为了进一步研究系统在不同情况下的参数变化，在海床深度为 16m 时本文对各环境 变量作适当的改变，求解得到此时系泊系统参数的变化情况，具体结果如表 7.3.2 所示： 表 7.3.2 不同情况下<u>系泊系统参数变化</u>

|水流速度 m/s|风速 m/s|钢桶倾角|浮标吃水深度|浮标游动半径|
|---|---|---|---|---|
|1.5|24|4.259°|1.3m|18.795m|
|1|36|3.615°|1.295m|18.0m|
|1.5|12|3.57°|1.295m|17.977m|
|0.5|36|2.543°|1.288m|16.053m|

锚链在各个情况下形状变化情况如下图所示：

图 7.3.3 风速 24m/s，水速 1.5m/s 图 7.3.4 风速 36m/s，水速 1m/s

<!-- source_page: 24 -->

图 7.3.5 风速 12m/s，水速 1.5m/s 图 7.3.6 风速 36m/s，水速 0.5m/s

八、模型评价及推广

8.1 模型的评价 本文的亮点之一是建立的非线性规划模型，将系泊系统的实际问题通过目标函数的 设计转化为优化问题，本文的另一个亮点在于对多元非线性方程组的求解设计的基于最 小二乘法的搜索算法以及在保证求解精度条件下，当模型解空间较大时设计的变步长搜 索算法，且在能够接受的时间内提高了搜索精度。 但是由于在实际情况下，系泊系统的结构存在变形，将其作为刚体进行计算会带来 计算误差。
8..2 模型的改进 在实际海洋中，由于海浪的作用力，会导致浮标的上下震动，这样会使得浮标的稳 态描述需要由一个竖直确定的振动方程确定，由于时间的限制以及模型的复杂程度，本 文对该情况尚未考虑。
8.4 模型的推广 本文建立的系泊设计模型具有一定的推广价值，在已知实际海洋的环境的条件下， 可以通过本文建立的模型，为系泊系统的参数设计提供理论依据。可以在航运，近浅海 勘探等方面得到应用。
九、参考文献

[1] 郝春玲，流速分布及锚链自身刚度对弹性单锚链系统变形和受力的影响，国家 海洋局第二海洋研究所，2006-09-15 [2] 郝春玲、滕斌，不均匀可拉伸单锚链系统的静力分析,大连理工大学，2003-08-30 [3] [国家标准]-GBT549-1996

附录 附录 1：问题一的解答程序 mq=1200;%ÖØÎïÇòÖÊÁ¿ n=210;%ÃªÁ´¸ÕÌå¸öÊý min=inf; minh=0;

<!-- source_page: 25 -->

minH=0;
minbeta=0;
minthital=zeros(1,4);
minthita2=zeros(1l,n)+pi/2;
minFt2=zeros (1,n+l);
for h=0:0.0001:2
Ft=zeros(1,5);%.0'0?; .OH 人 -人 -及 |
alpha=zeros(1,5);%.0'02; -0 +A-A|pA .ETO
thital=zeros(1,4);% + 0'UpA TO
beta=0;%,0T° pi .2To
Ft2=zeros(l,n+1l);3A%A"2; -OpA +A-A|
gama=zeros (1,n+1);$A*A"?; -O +A-A|pA TO
thita2=zeros(1l,n)+pi/2;% +A%A DA TO
.ite22 .0
v=24;% cEU
S=2*(2-h);
m=1000;%, j+&0BA;
rou=1025; $°£E@AUIE
g=9.8; %0gA | HOEUIE
V=pi*172%h;%°0E@Ia»y
Ffeng=0.625*S*v"2;% CcA!
Ffu=rou*g*Vv;%, jA|
Gfu=m*qg;%, j+&00A;
if Ffu-Gfu<0
continue;
end
alpha (1)=atan (Ffeng/ (Ffu-Gfu)) ;
Ft (1)=sqrt (Ffeng”2+ (Ffu-Gfu) "2);
%,010%; 0
Vg=1*pi*0.025%2;% 0'Uia»y
Ggang=10*g;%, O'UOGA|
Fgfu=rou*g*vg;
for i=1:4
alpha(it+l)=atan((Ft(i)*sin(alpha(i)))/(Ft(i)*cos (alpha(i))+Fgfu-Ggang));
Ft (i+1l)=Ft(i) *sin(alpha(i))/sin(alpha (i+1));
thital (i)=atan(Ft (i)*sin(alpha(i))*1/((Fgfu-Ggang) *1/2+Ft (i) *cos (alpha(i)))
)
end
$,01°2¢ 0
25

<!-- source_page: 26 -->

Vt=1*pi*0.15%2;% 0f°Ta»y
Vq=mq/7800; $081iCoTa»y
Gt=100%g;%.01°%; 00C 玉 |
Gq=mqxgjsOoTiCooc 玉 |
Ftfu=rou*g*Vt;$ .Of”.i 玉 |
Fgfu=rou*g*Vq; 300A|Co, jA|
gama (1) =atan (Ft (5) *sin (alpha (5)) / (Ftfu+Ft (5) *cos (alpha (5)) -Gt-Gg+Fgfu) ) ;
Ft2(1)=Ft(5)*sin(alpha(5))/sin(gama(1));
beta=atan (Ft (5) *sin(alpha (5))*1/ ((Ftfu-Gt) *1/2+Ft (5) *cos (alpha(5)) *1)) ;
$A2A 2; -0
mm=0.735; $A*A OEA;
roum=6450; $A%A AUIE
Vm=mm/roum; $A%A Ta»y
Fmfu=rou*g*Vm; $A*A"  [A|
Gm=mm*qg; $A*A OgA|
Lm=0.105;%A*A" *uqE
for i=1:n
gama (i+1)=atan (Ft2(i) *sin(gama (i))/ (Ft2(i) *cos (gama (i))+Fmfu-Gm)) ;
if gama (i+1)<0
gama (i+1)=gama (i+1) +pi;
end
Ft2 (i+1)=Ft2(i) *sin(gama(i))/sin(gama (i+1));
thita2 (i)=atan(Ft2 (i)*sin(gama(i)) *Lm/ ((Fmfu-Gm) *Lm/2+Ft2 (i) *cos (gama (i)) *L
m));
if thita2(i)<0
thita2 (i)=thita2(i)+pi;
end
end
H=h+sum(cos (thital)) +cos (beta) +Lm*sum(cos (thita2)) ;
if abs(H-18)<min
minh=h;
min=abs (H-18) ;
minH=H;
minthital=thital;
minthita2=thita2;
minbeta=beta;
minFt2=Ft2;
end
end
26

<!-- source_page: 27 -->

附录 2 问题 一 沉 底 修补 程序
function [r,minh,minbeta,minthita2,minH] = tuodir (n,mq)
SUNTITLED3 Summary of this function goes here
% Detailed explanation goes here
min=inf;
minh=0;
minH=0;
minbeta=0;
minthital=zeros(1,4);
minthita2=zeros(1,n)+pi/2;
mini=0;
for h=0.6:0.0001:0.72
Ft=zeros(1,5);%,0'0U?; .Oh +A-A|
alpha=zeros(1,5);%.0'0%; -0, +A-A|pA .TO
thital=zeros(1,4);% + 0'UpA TO
beta=0;% OL°pd 2Io
Ft2=zeros (1,n+1);%$A*A"?; Oh +A-A|
gama=zeros (1,n+1);$A*A"?; -O +A-A|pA TO
thita2=zeros(1l,n)+pi/2;% +A%A DA ETO
%,it8%2:0
v=12;% cEU
S=2*(2-h);
m=1000;%, ; +&0EAs
rou=1025;%°£EQAUIE
g=9.8; $0gA | LOEUIE
V=pi*172%h;%?0E®la»y
Ffeng=0.625*S*v*2;% ‘¢A|
Ffu=rou*g*v;%, {A]
Gfu=m*qg;$%, it+teOCAI|
if Ffu-Gfu<0
continue;
end
alpha (1)=atan (Ffeng/ (Ffu-Gfu)) ;
Ft (1)=sqrt (Ffeng”2+ (Ffu-Gfu) "2);
%,010%; 0
Vg=1*pi*0.025%2;% 0'Ula»y
Ggang=10*g;%, O'UOGA|
Fgfu=rou*g*vg;
for i=1:4
alpha(i+l)=atan ((Ft(i)*sin(alpha(i)))/(Ft(i)*cos (alpha(i))+Fgfu-Ggang));
27

<!-- source_page: 28 -->

Ft (i+1l)=Ft(i) *sin(alpha(i))/sin(alpha (i+1));
thital (i)=atan(Ft (i)*sin(alpha(i))*1/((Fgfu-Ggang) *1/2+Ft (i) *cos (alpha(i)))
)i
end
$,01°2¢ 0
Vt=1*pi*0.15%2;% 0f°Ta»y
Vq=mq/7800; $081iCoTa»y
Gt=100%g;%.01°%; 00C 玉 |
Gq=mqxgjsOoTiCooc 玉 |
Ftfu=rou*g*Vt;$ .Of”.i 玉 |
Fgfu=rou*g*Vq; 300A|Co, jA|
gama (1) =atan (Ft (5) *sin (alpha (5)) / (Ftfu+Ft (5) *cos (alpha (5)) -Gt-Gg+Fgfu) ) ;
Ft2(1)=Ft(5) *sin(alpha(5))/sin(gama(1));
beta=atan (Ft (5) *sin(alpha(5))*1/ ((Ftfu-Gt) *1/2+Ft (5) *cos (alpha(5)) *1)) ;
$A2A 2; -0
mm=0.735; $A*A OEA;
roum=6450; $A%A AUIE
Vm=mm/roum; $A%A" Ta»y
Fmfu=rou*g*Vm; $A%A°  {A]
Gm=mm*qg; $A3A OJA|
Lm=0.105; $A%A" *mqk
for i=1:n
gama (i+1)=atan (Ft2(i) *sin(gama (i))/ (Ft2(i)*cos (gama (i))+Fmfu-Gm)) ;
if gama (i+1)<0
gama (i+1)=gama (i+1) +pi;
end
Ft2 (i+1)=Ft2(i) *sin(gama (i))/sin(gama (i+1));
thita2(i)=atan(Ft2(i)*sin(gama(i)) *Lm/ ((Fmfu-Gm) *Lm/2+Ft2 (i) *cos (gama (i)) *L
m));
if thita2(i)<0
thita2 (i)=thita2(i)+pi;
end
H=h+sum(cos (thital))+cos (beta) +Lm*sum (cos (thita2)) ; $%aEad» 个
if gama(i+1)>pi/2-0.015
break;
end
end
28

<!-- source_page: 29 -->

if i<n&&abs (H-18)<min
minh=h;
minH=H;
minthital=thital;
minthita2=thita2;
minbeta=beta;
mini=i;
end
end
r=Lm*sum(sin (minthita2))+sin (minbeta)+sum(sin(minthital));
end
附录 三 : 问题 二 优化 程序
n=210;%A%*A" 01a ofy
kxmg=[];
kxh=[];
kxr=[];
kxbeta=[];
zfenshu=[];
for mg=1800:4100%7"  OCOORA;
mg
min=inf;
minh=0;
minH=0;
minbeta=0;
minthital=zeros(1,4);
minthita2=zeros(1,n)+pi/2;
minFt2=zeros (1,n+1);
for h=0:0.01:2
Ft=zeros(1,5);%.0'0?; -OpA +A-A;
alpha=zeros(1l,5);% 0'0?; -0 <A-A|pA TO
thital=zeros(1,4);% + 0'UpA .To
beta=0;%, 0I°pA .TO
Ft2=zeros (1,n+1);%$A%A"2; -OpA +A-A|
gama=zeros (1,n+1) ; $A*A"?; -O +A-A|pA TO
thita2=zeros(l,n)+pi/2;% +A%A DA ETO
s .ite2z
v=36;% cEU
S=2*(2-h) ;
m=1000;%, ;+&0RA;
rou=1025; $°£E@AUIE
29

<!-- source_page: 30 -->

g=9.8; 200A | MOR09E
V=pi*172%h;%20E014»y
Ffeng=0.625%S*v~2;% ‘cA|
Ffu=rou*g*v;% iA|
Gfu=m*g;%, +&00A|
if Ffu-Gfu<0
continue;
end
alpha (1)=atan (Ffeng/ (Ffu-Gfu)) ;
Ft (1)=sqrt (Ffeng”2+ (Ffu-Gfu) *2) ;
$. 0102¢ -0
Vg=1*pi*0.025%2;% 0'UTa»y
Ggang=10*g;% O'UOGA|
Fgfu=rou*g*Vvg;
for i=1:4
alpha (i+l)=atan((Ft(i)*sin(alpha(i)))/ (Ft(i) *cos (alpha(i))+Fgfu-Ggang)) ;
Ft (i+1)=Ft (i) *sin(alpha(i))/sin(alpha (i+1));
thital (i)=atan(Ft(i)*sin(alpha(i))*1/ ((Fgfu-Ggang) *1/2+Ft (i)*cos (alpha(i)))
) 7
end
$.0122:40
Ve=1*pi*0.15%2;% Of°1a»y
Vq=mq/7800; 3081iCoTa»y
Gt=100%g;% 01°%; -O0@A!
Gg=mq*g; $081 1CO0PA !
Ftfu=rou*g*vt;% 0I° ;A!
Fgfu=rou*g*Vvq; $00A|Co , jA!
gama (1) =atan (Ft (5) *sin (alpha(5))/ (Ftfu+Ft (5) *cos (alpha (5) ) ~Gt-Gg+Fqfu) ) ;
Ft2(1)=Ft (5) *sin(alpha (5))/sin(gama(1));
beta=atan (Ft (5) *sin (alpha(5)) *1/ ( (Ftfu-Gt) *1/2+Ft (5) *cos (alpha (5)) *1)) ;
人 六 及 -2
mm=0.735; $A%A ORA;
roum=6450; $A%A" AUIE
Vm=mm/roum; gs 六 = 天 14»y
Fmfu=rou*g*Vm; $A*A"  jA|
Gm=mm*g; $A*A OgA!
Lm=0.105; $A%A" *=qE
30

<!-- source_page: 31 -->

for 1=1:n
gama (i+l)=atan (Ft2(i)*sin(gama(i))/(Ft2(i) *cos (gama (i))+Fmfu-Gm)) ;
if gama (i+1)<0
gama (i+1)=gama (i+1)+pi;
end
Ft2(i+1)=Ft2(i)*sin(gama(i))/sin(gama (i+1));
thita2(i)=atan(Ft2(i)*sin(gama(i)) *Lm/ ((Fmfu-Gm) *Lm/2+Ft2 (i) *cos (gama (i)) *L
m));
if thita2(i)<0
thita2 (i)=thita2(i)+pi;
end
end
H=h+sum(cos (thital))+cos (beta)+Lm*sum(cos (thita2));
if abs(H-18)<min
minh=h;
min=abs (H-18) ;
minH=H;
minthital=thital;
minthita2=thita2;
minbeta=beta;
minFt2=Ft2;
end
end
if minthita2 (n)>pi/2%ADIIEC -i” ¥ux
[r,minh,minbeta,minthita2,minH]=tuodir (n,mq) ;
else
r=Lm*sum (sin (minthita2))+sin (minbeta)+sum(sin (minthital));
end
if minbeta*180/pi>5% Of°CakC?»°~'y598
continue;
end
if (90-minthita2(n)*180/pi)>163A0TEAZA 0&°L 21DHC2» ~1y169E
continue;
end
if abs(minH-18)>0.2
continue;
end
a=36/pi;b=1.5;c=1/20;
fenshu=a*minbeta+b*minh+c*r;
31

<!-- source_page: 32 -->

kxmq=[kxmq mq]; kxh=[kxh minh]; kxbeta=[kxbeta minbeta]; kxr=[kxr r]; zfenshu=[zfenshu fenshu]; end [fenshu,i]=max(-zfenshu); fenshu kxmq(i)

附录四：熵值法 function [ weight] = shangzhifa( x) n= 10; [datanum,weights]=size(x); k=1/log(n); R=zeros(1,weights); weight=zeros(1,weights); P=zeros(datanum,weights); for i=1:datanum for j=1:weights if x(i,j)==0 P(i,j)=0.001; else P(i,j)=x(i,j)/sum(x(1:datanum,j)); end end end

for i=1:datanum for j=1:weights P(i,j)=P(i,j)*log(P(i,j)); end end for i=1:weights P(1:datanum,i); R(i)=1-(-k)*sum(P(1:datanum,i)); end for i=1:weights

<!-- source_page: 33 -->

weight(i)=R(i)/sum(R(1:weights)); end end

附录五：二维模型制图 n=140; xq=0; yq=0; Lm=0.105; L=1; %minthita1=minthita1(5:8); %minthita2=minthita2(211:420); %minbeta=minbeta(2); for i=n:-1:1%ÃªÁ´ xz=xq+Lm*sin(minthita2(i)); x=xq:0.0001:xz; y=yq+cot(minthita2(i))*(x-xq); yq=yq+cot(minthita2(i))*(xz-xq); xq=xz; plot(x,y,'LineWidth',2); hold on end

xz=xq+L*sin(minbeta); x=xq:0.0001:xz; y=yq+cot(minbeta)*(x-xq);

x1=(xq-0.15):0.0001:(xq+0.15); y1=yq-tan(minbeta)*(x1-xq); x2=(xq-0.15):0.0001:(xz-0.15); y2=y1(1)+cot(minbeta)*(x2-x1(1)); x3=(xz-0.15):0.0001:(xz+0.15); y3=y2(size(y2,2))-tan(minbeta)*(x3-x2(size(y2,2))); x4=(xq+0.15):0.0001:(xz+0.15); y4=y1(3001)+cot(minbeta)*(x4-x1(3001)); plot(x1,y1,'LineWidth',2);hold on; plot(x2,y2,'LineWidth',2);hold on; plot(x3,y3,'LineWidth',2);hold on; plot(x4,y4,'LineWidth',2);hold on;

yq=yq+cot(minbeta)*(xz-xq); xq=xz;

<!-- source_page: 34 -->

for i=4:-1:1
XZ=XG+Lxsin (minthital (i));
x=xq:0.0001:xz;
y=yq+cot (minthital (i))* (x-xq) ;
yg=yq+cot (minthital (i))* (xz-xq) ;
XQ=XZ;
plot (xy 'LineWidth',2);
hold on
plot(xq,yq,'."','color','r', 'LineWidth', 50)
end
line([0,22],10,0], 'color', 'k', 'LineWidth',2);hold on;
line([0,22],[18,18], 'color','k', 'LineWidth',2) ;hold on
line([xg-1,xq+1], [yq,yq], 'LineWidth',2);hold on
line ([xg9-1,x9-1], [yq,yg+2], 'LineWidth',2) ;hold on
line([xg-1,xg+1], [yg+2,yqg+2], 'LineWidth',2) ;hold on
line ([xg+l,xq+1l], [yq,yg+2], 'LineWidth',2) ;hold on
axis ([0 30 -2 20])
ylabel ('#%a°£ 2 BIE(m)');
xlabel ('A8A®pA%aAs (m) 小
hold off
附录 六 ， 三维 模型 制图
n=140;
xq=0;
ya=0;
zq=0;
Lm=0.18;
L=1;
$minthital=minthital(5:8);
$minthita2=minthita2(211:420);
$minbeta=minbeta (2) ;
for i=n:-1:1%A%A"
xz=xq+Lm*sin (minthita2 (i)) *cos (gama4 (i));
x=xq:0.001:xz;
y=ygttan (gama4 (i)) * (x-xq) ;
yg=yg+tan (gama4 (i)) * (xz-xq) ;
z=zqg+ (x-xq) ./cos (gama4 (1)) . *cos (minthita2 (i));
zg=zq+ (xz-xq) ./cos (gama4 (i)) .xcos (minthita2 (i));
XQ=XZ;
plot3(x,y,z, 'LineWidth',2);
34

<!-- source_page: 35 -->

hold on

end

grid on

hold off

附录 7 三 维 考虑 沉 底 函数
function [ r,minh,minbeta,minthital,minthita2,minH ] =
tuodir2( nrmaqrvrVvshuivgqdH )

SUNTITLED11l Summary of this function goes here

% Detailed explanation goes here

mm=0.735; $A%A OEA;

Lm=0.105; $A%A" *nqE

alpha=0;% -cIO0EE@A+IOnAYMDYC

min=inf;

minh=0;

minH=0;

minbeta=0;

minthital=zeros(1,4);

minthita2=zeros(1,n)+pi/2;

mingama2=zeros(1,4);

mingama3=0;

mingamad=zeros (1,n);

for h=0:0.01:2
Ftx=zeros(1,5);%,0'U%; Oh +A-A pAx -0A;
Fty=zeros (1,5);%,0'0%; -OpA, +A-A|pAyY .ORAL
Ftz=zeros(1,5);%,0'0%; -OpA +A-A|pAz .ORAL
thital=zeros(1,4);% .= O'Upk %T00&20anAlkbpiC
gama2=zeros (1,4);% + 0'U I160UXOYEIIT0°0&x0apAdyC
beta=0;%,0I°pA 1160&20apAkdsC
gama3=0;% 01° I160UX0YEITT0° 0&x0apAtdisC
Ft2x=zeros(l,n);%A%A"2; -OpA +A-A|nAxX OA
Ft2y=zeros(l,n);%A%A"2; -OpA +A-A|pAY -OAg
Ft2z=zeros(l,n);%A*A"2; -OpA +A-A|nAz OA
thita2=zeros(1,n)+pi/2;%A*A"  +A WUpA s160820apAdiC
gamad=zeros (1,n);%$A%A" +A 10 -1I00UXOYEIT90°08X0apAtdsC
%,it8%2:0
S=2*(2-h);
m=1000;%, j t&0EA;
rou=1025; %$°£EQAUIE

35

<!-- source_page: 36 -->

g=9.8; $0gA LOEUIE
V=pi*172*h;%°0E@1ax»y
Ffeng=0.625*%S*v~2;% cA|
Ffu=rou*g*Vv;% jA|
Gfu=m*qg;%, ; +&00A|
Fshui=374* (vshui/gdH"2* (gdH-h) "2) ~2*2*h; SE+EUEGA | DG 下
if Ffu-Gfu<0
continue;
end
Ftx (1)=Fshui+Ffeng*cos (alpha) ;
Fty(l)=Ffeng*sin(alpha);
Ftz (1)=Ffu-Gfu;
gs 0102¢ 6
Vg=1*pi*0.025%2;% 0'UTa»y
Ggang=10*g;%, O'UOGA|
Fgfu=rou*g*vg;
Fshui2=[374* (vshui/gdH"2* (gdH-h-0.5)"2) ~2*1%0.05, 374* (vshui/gdH"2* (gdH-h-1.
5)^2)^2x*lx0.05,374x (vshui/gdH 2* (gdH-h=-2.5) *2) A2*1%0.05,374* (vshui/gdH 2* (g
dH-h-3.5)"2)"2*1%0.05] ; SR+EUE@A | DA 下
for i=1:4
gama2 (i)=atan (Fty(i)/ (Fshui2 (i) /2+Ftx(i)));
Ftp=Ftx (i) *cos (gama2 (i))+Fty (i) *sin (gama2 (i)) ;
thital (i)=atan ((Ftp+Fshui2 (i)*cos(gama2(i)))/ ((Fgfu-Ggang) /2+Ftz(i)));
Ftx (i+1)=Fshui2 (i)+Ftx (i);
Fty (i+1)=Fty (i);
Ftz (i+1)=Fgfu-Ggang+Ftz (i);
end
gs .6fez 2 .6
Vt=1*pi*0.15%2;% 0f°Ta»y
Vq=mq/7800; $081iCoTa»y
Gt=100%g;%.01°%; 00C 玉 |
Gq=mqxgjsOoTiCooc 玉 |
Ftfu=rou*g*Vt;$ .Of”.i 玉 |
Fgfu=rou*g*Vq; 300A|Co, jA|
Fshui3=0+374* (vshui/gdH"2* (gdH-h-4.5)"2) ~2*1%0.3; SB+EUEGA |
HAO 下
gama3=atan (Fty(5)/ (Fshui3/2+Ftx (5)));
36

<!-- source_page: 37 -->

Ftp=Ftx (5) *cos (gama3) +Fty (5) *sin (gama3) ;
beta=atan ((Ftp+Fshui3/2*cos (gama3))/ ((Ftfu-Gt) /2+Ftz (5)));
Ft2x(1)=Fshui3+Ftx(5);
Ft2y(1)=Fty(5);
Ft2z (1)=Ftfu-Gt+Ftz (5) +Fgfu-Gqg;
$A2A 2; -0
roum=6450; $A*A AUJE
Vm=mm/roum; $A*A 14»y
Fmfu=rou*g*Vm; $A*A"  [A|
Gm=mm*qg; $A*A OgA|
Fshuid=zeros (1,n); $E+EUE®A ID 人 GO 下
for i=1:n
Fshuid (i)=0; SE+EUE®A | nA»00OE
gama4 (i)=atan (Ft2y (i) / (Fshuid (i) /2+Ft2x(i)));
Ftp=Ft2x(i) *cos (gama4 (i)) +Ft2y (i) *sin(gamad (i)) ;
thita2 (i)=atan ((Ftp+Fshuid (i)*cos (gama4 (i))/2)/((Fmfu-Gm) /2+Ft2z(i)));
if thita2(i)<0
thita2 (i)=thita2(i)+pi;
end
Ft2x (i+1l)=Fshuid (1) +Ft2x (1i);
Ft2y(i+1)=Ft2y (i);
Ft2z (i+1) =Fmfu-Gm+Ft2z (i);
H=h+sum (cos (thital))+cos (beta) +Lm*sum (cos (thita2)) ; $aEa0» 个
if Ft2z (i+1)<Gm/2;
break;
end
end
if i<n&sabs (gdH-H)<min
minh=h;
min=abs (gdH-H) ;
minH=H;
minthital=thital;
minthita2=thita2;
minbeta=beta;
end
end
r=Lm*sum(sin (minthita2))+sin (minbeta)+sum(sin(minthital));
end
37

<!-- source_page: 38 -->

附录 八 第 三 问 优化 设计
mlcdq=[0.078 0.105 0.12 0.15 0.18];
mlz1=[0.078*3.2 0.105*7 0.12*12.5 0.15%¥19.5 0.18*28.12];
kx1=[];
kxn=[];
kxmg=[];
kxh=[];
kxbeta=[];
kxt=[1;
kxn=[];
zfenshu=[1];
kxthita2=[];
for 1=1:5
Im=mlcd(1) ;
mm=mlzl(1);
for n=100:20:280
n
for mg=2000:50:4500
v=36;% cEU
vshui=1.5; $E@A+EUIE
gdH=20;%'@] AoE *EigE
alpha=0;% -gLOOEE®A+TOnAYDYC
min=inf;
minh=0;
minH=0;
minbeta=0;
minthital=zeros(1,4);
minthita2=zeros(1,n)+pi/2;
mingama2=zeros (1,4);
mingama3=0;
mingamad=zeros(1,n);
for h=0:0.01:2
Ftx=zeros(1,5);% 0'0U%; -OpA +A-A|pAx ORAL
Fty=zeros(1,5);% 0'0?; -OpA +A-A|pAy .ORAL
Ftz=zeros(1,5);% 0'0U?; -OpA +A-A|pAz ORAL
thital=zeros(1,4);% .= .Gin %T00&20anAkbhC
gama2=zeros (1,4);%. + 0'U sI160UXOYEITT0°0&x0apAdLC
beta=0;%,01°pA 1100820apAtdsC
gama3=0;% 0I° 160UX0YEIIT0° 0&x0apAbisC
Ft2x=zeros (l,n);%A%*A"2; -OpA +A-A|pAx OA
Ft2y=zeros(l,n);%A%A"2; -OpA +A-A|pAY GO
38

<!-- source_page: 39 -->

FLt2z=Zzeros (1l,n);%A%A"2; -OpA +A-A|pAz -OA;
thita2=zeros (1,n);%A%A"  +A L0pA .To08ZOahAMDIC
gamad=zeros (1,n); 3A%A"  +A %0 51600X0YET T90°08XOanAMDIC
当 . ite2z
S=2* (2-h) ;
m=1000;%, j+&0RA;
rou=1025; %°£E@AUIE
9=9.8; 200A MOR09E
V=pi*172%h;%°0E@1a»y
Ffeng=0.625*S*v"2;% ‘cA|
Ffu=rou*g*V;% jA!
Gfu=m*qg; %  +&00A;
Fshui=374* (vshui/gdH"2* (gdH-h) ~2) *2*2*h; YE+EUEGA | pA»GOE
if Ffu-Gfu<0
continue;
end
Ftx (1) =Fshui+Ffeng*cos (alpha);
Fty(l)=Ffeng*sin(alpha);
Ftz (1)=Ffu-Gfu;
%.6102¢46
Vg=1*pi*0.025%2;% 0'Uta»y
Ggang=10*g;% O'UOGA
Fgfu=rou*g*vg;
Fshui2=[374* (vshui/gdH"2* (gdH-h=-0.5) ~2) *2*1*0.05,374* (vshui/gdH"2* (H-h-1.5)
^2)^2x1lx0.05,374x* (vshui/gdH 2* (H-h-2.5) ~2) ~2*1%0.05,374* (vshui/gdH"2* (gdH-h
-3.5)"2)~2*%1%0.05]; SB+EUEGA | nA»aOE
for i=1:4
gama2 (i)=atan (Fty(i)/(Fshui2 (i) /2+Ftx(i)));
Ftp=Ftx (1) *cos (gama2 (i)) +Fty (i) *sin(gama2 (i)) ;
thital (i)=atan ((Ftp+Fshui2 (i)*cos(gama2(i)))/ ((Fgfu-Ggang) /2+Ftz(i)));
Ftx (i+1)=Fshui2 (1)+Ftx(1);
Fty (i+1)=Fty(i);
Ftz (i+1)=Fgfu-Ggang+Ftz (i);
end
g .6fe> 2 .6
Vt=1*pi*0.15%2;% 0f°Ta»y
Vq=mq/7800; 3081iCoTa»y
39

<!-- source_page: 40 -->

Gt=100%g;%.01°2; 00C 玉 |
Gq=mqxgjsGOTiTCoOC 玉 |
FLtfu=rouxgxVt;s .Of i 五 |
Fgfu=rou*g*vq; 300A|Co, jA!
Fshui3=0+374* (vshui/gdH"2* (gdH-h-4.5)"2) ~2*1%0.3; SE+EUEGA |
pA»aOE
gama3=atan (Fty(5)/ (Fshui3/2+Ftx(5)));
Ftp=Ftx(5) *cos (gama3) +Fty (5) *sin (gama3) ;
beta=atan ( (Ftp+Fshui3/2*cos (gama3))/ ((Ftfu-Gt) /2+Ftz (5)));
Ft2x(1)=Fshui3+Ftx (5);
Ft2y(1)=Fty(5);
Ft2z (1)=Ftfu-Gt+Ftz (5) +Fqfu-Gq;
$A2A 2;-0
roum=6450; $A%A AUIE
Vm=mm/roum; $A%A Ta»y
Fmfu=rou*g*vm; $AA" [A|
Gm=mm*q; $A*A OgA;
Fshuid=zeros(l,n); SE+EUE®A | nA»U0E
for i=1:n
Fshuid (i)=0; SE+EUE®A | pA»GOE
gama4 (i)=atan (Ft2y(i)/ (Fshuid (i) /2+Ft2x(i)));
Ftp=Ft2x(i) *cos (gama4 (i))+Ft2y(i) *sin(gamad (i));
thita2 (i)=atan ((Ftp+Fshuid (i)*cos (gama4 (i))/2)/ ((Fmfu-Gm) /2+Ft2z(i)));
if thita2(i)<0
thita2 (i)=thita2(i)+pi;
end
Ft2x (i+1)=Fshuid (i) +Ft2x(1);
Ft2y (i+1)=Ft2y (i);
Ft2z (i+1) =Fmfu-Gm+Ft2z (1);
end
H=h+sum (cos (thital))+cos (beta) +Lm*sum(cos (thita2));% BIEpAkata
if abs (H-gdH)<min
minh=h;
min=abs (H-gdH) ;
minH=H;
40

<!-- source_page: 41 -->

minthital=thital;
minthita2=thita2;
minbeta=beta;
minFt2=Ft2;
end
end
if minthita2 (n)>pi/2%ADJIEC .让 ¥ux
[r,minh,minbeta,minthital,minthita2,mind]=tuodir2 (n,mq, v,vshui,gdH);
else
r=Lm*sum(sin(minthita2))+sin(minbeta)+sum(sin(minthital));
end
if minbeta*180/pi>5% 01°CakC?»*~1y59R
continue;
end
if (90-minthita2(n)*180/pi)>16%A0IEAA  OE°L  2LDYC2» ~1y169R
continue;
end
if abs (minH-gdH)>0.2
continue;
end
a=36/pi;b=1.5;c=1/20;
fenshu=a*minbetatb*minh+c*r;
kxn=[kxn n];
Kxmaq= [kxma mq] ;
kx1=[kx1l 1];
kxh=[kxh minh];
kxbeta=[kxbeta minbeta];
kxr=[kxr r];
zfenshu=[zfenshu fenshu];
end
end
end
[fenshu, i]=max (-zfenshu) ;
fenshu
kxma (1)
kxl(1)
kxn (1)
附录 9 第 三 问 不 同情 况 分 析 计 算
v=12;% cEU
vshui=1.5; $E®A-EUIE
41

<!-- source_page: 42 -->

gdH=20;%'2] ph°L *EiqE

mm=0.18%28.12;%A*A OEA;

Lm=0.18;%A%A *nJE

mq=2950; $00T1iCOORA,

n=180;%AA" 0la 6By

alpha=0;% 'cIoO8E®A+TopAMDYC

min=inf;

minh=0;

minH=0;

minbeta=0;

minthital=zeros(1,4);

minthita2=zeros(1,n)+pi/2;

mingama2=zeros(1,4);

mingama3=0;

mingamad=zeros(l,n);

for h=0:0.0001:2
Ftx=zeros (1,5);%,0'0%; -OpA, +A-A|pAX ORAL
Fty=zeros (1,5);%,0'0%; -OpA, +A-A|pAyY .ORAL
Ftz=zeros (1,5);%,0'0%; -OpA, +A-A|pAz OAE
thital=zeros(1,4);%. + 0!Upk io08z0apidhC
gama2=zeros (1,4);% ,+ 0'0 %I600X0YALT90°08X0apAMDYC
beta=0;%,0f °pi 4:1308 20apADYC
gama3=0;%, 01° -LT60UXOYETT96° 0ex0apAkDLC
Ft2x=zeros (1,n) ;&A%A"2; -OpA +A-A|nAxX -OAg
Ft2y=zeros (1,n);%$A*A"?; -OpA +A-A|pAyY .OA
Ft2z=zeros(l,n);%A*A"?; -OpA +A-A|pAzZ OA
thita2=zeros (1,n);2A%A" +A 20pi T608204nAMDYC
gamad=zeros (1,n);%A%A"  +A 40 I600X0YET 196°08xXOANAMDIC
当 .i+e22 0
S=2x* (2-h) 7
m=1000;%, ;+60RA;
rou=1025; %$°£EQAUIE
g=9.8; $0gA | WOEUIE
V=pi*172%h;%°0E@Ia»y
Ffeng=0.625*S*v~2;% ‘cA|
Ffu=rou*g*v;%, {A]
Gfu=m*qg;% it+eOC 玉 |

Fshui=374* (vshui/gdH^2x (gdH-h)^2)^2x2xhy SE+EUE@A | pA»UOE
if Ffu-Gfu<0
continue;
42

<!-- source_page: 43 -->

end
Ftx (1)=Fshui+Ffeng*cos (alpha) ;
Fty(l)=Ffeng*sin(alpha);
Ftz (1)=Ffu-Gfu;
gs 0102¢ 6
Vg=1*pi*0.025%2;% O1UTa»y
Ggang=10*g;%, O'UOGA|
Fgfu=rou*g*vg;
Fshui2=[374* (vshui/gdH"2* (gdH-h-0.5)~2) ~2*1%0.05, 374* (vshui/gdH"2* (gdH-h-1.
5)^2)^2x*lx0.05,374x (vshui/gdH 2* (gdH-h-2.5) 2) *2*1%0.05, 374* (vshui/gdH 2* (g
dH-h-3.5)"2)"2*1%0.05] ; SE+EUEGA | pA»a0E
for i=1:4
gama2 (i)=atan (Fty(i)/ (Fshui2 (i)/2+Ftx(i)));
Ftp=Ftx (i) *cos (gama2 (i))+Fty (i) *sin (gama2 (i)) ;
thital (i)=atan ((Ftp+Fshui2 (i)*cos(gama2(i)))/ ((Fgfu-Ggang) /2+Ftz (i)));
Ftx (i+1)=Fshui2 (i)+Ftx (i);
Fty (i+1)=Fty (i);
Ftz (i+1)=Fgfu-Ggang+Ftz (i);
end
gs .6fe2 2 36
Vt=1*pi*0.15%2;% 0T°Ta»y
Va=mq/7800; 5001iCota»y
Gt=100%g;3%,01°%; -00gA!
Gg=mq*g; $00T1Co0TA |
Ftfu=rou*g*Vt;$ Of° A;
Fgfu=rou*g*Vq; 300A|Co, jA|
Fshui3=0+374* (vshui/gdH"2* (gdH-h-4.5)"2) ~2*1%0.3; SE+EURGA|
HAO 下
gama3=atan (Fty(5)/ (Fshui3/2+Ftx (5)));
Ftp=Ftx (5) *cos (gama3) +Fty (5) *sin (gama3) ;
beta=atan ( (Ftp+Fshui3/2*cos (gama3))/ ((Ftfu-Gt) /2+Ftz(5)));
Ft2x (1)=Fshui3+Ftx(5);
Ft2y(1)=Fty(5);
Ft2z (1) =Ftfu-Gt+Ftz (5) +Fqfu-Ggq;
Sa 六 2。 -0
roum=6450; $A%A AUIE
43

<!-- source_page: 44 -->

Vm=mm/roum; $A*A 14»y
Fmfu=rou*g*Vm; $A*A"  [A|
Gm=mm*qg; $A*A OgA|
Fshuid=zeros (1,n); $E+EUE®A ID 人 GO 下
for i=1:n
Fshuid (i)=0; SE+EUE®A | nA»00OE
gama4 (i)=atan (Ft2y (i) / (Fshuid (i) /2+Ft2x(i)));
Ftp=Ft2x(i) *cos (gama4 (i)) +Ft2y (i) *sin(gama4d (i));
thita2 (i)=atan ((Ftp+Fshuid (i)*cos (gama4 (i))/2)/ ((Fmfu-Gm)/2+Ft2z(i)));
if thita2(i)<0
thita2 (i)=thita2(i)+pi;
end
Ft2x (i+1l)=Fshuid (1) +Ft2x(1i);
Ft2y (i+1)=Ft2y (i);
Ft2z (i+1)=Fmfu-Gm+Ft2z (i);
end
H=h+sum(cos (thital)) +cos (beta) +Lm*sum (cos (thita2));% BIEpAzaEa
if abs (H-gdH)<min
minh=h;
min=abs (H-gdH) ;
minH=H;
minthital=thital;
minthita2=thita2;
minbeta=beta;
minFt2=Ft2;
end
end
minbeta*180/pi
minh
r=Lm*sum(sin (minthita2))+sin (minbeta)+sum(sin (minthital))
44

