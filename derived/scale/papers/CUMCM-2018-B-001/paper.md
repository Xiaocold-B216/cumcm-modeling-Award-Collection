# Extracted Paper

<!-- source_page: 1 -->

mRig
ME

RGV 的 动态 调度 优化 问题
摘要
本 文 对 智能 加 工 系 统 中 RGYV 的 动态 调度 优化 问题 进行 研究 。
针对 任务 一 ， 我 们 首先 对 系统 进行 分 析 ， 给 出 了 几 个 重要 定义 和 优化 指导 原则 ， 例
如 RGYV 工作 循环 定义 、 系 统 效率 均衡原则 、CNC 满载 工作 上 限 等 。 同 时 ， 给
出 了 相关
分
析 和 证 明 ， 包 括 在 一 定 条 件 下 的 RGV 循环 的 最 短 用 时 证 明 ， 系 统 最 优 上 限 的 证 明 等 。
这 些 理论 为 我 们 建立 最 优化 模型 和 模型 评估 指标 提供 了 依据 。
对 于 情景 一 ， 我 们 对 原 有 模型 进行 转化 ， 将 其 转化 为 时 间 维度 上 的 多 队列 任务 调度
优化 模型 ， 并 基于 事件 对 时 间 进 行 离散 化 ， 为 减少 迭代 步 数 ， 根据 划分 缚 民 罗 各 最 优 关
态 转移 图 模型 ， 利用 状态 向 量 和 状态 转移 乍 阵 完成 系统 工作 的 模 所 PN
考虑 到
求解 该 优化 问题 计算 开销 较 大 ， na
全
型 中 的 优化 原则 结合 已 明确 的 优化 准则 构建 各 个 阶段 的 决策 方案,从 而 完成 问题 的 求
解 ， 得 到 在 8 ae
359、391; 经
检验 ， 在 求解 效率 和 求解 质量 上 都 达到 了 很 好 的 让 ®, N
对 于 情景 二 ， 我 们 分 析 了 两 类 CNC 在 系统 中 共存 了 产生 的 复杂 约束 情况 ， 结 合 系
统 效率 均衡 对 应 系统 整体 较 大 效率 的 规律 ，
CNC 的 数量 比例 。 再 通过
搜索
找到 了 最 优 的 CNC 空间
排 布 方案 ， 从 而 建立 带 工序 约束 的 最 优 状态 转换 图 模型 。
在 求解 时 ， 2
得 到 在 该 约束 条 件 下 ，8 个
小 时 内 三 组 参数 下 系统 可 产生 最 天 壮 和 司 [ 量 分 别 为
233、210、240;，
对 于 情景 三 ， 需 要 引入 了
因子 提 行 了 故障 的 随机 模拟 。 该 过 程 的 本 质 是 在 状态
转移 时 引入 不 确定 性 。 Te
对 状态 转移 矩阵 和 转移 约束 进行 拓展 补充 ，
并 再 价 和 区 进行 作 世人 仙 卫 了 区 了 风 隐 的 最 信 4 坊 转 区 因 杆 到 在 使 用 多 阶
段 决策 求解 时 ， 大
还 要 保持 系统 内 两 类 CNC 工作
能 力均 衡 以
取得 更 高 的 [2y 尝 有 于 情况较 多 ， 结 果 可 见 附件 Excel。
HS 人 ne
构建 了 结果 偏差 率 计 算 公 式 ， 并 为 该 标准提供
了 必要 的 理
持 ， 具 有 较 高 参考 意义 。 经 过 验证 ， 模 型 求解 算法 结果 与 最 优 解 有 很 好
的 过 沪 全 天 系统 效率 ， 我 们 构建 了 系统 效率 评价 指标 ， 用 于 刻画 系统 整体 效率 与 各 部
分 效率 均衡 情况 。
关键 字 : 状态
图 模型 ”多 阶段 决策 模型

” 非 线性

1

优化 模型 RGYV 最 优 调度

<!-- source_page: 2 -->

回味
计生

目录

一 、 问题 背景 与 重 述
3
二 、 模型 的 假设 .eee
三 、 符号 约定 .4
四 人
4 问题 一 分 析
42 间 题 一 分析
五 机 的 建人
6
5.1 模型 建立
5.2 最 从 居 太 村 和 国术 于
和
5.3 生字 人 和信，
5.4 srumRRiRrisEn
) 2
5.5

模型

的 求解

12

3
4
d
6
10

5.5.1 最 优 状 态 转移 图 模型 求解 算法 1
5.5.2 WLFHRIBIISHBIEBRRIIE ..oooo0
5.5.3 WATHEURIRITRA
HR BBURRE: .7
15
5.5.4 全 本人 1
六 、 的 评 从 与 这， 下
18
—~
附录 A 下
2
附录

B 5

123

Ldog

2

<!-- source_page: 3 -->

加 5
IE 辣

一 、 问 题背 景 与 重 述
随 着 信息 技术 、 控 制 工程 、 机 械 工程 等 技术 的 发 展 与 进步 ， 智 能 加 工 系统 日 益 无 人
化 、 自 动 化 、 智 能 化 ， 显 著 提 升 了 工业 加 工 、 物 流 服务 等 工作 的 效率 。 以 本 题 为 例 ， 该
智能 加 工 系统
自动

引导 车

由 8 台 计算 机 数控 机 床 (Computer
Number Controller，CNC)、!
(Rail

Guide Vehicle，RGV)、1

条 RGV

直线 轨道 、1

条 上 料 传

辆 轨道 式
送 带 、1 条 下

料 传送 带 及 其 他 附属 设备 组 成 。RGYV 是 一 种 无 人 驾驶 的 、 能 在 国定 轨道 上 自由 运行 的
智能 车 ， 能 够 根据 指令 完成 相关 的 作业 任务 。
在 该 类 系统 中 ，RGYV 的 运行 情况 对 整个 作业 系统 的 工作 效率 有 着 巨大 影响 ， 运 行
过 程 中 ， 易 出 现 因 不 同 工 作 组 调度 不 佳 ， 而 导致 空闲 等 待 的 情况 ， 降低 了 3 泡 行 效率 。 能
和 否 更 加 合理 地 调度 穿梭 车 ， 提
高 RGV 系统
的 运行 效率 ， 人
展 的 一 个 重要 因素 。
2
题目 要 求 针对 下 面 的 三 种 具体 情况 :
o
d
1. 一 道 工序 的 物料 加 工作

加 工 完成 ，

业 ， 每 台 CNC 安装 同样 的 刀具 $ 移 料 可 以 在 任 一 台 CNC 上

2.

两 道 工序 的 物料 加 工作 业 ， 每 个 和 和 的 第 一 稀 泛 工 刘 分 别 由 机 不同 的 CNC 人
次
加 工 完成 ;
3. CNC 在 加 工 过 程 中 可 能 发 生 故 障 《〈 据 统计 : 故障 的 发 生 概率 约 为 1%) 的 情况 ， 每
次 故障 排除 (人 工 处 理 ， 未
完成的 WkRD 时
间 介 于 1020
分 钟 之 间 ， 故 障 排除 后
即刻 加 入 作业 序列 。 room

完成 以 下 任务 :
任务 1: ea
RGV 动态 调度 模型 和 相应 的 求解 算法 ，
任务 2: 利用
表 全 申 系 统 作 业 参 数 的 3 组 数据 分 别 检 验 模 型 的 实用 性 和 算法 的 有 效
性 ， 给 出 ROY 人 交加 咯 和 系统 的 作业 效率 并 将 具体 的 结果 分 别 填 入 附件 2 的
Excel o

-

二 、模
型 的 假设

1. BANevaeae 可 在 未 收 到 需求 信号 时 主动 移动 到 指定 CNC 位 置 处 ; 此 外 , 自
动 引导 车 可 在 收 到 指令 后 维持 在 在 原 地 停止 等 待 状态 ，
2. 假设 RGYV 足够 智能 且 可 以 CNC 通讯 ， 可 以 获取 CNC 的 加 工 完成 剩余 时 间 以 及 当
前 班次 剩余 时 间 信息 ，
3. 假设 上 料 带 具有 理想 上 料 速 率 ， 即 : RGV
为 CNC (或 加 工 第 一 道 工 序 的 CNC) 上
生 料 时 ， 其 传送 带 保证 CNC 前 方 总 有 所 需 生 料 ;
4. 假设 下 料 带 具 有 理想 下 料 效率 ， 不 会 在 RGV 下 料 时 ， 出 现下 料 带 堵 塞 的 问题 ，;
3

<!-- source_page: 4 -->

加5
证 请
5. 假设 除了 CNC 在 加 工 过 程 中 可 能 发 生 故障 外 ， 其 他 部 件 都 不 发 生意 外 和 磨损 ， 且 可
在 指定 时 间 准时 完成 相应 操作 。
三 、 符号 约定

符号

意义

n

CNC

数量

-从>

总 时 间 (9) 了
M
TY
Vi
s
总
系统处 于 第 大 机
状态 转移 矩阵 集
系统 处 于 钴 j 个 状态 时 第; 个 状态 转移 矩阵
Q
Mics B oNC 的 类 型
P
CNC 的 故障 因子 矩阵
个
四
%
RYAES k ARA FTALHIT2) (5)
已
CNE 加 工 完成 一 个 一 道 工序 的 物料 所 需 时 间 (9)
让
NT RGYV 为 i 位置处 的 CNC 一 次 上 下 料 所 需 时 间 (9
ok W
RGV 在 第 大 个 状态 时 所 处 的 位 置
%Y, |2 ;处 的 CNC 在 系统 处 于 第 大 个 状态 时 距 下 一 次 空闲 状态 时 间 (5)
AQ
RGV 从 位 置 ; 移动 到 到 位 置 7 需要的 时 间 (s)
¢站
系统
在 第 大 个 状态 时 ，; 处 CNC 的 负载 情况
二

四 、 问 题 分析

4.1 问题一 分 析
该 问题 要 求 根据 一 般 问题 ，给 出 RGYV 动态 调度 模型 和 相应 的 求解 算法 。 针 对 该 问
题 ， 首 先 需要 对 该 系统 的 运行 特点 进行 一 定 的 抽象 、 概 括 和 证 明 ， 例 如 ， 在 最 优 的 调度
策略 下 各 部 分 机 器 效率 应 当 均衡 的 。 这 些 规则 将 用 于 构建 RGYV 动态 调度 模型 。
4

<!-- source_page: 5 -->

加 5
IE 辣

针对 情况 1， 结 合 对 系统 分 析 的 结果 ， 可 以 将 8 个 CNC 转换 为 8 个 工作 队列 ， 将 物
料 加 工作 业 抽 象 为 队列 中 的 事件 , 则 题目 第 一 问 可 以 转换 为 完成 队列 中 带 约束 条 件 的 任
务
最 优 调度 。 转 换 完成 后 ， 可 从 时 间 维 度 对 系统 基于 事件 进行 状态 划分 。 基 于 该 状态 划
分 结果 , 可 以 构建 最 优 状态 转移 图 (有
向 有 权 图 ) 模型 ， 其 中 带 权 节点 代表 CNC 的 处 理
时 间 、 带 权 有 向 边 带 代 表 RGYV 将 清洗工作 、 停 止 等 待 以 及 移动 所 需要 的 时 间 ， 由 此 构
建 状态 向 量 和 状态 转移 矩阵 。 该 模型 以 最 大 化 有 限时 间 内 完成 的 熟 料 数目 最 多 为 目标 ，
而 约束 则 可 引入 总 工时 约束 、 物 料 加 工 用 时 约束 、RGYV 运动 时 间 的 约束 等 。 此 外 ， 该 问
题 还 可 以 从 建立 物料 数目 确定 ， 最 小 化 时 间 的 角度 考虑 建立 相应 最 优化 模型 等 。 最 优 状
态 转移 图 模型 的 化 简 工 作 可 以 考虑 以 两 无 权 点 及 该 两 点 所 确定 的 一 条 带 权 有 向 边 代 蔡
原来
的 带 权 点 ， 从 而 完成 对 模型 的 构建 和 化 简 。
-从 >
针对 情况 2， 我 们 可 以 建立 带 有 工序 约束 的 最 优 状 态 转移 模型 ， 该 梭 轴 本 从 是 基于
系统
状态 转移 的 思想 ， 可 以 证 明 工 序 一 、 ng
多， 我
们 修改 状
态 转移 矩阵 的 约束 条 件 ， 限 制 状 态 向 量 的 转移 方向 从 而 完成 问题 的 求解 。 最 优化 目标 依
然 是 在 有 限时 间 内 最 大 化 生产 熟 料 数目 。
(并
针对 情况 3， Rs
约束 的 最 优 状 态 转移 模型
的 基础 上 引入 突 发 事件 随机 变量 ， 通过 引入 该 随机 妆 避 限 制 部 分 状态 的 转移 效果 ， 同 时
引入
等 待 时 间 变 量 ， 从 而 完成 问题 模型 的 建立 。“ | S
对 于 算法 的 求解 可 以 采用 引入 剪 枝 规则 、 回 渊 法 、 分 支 限界
法 等 。 值 得 注意的 是 ，
在 该 求解 该 模型 时 ， 分 支 限界 法 求 关 目 球 央 是 尽 快 技 册 请 中 约束 条 件 的 一 个 解 ， 或 在 满
Se
更 适合 求解 离散 最 优化 问题 。 但 是 ， 考
RAT
因此 在 求解 算法 时 采
用 分 阶段 优化 的 策 咯 完成 横 于 的 号 多， 同时 采用 基于 事件 的 时 间 离 散 化 处 理 ， 最后 可 以
对 结果 进行 分 析 比 较 ， 人 为 模 的 近似 解 。 除 此之 外 ， 在 该 类 最 优化 问题 求解 时 ， 也 可
MRRRERAR
RAE 2 等
4.2 ne

沸 j 并 可 以 洒 过 条 入 目 提供 的 数据 检验 模型 的 实用 性 和 算法 的 有 效 性 ， 并 对 结果
和 到 六 和 本 上 限 进行比较 , 判断 模型 和 算法 的 实用 性 和 有 效 性 ,同时 输出 该 过 程 中 RGV
的 调度 策略 。 对 于 系统 的 作业 效率 ， 可 以 定义 系统 工作 效率 为 系统 中 CNC 的 工作时 间
在 一 个 工时 内 比例 。 此 外 ， 可 从 系统 工作 效率 均衡 的 角度 分 析 模 型 实用 性 和 算法 的 有 效
性。

5

<!-- source_page: 6 -->

加5
ME

五 、 模型
的 建立 与 分 析
5.1 模型 建立
在 建立 模型 前 ， 我 们 首先 对 该 系统 的 基本 工作 状态 进行 一 定 的 分 析 。 结 合 分 析 结论
完成 模型 的 构建 和 改进 。 对 于 该 问题 我 们 有 以 下 分 析 :
定义 1RGY
工作 循环 ) RGF
对 每 个 CNC 都 操作 且 仅 操作 一 次 并 最 后 回 到 出 发 位 置 的
过 程 称 为 一 个 循环 〈 周期 )。
可 证 ， 对 于 本 题 中 三 组 数据 ，RGYV 的 循环 中 移动 距离 为 6 个 单位 长 度 且 中 途 停止
为 4 次 时 的 循环 是 所 有 循环 中 用 时 最 短 的 。
- 公 ，
证明 1 在 本 题 中 ，RG 太 一 次 循环 的 总 耗 时 为 也 4 由 上 下 和 时 间 刘 全 洛 Ni 刀 和 移动
时间 刀 组 成 。即
他 2
t=titltiy
合
通过
分 析 可 知 ， 当 CNC 的 种 类 和 数量 确定 时 ，sytj 在 同一 系统 中 是 常数 ， 故 的
相对
大 小 仅 由 怒 决 定 。 设 RGF 移动 ii 一 1 2.3) 这 Ri ii 需 时 间 ti = Aby+
(i— 1)AL,
其 中 Ab 为 移动 第 了 个 单位 的 时 间 ，Ata 为 后 续 每 多 当 单位 时 间 所 需 时 间 ， 且 根据 数据
Tho Aty
> Atz。
0
可 知 RG 太 在 4 个 位 置 至 少 停止 -7 中， 所 以 至 少 需要 的 时 间 为 4A6 ， 而 RGY在 一
2
假设 剩余 2 个 单位 需要 的 时 间 都 是 较 短 的
Ats, 人
所 以 结论 得 证 。
~
piapRH
A
让 人 人 系统 中 各 个 模块 的 工作 效率 在 匹配 (相等 或
近似 相等 ) 时 3 个 夭 损 获 得 最 大 效益 ， 该 状态 定义 为 系统 均 全
//

系统 si 你
在 只 CNC 装 有 一 种 类 型 刀片 的 情况 下 ，RGYV
与 CNC 协同 工
SR
的 效率 达到 最 大 化 ， 二 者 对 物料 的 处 理 能 力 应 当 尽量 匹配 。 因
为 当 RGV 处 理 能 力 大 于 CNC 的 时 候 ，RGYV 会 等 待 CNC 直到 空闲 的 CNC 出 现 的 ， 造
成 RGYV 的 产能 浪费 ,反之 亦 然 。 同 理 , 在 拥有 装 有 两 种 不 同类 型 刀片 的 CNC 的 系统 中 ，
两 种 CNC 对 物料 的 处 理 能 力也 应 该 尽量 均衡 ,因为 每 一 个 成 品 物料 需要 第 一 类 CNC 和
第 二 类 CNC 各 进行
一 次 加 工 ， 在 RGYV 服务 能 力 充足 的 情况 下 ， 如 果 第 一 类 CNC 的 处
理 能 力 大 于 第 二 类 CNC， 会 造成 产生 过 多 的 半成品 物料 而 没有 足够 的 第 二 类 CNC 进行
处 理 ， 造 成 阻塞 ， 而 第 二 类 CNC 的 处 理 能 力 大 于 第 一 类 CNC， 会 造成 没有 足够 的 半 成
品 物料 供给 第 二 类 CNC 加 工 ， 造 成 闲置 。 所 以 为 了 最 大 化 最 大 化 整个 系统 的 效率 ， 我
们 必须 尽量 保持 第 一 类 CNC 和 第 二 类 CNC 处 理 能 力 的 均衡 。
6

<!-- source_page: 7 -->

回味
外
定义
3 (CNC

满载

条 件 下 的 系统 工作 上 限 ) 假设所 有 的 CNC 全 部 满载

， 即所 有 的 CNC

都
处 理 进

行 “ 上 下 料 -处 理工 件 ” 操 作 的 循环 中 。 则 : 当
所 有 的 CNC

只 有 一 种 刀片 时 ，

在 一 个 班次 内 , 守 位
置 处 的 CMC

物料 加 工 数

量 的 上限 环 为
了

U; = L!

一 个 班次 的 总 加 工 上 限 为 U = 并 ?1 本， 其 中 如 为 CNC 加 工 完 成 一 个 一 道 工序 的 物料
所 需 时 间 ， 刀 为 RGY 为 CNC 一 次 上 下 料 所 需 时 间 。
当 CNC 有 装配 有 2 种 不 同类 型 的 刀片 的 时 ， 一
个 班次 内 CNC 能 够 加 工 的 物料 上 限

Se设 装 有 第 一 美 刀片 的 CNC 集合 为 @， 机 -次 ，则有 :
由 装配

两 种 类 型 刀片 的 CNC 中 加 工 的 物料

上 限 较 低 的 决定 ， 这 本

U=max(30,3°0;)
i€S

人

jeQ

质 由 系统

的 短 板 原理

ond
[一

SS

Maoaeaaonwnraaaearuanaaw 人 rn
为 了 便于 进一步
分 析 该 模型 ， 我 们 将 原来的 让 扣 抽 象 为 可 以 并 行 工作 的 任务 队列 ，
如 下所示 :
X
国上 下 梓
国 EEYTS

Q

ecfll AN ]
e
[AN
cc，

WE

om
oo

SA

下

人
2

3

六

国 chcw=

WET

|

-1

EGG

辐

同人 iii

一

移动 3 刻 时 间

图

1

国
稍 动 步时 间

带 约束 的 队列 调度 示意 图

W
DOVRRMIHE, WHTRAEIAIES RABE, 同时， 为 我
们 从 时 间 维度 对 系统 基于 事件 进行 状态 划分 提供 了 视角 。
从 图 1 可 知 ,在 任意 时 刻 ， 对 应 有 各 个 队列 (CNC) 的 状态 : 空 闸 、 工 作 ; 同时还 可
以 隐 性 的 反应 RGV 的 状态 ， 移 动 、 清 洗 等 。 从 时 间 维度 对 其 进行 离散 化 处 理 ， 由 此 可
以 构建 不 同时 刻下 系统 的 状态 转移 图 。 但 是 如 果 选 择 以 1s 为 基本 步 长 ， 会 导致夺 代 状
态 过 多 ， 且 由 于 步 长 较 短 ， 整 体 有 较 多 从 代 是 不 必要 的 ， 而 过 大 的 步 长 ， 无 法 精确 刻画
系统
的 状态 转移 过 程 。 因 此 ， 进 一 步 在 时 间 划 分 上 改进 ， 采 用 基于 事件 的 时 间 划 分 ， 并
由 此 引出 整个 过 程 的 状态 转移 图 模型 。
7

<!-- source_page: 8 -->

加5

站
5.2 最 优 状 态 转移 图 模型
对 于 情况 一 ， 我 们 建立 最 优 状态 转移 图 模型 来 描述 整个 RGVCNC 系统
的 调度 过
程。

Rs

N
o

图

2 ”最 优 状态 转移 图 模型 示意 图

\)

o

首先 ， 我 们 建立 系统 的 状态 向 量 你 ， 该 状态 onsaams
的 状态 。 由 于 以 秒 为 处 理 单位 会 出 现 大 量 的 重 锯 状 态 基 重复 计算 ， 我 们 从 RGV 运动 的
视角 作为 图 模型 建立 的 基准 对 模型 进行 离散 化 处 理 & 访 模型 将 以 秒 为 单位 的 时 间 划分 ，
转换 为 基于 事件 的 时 间 划分 。
t

$,

°

本

DPK
Tk,1

vie|™ ¥ t5 < Tonpi € N¥opi < [n/2],12 2 0
2

My

US
PHO= 1 和 代表 系统 处 于 第 大 个 状态 时 的 时 刻 , mx 代表 RGV 在 第 大 个 状态 时

所 处 的 倍 置 ， 在 向 量 从 末尾的 补充 ! 以 构建 齐 次 转移 矩阵 ，rk; 变量 代表 当 系统 处 于 第
民 个 状态 时 ;位置处 的 CNC 距离 下 一 次 空闲 状态 〈 完 成 当前 工作 所 需要 ) 的 剩余时 间 。
当 RGV 的 一 次 上 料 行为 完成 时， 模 型 状态 发 生 转 移 ，RGV 移动 到 下 一 个 位 置 进行
上 料 〈 移 动 之 前 RGV 可 能 会 执行 在 原 地 “停止等 待 ”信号 )， 相 邻 两 次 上 料 完成 的 时 间
作为
状态 之 间 的 时 间 。 值 得 注意的 是 ， 该 模型 中 所 求 的 最 优 路 线 的 深度 〈 节 点 数) 即 为
系统 在 约束 条 件 下 所 能 生产 熟 料 的 最 大 值 ， 记 为 W。
模型 应 当 满足 下 面 的 约束 ;
约束 一 : RGYV 在 某 一 时 刻 只 能 为 一 台 机 器 上 料 或 下 料 。
8

<!-- source_page: 9 -->

加5
1
站 二二
约束 二 ， 从 第 ;次 上 料 到 第 ;+ 1 次 上 料 的 间隔 时 间 大 于 RGV 从 第 一 个 位 置 运动 到
第 二 个 位 置的 时 间 。
上 述 约 束 将 在 状态 转移 的 过 程 中 得 到 保持 。 为 了 便于 描述 ， 我 们 定义 了 下 列 变 量 。
1. 移动 矩阵
CU

CT1

C=|

o
Cn

Cnpom

其 中 cy 为 RGV 从 位 置 ; 移动 到 到 位 置 7 需要
的 时 间 ，cj = cji， 易 知 ， 当 ;一 了 时
co =0。

_

2，CNC 工作 负载 变量

_从
€k1

Bo=|

:

2

ER

了

W

0 状态 亿 的 CNC Ha
1 状态 似 的 CNC; 上 面 有
由 或 者 处 理 完成 的 工件
构建 状态 转移 方程 如 下 ;
Ta
= AN
它 表 未 从 第 + 阶 彼 到 A+ HRL 并 态 转移 规律 。 其 中 仅 为 第 大 个 状态 的 系统
A
状态 向 量 。
设 xx 为 系统
处 于 第 个 状 SR 可 哆 的 状态 转移 矩阵 集 。
Chi 一

可

其中4 全

2 1VY

T

¥-

Ap

人

和 和 人生

Vo
|
向N
|

kx2

co

Ap

1

.

°

和

其 定义 如 下 ;

一 Ai

vs
1

1
1

其 中 的 含义 为 RGV 选择 的 下 一 个 目标
移 到 第 大 二 1 个 状态 所 需要 的 时 间 ， 其 定义如 下

CNC，A 代表 从 第 大 个 状态 经 过 4 转

Ati = terp, + ts + ti + Cpyi
ts = max{cy,
i Tk,i}
9

<!-- source_page: 10 -->

加5
EEEE
其中，
zx 表示 为 RGV 处 于 第 大 个 状态 时 的 位 置 ;
ty; 表示 转移 目标 位 置 处 CNC 的 上 料 时 间 ;
大 表示 下 一 次 上 料 的

开始 时 间 ， 为 行走 时 间 和 目标

CNC

剩余

工作 时 间 的 较 大 值 ;

te 表示 当前 状态 后 工件 清洗 的 时 间 ， 代 表 如 果 CNC 空置
则 清洗 ， 否 则 不 清洗 ;
cnki 表示 从 当前 状态 (k) 转移 到 下 一 个 状态 (k + 1) 需要
的 移动 时 间 。
对
于 公式 ， 函 数 帮 人 太 ) 定义 如 下 ，
F(Vi) = max{0,7p,;},1 <i <n,ieN*

函数 /Wi) 对 状态 Vi 的 CNC 剩余时 间 ms 取 max{0, Ry.i}» 因为 入 RE， 并 且
TEA

一 如，ek+Hi

一 工

一

此 外 ， 在 一 个 班次 (8 小 时 ) 的
时间 内
部 完成

， 所 以 在 状态 转移 的 时 候 引 入 约束

约束 三 : RGV

， 所 有 的 CNC

反

让

三、四。

的 工件 必须 全

)

一 定 能 够 回 到 原点 。

4s

te+ts+tu

约束 四

，RGV 到

一 I\)

+ 人

在 8 小 时 结束 时 处 于 非

工 帮 状态。

t 二

< Tr

易 知 约束 四 是 约束 三 时 条 件 更 为 严 棚 j 素 达 。
由 于 系统
的 上下 料 合

判 为 有 学 个 步骤

最 后 一 个 工件 的 上 下 料 操作
所 以 模型

最 优 佬 模型 上 标

的 深度 〈 长 度 )。

) '

oo
上

，所 以

我 们 在 求解 的 时 候 将 模型 中 8 个 CNC 的

淹 且 的 下 料 操作 ， 可 以 消除 这 个 约束 。
为 最 大化 M

值 ，换

言 之 ， 最 大 化 状态 转移 图 中 状态 传递

HI 下:

max Mj,

SR

Vierr = F(ViAr),

sto

Qtptto+t+cip < T,Vi € [Lo
大 十 下 十 2 大 十 如 十 丰 二 co < T, Vi € [LO

5.3 带 工序 约束 的 最 优 状 态 转移 图 模型
对 于 情况 二 ， 我 们 改进 针对 问题
我 们 设立

一 的 图 模型

CNC 类 型 向 量 Q, Fonn
& CNC

对 、 妃 和 移动 矩阵 C 的 定义 。
10

以 适应 问题 二 的 特殊 情况 。
的 类

型 ， 并 沿用 最 优 状 态 转移 图 模型 中

<!-- source_page: 11 -->

回味
1
首次 让 蒜

q1

o=|"l.aeton
mn

0 CNC'; 安装
第 一 类 刀片
1 CNC'; 安装
第 二 类 刀片
约束 一 : 当 RGYV 对 第 一 类 CNC 执行 上 下 料 操作 并 且 该 CNC 并 不 是 处 于 空置 状态
的 时 候 ，RGYV 的 下 一 个 操作 目标 不 能 是 第 一 类 CNC， 证
明 如 下:
#7
© RGV 对 第 一 类 非 控制 CNC 执行 上 下 料 操作 以 后 ， 若 CNC 非 空 RSSwwr
一 定 存在 一 个 半成品 工件 。
2
@ 半成品
工件 无 法 放 到 传送 带 上 ， 也 无 法 放 在 第 一 类 CNGK 中 。 1
由 @@ 可 知 ，RGYV 访问 一 个 非 空 第 一 类 CNC 以 后 凯 所 基 访 问 第 二 类 CNC。
在 第 大 个 状态 到 第 大 上 + 1 个 状态 进行 转移 的 时 笛 ， 通 过 下 式 实现 约束 一 :
qi =

(1

-

gr)ek

mx

人

1

#

1

并 且 修改 状态 转移 矩阵 的 约束 条 件 如 再 :
O

muRRARX

7

全

Ai 4

十 各 十 二 十 co

RRgas

crc, 没有 清洗 过 程 ， 不 计 清洗时 间

ea

即 妃 表示 各 和 PE 全
总的 类 学 模为 ，
谎

-

mm，

如 果 是 偶数CNC 则 上 料 时 间 为 Wo， 否则 为 如 。

max Mj

N

Vs = f(Vidr),

S

ttto + ti + cio < Da Vi € Lo
tytt+ 2t + ty + te+ cip < Ton,Vi € [Lunl,
(1= gp)erp, = Gpss # 1.
不 = (i mod 2)tyg + ((i + 1) mod 2)t;;.

11

<!-- source_page: 12 -->

回味
外
5.4 带 有 故障 风险 的 最 优 状 态 转移 图 模型
引入 故障 因子 已 = [p1. 有 珈 ,机 Bl， 其 中 六 表示 ;位 置 的 CNC 距离 修复 成 功
剩
下 的 时 间 。 如 果 产 为 0 则 表示 CNC 没有 损坏 。 根据题 意 , 在 RGV 为 第 大 台 CNC 上 料
完成 后 ， 该 CNC 处 于 加 工 状态 时 有 1% 概率
会 损坏 ， 即 mi = 9 其 中 为 第 ;个 CNC
距离 再 次 正常 工作 所 需 时 间 ， 由 于 故障 维修 时 间 介 于 10min 一 20min, 即 :(600s -1200s)。
所 以 ， 有 600< g; < 1200,9
€ 及 ;一 工 .m。 在 实际
的 模型 中 ， 每 次 状态 转移 都 有 可 能
有 至 多 mm， 至 少 0 个 处 于 工作 状态 的 CNC 出 现故 障 。
由 于 在 最 优 状 态 转移 图 模型 当 RGV 的 一 次 上 料 行为 完成 时 ， 模 型 状态 才 发 生 转 移 。
所 以 可 对 模型 进行 如 下 修改 ， 当 CNC 只 有 一 种 刀具 时 ， AN 的 估 增加 以 下
约束约束 ::
一 YY
2G

“move

Ap =Thiypi=0

cn

名

人

o

对 我 们 效率 的 影响 ;
和
认为 情况 1 与 情况 2 中 ,基本
满足 RGYV 供 成 能 为 与 CNC 工作 能 力 之 问 的 平衡 。 当
只 有 一 种 刀片 的 时 候 , 某 一 台 或 某 几 台 CNG 出 现 了 故障 , 我 们 认为 该 平衡 被 打破 , RGV
的 供应 能 力 大 于 CNC 工作 能 力 ， 你 外 系统 的 红 件 处 理 速 数量 减少 ， 但 是 单个CNC 的 工
作 效 率 变 高 。 当 装 有 两 种 刀片 时 ， 丽 音 奴 片 的 平衡 被 打破 ， 工 作 能 力 较 弱 的 一 方 ， 单 个
CNC 的 工作 效率 提升 ， 而 于 作 能 力 较 强 的 CNC 产生 或 增加 空间 ， 该 CNC 工作 效率 降
低 ， 束 个 系统 的 共 建 处 理 能 为 莉 E
故障 未 修复 时 ,=RGY的 圭 作 能 力 大 于 CNC，RGYV 出 现 等 待 情况 ， 系 统 效率 降低 ，
故障 修复 以 后 ， 和
当 CN at
(除了 满足 (1) - 3) 几 项 约束外 )， 根 据 系统 效率 均
衔 原则 Se 莉 溃 将 导致 各 工作 部 件 之 问 的 均衡 性 被 打破 ，
这 电 全 后 和 em
1 为 长于 动 满 足 系统 效率 均衡 原则 ,我们 主动 停止 使 用 部 分 CNC， 以 保证 系统
的 匹配。
2. 不 主动 调节 系统 的 效率 分 布 情况 ， 调 度 原则
不作 改 变。
5.5 模型
的 求解
使 用 原 模型 对 应 算法 直接 求解 《站 历 可 剪 枝 的 解 空间 树 ) 虽然 理论 上 可 以 得 到 最 优
解 ， 但 是 由 于 解 空间 树 过 于 庞大 ， 未 经 前 枝 的 搜索 算法 复杂 度 高 达 O(8")， 效率 较 低 、
收敛 速度 很 慢 ， 即 使 经 过 剪 枝 也 是 无 法 承受 的 !。
"最 优 性 剪 枝 优化

后 的 搜索 算法

实现 参见 附录

12

<!-- source_page: 13 -->

加5
0汪辣

因此 考虑 近似 求解 算法 ， 可 以 大 幅 提 升 求解 算法 的 求解 速度 ， 而 仅仅 牺牲
少量 结果
质量 。 这 里 我 们 将 原来 的 最 优化 问题 转换 为 多 阶段 决策 问题 ， 其 指导 原则 基于 该 最 优化
模型 的 各 种 最 优化 目标 和 约束 信息 ， 并 且 设计 算法 进行 求解 。
设 坊 为; 位置 CNC 的 在 整个 工时 内 实际 工作 时 间 ， 由 于 系统 中 RGYV 本 质 上 是 为
CNC 提供 服务 的 ， 即 : 尽 可 能 使 CNC 减少 等 待 时 间 ， 增 加 工作 时 间 从 而 提升 系统 整体
的 工作 效率 。 由 此 建立 工作 效率 度量 指标 一 CNC 的 工作 效率 为 :
Wene = 人

tpi

S.S.1 最 优 状 态 转移 图 模型 求解 算法

#

在 最 优 状 态态 转 移 图 模型 的 求解 过 程 中 ， ， 设 计 以 下 搜索 原则原则 :
1.
2.
3.
4.

= I\)SS

在 搜索
的 开始 阶段 ， 优 先 选择 前 两 个 CNC 进行 状态 转移 ; 2
在 状态 转移 的 过 程 中 ， 优 先 选择 转移 时 问 代价 小 的 进 生 和 5 站
当 转 移 代价 相 同时 ， artaoeog
需要 保证 任意 时 刻 状态 满足 可 行 性 约束 条 件 。 仿

算法 框架 :
JR
分 阶段 优化 原则 的 目标 是 : RGV 在 当前阶段 ,在 所 有 八 台 候选 CNC 中 ， 选择 可 以
最 快 上 料 并 进入 物料 加 工程 序 的 CNC 作为 下 一 阶段 的 目标 CNC。 随 着 系统 的 变化 算法
细节 有 所 不 同 。
%%
@
决策 过 程 :
TO
CNC 的 路 程 代价 ,该 CNC 加 工时 间 的 剩
余 ， 取 其 中 的 最 大 值 作 为 评估 个 。 选 择 八 台 CNC 中 评估
值 最 小 的 CNC 作为 目标 CNC，
意 为 选择 可 以 最 快 上 上 料 类 目标 CNC。
如 果 评 估 值 最 人 的 ERC 不 叭 一， 选择 其 中 上 料 时 间 较 短 的 。 如果 上 料 时 间 相 同 , 选
ee
5

的 最 优 状态 转移 图 模型 求解 算法

Row e
CNC 系统
中 与 单 类 型 CNC 系统 的 区 别 在 于 双 类 型 CNC 系统在 状
态 转移 的 限定 上 更 加 严格 ， 解 空间 更 小 ， 但 是 由 于 指数 级 复杂 度 的 特点 ， 一 般 的 方法 仍
然
无 法 求解 ， 我 们 采取
与 单 类 型 CNC 系统 的 相似 的 分 阶段 优化 算法 进行 计算 ， 框架 和
策略如 下 。
算法 框架 :
同 最 优 状态 转移 图 模型 求解 算法 的 基本 框架 ， 但 其 决策 规则 有 所 变更 。
决策 过 程 :

13

<!-- source_page: 14 -->

加5
EEEE
与 情况 1 中 算法 设计 基本 相同 ， 选 择 路 程 代 价 、 加 工时 间 的 剩余 中 的 大 者 为 评估
值 。 选 择 评估 值 最 小 的 CNC 作为 目标 ， 但 不 能 违反 以 下 约束 :
1. RGV

在 对 非 空 的 第 一 类 CNC 进行
上 下 料 操作 之 后 ， 不 执行 清洗 操作 ， 且 目的

CNC

一 定 是 第 二 类 CNC。
2. 如 果 评 估 值 最 小 的 CNC

违反 约束 ， 则 选择
评估 值 次 小 ， 如 此 往复 ， 直 到 找到
不 违反

约束
的 目标 CNC。

J)

三

g

)

|
上

众
，
+ AN

?

SN
NA

RD

nyy
b

外 \

w

ad

和
RRIO
情况 下 ， 总
致 相同 。C

JA=

人

CONC 刀片 类 型 比例 与 系统 产 出 关系 图
r

我 们 认为 系统 中 拥有 两 种 不 同型

号 的 CNC 的

体 效 源 最 早盘 BNC 的 比例 被 达到 当 是 尽量 两 类 CNC 处 理 物料 的 时 间 代价 大
处 理 # 料 的 时 间 代 价 分 为 两 部 分 ， 一 部 分 是 CNC 加 工 物料 的 时 间 和 RGV

上 料 的 民 Tee

p

是
一 个 定 值 。而 另 一 部 分

来 自 RGV

到 达 CNC 付出 的

时 间 ? 这 部 分 难以 计量 但 是 远 小 于 物料 加 工 的 时 间 ， 所 以 物料 加 工 的 时 间 占 有 主导
地 位 :| 国 的 横 轴 是 第 一 类 、 第二 类 CNC 的 比例 ， 纵 轴 是 采用 分 阶段 优化 算法 计算 三
种 情况

下， 第 一

类 、 第 二 类 CNC

比例 相同 的

空间 排 布 方案 的

3 中 所 示 ， 两 种 CNC 加 工 物料 时 间 几 乎 相同 的 情况
轴 的 对 称 且 在 两 种 CNC

成 品 数 的 平均

一 ， 系 统 处 理 能 力 呈 现 以 4:4 为 对 称

为 几乎 1:1 的 情况
下 取得 峰值 。 而 当 第 一 类 CNC

物料 处 理 时 间

小于， 即

工作 能 力 大 于 第 二 类 CNC

的 时 候 ， 峰 值 偏向 右 侧 即 第 一 类 CNC

二
类 CNC，

而 当 第 一 类 CNC

处 理 时 间 大 于 ， 即 工作 能 力 小 于 第 二 类 CNC

峰值

偏向 左 侧 即 第 一 类 CNC

物料
的

数目 大 于 第 二 类 CNC。

衡
优 化 原则 。
14

值。 正 如 图

的 数目
小于 第
的 时 候 ，

一 定 程度 上 证 明了 我 们 的 系统 均

<!-- source_page: 15 -->

加 5
汪汪

5.5.3

带 有 故障 风险 的 最 优 状 态 转移 图 模型 求解 算法

该 求解 算法 随机 模拟 故障 的 产生 ， 故 障 持续
时 间 在 10 分 钟 至 20 分 钟 之 间 随 机 生
成 。 算 法 在 RGV 每 次 进行 上 料 的 时 候 以 。 1% 的 概率
发 生 故 障 ， 如 果 发 生 故 障 ，在 物
料 加 工 的 过 程 中 随机 产生 故障 起 始 时 间 。
算法 框架 :
同 最 优 状 态 转 移 图 模型 求解 算法 的 基本 框架 。 此 外 ， 引 入 故障 变量 。 当 CNC 发 生
故障 时 ， 需 要 设置 该 CNC 故障 变量 为 1。
决策 过 程 :
1. 对 于 仅 有 一 种 类 型 刀片 的 CNC:
2
RGV 如 果 状 态 转移 的 最 优 目 标 为 某 一 故障 的 CNC 时 ， oa
无 故障 为 止 。 当 故障
时 间 结 束 ，CNC 重新 恢复正常 ，
<
WO5
2. 对 于 有 两 种 类 型 刀片 的 CNC:
同一
若 第 一 类 刀片 的 物料 处 理 时 间 为 右 ， 第 一 类 CNC 的 凑
处 理 时 间 为 刀 ， 第 二 类 CNC 的 数量 为 力 。 如 果 乒 着
刀 *mna 一 如 (71 一 1), 则 关闭
一 个 第 一 类 CNCy

他

量 纹 ny/
第 二 类 刀片
的 物料
2 并 且 厂na 一如 n? >

ting < tn2 并 且 tony — ting >

ting — ta(ny 一 1), 则 关闭 一 个 第 二 类 CNC。 约 到 的 含义 是 ， 从 优势 方 关闭 CNC 是 优
劣势 方差 距 减 小 的 情况 下 ， 关 闭 一 个 优势方 的 CNC 以 平衡 产能 , 达到 更 优 匹 配 。
个

5.5.4 模型
求解 与 结果 评价

和

“

最 优 状 态 转 移 图 模型 求解 结果 :
在 情况 一 条 件 下 ， 一 征 时 =e8 小 时 ) 内 第 一 、 二 、 三 组 能 够 生产 熟 料 的 最 大 数量
分
别 为 382、359、 321 个 ; CX 与 RGV 具体 的 调度 规则 见 支 撑 材 料 。
将 RGV = 人
间 进 行 绘制可 得 ;
在 该 图 中 3 厅 轴 描 述 了 RGV 的 空间 分 布 ，y 轴 描 述 了 RGYV 的 时 间 分 布 。 其
中 绿色
aoler
只 安装 一 种 刀片 时 移动 的 路 径 情 况 ， 而 黄 蓝 相 见 的 “ 紧 线 ”部
分则 刻画 所 RGV 正在 上 下 料 与 清洗 交替 进行 。 红 色 虚 线 则 表示 在 最 优 调度 下 此 时 RGV
NT
即 RGV 此 时 处 于 空闲 状态 。 注 意 到 该 方案 是 两 个 上 下 料 、 清
洗 动 作 次 蔡 进 行 ， 即 应 该 在 RGYV 在 某 处 重复 执行 该 操作 组 合 ， 更 具体 地 ， 由 于 RGV 不
会 对 在 工作 的 CNC 进行 操作 ， 因 此 其 模式 是 在 某 处 先后 操作 者 两 侧 的 CNC; 此 外 可 以
从 结果
中 看 到 ， 最 终结 果 在 中 间 过 程 呈 现 一 定 的 周期 性 ， 在 首尾 部 分 存在 打破 循环 ， 这
与 我 们 的 周期 性 假设 和 估计 基本 吻合 。
下 面 针 对 情况 一 ， 对 模型 求解 算法 的 求解 效果 与 质量 进行 分 析 :
根据 定义 3，CNC
满载 条 件 下 的 系统 具有 工作 上 限 ， 将 其 定义 为 超额 上 限 值 。 超 额
上 限 值 高 于 理论 最 优 解 且 接近 该 模型 的 最 优 解 ， 这 是 因为 CNC 满载 条 件 在 系统 运行 过
15

<!-- source_page: 16 -->

加5

1
四
一
一
一

正在 移动
正在
上下村
正在 清洗

…" 正在
等 待 完成 |

一

一

:二
| 一 一

|:

1] 一

第 1组

第 2组

一
-你 ，

入 罗

图 4 。 优化 后 RGV 的 运动 路 线 和 各 项 操作 时 间 图 了

程 中 是 较 难 满 足 的 ， 因 此 系统 在 时 间 上 会 有 一 定 的 损耗 用 和 咸 少 规定 时 间 内 生产的 熟
料 数目 。 因 此 以 该 上 界 作为 近似 解 的 评估 标准 具有 过
参考 价值。
下 面 定义 模型 结果 偏差 率 计 算 公式 ，
Ke”

A=MaNS
本
其 中 4 为 求解 值 ， 避 0A
| 画 蜀 求 解 算 法 所 得 解 与 超额 上 限 值 (CNC 满载
条 件 下 的 系统 具有 工作 上 限 ) 的 近 亿 二
表 太 我 优 状态 转移 图 模型 结果 分 析 表

Y-

一

2

第 2组

第 3 组

) Gemiemen|

384

372

396

下 4

求解 值

382

359

391

-

结果 偏差 率 | 0.9948

0.9651

0.9899

7

凰

数据 组 数 | 第 1 组

结合
该 结果 可 知 , 对 于 情况 一 下 的 三 组 数据 而 言 ， 该 模型 的 求解 算法 求解 效果 较 好 :
一 方面 计算 速度 较 快 ; 另 一 方面 , 所 求 结果 十 分 逼近 理论 上 界 ， 认 为 得 到 满意 的 近似 解 。
带 有 工序 约束 的 最 优 状态 转移 图 模型 求解 结果 :
在 情况
二 条 件 下 ， 一 个 工时 〈8 小 时 ) 内 第 一 、 二 、 三 组 能 够 生产 熟 料 的 最 大 数量

分 别 为 2533、210、240 个 。
CNC
CNC

编号 1-8 上 的 刀片 类 型 分 别 为 ;
与 RGV 具体 的 调度 规则 见 支 撑 材 料 。 在

16

该 图 中 ，z 轴 、Y 轴 分 别 描述 了 RGV

<!-- source_page: 17 -->

加5

表 2， 带 有 工序 约束 的 最 优 状 态 转 移 图 模型 刀片

CNC 编 号 |
第

1

一组 | 第 一 类

类 型最 优 分 布 表

2

3

4

5

6

7

8

第二 类

第 一 类

第 二 类

第 一 类

第二 类

第 一 类

第二 类

第 二 组

| 第 二 类

第

一类

第 二 类

第

一类

第 二 类

第

一类

第 二 类

第一 类

第 三 组

| 第 二 类

第

一类

第 一 类

第

一类

第 二 类

第

一类

第 一 类

第二 类

革

二 计生 二 六 下 2 和 |

-|

J—

一 一

四

2
-2

Lo

EL
|

第 1 组

人SN 1
人

先

组

第3 组

人 Ap
@
图 $ La
\

=—7

的 时 、 空 分 布 情况 。 全
径 情 况 并 且 此 时 RGWs
是 携带
任何 信物 这 行 2 共 和

这
物料 进行

外

的

了 在 CNC 只 安装 二 种 类 型 刀片 时 移动 的 路

“搬运

”操作 ， 而 绿色 虚线 部 分 则 是 描述 其 不 带

具有 更 的 时 间 开 销 。 黄 蓝 相 见

则 刻画 了

料 与 清洗 交替进行 。 红 色 虚 线 则 表示 在 最

CT

即 RGYV

人

即 应 该 在 RGYV

此 时 处

的“ 竖

线 ”部分

优 调度 下 此 时 RGV

于 空闲 状态 。 注 意 到 该 方案 是 两 个 上 下 料

在 某 处 重复 执行

该 操作 组

、清

合 ， 其 模式 也 是 在 某 处 先后

操作 两 笛 的 CNC; 此 外 可 以 从 结果 中 看 到 ， 最 终结 果 在 中 间 过 程 呈 现 一 定 的 周期 性 ， 只
是 周期 性 的 基本 模型 较 单一 类 型 刀片 有 所 不 同 。
下 面 给 出 模型 求解 算法 求解 结果 与 系统 工作 上 界 的 结果 偏差 率 分 析 。 值 得 注意 的
是 ， 这 里 的 上 界 是 在 确定 了 排 布 之 后 的 系统 工作 上 界 。
带 有 故障 风险 的 最 优 状 态 转移 图 模型

求解 结果

在 情况
三 条 件 下 ， 一 个 工时 〈8 小 时 ) 内 第
化 模型 进行 最 优 调度 所 取得 的 对 应 最 佳 结 果 为 :
对 于 只 有 一 类 刀片 的 CNC 的 三 组 数据 ， 其 在

17

一 、 二 、 三 组 在 随机 情况 下 ， 通 过 该 优
工期 内 分 别 发 生 3, 5,2 次 故障 的 条 件

<!-- source_page: 18 -->

加5
站 全二
表 3， 带 有 工序 约束 的 最 优 状 态 转移 图 模型 结果 分 析 表
数据 组 数 | 第 1 组

第 2 组 第3 组

超额

264

216

295

253

210

240

0.9722

0.8136

上限 值

求解 值
结果

偏差 率 | 0.9583

下 ， 产 量 分 别 为 376,250,387。

本

4

对 于 有 两 类 刀片 的 CNC 的 三 组 数据 ， 其 在 工期 内 分 别 发 生 3 .3.5

分 别
产量

、 为 243,205, 224。

2G
和

六 、 人

的

= \) SS

条件 下，

、

1. 模型
的 优点
、 尔
(a) 模型 建立 更 多 基于 理性 分 析 和 合理 推导， 入
reasrmearnmas
定义
和 证 明 ， 对 求解 的 决策 原则 进行 了 全 面 拉 分 析 和 讨论 ， 使 得 模型 具有 较 多 的
理论 支持 ;
四
(b) 模型 建立 从 状态 转移 的 视角 看 待 必 个 间 题 ,在 最 大 化 生产 件数 的 同时 将 各 工作 部
分 的 效率 均衡 考虑 在 内 。 通 于 化 笨 和 和 转换， 巧妙 地 将 以 秘 为 基本 单位 的 时间 划分
转换
为 基于 事件 的 时 回 划分 ， 减 求解
迁 代 次 数 ， 提 升 了 求解效率 。 在 模型的 求
解 算法 中 ， 通过 对 状 几 沿 村 的 压缩 存储 碱 少 了 计算 开销 。 此 外 ， 该 模型
的 近似 算
法 具有 快速 的 求解 速度 上 结果 和 近 最 优 解 ， 因 此 适合
于 任务 1 中 RGV 动态调度 ;
© ii
§ giieil 对 模型 求解 质量 以 及 系统 的 整体 性
能评 和 到科。
2. 寅 弄 的 天 <
4 党
状态 空间 较 大， 在 不 加 必要 限制 的 情况 下 ， 每 次 搜索 的 空间 为 8 个 ， 随
| 闭 钦 态 的 演进 搜索 量 呈 现 指数 级 上 升 ， 计 算 开销过 大 ， 因此 在 求解 模型 的 时 候 ，
考虑 使 用 分 阶段 优化 求解 ， 但 是 所 求 为近似 解 ， 且 较为
逼近 最 优 值 ， 但 仍 有 一 定
偏差。
(b) 此 外 , 本 题 中 很 多 性 质 的 证 明和 指导 原则 都 需要 满足 一 定 的 条 件 ， 例 如 系统CNC
满载 等 ， 尽 管 通过 机 理 分 析 可 知 ， 这 些 条 件 与 理论 最 优 情况 下 的 条 件 相差 不 大 ，
但 是 依然 存在 一 定 的 误差 ， 且 在 一 定 程度 上 限制 了 模型 的 普 适 性 和 推广 能 力 。
3. 模型
的 改进
18

<!-- source_page: 19 -->

加5
省 和 光头
(a) 可 以 进一步 深入 研究 系统 状态 的 特性 ， 例 如 : 周期 性 、 波 动 性 等 。 通 过 对 特性 进
行 概括
和 证 明 ， 并 据 此 改进 优化 过 程 ， 有 助 于 进一步 提升 模型 的 求解 精度 和 求解
速度 。
(b)

可 以 使 用 遗传 算法 原始 模型
角

会由 于 时 间 划 分 过 细 导

进行 求解 。 需 要 注意的 是 ， 如 果 从 时 间 和 状态 转移 视
致 染色 体 基 因数

目 过 多 问题 ， 或 者 基于 事件

编码 时 ， 由

于 各 个 事件 的 时 间 不 确定 ， 不 便于 对 所 选 方案 进行 编码 。 所 以 采用 可 以 采用 可 变
长 染色 体 的 遗传 算法 (Messy GA) [3]。 此 外 在 染色 体 交 又、 变异 操作 时 应 当 保 证
操作 后 的 染色 体 仍 在 可 行 解 区

域内 〈 不 能 出 现 一 个 物料 被 两 个 CNC 同时
加 工 )，

因此 需要 限制

的 有 效 范 围 。 从 而 提升 算法 求解 的 可 靠 性 。 其 基本

变异 和 交叉 操作

模型 如 下 :

_
2

你，

N
人
多
存 最 优 染色 体

o \ 由

& AZ
O
2
<

区

a

Preemesmon

) [|
¥

一

下 变异

四

ET
Yo|%, ，
谎 y

区

满足 终止 条 件

图

6

改进
遗传 算法 流程 图

根据 和 迭代 时 收敛 情况 ， 在 求解 时 间 和 解 的 质量 之 间作 出 权衡 。 此 外 ， 还 可 以 使 用
其 他 近似 求解 算法 完成 对 模型 的 求解 。
19

<!-- source_page: 20 -->

汪-这

Erires

参考 文献
[1]

吴 次 明 , 刘 永 强 , 张 栋 , 赵 韩 . 基于 遗传 算法 的 RGV

动态 调度 研究 [1]. 起 重 运 输 机

械 ,2012(06):20-23
[2] 陈 华 , 孙 启 元 . 基于 TS 算法
的 直线 往复 2-RGV

系统 调度 研究 [J].

工业 工程 与 管

理 ,2015,20(05):80-88.

[3] D. E. Goldberg, B. Korb, and K. Deb,

“Messy genetic algorithms: Mo- tivation, analysis,

and first results,” in Complex Syst., Sept. 1989, vol. 3, pp. 93-530.

5
-a,

ef/ 人

%°

外

这

一 一

站2
证

20

<!-- source_page: 21 -->

回 虽过

IE 辣
回 只 RN
waza

附录 A 最 优 性 剪 枝 优化 的 搜索 算法 C++
源 代码
注意 : 该 程序 在 总 时 长 为 1000s 时 可 以 很 快 给 出 答案
无 法 给 出 答案 《调整 代码 中 tot_t 的值 )。
1
2
3
4
5
6
7

#include <iostream>
#include <algorithm>
#include <vector>
#include <map>
using namespace std;
typedef pair<int, int> pii;
typedef pair<pii, vector<int>>

piv;

9
1

const int mov_t[] = {0, 20, 33,
const int proc_t[] = {560, 400,

46};
378};

1

const int ud_tD = {28, 31};

12

const int clr_t = 25;

1

const

15
16
17

Vector<piv> dfs_stack,
int global_ans = 0;

int

tot_t

=

， 但 在 8h 情况 下 由 于 复杂 度 过 高

-从
全

W

人

人

1000;

ans_stack;

全

答

多

18 void print_st(piv& st) {
19
2

cout << st.first.first << ' ' << st.finst.second;
for (int i : st.second) {
Vo)
外

21

cout

|:

<<

2

}

23

cout << endl;

26

”<<

1i;

<-T

%,

void print_stackC) TY

2

for Cauto& st, : Ra

-和
2

print

5

了
\\ /
:YA
3

32
33
34
55

int

36
»

nc(int rem_t, int cur_pos，vector<int>&
in
s = 0;
rem_t —= mov_t[cur_pos];
if (rem_t < 0) rem_t = 0;

cnc_sts)

for Cint i = 0; i < 8; i++) {
if (cnc_sts[i] != -1 8& rem_t >= cnc_sts[i]) {

38

res++;

39

}

4

了

4

res

+=

rem_t

4

return

res;

%

8 / (proc_t[@]

+ ud_t[0]);

21

{

/一

-

<!-- source_page: 22 -->

EEam

2

|

了
4
45
46
47
49
58

void dfsCint rem_t, int cur_pos, vector<int> cnc_sts，int cur_ans)
if Ccur_ans + eval_func(rem_t, cur_pos, cnc_sts) <= global_ans)
if Crem_t <= mov_t[cur_pos]) {
if (cur_ans > global_ans) {
global_ans = cur_ans;
ans_stack = dfs_stack;

s

}

s2

return;

5

了

s4
ss

dfs_stack.push_back(make_pair(make_pair(rem_t,
vector<int> order = {0, 1, 2, 3, 4, 5, 6, 7};

56

for

Cint

1 =0;

i <8;

i++)

cnc_sts));,
-从

{

W

57

int cur_max = i;

s

for (int j = ii j < 8; j+o {

59

cur_pos),

2

7

if (max(mov_t[abs(cur_pos — order[cur_max] / 2)J,
cnc_sts[order[cur_max]]) + ud_t[order[cur, ax]

max(mov_t[abs(cur_pos — order[j]1 / 2)], cnt.
ud_t[order[j] % 21) {
>、
0

cur_max = j;

上
四

}

63

swap(order[cur_max],

}
% 2]'<

sCorder[§11) +

二

}

6
65
66
67
6
69

order[il);

°

了
人
外
for Cint i : order) {
int pos
=1 / 2;
%,
int t = maxCmov_t[abSGeuF_pos — pos)], cnc_sts[i]) + ud_t[i % 2];
vector<int> —
s ¥ enc_sts;
new_cnc_sts[i] = —
加 - (cnc_sts[i] == -1? 0 : clr_t);

78

for

(int

j = IEE

j++)

ifGi

!= j)

7n
了2

if Seeda 疝 == -1) continue;
new_
cnc_sts[j] —= t + clr_t;

六

if

7

AN
_dfsCrem_t

人
。TN
77

She_stsL]

{

< 0) new_cnc_sts[j] = 0;

— t — clr_t,

pos,

new_cnc_sts,

cur_ans + (cnc_sts[i]

dfs_stack.pop_back();

78 了
19

w

int mainQ) {

81

ios::sync_with_stdio(false);

2

vector<int> init_st = {-1, -1, -1,

-1,

dfstot_t, 0, init_st, 0);
84
85

{
return;

cout << global_ans
print_stackC);

<< endl;

22

-1, —-1, -1,

—1};

== -1?

0 :

滞

<!-- source_page: 23 -->

回 虽过
p
[Oif=aeterd
waza
86
87

return 0;
了

附录 B Python 源 代 码
1
2
3
4

import

random

move_step_times = [0，20，33，46]
process_times = [560, 400, 378]

多

5 up_down_times = [28, 31]

-

6

clean_time

8
9
1
u

#
#
#
#

13
14

# move_step_times = [0，18，32，46]
# process_times = [545, 455, 182]

|

= 25

-从

move_step_times = [0, 23, 41, 59]
process_times = [580, 280, 500]
up_down_times = [30，35]
clean_time = 30

人

e

人 /一
答 -

下

15 # up_down_times = [27, 32]
16
17
18
19
2
21
22
23
24

# clean_time = 25
# INF = 100000000

%
27
2
2
38
3
3
33
34_
55
36

res = 0
“< 7)
cnc_states
6 人 i in range(8)]
fst_tine = [Tr
or i in range(8)]
iteng 半
国 [2a for i in range(8)]
brofl} SEO for i in range(8)]
items ='[]
broken_items = []

@@
人
AAA

cur_pos = 0
cur_time = 0
放
def move_time(posl, pos2):
return move_step, tuesrm

= or-

v

h pd
反 s1 — pos2)]

while True:
candidates = [i for i in range(8)]
candidates.sort(key=lambda 1i:max(move_time(cur_pos,
up_down_times[i

37
38
39

外

i // 2),

cnc_states[i])

% 2])

ok = False
for cur_cnc in candidates:
t1 = max(move_time(cur_pos,

cur_cnc // 2)，cnc_states[cur_cnc])
23

+

<!-- source_page: 24 -->

回 虽过

加
回 只 RN
4
a
4
4
4
45
46
47
48
49
58
s1
s2
53
s4
ss
56
57
58

to_cur_cnc_time = t1 + up_down_times[cur_cnc % 2]
ct = clean_time if not fst_time[cur_cnc] else 0
if cur_time + to_cur_cnc_time + ct + move_time(cur_pos, @) > 8 % 3600:
continue
ok = True
# print(cur_time, cur_pos, cnc_states, res)
if broken[cur_cnc] > 0:
continue
if random.random() < 0.01:
broken[cur_cnc] = random.randint(10 * 60, 20 *+ 60)
items.append({'cnc': cur_cnc + 1, 'up_time': cur_time + t1, 'down_time':
None})
加
print(len(items), cur_cnc + 1, cur_time + to corenc tine alloy
broken[cur_cnc])
=
broken_items.append({'cnc': cur_cnc + 1, 1
小
"down_time': None})
?
continue
}
for 1 in range(8):
cnc_states[i] -= to_cur_cnc_time + ct
4s
broken[i] -= to_cur_cnc_time + ct
>
if cnc_states[i] < 0:
二
cnc_states[i] = 0

5
6
61
6
63
6
65
66
67
6
69
78
7n

if broken[i] < 0:
broken[i] = 0

@

items.append({'cnc': cur_cni
1; 'upgtime':
None})
2
cnc_states[cur_cnc] = process_t ineso] 一 ct
if eramtaroaj
一
fst_time[cur_cnc -有 se
else:
res +=1
1 记
itel STiten_ dx[cur_cnc]]['down_time']
cur_tire CD
+ CCt
ur_pos =
cur_cnc // 2
item.idx[cur_cnc] = len(items) — 1

-证
73
74

in 二

ok:

break

m
76
7

print(res)
print(res * process_times[@]
for item in items:

四

print('\t'.join(map(str,

7
s

四
s

/ (8 * 8 % 3600))

item.values())))

print('Broken:')
for item in broken_items:

print('\t'.join(map(str,

item.values())))

print(items)
24

cur_time + t1,

= cur_time + tl

'down_time':

<!-- source_page: 25 -->

回 虽过
R

ChT

回 共 RN
waza

1
2

move_step_times = [@, 20, 33, 46]
process_times = [560, 400, 378]

3

up_down_times

4
5
6
7
s
9
10
11
12

clean_time
#
#
#
#

=

[28,

31]

= 25

move_step_times = [0，23，41，59]
process_times = [580, 280, 500]
up_down_times = [30, 35]
clean_time = 30
全
-从
W

# move_step_times = [0，18，32，46]
# process_times = [545，455，182]

13 # up_down_times = [27, 32]

二 于

14
15
16

# clean_time = 25
INF = 100000000

答

18
19
2
2
2
2
24

def move_time(posl, pos2):
return move_step_times[abs(posl

— pos2)]

e
for bin_class in range(l << 8):
cnc_class = [0 if (bin_class Xi
if

26
27
2
29
38
31
32
33

break
cnc_class = [0, 1, O, 二
1]
res = 0
8 个
cur_pos = 0
cur_time = 0
] V
half_pro 3Sho。
cnc_states,
=
or i in range(8)]
fst_time
rue for i in range(8)]

bin_class

i S6

外
== 0 else 1 for i in range(8)]

!= 0:

[-1 for i in range(8)]

35

SN

36

whilesTrue:

口

candidates = [i for i in range(8)]
candidates.sort(key=lambda 1i:max(move_time(cur_pos,
+ up_down_times[i

39
4
a
4
4
44

~

count = {}

25

37
38

人

全

-

i // 2),

cnc_states[i])

% 2])

ok = False
for cur_cnc in candidates:
if half_prod and cnc_class[cur_cnc] == 0:
continue
t1 = maxCmove_timeCcur_pos，cur_cnc // 2), cnc_states[cur_cnc])
to_cur_cnc_time = tl + up_down_times[cur_cnc % 2]
25

<!-- source_page: 26 -->

回 虽过

加
回 只 RN
45
46
47
48
49

ct = clean_time if cnc_class[cur_cnc] == 1 else 0
if cur_time + to_cur_cnc_time + ct + move_time(cur_pos, @) > 8 * 3600:
continue
if cnc_class[cur_cnc] == 0:
if cur_time + to_cur_cnc_time + process_times[1] + process_times[2] +
clean_time + move_time(cur_pos, @) > 8 + 3600:
half_prod = True
continue
ok = True
# print(cur_time, cur_cnc, cnc_states, cnc_class[cur_cnc], half_prod, res)
for i in range(8):
cnc_states[i] -= to_cur_cnc_time + ct
~
if cnc_states[i] < 0:
-从
cnc_states[i] = 0
RNNY
cnc_states[cur_cnc] = <
EN
if cnc_class[cur_cnc] == 0:
)
items.append({'cncl': cur_cnc + 1, 'up_timel)
《4 了: + tl1，
"down_time1': None, 'cnc2': None, 'up_gt
: Norle, 'down_time2':
None})
if item_idx[cur_cnc] != -1:
>
items[item_idx[cur_cnc]][" down_
= cur_time + t1
half_prod = item_idx[cur_cnc]
item_idx[cur_cnc] = len(items) — 1
else:
°
if not half_prod:
全

58
s1
s2
53
s4
ss
56
57
58
59
0

61
6
63
6
65
66

%

6
69

items[haLtf_prod] [cn
=_cur_cnc + 1
items[hatf_pr
sp_time2'] = cur_time + t1

7
n

if item_idx[cu
中
二 1:
items[item_idx[cuf-cnc]]['down_time2'] = cur_time + t1

了2
7
74
7
76

iten_idSESRZcnc
= half_prod
res += iv
二 Yopre = None
CU
9- to_cur_cnc_time + ct
册 curlLpas
= cur_cnc // 2

77

下

[DYeak

79

人 NA

80
81
82
83
84
85

num_1 = sum(cnc_class)
if count.get((8 — num_1, num_1)) is None:
count[(8 - num_1, num_1)] = 口
count[(8 — num_1, num_1)].append(res)
printCcount)

1

import

random

26

<!-- source_page: 27 -->

回 虽过

IE

辣

mRERER
waza
2
3
4

# move_step_times = [0, 20, 33, 46]
# process_times = [560, 400, 378]

5 # up_down_times = [28, 31]
6
7
8
9
1
u
12
13
14

# clean_time

move_step_times = [0, 18, 32, 46]
process_times = [545，455，182]

全
-从

1

up_down_times

全 W

16
17
18
19

clean_time

def move_time(posl, pos2):
return move_step_times[abs(posl

2

ans = 0

#
#
#
#

= 25

move_step_times = [0, 23, 41, 59]
process_times = [580, 280, 500]
up_down_times = [30, 35]
clean_time = 30

=

[27,

32]

= 25

>

22

2

u
25
26

¥

二

for bin_class in range(l << 8):

cnc_class = [0 if (bin_class & (1 << i)) == @ else 1 for i in range(8)]
°
# print(cnc_class)
bin_class

全

27

# if

2
29

:

#
break
# cnc_class = [0，1，0;

31
32
33

res = 0
cur_pos = 0
cur_time = 0

34

in_hand

55
36

cnc_states Le
i in range(8)]
itenaidx = [None for i in range(8)]

37

i

39
4
a

人

— pos2)]

2
)

!= 0:

%%

Tt

,1,0,1]

一 7
] 认

= No ne

[
= False
candidates = [i for i in range(8)]
candidates.sort(key=lambda 1i:max(move_time(cur_pos,

i // 2),

cnc_states[i])

+ up_down_times[i % 21)
4
4
44
45
46

for cur_cnc in candidates:
if in_hand is not None and cnc_class[cur_cnc] == 0:
continue
if in_hand is None and cnc_class[cur_cnc] == 1 and item_idx[cur_cnc]
None:
continue
27

is

<!-- source_page: 28 -->

EEam

2

|

47

mt = move_time(cur_pos, cur_cnc // 2)
rt = cnc_states[cur_cnc]
ct = 0
七 = max(mt, rt)
if cur_time + t + up_down_times[cur_cnc % 2] + move_time(cur_cnc // 2, 0)
> 8 % 3600:
continue
ok = True
# print(cur_time, cur_pos, cnc_states, item_idx, in_hand, res)
ct = clean_time if (cnc_class[cur_cnc] == 1 and item_idx[cur_cnc] is not
None) else 0
for i in range(8):
—~
cnc_states[i] -= (t + up_down_times[cur_cnc % 2] + ct) -从
if cnc_states[i] < 0:
e »
cnc_states[i] = 0
2
\
if cnc_class[cur_cnc] == 0:
items.append([cur_cnc + 1, cur_time + t, Non
Ay
— None])
if item_idx[cur_cnc] is not None:
in_hand = item_idx[cur_cnc]
4s

49
58
s1
s2
53
s4
ss
56
57
58
59
0
61
62
63

items[in_hand][2] = cur_time + t 全
65
66
67
6
69
78
7n
了2
也

item_idx[cur_cnc] = len(items) — 1
二
cnc_states[cur_cnc] = process_time:
else:
if in_hand is None:
°
items[item_idx[curJncj[-1]9= cur_time + t
ereda
res +=1
JV 》
else:
if item_idx
enel is None:

了4

item_idx[cur-cnc] = in_hand

7s
76
77

ighard = fone
race
[3] = cur_cnc + 1
items[item_idx[cur_cnc]][4] = cur_time + t

:

2

19

ao
81
82
83
84
85
86
87

党
]

SN
N

-

items[in_hand][3]

= cur_cnc + 1

items[in_hand][4] = cur_time + t

items[item_idx[cur_cnc]][5] = cur_time + t
item_idx[cur_cnc] = in_hand
in_hand = None
res +=1
cnc_states[cur_cnc] = process_times[2] — ct
cur_time += 七 + Up_down_times[cur_cnc % 2] + ct
cur_pos = cur_cnc // 2

88

break

89

if not ok:

%

break

91

全

ans = max(ans,

res)
28

滞

<!-- source_page: 29 -->

了
&F
入
%
%

部
