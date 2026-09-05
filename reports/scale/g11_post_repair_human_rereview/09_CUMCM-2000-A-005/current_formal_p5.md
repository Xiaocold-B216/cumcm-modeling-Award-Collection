# Current Formal Excerpt — CUMCM-2000-A-005 — source page 5

- Current body: `derived/scale/papers/CUMCM-2000-A-005/paper.md`
- Current body SHA256: `272BC28FCA3DF8069B06A102EB847BF285E515FBE39D50823F9832A430987E36`
- Current page segment SHA256: `7D8F862BB9FD79D0B07049BC34D0FB235FCB6C18037AD9DAE694D9E3EE7DB4F4`
- Extraction method: `STRICT_SOURCE_PAGE_MARKER_BOUNDARY`
- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`
- Repair page audit: `catalog/scale/g11_multi_route_formal_repair_pages.csv`

The block between the delimiters below is copied from the current `paper.md` substring. No human wording, OCR, rendering, or extraction was added in this stage.

<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->
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
<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->
