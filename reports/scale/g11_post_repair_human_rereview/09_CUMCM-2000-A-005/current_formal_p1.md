# Current Formal Excerpt — CUMCM-2000-A-005 — source page 1

- Current body: `derived/scale/papers/CUMCM-2000-A-005/paper.md`
- Current body SHA256: `272BC28FCA3DF8069B06A102EB847BF285E515FBE39D50823F9832A430987E36`
- Current page segment SHA256: `CB5B10C0BFBD02B71EE81606E23106D1DF64A1948C72702CA5CBDE96AF2CDB3A`
- Extraction method: `STRICT_SOURCE_PAGE_MARKER_BOUNDARY`
- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`
- Repair page audit: `catalog/scale/g11_multi_route_formal_repair_pages.csv`

The block between the delimiters below is copied from the current `paper.md` substring. No human wording, OCR, rendering, or extraction was added in this stage.

<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->
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
<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->
