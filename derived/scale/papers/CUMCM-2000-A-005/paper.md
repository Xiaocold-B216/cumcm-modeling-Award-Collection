# Extracted Paper

<!-- source_page: 1 -->

第 31 卷第 1 期
数学的实践与认识
V o l131 N o 11
2001 年 1 月
J an. 2001
M A TH EM A T ICS IN PRA CT ICE AND TH EO R Y

分 类 模 型

交

D NA

流

em p loy the B P ( back p rop aga tion ) a lgo rithm to tra in NN by u se of the N eu ra l N etw o rk
Too lbox in M A TLAB softw a re p ackage. In th is p ap er, tw o th ree2sto ry NN a re crea ted to inp u t
the ex tracted DNA cha racter vecto rs a s sam p les in to them. A fter the tra in ing, cha racters a re
ex tracted from the 20 uncla ssified a rtificia l sequence sam p les and 182 na tu ra l sequence sam p les
to fo rm the cha racter vecto rs a s inp u t of the tw o NN fo r clu stering. T he resu lts show s: the
clu stering m ethod p resen ted in th is p ap er can cla ssify the DNA sequences in qu ite h igh accu racy
and p recision. It is qu ite fea sib le to app ly the a rtificia l neu ra l netw o rk to DNA sequence
clu stering.

编者按:

100871)

：
科

( 北京大学, 北京

研

杨 健, 王 驰, 杨 勇
指导老师: 王 鸣

本文将 DNA 序列的碱基的组合看作“文章”的关键词, 用逐步优选法对关键词进行优选并用分

层分类的方法进行分类. 从理论上说, 这一方法可以提取较好的特征, 而且分类也较精细. 这一模型有一定
创造性, 分析问题比较精细而贴近实际, 思路清楚, 叙述通顺简练.

摘要:

本模型充分利用了所给数据的特点, 运用统计、最优化等数学方法, 从已知样本序列中提炼出能较

好代表两类特征的关键字符串, 据此提出量化的分类标准, 能较好的对任给DNA 序列进行分类. 首先, 从已

号

知样本序列中用广度优先法选出所有重复出现的字符串, 并计算其标准化频率及分散度. 然后, 利用样本数
据结合最小二乘法确定两类字符串各自的优先级函数, 并且逐步优化其参数使之达到稳定, 提高了可信度.
最后, 根据优先级函数找出关键词, 然后确定权数, 用层次分析法对未知样本进行分类, 并定出显著水平, 从

公
众

而得到了一个比较通用的分类方法. 经过检验, 此方法对 21—40 号待测样本进行了很好的分类, 对后面的
182 个 DNA 序列进行同样的操作, 也有较好的效果.

1

问题的重述 ( 略)

2

模型假设

信

( 1) 假定待分类样本 21—40 中既不属于 A 类也不属于 B 类的样本百分比不超过 5%.

微

( 2) 假设 keyw o rd 的重要性与 t 和 s 有确定的关系, 且只与 t 和 s 有关 ( t, s 定义见下).

3

( 3) 假设不代表 A 、
B 类特征的字符串在 DNA 序列中是均匀分布的.

模型的分析

从所给的 DNA 序列观察发现, 很多字符串重复出现的频率很高, 而且有些字符串在 A
类和 B 类中出现的次数有很明显的差距, 这暗示把某些字符串作为 A , B 两类的一个分类标
准. 所以应对 A 、
B 两类已知样本做统计分析, 找出其中可能代表该类特征的字符串. 因为
每个字符串重要性可能不一样, 所以对这些字串的重要性排序, 选出最能代表该类特征的一
部分字串. 然后用这些字串作为标准判断验证 A , B 两类, 看所选的标准的准确性, 最后用
于任何一个 DNA 序列的分类.

<!-- source_page: 2 -->

加 成 守 沁 加
天
32 数学 的 实 上 距 与 认识 1
4 定义 与 符号 说 明
A 类 样本 : 编号 为 1 一 10 的 DNA 序列
B 类 样本 : 编号 为 11 一 20 的 DNA 序列
词 Gvord): 由 ae, bg 组 成 的 在 样本 中 重复 至 少 两 次 的 字符 哩
关键 词 (keyword): 能 代表 A 类 或 B 类 的 特征 由 a ,ct g 组 成 的 词
分 散 度 (* ): 指 某 一 类 中 包含 某 个 word 的 DNA 序列 的 个 数
出 现 次 数 ( 1): 某 一 字符 串 在 DNA 序列 中 的 出 现 次 数
序列 长 度 (”):DNA 序列 的 长 度 #7
字符 串 长 (m ): 字符 串 的 长 度 二 SS
标准 化 频率 ( 1): /= 15m 标准 化 了 的 词 的 出 现 次 数 2XG \
优先 级 函数 (7 ): 衡量 词 重要 性 的 指标 , 5 和 ! 的 函数 H
权 值 D): 衡量 DNA 序列 类 别 特征 的 量化 指标 处
S 模型 的 建立 与 求解 禹
(1) Keywords 的 选择 CD
选择 keyword 是 所 有 工作 的 基础 ， 人 有 效 的 分 类 在 很 大 程度 上 依赖
keyword 选择 的 好 坏 , 所 以 我 们 的 原则 是 所 选 的 Keyword 一 定 要 能 代表 A 类 和 B 类 基因 序
列 的 尽量 全 面 的 特征 , 并 且 所 选 的 keyword 应 对 两 类 基因 有 好 的 区 分 度 , 以 利于 分 类
第 一 步 : 选择 word( 广 度 优先 法 ) 2 样 丰 为 人 ,
© 计算 字 长 为 1 的 word Rs CT
置 产 1 AT 】 有
@ 分 别 以 字 长 为 ; 羡 乱 纤 点 为 根 结 点
对 每 一 个 根 结 点 , 若 其 出 现 次 疾 天 于 1, 在 其 后 Me(
分 别 加 入 人 er 壬 长 度 为 六 1 v
的 新 字符 串 , 计算 坛 出 现 次 数 及 出 现 位 置 TIEEI
例如 :2 人 1 的 word ae 站 长 20E  /
人 人 对 于 把" 在 其 后 分 别 加 | / BESpRAXEREE
入 ee “生成 人 ac gg 入
全 由 人 为 2 的 新 吕 ， 一、
] 了 /LS 洛 中 找到 了 新 闻 , WE =  1, 转 到 ne)221 人
CN 兰 则 结束 “程序 流程 图 如 图 上 :
第 二 步 : 选择 Keywords( 和 逐步 优选 法 ) —
现在 我 们 已 经 有 了 A、B 类 的 所 有 的 语录 议 为 /
word, 下 面 要 在 这 些 word 中 选 出 好 的 En
keyword 图 1
@ 选 择 典型 代表
我 们 认为 , 对 于 每 一 个 word, 标准 化 频率 ! 和 分 散 度 * 越 大 , 它 越 具有 代表 性 , 所 以 我 们
先 在 所 有 的 word 中 人 工 粗 选 出 一 些 明 显 具 有 类 别 特征 的 word 作为 初 选 关键 词 , 选择 时 ，
994. 8 in c ic Journal P Shing Hous: Tig] er W t

<!-- source_page: 3 -->

加
全
1 其 杨 ， 健 等 :.DNA 分 类 模型 3 w
不 妨 多 选 出 一 些 , 尽量 不 要 丢失 信息 , 也 就 是 ' 圆 轿 吞 永 …, 我 们 在 具体 操作 时 , 对 A、B 类 各
选 出 了 30 个 左右
加 进行 初步 优选 :
我 们 假定 keyword 的 重要 性 只 与 5 和 s* 有关 , 而 且 这 种 关系 在 一 定 的 范围 内 有 确定 的
解析 表达 式 , 我 们 想 找 出 这 个 函数 关系 /.
显然 , / 是 s 的 增 函 数 , 也 是 : 的 增 函 数 , 所 以 假设 /具有 形式 :
GD = sx (D)
其 中 x 和 有 分 别称 为 * 和 的 影响 力 因子 #7
对 于 某 个 word, 由 (D 式 求 出 的 值 称 为 它 的 f 值 = ks
接 下 来 我 们 用 上 面 选 出 的 30 多 个 word 结合 最 小 二 乘法 来 确定 % 和 B. BA 美 为 例 ，
设 A 类 中 粗 选 的 word 分 别 有 值 : 5 光
t, 12, **°, 139 和 1，82， ”939 H
为 了 运用 最 小 二 乘法 对 (D) 式 取 对 数 有 : X
logf = alogs + Plogt % (2)
我 们 期 望 好 的 keyword 的 / 值 都 较 大 ， 2 限 之 上 , 所 以 把 A 类 的 39 个
word 的 /的 期 望 值 定 为 50. 0( 这 个 值 只 具有 相对 意 尽 ,导体 定 为 多 少 对 模型 的 优 劣 没有 影
响 )， 过
gs(X% 有 )= )> Co 时 Blogt - lg50)” (3)
达到 最 小 O
利用 MATLAB 提供 的 优化 工具 条 甸 理 此 最 小 二 乘 问题 , 得 到
o 70. a65 有 = 0.8057
同样 处 理 B 类 的 26 2
= 0 2217 应 = 1 3060
这 样 ， anaaan - 类 的 优先 级 函数 的 表达 式 :
六 一 中 几 (4)
2 ) V fo= sib (5)
这 语族 的 本 数 在 下 面 的 沙 可 中 下 人 这 地 优 人 西数 的 参半
WTA
优 钴 级 , 将 每 类 的 word 按 优先 级 大 小 排序 , 选择 优先 级 最 高 的 16 个 word 作为 每 类 初步 优
] 化 GH0 keywords
\® 对 上 面 得 到 的 keywords 重复 第 @ 步 的 方法 , 用 最 小 二 乘法 求 出 每 类 新 的 gx 和 B1H,
这 样 就 得 到 了 进一步 优化 之 后 的 优先 级 函数 , 用 此 函数 算出 每 个 word 新 的 优先 级 , 再 选择
优先 级 最 高 的 16 个 作为 进一步 优化 之 后 的 keyword
图 重复 几 遍 第 @ 步 , 直到 xx 和 8 的 值 达到 稳定 此 时 的 结果 是 :
o = 0 4585 有 = 08851
= 02347 应 = 13769
至 此 , 选择 keyword 的 工作 结束 , 而 且 得 到 的 keyword 是 按 优先 级 大 小 排序 的
) 由 上 面 的 工作 步 又 可 以 看 出 , 这 32 个 keyword 基本 上 代表 了 A 类 B 类 的 特征 , 而 且 A
94-2008 China Academic Journal Ele c Publishing House. All rights reserv http w.cnki.nef

<!-- source_page: 4 -->

四
34 数学 的 实践 与 认识 1 着。
类 B 类 的 keyword 基本 没有 重复 , 有 很 好 的 区 分 度 Keywords 见 表 1
表 1 选择 的 关键 字
A 组 B 组
关键 字 出 现 次 数 分 散 度 关键 字 出 现 次 数 分 散 度
agga 32 9 taa 50 10
ga 109 10 ttta 52 10
ggegg 28 7 aa 119 10
ggc 69 9 tat 148 10
ggaggc 11 8 at 131
aa 115 8 ttaa 34 edUAs
agg 65 4 tatt 36 Py SN
ggaa 34 10 ta 62. \¥
ggegga 17 10 att .2 10
a 318 10 a 32 H 10
[< 80 10 ttat S 2 10
- 42 10 attt 10
ggagg 26 9 tta 105k 10
gga 93 10 ttt 颂 58 10
gg 198 10 7 “ 552 7
g 425 10 祷 _ 193 10
AS
图 2 为 每 个 word 的 优先 级 对 分 散 度 、 标准 化 频率 的 图 象 其 中 keyword 用 圈 标 出 从
图 中 看 出 , 用 逐步 优选 法 求 出 的 keyword 确实 分 别 代表 了 A、B 类 的 重要 特征
ee 9
or YA 全 用
HR ! 人 n 0 : 1 本
J 人 1 罗 E SEE SRER E ia SRENAN
人 人
| 和
6 了 本 人
- | | 上
|
本
| 2 人 全
岂 2
Te ， MSN 一
1don rn RN
图 2
图 3 为 逐步 优选 法 的 流程 图 需要 注意 的 是 ,word 的 / 矿 值 不 仅 是 提取 keyword 的 标准 ，
而 且 也 反映 了 每 个 keyword 的 重要 程度 , 这 对 于 以 后 的 基因 分 类 标准 也 具有 重要 的 价值
(2) 加 权 系 数 的 确定
现在 来 提取 A 类 和 B 类 基因 序列 的 主要 特征 以 便 提 出 分 类 标准
对 于 某 条 基因 序列 P ,我们 假定 它 相 对 于 每 一 类 的 权 值 D 只 与 此 类 keyword 7E P h
的 出 现 次 数 ! 和 keyword 的 优先 级 ( 即 广 ) 有 关 , 我 们 希望 找到 这 个 关系
0 Academic Jour ai tsT d WW i.nef

<!-- source_page: 5 -->

杨

健等: DNA 分类模型

35

：
科

研

交

流

1期

图3

号

显然, 一个合理的假定是: P 的权值 D 是 l 和 f 值的某种组合.
设某条基因序列 P 的权值具有表达式:
16

公
众

D A (P ) =

∑f

ΚA

x A , i (P )

( 6)

x B , i (P )

( 7)

A,i

i= 1

16

D B (P ) =

∑f

ΚB

B,i

i= 1

式 ( 6) 中, f A , i 是 A 类第 i 个 keyw o rd 的优先级函数值
xA , i是序列 P 中具有 A 类第 i 个 keyw o rd 的个数

微

信

ΚA 称为 A 类 keyword 的影响力因子
式 ( 7) 中的变量、参数同理理解.
称 D A ( P ) 为基因序列 P 的 D A 值, D B ( P ) 为 P 的 D B 值
下面来确定 ΚA 和 ΚB , 以 ΚA 为例.

我们期望对于 10 个 A 类样本, 它们的 D A 值都较大且稳定在某个定值 ( 设为 d ) 周围,
另外, 为了提高分类效率我们把 ΚA 推广为 ΚA , k , 表示只与前 k 个 keyw o rd 有关, 它的作用在
第 3 点详细讨论. 借用最小二乘法的思想, 令
10

h ( ΚA , k ) =

k

∑ ∑f
i= 1

ΚA , k
A,j

(P i ) - d

2

( 8)

j= 1

利用M A TLAB 的最优化工具箱, 就可以确定 ΚA , k 的值使 h ( ΚA , k ) 达到极小 ( 与上面的分
析相同, d 只具有相对意义, 它的选择对模型好坏没有影响).

<!-- source_page: 6 -->

[ERfiaE
天
36 数学 的 实践 与 认识 1
3 ”层次 分 类 法
现在 要 确定 一 个 分 类 标准 值 ", 当 待 分 类 样本 P 对 某 类 的 权 值 > 时 就 将 忆 分 为 该
类 但 通过 上 面 确定 Xe %.x 的 过 程 可 以 看 出 , 由 A、B 类 的 已 知 样本 确定 > 值 会 使 标准 过
高 , 所 以 用 待 分 类 的 20 个 样本 确定 *， 一 个 合理 的 假设 是 这 20 个 样本 中 既 不 属于 A 也 不
属于 B 的 样本 数 很 少 ( 入 5% )， 用 下 面 的 程序 经 过 几 次 实验 即 可 得 出 较 合适 的 ， 值
另 一 个 问题 是 选取 多 少 个 keyword 选择 越 多 的 keyword 标准 越 严 , 所 以 在 算法 中 将 大
从 16 逐一 递减 到 7(K < 7 时 X .为 负 值 , 标准 无 判断 力 ), 逐 层 判别 忆 是 否 属于 A、B 类
计算 方法 : 2
对 于 待 分 类 样本 已 , 先 取 定 一 个 > 值 使 用 最 严格 的 标准 , 即 上 = 16 , HH 的 入 大
于 ，, 则 认为 忆 属于 A 类 , 并 记 下 此 时 的 大 值 和 D,4 (P) ENEPRENEALN 较 , 直到
k= 7 为 止 车 此 时 D, (P) 仍然 小 于 >, 则 认为 P 不 属于 A， 同 理 可 淹 呈 P 是 青 属 于 B
上 述 算法 中 > 的 确定 : 0 这
在 保证 不 漏 掉 一 个 待 分 类 样本 的 条 件 下 , 使 被 同时 归 为 念 话 西关 前 样本 数 最 小 (不 超
过 待 分 类 样本 总 数 的 5%). 币 NS
据 此 标准 确定 的 > 值 为 4 565( 表 2) X
表 2 AN o
NJANN ¥ 3 4 ] 5 六 6 了 8
- 3.5033 - 1.7439 - 1.1226 - 0.9562 - 0.6998 - 0.2840 0.6556 0.7058
x - 0.8553 - 0.1686 - 0.0716 0. 807 0.0301 0.0584 0.2300 0.2651
9 10 11 册 _ > 12 启 13 14 15 16
A 0.7953 0.9480 1. 地 5 ) 7 1.1628 一 1.2812 1.3328 1.4940 1.5398
六 0.3250 0.3353 0. 5353 0.4272 0.4915 0.5050 0.5220
程序 流程 图 如 图 4 JS-
4 方法 总 结 一 -7
和 RE 得 展 歼 们 16
下 : “%. V
统计 ON keyword 在 P 中 的 出 现 次 数 , 玉 ; / 亲人 Do/
用 层次 分 类 法 对 加 中 的 数据 进行 分 析 , 求 出 权 值 Df、Ds
现 二 次 数 所 De. Y /可 第 Ta
1 全 恬 让 两 组 数据 , 确定 P 属于 哪 一 类 还 可 以 定义 ~ Bp
LAIX PLEH,
显著 性 水 平 (以 A 为 例 ): 人
a) 层 数 为 16 Hbk - 局 > 1 的 定 为 高 度 显著 属于 [AN LNCTS)
ACT); 加
b) 层 数 为 15 一 一 14 Hki- 如 > 1 或 操 = ks HD,
- _D。 > 1 的 定 为 属于 显著 A (”);
oj 层 数 为 13 一 -7 Hki- k> 1 的 定 为 较 显著 属 于 A (”);
d) 其 余 认为 不 显著 ;
若 忆 对 A、B 两 类 均 不 显著 , 将 其 归 入 另类
-2008 Ch cademi E cPublishin ou 1 S TVe; W nef

<!-- source_page: 7 -->

加
人
1 期 杨 ， 健 等 . DNA 分 类 模型 站
S 模型 的 检验 及 效果
@ 对 A`B 类 已 知 样本 : 最 小 二 乘法 保证 A 类 样本 的 D， 值 ,B 类 样本 的 D。 值 足够 大 ，
这 些 样本 必 能 正确 归 类 ; @ 对 20 组 待 测 样本 可 以 看 出 ,A B 类 区 分 度 很 大
A 类 (11 个 ):23 23 27 29 32 34 35 36 37 39B 类 (9 个 ):
21 24 26 28 30 31 33 38 40
® 对 182 组 未 知 样本 : ( 略 )
可 以 看 出 有 少 部 分 样本 不 能 很 好 归 类 ”原因 一 是 已 知 样本 数量 太 少 .长度 太 短 , 无 法 有
效 检索 到 一 些 长 度 较 长 的 keyword， 二 是 模型 有 系统 误差 SRELESs  S3a
于 A 和 B cs
覃 型 的 稳定 性 : 分 别 把 A ,B 两 组 中 的 序列 任意 改变 一 些 字符 , 下 利 用 契 直 的 六 法 进行
分 类 , 经 过 多 次 实验 , 新 的 分 类 结果 均 和 原来 相同 ， oo
6 模型 的 改进
在 选择 Keyword 时 ， 二 上 可以 有 (看 全 组 伍 eyword) ,这 样 更 全 面
的 概括 A ,B 两 组 的 特点 , 使 的 分 组 更 充分 |
本 模型 是 利用 算术 加 权 的 方法 综合 个 keywoiag 鸭 分 闫 重要 性 , 可 以 探索 其 它 的 加 权
法 , 如 几何 加 权 法 , 对 加 权 数 的 选择 也 可 以 进一步 改进 SS
在 分 类 的 过 程 中 采用 学 习 法 : 如 果 某 个 DNA 序 昼 用 本 文 的 结果 判断 , 发 现 对 A 组 (或
B 组 ) 的 特点 高 度 一 臻 ,就 可 以 把 次 序列 列 XEA 组 作为 一 个 分 类 序列 , 然后 对 新 的 A,B 组 重
复 本 文 的 过 程 ， ed °
7 模型 的 评价 和 推广
(D) 模型 的 优点 SS
@ 本 模型 中 有 较 多 症状
数字 转化 函数 yj 冠 ( 几 内 录 )
@ tt 开 ps， 容易 用 计算 机 完成
© 术 机 型 的 算法 和 易 推广 到 实际 的 DNA 的 序列 分 析 中 , 具有 一 定 的 实际 应 用 价值
人 @ 误 入 司 光 择 时 考虑 较 全 面 (涉及 到 出 现 次 数 , 频率 , 理论 概率 各 个 方面 )
| @ 烛 降 何 * 个 给 定 的 DNA 序列 采取 多 层 分 类 法 , 能 够 保证 一 定 的 置信 度
3 汪峰 灵活 的 利用 拖 码 徊 … 使 得 程序 简洁 , 编程 最大 大 减少
Re
Q 所 给 分 类 数据 太 有 限 , 导致 采用 keyword 分 类 的 方法 , 判别 与 已 知 样本 长 度 相 差 太
大 的 未 知 序列 时 准确 率 有 所 限制
@ 一 些 新 的 想法 缺乏 足够 的 理论 根据 , 所 以 有 些 问题 的 解决 的 带 有 一 定 的 主观 性
@@ 本 模型 纯粹 从 数学 的 角度 来 分 类 , 缺乏 生物 学 背景
G3) 模型 的 推广 与 应 用
由 于 本 模型 主要 是 根据 20 个 长 度 比较 短 的 DNA 序列 的 特征 归纳 出 的 分 类 方法 , 如 果
直接 用 本 模型 的 结果 用 于 实际 的 科研 中 , 可 能 会 有 很 大 的 局 限 性 , 但 是 本 模型 用 keyword
作为 分 类 标准 的 思想 是 一 个 可 以 推广 的 比较 好 的 想法 , 具体 的 推广 思路 : 从 自然 DNA 序列
@ 1994-2008 China Academic Journal Electronic Publishing House. All rights reserv tp://www.cnki.net

<!-- source_page: 8 -->

已 二
和 -让
人 局 、| 、 和
第 31 卷 第 1 其 数学 的 实践 与 认识 Vol31 NO 国 =
2001 年 ! 月 MATHEMATICS N PRACTICE AND THEORY Jan 200 7F
任意 选 出 比较 多 的 (为 了 保证 较 高 的 准确 性 ), 利用 keyword 作为 分 类 标准 , 然后 利用 本 文
提供 的 加 权 系 数 的 确定 方法 就 可 以 定 出 一 个 具体 的 定量 标准 具有 一 定 实用 价值
参考 文献
[1] 李 涛 , 贺 勇 军 等 MATLAB 工具 箱 应 用 指南 一 一 应 用 数学 篇 电子 工业 出 版 社 .
[2] 豆 亚 湘 最 优化 方法 科学 出 版 社
[3] 张 妃 孝 , 玫 宗 燕 数据 结构 一 e+ + 与 面向 对 象 的 途径 “高教 出 版 社 .
[4] 汪 仁 官 概率 论 引 论 北京 大 学 出 版 社 . 二
5] 陈 家 易 , 孙 山 泽 等 数理 统计 学 讲义 高 教 出 版 社 .
[5] 陈 家 易 , 孙 山 泽 等 数理 统计 学 讲义 高 教 出 版 字 ~ 人 本
一 W
ve
. 本
The Grouping of DNA Sequences
. 、 SS
YANG Jian, WANG Chi, 机 Kong
(Peking U niversity, K
了 o
X -
Abstract 了 this paper, amethod to classify the os is proposed M athem atical
methods such as statistics and op tm ization are used to build the model The data is analysed
sufficiently and the“critical words”is got,gvhich can represent the characteristics of each
group. According to this, a quantijgtive tandard, for group ing is brought forward  Thismodel
can properly classify the given da foth ough testing First the stringsw hich appear repeatedly
(called words) in the given data afe [全 局 out The standard frequency and dispersion for
each word are calculat nd，using the Least Squares method, the priority function is
fixed Through stepw 四 tinizatid n, the coefficients are made stable Third, the key words
are selected out and ce eweight according to the priority function A't last, using the
“analyse hierarchy-process”’, the undetem ined data is classified This method can classify the
undetem ined data;( 21—No. 40) fairly well, it can also give good result for the last 182
“%, V/
X%
以 > DNA 序列 的 分 类
人 韩 轶 平 ， 余 杭 ， 刘 威
1=)
指导 老师 杨 启明
(浙江 大 学 ， 杭 州 ”310027)
编者 按 : 本文 借助 于 计算 机 符号 处 理 的 能 力 来 把 握 序 列 中 不 同 碱 基 的 丰 度 特征 , 从 而 进行 了 利用 数理 统计 方法
的 分 类 研究 而 后 引入 相关 度 分 类 判别 算法 及 反馈 机 制 来 比较 碱 基 的 相对 位 置 , 在 既定 方向 上 颇具 新 意 地 把 工作
推 向 深入 不 足 之 处 在 于 , 未 能 使 用 相关 度 工 具 对 各 类 样本 分 别 进行 分 析 ; 此 外 “ 纯 数 学 "必须 与 其 他 学 科 紧 密 结
合 才 会 有 优秀 的 建 模 工 作 , 本 文 虽然 对 编码 氨基 酸 的 三 联 体 进行 初步 探讨 , 着 墨 处 自 是 轻 淡 许 多
3 1994-2008 China Academic Journal Electronic Publishing House. All rights reserv http://www.cnki.net

<!-- source_page: 9 -->

第 31 卷第 1 期
数学的实践与认识
V o l131 N o 11
2001 年 1 月
J an. 2001
M A TH EM A T ICS IN PRA CT ICE AND TH EO R Y
sequences. T he second is the p eriod ic p rop erty of the DNA sequences. T he th ird is tha t am oun t
of info rm a tion of the sequences. B y u sing th is m ethod, w e cla ssify the na tu re sequences and
a rtifica l sequences. A t la st, w e ana lyze the cha racteristic in th is m odel and con sider the
genera liza tion of th is m odel.

116024)

研

( 大连理工大学, 大连

交

冯 涛, 康吉吉雯, 韩小军
指导老师: 贺明峰

流

关于 D NA 序列分类问题的模型

编者按:

本文以统计方法提取样本特征, 以之作为BP 神经网络的输入, 用M A TLAB 中相应算法进行训

练. 然后用于解决本分类问题, 得到了较准确的结果. 本文提取特征时考虑较为全面, 在此基础上正确地运

摘要:

：
科

用了神经网络方法, 发挥了神经网络适用于非线性问题、具有自适应能力的优点. 思路清楚, 文字简练.
本文提出了一种将人工神经元网络用于DNA 分类的方法. 作者首先应用概率统计的方法对 20 个

已知类别的人工 DNA 序列进行特征提取, 形成 DNA 序列的特征向量, 并将之作为样本输入BP 神经网络进
行学习. 作者应用了M A TLAB 软件包中的 N eu ral N etw o rk Too lbox ( 神经网络工具箱) 中的反向传播 (Back
p rop agation BP ) 算法来训练神经网络. 在本文中, 作者构造了两个三层BP 神经网络, 将提取的DNA 特征向

号

量集作为样本分别输入这两个网络进行学习. 通过训练后, 将 20 个未分类的人工序列样本和 182 个自然序
列样本提取特征形成特征向量并输入两个网络进行分类. 结果表明: 本文中提出的分类方法能够以很高的

公
众

正确率和精度对 DNA 序列进行分类, 将人工神经元网络用于DNA 序列分类是完全可行的.

问题重述 ( 略)

1

DNA 序列由四个碱基 A 、T、C、G 按一定规律排列而成. 已知所给人工序列 1- 10 属

信

于 A 类, 11- 20 属于 B 类. 本题中, 我们的主要工作有两个:
1) 提取 A 、
B 两类特征;
)
2 以所提取 A 、
B 两类特征为依据, 把 20 个人工序列及 182 个自然序列分为 A 、
B 两类
( 可能存在同时不具有 A 、
)
B 两类特征, 不能归为 A 、
B 中任一类的序列 .

微

在本题中, 先以序列 1- 20 为依据, 提取出 A 、
B 两类序列的统计特征, 然后运用神经网
络中的 B P 网络对未知序列进行了分类识别.

2

模型建立的理论依据
神经网络是近年来发展的一种大规模并行分布处理的非线性系统[ 1 ] , 其主要特点有:
1) 能以任意精度逼近任意给定连续的非线性函数;
2) 对复杂不确定问题具有自适应和自学习能力;
3 ) 具有较强的容错能力和信息综合能力, 能同时处理定量和定性的信息, 能很好地协

调多种输入信息的关系.
传统的分类识别方法, 对于一般非线性系统的识别很困难, 而神经网络却为此提供了一

