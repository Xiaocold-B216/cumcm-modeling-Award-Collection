# Extracted Paper

<!-- source_page: 1 -->

让 你
基于 0-1 规划 的 单 RGV 动态 调度 模型
摘要

本 文 从 规划 角度 出 发 ， 研 究 了 智能 加 工 系统 中 的 单 RGV 动态 调度 问题 。 由
于 RGY 型 号 多 样 、 功 能 有 简 有 繁 ， 因 此 本 文 从 RGY 是 否 能 预 判 CNC 加 工 完成 时
间 建立 了 两 套 单 RGV 动态 调度 模型 ， 并 进行 了 对 比分 析 。

针对 任务 一 中 情况 1， 本 题 仅 需 考虑 一 个 班次 中 单 工序 加 工 的 单 RGV 动态 调
度 模 型 。 本 文 以 RGV 的 调度 路 径 为 决策 变量 ， 以 获得 最 多 成 料 为 目标 函数 ， 约
东 条 件 为 每 次 调度 单 RGV 仅 能 对 一 台 CNC 进行 作业 、 每 班次 RGV 工作 时 长 不 超
过 8 小 时 、RGY 下 轮作 业 移动 起 点 为 上 轮作 业 终点 、 每 台 CNC 每 次 作业 仅 能 加
工 一 个 物料 ， 根 据 0-1 规划 的 思想 建立 单 目 标 规划 模型 ， 最 终 得 到 6NC 无 故障
下 加 工 单 工序 物料 的 所 获 成 料 最 多 模型 ， 本 这 天 每 抢 上 下 人 最 后
启发 信息 ， 建 立 启发 式 算法 得 到 近似 最 优 解 ， 并 给 出 算法 流程 图 及 欢 廊

针对 任务 一 中 情况 2， 本 题 需 考虑 一 个 班次 中 加 工 双 工 序 的 单 RGy 动态 调度
模型 。 首 先 ， 在 情况 1 模型 的 基础 上 ， 增 加 约束 条 件 ， 每 台 ONSAEIR H
刀具 加 工 一 道 工序 、 物 料 工序 状况 与 CNC 加 工 工序 类 型 恨 吧 配 ,/ 以 获得 成 料 尽
可 能 多 、 获 得 最 多 成 料 时 RGY 工作 时 间 尽 可 能 小 为 目 慰 建 双 目标 规划 模型 ，
并 给 出 以 循环 遍历 法 求 最 优 刀 有 具 分 布 方案 以 及 通过 求 得 每 轮 上 下 料 最 短 所 需 时
长 的 启发 信息 ， 建 立 启发 式 算法 得 到 近似 最 优 亿 ; 兴 放 给 出 算法 流程 图 及 分 析 。

针对 任务 一 中 情况 3， 在 任务 一 情况 1、2/ 异 型 的 基础 上 ， 将 CNC 的 故障 和
维修 等 效 转换 为 一 次 时 间 较 长 的 加 工作 业 ， 增 加 约束 条 件 ， CNC 加 工 过 程 中 有
的 梳 率 发 生 故 噶 、 故 了 发生 时 该 CNCE 加 工 的 物料 即 记 报 庶 ， 徘 除 玫 障 时 长
服从 10 ~20 分 钟 的 均匀 分 布 ， 凑 分 别 建兰 CNC 概率 故障 情况 下 的 单 、 双 工序 加
工 的 单 目标 规划 模型 、 上 在 情况 1
和 情况 2 算法 的 基础 上 加 入 仿真 随机 故障 得 到 情况 3 的 启发 式 算法 ， 并 给 出 算
法 流程 图 及 分 析 。

针对 任务 二 ， 利 用 和 st 人 对 任务 一 中 三 各 情况 的 规划 进行
解 和 检验 , 得 到 情况 ! 下 的 产量 为 382、359、392; 情况 2 下 的 产量 为 253、211、
243， 0 总 工作 时 长 为 28797、28755、28692， 最 优 刀 县 分 布
方案 为 [1， 2 ， 2 1,2].02,1,2,1,2,1,2,1]. [1,2,1,1,2, 1, 1, 2]; BLTJPt
况 3 下 总 量 为 376、354、383， 对 应 的 故障 次 数 为 3、3、4; 双 工序 情况 3 下 产
oyamhaif) 40， 加 工 工序 一 时 故障 次 数 为 3、1、1， 工 序 二 故障 次 数 为 2、
0 了 以 普天 性 、 经 济 性 、 实 施 模型 的 可 行 性 和 CNC 平均 非 有 效 工作 时 长 作为 模
型 缮 用 性 指标 ， 以 程序 运行 时 间 和 内 存 使 用 情况 作为 算法 有 效 性 指标 ， 分 别 对 两
4 模型 各 12 组 结果 进行 模型 的 实用 性 与 算法 的 有 效 性 评价 。 最 终 计 算 结果 反映
出 本 文 模型 实用 性 高 、 有 效 性 强 ， 且 可 预 判 模型 结果 更 优 。

最 后 ， 本 文 利用 仿真 数据 对 模型 进行 了 再 检验 ， 分 析 了 模型 的 优 扎 点 ， 讨
论 了 模型 的 改进 方向 并 对 模型 进行 了 简单 的 推广 。

关键 词 : 智能 RGV， 机 器 故障 ;动态 调度 ，0-1 规划 ;启发 式 算法

1

<!-- source_page: 2 -->

让 你
一 、 问 题 的 提出 和 重 述
1.11 问题 的 提出

轨道 式 自动 引导 车 (Rail Guide Vehicle, RGV) 因为 其 无 需 人 员 操 作 且 运
行 速度 快 的 特点 ， 能 实现 与 系统 快速 连接 并 按照 计划 进行 物料 的 传输 等 ， 在 当
今 自动 化 物流 系统 与 自动 化 仓库 中 有 着 重要 应 用 ，RGY 的 动态 调度 的 研究 对 车
间 的 高 效 作业 有 着 重要 意义 。

1. 2 问题 的 重 述

现 有 8 台 计 算 机 数控 机 床 (Computer Number Controller, CNC) 与 1 辆 轨
道 式 自动 引导 车 ， 附 属 设备 有 1 条 RGY 直线 轨道 和 上 、 下 料 传送 带 各 一 条 等 。 请
针对 以 下 三 种 具体 情况 完成 两 项 任务 。

情况 〈1)， 物 料 加 工 仅 一 道 工序 ， 每 台 CNC 安装 相同 刀具， 物料 可 以 在 任
一 台 CNC 完成 加 工 ;

情况 2， 物料 加 工 有 两 道 工序 ， 每 个 物料 两 道 工序 在 两 台 万 看 wer
上 依次 加 工 完成 ; -AN

情况 (3): CNC 在 加 工 过 程 中 约 有 1% 的 可 能 发 生 故 障 0
加 工 的 物料 报废 )， 每 次 排除 故障 需要 10 ~20 分 钟 ， 故 障 排除 后 ENC 即刻 加 入
作业 序列 。 AAA

任务 1， 研 究 一 般 问题 ， 给 出 RGY 动态 调度 模型 上 攻 也 的 求解 算法 ;

任务 2， 利 用 表 1 中 3 组 系统 作业 参数 分 别 验 验 模型 的 实用 性 与 算法 的 有 效
性 ， 给 出 RGY 的 调度 策略 与 系统 的 作业 效率 , 少 梅 其 体 结果 填 入 附件 2 的 EXCEL
表 中 。 N

二 、 问 题 的 分 析
2.1 问题 的 分 析 ANA 。

针对 任务 1:

关于 情况 1)， 在 智能 加 工 系统 中 通过 调度 1 台 RGV 对 8 台 CNC 进行 上 下
料 与 清洗 ，RGY 每 次 只 能 涯 中 全 CNC 进行 上 下 料 与 洗 料 ， 每 轮作 业 RGY 与 8 台
CNC 的 关系 可 用 0-1 逻辑 恋 量 表示 ， 以 所 获 成 料 数量 最 大 作为 目标 函数 ， 以 RGV
的 调度 路 径 作为 决策 变量 以 智能 加 工 系统 中 加 工 规则 作为 约 东 条件， 以 0-1
规划 思想 建立 音量 生机 划 本 型 可 以 得 到 一 道 工序 加 工 需求 下 的 RGV 动态 调度
模型。 并 网 昌 息 ， 给 出 具有 可 行 性 的 算法 。

XFPAQ): 现实 生产 生活 中 ， 物 料 往往 不 止 有 一 道 工 序 ， 由 于 工序 之
间 EN 也 全 有 时 对 有 限 加 工资 源 的 合理 规划 ， 能 有 效 的
全 本 文 拟 以 所 获 成 料 数量 最 多 、 所 获 最 多 成 品 数 量 时 RGV 工作 总
1 5 相 为 目标 函数 ， 仍 以 RGY 的 调度 路 径 作为 决策 变量 ， 以 智能 加 工 系统
中 痪 江 规 则 作为 约束 条 件 ， 根 据 0-1 规划 思想 建立 双 目 标 规划 模型 ， 可 得 到 两
道 工序 加 工 需求 下 的 RGV 动态 规划 模型 ， 并 给 出 具体 可 行 的 算法 。

关于 情况 3);， 当 CNC 存在 1 的 概率 故障 时 ， 在 情况 〈1)、(2) 所 建立 的
规划 模型 下 ， 将 故障 CNC 的 修理 时 间 视 为 一 次 较 长 的 加 工时 间 ， 因 此 故障 CNC
在 故障 排除 前 不 会 发 出 需求 指令 。 视 工作 人 员 排除 故障 的 时 间 在 10 ~20 分 钟 间
服从 均匀 分 布 ， 故 辜 排除 后 CNC 重启 ， 此 时 报废 物料 已 被 移 去 ，CNC 即刻 发 册
需求 指令 。 可 得 到 在 CNC 概率 故障 情况 下 的 RGV 动态 规划 模型 ， 并 给 出 具体 可
行 的 算法 。

针对 任务 2， 拟 考虑 将 模型 的 实用 性 分 解 为 模型 的 普 适 性 、 经 济 性 以 及 实施

2

<!-- source_page: 3 -->

回 成 革 动 国
Ee
模型 的 可 行 性 、CNC 平均 非 有 效 工 作 时 长 ， 将 算法 的 有 效 性 分 解 为 程序 总 运行
时 长 、Matlab 内 存 占用 量 。 利 用 三 组 系统 参数 分 别 检验 情况 1、2、3 的 模型 ，
讨论 计算 过 程 与 结果 的 模型 的 实用 性 与 算法 的 有 效 性 。
三 、 模 型 的 假设
3.1 模型 的 假设
(1) 因 安 全 需要 ， 系 统 启动 后 直到 系统 停止 作业 ， 中 途 不 能 更 换 刀 具 。
(2) RGY 运行 至 需要 作业 的 某 CNC 处 时 ， 上 料 传送 带 将 生 料 同时 送 到 访
CNC 正 前 方 ， 下 料 传送 带 将 清洗 后 的 成 料 能 立刻 送 走 。
(3) CNC 一 旦 发 生 故 障 ， 工 作 人 员 即 刻 开始 排除 故障 。
(4) RGY 所 有 的 计算 处 理 时 间 为 0， 不 会 对 系统 产生 任何 影响 。
(5) 除非 系统 因 已 连续 工作 8 小 时 而 停止 作业 ，RGV 的 移动 、 起 清
洗 等 操作 不 会 被 中 途 停止。 SS
四 、 符 号 及 变量 说 明 _s
wy | EaAX L, |) | 单位
EREEL k=0124 半 本
k ik = 0 时 ， SN *
[=12,.08 \/
asEacGEENoco
第 K 轮 上 料 RGV 是 否 前 入 第 ; 合 CNC
x® 0 e Slckt ERPRATAESS6 CNC
第 k 办 上 和 料 前 往 第 ! 台 CNC
p = L2RALFon ROV 移动 的 起 点 位 置
p = ] 攻 和 示 NCI# 与 CNC2H 之 间 ;
p 2 表示 CNC3# 与 CNC4# 之 间 ;
[3 二 CC5e5 CNC6# 之 间 ;
了 4 表示 CNCT# 与 CNC8H# 之 间 。
p® q o  FORKE RLROY 移动 的 起 点 位 置
一 | 9 =1234， 表 示 RGV 移动 的 终点 位 置
V/7 q = 1 表示 ONC1#5 CNC2H 之 间 ，
7 兴 < qd = 2 表示 CNC3# 与 CNC4# 之 间 ;
SNV 并 q = 3 表示 CNC5# 与 CNC6# 之 间 ;
I 蕊 S- q = 4 表示 CNC7# 与 CNC8H# 之 间 ，
区 到 表示 第 K 验 上 料 RGV 移动 的 终点 位 置
® RGV 前 往 第 ; 台 CNC 完成 第 K 轮 上 料 所 用 时 间 s
TO 第 K 轮 从 位 置 p(9 移 动 到 位 置 4@9 所 花 的 时 间 s
T 第 上 轮 上 料 后 第 ; 台 CNC 上 物料 剩余 加 工 完成 的 时 间 s
7 在 第 ; 台 CNC 的 处 第 K 轮 上 料 时 间 s
T® 在 第 ; 台 CNC 的 处 第 K 轮 洗 料 时 间 s
T® 第 上 轮 上 料 后 第 ; 台 CNC 的 加 工时 间 s
3

<!-- source_page: 4 -->

回 吕 过
u
CLyes

® 第 ! 侣 ONC 第 K 轮 上 料 后 到 其 发 生 故 障 时 刻 的 过 渡 时 间

流 TO~U(0TC) S

ty) 事件 C@9 发 生 的 时 刻 s

四 第 K 轮 上 料 发 生 故 障 的 第 ;全 CNC 的 维修 时 间

7 个 T 名 ~U(6001200) s

w® 第 K 轮 上 料 后 加 工 一 道 工序 的 CNC 产 出 的 成 料 总 数 个

w® 第 上 轮 上 料 后 加 工 两 道 工序 的 CNC 产 出 的 成 料 总 数 个

第 ; 合 ONC 的 加 工 工序
Y, . 他 车 CNC 负责 第 一 道 工序
【2, 第; 台 CNC 负责 第 二 道 工 序 <
第 K 轮 上 料 时 的 目标 工序 AS
xoO | xxo- 相 第 K 轮 上 料 时 RGV 中 无 物料 一 \
2, 第 K 轮 上 料 时 RGV 中 有 完成 了 工序 条 的 物 糙
CO 第 上 轮 上 料 时 第 ; 台 CNC 发 生 了 起 别 ) |
第 K 轮 上 上 料 时 第 ;全 CNC 发 生 了 起 说 的 往 率
PC oo AW
P(Cl )= DN
C S
= oAS
五 、 模 型 此 建立

由 于 现实 中 RGY 型 号 多 样 、 功 能 有 简 有 繁 ， 本 文 根 据 信息 处 理 能 力 将 RGY 分
为 两 类

第 一 类 为 能 通过 处 理 历史 下 求 从 号 得 到 每 台 CNC 实时 工作 状态 ， 综 合 考虑 并
比较 每 台 CNC 的 剩余 加 工时 间 .月 丰 料 时 间 以 及 RGY 移动 至 对 应 CNC 位 置 的 所 需
时 间 后 再 对 任务 进行 次 旗 基 断 的 RGW， 这 类 RGY 能 提前 向 下 一 轮 最 优 CNC 出 发，
总 使 得 8 小 时 内 全 体 CN 等待 时 间 最 少 。

第 二 类 为 仅 能 根据 当 轮 也 接收 到 的 需求 信息 、 上 下 料 时 间 以 及 RGV 移动 至 对
应 机 位 所 需 时 间 允 牌 荔 次 序 进行 判断 的 REV， 在 没 接收 到 需求 信号 时 ，RGV 停泊
在 原 地 。 \ v

ASCIFFILAPIE RGV 为 调度 对 象 ， 建 立 了 两 种 单 RGV 动态 调度 模型 ， 比 较 它
们 之 间 的 壮 宇 合并 讨论 其 优 劣 。

诅 体 的 思维 导 图 如 图 1:

p) AW RGV 移 动 时 长

13X ) 与 CNC 剩 余 完

SA， 没有 ; 记录 历 史 [EErr—— 成 作业 时 长 之 和

人 信和 的 凋 度 鲁 于 1 RGV 上 下 料 时 间

RGV 洗 料 时 间

RGV 动 态 调度 模型
RGV 移 动 时 长 与
”CNC 利 余 完成 作
具有 记录 历史 同时 考虑 历史 需 业 时 长 中 的 较 大 值
需求 信号 与 预 — 求 信号 和 当前 需 ”一 |

判 功能 的 RGV ，。， 求 信号 的 调度 重型 。 | | RGV 上 下 料 时 间

-| _RGV 洗 时间

图 1 ， 模型 思维 导 图
4

<!-- source_page: 5 -->

村
5. 1 任务 一 的 模型 建立 一 一 方法 一 : 考虑 历史 信号 的 调度 模型
任务 一 实际 为 在 CNC 有 无 发 生 故 障 的 情况 下 分 别 对 加 工 一 道 工序 、 两 道 工 序
的 物料 建立 4 种 RGV 动态 调度 模型 。 本 模块 下 4 种 模型 均 在 采用 第 一 类 RGY 的 基
础 上 建立 。
5.1. 1 无 故障 下 加 工 一 道 工 序 的 情况
(1) RGV 的 动态 调度 模型
在 智能 加 工 系 统 中 ， 调 度 1 台 RGV 对 两 边 排列 的 8 台 CNC 进行 上 下 料 与 洗
料 。RGY 小 车 ， 第 上 轮 上 料 对 于 第 ; 台 CNC 只 有 前 往 和 不 前 往 两 种 情况 ， 引 入 0-1
变量 zxg9， 则 有
0 _ f RGV 第 K 轮 上 料 不 前 往 第 ;人 台 CNC 加
(1，RGV 第 k 轮 上 料 前 往 第 ; 台 CNC oy
对 RGYV 而 言 ， 每 轮 移动 前 均 对 当前 8 全 CNC 各 自 的 加 工 秋 人 时间 生动
至 每 台 CNC 前 所 需 时 间 709w 中 进行 比较 ， nn
为 RGV 从 前 往 第 ; 台 CNC 完成 第 上 轮 上 料 所 用 时 间 ， nl
To = max (Tva] 二 (2)
其 中 p( 表 示 第 K 轮 上 料 的 RGV 移动 的 起 点 位 置 ， ov 轮 上 料 RGV 移动 的
终点 位 置 。 <
Jo _ | 加
(第 k 轮 上 料 前 第 玛 BNC 有 物料
其 中 六 @ 为 第 K 轮 上 料 前 第 ; 台 CNC 上 的 物料 状态 ， 旨 在 区 别 开 机 后 前 8 轮 上 料 之
后 不 需要 洗 料 的 情况 ， 其 中 入 9 的 处 第 K 轮 上 料 后 洗 料 时 间 用 7
表示 。 NA
综 上 ， 建 立 获得 成 料 数量 最 多 的 单 目标 规划 模型 如 下 :
决策 变量 为 <
AC
目标 函数 为 :- 让
max Z = max w® (4)
k
SPR | F Soh
约 东 外
GOT RGW4 轮 移动 去 等 待 时 间 最 短 的 CNC 前 ， 即
WA- max( zf : Te) = min To (5)
NB， 一 台 RGY 每 次 只 能 对 一 台 CNC 进行 上 下 料 与 洗 料 ， 即
8
> x®=1 (0)
(3) 每 台 CNC 在 装载 过 一 次 物料 后 ，CNC 上 一 直 有 物料 ， 即
HocD=j+xmo(-jo] (7)
C4) RGY 停泊 的 时 间 越 短 ， 工 作 时 间 越 接近 8 小 时 ， 系 统 工作 效率 越 高 。
RGY 一 个 加 工 班次 中 总 工作 时 间 不 超过 8 小 时 ， 即
5

<!-- source_page: 6 -->

ERiEAE
Be
k 8
> zx (TD +T RD)<8x3600 (9)
k=1i=1
(5) RGV 第 上 + 1 次 的 移动 起 点 pw+3 为 第 上 次 ROV 的 移动 终点 gwo ， 即
qdCO 一 DC (9)
(6) 每 轮 上 料 后 累计 成 品 产量 至 多 增加 1， 即
8
wk+D) — w(o 十 2 (H . xz) (10)
i=1
《7) 在 第 一 轮 上 料 前 ， 成 料 总 数 为 0， 即
w® =0 (11)
综 上 ， 获 得 最 大 数量 成 料 的 模型 ”为 :
max Z = max w® A7
k=123.;i=12"8 二 NY
max( xf : Te ) = min To 2XG \!
7
8
和 供
i=1 一
je =j+xefl
St k 8 (12)
> > xf ， C++ TO .9) <8x3600
k=1i=1
q® = pe 全 ”
8
wd wo 工 》 (Ho .xz 由)
i=1
1
一 etoD

|

由 于 难以 直 通过 模型 求 得 全 局 最 优 解 ， 考 虑 通过 求 得 每 轮 上 下 料 最 短 所
需 时 长 的 局 发 信息 ， 构造 启发 式 算法 得 到 近似 最 优 解 。

SN0 时 即 系统 启动 时 刻 ) 开始 ， 通 过 综合 考虑 所 有 历史 需求 信号 和 当
ES 找 出 能 最 快 完成 上 下 料 的 CNC， 并 响应 此 CNC 的 当 轮 需求 信号 ，
中 LE0h 完成 一 轮 上 下 料 的 过 程 ， 随 后 按照 实际 情况 判断 是 否 洗 料 。 反 复 执 行
上 述 操作 。 当 累计 超过 8 小 时 ， 中 止 循环 。

图 中 预计 完成 作业 时 间 即 玫 2 = mpx (7 T0 00) + 7 。

6

<!-- source_page: 7 -->

加 于
u
Che
RERsH ,
FHHANOT
V
计 完 成 作业 时 间
预计 完成 作业 时 间
根据 最 佳 方案 ， 全
家
<— | 俐 和
£ Eencameamd> 5 所
|
z 《Si
区 RA
一 一
5 二
费 的 时 间
o
CA
图 罗 ”情况 的 流程 图
5.1. 2 无 故障 下 加 工 两 道 工序 的 情况
《1) RGY 的 动态 调度 模型 -|
具有 两 道 工序 的 物料 ,| 竺 加 工 过 程 中 有 生 料 、 已 加 工 一 道 工序 的 物料 以 及
熟 料 三 种 工序 状 EN 一 台 CNC 仅 能 使 用 一 种 刀具 加 工 一 道 工 序
情况 下 ， 中 二 GW 在 上 下 料 时 “认识 ”机 械 铝 所 持 物 料 正 处 于 哪 种 工序 状态
并 对 其 进 和 人 ( 送 至 相应 CNC 进行 后 序 加 工 、 洗 料 ) 是 一 大 难点 。 本
文通 过 引 愉 合用 工序 状态 因子 KQO、CNC 加 工 工序 类 型 因子 苦 ， 当 这 两 种 因子 匹
配 成 项 时 ，RGY 才能 成 功 进行 上 下 料 。
于 Ag 台 CNC 进行 刀具 分 配 时 ， 共 有 27-; Cd = 254 种 刀具 分 布 方案 ， 由 于
疝 份 本 方案 下 RGY 工作 时 间 与 成 料 数量 不 同 ， 本 文 建立 了 以 RGV 调度 路 径 为
决策 变量 的 最 快 获得 最 大 数量 成 料 的 双 目 标 规划 模型 如 下 :
决策 变量 为 ;
2
目标 函数 为 ;
ImaxZ = max ww (13)
k 8
min 0 (TCD 二 TCD .Fo (14)
3Y (10 +18)
7

<!-- source_page: 8 -->

EiiEE
村
o 为 加 工 第 一 道 工序 的 CNC 数量 ，2 为 加 工 第 二 道 工序 的 CNC 数量 ，wt 为 第 K 轮
上 料 后 加 工 两 道 工 序 的 CNC 产 出 的 成 料 总 数 。
在 式 (5) - (11) 的 约束 下 ， 增 加 约束 条 件 :
(1) 一 个 加 工 班次 中 ， 一 台 CNC 只 能 安装 一 种 刀具 、 加 工 一 道 工 序 ， 即
，- 他 车 CNC 负责 第 一 道 工序 as)
”2 第 ! 台 CNC 负责 第 二 道 工 序
〈2) 物料 有 且 仅 有 两 种 工序 状况 ， 即
VD 第 轮 上 料 时 RGV 中 无 物料 aag
2, 第 K 轮 上 料 时 RGV 中 有 完成 了 工序 一 的 物料
〈3) 第 K 轮 上 料 时 ， 只 有 当 物 料 与 被 上 料 的 第 ; 台 CNC 的 工序 匹配 成 功 即
当 X4o = 其 时 才能 成 功 进行 上 料 ， 则 有 #7
xz —2$9(1— [x® _y) RS
(4) CNC 数量 满足 正 整数 约束 且 CNC 总 数量 一 定 , 即 “ 孝 “ 几 )
a+b=8abeN* 2XG (18)
综 上 ， 获 得 最 短 时 间 获 得 最 多 成 品 的 模型 ”为 : ood
max Z = max ww 从
k
k 8
ee BR
K=1 i=1
k=123.;i=12,..,
max(x( . Te) = min A
T® = 人 0 Fwuo) 二 TD
8
$.1
* 590- x® —x))
—|a ¥ 8abeN*
SPCE) +x(1 -£®)
2 小 1 (19)
X% > > xf (TD +1- £©) < 8x 3600
k=1i=1
(9 = ple+D)
濑 ”| ，
warD = w+ (F .xz
2 )
w® =0
xo € {0,1}
Yie{1,2}
x®e{1,2}
8

<!-- source_page: 9 -->

杞 所
EEEE
(2) 模型 的 求解 算法

对 每 一 种 刀具 分 布 方案 采用 与 情况 1 算法 相同 的 思路 构建 启发 式 算法 求 出
对 应 的 近似 最 优 解 ， 依 照 双 目 标 选 出 最 优化 刀具 分 布 方案 及 相应 的 物料 加 工 情
况 。

任何 一 种 刀具 分 布 方案 中 必然 同时 存在 工序 1 刀具 和 工序 2 刀具 ， 遍 历 254
种 刀具 分 布 方案 ， 并 进行 计算 :

从 0 时 刻 《〈 即 系统 启动 时 刻 ) 开始 ， 通 过 综合 考虑 所 有 历史 需求 信号 和 当
轮 需 求 信号 ， 在 所 负责 工序 符合 当前 目标 工序 的 CNC 中 ， 找 出 能 最 快 完成 上 下
料 的 CNC， 并 响应 此 CNC 的 当 轮 需求 信号 ， 对 此 CNC 完成 一 轮 上 下 料 的 过 程 ，
随后 按照 实际 情况 判断 是 否 洗 料 以 及 是 否 改变 目标 工序 。 反 复 执行 上 述 操作 。
当 累 计 超 过 8 小 时 ， 中 止 循环 。 最 终 依 据 双 决策 目标 找 出 最 优化 刀具 分 布 方案
及 相应 的 物料 加 工 情况 。 #7

TR
AN
阿 于
Ke
情况 计算 \/
人
加
选择 其 中 一 种 尚
要 可 > 人
累计 时 间 从 0 开 SN
始 ， 目 标 工序 设
定 为 1
7 SS =
5 二
/ ¥ 人 计 完 成 fF 业 时 间
过
rhy AS
RGVEjiR: 1
|
|=
_ | V 1 发 出 信号
ooHE-G>-
汶 - 是 低 CNC 是 否 已 育 +
N ReT 工件
业 ， 目标 工序 变 &
为 1
最 佳 的 方案
图 3 情况 2 的 流程 图
9

<!-- source_page: 10 -->

村
5.1. 3 概率 故障 下 加 工 一 道 工序 的 情况
(1) RGY 的 动态 调度 模型
实际 生产 生活 中 ， 工 业 流 水 线 上 存在 多 种 不 确定 因素 影响 着 正常 生产 ， 也
影响 了 调度 目标 的 实现 。 情 况 3 指出 CNC 在 加 工 过 程 中 可 能 发 生 概率 为 1% 的 故
障 ， 故 障 发 生 时 该 机 正在 加 工 的 物料 即刻 报废 ， 人 工 排除 故障 需要 10~20 分
钟 ， 排 除 故障 后 该 机 即刻 加 入 作业 序列 。 因 此 在 规划 RGV 动态 调度 模型 时 ， 应
考虑 通过 实时 采集 故障 机 信息 ， 及 时 更 新 ROV 作业 指令 ， 使 得 ROV 工作 不 因 圾
障 机 停滞 ， 从 而 提高 此 智能 加 工 系统 的 生产 效率 。
综 上 ， 建 立 概率 故障 下 获得 最 大 数量 成 料 的 单 目标 规划 模型 如 下 :
决策 变量 为
2
目标 函数 为 ; 3
ImaxZ = max w® -从 2
在 式 (5) - (11) 的 约束 下 ， 增 加 约束 条 件 : 2 \
CH) 机 器 故障 仅 发 生 在 加 工 过 程 中 ， 即
TU (0.7%®) (21T)
其 中 7 为 第 ;人 台 CNC t EESURE ny
(2) 加 工 过 程 中 第 ; 台 CNC 发 生 故 障 的 相 RE 即
(0 -De
P(e) =155% @)
(3) 修理 故障 机 耗 时 10~20 分 钟 ， 即
T~U (600,1200) (23)
eeEHRR C 呈 的 维修 时 间 。
(3) 第 K 轮 上 料 时 发 生 了 艇 障 的 第 [人 台 CNC 表示 为 C9， 当 C 扣 发 生 时 ，
k-1l-8="
e) = 2 [ro 十 7 . /| 上 TCD + 7 C24)
1i=1
etES ACAR HLR BE 75, 且 令 故障 机 的 维修 时 间 等 同 于 故障 机
Ar 间 和 妈
LA ho @
Draw
p) As max Z = max w®
R “
10

<!-- source_page: 11 -->

k=123.;i=12..8
max(x(*) . To) = min Too
TO = max(T0TOOwnasoj 上 TO
8
yxo-1
i=1
et _ £0 +x(1 -£®)
k 8
> zx (Te +T 9) <8x3600，
k=1i=1
q®) = ple+D) 次
8 o
s.t. wk+D = wo 十 D(r® xz);wm -0 2 P ea
i=1 {
T~U (07%) & s)
(0 X SS
P(c®) = 5 As \
Tj)~U(600,1200) X
k-1 8 K
0=3 ( [r 7 O
k=1i=1
C 旨 发 生 时 ， ofi? = 和 -7 多
x® e fo 了] YA
(2) 模型 的 求解 算法 Y
通过 生成 随 栅 数 模拟 故障 与 维修 ， 将 故障 与 维修 等 效 转换 为 CNC 仍 在 工
作 。 采用 与 情况 | 区 相同 的 四 路 构建 让 发 式 华 法 束 出 近似 最 优 解
人 系统 启动 时 刻 ) 开始 ， 通 过 综合 考虑 所 有 历史 需求 信号 和 当
轮 需求 信号 "/ 乒 能 最 快 完成 上 下 料 的 CNC， 并 响应 此 CNC 的 当 轮 需求 信号 ，
对 此 CNC 成 关 轮 上 下 料 的 过 程 ， 随 后 按照 实际 情况 判断 是 否 洗 料 。
3 了 模 所 概率 故障 ， 在 每 一 轮 上 料 时 刻 ， 通 过 生成 均 布 随机 数 来 决定 此 物
知情 有 可 能 在 未 来 的 加 工 过 程 中 发 生 故障 如 果 此 物料 的 加 工 过 程 会 发 生 故
障 , 测 分 别 生成 均 布 随机 数 以 决定 故障 的 发 生 时 刻 和 修复 故障 所 需 的 时 间 ， 并
记录 这 些 信息 。 在 每 一 次 RGV 完成 上 下 料 〈 和 洗 料 ) 时 刻 、RGYV 完成 移动 时
刻 、RGYV 原 地 等 待 时 段 ， 处 理 已 发 生 且 未 曾 处 理 的 故障 ， 将 此 次 故障 与 修复 的
概念 等 效 转 化 为 故障 CNC 正在 加 工 物料 ， 令 此 次 加 工时 间 等 于 修复 时 间 ， 且 此
次 加 工 结束 《〈 即 完成 修复 ) 之 后 此 CNC 中 不 存在 物料 〈 即 产生 故障 的 物料 被 人
为 报废 )。 如 果 发 生 故 障 的 CNC 正好 是 RGV 即将 响应 需求 的 CNC， 则 令 RGYV 原 地
等 待 ， 并 重新 开始 循环 选择 另 一 个 需要 被 相应 需求 的 CNC。
反复 执行 上 述 操作 。 当 累计 超过 8 小 时 ， 中 止 循环 。
11

<!-- source_page: 12 -->

回避
RE
吉
玉生
站 站 区 吉
区
设 守 预 设 参
数 ， 累计 时 间
从 0 开始
超过 8 小 时
画
页 有 RGV 位 Le
复 所 及 时 意
o BIBSRI2 AIRETF EEcNCE
|
0
RGV 所 耗费 的 AL
时 间
=
RGV 完 成 上 下 分 别 计算 RGV 二 下 让 VT
aaly
冶 清 8fF 业 全 CNCI 计 Ere 会 | Dath
= ZrfEAATE) 加 SS
让
过 成 作业  Dd
下 反方 2XG BE
为 最 \
村 四 一
= 工 过 程 中 S 复 所 家 时 间 转
太 的 未 来 发 生 L :
全 CNC 是 否 已 育 根据 最 佳 方 bj 人 换 为 此 CNC 的
和 情人 和 =, RoViED CA 2 SaLews
0 et RN 六
时 中 的 物 扯
1 - 大
梅 此 物 村 的 序 7 二
号 、CNC 序 号 N
y 和 BEth 数 “ 关 s
IOEE  |as— 判 昕 1%i 故 永 情况 人 > 下 人 和 本 全
过 让 训 让 NC 是 否 会 发 生 故 谭 /A \ RQNCAHIES
至 a
& T 出
= @)
4 © fovasisierad
REHALBATHE
人
8 —
出 工件 加 工 情
况 和 故障 记录
-一
图 4 情况 3-1 的 流程 图
_—T
r o—
5. 1. 4 BEEAUHE RONTP3l TFPIR
(1) RGY 疯 动 态 调度 模型
A 得 最 多 成 品
在 式 K5X>(C11) (15) - (18) (21) -〈25) 的 约束 下 ， 获 得 最 多 成 品 模
JS
人 二 (K)
1 N maxZ = max Wab
N k 8
| (Co . f7Go Go . Fo)
nn》 xf (T+TO
k=1i=1
12

<!-- source_page: 13 -->

EiAE
你

k=123.;i=12,..8
max(x( . To) = min Too
rm

8
yxo-1

i=1
zx- 二
a+b=8abeN*
je = £00 4 x09(1— £)
To < 8x 3600 A7

| ER
q®) = pt 2M \)

8 =
SUwC+D = Wo 十 > (1 xx ) ood (27)
oo 任
Te~v (01%) X
wy_ L
PC = 100 K
T()~U(600,1200)
k-1 8 °©
CN O
k=1i=1

(四 发 生 时 FU 可 0 70O — TO
6 发 和 时 伶 让 ”二 07 和 一 7
xm et
Yief12}

®(1,2)

-7 | 居

(2) 本 算法

* 信 成 卫 江 数 模拟 故障 与 维修 ， 将 故障 与 维修 等 效 转换 为 CNC 仍 在 工作 。 采
人 最 优 刀 有 具 分 布 方案 及 情况 2 算法 相同 的 思路 构建 启发 式 算法 求 出 近
/最 杖 解 。

局 择 之 前 在 情况 2 中 的 最 优 刀具 分 布 方案 ， 从 0 时 刻 《〈 即 系统 启动 时 刻 )
开始 ， 通 过 综合 考虑 所 有 历史 需求 信号 和 当 轮 需求 信号 ， 在 所 负责 工序 符合 当
前 目标 工序 的 CNC 中 ， 找 出 能 最 快 完成 上 下 料 的 CNC， 并 响应 此 CNC 的 当 轮 需
求 信号 ， 对 此 CNC 完成 一 轮 上 下 料 的 过 程 ， 随 后 按照 实际 情况 判断 是 否 洗 料 以
及 是 否 改变 目标 工序 。 反 复 执 行 上 述 操作 。

对 于 模拟 概率 故障 ， 算 法 与 上 一 种 算法 完全 一 致 ， 不 再 费 述 。 当 累计 超过 8
小 时 ， 中 止 循环 。

13

<!-- source_page: 14 -->

回味
A
- 各

选择 一 种 最 优

化 的 刀具 分 布

方案 设 填 预 设

超过 8 小 时

rr 人

> sg
i3 前 时 刻 之 前 是 否 存 溢 frreanid
未 处 理 的 故障 记录 。 完成 时 间 ,并
RGV 完 成 上 下 科 RGV 完 成 上 和 到 和
ERAE
市 [REVFH 上 下 和 下 人 Bl 理 村 Naugy 亲 ,累计 时
和 CNC 是 否 B 消 计 完 成 fEJd 间 = SN n bt 条 下 中
洗 作业 , 目标 工 d 由 RSVRF 要 的 时
村 y4
间 最 少 的 方案 为
上 旺 晶 BEHAE 7.\ _
= ) 厅 笨 条 政 际 个 夏
. TRREAE , 人 YL RS
<ehy>- & -] | RS
1A 间 ,并 取 走 故障
0 CNC 中 的 物
可 ，
艺 绚 陋 逢 至 及 J IN 全
工 过 程 中 故障 的 |
基本 8 时 列 和 > = Cvazmes
和 入 二 RCNCEH(ES
. 这
rr o
号 CNC 序 如 人: 站 RGYV 等 待 过 程 中 是 个
EA <
一 3 人
= 况 和 故障 记录
情况 3-2 的 流程 图
~ J_ |
5. 2 任务 一 的 模型 建立 s 一 方法 二 : 仅 考 虑 当 轮 信号 的 调度 模型

本 本埠 记 4 模型 均 在 采用 第 二 类 RGY 的 基础 上 建立 ， 由 于 论文 篇 幅 有 限 以
及 方法 其 相信 方法 二 算法 文中 不 再 展示 。

两 组 RGV 鹿 度 模型 ， 最 关键 的 区 别 即 为 是 否 在 未 接收 到 新 需求 指令 时 进行 预
0 法 二 中 ,此 时 RGY 前 往 第 ; 台 CNC 完成 第 K 轮 上 料 所 用 时 间 为 TCD +
你 当 RGY 移动 前 已 经 接收 到 多 个 需求 信号 时 ， 有

Go . (7(Go (Co (oO | = mi (Go) (k) (Co
max 区 (rg, 十 Tigpt0q00 十 7 和 )] = min (rg, 十 7 和 pa 十 7 和 ) (28)
k 8
k k k k k k
> > xx. (TD 二 To 十 7 十 大 ))<8x3600 (29)
k=1i=1
5. 2. 1 无 故障 下 加 工 一 道 工序 的 情况

在 式 (6) (7) (9) -〈11)〈28) (29) 的 约束 下 ， 建 立 加 工 一 道 工序 情况 想
获得 最 大 数量 成 料 的 模型 "为 ;

14

<!-- source_page: 15 -->

EiiEE
R n
EEEE
max Z = max w®
k=123..;i=12,..8
(9  (700 { p00 ©\| = min (7® + 7® ®
max [x(- (1) + Tooam 十 Ty; )] = min (r7 + pa 十 了 和 )
8
yo-1
i=1
k k k k
hf-= £09 4 10(1 — £09)
k 8
s.t. (9 . (TO TCD (oO L p00 .Fa (29)
) 了 Tao+T 二 7 )<8x3600，
k=1i=1
q® = ple+D) % O
8 o
wk+D) = w(D 十 > (1 xf9) e W
各 2
w® =0
x(9 e {0,1} 人
5. 2. 2 无 故障 下 加 工 两 道 工序 的 情况 NS
在 式 (6) (7) (9) - (11) (15) - (18) (282(29 入 的 约束 下 ， 建 立 加工 两 道
工序 情况 下 最 短 时 间 获 得 最 多 成 品 的 模型 将:
maxZ = max
k 8
(9 . [70O ， TO (0 70o ,FOOD
min) 2 [re” + Tpwgo0 + Ti0 TI |
k=1i=1 全
k=123.;i=12..8 %
®  (70 上 TO N] = min (7® + 7® ®
max [x(- (130 + T50  ¥6)| = min(r + Ti5Ju0 +767)
8
ys-: MY
i=1 ~
of?<s(e0 —)
a+ y/ ab €N*
At 是 EN +x(1-1)
Ni (30)
YN 0 .(Tra TO (9 下 T0o ,Fa
] 站 (2 二 Too 十 TD 二 TO 天 ) <8x3600
k=1i=1
加 二 pletD)
8
wk+D = wo 十 D(r® )
i=1
w® =0
x® €{0,1}
Ye{1,2}
®e(1,2)
15

<!-- source_page: 16 -->

EigaE
ELye
5. 2. 3 概率 故障 下 加 工 一 道 工序 的 情况
在 式 (6) (7) (9) - (11) (21) - (25) (28) (29) 的 约束 下 ， 建 立 获得
概率 故障 情况 下 加 工 一 道 工序 的 最 大 数量 成 料 的 模型 为 :
maxZ = max w®
k=123.;i=12,.8
max -mn(g rarz)
8
yo-1
i=1
hf-= £09 4 10(1 — £09)
» 4
09. (TO 上 TD (9 上 To .Fa
六 (CR +TBowo+TR + TS )s8x 3600, \
k=1i=1
q® = p+D 2XG
ar ,
GD 二 (@ (09 .09 4
Leower20o 人
=1 NS
本 从
(9 @® =
r-(or) RK
1
®) =
P(c*) = 155
T{)~U(600,1200) °
| k-1 8 人 MG ©
(9 _ @, [p0) Lp0@ .roT TOO AT
t = 2, 2 B [ F 1i 7
k=1i=1
COREN, 1 =1®
xx € {0~ 小
5.2.4 1
在 , (9) - (11) (15) - (18) (21) - (25) (28) (29) 约束 下 ，
建立 获得 概率 页 障 情况 下 加 工 两 道 工 序 的 最 短 时 间 获 得 最 大 数量 成 料 的 模型 ”
N_ max Z = max w(o
b
SA， k 8 “
i (9 . [709 709 ® | TO .0
mi 2 对 [+ Toam +TR TI
k=1i=1
16

<!-- source_page: 17 -->

EigaE
pA
站 放款
k=123.;i=12,.8
xl e {0,1}
max [+{ (7g8)+ Tiwge + Ti))] = min (Tgd + Tofloro +7330)
8
yo-1
i=1
#0 = xO(1 - -名
atb=8abeN*
je = £09 4 10(1- £09)
k 8 四
(9 . (TO TD (oO L p00 .Fa
之 2 (T” + Tiipguo +T + 放生 8x 3600. o
=1i=1 一
q0 = pl+D) 2XG \
8
s.t. 了 (32)
warD = w+ (F .xz
2 人
woO=0
(9 C) =
rar 和
-=- 工
P(c)= 100
7 名 ~U(600,1200) e@
k-1 8 人 MG °©
tm 一 》 》 fce . [ze 子 AAA HG 十 TO 十 了
k=1i=1
Cf 发 生 时 ， +Y Zoat) =Ty
soon 下
Yie(1,2}
5,)V
\“//a,
Se
SS | 用 题 给 3 组 参数 检验 模型 的 实用 性 与 算法 的 有 效 性 。
1 于 模型 的 实用 性
流 了 更 准确 地 描述 RGV 动态 调度 模型 的 实用 性 ， 本 文 从 实施 的 可 行 性 ”、 经
济 性 、 普 适 性 三 个 方面 分 别 进行 研究 。
巴 实施 的 可 行 性
一 个 可 行 性 高 的 调度 模型 不 能 脱离 实际 ， 应 能 实施 到 实际 生产 中 。RGY 的 动
态 调度 模型 是 否 能 运用 在 实际 生产 中 是 实施 的 可 行 性 的 最 重要 因素 。
加 经 济 性
一 个 好 的 调度 模型 能 实现 缩短 生产 周期 、 降 低 生产 成 本 、 提 高 生产 效率 等
目标 ， 进 而 提高 系统 的 经 济 效益 。RGYV 的 动态 调度 模型 直接 影响 该 智能 加 工 系
统 的 生产 能 力 ， 通 过 经 济 性 衡量 模型 的 实用 性 是 合适 的 。
17

<!-- source_page: 18 -->

回 成 革 动 国
ai
这 里 情况 1 和 2 下 ， 引 入 理想 总 完成 加 工 数 ， 意 指 在 一 个 班次 内 所 有 CNC
处 于 不 间断 工作 状态 。 用 实际 总 完成 加 工 数 与 理想 总 完成 加 工 数 表 的 比例 大 小
来 反应 其 经 济 性 的 高 低 。
@ 普 适 性
普 适 性 强 的 调度 模型 ， 能 对 同类 生产 对 象 、 流 水 线 具 有 普遍 的 适用 性 。
@CNC 平均 非 有 效 工 作 时 长
由 于 RGV 总 工作 时 长 受 总 产量 影响 ， 因 此 使 用 RGV 总 工作 时 间 计 算 可 得 CNC
平均 非 有 效 工 作 时 长 ， 便 于 对 其 进行 准确 的 评价 。
(RGV 总 工作 时 间 x8 -成 料 数 :7
CNC 平均 非 有 效 工人 时 长 = 一 (33)
(2) 算法 的 有 效 性 y
为 了 更 准确 地 描述 RGY 动态 调度 模型 所 对 应 算法 的 有 效 性 ， 本 文 悍 记 的
运行 总 时 长 与 程序 运行 占用 内 存 两 个 方面 分 别 进行 研究 。 \
外 程序 总 运行 时 长 yA _g
总 运行 时 长 短 的 程序 ， 能 快速 得 到 结果 ， 运 行 结 果 在 实 5
性 。 程 序 总 运行 时 间 越 得， 运行 结果 的 时 效 性 越 好 ， / 扯 江 的 有 效 性 越 高 。 程序
基于 Intel (R) Core (TM) i7-6700HQ2. 60GHz2. 60GHz 处 理 RIBAT
名 程序 运行 占用 内 存 罗 >
Matlab 内 存 占用 量 反 映 了 此 程序 的 优化 程度 ; 存 占用 量 越 小 ， 程 序 对 计
算 机 的 性 能 要 求 越 低 ， 算 法 的 实用 性 越 高 。 当 Wiat1la5 (R2018a) 空闲 时 在 本 机
上 的 内 存 占用 量 为 1434MB。
o
5. 3. 工 对 无 故障 下 一 道 工 序 的 两 种 有 V 动态 调度 模型 的 求解 与 检验
表 1; 情况 1 各 组 参量 在 两 种 方法 下 的 检验 结果
TaTZ EE CRES R E
WR1| re angs | EL | 万 于 2 | EL | e
理想 总 完成 加 RN 101
I 数 ( 件 |
站 完成 加 工 数 | vs
fny JWP | ow | om [m | me | w
igs//| 75 | o1ow | s6.3n | woen | on.ton | som
ONC 平均 非 有 效
TD 昨 时 全 3800. 3
下 7 可
下 作 时 间
ROVL TAER
| |
程序 总 运行 时
加
Matlab 内 存 占
抽 | to | w | wwr | me | oe | m
通过 循环 遍历 法 ， 在 同时 满足 两 个 决策 目标 的 情况 下 ， 组 1 得 到 了 8 种 最
优 刀 具 分 布 方案 ， 组 2 得 到 了 1 种 最 优 刀 有 具 分 布 方案 ， 组 3 得 到 了 2 种 最 优 刀
有 具 分 布 方案 ， 有 具体 分 配方 案 如 表 2。 由 于 这 些 刀 有 具 分 布 方案 同时 满足 了 两 个 决
18

<!-- source_page: 19 -->

回 8 昌国
策 目标 ， 因 此 在 后 文 情况 3 的 模型 求解 中 ， 每 组 选用 其 中 一 种 刀具 分 布 方案 来
进行 求解 。

表 2: 情况 2 中 3 组 参量 下 的 刀具 分 配方 案
[人
Goal ara
oczE| 2 [2 |2 [2 [22[2 2 1]2]z
Ge 2 [2[2 [2 [t[1[1[1[z][1]1
Got az az
Gil aaazla2aliila 2
Ge il il2zlalilil zz
coal zz
G3E E E E  HE RE
+/
5. 3.2 对 无 故障 下 两 道 工序 的 两 种 RGY 动态 调度 模型 的 wigg
表 3: 情况 2 中 3 HLBRIEFFE FIkGL §
Ti | 和 队 | 而 5
[| | 7
理想 总 完成 而 WoA SS 国
工 数 〈 件 ) “1 s
总 完成 加 工 数
人
EH| 到 0 | 绍 的 7 而 5 | aer | om | 入 5
CNC 平均 非 有 效 AAA
工作 时 长 9 | 9549
RGV 总 工作 时 间 |
2 2 | 2 | |
EECIEOCEES
和 本
用 量 qi)
WA
已 人
中 、
5 卫 尖 概率 故 陪 下 _ 道 工序 的 两 种 RGV 动态 调度 模型 的 求解 与 检验
表 4: 情况 3 〈1) 中 3 组 参量 在 两 种 方法 下 的 检验 结果
RE HT | 9 |  @3
况 1) | 方法 1 | 方法 2 | 方法 1 | 方法 2 | 方法 1 | 方法 ?
总 完成 加 工 数 357
〈 件 )
CNC 平均 非 有 效
工作 时 长 4099
( 秒 )
19

<!-- source_page: 20 -->

Da 口 |
村
Eu EECE EECIEZ
〈 秒 )
故障 次 数 | 3 | 3 | 3 | 2 | 4 | 4
es
Matlab 内 存 占
TENEIEIEIEIEE
5. 3.4 对 概率 故障 下 两 道 工序 的 两 种 RGV 动态 调度 的 模型 求解 与 检验
表 5: 情况 3 (2) 中 3 组 参量 在 两 种 方法 下 的 检验 结果
情况 3 (基于 情况 | 组 1 | 组 2 ] 组 3
Er 二
总 完成 加 工 炎 有 |
天 本 本 本 本 本 本 本 全
CNC 平均 非 有 效 工 再
作 时 长 〈 秒 ) 《了 全
RGV 总 工作 时 间 8636 区
了 了 天 二
工序 1CNC 故障 次 |
£or  |RT
| 飞
TS
Ti oe
Matlab 内 存 占 用 AN
2
加 Z2)
5. 3.5 基 于 3 种 情况 对 六 次 术 及 算 的 评 从
(1) 模型 实用 性 的 尝 价 |
@ 实 施 的 可 行 性 = 根据 表 1、3、4、5 与 模型 ， 在 一 个 班次 内 能 够 完整 并 较
好 地 对 pov | 人
Day. 根据 表 1、3 与 模型 ， 在 一 个 班次 内 ， 总 完成 加 工 数目 与 理想 总
完成 加 夫人 下 不 大 ， 说 明了 模型 有 较 高 的 经 济 性 。
得 SY 根 据 表 1、3、4、5，RGV 调度 模型 能 对 不 同 3 组 参数 进行 求
全 放生 四 说 明了 模型 的 普 适 性 。
TAR ， 本 文 所 建立 的 单 RGV 动态 调度 模型 具有 实用 性 。
(2) 算法 有 效 性 的 评价
名 程序 总 运行 时 长 : 根据 表 1、3、4、5， 利 用 计算 机 安排 计算 出 一 个 班次
内 的 调度 方案 所 花 的 时 间 都 非常 的 短 。
@@ 程 序 运行 占用 内 存 : 根据 表 1、3、4、5， 计 算 机 在 进行 安排 调度 方案 ，
所 占用 的 运行 内 存 整 体 偏 小 。
综 上 ， 本 文 所 建立 的 单 RGV 动态 调度 模型 所 对 应 的 算法 具有 有 效 性 。
20

<!-- source_page: 21 -->

杞 所
EEEE
5. 3. 6 基于 情况 1、2 对 两 种 RGV 动态 调度 模型 进行 比较
由 于 ， 情 况 3 存在 随机 因素 ， 模 拟 过 程 中 ， 随 机 因素 对 结果 的 影响 很 难 消
除 ， 因 此 只 基于 情况 1、2 对 两 种 RGV 动态 调度 模型 进行 比较 。
表 4: 情况 1 中 3 组 参量 在 两 种 方法 下 的 成 料 数
LT
全 山上 记 基 1 万 基 2 | EL [ JE | ET | 放下 2
理想 成 料 数 401
〈 件 )
天 有数 (FT 3 3 | 3 3 | [96
根据 表 4， 利 用 柱状 图 表示 其 差异 ， 如 图 6: _
450 es D)
[—7
400 ] 所 蕊 二
理想 情况
350 ‖ 于
国门
300 | |
F 目
—1 250 p
训 200 {
Ea] SN
150
100 有
60 /
0 f
旗 2 3
组 别
图 \tn Lmres as
表 5 汪 情况 2 中 3 组 参量 在 两 种 方法 下 的 成 料 数
TIRSUL | 9 | m3
全 吕 30 | 才 寺 1 | 万 法 2 | EL | JE | ET | 万
9
NU 件 ) 羡
 | aa Ta | ar | 2 | 39 2
\ 根据 表 5， 利用 柱状 图 表示 其 差异 ， 如 图 7:
21

<!-- source_page: 22 -->

EE
村
。
方法 二
300 故国 理想 情况
250
# 200
全
1= 150
3
100 #7
1Q7
50
i \)
0 上 0
1 2 )
组 别 j 人 ;
图 7 ”情况 2 两 种 方法 各 组 别 笑料 数
综 上 ,由 图 6 与 图 7 可 以 得 到 ， 在 情况 1、 仿 KEy 在 一 个 班次 内 ， 方 法 一 所 产
出 的 成 料 总 数 更 加 接近 理想 成 料 总 数 ， 条 优 于 方法 二 。
AS
六 、 模 型 的 检验
6. 1 仿真 检验 o
o T BUERU 3 S SR TT  ASCR = H
新 组 合 得 到 仿真 数据 ， 如 表 7
1 六 考 7 仿真 数据 表
| 系统 作业 参数 时 长
一 RCV| 移 动 1 个 单位 所 需 果 间 20
FRRGV 移动 2 个 单位 所 需 时 间
=/ | RGV 移动 3 个 单位 所 需 时 间 16
ZIBNC 加 工 完成 一 个 一 道 工序 的 物料 所 需 时 间 560
A ON 帮工 完成 一 个 两 道 工序 物料 的 第 一 道 工序 所 需 时 间 155
人 ONC 加 工 完成 一 个 两 道 工序 物料 的 第 二 道 工序 所 需 时 间 500
TAN 。 RGV 为 CNCI#，3#，5#，7# 一 轮 上 下 料 所 需 时 间 28
RGV 为 CNC2#，4#，6#，8# 一 轮 上 下 料 所 需 时 间 35
RGV 完成 一 个 物料 的 清洗 作业 所 需 时 间 %
根据 表 7 中 的 系统 作业 参数 ， 对 CNC 概率 故障 情况 下 加 工 两 道 工序 的 物料
进行 最 快 获得 最 多 成 品 的 双 目标 规划 ， 检 验 结果 如 表 8:
22

<!-- source_page: 23 -->

BEEE
表 8 。 仿真 检验 结果 表
本 情况 3 《基于 情况 9
模型 的 检验 方法 1
成 料 歼 《 作 ) 201
ONC PHAEA2 LAEITE (7) 1338.5
最 终 完 成 物料 清洗 时 刻 《 秒 ) 28751
程序 总 运行 时 长 〈 移 ) 0.006976
工序 10NC 故障 次 数 1
工序 2CNC 故障 次 数 2
算法 空间 复杂 度 00D _
算法 时 间 复杂 度 | om2 AR
-YYS
七 、 模 型 的 评价
7.1 模型 的 评价 &
7.1. 1 模型 的 优点 多 \
针对 情况 1 的 模型 1; N

对 于 单 道 工序 的 RGV 调度 模型 ， 人 人 入 ， 而 且 能 够 运用 该 模
和
效 性 ，
针对 情况 2 的 模型 2:

对 于 双 才 工序 的 RGY 调度 本 虹 , 我 们 全 型 的 基础 上 加 入 了 目标 工序 的
概念 ， 以 此 来 保证 RGV 中 的 物料 并 放 与 ONC 工序 相 匹配 。 另 外 ， 本 题 中 ， 由 于
工艺 流程 比较 简单 ， 对 于 模型 的 各 名 采 用 循环 遍历 法 ， 能 够 找到 各 刀具 数量 与
位 置 的 最 佳 分 配方 案 。
针对 情况 3 的 模型 3;

在 模型 1、2 的 前 提 我 们 还 建立 故障 模拟 模型 ， 能 够 较 好 地 表示 出 1% 的
故障 发 生 概率 ， 而 竺 能 够 及 时 发 现 与 处 理 故障 CNC， 提 高 了 工作 的 效率 ， 从 而
Betk EL EE T
7.1.2 模型 的 缺点 【

HSC 出 :

- 册 于 齐 道 工序 的 ROY 调度 模型 ， 在 实际 生产 过 程 中 ， 信 号 的 发 出 与 接受 并
全 es 会 有 时 间 延 迟 ， 这 是 该 模型 未 考虑 的 。

[ 译 情 况 2 的 模型

允 于 双 道 工序 的 RGV 调度 模型 ， 由 于 题目 CNC 台数 偏 少 只 有 八 台 ， 且 物料
加 工 工序 次 数 只 有 两 次 ， 对 于 模型 的 求解 ， 采 用 了 循环 遍历 法 就 能 够 很 快 找 出
各 刀具 数量 与 位 置 的 最 优 分 配方 案 。 当 CNC 数目 与 加 工 工序 次 数 增加 时 ， 模 型
的 求解 时 间 会 以 指数 倍增 长 ， 那 么 算法 的 就 不 是 很 具有 有 效 性 。
针对 情况 3 的 模型;

对 于 CNC 故障 模拟 下 RGV 调度 模型 ， 由 于 故障 CNC 修理 时 间 是 10-20 分
钟 。 在 现实 生活 中 ， 修 理 时 间 可 能 是 属于 10-20 分 钟 间 无 规律 或 有 传统 的 分
布 ， 而 我 们 以 均匀 分 布 来 确定 我 们 的 修理 时 间 ， 这 里 降低 了 模型 的 实用 性 。

23

<!-- source_page: 24 -->

回 吕 过
Efes
八 、 模 型 的 改进
8. 1 模型 的 改进

〈1) 在 实际 生产 中 ， 延 迟 时 间 会 由 多 种 随机 因素 决定 ， 因 此 使 用 一 个 固定
的 近似 延迟 时 间 来 将 其 代替 并 纳入 模型 的 计算 ， 以 尽 可 能 减 小 误差 。

(2) 当 CNC 数量 增多 时 ， 使 用 遗传 算法 、 蚁 群 算法 等 近似 最 优 解 算法 来 计
算 刀 具 分 布 方案 ， 进 而 提高 计算 效率 。

(3) 结合 现实 中 的 故障 发 生 情况 ， 制 订 更 加 接近 真实 情况 的 故障 发 生 方
案 ， 使 仿真 结果 更 加 符合 真实 情况 。

九 、 模 型 的 推广 和 应 用 _

此 次 基于 RGYV 的 单 RGV 动态 调度 模型 的 建立 与 解决 有 着 重要 的 L 阁 多，
单 RGV 调度 在 工业 生产 、 终 端 排序 、 云 调度 系统 等 领域 具有 灵活 的 重要 的 应
用 价值 。 ARAIEAIE SAATIAE EE  H
着 广泛 应 用 。 A 4=
参考 文献 ;

Le
[ 匡 姜 启 源 ， 谢 金星 ， 叶 俊 . 数学 模型 第 愤 版 ) 人 . 北京 : 高 等 教育 出 版 社 ，2003. 85-130.
[2] 张 继 坤 . 浅 谈 应 用 技术 成 果实 用 性 角 和 [J]. 科学 管理 研究 , 1989, 04: 43-45.
一
Vlo
e-
24

<!-- source_page: 25 -->

下
站 六 和

附录 :
所 有 代码 基于 Matlab R2018a
代码 文件 名 与 问题 的 对 应 关系
情况 一 方法 一 第 一 组 : Situation1Team1.m
情况 一 方法 一 第 二 组 : Situation1Team2.m
情况 一 方法 一 第 三 组 : Situation1Team3.m
情况 二 方法 一 第 一 组 : Situation2Team1.m
情况 二 方法 一 第 二 组 : Situation2Team2.m
情况 二 方法 一 第 三 组 : Situation3Team3.m
单 工序 情况 三 方法 一 第 一 组 : Situation3_1Team1l.m A7
单 工序 情况 三 方法 一 第 二 组 : Situation3_1Team2.m 全 NY
单 工序 情况 三 方法 一 第 三 组 :Situation3_1Team3.m _ “由
双 工 序 情 况 三 方法 一 第 一 组 :Situation3_2Team1.m 2XG
双 工序 情况 三 方法 一 第 二 组 : Situation3_2Team2.m ood
双 工 序 情 况 三 方法 一 第 三 组 ;Situation3_2Team3.m
情况 一 方法 二 第 一 组 : Simplify_Situation1Team1.m As
情况 一 方法 二 第 二 组 : Simplify_Situation1Team2.m ”全
情况 一 方法 二 第 三 组 : Simplify_Situation1Team3.m X
情况 二 方法 二 第 一 组 : Simplify_Situation2Team1.m
情况 二 方法 二 第 二 组 : Simplify_Situation2Team2.m
情况 二 方法 二 第 三 组 : Simplify_Situation3Team3.m
单 工序 情况 三 方法 二 第 一 组 : Simplify, Situation3_1Team1.m
单 工序 情况 三 方法 二 第 二 组 : sona nnon
单 工序 情况 三 方法 二 第 三 组 : Simp fiy Situation3_1Team3.m
EAEA cptpoi
双 工 序 情 况 三 方法 二 第 二 绍 河 Simplify_Ssituation3_2Team2.m
ETHR=E=Eo, Frtoit, shontons 2
绘图 的 代码 : Plot.
alt Msn

Zn
om， 下 文 仅 给 出 各 类 型 第 一 组 的 代码 。
SA
有 证 方 法 一 第 一 组 的 代码
Situation1Team1.m
% 情 况 1 下 的 代码
clear;clc;
%% 计时
tic
%% 输入 不 同 组 别 参数
Move=[0,20,33,46];% 第 一 组 [0,20,33,46] 第 二 组 [0,23,41,59] 第 三 组 [0,18,32,46]
Work=560;% 第 一 组 560 第 二 组 580 第 三 组 545
Switch=repmat([28,31],1,4);% 第 一 组 [28,31] 第 二 组 [30,35] 第 三 组 [27,32]

25

<!-- source_page: 26 -->

区
加 只 RN
Wash=25;% 第 一 组 25 第 二 组 30 第 三 组 25
%% 预 设 系统 情况
Position=1;% 记 录 RGV 的 位 置 ， 取 值 为 1~4
Left=zeros(18);% 记 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation=zeros(18);% 记 录 8 台 CNC 当前 是 否 拥有 工件 ，0 为 无 ，1 为 有
Time=0;% 系 统 已 运行 时 间
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和
Rec=[];% 记 录 每 个 工件 的 上 下 料 信息
%% 系统 开始 运行
while Time<=28800
fori=1:8% 计 算 预 计时 间 A7
Expect(1,i)=Move(1+abs(Position-ceil(i/2))); 一 NY
if Left(i)<=Expect(1,i) 加 \)
Expect(2,i)=0; 2XG
else ood
Expect(2,i)=Left(i)-Expect(1,i);
end As
Expect(3,i)=Switch(i);
Expect(4,i)=sum(Expect(1:3,i)); X
end
[MinNumber]=min(Expect(4,:));% 找 出 下 一 个 目标
Time=Time+Expect(1,MinNumber)+Expect(2, MinNumber);%RGV 移动 至 下 一 个 目标 位 置 并
等 待 AAA O
flag=0;% 目 标 CNC 是 否 已 有 工 Ye 1 为 有
fori=size(Rec1):-1:1% 记 录 本 次 操作 的 里 刻
if Rec(i,1)==MinNu && isnan(Rec(i3))% 同 时 发 生 上 料 和 下 料
flag=1;
Rao 二 下 料 开 始 时 间
Rec= 人 限 eciMinNumberTime,NaN];% 记 录 上 料 开始 时 间
ed V
//
mv
SS 发 生 上 料
To
if Situation(MinNumber)==0% 不 用 清洗 的 情况
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber);% 完 成 换 料
fori=1:8%CNC 的 时 间 推 进
if Left(i)-Expect(4,MinNumber)<0
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber);
26

<!-- source_page: 27 -->

3
加 只 RN
end
end
Left(MinNumber)j=Work;% 换 料 的 CNC 更 新 剩余 时 间
else% 需 要 清洗 的 情况
Time=Time+Expect(3,MinNumberj+Wash;% 完 成 换 料 与 清洗
fori=1:8%CNC 的 时 间 推 进
if Left(i)-Expect(4,MinNumber)-Wash<0
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber)-Wash;
end
end A7
Left(MinNumber)j=Work-Wash;% 换 料 的 CNC 更 新 剩余 时 间 一 NY
end 由
Position=ceil(MinNumber/2); %RGV 位 置 更 新 2XG
end Ls of
while ~(Rec(end,3)+Expect(3,MinNumberj+Wash<=28800)% 筛 选 均 陈 狗 缘 无 效 数据
Rec(end,:)=[]; As \ \
end &
n X
SUM=size(Rec1);% 成 料 数
WAIT=(Rec(end,3)*8-size(Rec,1)*Work)/8;%CNC 平均 非 有 效 工 作 时 长
Last=Rec(end,3)+Expect(3,MinNumber)+Wash;% 最 终 完成 物料 清洗 时 刻
%% 计时 [e]
人
clear Expect flag i Left MinNumber Move Position Situation Switch Time Wash Work;
memory 和 NS-
用 于 情况 二 方法 _ 生 -0 他
Situation2Team1.m
% 情 况 2 动 徊 | V
clear;clc; //
2 和
tie L
&% 谢 捕 环 同 组 别 参数
证 oos aaa 第 二 组 [0,23,41,59] 第 三 组 [0,18,32,46]
Work=[400,378];% 第 一 组 [400,378] 第 二 组 [280,500] 第 三 组 [455,182]
Switch=repmat([28,31],1,4);% 第 一 组 [28,31] 第 二 组 [30,35] 第 三 组 [27,32]
Wash=25;% 第 一 组 25 第 二 组 30 第 三 组 25
%% 记录 所 有 刀具 分 布 情况 下 的 工作 情况
Rec=cell(11);% 用 以 记录 每 一 种 刀具 分 布 情况 下 的 完整 加 工 情况
Statistics=[];% 统 计 成 功 加 工 数 和 失败 加 工 数
Order=[];% 记 录 每 一 种 刀具 分 布 方案
%% 遍历 所 有 刀具 分 布 情况
27

<!-- source_page: 28 -->

Snud
[EEREEs
fori=1:7% 刀 具 2 的 数量
Type=nchoosek(1:8,i);% 生 成 所 有 的 组 合 情 况
forj=1:size(Type,1)% 确 定 一 种 刀具 分 布 情 况
Tool=ones(1,8);
for k=1:size(Type(j,:),2)
Tool(Type(j k))=2;
end
Order=[Order;Tool];
Position=1;% 记 录 RGV 的 位 置 ， 取 值 为 1*4
Left=zeros(1,8);% 记 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation=zeros(1,8);% 记 录 8 台 CNC 当前 是 否 拥有 工件 ，0 为 无 ，1 为 有
Time=0;% 系 统 已 运行 时 间 2
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 GM 加， 第
三 行为 预计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和 _ R
mghec- 记录
Now=1;% 当 前 RGV 目标 工序 ， 取 值 仅 为 1 或 2 ond
while Time<=28800
for k=1:8% 计 算 预 期 时 间 As
if Now*=Tool(g% 排 除非 目标 工序 的 色 NC
Expect(:,k)=inf; K
continue;
end
Expect(1,k)=Move(1+abs(Pgsition-ceil(k/2)));
if Left(k)<=Expect(Z;k) O
eeooy 人
else
Exp )=Left(k)-Expect(1k;
end
RA - J
k)=sum(Expect(1:3,k));
-oo
Higttommasssic  iv
下 =Time+Expect(1,MinNumber)+Expect(2,MinNumbenr);% 移 动 至 下 一 个 目标 位
| < 放 Now==1% 当 前 目标 是 工序 1 的 CNC
N flag=0;
for k=size(TempRec1)j:-1:1% 记 录 本 次 操作 时 刻
if TempRec(k,1)==MinNumber && isnan(TempRec(k,3))% 同 时 发 生 上 料
和 下 料
flag=1;
TempRec(k,3)=Time;
TempRec(end+1,1)=MinNumber;
TempRec(end,2)=Time;
TempRec(end,3:6)=NaN;% 构 建 此 工件 工序 2 ff)id HHEpE
28

<!-- source_page: 29 -->

—
下
二 二
回 共 RE
break;
end
end
放 flag==0% 仅 发 生 上 料
TempRec(end+1,1)=MinNumber;
TempRec(end,2)=Time;
TempRec(end,3:6)=NaN;
end
if Situation(MinNumber)j==1% 换 料 时 取 下 了 一 个 已 经 完成 工序 1 的 工件
Now=2;% 下 一 道 目 标 工序 发 生变 化
NEXT=k;% 记 录 此 工件 的 序号
end A7
Situation(MinNumber)=1; 二 NY
Time=Time+Expect(3,MinNumber);% 完 成 换 料 一 \)
for k=1:8 2XG
if Left(k)-Expect(4,MinNumber)<0 ood
Left(k)=0;
else A
ee R :
end 全
end
Left(MinNumber)=Work(1);
else% 当 前 目标 是 工序 2 的 ONG
flag=0; O
cars
if TempRec(k,4)==MinNumber && isnan(TempRec(k,6))% 取 下 已 完成 工
件 SN 一
~r TempRec(k,6)=Time;
TempRec(NEXT,4)=MinNumber;
一 ) V TempRec(NEXT,5)=Time;
7 break;
下 4 end
p) end
| // §- ifflag==0% 放 置 待 加 工 工序 2 的 工件
SA， TempRec(NEXT,4)=MinNumber;
TempRec(NEXT,5)=Time;
end
Now=1;% 此 时 目标 工序 重新 变 为 工序 1
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber)j+Wash;% 完 成 换 料
for k=1:8
if Left(k)-Expect(4, MinNumber)-Wash<0
Left(k)=0;
29

<!-- source_page: 30 -->

an
下
近
加 只 RN
else
Left(k)=Left(k)-Expect(,MinNumber)-Wash;
end
end
Left(MinNumber)=Work(2)-Wash;
end
Position=ceil(MinNumber/2);% 更 新 位 置
end
Rec=[RecTempRec];% 记 录 本 次 刀具 分 布 情况 下 的 完整 加 工 情况
Statistics=[Statistics;0,0];% 统 计 本 次 刀具 分 布 情况 下 的 成 功 加 工 数 和 失败 加 工 数
for k=1:size(TempRec,1)
if isnan(sum(TempRec(k,:))) A7
Statistics(end,2)=Statistics(end,2)+1; 一 NY
else o/z 由
Statistics(end,1)=Statistics(end,1)+1;
end ood
end
end As
end 会
%9%6 对 所 有 情况 数据 的 分 析 X
Rec(1)=[]; K
MaxProduct=max(Statistics(:,1));% 最 大 产量
CompleteTime=inf;% 产 量 最 大 情况 下 的 最 短 完 成 时 间
Bestplan-cell(.3;% 产 量 最 大 旦 完成 网 丫 最 得 的 物料 加 工 情 况
人
fori=l:size(Rec,2)% 找 出 产量 最 大 情况 :的 入 短 完 成 时 间
if Statistics(i,1)==MaxProduct
for Cn
J =
if ~isnan(Rec{L,i}j,6))
i}(j,6)<=CompleteTime
o 】 ah
7 end
下 C-
含 nd
a
end
fori=1:size(Rec2)% 找 出 产量 最 大 且 完 成 时 间 最 短 的 所 有 方案 并 记录
if Statistics(i,1)==MaxProduct
for j=size(Rec{1,i},1):-1:1
if ~isnan(Rec{1,i}(j,6))
if Rec{1,i}(j,6)==CompleteTime
BestPlan=[BestPlan,Rec{1,i}];
BestKnife=[BestKnife;Order(i,:)];
30

<!-- source_page: 31 -->

3
加 只 RN
end
break;
end
end

end
end
BestPlan(1)=[];
REC=BestPlan{lend};% 挑 选 一 个 最 佳 方案
while ~(REC(end,6)+Expect(3,MinNumber)+Wash<=28800)

REC(end,:)=[];
end
%% 计算 y
SUM=size(REC,1);% 成 料 数 二 从 >
WAIT=(REC(end,6)*8-size(REC,1)*sum(Work))/8;%CNC 平均 非 有 效 工作 时 长 \)
Cclons beeaNomWahAREARBAT ) 2
%% 计时 ood
toc p SS
clear CompleteTime Expect flag jj k Left MaxProduct MinNumb et Move N XT Now Order Position
Situation Switch TempRec Time Tool Type Wash Work; ”全
memory AR
用 于 单 工序 情况 三 方法 一 第 一 组 的 代码
Situation3_1Team1.m @
% 情 况 3〈 基 于 情况 1) 下 的 代码 4 O
clear;clc; YA
%% 计时
tic 放
%% 输入 不 同 组 别 参数
woue<o205346]& 息 和 1 第 二 组 [0,23,41,59] 第 三 组 [0,18,32,46]
Work=560;%3 —4 #—4H 580 第 三 组 545
Switch=repma b o 第 二 组 [30,35] 第 三 组 [27,32]
Wash=2 > 第 二 组 30 第 三 组 25
人
Pasitio AEL%iSk RGY 的 位 置 ， 取 值 为 1r4
RegFamis s & onc 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Sitbatiof-zeros(1.8);% 记 录 8 台 CNC 当前 是 否 拥有 工件，0 为 无 ，1 为 有
Time=0;% 系 统 已 运行 时 间
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和
Rec=[];% 记 录 每 个 工件 的 上 下 料 信 息
Error=[];% 记 录 故 障 信息
%% 系统 开始 运行
while Time<=28800

fori=1:size(Errop1)% 检 查 错误 信息

31

<!-- source_page: 32 -->

Snud
[EEREEs
if Time>=Error(i,3) && Time<=Error(i,4) && Error(;5)==0% 故 障 已 发 生
Error(j5)=1;% 标 记 为 已 处 理
Left(Error(j2))=Error(li4)-Time;% 将 故障 修复 所 需 时 间 转 换 为 当前 工作 剩余 完成
时 间
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
end
end
fori=1:8% 计 算 预 计时 间
Expect(1,i)=Move(1+abs(Position-ceil(i/2)));
if Left(i)<=Expect(1,i)
Expect(2,i)=0;
else A7
Expect(2,i)=Left(i)-Expect(L,i); 二 NY
end 一 \)
Expect(3,i)=Switch(i); 2XG
Expect(4,i)=sum(Expect(1:3,i)); ood
end SS
[MinNumberj=min(Expect(4,:));% 找 出 下 一 个 目标 As SS
Time=Time+Expect(1MinNumber);%RGYV 2 六 ROAS
flag=0; 多
fori=1:size(Erron1)% 运 动 后 再 次 检查 错误 信息
if Time>=Error(i,3) && Time<=Error(i,4) && Error(i,5)==0 && MinNumber==Error(i,2)%
运动 中 原 目标 发 生 了 故障 ®
Errorl5)=1;% 标 记 为 由 于 O
onerkratohn 地 aaaearf
forj=1:8%CNC 的 时 间 扒 进 )
if Left()-EX pect(1,MinNumber)<0
Left( -
alse--”
(j)=Left(j)-Expect(1,MinNumber);
2
oreooomeapaapamaamaoanreaaan
时
i 兴 - flag=1;
N end
end
iflag% 由 于 原 目 标 CNC 发 生 故 障 ， 重 启 循环
continue;
end
flag=0;
fori=l:size(Erron1)% 等 待 中 检查 错误 信息
if Time<=Error(i,3) && Time+Expect(2,MinNumber)>=Error(i,3) && Error(i,5)==0 &&
MinNumber==Error(j2)% 等 待 中 原 目标 发 生 了 故障
32

<!-- source_page: 33 -->

下
总
加 只 RN
Error(j5)=1;% 标 记 为 已 处 理
Situation(Errorlj2))=0;% 修 复 完 成 后 取 走 故障 工件
for j=1:8%CNC 的 时 间 推 进
if Left(j)-(Error(i,3)-Time)<0
Left(j)=0;
else
Left(j)=Left(j)-(Error(i,3)-Time);
end
end
Left(Error(j2))=Errorli4)-Error(;3);% 将 故障 修复 所 需 时 间 转 换 为 当前 工作 剩余
完成 时 间
Time=Error(;3);% 时 间 调 整 至 故障 发 生 时 A7
flag=1; 二 NY
end 一 \)
end 2XG
ifflag% 由 于 原 目标 CNC 发 生 故 障 ， 重 启 循环 ood
continue;
end As
Time=Time+Expect(2,MinNumber);% 正 常 等 待 &
flag=0;% 目 标 CNC 是 否 已 有 工件 ，0 为 无 ， :大 2
fori=size(Rec1):-1:1% 记 录 本 次 操作 的 时 刻 4 W\
if Rec(i,1)==MinNumber && isnan(Rec(;3))% 同 时 发 生 上 料 和 下 料
flag=1; O
einomiyo
Rec=[RecMinNumberTifynejNaN];% 记 录 上 料 开 始 时 间
break; 0 》
end 放
end A nd
ifflag==0% 仅 发 生 上 料 让
Rec=[Rec;Mi ber,Time,NaN];
wing VV
if Si bg inNumber)==0% 不 用 清洗 的 情况
nmwner
六 TimesTime+Expect(3,MinNumber);% 完 成 换 料
| N ri=1:8%CNC 的 时 间 推 进
N if Left(i)-Expect(4,MinNumber)<0
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber);
end
end
Left(MinNumber)=Work;% 换 料 的 CNC 更 新 剩余 时 间
if unifrnd(0,100)>=99% 生 成 故障 信息
StartTime=Time+unifrnd(0,Work);% 随 机 生成 故障 开始 时 间 《发生 在 加 工时 )
33

<!-- source_page: 34 -->

回 成 革 动 国
宝 这
村
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
Error=[Error;size(Rec,1), MinNumber,StartTime,StartTime+ProcessTime,0];% 记 录
故障 信息
end
else% 需 要 清洗 的 情况
Time=Time+Expect(3,MinNumber)+Wash;% 完 成 换 料 与 清洗
for i=1:8%CNC 的 时 间 推 进
if Left(i)-Expect(4,MinNumber)-Wash<0
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber)-Wash;
end A7
end 一 NY
Left(MinNumber)j=Work-Wash;% 换 料 的 CNC 更 新 剩余 时 间 一 \)
if unifrnd(0,100)>=99% 生 成 故障 信息 _
StartTime=Time-Wash+unifrnd(0,Work);% 随 机 生成 故 站
ProcessTime-uniffndl600.1200) 汉 随机 生成 人 工 修复 需 时 间
Error=[Error;size(Rec,1),MinNumber,StartTime, artTi n eip ocessTime,01;% 记 录
故障 信息 全
end X
end
Position=ceil(MinNumber/2);%RGV 位 置 更 新
end @
whil (Reclend 3)sExpect(s MinNur#y) ash<=28800)
Rec(end,:)=[]; AAA
end
%% 计算 =
SUMs=size(Rec,1)-size(Error,1), RF
we 于 和 ascnc 平均 非 有 效 工 作 时 长
Last=Rec(end,3)+Ex inNumber)+Wash;% 最 终 完 成 物料 清洗 时 刻
oa V
toc 7
coated MinNumber Move Position Situation Switch Time Wash Work ProcessTime
S lime;
F
L\
用 于 双 工 序 情况 三 方法 一 第 一 组 的 代码
Situation3_2Team1.m
% 情 况 3〈 基 于 情况 2) 下 的 代码
clear;clc;
%% 计时
tic
%% 输入 不 同 组 别 参数
Move=[0,20,33,46];% 第 一 组 [0,20,33,46] 第 二 组 [0,23,4159] 第 三 组 [0,18,32,46]
34

<!-- source_page: 35 -->

回 玫 SA
Work=[400,378];% 第 一 组 [400,378] 第 二 组 [280,500] 第 三 组 [455,182]
Switch=repmat([28,31],1,4);% 第 一 组 [28,31] 第 二 组 [30,35] 第 三 组 [27,32]
Wash=25;% 第 一 组 25 第 二 组 30 第 三 组 25
%% 预 设 系 统 情况
Tool=[12,1212,12];% 预 设 刀 具 分 布 情况 ， 是 情况 2 下 的 最 优 方案
Position=1;% 记 录 RGV 的 位 置 ， 取 值 为 1*4
Left=zeros(18);% 记 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation=zeros(18);% 记 录 8 台 CNC 当前 是 否 拥有 工件 ，0 为 无 ，1 为 有
Time=0;% 系 统 已 运行 时 间
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和
Now=1;% 当 前 RGV 目标 工序 ， 取 值 仅 为 1 或 2 A7
Error=[];% 记 录 故 障 信息 一 NY
Rec=[];% 记 录 每 个 工件 的 上 下 料 信 息 一 \)
%% 遍历 所 有 刀具 分 布 情况 2XG
while Time<=28800 ood
fori=1:size(Erron1)% 检 查 错 误 信 息
if Time>=Error(i,3) && Time<=Error(i,4) && Error(i,5)==0% REE KAE
Errorlj5)=1;% 标 记 为 已 处 理 \/
Co
时 间 4 W\
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
end @
end / O 〇
fori=1:8% 计 算 预 期 时 间
计 Now~=Tool(i)% 排 除非 目 - 序 良 CNC
Penbnn 下 二
continue; A nd
oo
Expect(1,i +abs(Position-ceil(i/2)));
ifle 1
Oo
人 中
| N d
N Expect(3,i)=Switch(i);
Expect(4,i)=sum(Expect(1:3,i));
end
[MinNumberj=min(Expect(4,:));% 找 出 下 一 个 目标
Time=Time+Expect(1MinNumber);% 移 动 至 下 一 个 目标 位 置
flag=0;
fori=1:size(Erron1)% 运 动 后 再 次 检查 错误 信息
if Time>=Error(i,3) && Time<=Error(i,4) && Error(i,5)==0 && MinNumber==Error(i,2)%
运动 中 原 目标 发 生 了 故障
35

<!-- source_page: 36 -->

回 成 革 动 国
RE 0
加 只 RN
Error(j5)=1;% 标 记 为 已 处 理
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
for j=1:8%CNC 的 时 间 推 进
if Left(j)-Expect(1,MinNumber)<0
Left(j)=0;
else
Left(j)=Left(j)-Expect(1,MinNumber);
end
end
Left(Error(j2))=Error(li4)-Time;% 将 故障 修复 所 需 时 间 转 换 为 当前 工作 剩余 完成
时 间
flag=1; 人
» -从 >
end 一 \)
iflag% 由 于 原 目 标 CNC 发 生 故 障 ， 重 启 循环 2XG
continue; ood
end
flag=0; As
fori=1:size(Errop1)% 等 待 中 检查 错误 信息 ~ ,
if Time<=Error(i,3) && Time+Expect(2,Min Wu iber)>=Error(i,3) && Error(i,5)==0 &&
MinNumber==Errorli2)% 等 待 中 原 目 标 发 生 了 故障 4 SS
Error(j5)=1;% 标 记 为 已 处 理
Situation(Errorlij2))=0;% 修 复 完成 后 取 走 故 障 工件
for j=1:8%CNC 的 时 间 推 刘 O
if enter 下 ae
Left(j)=0;
else =
Left( or
ead_
end
到 hi 四 上 -are anertayoo6 大 了 往复 所 宕 时 间 转 区 为 当前 工作 利信
完成 时 为
Roomwaaan
六 ag=1;
a
放 flag% 由 于 原 目 标 CNC 发 生 故 障 ， 重 启 循环
continue;
end
Time=Time+Expect(2,MinNumber);% 正 常 等 待
放 Now==1% 当 前 目标 是 工序 1 的 CNC
flag=0;
for k=size(Rec1):-1:1% 记 录 本 次 操作 时 刻
if Rec(k,1)==MinNumber && isnan(Reclk,3))% 同 时 发 生 上 料 和 下 料
36

<!-- source_page: 37 -->

—
下
二 二
回 共 RE
flag=1;
Rec(k,3)=Time;
Rec(end+1,1)=MinNumber;
Rec(end,2)=Time;
Rec(end,3:6)=NaN;% 构 建 此 工件 工序 2 c SA
break;
end
end
放 flag==0% 仅 发 生 上 料
Rec(end+1,1)=MinNumber;
Rec(end,2)=Time;
Rec(end,3:6)=NaN; A7
end 一 NY
ffsituation(MinNumbenj-=1% 换 料 时 取 下 了 一 个 已 经 完成 工 庄 3 的 工 和 )
Now=2;% 下 一 道 目 标 工序 发 生变 化 3
NEXT=k;% 记 录 此 工件 的 序号 ood
end
Situation(MinNumber)=1; As
Time=Time+Expect(3,MinNumber);% 完 成 换 料 全
Te X
if Left(k)-Expect(4,MinNumber)<0
Left(k)=0;
else [o)
Fe EGR inNumber);
w
end
和
SN
if unifrnd(0,100)>=99% 守 成 故障 信息
Seraaesyne 航 和 naoworayyw 随 生成 了 开始 昌 (发 生 在 加 工时 )
ProcEsTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
o Rowinwumbersanmmesanmmnetprocssmmeola 记 录
和
六 8 认 目 标 是 工序 2 的 CNC
AS
SA， for k=size(Rec1):-1:1% 记 录 本 次 操作 时 刻
if Rec(k,4)==MinNumber && isnan(Rec(k,6))% 取 下 已 完成 工件
flag=1;
Rec(k,6)=Time;
Rec(NEXT,4)=MinNumber;
Rec(NEXT,5)=Time;
break;
end
end
37

<!-- source_page: 38 -->

回 成 革 动 国
二
村
放 flag==0% 放 置 待 加 工 工序 2 的 工件
Rec(NEXT,4)=MinNumber;
Rec(NEXT,5)=Time;
end
Now=1;% 此 时 目标 工序 重新 变 为 工序 1
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber)+Wash;% 完 成 换 料
for k=1:8
if Left(k)-Expect(4,MinNumber)-Wash<0
Left(k)=0;
else
Left(k)=Left(k)-Expect(4,MinNumber)-Wash; A7
end 一 NY
P
end += 由
Left(MinNumber)=Work(2)-Wash;
if unifrnd(0,100)>=99% 生 成 故障 信息 , s d
StartTime=Time-Wash-+unifrnd(0,Work(2)); %E4 ZER 障 开 始 时 间 ( 发 生 在 加 工
时 ) JS NS
ProcessTime=unifrnd(6500,1200);% 随 机 生成 涩 玉 修 复 所 需 时 间
oronn 拓 rroronans
息
end
end @
Position=ceil(MinNumber/2)3 J85 [/&. O 〇
end
while ~(Rec(end,6)+Expect(3,MinNu 人 on
Rec(end,:)=[]; 放
end A nd
%% 计算 一 让
SUM=size(Rec1)-si ;% 成 料 数
WAIT=(Rec(en /中 ranwooyaxouc 平均 非 有 效 工 作 时 长
CC
%% 计时
taesN A
让 npleteTime Expect flag i j k Left MaxProduct MinNumber Move NEXT Now Order Position
Situation Switch TempRec Time Tool Type Wash Work ProcessTime StartTime;
memory
用 于 情况 一 方法 二 第 一 组 的 代码
Simplify_Situation1Team1.m
% 情 况 1 下 的 简化 模型 代码
clear;clc;
%% 计时
tic
38

<!-- source_page: 39 -->

EEEE
%% 输入 不 同 组 别 参数
Move=[0,20,33,46];% 第 一 组 [0,20,33,46] 第 二 组 [0,23,41,59] 第 三 组 [0,18,32,46]
Work=560;% 第 一 组 560 第 二 组 580 第 三 组 545
Switch=repmat([28,31],1,4);% 第 一 组 [28,31] 第 二 组 [30,35] 第 三 组 [27,32]
Wash=25;% 第 一 组 25 第 二 组 30 第 三 组 25
%% 预 设 系统 情况
Position=1;% 记 录 RGV 的 位 置 ， 取 值 为 1~4
Left=zeros(18);% 记 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation=zeros(1.8);% 记 录 8 台 CNC 当前 是 否 拥 有 工件 ，0 为 无 ，1 为 有
Time=0;% 系 统 已 运行 时 间
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和 A7
Rec=[)%6 记 录 每 个 工作 的 上 下 料 信息 =
%9 系统 开始 运行 _ 内
while Time<=28800 2XG
fori=1:8% 计 算 预计 时 间 / ood
Expect(1,i)=Move(1+abs(Position-ceil(i/2))); SS
Expect(2,i)=Left(i); As NS
Expect(3,i)=Switch(i); SN
Expect(4,i)=sum(Expect(1:3,i)); X
end
[MinNumber]=min(Expect(4,:));% 找 出 下 一 个 目标
Time=Time+Expect(1,MinNumber)+Expect(2, MinNumber);%RGV 移动 至 下 一 个 目标 位 置 并
等 待 £& 7 ©
flag=0;% 目 标 CNC 是 否 已 有 工 Ye 1 为 有
fori=size(Rec1):-1:1% 记 录 本 次 操作 的 里 刻
NE
flag=1; \ -
Rao 二 下 料 开始 时 间
Rec= 人 限 eciMinNumberTime,NaN];% 记 录 上 料 开始 时 间
ed V
//
2
SS 仅 发 生 上 料
To
if Situation(MinNumber)==0% 不 用 清洗 的 情况
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber);% 完 成 换 料
fori=1:8%CNC 的 时 间 推 进
if Left(i)-Expect(4,MinNumber)<0
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber);
39

<!-- source_page: 40 -->

3
加 只 RN
end
end
Left(MinNumber)j=Work;% 换 料 的 CNC 更 新 剩余 时 间
else% 需 要 清洗 的 情况
Time=Time+Expect(3,MinNumberj+Wash;% 完 成 换 料 与 清洗
fori=1:8%CNC 的 时 间 推 进
if Left(i)-Expect(4,MinNumber)-Wash<0
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber)-Wash;
end
end A7
Left(MinNumber)j=Work-Wash;% 换 料 的 CNC 更 新 剩余 时 间 一 NY
end 由
Position=ceil(MinNumber/2); %RGV 位 置 更 新 2XG
end ood
while ~(Rec(end,3)+Expect(3,MinNumber)+Wash<=28800)
Rec(end,:)=[]; As
end &
n X
SUM=size(Rec1);% 成 料 数
WAIT=(Rec(end,3)*8-size(Rec,1)*Work)/8;%CNC 平均 非 有 效 工 作 时 长
Last=Rec(end,3)+Expect(3,MinNumber)+Wash;% 最 终 完成 物料 清洗 时 刻
%% 计时 [e]
人
clear Expect flag i Left MinNumber Move Position Situation Switch Time Wash Work;
memory 和 NS-
用 于 情况 二 方法 -征服
Simplify_Situation2Tea
% 情 况 2 Te
cleariclc; //
2 和
tasN A
hib Sr \ 环 同 组 别 参数
证 oos aaa 第 二 组 [0,23,41,59] 第 三 组 [0,18,32,46]
Work=[400,378];% 第 一 组 [400,378] 第 二 组 [280,500] 第 三 组 [455,182]
Switch=repmat([28,31],1,4);% 第 一 组 [28,31] 第 二 组 [30,35] 第 三 组 [27,32]
Wash=25;% 第 一 组 25 第 二 组 30 第 三 组 25
%% 记录 所 有 刀具 分 布 情况 下 的 工作 情况
Rec=cell(11);% 用 以 记录 每 一 种 刀具 分 布 情况 下 的 完整 加 工 情况
Statistics=[];% 统 计 成 功 加 工 数 和 失败 加 工 数
Order=[];% 记 录 每 一 种 刀具 分 布 方案
%% 遍历 所 有 刀具 分 布 情况
40

<!-- source_page: 41 -->

Snud
[EEREEs
fori=1:7% 刀 有 具 2 的 数量
Type=nchoosek(1:8,i);% 生 成 所 有 的 组 合 情 况
forj=1:size(Type,1)% 确 定 一 种 刀具 分 布 情况
Tool=ones(1,8);
for k=1:size(Type(j,:),2)
Tool(Type(j k))=2;
end
Order=[Order;Tool];
Position=1;% 记 录 RGV 的 位 置 ， 取 值 为 1*4
Left=zeros(1,8);% 记 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation=zeros(18);% 记 录 8 台 CNC 当前 是 否 拥有 工件 ，0 为 无 ，1 为 有
Time=0;% 系 统 已 运行 时 间 全
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 GM 加， 第
三 行为 预计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和 一 \)
mghec- 记录
Now=1;% 当 前 RGV 目标 工序 ， 取 值 仅 为 1 或 2 ond
while Time<=28800
for k=1:8% 计 算 预 期 时 间 As
if Now~=Tool(k)% 排 除非 目标 工序 的 GNC
Expect(:,k)=inf; K
continue;
end
Expect(1,k)=Move(1+abs(Pgsition-ceil(k/2)));
Expect(2,k)=Left()il, »  ©
SA
Expect(4,k)=sum( 4 全 本
end
[~,MinNumbe| nABpecta Rit FHE
Time=TimetExpekct(1,MinNumberj+Expect(2,MinNumber);% 移 动 至 下 一 个 目标 位
置 并 等 待
与 】 Wowaerramenc
% flag=0;
N Dorcsatemecsawicssnors
这 if TempRec(k,1)==MinNumber && isnan(TempRec(k,3))% 同 时 发 生 上 料
NT
R < flag=1;
TempRec(k,3)=Time;
TempRec(end+1,1)=MinNumber;
TempRec(end,2)=Time;
TempRec(end,3:6)=NaN;% 构 建 此 工件 工序 2 ff)id HHEpE
break;
end
end
ifflag==0% 仅 发 生 上 料
41

<!-- source_page: 42 -->

回 8 昌国
后
站 全 入
TempRec(end+1,1)=MinNumber;
TempRec(end,2)=Time;
TempRec(end,3:6)=NaN;
end
if Situation(MinNumber)j==1% 换 料 时 取 下 了 一 个 已 经 完成 工序 1 的 工件
Now=2;% 下 一 道 目 标 工序 发 生变 化
NEXT=k;% 记 录 此 工件 的 序号
end
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber);% 完 成 换 料
for k=1:8
if Left(k)-Expect(4,MinNumber)<0 A7
Left(k)=0; “ NY
o
else 2XG \)
Left(k)=Left(k)-Expect(4,MinNumber);
end ood
end
Left(MinNumber)=Work(1); As
else% 当 前 目标 是 工序 2 的 CNC Q
frag-0; A BA
for k=size(TempRec1):-1:1% 记 录 14 操作 上 刻
if TempRec(k,4)==MinNumber && isnan(TempRec(k,6))% 取 下 已 完成 工
件 @
flag=1; /L » ©
AR
TempRe€( -winwumber
人
—
brea »
一 -54
~ 让 Romegearrramrf
7 TempRec(NEXT,4)=MinNumber;
下 4 TempRec(NEXT,5)=Time;
p) end
13/ 4 Now=1% 此 时 目标 工序 重新 变 为 工序 1
SA， Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber)j+Wash;% 完 成 换 料
for k=1:8
if Left(k)-Expect(4, MinNumber)-Wash<0
Left(k)=0;
else
Left(k)=Left(k)-Expect(4,MinNumber)-Wash;
end
end
42

<!-- source_page: 43 -->

回 成 革 动 国
和
加 只 RN
Left(MinNumber)=Work(2)-Wash;
end
Position=ceil(MinNumber/2);% 更 新 位 置
end
Rec=[RecTempRec];% 记 录 本 次 刀具 分 布 情况 下 的 完整 加 工 情况
Statistics=[Statistics;0,0];% 统 计 本 次 刀具 分 布 情况 下 的 成 功 加 工 数 和 失败 加 工 数
for k=1:size(TempRec,1)
if isnan(sum(TempRec(k,:)))
Statistics(end,2)=Statistics(end,2)+1;
else
Statistics(end,1)=Statistics(end,1)+1;
end A7
end 一 NY
end o/z 由
end
%% 对 所 有 情况 数据 的 分 析 ood
Rec(1)=[];
MaxProduct=max(Statistics(:,1));% 最 大 产量 As
CompleteTime=inf;% 产 量 最 大 情况 下 的 最 短 完 成 时 间 \/
BestpPlan=cell(11);% 产 量 最 大 且 完成 时 ao
Bestknife=[];% 产 量 最 大 且 完 成 时 间 最 短 的 刀具 分 布 诱 案 S
fori=1:size(Rec2)% 找 出 产量 最 大 情况 下 的 最 短 完 成 时 后
if Statistics(i,1)==MaxProduct @
for j=size(Rec{1,i},1):-1:1 人 O
regeooalg
if Rec{1,i}(j,6)<=CompleteTime
At
end \
uaaey 上
end
asy |V
end /
end 下 4
r Sr )% 找 出 产量 最 大 且 完 成 时 间 最 短 的 所 有 方案 并 记录
| if Statistics(i,1)==MaxProduct
N * for j=size(Rec(1,i},1):-1:1
if ~isnan(Rec{1,i}(j,6))
if Rec{1,i}(j,6)==CompleteTime
BestPlan=[BestPlan,Rec{1,i}];
BestKnife=[BestKnife;Order(i,:)];
end
break;
end
end
43

<!-- source_page: 44 -->

EEEE

end
end
BestPlan(1)=[];
REC=BestPlan{lend};% 挑 选 一 个 最 佳 方案
while ~(REC(end,6)+Expect(3,MinNumber)+Wash<=28800)

REC(end,:)=[];
end
%% 计算
SUM=size(REC,1);% 成 料 数
WAIT=(REC(end,6)*8-size(REC,1)*sum(Work))/8;%CNC 平均 非 有 效 工 作 时 长
Last=REC(end,6)+Expect(3,MinNumber)+Wash;% 最 终 完成 物料 清洗 时 刻
%% 计时 二
2 -从 >
clear CompleteTime Expect flag jj k Left MaxProduct MinNumber Move NE Now Order Position
Situation Switch TempRec Time Tool Type Wash Work; 人
memory 4 ood

SS

用 于 单 工序 情况 三 方法 二 第 一 组 的 代码 AS) NS
Simplify_Situation3_1Team1.m SN
% 情 况 3〈 基 于 情况 1) 下 的 简化 模型 代码 X
clear;clc; K
%% 计时
tic @
%% 输入 不 同 组 别 参数 A / o
Verpaoontay 20 网-oaamaaa 第 三 组 [0,18,32,46]
Work=560;% 第 一 组 560 第 二 组 5804 和 二 级 545
ETA 第 二 组 [30,35] 第 三 组 [27,32]
Wash=25;% 第 一 组 25 第 二 4 天 25
%%6 预 设 系统 情况 ~
Position=1;% 记 录 是 八 ， 取 值 为 1~4
Left=zeros(1,8);%1c.3% 8 人 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation :为 );% 记 录 8 台 CNC 当前 是 否 拥有 工件 ，0 为 无 ，1 为 有
go
Expsetones(d );% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
人 ASWw 第 四 行为 前 三 项 之 和
ReE 丰 % 记 录 每 个 工件 的 上 下 料 信息
Error=[];% 记 录 故 障 信息
%% 系统 开始 运行
while Time<=28800

fori=1:size(Errop1)% 检 查 错误 信息

if Time>=Error(i,3) && Time<=Error(i,4) && Errorl;5)==0% 故 障 已 发 生
Errorlj5)=1;% 标 记 为 已 处 理
Left(Error(j2))=Errorlj4)-Time;% 将 故障 修复 所 需 时 间 转 换 为 当前 工作 剩余 完成
时 间
44

<!-- source_page: 45 -->

人
加 只 RN
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
end
end
fori=1:8% 计 算 预 计时 间
Expect(1,i)=Move(1+abs(Position-ceil(i/2)));
Expect(2,i)=Left(i);
Expect(3,i)=Switch(i);
Expect(4,i)=sum(Expect(1:3,i));
end
[MinNumberj=min(Expect(4,:));% 找 出 下 一 个 目标
Time=Time+Expect(1,MinNumber);%RGV 移动 至 下 一 个 目标 位 置
flag=0; A7
fori=1:size(Erron1)% 运 动 后 再 次 检查 错误 信息 一 SS
if Time>=Error(i,3) && Time<=Error(i,4) && Error(i,5)==0 && Mi mbers=Error(i,2)%
运动 中 原 目标 发 生 了 故障 2
Errorlj5)=1;% 标 记 为 已 处 理 ood
Situation(Errorli2))=0;% 修 复 完成 后 取 走 故障 工作 人
forj=1:8%CNC 的 时 间 推 进 US \
if Left(j)-Expect(1,MinNumber)<0 ”全
Left(j)=0; X
else
Left(j)=Left(j)-Expect(1,MinNumber);
end @
end V4 O 〇
erotaraolqeeapamanapsoaraean
时 间 人
flag=1; 放
end A nd
oo 一
ifflag% 由 于 原 旧 标 发 生 故 障 ， 重 启 循环
ope | V*
end //
=X%
IN E1:sizefError1)% 等 待 中 检查 错误 信息
| /, 下 ime<=Error(i,3) && Time+Expect(2,MinNumber)>=Error(i,3) && Error(i,5)==0 &&
VAN erErol 2% 1  ERIE T H
Error(j5)=1;% 标 记 为 已 处 理
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
for j=1:8%CNC 的 时 间 推 进
if Left(j)-(Error(i,3)-Time)<0
Left(j)=0;
else
Left(j)=Left(j)-(Error(i,3)-Time);
end
45

<!-- source_page: 46 -->

回 玫 SA
end
Left(Error(j2))=Errorli4)-Error(;3);% 将 故障 修复 所 需 时 间 转 换 为 当前 工作 剩余

完成 时 间
Time=Error(;3);% 时 间 调 整 至 故障 发 生 时
flag=1;
end
end
iflag% 由 于 原 目 标 CNC 发 生 故 障 ， 重 启 循环
continue;
end
Time=Time+Expect(2,MinNumber);% 正 常 等 待
flag=0;% 目 标 CNC 是 否 已 有 工件 ，0 为 无 ，1 为 有 A7
fori=size(Rec1):-1:1% 记 录 本 次 操作 的 时 刻 一 NY
if Rec(i,1)==MinNumber && ”0 \)
flag=1; 所
Recli3)=Time;% 记 录 下 料 开 始 时 间 ood
Rec=[RecMinNumberTime,NaN];% 记 录 上 料 开 始 B 而
break; US \ \
end 人
. 这
ifflag==0% 仅 发 生 上 料
Rec=[Rec;MinNumber,Time,NaN];
end @
if on
Situation(MinNumbenj=1  ¢ A
Time=Time+Expect(3,MinN dmber 5 完成 换 料
for i=1:8%CNC 上
if Left(i)-Expec ¥ nNumber)<0
Left(i)=0;
else
“% 中 Reeeaamnaamben
2
人 只 人 CNC 更 新 剩余 时 间
| /, nifrnd(0,100)>=99% 生 成 故障 信息
SA， StartTime=Time+unifrnd(0,Work);% 随 机 生成 故障 开始 时 间 〈 发 生 在 加 工时 )
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
Error=[Error;size(Rec,1), MinNumber,StartTime,StartTime+ProcessTime,0];% 记 录
故障 信息
end
else% 需 要 清洗 的 情况
Time=Time+Expect(3,MinNumber)+Wash;% 完 成 换 料 与 清洗
for i=1:8%CNC 的 时 间 推 进
if Left(i)-Expect(4,MinNumber)-Wash<0
46

<!-- source_page: 47 -->

回 成 革 动 国
二
村
Left(i)=0;
else
Left(i)=Left(i)-Expect(4,MinNumber)-Wash;
end
end
Left(MinNumber)j=Work-Wash;% 换 料 的 CNC 更 新 剩余 时 间
if unifrnd(0,100)>=99% 生 成 故障 信息
StartTime=Time-Wash+unifrnd(0,Work);% 随 机 生成 故障 开始 时 间 ( 发 生 在 加 工时 )
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
Error=[Error;size(Rec,1), MinNumber,StartTime,StartTime+ProcessTime,0];% 记 录
故障 信息
end A7
end 一 NY
Position=ceil(MinNumber/2);%RGV 位 置 更 新 2 \)
end
while ~(Rec(end,3)+Expect(3,MinNumber)+Wash<=28800) p ood
Rec(end,:)=[]; SS
end As NS
%% 计算 人
SUM=size(Rec1)-size(Erron1);% 成 料 数 A X
WAIT=(Rec(end,3)*8-size(Rec,1)*Work)/8;%CNC 平均 FERCTf 时 长
Last=Rec(end,3)+Expect(3,MinNumber)+Wash;% 最 终 完 成 物料 清洗 时 刻
%9% 计时 O
toc AZ O 〇
clear Expect flag i Left MinNumber Jr Situation Switch Time Wash Work ProcessTime
StartTime; JY )
memory 放
oa
Simplify_Situation3 电 Teamdl.m
% 情 况 3 (FkT aa
clear;clc; 7,
2 和
tie, NA
和 司 组 别 参数
Move=[0,20,33,46];%5—41[0,20,33,46] 第 二 组 [0,23,41,59] 第 三 组 [0,18,32,46]
Work=[400,378];% 第 一 组 [400,378] 第 二 组 [280,500] 第 三 组 [455,182]
Switch=repmat([28,31],1,4);% 第 一 组 [28,31] 第 二 组 [30,35] 第 三 组 [27,32]
Wash=25;% 第 一 组 25 第 二 组 30 第 三 组 25
%% 预 设 系 统 情况
Tool=[12,12,12,12];% 预 设 刀 有 具 分 布 情况 ， 是 情况 2 下 的 最 优 方 案
Position=1;% 记 录 RGV 的 位 置 ， 取 值 为 1*4
Left=zeros(18);% 记 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
Situation=zeros(18);% 记 录 8 台 CNC 当前 是 否 拥有 工件 ，0 为 无 ，1 为 有
47

<!-- source_page: 48 -->

下
总
加 只 RN
Time=0;% 系 统 已 运行 时 间
Expect=ones(4,8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
计 上 下 料 时 间 ， 第 四 行为 前 三 项 之 和
Now=1;% 当 前 RGV 目标 工序 ， 取 值 仅 为 1 或 2
Error=[];% 记 录 故 障 信息
Rec=[];% 记 录 每 个 工件 的 上 下 料 信息
%% 遍历 所 有 刀具 分 布 情况
while Time<=28800
fori=1:size(Erron1)% 检 查 错 误 信 息
if Time>=Error(i,3) && Time<=Error(i,4) && Error(;5)==0% 故 障 已 发 生
Error(j5)=1;% 标 记 为 已 处 理
efEron, 2)-rro  Time  AFHER8  T T)524 1 A%
时 间 一 SS
Situation(Error(i2)=0% 修 复 完成 后 取 走 故障 工作  _ \
end 2XG
end ood
fori=1:8% 计 算 预期 时 间
if Now~=Tool()% 排 除非 目标 工序 的 CNC As
Expect(:,i)=inf; 会
continue; X
end
Expect(1,i)=Move(1+abs(Position-ceil(i/2)));
Expect(2,i)=Left(i); ®
Expect(3,i)=Switch(i); O
corernn 有 从
end
0
Time=Time+Expect(1,Mi 至 hber);% 移 动 至 下 一 个 目标 位 置
flag=0; _—
for i=1:size(Err -区 运动 后 再 次 检查 错误 信息
if 五 m > 中 ,3) && Time<=Error(i,4) && Error(i,5)==0 && MinNumber==Error(i,2)%
运动 人 故障
让 (5)=1;% 标 记 为 已 处 理
他 Situation(Error(i2))=0;% 修 复 完成 后 取 走 故障 工件
| N for j=1:8%CNC 的 时 间 推 进
N if Left(j)-Expect(1,MinNumber)<0
Left(j)=0;
else
Left(j)=Left(j)-Expect(1,MinNumber);
end
end
Left(Error(j2))=Error(i4)-Time;% 将 故障 修复 所 需 时间 转 换 为 当前 工作 剩余 完成
时 间
flag=1;
48

<!-- source_page: 49 -->

回 成 革 动 国
RE 0
加 只 RN
end
end
ifflag% 由 于 原 目标 CNC 发 生 故 障 ， 重 启 循环
continue;
end
flag=0;
fori=1:size(Errop1)% 等 待 中 检查 错误 信息
if Time<=Error(i,3) && Time+Expect(2,MinNumber)>=Error(i,3) && Error(i,5)==0 &&
MinNumber==Error(j2)% 等 待 中 原 目标 发 生 了 故障
Error(j5)=1;% 标 记 为 已 处 理
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
for j=1:8%CNC 的 时 间 推 进 二
if Left(j)-(Error(i,3)-Time)<0 二 个，
Left(j)=0;
else 2XG
Left(j)=Left(j)-(Error(i,3)-Time); ood
end p
end
tErer 2-Eror a erorticts 2BEE 所 需 时 间 转 换 为 当前 工作 剩余
完成 时 间 x
Time=Errorl;3);% 时 间 调 整 至 故障 发 生
flag=1;
end @
end O 〇
放 flag% 由 于 原 目 标 CNC 发 生 故 障 丰 主 启 循环
continue; /Y )
end
Time=Time+Expect(2,Mi sx 党 人
if Now==1% 当 前 且 标 是 工序 1 的 CNC
flag=0;
for.k pe 人  ——
7 c(k,1)==MinNumber && isnan(Rec(k,3))% 同 时 发 生 上 料 和 下 料
下 Ce
六 Rec(k,3)=Time;
| N Rec(end+1,1)=MinNumber;
N Rec(end,2)=Time;
Rec(end,3:6)=NaN;% 构 建 此 工件 工序 2 fic saE kE
break;
end
end
ifflag==0% 仅 发 生 上 料
Rec(end+1,1)=MinNumber;
Rec(end,2)=Time;
Rec(end,3:6)=NaN;
49

<!-- source_page: 50 -->

Da 口 |
二
本
end
if Situation(MinNumbenj==1% 换 料 时 取 下 了 一 个 已 经 完成 工序 1 的 工件
Now=2;% 下 一 道 目 标 工序 发 生变 化
NEXT=k;% 记 录 此 工件 的 序号
end
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber);% 完 成 换 料
for k=1:8
if Left(k)-Expect(4,MinNumber)<0
Left(k)=0;
else
Left(k)=Left(k)-Expect(4,MinNumber); A7
end 一 NY
o
end 2XG \)
Left(MinNumber)=Work(1);
if unifrnd(0,100)>=99% 生 成 故障 信息 p e ped
StartTime=Time-+unifrnd(0,Work(L));%BHL2& Fi HesJELE fi 〈 发 生 在 加 工时 )
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 修 旨 2o. 间
Error=[Error;size(Rec,1),MinNumber,StartTime, StartTime+ProcessTime,0];% 记 录
故障 信息 =K
end K
else% 当 前 目标 是 工序 2 的 CNC
flag=0; @
for eelRec 1: LIKERAYH 作 时 侧
if eAns
flag=1; /V)
en
1 Nr
Rec(NEXT/4)=MinNumber;
ReclNEXTS) Time;
上
-下 广
eatnaatah
SN ec(NEXT,4)=MinNumber;
VY/, Rec(NEXT,5)=Time;
SA， end
Now=1;% 此 时 目标 工序 重新 变 为 工序 1
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumberj+Wash;% 完 成 换 料
for k=1:8
if Left(k)-Expect(4,MinNumber)-Wash<0
Left(k)=0;
else
Left(k)=Left(k)-Expect(4,MinNumber)-Wash;
50

<!-- source_page: 51 -->

回 成 革 动 国
二
村
end
end
Left(MinNumber)=Work(2)-Wash;
if unifrnd(0,100)>=99% 生 成 故障 信息
StartTime=Time-Wash+unifrnd(0,Work(2));% 随 机 生成 故障 开始 时 间 ( 发 生 在 加 工
时 )
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
Error=[Error'NEXTMinNumberStartTime,StartTime+ProcessTime,0];% 记 录 故 障 信
息
end
end
Position=ceil(MinNumber/2);% 更 新 位 置 A7
end 一 NY
while ~(Rec(end,6)+Expect(3,MinNumber)+Wash<=28800) o/z 由
Rec(end,:)=[];
end p ood
%% 计算 Q
SUM=size(Rec1)-size(Erron1);% 成 料 数 A5) \
WAIT=(Rec(end,6)*8-size(Rec,1)*sum(Work))/8;%CNC 平 HdF 有 作 时 长
Last=Rec(end,6)+Expect(3,MinNumber)+Wash;% 最 终 aa
2
toc
clear CompleteTime Expect flag ij k Left MaxProduct MinNumber Move NEXT Now Order Position
Situation Switch TempRec Time Tool by/ sh Work ProcessTime StartTime;
memory 人
用 于 绘图 的 代码 放
Plot.m A nd
% 用 于 绘制 统计 图 的 代码 7
clear;clc;
%% 情况 LTH 人 V
人
Way1=[38 ,392];
v 但 f2-{256,23 ,366];
Switche] 28+31,30+35,27+32]/2;
deal=28800./(Work+Switch)*8;
y=[Way1' Way2' Ideal'];
b=bar(y);
for k = Lisize(y,2)
b(k).CData = k;
end
legend( 方 法 一 "方法 二 "理想 情况 小
xlabel(' 组 别人
ylabel([ 成 料 数 族
51

<!-- source_page: 52 -->

EiiEaE
Ja ¥ . = i1
EIEEHER
title(' 情 况 1 下 各 方法 成 料 数 条 形 图 );
%% 情况 2 下 的 作 图
Work=[400+378,280+500,455+182];
Way1=[253,211,243];
Way2=[235,202,240];
Switch=[28+31,30+35,27+32];
Ideal=28800./(Work+Switch)*8;
y=[Way1' Way2',Ideal’];
b=bar(y);
for k = 1:size(y,2)
b(k).CData = k;
end A7
legend( 方 法 一 "方法 二 "理想 情况 =
xlabel(' 组 别 J) 一 \)
yiabel( 成 料 数 2G
title(' 情 况 2 下 各 方法 最 优 方 案 成 料 数 条 形 图 ); ood
模型 的 检验 的 代码 任
ModelTest.m &
% 模 型 检验 的 代码 AR
clear;clc;
%% 计时
tic @
%% 输入 不 同 组 别 参数 $O, ©
Move=[0,20,41,46];
Work=[455,500]; A
ions 人吉
Wash=25; A nd
%96 预 设 系统 情况 ~
Re  , mi 是 情况 2 下 的 最 优 方案
Position=1;% 记 录 RGV 揭 位 置 ， 取 值 为 1~4
Left=zer y 录 8 台 CNC 当前 工作 剩余 完成 时 间 ， 等 待 时 为 0
oonedas6 ac sn 人 0 为 无 ，1 为 有
Timesgkx 条 统 运行 时 间
ECEDiE(4.8);% 预 计时 间 ， 第 一 行为 预计 运动 时 间 ， 第 二 行为 预计 等 待 时 间 ， 第 三 行为 预
计 几 让 凋 时 间 ， 第 四 行为 前 三 项 之 和
Now=1;% 当 前 RGV 目标 工序 ， 取 值 仅 为 1 或 2
Error=[];% 记 录 故 障 信息
Rec=[];% 记 录 每 个 工件 的 上 下 料 信 息
%% 遍历 所 有 刀具 分 布 情况
while Time<=28800
fori=1:size(Errop1)% 检 查 错误 信息
if Time>=Error(i,3) && Time<=Error(i,4) && Errorl;5)==0% 故 障 已 发 生
Errorlj5)=1;% 标 记 为 已 处 理
52

<!-- source_page: 53 -->

回 成 革 动 国
RE 0
加 只 RN
Left(Error(j2))=Error(li4)-Time;% 将 故障 修复 所 需 时 间 转 换 为 当前 工作 剩余 完成
时 间
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
end
end
fori=1:8% 计 算 预期 时 间
if Now~=Tool()% 排 除非 目标 工序 的 CNC
Expect(:,i)=inf;
continue;
end
Expect(1,i)=Move(1+abs(Position-ceil(i/2)));
if Left(i)<=Expect(1,i) A7
Expect(2,i)=0; 二 NY
else 一 \)
Expect(2,i)=Left(i)-Expect(L,i); 2XG
end ood
Expect(3,i)=Switch(i);
Expect(4,i)=sum(Expect(1:3,i)); As
end 2\ 7
FoureonamaatrX
Time=Time+Expect(1MinNumber);% 移 动 至 下 一 介 慎 标 位 置
flag=0;
fori=1:size(Erron1)% 运 动 后 再 次 检查 错误 信息
if Time>=Error(i,3) && TO r(i,4) && Error(i,5)==0 && MinNumber==Error(i,2)%
运动 中 原 目标 发 生 了 故障 AAA
Errorlj5)=1;% 标 记 为 马 处 理
Situation(Erroit 区 =0;% 修 复 完 成 后 取 走 故障 工件
forj=1:8%CNC 的 时 间 牙 进
if Left(j- Expect(1,MinNumber)<0
有 六
else
7 Left(j)=Left(j)-Expect(1,MinNumber);
下 C-
含 nd
| // Left(Error(j2))=Error(i4)-Time;% 将 故障 修复 所 需 时间 转 换 为 当前 工作 剩余 完成
训
flag=1;
end
end
iflag% 由 于 原 目 标 CNC 发 生 故 障 ， 重 启 循环
continue;
end
flag=0;
fori=1:size(Errop1)% 等 待 中 检查 错误 信息
53

<!-- source_page: 54 -->

下
总
加 只 RN
if Time<=Error(i,3) && Time+Expect(2,MinNumber)>=Error(i,3) && Error(i,5)==0 &&
MinNumber==Error(j2)% 等 待 中 原 目标 发 生 了 故障
Error(j5)=1;% 标 记 为 已 处 理
Situation(Error(j2))=0;% 修 复 完 成 后 取 走 故障 工件
for j=1:8%CNC 的 时 间 推 进
if Left(j)-(Error(i,3)-Time)<0
Left(j)=0;
else
Left(j)=Left(j)-(Error(i,3)-Time);
end
end
fror 2)-Error(  ror AHIRAER T B EE5 ST MA
完成 时 间 一 SS
Time=Error(;3);% 时 间 调 整 至 故障 发 生 时 一 \)
flag=1; 2XG
end ood
end X
iflag% 由 于 原 目 标 CNC 发 生 故 障 ， 重 启 循环 As
continue; 会
s X
Time=Time+Expect(2,MinNumber);% 正 常 等 待
放 Now==1% 当 前 目标 是 工序 1 的 CNC
flag=0; @
for eielRec 1: LIKERAH 作 时 章
if Rec(k,1)==MinNumb oemastnm
flag=1; JY )
Rec(k,3)= ;
Rec(end+1;1)=MinNumber;
Sectnd21 Tme
区
二 pie
%
位 L
| N Rec(end+1,1)=MinNumber;
N Rec(end,2)=Time;
Rec(end,3:6)=NaN;
end
if Situation(MinNumbenr)j==1% 换 料 时 取 下 了 一 个 已 经 完成 工序 1 的 工件
Now=2;% 下 一 道 目 标 工序 发 生变 化
NEXT=k;% 记 录 此 工件 的 序号
end
Situation(MinNumber)=1;
Time=Time+Expect(3,MinNumber);% 完 成 换 料
54

<!-- source_page: 55 -->

Bgae
后
站 全 入
for k=1:8
if Left(k)-Expect(4,MinNumber)<0
Left(k)=0;
else
Left(k)=Left(k)-Expect(4,MinNumber);
end
end
Left(MinNumber)=Work(1);
if unifrnd(0,100)>=99% 生 成 故障 信息
StartTime=Time+unifrnd(0,Work(1));% 随 机 生成 故障 开始 时 间 〈 发 生 在 加 工时 )
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
Eror-{Erore(Re3 MInNumer arTime statTime frocessTIEX 记 录
故障 信息 一 SS
end 二 \)
else% 当 前 目标 是 工序 2 的 CNC 2XG
flag=0; ood
for k=size(Rec1):-1:1% 记 录 本 次 操作 时 刻 JS》
if Rec(k,4)==MinNumber && isnan(Rec(k,6))% 取 Re 二 [ 件
flag=1; SN
Rec(k,6)=Time; X
Rec(NEXT,4)=MinNumber;
Rec(NEXT,5)=Time;
break; @
end $O, O
2
ifflag==0% 放 置 待 加 工 工序 2 的 玉 件
Rec(NEXT,4)=MinNumber;
Rec(NEXT,5)=T We
end 一 ~ ]
Now=1;% 此 上 示 工序 重新 变 为 工序 1
Situati 2
epnannonomoaep
人 |
VY/, §- Left(k)=0;
SA， else
Left(k)=Left(k)-Expect(4,MinNumber)-Wash;
end
end
Left(MinNumber)=Work(2)-Wash;
if unifrnd(0,100)>=99% 生 成 故障 信息
StartTime=Time-Wash+unifrnd(0,Work(2));% 随 机 生成 故障 开始 时 间 ( 发 生 在 加 工
时 )
ProcessTime=unifrnd(600,1200);% 随 机 生成 人 工 修复 所 需 时 间
55

<!-- source_page: 56 -->

马 :二
和
;和 p = 3)
e
Error=[Error'NEXTMinNumberStartTime,StartTime+ProcessTime,0];% 记 录 故 障 信
息
end
end
Position=ceil(MinNumber/2);% 更 新 位 置
end
while ~(Rec(end,6)+Expect(3,MinNumber)+Wash<=28800)
Rec(end,:)=[];
end
%% 计算
SUM=size(Rec'1)-size(Error1);% 成 料 数
WAIT=(Rec(end,6)*8-size(Rec, 1)*sum(Work))/8; %CNC 平均 非 有 效 工 作 时 长 #7
Last=Rec(end,6)+Expect(3,MinNumber)+Wash;% 最 终 完 成 物料 清洗 时 刻 二 Si
%% 计时
0/0 2 \
toc 1 7
O 〇
和
~ 下
Mg
AZ
e-
56

