# Extracted Paper

<!-- source_page: 1 -->

口 | 到 口
第 20 卷 第 7 期 工程 数学 学 报 Vol.20 No.8 aa
2 年 32 月 JOURNAL OF ENGINEERING MATHEMATICS Po
文章 编号 :1005-3085(2003)07.0063.06
答 2
露天 人 矿 生 产 的 车 辆 安排
丁 余 良 ， 胡 海 林 ， 郭 丽 君 _
指导 教师 : 李 新 秀 一 和 伏 》
(南京 邮电 学 院 ,南京 210003) =\)
编者 安 ; 本 文 模型 完整 正确、 叙述 清楚 严格 ,求解 方法 可 行 ,结果 准确 ,对 内 :Asons
是 一 篇 优秀 论文 。 此 外 本 文 还 讨论 了 有 关 几 种 等 待 的 情况 , 昌 末 宕 妥 解决 /但 已 属 不 易 。 缺 点 是
本 文 不 太 精炼 ,此 处 已 作 删 节 . NS
摘要 ; 本 文 研究 了 锅 天 矿 生 产 的 车 辆 安排 最 优化 问题 。 利 用 宝 要 月 标 法 将 允 目 标 最 优化 问题 转化 为 音
目标 最 优化 问题 ,根据 主要 目标 (总 运 量 ) 列 出 最 小 用 寺村 最 小 卡车 到 符 化 为
条 件 ,然后 逐步 简化 ,将 非 线性 规划 转化 为 线性 整 妆 拓 爷 s 并 适 过 SAS 软件 编程 遍历 120 个 线性
规划 子 问题 ,经 过 比较 得 出 最 优 解 .最 后 在 最 优 解 基础 上 运用 贪心 算法 求 出 所 用 的 最 少 卡 车 数 并
给 出 了 一 个 班次 的 运输 方案 。 对 于 问题 一 ,得 到 最 小 总 运 为 85628 62 吃 公里 ,此 时 7 台电 久 分
别 放 在 第 1.2.3.4,8.9,10 名 点 ,后 庆生 最 少 鸭 13 辆 。 对 于 问题 二 ,利用 类 似 于 问题 一 的 解法 ，
在 充分 和 用 现 有 卡车 和 铲 车 的 条 佬 有 有 人 博得 最 大 的 产量 为 103334 吨 、20 辆 车 完全 利用 ,相应 的 匀
点 为 :1,2,3,4,8,9,10。 15 小 运输 量 为 147792. 26 吨公里 ,相应 的 岩石 产量 为 49280 吨 ,矿石 产量
为 54054 吨 。 |
于- 生 玉生 和亲 上 本人
2 人 7
关键 词 = RLHE: 转移 时 间 差
分 类 号 ， os 中 图 分 类 号 ; 0221.2 文献 标识 码 ; A
AS 、 、
L PRgRAE () 2 模型 假设 ( 略 ) 3 符号 说 明 ( 略 )
让 品
4 问题 分 析
这 是 一 个 多 目标 最 优化 问题 。 优 化 目标 有 两 个 ,最 小 运输 量 和 最 少 卡车 数 ,两 个 目标 在
一 定 程 度 上 是 相互 影响 的 。 在 运输 成 本 中 ,总 运 量 是 主要 决定 因素 ,把 总 运 量 作为 主要 目
标 , 将 卡车 数 转 化 成 约束 条 件 ,使 卡车 总 数 不 大 于 20, 得 到 改进 模型 。 根 据 多 目标 的 主要 目
标 法 的 有 效 解 理 论 ,在 此 最 优 解 集 上 求 最 少 卡车 数 的 有 效 解 或 弱 有 效 解 。 另 外 ,由 于 电 铲 和
外 点 只 能 同时 为 一 辆 卡车 服务 , 若 此 时 还 存在 其 他 卡车 在 该 铲 点 或 印 点 需要 服务 ,就 出 现 等
待 情况 ,在 解决 时 应 避免 该 情况 发 生 。 在 装 石料 时 若 一 条 路 线 中 卡车 数 超过 一 定 值 时 ,必然
会 出 现 等 待 。 为 了 方便 讨论 ,我 们 按 矿 石 漏 , 倒 装 场 !, 倒 装 场 II, 岩石 漏 , 岩 场 的 顺序 将 它

<!-- source_page: 2 -->

EliAl
64 工 程 数 学 学 报 第 20 卷 1
们 依次 记 作 外 点 Dy ,D;，…D, 装 点 Su,S -So。 于 是 ,每 条 S-*Di-*S 路 线 的 运行 周期 为
1(i,j)=3+5+ 28ED san y(5,j)h s, 5D, 之 间 的 距离 (km)， 为 卡车 速度 (km/
hb)。 由 于 每 装 一 次 车 的 平均 时 间 为 Smin( 大 于 印 车 时 间 3min) ,那么 每 条 路 线 上 可 容纳 的
最 大 车 辆 数 w(i ,7) = | 工 全 尹 ]。 此 外 ,每 辆 车 一 个 班次 工作 480min, 则 一 辆 车 在 相应 的
= ，\_「 480
路 线 上 运输 次 数 的 上 界 为 MEG)= | |。
5 模型 的 建立 及 求解 _
5.1 模型 准备 -从 >
在 模型 建立 之 前 , 先 给 出 几 个 必要 的 命题 (证 明 过 程 路 ) 和 分 析 过 程 。 我 们 用 先 志 数 o,
来 刻画 第 ” 辆 车 是 否 被 利用 。 当 第 辆 车 被 利用 时 eu = 1 ,否则 c, 73
命 大 1 第 ” 辆 车 是 否 被 利用 的 标志 数 cy = flog(T Tv,0 M 让 大 1.2，…,20，
其 中 Yi 是 第 ， 辆 车 从 Si 到 的 运输 次 数 ,Jiag 为 和
命 顾 2 第 i 个 铲 点 是 否 有 铲 车 的 标志 数 忆 = 1 8
5.2 问题 一 的 模型 K
对 于 问题 1 和 问题 ,都 必须 满足 :
1 各 铲 点 向 所 有 印 点 提供 的 岩石 和 玉石 是 量 应 分 别 不 大 于 该 匀 点 矿石 数量 和 岩石
数量 y， 即 为 模型 中 的 (1) 式 。 从
2) 由 所 有 铲 点 向 各 印 点 运输 的 看 料 总 和 应 不 小 于 务 点 所 需 石料 的 下 限 , 即 为 模型 [中
的 (2) 式 。 <o
3) 品位 限制 ,在 三 个 矿 右 狂 点 ,矿石 的 平均 铁 含量 应 在 给 定 范围 内 , 即 为 模型 工 中 的
(3) 式 。 ~
4) 由 于 铲 节 数 晤 凋 天 新 以 要 求 利用 的 名 点 数 不 超 过 7 个, 即 为 模型 工 中 的 (4) 式 。
5) 每 人 信人 的 工作 次 数 不 大 于 96 次 , 即 为 并 型 了 中 的 (5) 式 。
oa 5 作 次 数 不 大 于 160 次 , 即 为 模型 工 中 的 (6) 式 。
Jr 六 六 得 问题 一
优 公 得 问题 一 的 基本 模型
N 20 5
min f = 1542 2 了 | Y,(i,7)d(i,i)i
min c, 这 里 om = flag( ) SVG = 1,2,…,20
St 154 T Yi < k;5154 六) <yi=1.2,-,10 (1)
154 号 和 Yi >MD,  j=1,2,+,5 (2)
六 六 (有
28.5% < “一 一 一 所 30.5% ,= 1,2,3; (3)
工人 7)

<!-- source_page: 3 -->

口 | 上 日
第 7 其 喜 天 矿 生产 的 车 辆 安 拓 65 —
Ih, <Toh = flag( Z TY,(1,1)).7 =1,2,,10; (4)
GD 所 96 了 = .210i (5)
35Y,0.) <160 j=12.05 (6)
h €10,1}¢, € (0,1),i = 1,2,,105n = 1,2,+,20 (7)
ZENUI0a = 1,2,,2050 = 12105 = 1,2,,5 (8)
5.3 模型 的 求解
和 二 人 十 汪 全” 信人 于 本 人 全 es 和 让 全
用 一 般 的 非 线性 规划 求解 。 SS
少 卡车 数 设 为 次 要 目标 ,将 次 要 目标 转化 为 约束 条 件 ,从 而 使 得 模型 工 简 人 为 哎 目 标 规划 问
题 。 i
进 模型 为 v,
min f = 6542)xad 有 人 X
(0 ,02) ,3),(5),(6),(7) ,8) ABEL
号 =7. h = Jag( 32Y,(0))i =1,2,,10; (4y
20 10 5 O
SS20c = flag 2 IWDNn = 2 20， (9)
由 于 排 时 计划 无 效 ,等 待 问题 很 闪 和 二 示 上 解决 ,我 们 这 里 深入 讨论 一 个 班次 内 所 有 卡
车 来 回 于 第 守 个 铲 点 和 第 7 § 和 点 次 数 的 上 界 M(i ,7) ,由 于 每 条 路 线 卡车 的 运行 周期 是 一
证 的 , 昌 相 人 守门 扫 不 小 于 后 而 在 芝 条 了 红 的 车次 也 是 一 定 的 ,加 之 有 相应
铲 点 岩石 和 矿 石 最 大 产量 的 限制 , 得 到 ( ME(i, 旋 为 一 辆 车 在 相应 的 路 线 上 运输 次 数 的
上 界 )
MC5 -Re x ME(Gi [Pi7)M154]|
368 64 68 71 72 68 84 87 7017
了 68 64 68 70 81 66 84 87 80
以 > 61 68 64 68 71 81 68 64 70 81| = (M(i,j)gus
NY 81 71 70 68 72 75 68 74 80 8l
81 71 84 68 74 80 68 74 76 8l
3 480
其 中 5 人 4 MEGL) =
于 是 , 夸 YG 所 MG Yi = 1,2,，…,5. 得 到 最 终 求 解 模型
模型 四， min f=1543 51C3)Y,(1,)) xd(i,7)], 5 (1)……(9) 同 模型 了
3Y,(0) < MG)ai = 1210 = .2.5 (10)
根据 以 上 的 改进 模型 ,为 了 便于 求解 ,暂时 不 考虑 约束 条 件 (9) ,由 Ih=TBFALE

<!-- source_page: 4 -->

EliAl
66 工程 数学 学 # 第 20 卷 —
分 成 120 个 子 问题 ,将 六 Y,(i , 疙 看 作 一 个 变量 ,一 共 50 个 变量 。 每 个 子 问题 恰好 是 整数
线性 规划 ,利用 SAS 软件 对 每 个 子 问 题 分 别 求 解 , 经 过 比较 得 到 最 优 解 : 最 小 总 运 量 为 =
556.03% 154= 85628.62 吨公里 。 此 时 5,6,7 三 个 铲 点 没有 运输 量 , 恰 好 满足 铲 车 数量 的
约束 ,主要 目标 已 经 解决 。 在 此 基础 上 ,分 析 车 辆 分 配方 案 ,使 所 用 卡车 数量 最 少 。 若
总 Wi) 三 MEG ), 则 安排 一 辆 卡车 在 一 个 班次 内 只 行驶 S - DD 路 线 。 但 当 六 yy
(7 不 是 ME(i 7 的 整数 倍 时 ,必然 还 要 其 他 卡车 将 剩余 的 石料 运输 完 ,其 车 次 为 2(i，
门 = mod( 写 Yu(ij)，ME(i, 门 )。 通 过 调整 卡车 在 各 路 线 的 运输 可 使 卡车 数 最 少 。 这 里
运用 了 贪心 算法 :1 ,具体 算法 如 下 : %
() 将 剩余 车 次 矩阵 2,,. PIETIERILERN FRIEE Tin vs 所 Sr
(2) 首先 尽 可 能 多 运输 T ARATREHLHAA EFEENA 总 工作 时
间 ,如 有 时 间 剩 余 , 叫 转 移 到 Tio .5 次 大 元 素 对 应 的 路 线 , 选 择 其 中 pRRLEo 总 工作 时 间
的 最 大 路 线 ;运输 后 就 在 Tin .* 中 减 去 已 运输 的 次 数 ; 人 / /
(3) 依 此 策略 直至 一 辆 卡车 的 工作 时 间 排 满 为 止 ; 人 NS
(4) 若 Zio .* 中 还 存在 非 零 元 素 就 返回 (1) , 按 上 术 方 ; 宣 复 ,直至 剩余 车 次 矩阵 Zio
中 元 素 都 为 夫 , 结 束 。 MK-
经 过 调整 并 且 考虑 到 转移 时 间 差 ,我 们 得 到 第 纪 问 所 需 最 小 车 辆 数 为 13 辆 ,其 安排 如
表 1。
定理 1 在 该 问题 中 所 利用 的 最 尖 的 地 负数 为 13 辆 。
证 明 在 报信 中 ,我们 将 运 畏 志 和 Cn、* 和 运 菠 计划 安排 区 Niovs 相 乘 并 求 和 得 出
5 1 5
在 此 方案 下 的 再 要 工作 时 间 电 和 total = S, 3 TUi,5) X NGC7D)= 6038.976 分 钟 ,每 辆 卡
车 的 有 效 工 作 时 间 都 是 480 将 卡 和 n= total /480=12.5813 辆 ,所 以 所 需 卡 车 数
必然 大 于 12 辆 。 而 表 -1 中 已 给 出 了 13 辆 车 的 可 行 运输 方 案 , 所 以 命题 成 立 。
中风 访 。 趟 [问题 1 一 班次 的 运输 方案
7 TY
MRNA
TIN C C  ER E
攻关 区 天王 瑟 本 基 攻 古本 天 本 项 本 天 本 世
天 本 本 和 到 本 和 和
aaa IC C
二
其 中 ,13(3) 表 示 第 3 辆 卡车 在 铲 点 2 与 印 点 1 之 间 共 运输 了 13 车 次 ,其 他 类 似 。
5.4 转移 时 间 差
在 以 上 的 讨论 中 ,我 们 均 没 有 考虑 当 一 辆 卡车 从 一 条 路 线 转移 到 另 一 条 路 线 上 的 时 间
差 。 时 间 差 的 产生 主要 是 在 运输 过 程 中 ,这 辆 车 无 需 再 回 到 原来 的 铲 点 ,而 是 直接 到 另 一 条
路 线 上 相应 的 铲 点 ,由 于 两 条 路 线 的 不 同 ,造成 了 卡车 在 转移 过 程 中 的 转移 时 间 差 。 不 妨 设

<!-- source_page: 5 -->

营 讽
第 7 期 露天 矿 生 产 的 车 辆 安排 67 2
(为 一 条 从 S, 到 了 ; 的 运输 路 线 ,那么 当 一 辆 卡车 从 路 线 转移 到 路 线 时 ,其 转移 时 间 差
上 ,=
AID 方 ) 一 (ija)) = 2)-T()
1yJ1 324J2 e 2 2 T( 1 i) 也

结论 :根据 最 优 结果 进行 分 配 车 次 ,考虑 转移 时 间 差 ,其 时 间 的 总 量 必然 比 原 来 的 理想
时 间 总 和 6038.976 大 。

5.5 等 待 问题 的 讨论

由 于 对 任何 多 于 两 辆 车 的 讨论 都 可 转化 为 两 辆 车 的 情况 ,所 以 ,在 此 仅 讨论 两 辆 车 产生
等 待 的 情况 。 根 据 卡 车 出 现 等 待 的 位 置 对 等 待 情况 进行 分 类 ， ae AY

T - (天 一 e)
LAX
Cl BE19PR2 C2 国生 Cl

人 S2 kX

3 £1 XK 3 名

图 中 :48 表示 装 货 时 间 段 (Smin) ,CD 孝 示 却 货 时 间 段 (3min) ,S1,S2 表示 两 辆 卡车 ,ita 分 别 表示 两 辆 卡车 开始
在 信 点 装 货 的 时 间 ,tcicz) 表 示 时 间 段 A1(2) - B1(2) - C ,全 表示 一 图 所 用 的 时 间 ; 对 于 图 一 ,Marjmod(ry - 1,),mod
(n-reDikFaAEELzrRBLEnARE.  ©

1. 在 铲 点 处 产生 等 待 ., 如 果 有 两 辆 宇 硒 同一 条 路 线 上 运行 ,那么 它们 的 运行 可 以 用 图 一
表示 ， 只 有 当 Maz imod(oo 六 mod( —t,, T)<5 时 ,两 车 才 会 在 装点 发 生 等 待 。 如
果 这 两 车 在 不 同 的 路 线 上 但 人 人 人 二 加 几 一 ， 则 只 有 当 以 下 三 式 0< mod
(t=11, T)<5,0<mod(t 未 T)<5,maz(tb)<i<480 联 立 有 解 的 时 候 ,两 车 才 会
产生 等 待 \

2. 印 点 处 六 4 等 LVr 1 的 讨论 ,可 以 分 为 两 种 情况 ; 当 两 辆 车 在 同一 条 路 线 上 面
运行 时 (图 了 关闭 入 必 须 满足 Mazimod(ta - 6) ,mod(2a ~13, T)| <3, (SIERT CD); 当
两 辆 - 在 司 全 条 路 线 上 运行 时 (图 三 ) ,只 有 当 以 下 三 式 xma<mod(: -TD<3+tia，
ok 0 12, T2)<3+ tey, max{ty, 1,) <t<480 联 立 有 解 时 ,两 车 才 会 发 生 等 待 。

A\

5.6 问题 二 的 模型

对 于 问题 2 ,基于 问题 1 的 约束 条 件 , 求 最 大 产量 且 运 输 量 最 小 ,可 得 出 模型 如 下 :

模型 下 ;max 六 = 154 3 和 SG

min £= 154 呈 三 [六 x asse (DG10) 同 模型 册 ，

采用 类 似 于 问题 1 的 解法 ,首先 不 考虑 约束 条 件 (9) , 按 铲 点 分 布 不 同 , 共 分 为 Cio =
120 个 整数 线性 规划 子 问题 , 求 出 其 产量 最 大 的 解 。 然 后 ,将 最 大 产量 作为 一 个 约束 条 件 ，
并 考虑 岩石 产量 优先 ,再 次 利用 SAS 求解 最 小 运 量 。 求 得 总 产量 671 车 次 ,10.3334 万 吨 ，
总 运 量 为 147792.26 吨公里 ,其 中 岩石 产量 为 320 车 次 ,49280 吨 ;矿石 产量 为 351 产量 ，

<!-- source_page: 6 -->

ES
EliAl
EY
2
mEEsE
68 工程 数 学 学 报 第 20 着 并
ae
54054 吨 ; 卡 车 数量 为 20 辆 。
类 似 于 问题 1 ,采用 贪心 算法 ,并且 考 虑 转移 时 间 差 , 求 出 安排 如 表 2:
表 2 问题 2 一 班次 的 运输 方案
本 玫 本 天 区 油 蝶
40)18
3
104o10( 4»37a4
p ese fi) 0 | 0 | 0 fwe
T0 w o [e] 0  magam
4 23(7)500) 19。9 7) N7
4400D) (5) 7(6) _ \ SN
27 is
| 一
学 J
6 模型 的 评价 与 改进
本 文 对 建立 的 两 个 基本 模型 逐步 简化 求解 ,将 多 本 要 目标 法 转化 为 单 目
标 规划 , 非 线性 规划 转化 为 线性 规划 ,利用 SAS 软 f 的 歼 数 规划 求解 ,模型 简单 ,适用 性 强 ，
容易 编程 实现 求解 ,并 且 能 够 很 好 的 解决 问题 的 整 痢 约束 。 由 于 模型 的 简单 化 ,就 避免 不 了
很 多 的 重复 操作 ,将 原 问 题 分 成 120 个 简单 的 整数 规划 的 子 问题 ,为 了 求 得 最 优 解 ,必须 痪
历 这 120 个 问题 , 求 出 各 个 子 问题 的 最 优 解 ,再 进行 比较 ,时 间 开销 很 大 ;但 是 ,在 求解 过 程
中 ,我们 发 现 很 多 情况 其 实 是 不 符 食用 求 移 , 这 和 可 以 将 那些 对 产量 上 限 很 不 敏感 的 匀 点 不
耶 考 虑 ,作出 适当 的 简化 。 AAA
参考 文献 ; N 二
_—
[1] 0 avlity 长 春 , 吉林 教育 出 版 社 ,1992
[2] f#R&. 0 速成 [M] , 北京 , 科学 出 版 社 ，1998
[3] KK [M]. 北京 : 电子 工业 出 版 社 ,2001
洽 Truck Arrangement for an Opencast Iron Mine
DING Yu-liang, HU Hai-lin, GUO Li-jun
Advisor: L1 Xin-xiu
(Nanjing University of Posts and Telecommunications, Nanjing,210003)
Abstract: In this paper, we study the optimization problem of the truck arrangement for an opencast iron mine.
We use the primary — object method to transform the multi - object optimization problem to a single 一 object opti-
mization problem. Based on the primary object (the total transportation load) we setup a minimal transportation
load function. and use the secondary object as a regulation. then we simplify the cost function, and transform the
non 一 linear programming problem to the linear programming problem. (下 转 114 页 )

<!-- source_page: 7 -->

是 刘
114 工程 数学 学 报 第 20 着 oa
[2] 宋 济 .知识 助 我 登 上 领 奖 台 [Jj. 游泳 ,2002;4:27 一 28
[3] BRE. 毛泽东 畅游 九江 [J]. 游 瀛 ,2002;4:28 - 28
[4] 史 力 生 .用 数字 直接 模拟 层 流 [J] ,长 沙 铁道 学 院 学 报 ,1994;12(2):43 - 54
[5] 杨波 , 程 亮 , 陈 晶 , 李 亮 , 吴 菊 . 抢 滤 长 江 最 佳 路 线 的 探讨 [J] .数学 通讯 ,2002;24:42 一 43
The Application of Mathematic Model in the Competition
of Crossing the Changjiang River
CHEN Li, PAN Hai-li, GUO Ling 一
Instructor; CHEN Tao 全 人 本
(Nanchang University, Nanchang 330047) 一 W
2
Abstract: This paper establishes the optimal model for crossing issue. At the re are present-
ed on the first two questions given in the article. We also analyze the main ES the percentages different of
people who can succeed in reaching the opposite bank in 1934 and in 2 the necessary requirements
for those who can reach the destination successfully. In 2002 the an speed of those successful competitors
was 1.43m/s. In the process of analyzing the latter problems, Ne that adjusting the competitor’s flat - out
direction as current changes is brought forward to establish Model iT and Model 区， Model 内 provides an ideal
crossing way in the case that one can adjust his flat ~- out direction at any time as current changes and gives a rela-
tively rational distribution function of water speed. By Stalyring water speed on the foundation of the real condi-
tion, we get a more rational distribution fu ion 人 water speed and build Model V. The LINGO and MATHE-
MATICA software are used in proceeding to gort  Sprimized answer. By the end, the models established in this
paper can be spread to other fields s air — flight, space flight and navigation.
Keywords: the competition of h River; optimal route
一 一 人
(上 接 68 列 ) V
Ko

2 SAS software，we traverse all the 120 linear programming sub — problems, and get the most
opti ‘solh ion. Based on the solution we use the greedy algorithm to get the least truck number and the plan
for Ne routine. For problem one，we figure out that the minimal total transportation load is 85628. 62
ton * kmythe seven forklifts are placed in the 1st,2nd,3rd，4th,8th,9th forklifts position, 13trucks are needed.
For problem two, we use the similar solution to problem one, and make a full use of the present resource, we get
a maximal production quantity is 103334 ton, 20 trucks are used, and forklifts are placed in the 1st, 2nd, 3rd,
4th, 8th, 9th,10th forklifts position. The minimal transportation load is 147792.26 ton * km, the quantity of
rocks is 49280 ton, the quantity of ore is 54054 ton

Furthermore, we analyze the time when two trucks would wait in the same line, and the cost of time for a
truck moving from one transportation routine to another.
Keywords: primary - object method. greedy algorithm ,the time difference of transfer.

