# Current Formal Excerpt — CUMCM-1999-B-003 — source page 6

- Current body: `derived/scale/papers/CUMCM-1999-B-003/paper.md`
- Current body SHA256: `5AF0061C03FA255BA04B35F28021E9090E4CDF772FF87BCB7E617B6A4A634CF9`
- Current page segment SHA256: `C9829109AC7FFF5305D92EDD2E731644F658C6F7CF70B95C5A0B2DA7DF4FB425`
- Extraction method: `STRICT_SOURCE_PAGE_MARKER_BOUNDARY`
- Repair route: `DOC_EXISTING_EXTRACTION_RECONSTRUCTION`
- Repair layer: `G11_MARKER_ONLY_PAGE_LOCAL_FORMAL_BODY`
- Repair page audit: `catalog/scale/g11_multi_route_formal_repair_pages.csv`

The block between the delimiters below is copied from the current `paper.md` substring. No human wording, OCR, rendering, or extraction was added in this stage.

<!-- BEGIN EXACT CURRENT PAPER.MD SUBSTRING -->
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
<!-- END EXACT CURRENT PAPER.MD SUBSTRING -->
