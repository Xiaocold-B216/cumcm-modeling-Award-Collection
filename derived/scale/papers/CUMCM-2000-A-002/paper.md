# Extracted Paper

<!-- source_page: 1 -->

加
和 o
第 31 卷 第 1 其 数学 的 实践 与 认识 volal Nu BERAE
2001 年 1 月 MATHEMATJCS N PRACTICE AND THEORY Jan 0
DNA 序列 分 类 的 数学 模型
昌 金 翅 ， 马 小 龙 ， 曹芳
指导 老师 : ” 陶 大 程
(中 国 科学 技术 大 学 ， 合 肥 230026) 一
-从 >
编者 按 :本文 能 从 生物 学 背景 提出 不 同 的 三 种 判别 模型 和文 这 人 区 让 下
21 一 40 和 182 样本 均 进行 了 分 类 , 分 类 正确 率 较 高 人 /一
摘要 :本文 从 三 个 不 同 的 角度 分 别论 述 了 如 何 对 DNA Treeoas 对 mr
三 类 模型 )
首先 , 从 生物 学 背景 和 几何 对 称 观 点 出 发 , 建立 了 DNA fr 形式 建立 了 初步
数学 模型 - 积分 模型 , 并 且 通 过 模型 函数 计算 得 到 了 1 到 20 号 DNA FY 结 朵 , 发 现 与 题目 所 给 分 类
结果 相同 , 然后 我 们 又 对 后 20 个 DNA 序列 进行 了 分 类
然后 , 从 人 工 神经 网 络 的 角度 出 发 , 得 到 了 第 二 类 数学 模 oATL :神经 网 络 模型 并 且 选 择 了 三 种 适用
于 模式 分 类 的 基本 网 络 , 即 感知 机 模型 , 多 层 感 知 机 BP 网 络 ) 开 生 以 RLVQ 矢量 量化 学 习 器 , 同时 就 本 问
题 提 出 了 对 BP 网 络 的 改进 (改进 型 多 层 感知 机 ), 最 后 采用 多 种 训 弥 方案 , 均 得 到 了 较 理想 的 分 类 结果 同
时 也 发 现 了 通过 人 工 神经 网 络 的 方法 得 到 的 分 类 结果 与 积分 模型 得 到 的 分 类 结果 是 相同 的 (前 四 十 个 ).
最 后 , 我 们 对 碱 基 赋 了 予 几何 意义 :A. ¢ G T 分 别 瑟 示 右 下 左 上 用 DNA 序列 控制 平面 上 点 的 移动
每 个 序列 得 到 人 3 作为 特定 , 建立 起 了 模型 函数 , 同时 也 得 到 了 后 二 十 个 DNA
序列 的 分 类 结果 ， 而 县 发 现 结果 与 上 OOT -个 不 同 , 在 本 模型 中
表示 为 不 可 分 的 )， 此 模型 保留 的 信息 量 更 多 , 面目 稳定 性 更 强
1 问题 的 重 述 ( 略 ) 和
_—
2 EAERIEERT
第 一 类 数学 模型 ;积分 模型
D Weyaanraokacm 在 这 条 链 上 不 仅 包含 有
人 条
AS 调控 信息 (三 维 空间 和 一 维 时 间 ), 找到 这 些 信息 的 编码 方式 和 调节 规律 是 人
2 下 面 我 们 首先 将 着 手 从 几何 学 的 角度 来 分 析 DNA 序列
鉴 冬 自然 界 对 称 这 一 朴素 原理 , 我 们 的 模型 始 于 对 4 种 碱 基 对 称 性 的 考察 图 1.1( 略 ) 从 纯
化 学 的 角度 , 我 们 可 以 将 碱 基 进行 两 类 划分 : (1) 按 双环 或 单 环 结构 , 可 分 为 : 味 叭 碱 基 R (A
或 G) 与 喀 啶 碱 基 Y(C 或 T) (2) 按 环 中 对 应 位 置 上 是 否 存在 氨基 或 酮 基 , 可 分 为 : 氨基 碱 基
M (A 或 C) 与 酮 基 碱 基 K(G 或 T) 从 生物 学 的 角度 , 在 双 螺 旋 结构 中 , 按 碱 基 对 形成 氧 键 的
数目 或 强 弱 , 碱 基 又 可 分 : 强 氧 键 碱 基 S(G 或 C) 与 弱 氧 键 碱 基 W (人 或 T), 这 一 种 划分 既
包含 了 化 学 的 也 包含 了 DNA 双 螺 旋 的 结构 信息 在 内
参照 基本 粒子 理论 中 的 做 法 , 我 们 利用 三 维 Euclid 空间 中 的 对 称 几何 图 形 一 一 立方 体
G 来 表示 碱 基 的 上 述 三 种 对 称 性 如 图 1.2 所 示 , 以 G 的 中 心 为 坐标 原点 建立 三 维 直角 坐
94-200: ina Academic Journal Electronic Publishing House. All rights reserved.  http://www.cnki.nq

<!-- source_page: 2 -->

ERiEE
EEEA
1 其 昌 人 金地 等 DNA 序列 分 类 的 数学 模型 5
标 系 , 使 G 的 三 组 对 面 分 别 与 三 条 坐标 轴 相 垂直 分 别 与 X, 了, Z 轴 相 交 的 G 的 三 组 对 面
称 为 喀 啶 / 镖 叭 面 , 酮 基 / 毛 基 面 , 弱 氧 键 / 强 氧 键 面 在 G 的 六 个 面 中 各 引 一 条 对 角 线 , 使 相
对 面 的 对 角 线 两 两 相互 垂直 , 如 图 1.2 所 示 在 味 叭 面 对 角 线 的 两 端 分 别 标 上 4 和 G; 在 喀
啶 面 对 角 线 的 两 端 分 别 标 上 C 和 了 , 如 图 1.2 所 示 显然, 此 时 上 述 碱 基 的 三 种 对 称 关 系 全
部 自动 成 立 而 且 , 六 条 对 角 线 刚好 是 正四 面体 4 CC7 的 六 条 棱
z y
A
一 从
| 月 0
AMY
# p
~
: 价
MA
LA
X
mw 7
sx
NA
全
一 图 1.。 用 立方 体 表示 碱 基 的 三 种 对 称 性
srsgNWE ttoNA 序列 , 阅读 方向 不 限 从 第 一 个 碱 基 开 始 , 依次 考察
此 序列 加 全 察 一 个 碱 基 当 考 察 到 第 ”个 碱 基 时 (xz= 1 2, … 江 ), 统计 一 下 从 1 到 ，
人 了 和 生 和 近 才 ccn en 分 别 表 示 4 种 碱 基 4、C\、G、 了
出 现 的 次 数 0 图 1.3 所 示 显然 它们 都 是 非 负 整数 根据 正四 面体 的 对 称 性 我 们 可 以 证
本 内 存在 只 一 的 一 个 点 与 这 四 个 非 负 整数 一 一 对 应 在 图 1.3 所 示 建 立 的 坐
标 约 之 下 , 点 P, 的 坐标 可 用 四 个 非 负 整数 来 表达
Xo=2ot G)- n, Yo= 2Wat C)- n,Ze=2Un+ Tn)- 六 TDE[- n,
nl,n=1,2,,L;
Hrpx,, PP 和 2Z, 为 点 P, 的 三 个 坐标 分 量 当 靖 从 1 到 时 ,我 们 依次 得 到 己 , Pa, …，
P 共 Z 个 点 将 相 邻 两 点 用 适当 的 曲线 连接 所 得 到 的 整 条 曲线 , 就 成 为 表示 此 DNA 序列
的 忆 - 曲 线 可 以 证 明 ,P- 曲 线 与 所 表示 的 DNA 序列 是 一 一 对 应 的 , 也 就 是 说 , 给 定 一 定
DNA 序列 , 存在 唯一 的 一 条 己 - 曲 线 与 之 对 应 ; 反之 , 给 定 一 条 尸 -曲线 , 可 以 找到 唯一 的 一
个 DNA 序列 与 之 对 应 换言之 ,P- 曲 线 很 大 程度 上 包含 了 DNA 序列 的 内 萤 信 息 己 - 曲 线
ht T

<!-- source_page: 3 -->

48 数学 的 实战 与 认识 1 tien
—
V 了
n
1 n L
-一
图 1 3 DNA 序列 示意 图 全
是 与 符号 DNA 序列 等 价 的 另 一 种 几何 表现 形式 nmol
完 来 挖掘 DNA 序列 的 内 蕴 信 息 “\)
忆 - 曲 线 的 三 个 分 量 都 具有 明确 的 生物 学 意义 :站 ， 表示 顺 0[ 庆 站 有 的 分 在
当 从 1 到 这 个 子 序列 中 嘲 叭 碱 基 多 于 喀 喧 碱 基 时 ,并 ,> 5
= 0 同样 , 交 表示 氨基 / 债 基 碱 基 沿 序列 的 分 布 当 在 子 序 多 生活 基 碱 基 多 于 酮 基 碱 基 时 ，
Jrv> 0; 否则 , v.< 0; 当 两 者 相等 时 甩 = 0 Z， 表示 强 / 弱 氧 键 砚 E 列 的 分 布 2555%05
碱 基 多 于 强 氨 键 碱 基 时 ,Z,> 0; 否则 , Z,< 0; Q 由 概率 论 中 的 结论 : 如 果
任何 一 种 分 布 均 不 能 由 其 他 两 种 分 布 的 线性 倒 加 臣 示 出 来 , 则 这 三 种 分 布 是 相互 独立 的
给 定 的 DNA 序列 唯一 的 决定 了 这 三 种 分 布 ; 2 序列
我 们 对 P, 的 三 个 坐标 分 量 分 别 积分 , 发 现 7 Z,， 两 个 方向 上 并 没有 什么 区 别 , 而 在 X，
方向 上 , A 组 均 大 于 零 , B 组 均 小 于 零 ©
% = 人 :ou
这 表明 在 整个 序列 上 不 同 结构 的 碍 趟 光 占 的 成 分 , 即 A 组 嗓 叭 的 含量 较 大 ,B 组 喀 啶 的
含量 较 大 hm
PLY 方向 分 量 大 于 / 村 珊 标 给 出 的 序列 2 40 进行 分 类 , 得 到 如 下 结果 :
A %:2,3,5,7,9,14 机 已 19; B 类 : 1, 4, 6, 8, 10, 11, 12, 13, 16, 18, 20
由 到 由 二 RE
的 所 加 人 预见 新 趋势 , 创造 新
Te 处 理 横 式 分 类 的 问题
在 术 题 中 全 采用 如 下 几 种 方案 : 1 单 层 感知 机 ; 2 双 层 感知 机 ; 3 改进 型 双 层 感 知 机
cvc' 量 量化 学 习
] 作 洒 于 各 种 算法 我 们 又 采用 了 三 种 统计 方案 , 即 ;
N 统计 oa ¢ g ¢TEDNA 序列 中 出 现 的 次 数 ( 共 有 4 种 )
2 统计 ao c g :的 两 两 组 合 在 DNA 序列 中 出 现 的 次 数 ( 共 有 对 种 不 同 的 组 合 )
3 统计 oa c g 的 三 三 组 合 在 DNA 序列 中 出 现 的 次 数 ( 共 有 二 种 不 同 的 组 合 )
所 以 总 共 可 以 得 到 12 种 模式 分 类 模型
下 面 给 出 详细 讨论 , 但 只 列 出 12 种 方案 中 的 四 种 , 因为 剩 下 八 种 只 是 在 统计 方案 上 有
所 不 同 , 其 训练 实质 和 学 习 实 质 以 及 最 后 的 模拟 实质 是 相同 的 , 所 以 不 需要 一 一 罗列
第 一 方案 ( 单 层 感知 机 )
1 综述 :
4 © 1994-200: ina Academic Jour ni blishin ou ]l rights TVei tp://w ki.nef

<!-- source_page: 4 -->

7
1 其 昌 金 地 等 DNA 序列 分 类 的 数学 模型 9 w
单 层 感知 机 是 一 个 具有 单 层 计算 神经 元 的 神经 网 络 , 并 由 线形 域 值 单元 组 成 原始 的
Percep tron 算法 只 有 一 个 输出 节点 , 它 相当 于 单个 神经 元 当 它 用 于 两 类 模式 的 分 类 时 , 相
当 于 在 高 维 样本 空间 中 , 用 一 个 超 平面 将 两 类 样本 分 开 下 Rosenblatt 也 已 证 明 , 如 果 两 类
模式 是 线形 可 分 的 ( 指 存在 一 个 超 平面 将 它们 分 开 ), 则 算法 一 定 收敛 ”感知 器 特别 适用 于
简单 的 模式 分 类 问题 , 也 可 用 于 基于 模式 分 类 的 学 习 控制 和 多 模 态 控制 中
2 修正 方案 ;
首先 分 析 问 题 实质 , 即 采用 一 个 单一 神经 元 解决 简单 分 类 问题 : 将 ”个 输入 矢量 分 为 两
类 , 其 中 一 部 分 为 1, 另 一 部 分 为 0 最 后 确定 网 络 结构 (图 1. 4): 从
起 知 儿 神经 元 二 A7
w, \ ZXG \)
2(2) | | )
人 mn 四
六 (RCR) b
图 1.4
3 训练 算法 : (采用 单 层 感知 其 经 典 饶 演 这 里 略 去 )
判定 网 络 收敛 的 标准 有 两 种 * 和 时 下 均 平方 误 郑 二 是 误差 平方 和 这 里 采用 第 二 种
Ag 当 给 网 络 提供 一 输
入 模式 时 , 网络 将 按 上 式 请 刀 册 答 出 值 y, 并 可 根据 y， 为 1 或 0 判断 出 这 一 答 入 模式 属于
记忆 中 的 哪 一 种 模式 TS
4 训练 和 模拟 结果 :， ¥
a) Ah 20 人 序列 中 随机 选取 不 同 的 4 个 序列 (向 量 ) 进行 训练 , 再 对 20
个 序列 (向 景 ); 进 行 重新 模拟 , 其 正确 率 为 90% , 发现 出 错 的 原因 在 于 , 第 4 个 和 第 17 个 序
Re
CT 序列 中 随机 选取 不 同 的 4 个 序列 (向 量 ) 进行 训练, 共
进行 两 次 , 二 对 20 个 序列 (向 量 ) 进行 重新 模拟 , 其 正确 率 为 95% ,依然 发 现 出 错 的 原因 在
1 也 人 和 第 17 个 序列 在 这 几 种 统计 方式 下 具有 相似 性
Ne 每 次 从 20 个 已 知 结果 的 DNA 序列 中 随机 选取 不 同 的 4 个 序列 (向 量 ) 进 行 训练 , 共
进行 三 次 , 再 对 20 个 序列 (向 量 ) 进行 重新 模拟 , 其 正确 率 为 95% ,依然 发 现 出 错 的 原因 在
于 , 第 4 个 和 第 17 个 序列 在 这 几 种 统计 方式 下 具有 相似 性
5. 结论 : 数据 为 线性 不 可 分 的 , 所 以 单 层 网 络 不 能 实现 完全 识别
6 优 缺 点 分 析 : 以 上 采用 的 是 单个 神经 元 的 网 络 进行 分 类 , 其 优点 是 运算 速度 快 , 但 模
式 分 类 正确 率 较 低
第 二 方案 ( 双 层 感知 机 , 即 BP 网 络 )
上 综述 :BP 神经 网 络 , 由 于 含有 隐 焉 层 , 所 以 可 实现 非 线性 分 美 BP 算法 居于 9 算法 ，
99. 08 Chin, ad r ctronic Publish: 0 1 rights reserve h w

<!-- source_page: 5 -->

加 成 守 沁 加

.

meE
50 HBo%oo9 Bk5 0 1 tien
是 一 种 监督 式 的 学 习 算 法

2 算法 推导 : ( 略 )

3 网 络 结构 (图 1. 5):

输 人 随机 感知 机 FIBAN

/一 一

pP al w2 二
R ay
-| ERA
十 诱导
[这 - 帮 -|
| 王 |
E
” 直 ADN S2
1 1 |
可 52
图 1.5 人 DA

4 训练 算法 : rasassaaaae 和 am

S 训练 和 模拟 结果 : 与 第 一 方案 相似 , 只 是 分 类 正确 率 有 所 提高

7 结论 : 本 题 所 给 数据 是 线性 不 可 分 的 8 而 且 通 过 简单 的 模式 分 类 也 很 难 行 得 通 , 所 以
即使 用 多 ( 双 ) 层 网 络 也 难以 实现 完 休 ;中

& 优 负 点 分 析 : 以 上 采用 的 是 区 人 秋 经 元 的 带 有 一 个 隐藏 居 的 网 络 进行 分 类 , 其 优点 是
运算 速度 较 快 , 且 模 式 分 类 正确 率 才 再 , 介 依 然 存在 不 可 完全 识别 的 问题

和

1 综述 为 了 改进 上 述 宅 沁 的 不 可 完全 识别 的 缺点 , 现在 对 网 络 进行 改进 , 其 目的 是 使
网 络 可 以 对 所 有 向 景 进行 正 崩 的 分 类

2 Us & aa 1 分 类 信息 为 原 网 络 结构 与 BP 神经 网 络 相似 , 但 随机 感
各 机 民 的 ii 用 sigmoid 函数

3 RH 网 络 相同 的 训练 算法

\4 结果 (分 类 正确 率 有 所 提高 , 这 里 晤 去 )

S 1 生 结 论 数据 是 线性 不 可 分 的 , 而 且 通过 简单 的 模式 分 类 也 很 难 行 的 通 , 所 以 只 是 简单
es 所 以 下 面 将 采用 其 它 方法 (LVQ 矢量 量化 学 习 ) 进
重负 式 识别

6 DRRAAIHT: 以 上 采用 的 是 改进 型 多 个 神经 元 的 带 有 一 个 隐藏 层 的 网 络 ( 也 就 是 改进
型 BP 神经 网 络 ) 进行 分 类 , 其 优点 是 运算 速度 较 快 , 且 模 式 分 类 正确 率 较 高 , 但 依然 存在 不
可 完全 识别 的 问题

第 四 方案 LVQ 学 习 向 量 量化 )

1 综述: 学 习 向 量 量化 (LVQ ) 是 在 监督 状态 下 对 竞争 层 进行 训练 的 一 种 学 习 算法 况
争 层 将 自动 学 习 对 输入 向 量 进行 分 类 , 这 种 分 类 的 结果 仅仅 依赖 于 输入 向 量 之 间 的 距离
如 果 两 个 输入 向 量 之 间 特 别 相近 , 竞争 层 就 把 他 们 分 在 同一 类

@ 1994-2008 China Academic Journal Electronic Publishing llrights reserved。 http:/www et

<!-- source_page: 6 -->

加
人
1 期 昌 金 起 等 : DNA 序列 分 类 的 数学 模型 ij
2 训练 算法 : (采用 经 典 算法 这 里 略 去 )
3 训练 和 模拟 结果 : (分 类 正确 率 有 所 提高 , 这 里 略 去 )
4 要 想 从 网 络 角度 和 学 习 算法 上 调整 , 使 得 对 已 有 的 数据 进行 正确 分 类 , 必须 进行 大 规
模 学 习 , 但 是 如 果 对 所 有 的 样本 进行 训练 再 检 策 网 络 分 类 能 力 , 其 可 信服 程度 就 大 大 降低
了 ， 所 以 最 后 将 采用 改进 网 络 输入 的 办 法 , 即 结合 生物 学 结论
5 优 缺点 分 析 : 可 靠 性 较 高 , 但 算法 复杂 度 较 大
第 五 方案 :
仅 从 神经 网 络 结构 上 的 角度 考虑 , 我 们 发 现 很 难 找到 一 个 很 好 的 网 络 ， 呈 随 他 %
学 重建 神经 网 络 As
引用 生物 学 的 结论 , 我 们 将 输入 模式 变 为 In
抽取 4 个 样本 100 表 示 A+ G) 含 量 的 输入 序列  l
采用 BP 神经 网 络 结构 训练 方案 采用 方案 二 中 的 误差 逆 传 播 算法
训练 和 模拟 结果 : CN
a) 从 20 个 已 知 结果 的 DNA 序列 中 随机 选取 不 wo 种 内 了 训练, 再 对 20 个 向 量
进行 重新 模拟 , 其 正确 率 为 95% 和 计 网 络 和 LVQ 向 量 量化
学 习 是 相同 的 ) , 发 现 出 错 的 原因 是 由 于 学 习 不 充分 造成 鸭 其 本 质 是 第 4 组 数据 和 第 17
组 数据 可 分 性 不 好 , 所 以 反应 到 网 络 上 其 可 学 习性 又 较 半 ; 但 如 果 学 习 不 足 , 则 会 导 制 误 判 ，
所 以 应 加 大 学 习 力 度
b) 每 次 从 20 个 已 知 结果 的 DNA 序列 利 睛 机 选取 不 同 的 4 个 向 量 进行 训练 ， 共 进 行 两
次 , 在 对 20 个 向 量 进行 重新 模拟 人 8 和 仙 这 为 100%， 这 次 的 结果 充分 说 明了 上 述 问题
结论 : 人 所 以 如 果 加 大 训练 力度 可 以 对 其 它 数据
进行 正确 率 更 高 的 分 类 我 们 对 网 络 进行 了 100 次 随机 抽取 , 每 次 抽取 的 结果 均 进 行 训练 ，
最 后 对 40 To
的 , 所 以 有 理由 认为 这 个 结论 的 正确 性
模拟 结果 序列 21~ 40 为 :
A 类 ;227 人 克 34, 35, 37, 39; B 类 :; 21, 24, 26, 28, 30, 31, 32, 33, 36, 38, 40
人 二 维 随机 游 动 模型
人 别 代表 复 平 面 上 四 个 不 同 的 方向 , 顺序 读 取 DNA 序列 , 得 到 一 条 由 原点
出 冶 的 每 次 相应 方向 移动 单位 长 度 的 轨迹 ”发现 曲线 明显 地 向 两 个 相反 的 方向 收敛 (图
六 GD7 我 们 依 此 建立 如 下 的 数学 模型
INJEDNA 序列 长 为 5 , 记 4w Go Cu 7, 为 1 到， 这 个 子 序列 中 碱 基 4 ,G,C,7 所 出 现 的
次 数 , 令 P, 为 复 平 面 上 的 点 , 且
Py=A,+ Gui- 7T- Co= Ud，- 7T)+ 1iG- C)= ae,
其 中 5 TO GCCcD58= Argp,B- 过于 8
假设 z= 0 时 ,4i= Go= Co= To= 0, 当 ”从 0 到 Z 时 ,在 复 平面 上 便 得 到 了 Z + 1 个 点 , 并 且
得 到 了 从 原点 出 发 的 一 条 游 动 轨 迹
) 鉴于 幅 角 信息 的 突出 重要 地 位 , 我 们 依 此 对 DNA 序列 进行 分 类 , 为 了 避免 那 种 螺旋 轨
1994-2 i cademic Journal Electroni blishing H 1I rights reserve http://ww net

<!-- source_page: 7 -->

本
52 数学 的 实践 与 认识 1 tien

迹 我 们 假设 DNA 序列 可 分 类 , 当 上 且 仅 当 3m EN ,s + Yn> p B 六 8 保持 定 号

模型 一 : 对 20 个 参数 已 知 的 DNA 序列 ,分别 求 出 其 相应 的 游 动 方程 Pi= C ，- Th)+
1G- co , 设 8. 为 第 ;类 第 / 个 DNA 序列 的 Argpx

6= Fre. 7 = 1,2,-,10, i= 1,2

在 每 一 类 中 求 出 ba- min 6, B max O, 从 而 得 到 每 个 类 的 种 角 特 征 区 间 [6la, 6 ] ，
如 果 [Ga Bls]n[ 人 sw @s]- 纪 , 则 对 任意 DNA 序列 , 若 可 分 类 , 则 满足 区 ,xx ee.] 的
属于 第 ; 类 ; 否则 , 不 可 分 类 = ks

显然, 这 时 存在 着 不 可 分 类 的 情形 , 这 主要 是 由 于 我 们 从 DNA 序列 样 想 和 志 届 了 两 类
游 动 在 辐 角 上 的 趋势 信息 并 将 作为 我 们 进行 分 类 的 标准 7
而 实际 上 总 有 限 , 前 面 关 于 可 分 类 的 假设 是 基于 对 游 动 辐 角 变化 总 体 是 私 的 一 种 控制
对 于 有 限 而 言 ,对 此 也 有 刻画 即 3 swN s + 当心 5，, 辐 角 保 所 区 信 息

模型 二 上面 模型 一 提取 了 DNA aa SS 这 里 我 们 假设 各 类 的
DNA 序列 的 8 在 如 下 变换 后 满足 正 态 分 布 首先 往 梨 值 可 以 与 复 平 面 中 的 圆周 上 的 点 奸
立 自然 的 对 应 关系 , 并 且 圆周 控 去 一 点 之 后 同 胚 了 天 * 直 绑 \ 为 方便 起 见 ,投影 后 的 点 仍 用 原
来 的 字母 表示 , 从 {9 : 1<) 三 10} 可 得 均值 w 和 方差 车 及 在 第 § 类 的 概率 密度 函数 为 P, (9
(8
外 。

任 给 一 个 DNA FE 区 的 祁 率 :

A & 9
P®- fn ET - —@
和 + (98 9+ 挛

以 概率 0 oo

下 面 再 用 区 间 估 起 法 给 出 结果 在 统计 意义 上 的 可 信 度 , 设 ， 个 相互 独立 的 样本 六
N OF 1.2%asd 2= CH) 各 则 7 (Z- 0)/(@/n)~ N (0.D，
en [GT 2)% Ca DG 22- 1)
代 蔡 ye @- OA AGO 记 因 天 w (00
0 LE 2)/07+ TCD 2)/0T+ + [GOPMo- D~ X (a-
NL BiTT 二 这 -MA 他 -ro- DREIR ¥ 55(50%/0) PHIMOL TREAE o
全 全 D 可 得 六 ,使 得 Pr(|i|< te)= 1 w 即 Pr(lz- alMsmM2s = 工
只 观 而 我 们 便 得 到 了 a 的 1- we 水 平 上 的 置信 区 间 为 [z- 六 sw 2+ 7Snma2] 现在
共有 10 个 已 知 样本 点 XXX as Xin 为 了 保证 与 (SmXOD) 相互 独立 , 现 将 这 10 个 样本
点 等 分 成 两 组 这 样 便 得 到 Z= Ci Xot 4 X9/5,2'= Ce e+, 7- (Z-
a)MCOAJIAO Se [Ce Z0H CT- Z2))+ AT Go 2)°1/(5- 1),1= (Z- a)/(55/
5) 2, 依 前 所 述 给 定 w 我 们 可 得 v 的 1-_w 水 平 上 的 置信 区 间 为 [z- 六 sw，Z+ TS
521

由 该 模型 可 以 看 出 曲线 的 趋向 正 代 表 着 序列 中 所 含 对 应 元 素 的 整体 含量 和 分 布 当 基
因 序 列 中 所 含 的 非特 征 随机 信息 较 多 时 ,会 导致 游 动 遇 线 昌 放 所 押 情 形 , 从 而 导致 前 进 号 离

1994-2008 Ac ic Journal Electronic Publishing ]l rights reserved， ht WwW.cnki.n

<!-- source_page: 8 -->

BliE
和
1 期 吕 人 金 翅 等 :DNA 序列 分 类 的 数学 模型 asa
变 短 , 但 是 由 随机 信号 在 各 方向 上 的 平均 性 , 总 体 前 进 方向 并 未 受到 影响 , 故我 们 只 提取 方
向 而 忽略 距离 作为 特征 信息
我 们 从 不 同 角度 , 提取 序列 整体 上 和 局 部 之 间 的 特征 , 建立 了 以 上 三 种 数学 模型 三 种
模型 各 有 优 劣 , 但 他 们 在 特征 提取 , 模式 识别 和 分 类 上 的 都 具有 一 定 的 普 适 性 和 优越 性
参考 文献:
[1] 郝 柏 林 , 刘 寄 星 理论 物理 与 生命 科学 上 海 科学 技术 出 版 社
[2] 金 冬 燕 , 金 ” 奇 , 侯 云 德 核酸 和 和 蛋白质 的 化 学 合成 与 序列 分 析 科学 出 版 社 #7
一
一 SS
<Z
The M athematical M odels on the Classir a tion
of The DNA Sequence
LU Tin-chi, MA Xiao-long, 4 ang
(The U niversity of Science and Technolo 和 Hefei 230026)
J \S
Abstract  This paper dealsw ith the problem of how to classity the DNA sequences from three
different angles and accordingly establishes three kinds of models
Firstly, on the point of biological backeiound and geometrical symmetry, we established a
descriptive model of 3-dmensio: d % curve on the DNA sequence, by which we got a
rudin entary mathem aticalmodel-Cajeul dsmodel Through the integration of themodel function,
we have acquired the classification results of the DNA sequences from 1 to 20, and found them
identical to the cr 让 iven by the problem. Then we classified the latter 20DNA
sequences )
Then, on the.view-of 中 neural networks, a second model - The A rtificial neural
networks 全 和 We chosen three kinds of basic networks, which well fit into
the classifi tion at last And by the same tine,we proposed the mprovementof theBP network,
and. gain comparatively ideal classification results by varius training programmes
also, id the results identical to what we have got by Calculus model
\ g end,we endowed A,C, G, T with geometrical meaning: A indicates right,while C as
有 9 asup,Tasleft We got amobile curve from each sequence with the points of theplain
As according to the controlling of theDNA sequence By follow ing the feature of themoving
人 NS themodel function was established By thewayweacquired the classification results of
the latter 20DNA sequences and found them practically identical to the results of the two above
models (One of results differently showed in this model is regarded as indivisible) This model
containsmore information, and ismore stable
> -2008 China Academic Journal Electronic Publish: Se 1lrights t ki.ne

