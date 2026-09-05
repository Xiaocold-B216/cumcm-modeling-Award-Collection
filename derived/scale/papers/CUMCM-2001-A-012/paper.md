# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
EiEE
第 19 卷 ， 建 模 专辑 工程 数学 学报 Vol. 19 Supp
20024702 JOURNAL OF ENGINEERING MATHEMATICS Feb. 2002
文章 编号 :1005-3085(2002) 05-0035-06
Paxan 一 /办
血管 的 三 维 重建 -
可 人
徐 晋 (电子 工程 与 信息 科学 系 ) ， 刘 雪 峰 (数学 系 ) ， 柏 容 刚 (电子 了 王 与 全 下 系 )
指导 老师 : 罕 ” 斗 (数学 系 ) /一
(中 国 科 学 技术 大 学 ,合肥 230026) 】
编者 按 :本 文 分 析 了 每 张 切片 与 管道 曲面 的 交 线 是 一 族 圆 的 包 络 线 , 且 这 族 圆 中 刘 短 治 人 -几何 特性 ，
建立 了 相应 的 算法 ,将 中 轴线 拟 合成 Berier 曲线 ,并 用 两 种 算法 对 模型 进入 以 检验 ,六 夫 有 一 定 特色 。
摘 ， 要 :对 血管 的 三 维 重建 问题 ,我们 假定 血管 为 等 径 管 道 ,通过 分 析 录 Listy 哈 出 了 确定 其 管道 中 轴线 和 半径 的 数学
模型 一 -搜索 每 个 切片 截面 , 求 最 大 内 切 圆 ,该 内 切 圆 圆心 即 风 切 态 乱 笨 与 管道 中 轴线 的 交点 ,该 内 切 圆 半径 即 为
管道 半径 ,再 通过 拟 合 各 个 交点 求 出 轴 心 线 。 4\8
本 模型 中 ,我 们 确立 了 两 种 有 效 的 误差 分 析 方法 :并 由 此 发 现 由 于 中 轴线 与 切片 交角 过 小 会 使 结果 产生 较 大 偏
差 。 为 解决 此 问题 我 们 从 其 它 广 向 重新 对 血管 进行 切 抽 再 进行 处 理 求解 ,得 到 更 加 精确 的 结果 。
关键 词 : 血管 :等 径 管道 :旋转 切面 A Z o
分 类 号 : AMS(2000) 65D17 中 图 分 1 J0 42.1 文献 标识 码 : A
MY》
1 问题 重 述 ( 略 )
条 件 假 设 SN 站
1) .血管 的 表面 是 由 半径 固定 圆心 连续 变化 的 一 族 球 滚动 形成 的 包 络 面 。
2) .医学 上 ,血管 未 存 在 严重 扭曲 。
3). raspap Yorisi—cs .
AN / ” ~
2 问题 分 模型 建立
N
s 3 要 各 腿 设 油管 可 视 为 表面 是 由 球 心 沿 着 某 一 曲线 ( 称 为 中 轴线 ) 的 球 滚动 包 络 而 成 的 管
证 yt-
记
Welhscotsscaen ax 各 信道 有 如 FJ 属性 :
定理 ”等 径 管道 每 个 切片 的 轮廓 线 是 一 族 半 径 ,圆心 连续 变化 的 圆 的 包 络 线 ,而 这 族 圆 中
半径 最 大 的 圆 的 圆心 即 为 管道 的 中 轴线 与 切片 的 交点 ,半径 即 为 管道 半径 。
利用 这 个 定理 ,我 们 建立 模型 如 下 :
1 . 对 第 个 切片 , 求 其 轮廓 线 最 大 内 切 圆 的 半径 R, 与 圆心 Ci=0,1,，…99:
2) .由 R=ThSR, 确定 管道 半径 R;
3) . 将 各 圆心 C; 拟 合成 Bezier 曲线 ,此 曲线 即 为 管道 的 中 轴线 。
4) . 确立 误差 分 析 方法 ,提出 调整 算法 ,对 2) 3) 步 结果 进行 调整 。
3 ，@ 1994-2006C cademic Journal Electronic Publishing House. Allrights resei ttp://wn

<!-- source_page: 2 -->

ERi
有
36 工程 数学 学 报 第 19 0
3 ”模型 求解
1D .导入 数据 转换 存储 方式
为 方便 计算 , 先 将 Bmp 文件 用 程序 (本 文 使 用 Mathematica) 导入 计算 机 转换 成 三 维 矩 阵
存储 。
2). 求 截面 轮廓 线 上 各 点 的 坐标
由 “管道 中 轴线 与 每 张 切 片 有 且 只 有 一 个 交点 ”, 知 截面 为 单 连通 的 区 域 , 轮 廓 线 为 一 闭合
曲线 。 本 文 使 用 了 Matlab 的 edge 0) 函数 求 出 此 轮 席 线 。 由 于 数据 量 较 大 ,以 稀 确 矩阵 存 取 数
和 - 惟 ，
3) . 求 轮廓 线 最 大 内 切 圆 的 半径 与 圆心 的 算法 = 蛋
总 体 思想 : /二
在 截面 内 选取 一 定数 量 的 点 ass
的 一 个 Ne 图 的 半径 。 在 这 些
由 一 定数 量 的 点 确定 的 最 小 内 切 圆 中 半径 最 大 的 一 个 ,这 个 图 就 是 促 廊 线 的 最 大 内 切 圆 。
具体 步 又 : S\， N
确定 搜索 的 起 点 :在 00. bmp 的 截面 中 搜索 2 则
最 大 内 切 圆 的 圆心 不 会 离 起 点 太 远 ;管道 是 连续 的 ,所 匡 相信 调 层 的 轮廓 线 的 最 大 内 切 圆 圆心
的 距离 不 会 太 大 我 们 每 次 取 前 一 层 求 的 圆心 为 当前 必 搜 崇 的 起 点 ,在 小 范围 内 进行 搜索 ,得
到 所 求 。
对 100 个 半 钨 取 王 值得 到 管道 半径 : 局 R = 29.75
人 .由 国 心 坐标 求 中 心 轴 线 方程 及 畏 线 投影
TO 我 们 选取 Bezier 样 条 来 拟 侣 管道 中 心 轴线 ,得
到 中 轴线 的 侧 视图 二 1 :
4 ”模型 AT
方法 一 2
设 求 得 的 轴线 这 AS) ,血管 实际 轴线 为 mrw) 。
在 第 = 层 化 有 轮 廊 线 sfz) , 设 点 pfx,y, 了 位 于 sfz) 。
2
SA N D(r, p) =Min{Distance(p, q) } fg 位 于 rfs) )
] Sr 实际 轴线 ro () 的 距离 为 :
1N\) D(ro, p) =Min{Distance(p, g) } fg 位 于 rofs) )
H Drm, 中 恒 为 管道 半径 R。
Np =|D(r.p)- B)|
如 果 所 求 的 轴线 于 血管 轴线 相 吻 合 , 则 A = 0; 我 们 求 轮廓 线 *fz) 上 的 所 有 点 对 应 的 A
的 均值 EverageA7z) ;因为 点 较 多 ,每 隔 4 层 , 随 机 地 取 切 片 轮廓 线 *(z) 上 200 个 点 -
p(i,z) i=1,2,....,200;
Everaged (z) =- 二 2eror 2))
我 们 作 Everaged (2) - = 的 图 像 , 即 误差 分 布 图 ( 见 图 2) 。
3。 @ 1994-2006 China Academic Journal Electronic Publishing House. Allrights reserved. http:

<!-- source_page: 3 -->

ERi

i

EeEm
建 模 专辑 血管 的 三 维 重建 oa

分 析 图 像 可 知 :

1) .我 们 拟 合 的 中 轴线 rf(y 在 整个 = 轴 上 (0 <2 &99) 与 血管 的 实际 中 心 轴 基 本 相 吻 合 。

2) .尽管 所 得 的 差 值 没有 具体 的 几何 意义 ,但 是 如 果 对 不 同 层 的 差 值 进行 比较 ,可 发 现 中
轴线 的 拟 合 在 层 数 > <30 的 地 方 误 差 较 小 , 随 着 z 值 的 增加 ,误差 变 大 ,这 在 直观 上 是 可 以 理
解 的 : 当 z 增 大 时 ,轴线 与 x - ?平面 接近 平行 , 企 变 大 ,切片 上 容纳 的 信息 有 限 ,产生 较 大 误
差 。 且 易 知 > 接近 9%9 时 ,图像 如 下 ( 见 图 3) :

100 Q0 z
。 e
30 DRRRRRRES 50 人 多
™ Tee 一 SS
50 天 全 AN
一 ~ 人
一 MA
4 -一 。 一 、
| - 了 低
全 ?5 本 2 了 5 278 0 100 o 800 2sn 200 asn 400 ®
x=0.y- : 平面 的 投影 作 、 : 平面 的 投影
了 | 一
ae 二 ~ | 人 人
375 LA o [< TT 四 和
7 OX 1 从
人 / o 3 和
235 | ] 一 0 人
| 了 人 05 5
100 ”一 3 400 y 二
V- ? 平面 的 投影 三 维 透视 图
2 ] 图 1 “模型 求解 结果
2
人 ZE A
V¥/, 2 " Y
Q 网
1 ee
网 层
0 /20 40 60 80 区
图 2 误差 分 布 图
例如 :P 点 得 不 到 最 小 值 ,故此 处 的 误差 非 拟 合 误差 。

方法 二 :重建 截面 求 面 积

4 19 4. 0 i a m Jou El on is] mng u All T h 四 t WV
12 X

<!-- source_page: 4 -->

EgoE
38 工程 数学 学 报 第 19 7
六 - 一 Z=gg
了 ” . .
*
_ 图 3 轮廓 线 上 的 点 到 轴线 的 距离 -
由 得 到 的 管道 中 轴线 重建 100 张 切片 的 截面 图 像 ,与 原先 给 定 的 100 张 图 象 比较 。 设
N (为 原 先 给 定 的 第 ;截面 所 含 象 素 点 的 个 数 (可 视 为 面积 ) , Mi) 为 重建 管道 的 第 截面
所 含 象 素 点 的 个 数 , P( 为 重建 管道 的 第 1 截面 与 原先 给 定 的 截面 的 重 登 区 域 所 含 象 素 点 的
个 数 。 比 较 公式 为 多
A 人 -YXCO- 2 P(i) 一 SS
M(i)
6 \)
显然 ,A EORLD, TRTHTLA ALARE  OBURH H1 0oh h 2  BTESERT 0f 。 这 个 误
差 值 就 作为 评判 设计 的 模型 好 坏 以 及 进一步 修正 结果 的 标准 。 ，“ 了 =
由 管道 中 轴线 重建 = 截面 的 算法 : AX
对 = = 平面 ,把 中 轴线 上 = Er7- Ri+ 8 7 范围 内 的 所 有 全 点 投影 到 : ~/ 平面 上 ，
得 到 的 /2 R+ 17 个 投影 点 作 圆心 ,以 外 下 - (= - 中 为 寺 季 作 加 ,这 /2 R+ 17 个 加 重奏 所 形
成 的 图 形 即 为 重建 的 = = 1 的 截面 。 heS
我 们 通过 计算 得 到 了 第 30,40,50,60,70 层 的 重 息 必 象 。 分别 计 算出 :
A(30) =5.7%, A(40) =6.5%, A(50) =7.1%, A(60) =6.8%,A(70) =6.5 %;
由 于 计算 量 比较 大 , 仅 取 5 个 层 分 析 , 对 其 它 层 同 理 可 求 A (及 。
下 左 图 是 第 30 TO :
/\ ~
及 V
和 p 200 一 -一
2
可 本 wi { /
SELEEE ,
3 本 1 站 | HE 200 / .
本 1
2 1 | h, _
200 7 y ;
o 下 4 由 |
<SNA | |
YN GELME e
避 \ 站 :ao 260 380 下 四 上 HES
50 人 150200 £350
BEHEE 第 95 层 上 得 到 的 最 大 内 切 圆 的 圆心 (5 个 点 /
图 4 重建 截面 所 得 结果
由 上 右 图 可 知 , 用 中 轴线 方程 重建 的 截面 与 原 截 面相 比 ,在 凹 处 有 一 部 分 溢出 ,而 在 凸 处
有 一 部 分 没有 履 盖 。 分 析 这 种 现象 产生 的 原因 :例如 在 求 第 95 层 轮 廓 的 最 大 内 切 圆 圆心 时
得 到 了 5 个 点 :
7VL70,280) ,771,2857 ,172 ,2897 ,773 ,2937 ,{74,296}} R=29.614
BATHER—  5 00 LER 25 J7 1—S000 H 28, BRAI 5R JoK Ay U  oe B 0J2T3
« 1 Chin J 1 t 1C | hi 1 g T V tip: 于

<!-- source_page: 5 -->

建 模 专辑 血管 的 三 维 重建
值 , 显 然 偏离 了 中 轴线 ,理想 的 算法 应 该 是 将 几 个 同时 为 最 大 的 点 拟 合 , 得 到 样 条 四 线 , 在 样 条
遇 线 上 取 中 点 , 才 是 比较 合理 的 结果 。 我们 采用 下 面 的 方法 从 另 一 个 角度 修正 误差 。
模型 的 修正 :
分 析 误差 可 知 , 中 轴线 的 拟 全 在 切片 与 中 轴线 近似 重 直 的 时 候 , 拟 合 误差 小 。 由 此 ,我 们
考虑 根据 已 知 数据 ,在 其 它 方向 上 做 血管 的 剖面 。
xY=250
ad 为 轴 心 ,旋转 切面 ;
Z E(- co cq 人
y-250=tg(1) X(x-250) (0<t<Pi -从
E/0,997 全 \S
e ~. 全 /一
A 一 74
Wip; 一 ce 略 JR 中
了 J 了 天 } te 1
AR i
本 de 3 | | 的
机 钦
污 > 人 = LeplW In
ER  aa A 四
人 一、 TS S j
« 人 各
z00 T, 峙
~ Sam 人 2 四 au
~gf
fa's 全 an 和 )
:变化 时 ,产生 连续 的 带 醒 每 一 次 所 得 截面 与 血管 的 中 心 轴 线 近似 垂直 , 故 得 到 较 好 的
截面 近似 于 贺 形 ) ,这 有 利于 各 可 而 的 最 大 内 接 加 之 半 从 ,加 心 相 切 示意 图 及 投影 示
意图 如 上 。
e we 二 者 比较 如 下 ,其 中 Z1 为 调整 后 的 轴线 , 12 为
原 轴 线 : 2 V:
0
总 ——
4) —
s0 Le
s00 250 400
- v
图 6 模型 修正 后 所 得 轴线 的 侧 视图
直观 上 看 ,可 以 发 现 调整 之 后 ,所 得 的 中 心 轴 线 更 为 光滑 ,并 且 在 第 90 - 100 层 得 到 更 多
用 于
局 *

<!-- source_page: 6 -->

回 叶 这
人
40 工程 数学 学 报 第 19 T
有 效 数 据 。 我 们 用 误差 分 析 方法 二 ,对 调整 后 的 轴线 对 第 30,40,50,60,70 层 分 析 ,与 调整 前
比较 的 如 下 :
表 1 模型 修正 前 后 误差 比较 表
| sao | sn | so | so | Aro
调整 前 | 57% | 65% | 741% | 68% | 65%
调整 语 | 32% | 25% | ?7% | 30% | 32%
模型 的 优 缺 点 分 析
1) HBURARERRAEALHORIT BUTAT, JR PRYFRATT LI ARR AL 45  T730 0 JLT
特性 。 AA)
2) 错开 的 优点 是 对 得 线 扯 击 比较 大 的 情况 通过 这 轩 前方 向 ,可以 避 枯 和 pia
进行 求解 。 = )
3) ”通过 向 切片 所 在 面 投影 ,由 轴线 计算 截面 ,不仅 能 计算 误差 g; ~ atd
的 途径 。 &， )
4) 误差 分 析 的 方法 (一 ) 虽 不 能 够 测 出 误差 的 绝对 值 ,1 dns 单 ，
速度 快 ,适用 于 比较 几 条 轴 心 线 的 优 劣 。 从 ]
参考 文献 : 也
[1] 张 韵 华 . Mathematica 符号 计算 系统 实用 教程 [M] .合肥 :中国 科 学 ,1998
[2] 李 尚 志 . 数学 实验 [M]. 北京 :高 等 教育 出 版 社 ,1996
[3] 关 履 泰 . 计算 机 辅助 几何 图 形 设计 [M]. 北京 :高 等 教育 出 版 社 ,1999
[4] 本 天 本
[5] Barhill R E ,Riesenfeld R F. Computer Aidéd Geoh etric Design[M]. Academic Press New York ,1974
[6] FRaty , 骆 岩 林 - CE 13 Ser A Suppl. 1998 .87 - 90
| 到 Rebniding of Vessel
3 ，LIU Xuefeng, BAI Rong gang
一 一 Adviser: DOU Dou
PP of Science and Technology of China ，Hefei 230026)
r=4
Abstract : Mg blem of 3D rebuilding of vessel ,we consider vessel with constant radius and have built a model to calculate
the axis and Te .In this model we deal with each slice and get the inscribed circle with maximum radium , whose center
is justoh the axis of vessel and if s radium just vessel s radium.
] 1 ia nodél ,we have introduced two efficient way to analyse the error . We find that error increases when the angle between
the axis and the slice decreases. To handle this problem ,we cut the vessel in different direction，The result is good.
“IN :vessel; 3D rebuilding; constant radius
) 也 于
-2006 hi A 8 Journ | Ele 'on1 ubli h ng H Si A 1 gh TeSeTVe tt WA 2
) 模 大

