# Extracted Paper

<!-- source_page: 1 -->

mg
faz |，

汽车 总 装 线 配 置 的 优化 模型 研究
摘
生产 具有 品牌

要

、 配 置 、 动 力 、 驱 动 、 颜 色 等 属性 的 多 种 型 号 的 汽车 ， 对 总

装

线 和 喷涂 线 上 的 装配 顺序 各 项 提出 了 各 种 不 同形 式 的 要 求 ， 而 且 不 同 的 装配

顺序

造成 的 生产

出 符合 生产 要

成 本 也 不 尽 相同 。 本 文 主要 通过 建立 数学 模型
求 、 且 具有 较 低 生产

首先
是 数据 处 理 ， 使 用 python
读 取 的 规范形式
动 形成 相互

将 原 附件 数据 中 的 生产 计划 整理 成 方便 数据
日 的 装配 顺序 ， 5

校 验 ， 保 证 装配 顺序 的 准确 性 ;

先 将 黑色 的 汽车

油 汽车 等 关键

=

“W

线 和 喷涂 线 的 各 项 要 求 ， ocean

手工 填 入 装配 顺序 表 。 在 确定 一 些 视 便 庆

求解
的 搜索 规模 后 ， 建 立 生产

然后

成 本 的 装配 顺序 。

， 设 计 Excel 表格 存储 每

接着 ， 通 过 分 析 总 装

并 设计 算法 ， 给

Jh

\ 装 配 顺 序 问 题

成 本 最 小 优化 模 到

Fih 用 计算
机 搜索 四 驱 、 柴

等 可 以 连续 排列 的

颜色 ， 此 时 注意 蓝 色 汽 车 只 能 与

属性 汽车 的 位 置 ;

， 配 置 白 色 和 棕色

白色 间隔 等 关键 要 求 ， 尽 可 能 多 地 将 这 些 汽车 连续 地 填 入 装配 顺序 表 ;
最 后 ， Re
未 分 配 的 、 颜色

成 分 复杂 的 汽 二

8

是

对 应 着 剩余 尚
本 符合

在 总 闭 线 上 排列 时 的 具体

要 求 ， To
图 ， 装 配 顺序 的 己 题 转化

成 了 图 的 遍历 问题

构成
了一 个有向
。 使 用 基于 遗传 算法 的 TSP 问题 和

广 和
验证 各

的 特殊 颜色 能 否 按 顺序 分 配 在 指定 的 C1

从 same
h)

采用 Matlab

并 且 取 代价 最 小 的 路 径 填 入 装配 顺序 表 。

Eon——————

有

或 C2 喷涂线 上 ， 计 算

综合 利用 多 种 计算 机

工具 ， 在 计算

人 工 经 验 介入 、 计 算 过 程 衔接 方面 取得 了 较 好 效果 。

关键 词 : 汽车 装配 顺序

优化 模型

邻接 矩阵

1

路 径 搜 索

遗传 算法 TSP 问题

%

<!-- source_page: 2 -->

加5
嫩

1， 问
题的重述
某 汽 车 公司 生产 以 下 型 号 的 汽车 ， 每 种 型 号 由 品牌 、 配 置 、 动 力 、 驱动 、
颜色
5 种 属性 确定 。 品
牌 分 为 AL 和 A2 两 种 ， 配 置 分 为 B1、B2、B3、B4、B5
和 B6 六 种 ， 动 力 分 为 汽油 和 柴油 2 种 ， 驱 动 分 为 两 驱 和 四 驱 2 种 ， 颜色 分 为
黑 、 白 、 蓝 、黄 、红 、 银 、 棕 、 灰 、 金 9 种 。
公司 每 天 可 装配 各 种 型 号 的 汽车 460 辆 ， 其 中 白班 、 晚 班 (每 班 12 小 时 )
各 230辆 。 每 天 生产 各 种 型 号 车 辆 的 具体 数量 根据 市 场 需求 和 销售 情况 确定 。
待 装配 车 辆 按 一 定 顺序 排 成 一 列 ， 首先 匀速 道 过 总 装 线 依次 进行 总 帮 作 业 , 了
后
按 序 分 为 C1、C2 线 进行 喷涂 作业 。
Lp
“让
erToRWonISigEEIRIHNI 和 ni
作业 对 经 过 生产 线 车 辆 型 号 有 多 种 要 求 。
X
1.1 装配要 求

4s

1. 4ER EERIMIEAR
REI AlJ A2 Gih. 装配 当天 两 种 品牌
各 一 半数 量 的 汽车 。
杀
2. 四 驱 汽车 和 柴油 汽车 连续 装配 数量 不 得 超过 2 辆 ， 并 且 两 批 之 间 间 隔 的
汽车
的 数量 至 少 是 10 辆 。 er
仍 希 望 间隔 数量 越 多 越
好 。 问 量 数量 在 5. 辆 仍 是 可 以 各 入 的 ， 但 代价很 高。
3. 时 外 过 外 抽 本 50-70
辆 之 间 ， 两 批 黑色 汽车 在 总 装 线 上 需
间隔 至 少 20 辆 。
4 蓝本 线 和
凶 问 二 需要 清 足 一 定 的 规则

过

5 荐 SS、 红 三 种 颜色 汽车 的 喷涂 只 能 在 C1 线 上 进行 ， 金 色 汽车
的 喷涂
并 Sa
. 喷涂 线 上 不 同 颜色 汽车 之 间 的 切换 次 数 尽 可 能 少 ， 黑 色 汽车
与 其 它 颜色
的 汽车 之 间 的 切换 代价 很 高。
1. 3 需要 解决 的 问题

1. 建立 数学 模型 或 者 设计 算法 ， 使 其 能 给 出 符合 要 求 、 是 具有 较 低 生 产 成
本 的 装配 顺序 。
2. 给出 9 月 17 日至 9 月 23 日 每 天 的 装配 顺序 。
2

昌

<!-- source_page: 3 -->

加5
EEEE

2， 问
题 的 假设
1. 生产

题目 中 所 指 的 装配 线 上 不 同 汽车 配置 切换

、喷 涂 线 上 不

同 汽车 颜色 的 切换 构成 。 汽 车 配置 切换 和 普通 的 颜色 切换 代价 设

为 1， 黑色 切

换

成本 只 是 由

为 其 他 颜色 成 本 耗费 较
2.

高 ， 设 为 10。

在 无 法 满足 柴油 、 四 驱 汽车 的 批 次 间隔 k 至 少 是 10 的 情况

必须 大 于 5，
3.9 月 23

而 且 间隔
日 Al

下 ， 间隔 k

越 小 代价 越 高 ， 设 为 10-k。

和 A2 品牌 数量 为 奇数 ， 在 尽 可 能 均衡 的 情况

班 和 晚 班 装配 的 汽车 数量 相差 1 辆 。

下 ， 人 允许 白

-从 >

4. 在 考虑 不 同 工 作 日 的 装配 顺序 时 ， 总 装 线 和 师 涂 线 的 各 项 要 浇 厅 当日 晚
班

与 次 日 白班 交接 同样 适用 。

发 盖

5. At—

~

3. “人
符号

人
含义

I

Al 品 竹下 标 爸 多 y/ 0120,F11 = {1,- 181,231,

了

A2 AL

x

on

否则 xx = 0，EEITUJ

3

和

=1， 否则 me = 0,， kelUJ

ps
多

是 柴油 车 zx = 1， 否则 zx = 0，k ETUTJ

WRN

4，

411}

20 日 | = {182,…230,412,…,460}

问 题 的 分 析 与 数据 处 理

4.1 问题
的 分析
题目 所 要 解决 的 最 终 问题 是 每 天 460 个 汽车 装配 的 顺序
行 解 的 问题规模

，460 的 阶乘
是 一 个 1027 位

建立
通用 的 数学 模型

，初

步估 算 寻 求 可

数 。 即 使 可 以 设计 精巧

的 约束 条 件

， 但 在 使 用 计算 机 搜索 可 行 解 时 可 能 会 遇 到 无 法 及 时 给 出

答案
的 问题 。
3

<!-- source_page: 4 -->

加 5
籁

通过
分 析 9 月 17 日至 9 月 23 日 每 天 的 生产 计划 可 以 发 现 ， 所 产 汽车的 颜
色 可 以 分 为 黑色 、 和 白色
与 棕色 、 其 他 数量 较 少 的 颜色 等 三 种 情况 。 根 据 总 装 线
和 喷涂 线 的 各 项 要 求 ， 这 几 种 颜色 的 汽车 有 着 如 下 的 不 同 特征 ;
。 ”黑色 汽车 需要 连续 生产 ， 尽 量 不 要 与 其 他 颜色 切换

， 除 非 付出 较 高 代

价 切换
成 其 他 颜色
。

和 白色、

银色 、 灰 色 或 棕色 可 以 连续 排列 且 有 时 数量

较 多 ， 特 别 是 棕色

可 以 与 许多 的 其 他 颜色 切换
。 ”其 他 颜色 数量

较 少 ， 却 有 复杂 的 切换 规则

-

根据
以 上 特征 ， 尝 试 以 下 逐步 按 顺 序 求解 的 过 程

-从 >

首先 ， 手 动 排 黑 色 汽车 的 装配 位 置 ， Rs
车 ， 在 确定
一 些 初 值 后 ， 再 使 用 计算 机 搜索 四 驱 、 柴 油 汽
性 汽车

的位 置 ;

人

om

x

接着

， 配 置 白色 和 棕色 等 可 以 连续 排列 的 颜

白色 间隔 ;

和

保

注意
蓝 色 汽车 只 能 与

最 后 ， 剩 余 未 确定 配置 顺序 的 颜色 数量 较 少 ， 并 且 因 为 以 上 两 步 都 是 连续
排列 的 ， Sial,
接 搜索 可 能 的 顺序 。

v A

可 以 使 用 计算机 直

%,

4. 2 数据处 理
wm
据 整理 。
phone

向

秆 Fat

JY
和 wa

Ce

xlrd 可 以 方便 快捷 地 读 写 、 操
纵 excel 单元 格 ， 将

Coreeogpe

悍 序 文件 名 “problem_D_Datapy”，
人

需要 设计 合适 的 表格 对 数

python

中 和
有具体
见 附件 1-2。

让
设 计 有 关 表格

整理 得 到 的 生产 计划 表 〈 数 据 文件夹 中 excel 文件

“schedule
.xlsx" 的 "sheetl" 表 单 ) ， 列 举 了 每 日 所 有 不 同 种 类 汽车 的 生产 数量 ，
添加 的 最 后 一 列 “ 装 配 剩余 "使 用 以 下 公式 ， 统 计 还 没 安排 装配 顺序 的 剩余 汽车
数量

(以 9 月 17 日 为 例 ) 。
H2=G2-COUNTIFS('9.17'1A:A，sheet1!A2，'9.17'1C:C，sheet1!B2，'9.17'1D:D，
sheet1!C2,'9.17'1E:E，sheet1!D2，'9.17'!F:F，sheet1!1E2，'9.17'1G:G,sheet1!F2)
4

是

<!-- source_page: 5 -->

IE 辣

|

EEEEE

表 1 生产 计划 表
A

B

C

D

E

F

G

mBl

sE

H

2

1 Em|

2018/9/17 |

mer

mEl

wan

we.

3

2018/9/17

Al

B3

汽油

四 驱

白

4

0

4

2018/9/17

Al

B1

汽油

四 驱

黑

3

0

5

2018/9/17

Al

B2

汽油

四 驱

黑

1

0

6

2018/9/17

Al

B3

汽油

四 驱

黑

6

0

了 | 2018/9/17

Al

B1

汽油

四 驱

灰

2

0

8

2018/9/17

Al

B1

汽油

两 驱

白

109

0

9

2018/9/17

Al

B2

汽油

两 驱

白

27

0

10

2018/9/17

Al

B5

汽油

两 驱

白

3

0

11

2018/9/17

Al

B1

汽油

两 驱

黑

101

0

12|

2018/9/17

Al

B2

汽油

两 驱

黑

75

0

13 | 2018/9/17

Al

B3

汽油

两 驱

黑

2

0

Al

B1

14 20189/17 | Al
15 2018/9017 | Al
16 2018/9017 | An
17

2018/9/17

BS
81
上2

Al

四 驱

汽油

B2
81
B2

两 驱

， 汽 由 。 PE
汽由
RE
mm
PE

21 | 2018/93/17

Al

B1

汽油

两 驱

22

2018/93/17

Al

B1

汽油

两 驱 人

23 | 2018/3/17

Al

B2

汽油

两 驱 N

24 | 20180/17 | A1

B3

汽油

25 | 2018/93/17

Al

B5

26

2018/3/17

A2

B1

27 | 2018/9/17

A2

B1

on

28

2018/3/17

A2

w

FF 油

29

2018/3/17

A2

B4

认得

JJ

表 2 是 9 月 17 |
表单 ， 其 他 日 期 的 表单 类 似

白

， 污 由 。 PE
汽 由 。 KE
FF
PE

B1

18 20189/17 | Al
19 20188017 | Al
20 2018/917
Al

汽油

2

B
4
红
=

， 黄
®
， 灰

2
2
1

Jo
°

4

Ya4=

六
醒

了

ANY

、

》}

0

0

0
0

4

0

银

1

0

两 驱

区

1

0

汽油

两 驱

银

1

0

汽油

四 驱

白

2

0

黑

9

0

四 驱

黑

1

0

两 驱

白

3

0

-

7

|

3

_

蔓

和 |

[[o |

(数据 文件 夹 中 excel 文件 schedulexlse
的 9.17"
】， 在 喷涂 线 后 添加 了 "装配 代价

“喷涂 代价 “~“ 其

他 代价 ”总 代 便于 7 到 术 验 "、 ,喷涂
校对 "等 列 ， 对 应 公式 和 作用 如 下
. EAAR

统计 同一

品牌 下 ， 装 配 线 上 不 同 汽车 配置 切换 代价

Mrs=IF(Cssc4,1,6)*ITF(D5<>D4,1,9)

SEE

涂 代 价 : 统计 喷涂 线 上 的 颜色 切换 代价 ， 其 中 黑色 切换 为 10

js=TF(G3-" 黑 "16,1)*TF(G5<y63,1,6)

。

”其
他 代价 ; 柴油 和 四 驱 汽 车 的 批 次 间隔 k 小 于 10， 代 价 为 10-k

特殊 情况

*。

总 代价 : 累计
以 上 三 种 代价

L2=SUMIF(A:A,A2,I:I)+SUMIF(A:A,A2,]:])+SUMIF(A:A,A2,K:K)

5

<!-- source_page: 6 -->

回味
p
S
TE

EEE
sa

*。

装配

校对 : 校对 装配 顺序 中 的 配置 是 否 是 出 现在 计划 表 中 的 有 效 配置

05=COUNTIFS(sheet1!A:A, '9.17'!A5,sheet1!B:B,'9.17'!C5,sheet1!C:C,'9.17'1D5,shee
t11D:D, '9.17'!E5,sheet1!E:E,'9.17'!F5,sheet1!F:F，'9.17'165)

。 ”喷涂

校对 : 校对 装配 顺序 上 的 汽车 是 否 交 蔡 分 配 到 喷涂 线 C1 和 C2上

P5=IF (H5=H3,1,0)
A

ec

pb

卓 其 |]
甘 宙 网 - | 辟竹 -| RE-|
2018/9/17

E

#2 9 月 17 日 的 装配 顺序
F
Ge
au

0

动 放 - | 更动 =|， 颜 人 -| Eek-| 凌 机 他 -| 顺治 人 | -| 其 他 人 -| 总 代价 | ~ | 装配 优 - 话 8 校 对

zaear7

2

1

AT

B1

汽 泪

四 驳

黑

E

o0

2018/9/17

3

AT

B1

汽油

两 区

2

c2

D

0

1

1

2018/9/17

4

A1

B1

汽 泪

两 欧

=

C1

D

0

1

1

AN

AP

[3

1

2018/9/17

5

A1

B1

RE

两 驱

=

c2

1

0

ap

1

2018/9/17

6

AT

B1

汽油

两 区

2

C1

D

0

1

1

2018/9017

了

AT

B1

E

PE

=

C2

1

0

2018/9/17

9

AT

B1

汽油

两 中

=2

c2

D

0

2018/9/17

za

10

TAN

AT

B1

ha:d

FE

2

CI1

0

0

2018/9/17

12

AT

B1

汽油

两 中

=2

2018/9/17

13

AT

B2

ha:d

四 驱

2

2018/9/17

15

AT

B1

汽油

两 中

=2

2018/9/17

28917

8

AT

AT

时

站

PE

FE

要

CI

EC

FE

mm

E

0

a

0

J

av
>

=

1

1

0

o

C1

D

0

c2

0

0

1

1

c2

D

0

1

1

CO0

o

1

¥

1

1

1

2018/9/17

16

AT

B1

ha:d

FE

2

CI1

0

0

1

1

2018/9/17

17

A1

B1

汽油

两 跑

2

c2

1

0

1

1

2018/9/17

18

AT

B1

汽油

两 中

=2

C1

2018/3/17

19

Al

B1

汽油

两 区

E

C2

2018/9/17

20

A1

B1

汽油

两 跑

2

[s]

2018/9/17

”21

AT

B1

汽油

FR

2

c2

2018/3/17

22

Al

B1

汽油

两 区

E

C1

2018/9/17

23

A1

B1

汽油

两 跑

2

2018/9/17

24

AT

B1

汽油

FR

2018/3/17

25

Al

B3

汽油

2018/9/17

26

A1

B3

汽油

2

Ab

2018/917
2z018/307

27
28

2018/917
z018/3117

30
31

A1
和

33

AT

aao7

zasa7

2018/9/17

018917

018/9

A1
Al

2

AN

3

ANa

BT
6

汽由
FA

1

1

1

1

0

1

1

0

1

1

0

0

1

1

c2

D

0

1

1

2

C1

D

0

1

1

四 驱。

=

“e

0

0

1

1

中

/

&

D

0

1

PN

是
芭

C2
c

BT qisE
Be 二

PE
_PEw

2
=

B1

PE

2

8

Ta

请 二】

六十

KE

cc

CT
=

人
-

0

ct
[=3

[J
1

0
10

1
1

1
1

c

0

0

1

1

D
®

6

1

0

[Gl

0

JRV A
——
[ speett | 917K] ag ga1o | 920 | 521 [ 922 [93 |
2)

1

0
0

0

10
1

1
1

1
1

1

1
1

1

1

1

v

上 AL
未 役 诗 侈 表格 在 整理 ， 装配 情况， 、 手 工 介入 搜索 、 导 入 、 计算 结果 、 过 程 中 发、

全 时作
RN

TSA，

N

5，

模

型 的 建立 与 问题 的 求解
——

KS

5.1 生产
成 本 优化 模型
根据 上 一 节 中 的 问题

分 析 ， 建 立 如 下 有 关 四 驱 、 柴 油 汽车 装配 问题 约束 。

6

<!-- source_page: 7 -->

回味
站 二二
1. 各 类 汽车 数量 约束

做 表 示 装 配 顺 序 是否 是 四 驱 汽车 ， 则 以 下 公式 分 别 表示
Al 黑色 四 驱 :， xy ，
A2 黑色四 了 驱 :
xy ，
Al 非 黑色四 驱 : 习 (L - zw，

A2 非 黑色四 驱 : 立 (4 -xy ，

(1)

了 天 表示 装配 顺序 上 是 否 是 柴油 动力 汽车 ， 则 以 下 公式 分 别 表示
Al 柴油 汽车 ; 对 = ，
A2 柴油 汽车 Y > ，
Al 黑色 柴油 汽车 : Y xz,

A2 黑色 柴油汽车 : Y xz ， -从

iel

JE 了

Al 柴油 四 驱 : 六 yz ，

)

GE

A2 柴油四 驱 : Y 2

2， 柴 油 和 四 驱 汽 车 连续 排列 不 能 超过 两 个

人

如 果 罗 = 1 表示 装配 顺序 是 四 了 驱 汽 车 ， wd,

)
人 前 后 连续 3 个 取 值

的 和 来 约束 四 驱 汽车 连续 排列 不 能 超过 两 个 ,各 如 麻 w = 1， 们
NS

< 2，

t=k-1

人 = 2 …，459 ， 可 以 验证 其 等 价 于
大 十 1

(0]

人

(3)

同 理， 站

袜 人

-5
q

ss

k=2

…，459

(4)

一 1

3 柴 消 有 几 X 车 批 次 问 隔 约束
可 届 奉 用 和 ， 加 连续 取 值 的 和 表示 相 钙 批 次 的 四 驱 汽车 的 间隔 ， 如 下 表述
全 92% 10

短
N

S-y)210,

k =12, -, 460

(5)

同 理 ， 可 以 将 柴油 汽车 相 邻 批 次 的 间隔 不 少 于 10 表示 为
六 4

-2)

> 10，

大 =12,

了

---,

460

(6)

<!-- source_page: 8 -->

生

EEEE
4. 生产 成 本 最 小 的 目标 函数
如 果 无 法 满足 柴油 和 四 驱 汽 车 的 批 次 间隔 k 至 少 是 10 的 情况 下 ， 间
隔 k 必
须 大 于 5， 代价 为 10-k，

上 面 (5-6) 变 为

六 (4 ->5，

六 0- 2) >5， k=7

,460

(7)

此 时 ， 成 本 最 小 的 目标 函数 可 以 表示 为

san-$10由 上 述 (1-8)

a-)+s(0-

， 可 以 得 到 生产

2

(8)

成 本 最 小 的 优化 模型 如 下

-从 >

MIN= 浊 *(。 - Sa 一 中 | + :| - 2 了

ST

Al 黑色
四 驱 = xy
ie7

A2 oem
人
有

Al 非 黑 色 四 驱

A2 名

SN /

=(L- zx)y

Al 柴油 汽车 = =
@

钻 黑色 柴油 汽车 = 对 xz，

Al 和

A2 柴油
四 驱 = 允 yz，

yw

GTON

JE

Al OA

3- Sr

有

一 xy

A2 柴油 汽车
= 对 >，

iel

SN

3

7

\v*

y)25,

Wo

S

>z,

k=2 …，459

Y(U-z)25,

k=7 , 460

k

1=k-6

的 是 ， 上 述 模型

|

没有 约束 黑色 汽车 的 配置 顺序 和 成 本 ， 这 需要 手

并 且 注 意 优先 按 顺 序 排 入 相同 配置 的 汽车

。 使 用 数据 处 理 中 设计 的

Excel 表格 ， 尽 可 能 多 地 事先 按 顺 序 确定 各 类 汽车 配置 顺序 ， 然 后 将 初 值 带 入 上
述 生 产

成 本 优化 模型

进行 求解 ， 相 关 程 序 见 附件 -3， 结 合

手工 介入 的 调整 ， 可

以 得 到 如 图 1 所 示 的 9 月 17 日 -9 月 23 日 部 分 装配 顺序 ， 相 关 结 果 记 录 在

“schedulexlsx"
表 单 中。

8

<!-- source_page: 9 -->

可
ss

0

Bs

9 月 17 日
请
四 四

10 四 四

10 四 四

10 四 四 10 四 四

izies

12

四四

5

区可

50

mm

[

19

EEE

29

]

|四 四

EIE]

10 四 四

路 径 搜索

6

12

mm

L

o75

夯

9 月 18 日

=

o

记EER
»

%

®%

mEnmmwEs

[站 下

oo

EE]

aaiazmnai

EE])

ma

El

mm2

®%

¢ aa

[十

maila

村

5

SELLS

[|-一

此

夯|

柴

此

直上

让 | 二 二 吉本 | 基 | 相 as
柴

EEE

此

®

®

此

®

柴

路径

9

am
NCE

搜索 ®

更

Laaalyaaiaaniaaan

9 月 20 日
0

—

四 四

10

四

可

10

四 四

10

可

10

四

四

20

[(

50

mww

31

|

四

百

11

西10 丁 10 画 画 25

路 径 搜索

12

32

A

FA

口

vv

T

路 径 搜索

TI

50

机

机

柴

2

柴

a

本

[Ca
所

7

]

_

本

四

|

&

5

@®m

本

1

四 四

本

外

10 四

-

EE])

ms;
®

此

eaacaaus5

23

El

日

[EE

ww

m@iEscsscaasans

本

1

酝

13

15

四

2

丁酉 26

四

ET

[EEE ARRRH

路 径 搜索

站

|

EEEEEEEEEEEEEE

|

E

口

SEA

7

了

=

[ass
一 本
一 一
[SRRRRE
-一

荣 。 路径 搜 索 ” 深

ES

ES

ES

)Y

9 月 23 日

丁丁

|

HA

23 四 四 1 名品 证

9 月 22 日

E3E3

RSSRSRSRRRS

HN W]

2
|

Ze

PT
N
</
四 跨国 下 下

本

10 四 四

A\

9 月 21 日

训 西

12| 四 四

ilaaioaaioaam

[]

于

107

E

总

AK\
ASS

E 丘3

四 四 10
四 四

CLII |

\

全

可 Ba 本 alalalalalalalals
让
Xe
\

柴

4

Us<s<by

FT
Ta
T
Rn
”vrA

庆 后 局 吉 关 后 二 二 主导- 号
C
ww

四

二

小

[REEEREEREA光
TV

|

中

一
E3
E3E3
上

[LEEE IE3E3

|

ss
图 1 2018
年 9 月 17 日-9 月 23 日 部 分 装配 顺序 示意
9

[|
图可
以 放大

四 四

让

RERER

E3

FRRRRREER J N

W]

|

<!-- source_page: 10 -->

回 虽过

四

5. 2 路 径 搜索 模型
经 过 上 述

成 本 优化 模型

的 求解

， 如 图 1 所 示 ， 装 配 顺序 表 中 通常

只 含有 数

量 不 多 的 空余 位 置 ， 对 应 着 剩余 尚未 分 配 的 、 颜 色 成 分 复杂 的 汽车 ， 如下 表 3
所 示 ， 是 在 求解 9 月 20 日 的 装配 顺序 表
共有 14 量 ， 颜 色 和 配置

时 ， 最 后 剩余 品牌为 A2 的 部 分 汽车 ，

型 号 都 较为 复杂 。
表 3 9 月 20 日 未 安排 装配 顺序 的 汽车

2018/920
2018920
2018/9/20

A2
A2
A2
全

B1

汽油
汽油
汽油
间

2018/9/20

A2

B4

汽油

2018920
2018/920
2018/920

A2
A2
A2

Bl
BS

0
0
2|

Bi
两

驱

白

3

B6
Bl
B4

汽油
汽油
汽油

两 驱
两 驱
两 亚

a
黑
黑

1
36
1
次

ae
”总

2018/9/20

A2

BS

汽油

两 亚

黑

2018/9/20

A2

B6

汽油

两

驱

黑

2018/9/20

A2

B6

汽油

两

驱

2]

1

1

2018/9/20

A2

B1

汽油

两 驱

人 金

2

1

2018/920
2018920

2018920
2018/920
2018/920

A2
A2

Bl
B4

汽油
汽油

A2
A2
A2

B4
Bl
B4

汽油
汽油
汽油

2018/9/20
2018/9/20

A2
A2

B4
B4

汽油
汽油

2018/9/20

A2

B1

2018/920
2018/920

A2
A2

B6
Bl

ZZ

两 驱
两 驱

红
局

两 驱
两 驮
535

人 一

2
1

演

1
1
1

0
0
0
2
3

汽油
柴油

两

驱

iR
=3

两 更 轧 。 棕
两 蔓
a

2
5

1
1

1
0

柴油

两

驱

黑

3

0

以 这 14 辆 车 为 顶点 ， 按 照 闫 色 是 否 符合 在 总 装 线 上 排列 时 的 具体要 求 ， 将
顶点 相互 连接 起 来 。 Ne
构成

了 一 个 有 和 图。 此 本 必

1 Emegpen
用

惑

o

的 问题 转化 成 了 图 的 遍历 问题 。
0

程序 文件 名 为

- nu 具体
见 附件 -3。 以表 2 中 的 装配 问题为 例 ， 在 命令 窗口
中 输入

>>num=[1112111231];
>>config={'B1','B4','B6','B1','B4','B6','B1"',
'B4"', 'B4", 'B6"};

>>color={' 银 '， 自 "， 自 5 红 , 红 ' 红 ,5 e, R, R
>>Graph=genGraph(config, color,num)

A BT SRAGHCNUFT Xob S2 FET F &I5 BEAELRE d F

10

4

ER)

<!-- source_page: 11 -->

[OFe

区

o
表 4 按 归 颜 色 是 否 符合 在 总 装 线 上 排列 要 求生 成 的 图 的 信 捷 矩阵
图

日

Inf

Inf

1

1

1

1

1

1

1

Inf

Inf

Inf

Inf

B

Inf

8

工

Inf

Inf

Inf

Inf

Inf

Inf

Inf

工

工

1

1

=

Inf

1

9

Inf

Inf

Inf

Inf

Inf

Inf

Inf

1

1

1

1

园

1

Inf

Inf

8

Inf

Inf

Inf

1

1

1

1

1

1

1

加 |

1

Inf

Inf

Inf

日

Inf

Inf

工

工

1

1

1

1

1

园

1

Inf

Inf

Inf

Inf

日

Inf

1

1

1

1

1

1

1

图

1

Inf

Inf

Inf

Inf

Inf

8

1

1

1

1

1

1

1

s

1@0

Inf

Inf

1

1

1

1

o

10

10

10

10

10

10

=

1

Inf

Inf

1

1

1

1

1

日

1

Inf

Inf

Inf

Inf

l10

1

Inf

Inf

1

1

1

1

1

1

e

Inf

Inf

0

[]

Inf

1

1

1

1

1

1

1

Inf

Inf

日

1

回

Inf

1

1

1

1

1

1

1

Inf

Inf

1

1

[]

Inf

1

1

1

1

1

1

1

Inf

Inf

1

8

1

[2a

Inf

1

1

1

1

1

1

1

Inf

Inf

1

1

日

区
\

2， 基 于 遗传 算法 的 TSP 问题 求解
R 4s :
旅行
商 问题 ， 即 TSP 问题 rs problem) 又 称 旅行 推销 员
问题 、 货 郎 担 问 题 ， 是 研究 的 较为 充分 的 图 的 顶点 遍历 问题 04，

并 且 已 经 证 明

是
一 个 NPC 问题 。 将 现 有 基于 遗传 算法 的 TSP 求解 代码 馈 适 当 改写 为 Matlab
A

7

程序 “ga_TSP.m”， Te

得 到 如 下 结果 ， 有具体
见 附件 -

5。 通 常 ， 对 于 将 装配 顺序 问题

续 化 成 的 15 个 左右 顶点 的 有 向 图 ， 基 于 遗传 算

法 的 TSP 问题 求解 程序 人

000 代 以 内 收敛，

、

这

一

、

一 |

才 )

e

Xo

图 2 基于
坦 传 算法 的 TSP 问题 求解

11

_-

如 图 2 所 示 。

<!-- source_page: 12 -->

La
Erires
但 还 存在
以 下 问题 ， 一 是 如 图 2 所 示 ， 因 为 装配 顺序 问题
是 所 有 顶点
求解 失败

都 有 边 连接

的 ，TSP 问题

求解 过 程 不 太 稳

转化 的 有 向 图 不

定 ， 时 常会
出 现 迭代 之 后

， 没 有 通路
的 情况 ， 二 是 求解 TSP 问题 结果 得 到 只 是 一 条 路 径 ， 颜 色

和 配置 切换 造成

的 成 本 无 法 在 求解

序 分 配 在 指定 的 C1

3 广度
经

过 程 中 确定 ， 一 些 特定 颜色 无 法 保证 能 按 顺

或 C2 喷涂 线 上 。

优先 搜索 图 中 指定

起 点 和 终点 的 所 有 路 径

过 以 上 分 析 ， 转 化 得 到 的 有 向 图 的 边 并 不 是 太 多 ， 顶 点 规模
不 是 太 大，

可 以 考虑 搜索 图 中 指定

起 点 和 终点

序

具 体

文件 名 称 "findPath.m"，

的 所 有 路 径 。 采 用 广度 优先 搜索 算法 四 ， 程

见 附件-6。 以表 4 中 的 邻接 矩阵

为 例 ? HA 2

令 ， 得 到 满足 颜色 转化 要 求 ， 并 且 经 这 所 有 顶点 的 路 第 近 2 Hfo wEh

-

>>pathsAll
>>paths

=

= findpath(Graph，13，14，6);

三

f

TRERG TEE

ER

三 三 三 三 3 三 三 二三 |

了
一

所示 。

pathsAll(pathsAll(:,end-1)~=0,1:end-1

CTEE

国

下指

全

于

本

运

一

一

一

1

一

和
了

ye

i 谎

-

N

路 径 代价 计算

图 3 广度

-|

优先 搜索 图 中 指定

对 于 上 述 搜索 得 到 的 所 有 路

起 点 和 终点 的 所 有 路 径

径 ， 以下 采用

Matlab 验证 各 个 路 径 上 的 特殊 颜

色 能 否 按 顺序 分 配 在 指定 的 C1 或 C2 喷涂线 上 ， 计 算 各 种 路 径 上 切换 配置 和 颜
色
的 代价 ， 并 且 取 代价 最 小 的 路 径 填 入 装配 顺序 的 整个 过 程 中 去 ， 程

称 "pathsCostm"*， 具 体 见 附件-7。

12

序 文件 名

<!-- source_page: 13 -->

多

function

[minCost,opt_paths]=pathsCost(paths,config,color,num,c)

%paths:

需要 验证 的 所 有 路 径

%config: 汽车 配置
%color: 汽车 颜色

%num: 对 应 的 汽车数量
%c: 起 始点 处 的 喷涂 线 分 配
%miniCost:

最小 代价

%opt_paths:

最 小 代价 对 应 的 所 有 最 优 路 径

在 命令 窗口 中 输入 指令
>>

[minCost,opt_paths]=pathsCost(paths,config,color,num,c);

>> minCost

*
全

和

ef/

<

最 终 算得共有 16 条 代价 最 小 为 9 的 装配 顺序 ， 如 下 图

本站 二

5
下 enter

和

Fa
站 ce
te

EEC

FLb

从

|

人

CE

AX
FAW
个

-

TD

E

二 EEC

二R

AN

二人
下 下 二 商 二 下 直下 到 下 生 和
SESS/
Eee

村

是 se

f

A

@ester
国 crasn

0
dl4

是

wo

NESEESESE

访

¢
加

分

Wa

VD 人

图 4 路 径 代价计算

取 其 中 一 条 ， 完成 20 日 尚未 完成 的 部 分 装配 顺序 如 下 表
的 装配 顺序 表 见 附录 -8。 具 体 计算 结果 见 数据 文件 夹 *paths.mat"和
“schedule.xlsx"
文 件 。

13

5，9 月 20 日 完整

<!-- source_page: 14 -->

回味
四
表 5 最 优 搜索 路 径 代入 装配 顺序 表
2018/9/20

443

A2

B1

汽油

四 驱

a8

c2

2018/9/20

444

A2

B1

汽油

四 驱

白

C1

2018/9/20

445

A2

B4

汽油

两 驱

白

C2

2018/9/20

”446

A2

B6

汽油

两 驱

白

C1

2018/9/20

447

A2

B6

汽油

两 驱

棕

c2

1 2018/9/20

448

A2

B6

汽油

两 驱

红

C1

2018/9/20

449

A2

B4

汽油

两 驱

棕

C2

2018/9/20

450

A2

B1

汽油

两 驱

红

C1

2018/9/20

451

A2

B4

汽油

两 驱

银

c2

2018/9/20

452

A2

B4

汽油

两 驱

银

C1

2018/9/20

453

A2

B1

汽油

四 驱

银

c2

2018/9/20

454

A2

B1

汽油

两 驱

红

C1

1 2018/9/20

”455

A2

B1

汽油

两 驱

金

C2

2018/9/20

456

A2

B4

汽油

两 驱

红

CT1

2018/9/20

”457

A2

B4

汽油

两 驱

棕

C2

-

1 2018/9/20

458

A2

B4

污浊

两 驱

棕

C1

A

nso 0

h

w

ma

m

&

a YY

6. ie>

'

6.1 评价
与 改进

DA

在 模型

其

展示 数据
快速

的 建立 和 求解 过 程 中 ， 5 用
， 使 用 python
整理 规范 数据

实现 算法 ， 在 计算 结果 展 2

+
\ )

机 工具

， 使 用 Excel 汇总

， 使 用 Lingo 优化 配置 方案

ATLEAA.

， 使 用 Matlab

计算 过 程 衔 接 方面 取得 了 较

好 效果 。 在 进行 充分 的 理论 分 相 曲 甘 础 上 ， 正 是 综合 采用 以 上 手段 ， 才 实现 了
二

人
对 于 原

设计 。

题 目 中 这 样 复 委 的 综合 问题 ， 本 文 给 出 的 模型 和 求解 过 程 仍然 显得

复杂 ， 6，

需要 较 多 的 经 验 性 人 工 干预 ， 需 要 进行更 高

6 守 0榴 的 推广 应 用

的 抽象 梳 所

更

智能 化 的 算法 进行 改进 。

有

samer

泛 ， 实 现 了 对 数据

人

多

下

全

的 归 本 方案

属性 不 同 、 要 求 形式
多 样 、限 制 条

的 统筹 分析 ， 可 以 运用 于 工厂 机 器 的 顺序 调配 、 车 站

班次 的 调配 等 实际 问题 ， 在 提升

资源 利用

率 、 节 约 生产成 本 、 提 高 经 济 效益 方

面 有 着 积极
作用 。
参考 文献
器 ] 来 学 伟 . 贪心 算法 在 TSP 问题
中 的 应 用 中.
思 ] 陈 灵 佳 . 蚁 群 算法 在

许昌 学 院 学 报 ,2017.36(02):41-44.

解决 TSP 问题
中 的 应 用 四 .电子 技术 与 软件

14

工程 ,2017(10):145.

<!-- source_page: 15 -->

多
二
EEE
D] 李

月. 基于 遗传 算法 的 免疫 算法 对 TSP 问题 的 改进 与 研究 囊 . 中 国 传媒 大 学 学 报 (自然 科学

版 )2017,.24(04):58-63.
[ 针 囊 豪 . 旅行

商 问题 的 研究

与 应 用 [D]. 南

京 邮 电大 学 ,2017.

[5] 联 合 开发 网 基于 遗传 算法 的 TSP 算法 [EB/OL]. http:/www.pudn.conyDownloadjitenyid/3107168
html,
2018.9.15.
[6]Matlab 论坛 . 广度 优先 搜索 所 有 路 径 [EB/OL]. http://www.ilovematlab.cn/thread-212175-1-1htm,
2018.9.15.

-a,

-从
&

外
%

)

_—

AL

ee

15

和

<!-- source_page: 16 -->

回味
RE 辣
党

站 全
aaa
附件 -1 使 用 python 整理 生产 计划 表

使 用 python 将 “CUMCM-2018-Problem-D-Chinese-Appendix.xlsx"中 的 生产 计划 数据 整
理 成 规范 形式

， 程 序 文件 名 "problem_D_Datapy”，

具体
见 数据 文件 夹 。

# -#- coding: utf-8 -*import xlwt
import xlrd
data=x1rd. open_workbook( 'Problem_D_Data.xlsx')
sheet=data. sheet_by_name('Sheet1")
cols = sheet.col_values(®)
riqi_index=([x for x in range(len(cols)) if cols[x] == “日期 ])
workbook = xlwt.Workbook (encoding="utf-8')
sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)

多
=LUysJ

# 为 样式 创建 字体

=

style = xlwt.XFStyle()

font = xlwt.Font()
font .name = 'Times New Roman'
font.bold = False

2
H

I\)

# 设 置 样式
的 字体

style.font = font
sheet1l.write(86，6，
sheetl.write(e, 1,
sheetl.write(e, 2,
sheet1.write(86，3，

' 日期
"品牌
' 配置 '
' 动力

'，style)
'，style)
style)
'，style)

sheet1.write(86，5，
sheet1.write(86，6，

' 颜色
' 数量 '

'，style)
style)

sheet1.write(9，4，

"驱动

4s
4

'，style)

idx=0
全
for k in ER
@
for t in range(riqi_index[k
i_index[k]-2):
for s in range(5):
if sheet.cell_valde(rigi-index[k]+t+1,s+4)
idx =
1

\

丝 @d 的 呈 产 计划 就 记录 一 行

-全

中位 置 为第1 列

sheetl.wnite(idx, 0, sheet.cell value(riqi_index[k]+t+1,0),

style)

sheetl.write(idx,

style)

人

人
2

va

1, sheet.cell value(riqi_index[k]+t+1,1),
2 列

hegt1.write(idx，2，sheet.cell_value(riqi_index[k],s+4)，style)

分

# 配 置 在原 表 中 位

置 为上 方 的 第 2 行

sheet1.write(idx，3，sheet.cell_value(riqi_index[k]-1,s+4)，style)

# 动 力 在 原 表 中 位 置 为上 方 的 第 1 行

sheetl.write(idx, 4, sheet.cell value(riqi_index[k]+t+1,2),

TAN

# 驱 动 在原 表 中 位 置 为 第 3 列

NA

# 颜 色 在 原 表 中 位 置 为 第 4 列

人N

!=0:

sheetl.write(idx,

5, sheet.cell value(riqi_index[k]+t+1,3),

sheetl.write(idx, 6, sheet.cell value(riqi_index[k]+t+1,s+4),

# 对 应 以 上 属性 的 汽车 生产 需求

workbook.save('problem_D_Data_Chuli.xls')

16

style)
style)
style)

<!-- source_page: 17 -->

区

|

四
附件 -2 规范 生产 计划 安排
规范 后 的 生产 计划 安排 ， 以 下 图 2018
年 9 月 20 日 为 例 ， 数 据 文件 名
“Problem_D_Data_Chulixls"， 具 体 见 数据 文件 夹 。
日 期 河 。 品牌 *| ， 醒置 *|

2018920
| 20l8920
1 2018920
| 2018920
2018920
1 20l8920
| 2018920
2018920
| 2018920
| 2018920
| 20l8920
| 2018920
1 2018920
|2018920
2018920
1 2018920
|2018920
2018920
|2018920
| 2018920
2018920
| 2018920
1 2018920
|2018920
2018920
|2018920
| 2018920
2018920
| 20l8920
| 2018920
|2018920

Al
A1
Al
Al
Al
Al
Al
Al
Al
Al
Al
Al
Al
A1
Al
A1
A1
Al
A1
Al
Al
Al
Al
A1
A2
A2
a2
A2
a2
A2
a2

| 20189204=s27

| 2018/920
2
全
2018/920
|

WW

lsscd

01892
18920
2018920
2018920
|2018920
1 2018920
| 2018920
2018920
|2018920

Bl
B2
BS
BS
Bl
B3
Bl
B2
B5
Bl
B2
B3
BS
Bl
B2
Bl
B2
Bl
B2
B3
Bl
B3
Bl
B3
Bl
ax
BS
B

动力 |

1

B5
B6

汽油
汽油

B4

汽油

两 驱

两 驱

2

B4

Bl

汽油

A2

B6

汽油

A2
A2
A2
A2
a2
a2
a2
A2
A2

驱动 |

汽油
四驱
汽油
四驱
汽油
四驱
汽油
四驱
汽油
四驱
汽油
四驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两驱
汽油
两 驱
汽油
两
C
D
汽油
,两 驱
汽油
“两
汽油
两驱
o |
两 驱
汽油 局 。 四 驱
汽油 “” 四 驱
汽油
四驱
油
四驱
汽油
两驱
汽油
两驱
fa
I

Bl
B4
Bl
B4
了4
B4
B6
Bl
Bl

两驱
两驱

汽油

两驱
两 驱

汽油
汽油
汽油
汽油
汽油
汽油
汽油
柴油
柴油

两驱
两驱
两驱
两驱
两驱
两驱
两驱
两驱
两驱

17

颜色[~|

2
黑
黑
灰
扫
银
a
自
自
黑
黑
黑
2
红
p

”数量-~|

of)

9
3
2
1
2
1
114
2
1
2 了
5sdEES>
7 全

帮
区
蔓
蓝
if
if
a
黑
黑
if
自
a
2

4
1
7
1
3
3
1
2
1
8
2
1
1
3
1
36

黑
黑

1
4

黑
红

红

红

全
金
蓝
蓝
iR
棕
棕
a
2

18
3

2
1

2
1
1
1
2
5
1
1
3

<!-- source_page: 18 -->

回 虽过
IE 辣

7

EEE
waza

附件 -3 求解 生产 成 本 优化 模型

的 Lingo 程序

程序 文件 名 为 "生产 成 本 优化 模型 .lg4”， 注 意 满足 于 局 部 最 优 解 ， 不 要 勾 选 "Use Global
Solver 选项 ， 求 解 一 段 时 间 后 可 以 手动 打 断 求解 过 程 ， 具 体 见 数据 文件 夹 。
model:
sets:

xiaobiao/1..460/:A1_,A2_,y,z,%;
shuzhi/l..10/:SL;
!a1
黑 色 四 驱 、a2
黑 色 四 驱 、 al1 非 黑色
四驱、
&2 非 黑色
四 驱 、a1 柴 油 、a2 柴 油 、&a1
黑 色 柴 油

…… 等 特殊 汽车 数值 ;
endsets
init:
y,z=@ole('LingoData.xlsx");

endinit

人

data:
! 打 开 Excel

文

件 'LingoDpata.xlsx'"

读

取 相 关 数据

7

Al_,A2_,x,SL=€ole('LingoData.xlsx');
enddata
min=@sun (xiaobiao(k) | k #GE# 12:
ea 一
Y(k)* (10-@sum (xiaobiao(t) | (t #GE# k-11) #AND¥ (t #LE¥ k) 3
(1-y(£))))
+2 (k) * (10-@sum (xiaobiao(t) | (t #GE# k-11) #aND¥ (t #LEf
K), :
(1-2(£))))
)7
@sum(xiaobiao

(I):Al_(I)*x(I)*y(I))=SL(1);

@sum (xiaobiao(I) :A2_(I)*x(I)*y(1))=SL(2);
@sum(xiaobiao(I):Al_(I)*y(I)*(1-x(I)))=SL(3);

|

@sum(xiaobiao(I):A2_(I)*y(I)*(1-x(I)))=SL(4);
@sum(xiaobiao(I):Al_(I)*z(I))=SL(5);
@sum(xiaobiao(I):A2_(I)*z(I))=SL(6);

@sum (xiaobiao(I)
@sum

(xiaobiao

(I)

:Al_(I)*x(I)*z(I))=SL(7);

:A2_(I)*x(I)*z(I))=SL(8);

@sum(xiaobiao(I):Al_(I)*y(I)*z(I))=SL(9);

@sum (xiaobiao (T) :A2_(I)*y(T)*z(I))=SL(10)
;0)
@for

)7

(xiaobiao(I)

|

(I

#GE#

3-y(I-1)-yY(I)-Y(I+1)
3-z(I-1)-z(I)-z(I+1)

efor (xiaobiao(k)

2)

ndl

>= y(I);
>= z(I);

#LE#

有

H

| k #GE¥

@sum(xiaobiao(t)

|

(t

k-6)

#AND#

)7

(1-y(£)))>=5;
@sum (xiaobiaoktladeft #GE# k-6) #RND#
(1-2(£)))3=57
v

efor

(xiaobidg

(t

k)

:

(t $LEY k)

:

):

bi
1
@bin
bin (
&
(IT 和 由 ;

18

#LE#

a

<sD

essS
AN

<!-- source_page: 19 -->

回 虽和
和

人

上
[1
Feasible solution found.
Objective value:
Objective bound:
Infeasibilities:
Extended solver steps:
Total solver iterations:
Variable
AL_(1)
AL_( 2)
R1_(3)
RL_(4)
BR _( 5)
R1_( 6)
R_(7)
R1_( 8)
R1_(9)
Al_( 10)
Bl_( 11)
Bl_( 12)
Bl_( 13)
Ba_( 14)
A1_( 15)
A1_( 16)
a1_(17)
a1_( 18)
a1_( 19)
a1_( 20)
A1_( 21)
A1_( 22)
A1_( 23)
Ba_( 24)
A1_( 25)
A1_( 26)
Ba_( 27)
Ba_( 28)
A1_( 29)
RL_(30)

%,

-13.00000
-39.78077
0.000000

1
466

Value
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.000000
1.008g00
1¢p0608g
1
上
1
oo
1%0d00g0
1.000000
1.000000
1.000000

g

)

一 一

Y/ "

19

Reduced Cost
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000%
9-0000g
<
0.000800
SS
0.000068
9#00000
6#600000
了
7600000
0.960000
0.600000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000
0.000000

<!-- source_page: 20 -->

回 虽过
0

汪汪 | 站
回 蕉
9
waza
Bi 3

附件 -4 邻接 矩阵 生成
使 用 Matlab
将 除 大 部 分 黑 、 白 色 以 外 的 其 他 杂 色 汽车 ， 按 允许 的 装配 顺序 生成 邻接 矩
阵 ， 以 求解
2018 年 9 月 20 日 装配 顺序 过 程 的 一 些 装 配 顺 序 为 例 ， 程 序 文件名 为
“genGraph.m”，

有具体
见 数据 文件 夹 。
2018/9/20

443

A2

| zolaez0

4

i2018/9/20

”445

A2

|2018/9/20

446

A2

1 2018/3/20

||2018/9/20

ass

447

A2

1 2018/9/20

449

A2

2018/9/20

20189120
1 2018/9/20
2018/20，
中 2018/3/20

i 2018/9/20

450

454

456

全

A2

458
459

AM2
AM

460

时

AZ

二

81

PE

六由

2018/920
2018/920

A2
A2

Bl
了 B1

2018/520

AZ

了 1

A2
A2
A2
A2
A2
A2

B1
也4
BS
BG
了 B1
B4

2018920
2018920

az
A2

过 二
看

2018920

az
Az

A2

两
两
两
西
两
两

—~

污 油
和油

两 驱
两 驱

有和 油
汽油
汽油
柴油
柴油

两
两
两
两
西

驱
驱
驱
驱
驱

黑
黑
黑
红
红

36
18
1
4
3
2

0
°
°
0
2
1

全
E

E

1
1

1

o
o

@
5
5
g
黑

2
和
1
1
3

2
3
1
0
0

瀑

红
全

1

未 分 配 的 汽车

V

o

Graph=one

本

idx=zeros (|

% 连 接 图 共有 N 个 顶点

H Lromesnrnsmnss

\

人
YU

jeth(num)
\
1ax(s: (senun(k)-1))=k;
s=s+num(k);

end
for

k = 1:N
for t =

0
0
1

-

驱
驱
驱
驱
驱
驱

b
两 驱
> 油 O mE

FOATI

function Graph=genGraph(config,color,num)
】

汽油
汽油
汽油
汽油
汽油
再

6
m,

2018/9/20
2
“Ba
2018//20,
A2
也4
2018/9/20 I=
B6
2018/920
1
2018/920
Apd

N=sum(num) ;

Ya

\

hs

2018/9/20
2018/5/20
2018/5/20
2018/920
2018/920
2018/920

20las20
20lasz20

H

Q

污 油
汽油
PI

汪汪

of-

8

Aa

汽油
汽油

Bs

&

PK

空余 的 位 置

az

&

AZ

公

20lagpzo

白

PE

A2
AM
人

ia01a120 本
z018/3/20

PE

mE

A2

4
452
43

A2

中 2018/9/20
|2016/9/20

沪 油

时

A2

455

12018/8/20

B1

人

1:N

if t==k
Graph(k,t) = 0;
end
if t ~= k
if stremp(color{idx(k)},"Fi")

if strcmp(colorfidx(t)}，
白 ')
Graph(k,t) = 1;
end
if strcmp(colorfidx(t)}，
蓝 ')

% 白 色 汽车 在 装配 线 上 的 允许 连接 情况

20

1
1

二

e 站

8

SS

<!-- source_page: 21 -->

回 虽过
IE 辣

7

四
waza
Graph(k,t) = 1;

end
if stremp(color{idx(t)},
i')
Graph(k,t) = 1;
end

end
if strcmp(colorfidx(k)}，'
黄 ') 。 % 黄 色 汽车 在 装配 线 上 的 允许 连接 情况
if stremp(color{idx(t)},
l')
Graph(k,t) = 1;
end
if stremp(color{idx(t)},"
%")
Graph(k,t) = 1;
end
if stremp(color{idx(t)},
i')
Graph(k,t) = 1;
end
if stremp(color{idx(t)},"&")
Graph(k,t) = 1;
end
end
人
if strcmp(colorfidx(k)}，' 红 ') 。 % 红 色 汽车 在 装配 线 上 的 允许 连接 情况
四
<sD
if stremp(color{idx(t)},
#l')
SS
Graph(k,t) = 1;
“\
end
人
if stremp(color{idx(t)},"
%")
(|
Graph(k,t) = 1;
end
if stremp(color{idx(t)},
i')
Graph(k,t) = 1;
end
if stremp(color{idx(t)},"&")
Graph(k,t) = 1;
end
a
end
if strcmp(colorfidx(k)}，
蓝 ') 。 % 蓝 色 汽车在 装
人允 请 连 接 情况
if strcmp(colorfidx(t)}，
白 ")
Graph(k,t) = 1;
end
end
if stremp(color{idx(k)},"%")
xRgernn Lonimstin
if stremp(color{idx(t)},
#3)
Graph(k,t) = 1;
end
if stremp(color{idx(t)},#41
Graph(k,t) = 1;
end
if stremp(color
9)
Graph(k,t)

end
if stramplestor(idk(t)}, 你)
合演

end

Graph(k,

=

18;

stramp(eolor{idx(t)},
#')

0

= 19;

人

1

/)

end

% 人 金色 汽车 优先 与 黄 、 红 汽车 连接

if stremp(color{idx(t)},"
%")
Graph(k,t) = 1;
end
if stremp(color{idx(t)},
#l')
Graph(k,t) = 1;
end
if stremp(color{idx(t)},
#")
Graph(k,t) = 1;
end
if stremp(color{idx(t)}, 4")
Graph(k,t) = 1;
end
if stremp(color{idx(t)},"&")
Graph(k,t) = 1;
end

if stremp(color{idx(k)},
#")

if stremp(color{idx(t)},"
%")
Graph(k,t) = 1;

% 灰 色 汽车 在 装配 线 上 的 允许 连接 情况

% 银 色 汽 车 在 装配 线 上 的 允许 连接 情况

21

<!-- source_page: 22 -->

回 虽过

号

7
回 共

9
waza

end
if stremp(color{idx(t)},
#i')
Graph(k,t) = 1;

end
if stremp(color{idx(t)},
#")
Graph(k,t) = 1;

end
if stremp(color{idx(t)}, 4")
Graph(k,t) = 1;

end
if stremp(color{idx(t)},"&")
end

end

Graph(k,t) = 1;

if stremp(color{idx(k)},
Fi")

% 棕 色 汽 车 在 装配 线 上 的 允许 连接 情况

if strcmp(colorfidx(t)}，
棕 )
Graph(k,t) = 1;

end
if stremp(color{idx(t)},"(1")
Graph(k,t) = 1;

人

end
if stremp(color{idx(t)},
#")

全

Graph(k,t) = 1;

end
if stremp(color{idx(t)}, 4")

NS

全

-

人

Graph(k,t) = 1;

end
if stremp(color{idx(t)},"&")
end
end

end

end

Graph(k,t) = 1;

end

全

>>num=[1112111231];
>>config={'"B1'，'B4'，'B6'，'B1'，'B4'，'B6'，'B1'，'B4'，'"B4'，'B6'};

>>color=f " 银 '， 自 ，， 自 " 红 ' 红 "5 红 ' 金 5 银 二 术 ' 标 3
>>Graph=genGraph(config,colorsnum)

个

生成 所 求 装 配 顺 序 对 应 图 的 令 洋 所 陈 如 下 ;
B

mf

8

1

=

1 了

-人
W

/Tof |Inf

mr

mr

Inf

mm

il

1

1

1

区

@

Inf

Inf

If

1

1

1

1

1

1

1

If

Inf

Inf

©

Inf

1

1

1

1

1

1

1

1

Inf

Inf

1

1

1

1

e

1o

10

1

10

10

1o

1

If

If

1

1

1

1

1

1

8 日 Inf

Inf

Inf

Inf

园

Imf

1

1

1

1

1

1

1

Inf

Inf

1

6

1

1

[1a

Imf

1

1

1

1

1

1

1

mm

1

1

1

@

22

<!-- source_page: 23 -->

回味
IE

ioa

EEE
sa
附件 -5

使 用 遗传 算法 求解 TSP 问题

使 用 Matlab 采用 遗传 算法 搜索 给 定 邻 接 矩 阵 为 Graph 的
图 对 应 的 TSP 问题 ， 程序 文
件 名 称 "ga_TSP.m”， 具 体 见 数据 文件 夹 。
(以 下 代码 改写 自 联 合 开发 网 ，http:/www.pudn.com/Downloadjitenvyid/3107168.html)
可 function ga_TSP (dislist)
CityNun=size (dislist, 2)

'| [ain_yaax, index]=nin(ynax) :
pinly
机

gnmax=500000:

plot (yaean。b
) ;grid:

inn=30; % 初 始 种 群 大 小

plot (max 'r ): hold on:

% 最 大 代数

pc=0.8: % 交 叉概 率

title(
搜索 过 程 ') :

pm=0.8: % 变 异 概 率

1legend( 最 优 和 解 :平均解 ') :

% 产 生 初始 种 群
s=zeros (inn, Citylum) :
for i=1:inn

fprintf ( 遗传 算法 得 到 的 最 短 距离 :%. 2f \n ,min_ymax) ;
fprintf ( BEHERINRERS):
o,
disp (xmax (index,
:)) :

s(i, )=randpern (Citylum) :

end

[,p]=objf(s, dislist) ;

计算
所 有 种 群 的 适应 度

en=1;

“Jfunction

ymean=zeros (gn, 1) :
ymax=zeros (gn, 1) :
xmax=zeros (inn, Citylium) :
senew=zeros (inn, Cityliun) :
sanew=zeros (inn, CityNun) ;
for

[f,pl=objf
(s, disli;

innesize(s,1); % 读
f=zeros(imn, 1) :
了 for i=l:imn
end

于 1: 2: im

f=1000. 蜂 7

% 根 据 个
fsum=0

scnew(j+1,
: )=scro(2,:)

:

smnew(j,
:)=aut (scnew(j, :),pa) : SEEHE
smnew (j+1, : )=aut (scnew(j+1,
: )，pm) :人
end

ET

ymean (gn)=1000/nean(£) :

fsua=fsuntf
(i) 15:%

i=1:inn

end
4% 计 算 累积概率

pezeros (im, 1) ;

p(l)=ps(1) :

% 记 录 当 前 代 的 最佳 个

了 for 1=2:imn

1°
四

下

p(i)=p(i-l)+ps(i:

pp
和

倒数

Cond
p 生 cosdim.D:

max (gn) =1000/ fmax ss

samazx, :) :

MERE

度 计 符 其 被 选择
的 概率

ps(i)=f(i) 15/fsum:
新 种群 的 适应 度

SHHBHE,

Sifor il:im

刁 for

s=smnew: % 产 生 了 新 的 种 群
[f,p]=objf
(s, dislist) : % 计 算
% 记 录 当 前 代 最 好 和 平均 的 适应 度
[fmax, nmax]=max(f) :

tis(i,0)):

o

seln=sel
(p) : % 选择 操作
scro=cro(s, seln,pc) : % 交
叉 操作

scnew(j, :)=scro(l, :) :

-

小

£(1)=CalDist(di

“Iwhile gnignaaxtl
日

全

end

23

让 适应 度 越 好 的 个 体 被 选择 概率 越 高

辣

<!-- source_page: 24 -->

回味
PE
0 光 汪 | or
回
th
waza

SEETEHEHNSETEE

scro (2,:)=s(seln(21。:)

[] function pec=pro (pe)
test (1:100)=0;
1-zeuna(l00epe) ;
amtkl:1)=l:
mround(rand#99)+1:

chk2=nas (cl, c2)
middle=scro(1, chbl+l:chb2) ;
scro (1. chbl+1: chb2)=scra (2, chbl+l: chb2) :
scro(2, chbl+1: chb2) —niddle:

peestest(n):
end

和 一
% “选择

一

一

”操作

本

for il:chpl % 似 于 有 问题

刁

function selnesel (p)

while

i=1:2

sero(t 1)=y:
E

% 产 生 一 个 随机 数

<sD
NS

while

find(scro(2,

chbl+1: chb2) -sc 过

zhi=find(scro (2, chb;

v=scro(l,

了1

while

Ps

end

prand=p-r:
]

chbl+l: chb2)==scro(l,1))

y=sero (2. chbl+zhi)

% 从 种 群 中 选择 两 个 个 体， 最 好 不 要 两 次 选择 同一 个 个 体

rerand:

find(scro(1,

ahi=find(scro(t, chbltl:chb2)r-scrodl ,月 )

selnzeros(2,1):
[Jfor

:

证 oe=t
elmromd(rands (bn-2))+1; % 在 [1, b- DBEARNSE—AFR
2-round Grandr (bn2))41
hbl=ainfclc2)

er.

prand(j)<0

chbl+zhi) :

)==scro

)

一

ead

了 1 四
end
_
_
seln(i)=j: % 选 中 个 体 的 序号
if 这 2&j=-seln(i-D)
WEERREE—K
rand; % 产 生 一 个 随机 数

ofor ichb2+1:bn，
SS
while find », Noaa)
hilogieal
(sexa(1, 1: chb2)==sera(1, 1):
ro
bn

司

a

prand=p-r;
J=1:
品

while

E

£ind(sc¥o (2, 1: chb2)==scro(2,1))

prand(j)<0

E

La 了 itl:
ond

h

nd

CA

4
%“
交 叉 " 操作
function

ind

end

logical (scro (2. 1: chb2)==scro (2.1)) :

smsexo(L zh;
crol2.D:

nd

scro=cro(s, seln,pc)

3“ 变异 ”操作
司 function smev=mut (snew.pm)

bn=size(s, 2):

pec=pro (pc) ; % 根 据 交 叉 概 率 决定 是 否 进行:
scro(l,

则 是 ，0 则 否

hm-sizc (snew 2) ;

:)=s(seln(1),:):

%,

sTnew=snew;

)

24

(2)

<!-- source_page: 25 -->

回味
IE 辣
7
回

pmarpre (pm) ;根据 突 异 入 率 决 定 是 否 进 生 究 异 操作 ，1 则 是 ，0 则 否
if pmm==1
el-round rands(bnr2))41; STELL br1] BEAMA=E—
ERl
c2=round (rand# (bn-2))+1:

chbl=min(cl, c2) ;
chb2=max (cl, c2) ;
x=snew (chbl+1: chb2) ;
snnew (chb1+1: chb2)=fliplr (x) ;
end
end

由
适应度 函 数
function

F=CalDist(dislist,s)

-a,

AS

DistanV=0:

本
中 for

2)

“让

i=l: (n-1)

DistanV=DistanV+dislist(s(i),s(i+1)):

<

end
DistanV=DistanV+dislist(s(n).s(1)):
F=DistanV:
end
-'

>> load paths
>>

ga_TSP(Graph)

外

%

Ah

25

吕 趟

aa

<!-- source_page: 26 -->

回味
RE
辣
二
|

EEE
aaa
附件 -6 广度

优先 搜索 图 中 指定

起 点 和 终点

的所 有 路 径

使 用 Matlab
按 广度 优先 搜索 给 定 邻 接 矩 阵 为 Graph 的 图 中 从 顶点 partialPath
到 顶点
destination 间 的 所 有 路 径 ， 程 序 文件 名 称 "findPath.m"， 具 体 见 数据 文件 夹。
(以
下 代码 来 自 Matlab 论坛 ，http:/www.ilovematlab.cn/thread-212175-1-1.html)
1
2
3

function possiablepaths = findpath(Graph, partialPath, destination, partialweight)
% FindPathiEREFIETRE
TAE Mpartia1pathiEF destinationk B5iE, ZLBKIZHTEATTES
% Graph: BRIE, SEETHORTET AZEESER, BEERARMNE

8
9

lastlode = partialpath(pathLength); % 得 到 最 后 一 个 节点
nextNodes - find(@<Graph(lastNode,:) & Graph(lastNode,:)<inf); % 根 据 craph 图 得 到 最 后 一 个 节点 的 下 一 个 节点

4
5
6
7。

% partialpecn: BETHE, 如果 partialpath
就 个 数 ，夫 示 这 个 就 是 起好 点
% destination; 目标名 点
% partialwelght: partialPath
的 权 值 ， 当 partlalPath
为 一 个 娃 时 ，partialwelght为
patntength = lengrhpartialParn)

10
1
了
13
u
5

Glength = lengthtGraph);
possiablepaths = [];
3 lasthade -= destinarion
* NRlasthod=SEIRTOIEE, MiRApartialoarhifiEH
possiablapaths = partialpach
possiablepaths(GLength + 1) - partiallieight;

16
17

return;
elself "1sempty(

23

3 出 路 径

=
26

tmppath(GLengch + 1) = partialisight + Graph(lastilode, destination);
REH 狂 组 长度 至 Lengtht1 ， 最 后 一 个 元 系 用 于 存放 该 路 他 的 总 路 阳

28

nexthodes(1)

29

elseif visempty(

°,
HEERIDRS

pERE,

ZRAEE—1,

partialPath

== destination

) ) %#Ok<*EFIND>

tmppath = cat(2, partialbath, destination);

27

可
全

find(

18
rerurnz
19 end
28 snexenodes 中 的 雪 一 定 大 于 8, 卫 为 了 让 nexthedes ()ZH, FERT(ENO
2 for il:length(nexthodes)
22
if destination = nexthedes()
24

EHER

一

x奸 接 成 一条 吉 吾 的

possiablepaths( length(possiablePaths) + 1

，: ) = tmpPath;e

= o;

find( partialPath == nexthodes(i)

) )

38
exthodas(i) = 9
3
end
2 end
nextndes = nextices (aexttides ve 有
34
wi§nexthodesHheliiEAE. 因 T 个 节 点 可 能 已 经 这 历 寺 或 二 就是 上 本 点
3 for ic12length(nextuades)

36 | tappath - cat(z, partislpach, nextiodef(d));
37

mppsbpaths - Findpath (Graph, trpPath,

@

destination, parcislieight + Graph(lssthiods, nextiiodes(1)));

3 em possiablepaths =- car(l, possiablepath 浊jj这区

Sath2);

-—
使 用 路 径 搜索 算法 搜索 得 到 有 径 〈 部 分 ) 如 下
>>pathsAl1 = findpath(Graph，13，
0);
>>paths = pathsAll(pathsAll(%,end-1)~=0,1:end-1);

居于 aa
全
日

= 引

ap
5多
:
CEECEREECEIEECEREECEREECESEECEEECEIEECER|
放生 生生 人yeag和
3
四
1
1
下
O
日
引
四
A| 回 :me
站
——
‘
生生
汪汪 四 于
1 2
as

人
p

7

YZ
下

1

引

3

加

1

和 和 全、
人
上
人
WU
一
本
站

5

了

本

是

昌

引

|
一
一

w

本

iT
人

于

上

:l.

26

可

<!-- source_page: 27 -->

回 虽过
ME

7

四
waza

附件 -7 路 径 代价 计算
由 于 各 种 汽车 的 颜色 在 装配 线 上 的 组 合 形式 多 样 ， 使 用 路 径 搜索 算法 给 出 的 可 能 路 径
非常 多 。 以下 采用 Matlab 计算 各 种 路 径 的 代价 ， 并 且 取 代价 最 小 的 路 径 填 入 装配 顺序 的 整
个
过 程 中 去 ， 程 序 文 件 名 称 "pathsCostm"， 有具体
见 数据 文件 夹 。
function [minCost,opt_paths]=pathsCost
(paths, config, color,num,c)
%paths: 需要 验证 的 所 有 路 径
%config: 汽车 配置
%color: 汽车 颜色
%num: 对 应 的 汽车数量
%c: 起 始点 处 的 喷涂 线 分 配
%miniCost: 最小 代价
%opt_paths: 最 小 代价 对 应 的 所 有 最 优 路 径

N=sum(num) ;

o

idx=zeros(N,1);

P=y

-人“让 Ry

% 用 来 记录 每 个 项 点 的 属性 类 表 序 号

for k = 1:length(num)
idx(s: (s+num(k)-1))=k;
s=s+num(k);
end
maxpath=size(paths,1);

人 一

Cost = zeros(maxpath,1);

for k=1:maxpath
path = paths(k,1:end-1);
Coste = 6
for

t = 1:N
if t>=2

if ~strcmp(config{idx(t)},config{idx(t-1)})

全

% 装 配 线 上 配置 改变 代价 +1

end
if

end

end

Cost8

=

Cost8@+1;

t>=3

if ~stremp(color{idx(t)}, color{idx(-2)})

w

% 喷 涂 线 上 颜色 改变 代价 +1
Cost8

=

% 人 金色 汽车 喷绘

线 为 C2

if strcmp(colorfid
if (c == 人
end

end

if stremp
if (c

X%
一

ost(k!

1

inco t=

&

ki=

ER

和@

爹 ')
==1) 1| (c == 2 8& mod(t,2) == 0)

Cost8 = Cos

MX 黄 、 蓝 、2

人

Cost8@+1;

0000;

全 为 ca

(t)}，
黄 ') || stremp(color{idx(t)},
#') || strcmp(colorfidx(t)}，
红 ')
et
==- 6) || (c == 2 && mod(t,2) == 1)

CoSte '= Coste+100000;

st6j

min(Cost);

Cost==minCost;

pt_paths=paths(mink,1:end-1);

27

<!-- source_page: 28 -->

回味
RE
辣
7

EEE
aaa
>> [minCost,opt_paths]=pathsCost(paths,config,color,num,c);
>>

minCost

最 终 算 得 共有 16 条 代价 最 小 为 9 的 装配 顺序 ， 如 下 图 所 示 。
1

3

车
Qroeas
2
[>
RCI
En
Room
ea
re
Ce
sRe

国 ans double

E
|
E
E

2

T
——
B
S 本
S
BE
S
4 B
NE
S
S
S S BJR
S—
BO
S
S S S BR
S—C
S
S
S S S S BJR— S—C
S
S
S S S S
R——C
|
[DERRRECIREEIRRIRLIREIIIERIREIEICIEC
辐 |
E
S
S
S SC S S
R— S—C
BS
S
S S S
R——C
CS
S
S
S S S S S S N——

EC

上

i
中上
|
|
|
E
|

2

了
5

“\

日
<
Eee
可 NT
>
Em
Sa
Se
所
四
名
是
re
是
有
取
其中 一
据 文

X

FL
J==

S

条 注意 四 驱 汽车 的 位 置 )》 ， 完 成 2

|
装配 顺序如 下 。 具 体 计算 结果 见 数

件 坎 “paths.mat"
和 “schedule.xlsx”。

[]
2018/9/20

443

BT

Omm

PE

白

C2

2018/9/20

”444

B1

汽油

四 驱

a

C1

1 2018/9/20

445

汽油

两 驱

白

C2

2018/9/20

”446

汽油

两 驱

白

C1

B6

汽油

两 驱

棕

C2

B6

汽油

两 驱

红

C1

A2

B4

汽油

两 驱

棕

C2

A

A2

B1

汽油

两 驱

红

C1

451

A2

B4

汽油

两 驱

银

C2

452

A2

B4

汽油

两 驱

银

CT

453

A2

B1

汽油

四 驱

银

C2

2018/9/20

A2

1 2018/9/20
| 2018/9/20
Eee

|
P

8

%,

1

/20

454

1

Moiaezo

全

a2

A2

B1

汽油

两 驱

红

C1

2018/9/20

456

A2

B4

汽油

两 驱

红

C1

2018/9/20

457

A2

B4

汽油

两 驱

和棕

C2

1 2018/9/20

458

A2

B4

汽油

两 驱

棕

C1

1 2018/9/20

459

A2

B1

汽油

四 驱

白

C2

2018/9/20

460

A2

B1

汽油

四 驱

白

C1

m1

omm

28

mE

&

Q

<!-- source_page: 29 -->

ERi

A

附件 -8 9 月 20 日 的 装配 顺序
装配 顺序

品牌

配置

力

驱动

色

喷涂 线

aaa
ca
le |
Lam
li 本 | ae
La lalam
ll
| &a [ a |
LA
am |
| om | ae
wa
|
Lam
li 本 | & | a |
wiia
iaaliEEle ie
LDL
Li
| 本 |
cepl
[o [a [e [orm [me | a [ oAR
Le
ww nm
ma
| e\§
Law
la | | Eee
L” wan
mm
ar
[»
w Tw [
[ mm [Qg ")e |
La
nm mANNSN
Leola
ia
o le
[Leola

iiLei

ol el

La lw
cr
mi alle
L> ww
am
mm
ne
[2 |“|
LA
mm
[oz
|

|

[ae
有
|
LA
v | » |rw | omw | w | a|
sw
aliElc
ie
人 >
wm
| 本 | me |
CSICE
L> wm
li 本 | me
wa
iiilc
ie
L”| wm
mm
me
|
|Lgs laila
li
iio
le
La
wm
mm
me |
[Lawala
li
ii ol el
La
wm | w | m= | me |
[Laola
li
iio
le
Lo wm
出 | 本 |
| e |
29

<!-- source_page: 30 -->

加器

EEI

N

E

E

E

EE

E

EE

E

EE

[Lam
ll 本 | me
I

本
C

I

四

IE2

四
[2

Lwm 和 lw

nm

相

| m | cepl

Lo

[w

[m

[rw

[mm

Lo

[w

[m

[rw

[ mm | safy =B

LS

|

| n | cAF

Le

LS

LS

Cr

owm

四

本

本

Le

|m

|

La

al

AGEN
=
e|
本 天 本
Afm

mo

| wJQ¥F

| rw

四
oy

攻 | =

本

| wx | x

|

La

o |

| @ |

本 | me

|

可 | me

|

[ w | mx | x | @ |

ta me
ISO

人 全
TAN

E

|

[|
四

[|
四

国 世 国 本 站 国 国 癌 国 本 天 本 一 国 大 改写 二
La
am
lm | 本 | me
|
CCI

[Le

I

am

lm
30

E

| 本 | me

EE

|

<!-- source_page: 31 -->

加器

Le

Law

[a

[e

[ ew

am

[ mx | 2

[ @ |

rm 本 | me

|

四

四

IC2

O

E

EE

ICC

O

E

EE

ea

| cepl

四

国宝 本
加

L”>

wm

mm

相

Lo

[w

[m

[rw

[mm

Lo

[w

[m

[rw

[ mm | aafy =B

LS

| a

[| cAR

Le

LS

LS

o|

国宝 国 国 站 国 大 可 国 国

国力 <

s

e

Le

oa

wm

ome

| 8

@|

Le

|w

Afm

| wx | a

| @ |

|

La

| mo

本 | ee

|

La
mm 可 | ee

|

FT
四
2 风 | 攻

ta

w

wm | ww

|

omx | s

NE

a|

本
TAN
四

[|
四

[|
四

Cw
a
[La

wm
w
me | 8
@|
mr
| 本 | 日 | el |

四

[La

<!-- source_page: 32 -->

加器

ICEN

0

C

E

C

EE

[Lam
| 本 | 日 | el

ICE2

四
四

LA

Lon [a

[e

[ew

[me

Lw

mm

相

四
[|

Lw

lw

[w

[m

[rw

[mm

LS

[

[@

|

| a | cepl

| a

| oAR

[|
La

ae

La

AS

PS

[ o|

国 世关 国 肖国 国 癌因本

国力 <

s

e

w

ome

| 8

@|

oa

国志 本

La

wm

IE

| mo

本 | ee

|

am
可 | ee

|

2

La

四
多

Ma

ISO

w

w

owm | ww

[w

[m

omx | m

| owx | x

AlLS
w | w
| ow | =
TAN

a|

| @ |

a|

四

[|
|

[|
四

e
oa
wm
w
ome | ®
@|
[Lam
本
| me
|
四

[Lam
[rw | 本 | me

|

<!-- source_page: 33 -->

加器

四

[Lam
ar | 本 | me
四

om

|ow

wm | w

四

二

四

ome | o®

|
a|

四

四
[|

Le

lw

mm

1

相

mm | cepl

LS

[2
La

T

TN

LS

Y

T

国人

w

oe

m

oe

AGEN

x

@

w

e

owm

ww

ome | ®

@|

国志 国力

IAA

| wo | wo | wfVYrw

| mm | m

a |

|m

em | m

a

[o

[ wdgo

四

JTe

| em | owx |

=

[ em | owx | x

| @ |

[ wm | ox | x

| @ |

| e JQ¥F

oy

JW¥

[

ISO

o

[w

Ma

w

[ rs [ wx | @ | @ |

| rw

owm | ww

omx | m

本
TAN

|

|

@ |

a |

四

[|

om

|e

[owm |em

| oww |om

| o@

Cow

e

[owm |m

| oww |om

| @

[|

EEE
E
T
| w | wo | m | rw | omm | ®
四

[mw
33

a

|

<!-- source_page: 34 -->

加器

Lw

Lo

[ a

[ ew [

w

[ mx | 2

| @ |

wm

四

国宝
四

本
四

La
[|

[Low

nm

lm

本

|

国宝

cepl

四

[2

LP

|oe

|ow

| m

| owx | s/gNad |

wm

ASS o |

LS
Le

we
w
AGEN

s

e

EEEEE
T
Lm

[ow

[La

|

Afrem

| mo

| wx | a

| @ |

本 | ee

|

FT

[La

RE

me

四
区

Ia

SO

w

owm | ww

omx | s
C

人
TAN

a|
E

四

[|
四

[|
四

w
a
wm
w
ome | 8
@|
[Lam
| 本 | 日 el
四

[Loan
[rw [ wm | & | a |

<!-- source_page: 35 -->

加器

EEEIN

N

C

E

| =m [ml
本 | 日 el
四

本
四

四
四

四
[|

La

Lw

| wm

[ow

[m

lm

[rw

相

[mm

ea | cepl

| a

| oAR

ASS

o |

Lo

国人

Le

LS
La

w

oa

m

r

AGEN

s

e|

EEEE
E
四

本

La

IC

| mo

本 | ee

|

[LamRE
nm 可 | ee

|

[|
四
|

Ia

ISO

w

ow | ww
T

omx | s
C

a|
E

AlL®
w | ma
om |ona|
TAR
IE

T

T

[|

C

四

[|
E

EEE
E
| w [ w | m
[o

[=

[a

[w

T

[w

[ w [ = [rw

C

E
本
|

[m

[ a [ @ |

[ wm | & | a |

<!-- source_page: 36 -->

加器

L=

| a

| @ |

w |ow
w | ww ome | o®
[|

a |

Lam

[ w

[ w

[

w | m

am
本

el

四

|

Lo
四

四

本

四
LPl| wm

mm

相

mm | cepl

Lom

[w

[m

[rw

[mm

fom

[w

[m

[rw

[ mm | safpy =B

LS

| 8 | cAR

Lam
T

T

LS

La AS

o |

国宝 本 四国 国 忆 因 本 二 国力 <

天

国志 因 本 站 国 国 忆 因 本 局 因 本

国国避 本

四

大忆

IC

La

aa | mo

本 | me

|

Lm

| w Q¥F

nm 可 | me

|

FT

L

tly JTm

| ew | omx |

四

Ia

ISO

w

ow | ww
T

omw | ®

本
TAN

|

@ |

a|

E

四

[|
四

[|
四

EEE
[La
四

[La

<!-- source_page: 37 -->

加器

Lo

[| w

[ m

[ ew [ mx |

|

La

@ |

四

四
四

国宝 本

本

四

国宝
[|

Lo

| wm

Lowe [w

[m

lm

[rw

相

[mm

Lo

mm | cepl

| 8 | oAZ

[2

Le

Lo

LS

Law

nm

| ma | 本 AN

国宝 本 站 国 国 癌 因 本
本
四

国力 <

EC 国 国 忆 一

本
IE

[Law

= |

| mo

本 |

ae

|

La

wm
本 |

Le

|

op

JW

FRR

1

ta
Se

w

|

m

[ e

owm | ww

| oex | x

omm | x

人 wa
TAN

| @ |

a|
E

四

[|
四

[|
四

国志 因 国 汪 国 国 二 因 本 富国 本 天 大略 国 国 忆
[Lam am
| 本 | ae
|
四

[Lo

<!-- source_page: 38 -->

加器

四

本
四

国宝

本

四

四

本

四

本
[|

La

| wm

lm

相

mm | cepl

国宝

LS

[|

La mV

LS
La

AS

国宝 本 国 国 忆 因 本

国力 <

国宝 本 四国 国志 因 本 剧本
四

加

2

|

L

ty

国国避 本

| em | m

a |

wm
上 me

oy

JW

Se

w

ta

天国 忆 到

IC

| o | w | wfVymw
Lm

o |

w

Je

[

=

w

[m

| em | omx | m

| @ |

[ e

| owx | x

| @ |

[ m

| owx | x

| @ |

| ww

mm | m

人 站
TAN

a|

|

[|
四

[|
|

本 二 本 大 癌 国 要因 本国
La wm
| 本 | me
0

|

[Le

<!-- source_page: 39 -->

加器

Loo | a

[ w

[ ew | mx | =

Len

[w

[ew

[Lo
[m

本 一 本国

加 本

四

本

[ mx

本

本

Les

[m

[e

L2

| wm

[ew

[

[ me

| @ |
|

[ e | @ |

Loee | om
ow | ww omx | o®
[|
nm 本

国宝 本 一 故居

二天本

Lo

Lo

[w

[w

[rw

@ |

mm

oa|

| cepl

| m | cAR

[ mm | safy =B

Le
T

T

LS

Lo AS

本

本

本

本

国力 <

x

本 辣 本 王国 大 总 因 本 剧本
四

o|

e

国人

IAA

本

人工

2

了

Lo

wm

o

JW¥

SC

e

| w

|oe

|ow

四

ta

w

|

w

w

[ w

| ww

| wx | & |

mw

| m

[ em | ox | & |

人 人
TAN
Lew

|m

| oww |ow

国宝

@ |

a|

@ |

|

|

[|
四

本 本 大 忆 靖国 富国 醒 天国 加 国 本 二 加
本
四

[w

|

<!-- source_page: 40 -->

家
，

%"

各
&
