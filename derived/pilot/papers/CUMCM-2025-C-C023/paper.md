# Extracted Paper

<!-- source_page: 1 -->

基于 混合 效应 模型 的 NIPT 时 点 优化 与 胎儿 异常 判定
摘要
无 创 产 前 检测 (NIPT) 结果 的 准确 性 高 度 依赖 于 胎儿 游离 DNA 浓度 ， 该 浓度 受孕
周 (GA)、 身 体质
量 指数 (BMI) 等 因素 显著 影响 。 本 文 基于
临床 数据 ， 构 建 了 混合 效
应 模型 与 孕妇 潜在 风险 最 小 的 优化 模型 相 结合 的 优化 框架 ， 系 统 研究 NIPT 检测 时 点 优
化 与 胎儿 数 色 体 异 常 判 定 问题 。

针对 问题 一 , 首先 对 胎儿 立 染 色 体 浓度 (FF) 与 孕 周 (GA)、 身 体质
量 指数 (BMI)
的 相关 性 进行研究 。 通 过 对 FF 进行 logit 变换 ， 建 立 包含 二 次 项 的 线性 混合 效应 模型
(LMM) ， 并 引入 随机 截 距 与 斜率 捕捉 个 体 差异 。 结
果 表 明 : FF 随 GA 单调 上 升 ，BMI
旺 倒 U 型 关系 。 经 过 似 然 比 检验 ，GA 一 次 项 与 二 次 项 均 显著 ， 而 BMI 仅 二 次 项 显著 ，

模型
拟 合 优 度 达 到 = 0.8962， 显 著 优 于 传统 广义 线性 模型 。
针对 问题 二 , 本 研究 以 男 胎 Y 染色 体 浓度 最 早 达标 时 间 (FF
> 4%) 为 核心 ， 构 建
孕妇 潜在 风险 最 小 化 的 优化 模型 ， 充 分 考虑 孕妇 检测 失败 风险 、 时 间 风 险 ， 利 用 动态 规
划算 法 对 BMI 进行 5 段 分 组 并 确定 最 优 检测 时 点 。 分 组 结果 为 : [20.7,26.8] 一 1.9 周 、

[6.939.9] 一 12.8 周 、140.0.42.5| 一 17.5 周 、142.8.46.8| 一 20.4 周 、[44.7.46.8| 一 22.8
周 。 检 测 误差
分 析 表 明 ， 高 BMI 群体 对 误差
更 敏感 ， 推 荐 时 点 随 误差 增 大 而 推迟 ， 但

分 组 结构 保持 稳定 。
针对 问题 三, 本 研究 引入 年 龄 、 怀
孕 次 数 、 生 产 次 数 等 多 因素 ， 建 立 扩展
孕妇 潜在
风险 最 小 化 的 优化 模型 。 通 过 动态 规划 分 段 和 单调 性 控制 ， 得 到 5 组 年 龄 层 ， 各 组
BMI 分 区 及 对 应 时 点 。 多 因素 协同 效应 显著 , 年 龄 与 怀孕 次 数 增加 使 推荐 时 点 提前 ， 生
产 次 数 增加 则 推迟 检测 ， 经 交叉 验证 与 灵敏 度 回 验 验证 稳健 。

针对 问题 四 , 本 研究 针对 女 胎 染 色 体 异常 判定 ， 提 出 “ 男 胎 校 准 + 协 变量 校正 + 经
验零 分 布 + 多 重 检验

校正 ”的 综合 判定 模型 。 通 过 孕 周 分 层 、Z 值 标准化 与 FDR 控制 ，

输出
三 级 判定 结果 〈 阴 性 /可 疑 /阳性 )， HFRN ChrX 质 控 门 限 与 一 致 性 聚合 ， 降 低 批 次
效应 。 在 1% 假 阳性
率 约束 下 ， 女胎 检 出 3 例 阳性 、26 例 可 疑 ， 验 证 了 模型 具有 良好 的
稳健
性 与 临床 适用 性 。
本 文 创 新 性 在 于 : 一 是 建立 了 融合 混合 效应 与 动态 规划 的 NIPT 时 点 优化 框架 ; 二
是 提出 了 多 因素 协同 下 的 分 组 策略 与 误差 传播 分 析 方法 ; 三 是 制作 了 交互 网 页 , 为 孕妇
提供 最 优 NIPT 检测 时 间 ， 切 实 推广 模型应 用 。

关键 字 : 无 创 产 前 检测 ”混合 效应 模型 ”优化 模型 Z 值 判定 _ 数 色 体 异 常 得 查

1

<!-- source_page: 2 -->

一 、问 题 重 述
1.1 问题 背景
近年

来我 国

的 无 创 产 前 检测 技术 已 实现 广泛 应 用 与 持续 迭代 , 无 创 产 前 检测 (NIPT)

是 一 项 基于 孕妇 外 周

血 中 胎儿 游离 DNA

的 高 通 量 测序

技术 ， 用 于 评估 胎儿 常见 染色 体

非 整 倍 体 异常021。 该 技术 主要 针对
唐 氏 综合 征 (21 三 体 )、 爱 德 华氏 综合 征 (18 三 体 )
及 帕 陶 氏 综 合 征 (13 三 体 ) 等 染色 体 疾病 进行 得 查 E41。NIPT 结果 的 准确 性 在 很 大 程
度 上 依赖 于 胎儿 分 数 /性 染色 体 相 关 的 浓度 指标 : 对 于 男 胎 ， 通 常 认 为 当 胎 儿 游离 DNA
所 致 的 Y 染色 体 信 号 达到 一 定 比例 (临床
上 常 以 4% 作为
经 验 冰 值 ) 时 ， 检 测 结果 更
为 可 靠 ; 对 于 女 胎 ， 则 需 确保 X 染色 体 相关 指标 处 于 正常 范围 5 ?1。 此 外 ， 孕 妇 的 孕 周
(GA) 及 身体 质量 指数 (BMI) 等 因素 对 检测 性 能 与 最 佳 检测 时 机 具有 显著 影响 一 一 胎
儿 分 数 随

孕 周 增加 而

上 升 ， 而 高 BMI

与 低 胎儿 分 数 相关 E6sl。 临 床 实践 中 ， 过
早 检测

可 能 导致 “信息
不 足 /不 报告 (no-cal)”，

而 过 晚 检 测 则 与 母册 随 访

上 升 相 关 B491。 因 此 ， 基 于 生物 学 规律 与 统计 证
出 能 力 的 同时 降低 临床 风险 具有 重要 意义 Pol。

|

站

与 干预 时 机 相关 风险

据 ， 科 学 确定 检测
时 点 ， 对 于 在 保证 检

[让 兰芝

Ce
M-t-"==
AT) en
内
T- I=
下
-Te )
一 信

图 1 NIPT

示意 图

1.2 问题要 求
本 研究 需 结合 所 提供 的
问题

临床 数据 ， 建 立 数学 模型 以 系统 研究

1 分 析 胎儿 Y 染色 体 浓度

与 孕妇

孕 周 数 、BMI

以 下 四 个 问题 :

等 指标 之 间 的 相关

性， 建 立 关

系 模型 并 检验 其 显著 性 。
问题
2 以 男 胎 孕 妇 的 BMI 为 主要 影响 因素 ， 对 其 进行
合理 分 组 ， 确 定 每 组 的 最 佳
NIPT 检测 时

点 ， 以 最 小 化 孕妇 的 潜在 风险 ， 并 分 析 检 测 误差 对 结果 的 影响 。
2

<!-- source_page: 3 -->

问题
3 综合 考虑 体重 、 年 龄 、 检测 误差 及 Y 染色 体 浓度 达标 比例 等 因素 ,对 男 胎 孕
妇
进 行 BMI 分 组 ， 确 定 每 组 的 最 佳 NIPT 时 点 ， 以 最 小 化 潜在 风险 ， 并 分 析 误差影响 问题
4 针对 女 胎 孕 妇 ， 综 合 考虑 X 染色 体 及 其 他 染色 体 (21、18、13 号) 的 Z值 、
GC 含量 、 读 段 数 、 比例 及 BMI 等 因素 ， 建 立 女 胎 染 色 体 异 常 的 判定 方法 。
13 我 们 的 工作

5

国

&

本
T<'H ior=E|EESE

3
MMag

Bit

着
动态

LT

并

Ei
QFSTL
三
1 一作 全 定 生 由

am

村 <

Tilefgen|
B2

图 2

aa|

[38

[Namesn八

v

FE

瘟 体 流程 图

二 、 模 型 假设
为 简化 问题 ， 本 文 做 出 以 下 假设 :
* 假设 1: 假设 附件 提供 的 NIPT 临床 数据 真实 准确 * 假设 2: 假设
在 相近 的 BMI 值 区 间 内 ， 孕 妇 的 生理 特性 及 胎儿 Y 染色 体 流 度 的
变化 规律 是 连续 昌平潜 的 。
* 假设 3: 假设 模型 中 的 测量 误差 服从 均值 为 零 的 正 态 分 布 -

3

<!-- source_page: 4 -->

三 ， 符号 说 明
符号

说 明

单位

FF
GA
BAMT

胎儿 站 染色 体 浓度
孕 周
身体 质量 指数

了
周
ks/m2

v

logit(FF)

至

Bo,By--

园 定 效应 系数

=

uiby

随机 效应

=

a*
Pb 切
9

方差
达标 概率
浓度 靖 值 (0.04)

=

T.(b)

最 早 达标 时 间

民

一周

误差 放 缩 因子

了

0)

A

检测 失败 风险

NARD

临床 时 间 风 险

|

2

Z 值

ASTr、

了

FDR

核 正后 的9 值

~

=

四 、 问 题 一 : Y 染色 体 波 度 与 茸 周 、BMI 的 关联 异型
41 问题分 析
问题 一 的 核心 目标 是 建立 胎儿 立 染 色 体 潜 度 (FF) 与 孕 周 (GA) 及 身体 质量 指数
(BMD) 之 间 的 定量 关系 模型 。FF 作为 (0.1D) 区 间 的 比例 变量 ， 其 分 析 包含
两 个要 点: 一
是 需要 处 理 同一 孕妇 多 次 测量 导致 的 组 内 相关 性 ; 二 是 其 次 ， 数 据 具 有 虚 型 的 纵向 结
构 ， 同 一 孕妇 的 多 次 观测 在 生理 上 必然 相关 。 本 研究
对 因 变 量 FF 进行 losit 变换
以 消除
比例
数据 的 边界 约束 ; 对 孕 周 和 BMI 引入 二 次 项 以 捕捉 非 线性 关系 ; 采用 线性 混合 效
应 模型 框架 处 理 纵向 数据 的 组 内 相关 性 ， 通 过 随机 截 距 和 随机 斜率 刻 表 个 体 异 质 性 ， 从
而 构建 出 数学 上 严 谦 且 生 物 学 上 合理 的 定量 模型 。

4

<!-- source_page: 5 -->

We
人
|
CD |
El
iD)
1/em
em) ee)EB|
和二 |
|
|te
CE
Eee 人 下
图 3 问题

一 流程 图

42 数据
预 处理

本 研究 使 用 来 自 真实 临床 检测 记录 的 NIPT 数据 ， 有 效 观测 量 N = 1082， 涉及 267
名了 孕 妇 ， 人 均 测量
次 数 约 为 405。 核心 变量 统计 如 下 :
表1

为 直观 展示 FF

与 GA、BMI

核心 变量 的 描述 性 统计 结果
变量 ” 均数 (人

标准
莽全

FF

0.0772

—

0.0335

BMI

32.29

2397

之 间 的 复杂 关系 模式 ， 本 节 构 建 二 维 热力 图 进行 可 视

化 分 析 。 将 GA 和 BMI 分 别离 散 化

为 若干 区 间 ， 计 算

生成

每 个 (GA, BMD

组 合 下 FF 的 均值 ，

热力 图 矩阵 。
热力
图 分 析 结果 :
非 单 调 性 : FF 值 在 GA-BMI 平面 上 呈现 明显 的 非 单调 变化 模式 ， 排 除了 简单线性
关系
的可 能 性;
局 部 最 优 区 域 : 热力 图 显示 FF 在 特定 的 (GA, BMI) 区 域内 达到 相对 高 值 , 呈现" 山
峰 ” 状 分 布 特征
该 可 视 化 结果 从 数据 层面 证 实 了 变量 间 关 系 的 复杂 性 和 非 线 性 特征 , 为 后 续 引 入 二
次 项 和 交互 项 提供 了 直观 的 经 验证 据 ， 同 时 排除 了 使 用 简单 线性 模型 的 可 行 性 。

5

<!-- source_page: 6 -->

=

区3

下

CE

hr 人

在 不同 有 Kao 区 下 的 二

|
0

<

Fib

=

本

2

各

mE)

ee
cr

本

PE

E

wf
上

—

本

图 4 FF 在 不 同 耶 周 和 BMI 区 间 下 的 均值
分 布 热力 图
43 模型 建立
为 刻画 胎儿 Y 染色 体 浓度 (FF) 随 孕 周 (GA) 与 体质 指数 (BMD) 的 演化 规律 ， 并
兼顾
个 异 质 性 体 间 ， 本 节 采 用 线性 混合 效应 模型 (LMMJ。 本 节 通 过 在 固定 效应 中 引入
GA 和 BMI 的 二 次 项 来 捕捉 可 能 存在 的 非 线性 关系 ， 这 并 不 改变 模型 属于 线性 模型 杠
架
的 本 质 ， 而 是 增强 了 其 描述 复杂 现实 关系 的 能 力 。
43.1 响应 变量

与自 变 量 处 理

Step1: 响应 变量 为 Y 染色 体 浓度 FF， 其 取 值 位 于 区 间 (0.10 内 。 为 消除 比例 数据
的 边界 限制 并 改善 模型 拟 合 ， 对 FF 进行 logit 变 换 :

人

变换 后 的 y 取 值 于 整个 实数 域 ， 更 适用 于 线性建 模 。
Step2: 自 变量 包括 孕 周 (GA) 和 身体 质量 指数 (BMI)。
与 多 重 共 线 性 ， 对 GA 和 BMI 进行
中 心 化 处 理:

o

为 减少 变量 间 的 量 纲 差异

GA.
= GA-GR，BMI
~ BMI-BRT

@

其 中 GA 和 了 BMI 分 别 为 样本 中 GA 和 BMI 的 均值 。
4.3.2 模型 结构
设 第 ;位 孕妇 在 第

次 检测 中 经 logit 变换 后 的 响应 变量 为 %j ， 则 其 模型 表达 式 为 :

s = (Bo +us) + (Bu +b) - GAcs + By- GAZ; + By- BMlcys + B- BMIZ 二 5
6

G)

<!-- source_page: 7 -->

其中:
(1) 固定 效应 部 分 :

Nox = Bo + FiGAq + BaGA; 十 BaBMIoa + BBMIE,;

0)

该 部 分 用 于 刻画 群体 层面 FF 随 GA 与 BMI 变化
的 平均 趋势 ,引入 二 次 项 旨 在 捕捉 变量
间 可 能 存在 的 非 线性 关系 (如
堪 速 变化 、 倒 U 型 关系等 )， 从 而 更 精确 地 揭示 其 内 在 相

关性 。
(2) 随机 效应 部 分 :

u~ N(0,02),
该 部 分 用 于 描述 个 体 层面

平 差异 ; 随机 斜率

bi~ N(0,08),

Covlus,be) =ou

©)

的 随机 变异 。 其 中 ， 随 机 截 距 w 反映第 ; 位 孕妇 FF 的 基线 水

反映 其 对 孕 周 变化 的 响应 速率 差异 。 该 结构 有 效 解决 了 同一 孕妇

多 次 测量 带 来 的 组 内 相关 问题 。

(3) 残差 项 ;

cvN(o)

©

代表 模型 未 能 解释 的 随机 测量 误差 。
该 模型 兼 具 固 定 效应 与 随机 效应 ， 流 能 够 分 析 GA 和 BMI
对 FF 的 群体 平均 影响 ，
又 能 合理 处 理 纵向 数据 中 的 个 体 差异 与 重复 测量 相关 性 ,从 而 构建 出 稳健 且 解 释 性 强 的

统计 关系 模型 43.3 模型 的 比较 与 选择

为 确定 最 优 模型

形式 ， 本 节 系统 比较 了 线性 混合 效应 模型 和 种 广义 线性 模型 。 评 价

指标 涵盖 AIC、 对 数 似 然 值 以 及 在 FF 原 量 纲 上 的 拟 合 优 度 (R® 和 RMSE).

表 2 线性
混合 效应 模型 与 广义 线性 模型 拟 合 优 度 对 比

MD
MixedLM:
随机 截 更 + 斜率
+ 二 次 项

Ce
区 和 加

71263

-34732

Tao9a -3679%

RMSEFP MASE

。 08962

00108

0322

0003 0003

0o38

基于 前 述 模型 比较 结果 , 最 终 确定 了 包含 二 次 项 和 随机 斜率 的 混合 效应 模型 作为 最

优 模型 。 该 模型 不 仅 上 共有 最 低 的 AIC 值 (712.63) 和 最 优 的 对 数 似 然 值 (-347.32)， 在
FF 原 量 纲 上 也 表现 出 最 佳 的 拟 合 优 度 (Re = 0.8962，RMSE=0.0108) 。 与 广义 线性 模
型 相 比 ， 线 性 混合 效应 模型 带 来 了 显著 的 改善 ( 似 然 比 检验 LR=41.29,Ps 1.1x 10-9)，
强 有 力 地 证 明了 捕捉 非 线性 关系 的 必要 性 。

7

<!-- source_page: 8 -->

44 模 型 求解
本 节 采 用 家 大 似 然 估计 方法 对 所 定义 的 线性 混合 效应 模型 进行 参数 估计 。 具 体 算法
步戏 如 下 :
Step1: 模型 表达 与 似 然 数 构建
将 模型 写 为 矩阵 形式
y=XB+Za+e
O)
其 中 ，y 为 所 有 观测 的 logit(FP) 向 量 ; X 为 固定 效应 设计 失 阵 ， 包 含 C4e、G42、
BMI.. BMIZ: 也 为 随机 效应 设计 矩阵 ; YN(Q,G)
为 随机 效应 向 量 ; e ~ (0,R) 为
残差 向 量 。 总 方差- 协 方 关 结 构 为 :
Var(y) = V = ZGZ" + R

(8)

对 应 的 受 限 对 数 似 然 画 数 (REML) 为 :
4B0)= -iogvl- iogXIVXI-3G-xXprvie-X6
©)
其 中 0 为 方差 组 分 参数 。
Step2: 选 代 优化求解
使 用 牛顿 拉 弗 森 算法 或 期 望 最 大 化 算法 《EM) 进行
透 代 优化 ;逐次 更 新 固定 效应 系数
有 与 方差
组 分 0 (包括 oog,ouno?)， 直 至 对 数 似 然 本 数 收敛。
Step3: 结果 提取 与 解释
选
代 收 伍 后 提取 各 参数 的 估计 值 . 标准 误 及 假设 检验 结果 〈( 见 表 3)。 为 更 直观 解释 模
型 结果 ， 将 logit 尺度 下 的 固定 效应 条 数 转换 为 FF 原 尺度 下 的 平均 边际 效应 (Average
Marginal Effect, AME)， 具 体 通过 数值差分 或 Delta 方法 实现 :
AN
230 2。PR GE
Ga0)
Step4: 随机 效应 估计
通过 BLUP (Best Linear Unbiased Prediction) 估计 每 位 孕妇 的 随机 效应 ws 和 思 ， 并 计算
组 内 相关 系数CC;
只 二 Var(G4)

RERCALO

8

an

<!-- source_page: 9 -->

[本页包含图像型或无法可靠文本化的内容，请参见原 PDF 第 9 页]

<!-- source_page: 10 -->

46 结 论
本 研究 通过 建立 线性 混合 效应 模型 ， 成 功 揭示 了 胎儿 Y 染色 体 浓度 与 孚 周 、BMI
之 间 的 定量 关系 ， 主 要 结论如 下 :
1. 孕
周 效应 : FF 随 孚 周 显著 单调
(5cw

=0.003,p
< 0.001) ， 孕 周

上 升 (8ca = 0.042,P < 0.001) ， 且 存在
加 速效 应
每 增加 1 周

，FF

平均

上 升 0316 个 百分点

2.BMI 效应 : FF 与 BMI 呈 倒 U 型 关系 (BawmP = —0.003.p = 0.009) ， 在 BMI<31
kg/m? 处 达到 峰值 ， 之 后 随 BMI 增加
而 下降
3. 个 体 差 异 : 个 体 间 变 异 显著 (ICC<0.81) ， 证 实 采用 混合 效应 模型 的 必要 性

五 、 问 题 二 : 基于 BMI 分 组 的 NIPT 时 点 优化 模型
S.1 问题分 析
NIPT 检测 的 准确 性 高 度 依赖 于 胎儿 Y 染色 体 浓度 是 否 达 到 临床 阔 值 (4%) ， 而 该
浓度 受孕 妇 BMI 和 孕 周 的 共同影响 。 临 床 实践 表明 ，BMLI 较 高 的 孕妇 往往 需要 更 长 的
等 待 时 间 才 能 使 胎儿 Y 染色 体 浓度 达标 。 因 此 ， 科 学 确定不 同 BMI 群体 对 应 的 最 佳 检
测 时 点 ， 对 最 小 化 检测 失败 风险 与 临床 时 间 风 险 具 有 重要 意义 。 本文 旨 在 建立 一 种 基于
BMI 分 组 的 NIPT 时 点 优化 模型 ， 通 过 量化 BMI 与 最 早 达标 时 间 的 关系 ， 进 行 合理 分
组 并 在 每 组 内 推荐 统一 检测 时 间 ， 从 而 在 保障 检测 可 靠 性 的 前 提 下 ， 尽 可 能 降低
因 检测

过 早 或 过 晚 所 带 来 的 潜在 风险 。

ASS
1
||
CE
|1
上
1
1
) 人
Xe)
|
人
| 二
十

3
1
|

上 一

一 一 一 一 一 一 一

11
由
国|

一 一 一 一 一 一 一 一 一 一 一 一 一 一 一 一 一 一 一 上

图 7 问题 一 流程 图
5.2 数据处 理

基于 问题 一 的 线性 混合 效应 模型 ， 在
孕 周 区 间 |10,28] 的 离散
网 格 上 ， 对 每 个 BMI 水 平
逐 点 计算 FF 达到
阔 值 0 = 0.04 的 概率 Ptt,急 ， 并 以 首次 使 该 概率 不 低 于 4 = 0.95 的 孚
周作
为 最 早 达标 时 间 7T"亿 ;随后
将 离散 的 {(b. T(0))} 输入 带 单 调 先 验 的 贝 叶 斯 单调

10

<!-- source_page: 11 -->

回归 进行 平滑 ， 约 束 曲 线 随 BMI 单调 不 降 ， 得 到 稳健 的 平滑 函数 Tswe(b) 及 其 95% 置
信 带 ， 作 为 后 续 BMI 分 组 与 台阶 化 优化 的 输入 。
53 模型 建立
S3.1 基于

期 望 损失 最 小 化 的 BMI 分

组 与 时 点 决策

为 将 连续 的 推荐 孕 周 曲线 转化 为 临床 可 执行 的 有 限 分 组 策略 , 需 同步 优化 分 组 边界
和 各 组 的 统一 推荐 检测 时 点 。 本 小 节 详 细 半 述 该 优化 模型 的 目标 函数 与 约束 条 件 。
1. 决策 变量
设 将 BMI 定 义 域 划分 为 乓 段 (本 研究取 开 = 5), 定 义 分 段 断 点 集合 e = (co,cl,…,cK)，
满足

co = bmin,Ck = bmax, Co—1 < cu。

定义 每 段 的 统一 推荐 检测 孕 周 为 t= (at2,…,tK)， 其 中 心< [12,23|。
若
某 孕 妇 的 BMI值 上 € (cv-bcs, 则 其 被 归 和 人 第 s 组 ， 并 采用 统一 的 推荐 检测 时 点

to
2. 风险 度量 优化 目标 需 最 小 化 总 体 风险 ， 该 风险 由 两 部 分 构成 :
技术 失败 风险 rea(t,b): 在 推荐 孕 周 + 进行 抽 血 检测 时 ， 胎 儿 习 染色 体 浓度 仍 未 达
到 净值 0 = 4%6 的 概率 。 该 风险 是 孕 周上 和 BMIb 的 函数 :
Ta 人 (人 一 1 一 pr 人 要

(12)

其 中 mtt,b) 由 问题 一 的 混合 效应 模型 推 得 ， 并 引入 了 误差 缩放 因子 < 以 考量 检测 噪声 。
时 间 风 险 gb: 检测 时 机 过 列 所 带 来 的 临床 代价 。 该 函数 被 定义 为 分 段 线性 函数 ，
以 体现 不 同 孕 周 阶段 风险 的 差异 :

4 ={0，t<l2alt=12)

12<t<Blba+/(t—28),

t>28

(9)

其 中 , ac 和 有 为 惩罚 系数 ， 且 通常
E > o, 表示孕 28 周 后 延迟 检测 的 临床 风险 代价 更
高 。 此 函数 迫使 优化 解 不 会 为 了 无 限 提高 达标 概率 而 过 度 推 迟 检测 。
S3.2 目标 函数
目标 函数 旨 在

最 小 化 所 有 孕妇 的 群体 加 权 总 风险 , 并 附加 对 分 组 复杂 度 的 正则 化 惩

罚:
K

minJ(e,) = 3 3 wi lraa(ta,b) + 6(t)] + AK
=1iel,

其中:
1, 表示 被 划分 到 第 * 组 的 个 体 索 引 集合 。
ax 代表 第 ;个 样本 的 权重 (可 反映 其 在 人 群 中 的 分 布 )， 满 足 Zius = 1。
11

(14)

<!-- source_page: 12 -->

AK 是 正则
化 项 ,用 于 抑制 分 组 数 天 过 多 导致 的 方案 过 于 复杂 、 难 以 临床 执行 。 当
天 国定 时， 可 取入 = 0。
该 目标 函数 体现 了 "安全 -及 时 -可 执行 "三 者 的 权衡 : ra 追求 检测 的 可 知性 (安全 );
&t) 约束 检测
的 及 时 性 ; AK 保证
策 几 的 简洁 性 〈 可 执行 )。
533 约束 条 件
优化 问题 需 满足 以 下 约束 :
保障
率 约束 (安全性 ): 对 于 任意
分 组 *， 其 组 内 在 最 不 利 情况 下 的 达标 概率 仍 需 满
足 最 低 置信水 平 4 (基线 9 =0.95).
minpu(tab)Za. s=1. K
as)
该 约束 确保 了 分 组 的 鲁 棱 性 ， 即 只 要 孕妇 属于 该 组 ， 即 保证 其 在 推荐 时 点 检测 的 可 千
性。
可 执行
域 约 束 : 推荐 的 检测 孕 周 必须 在 临床 可 行 的 时 间 窗 口内 。
t,€[12,28],

s=1,....K

(16)

履 盖 性 与 非 重合 性 约束 : SHURENA BMUEUK, Bs RERR.
bi

一 co < €1 < +++ <CK

一 Do

(17)

单调
性 约束 〔 临 床 合理性 ): 推荐 孕 周 应 随 BMI 卉 加 而 非 递 减
该 约束 符合 "高 BMIB
强 方案
的 一 致 性。

hSh< Stk
as)
ERACI AOKRER, SFIERDHLLIALMSO
1, H

S4
模 型 求解
本 研究 采用 离散 化 结合 动态 规划 (DP) 的 算法 求解 上 述 优化 模型 ， 具 体 步 邓 如 下 :
Stepl: 离散
化 处 理 将 BMI 取 值 范围
按 步 长 (如 0.1 kgln) 离散 化 为 有 序 网 格 点
80 <by 三 :三 bm， 将 孕 周 搜索区 间 [10, 28] 按 步 长 (如 0.1 周 ) 离散
化 为 候选 检测
时 点 集合 了 。
Step2: 预计 算 区 间 代价 对 于 任意 BMI 区 间 [i : 让 和 候选时 点 4 E 三 ， 若 满足
该 区间
内所 有 BMI 点 在 时 点 上 的 最 小 达标 概率 约束 〔 即 minkefsjl pxtt,bgj) > 9)， 则 计算将 访
区 间 归 为 一 组 并 推荐 在 周 检测 的 代价 :
Clligit)
= 》 at [raattao)+eb]
=

12

(09)

<!-- source_page: 13 -->

对该 区 间 ， 其 最 小 代价 为 C(f, 7) = minterC(f
了 下， 并 记录 对 应 的 最 优 时 点 忆 (7)。 若
不 满足 约束 ， 则 置 C(L 让 = +oc。
Step3: 动态 规划 分 段 定义 DPU,o 为 将 前 了 个 BMI 点 划分 为 * 段 的 最 小 放风 险 。 状
态 转移 方程 为:
DP态 s] = 二 ai{DPRs =1]+C+1,5)}

(20)

同时 记录 状态 转移 路 径 。 算 法 复杂 度 为 O(o)。
Stepd:
回 测 与 后 处 理 从 DPIw,K] 开始 回 澜 ， 得 到 最 优 的 分 组 类 点 :cl .ex 以
及 每 段 对 应 的 推荐 检测 时 点 4。 = ((cr + 1.c.)。 为 确保 分 组 的 单调 性 和 保障 率 约束 ，
对 得 到 的 时 点 序列 进行 投影 和 籁 调 《如
台 体 平移 )。
Steps: 结果 输出 最 终 给 出 K 个 BMI 区 间 及 其 对 应 的 推荐 从 测 孕 半 、 段 内 平均 保障
率 、 平 均 风险
等 指标 。
该 算法 高 效 地 解决 了 分 组 和 时 点 指派 联合 优化 问题 , 确保 了 在 注 足 临床 约束 下 的 全
局 风险
最 小 化。
SS 求解 结果
为 便于 理解 ， 将 连续 建议 曲线 与 台阶 化 策略 进行 对 昭 必 未” 并 给 出 各 分 段 的 统计 江
总。
SM-MBRBPN.

展

单 届 二 村 ”闪失 最 优 台 闻 化 分 给

汪

2

图 8 连续
建议 Thwe() 与 5 段 风险 最 优 台阶 化 的 着 加 。

13

<!-- source_page: 14 -->

表 4 不 同 BMI 分 组 的 推荐孕 周
组 别 。 BMI 区 间 。 推荐孕 周 〔 周 ) 保障
率 光 值 ”风险雹 什
1

[207.268]

ne

09103

00897

2

(269,399)

ns

0.9693

00547

3

[400, 2.5)

173

09244

0.2406

4

[8468]

204

09264

03256

s

[447, 46.8)

228

09243

03997

5.6 敏感
性分析
为 评估 推荐 策 骆 对 检测 噪声 的 稳健 性 , 针对 “误差
缩放 因子 &” 开展 灵敏 度 分 析 , 并
在 两 种 保障 水 平 下 统计 加 权 平均 推荐 孕 周 及 其 相对 位 移 。 表 6 给 出 了 真实 测算 结果 ， 品
声 越 大 、 保 障 越 高 ， 平 均 推荐 孕 周 越 跪 。
表 S5 不 同 “ 下 的 平均 推荐 孕 周 与 相对 位 移
情 最 。。 &

RE

SEBRE ON) WHESAOD)

q=095

075

s

1844

4=005

100

5

To

+1.36

1

q=095

125

和

7 73

+0.65

=o0
9=098

19
075

5
了

we
1730

42m
-132

-oo

125

5

2138

+2.76

KZX

14

本

<!-- source_page: 15 -->

表6

不 同上 下 的 平均 推荐 孕 周 与 相对 位 移

情景

A 。 段 数 。 乎 均 推 荐 孕 周 ( 周 ) 相对
位 移 At ( 周 )

q=095

075

5

1844

+136

q=095

100

5

17.08

+0.00

q=095

125

5

1773

0.65

4=095

150

5

1967

十 2.59

4=098

075

s

1730

~1.32

q=098

100

5

1862

+0.00

q=098

125

5

2138

+276

q=098

150

5

23.10

+448

六 、 问 题 三 : 多 因素 协同 下 的 NIPT 时 点 决策 模型
6.1 问题分 析
在 问题
二 仅 考虑 BMI 单一 因素
的 基础 上 ， 问 题 三进一步
引入 孕妇 年 龄 (AGE)、 怀

孕次 数 (G) 与 生产次 数 (P) 三 项 临床
协 变量 ， 间 在 更 全 面 地 评估 多 因素 对 胎儿 站 染
色 体 浓度 (FF) 最 早 达标 时 间 的 影响 。 需 要 解决 的 核心 问题 包括 : 如 何 筛选 具有 统计 显
著 性 的 协 变量 ; 如 何 建立 多 因素 混合 效应 模型 ; 如 何在 兼顾 达标 比例 与 检测 误差 的 前 提
下 ， 给 出 基于 BMI 分 组 的 可 执行

健性 。

推荐 策略 ; 以 及 如 何 评估 模型

在 不 同 误差 口径 下 的 稳

TY,
‘oJ S—
1
| GEmD
)
>

[1
1

ER
由 人

|

ED

|
图 9 问题
三 流程 图

15

!

|
1

<!-- source_page: 16 -->

6.2 模型 建立
6.2.1 扩展

的 混合 效应 模型

首先 在 问题 一 模型 基础 上 引入 多 因素 ， 建 立 扩 展 的 混合 效应 模型 。 对 FF 进行 logit
变换 后 ， 模 型 形式 为 :

i5 =Bo + BiGA; + BGAL + BsBMly;

+BBMP + Bace AGEeis + BoGoys
+BpPegs + ios + WiGAgy + €55

CD

其 中 新 引入 的 固定 效应 项: (1) Sace: FERAMBRY (2) pc: 怀孕
次 数 的 偏 效应 (3)
pp: 生产
次 数 的 仿效 应
通过 Elastic-Net
变量 筛选 与 显著 性 检验 ， 确 保 上 述 纳入 模型 的 协 变量 具有 统计 学 意
义。
6.2.2 多 因素
优化 模型 框架
在 问题 二 优化 模型 基础

上， 引 入 协 变量向 量 :

2=(AGE.,Ge, P)T
其 中 各 变量 均 已 中 心 化 处 理。 目标 是 在 给 定 概率 模型
策略 ， 并 最 小 化 总 体 风 险 。

的前 提 下

,构造
可 执行 的 分 段 推荐

决策 变量
(1) 分
段 断 点 : < = (ciei) cx)， 满 足 co = bmin,ckr = bm (2) 段内 推
着 孕 周: t=(,... tk), tell228| (3) 新 增 : 协 变量 线性 偏 移 : YE R3， 用 于 对 个
体 锥 荐 时 点 进行 个 性 化 微调
目标 函数
K

min Jet,y)= pHBL

[ma (ta+ 7720.b5%) +6 (t +972)] + AK +Q(7)

其 中 : - raa 为 技术 失败 风险 , 考虑 了 个 体 协 变量
Pllylly 为 稀 朴 正则 项 ， 防 止 对 协 变量 的 过 度 依赖

影响 - g 为 时 间 风 险 函 数 -新 增 : (7) =

约束 条 件 1. 保障
率 约束 :

minminp(t +972,052) 2 ¢,
同时 考虑 段 内 最 弱 个 体 与 最 差 检测 条 件 ， 安 全 性 更 强

16

(22)

5

天

<!-- source_page: 17 -->

2. 可 执行
域 约束
t €[12,28],

|yfle<T

相 较 问题 二 新 增 约 束 : 对 协 变量 伪 移 量 施加 界 约束 ， 保 证 调整 三 度 在 临床 可 接受 范围 内
3. 分 段 覆盖 性 与 非 重 驮 性
4 单调
性 约束 : 所 三思 三 … 三 帮
5. 新 增 -一 一 致 性 约束 ; 同一 分 段 内 个 体 推荐 时 点 的 调整 方向 需 符合 临床 先 验 : (1)
年
零 效应 : ?YAaE < 0 (年
零 越 大 ， 推 荐 时 点 越 早 ) (2) 生产
次 数 效应 : YP > 0 (生产 次
数 越 多， 推 荐 时 点 越 噶 )
6.3 模型 求解
采用 "两 阶段 ”动态 规划 "策略 :
1. 偏 移 量 预 估计 : 固定 一 条 连续 推荐 曲线 ， 求 解 :

省= 2

[raa(Tinom(b:) + 7726, 区 ] +

2. 区 间 代 价 预 计算 : 对 每 个 BMI 区 间 和 候选时 点 ， 计 算 带 有 个 体 化 调整 的 代价 函
数
3. 动态 规划 分

段 ; 采用 与 问题 二 相同 的 DP 框架 ,但 代价 函数

考虑 了 个 体 协 变量 调

整
4 后 处

理 与 稳健 性 回 验 : 对 多 种 误差 场景 和 保障 水 平 进行 回 验 ,必要
时 进行 整体 平

移
算法
复杂 度 保持 在 O(n?)
量 级 ， 与 问题
二 相同 ， 具 备 工程
可 行 性。
6.4 求解 结果
本 节 对 样本 按 年 龄 分 层 并 在 各 层 内 进行 BMI 分 段 台 阶 化 。 表 7 显示 出 清晰 的 一 致
性 规律 ;
， 同龄
层 内 随 BMI 单调 后 移 , 各 年 龄 层 的 推荐 孕 周 均 随 BMI 雯 加 而 后 移 。 其 中 在 BMI
~ 40 左右 常 出 现 阶 跃 式 上 移 ， 提 示 高 BMI 区 间 对 时 点 安排 更 敏感 。
*， 同一 BMI 水 平 下 随 年 龄 整体 验证 “更晚 "。 在 中 高 BMI 段 ， 年 苍 越 大 推荐 孚 周 越 晚。

。 意义 。 低 BML 且 年 轻 (如 <25 岁 、BMI <32) 的 受 检 者 可 在 里 孕期 (10-13 周 ) 安
排检 测 ; BMI 升 高 与 /或 年 零 升 高 时 ， 需 后 移 至 中 晚 孕期 (例如 BMI
~ 40 时 普遍 需

要 18-22 周 ，> 40 岁 且 BMI > 34 时 建议 25-26 周 附近 ) 。

17

<!-- source_page: 18 -->

表7

按 年 龄 分 层 的 BMI 分 段 推荐孕 周

年 锥层

BMI 区间 。 推荐孕 周 ( 周)

<5 岁

网 格 数 。。 年 齿 层

BMI区 间

推荐孕 周 ( 周 ) 网格 数

|2s9s, 31.98]

106

31

30-34 岁 195.50, 41.50]

150

6l

5 岁 。 [8208 3448
5 岁 (3458, 36.08)

128
152

25
16

0MY
30-3%

[4160, 44.10]
[4420, 46.50]

186
21

26
27

5 岁 。 7.68, 3028]

215

17

s9y

poom 32 人

25-29 岁 126.62， 32.53|
25-29岁 “192.62, 3672)
25-29岁 “136.852, 3052)

105
128
156

2
28

35-39 岁 9292, 3372]
35-39 岁 8382, 34.42)
3PY [3452 305

2520%

[30.62, 42.02)

19.1

2

Ce

25-29 岁 42.12，44.62]

22.4

26

S0y

m2

时

30-34 岁 “|2070, 2350)
30-34岁 “|29.90， 35.40]

141
141

32
6。

>40 岁 。 93.49, 33.99|
240
>oy
piossm 2

6

>40 岁

和

ya

加 mo

[84.59, 34.99]

a;
179
179
179

263

9
7
st

s

6.5
敏 感性 分 析
通过 引入 误差 缩放 因子 < 模拟 不 同 检测 嗓 声 水 平 ， 分 析 推荐 时 点 的 变化 :
表 8 ”不同 误差 水 平 下 的 推荐 孕 周 变化

©

EHEERN (N)相对 变化 (N) AATRE

075

2020

0.47

低
唤 声 条 件

io Ta

ow

闪闪 条件

125

+0.50

中 等 品声 条 件

1L04

高
只声条件

ua

23.7

二

同时 分 析 各 协 变 量 的 影响 程度 : (1) 年
零 效 应 : 年 龄 每 增加 1 岁 ， 推 荐 检测
时点 平
均 提前 0.065 周 (2) 怀孕
次 数 效应 : 怀孕
次 数 增加 1 次 ， 推 荐 检测 时 点 平均 提前 0.057
周 (3) 生产
次 数 效应 ; 生产
次 数 增加 1 次 ， 推 荐 检测 时 点 平均 推迟 0.039 周
结果 表明 ， 噪 声 越 大， 推 荐 时 点 越 晚 ， 但 分 组 边界 保持 稳定 ， 说 明 模型
具有 较 强 的
鲁 棒 性 。 协 变量 的 影响 方向 与 临床 经 验 一 致 ， 虽 然 数 值 不 大 ， 但 共同 作用 提高 了 模型 的
个
性 化 程度 。
18

<!-- source_page: 19 -->

6.6 结论
问题 三 在 问题 二 的 基础 上 ， 成 功 构建 了 多 因素 协同 下 的 NIPT 时 点 优化 模型 。 通 过
引入 年 龄 、 怀 孕 次 数 和 生产 次 数 等 协 变量 ， 并 建立 相应 的 优化 框架 与 约束 条 件 ， 模 型 在
保持 分 组 稳健 性 的 同时 ， 显 著 提 升 了 个 性 化 推荐 能 力。 敏 感性
分 析 表 明 ， 模 型 对 检测 误
差 具 有 良好
的 适应 性 ， 分 段 结构 稳定 ， 推 荐 时 点 随 噪声 增 大 而 系统 性 后 移 。 各
协 变量 的
影响 程度 虽 小 ， 但 方向 符合 临床 先 验 ， 共 同 增强 了 模型 的 解释 能 力 。 该 模型
为 临床 实践
中 个 性 化 检测 策略 的 制定 提供 了 更 为 科学 、 可 靠 的 理论 依据 ,进一步
降低 了 孕妇 的 潜在
临床 风险 。

七 、 问 题 四 : 女 胎 染色 体 异 常 的 统计 判定 模型
7.1 问题分 析
针对 女 胎 染色 体 异 常 判 定 中 无 法 依赖 Y 染色 体 信号 ， 且 易 受 测序 批 次 效应 、 孕周 、
BMI 及 多 项 质 控 指 标 干 扰 的 问题 ， 本 研究
旨 在 构建 一 个 综合 统计 判定 流程 ， 该 流程需 在
严格 控制 假 阳性 率 (FPR) 的
前 提 下 ， 通 过 有 效 整合 男 胎 校准 数据 、 协 变量 校正 、 分 层
霉 分布 估计 以 及 多 重 检验 校正 等 多 重 统计 技术 ， 以 实现
对 第 13、18 和 21 号 染色
体 非整
倍 体 异 常 信号 的 准确 识别 与 风险 分 层 ， 从 而 为 临床 提供 可 靠 且 可 操作 的 筛 查 结论 。

1
全
| | cs GD |
|
GD)ao)
ee》
Da ’l| 必 四 ||
JE
一

一

一 一 一 二

I

1

请

时 ]

La

机

1

]

Ea

图 10 问题
四 流程 图
7.2 数据
预处理
本 研究 从 原始 数据 中 系统 提取 了 三 类 变量 ， 包 括 基本 特征 (如 GA、BMI、 年龄 ) 、
测序 质量 指标 如
总 读 段 数 、 唯 一 比 对 数 、 比 对 率 、 重 复 率 、GC 含量 、 检 测 批 次) 以
及 染色
体 信号

(Chrl3/18/21

的 Z 值 ，并
以 ChrX 作为
内 部 质 控 参 考) ; 为

减少
孚 周 带 米

的 系统
性 变异 ， 首 先 将 GA 划分 为 Early (<14 周 ) Mid (14-22 周 ) 和 Late (>22周 )
三 个 层次 ， 进 而 所 有 分 析 均 在 “染色 体 x 孚 周 层 ”内 独立 进行 ， 以 控制 层 内 变异 并 提升
模型 稳健 性 。
19

<!-- source_page: 20 -->

7.3 模型 建立
7.3.1 男 胎 回 归 校 正 与 零 分 布 构建
在

每 个 “染色
体 - 孕 周 ” 层 内 ， 利 用 男 胎 阴 性 对 照样 本 拟 合 线性 回归 模型 :
We 一 io+ 有

ri+eico，icAt

其 中 协 变量
向 量 r* 涵盖 GA、BMI、 读 段 数 、 比 对 率 、 重 复 率 、 唯 一 读 段 数 、GC含
与 批 次 等 变量 ; 对 残差 进行 19 Winsorize 截 尾 处 理 后 ， 计 算 其 稳健 位 置 与 尺度 参数 :

量

fioeg = median(sico)，

io = MAD(sieo)

针对 Chr21 厚度 尾 特性 采用 上 分 布 拟 合 零 分 布 ，Chrl3 与 Chrl8 则 使 用 正 态 分 布 ，
以 更 准确 地 反映 其 统计 特性 。
7.3.2 女 胎 标 准 化 与 假设 检验
将 女 胎 样本 代入 上 述 回归 模型 得 到 残 差 并 标准 化 为 Z 值 :

es

(BH)

依据 零 分 布 类 型 计算 双 侧 了 值 , 并 在 各 "染色体
- 孕 周 " 层 内 通过 Benjamini-Hochberg
方法 进行 多 重 检验 校正 得 到 4 值 ， 从 而 控制
假发 现 率 。

7.33 判定 规则 与 一 致 性 育 合
设

定 如 下 双 阔 值 判 定 规则 :

。 阳性: [2cq) > sar B Gico 三 qur
WIBE: [2icql > xm 或 和 eg 三 0

。 阴性 : 其 他 情况
进而 对 同一 受 试 者 在 同一 染色 体 上 的 多 次 检测 结果 进行 一 致 性 聚合 , 要 求 至 少 上 次
同 符 号 且 通 过 阔 值 的 检测 才 最 终 判 定 为 阳性 ， 同 时 引入 ChrX 的 Z 值 作为 质 控 门限 ， 进
一 步 筛 除 异常 批 次 或 样本 。
7.4 模型 求解
采用 网 格 搜索 方法 在 男 苔 数据 上 评估 不 同 盖 值 组 合 下 的 假 阳性 率 , 通过 求解 以 下 优
化 问题 确定 最 优 参数 :

20

<!-- source_page: 21 -->

SO(O)
一 AP:FPR(O)

st

FPR<a，

Alhosny€6, K€ {1,2,3)

其中 0 = (2ar,gqar
Zsus Gouss k) ， 在 FPR 不 超过 1% 的 约束 下 ， 最 终 选 定 基线 参数 为
zi ==26，qir
= 0.05, 大 = 2， 实 现在 控制 假 阳性 的 同时 最 大 化 检 出 效能 ，
7.5 结果 可 视 化 分 析
通过 对 附件 中 所 有 女 胎 样本 进行 系统 性 的 判定 分 析 得 到 了 详实
的 统计 结果 。 在 总
共 147
个 样本 中 ,判定
为 阴性 的 有 118例 ， 占 总 数 的 80.3%; 判定
为 可 疑 的 有 26 例 ， 占
17.7%; 判定
为 阳性 的 有 3 例 ， 占 2.0%。 这 一 分 布 情况 表明 ， 大 多 数 样本 显示 正常 娄 色
体 状态 ， 只 有 少数 样本 存在 异常 或 可 疑 情况 ， 这 与 临床 实际 情况 和 预期 相符 。

区

二

冯 浪 色 体 的 个 体 级 结论 分 布

面

bel_subyect

入”
四
P

王
-

2
要

图1

1
本

-

2

-

ea

日
于

各 染色 体 的 个 体 级 结论 分 布 〈 阴 性 /可 疑 /阳性
计数 )
普 次 达到 铀 值 的 孕 周 【〔 按 最 终结 论 )

机
和 ma
村。

-

图 12

9

首次 达到 阔 值 的 邓 周 分 布

21

<!-- source_page: 22 -->

在 可 视 化 分 析 方面 ， 本 节 通过 多 个 维度 的 图 表 展 示 了 模型 的 判定 效果 ， 图 1 展示 了
不 同 染 色 体 在 各 个 判定 等 级 下 的 样本 分 布 情况 ， 可 以 清楚 地 看 到 阳性 样本 数量 较 少 ,而
可 疑 样本 主要 分 布 在 闽 值 附近 区 域 。 图 12 显 示 了 全 体 女 胎 样本 | 值 的 分 布 直方 图 ， 闽
值
线 z= 2.6 能 够 清晰 地 将 阳性 候选 样本 分 离 出 来 ， 显 示 出 良好
的 区 分 度。
aa
ma
x

|

"

IEF2'

Ta

Et

.

|
js

Chrl3:

g

m—

=

4

|

3
|

SREENET 5

网 值 线 【虚线 ) Z LXhAdIX,
分 离 良好

Hz'5Mil

_

Chrl8:

间 梯 呈现 清晰 分 离 ; 少数
样本 跨越 出 值 -

ee
|

山 rr

总

0

|

几 本

和 六 生生

Fi
ER

Chr21;

采用 《 零 分 布 与 惫 变量 校正

后 ， 厚 尾 被 抑制 ，

边缘
闯 本 更 稳定 ,，

图 13 素 周 vs. | 散 点
图 13 展 示 了 首次 达到 靖 值 的 孕 周 分 布 情况 , 可 以 发 现 阳性 样本 普遍 在 较 早孕 周 (<16
周 ) 就 达到 了 判定阔 值 ， 这 表明 异常 信号 往往 出 现 较 早 且 相 对 稳定 。 孕 周 与 12| 值 的 散
点
图 展示 出 21 号 染色 体 在 经 过 ;分 布 校正 后 , 原本 明显 的 厚 尾 现象 得 到 了 有 效 抑制 ， 边
缘 样本 的 判定 更 加 稳定 可 售 。
7.6

结论

本 研究 针对 女 胎 染 色 体 异常 判定 问题 , 建立 了 一 个 基于 多 因素 协 变 量 校正 与 一 致 答
形 合 的 统计 判定 模型 ， 得 出 以 下结论 :
模型
有 效 性 : 通过
孚 周 分 层 、 男 胎 校准 和 协 变量 回归 ， 有 效 消除 了 系统
性 偏 倚， 提
22

<!-- source_page: 23 -->

升 了 判定 的 稳健 性 和 可 比 性 。 特 别 对 21 号 染色 体 采用 ¢ 分 布 处 理 ， 较 好 地 解决
了厚尾
问题 。
误差 控制 良好 : 通过 FDR 校正 和 一 致 性 聚合 (k = 2) ， 在 保证 高 灵敏 度 的 同时 将
整体 FPR 控制 在 19 以下， 满足 了 临床 得 查 的 要 求 。
临床 适用 性 强 : 输出 " 阴性 /可 疑 / 阳 性 ”三 级 判定 ， 明 确 且 可 操作 ， 可 疑 清单
可 为 复
检 提 供 优先 方向 ， 提 高 了 筛 查 效率 。
推广 性 良好 : 模型 框架 不 依赖 于 特定 数据 类 型 ， 可 扩展 至 其 他 染色 体 异 常 的 得 查 场
景 ， 有 具备 良好 的 泛 化 能 力 。
本 模型 为 女 胎 桨 色 体 异 常 的 早期 筛 查 提供 了 科学 、 可 靠 的 判定
工具 ， 具 有 较 强 的 理
论 基础 和 实际 应 用 价值 。 通 过 综合 考虑 多 种 影响 因素 和 建立 严格 的 统计 判定 规则 , 实现
了 对 女 胎 染色 体 异 常 准确 、 稳 健 的 检测 。

八 、模
型 的 评价
8.1 模型
的 优点
* 优点 1: 融合 混合 效应 与 动态 规划 ， 建 模 科 学 严谨 。
。 优点 2: 女 胎 异 常 判 定 模型 综合 性 强 ， 误 差 控 制 良好 。
。 优点 3: 可 视 化 与 交互 式 工具 支持 ， 便 于 临床 落地 。
8.2 模型
的 缺点
* 缺点 1: 数据 依赖 性 强 ， 泛 化 能 力 有 待 验证 ;
© 缺点 2: 未 考虑 其 他 潜在 影响 因素 : 如 孕妇 遗传 背景 、 饮
食 习 惯 、 胎 盘 功能等 未
纳入 模型 。

参考 文献
[1] LIUS, BIQ. HUANG S, et al. Utilizing non-invasive prenatal test sequencing data for
human genetic investigation[J]. Cell Genomics, 2024, 4(10):100669.
[2] MOKVELD T, SISTERMANS E, et al. A comprehensive performance analysis of the
within-sample testing method wisecondor and its variants[J]. PLOS ONE, 2023, 18(5):
e0284493.

B] 王 连 , 程 世 斌 , OE, 等 . 无 创 产 前 DNA 检测 在 性 染色 体 非 整 倍 体 筛 查 中 的 效果 评价

串 , 中 国生 殖 健康 杂志 , 2024, 35(5):465-469.
23

<!-- source_page: 24 -->

[4] 姚静 怡 , 汉 树 人 , 谢 晓 姐 , 等 , NIPT 提示 胎儿 性 染色 体 非 整 倍 体 疾 病 高 危 孕 妇 的 产 前
诊断
及 妊娠 选择 器 . 国际 妇 产 科学 杂志 , 2024, 51(1):32-36.

[5] GAZDARICA J. FORGACOVA N, SLADECEK T et al Insights into non-informative
results from non-invasive prenatal screening through gestational age, matemal bmi, and
age analyses[J]. PLOS ONE. 2024, 19(3):¢0280858.
[6] PAN Y. LIN Y, LIS, et al. A statistical investigation of parameters associated with low
人fetal fraction in non-invasive prenatal testing(J]. Journal of Matemal-Fetal & Neonatal
Medicine, 2024.
[7) GAUDET E. WUY HEETDERKS W. et al. Z-score-based posttest risk is a robust way
to report results of noninvasive prenatal screening|J]. American Journal of Obstetrics and
Gynecology. 2025.
[8] TANG Z, WANG S. LIX, et al. Longitudinal integrative cell-free dna analysis in gestational diabetes mellitus{J]. Cell Reports Medicine, 2024, 5(8):101660.
[9] 李 扬 , SBEH, 文晓 燕 , 等 . 产 前 血清 学 四 联 得 查 后 联合 NIPT 产 得 模式 在 胎儿 染色 体
筛 查 中 的 应 用 中.

蚌埠 医科 大 学 学 报 , 2024. 49(2):207-210.

[10] KIM S H. PARK D H, etal Clinical evaluation of noninvasive prenatal testing for sex
chromosome aneuploidies in 9,176 pregnant women: a single-center retrospective study
[7]. BMC Pregnancy and Childbirth, 2024, 24:6275.
ID] 刘 静 , S24%,
焦 红 燕 , 等 . 无 创 产 前 检测 在 双 胎 之 一 消失 孕妇 中 的 应 用 价值 吓 . 中 华 围

产 医学 杂志 , 2024, 27(4):278-284.
九 、 扫 使用 记录
未

使 用 ai 技术

24

<!-- source_page: 25 -->

附录 A

文件 列表

文件 名

功能 描述

qlpy
q2pPy
a3.py
q4py

间 题 一 程序代码
间 题 二 程序代码
间 题 三 程序
代码
问题
四 程序 代码

附录 B” 男 胎 孕 妇 关键 数据 展示
(GA)

为 把 握 变 量 关系 与 建 模 假设 的 合理 性 ， 我 们 对 “胎儿
Y 染色 体 浓度 (FF)
BMI GC 含量 “年龄 ”等 核心 要 素 进行 了 可 视 化 探索 。

”孕 周

主要 观察 与 结论
(1) FF 与 BMI 的 方向 性 关系 各 BMI 分 位 区 间 的 FF 分 布 整体 呈现 “ 峰 位 随 BMIAEATH
左 移 、 右 尾 被 抑制 ”的 规律
(2) FF 与 孕 周 的 关系 与 异 方差 随 GA 增加 ， 提 琴 图 的 中 位 线 与 高 密度 区 域 总体 上 移
G) FF 与 GC 含 莉 的 质量 属性 GC 含量 聚集 于 ~ 40% 左右 的 狭窄 带 ，FF 在 该 带 内 呈 数
布 状 且 未 出 现 显著 线性 趋势 .
建 模 含 义 与 实施 要 点
"变换
与 结构 : 对 0<FF<1 进行 logit 变换， 采用 “ 主 效应 (GA. BMI) 十 二 次 /交互
的 均值 方程 ; 个 体内 重复 观测 使 用 随机 截 距 /斜率 (MixedLM) 吸收
异 质 性。
* 单调
与 平滑 : 在 达标 概率 曲线 上 施加 单调 性 约束 《对 GA 为 非 减 、 对 BMI 为 非 增 ) ，
以 单调 样 条 / 贝 叶 斯 单调 回归 进行 平滑 ， 避 免 不 合 理 局 部 回 摆 。
© 蜡 方 差 /质量
控制 : 对 GC、 读 段 数 、 比 对 率 、 重 复 率 等 质量 变量 ， 通 过 稳健 标准 误
(HC 类 ) 或 加 权 最 小 二 乘 处 理; 必要 时 对 异常 批 次 分 层 或 吻 除 。
， 策略 输出 : 问题 二 在 BMI 轴 上 进行 K 段 台 阶 化 近似 ， 最 小 化 “达标 失败 风险 + 时
机 风险 ”; K 取 小 以 保证 可 执行 性 ， 冰 值 (如 4%6) 与 置信 水 平 在 稳健 性 中 做 灵敏 度
分析 。

25

<!-- source_page: 26 -->

[本页包含图像型或无法可靠文本化的内容，请参见原 PDF 第 26 页]

<!-- source_page: 27 -->

附录 C

交互

式 网 页 与 工程 实现 (展示 )

按 BMI 一 键 计算 最 佳 检测 孕 周
采用 皮 率 一 单 铅 一 SHCIRANER, ARBLGRIMONE, HEN
« 灵 教二油
节 。 设计 语言 采用 柔和 页 兰 请 色 系 与 靶 斑 和 志 ， 让 科学 决策 也 可 以 很 优 束 .

愉 个体 参数
anun

aoma

# BMI 一 推荐 孕 周 《台阶 化 )

—

Ls

—_—
ps
%
A
pa—
Pr
FT
22.0wm
区有
史记

»
|

|
二
分 姐 规 则 与 口径

23.3。

E|
=

oo ED

下

芝
2

E

a=本

二
=

bm 和 EDme

和

个
图 15

按 BMI 一 键 计算 最 佳 从 测 节 若 的 交互 式 网 页 截图

页 面 惑 合 “概率 一 单调 一 台阶 化 ”的 完 装 决 策 链 路: 左 侧 支持 身高 /体重 或 直接
BMI 输入 ， 右 便 实时绘制 BML- 推荐 孕 周 的 台阶 化 曲线 ; 提供 基线 (4=-0.95) 与 保守
(q=0.07) 策略 切换 、 检 测 噪 声 < 灵敏 度 调 节 ， 以 及 一 键 复制 与 导出 /打印 等 功能 。 该 实
现 展示 了 我 们 对 问题 机 理 的 深入 理解 与 可 视 化 落地 能 力 。 要 点 说 明 :
.方法
贯通 可 视 化 : 将 “最 时 达标
概 率 推 斯 一 单调 回归 平滑 一 分 段 台阶 化 (K=4)”
的 核心 流程 。 抽 象 为 面向 用 户 的 交互 控件 与 台阶 曲线 ， 便 于 临床 /决策 端 直观 理解 。
.稳健
性 开关 : 保守 口径 (4=0.97) 及 噪声
因子 < 采用 “统一 平移 不 改 月” 的 落地 规
则 ,方便 在 临床 安全 边界 内 快速 调 参 。
.工程
可 用 性 : 页 面 提供 结果 复制 、 打 印 /导出
与 一 键 截图 ， 便 于 报告 留 妆 与 院内 沟通 ;
界面 采用 柔和 莫 兰 迪 配色 与 我 璃 拟态 风格 ， 强 调 学 术 严 谦 与 审美 统一 。

27

<!-- source_page: 28 -->

附录 D

女 胎 部 分 异常 个 体 展示
表 9 阳性
个 体 清单

受 试 者 ID

旭 色 体

BI03
BOG2
B107

13
18
18

表 10
受 试 者 ID

命中 次 数 。 最强 |z| ”对 应 孕 周 (w)

2
2
2

401
465
390

196
133
150

9值 。则
值 (z'9)

0018
0001
0028

(26,005)
02.6,.003
(26,005)

可 疑 个 体 (各 染色
体 前 5 名 ， 按最 大 |:| 排序 )
刀 色 体

”最 大 |z| ”对 应 孕 周 (w)

4值

可 疑 原因

Bo62
Bl143
BOGS

13
13
3

841
487
414

133
230
249

0000
0.000
0.003

接近
风 值 / 单 次 命中
接近
风 值 / 单 次 命中
”接近
间 值 / 单 次 命中

B047

13

335

169

0080

“接近
网 值 / 单 次 命中

B141

13

319

250

0.059

“接近
内 值 / 单 次 命中

Bo42
B066
Bl103
BOI3
B133
Bl32

8
18
18
18
18
2

332
3.48
334
312
305
344

123
164
196
260
236
121

0.021 。 拷 近 风 值 / 单 次 命中
0048 接近
风 值 / 单 次 命中
0062 ”接近
则 值 / 单 次 命中
0184 接近
间 什 / 单 次 命中
0184
HiTM{EMAGD
0.087 接近
间 值 / 单 次 命中

BIN

21

319

244

0.224

接近
则 值 / 单 次 命中

B008

2

295

209

0.494

”接近
网 值 / 单 次 命中

BO4Y
BOST

2
2

292
272

166
126

0.494
0.413

EEM{IMKGS
接近
风 值 / 单 次 命中

附录 下 代码
ql.py
1
2

|#!/usr/bin/env

python3

3

|# -~*-

utf-8

coding:

-—x—
28

<!-- source_page: 29 -->

4 | sm
5 | 画 两 张 散点 图 :
6 |1) x=BMI，y=Y
染 色 体 浓度 (FF)
7 |2) x= 孕 周 (6A， 周 )，y=Y 染 色 体 浓度 (FF)

8 | 使用 : python plot_scatter_ff.py
o | om

(确保
间 目 录 有 “附件 .xlsx” )

10

11

|import re

12

|import

numpy

as

np

13

|import

pandas

as

pd

14 | import matplotlib.pyplot as plt
15 |from pathlib import Path
16 |plt.rcparams["font.sans-serif"] = ["SimHei"，"Microsoft Yahei"
, "Arial Unicode MS", "DejaVu Sans"]
17

|plt.rcParams["axes.unicode_minus"]

18
19
20
21
22
23

= False

|# ====== 参数 -=====
[INPUT_XLSX = "附件 .xlsx”
# 你 的 Excel XfF
|SHEET = 9
# 工作 才
|OUT_DIR = Path("")
|OUT_DIR.mkdir (parents=True, exist_ok=True)

24

25 |# -=====

工具 函数 ======

26 |def parse_ga(s):
27
""" 将 '13w+6'/"13W46'/'"I5+2"/"13w'
等 解析 为 周 的 浮 点 数 ; 失败
返回 NaN。""”

28

if pd.isna(s):

29

t = str(s).strip().lower()

30

t = (t.replace(”
+", "+")

31

32
33
34
35
36

return np.nan

<replace("f§",

"w")

.replace("
天
"，"+"))
if "w” in t:
# 形 如 13w 或 13w+6
a, b = t.split("w"，1)
try:
w = float(re.sub(r"[*\d\.\=]", "", a))
29

<!-- source_page: 30 -->

37

except:

38

w = np.nan

39
40

d = 6.9
if "+" in b:

41

try:

42
43
44
45
46
47

d = float(re.sub(r"[^\d\.\-]"，""，b.split("+"

[EYE5)))

except:
d = 6.9
return w + d/7.9
if "4" din t:
# 形 如 15+2
a, b = t.split("+", 1)

48

try:

49

return float(re-sub(r"[^\d\.\-]"，""， a)) + float(
re.sub(r"[*\d\.\=]", "", b))/7.@

50

except:

s1
52
53
54
55

return np.nan
try:

# 纯 数字
return float(re.sub(r"[^\dNA\-]
except:
return np.nan

"", t))

56

57

58

|def

fuzzy_pick_col(columns,

"EFAPRBER

keywords):

(BEXR)

， 返

回 第 一 个 匹配 列

None。"""
59

for

5

in

columns:

60

1c = str(c).lower()

61

for

62
63
64
65

kw in

keywords:

if kw in 1c:
return <
return None

66 |# -===== 谈 数 据 并 准备 列 =====67 |dfe = pd.read_excel (INPUT_XLSX, sheet_name=SHEET)
68

30

名 ， 和否则

<!-- source_page: 31 -->

69

|#

试

直接

用 中 文

列 名 ; 否则
做 模糊 匹配

70

|FF_col = "Y 染 色 体 浓度 " if "Y 染 色 体 浓度
fuzzy_pick_col(df@.columns,

71

|Hocol = "身高 "
评 “" 身 高"
fuzzy_pick_col(dfe.columns，["

72

|W_col

=“" 体 重 "

["y",

"in dfe.columns else

“ff",

"胎儿
分 "])

in dfe.columns else
身 高 ","height"])

if“ 体 重 "

in df8.columns

else

fuzzy_pick_col(dfe.columns，["
体 重 ","weight"])
73 |GA_col = "检测孕 周 ” if "检测
孕 周 "” in dfe.columns else
fuzzy_pick_col(df8.columns，["

孕

周 "，"gest"])

74

75 |missing = [name for name,col in [("Y 桨 色 体 浓度 ",FF_col)，("
身 高
”，H_col),("
体 重 ",W_col),(" 检 测 孕 周 ",GA_col)]
76

|if

77

if

col

is

None]

missing:

raise

ValueError(f" 以 下 必需 列 未 找到 : {missing}:

请 检查

Excel 7|%J2% f17: {dfe.columns.tolist()}")
78

79

|df = dfO[[FF_col, H_col, W_col, GA_col]).copy()

80 |df .columns

= ["FF","H","W","GA_txt"]

81

82

|# 百分数
转 比 例 ( 若 需 要 )

83

|if

84

df["FF"]

df["FF"]

.max()

>

1:

= df["FF"]

/ 100.0

85

86 |# 计算 BMI、 解 析 孕 周
87 |df["BMI"] = df["w"] / ( (df["H"]/188.8)#*2 )
88 |df["GA"] = df["GA_txt"].apply(parse_ga)
89

90

|# 清洗

91

|df = df:replace([np.inf,-np.inf]，np.nan).dropna(subset=["FF"，
"BMI"，"GA"])
92 |df = df[(dF["FF"]>=0) & (df["FF"]<=1)].copy()
93

94

|print(f"
有 效 样本 量 : N={len(df)}")

95

96

|# ======

图 1: x=BMI, y=FF ======

31

<!-- source_page: 32 -->

97
98
99

jplt.figure()
|plt.scatter(df["BMI"]，df["FF"]，s=18，alpha=9.6)
|plt.xlabel("BMI")

100

|plt.ylabel("Y
染 色 体 浓 度 (FF)

101

|plt.title("BMI vs FF ( 散 点 图 ) ")

102

|outl

= OUT_DIR

")

/ "scatter_bmi_vs_ff.png"

103 |plt.savefig(outl, dpi=180, bbox_inches="tight")
104 |p1t.show()
105
106 |# ====== 图 2: x=
孕 周 (GA) ，y=FF ======
107 |plt.figure()
108 |plt.scatter(df["GA"], df["FF"], s=18, alpha=0.6)
109

|plt.xlabel("
孕 周 ( 周 ) ")

110

|plt.ylabel("Y
染 色 体 浓 度 (FF) ")

111

|plt.title("
孕 周 vs

FF

( 散

点 图 ) ")

112 |out2 = OUT_DIR / "scatter_ga_vs_ff.png"
113 |plt.savefig(out2, dpi=180, bbox_inches="tight")
114 |plt.show()
115
116 |print("
导 出 : "，outl，out2)
q2py

1 |# -#- coding: utf-8 —x2 |
3W
(RER, SORFX
4 | 贝 叶 斯 单调曲线 + 可 选 分 和

+ RTFHM) :
+ 检测 误差 敏感 性

5

6 | 流程 :
7

|1) 读
取 数据 ? 拟 合 一 问 最 优 MixedLM
机 斜率 ,全 GA/BMI 二 次 项 )

(logit(FF), ， 随 机 截 距 + GA 随

8 |2) 计算 “最
早 达标 孕 周 ” T#(b): 满足 Pr(FF >= thr) >= q 的 最 时
t
9
10

- 口径 可 选 : typical ( 仅 残 差 方 差 ) / new ( 残 差 + 随机 效应 方
差)
|3) 用 贝 叶 斯 单调 模型 拟 合 Ta(b) 一 得 到 T_bayes(b); 若 PyMC 不 可

32

<!-- source_page: 33 -->

用 则 回 退 PAVA

11 |4)
12
13

【关键 】 保 守 纠

偏 : T_bayes(b) = max(T_bayes(b)，T#(b)) ， 保 证

回
验 不 低 于 9
|5) (可 选 ) 风险
最 优 台阶 化 为 K 段
|6) (可 选 ) 误差 敏感 性: 把 残 差 标 准

差 按 kappa

放缩

14
15 |powershell 一 行 示例 (与 第 三 问 保持 “typical” 口
径一 致) :
16 |python 2.py --data 附件 .xlsx --sheet 男 胎 检测 数据 --q 0.95 -thr 6.64 --tmin 10.0 --tmax 28.@ --bstep 6.1 --segment—k 4
--roundto

这

@.1

--lam-hi

6.38 --guarantee-mode

typical

|

18
19 |import argparse，os，re，warnings，math
20 |import numpy as np
21 |import pandas as pd
22 | import matplotlib.pyplot as plt
23 |from scipy.special import logit
24 |from scipy.stats import norm
25

|import

statsmodels.api

as

sm

26 |from statsmodels.regression.mixed_linear_model import MixedLM
27 |from sklearn.isotonic import IsotonicRegression
28
29

|warnings.filterwarnings("ignore",

30

|plt.rcParams["font.sans-serif"] = ["Microsoft YaHei”, "SimHei"
, "Arial"]
|plt.rcParams["axes.unicode_minus"] = False

31
32
33
34

|§ 一
一 一 27

35

|# 通用 工具

36 |# ---------------------------37 |def ensure_dir(d):
38
os.makedirs(d, exist_ok=True)
39
40

|def

parse_ga_to_week(x):

33

category=UserWarning)

<!-- source_page: 34 -->

41

if x is None or (isinstance(x, float) and np.isnan(x)):

42

return

np.nan

43
44
45

if isinstance(x, (int, float)):
return float(x)
s = str(x).strip().lower()

46

s = S.replace('
周

47

s = s.replace('
+', '+').replace('+',

'，'w').replace('
天

'，')

'+').replace(’

', '

=)

48

m = re.match(r'"\sx(\d+)\sxw\sx(2:\+\sx(\d+))
\sx$", s)

49

if

50
31
52

m:

w = int(m.group(1)); d = int(m.group(2) or @); return
w + d/7.9
m = re.match(r'~\sx(\d+)\sx\+\sx(\d+)\sx$', s)
if

53

m:

w = int(m.group(1)); d = int(m.group(2)); return w+ d
/7.@

54
55

m = re.match(r ~\sx(\d+)\sxw\sx(\d+)\sx$', s)
if mi:

56

w = int(m.group(1));

57
58
59

77.0
n = re.search(r'(\d+)"，5)
if m:
return float(m.group(1))

60

return

d = int(m.group(2));

return

np.nan

61

62 | def detect_id_column(df):
63
candidates = [
64

"1p","1d","id","PID","Pid","pid",

65

”孕妇 代码 "7"

66
]

68

for

69
7

体 "," 个

体 ID"，

“"subject”,"Subject","SUBJECT","patient”,"Patient"

67

70

孕 妇 ID"，" 个

c

in

candidates:

if c in df.columns:
return

c

df["_FAKE_ID_"] = np.arange(len(df))
34

w + d

<!-- source_page: 35 -->

72

return "_FAKE_ID_"

73

74
75
76

|def read_data(path, sheet_name=None):
if sheet_name is None or str(sheet_name).strip() == "":
xls = pd.ExcelFile(path)

77

sheet_name

78

df

79

print(f"[INF0]

=

-

x1s.sheet_names[@]

pd.read_excel(xls,

sheet_name=sheet_name)

未 指定 工作 表 ， 已 自动 读 取 : {sheet_name}”

)
80

else:

81
82

df = pd.read_excel(path, sheet_name=sheet_name)
print(f"[INF0] 已 读 取 工 作 表 : {sheet_name}")

83

84

df.columns = [str(c).strip() for c in df.columns]

85
86

#

87

ff_cols

FF

染色

88

=

体 浓

["FF","FF%","FF

度 "，"Y 浓 度 "，"Y

(%)

Refrik

","FF(X)","V¥

afkicE","yY

浓度 "]

89

ff_col = next((c for c in ff_cols if c in df.columns),
None)
if ff_col is None:

90
91

raise ValueError("
缺 少 FF (或 Yifefsikik/&)
列 ")
df["FF"] = pd.to_numeric(df[ff_col], errors="coerce")

22
93

if df["FF"].dropna().gt(1.0).mean()
df["FF"] = df["FF"]/100.0

> 0.5:

94
95

#

GA

96

ga_cols

97

ga_col = next((c for c in ga_cols if c in df.columns),

= [【"GA"，" 检 测

孕 周 "，"

孕 周 "，" 孕

周 数 "，" 孕

None)

98

if ga_col is None:

99

100

raise

ValueError("

狭

少

GA/

101

102

孚

周

列

")

df["GA"] = df[ga_col].apply(parse_ga_to_week)
# BMI

(或 身高 体重 )

35

周 ( 周 )"]

<!-- source_page: 36 -->

103
104

bmi_cols = ["BMI","
体 质 指数 ","bmi"]
bmi_col = next((c for c in bmi_cols if c in df.columns),
None)

105

if bmi_col

106

is not None:

df["BMI"] = pd.to_numeric(df[bmi_col], errors="coerce"
)

107

else:

108
109

if 〈" 身 高 "in df.columns) and (" 体 重 " in df.columns):
h_m = pd.to_numeric(df["
身 高
"]，errors="coerce")
/100.0

110

w_kg

1

df["BMI"] = w_kg/(h_m+#2)

112

= pd.to_numeric(df["
体 重

"]，errors="coerce")

else:

113
114

raise ValueError("
缺 少 BMI 或 身高 /体重 ")
df = df.replace([np.inf,-np.inf]，np.nan).dropna(subset=["
FF","GA","BMI"])

ns
116

df = df[(df["FF"]>9) & (dF["FF"]<1)]
print(f"[INFO] N={len(df)}; FFE({df.FF.min():.4F},{df.FF.
max():.4}); GAS[{df.GA.min():.2F},{dF.GA.nax():.2F}]; BMI
E[{df.BMI.min():.2f}, {dF.BMI.max():.2F}]")

117

return

df

118

119
120

|# ----------------------------

121

|#

122

|8# 一
一一

123
124
125
126

|def fit_mixedlm_best(df，id_col):
d = df.copy()
d["GA_c"] = df"GA"] - d["GA"].mean()
d["BMI_c"] = d["BMI"] - d["BMI"].mean()

一 问

最 优 MixedLM

(logit

基 网 ，含

二 次

项 ，GA

随机 斜率 )

127

# logit(FF)

128

y = np.log(d["FF"].clip(1le-6, 1-1e-6) / (1 - d["FF"].clip
(1e-6, 1-1e-6)))

129
130

X = sm.add_constant(pd.DataFrame({
"GA_c": d["GA_c"],

36

<!-- source_page: 37 -->

131
132
133

"GA_c2": d["GA_c"]x%2,
"BMI_c": d["BMI_c"],
"BMI_c2":d["BMI_c"Jxx2,

134

m

135
136

Z = sm.add_constant(d[["GA_c"]], has_constant="add")
print("[INFO] filfr MixedLM (BiHLAFE + GA 随机 斜率 +

二 次

项 ) .……”")

137
138
139

model = MixedLM(endog=y, exog=X, groups=d[id_col], exog_re
=2)
res = model.fit(method="1bfgs", reml=False, maxiter=1000,
disp=False)
print(res.sunmary())

140

return

res,

d

141

142
143 | 等 :一

144

|# 从

MixedLM

计算

Pr(FF>=thr)

与

Tk(b)

145 |# ---------------------------146 |def eta_fix_from_b_t(res, GA_mean, BMI_mean, t_week, b_bmi):
147

b = res.fe_params

148
149
150
151

ga_c = t_week - GA_mean
bmi_c = b_bmi - BMI_mean
* 二 次 项
return float(b["const"] + b["GA_c"]xga_c + b["GA_c2"Jx(

ga_cxx2) +
152

bf[f"BMI_c"]*bmi_c + b["BMI_c2"]x(bmi_cx%2)),
ga_c

153
154

|def eta_sd(res,

ga_c,

mode="new"):

155

"""1logit(FF)

156

vse=

157
158
159

if mode == "new":
cov_re = np.asarray(res.cov_re) # 2x2: [const, GA_c]
vec = np.array([1.0, ga_c], float)

的 标准

float(res.scale)

差 ; typical=
仅 残 差 ; new= 随 机 效应 + 残 差 。
#

REHE

37

<!-- source_page: 38 -->

160
161

v += float(vec @ cov_re @ vec)
return math.sqrt(max(v, le-12))

162

163
164
165
166
167

|def prob_ge_threshold(res, GA_mean, BMI_mean, t_week, b_bmi,
thr=0.04, mode="new"):
eta_fix, ga_c = eta_fix_from_b_t(res, GA_mean, BMI_mean,
t_week, b_bmi)
sd = eta_sd(res, ga_c, mode=mode)
z = (eta_fix - logit(thr)) / sd
return float(norm.cdf(z))

168

169 |def tstar_for_bmi(prob_fn，b_bmi，q=9.95，t_min=19.9，t_max
=28.0, step=0.1):
170
grid = np.arange(t_min, t_max + le-9, step)
171
probs = [prob_fn(t, b_bmi) for t in grid]
172
idx = next((i for i, p in enumerate(probs) if p >= 9)，
None)
173
if idx is None:
174
return float(t_max)，False
175
lo = max(t_min, grid[max(e, idx-2)])
176
hi = grid[idx]
177
for _ in range(25):
178
mid = 0.5x(lo+hi)
179
if prob_fn(mid，b_bmi) >= q:
180
hi = mid
181

182
183

else:

lo = mid
return float(hi), True

184
185
186

|§ wemmemmmfemei

po———

187

|# A 方案 :

183

|§ ~mmmme—————————

贝 叶 斯 单调拟 合 〈 若 无 PyMC

自动

回 退 PAVA)

189 |def bayes_monotone_curve(b_grid, T_star, method="vi", draws
=1500, seed=2025):
38

<!-- source_page: 39 -->

190
191 |

_e
返回 : T_mean,

192

-

193

值
与 95X%CI
- 车 未 安装 /失败 :

回 退 到 PAVA ( 仅 点 估计 )

194

=-

下 都 做 保守 纠偏 : T_mean

195

T_star)
“he

196
197

b = np.asarray(b_grid,
y = np.asarray(T_star,

198

assert

199
200
201
202
203
204
205

著

T_lo,

安装 了 PyMC:

【关键 】 两

种 情况

len(b)

T_hi
用 “ 非 负 增 量 的

==

累积 和 ”保证

严格

单调 ， 取 均

= max(T_mean,

float).ravel()
float).ravel()

len(y)

try:

206

import
import
# 兼容
try:
sp

= pm.math.softplus

except

Exception:

207
208

pymc as pm
pytensor.tensor as pt
softplus

try:
from pytensor.tensor.nnet

import softplus as

sp
209

except

210

Exception:

sp = pm.math.loglpexp

211
212

#

213

db = np.diff(b，prepend=b[9])

214
215

if np.any(db <= @):
uniq = np.unique(b)

216

等 距 尺 度 “( 避 免 8 步 长 )

minstep = np.min(np.diff(uniq))

if len(unig)

> 1

else 1.0
217
218
219
220

db = np.where(db <= @, minstep, db).astype(float)
with pm.Model() as m:
sigma = pm.HalfNormal("sigma",
39

@.3)

<!-- source_page: 40 -->

221

mu@

= pm.Normal("mu9"，mu=float(np.percentile(y

,19))，sigma=2.9)
222

s

= pm.HalfNormal("scale_inc",

223

z

= pm.Normal("z", mu=0.8, sigma=1.0, shape=

sigma=0.5)

inc

= pm.Deterministic("inc"，sp(z) % s % db)

len(b))
224
非
负 增 量

225

theta = pm.Deterministic("theta”, mu@ + pt.cumsum(
inc))

226

pm.Normal("y_obs", mu=theta,

sigma=sigma, observed

=y)
227

228
229
230
231
232
233
234

if method.lower() == "nuts":
idata = pm.sample(draws, tune=draws, chains=4,
target_accept=0.9,
random_seed=seed, progressbar=True)
else:
approx = pm.fit(10000, method="advi",
random_seed=seed,
callbacks=[pm.callbacks.
CheckParametersConvergence (tolerance=1e-3)])
idata = approx.sample(draws, random_seed=seed
)

235
236

theta_post = idata.posterior["theta"].stack(s=("chain"
,"draw")).values

# (n,

S)

237
238

T_mean = theta_post.mean(axis=1)
# 保守 纠偏

239

T_mean

= np.maximum(T_mean,

T_star)

240

241
242
243
244
245

lo = np.percentile(theta_post, 2.5, axis=1)
hi = np.percentile(theta_post, 97.5, axis=1)
return T_mean, lo, hi
except

Exception

as

e:

40

#

<!-- source_page: 41 -->

246 |

print(F"[WARN] PyMC

不 可 用 或 推断

失败 ， 回 退 到 PAVA: {e}

ho

247
248

ir = IsotonicRegression(increasing=True,
="clip")
T_hat = ir.fit_transform(b, y)

249

#

250
251
252

T_hat = np.maximum(T_hat, T_star)
return T_hat, None, None

out_of_bounds

保守 纠 侠 (关键 ! )

253

254 |# ------------

255
256
257
258
259

分 段 : 风险

感知

的

最 优 台 阶 化 (可
选 后 处 理)

|def phi_time(t, alpha=0.02, beta=0.12):
"""
时 间 惩 罚 : <=12
无 惩罚 ; 12-28 线 性 ; >=28
斜 率 更 大 """
if t <= 12.9: return 9.9
if t < 28.0: return alphax(t-12.0)
return alphax(28.0-12.8) + betax(t-28.9)

260

261
262
263
264

|def t_key_index(t, round_to):
return int(round(float(t) / float(round_to)))
|def _prob_vec_at_t(res, GA_mean, BMI_mean, b_grid, t, thr
=0.04,

265

kappa=1.0,

mode="new"):

"""
同 一 时 点 t 上 ， 对 一 惠 _BMI 计算
否 计 入 随机

效应

p(FF>=thr). mode 控制 是

。""”

266

b = res.fe_params

267
268
269

ga_c = float(t - GA_mean)
bmi_c_vec = b_grid - float(BMI_mean)
eta_fix = (float(b["const"]) + float(b["GA_c"])xga_c +
float(b["6GA_c2"])x(ga_cx%2)

270

+ float(b["BMI_c"])xbmi_c_vec + float(b["BMI_c2
"1)%(bmi_c_vecxx2))

271
m
273

sd = eta_sd(res, ga_c, mode=mode) % float(kappa)
z = (eta_fix - float(logit(thr))) / sd
return norm.cdf(z).astype(float)
41

<!-- source_page: 42 -->

274
275
276

|def

precompute_prob_prefix_from_curve(res, GA_mean, BMI_mean,
b_grid, T_curve,

277

thr=0.04, round_to=0.1,
kappa=1.0, mode="new"):

278

本

279

用

280

T_curve(b) 的 唯一 四 舍 五 人 时 点 作为 候选 台阶 时 点 ， 预 计算 所
有 候选 t 的
p(t, b) 前缀 和 : k -> 累积
和 数组 ， 便 于 0(1) 取 任 意 连 续 BMI
子 段 的 概率和 。

281

282
283
284
285
286
287

t_candidates = np.round(np.asarray(T_curve, float) /
round_to) x round_to
t_vals = np.unique(t_candidates)
p_prefix = {}
for t in t_vals:
p_vec = _prob_vec_at_t(res, GA_mean, BMI_mean, b_grid,
t, thr=thr, kappa=kappa, mode=mode)
pref = np.zeros(len(b_grid)+1, dtype=float)

288

pref[1:]

289

p_prefix[t_key_index(t, round_to)] = pref

290

return

t_vals,

= np.cumsum(p_vec)
p_prefix

291
292 |def dp_segment_bmi_fast(b_arr, T_curve, p_prefix,
293
1lam=0.61, round_to=e.1,
294
w_fail=1.0, alpha=0.02, beta=0.12):
295
ee
296
297
298

fERPMl T_curve(b) 上 做 最 优 台阶 化 每段 时 点 t 取 遍 段 T_curve 的 “中 位 数 ” 并 按 round_to 对 齐 到
最
近 候 选 键 (p_prefix 的 key) .
目标 : 二 {段 } [Z_{bE段 } (w_fail#(1-p(t,b)) + phi_time(t))]
+ lam % (#segments)

299

0

300

n = len(b_arr)

301

T = np.asarray(T_curve, float)
42

<!-- source_page: 43 -->

302

keys = list(p_prefix.keys())

303

304

# 预先
算 每 个 子 段 [i:j]
键)

305
306
307
308
309

best_t = np.full((n, n), np.nan, float)
for i in range(n):
for j in range(i, n):
t_med = float(np.median(T[i:j+1]))
kk = t_key_index(t_med, round_to)
not

in

的 推荐 时 点 (中 位 数 “" 对 齐 到 最 近 候 选

310

if kk

p_prefix:

311
312

kk = min(keys，key=lanbda k: abs(k-kk))
best_t[i, j] = round(kksround_to, 10)

313

314

#

315
316
317
318
319

€ = np.full(n+1, np.inf)
prev = np.full(n+1, -1, int)
Cc[6] - 9.9
for j in range(1, n+1):
best_val = np.inf; best_i = -1

320

动态 规划

i in

range(@,

321

for

t_rec

= best_t[i,

322
323

k = t_key_index(t_rec, round_to)
pref = p_prefix.get(k)

324

if pref is None:

325
326
327

328

j):

j-1]

k = min(keys, key=lambda kk: abs(kk-k))
pref = p_prefix[k]
L=3j-i

sum_p = pref[j] - pref[i]

# 段 内 p

的 和 (o(1))

329
330
331
332
333

cost_seg = w_failx(L - sum_p) + Lyphi_time(t_rec，
alpha=alpha, beta=beta)
cost = C[i] + cost_seg + lam
if cost < best_val:
best_val = cost; best_i = i
c[j] = best_val; prev[j] = best_i
43

<!-- source_page: 44 -->

334
335

# 回溯

336

segs

337

cur

338
339
340
341

while cur 》9:
i = prev[cur]i j = cur-1
segs.append((i，j，float(best_t[i，j])))
cur = i

342

segs.reverse()

343

return

= []
=

n

segs

344

345 |def find_lambda_for_k(b_grid, T_curve, p_prefix, target_k=5,
346
lam_10=0.6, lam_hi=0.05, tol-le-4,
347
round_to=0.1, w_fail=1.0, alpha=0.02,
beta=0.12, max_iter=25):
348
"""
二 分 搜索 入 ， 使 分 段 数 尽 量 接近 target_k (支持 “4 或 5) 。
349

best

350
351
352

for _ in range(max_iter):
lam_mid = 8.5#*(lam_lo+lam_hi)
segs = dp_segment_bmi_fast(b_grid, T_curve, p_prefix,

=

None

353

lam=1am_mid,

round_to=

round_to,
354

w_fail=w_fail, alpha=alpha,
beta=beta)

355

k = len(segs)

356

if best is None or abs(k-target_k) < abs(len(best[1])target_k):

357

358

best

= (lam_mid,

if k > target_k:

359

lamn_lo = lam_mid

360
361
362

elif k < target_k:
lam_hi = lam_mid
else:

363

segs)

return

lam_mid,

# 段 太 乡 -惩罚
伪 小 -加 大 入
#

段 太 少-息 罚 俩 大一 减小 入

segs

44

<!-- source_page: 45 -->

364

if lam_hi - lam_lo < tol:

365

break

366

return

best

# 返回

“最 接近 ”的

方案

367
368 |def export_segments_bayes(outdir, b_grid, T_curve, segments,
prob_fn_at,

369

alpha=0.02, beta=0.12, fname_csv="
bmi_segments_bayes.csv",

370

|

fname_fig="fig_t_bayes_segments.png"

):
371

""" 导 出 分 段 表 与

372

os.makedirs(outdir

登 加 图 。""”

exist_ok=True)

373

rows

374
375
376
377
378

for (i, j, t_rec) in segments:
bmin, bmax = float(b_grid[i]), float(b_grid[j])
b_list = b_grid[i:j+1]
probs = [prob_fn_at(t_rec, b) for b in b_list]
risk_mean = float(np.mean([(1-p) + phi_time(t_rec,

= []

alpha=alpha,

379

beta=beta)

for

p in probs]))

rows .append ({

380
381
382
383
384
385

“BMI_min": round(bmin, 2),
“BMI_max": round(bmax, 2),
“t_recommend_week": round(float(t_rec), 2),
"p_ge_thr_mean": round(float(np.mean(probs)), 4),
"risk_mean": round(risk_mean, 4),
“n_grid": int(len(b_list))，

386

H

387

seg_df

388

seg_path

= pd.DataFrame(rows)

389
390

seg_df.to_csv(seg_path, index=False, encoding="utf-8-sig")
print(f"[OK] 已 导出 分 段 表 : (seg_path}")

= os.path.join(outdir,

fname_csv)

391

392

# &inE

393
394

fig, ax = plt.subplots(figsize=(8.6,5.2))
ax.plot(b_grid，T_curve，1lw=2.2，1label-"
单 调 推荐 曲线 $T_
45

<!-- source_page: 46 -->

|

{NNrm Bayes}(b)$")

395

for

396

ax.hlines(y=t_rec，xmin=b_grid[i]，xmax=b_grid[j]，
linewidth=3, alpha=e.85)
ax.vlines(x=b_grid[j], ymin=min(T_curve[i:j+1]), ymax=
max(T_curve[i:j+1]),
linestyles="dotted", alpha=0.35)
ax.set_xlabel("BMI")
ax.set_ylabel("
推 荐 孕 周 ( 周) ")
ax.set_title("BMI推 荐 检测 孕 周 : 单调 曲线 + 风险
最 优 台阶 化

397
398
399
400
401

(i,

j,

t_rec)

in

segments:

分 段 ")

402
403
404
405
406

ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig_path = os.path.join(outdir, fname_fig)
fig.savefig(fig_path, dpi=180)

407

print(f"[OK]

已 导出
倒 加 图 : {fig_pathj")

408

409

410 |# ========= 曲线
后 处 理 : 推荐 查询 / BR / 分 位 点 标注 =========
411

|def postprocess_and_export(res, GA_mean, BMI_mean,

412

curve_csv="out_qg2_bayes/

t_bayes_curve.csv",
413
414

outdir="out_q2_bayes",
thr=0.04, q_target=0.95,

415

416
417
418
419
420
421
422

guarantee_mode="new"):

os.makedirs (outdir, exist_ok=True)
tbl = pd.read_csv(curve_csv)
if mot {"BMI","T_bayes_mean"}.issubset(tbl.columns):
raise RuntimeError(f"[ERROR] {curve_csv} 缺少 必须 列
BMI/T_bayes_nean")
b_grid = tb1["BMI"].to_numpy(dtype=Ffloat)
t_mean = tbl["T_bayes_mean"].to_numpy(dtype=float)
t_lo = tbl["T_bayes_lo"].to_numpy(dtype=float) if "
T_bayes_lo"

in tbl.columns

else

46

np.full_like(t_mean,

np.nan)

<!-- source_page: 47 -->

43 |

t_hi = tbl["T_bayes_hi"].to_numpy(dtype=float)
T_bayes_hi"

in

tbl.columns

else

if "

np.full_like(t_mean,

np.nan)

424

425

# 即时 查询 ;: 线性 插值

426
427
428

def recommend_week (bmi):
b = float(np.clip(bmi, b_grid.min(), b_grid.max()))
return float(np.round(np.interp(b, b_grid, t_mean), 1)
)

429
430
431

print("\n[RECOMMEND] 示例 : ")
for bmi_test in [25，38，32，35，46，45]:
print(f"

bmi_test):.1f}

BMI={bmi_test:>4}:

推荐

{recommend_week(

周 ")

432

433
434
435
436
437
438
439
440
441
442
443
444
445

# 回 验 : 按 口径 计算 Pr(FF>=thr) @ 推荐 点
def prob_ge_thr_at(t_week, b_bmi):
be = float(res.fe_params["const"])
bl = float(res.fe_params["GA_c"])
blq= float(res.fe_params["GA_c2"])
b2 = float(res.fe_params["BMI_c"])
b2q= float(res.fe_params["8MI_c2"])
ga_c = float(t_week - GA_mean)
bmi_c = float(b_bmi - BMI_mean)
eta_fix = b8 + blxga_c + blgx(ga_cxx2) + b2xbmi_c +
b2q*(bmi_c##2)
sd = eta_sd(res，Bga_c，mode=guarantee_mode)
z - (eta_fix - float(logit(thr))) / sd
return_ float(norm.cdf(z))

446

447
448
449
450 |

probs = [prob_ge_thr_at(t, b) for t, b in zip(t_mean,
b_grid)]
chk = pd.DataFrame({"BMI": b_grid，"T_recommend": t_mean,
"P_ge_thr": probs})
chk_path = os.path.join(outdir，"guarantee_check_on_curve.
csv")
chk.to_csv(chk_path, index=False, encoding="utf-8-sig")
47

<!-- source_page: 48 -->

451 |

print(f"\n[CHECK] 推荐 曲线 处 保障 率 : min={np.min(probs):.3f
}, median={np.median(probs):.3f} | 已 导出 《chk_path}")

452
453
454
455

# 分 位 点 蕉 荐 表
qs = [0.10, 0.25, 0.50, 0.75,
b_q = np.quantile(b_grid, gs)

456
457
458
459

rows = []
for q, b in zip(qs, b_q):
t = float(np.interp(b, b_grid, t_mean))
lo = float(np.interp(b, b_grid, t_lo)) if np.isfinite(
t_lo).any() else np.nan
hi = float(np.interp(b, b_grid, t_hi)) if np.isfinite(

460

t_hi).any()

461
462

else

©.90]

np.nan

rows
. append ({
"quantile": g, "BMI": round(float(b), 2),

463

464

"T_recommend_week":

round(t,

2),

"T_lo": round(lo，2)

if np.isfinite(lo) else np.

nan,
465

"T_hi": round(hi, 2) if np.isfinite(hi) else np.
nan

466

})

467

468

dfq

=

pd.DataFrame

(rows)

469

q_path = os.path.join(outdir, "recommend_by_bmi_guantiles.
csv")
dfq.to_csv(q_path，index=False，encoding="utf-8-sig")

470

print(f"[OK]

分 位 点 推荐 表 已 导出 : {a_path}")

471

472

# 标注 图

473
474

fig, ax = plt.subplots(figsize=(8.2, 5.2))
if np.isfinite(t_lo).any() and np.isfinite(t_hi).any():

475

476
47|

ax.fill_between(b_grid,

t_lo,

t_hi,

alpha=e.18,

linewidth=0, label="95%[X
[i")
ax.plot(b_grid, t_mean, lw=2.4, label=r"$T_{\rm Bayes}(b)$
人

for q bin zip(as, b_a):
48

<!-- source_page: 49 -->

478
479
480
481

t = np.interp(b, b_grid, t_mean)
ax.axvline(b, color="gray", 1s=":", lw=1.0, alpha=0.6)
ax.plot([b]，[t]，"o"，ms=5)
ax.text(b，t，f”{int(q#199)}%"，va="bottom"，fontsize

482

=19)
ax.set_xlabel("BMI")

483
484

ax.set_ylabel("
推 荐 孕 周 ( 周 ) ")
ax.set_title("sMI
一 推荐 检测 孕 周 ( 贝 叶 斯

485
486
487
488
489

ax.grid(True, alpha=e.3)
ax.legend()
fig.tight_layout()
fig_path = os.path.join(outdir, "fig_t_bayes_curve_marked.
png")
fig.savefig(fig_path, dpi=180)

490

print(f"[OK]

标注

单调 曲线 ) )

图 已 导出 : {fig_path}")

491

492

return recommend_week

493

494

495

|# ====

误差

496

|def prob_ge_threshold_scaled(res, GA_mean, BMI_mean, t_week,
b_bmi,

497

敏感

性: B

thr=0.04,

RWRE"

kappa=1.0,

EHRET

""" 与 prob_ge_threshold

类 似 ;但
效应

498

b = res.fe_params

499

Ba_c

= t_week - GA_mean

500

bmi_c

= b_bmi

501

eta

= (b["const"]

kappa^2

mode="new"):

缩 ; mode

控制 是 否 计 和 人 随机

LHMMHE

把 残 差 方差 按 kappa~2 放

，"""

~- BMI_mean
+ b["GA_c"]xga_c

+ b["GA_c2"]x(ga_c

*%2)

502
503
504
505
506

+ b["BMI_c"]#bmi_c + b["BMI_c2"]x(bmi_cxx2))
v = float(res.scale) x (float(kappa)xx2)
if mode == "new":
vec = np.array([1.0, ga_c], float)
v

+= float(vec

@ np.asarray(res.cov_re)

49

@ vec)

<!-- source_page: 50 -->

507
508
509

sd = math.sgrt(max(v, le-12))
z
= (eta - float(logit(thr))) / sd
return float(norm.cdf(z))

510

S11

|def compute_T_star_grid(prob_fn,
t_max=28.0, step=0.1):

b_grid, g=0.95, t_min=10.0,

""" 在 BMI 网 格 上 掀 量 算 Ty(b)

与 是 否 可 达标 ; prob_fn(t_vec，

512
b)

需

支持
向 量化 t"”"

513

T_star,

514
515
516
517

for b in b_grid:
grid = np.arange(t_min, t_max + le-9，step)
probs = prob_fn(grid，float(b))
idx = next((i for i, p in enumerate(probs) if p >= q)
»

reach

=

[],

[]

None)

518
519

if idx is None:
T_star.append(float(t_max));

520

else:

s21

reach.append(False)

lo = max(t_min, grid[max(®, idx-2)]); hi = grid[
idx]

522

523
524
525
326
327
528
529

for _ in

range(25):

mid = 0.5x(lo+hi)
if prob_fn(np.array([mid]), float(b))[0] >= q:
hi = mid
else:
lo = mid
T_star.append(float(hi)); reach.append(True)
return np.array(T_star, float), np.array(reach, bool)

530
531

532
533
534
535
536

|# ---------------------------|# 主流 程
|# ---------------------------|def main():
parser = argparse.Argumentparser(description="
第 二 问: 贝叶
斯 单调

曲线

+

可 选

分段 +

误差

敏感 性 ")

50

<!-- source_page: 51 -->

5337 |

。 parser.add_argument("--data"，type=str，default="
附 件 .xlsx
中

538
539

parser.add_argument("--sheet"，type=str，default=None)
parser.add_argument("--idcol”, type=str, default=None)

540

541

parser.add_argument("--q",

type=float,

default=0.95,

help=

"保证
通过 率 阔 值 ")

542

parser.add_argument("--thr", type=float, default=0.04,
help="ik#R
(if (FF 比例 ) ")

543

parser.add_argument("--tmin",

544
545
546
547
548
549
550

parser.add_argument("--tmax"，type=float，default=28.9)
parser.add_argument("--bmin"，type=float，default=None)
parser.add_argument("--bmax"，type=float，default=None)
parser.add_argument("--bstep”, type=float, default=e.1)

551

type=float,

default=10.0)

# 贝 叶 斯 相关
parser.add_argument("--method”, type=str, default="vi",
choices=["vi","nuts"], help="PyMC 推 斯 方式")
parser.add_argument("--draws"，type=int，default=1599，
help="
后 验 抽样 规模 ")

552
553

#

554

parser.add_argument("--segment-k", type=int, default=e,

可 选 分 段

help=">0

555

WIZHMMX&MLH

help="
分 段 时 段 内 在

556

段 (如

4 或

5)")

的 四 含 五 人 精度 ")

parser.add_argument("--lam-hi", type=float, default=e.es,
help=
"二 分 搜索 的 上 界 (

557

K

parser.add_argument("--roundto”, type=float, default=0.1,

越 大 段 越 少 ) ")

parser.add_argument("--wfail"，type=float，default=1.9，
help="
失 败 惩 罚 权 重 w_fail")

558

parser.add_argument("--alpha”, type=float, default=e.62,
help="12-28
i 4 Jif if [a] 4& $i")

559

parser.add_argument("--beta”, type=float, default=0.12,

help=">=28
周 每 周 时 间 惩 罚 ")
560

51

<!-- source_page: 52 -->

561

#

562

误差

敏感 性

parser.add_argument('--err-eval',

help= "是 否 做 检测

563

误差 敏感

parser.add_argument('--sigma-grid’,
0.75,1.00,1.25,1.50,2.00",

s64 |

action='store_true',

性 分 析 (BRK/RMARENE)

help="sd

fii%

*)

types=str, default="
kappa

列表 ， 逗 号

分 隔， 如

0.85,1.0,1.15")
565
566

#

567

parser.add_argument ("--guarantee-mode",

568 |

,"new"], default="typical®,
help="typical=
群 体 平均 个 体 ; new=
新 受检
者

569
570
571
572
3573
574
575
576
577
578
579

(更

口径 : typical

( 仅

残 差 ) / new ( 残 差 +

随机 效应 )

choices=["typical"

保守 ) ")

args = parser.parse_args()
outdir = "out_q2_bayes"
ensure_dir(outdir)
# 1) 数据 & ID
df = read_data(args.data, sheet_name=args.sheet)
id_col = args.idcol or detect_id_column(df)
print(f"[INFO] 使 用 个 体 ID 列 : {id_col}")
# 2) MixedLM (与 一 问 最 项 一 致 * logit + GA/BMI
距

580
s81

保证

+ GA

随机

—iK. BIHL#

斜率 )

res, d2 = fit_mixedlm_best(df, id_col=id_col)
GA_mean, BMI_mean = float(d2["GA"].mean()), float(d2["BMI"

] .mean())
582

583
584
585
586

# 3) 概率 函数 ( 按 口 径 )
def prob_fn_scalar(t, b):
return prob_ge_threshold(res, GA_mean, BMI_mean,
t_week=t, b_bmi=b, thr=args.
thr,

587

mode=args.guarantee_mode)

52

<!-- source_page: 53 -->

588

589

590
591 |
592

# 4) BMI

网

格 与 T#(b)

bmin = args.bmin if args.bmin is not None else float(d2["
BMI"] .min())
。 bmax = args.bmax if args.bmax is not None else float(d2["
BMI"] .max())
b_grid = np.round(np.arange(bmin, bmax + le-9, args.bstep)
，3)

593
594

T_star = []

595

reach

596
597

599

for b in b_grid:
tstar, ok = tstar_for_bmi(prob_fn_scalar, b_bmi=float(
b), g=args.q,
t_min=args.tmin, t_max=args.
tmax, step=e.1)
T_star.append(tstar); reach.append(ok)

600

T_star

= np.array(T_star,

602

## 5)

贝 叶 斯

603

print("[INFO]

598

= []

float)

601

604

单调
曲线 (无
须 强制 分 段 )
拟 合 贝 叶 斯

单 油 曲 线 ' 《不

可 用 则回 退 PAVA)

...")

T_mean, T_lo, T_hi = bayes_monotone_curve(b_grid, T_star,
method=args.method, draws=args.draws, seed=2025)

605

606

# 6)

导出
与 作 图

607

out_csv

608

df_out = pd.DataFrame({

= os.path.join(outdir,

"t_bayes_curve.csv")

609

"BMI":

610

SStSPe

b_grid,

611

"T_bayes_mean":

612
613
614
615
616

"T_bayes_lo": T_lo if T_lo is not None else np.nan,
"T_bayes_hi": T_hi if T_hi is not None else np.nan,
"reachable": reach,

Star
T_mean,

H
df _out.to_csv(out_csv, index=False, encoding="utf-8-sig")
53

<!-- source_page: 54 -->

617

print(f"[OK]

已 导出 : fout_csvj")

618

619
620

fig, ax = plt.subplots(figsize=(8.6,5.2))
ax.scatter(b_grid, T_star, s=10, alpha=0.35, label=r"$T_\
star(b)$

621

|

(最
早 达标 ) ")

ax.plot(b_grid,

(REFa,

622
623

T_mean,

SRFAM)

lw=2.5,

label=r"$T_{\rm

Bayes}(b)$

")

624

if T_lo is not None and T_hi is not None:
ax.fill_between(b_grid, T_lo, T_hi, alpha=0.18,
1linewidth=9，1label="95%
置 信 带 ")
ax.set_xlabel("BMI")

625

ax.set_ylabel("
孕 周 (

626

周 ) ")

ax.set_title("
基 于 一 问 MixedLM

的 推荐 检测 时 点 :_ 贝 叶 斯 单调

曲线 ")

627
628
629
630
631
632
633

ax.grid(True, alpha=e.3)
ax.legend()
fig.tight_layout()
out_fig = os.path.join(outdir, "fig_t_bayes_curve.png")
fig.savefig(out_fig，dpi=186)
print(f"[OKk] 已 导出 : {out_figj")

634

# 7)

635

rec_fn = postprocess_and_export(

回验 、分 位 点 表 、 标 注
GA_mean,

图 ， 并 返回

查询

636

res,

637

curve_csv=out_csv, outdir=outdir,

638

thr=args.thr,

639

guarantee_mode=args. guarantee_mode

函数

BMI_mean,
g_target=args.q,

640

)

641

print("\n[QUERY] BMI=33

的

推荐 孕 周 : ", rec_fn(33.0),

"M")

642

643

# ======

644
645

if args.segment_k and args.segment_k 》9:
print(f"\n[SEGMENT] 目标
分 段 数 K = {args.segment_k}")

646

订 选 : 对 单调
推荐 曲线 做 K

# 预计
算 前 绷 概 率 (候选

段 台 阶 化 (风险
最 优)

+ 来 自 T_bayes_mean

54

的

唯一 值 ;

<!-- source_page: 55 -->

|

kappa=1)

647

_»

p_prefix

= precompute_prob_prefix_from_curve(

648

res,

649
650

b_grid=b_grid, T_curve=T_mean,
thr=args.thr, round_to=args.roundto,

651

mode=args.guarantee_mode

652
653
654

GA_mean,

BMI_mean,

)
# 给 定 K， 用 二 分 搜索 入 找到
最 接近 K
lam_star, segs = find_lambda_for_k(
p_prefix,

段 的 方案

655

b_grid,

656
657

1am_10=0.0, lam_hi=args.lam_hi, tol=le-4,
round_to=args.roundto, w_fail=args.wfail,

658

T_mean,

kappa=1.0,

alpha=args.alpha,

659
660

target_k=args.segment_k,

beta=args.beta,

)
print (£"[SEGMENT] A={lam_star:.5f},

max_iter=3@

##%| {len(segs)}

B:")

661
662

for idx, (i, j, t_rec)
print(f"
组 fidx}:
1:.2F}] 一 推荐

{t_rec:.2f}

in enumerate(segs, 1):
BMIE[{b_grid[i]:.2f}, {b_grid[j
JA

(F#¥=(3-ixaH")

663

664

#

665

def prob_fn_at(t_week,

666

段 内 概率
return

函数

(用 于 导出
表 统 计) ”

按 口 径

b_bmi):

float(_prob_vec_at_t(res,

667

GA_mean,

np.array([b_bmi],
float),

t_week,

668

thr=args.thr,

=1.9，
669

mode=args.
guarantee_mode) [9])

670

671

BMI_mean

export_segments_bayes (

672
673

outdir, b_grid, T_mean, segs, prob_fn_at,
alpha=args.alpha, beta=args.beta,

674

fname_csv="bmi_segments_bayes.csv",

55

kappa

<!-- source_page: 56 -->

675

fname_fig="fig_t_bayes_segments.png"

676

)

677

678

# ======

679
680
681

if args.err_eval:
print("\n[ERR-IMPACT] 开始 检测 误差 敏感 性 分 析 ...")
kappas = [float(x) for x in str(args.sigma_grid).split
(",") if str(x).strip()!=""]

(可 选 ) 误差

敏感

682

outdir_err

683

ensure_dir (outdir_err)

性 ;: kappa

放

= os.path.join(outdir,

缩 残 差 方 差 ======

"error_impact")

684

685
686

# 复 用 BMI 网 格
bmin = args.bmin if args.bmin is not None else float(
d2["BMI"] -min())

687

688

bmax = args.bmax

if args.bmax

is not None else float(

d2["BMI"].max())
b_grid = np.round(np.arange(bmin, bmax + le-9, args.
bstep), 3)

689
690

*

691

step_curves = {}

为

画

Step

释

加

# kappa -y 台阶
化 后 的 y(b)

692

bayes_curves

# kappa

= {}

图

准备

容

兰

->

T_bayes_mean(b)

693

694
695
696

rows = []
for kappa in kappas:
print(f"[ERR-IMPACT] kappa={kappa:.2f}")

697

# 1) WEEHEM

(方差 xkappa^2)

， 支
持 向 量化

ti

按口

径
698
699

700
701

def

prob_vec_tk(t_vec,
t_vec

b):

= np.asarray(t_vec,

float)

return np.array([prob_ge_threshold_scaled(res,
GA_mean, BMI_mean, t, b,
thr=
args.thr, kappa=kappa,

702

mode

56

<!-- source_page: 57 -->

=args.guarantee_mode)
703

for t in t_vec]，float)

704

705
706
707

# 2) 计算 Tx(b)
T_star_k，reach_k = compute_T_star_grid(
prob_fn=prob_vec_tk, b_grid=b_grid,

708

g=args.q,

t_min=args.tmin,

t_max=args.tmax,

贝 叶 斯

单调
弗 线 ( 含 保守 纠偏 )

step=0.1
709

)

710
71

# 3)

712
713

T_mean_k, T_lo_k, T_hi_k = bayes_monotone_curve(
b_grid, T_star_k, method=args.method, draws=
args.draws, seed=2025
)
bayes_curves[kappa] = T_mean_k.copy()

714
715
716

n7

# 4)
|

718
719

若

指定 了 K 段 : 在 kappa

下 重新

做 风险 最 优 台 阶

#

nseg, bounds_str, trec_str, gmin, gmed = ©, "[]",
“[1", np.nan, np.nan
if args.segment_k and args.segment_k
》9:

720
721

# 预计
算 前 组 概率
—» p_prefix_k =

(注意

kappa +

口径 )

precompute_prob_prefix_from_curve (
722

res,

723

b_grid=b_grid, T_curve=T_mean_k,

724

thr=args.thr,

725

=kappa,

GA_mean,

BMI_mean,
round_to=args.roundto,

kappa

mode=args
. guarantee_mode

726

)

727

lam_star_k,

segs_k

= find_lambda_for_k(

728

b_grid, T_mean_k, p_prefix_k,

729

target_k=args.segment_k,

730

1am_10=0.8, lam_hi=args.lam_hi, tol=le-4,
57

<!-- source_page: 58 -->

T31

round_to=args.roundto, w_fail=args.wfail,

732

alpha=args.alpha,

beta=args.beta,

max_iter

=30
73
734

)
nseg = len(segs_k)

735

#

736

记录

边界

与 推荐 时 点

bounds = [(float(b_grid[i])，float(b_grid[j]))
for (i,j,，_) in segs_k]
tlist = [float(t) for (_,_,t) in segs_k]
bounds_str = str(bounds)
trec_str
= str(tlist)

737
T38
739
740

741

#

742
743

def p_at(t_week, b_bmi):
return float(_prob_vec_at_t(res, GA_mean,

段 内 保障 率 (用

kappa + 口径 )

BMI_mean,
744

np.array([
b_bmi], float), t_week,

745

thr=args.thr,
kappa=kappa,

746

mode=args .
guarantee_mode)

747

#

|

[el)

每

个 段 把 该 段 所 有 网 格 的 概率

都 算 一 遍 ， 汇 总 min

/median

748
749
750
751

all_probs = []
step_y = np.empty_like(b_grid, float)
for (i,j,t_rec) in segs_k:
probs_seg = [p_at(t_rec, b) for b in
b_grid[i:j+1]]

752

all_probs .extend(probs_seg)

753

step_y[i:j+1]

754

= t_rec

gnin = float(np.min(all_probs))

if all_probs

else np.nan
755

gmed = float(np.median(all_probs)) if
all_probs

else

np.nan

58

<!-- source_page: 59 -->

756

step_curves[kappa] = step_y

757

758

# 导出 该 kappa

759
760

seg_df = pd.DataFrame({
"BMI_min":[round(b_grid[i],2) for (i,_,_)
in

的

分 段 表 (可 选 )

segs_k],

761

"BMI_max":[round(b_grid[j],2) for (_,j，)
in segs_k]，

762
763
764

"t_recommend_week" : [round(float(t),2) for
(Ls_st) in segs_k],
bH
seg_df.to_csv(os.path. join(outdir_err, £"
segments_kappa_{kappa:.2f}.csv"),

765 |

index=False，encoding="utf-8-sig
fo!

766

767
768

* 汇总 一 行
rows .append({

769

"kappa":

770

"n_segments":

771
772

"boundaries": bounds_str,
"t_rec_list": trec_str,

773

"reach_ratio_on_grid":

kappa,
nseg,

float(np.mean(reach_k))

,
774

"guarantee_min_on_segments": gmin,

775

"guarantee_median_on_segments":

776

gmed

])

777

778

# 5)

导出 敏感 性 摘要

779

df_sum

780

df_sum_path = os.path.join(outdir_err，”

= pd.DataFrame(rows)

error_impact_summary.csv")

781 |
782 |

df_sum.to_csv(df_sum_path，index=False，encoding="utf
-8-sig")
print(f"[ERR-IMPACT] 摘要
已 导出 : {df_sum_path}")
59

<!-- source_page: 60 -->

783

784

# 6)

785

#

画图 : 曲线

786
787
788

fig, ax = plt.subplots(figsize=(8.6,5.0))
for kappa, y in bayes_curves.items():
ax.plot(b_grid, y, lw=1.8, alpha=0.9, label=f"

6.1

&

台阶

分

段 随 kappa

的 变化

MiZRAMAE

kappa={kappa:g}")
789

ax.set_xlabel ("BMI"); ax.set_ylabel("
推 荐 孕 周 ( 周 ) ")

790

ax.set_title("
误 差 放 缩 kappa

791

ax.grid(True, alpha=0.3); ax.legend(ncol=2, fontsize

下 的 单调

推荐 曲线

对 比 ")

-=9)
792
793

fig.tight_layout()
fig.savefig(os.path.join(outdir_err,
fig_curves_vs_kappa.png"), dpi=170)

"

794

795

# 6.2

796

if

GMABRBEME

( 仅

在 设 了 K 本有 )

step_curves:

797

fig，ax = plt.subplots(figsize=(8.6,5.0))

798

for

799

kappa,

y in

step_curves.items():

ax.step(b_grid, y, where="mid", lw=2.2, label=
f"kappa={kappa:g}")

800

ax.set_xlabel("BMI");

ax.set_ylabel("
推 荐 孕 周

( 周 ) ")
801

|

ax.set_title(f"k={fargs.segment_k}

kappa

的 变化 ")

802

803

ax.grid(True,

alpha=0.3);

ax.legend(ncol=2,

fontsize=9)
fig.tight_layout()

804

fig.savefig(os.path.join(outdir_err，

fig_segments_vs_kappa.png"), dpi=170)
805

806

段 的 台阶
化 结果 随

print("[ERR-IMPACT]

完成

807

808

|if __name__

809

main()

== "__main__":

60

。")

b

<!-- source_page: 61 -->

a3.py
1

|# -*#-

2

coding:

|wen

3 |q93.py

utf-8 —x—

第 三 问 ( 接 人 Pymc

图

+

方案 A(6

作用

的 贝 叶 斯 单调回归 + 批量

kappa + £

研究 ) )

4 |- 一 -一 -一 -一 -- 一 -一 一 一 ------ 一 -一 一 -------:

-

5 |- 单 油 化 支持 : Bayes(PyMC) / PAVA; 若 无 PyMC 自动 回 退 PAVA
6 |- 支持
一 次 输入 多 个 kappa: --kappa-batch "1.00,1.15,1.25"
7|
， 批量 模式 默认 每 个 kappa 输出 到 outdir/kappa_x.xx 子 目 录 (~no-batch-subdir 可 关闭 )
8 | 只 在 第 一 轮 画 “灵敏
度 图 ”， 吉 免 重 复 计算
9

|- 支持 画 95%

置信 带 (--show-cred，

仅

Bayes

时 有 效 )

10 |- 方案 A: 新 增 --omit-g 5 --g-grid "8,1,2,3":
11 | ，omit-g: 固定 效应 中 不 加 入 5 (怀孕
次 数 ) ， 用 手 与 妆 会 6” 做 对
照

12 |

，g-grid:
BMI)

13

|fk#i:

在 模型含 6 时 ， 指 定 一 组 6 水 平 %- 分 别 计 算 与

单调 曲线 ， 并 绘制 相 邻 6
pandas,

numpy,

的 At*

statsmodels,

曲线

scikit-learn,

matplotlib

14 | 可 选 : pymc>=4 (jc3 A ULoJ07
66 90 J5) 09)
15: ws
16
17 |import argparse, os, re, warnings, math,
18
19

pathlib

|from dataclasses import dataclass
|from typing import List, Tuple, Optional

20
21

|import

numpy

as

np

pandas

as

pd

22

|import

23

|from scipy.stats

24

|from

25
26
27

|# ---------|try:

28

import

import norm

sklearn.isotonic

import

IsotonicRegression

statsmodels —--------statsmodels.api

as

sm

61

scipy,

绘制 tr(

|

<!-- source_page: 62 -->

29
30

31

from statsmodels.regression.linear_model import OLS
|except

Exception

as

e:

raise RuntimeError("
需 要 安装 statsmodels: pip install
statsmodels") from e

32
33 |# ---------- optional: PYMC ---------34 |HAs_pYMC = False
35 |try:
36
37

import
try:

pymc

as

pm

38
import pytensor.tensor as pt
39
except Exception:
40
import aesara.tensor as pt
4
HAS_PYMC = True
42 |except Exception:
要
HAS_PYMC = False
44
45

46 |# =-=====-=-------- 基础 清洗 ===-=-==-------===47 |def logit(p: np.ndarray, eps: float = le-6) -> np.ndarray:
48

p = np.clip(p,

eps,

1 - eps)

49

return np.log(p / (1 - p))

50

51
52

|def try_get_col(df: pd.DataFrame, candidates: list) ->
Optional[str]:
for

53

c

54
55

in

candidates:

if c in df.columns:
return
return

上

None

56

57 |def ff_to_fraction(val):
58

if val

is None

or

(isinstance(val,

float)

and

)):
59

60

return

np.nan

if isinstance(val,

(int, float, np.number)):
62

np.isnan(val

<!-- source_page: 63 -->

61
62

x = float(val)
if ec xx li:

63

return

X

64
65

if 1.5 <= x <= 100:
return x/100.0

66

return

67
68
69
70

s = str(val).strip().lower()
if s.endswith('%'):
try:
return float(s[:-1])/188.9

71

72
了3
74
T5

except:

return np.nan
mm = re.match(r'~\d+(2:\.\d+)?$", s)
if m:
x = float(s)

76

if

77

@

¢

%

¢1:

return

78
79
80

np.nan

x

if 1.5 ¢<= x <= 100:
return x/100.0
return

np.nan

81
82

83
84 |def phi_time(t_week: float, alpha: float = 9.92，beta: float =
0.12, t_ref: float = 28.8) -> float:
85

86

""" 相 对 28 周
后 更 贵 ) , ""

的时 间 巧

罚: 提前 用 alpha，

汪 后 用 beta

(默认 滞

return (t_ref - t_week) x alpha if t_week < t_ref else (
t_week

~ t_ref)

x beta

87
88 |def compute_segment_metrics(b_grid, segs, prob_fn_at, alpha:
&
90

float

ws
返回

= @.82,

beta:

float

= 0.12):

每 段 : BMI_min/max 、 推 荐 周 、p_ge_thr_mean 、risk_mean、

n_grid.

63

<!-- source_page: 64 -->

91 |

risk_mean = mean( (1-p) + phi_time(t_rec)

|

)，

与 第 二 问 口 径

一致

9%2
93
94

ee
import numpy as np
rows = []

95

for

96
97
98
99

i, j, t_rec = (s.start_idx, s.end_idx, float(s.y_hat))
bmin, bmax = float(b_grid[i])，float(b_grid[j])
b_list = b_grid[i:j+1]
probs = [float(prob_fn_at(t_rec，float(b))) for b in
b_list]
p_mean = float(np.mean(probs))
r_mean = float(np.mean([(1.9 - p) + phi_time(t_rec,
alpha，beta) for p in probs]))
rows .append(dict(
BMI_min=round(bmin, 2), BMI_max=round(bmax, 2),
t_recommend_week=round(t_rec, 2),
p_ge_thr_mean=round(p_mean, 4),
risk_mean=round(r_mean, 4),
n_grid=int(len(b_list)),

100
101
102
103
104
105
106
107

s in

108

))

109

return

segs:

rows

110

m
112
113

|def ga_to_weeks(val):
if val is None or (isinstance(val, float) and np.isnan(val
)):

114
115
116

if

return np.nan
isinstance(val,
return

(int,

float,

np.number)):

float(val)

117

s = str(val).strip().lower()

118

s = (s.replace('

19 |

*).replace('[','d").replace(’ + ',"'+'))
m = re.match(r'A(\d+)\skw2\sx(2:\¢[\sx)\sx
(\d{1,2}) \sxd?8"
,S) # 11w+6 / 1146

周 '，'w').replace('
天 '，d').replace(' 因 '，w

64

<!-- source_page: 65 -->

120
121
122

if mi:
return int(m.group(1)) + int(m.group(2))/7.0
mm = re.match(r'~(\d+)\sxu$', s)
#

123
124
125

if m:
return float(m.group(1))
m = re.match(r'~(\d+)w(\d{1,2})d$", s)
#

126
127
128
130
131

11w6d

if mi
return int(m.group(1)) + int(m.group(2))/7.0
m = re.match(r'~\d+(2:\.\d+)?$", s)
#

129

11lw

if

14

/

14.5

m:

return float(s)
return np.nan

132

133 |def to_numeric_loose(series: pd.Series) => pd.Series:
134
s_num = pd.to_numeric(series, errors='coerce')
135
need = s_num.isna()
136

if need.any():

137
138
139

s_str = series.astype(str).str.extract(r'(\d+)",
expand=False)
s_fill = pd.to_numeric(s_str, errors='coerce')
s_num = s_num.where(~need, s_fill)

140

return

s_num

141
142

143

|# ===========<======

144

|def fit_baseline_model(df:

MixedLM

拟 合 =================

pd.DataFrame，

145

col_ff:

146

col_id: Optional[str],

147

add_age_gp:

148
149

str,

col_ga:

str,

col_bmi:

str,

bool,

col_age: Optional[str], col_g: Optional
[str], col_p: Optional[str],
omit_g: bool = False):
65

<!-- source_page: 66 -->

150
151
152
153
154
155
156
157
158
159

y = logit(df[col_ff].to_numpy())
GA = df[col_ga].to_numpy().astype(float)
BMI = df[col_bmi].to_numpy().astype(float)
GA_c = GA - np.nanmean(GA)
BMI_c = BMI - np.nanmean(BMI)
X_list = [GA_c, GA_Ckx2, BMI_c, BMI_cxx2]
age_gp_cols = []
if add_age_gp:
if col_age and col_age in df.columns:

160

161
162
163
164
165
166
167
168
169
170

age_gp_cols.append('AGE")

a = pd.to_numeric(df[col_age], errors='coerce’).
to_numpy (dtype=float)
X_list.append(a - np.nanmean(a))
if (not omit_g) and col_g and col_g in df.columns:
age_gp_cols.append('G")
g = pd.to_numeric(df[col_g], errors='coerce').
to_numpy (dtype=Float)
X_list.append(g - np.nanmean(g))
if col_p and col_p in df.columns:
age_gp_cols.append('P")
p = pd.to_numeric(df[col_p], errors='coerce').
to_numpy (dtype=Float)
X_list.append(p - np.nanmean(p))

171

172

X = np.column_stack(X_list)

173

X = sm.tools.tools.add_constant(X，has_constant='add')

174

175

design

= {

176
177

'GA_mean': float(np.nanmean(GA)),
"BMI_mean': float(np.nanmean(BMI)),

178

"age_means':

179

{

'A6E': float(pd.to_numeric(df[col_age]，errors='
coerce') .mean()) if (col_age and col_age in df.columns) else
8.9，
66

<!-- source_page: 67 -->

180 |

"6': float(pd.to_numeric(df[col_g]，errors='coerce
").mean())

181

|

if
"P'":

(col_g

and

col_g

in df.columns)

else

9.9，

float(pd.to_numeric(df[col_p]，errors='coerce

*).mean()) if (col_p and col_p in df.columns) else 6.9，
182

和

183

‘age_gp_cols':

age_gp_cols

184

}

185
186
187
188

if col_id and col_id in df.columns:
groups = df[col_id].astype('category')
Z = np.column_stack([np.ones_like(GA_c), GA_c])

189

190
191
192
193
194
195
196
197
198

try:

with warnings.catch_warnings():
warnings.simplefilter("ignore")
md = sm.MixedLM(endog=y, exog=X, groups=groups
, exog_re=2)
mfit = md.fit(method="1bfgs’, reml=False,
maxiter=500, disp=False)
return 'MixedlM', mfit, design
except Exception as e:
warnings.warn(f"MixedLN 拟
侣 失败 ， 回 退 OLS(HC3): {
e}")

return 'OLS', OLS(y, X).fit(cov_type='HC3'), design

199

200

|# =====-==-=-=-=-=-====-

201

|def mu_at_t_bmi(result, model_type, design, t_week: float, bmi

PEHG

t+

=-=========-====-=-=-

: float,

202
203
204
205
206
207

age_val: Optional[float], g_val: Optionall
float], p_val: Optional[float]) -> float:
GA_c = float(t_week - design['GA_mean'])
BMI_c = float(bmi - design['BMI_mean'])
X = [1.0, GA_C, GA_Ck#2, BMI_c, BMI_cxx2]
if 'age_gp_cols' in design and design['age_gp_cols']:
means

= design['age_means']

67

<!-- source_page: 68 -->

208

if 'AGE' in design['age_gp_cols'] and age_val is not
None:

209
210
211

X.append(age_val - means.get('AGE'，98.9))
if "6G' in design['age_gp_cols'] and g_val is not None:
X.append(g_val - means.get('6'，9.9))

212

if

213
214

"P'

in design['age_gp_cols']

and

p_val

is

not

None:

X.append(p_val - means.get('p'，9.6))
beta = result.fe_params if model_type == 'MixedlM' else
result.params

215

return float(np.dot(beta, np.asarray(X, float)))

216

217
218
219
220
221
222
23
224

|def sd_at_t(result, model_type, t_week: float, design,
var_mode: str='new', kappa: float=1.8) -> float:
v = float(result.scale) * float(kappa)xx2
if (var_mode == 'new') and (model_type == ‘MixedLM') and
hasattr(result, 'cov_re'):
GA_c = float(t_week - design['GA_Lmean'])
vec = np.asarray([1.0, GA_c], float)
try:
cov_re = np.asarray(result.cov_re, float)
v += float(vec @ cov_re @ vec)

225

except

226

227
228
229

230
231
232
233

Exception:

pass

return math.sgrt(max(v, le-12))
|def

prob_ge_thr(result,

model_type,

design,

t_week:

float,

bmi

: float, thr: float,
age_val: Optional[float], g_val: Optionall
float], p_val: Optional[float],
var_mode: str='new', kappa: float=1.9) ->
float:
eta = mu_at_t_bmi(result, model_type, design, t_week, bmi,
age_val, g_val, p_val)
sd = sd_at_t(result, model_type, t_week, design, var_mode=
var_mode,

kappa=kappa)

68

<!-- source_page: 69 -->

234

return float(norm.cdf((eta - float(logit(np.array([thr]))
[e]))

7 sd))

235

236

|def tstar_for_bmi(result, model_type, design, bmi, q, tmin,
tmax, step, thr,

237

238
239
240
241
242
243
244
245
246
247
248

age_val,

g_val,

p_val,

var_mode='new',

kappa

=1.9) -> float:
grid = np.arange(tmin, tmax + le-9, step)
probs = [prob_ge_thr(result, model_type, design, t, bmi,
thr, age_val, g_val, p_val, var_mode, kappa) for t in grid]
idx = next((i for i, p in enumerate(probs) if p >= q),
None)
if idx is None:
return float(tmax)
lo = max(tmin，grid[max(9，idx-2)])
hi = grid[idx]
for _ in range(25):
mid = 0.5x(lo+hi)
if prob_ge_thr(result, model_type, design, mid, bmi,
thr, age_val, g_val, p_val, var_nmode, kappa) >= q:
hi = mid

249

else:

250
251
252

lo = mid
return float(hi)

253

254 |# ================= 台阶 化 -===============255 |@dataclass
256

257
258
259

|class

Segment:

start_idx: int
end_idx: int
y_hat: float

260

261

|def stepwise_segments_L2(x: np.ndarray, y: np.ndarray, K: int,
min_width:

Optional[int]=None)

69

->

List[Segment]:

<!-- source_page: 70 -->

262
263

order = np.argsort(x，kind="mergesort")
x，y = x[order]，y[order]

264

n=

265

K = int(min(max(1,

266
267
268

if min_width is None:
min_width = max(1, n // (K % 4))
Wy = np.cumsum(y); W = np.cumsum(np.ones_like(y)); yy = np

len(y)

K), n))

Lcumsum(yx%2)

269
270
271
272
273
274
275
276
277
278
279
280
281

def cost(i,j):
sw = M[j] - (W[i-1] if i>@ else 0.0)
swy= Wy[j]- (Wy[i-1]if iy8 else 6.6)
syy= yy[31- (yy[i-1]if i>8 else 0.0)
return float(syy - (swy##2)Vmax(sw,le-12))
def mean(i,j):
sw = M[j] - (W[i-1] if i>8 else 0.0)
swy= wy[j]- (Wy[i-1]if i>8 else 0.0)
return float(swy/max(sw,le-12))
€ = np.full((n,n), np.inf); M = np.zeros((n,n))
for i in range(n):
je = max(i, i+min_width-1)
for j in range(je, n):

282

Cc[i,j]

283

= cost(i,j);

M[i,j]

= mean(i,j)

dp = np.full((K+1,n), np.inf); ptr = =np.ones((K+1,n),
)

284
285

286
287

for j in range(min_width-1, n):
dp[1,j]

= 5[9,j];

ptr[1,j]

= -1

for k in range(2, K+1):
for j in range(ksmin_width-1, n):

288

imin

289
290
291

for 1 in range(imin, j-min_width+1):
cand = dp[k-1,i] + C[i+1,3]
if cand < best:

292

best，arg

293
294

= (k=1)smin_width-1;

dp[k,j]=best;
segs=[];

k=K;

= cand,

ptr[k,j]=arg

j=n-1
70

best

i

= np.inf;

arg=-1

int

<!-- source_page: 71 -->

295
296
297
298

while k>=1:
i=ptr[k,j]; st=0 if ic else i+1; ed=j
segs.append (Segment(st,ed, float(M[st,ed]))); j=i; k-=1
segs.reverse()

299

return

segs

300

301

|def enforce_monotone_on_segments(segs:
Segment] :

List[Segment]) -> List[

302
303

if not segs:
return segs

304
305
306
307

309
310

n_list = [seg.end_idx-seg.start_idx+1 for seg in segs]
y_list = [seg.y_hat for seg in segs]
idx = list(range(len(segs)))
iso = IsotonicRegression(increasing=True，out_of_bounds='
clip')
y_mono = iso.fit_transform(idx, y_list, sample_weight=
n_list)
for seg, ym in zip(segs, y_mono):
seg.y_hat = float(ym)

311

return

308

segs

312

313
314
315
316
317

|def summarize_segments(x_sorted: np.ndarray, y_sorted: np.
ndarray, segs: List[Segment], roundto=0.1) -> pd.DataFrame:
rows=[]
for s in segs:
bmin，bmax = float(x_sorted[s.start_idx])，float(
x_sorted[s.end_idx])
n = int(s.end_idx - s.start_idx + 1)

318

t = float(s.y_hat)

319

if roundto and roundto>e:

320

321

t = round(t/roundto)xroundto

rows.append ({"BMI_nin": bmin, "BMI_max": bmax, "n": n,
"t_star_rec":

322
323

t})

return pd.DataFrame(rows)

71

<!-- source_page: 72 -->

324
325
326

|def assign_segments(x_sorted:

-> np.ndarray:
seg_id = np.empty(len(x_sorted),
for s in segs:

327
328
329

np.ndarray,
int);

seg_id[s.start_idx:s.end_idx+1]
return

segs:

List[Segment])

cur=1

= cur; cur+=1

seg_id

330

331

|# -===--=----------

332
333

|def bayes_monotone_curve(b_sorted: np.ndarray,
y_obs: np.ndarray,

F{L:

Bayes / PAVA -=----=--=-=--=------

334

method:

335

vi_steps:

int = 12000,

336

draws:

int

=

337

tune:

int

338

chains:

339

target_accept:

340

seed:
np.ndarray,
下

np.ndarray]:

342

使 用贝 叶 斯
合 单调 曲线 :

单调回归

343

T(b_k)

341

344
345

= mue

str

=

"vi',
1000,

=

1000,

int

= 2,

(累积
非 负 描 量 ) 对

+ cumsum(

y_k ~ Normal(T(b_k),
T_mean,

T_lo,

x s x Ab_k

拟

)

sigma)

T_hi

分 别为 后 验 均

和
try:
import

pymc

as pm

try:

351

import

352

except Exception:

353
354

《【b_sorted，y_obs)

softplus(z_k)

下 /上 界 (长 度 = len(b_sorted))

350

= 0.9,

返回 :

346
347
348
349

float

int = 42) -> Tuple[np.ndarray,

except

pytensor.tensor

import aesara.tensor
Exception as e:
72

as pt
as pt

值 与 95%

置信 带 的

<!-- source_page: 73 -->

355 |

raise RuntimeError("
未 检测 到 PyMC，
method

pava

或 安装 pymc>=4")

from

请 改 用 --mono-

e

356

357

n = len(b_sorted)

358
359

if n 1= len(y_obs):
raise ValueError(f"b_sorted
vs {len(y_obs)}")

与 y_obs

长 度 不 一 致 : {n}

360

361
362
363
364

db = np.diff(b_sorted)
if db.size == 9:
db = np.array([1.6])
step = np.concatenate([[np.median(db)],

db])

365

366

try:

367

sp

368
369

= pt.nnet.softplus

except Exception:
def sp(x): return pt.loglp(pt.exp(x))

370

371
372

with pm.Model() as m:
mu = pm.Normal('mud', mu=np.nanmedian(y_obs), sigma
=2.0)

373
374
375

s = pm.HalfNormal('s', sigma=0.5)
z = pm.Normal('z', ©.0, 1.9，shape=n)
inc = pm.Deterministic('inc’, sp(z) # s x step)
|

非 负 增 量 * 步 长

|

单调

376 |

T = pm.Deterministic('T'，mue + pm.math.cumsum(inc)) #
曲线

377

sigma

378

pm.Normal('y',

= pm.HalfNormal('sigma',
mu=T,

sigma=0.4)

sigma=sigma,

observed=y_obs)

379

380
381
382

#

if method == 'vi':
approx = pm.fit(n=vi_steps, method='advi’,
random_seed=seed, progressbar=False)
samples = approx.sample(draws=draws, random_seed=
seed)

7

<!-- source_page: 74 -->

383

# 取出

384

T_samps

385

try:

386
387
388
389
390
391
392

T

的 样本
= None

da = samples.posterior['T']
dims = list(da.dims)
if ‘chain’ in dims and 'draw’ in dims:
pt_dim = [dfor d in dims if d not in ('
chain®, "draw’)]
if len(pt_dim) == 1:
da = da.transpose('chain'，'draw'，
pt_dim[e])
T_samps = da.values

393

except

394

Exception:

T_samps = samples.get_values('T', combine=True
)

395
396

else:
idata = pm.sample(draws=draws, tune=tune, chains=
chains,

397

target_accept=target_accept,
random_seed=seed,

398
399
400
401

cores=1)

da = idata.posterior['T']
dims = list(da.dins)
if "chain， in dims and ‘draw' in dims:
pt_dim = [d for d in dims if d not in ('chain’
,tdraw')]

402
403

if len(pt_dim) == 1:
da = da.transpose(’chain’,
draw’, pt_dim

[e])
404

T_samps

= da.values

405

406

T_samps

= np.asarray(T_samps)

407

n_points

= n

408

409

def to_draws_points(arr:

np.ndarray,

ndarray:

74

n_points: int) => np.

<!-- source_page: 75 -->

410

if arr.ndim == 1:

411
412

413
414

if

arr.shape[@] == n_points:
return arr[None, :]

raise ValueError(f"
采 样 形状 异常 : {arr.shape}")
if arr.ndim == 2:

415

if arr.shape[-1]

416

return

417
418
419

==

n_points:

arr

if arr.shape[@] == n_points:
return arr.T
if arr.shape[@] > arr.shape[1] and arr.shape[1]

!=

n_points:
420

421
422
423
424
425
426
427

arr

430

arr.T

if arr.shape[-1] != n_points:
raise ValueError(f"
采 样 形状 异常 : {arr.shape}
vs n_points={n_points}")
return arr
if arr.ndim >= 3:
axes = list(range(arr.ndim))
cand = [i for i, s in enumerate(arr.shape) if s ==
n_points]
if not cand:

428

429

=

if

arr.shape[-1]

!= n_points:

raise ValueError(f"
采 样 形状 异常 : {arr.
shape} vs n_points={n_points}")
point_axis = arr.ndim - 1

431

else:

432
433

point_axis = cand[-1]
if point_axis != arr.ndim - 1:

434

axes.remove(point_axis)

435

axes.append(point_axis)

436

arr = np.transpose(arr,

437

438

return

arr.reshape(-1,

axes)

n_points)

raise ValueError(f"
# # [f 5 #: ndim={arr.ndim}")

439

440

T_samps

= to_draws_points(T_samps,

75

n_points)

<!-- source_page: 76 -->

441
442
443

T_mean = T_samps.mean(axis=0)
T_lo = np.quantile(T_samps, 0.025, axis=0)
T_hi = np.quantile(T_samps, ©.975, axis=0)

44

445

if not (len(T_mean) == len(T_lo) == len(T_hi) == len(
b_sorted)):

446
447

raise RuntimeError(f"
返 回 长 度 不 一 致 : mean={len(T_mean)
}, lo={len(T_lo)}, hi={len(T_hi)}, b={len(b_sorted)}")
return T_mean, T_lo, T_hi

448
449

450
451
452

|def pava_monotone_curve(b_sorted: np.ndarray, y_obs: np.
ndarray) -> np.ndarray:
iso = IsotonicRegression(increasing=True，out_of_bounds='
clip')
return iso.fit_transform(b_sorted，y_obs)

453
454

455 |# -============--=== 绘图 (ll I/RMJE)
456
457

-=-=====-=-=-=---

|def _mpl_setup():
import matplotlib.pyplot as plt

458

try:

459
460

plt.rcParams[’font.sans-serif'] = ['SimHei','Microsoft
YaHei','Arial’, 'Dejavu Sans']
plt.rcParams['axes.unicode_minus'] = False

461

except

462
463

Exception:

pass
return

plt

464

465

|def plot_curve(figpath_png: str, b_grid: np.ndarray, T_star:
np.ndarray,

466

T_curve:

np.ndarray,

dpi:

int=180,

save_pdf:

bool=False,
467

cred_lo: Optional[np.ndarray]=None, cred_hi:
Optional[np.ndarray]=None):

76

<!-- source_page: 77 -->

468
469
470

plt = _mpl_setup()
fig = plt.figure(figsize=(7.2, 4.6))
plt.scatter(b_grid, T_star, s=10, alpha=0.55,

471

BMI) raw')
if cred_lo is not None and cred_hi is not None:

472

label="Ts(

474

plt.fill_between(b_grid, cred_lo, cred_hi, alpha=0.18,
label='95% CI')
plt.plot(b_grid, T_curve, linewidth=2.2, label='Monotone
curve')
plt.xlabel('BMI'); plt.ylabel('Gestational week')

475

plt.title('Tx(BMI)

476
477
478
479
480
481

plt.legend(loc="best', frameon=False)
fig.tight_layout()
fig.savefig(figpath_png，dpi=dpi)
if save_pdf:
fig.savefig(figpath_png.replace('.png',
plt.close(fig)

473

& Monotone

Curve')

.pdf'))

482

483
484

|def plot_segments(figpath_png: str, b_sorted: np.ndarray,
T_sorted: np.ndarray,
segs: List[Segment]，dpi: int=180, save_pdf:
bool=False):

485

plt

= _mpl_setup()

486
487

fig = plt.figure(figsize=(7.2, 4.6))
plt.plot(b_sorted, T_sorted, linewidth=1.9,
label="'Monotone

488

for

alpha=0.95,

curve')

s in segs:

489

x = b_sorted[s.start_idx:s.end_idx+1]

490

y = np.full_like(x,

segs[segs.index(s)].y_hat,

dtype=

float)
491
492

plt.plot(x, y, linewidth=3.8)
plt.xlabel('BMI'); plt.ylabel('Gestational week')

493

plt.title('Monotone

494

plt.legend(['Monotone curve','Steps'],

Curve

with

=False)

77

K-step

Approximation')

loc='best', frameon

<!-- source_page: 78 -->

495
496
497
498
499

fig.tight_layout()
fig.savefig(figpath_png, dpi=dpi)
if save_pdf:
fig.savefig(figpath_png.replace('.png',
plt.close(fig)

.pdf'))

500

501

|def plot_sensitivity(figpath_png:

str, kappas: List[float],

compute_T_curve_fn,

502
503
504
505
5306
507
s08
509

dpi: int=180, save_pdf: bool=False):
“""compute_T_curve_fn(kappa) -> (b_grid, T_curve)"""
plt = _mpl_setup()
fig = plt.figure(figsize=(7.2, 4.6))
for k in kappas:
b, T = compute_T_curve_fn(k)
plt.plot(b, T, linewidth=2.8, label=f'kappa={k:g}')
plt.xlabel('BMI'); plt.ylabel('Gestational week')

510

plt.title('Sensitivity:

511
512
513

plt.legend(loc='best'，frameon=False)
fig.tight_layout()
fig.savefig(figpath_png，dpi=dpi)

514

if save_pdf:

515
516

fig.savefig(figpath_png.replace('.png'，'.pdf'))
plt.close(fig)

Monotone

Curves

vs kappa')

517

SI18

|# 方案 A:

519

|def

按 6 分 层 的

两张 图

plot_curves_vs_g(figpath_png:

str,

b_grid:

np.ndarray,

curves_by_g, dpi: int=180, save_pdf: bool=False):
520

plt

521

fig = plt.figure(figsize=(9.6,

322

523

for

[e]):

= _mpl_setup()
g_val,

curve

in

plt.plot(b_grid,

5.2))

sorted(curves_by_g,

key=lambda

curve, linewidth=2.2,

label=f'G={

g_valig}')
524

plt.xlabel('BMI'); plt.ylabel('
推 荐 孕 周 ( 周 ) ')

525

plt.title("
不 同 6

水 平 的 tx(BMI)

78

单调

x:

推荐 曲线

对 比 ')

x

<!-- source_page: 79 -->

526
3527
528

plt.legend(frameon=False); plt.grid(alpha=e.25)
fig.tight_layout(); fig.savefig(figpath_png, dpi=dpi)
if save_pdf: fig.savefig(figpath_png.replace('.png’,".pdf’
))

529

plt.close(fig)

530

531

|def plot_delta_tstar_vs_g(figpath_png:

str,

b_grid:

np.ndarray

, curves_by_g, dpi: int=180, save_pdf: bool=False):
532

""" 对 相

533

plt

534
535
536

fig = plt.figure(figsize=(9.6, 5.2))
curves_by_g = sorted(curves_by_g, key=lambda x: x[9])
for (g1, c1), (g2, c2) in zip(curves_by_g[:-1],
curves_by_g[1:]):
delta = np.asarray(c2) - np.asarray(cl)
plt.plot(b_grid, delta, linewidth=2.0, label=f'Ats: G

537
538
539

邻 @ 作 差 : At# = tx(G_{i+1})

- tx(6_i)"""

= _mpl_setup()

={gl:g}~{g2:g}")

plt.xlabel('BMI');

plt.ylabel('At+ ( 周 ) ')

540

plt.title("
相 邻 6

水

541
542
543

plt.legend(frameon=False); plt.grid(alpha=9.25)
fig.tight_layout(); fig.savefig(figpath_png, dpi=dpi)
if save_pdf: fig.savefig(figpath_png.replace('.png'，'.pdf'

平 的 推荐 周 数 差 值 (Otx)

*)

))

544

plt.close(fig)

545
546

547

|# =-======--===-=-===-=

548

|def main():

549

ap

主流 程 -==-=========-=-=-

= argparse.ArgumentParser()

550

ap.add_argument('--xlsx'，required=True)

551

ap.add_argument('~-sheet',

552

ap.add_argument('--id-col'，dest='id_col'，default=None)

default=None)

553

554
555

ap.add_argument('--col-ff'，dest='col_ff'，default=None)
ap.add_argument('--col-ga'，dest='col_ga'，default=None)
79

<!-- source_page: 80 -->

556
557

ap.add_argument('~-col-bmi', dest='col_bmi', default=None)
ap.add_argument('~-col-age', dest='col_age', default=None)

558

ap.add_argument('--col-g',

dest='col_g',

559

ap.add_argument ('--col-p',

dest='col_p', default=None)

default=None)

560

561

ap.add_argument(‘'--thr',

type=float,

default=0.04)

562
563
564
565
566

ap.add_argument('--q', type=float, default=0.95)
ap.add_argument('--tmin', type=float, default=12.0)
ap.add_argument('--tmax'，type=float，default=28.9)
ap.add_argument('--tstep'，type=float，default=8.25)
ap.add_argument('--bmi-step', dest='bmi_step', type=float,
default=0.1)

567

568
s69 |

ap.add_argument('~-var-mode', dest='var_mode', choices=["
new',"typical'], default='new',
help="new: scalexkappa®2 + REJf %; typical
:

570 |

{lscalexkappa~2')

ap.add_argument(‘-—kappa',

type=float, default=1.0,

help='

误差 放大 倍数 ")
371

572

ap.add_argument('--mono-curVe'y dests'*mono_curve'，action=

573

‘store_true', default=True)
ap.add_argument ('--no-mono-curve',

574

action="store_false')
ap.add_argument ('~-mono-steps', dest='mono_steps', action=
‘store_true',

575

dest='mono_curve',

default=True)

ap.add_argument ('~-no-mono-steps', dest='mono_steps’,
action='store_false')

576

577

ap.add_argument ('--bmi-min',

dest='bmi_min',

type=float,

dest='bmi_max',

type=float,

default=None)
578

ap.add_argument(‘'--bmi-max',

default=None)
579
580

ap.add_argument('--K', type=int, default=4)
80

<!-- source_page: 81 -->

381

ap.add_argument('--roundto'，type=float，default=9.1)

582

ap.add_argument ('--min-width',

dest='min_width',

type=int,

default=None)

583

ap.add_argument ('--outdir’, default='out_g3')

584

585

# 绘图

586

ap.add_argument('--plots'，action='store_true'，help='
生 成
| “三

587 |
录

588
589

590

张 图 ")

ap.add_argument('--figdir'，default=None，help='
图 片 输出 目
(默认 与 outdir

ap.add_argument('--save-pdf',

dest='save_pdf',

action="

store_true'，help='
同 时 保存 PDF')
ap.add_argument ('--kappa-grid', dest='kappa_grid', default
='0.9,1.0,1.15,1.25",

591

592

相同 ) ")

ap.add_argument('--fig-dpi'，dest='fig_dpi'，type=int，
default=180)

help= "灵敏

度 图 的 kappa

列表 ， 逗

号 分 隔 ")

ap.add_argument ('~-show-cred’, action='store_true', help='
bayes

单调
化 时 显示

95%

置信 带 ")

593

594
595

# 单调
化 控制
default_mono = 'bayes' if HAS_PYMC else 'pava’

596

ap.add_argument('--mono-method',

choices=['bayes','pava’],

default=default_mono,
597

help= "单调 化 方式 (默认 :
bayes

598

,

否则

pava)

若 装 了 Pymc

则

了)

ap.add_argument (*~-envelope', action='store_true’, default
=True,

599
600

help=
"是 否 取 上 包 络 max(T_mono,
ap.add_argument ('--no-envelope',

T_star)')

dest="envelope',

action="

store_false')
601

602
603

# Bayes 细节
ap.add_argument ('--bayes-method', choices=['vi','nuts'],
default="vi’,
81

<!-- source_page: 82 -->

604
605

help='
贝 叶 斯 推断 方式 : vi(ADVI) 或 nuts')
ap.add_argument ('--vi-steps', type=int, default=12000)

606

ap.add_argument('--draws',

607

ap.add_argument ('--tune’, type=int, default=1000)

608

ap.add_argument('--chains',

609

ap.add_argument('--target-accept',

610
611
612
613

type=int,

default=1000)

type=int,

default=2)

type=float,

default

-0.90)
ap.add_argument (‘--seed', type=int, default=42)
# 批量 kappa
ap.add_argument ('--kappa-batch®, dest='kappa_batch',
default=None,

614

help=
"一 次 性 中 多 个 kappa，

615
616

"1.00,1.15,1.25"")
ap.add_argument ('--batch-subdir', action='store_true',
help='
批 量 模式 : 每 个 kappa 输出 到 outdir/
kappa_x.xx

617

各

目录

《默认

开启

)

逗
号 分 陋 ，例如

吵

ap.add_argument('--no-batch-subdir' dest='batch_subdir'，
action='store_false')

618

ap.set_defaults(batch_subdir=True)

619

620

# ==== 方案 A: 6 效应 研究 vse==

621

ap.add_argument('--omit-g',

622

helps "不 把 6
对

623
624

626

纳入

固定

ap.add_argument('--g-grid'，default=None，
help='按 6 分 层 绘制 /导出 : 例如

"提前

"0,1,2,3";

念 6 时 有 意义 ")

ap.add_argument('"--alpha'，

惩罚 7 周 【风险

指数 ) ")

" 洁 后 惩罚/ 周 (风险

指数 ) ")

ap.add_argument('--beta'，

type=float,

default=0.02,

help=

type=float, default=e.12, help=

627

628
629

效应 (用 于 和 含 6 模 型 作

照 ) ")

仅 在 模型
625

action='store_true',

args = ap.parse_args()
os-makedirs(args.outdir，exist_ok=True)
82

<!-- source_page: 83 -->

630
631

figdir = args.figdir or args.outdir
pathlib.Path(figdir).nkdir(parents=True, exist_ok=True)

632
633

634
635
636
637

#

读表

xls = pd.ExcelFile(args.xlsx)
sheet_name = args.sheet or (next((s for s in xls.
sheet_names if (' 男 胎 ，in s or ' 女 胎 ，in s)), xls.
sheet_names[0]))
df = pd.read_excel(args.xlsx, sheet_name=sheet_name)
df.columns = [str(c).strip() for c in df.columns]

638

639
640

# 列 名
col_id

= args.id_col

， 受 试

者 ID'， 样 本 ID'])

col_ff

= args.col_ff

61|

or try_get_col(df，['

孕 妇 代码 "ID'

or try_get_col(df，['Y

畸 色 体 深度

FF','fetal_fraction’,
'FF%", 'FF(%)"', 'Y¥: @a {kFF'])

642 |
643 |

colga

= args.col_ga

周 "'， 孕 周 数 "， 孕

or try_get_col(df,

[' 检 测

孕 闭 '， 孚

周 ( 周 )"，GA'"])

。 col_bmi = args.col_bmi or try_Bget_col(df，["BMI'，
体 质 指数
"5 "孕妇 BMI'])

644
645

col_age = args.col_age or try_get_col(df，['AGE'，
年 龄 '])
colg
= args.col_g
or try_get_col(df，['6'， 怀 孕 次 数 '，
“ 孕次 "])

646

col_p

= args.col_p

or try_get_col(df,

['P',"4i=k¥",

" 产次 "])
647

648

if any(c is None for c in [col_ff, col_ga, col _bmi]):

649

raise

ValueError(f"
核 心 列 无 法 识别 ， 请 手动

指定 : FF({

col_f£}), GA({col_ga}), BMI({col bmi})")
650

651

#

清洗

652

core_cols

653

col_g, col_p, col_id] if c]
d8 = df(core_cols].copy().replace([np.inf, —np.inf], np.

=

[c for

c in

[col_ff,

nan)

83

col_ga,

col_bmi,

col_age,

<!-- source_page: 84 -->

654
655
656

de[col_ff] = de[col_ff].apply(ff_to_fraction)
de[col_ga] = de[col_ga].apply(ga_to_weeks)
if col_age and col_age in d9.columns: d9[col_age] =
to_numeric_loose(de[col_age])

657
658
659
660

if col_g
and col_g
in de.columns: de[col_g]
to_numeric_loose(de[col_g])
if col_p
and col_p
in de.columns: de[col_p]
to_numeric_loose(de[col_p])
d8 - de.dropna(subset=[col_ff，col_ga，col_bmi])
de = de[(de[col
ff] > 8) & (de[col_ff] < 1)]

=
=

661

662
663

# 拟合
add_age_gp = any([c in d9.columns for c in [col_age, col_g
，<col_p]])

664
665

model_type，result，design = fit_baseline_model(
de，col_ff，col_ga，col_bmi，col_id，

666
667
668

add_age_gp, col_age,
omit_g=args.omit_g

col_g,

col_p,

)

669

670
671
672

# BMI 栅 格
if args.bmi_min is not None and args.bmi_max is not None
and args.bmi_max > args.bmi_min:
bmi_min, bmi_max = float(args.bmi_min), float(args.
bmi_max)

673

else:

674
675
676

bmi_min = float(np.nanmin(d@[col_bmi]))
bmi_max = float(np.nanmax(de[col_bmi]))
b_grid = np.arange(bmi_min, bmi_max + le-9, args.bmi_step)

677

678

# 代表 值 (中 位 数 )

679

age_med = float(np.nanmedian(de[col_age]))
col_age in d8.columns) else None
gmed
= float(np.nanmedian(de[col_g]))

680 |

col_g

in d9.columns)

else

None

84

if (col_age and
if (colg

and

<!-- source_page: 85 -->

681 |

。 pmed
|

682
683

-= float(np.nanmedian(de[col
p]))

col_p

in d@.columns)

else

if (colp

and

None

684 |

print(f"[OK] 模型 : {model_type}; sheet={sheet_name}; N={
len(de)}: "
f"GAE[{de[col_ga] .min():.2f},{fde[col_ga].max():.2f}]

685 |

f"BMIE[fde[col_bmi].min():.2f},{de[col_bmi].max():.2

686

f)]")

if model_type == 'MixedLM':

687

688

try:

print(f"[INFO] MixedlM 收敛 : 11f={getattr(result,"
11f'，np.nan):.3f}; scales{float(getattr(result,'scale’, np.
nan)):.4f}")

689

except:

690

pass

691

692

693

La

。^
> 上

和 au

def run_pipeline_for_kappa(kappa_val: float, out_dir_use:
str, fig_dir_use: str,

694

draw_sensitivity_once:

bool

=

True):

695
696

# 1) T#(b): 二 分
T_star_loc = [tstar_for_bmi(result, model_type, design
, b, args.q,

697

args.tmin,

args.tmax,

.tstep, args.thr,
698

age_med,

699

var_mode=args.var_mode,

g_med,

kappa=kappa_val)

700
701
702
703

for b in b_grid]
T_star_loc = np.asarray(T_star_loc, float)
# 2) MMf

(Bayes 或 PAVA)

704

b_sorted_loc

= np.asarray(b_grid)

85

p_med,

args

<!-- source_page: 86 -->

705
706

T_bayes_lo = T_bayes_hi = None
if args.mono_method == 'bayes' and HAS_PYMC:

707

T_mean,

T_lo,

T_hi

= bayes_monotone_curve(

708

b_sorted_loc,

709

method=args.bayes_method,

T_star_loc,

vi_steps=args.

vi_steps,

710

draws=args.draws,

tune=args.tune,

chains=args.

chains,
711

target_accept=args.target_accept,

seed=args.

seed

712
713
714
715
716

)
T_mono_loc = T_mean
T_bayes_lo, T_bayes_hi = T_lo,

T_hi

if args.mono_method == 'bayes'

and not HAS_PYMC:

else:

717

warnings.warn("
未 检测 到 PyMC ， 自 动 问 退 -PAVA

调
718

单

回归 。"，Runtimewarning)

T_mono_loc
T_star_loc)

= pava_monotone_curve(b_sorted_loc，

719
720

#

上 包络

721

if args.envelope:

722

T_curve_loc

723

= np.maximum(T_mono_loc,

T_star_loc)

if T_bayes_lo is not None and T_bayes_hi

is not

None:
724

T_bayes_lo

= np.maximum(T_bayes_lo,

T_star_loc

T_bayes_hi

-

T_star_loc

)
725

np.maximum(T_bayes_hi,

)
726

else:

727
728

T_curve_loc

= T_mono_loc

729

#3)

730

segs_loc = stepwise_segments_L2(b_sorted_loc,

台阶 化

T_curve_loc,

K=args.K,

min_width=args.min_width)

86

<!-- source_page: 87 -->

71

if args.mono_steps:

732

segs_loc

= enforce_monotone_on_segments

(segs_loc)

733

734

# ====

一 致 ) ===-

T35

新增:

每

段 概率 均值 与 风险

指数

(与 第 二 问

def prob_fn_at(t_week: float, b_bmi: float) -> float:

736 |

#

复 用 第 三 问 同 口径

的 概率

函数

(F

kappa、

方 差 模型

等)
737

return

prob_ge_thr(result,

model_type,

738
739

t_week, b_bmi, args.thr,
age_med, g_med, p_med,

740

var_mode=args.var_mode,

design,

kappa=

kappa_val)
741

742
743

rows_risk = compute_segment_metrics(
b_grid=b_sorted_loc, segs=segs_loc, prob_fn_at=
prob_fn_at,

744

alpha=getattr(args,
args,

745

'beta’,

'alpha',

0.82),

beta=getattr(

@.12),

)

746
747

748
749
750 |

import

pandas

as

pd,

os

df_risk = pd.DataFrame(rows_risk)
out_risk = os.path.join(out_dir_use, "
segments_q3_with_risk.csv")
df_risk:to_csv(out_risk，index=False，encoding="utf-8sig")

751 |
752
753
754
755
756
757

print(f"[OK@kappa={kappa_val:B}]
out_risk}")
# === 新 增 END ==-=

风险 指数 (分
段) 一{

# 4) 导出 CSV
os.makedirs(out_dir_use, exist_ok=True)
pl = os.path.join(out_dir_use, 'g3_tstar_by_bmi.csv')
p2 = os.path.join(out_dir_use, 'g3_bmi_stepify_summary
87

<!-- source_page: 88 -->

.csv')
758 |

p3 = os.path.join(out_dir_use,

°

q3_bmi_stepify_detailed.csv')

759

pd.DataFrame({"BMI": b_sorted_loc,
T_star_loc, "t_curve": T_curve_loc})\

760

.to_csv(pl,

761
762

index=False,

"t_star":

encoding='utf-8-sig')

order = np.argsort(b_sorted_loc, kind="mergesort")
b_sorted2 = b_sorted_loc[order]; T_sorted_loc =

763

T_curve_loc[order]
summary_loc = summarize_segments(b_sorted2,

764
765

T_sorted_loc, segs_loc, roundto=args.roundto)
seg_id_loc = assign_segments(b_sorted2, segs_loc)
detailed_loc = pd.DataFrame({"BMI": b_sorted2, "t_star
":

T_sorted_loc,

766 |

"seg_id":

summary_loc.to_csv(p2,

seg_id_loc})

index=False, encoding='utf-8-

sig’)

767 |

detailed_loc.to_csv(p3，index=False，encoding='utf-8sig )

768

769

print (£"[OK@kappa={kappa_val:g}] tx(BMI) — {p1}")

770

print(f"[OK@kappa={kappa_val:g}]

台阶 化 (汇总 ) — {p2}"

print(f"[OK@kappa={kappa_val:g}]

台阶 化 (明细
) 一 {p3}"

m

|

)
)

72 |
773

with pd.option_context('display.max_rows',
display.width', 120):
print(summary_loc)

5@, '

774

775

#5)

776

if args.plots:

777

终图

fig_curve = os.path.join(fig_dir_use,

'

fig_g3_curve.png')

778 |
7

|

fig_seg
= os.path.join(fig_dir_use,
fig_q3_segments.png')
fig_sens = os.path.join(fig_dir_use,
88

'
'

<!-- source_page: 89 -->

780

fig_q3_sensitivity.png')
pathlib.Path(fig_dir_use).mkdir(parents=True,
exist_ok=True)

781

782
783
784
785

plot_curve(fig_curve, b_sorted_loc, T_star_loc,
T_curve_loc,
dpi-args.fig_dpi, save_pdf=args.
save_pdf,
cred_lo=(T_bayes_lo if (args.show_cred
and T_bayes_lo is not None) else None),
cred_hi=(T_bayes_hi if (args.show_cred
and T_bayes_hi is not None) else None))

786

plot_segments(fig_seg,

b_sorted2,

T_sorted_loc,

segs_loc,

787

dpi=args.fig_dpi, save_pdf=args.
save_pdf)

788

789

# 灵敏 度 (RUE—%)

790

if draw_sensitivity_once:

791

try:

792

kappas = [float(s) for s in str(args.
kappa_grid).split(',"')

793

except

794

if s.strip()!=""]

Exception:

kappas = [0.9, 1.0, 1.15, 1.25]

795

796

def

_compute_T_curve_for_kappa(kappa_sens:

float) :
797

T_star_k = [tstar_for_bmi(result,
model_type, design, b, args.q,

798

args.tmin,

args.

tmax, args.tstep, args.thr,
799

age_med,

g_med,

p_nmed,
800

var_node=args.
var_mode,

kappa=kappa_sens)

89

<!-- source_page: 90 -->

801

for b in b_sorted_loc]

802

T_star_k

803

if

= np.asarray(T_star_k，float)

args.mono_method

==

'bayes'

and

HAS_PYMC:
804

T_mean_k,

805

_, _ = bayes_monotone_curve(

b_sorted_loc,

806

T_star_k,

method=args.bayes_method,

vi_steps

=args.vi_steps,
807

draws=args.draws,

tune=args.tune,

chains=args.chains,

8308

target_accept=args.target_accept,
seed=args.seed

809

)

810

T_mono_k

811
812

= T_mean_k

else:
T_mono_k = pava_monotone_curve(
T_star_k)
T_curve_k = np.maximum(T_mono_k, T_star_k)

b_sorted_loc,
813

if args.envelope

else

814
815

T_mono_k

return b_sorted_loc，T_curve_k

816

plot_sensitivity(fig_sens，kappas，
_compute_T_curve_for_kappa,

817

dpi=args.fig_dpi，save_pdf=
args.save_pdf)

818
819
820

print(f"[Ok@kappa={fkappa_val;g}]
- {fig_curve}\n - {fig_seg}\n - {fig_sens}")
else:
print (f"[OK@kappa={kappa_valig}]
- {fig_curve}\n

图

已 保存 : \n

图

已 保存 : \n

且 模

型 含6且 未

- {fig_seg}")

821
822

|
823 |

# 6)

方案 A: 按

6 分 层 ( 仅 当 提供

”omit_g 时 执行 )
if (args.g_grid
age_gp_cols'，

[]))

and

--g-grid

is not None) and (('G'
(not

args.omit_g)):

90

in design.get("

<!-- source_page: 91 -->

824
825

try:
split('，')

826
827

g_list = [float(s) for s in str(args.g_grid).
if s.strip()!=""]
except Exception:
g_list = []

828

829
830

if g_list:
curves_by_g = []

831

df_out

832

for gv in g_list:

833

834
835

#

= pd.DataFrame({'BMI':

重新 计算 该 6 的

ty

b_sorted_loc})

与 单调 化

T_star_g = [tstar_for_bmi(result,
model_type, design, b, args.q,
args.tmin, args.
tmax, args.tstep, args.thr,

836

age_med,

gv,

p_med,

837

var_mode=args.

var_mode, kappa=kappa_val)
838

for b in b_sorted_loc]

839

T_star_g

= np.asarray(T_star_g,

float)

840

#

841

if args.mono_method == 'bayes' and

HRfe

HAS_PYMC:
842

T_mean_g, _, _ = bayes_monotone_curve(

843

b_sorted_loc,

844

method=args.bayes_method, vi_steps

T_star_g,

=args.vi_steps,
845

draws=args.draws,

tune=args.tune,

chains=args.chains,

846

target_accept=args.target_accept,
seed=args.seed

847

)

848

T_mono_g

849

else:

91

= T_mean_g

<!-- source_page: 92 -->

850

T_mono_g = pava_monotone_curve(
b_sorted_loc,

T_star_g)

851

T_curve_g
if args.envelope

else

= np.maximum(T_mono_g,

T_star_g)

T_mono_g

852
853

curves_by_g.append((gv,

854
855
856
857

df_out[f't_curve_G{int(gv)}']

858 |

T_curve_g))

= T_curve_g

# 导出 CSV + 两 张 图
p_csv_g
= os.path.join(out_dir_use，，
q3_tstar_by_bmi_vs_g.csv')
p_fig_g
= os.path.join(fig_dir_use, '
fig_q3_curves_vs_g.png')

859

|

860 |

p_fig_dlt

= os.path.join(fig_dir_use,

fig_q3_delta_tstar_vs_g.png')
df_out.to_csv(p_csv_g,

index=False,

'

encoding=

utf-8-sig')

861

plot_curves_vs_g(p_fig_g,

b_sorted_loc,

curves_by_g,

dpi=args.fig_dpi, save_pdf=args.save_pdf)
plot_delta_tstar_vs_g(p_fig_dlt, b_sorted_loc,

curves_by_g,

dpi=args.fig_dpi,

862

save_pdf=args.save_pdf)

863
864

print(f"[OK@kappa={kappa_val:g}]

线 / 差
和

按

6

分 层 的 曲

值 图 已 生成 : \n ~ 《PLfig-g}y\n - {p_fig_dlt}\n - {p_csv_g

865

else:

866 |

print("[WARN] --g-grid

解析

为 空 ， 已跳 过 按 6 分

B.")

867

elif args.g_grid
not

in

868
(按 6

is not None and (args.omit_g or ('G'

design.get('age_gp_cols’,

print("[WARN]

当前

分 层 没 有 意义 )

。")

[]))):

模型 未 包含

869

870

# ---------- 批量 或 单 次 执行 ----------

871

if args.kappa_batch:
92

6， 已 忽 赂 --8-grid

<!-- source_page: 93 -->

872
873

try:
k_list = [float(s) for s in args.kappa_batch.split
(',") if s.strip()!=…]

874

except

875
文 逗号

Exception:

raise ValueError("
解 析 --kappa-batch 失败 ， 请 用 英
分 陋 ， 例 如 1.99,1.15,1.25")

876

877
878
879
880

print(f"[INF0] 批量 运行 kappa = {k_list}")
for idx, kappa_val in enumerate(k_list):
if args.batch_subdir:
out_use = os.path.join(args.outdir，f"kappa_{
kappa_val:.2f}")

881

fig_use

= out_use

882

else:

883
884
885
886

suffix = f"_k{kappa_val:g}".replace(’.', 'p')
out_use = f"{args.outdir}{suffix}"
fig_use = args.figdir or out_use
run_pipeline_for_kappa(kappa_val, out_use, fig_use

887

draw_sensitivity_once=(idx

== 9))
888

889

else:

run_pipeline_for_kappa(args.kappa,

args.outdir,

args.

figdir or args.outdir,
890

draw_sensitivity_once=True)

891

892
893

|if __name__

==

'__main__':

894

warnings.filterwarnings("ignore”,

895
896

warnings. filterwarnings("ignore”, category=FutureWarning)
main()

a4py
1 |# -#- coding: utf-8 -+
2 | se
93

category=RuntimeWarning)

<!-- source_page: 94 -->

3 |04 Transfer++
4 |- per-chrom empirical-null
，batch covariate
5

|- Grid-scan

for

FPR

(normal / Student-t)，winsorization

control

6 |- per-chromosome thresholds
7

|- Chinese-friendly

&

polished

(z/q/consistency)
visualizations

(+

multi-page

PDF

report)
8
9 |Typical run:
10 | python q4_transfer.py --xlsx "附件 .xlsx”--male-sheet " 男 胎
检测 数据 ”--female-sheet " 女 胎 检测 数据 ”\
1
--col-subject "孕妇 代码 ”--col-ga "检测
孕 周 ”--col-bmi "Z
妇 BMI"\
12
--col-z13 “13 号 染色 体 的 z 值 ”--col-z18 “18 号 染色 体 的 z 值 ”-col-z21“21 号 染色
体 的 z 值 ”\
13
--qc-features "GA,BMI,reads,align_rate,dup_rate,
unique_reads,gc” \
14
--batch-col "检测 日 期 ”--student-chrom "21”--winsor 6.61
\
15
--grid-scan --target-fpr 9.91 --grid-z "2.6,2.8,3.0,3.2"
--grid-q

"0.93,0.05,0.08"

--grid-consist

"2,3"

\

16
--outdir "out_g4_transfer_final"
17
18 |To set per-chromosome thresholds (optional, override global):
19 | --z-thr-21 2.6 --q-thr-21 8:85 --consist-21 2
可
21
22 | import os，re，json，argparse，warnings
23 |from typing import List, Tuple, Dict, Optional
24

25
26
27
28
29

|import numpy as np
|import pandas as pd
|import matplotlib.pyplot as plt
|from matplotlib import font_manager as _fm
|from matplotlib.backends.backend_pdf import PdfPages
94

<!-- source_page: 95 -->

30 |from math import erf
31
32 |# Optional SciPy
33 |try:
34
35

36

import
|except

scipy.stats

as sps

Exception:

sps = None

37

38

|# ------------------------

Pretty

& Chinese

Fonts

39 |_PRETTY_PALETTE = ["#4C78A8", "#F58518", "#E45756", "#728782",
"#54A248",
40
"HEECA3B", "#B279A2", "#FF9DA7", "#9D755D",
"#BABOAC"]
41
42 |def _pick_chinese_font():
43
candidates = ["Microsoft YaHei"，"Microsoft YaHei UI", "#{
软

雅 黑 "，

4

"Simhei"，"

45

"NMoto Sans CIK SC", "Source Han Sans SC", "
思源

46
47
48
49

"5“pPingFang_ SC"，“" 蔷
方 - 简 "，

黑体 ”，

“"WenQuanYi Micro Hei"]
available = {f.name for f in _fm.fontManager.ttflist}
for name in candidates:
if name in available:

50

51
52
53

黑体

return

name

return None
|def _setup_mpl():

54

import

55
56
57

font = _pick_chinese_font()
if font:
mpl.rcparams["font.sans-serif"] = [font，"Dejavu Sans"
，"Arial"]

matplotlib

as

mpl

58 |

mpl.rcparams["axes.unicode_minus"]

95

= False

<!-- source_page: 96 -->

59
60
61
62

mpl.rcparams["axes.titleweight"] = "bold"
mpl.rcpParams["figure.dpi"] = 149
mpl.rcParams[“axes.grid”] = True
mpl.rcParams[“grid.alpha”] = 0.25

63

64

|def _annotate_bars(ax):

65
66

for container in ax.containers:
ax.bar_label(container, fmt="%.0f", padding=2,
fontsize=9)

67

68 |# 一一--------------- 一 Math & Stats
69 |def
70
71
72
73 |def

_norm_cdf(x: np.ndarray) -> np.ndarray:
x = np.asarray(x, dtype=float)
return 9.5 # (1.9 + np.vectorize(erf)(x / np.sqrt(2.9)))
two_tailed_p_from(z: np.ndarray, family: str = “normal"，
df: Optional[float] = None) -> np.ndarray:

74

z = np.asarray(z,

75

if family == "student" and sps is not None and df is not
None and df > 1:
return 2.0 x (1.8 - sps.t.cdf(np.abs(z), df=df))
return 2.9 * (1.9 - _norm_cdf(np.abs(z)))

76
77
T8
79

dtype=float)

|def bh_fdr(p: np.ndarray) -> np.ndarray:

80

p = np.asarray(p,

81

n = p.size
n

==

@:

return

dtype=float)

82

if

83

order

= np.argsort(p)

P

84

ranked

= p[order]

85
86
87
88
89

q = np.empty_like(ranked)
prev = 1.9
for i in range(n，9，-1):
val = ranked[i-1] * n / i
prev = min(prev, val)
96

<!-- source_page: 97 -->

90
91
92
93

q[i-1] = prev
out = np.empty_like(q)
out[order] = np.clip(q, @, 1)
return out

94

95

|def parse_ga_bins(spec: str) -> List[Tuple[str, float, float

]]:

96
97
98
99
100
101

bins = []
parts = [p.strip() for p in spec.split(",") if p.strip()]
for p in parts:
name, rng = [x.strip() for x in p.split(":"，1)]
if rng.startswith("<="):
upper = float(rng[2:]); bins.append((name, -np.inf
» upper))
elif rng.startswith(">="):
lower = float(rng[2:]); bins.append((name, lower,
np.inf))
elif rng.startswith(">"):
lower = float(rng[1:]); bins.append((name, np.
nextafter(lower, np.inf), np.inf))
elif rng.startswith("<"):
upper = float(rng[1:]); bins.append((name, -np.inf
, np.nextafter(upper, =np.inf)))

102
103
104
105
106
107
108

else:

109

if "=" in rng:

110

a,

b = rng.split("-"，1);

bins.append((name，

float(a), float(b)))
111

else:

112

v = float(rng);

113

return

bins.append((name,

v,

v))

bins

114

115

116
n7

|def

assign_bins(values:

pd.Series,

bins:

List[Tuple[str,

, float]], cat_name="ga_bin") => pd.Series:
labels = []
for v in values.astype(float).values:
97

float

<!-- source_page: 98 -->

ns
119
120
121
122

label = None
for name, lo, hi in bins:
if (v >= 10) and (v <= hi):
label = name; break
1abels. append (label)

123

return

126
127
128
129
130
131
132
133

index=values.index,

name=cat_name

)

124
125

pd.Series(labels,

|def

robust_loc_scale(x:

np.ndarray,

robust:

bool

= True)

134
135
136
137
138
139

|def winsorize(x:

140

if p <= @:

141
142

lo, hi = np.quantile(x, [p, 1-p])
return np.clip(x, lo, hi)

np.ndarray, p: float = 9.61) -> np.ndarray:
return

x

143

144
145

=>

Tuple[float, float]:
x = np.asarray(x, dtype=float)
if x.size == @: return 0.9, 1.0
if robust:
med = float(np.median(x))
mad = float(np.median(np.abs(x - med)))
signa = 1.4826 x mad
if sigma <= le-12:
sigma = float(np.std(x, ddof=1) if x.size > 1 else
1.0)
return med, (sigma if sigma > 8 else 1.0)
mu = float(np.mean(x))
sd = float(np.std(x, ddof=1) if x.size > 1 else 1.0)
return mu, (sd if sd > @ else 1.0)

|def fit_ols(X: np.ndarray, y: np.ndarray) -> np.ndarray:
XtX = X.T @ X

146

ridge

= 1e-8

x np.eye(X.shape[1])

147

beta = np.linalg.solve(XtX + ridge, X.T @ y)

148

return

beta

149

98

<!-- source_page: 99 -->

150

|def design_matrix(df: pd.DataFrame，features:

List[str]) -> np

.ndarray:

151

cols = []

152

for

153

f

in

if

f

154

features:
==

"intercept":

cols.append(np.ones((len(df), 1)))

155

else:

156

if f not in df.columns:

157

warnings.warn(f"[WARN]

填充

158
159
160
161

缺少 特征 列

“{f}'" ， 用

9

。")

cols.append(np.zeros((len(df)，1)))
else:
cols.append(df[[f]].astype(float).values)
return np.hstack(cols) if cols else np.ones((len(df), 1))

162

163
164
165
166

|def find_first_existing(df: pd.DataFrame, candidates: List[str
], default: Optional[str] = None) -> Optional[str]:
for c in candidates:
if c in df.columns: return c
return

default

167

168

|def load_sheets(xlsx_path: str, male_sheet: Optional[str],
female_sheet: Optional(str]) -> Tuple[pd.DataFrame, pd.
DataFrame]:

169
170
171

xls = pd.ExcelFile(xlsx_path); sheets = xls.sheet_names
def _read(sname): return pd.read_excel(xlsx_path,
sheet_name=sname)
mdf = _read(male_sheet) if (male_sheet and male_sheet in
sheets)

172
173
174

175
176

else

None

fdf = _read(female_sheet) if (female_sheet and
female_sheet in sheets) else None
if mdf is None:
for

s

in

sheets:

if " 男 " in s: mdf = _read(s); break
if fdf is None:
99

<!-- source_page: 100 -->

177
178
179
180
181

for s in sheets:
if " 女 " in s: fdf = _read(s); break
if mdf is None or fdf is None:
for s in sheets:
df = _read(s)

182

sex_col

别

= find_first_existing(df，["

性 别 "，“" 胎 儿 性

"，"sex"，"Sex"]，None)
if sex_col is not None:
mdf = df[df[sex_col].astype(str).str.contains(

183
184

" 男 |male|Male"，case=False，regex=True)].copy()

185

fdf = df[df[sex_col].astype(str).str.contains(
" 女 |female|Female"，case=False，regex=True)].copy()

186

break

187

if mdf is None or fdf is None:

188

189

raise

ValueError("
未 能 找到 男 胎 / 女 胎 数据 表 。 请

male-sheet 与 ~--female-sheet 指定
return mdf，fdf

通过

--

。")

190

191

|# -------------

GA parsing

& numeric

cleaning

=—=—=-=========

192 |def _parse_ga_value(val):
193
if val is None or (isinstance(val, float) and np.isnan(val
)): return np.nan
194
if isinstance(val, (int, float)) and not isinstance(val,
bool): return float(val)
195
s = str(val).strip()
196

if

197

s = s.replace(" Ji ¥","w").replace(" %Jil","w").replace(" Ji "

s

==

"":

return

,"w").replace("
198

5

=

np.nan

K","d").replace("W","w").replace("D","d")

re.sub(r"\s+",

ha

s)

199

m = re.match(r"~(\d+)\sxw\+?(\d+)\sxd?$",

200

if

201

w = int(m.group(1)); d = int(m.group(2)); w += d//7; d
%= 7; return float(w) + d/7.0
m = re.match(r"~(\d+)\sxus$", s)
if m: return float(int(m.group(1)))

202
203

s)

m:

100

<!-- source_page: 101 -->

204
205
206
207

mm = re.match(r"~(\d+)\+(\d+)$", s)
if m:
w = int(m.group(1)); d = int(m.group(2)); w += d//7; d
%= 7; return float(w) + d/7.0
m = re.match(r"~(\d+)\syu(\d+)\sxd$", s)

208

if

209
210
211
212
213

w = int(m.group(1)); d = int(m.group(2)); w += d//7; d
%= 7; return float(w) + d/7.0
m = re.match(r"~(\d+)\sxd$", s)
if m: return int(m.group(1))/7.8
m = re.match(r"~(\d+(2:\.\d+)2)$", s)
if m: return float(m.group(1))

214

return

215
216
217

m:

np.nan

|def coerce_ga_weeks(series: pd.Series) -> pd.Series:
parsed = series.apply(_parse_ga_value)

218

n_total

219
220

if n_nan > @:
examples = series[parsed.isna()].astype(str).head(5).
tolist()
warnings.warn(f"[WARN] 有 {n_nan}/{n_total} 条了 孕 周 无法

221

= len(series);

n_nan

=

int(parsed.isna().sum())

解析 ， 例 如 : {examples}")

222
223
224
225
226

return parsed
|def _coerce_num_series(s: pd.Series) -> pd.Series:
if s.dtype == object:
s2 = s.astype(str).str.replace('%',"",regex=False).str
.replace(',","'",regex=False).str.strip()

227

s2

= pd.to_numeric(s2,

errors='coerce')

228

else:

229
230

s2 = pd.to_numeric(s, errors="coerce')
if s2.notna().sum()>@ and ((s2.dropna() > 1).mean() > 0.5)
and (s2.max()<=100):
s2 = s2/198.9
return s2

231
232

101

<!-- source_page: 102 -->

233
234 |# ------------- Batch covariate ------------235 |def add_batch_ohe(df: pd.DataFrame, col: str, max_levels: int
= 20) -> Tuple[pd.DataFrame, List[str]]:
236
if (col is None) or (col not in df.columns): return df, []
237
ser = df[col]
238

try:

239

dt = pd.to_datetime(ser, errors="coerce")

240

except

241

dt

=

None

242

if dt

is

not

243
244
245
246
247
248

Exception:
None

and

dt.notna().any():

base = dt.min()
df["_batch_days"] = (dt - base).dt.days.astype(float)
return df, ["_batch_days"]
vals = ser.astype(str)
top = vals.value_counts().index[:max_levels]
ohe = pd.get_dummies(vals.where(vals.isin(top), other="
_other"), prefix="batch", drop_first=True)
df = pd.concat([df, ohe], axis=1)
return df, list(ohe.columns)

249
250
251
252

|# ===———=-=—-—-

253

|def

Core

calibration

calibrate_and_apply(

254
255
256

male: pd.DataFrame,
female: pd.DataFrame,
chrom_cols: Dict[str,

257

ga_col:

258

bmi_col: Optional[str],

259

subject_col:

260
261
262
263
264
265

qc_features: List[str],
ga_bins_spec: str,
outdir: str,
robust_scale: bool = True,
min_n_bin: int = 25,
winsor_p: float = 0.0,

str],

str,
str,

102

& application 一

<!-- source_page: 103 -->

266
267
268
269

null_family_per_chrom: Dict[str，str] = None,
student_df_per_chrom: Dict[str, Optional[float]] = None,
alpha: float = 0.05,
z_thr: float = 3.0,

270

q_thr:

271

suspect_z:

float

float = 6.19，

float = 9.65，
= 2.5,

272

suspect_q:

273

min_consistency:

274

# Per-chrom

overrides

275

z_thr_map:

Optional[Dict[str, float]] = None,

276

q_thr_map:

Optional[Dict[str,

277
278

min_consistency_map: Optional[Dict[str，int]] = None，
estimate_fpr_with_male: bool = False,

279
280

281

int = 2,
(optional)
float]]

= None,

|):
os.makedirs (outdir,

exist_ok=True)

_setup_mpl()

282

283
284

bins = parse_ga_bins(ga_bins_spec)
male = male.copy(); female = female.copy()

285

286

if ga_col not in male.columns or ga_col not in female.
columns:

287

raise
在

ValueError(f"
孕 周 列 “{ga_col}"

在 数据
表 中 不 存

。")

288

289
290

male["ga_bin"] = assign_bins(male[ga_col], bins, "ga_bin")
female["ga_bin"] = assign_bins(female[ga_col], bins, "
ga_bin")

291

292

feat_list = ["intercept"] + [f for f in qc_features if f
and f != "intercept”]

293

294
295

cal_rows = []
female_rows = []

296

103

<!-- source_page: 104 -->

297

for chrom, colname in chrom_cols.items():

298

if

colname

not

in

male.columns

or

colname

not

in

female.columns:

299

300 |
301

warnings.warn(f"[WARN]

缺少 染色

体 列 “{colname}'，

跳 过 {chrom}."); continue
family = (null_family_per_chrom or {}).get(chrom，"
normal")
df_override = (student_df_per_chrom or {}).get(chrom,
None)

302

303
304
305
306
307

for (bin_name, _, _) in bins:
msub = male[male["ga_bin"] == bin_name].copy()
fsub = female[female["ga_bin"] == bin_name].copy()
if msub.shape[0] < min_n_bin:
warnings.warn(£"[WARN] 男 胎 {chrom}/{bin_name}
样本 数 {msub.shape[8]}“

308

msub

{min_n_bin}，

使 用 全 体

男 胎 代替

= male.copy()

309

310
311
312
313
314
315
316

X_m = design_matrix(msub, feat_list)
y_m = msub[colname].astype(float).values
beta = fit_ols(X_m, y_m)
residm = y_m- X_n @ beta
if winsor_p > 0:
resid_m = winsorize(resid_m, winsor_p)
mue, sigmad = robust_loc_scale(resid_m, robust=
robust_scale)

317

318

# Estimate df for t family if needed

319

df_est

320

if family == “student":

= None

321

if df_override and df_override

322
323

df_est = float(df_override)
elif sps is not None:

324

325

> 1:

try:

df_fit，_，_ = sps.t.fit(resid_m)
104

，")

<!-- source_page: 105 -->

326

if df_fit and df_fit > 1: df_est =
float(df_fit)

327

except

328

Exception:

df_est

329

= None

else:

330

m4 = np.mean((resid_m

-~ np.mean(resid_m))

*%4)

331

v = np.var(resid_m); g2 = m4 / (vs+2 + le
-12) - 3.9

332

if g2 > @: df_est = 6.0 / g2 + 4.9

333

334

cal_rows .append({

335

“chrom":

336
337
338
339
340
341
342
343

“"ga_bin": bin_name,
“n_male_used": int(len(msub)),
"features": ",".join(feat_list),
"beta_json": json.dumps(beta.tolist()),
"mue": float(mue),
"sigmag": float(signma8)，
"null_family": family,
"student_df": df_est

344

chrom,

))

345

346
347
348
349
350

if fsub.shape[@] == 9: continue
X_f = design_matrix(fsub, feat_list)
y_f = fsub[colname].astype(float).values
resid_f = y_f - X_f @ beta
ztilde = (resid_f - mu6) / (sigma@ if sigma@>e
else

1.9)

351

pvals = two_tailed_p_from(ztilde, family=family,
df=df_est)

352
353
354

female_rows.append(pd.DataFrame({
"subject_id": fsub[subject_col].astype(str).
values

if

subject_col

in fsub.columns

105

else

np.arange(len(

<!-- source_page: 106 -->

fsub)) .astype(str)，
355

"chrom":

chrom,

356

"ga_bin":

bin_name,

357
358

"GA_weeks": fsub[ga_col].astype(float).values,
"BMI": fsub[bmi_col].astype(float).values if (
bmi_col

and

359
360
361
362
363
364

bmi_col

in fsub.columns)

else

np.nan,

"y_pred": (X_f @ beta),
"resid": resid_f,
"z": ztilde,
"z_abs": np.abs(ztilde),
"p": pvals

365

m

366

367

cal_df

368

cal_path = os.path.join(outdir, "male_calibration_summary.

= pd.DataFrame(cal_rows)

csv")

369

cal_df.to_csv(cal_path,

index=False)

if len(female_rows)==0:

raise ValueError("
示 生成 女 胎 结果

370

371

【检查
列 名 /数据 是 否 匹 配 ) . ")
372

fem

= pd.concat(female_rows，ignore_index=True)

373

374
375
376

# q-values per (chrom, ga_bin)
fem["q"] = np.nan
for (chrom, bin_name), g in fem.groupby(["chron", "ga_bin"

n:

377 |

idx = g.index.values; fem.loc[idx，"q"] = bh_fdr(g["p"

].values)
378

379 |
380
381

|

# -~------ Sample-level labeling with per-chrom thresholds
se
def get_z_thr(c): return (z_thr_map or {}).get(c, z_thr)
def get_q_thr(c): return (q_thr_map or {}).get(c，q_thr)

382

106

<!-- source_page: 107 -->

383
384

fem["z_thr_used"] = fem["chrom"].map(get_z_thr)
fem["q_thr_used"] = fem["chrom"].map(get_q_thr)

385

386
387
388

def label_row(z_abs, q, zt, qt):
if (z_abs >= zt) and (q <= qt): return "阳性 "
if

(z_abs

>=

suspect_z)

or

(q

<=

suspect_q):

return

”

可 疑 (建议
复 检 )”
389

return

"阴性

"

390

391
392
393
394

fem["label_sample”] = [label_row(a, b, c, d) for a, b, c,
d in zip(
fem["z_abs"].values, fem["q"].values, fem["z_thr_used"
].values, fem["q_thr_used"].values
)]
fem_path = os.path.join(outdir, "female_anomaly_results.
csv"); fem.to_csv(fem_path, index=False)

395

396
397

# -~------ Subject-level aggregation (per-chrom consistency
和 em
def get_k(c): return (min_consistency_map or {}).get(c,
min_consistency)

398

399

subj_rows

400
401

for sid, gsub in fem.groupby("subject_id"):
for chrom, gc in gsub.groupby("chron”):

402

403

=

zt

[]

= get_z_thr(chrom);

qt = get_qg_thr(chrom);

k =

int(get_k(chrom))
pos_hits = gc[(gc["z_abs"]>=zt) & (gc["q"]<=qt)]

404

pos_sgn

= np.sign(gc.loc[gc["z_abs"]>=zt，"z"].

values)

405
406
407

maj = @ if pos_sgn.size==0 else int(np.sign(np.sun
(pos_sgn)))
consistent = (pos_hits.shape[@] >= k) and (np.sum(
np.sign(pos_hits["z"].values) == maj) >= k)
if consistent and pos_hits.shape[e] >= k:
107

<!-- source_page: 108 -->

408 |

lab =“" 阳性 "; t_earliest = float(pos_hits["
GA_weeks"].min())
elif (ge["z_abs"].ge(zt).any()) or (gc["q"].1le(

409

suspect_q) .any()):

410

lab -“

可 疑 (建议
复 检 )"; ridx = int(np.argmax(

gc["z_abs"].values));

t_earliest

= float(gc["GA_weeks"].

values[ridx])
411

else:

412

lab

413

=“"

阴

性 "; t_earliest

= np.nan

subj_rows.append({"subject_id": sid，"chrom":
chrom，"1abel_subject": lab，"earliest_weeks": t_earliest,
"n_samples": int(gc.shape[0]), "
n_pos_hits": int(pos_hits.shape[e]),
"z_thr_used": zt, "q_thr_used":
qt, "consistency_used": k})
subj = pd.DataFrame(subj_rows); subj_path = os.path.join(
outdir, "subject_summary.csv"); subj.to_csv(subj_path, index
-=False)

414
415
416

417

418

# -------

|

Optional

quick

male

FPR estimate

(at current

thresholds) —------

419

fpr_val

420
421
422
423

if estimate_fpr_with_male:
mrows = []
for _, row in cal_df.iterrows():
chrom = row["chrom"]; family = row["null_family"];
df_est = row["student_df"]
msub = male[male["ga_bin"] == row["ga_bin"]].copy

424

= None

()
425

426
427

if

msub.empty:

continue

feat = row["features”].split(","); beta = np.array
(json. loads(row[ "beta_json"]))
X_m = design_matrix(msub,

feat); y_m = msub[

chrom_cols[chron]].astype(float).values
428

resid_m = y_m - X_m @ beta
108

<!-- source_page: 109 -->

429

ztilde_m = (resid_m - row["mud"]) / (row["sigmae"]
if

row["sigma@"]>e

430

else

1.9)

p_m = two_tailed_p_from(ztilde_m, family=family,
df=df_est)

431

mrows .append(pd.DataFrame({

432

"subject_id": msub[subject_col].astype(str).
values if subject_col in msub.columns else np.arange(len(
msub)) .astype(str)，
"chrom": chrom，"ga_bin": row["ga_bin"]，"

433

z_abs":

434

np.abs(ztilde_m),

"p":

p_m

)))

435
436
437
438

if mrows:
mal = pd.concat(mrows, ignore_index=True)
mal["q"] = np.nan
for (chrom, bin_name), g in mal.groupby(["chrom"，
"ga_bin"]):
mal.loc[g.index，"q"] = bh_fdr(g["p"].values)

439
440

msubj_rows

441
442
443

for sid, gsub in mal.groupby("subject_id"):
for chrom, gc in gsub.groupby("chrom"):
zt = get_z_thr(chrom); qt = get_q_thr(
chrom);

= []

k = int(get_k(chrom))

444

pos_hits = gc[(gc["z_abs"]>=zt) & (gc["q"
]<=qt)]

445
446

consistent = (pos_hits.shape[e] >= k)
lab = "阳性 " if consistent else (" 可 疑 ( 建

议 复 检 )” if ((ge["z_abs"].ge(zt).any()) or (gc["q"].le(qt).
any()))

447

else“ 阴 性 ")

msubj_rows.append ({"subject_id": sid, "
chron”: chrom, "label_subject”: lab})

448

msubj

449

if

450

=

not

pd.DataFrame(msubj_rows)
msubj.empty:

fpr_val = float((msubj["label_subject"]=="
阳 性
").mean())

451

|

109

<!-- source_page: 110 -->

452 | 。 ## -一 -一
|

-一

------- Visualizations

————————————————————————

453
454
455

pdf_path = os.path.join(outdir，"figures_report.pdf")
with Pdfpages(pdf_path) as pdf:
# 1) Subject counts by chromosome

456

counts

= subj.groupby(["chrom","label_subject"]).size

().unstack(fill_value=9)
ax = counts.plot(kind="bar"，rot=9)

457
458

for

i,

container

in

enumerate(ax.containers):

459

color = _PRETTY_PALETTE[i % len(_PRETTY_PALETTE)]

460

for

461

bar

in

container:

bar.set_color(color); bar.set_edgecolor("white
本

462
463

_annotate_bars(ax)
ax.set_title("
各 染色 体

464
465

的 个体

级 结论
分 布

ax.set_xlabel("
次 包 体 "); ax.set_ylabel("
人 数 ")
plt.tight_layout(); plt.savefig(os.path.join(outdir,”
chart_subject_label_counts.png"), bbox_inches="tight"); pdf.
savefig(); plt.close()

466

467

# 2) |z| histogram (global) + vertical line at global
|

468

469
470
an
472
473

z_the
plt.figure()

fem["z_abs"].plot(kind="hist", bins=40)
plt.axvline(x=z_thr, linestyle="--", linewidth=1.5,
label=f"4:
Jij @{f z={z_thr}")
plt.legend()
plt.title("
女 胎 样 林 |z| 分 布 "); plt.xlabel("|z|"); plt
.ylabel("
频 数 ")
plt.tight_layout(); plt.savefig(os.path.join(outdir,"
chart_zabs_hist.png"), bbox_inches="tight"); pdf.savefig();
plt.close()

474
475
476

# 3) Earliest weeks boxplot
dfw = subj[subj["label_subject"].isin(["
阳 性 ," 可 疑 ( 建
110

<!-- source_page: 111 -->

议
复 检 )"])]

477
478
479 |

if not dfw.empty and "earliest_weeks" in dfw.columns:
data = [dfw[dfw["label_subject"]=="
阳 性 "]["
earliest_weeks"].dropna().values，
dfw[dfw["label_subject"]=="
可 疑 (建议 复 检 )"
]["earliest_weeks"],dropna()
.values]

480

labels

481
482

plt.figure()
bp = plt.boxplot(data, tick_labels=labels,

= [" 阳 性 "," 可 疑 "]

patch_artist=True)

483
484

for 1, box in enumerate(bp["boxes"]):
box.set_facecolor(_PRETTY_PALETTE[i % len(
_PRETTY_PALETTE)]); box.set_edgecolor("black")

485

plt.title("
首 次 达到 阔 值 的 孕 周 〈 按 最 终结 论 ] ");

486

plt

.ylabel("
孕 周 ( 周) ")
plt.tight_layout(); plt.savefig(os.path.join(
outdir,"chart_earliest_weeks_box.png"), bbox_inches="tight")
; pdf.savefig(); plt.close()

487

488
489

# 4) GA vs |z| scatter per chromosome
for chrom in sorted(fem["chron"].unique(), key=lambda
XXX

490
491
492
493
494
495
496
497
498

int(x))

H

sub = fem[fem["chron”]==chrom].copy()
if sub.empty: continue
plt. figure()
colors = {" 阳 性 ": _pRETTY_PALETTE[2]，"
可 疑 (建议 复
检 )": _PRETTY_PALETTE[1]，" 阴 性 ": _PRETTY_PALETTE[0]}
for lab, dfc in sub.groupby("label_sample”):
plt.scatter(dfc["GA_weeks"]，dfc["z_abs"]，s
=18, alpha=0.85, label=str(lab), c=colors.get(lab,
_PRETTY_PALETTE[@]))
# per-~chrom threshold line
plt.axhline(y=get_z_thr(chrom), linestyle="--",
linewidth=1.5, label=f"zf {if({chrom})={get_z_thr(chrom)}")
plt.xlabel("
孕 周 ( 周 ) "); plt.ylabel("|z|")
111

<!-- source_page: 112 -->

499

plt.title(f"
孕 周 vs |z| ({chrom}

500

plt.legend()

501
s02

号 染色 体 ) ")

plt. tight_layout()
fn = os.path.join(outdir, f"chart_ga_vs_z_chr{
chrom}.png")

503

plt.savefig(fn,

bbox_inches="tight");

pdf.savefig

(); plt.close()
504

505

# ------------- Meta JSON -------------

506

meta

507

suspect_z, “suspect_q": suspect_g,
"min_consistency”: min_consistency,

= {"z_thr":

z_thr,

"q_thr":

g_thr,

"suspect_z":

"winsor_p":

winsor_p,

s08
so9 |
510

“z_thr_map": z_thr_map, "q_thr_map": q_thr_map, "
min_consistency_map": min_consistency_map,
"null_family_per_chrom": null_family_per_chrom, "
estimated_FPR_male": fpr_val}
with open(os.path.join(outdiry"run_mieta_plussjson")，"w"，
encoding="utf-8")

as f:

511
json.dump(meta, f, ensure_ascii=False, indent=2)
s12
513
return fem, subj, cal_df, fpr_val
514
515 |# ------------- Grid scan 一 一 一 ------516 |def grid_scan_thresholds(male: pd.DataFrame，fem: pd.DataFrame
, cal_df:

pd.DataFrame,

517

chrom_cols:
subject_col:

str,

ga_col:

s18
float], consist_grid:
519

str,

z_grid: List[float], q_grid: List[
List[int],
null_family_per_chrom: Dict[str,str])

-> pd.DataFrame:

520
521
322

Dict[str,str],

rows = []
mrows = []
for _, row in cal_df.iterrows():
112

<!-- source_page: 113 -->

3523
524

chrom = row["chrom"]; family = row["null_family"];
df_est = row["student_df"]
msub = male[male["ga_bin"] == row["ga_bin"]].copy()

525

526
3527

if msub.empty:

continue

feat = row["features"].split(","); beta = np.array(
json. loads (row[“beta_json"]))
X_m = design_matrix(msub, feat); y_m = msub[chrom_cols
[chrom]].astype(float).values

528

resid_m

529

ztilde_m = (resid_m - row["mud"]) / (row["signae"] if

= y_m - X_m @ beta

row["signa®"]>@

530

else

1.9)

p_m = two_tailed_p_from(ztilde_m, family=family, df=
df_est)

$31
532

mrows . append (pd . DataF rame ({
"subject_id": msub[subject_col].astype(str).values
if subject_col in msub.columns else np.arange(len(msub)).
astype(

533

str) 的

"chrom":

chrom,

np.abs(ztilde_m),
534
535

"ga_bin":

row["ga_bin"],

"z_abs":

"p": p_m

m
if

536

not

mrows:

warnings.warn("
男 萎 数 据 不 足 ， 无

法 做 姜 值 网 格 扫描 。 ");

return pd.DataFrame()
537

mal = pd.concat(mrows,

538

mal["q"] = np.nan

539

for

(chrom,

bin_name),

ignore_index=True)
g in

mal.groupby(["chrom",

"ga_bin"

]):
540

mal.loc[g.index，"q"] = bh_fdr(g["p"].values)

541

542

543
544
545
546
547

for

zt in z_grid:

for qt in q_grid:
for k in consist_grid:
msubj_rows = []
for sid, gsub in mal.groupby("subject_id"):
for

chrom,

gc
113

in

gsub.groupby("chrom"):

<!-- source_page: 114 -->

548

pos_hits = gc[(gc["z_abs"]>=zt) & (gc[

"q"]<=qt)]
549
550

consistent = (pos_hits.shape[@] >= k)
lab = "阳性 "if consistent else (" 可 疑

"if ((gc["z_abs"].ge(zt).any()) or (gc["q"].le(qt).any()))
else“

阴 性 ")

551

msubj_rows.-append({f"subject_id":

sid,

"chrom": chrom, "label®: lab})
552

msubj

553

fpr = float((msubj["label"]-="
阳 性 ").mean())

= pd.DataFrame(msubj_rows)

if not msubj.empty else np.nan

554
555
556
557

fsubj_rows = []
for sid, gsub in fem.groupby("subject_id"):
for chrom，gc in gsub.groupby("chrom"):
pos_hits = gc[(gc["z_abs"]>=zt) & (gc[
"g"]<=qt)]

s58

sgn = np.sign(gc.loc[gc["z_abs"]>=zt，
"z"].values)

559

maj = 9 if sgn.size==@ else int(np.
sign(np.sun(sgn)))

560

consistent = (pos_hits.shape[@] >= k)
and (np.sum(np.sign(pos_hits["z"].values)==maj) >= k)
lab = "阳性 "if consistent else (" 可 疑

561

"if ((ge["z_abs"].ge(zt).any()) or (gc["q"].le(qt).any()))
else“"

562

阴 性 ")

fsubj_rows.append({"subject_id": sid,
"chrom": chrom, "lapbel": lab})
fsubj = pd.DataFrame(fsubj_rows)
pos_cnt = int((fsubj["label"]=="
阳 性 ").sun())
if not fsubj.empty else 9

5363
364
565

rows.append({"z_thr":

zt, "q_thr": qt,

consistency”: k, "pseudo_FPR_male": fpr, "
female_positive_count": pos_cnt})
566
567

return

pd.DataFrame(rows)

|

114

"

<!-- source_page: 115 -->

568
569
570
571
572

|# ------------- CLI ------------|def build_argparser():
p = argparse.ArgumentParser(description="Q4 Transfer++")
p.add_argument("--xlsx"，type=str，required=True)
p.add_argument("--male-sheet"，type=str，default=None)

573

p.add_argument ("--female-sheet",

type=str,

574
3575

p.add_argument("--col-subject"，type=str，default=None)

576

p.add_argument("--col-ga",

577
578
579
580

p.add_argument("--col-bmi"，type=str，default=None)
p.add_argument("--col-z13", type=str, default=None)
p.add_argument("--col-zl8"，type=str，default=None)
p.add_argument ("--col-z21", type=str, default=None)

type=str,

default=None)

default=None)

581

582
583 |
584

|

p.add_argument ("--qc-features”, type=str, default="GA,BMI,
reads,align_rate,dup_rate, unique_reads,gc")
p.add_argument("--ga-bins", type=str, default="Early:<c=14,
Mid:14-22,late:>22")
p.add_argument("--outdir"，type=str，default="

out_q4_transfer_final")
585
586

p.add_argument("--robust-scale"，action="store_true")

587

p.add_argument("--standard-scale”,

588

action="store_false")
p.set_defaults(robust_scale=True)

dest="robust_scale",

589

590

p.add_argument("--student-chron”,
help= "逗号 分 隔 ， 需 要 用 t

591

分 布

type=str, default="21",

的 染色 体 (默认

21)

")

p.add_argument("--winsor", type=float, default=0.01, help=
"对 男 胎 残

差 的 截 尾 比例 (如

9.61

表示

1%)

")

592
593

p.add_argument ("--batch-col”,

|

594
595

="
批 次 列 名 (检测
日 期 /批号 等 ) ;

type=str,

default=None,

自动

化 或 one-Hot)

数值

help

")

p.add_argument("--batch-max-levels", type=int, default=20)
|

115

<!-- source_page: 116 -->

596
597
598

p.add_argument("--alpha", type=float, default=0.5)
p.add_argument ("--z-thr", type=float, default=3.0)
p.add_argument ("--g-thr", type=float, default=0.05)

599

p.add_argument("--suspect-z",

type=float,

default=2.5)

600

p.add_argument("--suspect-q",

type=float,

default=0.10)

601

p.add_argument ("--min-consistency”,

type=int,

default=2)

602

603
604
605
606
607

# Per-chromosome overrides
p.add_argument ("--z-thr-13", type=float, default=None)
p.add_argument("--z-thr-18"，type=float，default=None)
p.add_argument("--z-thr-21"，type=float，default=None)
p.add_argument("--q-thr-13"，type=float，default=None)

608

p.add_argument("--9q-thr-18"，type=float，default=None)

609
610
611
612
613

p.add_argument("--q-thr-21"，type=float，default=None)
p.add_argument("--consist-13"，type=int，default=None)
p.add_argument("--consist-18"，type=int，default=None)
p.add_argument("--consist-21"，type=int，default=None)

614

p.add_argument("--grid-scan”,

运行
615

|

616

|

action="store_true",

help="

国 值 网 格 扫描 并 输出 FPR 表 ")

p.add_argument("--grid-z"，type=stri

default="

2.6,2.8,3.0,3.2")
p.add_argument("--grid-q",

type=str,

default="

©.03,0.05,0.08")
p.add_argument("--grid-consist”, types=str, default="2,3")
p.add_argument("--target-fpr", type=float, default=0.e1,
help="
目 标 FPR (Ji Fik #¥ #E % ® 0i) ")

617
618
619

return

p

620

621

622
623
624 |

|def

auto_map_columns(df:

pd.DataFrame,

overrides:

Dict[str,

oOptional[str]]) -> Dict[str, Optional[str]]:
cand = {
"subject_id": [" 孕 妇 代码 "，" 受 坛 者 ID"，"subject_id"，"
ID"，" 编 号 "]，
"GA":

[" 检 测

孕 周 "，“ 检 测

116

孕 周 数 "，“" 孕 周 "， "GA",

"gw

，“

<!-- source_page: 117 -->

GA_weeks"],
"BMI": ["
孕 妇 BMI"，“
孕 妇 BMI
指 标 "，"BMI"]，
"reads": [" 原 始 读 段 数 ( 估 )"，" 原 始 读 段 数 "， "reads"，”

625 |
626

|

total_reads"],

627 |

"align_rate": [" 在 参考 基因 组 上 比 对 的 比例 "，" 比
对 率
"，”
align_rate"],
“dup_rate": [" 重 复读 段 的 比例 "，" 重 复读
数 比例 ”， "EHEFE

628
|

",

629

"dup_rate"],

"unique_reads™:
unique_reads"]，

[" 叭 一 比 对 的 读

段 数 "，“" 叭 一 比 对 读数

630

"gc":

["6CAM",

631

"z13":

["13 号 染色 体 的 z 值

"，"z13_prime"，"Z13"，"Z13 "

"z18":

["18%
M«f4 (KR9Z(H",

"218_prime",

"Z18",

"218'"

"z21":

["21 号 染色 体 的 z 值

"，"z21_prime"，”Z21%

"z21'"

|
632

"6C",

"gc"],

1.

|

|
633 |

1.
]，

634
635
636

}
out: Dict[str, Optional[str]] = {}
for key, cands in cand.items():

637

override

638

out[key] = override if override
((c

639
640
641

642
643
644
645
646

for

c in

= overrides.get(f"col_{key.lower()}")
cands

is not None else next

if c in df.columns),

None)

return out
|def

main():

ap = build_argparser();

args = ap.parse_args()

male, female = load_sheets(args.xlsx,
args.female_sheet)

args.male_sheet,

647

merged_cols = pd.Index(male.columns).union(pd.Index(female
.columns))
df_for_map = pd.DataFrame(columns=merged_cols)

648

overrides

=

{

n7

"，”

<!-- source_page: 118 -->

649

"col_subject":
, "col_bmi":

650

col_z21":

}

652

auto

args.col_ga

args.col_bmi,

"col_z13":

651

args.col_subject，"col_ga":

args.col_z13,

"col_z18":

args.col_z18, "

args.col_z21

= auto_map_columns(df_for_map，overrides)

653

654

# Rename

655

rename_map_m

656

for std, real in auto.items():

657

if

658
659

real

= {};
is

not

rename_map_f

= {}

None:

if real in male.columns: rename_map_m[real] = std
if real in female.columns: rename_map_f[real] =
std

660

male = male.rename(columns=rename_map_m); female = female.
rename(columns=rename_map_f)

661
662

#

663

if "GA" in male.columns: male["GA"] = coerce_ga_weeks(male

664
665
666
667

GA

to

weeks

["GA"])

if "GA" in female.columns: female["GA"] = coerce_ga_weeks(
female["GA"])
# Coerce numerics
for name in [auto.get('align_rate'), auto.get('dup_rate'),
auto.get('ge'),

668

auto.get('reads'),

auto.get('unique_reads'),

auto.get('BMI')]:
669
670

for

df_

in

if name

(male,
and

female):
(name

671
672
673
674

# Batch covariate
added_batch_feats = []

675

if args.batch_col:

in df_.columns):

df_[name] = _coerce_num_series(df_[name])

ng

<!-- source_page: 119 -->

676

male，feats_m = add_batch_ohe(male, args.batch_col,
max_levels=args.batch_max_levels)

677
678

female, feats_f = add_batch_ohe(female, args.batch_col
, max_levels=args.batch_nax_levels)
added_batch_feats = sorted(set(feats_m) | set(feats_f)
)

679

680
681

682
683 |
684
685

# Build QC features
qc_feats

= [x.strip()

for

x in

(args.qc_features

or

"").

split(",") if x.strip()]
if ("6A" not in qc_feats) and ("GA" in male.columns or "GA
”in female.columns): qc_feats.insert(0,"GA")
if ("BMI" not in qc_feats) and ("BMI" in male.columns or "
BMI" in female.columns): qc_feats.insert(1,"8MI")
qc_feats = [f for f in qc_feats if f] + added_batch_feats
if "intercept" in qc_feats: qc_feats.remove("intercept")

686
687

688
689
690
691

#

Chrom

columns

chrom_cols = {"13":"Z13","18":"Z18","21":"221"}
missing_any = [v for v in chrom_cols.values() if (v not in
male.columns or v not in female.columns)]
if len(missing_any)>@:
warnings.warn(f"[WARN] Z 列 缺 失: {missing_any}。 请 用
--col-213/--col-z18/--col-z21 指定 。")

692

693
694

# Subject id
subject_col = "subject_id" if "subject_id" in female.
columns

or

subject_id")

695
696

"subject_id”
or

in male.columns

(auto.get("

if subject_col not in male.columns: male[subject_col] = np
.arange(len(male)).astype(str)
if subject_col not in female.columns: female[subject_col]
= np.arange(len(female)).astype(str)

697

698

else

"subject_id")

# Null

family

per

chrom

119

<!-- source_page: 120 -->

699
700
701

student_set = set([s.strip() for s in (args.student_chrom
or "").split(",") if s.strip()])
null_family_per_chrom = {c: ("student” if c in student_set
else "normal") for c in chrom_cols.keys()}
student_df_per_chrom = {c: None for c in chrom_cols.keys()
}

702
703

# Per-chrom thr maps (fallback to global)

704

z_thr_map

705

"13": args.z_thr_13 if args.z_thr_13 is not None else
args.z_thr,
"18": args.z_thr_18 if args.z_thr_18 is not None else

706

= {

args.z_thr,

707

"21": args.z_thr_21 if args.z_thr_21 is not None else
args.z_thr,

708

}

709

q_thr_map

710

= {

"13": args.q_thr_13 if args.q_thr_13 is not None else
args.q_thr,

71
712

"18": args.q_thr_18 if args.q_thr_18 is not None else
args.q_thr,
"21": args.q_thr_21 if args.q_thr_21 is not None else
args.q_thr,

713
714
715
716

}
min_consistency_map = {
"13": args.consist_13 if args.consist_13 is not None
else args.min_consistency,
"18": args.consist_18 if args.consist_18 is not None
else

args.min_consistency，

717

"21": args.consist_21 if args.consist_21 is not None
else args.min_consistency,

718

}

719

720

fem，subj，cal_df

721

male=male,

fpr_val = calibrate_and_apply(

female=female,

120

chrom_cols=chrom_cols,

<!-- source_page: 121 -->

722

ga_col="GA",
or

723

724
725
726

"BMI"

bmi_col=("BMI" if "BMI" in female.columns

in male.columns

728
729

None),
qc_features=qc_feats,

ga_bins_spec=args.ga_bins,
outdir=args.outdir, robust_scale=args.robust_scale,
min_n_bin=25, winsor_p=args.winsor,
null_family_per_chrom=null_family_per_chrom,
student_df_per_chrom=student_df_per_chron,
alpha=args.alpha, z_thr=args.z_thr, q_thr=args.q_thr,
suspect_z=args.suspect_z,

727

else

subject_col=subject_col,

suspect_g=args.suspect_q,

min_consistency=args.min_consistency, z_thr_map=
z_thr_map, q_thr_map=q_thr_map, min_consistency_map=
min_consistency_map,
estimate_fpr_with_male=False
)

730

71
72
7T33
734

# Ensure male has GA bins for grid scan
if 'ga_bin' not in male.columns and 'GA' in male.columns:
male = male.copy()
male['ga_bin'] = assign_bins(male['GA'], parse_ga_bins
(args.ga_bins))

735

736
737
7T38
739
740
741

# Grid scan if requested
if args.grid_scan:
z_grid = [float(x) for x in (args.grid_z or "").split(
",") if x.strip()]
q_grid = [float(x) for x in (args.grid_q or "").split(
",") if x.strip()]
k_grid = [int(x) for x in (args.grid_consist or "").
split(",") if x.strip()]
grid = grid_scan_thresholds(male, fem, cal_df,
chrom_cols,

742

subject_col,

"GA",

z_grid,

q_grid,

k_grid,

null_family_per_chrom)
grid_path = os.path.join(args.outdir, "fpr_grid.csv");
grid.to_csv(grid_path,

index=False)

121

<!-- source_page: 122 -->

743

gsel = grid[(grid["pseudo_FPR_male"].notna()) & (grid[
“pseudo_FPR_male"] <= args.target_fpr)].copy()
if not gsel.empty:

744

745

best = gsel.sort_values(["female_positive_count”,"
z_thr","consistency”], ascending=[False, True, True]).head
|

(1)

|

best. to_csv(os.path. join(args.outdir, "
fpr_grid_best.csv"), index=False)

746
747

748
749
750
751

# Print overall with deprecation-safe groupby
subj_overall = (
subj.groupby ("subject_id")["label_subject"]
.apply(lambda labs:“" 阳 性 " if "Ff" in set(labs)

752

else

(" 可 疑 (建议
复 检

)”if any(str(x).

753
754
755
756
757

startswith("
可 疑 ") for x in labs)
else“" 阴 性 "))
.reset_index(name="overall")
)
cnts = subj_overall["overall”].value_counts().to_dict()
print("[DONE] 个 体 总 体 结论 : *, cnts)

758

print(f"[INFO]

图 表 已 输出 至 飞 args.outdir}，

并 汇总 到

figures_report.pdf")
759

760

if args.grid_scan:

print(F"[INFO] 已 生成 fargs.outdir}/fpr_grid.csv (与
fpr_grid_best.csv， 如 可 用 ) ")

761

762
763

|if __name__ == "_main__":
main()

122
