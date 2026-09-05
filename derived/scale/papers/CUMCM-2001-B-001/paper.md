# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
区
第 19 卷 建 模 专辑 工程 数学 学 报 Vol. 19 Supp.
2002.02J3 JOURNAL OF ENGINEERIN G MATHEMA TICS Feb. 2002
文章 编号 11005-3085 (2002) 05-0095-06
\ AT 让 ~ H- I
公交 车 调度 优化 模型 _-
-从 >
李 成 功 ， 脱 小 伟 ， 郭 尚 彬 = 蛋
指导 教师 : ” 祁 忠 斌 2
(兰州 工业 高 等 专科 学 校 ,兰州 30050) 由 一
纺 者 接 :本文 根据 时 间 和 空间 客 法 不 光 条 变 化 的 情况 研究 车 辆 调度 的 规律 .在 保证 绢 这 益 和 使 从 窑 消 意 的 情况 下 给 出 了
调度 时 蓝 表 。 本 文 分 析 问 题 比较 精细 ,叙述 通顺 简练 。 en 0 9 与 120 % 的 不 同 提 法 考虑
不 够 。 ，
摘要 :本 文 主要 研究 了 一 条 公交 线路 在 其 每 时 段 内 各 个 车 站 点 的 客 昔 统 许 冰 所 为 已 知情 况 下 的 车 辆 运行 计划 时 刻 表 的 抽
定 问题 一般 情况 下 ,公交 公司 在 调查 研究 取得 一 定数 据 的 基干 匡 部 是 接 " 接 连 开 岂 "的 方法 安排 工作 日 的 车 辆 和
车 调度 表 , 使 得 在 运行 期 内 ,一 组 车 辆 “鱼贯 而 出 ,再 鱼贯 而 入 ” 曾 我 和 主要 研究 了 随 着 时 间 和 空间 上 客流 不 均衡 性
的 变化 ,车 辆 应 如 何 调度 的 规律 ,建立 了 目标 规划 模型 。 实 现 了 “有 早出 ,有 晚 出 ”车 辆 有 多 有 少 的 调度 计划 。 在 保
证 一 定 效益 和 顾客 满意 的 情况 下 ,使 在 岗 车 辆 的 总 运 和 时 间 最 短 。 所 有 的 计算 都 在 计算 机 上 实现 ,得 出 了 调度 时 刻
表 , 且 最 少 的 车 辆 数 为 S/ frrriy 0. 68 :0.46
关键 词 : 公交 车 调度 :客流 量 ; 目标 规划 /: A
分 类 号 : AMS (2000) 90 C08 中 图 分 用 T8 1 文献 标识 码 : 4
1 已 知 数据 及 问题 站 站
我 们 要 考虑 的 是 某 城市 的 王 条 公交 线路 上 的 车 辆 调度 问题 。 现 已 知 该 线路 上 行 的 车 站 总
数 NI( -14) ,下 衍 的 第 站 总 数 Nz( =13 ) 。 且 在 问题 中 给 出 了 某 一 个 工作 日 (分 为 mA
时 间 段 ,第 之 时间 段 的 时 间 跨 度 为 乓 = 1 小 时 ) 中 第 计时 间 段 第 7 站 点 上 行 方向 上 、 下 车 的 乘
客 数量 ; 和 i 时 间 段 第 7 站 点 下 行 方向 上 \ 下 车 的 乘客 数量 为 Oo( 功 ，
Q"afi) 7 上 点 间 的 距离 分 别 为 怀 ), 工 7 。 公 交 公 司 供给 该 线路 同一 型 号 的 大 客车 ,每
朵 | 了 4=100 人 ,由 统计 知 ,该 线路 上 客车 运行 的 平均 速度 为 "= 20 公里 /小 时 。
计 展 要求 ,乘客 候车 时 间 不 要 超过 Ti=10 分 钟 , 早 高 峰 一 般 不 要 超过 7 =5 分 钟 ,车 辆
满载 紊 不 应 超过 “= 120 %, 一 般 也 不 要 底 于 r=50%.
现 要 我 们 根据 以 上 资料 和 要 求 ,为 该 线路 设计 一 个 便于 操作 的 全 天 (工作 日 ) 的 公交 车 调
度 方 案 ,包括 两 个 起 点 的 发 车 时 间 表 ;一 共 需 要 多 少 辆 车 ;并 给 出 刻 划 乘 客 和 公交 公司 双方 利
益 满意 程度 的 指标 ,进行 评估 等 。
2 问题 的 初步 分 析 及 基本 假设
制定 公交 车 调度 方案 需要 考虑 的 因素 非常 多 , 且 很 多 因素 都 是 随机 的 。 为 了 抓 住 重点 , 简
化 模型 建立 及 求解 ,必须 作 一 定 的 简化 假设 和 设 定 。
人 。 @ 1994.2006 China Acade rnal Electronic Publishi use. All rights reserved. http:Wwww.cnki

<!-- source_page: 2 -->

ERi
i
人
96 工程 数学 学 报 第 19 T

1 汽车 从 起 点 站 发 车 后 ,都 能 在 领 定 的 时 间 里 到 达 终 点 站 ，

2) 实际 运行 过 程 中 ,发 车 时 间 间隔 允许 有 一 些 细小 的 调整 ，

3) “乘客 在 规定 的 时 间 内 都 可 以 乘 车 ;

4) 乘客 的 满意 程度 只 以 他 所 乘 的 车 的 拥挤 程度 来 衔 量 ，

5) 已 知 平均 速度 , 故 不 计 乘客 上 下 车 和 其 它 因素 所 占用 时 间 ;

6)， 采用 正 班 全 程 余 点 对 开 的 调度 方式 。

3 ”模型 的 建立 <

该 问题 给 出 了 一 个 国定 线路 上 的 一 个 工作 日 各 个 站 点 4 在 各 个 时 段 1 Re
信息 及 一 些 要 求 。 统 计数 据 0 240). O'). 0ul) ER T RSRNLR
分 布 ,通过 适当 的 整理 分 析 , 可 以 确定 我 们 要 做 调度 计划 所 需 的 信息 3 建立 及 求解
主要 通过 下 面 几 个 步骤 :

1 对 数据 进行 处 理 , 并 在 假设 的 基础 上 结合 实际 ,确定 车 轩 调 度 所 需要 的 参数 ，

2/ 在 取得 参数 的 基础 上 ,通过 目标 规划 的 方法 编 抽 运 特 册 基 二

3) 根据 运行 时 刻 表 , 确 定 顾客 与 公交 公司 的 满意 度 ,进行 可 型 评价 :

(一 ) 确定 各 主要 运行 参数 如 下 ; -

1 第 ;时 间 段 内 的 客运 量 0() : 多

0(1 = 30"ip) + 30'u(i) i=1,23, m 人

2 时 间 不 均匀 系数 (及 高 几时 段 : 目

_ / ”
Ce i=1,2,3, m 2)

令 T,={i K(i) =1.8} , 称 .% EITEEA T,=7i 1.0 <K(i) <1.8} , 称 思 为 平 峰
时 段 : 令 To=(i) KE( <1 夺标 7 为 低 峰 时 段 。 另 外 , 记 K(9) = maxt K(D7, 即 * 为 最 高
峰 时 段 序号 。 让

3) 第 ;时间 段 内 的 客流 量 0'(7) :

~ MNsoi- 0"(i) + SU0'u(ii) - 0"ulip) ®

4 和 双关 和 沦 量 :

p 2+ ibori ORN
Se =300(i) - 0(i). Q'uli) = 300ui) - 0"utin) Hh Ki, Ko

3/ J )
1 下行 高 峰 站 点 序号 , 则 第 ;时间 段 高 峰 站 点 客流 量 为 ，
Q"(i) =max{ Q".(i), Q"a(i)} 4)

5 周转 时 间 mi) :为 车 辆 运行 一 周 所 需 时 间 ,影响 因素 很 多 ,比如 车 站 停靠 时 间 ,排队
待 发 时 间 流量 的 大 小 :道路 的 交通 等 。 在 我 们 假设 的 基础 上 ,可 设

10() = tw+ Am )

其 中 ra 为 车 辆 往返 时 间 , 即 wo-[ Be+ 3u) Svi Am 为 车 辆 调度 时 间 ,其 分 别
为 :0 <AT <2( 高 峰 时 ) ， 0 三 AT <6( 平 峰 时 ) 0 <AT; <10( 低 峰 时 ) 。

6) 计划 车 容量 4 : 指 行车 作业 计划 限定 的 车 辆 载 客 量 , 又 称 计划 载 客 量 定额 。 这 是 根
23 © 1994-20 na Academic Journal Electronic Publishi use. All rights re e tp cnki.n

<!-- source_page: 3 -->

ERi
v ~
四
建 模 专 辑 公交 车 调度 优化 模型
据 计划 时 间 内 线路 客流 的 实际 需要 、 行 车 经 济 性 要 求 和 运输 服务 质量 标准 确定 的 计划 完成 的
车 辆 载 客 量 。 可 按 下 式 确定 -
和 二 六 "0 (6)
其 中 : go 为 车 辆 额定 载 客 量 (go = 100 人 ) ;
六 为 车 辆 满载 率 定 额 。 由 题 总,50 %= 三 m <7=120%
7) 行车 频率 初 值 /， : 指 在 第 ;时 段 内 通过 线路 上 同一 站 点 的 车 辆 数 的 计算 值 , 则
太 _ p
8) 所 需 车 辆 数 及 频率 : -从 >
(V 每 时 段 车 辆 数 A, 及 频率 广 : “\)
L %4
人 7” ， 其 中 男 表 示 第 7 时间 段 车 辆 的 周转 系数 ， 阿 ma
fi, ti =to(i)
| MsT。 A
4 barem ursv ®

@ 不 计 其 它 因素 的 影响 ,我 们 认为 ,最 高 峰 ea A, 即 为 线路 所 需 车 辆 数 4 ，
其 中 * 为 最 高 峰 时 段 序号 : 这

(3) 正如 班车 数 : 正 班车 数 4， 与 加 班车 数 4 通常 可 根据 路 线 车 辆 数 4 \ 客 流 的 时 间
不 均匀 系数 K(w 及 车 辆 满载 率 定 额 r, 等 按 再 式 确定 :

“ 有
% :
式 中 :o 为 车 辆 系数 。

“为 识 峰 时 段 * AE

六 为 平 峰 期 载 客 率 定 打 于

根据 线路 车 辆 美 型 及 科 均 满载 程度 的 不 同情 况 ,车 辆 系数 约 为 :o = 1. 0 一 1. 20 ,因为 同一
车 型 ,所 以 取 )

IEFHA , ]

你 \pSEBAgT  § € 7 即 在 高 峰 时 段 时 ,需要 增 开 加 班车 。

9) ATRIAN 1-

SA 大 _ _ |
生生 刘 册 的 计算 行车 癌 是 指正 点 行车 时 ,前 后 丙 辆 车 到 达 同 一 个 车 站 的 时 间 间
山 又 积 革 下 。 可 由 下 式 确定

\ 民 | 2 i €T,

万 = (10)
mi T1,t/fyf , i €T, UT,

行车 间隔 确定 是 否 合理 ,直接 影响 营运 线路 的 运送 能 力 和 运输 服务 质量 ( 即 顾客 的 满意 程
应 。

(2) 行车 间隔 的 分 配 : 即行 车 间隔 计算 值 的 分 配 , 指 对 呈现 小 数 的 行车 间隔 值 进行 取 整
数 处 理 , 使 之 确定 为 适当 的 数值 以 便 掌握 的 过 程 。

假设 某 段 时 间 “内 行车 间隔 /的 计算 值 为 小 数 , 即 六 = E+ af 为 /的 整数 值 部 分 :
为 小 数值 部 分 ) 。 令
2 C 4-2006 Chi cademic Journal Electronic Publishing House. All rights reserved.  http://ww ki.n

<!-- source_page: 4 -->

ERi
HEe Y
98 工程 数学 学 报 第 19 郑 wm
L() = [= E+1 L() =Lrl-E (1y
再 设 6 WA 1(i) , 1C0) NBIRRIEREES A Sa, S*, 所 需 车 辆 数 为 4,, 则 易 得
Sq=ti- dimnfi，S=4i- 9v (12)
10. 最 多 运行 圈 数 M :
记 7o( 人 小 时 /为 一 个 工作 日 的 时 间 ,和 =minf mo( 动 , 则
M=(To X60)/ t, 113)

有 具体 各 参数 算法 及 调整 ;

在 已 确定 车 辆 调度 形式 及 线路 原始 数据 基础 上 进行 的 运行 参数 计算 ,是 一 个 包括 初 值 计
雪人 等 人 和 纪 拓 这 得 加 人生
要 求 , 则 应 返回 至 前 面 有 关 步 又, 修改 有 关 数 据 后 重新 进行 ,直至 符合 要 3 AIE. 内

有 具体 运行 参数 的 调整 通过 编程 实现 (流程 图 ,程序 及 结果 见 附 页 / 7

(二 ) “建立 目标 规划 模型 编制 行车 时 刻 表 : lyod

我 们 所 制定 的 行车 时 刻 表 是 一 个 4 X2M 矩阵 让 奇 、 偶 数列 元 素
xx xs2x 分 别 表示 第 * 班车 在 第 上 圈 (E=1,2，…a0) 中 往生 吉 S13 ,40 的 发 车 时 刻 ( 精
确 到 分 钟 ) 。 若 没 发 车 , 则 令 x201(B x20 HO0 AINY 5,, ZOME,4 i=Le, ;1-4,0
就 是 时 刻 x, 所属 的 时 间 段 的 序号 。 28

我 们 要 考虑 的 目标 是 :在 早 高 峰之 前 ,使 尽 可 能 多 的 奈 尽 可 能 晚 出 车 ,而 在 晚 高 峰之 后 ,又
使 尽 可 能 多 的 车 , 尽 可 能 早 地 下 班 。 这 样 ,作为 公交 公司 ,就 可 以 减少 付 给 因 排 队 待 命 而 在 岗
的 那些 行车 人 员 的 工资 。 为 此 , 令 @

ki(s) = ming J| £, 07 We (5) =maxt j| sy #07 ， (14)
则 显然 ,第 * 班车 在 第 ed Low72] 圈 收 车 :再 记 为 同一 圈 \ 同 一 站 上 继
第 * 班车 后 所 发 的 第 一 辆 车 的 班次 序号 。 则 有 目标 函数
j 时 +(2M- fy) (15)
及 约束 条 件 ， 下
v 1 so 二 可
2 | xy | €La(i) 1(i)}
下 4 5<x,,<23 (9

\ A j=2.3,2M
Is- s=1,2,4

此 缠 型 可 通过 计算 机 模拟 求解 得 出 行车 时 刻 表 从 而 可 制定 出 调度 方案 (程序 见 附录 ) ,但
控制 变量 x ,的 个 数 很 多 ,算法 非 线性 ,计算 量 很 大 。 在 实际 编制 中 往往 从 高 峰 时 段 开 始 向 前
后 推算 ,用 手工 较 容易 实现 ,而且 还 可 以 微调 。 部 分 时 刻 表 见 表 1 。
2 © 1994-2006 China Academic Journal Electronic Publishing H llrights reserved。 http://www.cnkin

<!-- source_page: 5 -->

回味 汉 回
建 模 专辑 公交 车 调度 优化 模型 o
表 1 行车 时 刻 表 ( 部 分 /
Ta 6
班次 4 214 2146414Ta4s[a|4aslao
24 | |500|5ss0|636|721|806|ss |
2 | | | | 1722jsos|ss|9jio2sunlnssg
256 | | | | as | |
2 | | | | 7a6snplssl | |
2 | | | | Daslsals9ool94lioszlu:acDojaso
29 | Isaofeoofeaalraolsas] | | | ea7
30 | | Jew|eas[raalsasloos[oso] | 07 人 7
u | | nasalzal | [ | FR
3 | |520| 606|6s0|736|821|9o7| 955|1039a2|1 站 |
33 L Jenfenlrnlonlomnlywlisdushe 13.01
(Z) 刻 划 公交 公司 及 顾客 的 满意 程度 : 人
记 4 为 实际 某 一 行车 方案 中 第 ; 时 段 上 的 平均 每 全 车 的 袁 党 一 显然, 了- 本 “,
也 -100 一 人 .
4 pi=y 100 4 9 搬 s
0, 了 <100, 0, di 三 人
其 中 9 为 车 辆 收益 载 客 量 。 [e]
z z [e]
令 p-t 2 p=t i C 忆 ，
忆 越 小 时 越 满 意 。(0 <p, P <U)
0 p =0.8 时 ,PP=0.32,P' =0.54.
4 模型 的 评价 与 推广 厂
本 文 是 在 一 定 假 弯 粤 件 下 所 考虑 问题 的 ,具有 一 定 的 实际 推广 意义 ,可 以 用 来 制定 一 些
良好 条 件 下 的 和 车辆 调度 计划 ,但 对 于 因素 太 多 条件 太 复杂 的 运行 系统 则 需 用 人 工 模拟 与 理论
分 析 相 个 和 。
sahif
站 AR 汽车 运输 工程 [M]. 北京 :人 民 交 通 出 版 社 ,1987
中 四 大 学 生 数 学 建 模 辅导 教材 [M]. 长 沙 :湖南 教育 出 版 社 ,1997
The Optimizing Modle on the Dispatch of Buses
LICheng gong， TUO Xiao-wei, GUO Shang bin
Teacher: QI Zhong bin
(Lanzhou Higher Polytechnical College ,Lanzhou 730050)
Abstralt : This passage discusses the problem of how to determine the timetable of the buses on a certain route under the condition
of known statistical data of passenger flow at various stops during every time period. Under normal conditions ,bus companics arrange
the vehicle dispatching timetable on the basis of investigated data with the “succession” method during work days to make a group
#h 工
撞 大

<!-- source_page: 6 -->

回 叶 这
EU
|
四
入
100 工程 数学 学 报 第 19 T
of buses "file in and out "during aperation period while we have mainly doue the research on the uneven variation of the passenger
flow in time and space ,the research on the laws of how to dispatch buses and we have established a target planning model which has
realized the dispatching plan of "some early and some late”and when there are more ,when there are fewer . Under the circum
stances of ensuring certain banefits and the satisfaction of passengers ,the overall operating time of the buses in operation has been
made the shortest ,the dispatching timetable has been got ,while the number for the least buses is 42 and the ratio of satisfaction be-
tween passengers and bus companies is 0.48 :0. 46
Key words :Bus Dispatching; Passenger Flow ; Target- Planning
和 %
o <sJ》
° W
(上 接 94 页 ) 5
Optimization of Dispatching S )
FU Changjian Yang Carxia Qin Mi
Advisr:  CHEN Jin'mi
全
(SiChuan University , Cherlgdu 610064)
AS
Abstract :is to find out the best way to dispatch buses. We set a optimized model whose target function is the profit of bus com
pany. At the same time , it guarantee the proportion that the passengers waiting for their buses more than 10 min (or 5 min)in the
total is less than qd given before. First , every station’s nonparameter distribution function about the number of passengers is fitted by
method of least squares. We use a simple method to_estimate tha at least 43 buses are needed , and then , we use Maple to get the
optimal solution refer to it. It shows the best pa d patching buses in different conditions of the number of passengers. It can
help bus companny to get the top profit , meamvhile jj assengers may not wait for their busforalong time. In the end , we evalur
CA
ate and popularize the model , and point out the effective ) to improve it.
Key words : dispatching buses ; optimized“fodel ; mathod of least squares
] NA
一 -一 j
% ]
所
2 994-2006 China Academic Journal Electronic Publishing House. Allrights reser ttp:Wwww.cnkin

