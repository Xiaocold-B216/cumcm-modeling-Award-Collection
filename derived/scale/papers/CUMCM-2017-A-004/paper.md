# Extracted Paper

<!-- source_page: 1 -->

CT 系统 标定 与 图 像 重 建

摘

要

为 解决 CT 系统 参数 标定 及 成 像 问题 ， 本 文 由 相关 理论 基础 入 手 ， 剖 析 模 板 形 态 学 特
征 ， 以 此 为 切入 点 建立 并 优化 了 标定 模型 ， 并 且 对 根据 未 知 介质 进行 图 像 重 建 ， 根 据 图 形
特性
实现 了 噪声 去 除 。
针对 问题 一 ， 我 们 根据 基础 理论 知识 ， 结 合 几 何 计算 ， 得 出 标定 模型 在 各 个 照射 角度
中 的 投影 强度 表达 式 ， 尝 试 通过 函数 拟 合 的 方法 求解 。 在 扫描图 中 ， 圆 和 椭圆 的 投影 函数
相互 耦合 ， 为 了 更 好 的 将 其 区 分 开 ， 我 们 从 图 像 处 理 的 角度 入 手 ， 通 过 高 通 滤 波 和 形态 学
操作 大 致 提取 出 椭圆 曲线 边界 ， 利 用 其 宽度 信息 粗略 求 出 各 次 投影 的 角度 。- 再 利用
粗测 的
角度 ， 计 算出
圆 的 轨迹 ， 控 去 受 圆 形 投影 影响 的 数据 点 ， 以 此 来 消除 圆 的 投影 函数 对 椭圆
投影 函数 的 影响 ， 用 剩 下 的 数据 对 覃 圆 投影 曲线 进行 拟 合 ， 得 到 了 很 好 的 效果 ， 以 较 高 的
精度 精确 计算 出 X 光 各 次 照射 角度 及 其 他 标定 相关 的 参数
针对 问题 二 、 三 ， 考 虑 到 逆 Radon 变 化 的 卷 积 特性 ， 首 先 使 用 线性 插值 得 到 新 的 图 像
作为 着 Radon
变 换 的 输入 ， 再 经 由 坐标变换 ， 内 插 缩 放 、 滤 波 变换 等 操作 得 到 最 终 的 介质
吸收
率 分 布 图。
针对 问题 四 ,模型 检验 部 分 ， 我 们 从 误差 理论 角度 进行 分 析 ， 研 究 标定 模型 的 敏感 性 ，
并 尝试 大 为 引入 噪声 ， 验 证 模型
的 稳定 性 。 在 研究 过 程 中 我 们 发 现 了 原 定 标 模型 在 特定 角
度 附 近 精 度 大 幅 下 降 的 问题 ， 针 对 该 问题 ， 尝 试 设计 出 “三 角形 ”标定 模板 等 若干 种 模板 ，
最 终 兼顾 合理 性 及 稳定 性 ， 确 定 “ 双 李 圆 ”模板
作为 新 标定 模板 ， 从 理论 上 证 明 其 稳定 性
优
于 原 模版 。
关键 词 CT 系统

、Radon
变 换 、 图 像 处 理 、 最 小 二 乘 拟 合 、 插 值 、滤 波

1

<!-- source_page: 2 -->

1

问题重 述

1.1 “问题 背景
X 射 线 是 一 种 能 够 穿 透 物体 的 能 量 射线 ， 并 会 产生 衰减

、 折 射 、 散 射 等 物理 现象 。 计
技 术 依 据 X 射 线 穿 过 待 测 物体 发 生 吸收 衰减 的
算 机 断层 成 像 (Computed Tomography，CT)
原理 ， 可 以 在 不 破坏 物体 内 部 结构 的 情况 下 对 其 进行 三 维 可 视 化 成 像 。CT 技 术 作 为 一 种
重要 的 无 损 检测 技术 ， 广 泛 应 用 于 医学 成 像 、 工 业 探伤 、 货 运 安检 以 及 文物 复原 等 领域 。
CT 技术 的 发 展 大 致 经 历 四 个 阶段 : 第 一 代 CT 设 备 通过 平行 束 平移 旋转 扫描 获得 投影
数据 ， 第 二 代 设 备 使 用 小 角度 遍 形 射线 束 代 替 平 行 束 ， 第 三 代 设备 仅 包 含 扇形 束 的 旋转 扫
描 动作 ， 不 再 采用 平移运动 ， 第 四 代 设 备 将 探测 器 固定 于 360* 圆 周 上 ， 仅 旋转 X 射 线 源 以
解决
环形 伪 像 问题 。 由 于 被 测 物 与 扫描 环境 的 复杂 性 ，CT 扫 描 方式 日 趋 灵 活 。
CT 技术 快速 发 展 ， 对 CT 设备 的 精密 度 要 求 随 之 提升 。 由 于 安装 过 程 中 存在 误差 ， 实
际 的 CT 成 像 系统 不 满足 理想 成 像 关系 ， 会 使 断层 图 像 的 重建 质量 受到 影响 因此 ， 使
用 CT 系
统 前 需要 借助 已 知 结构 的 样品 进行 标定 ， 修 正安
装 误差 。

1.2 ”相关 信息
和 典型 初代 二 维 CT 系统 如 图 ?? 所 示 , 探 测 器 平面 由 512 个 等 距 接收 点 组 成 ，X 射
线 垂直
入 射 。 发 射 器 与 探测 器 相对 位 置 固定 不 变 ， 探 测 系统 绕 固定 旋转 中 心 逆 时 针 旋 转 180 次 。 对
每 一 个 X 射 线 方向 ,探测 器 测量 经 位 置 固定 不 动 的 二 维 待 检测 介质 吸收 衰减 后 的 射线 能 量 ，
并 经 过 增益 等 处 理 后 得 到 180 组 接收 信息 。

S1

S2

Sa

S4

S512

图 1: CT 系统 示意 图

2

<!-- source_page: 3 -->

1.3 ” 需 解决
的 问题
本 文 将 题 述 问题 归结

为 以 下 三 个 部 分 ， 建 立 数学 模型 进行 分 析 研 究 。

问题 一 : 参数 标定
根据 标定 模板 的 几何 形状 与 附件 1 给 出 的 吸收 强度 ， 以 及 附件 2 给 出 的 探测 器 接收 信
息 ， 标 定 CT 系统 的 相关 参数 ， 包 括 旋转 中 心 的 位 置 、 探 测 器 单元 间距 、X 射 线 的 180 个 投
射 角度 。
问题 二 、 三 : CT 成 像

利用 已 标定 的 CT 系统 参数 ， 结
合 附件 3、 附 件 5 给 出 的 未 知 介质 接收 信息 进行 成 像 ， 确
定 未 知 介质
的 位 置 、 几 何 形状 与 吸收 率 等 信息 ， 并 具体 给 出 附件 4 所 给 位 置 的 吸收 率 。
问题 四 : 模型
分 析 与 改进
分 析 问 题 一 中 参数 标定 的 精度
改进 。

与 稳定

2

性 ， 自 行 设 计 新 模板 、 建 立 对 应 标定 模型

以做 出

问题分 析

本 问题 主要 研究 CT 系统 的 参数 标定 与 成 像 。 首 先 通 过 投影 信息 确定 X 射 线 入 射 角度 及
探测
器 单元 间距 ， 通 过 图 像 重 建 确定 旋转 中 心 位 置 ， 完 成 系统 参数标定 ， 其 次 由 投影信息
直接 重建 图 像 ， 获 取 未 知 介质 信息 ;最 后 分 析 参 数 标定 的 精度 与 稳定 性 ， 设 计 新 模板并 建
工 标 定 模型 。
2.1

”问题 一

分
析 问 题 一 ， 建 立 投影 强度 曲线 的 数学 模型 。 首 先 分 析 椭 圆 投影 宽度 随 X 射 线 角 度 的
变化 规律 ， 以 粗略 确定 各 入 射 角度 及 旋转 中 心 。 在 各 入 射 角度 对 应 的 投影 强度 曲线 中 ， 通
过 图 像 重建 去 除 圆 形 模板 影响 的 点 位 ， 拟 合 椭圆 投影 强度 曲线 ， 求 解 增益 系数 、 探测 器 单
元 间距 、 入 射 角度
的 关系 。 其 次 在 原 强度 曲线 中 ， 扣 除 椭圆 投影 的 影响 ， 得 到 180
组 精确
的 圆 形 投影 强度 曲线 。 拟 合 圆 形 投影 强度 曲线 ， 通 过 投影 宽度 求解 探测 器 单元 间距 ， 从 而
精确 求解 增益 系数 与 X 射 线 入 射 角度 。 最 后 通过 图 像 重 建 ， 确 定 旋转 中 心 位 置 。

3

<!-- source_page: 4 -->

2.2

”问题 二 、 三

CT 系统 的 工作 原理 是 由 投影 重建 图 像 ， 针 对 平行 束 系统 的 重建 算法 包括 直接 反 投 影
法 、 滤 波 反 投 影 法 、 卷 积 反 投影法 等 ， 相 关 文 献 中 已 有 详细 论述 。 针 对 问题 二 应 以 投影 信
息 与 标定 所 得 系统 参数 作为 输入 ， 通 过 逆 Radon 变 换 重 建 图 像 ， 并 对 图 像 进行 滤波 去 噪 处
理 ， 以 得 到 未 知 介质 的 信息 。
2.3

”问题 四

分 析 问 题 一 中 参数 标定 的 精度 与 稳定 性 ， 针 对 确定 9 取 值 时 所 用 的 arccosb 函 数 在 极 值
点 附近 对 误差 的 敏感 性 进行 改进 。 提 出 以 斜 45* 椭 圆 代替 圆 形 的 新 模板 ， 建 立 相 应 标定 模
型 ， 对 其 精度 与 稳定 性 进行 评估 。

3
3.1

3.2

”假设
与 符号

“模型 假设

1.

入 射 的 X 射 线 完全

平行 ， 忽 略 相互干涉 。

2.

探测 器 单元 阵列 与 二 维 待 检测 介质
生 的 倾斜 。

3.

附件 所 给 接收 信息 均 为 精确 值 。

处 于 同一 平面 中 ， 忽 略 载 物 台 在 任意 角度 可 能 发

”符号说 明

4 ， 模型 建立 与 求解
4.1

CT 成 像 的 理论 基础

又 射线 与 物质 的 相互 作用
当 X 射 线 照射 在 被 检测 物体 上 时 ， 一 部 分 射线 能 量 被 物体 吸收 ， 使 得 射线 强度 发 生 衰
减 。 其 衰减 遵循 Lambert-beer
吸 收 定律 中 ， 呈 指数 变化 。 如 图 ?? 所 示 ， 设 X 射 线 初 始 强度
为 矶 ， 穿 过 厚度 为 z， 吸 收 系数 为 /的 均匀 介质 后 强度 变 为 [， 则 有 :

I=TIe*

(1)

HZ 一-了
7 了

2
(2)

4

<!-- source_page: 5 -->

符号

符号 说 明

Ad

0;
a
b
R
D
JJ
9(s,0)

探测

投影

单位

器 单元 间距

mm

第 ;组 X 射 线 的 入 射 方向
[HEESS]
顶 圆半 短 轴
圆 半径
椭圆 投影 宽度
吸收
率 函 数 ， 表 示 介 质 吸 收 强度 的 分 布
函数 ， 表 示 计 算 所 得 的 投影 强度 值 ，s 为 真实 投影

rad
mm
mm
mm
mm

坐标

h(l,6)
k
各

采样

函数 ， 表 示 探 测 器 采样 数据 拟 合 所 得 曲线 ，] 为 像
素 坐 标 ， 为 真实 投影 长 度 的 1At 倍
增益 系数 ， 探 测 器 接收 信息 与 投影 强度 的 比值
比例 系数 ， 表 示 由 采样 信息 重建 的 图 像 与 吸收 率 数据
的 比值

mm~!

表 工 符号说 明
对 于 二 维 平面 内 的 不 均匀 介质 ， 吸 收 系数 表示 为 厚度 z 的 函数 wW(z)， 此 时 Lambert-beer吸
收 定律 表示 为 :
/om

一 2

式 ?? 表 明 ，X 射 线 穿 过 物体 后 的 射线 强度 与 被 检测 物体 的 吸收 系数 相关
理 本 质 就 是 通过 探测 器 接收 的 强度 信息 计算 吸收 系数 /的 分 布 。

(3)

，CT
成 像的物

数据
意义 的 分 析 解释
相关 文献 显示 ， 探 测 器 接收 的 投影 信息 应 与 吸收 系数 HK(Z) 沿 投影 方向 的 线 积分 成 正
比 ， 现 有 图 像 重 建 算法 均 以 此 为 前 提 。 针 对 本 题 所 给 数据 ， 分 析 附 件 1 可 知 标定 模板 吸收
率
处 处 相同 ; 将 附件
2 中 同一 入 射 角度 对 应 的 全 部 接收 值 求 和 《如
图 ?? 所 示 )， 可
见 接收 值
总 和 基本 保持不 变 。 可 以 认为 ， 本 题 所 给 数据 存在 类 似 关 系 ， 即 探测 器 接收 信息 与 吸收 率
函数 帮 z, 妇 沿 X 射 线 入 射 方向 的 线 积分 〈 即 投影 强度 ) 成 正比 :

/ Je 有 = EL
式 中 心 凡, 9) 为 探测 器 接收 信息 ，jz, 人 为 介质 的 吸收 率 分 布 ， 人 为 增益 系数 。

5

四

<!-- source_page: 6 -->

H

7

I,
xX

图

=

2:

Lambert-beer

吸 收

定律

示意

As

x104

y

示 1241

std=1.8565

AN
1

到 全

图

aaaivirawRIAe

的

9

AN
SY4
\

SN

2
全

) N

Treeoa

\

可 1238
1.237

NAN Te

SN
pP

1.236

L\ \Y

2

0

30

60

9
测 次

120

150

180

x

NS

adeot

*

图 4:

图 3: 各 次 测量 的 接收 值 总 和

接收 信息 分 析 示 意图

Radon
变 换

吸收
率 函 数 扩 rz;, 沿 4 方向 的 投影 函数 为 凡 (b,)《〈 如 图 ?? 所 示 )， 由 0 ?组 成 的 极 坐标系
统 张 成 Radon
空 间 ， 空 间 中 任意 点 (4 邹 的 值 实际 上 代表 吸收 率 函数 的 一 个 线 积 分 值 。
物体 空间 的 吸收 率 函 数 帮 z, 切 与 Radon 空 间 的 投影 函数 (1, 人 有 明确 的 映射 关系 ， 通 常
将 物体 空间 函数 变换 至 Radon 空 间 函 数 的 过 程 称 为 Radon 变 换 ， 反 之 称 为 着 Radon
变 换。实
际 上 ，Radon 空 间 的 函数 值 是 CT 系统 中 探测 器 采集 的 一 个 数据 点 ， 只 要 有 充分
的 扫描 数
据 ， 就 可 以 通过 插值 方式 重建 物体 空间 的 图 像 。
4.2

问题 一

首先 建立 投影 强度 模型 ， 分 析 强 度 曲线 线 型 的 影响 因素 ， 可 知 标定 参数 的 核心 问题 在
于 入 射 角度 的 确定 。 模 型 求解 部 分 从 数据 图 像 的 形态 学 角度 出 发 ， 粗 略 确定 X 射 线 的 入 射
角度 ， 从 而 分 离 覃 圆 与 圆 形 模板 的 投影 强度 ， 通 过 拟 合 投影 函数 标定 CT 系统 各 参数 值 。
6

<!-- source_page: 7 -->

N\

SN

AAA

人 NS
2(s,0)

hY

人

NM

1

图 5:
4.2.1

，

吸收 率 函 数 及 其 投影 函数

“投影
强度 模型 的 建立

记 第 ;组 X 射 线 入 射 方向 与 正方 形 托盘 紧 直 轴 的 夹 角 为 4， 探 测 器 位 于 托盘 正 下 方 时 0 为 0，
以 道 时 针 方向为 正 。 记 旋转
中 心 为 0 点 ， 在 探测 器 平面 的 投影 点 为 0%， 以 此 为 原点
建立 投
影 强度 坐标 轴 【如
图 ?? 所 示 )， 表 示 物 体 空 间 的 真实 投影 坐标 ， 单 位 为 mm。 记 椭圆 中 心

为 0,， 圆 形 中 心 为

00，Z0;00, 二 ao0|

= 由

，/0200。 =

，|00:| =

心 ， 则 O,，

O: 在 So 轴 上 的 投影 为 :

50,(8) = 4isin(al 一 外

(5)
(6)

502(0) = Apsin(az — 6)
首先

建立 椭圆 的 投影 强度 模型 。 以 椭圆
中 心 为 基准 ， 计 算 吸 收 率 的 线 积分 值 可 得 :

，，

4a2?

fls

0)=y

本

— (a2 sin20 + b2 cos? 9)2°

1a2?
二 a2sin’

+ b2 cos? f

M

402 了 2

(8)

于 是 在 so 轴 中 ， 有

91(5,0) = 1(s — 50,.)
一

加

四

4a20?

四

(a2sin20 + b2 cos?

2

So

7

二 a2sin20 + b2 cos? §

<!-- source_page: 8 -->

0.0)"
od)

忆

5

R0,(0,)

a

5(0)

ie
|
| wao |

AN
$O:

EN

人 和 AL 和、|

图 6: 投影 强度 坐标 系
由 增益

系数 上 与

探测 器 单元 间距 Ad 的 定义 可 得 :

hy(1,8)
= oa(LAd'O)
AG2W2EAAG?

本

为 方便 表述 ， 记

so

Sin20 + b2 cos? Da

，

加 Ad)

4a202 大 2

(9)

二 a2sin20 十 刀 cos20

由
1

(a2sin20 十 刀 cos20)2

da2b?k?
CQ

-

a? sin2

0 十

b? cos?

0

则有
So

且 O = RU 一 AD) +Cn

(10)

由
式 ?? 可 见 ， 当 0 确定 时 ， 采 样 函数 Mg) 的 平方 为 的 二 次 曲线 。
借助

以 上 对 于 椭圆 投影 强度 模型

的 分 析 ， 令 o = b = 丸 即 可 得 到 圆 形 投影 强度 模型 ;

Ky = —412Ad
Ce = 4R%?
尼 (D) = Ky(l — 和 六 十 Cs

8

(11)

<!-- source_page: 9 -->

4.2.2

”投影
强度 模型 的 求解

形态
学 粗 测 入 射 角度 、 旋 转 中 心 以 及 探测 器 单元 间距
椭圆 模板 的 投影 宽度 刀 可 由 X 射 线 入 射 角度 唯一 确定 〈 如 图 ?? 所 示 )， 其 计算 公式 为 站]:
2vm?a® + b?
万 = 一 Ta

.
(12)

其 中 思 为 切线斜率 ， 由 此 得 到 入 射 角度 的 计算 公式 为 :
0 一 arcot/

DA

(13)

N

了
SS

<

和 人

，

A
N

29)

150
200
250

|

»

交 NR2

和

NO
7e

20

40

60

B80

100

120

140

160

180

、
图 7: 顶 圆 投影 宽度 示意 图

图 8: 顶 圆 投影 宽度 粗 测 用 图

通过 分 析 探 测 器 接收 信息 ， 将 椭圆 投影 像素 宽度 的 极 大 值 作为 长 轴 的 估计 值 ， 估 算 控
测 器 单元 间距 Ad 以 及 每 一 投影 角度 对 应 的 真实 投影 宽度 ， 从 而 粗略 测算 180 个 入 射 角度 的
取值 。
求解
结果 如 图 ?? 所 示 ， 可 近似 认为 入 射 角度 线性 增加 。 以 等 距 分 布 的 入 射 角 对 探测 器
接收 信息 作 逆 Radon
变 换 ， 所 得 图 像 的 中 心 位 置 即 为 旋转 中 心 。 以 椭圆中 心 、 圆 形 中 心 与
旋转 中 心 为 顶点 构造 三 角形 ， 利 用 其 在 两 幅 图 像 中 的 相似 性 即 可 粗略 确定 旋转 中 心 在 正方
形 托盘
中 的 位 置。
分 离 提取 投影 强度 曲线
圆 形 投影

中 心 位 置 的 确定

”粗略 测算 入 射 角度 及 旋转 中 心 后 ， 可 估算 每 一 强度 曲线 中
9

<!-- source_page: 10 -->

250

粗 测 的 角度
医生

0
~150

起

ar

_末

ae

要 1o0

0

50 [一

%

em

30

了

60

图 9:

90

120

150

180

入 射 角度 粗 测 数据 图

1e

Va"

20 上

/

A\

到

IT

一

| 人
|
|

地

\

80
90

一

/
\

/
SS

图 10: 重建 图 像 〈 左 ) 与 原始图 像 〈 右 )
圆 形 投影 的 中 心 位 置 。
如
图 ?? 所 示 ， 圆 心 投 影 位 置 应 满足 关系 式 :

1 = lycos(0
+ a) + Lo

(14)

式 中 1 为 旋转 中 心 至 圆心 的 像素 长 度 ，o 为 图 ?? 中 三 角形 的 一 个
内 角 ， 均 可 由 重建
图 像估
算 。Zo 为 旋转 中 心 对 应 的 投影 像素 坐标 ， 可 将 椭圆 投影 宽度 的 极 小 点 近似 作为 0 = 0 的 情
形 进行 估算 。
模板 投影 强度 曲线 的 分 离 拟 合 ”借助 Ad 估 计 值 可 计算 圆 形 投影 的 像素 宽度 。 在 各 投
影 强度 曲线 中 ， 以 圆心 投影 坐标 为 中 心 ， 在 左右 两 侧 去 除 两 倍 圆 形 投影 宽度 内 的 数据 点 ，
从 而 完全 消除 圆 形 投影 的 影响 ， 得 到 椭圆 投影 强度 的 部 分 数据 。
10

<!-- source_page: 11 -->

和 人 \、
和、

AN
入 、

!

AN

/

人 oO

、、C,

|二
六
一 冯
LS |
1NI
JAN
7/
INLA

“、
N

图 11: 圆心 投影 位 置
对 各 投影 角度 ， 利 用 上 述 数 据 拟 合 二 次 多 项 式 得 到 完整 的 椭圆 投影 强度 曲线 。 从 全 部
接收 信息 中 扣除 椭圆 投影 强度 ， 即 可 得 到 圆 形 投影 强度 数据 ， 进 而 拟 合 得 圆 形 投影 强度 曲
线 。 图 ?? 显 示 分 离 出 的 投影 强度 数据 ， 图 ?? 显 示 拟 合 所 得 投影 强度 曲线 。

图 12: 椭圆 投影 强度 数据

〈 左 ) 与 圆 形 投影 强度 数据

11

〈右 )

<!-- source_page: 12 -->

说

可
™

m

x0
ao

本
如

人

图 13:
标定

椭 圆 投影 强度 拟 合 结果

〈 左 ) 与 圆 形 投影 强度 拟 合 结果

(右)

系统 参数
探测
器 单元 间距 Al

设 拟 合 所 得 圆 形 投影 强度

曲线 为 :

(15)

B3(1,6) = ail* + gal + g3
与 投影 模型 比较 系数 得 ;

Ky=q

(16)

so

总 =

-下

加

(17)
四
4q,

Co=gs—1-

(18)

则

有
r
&

和
d3

Ad-

一

Ad?
I

R

|P-2
到
3401 一

(19)
93

op
| 一 叶二
=281/
2

拟 合 180 组 圆 形 投影 强度

曲线

， 将 曲线 系数 代入 式 ?? 解 出 Ad，

Ad = 0.2768mm
12

对 计算 结果 取 均 值得 :

(20)

<!-- source_page: 13 -->

入
射 角度 9” 设 拟 合 所 得 李 圆

投影 强度 曲线 为 :

己 (0) 一 PP 十 Do 十 Ps

(21)

相应地 有 :
Ki=m
Sop _ _D2

(22)

=

_

CI 一 有
为

(23)

r

(

"

求 出 4， 对 开 ; ，C4 表 达 式 进行 变换 可 得 :
C1

加

a2sin20

十 妃 cos20

加

肥

一 Z

RAPD
胎 加 加
9DD2
一
下 Ad 2 +2a*
—b 2
=

cos 20

=

(25)

CT

二 42@2 一 辣 届 二 (0 — p)AR
—~

8pi(b*
— a?)

由 于 探测 系统 逆 时 针 旋 转 ，6 值 单调 增加 ， 由 此 可 确定 b 的 180 组 取 值 。
由
图 7? 可见光 经 计算 修正 后 % 序 列 更 接近 其 线性 拟 合 值 ， 相 邻 两 点 间距 1 左右
个 别 点 出 现 偏差 。 计 算 结果 见 表 ????。
250

14

200
=
S150

s12
F
N '

Hioo
g

Z08
.

E 50
0

，仅在

Top
0

30

60

90

120

150

0.4

180

0

30

60

测 次

图 14:

90
测次

入 射 角度 序列

〈左 ) 与

13

前 向 对比 图 〈 右 )

120

150

180

<!-- source_page: 14 -->

TO TT
本 本 基本
天 本 区 2 天生 天 和
人 or |5 [wom|o | siow
5
| | ao | 9 00
io
| | ao |
mol
a
| | ae | 5 | 0
ia
root
| | so | 二 ol
C | ea | 区 | oo | 2 0
本 | aol | 2 | oo
区 |] ee | 区 | 00 | | 0
| we | |
NE ouo
了 | ee | w | wom | w | oiow
了 | ae | w | ooo | w_| rom
| ae | | oool 这 | 06
6 | Tie |TOO | To
o | Tie5s Too| 二 | Too
人 |] Te ao nsoo | | oil
n|woi
[w | wom |w |wews
0
| 50 | ao | | so
到 oo | | 000 | oa | so
吕 | ap | o | wan |
ouoml
o em
| oo | war | oo | oo
宁 we | | wo6 |
ore
n | woisr | n| we | n| oes
ee
| on | ween | 7 | bo
le
| Tao| | 06
ER
本 ER 了
EIIRRETIETE
© |] ug | w | ioo | sl aoig
可 | use | | io | | 56ig
本戎 RICE 天 本 项 各 下 7
14

<!-- source_page: 15 -->

CT
| 06 | w | mooe | 机 | miom
下 mee |w | 86 | | 6
| mee |w | over | 9 | oroms
o0 |soi|
on |moie | 02 | weee
本
基本 天 机 可 可 ET
too |isioiz|
| 0 | | 0
疯 | 二 0 10 | 6 | | 8
到 TO | |
|
|
而 | 06 | 1 | 0 | 17 | 8
ET
机 | 166 | | 6 | | 6
到 0 | | 0 |
|
ET
E
E
志 66 上 瑟 ia
1 | 6000 | 1 | 16260009 135 | 1090109

13 | 0406 | 137 | 1050463 | 1 | 1000109
19 | 9700 0 108680 | 141 | 1696469

到 DO
| 100 | | 2
1
| 1 | 86 | | 1
避让 ea | 1 | 8065 | 1 | 18
全
ET
丽 |
|
ERIC 机
CI
tos |orowz
|| 0| ws | raseis
too |oroiz|
to7 |mmois
| 0
EEC
下
|
|
而 |
| | 06 | 7 | 6
ii5 |aooiz
| imv | amois | 0 | aws

旋转
中 心 位 置 (z,y) 解 得 入 射 角度 序列 和 后 ， 通 过 线性 插值 将 探测 器 接收 信息 处 理 为
入 射 角 度 间 距 相等 的 情况 ， 以 满足 送 Radon 算 法 的 输入 要 求 ， 获 取 更 高 质量 的 重建 图 像 。
15

<!-- source_page: 16 -->

再 次 运用 图 ?? 所 示 的 方法
图 ?? 所 示 :

， 利 用 三 角形 相似 性 确定 更 精确 的 旋转 中 心 位 置 ， 计 算 结果 如

Z = 40.8436
mm

y = 56.1495 mm

100

80

esshn
60

(40(8436,56.1495)

E

—

E

—)

>

40

|

20

0
0

20

40

60

80

100

x/mm

图 15: 旋转
中 心 位置

4.2.3

”模型
分 析 与 评价

本 模型 根据 拟 合 结果 求解 0， 由 于 拟 合 过 程 中 可 能 存在 误差 ， 故 求 得 的 结果 也 存在 一
定
的 误差 。
依照
前 面 的 推导 ， 有

cos28 一 页 1二 ，C
(元

AR 由

对 于 标定 用 的 模型 ， 我 们 认为 所 提供 的 参数 值 是 足够 精确
的 主要
来 源 为 C、K 和 Al。 记 参数 P 的 误差
为 5LP)， 则 有

、
1_C
jcos2g)
= —pr——3(AP)
16

(26)
的 ，可 以

忽略
其 误差 。 于 是 误差

(27)

<!-- source_page: 17 -->

于 是 ， 只 需求
出 5(&AD)， 根 据 误差
传递 公式 ， 有
其中

5( CA
关
AD = 5( NOCAa2
关
)JAPR+ CAD2
元 5(AD)

(28)

CC _ 10
CC
-VCO5

(29)

因为 ，K 与 C 都 是 由 二 次 曲线 拟 合 结果 计算 得 出 的 ， 于 是 分 析 二 次 函数 拟 合 参 数 的 置信 区
间 。 最 小 二 乘法 做 二 次 拟 合 时 ， 记 预测
值 为 Plz)， 预 测 残 差 平方 和 为 @(ao al ozj)， 则 有
P(z) = aaz2

十 az 十 ao

(30)

N

Qav.ar,a2) = 3°(Pa) — w)?

(1)

r=1

利用 最 小 二 乘 的 思想 进行 拟 合 ， 则 要 求 @(ao, al, oz) 取 最 小 值 ， 即

2_

器 =0

(32)

人 =0

计算 后 求 得 最 优 预测 汶 ;

元 Znm Yai|
Yo Ya2 Yal|

[a]
[Zu
|a| = [Saw

Yap

|a

Yal

Yal|

(38)

>aty;

记
mm

M=|Yas

y

a?

Ya? 工读

(34)

Ya? Yal Nal
则 ， 考 虑 误差 后 ， 有
ao 十 Aao

2o(yi + Ayi)

w+Aa|

| 三 ze+Am

M |ay+ Aay| = | Swiys
+ Ayy)

与 原 式 相 减 可得 :

Auo
M|Aay|

(35)

忆 Ay
=

|SAy

Aay

并 mAw
17

(36)

<!-- source_page: 18 -->

即

Am

¥Au,

Au| =

并 mAw

Aay

>aAy;

(37)

因为
% 为 测量 误差 ， 可 以 视 为 均值 为 0， 标 准 差 为 5 的 独立 高 斯 分 布 ， 则有
E(y) =0
1

(38)
i=j

Et) = | 0 itj

(39)

至 此 ， 可 从 理论 上 求 得 ao at; as 的 表达 式 ， 且 式 子 均 由 包 的 线性 表达 式 构成 ， 利 用 期 望 的
线性 性 ， 可 以 求 得 BE(a), B(a?), E(a) 若 对 于 每 一 次 拟 合 ， 都 进行
如 此 计算 ， 需 要 极 大 的
计算 量 ， 且 不 利于 直观理解 ， 在 此 给 出 一 种 十 分 粗糙 的 方法 计算 其 误差 ,可 以 较 直观的 看
到 误差
的 大 小;
对 于 y = oz2+wz
十 ao，y 的 相对 误差 是 由 az,aayai 的 相对 误差 共同 影响 的 ， 由 于 拟 合
出 来 的 曲线 并 非 奇 异 的 二 次 曲线 ， 可 以 认为 cxz?, az ui 三 项 的 值 大 小 相当 ， 于 是 az ar, ao 的
相对 误差 大 致 相等 ， 对 于 y 的 误差 ， 可 用 其 方差 的 无 偏 估计 来 表示 ， 即 ;

) 人 -2
N

好
内

ao

y 的 值 用 其 均值表示 ， 即 y 的 相对 误差为 难 。 如 图 ?? 所 示 ， 用 Matlab 取 出 其 中 一 条 进行 计
算 ， 可 知 该 值 大 致 为 10-7 - 10-6。
对
于 5(AD)， 其 值 的 是 利用 圆 的 拟 合 曲线 求解 的 ， 单 次 误差 求法 与 枯 圆 类 似 。 由 于
在 180 行 数据 中 都 求 得 了 该 值 ， 并 取 了 平均 ， 其 误差 较 之 原来 减 小 了 sgrt(180) = 13.4145,
与 椭圆 的 误差 相 比 可 以 忽略 。
综 上 ，cos26 的 相对 误差 大 概 在 10 的 -7 至 -6 次 方 量 级 。 因 为
Ce 人 = sin20

所 以

Was

5

(41)

人)

当 sin20 > 10-?， 即 b 与 sin2b 的 零点 距离 大 于 0.02 时 即 可 以 认为 ， 算 得 的 0 相对 误差 小
于 10-4。 计 算 可 知 ， 除 了 极 少数 几 个 点 之 外 ， 其 余 角 度 值 都 可 以 认为 足够 精确 ， 相 对 误差
小
于 10-4。
18

<!-- source_page: 19 -->

..
&

/

\

人
一
一
{

X

0

50

100

150

200

人
和

1

e

一 一 一
350

400

450

500

|

人
图 16:
4.3

曲线 拟 合 及 误差 计算

”问题 二 、 三

4.3.1 ， 逆 Radon 变 换 与 图 像 重建 模型
参数 修正 ”本 部 分 将 道 Radon 变 换 作为 重建 CT 图 像 的 基础 手段 。 为 满足 该 函数 对 输入
参数
的 要 求 ， 首 先 将 入 射 角度 修正 为 线性 拟 合 值 ， 通 过 插值 方法 对 接收 信息 进行 相应 修
正:

记 ( 太 的 ) 为 入 射 角度 4 对 应 的 第 E 个 采样 值 ， 通 过 线性 插值
的 修正 采样 函数 户 (, bo)。
设加 € [bi]， 插 值 方法为 :

应并
及 的) 一 六
i+1

像

7 一 的有 0

的 办 法 得 到 角度 tr = za 处

二 加 JE 的

(43)

i

图 像 重 建 ”以 修正 后 的 接收 信息
， 计 算 结果 如 图 ?? 所 示 。

与 入 射 角度 序列 作为

输入 ， 通 过 逆 Radon
变换 重 建图

系数 修正 ”由 于 题 述 接收 信息 经 由 道 Radon 变 换 所 得 图 像 数 据 与 吸收 率 数 据 不符 ， 两
者 大 致 存在 线性 关系 ， 在 此 需 引 入 比例 系数 以 进行 修正 。
六 的 取 值 由 问题 一 所 给 数据 计算 。 观 察 重建 图 像 断 面 数据 〈 图 ??) 与 全 部 图 像 数据 的
频数 直方 图 〈
图 ??)， 由 于 标定 模板 为 单一 均匀 介质 ， 可 利用 聚 类 分 析 算 法 将 图 像 数 据 分
为 两 类 ， 对 其 中 高 值 类 取 均 值 即 可 得 到 各 的 取 值 ， 将 重建 图 像 数 据 除 以 妨 作 为 修正 。
19

<!-- source_page: 20 -->

0

人

用

宇和

区 了
图 17: 未 知 介质 重建 图 像
0.5

FRR

|

0.4
_03

|

9
¥

0.2

|

0.1 上

小 wu

-0.1 !
0

100

， RU—
200

探测

300

400

500

器 (像素 ) 次 序

图 18: 重建
图 像 断 面 数据
滤波 去 噪

”针对
图 像 噪声

， 利 用 Wiener 滤 波 进 行 去 噪 处 理 ， 计 算 结 果 如 图 ??-?? 所 示 。

对 于 问题 二 《附件3)，Wiener 滤 波 对 几何 伪 影 的 消除 效果 显著 。 由 信号
强度 频数 直方
图 可 见 ， 原 始 图 像 的 信号 强度 有 若干 明显 峰值 ， 且 峰值 附近 的 分 布 情况 与 问题 一 中 的 咯
声
分 布 类 似 ， 滤 波 去 噪 使 峰 型 更 为 尖锐 ， 对 噪声 有 较 好 抑制 效果 。 因 此 对 于 问题 二 ， 采
用 Wiener 滤 波 后 的 图 像 数 据 求解 吸收 率 分 布 。
对
于 问题 三 《附件5)， 由 信号 强度 频数 直方 图 与 滤波 前 后 对 比 图 可 见 ， 介 质 本 身 吸收
率 分 布 广 、 高 频 分 量 大 ， 滤 波 会 抹 除 较 多 的 边缘 信息 。 因 此 对 于 问题 三 ， 售 弃 Wiener
滤波
所 得 结果 ， 利 用 原始 图 像 求 解吸 收 率 分 布 。

20

<!-- source_page: 21 -->

8000

6000

4000

2000

0
-0.1

0

0.1

0.2

0.3

0.4

0.5

0.6

吸收 率

图 19:

图 像 数据 频数 直方 图

B
50

50

是 100

天 100

E

=

#

150

=0
后 全

200

200

2
Peal

站

外

250
50

100

150

200

250

50

100

150

200

250

图 20: 问题
二 重建 图 〈 左 ) 与 滤波
所 得 结果 〈 右 )

4.3.2 ”未 知 介质 信息 的 求解
吸收
率 分 布 ”由 于 上 述 重建 图 像 的 单位 坐标 长 度 对 应 于 探测 器 阵列 的 间距 ， 图 像 数据
点 位 与 需求 的 吸收 率 分 布点 位 (256 x 256)
并 不 相符 。 为 提高 吸收 率 求解 的 精度 ， 应
将所求
点 位 变换 为 重建 图 像 中 的 坐标 ， 变 换 方 法 如 下 :
aa

(44)

由 变换 所 得 坐标 利用 周围 四 点 数据 进行 插值 运算 ， 即 可 得 到 吸收 率 的 分 布 《 如 图 ????所
示 )， 计 算 结果 录 于 附件 problem2.xls。 对 于 附件 4 要 求 的 10 个 位 置 ， 同 样 运用 上 述 方法 计算
吸收 率 ， 所 得 结果如 下 ;

21

<!-- source_page: 22 -->

吸收
率 频数 分 布 直方图

4000
&

3000

£

2000

0

% 3

0

0.2

0.4

0.6

0.8

1

1.2

14

1.6

0

0.2

0.4

0.6

0.8

1

1.2

1.4

1.6

4000

局

3000

这 2000

£ 1000
% 2

图 21:

问题 二 投影 强度 频数 直方 图 (上 )

位 置 坐标 /mm
(10.0000,18.0000)
(43.5000,33.0000)
(48.5000,55.5000)
(56.0000,765000)
(79.5000,18:0000)

|0.0003 |
| 0.0002[
| 10632
”|
| 13133
|-0.0043 |

与 滤波
所 得 结果 CT)

位 置 坐标 /而

吸收 率

(34.5000,25.0000)
(45.0000,75.5000)
(50.0000,75.5000)
[(65.5000,37.0000)
(98.5000,43.5000)

1.0033
1.2096
1.4210
-0.0012
0.0012

表 2: 问题
二 吸收 率 数 据

位 置 琢 标 /7
(10.0000,18.0000)
(43.5000,33.0000)
(48.5000,55.5000)
(56.0000,76.5000)
(79.5000,18.0000)

|0.0657 |
|6.9510 |
|6.3600 |
|72257 |

BLEAE /mm

玻收率

(34.5000,25.0000)
(45.0000,75.5000)
(50.0000,75.5000)
(65.5000,37.0000)
(98.5000,43.5000)

2.8779
-0.0351
3.2544
0.0234
0.0436

表 3: 问题
三 吸收 率 数据
介质 几何 信息

”将 重建 图 像 坐 标 变换 为 正方 形 托盘

几何 形状 ， 如 图 ?? 所 示 。

22

坐标

， 即 可 得 到 未 知 介质 的 位 置 与

<!-- source_page: 23 -->

10

10

至 150

#150

图 22: 问题
三 重建 图 ( 左 ) 与 滤波
所 得 结果 ( 右 )
4.3.3 ”模型
分 析 与 评价
对 于 Radon
道 变换 ， 依 据 卷 积 反 投影 法 ， 可 以 先 将 探测 曲线 与 响应 函数 进行 卷 积 ， 之
后 再 进行 反 投 影 操 作 ， 即 可 得 到 吸收 率 的 空间 分 布 情况 ， 在 连续 且 现 想 的 情况 下 ， 此种 广
法 可 以 精确 的 还 原 出 吸收 率 空间 分 布 图 像 。 但 是 在 实际 操作 中 \ 十 于 测量 误差 及 离散 化 操
作 ， 难 免 会 造成 一 系列 误差 。 主 要 来 源 为 :
、 探 测 器 采样
的 误差 ， 可 以 认为 是 高 斯 自 噪声 ， 几 乎 无 法 消除 ;
2、 投 影 函 数 ffb) 经 过 采样 得 到 采 释 函数 后 造成 的 信息 丢失 ， 利 用 抽样 值 复原 fb) 曲线
时 ， 根 据 采样 定理 ， 若 ftt) 的 频 域 表 达 式 Fw) 满足 Fw) = 0 ylo| > r， 则 可 以 通过 采
样 函数
与 :人 区 的 卷 积 来 精 稍 还 原 。 但 是 由 于 ftb) 在 空间 域 中 的 宽度 是 有 限 的 ， 由 健 立 时
变换 的 性 质 可 知 其 在 频 域 是 无 穷 宽 的 ， 故 无 法 精确复原 。 其 次 ， 通 过 与 sem 来 复原 函数 ，
需要 计算 到 无 穷 远 ， 不 现实 ， 一 般 采 用 矩形 窗 、 汉 明 窗 等 宽度 有 限 的 函数 作为 蔡 代 。 于 是 ，
量化 步 又 会 丢失 一 定量 的 信息 。
3、 系 统 函数 的 传 立 叶 变换 C(R) 实 际 上 是 不 存在 的 ， 只 能 用 趋 近来 表示 :
2(e
一 4r2R2)

C(R) = liny (& +4r?R2)?

(45)

可 以 看 到 C(0) = lim -0 宇 ， 趋 于 无 穷 大 ， 实 际 计算 中 不 可 实现 ， 故 e 只 能 取 有 限 值 。 为了
拟 合 有 限 的 情况 ， 和 常常 采用 “BR-L” 滤 波 函 数 或 者 “S-L” 滤 波 函 数 来 实现 。 在
这个过程
中 ， 也 会 造成 误差
综 上 ， 在 进行 Radon 逆 变换 的 过 程 中 ， 无 可 加 免 会 引入 误差 ， 需 通过 平均 等 方法 才能
减小 误差。

23

<!-- source_page: 24 -->

< 1000

和

:

am

图
Z

0
0

可

2

有

4

5

6

0

1

2

3

4

5

6

< 1000

1

:
<

mm

这 。
图 23:
4.4

4.4.1

问题 三 投影 强度 频数 直方 图 (上 )

与 滤波
所 得 结果 《下 )

问题 四

模型 精度 与 稳定 性 分 析

对 于 问题 一 中 的 标定 模型 ， 精 度 分 析 如 ?? 所 述 ， 标 定 角度 的 相对 误差 小 于 10-4。
为 分 析 标 定 模型 稳定 性 ;引入 高 斯 白 噪声 进行 参数 标定 ， 将 入 射 角度 % 的 预测 误差 作
为 稳定 性 评估 指标 :
1

S=

180

2

其 中 下 标 s 表 示 标 准 值 。 对 于 强度 不 同 的 高

(46)

斯 白 噪 声 ， 稳 定性 分 析 结 果 如 下 :

于
各
ICIO
IT
国生
和
表 4 稳定
性 分 析 结 果

由 于 整个 计算 过 程 比较 复杂 ， 从 随机 过 程 的 角度 出 发 分 析 引 入 高 斯 噪声 之 后 造成 的 影
响 有 着 比较 大 的 困难

， 但 可 以 利用 蒙特 卡 罗 的 思想 ， 通 过 观察 结果 来 描述
24

高 斯 噪声 带 来 的

<!-- source_page: 25 -->

80

80

‘

SR

20

20

图 24:

“7

NE

0

和

Ar

六

未 知 介质 的 几何 信息

影响 。

由 表格
可 以 看 出 ， 随 着 噪声
的 增 大 ， 计 算得 到 的 角度 与 无 噪声 标定 角度 的 偏差 逐渐 增
大 ， 且 其 具体 数值 存在 较 大 的 波动 。 观 察 标定 角度 的 图 像 〈 图 ??)， 可 以 发 现在 绝 大 部 分
角度 上 ， 标 定 角度 与 无 噪声 标定 角度 符合 得 比较 良好 ， 只 有 在 红 圈 标 出 的 区 间 中 有 着 较 大
的 偏差 ， 且 这 个 偏差 值 并 不 稳定 。 根 据 之 前 的 误差 分 析 ， 造 成 这 个 问题 的 主要 原因 是 该 角
度 处 的 误差 传递 系数 很 大 ， 略 有 测量 误差 就 会 导致 很 大 的 偏差 ， 在 这 个 角度 附近 难以 精确
定标 。
250 —————

20——]

w

二

是Z100; /|

150

要 |

)

E Ji

%

:g 如
3

e

9

10

150

1

o

0

30

测 次

6

9

120 16

180

测次

图 25: 稳定
性 分 析结果
4.4.2 ”新 模板 设计 与 标定 模型

的 建立

设计 思路

前 文 分 析 标 定 模型 精度 的 问题 时 曾 指出 在 cosb 一 1 或 cosb 一 0 时 ， 通 过 求 cos26
来 求
解 4 会 有 极 大 的 误差 传递 系数 ， 解 对 数据 波动 十 分 敏感 。 此外 ， 我 们 在 检验 其 稳定 性 的 时
候 发 现 ， 如 图 ?? 所 示 ， 当 对 原始 数据 加 入 高 斯 噪声 之 后 ， 求 得 的 标定 角度 在 大 部 分 地 方 都
25

<!-- source_page: 26 -->

是 接近 于 无 噪声 时 的 标定 值 ， 但 是 在 红 圈 标注 处 ， 与 无 噪声 标定 值 的 差距 较为 明显 ， 且 不
同 次 实验
区 别 很 大 ， 这 正 是 该 位 置 的 敏感 性 造成 的 ， 甚 至 会 导致 出 现 函数 值 略 大 于 1《〈 例
如 arccos(1.0001)) 等 无 法 计算 的 情况 ， 这 也 正 是 原 标定 模型 的 一 个 不 尽 如 人 意 的 地 方 。
为 了 解决
这 个 问题 ， 我 们 尝试 在 原 标定 模型 上 进行 修改 来 满足 更 高 精度 的 需求 ， 依 照
第 一 题 求解 的 经 验 ， 为 了 得 到 更 精确 的 解 ， 应 当 尽 可 能 多 的 利用 上 探测 器 探测 到 的 各 个 吸
收 强度 值 ， 即 考虑 用 拟 合 函 数 的 方法 来 减 小 单个 强度 值 的 测量 误差 ， 这 就 要 求 模板 的 投影
函数 表达 式 应 足够 简单 ， 方
便 拟 合 。 在 这 一 点 上 ， 我 们 首先 考虑 了 用 多 边 形 ， 如 正三 角
形 、 正 方形 等 ， 其 拟 合 函 数 都 是 分 段 直 线 ， 十 分 方便 ， 但 是 在 实践 过 程 中 发 现 ， 虽 然 没
有 arccos(z)
的 敏感 性 困难 ， 但 是 其 本 身 对 于 形状 的 精度 有 很 高 的 要 求 ， 如 图 ?? 所 示 , 正 三
角形 的 顶点 偏离 一 个 像素 ， 就 会 对 拟 合 结果 有 很 大 影响 ， 这 引入 了 一 种 新 的 敏感 性 ， 对 工
艺 有 极 高 的 要 求 ， 故 认为 该 方法 不 合理 。

加

/

中

aal%
»

/
\

/

/

7N

\

(100,200)
(100500)
(358350)

\

\\

/

图 26:

本

/
\N

在

人

，

项 点 坐标

PN

呈

y

外\
-

/
\

¢

/

/

六

顶点 内 标

(100,200)
MSGiooso0)
|(359350)

\N

/
\

/

/

正三 角 模 型 入 射 角度 拟 合 曲线

考虑 到 椭圆 投影 函数 为 二 次 多 项 式 ， 方 便 拟 合 ， 列 含 信息 量 足 够 丰富 ， 最 终 选 择 在 新
模型
中 保留 李 圆 形 。
解决 敏感 性 的 一 个 方法 就 是 通过 两 组 数据 来 求 得 角度 值 ， 要 求 这 两 组 数据 在 各 个 位 置
敏感
性 不 同 ， 于 是 对 于 每 个 位 置 ， 可 以 选 出 敏感 性 较 低 的 数据 作为 测量 值 ， 这 会 对 结果 有
很
大 的 改善 。 因 此 ， 设 计 新 的 模板 为 两 个 椭圆 形 介质 ， 如 图 ?? 所 示 ， 其 中 大 椭圆
半 长轴
为 40mm， 半 短 轴 为 15mm， 与 原 模 板 一 致 。 另 外 一 个 椭圆 置 于 原 模版 中 圆 的 位 置 附 近 ， 长
轴 与 大 椭圆 长 轴 45 度 角 ， 有 具体 参数 如 图 所 示 。
对 该 模板 进行 定性 分 析 ， 由 于 两 个 椭圆 的 朝向 不 一 样 ， 可 以 解决 单个 椭圆 定 角 度 时 存
在 敏感 角度 的 问题 〈 只 要 设计
好 夹 角 ， 使 得 其 各 自 的 敏感 角度 不 重合 ) 。 另 一 方面 ， 由 于
取消 了 原 模板 中 的 圆 ， 需 要 用 其 他 方式 进行 探测 器 间距 5d 的 定 标 ， 这 对 于 单个 彬 圆 是 比
较 麻 烦 的 ， 但 是 对 于 两 个 椭圆 ， 就 可 以 利用 其 几何 关系 ， 经 过 三 角 运 算得 到 ， 尤
其在 夹角
为 45" 时 更 为 简单 。 最 后 由 于 椭圆 大 小 区 别 比 较 明 显 ， 提 取出 两 条 曲线 并 没有 本 质 的 困难 ，
26

<!-- source_page: 27 -->

15
和

<一 一 >

.3.75
40
100|

| 4

SR
|

四
0

50
50

¥

40

|10

图 -27:- 新 模板
设计 示意 图
与 此 前 的 圆 形 模 极 筹 法 类似 。
标定 模型
探测
器 单元 间距 A 首先
参照 原 标定 模型 ， 将 中 心 枯 圆 与 余 置 顶 圆 的 采样 数据 分 离 ，
分 别 拟 合 采样 函数 。
设 拟 合 所 得 中 心 棋 圆 投影 强度 曲线 为 ;
B2(1,0) = pyl® + pol + ps

(47)

根据式 ??， 入 射 角度 与 中 心 顶 圆 投影 曲线 存在 如 下 关系 :

dl
COS 20

一

一半 网 二 (dp 一动 A

RE

(48)

设 拟 合 所 得 斜 置业 加 投影 强度 曲线 为 ;
B2(1.0) 一 六 到 十 rm 十 7
27

(49)

<!-- source_page: 28 -->

50
100
150

200
250

300
350

wT

20

40

60

80

100

120

140

与

160 180

图 28: XUIH F AARL SRAEHAFl
由 于 中 心 李 圆 与 斜 置顶 圆 的 长 轴 夹 角 为 457， 对 式 ?? 将 0 以 g + 45* 代
椭圆 投影 曲线 的 关系 为 :

\C
为

>

i

\ cos2(0 + 45 )=s2=-

4(2a3 — B3)r} + (4r3ry

入 ，得

入 射 角度
与 斜 置

— r)Ad?

(50)

—

方便 表述 ， 记

(DAC
CC
4(2a3 一 0})p}
SE
C)
(4r3r, — 12)Ad?
2
4(2a2 一 B)r}
B=mmea)
则有

cos20 = A,Ad + B,
sin20 = AyAd + By
28

(51)
(52)

<!-- source_page: 29 -->

联 联

求解 从 而 确定 Ad 的 取 值 :
— (A1By + 42B2) 十 V 24142BIP

Ad = 1

一 4

一 4

入
射 角度 b ”将 各 次 计算 的 Ad 取 平 均 ， 代 回 求解 出 cos26 及 sin20。
套 拟 合 数据 中 独立 计算 的 ， 其 误差 几乎 不 存在 耦合 关系 。
分 析 该 计算 的 敏感 性 ， 由 误差 传递 公式 ，

十 4

十 4

-

(53)

且 这 两

个 值是 从 两

-Al(cos20)

-

5 一 [— 2sin20)]

64

A(sin26)
30) =

|2cos26)|

(55)

因为 sin2b 与 cos26 不 可 能 同时 为 0， 所 以 无 需 担心 敏 感性 极 强 的 问题 。
继续 分 析 sin20 与 cos20 的 误差 ， 以 cos20
为 例:
2b
2C1Ad
0(cos20) = | 可
十 2

TEARARAN

BAREE

2
a(by) 十 这

0 2982 —f Lea? MORFLLL,
4bya?

.

5(cos20) ~ |

2C1Ad

+ 21) 8(ay)

故 可 以 认为 误差 近似 等 于 :

4a,b?

5(by) 十 |

5(a)

sin20
的 误差 与 之 同 理 ， 只 需 将 对 应 的 尺寸 换 成 小 椭圆 的 尺寸 即 可 。
尺寸
是 大 李 圆 的 区 倍 ， 从 公式 中 可 以 看 到 误差 与 尺寸 的 -1 次 方 成 正比 ， 所以 :
sin26 ~ Tcos20

记 由 cos20 和 sinz20 算 得 的 g 分 别 为 4. 和 和 ，

其

中 必 +v=

因为

1,

(56)

(57)
因为
小 椭圆

(58)

为 了 尽 可 能 减 小 的 误差 ， 记

0 一 ug 十 ob。

(59)

E(6%) = E(uf, +0,)?

(60)

则

两 者 的 噪声 来 源 基 本 独立

， 故 认为 其 协 方差 系数 为 0， 于 是
E(0?) =

对 上 式 求 导 ， 可 知v =

五 (wu202 +v*6?)

政 灾 时 ， 误差
的 方差 达到 最 小 。 可 以
2
BE)

五 (5(cos20)2)
~
48in220),
29

(61)

求得 ;
(62)

<!-- source_page: 30 -->

_ T2E((sin26)?)
EC
4cos220。

(63)

Tsin220。
cos220, + T'sin?20,,
c05220。
cos220。 + T'sin?20,

©4)
四
(65)

所 以 ， 此时 :
“一
“一

从 而 求解 0 = vb + vb 的 值 。
旋转
中 心 位 置 (z, 刀 “利用 分 别 拟 合 的 两 条 采样 函数 曲线 ， 经 由 变量 替换 得 到 中 心 椭
圆 与 斜 置 椭圆 的 投影 强度 曲线 ， 从 而 计算 两 顶 圆 中 心 OD,, 0: 的 投影 位 置 曲线 。 以 O1, Oo 与
旋转 中 心 O 为 顶点 构造 三 角形 ， 由 Ou, Oz 的 投影 位 置 曲线 可 确定 三 角形 的 内 角 ， 从 而 在 正
方形 托盘 上 定位 出 旋转 中 心 的 位 置 。 此 部 分 计算 与 原 模型 基本 相同 ， 此 处 不 再 歼 述 。

5 ”模型 评价
本 文 以 Radon 变 换 等 物理 背景 为 理论 依据 站 进行 了 三 维 平面 上 的 平行 射线 CT 成 像 系 统
的 建 模与 分析 。
在 由 题目 所 给 模板 对 GT 系统 进行 标定 时 ， 先 使 用 图 像 处 理 的 形态 学 操作 得 到 了 椭圆
投影
的 宽度 变化 规律 ， 计 算得 到 各 角度参数 、 旋 转 中 心 的 估计 值 ， 由 此 进一步
处 理 图 像，
将 李 圆 和 圆 的 两 部 分 影响 独立 出 来 并 分 别 进行 拟 合 ， 在 题 述 条 件 下 ， 由 拟 合 结果 得 到 了 高

精度
的 结果 。
由 于 原 标定 模型 的 单个 椭圆 的 定 标 能 力 限制 ， 该 模型 在 敏感 角度 附近 难以 达到 理想 精
度 ， 在 引入 高 斯 白 噪声 的 情况 下 产生 了 较 大 的 测量 误差 。
因此 原 标 定 模型 对 噪声 的 抵抗 能 力 较 差 ， 应 用 范围受 限 。 但 在 经 过 良好 滤波 除 噪 的 情
襄 下 ， 能 达到 较为 理想 的 标定 精度 。
新 模型 针对 原 有 标定 模型 的 固有 缺陷 进行 了 改进 ， 以 斜 置 椭圆 蔡 代 圆 形 模板 ， 在 大 致
保留 原 有 模型 特性 的 基础 上， 引 入 了 相位 不 同 的 新 标定 曲线 ， 通 过 双 椭 圆 标 定 曲线 的 互
补 ， 克 服 了 原 有 的 敏感 性 缺陷 ， 在 同等
条 件 下 ， 与 原 模型 相 比 可 以 取得 更 高 的 标定 精度 。

参考 文献
0]

庄 天 戈 . CT 原理
与 算法 [M]. 上 海 交 通 大 学 出 版 社 , 1992.

[2] 沈 建 仪 . 椭圆 平行 切线 的 性 质 及 应 用 冲 . 中 学 数学 教学 , 1987(04).
30

<!-- source_page: 31 -->

[3]

郭 立 倩 . CT 系统 标定 与 有 限 角度 CT 重建 方法 的 研究 [D].

大 连理 工大 学 , 2016.

[4] Turbell H. Cone-beam reconstruction using filtered backprojection /[J]. Linképing University, 2001.
[5] JiangHsieh, Hsich,

张 朝 宗 ,等 . 计算 机 上 断层 成 像 技 术 :原理 、 设 计 、 伪 像 和 进展[J]. 2006.

[6] 高上 凯 . 医学 成 像 系 统 .第 2 版 [M]. 清华
大 学 出 版 社 , 2010.

31

<!-- source_page: 32 -->

附录
"problem_1.m"
clc;close

次

获取 数据

dataFile
data

入

all;
=

:..N\A

题

附件 .xls?;

= xlsread(dataFile,2);

参数设 定

lenTheta = 180;
pixScale = 512;

% 总 测量 角度 数
% 单 次 测量
像素 数目

normScale=

% 标准
尺度 (100mm)

100;

graphScale=256;

%

目标

像素

义 度 (256pixel)

a=40; b=15; R=4;
% 图 形 参 数
normEllips0 = [50,50]; % 椭圆 中 心 位 置
normCircle0

=

[95,50];

%

圆 形 中 心 位 置

次 基本 信息 提取
figure(?Name," 各 次 测量 的 接收

值 总 和 ?) ;plot (sum(data) , ’b.”) ;hold on;

axis([1,lenTheta,min(sum(data))*0.997,max (sum(data))*1.003]);
plot([1,lenTheta], [mean(sum(data)) ,mean(sum(data))],’r-’);
text (lenTheta-50,max (sum(data))*1.003-20, [’std=’,num2str(std(sum(data)))], ’FontSize’,14)

legend(? 各 次 测量 的 接收

值 求 和 ,多 次 测量 的 接收 值 均值 2) ;

次 粗 测 太 度 及 角度
% 获取 曲线 边缘 ， 得 到 椭圆 宽度 变化
% figure(?Name',， 原 始 数据
灰 度 图 ') ;colormap (gray) ; imagesc(data) ;
curv

= abs(diff(data));

curv

= curv

> 1;

se = strel(’square’,3);
curvEllips

= imopen(curv,se);

curvEllips

= bwareaopen(curvEllips,500);

% 1RB)& — fB
widthEllips

A

ERE BHE

= zeros(1,lenTheta);
32

<!-- source_page: 33 -->

for

j=1:lenTheta

widthEllips(j)

= find(curvEllips(:,j),1,’last’)-(find(curvEllips(:,j),1,
first’));

end

% 粗略 计算 角度 和 尺度
ToughScale

= max(widthEllips)/2/a;

normWidthEllipse = widthEllips/roughScale;
roughTheta
for

= zeros(1,lenTheta);

j=1:lenTheta
roughTheta(j)

= 180/pi*real(acot(sqrt((4*a~2-normWidthEllipse(j)~2)/(normWidthEllips

end

% 拟 合 得 到 各 个 角度 ,粗略 得 到 逆 变 换 图
diffRoughTheta

= diff (roughTheta);

breakP1

=

find(diffRoughTheta<-0.1,1);

breakP2

=

find(diffRoughTheta(breakP1+10:end)>0.1,1)+breakP1+10;

roughTheta(1:breakP1)=roughTheta(1:breakP1);
roughTheta (breakP1+1:breakP2-1)=180-roughTheta(breakP1+1:breakP2-1) ;
roughTheta (breakP2:end)=180+roughTheta(breakP2:end) ;
[temp, ]=polyfit(1:lenTheta,roughTheta,1);
k_temp

= temp(1);

b_temp

= temp(2);

linerTheta

=

(1:lenTheta)*k_temp+b_temp;

figure('Name, 粗 测 角 度 及 拟
hold

合情

况') ;plot (1: 1enTheta, roughTheta, ’r.’);

on;plot(1l:lenTheta,linerTheta,’b-’);

legend( 粗 测 的 角度
roughMap

， 拟 合 的 角度 ?) ;

= iradon(data,linerTheta,pixScale);

% 旋转 修正
Status

= regionprops((roughMap>max(max(roughMap))/5)) ;

[~ ,orderE11ips]

= max([Status(:).Areal);

[~,orderCircle]

= min([Status(:).Areal);

pixE11ips0

= Status(orderEllips).Centroid;

pixCircle0

= Status(orderCircle).Centroid;

fixAng

= angle((pixCircleO-pixEllips0)*[1;1i]);
33

<!-- source_page: 34 -->

linerTheta
roughMap

= linerTheta+fixAng*180/pi;

= iradon(data,linerTheta,pixScale);

% 得 到 小 圆 圆心 在 图 像 中 位 置
Status

= regionprops((roughMap>max(max(roughMap))/5)) ;

[~,orderCircle]
pixCircle0
pix0

=

= min([Status(:).Areal);

= Status(orderCircle).Centroid;

[pixScale/2,pixScale/2];

% 得 到 轴 在 探测 器 阵列 中 的 投影 位 置
[~ ,minwidthEl11ipsPos]
tempStart

tempEnd

= min(widthEllips);

= find(data(:,minWidthEllipsPos)>0,1,’first’);

= find(data(tempStart:end,minWidthEllipsPos)==0,1, first’)+tempStart;

AxisPosInSensors

=

(tempStart+tempEnd)/2+abs(pix0(1)-pixCircle0(1));

次 拟 合 得 到 精确
% 拟 合 准备

矿 寸 和 角度

pixCircleCenter

= zeros(1,lenTheta);

pixEllipsCenter

= zeros(1,lenTheta);

fitEllipsData=

data;

fitCircleData=

data;

fitEllipsAns

= zeros(pixScale,lenTheta);

fitCircleAns

= zeros(pixScale,lenTheta);

fitAns

= zeros(3,lenTheta);

fitMin

= max(max(data))*0.01;

x = 1:pixScale;

% 拟合 过 程
for

j=1:lenTheta

% 顶 圆 的 宽度 曲线 拟 合
pixCircleCenter(j)

= int16(AxisPosInSensors

- norm(pix0-pixCircle0)+*cos(linerTheta(:

fitEllipsData(int16(pixCircleCenter (j)-2*RxroughScale:pixCircleCenter (j)+2*R*roughSc

fitEllipsRange = find(fitEllipsData(:,j)>fitMin);
fitEllips = polyfit(x(fitEllipsRange)’,fitEllipsData(fitEllipsRange,j). 2,2);
fitEllipsAns(:,j) = (fitEllips(1)*x. 2+fitE1lips(2)*x+fitE1lips(3))’;
34

<!-- source_page: 35 -->

fitEll1ipshns(fitEl11ipshAns(:,j)<0,j)=0;
fitEllipsAns(:,j) = sqrt(fitEllipshAns(:,j));
%

圆 的 宽度 曲线 拟 合

fitCircleData(:,j)
fitCircleRange

fitCircle

= data(:,j)-fitEllipsAns(:,j);

= find(fitCircleData(:,j)>fitMin);

= polyfit(x(fitCircleRange)’,fitCircleData(fitCircleRange,j)."2,2);

fitCircleAns(:,j)

=

(fitCircle(1)*x. 2+fitCircle(2)*x+fitCircle(3))’;

fitCircleAns(fitCircleAns(:,j)<0,j)=0;
fitCircleAns(:,j)

= sqrt(fitCircleAns(:,j));

% 拟 合 结果处 理
pixCircleCenter(j)

= -fitCircle(2)/fitCircle(1)/2;

pixEllipsCenter(j)

= -fitEllips(2)/fitEllips(1)/2;

deltal

= 8/(sqrt(fitCircle(2)"2-4xfitCircle(1)*fitCircle(3))/abs(fitCircle(1)));

G = -8/((fitCircle(2)"2-4xfitCircle(1)*fitCircle(8))/fitCircle(1)/4);

temp = -deltal 2*(fitE1lips(3)-fitEllips(2) "2/fitE1lips(1)/4)/fitE1lips(1);
cosTheta2
fitAns(:,j)

=

(temp/b~2-a~2/b"2)/(1-a"2/b"2);
=

[deltalL,G,cosTheta2];

end
figure (’Name’

,椭圆

部

分 数据 图 ') ; colormap (gray) ; imagesc(fitEllipsData) ;

figure(’Name’,

椭圆

部 分 拟 合 图 ') ; colormap(gray) ; imagesc (fitEllipsAns)

;

figure(Name”,' 小

圆 部 分 数据 图 ') ; colormap(gray) ; imagesc(fitCircleData) ;

figure(Name”,，' 小

圆 部 分拟

合图 ') ;colormap(gray) ; imagesc(fitCircleAns);

figure(?Name”,"
拟 合 结果 与 实际 数据 比 对 图 ) ;
temp

= 150;

subplot(2,1,1);hold

on;

plot(fitEllipsData(:,temp),’b.’);plot(fitEllipsAns(:,temp),’g-");
plot(fitCircleData(:,temp),’b.’);plot(fitCircleAns(:,temp),’g-");
subplot(2,1,2);hold

on;

plot(fitEllipsAns(:,temp)-fitEllipsData(:,temp),’r-");
plot(fitCircleAns(:,temp)-fitCircleData(:,temp),’r-");

% 得 到 拟 合 出 的 角度 并 修正 方向
fixTheta

= 1/2*acos(2.*fitAns(3,:)-1)*180/pi;
35

<!-- source_page: 36 -->

diffFixTheta

= diff (fixTheta);

breakP1

=

find(diffFixTheta<0,1);

breakP2

=

find(diffFixTheta(breakP1+1:end)>0,1)+breakP1+1;

fixTheta(1:breakP1)=fixTheta(l:breakP1);
fixTheta(breakP1+1:breakP2-1)=180-fixTheta(breakP1+1:breakP2-1);

fixTheta(breakP2:end)=180+fixTheta(breakP2:end) ;
figure(Name,

修

正

后 的 各 个 角度 ') ;subplot (1,2,1) ;plot (fixTheta,’.’);

subplot(1,2,2);plot(diff(fixTheta),’r-");

set(gef, ’Position’, [500

500

900

400]);

次 相关 参数 的 求解
% 得 到 深度 系数 和 探测 器 间距
G = mean(fitAns(2,:));
deltaL

= mean(fitAns(1,:));

[interpData,intepThetal=interpForIradon(fixTheta,data);
fixMap

= iradon(interpData,intepTheta,’spline’,’Hann’,pixScale);

% 精 测 旋转中 心
Status

= regionprops ((fixMap>max (max(fixMap))/5));

[*,orderEllips]

= max([Status(:).Areal);

[~ ,orderCircle]

= min([Status(:).Areal);

pixE11ips0

= Status(orderEllips).Centroid;

pixCircle0

= Status(orderCircle).Centroid;

pix0

=

norm0

[pixScale/2,pixScale/2];
=

((2*pix0-pixEllips0-pixCircle0)*deltaL+normEllipsO+normCircle0)/2;

figure(?Name,，' 修
hold

正 的 重建

图 像 ') ; colormap (gray) ; imshow (fixMap) ;

on;plot(pix0(1),pix0(2),’ro’);

plot([pixE11lips0(1),pixCircle0(1)], [pixE11lips0(2),pixCircle0(2)], ko’);
plot([pix0(1),pixE1llips0(1),pixCircle0(1),pix0(1)], [pix0(2),pixEllips0(2),pixCircle0(2),

% 绘制

原 尺 寸 图 内 的 旋转 中 心

figure(,Name, ,旋转
中 心 示意 图 ));

plot([0,100,100,0],[0,0,100,100],’k-") ;hold
tempLen

= 1000;

xEllipsPos

= zeros(tempLen);
36

on;

<!-- source_page: 37 -->

yE11ipsPos

= zeros(tempLen) ;

xCirclePos

= Zeros(tempLen) ;

yCirclePos

= zeros(tempLen) ;

for

i=1:tempLen
sita

= i/tempLen*2*pi;

xEllipsPos(i)

= b*cos(sita)+normE1lips0(1);

yEllipsPos(i)

= a*sin(sita)+normE1llips0(2);

xCirclePos(i)

= R*cos(sita)+normCircle0(1);

yCirclePos(i)

= R#sin(sita)+normCircle0(2);

end
plot (xEllipsPos,yEllipsPos, ’k-7);
plot(xCirclePos,yCirclePos, ’k-);
plot(norm0(1),norm0(2),’ro’);
plot ([normE11ips0(1) ,normCircle0(1)], [normE11lips0(2) ,normCircle0(2)],’ko’);
plot ([norm0(1) ,normE11ips0(1) ,normCircle0(1) ,norm0(1)] , [norm0(2),normE11lips0(2) ,normCirc
axis(’equal’);
set(gca,’YDir’,

’reverse’);

% 求解 :吸收 率" 系 数
figure(?Name12
重 建 图 形 的 吸收 率 分 布 ') ;hist(fixMap(:) ,1000) ;
[fixKmifixKmC]

= kmeans(fixMap(:),2);

Gt

= max(fixKmC)/1.00;

次

保存 数据

CalibrationResults

= {

{’Theta’;

roundn(fixTheta,-4)};

{’norm0’;

roundn(norm0,

-4)};

{’deltal’;roundn(deltal,

-4)};

{°G6°;

roundn(G,

-4)};

{Gt 7

roundn(Gt ，

-4)}

};
for

i=1:length(CalibrationResults)
xlswrite(’Calibration.xls’,{CalibrationResults{i}{1}},1, [’A’

num2str(i)1);

xlswrite(’Calibration.xls’,

num2str(i)l);

CalibrationResults{i}{2}

end
37

,1,[’B’

<!-- source_page: 38 -->

"problem_2.m"
clc;close

次

all;

获取 数据

dataFile
data

=

:..N\A
题 附件 .xls?;

= xlsread(dataFile,3);

points=xlsread(dataFile,4);
CalibrationFile

=

’Calibration.xls’;

CalibrationData

= xlsread(CalibrationFile,1);

Theta

= CalibrationData(1,:);

norm0

= CalibrationData(2,1:2);

deltal=

CalibrationData(3,1);

G

= CalibrationData(4,1);

Gt

= CalibrationData(5,1);

次

计算 /显示 /保存

pixScale

= 512;

desScale

= 256;

[interpData,interpTheta]
Map

= interpForIradon(Theta,data);

= iradon(interpData,interpTheta,’spline’, ’Hann’,pixScale)./Gt;

figure(’Name’,’

B

#i#Radon% #)

; colormap(gray) ; imagesc (Map) ;

% 图 像 插 值
pix0

=

desGraph
for

[pixScale/2,pixScale/2];
= zeros(desScale);

i=1:desScale
for

j=1:desScale
pixPoint

= pix0+([i-0.5,j-0.5]./desScalex100-[norm0(2),norm0(1)])/deltal*pixScal

desGraph(i,j)

= interpAbsorbMap(pixPoint,Map);

end
end

figure(Name， 吸 收 率 平面

分 布 图') ; colormap (gray) ; imagesc (desGraph) ;

38

<!-- source_page: 39 -->

%

图 像 wiener
滤 波

K=wiener2(desGraph, [5 51);

figure(;Name, ,吸收
率 占 比 分 布 图 )) ;
[tempA,tempB]=hist(desGraph(:)

,1000) ;

Subplot(211) ;bar (tempB,tempA,’b’) ;axis([-0.2,1.6,0,4000]);

ylabel("
原 始 重建 图 像 吸 收 率 分 布 :) ;
[tempA ,tempB]=hist(K(:)

,1000) ;

Subplot(212) ;bar (tempB, tempA, ’r’) ;axis([-0.2,1.6,0,4000]);

ylabel(?
滤 波 后 的 图 像 豚 收 率 分 布 :) ;
figure(?Name,，'

滤 波

前 后对 比 图 ) ;

subplot(121) ;imagesc(desGraph);

ylabel(? 原

Subplot(122) ; imagesc(K) ;

ylabel(?
滤 波 处 理 ?);

Set(gcf, ’Position’, [600

500

900

始 图 像 :) ;

400] ) ;

% 计算
各 点 吸收 率
Absorbtion

= zeros(1,length(points));

fprintf(
各 点 吸收 率 数据 : \n2) 1
pixPoints
for

= zeros(length(points),2);

i=1:length(points)
pixPoints(i,:)

=

[points(i,1),100-points(i,2)]/100*desScale*pixScale/512;

Absorbtion(i)

= interpAbsorbMap([pixPoints(i,2),pixPoints(i,1)],K);

fprintf (’%.4f\n’,Absorbtion(i

));

end

% 显示
各 点 位 置
figure(Name”， 各 点 分
for

布 图 ') ;colormap(gray) ;imagesc(K) ;hold

on;

i=1:length(points)
plot(points(i,1)*desScale/100, (100-points(i,2))*desScale/100, r*’);
text (points(i,1)*desScale/100, (100-points(i,2))*desScale/100,num2str
(roundn (Absorbti

end

% 保存 数据
x1lswrite(’problem2.x1ls’,roundn(K,-4));

39

<!-- source_page: 40 -->

"problem_3.m"
clc;close

次

all;

获取 数据

dataFile
data

=

:..N\A
题 附件 .xls?;

= xlsread(dataFile,5);

points=xlsread(dataFile,4);
CalibrationFile

=

’Calibration.xls’;

CalibrationData

= xlsread(CalibrationFile,1);

Theta

= CalibrationData(1,:);

norm0

= CalibrationData(2,1:2);

deltal=

CalibrationData(3,1);

G

= CalibrationData(4,1);

Gt

= CalibrationData(5,1);

次

计算 /显示 /保存

pixScale

= 512;

desScale

= 256;

[interpData,interpTheta]
Map

= interpForIradon(Theta,data);

= iradon(interpData,interpTheta,’spline’,’Hann’,pixScale)./Gt;

figure(?Name”

,直接

逆 Radon 变 换 ") ; colormap (gray) ; imagesc (Map) ;

% 图 像 插 值
pix0

=

desGraph
for

[pixScale/2,pixScale/2];
= zeros(desScale);

i=1:desScale
for

j=1:desScale
pixPoint

= pix0+([i-0.5,j-0.5]./desScalex100-[norm0(2),norm0(1)])/deltal*pixScal

desGraph(i,j)

= interpAbsorbMap(pixPoint,Map);

end
end

figure(Name， 吸 收 率 平面
%

分 布 图') ; colormap (gray) ; imagesc (desGraph) ;

图 像 wiener
滤 波
40

<!-- source_page: 41 -->

K=wiener2(desGraph, [5 51);

figure(;Name, ,吸收
率 占 比 分 布 图 )) ;
[tempA, tempB]=hist (desGraph(:),1000);
subplot(211) ;bar (tempB,tempA,’b’);axis([-0.2,6,0,10001);

ylabel("
原 始 重建 图 像 吸 收 率 分 布 :) ;
[tempA ,tempB]=hist(K(:)

,1000) ;

Subplot(212) ;bar (tempB,tempA, 'r’);axis([-0.2,6,0,10001);

ylabel(?
滤 波 后 的 图 像 豚 收 率 分 布 :) ;
figure(?Name,，'

滤 波

前 后对 比 图 ) ;

subplot(121) ;imagesc(desGraph);

ylabel(? 原

Subplot(122) ; imagesc(K) ;

ylabel(?
滤 波 处 理 ?);

Set(gcf, ’Position’, [600

500

900

始 图 像 :) ;

400] ) ;

% 计算
各 点 吸收 率
Absorbtion

= zeros(1,length(points));

fprintf(?
各 点 吸收 率 数据 : \n?);
pixPoints
for

= zeros(length(points),2);

i=1:length(points)
pixPoints(i,:)

=

[points(i,1),100-points(i,2)]/100*desScale*pixScale/512;

Absorbtion(i)

= interpAbsorbMap([pixPoints(i,2),pixPoints(i,1)],desGraph);

fprintf (’%.4f\n’,Absorbtion(i

));

end

% 显示
各 点 位 置
figure("Name”， 各
for

点 分 布 图 ') ;colormap(gray) ; imagesc (desGraph) ;hold

on;

i=1:length(points)
plot(points(i,1)*desScale/100,(100-points(i,2))*desScale/100，T#?)
text (points(i,1)*desScale/100, (100-points(i,2))*desScale/100,num2str (roundn(Absorbt:

end

% 保存 数据
x1lswrite(’problem3.x1ls’,roundn(desGraph,-4));

41

<!-- source_page: 42 -->

"problem_4.m"
clc;close

次

all;

获取 数据

dataFile

=

originData

:..N\A

题

附件 .xls?;

= xlsread(dataFile,2);

CalibrationFile

=

’Calibration.xls’;

CalibrationData

= xlsread(CalibrationFile,1);

Theta

= CalibrationData(1,:);

norm0

= CalibrationData(2,1:2);

deltaLs=

CalibrationData(3,1);

G

= CalibrationData(4,1);

Gts

= CalibrationData(5,1);

Wh

参数 设 定

lenTheta = 180;
pixScale = 512;

% 总 测量 角度 数
% 单 次 测量
像素 数目

normScale=

% 标准
尺度 (100mm)

100;

graphScale=256;

%

目标

像素 久 度 (256pixel)

a=40; b=15; R=4;
% 图 形 参 数
normEllips0 = [50,50]; % 椭圆 中 心 位 置
normCircle0

次
data

=

[95,50];

%

圆 形 中 心 位 置

基本 信息 提取
= originData;

次 粗 测 太 度 及 角度
% 获取 曲线 边缘 ， 得 到 椭圆 宽度 变化
% figure(?Name:, 原 始 数据
灰 度 图 ') ;colormap (gray) ; imagesc(data) ;
curv

= abs(diff(data));

curv

= curv

> 1;

se = strel(’square’,3);
curvEllips

= imopen(curv,se);

curvEllips

= bwareaopen(curvEllips,500);

42

<!-- source_page: 43 -->

% 得 到 每 一 角度 对 应 的 椭圆 宽度 数据
widthEllips
for

= zeros(1,1enTheta) ;

j=1:lenTheta

widthEllips(j)

= find(curvEllips(:,j),1,’last’)-(find(curvEllips(:,j),1,
first’));

end

% 粗略 计算 角度 和 尺度
ToughScale

= max(widthEllips)/2/a;

normWidthEllipse = widthEllips/roughScale;
roughTheta
for

= zeros(1,lenTheta);

j=1:lenTheta

roughTheta(j)

= 180/pi*real(acot(sqrt((4*a~2-normWidthEllipse(j)~2)/(normWidthEllipse
(j)

end

% 拟 合 得 到 各 个 角度 ,粗略 得 到 逆 变 换 图
diffRoughTheta = diff (roughTheta);
breakP1

=

find(diffRoughTheta<-0.1,1);

breakP2

=

find(diffRoughTheta(breakP1+10:end)>0.1,1)+breakP1+10;

roughTheta(1:breakP1)=roughTheta(1:breakP1);
roughTheta (breakP1+1:breakP2-1)=180-roughTheta(breakP1+1:breakP2-1) ;
roughTheta (breakP2: end)=180+roughTheta(breakP2:end) ;
[temp,

]=polyfit(1:lenTheta,roughTheta,1);

k_temp

= temp(1);

b_temp

= temp(2);

linerTheta
roughMap

=

(1:lenTheta)*k_temp+b_temp;

= iradon(data,linerTheta,pixScale);

% 旋转 修正
Status

= regionprops((roughMap>max(max(roughMap))/5)) ;

[~ ,orderE11ips]

= max([Status(:).Areal);

[~,orderCircle]

= min([Status(:).Areal);

pixE11ips0

= Status(orderEllips).Centroid;

pixCircle0

= Status(orderCircle).Centroid;

fixAng

= angle((pixCircleO-pixEllips0)*[1;1i]);

linerTheta

= linerTheta+fixAng*180/pi;
43

<!-- source_page: 44 -->

roughMap

= iradon(data,linerTheta,pixScale);

% 得 到 小 圆 圆心 在 图 像 中 位 置
Status

= regionprops ((roughMap>max
(max (roughMap))/5)) ;

[7,orderCircle]
pixCircle0
pix0

=

= min([Status(:).Areal);

= Status(orderCircle).Centroid;

[pixScale/2,pixScale/2];

% 得 到 轴 在 探测 器 阵列 中 的 投影 位 置
[~ ,minwidthEl11ipsPos]

tempStart
tempEnd

= min(widthEllips);

= find(data(:,minWidthEllipsPos)>0,1,’first’);
= find(data(tempStart:end,minWidthEllipsPos)==0,1, first’)+tempStart;

AxisPosInSensors

=

次 ANBHTRE,

AHTHEE
B RUR 19] AL

gaussPower
data

(tempStart+tempEnd)/2+abs(pix0(1)-pixCircle0(1));

= 0.00002;

= imnoise(originData./max(max(originData)),’gaussian’,0,gaussPower) .*max(max(origir

次 拟 合 得 到 精确
% 拟 合 准备

矿 寸 和 角度

pixCircleCenter

= zeros(1,lenTheta);

pixEllipsCenter

= zeros(1,lenTheta);

fitEllipsData=

data;

fitCircleData=

data;

fitEllipsAns

= zeros(pixScale,lenTheta);

fitCircleAns

= zeros(pixScale,lenTheta);

fitAns

= zeros(3,lenTheta);

fitMin

= max(max(data))*0.03;

x = 1:pixScale;

% 拟合 过 程
for

j=1:lenTheta

% 椭圆
的 宽度 曲线 拟 合
pixCircleCenter(j)

= int16(AxisPosInSensors

- norm(pix0-pixCircle0)*cos(linerTheta(;

fitEllipsData(int16(pixCircleCenter (j)-2*R*roughScale:pixCircleCenter (j)+2*R*xroughSc
44

<!-- source_page: 45 -->

fitEllipsRange = find(fitEllipsData(:,j)>fitMin);
fitEllips = polyfit(x(fitEllipsRange)’,fitEllipsData(fitEllipsRange,j). 2,2);
fitEllipsAns(:,j) = (fitEllips(1)*x. 2+fitE1lips(2)*x+fitE1lips(3))’;
fitEllipsAns (£itE1lipsAns(:,3)<0,j)=0;
fitEllipsAns(:,j) = sqrt(£itEllipsAns(:,3));
% 圆 的 宽度 曲线 拟 合
fitCircleData(:,j) = data(:,j)-fitEll1ipsAns(:,j);
fitCircleRange = find(fitCircleData(:,j)>fitMin);
fitCircle

= polyfit(x(fitCircleRange)’,fitCircleData(fitCircleRange,j)."2,2);

fitCircleAns(:,j)

=

(fitCircle(1)*x. 2+fitCircle(2)*x+fitCircle(3))’;

fitCircleAns(fitCircleAns(:,3)<0,j)=0;
fitCircleAns(:,j)

=

sqrt(fitCircleAns(:,j));

% 拟 合 结果处 理
pixCircleCenter(j)

= -fitCircle(2)/fitCircle(1)/2;

pixEllipsCenter(j) = -fitEllips(2)/fitEllips(1)/2;
deltaL = 8/(sqrt(fitCircle(2) 2-4+fitCircle(1)*fitCircle(3))/abs(fitCircle(1)));
G = -8/((fitCircle(2) 2-4xfitCircle(1)*fitCircle(3))/fitCircle(1)/4);
temp = -(fitEllips(3)-fitEllips(2)~2/fitEllips(1)/4)/fitEllips(1);
cosTheta2

=

fitAns(:,j)

(temp/b~2-a~2/b"2)/(1-a"2/b"2);

= [deltal,G,temp];

end

figure(Name，，

椭

圆 部 分 拟 合 图 ') ; colormap(gray) ; imagesc (fitEllipsAns)

figure(Name”,，' 小

圆 部 分 拟 合 图 ') ;colormap(gray) ; imagesc(fitCircleAns);

% 得 到 拟 合 出 的 角度 并 修正 方向
G = mean(fitAns(2,:));
deltaL = mean(fitAns(1,:));
temp = deltal"2.xfitAns(3,:);
temp

=

fixTheta

(temp./b"2-a"2/b"2)./(1-a"2/b"2);
= real(1/2+xacos(2.*ktemp-1)*180/pi) ;

diffFixTheta = diff (fixTheta);
breakP1 = 61;
45

;

<!-- source_page: 46 -->

breakP2

=

152;

fixTheta(1:breakP1)=fixTheta(l:breakP1);
fixTheta(breakP1+1:breakP2-1)=180-fixTheta(breakP1+1:breakP2-1);

fixTheta(breakP2:end)=180+fixTheta(breakP2:end) ;
figure(Name,

修

正

后 的 各 个 角度 ') ;subplot (1,2,1) ;plot (fixTheta,’.’);

subplot(1,2,2);plot(diff(fixTheta),’r-");

Wh

相关 参数

的 求解

[interpData,intepTheta]=interpForIradon(fixTheta,data) ;
fixMap

= iradon(interpData,intepTheta,’spline’,’Hann’,pixScale);

figure(?Name," 重 建 图

% 求解 :吸收

率" 系 数

[fixKm,fixKmC]
Gt

像 ') ;colormap(gray) ; imagesc(fixMap) ;

= kmeans(fixMap(:),2);

= max(£ixKmC)/1.00;

fprintf( "高

斯 误差 强度 :%.6f\n? ,gaussPower) ;

fprintf( 求 得 角度 误差 :%.4fNn7

,std(fixTheta-Theta)) ;

"interpAbsorbMap.m"

党 图 形 插值
% 输入 : 带 权 图 和 目标 坐标 点
% 输出 :目标 坐标 点 附近 点 的 线性 插值
function

val

得 到 的 权值

= interpAbsorbMap(Point
,Map)

floorX

= floor(Point(1));ceilX

= ceil(Point(1));

floorY

= floor(Point(2));ceilY

= ceil(Point(2));

if

floorX<1i
floorX

=

1;ceilX

= floorX+1;

end

if ceilX>length(Map)
ceilX

= length(Map);floorX

= ceilX-1;

end
if

floorY<1

46

<!-- source_page: 47 -->

floorY

=

1;ceilY

= floorY+1;

end

if ceilY>length(Map)
ceilY

= length(Map);floorY

= ceilY-1;

end
tempY1

=

(Map(ceilX,floorY)-Map(floorX,floorY))*(ceilX-floorX)+Map(floorX,floorY);

tempY2 = (Map(ceilX,ceilY)-Map(floorX,ceilY))*(ceilX-floorX)+Map(floorX,ceilY) ;
val

=

(tempY2-tempY1)*(ceilY-floorY)+tempY1;

end

"interpForlradon.m"
function

[interpData,interpTheta]=interpForIradon(Theta,data)

interpTheta

= Theta(1l):(Theta(end)-Theta(1))/(length(Theta)-1):Theta(end);

interpData

= data;

for

j=2:length(Theta)-1

if interpTheta(j)<Theta(j)
start

= j-1;

finish

= j;

start

= j;

finish

= j+1;

else
end
interpData(:,j)

=

(data(:,finish)-data(:,start))#*(interpTheta(j)-Theta(start))/(

end
end

47
