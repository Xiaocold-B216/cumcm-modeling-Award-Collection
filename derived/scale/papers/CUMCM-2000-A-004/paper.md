# Extracted Paper

<!-- source_page: 1 -->

[Elkgis:
贿 V
sid
第 31 卷 第 1 其 数学 的 实践 与 认识 Vol31 NO 国 =
2001 年 ! 月 MATHEMATICS N PRACTICE AND THEORY Jan 200 7F
任意 选 出 比较 多 的 (为 了 保证 较 高 的 准确 性 ), 利用 keyword 作为 分 类 标准 , 然后 利用 本 文
提供 的 加 权 系 数 的 确定 方法 就 可 以 定 出 一 个 具体 的 定量 标准 具有 一 定 实用 价值
参考 文献
[1] 李 涛 , 贺 勇 军 等 MATLAB 工具 箱 应 用 指南 一 一 应 用 数学 篇 电子 工业 出 版 社 .
[2] 袁 亚 湘 最 优化 方法 科学 出 版 社 .
[3] 张 妃 孝 , 玫 宗 燕 数据 结构 一 e+ + 与 面向 对 象 的 途径 “高教 出 版 社 .
[4] 汪 仁 官 概率 论 引 论 北京 大 学 出 版 社 .
[5] 陈 家 易 , 孙 山 泽 等 数理 统计 学 讲义 高 教 出 版 社 . = 7
一 W
和
了
The Grouping of DNA Sequences
SS
YANG Jian, WANG Chi, Kong
(Peking U niversity, “EaK”
了 o
X -
Abstract 了 this paper, amethod to classify the os is proposed M athem atical
methods such as statistics and op tm izaton are used to build the model The data is analysed
sufficiently and the“critical words”is got,gv hich can represent the characteristics of each
group. According to this, a quantijgtive gtandagg) for grouping is brought forward Thismodel
can properly classify the given da foth ough testing First the stringsw hich appear repeatedly
(called words) in the given data afe [全 局 out The standard frequency and dispersion for
each word are calculat nd，using the Least Squares method，the priority function is
fixed Through stepw 四 tindzation, the coefficients are made stable Third, the key words
are selected out and ce eweight according to the priority function Atlast，using the
“analyse hierarchy-process”’, the undetem ined data is classified This method can classify the
undetem ined data;( 21—No. 40) fairly well, it can also give good result for the last 182
0
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
3 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved  http://www.cnki.net

<!-- source_page: 2 -->

加
赔 生 9

1 其 韩 轶 平等 :DNA 序列 的 分 类 9 wm

摘要 : 本文 对 A 题 中 给 出 的 DNA 序列 分 类 问题 进行 了 讨论 “从 “不 同 序列 中 碱 基 含 量 不 同 "入 手 建立 了

欧 氏 距离 判别 模型 , 马 氏 距离 判别 模型 以 及 Fisher 准则 判定 模型 ; 又 从 “不 同 序列 中 大 基 位 置 不 同 "入 手 建立

了 利用 序列 相关 知识 的 相关 度 分 类 判别 算法 , 并 进一步 研究 了 带 反馈 的 相关 度 分 类 判别 算法 “对 于 题 中 所

给 的 待 分 类 的 人 工序 列 和 自然 序列 , 本 文 都 一 一 作 了 分 类 接着, 本 文 又 对 其 它 各 种 常见 的 分 类 算法 进行 了

讨论 , 并 着 重 从 分 类 算法 的 稳定 性 上 对 几 种 方法 作 了 比较
1 问题 的 重 述 ( 略 )
2 模型 的 条 件 和 假设 ( 略 ) -从 >
3 符号 约定 2XG \)

na: 任 一 给 定 序列 中 碱 基 A 的 百 分 含 量 H

ng: 任 一 给 定 序列 中 碱 基 G 的 百 分 含 量 ;

nt: 任 一 给 定 序列 中 碱 基 T 的 百 分 含量 ; As

nc: 任 一 给 定 序列 中 碱 基 C 的 百 分 含量

Gi 由 某 些 具有 相同 属性 的 个 体 组 成 的 类 RK
4 问题 的 分 析 和 解答
4.1 概述

根据 题 意 , 我 们 首先 要 提取 出 列 的 特 征 , 然后 给 出 它 的 数学 表示 , 最 后 选择 并 构
总 关 NE KE 人 ow 序列 , 我 们 认为 , 反映 该 序列 特
征 的 方面 有 两 个 : 人 |

1. 碱 基 的 含量 ， 的

2. 碱 基 的 排列 情况 , J5 现 澡 该 序列 的 形式
4.2 ”基于 碱 基 含 量 特 征 分 类 的 模型

首先 ， 2 的 含量 百分比 作为 该 序列 的 特征 这 样 的 抽
L, ig 物 学 的 意义 前 面 提 到 过 , 在 不 用 于 编码 蛋白 质 的 序列 片断 中 ,4 和
T Hyrg AlLe, 因此 以 某 些 碱 基 特 别 丰富 作为 特征 去 研究 DN4 序列 的 结构 是 具有 可
fr 的 足 下 的 4 ,G,T,C 的 含量 百分比 分 别 记 为 naa, ng, nt, ne, 则 得 到 一 组 表征 该 序
IES 征 的 四 给 向 量 (na， ng, nt, nc). 考虑 到 na, mb ng,nc 线性 相关 (nat ng+ ntt mc= 1)， 所
1y 我 们 采用 简化 的 三 维 向 量 (we, wp mg) 来 进行 计算 对 于 标号 为 ;的 序列 , 记 它 的 特征 向 量
为 江 ;， 显 然 , 任意 序列 的 特征 向 量 与 一 个 3 维 空间 的 点 对 映

一 般 的 判别 问题 为 : 设 有 大 个 类 别 Gu Ga, …, Go 对 任意 一 个 属于 G, 类 样品 x, 其 特征
向 量 X 的 值 都 可 以 获得 现 给 定 一 个 由 已 知 类 别 的 一 些 样品 xu xz, …,x* 组 成 的 学 习 样
本 , 要 求 对 一 个 来 自 这 大 个 类 别 的 某 样品 x*, 根据 其 特征 向 量 X 的 值 作出 其 所 属 类 别 的 判
[8

在 本 题 DNA JFFHIKP k=2,G1=4,Go= B, FFIEMIE x 是 三 维 的 学 习 样 本 共 包
含 w= 20 个 样本 , 其 中 10 个 属于 4 , 10 个 属于 B3， 我 们 分 别 采 用 了 欧 氏 距离 (Euclid) 分 类 模
型 马 氏 距离 M ahalanobis) 分 类 横 型 和 Fisher 判别 模型 来 对 序列 样本 分 类

<!-- source_page: 3 -->

加
BeF
40 数学 的 实战 与 认识 1 tien
4.2.1 欧 氏 距离 (Euclid) 分 类 模型
在 欧 氏 距离 (Euclid) 分 类 模型 中 , 把 每 个 样本 视 为 三 维 空间 的 一 个 点 , 以 其 到 不 同 集合
几何 中 心 的 欧 氏 距离 作为 判 据 有 具体 的 算法 如 下 :
1. 计算 属于 A 类 与 属于 B 类 的 10 个 样本 点 的 集合 各 自 的 几何 中 心 :
Ci = pNe Cs = oXx
2. WTAERIREA H x , 分 别 计 算 该 点 到 cv MBRIREEB D.= 区 CC | 以 及 该 点 到
Cs 的 欧 氏 距离 ps= 区 -= cs 上 一
3. 判别 准则 如 下 : -从 》
(1) 若 D< Do, 则 将 X ,点 判 为 A 类 ; = 蛋
(2) 若 D4> De, 则 将 站 点 判 为 B 类 ; 2XG
(3) 若 Di= De, 则 将 并 ,点 判 为 不 可 判 类 ; 同一
用 上 述 算法 对 已 知 样 学 习 样 本 A 1 一 A 20 进行 分 类 , 结果 是 除了 A 4/ 被 错误 的 分 到 了 B
类 外 , 其 余 的 19 个 样本 全 部 正确 , 分 类 准确 率 达 到 95%. VA NS
用 上 述 算法 对 未 知 的 人 工序 列 A 21 一 A 40 | 的 结果 是 :
A %:22,23,25,27,29, 30, 32, 34, 35, 36, 37, 3 器 /1B > 闫 \21, 24, 26, 28, 31, 33, 38, 40
用 上 述 算法 对 未 知 的 自然 序列 N 1—N 182 人 到 的 结果 见 附 录 ( 略 )
用 欧 氏 距离 作为 判 据 虽 然 简便 直观 , 但 存在 着 明显 的 缺陷 : 从 概率 统计 的 角度 来 看 , 用
欧 氏 距离 描述 随机 点 之 间 的 距离 并 不 好 图 此 当 待 分 类 样本 是 随机 样本 ， 具有 一 定 的 统计
HRE, BTRIT ERAHE) 随机 塌 之 间 的 接近 程度
4.2.2 wa A
2 我 们 采用 马 氏 距离 来 代替 欧 氏 距 离 改进 后 的 算法
如 下 :
设 : 二 人 ad 让 加 (us ,me), 协 方差 矩阵 为 非 奇异 阵 户 xs， 则 三 维 样本 区
到 总 体 G 的 马 本 座
% an ,@)={ KTCG- p)
2 可 用 学 习 样 本 的 均值 来 代替 , 协 方差 矩阵 可 用 学 习 样 本 的 样本 协 方差
AN 来 代 蔡 一
<》 网 吕 区 刘 识 用 于 尖 别 模型 迹 特 判 据 如 下
] 人 LN 天 mw CC4)< dm (x,B), WHEx 为 A 类 ;
|N), Fidm (X ,4)> dm (X,B), WHE x 为 B 类 ;
3. Fdm (X,4)=dm (X,B), WHIE x 为 不 可 判 类 ;
用 上 述 算 法 对 已 知 样 学 习 样本 A 1 一 A 20 进行 分 类 , 结果 是 除了 A 4 被 错误 的 分 到 了 B
类 外 , 其 余 的 19 个 样本 全 部 正确 , 分 类 准确 率 达 到 95%.
用 上 述 算法 对 未 知 序 列 A 21 一 A 40 进行 分 类 , 得 到 的 结果 是 :
A 类 : 22, 23, 25, 27, 29, 30, 32, 33, 34, 35, 36, 37
B 类 : 21, 24, 26, 28, 31, 38, 39, 40
) 用 上 述 算法 对 未 知 的 自然 序列 N 1—N 182 进行 分 类 , 得 到 的 结果 见 附录 . ( 略 )

<!-- source_page: 4 -->

加
三 辣
1 期 韩 轶 平等 :DNA 序列 的 分 类 1 mm
4.2.3 Fisher 准则 分 类 模型
在 多 维 空间 里 分 类 的 方法 不 仅仅 是 距离 分 类 法 一 种 , 常用 的 Fisher 分 类 法 就 是 另 一 种
基于 几何 特性 的 分 类 法 在 距离 判别 模型 中 , 三 维 空间 的 样品 莹 被 映射 为 一 维 的 距离 ! 来
作 判 断 Fisher 分 类 法 的 思想 也 是 把 三 维 空间 的 样本 映射 为 一 维 的 特征 值 y, 并 依据 ” 来 进
行 判别 有 具体 的 作法 是 先 引 入 一 个 与 样本 同 维 的 待定 向 量 w 再 将 ， 取 为 蕊 坐标 的 线性 组
合 y= wx 而 wx 的 选取 要 使 同一 类 别 产生 的 尽量 聚拢 , 不 同类 别 产生 的 尽量 拉 开
这 样 , 我 们 便 可 将 样品 过 到 某 一 类 cG 的 距离 定义 为 y>= wx 与 yc= wec 之 间 的 欧 氏 距离 :
LX,G)= [y- yc 上 上 lc- o) | #7
其 中 < 为 G 的 几何 中 心 =
Fisher 分 类 的 判 据 为 国 由
1 车 5 OA)<L CC,8)， 则 判定 x 为 4 类 2
2HL (X,4)>L (X,B), WHEx 为 8 类 ;  ud
3FL(A)=1 CC,B ), 则 判定 x 为 不 可 判 类 p XS
根据 对 x 的 要 求 , Fisher 提出 了 比较 有 效 的 选择 算法 , 利用 该 饼 法 , 从 学 习 样本 中 获得 :
u= (03365, - 0 087, 0 9377)7 人
ZK,4)= |0.3365 (na- 02860)- Q 087 (n Ka + 09377 (ng- Q 3830) |
L(X,B)= [0.3365" (na- Q 2940) - Q 087 (nf- 0.5010) + Q 9377" (ng- Q 1010) |
用 上 述 算法 对 已 知 样 学 习 样本 A 1 一 A 20 进行 分 类 , 结果 仍然 是 除了 A 4 被 错误 的 分 到
了 B 类 外 , 其 余 的 19 个 样本 全 部 正确 , 分 类 崔 确 率 达 到 95%.
对 于 未 知 序 列 A 21 一 A 40 进行 分 粕 得 到 的 结果 是 :
A %:22,23,25,27,29,34,35,36, 和 类 : 21, 24, 26, 28, 30, 31, 32, 33, 38, 39, 40
用 上 述 算法 对 未 知 的 自然 序列 N 1- 有 182 进行 分 类 , 得 到 的 结果 见 附录 . ( 略 )
4.2.4 三 种 距离 分 类 模 下
这 三 种 模型 在 分 类 结 中 :有 一 定 的 区 表 1
别 , 对 于 序列 A30332 江 33 及 A39, 三 种 RAR URATA
7 的 册 了 不 同 且 到 Ps ， 人
 Tagp ginms—twan ， \ .
sEAI 24 和 当 三 种 分 类 法 结 ， ， 。
果 完 全 -| 敦 困 X 人 为 它 判 别 有 效 若 不 然 。 和 ，
当 呈 种 分 类 法 结果 不 一 致 时 , 认为 该 序列 —— —
称
忌 对 于 三 种 方法 都 无 法 正确 分 类 的 A 4 序列 , 可 认为 是 异常 情况 , 不 影响 算法 的 性 能
4.3 ”基于 碱 基 位 置 特征 分 类 的 横 型
虽然 上 述 采用 碱 基 A ,T,G,C 在 DNA 序列 里 的 含量 作为 该 序列 的 特征 的 方法 有 一 定
的 生物 学 意义 并 且 在 DNA 序列 的 分 类 中 获得 了 比较 理想 的 结果 但 是 ,用 这 种 方法 抽取 特
征 , 没有 充分 体现 碱 基 排 列 的 信息 量 , 仅仅 考虑 碱 基 含 量 并 没有 体现 碱 基 在 序列 中 的 排列 情
况 例如 ,序列 ATGC) 与 序列 (CGTA ) 有 着 相同 的 碱 基 含量 , 他 们 的 特征 向 量 是 完全 一 样
的 , 并 不 能 体现 在 排列 结构 上 的 不 同 因此 ,直接 从 序列 本 身 的 碱 基 排列 顺序 来 考察 序列 就
成 为 “种 更 加 合适 的 提取 特征 的 方式 因此 采纳 数值 序列 中 的 相关 性 分 析 设计 了 算法
© 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved. — http://www.cnki.net

<!-- source_page: 5 -->

[ERfiaE
天
42 数学 的 实践 与 认识 1
通常 任意 两 个 数值 序列 的 相关 性 都 是 通过 这 两 个 序列 的 相关 函数 来 刻画 的 ”由 于 本 题
中 的 DNA 序列 是 非 数值 的 序列 , 同时 无 法 将 碱 基 按 通常 的 方式 进行 数值 化 , 因而 刻画 任意
两 个 序列 的 相关 程度 的 变量 需要 重新 定义
4.3.1 定义 一 : 相关 运算 “@ ” 表 2
对 于 任意 碱 基 放 和 六 相关 运算 儿 Dn" 的 值 @ AAA oo T c
由 表 2 定义 : A 1 0 0 0
4.3.2 定义 二 : 哑 元 O G 0 1 0 [4
除 四 个 碱 基 外 , 我 们 另行 定义 一 个 哑 元 o, 规 工 0 0 #7 0
定 任意 碱 基 与 哑 元 作 相关 运算 的 结果 都 为 0Q C 0 0 一。 SN
4.3.3 “定义 三 : 序列 的 延 拓 一 \
对 于 任意 一 个 长 度 为 Y 的 序列 4 (其 中 0< 2XG
<N), 定 义 它 的 延 拓 为 如 下 一 个 无 限 序 列 : / H
AjMO0<j<N 时 ,47=4 当 - o©<j<0kN <j<pi “ /0.
即 在 该 序列 的 左右 两 端 均 用 哑 元 O 填充 WAs
4.3.4 定义 四 : 序列 的 相关 度 g \¢
对 于 任意 的 两 个 序列 4 v,Bw， 定 义 序列 4 wb) ” 目 关 序 列 9 ， 为 :
- J\
Si= YAL:@Bi (0< i<Sem-n
定义 序列 下 对 序列 4 的 相关 度 为 : ”个
5 OZ i<n+tm- 1)
例如 对 于 序列 4 re erero 相关 序列 及 相关 度 的 计算 步 又
如 下 : _
本 .第 广 项 So= 420B 0= TO4= 0
471 了 4 站 人 -| A 卫 4 4 4% 4 4 4 和
h O 一 一 ” C T O O O O O O h
h O O O A G 了 C 了 C O h
h Bi3 7 Bl1 Bi 万 十 万 二 万 于 万 让 B3 B h
=A
\\ A 第 二 项 Si=414DO8o+4298i= TOG+ CO4= 0
h 下 1 了 4 了 1 了 站 Af Al 4 到 了 4 村 A3 有 二 A7 h
. 0 O 了 C 工 O O O O O h
以 > O O O A G 了 C T C O
一 Bi3 万 2 Bl1 Bi Bi 万 二 万 于 万 让 B3 B h
第 三 项 :82= 4 0OB ot 4 IOBI= TOT+ GOc+4OT= 1
h O O O 工 C 工 O O O O h
h O O O A G T c T C O h
h Bi3 万 2 Bl1 Bi Bi Bi Bi 万 让 B3 B h
以 下 类 推 得 ( 表 略 ):
第 四 项 :8Ss=40@Bi+41I9p:+4298:=TOc+ COT+ TOG=0

<!-- source_page: 6 -->

加 天
1 期 韩 轶 平等 :DNA 序列 的 分 类 3 - 机
BHI:Sa=40OB2+ 4 1OB3+4:0B:= TOT+ COC+ TOT= 3
第 六 项 :SSs=40@83+41984+4298:=TOCc+ COT+ TOC= 0
第 七 项 :Se=4o@p84+4198:= COc+ TOT=2
第 八 项 :8S)=40@B8:=TOCc= 0
第 八 项 :8S7= 4o98s= TOC= 0
0 O O O O O O O O 工 C 人
0 O O O A G 了 C 了 C bg we
贸 Bis Bi :1 万 让 Bi B3 Bi Bi Bi BifaT …
- { \"4
o SS
两 序列 的 相关 度 为 S= MAX (S.}= Se= 3 _ 由
4.3.5 定理 一 : 任意 给 定 三 个 序列 S,A,B, 若 A 与 S 多 相关 度 大 于 色 信 的 相关 度 且 B 与
A 等 长 , 则 A 5s 属 同一 类 的 可 能 性 大 于 B 5s 属 同一 类 的 可 能 性 厅
4.3.6 基于 相关 度 的 分 类 算法 : /
利用 上 述 概念 ， 一个 了 关内 人 类 :
1. XTFPHIA 21—A 40,N 1—N 182 中 的 任意 一 全 序列 | 将 其 与 序列 A 1 一 A 20 中 的 每
人
2. 对 于 前 十 个 相关 度 , 求 出 它们 的 平均 相关 度 SASS (SS1+ SS2+ ……SS10) /10, 并 定
义 其 为 与 A 类 的 相关 度 ;
3. 对 于 后 十 个 相关 度 , 求 出 它们 的 平均 相关 度 SB= (SS11+ SS12+ ……SS20)V/10, 并
定义 其 为 与 B 类 列 的 相关 度 ; 作 1 9
4. 记 W = near
若 W > 1, 则 将 X 点 判 为 A_ 类 ;
若 W< 将 RE
若 W= 1, 则 将 X 点 阁 Ms
5.W 可 作为 衡量 该 序列 分 类 的 可 信 性 的 一 个 标准 “显然 当 W 越 接近 于 1, 该 序列 与 A
基 的 相关 性 和 器 必 关 久 相关 性 区 到 六 让， 分 类 结果 就 越 不 可 信 ; 反之 ,W 与 1 差 的 越 远 ，
2 关 竹 和 与 B 类 的 相关 性 区 别 就 越 小 , 分 类 结果 就 越 可 信 ”这 个 变量 对 我
们 下 面 (& a 相关 度 分 类 算法 具有 重要 的 意义
由 用 k77 对 已 知 样 学习 样 本 A 1- A 20 进行 分 类 , 得 到 的 结果 是 分 类 完全 正确 ,A ,B
ER 准确 率 达 到 100%.
TAR 21 一 A 40 进行 分 类 , 得 到 的 结果 是 :
类 : 22 23 25 27 29 34 35 36 37
B 类 :21 24 26 28 30 31 32 33 38 39 40
用 上 述 算法 对 未 知 的 自然 序列 N 1—N 182 进行 分 类 , 得 到 的 结果 见 附录 ( 略 ) .
4.3.7 相关 度 分 类 算法 的 改进 一 一 带 有 反馈 的 分 类 算法
上 述 的 相关 度 分 类 算法 是 一 次 性 学 习 过 程 , 学 习 的 过 程 只 体现 在 学 习 样本 的 过 程 中 , 而
在 对 未 知 样本 分 类 的 过 程 中 没有 对 已 分 类 情况 作出 修正 , 即 是 属于 无 反馈 型 的 学 习 然而 ，
采用 反馈 型 的 学 习 过 程 会 有 更 好 的 分 类 结果 一 般 说 来 , 带 反 馈 的 算法 以 神经 网 络 算法 最
县 有 从 表 性 但 对 于 一 般 的 分 类 算法 而 言 , 可 以 采用 多 次 反复 分 类 的 办 法 来 实现 反馈 的 目
© 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved  http://www.cnki.net

<!-- source_page: 7 -->

加
人
44 数学 的 实践 与 认识 1 tien
的 “针对 上 述 的 相关 度 分 类 算法 ,我 们 设计 了 如 下 带 反馈 的 相关 度 分 类 算法 :

1. 对 全 部 182 个 样本 进行 相关 度 分 类

2. 计算 全 部 182 个 W 的 值

3. 在 所 有 被 判 为 A 类 的 待 分 类 序列 中 , 取出 W 值 最 大 的 一 个 , 作为 标准 学 习 样本 , 加
入 到 A 类 的 标准 样本 中 ( 若 有 多 个 , 则 全 部 加 入 到 A 类 中 , 若 无 被 判 为 A 类 的 序列 , 则 保持
A 类 标准 学 习 样本 不 变 )

4. 在 所 有 被 判 为 B 类 的 待 分 类 序列 中 , 取出 W 值 最 小 的 一 个 , 作为 标准 学 习 样 本 , 加
入 到 B 关 的 标准 样本 中 ( 若 有 多 个 , 则 全 部 加 入 到 B 类 中 , 若 无 被 判 为 B 关 JRWP
B 关 标 准 学 习 样本 不 变 ) LA

5. 重复 对 剩余 的 待 分 类 序列 进行 相关 度 分 类 , 并 按 上 述 步 又 不 断 扩 充 震 汶 学 习 样 本 ，
直至 全 部 的 待 分 类 序列 都 被 加 入 到 标准 学 习 样本 中 名

我 们 用 新 算法 编程 对 182 个 序列 进行 了 重新 分 类 , 得 到 了 an
结果 , 而 且 新 的 分 类 结果 的 W 值 明显 与 1 离开 的 更 大 , 这 使 我 清理 由 相信 , 反馈 对 算法 的
性 能 有 一 定 的 改进 WANs
S 进一步 研究 的 问题 X
5.1 基于 生物 学 的 特征 抽取

我 们 上 述 的 两 种 特征 抽取 方法 更 多 的 是 从 纯 数 学 眼光 来 研究 序列 的 特征 除 此 之 外 ，
我 们 还 可 以 考虑 DNA 序列 在 生物 学 意义 的 数学 特征

一 个 此 世 窜 史 考 上 到 的 方面 5 联 体 在 DNA 序列 中 的 出 现 ”由 于 具有 三 联 体形 式
的 遗传 密码 子 对 蛋白 质 的 合成 具 押 人 gateFaniaeaTe
列 的 本 质 特征 ” 题 中 没有 明确 的 措 明 所 络 的 序列 是 全 序列 还 是 序列 片断 ,我 们 无 法 对 三 联
体 在 序列 中 的 出 现 位 置 进攻 ,种 代 蔡 的 方法 是 将 序列 假定 为 全 序列 , 从 第 一 个 碱 基 开
始 三 个 三 个 一 组 的 划分 为 上 间 村, 然后 统计 64 个 密码 子 的 出 现 概率 , 形成 64 维 的 向 量 再
使 用 距离 分 类 等 模型 = 或 利用 生物 学 的 知识 先 将 64 维 向 量 的 某 几 维 合并 , 降 维 后 再 分 类
开本 叶 生 六 人 类 六 法 比 信也 加 了 的 划分 一 位 碱 基 的 缺失 或 错位 均 会
这 成 分 类 地 所 以 必须 加 以 修改 , 一 条 思路 是 尝试 将 序列 移 一 位 或 二 位 再 划分 密码 子 , 由
于 时 间  » SAA
5.2 人 ah
Se gone 随 着 计算 机 速度 提高 被 广泛 应 用 “对 于 本
有 we 人 ae 0

MUE 对 于 基于 碱 基 含 量 的 特征 向 量 (uc, no we), 构造 了 如 下 的 反 向 传播 算法 :

1. 网 络 简单 的 分 为 两 层 , 一 层 为 输入 层 , 有 3 个 单元 ,分别 为 权重 w 5 一 层 为 输出
层 , 有 1 个 单元 ,为 判别 结果 ; 各 单元 均 为 Signoid 型 函数 激励

2. 设 定 (o, 轧 o) 的 初 值 为 (0, 0. 0);A 美学 习 样本 的 标准 输出 定 为 :B 类 学 习 样本 的 标
准 箱 出 定 为 0

3. 对 每 一 个 学 习 样本 , 计算 S= uv na+ b* ntt cv ng 作为 输出

4. 将 学 习 样本 的 标准 输出 与 8 相 减 , 所 得 的 差 用 来 指导 权重 的 改变 , 权重 的 改变 遵从
w idrow -Hoff 准则

<!-- source_page: 8 -->

加 ;如
人
1 期 韩 轶 平等 :DNA 序列 的 分 类 5 mm
5. 反复 学 习 样本 , 到 权重 值 稳定 收敛
6. 代入 竺 分 类 样本 , 分 类
用 上 述 算法 所 得 到 的 结果 与 普通 的 分 类 模型 没有 区 别 事实 上 当权 值 稳定 收敛 后 ,S=
ar na+ b* ntt c* ng 就 是 特征 空间 的 一 张 ( 超 ) 平 面 , 从 这 一 点 来 说 , 人 工 神经 网 络 模型 与
一 般 的 距离 分 类 模型 得 到 的 结果 没有 两 样 考虑 到 人 工 神经 网 络 模型 还 存在 结果 对 初 值 有
较 强 敏感 性 , 缺乏 选择 理想 步 长 的 准则 和 收 和 剑 性 等 问题 , 在 一 定 的 时 间 内 , 我 们 无 法 较 好 的
解决 这 些 问 题 , 所 以 我 们 也 没有 作 进一步 讨论
6 ”算法 的 稳定 性 -从 >
前 面 比 较 算 法 的 时 候 , 兽 多 次 提 到 分 类 算法 的 稳定 性 问题 分 类 钴 夫 的 篇 虽 竹 是 除了
算法 的 成 功率 之 外 的 习 一 较 重 要 的 指标 人
轻微 变化 时 作出 正确 判别 的 能 力 对 于 本 题 , 是 指 算法 在 样本 席 列 发 生 卫 轻微 的 碱 基 缺 失 ，
错位 , 错 排 情况 时 作出 正确 判别 的 能 力 5 A 序列 粗 粒 化 和 模
型 化 的 问题 , 所 以 分 类 时 是 对 序列 的 整体 特征 进行 区 分 局 部 碱 基 揭 组 成 变化 应 该 对 算法
的 分 类 结果 没有 影响 我 们 所 提出 的 几 个 模型 均 较 2
参考 文献: 3
[1] 和 孙 刀 恩 , 孙 东 旭 , 朱德 隐 《分 子 遗 传 学 》 南京 大 学 出 版 社 , 1996.
[2] 白 其 峰 .《 数 学 建 模 案例 分 析 》 海洋 出 版 社 , 2000. @
[3] 潘 德 惠 《数学 模型 的 统计 方法 》 辽宁 和 党 技术 出 版 入 986-
[4] 净 平 凡 , 黄 端 旭 《人 工 神经 网 络 》 安放 社 , 1991.
[5] 李 振 刚 《分 子 遗传 学 概论 》 中 国 科学 按 采 县 19%.
[6] DuaneHanseiman.BruceL ittlefield (M asteringMATLAB: a comprehensive tutorial and reference》 Prentice Hall,
1996. JS
~ 一 上
) ssitication of DNA Sequences
一
Y HAN Yiping， YU Hang， LIU Wei
他 (ZhejiangUniv ，Hangzhou 310027)
以 >
SN This paper proposes severalmethods for the classification of DNA sequences We
noticed that different sequences have different alkali radicals and therefore set up models using
Euclidean distance, M ahalanobis distance and Fisher princple We also noticed that different
sequences have different pemutations of alkali radicals and an algorithm using relativity
analysis is proposed Further we discussed a relativity analysis algorithm w ith feed-back
mechanism. As to the naturaland artificial data given our algorithm swork welland fine results
are given At last several other common algorithm s are compared, especially on their
stabilities
23 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved. — http://www.cnki.net

