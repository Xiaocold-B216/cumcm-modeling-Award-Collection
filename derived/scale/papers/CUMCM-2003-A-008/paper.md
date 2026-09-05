# Extracted Paper

<!-- source_page: 1 -->

、
ES
第 2 着 第 7 基 工程 数学 学 报 Vel,20 No7 =
?003 年 2 月 JOURNAL OF ENGINEERING MATHEMATICS 2 2
一 -一 一
文章 编号 :1005-3085(2003)07-0020-09
考虑 自 愈 的 SARS 的 传播 模型
李 贝 ， 徐 海 没 ， 郭 佳 佳 A7
(大 连理 工大 学 , 大 连 116024) 二 \S
er =
编者 按 ， 本 文 根 据 SARS ouaewanaaaaat anA As 全 amamia
治 站 (或 死亡 ) 而 具有 免疫 力 的 人 五 类。 考虑 自 念 和 控制 用 参数 乱 示 ) 建 立 了 微分 方程 席 型 和 村
拟 模 型 ,研究 了 疫情 随 各 参数 (包括 自 念 率 ) 变 化 的 规律 ,为 控制 疫情 提供 了 具有 一 定 参考 价值 的
意见 ,作者 如 能 通过 对 前 期 数据 的 分 析 去 确定 参数 , 则 模 表 还 能 发 挥 定 的 后 期 预测 功能 。 本 和
已 发 表 文章 的 主要 部 分 。 A
摘 要: 本 文 根 据 对 SARS 传播 的 分 析 , 把 人 群 分 为 5 类 : 易 感 舌 s 洪 伏 期 类 , 息 病 未 被 发 现 类 、 吕 病 已 被 必
现 关 和 治愈 及 死亡 组 成 的 免疫 类 ,并 考虑 自 念 因素 ,提出 了 两 个 模型 ,微分 方程 模型 和 基于 Smoll
World Nerwork 的 模拟 模型 。 对 微分 方程 模型 ,以 香港 为 例 讨 论 了 自 仿 的 影响 ,在 一 定 意义 下 说 明
自 外 现象 在 SARS 传 插 中 是 将 的 人 昼 抽 模型 利用 Small World Nerwork 模拟 现 实 中 人 们
ZRIERfEE Srnajd 模型 中 观 区 所 的 基 本 思想 "考察 区 域内 每 个 成 员 如 何 影响 与 共有 联系
的 其 他 成 员 ", 用 影响 类 比 传 网 * 从 惠 病 者 雪 传 妇 与 其 有 接触 的 健康 人 的 角度 , 异 拟 SARS 的 传播
过 程 ,然后 吸收 元 胞 自动 机 模 基 L 何 步 更 新 的 思想 ,最 终 建 立 了 一 个 如 病 者 传 浊 邻居 , 卫 一 个 成
员 同 时 受 所 有 久居 影响 的 革 下 Soul World Nerwork 的 村 拟 柄 型。 对 此 模型, 我 们 讨论 了 一些 主 要
参数 及 接种 疫苗 的 昌 而 ,最 后 拟 合 北京 数据 ,讨论 了 提前 或 推迟 5 天 采取 措施 的 影响 。
关键 词 : SARS; w /  slh Wori Network; Sznajd 模型 ;元 胞 自动 机 模型 ; 模拟
分 类 号 : 2 中 图 分 类 号 : 0241.81 文献 标识 码 : A
证 Ja 作品
1 E2 个 入 设 与 符号
攻 本 假设
(1) 假设 SARS 的 传播 方式 为 接触 性 传播 ,不 与 患 病 者 接触 就 不 会 被 感染 ;
(2) 假设 人 们 被 感染 后 需 先 进入 洪 伏 期 ,在 潜伏 期 内 不 具备 传染 性 ;
(3) 假设 SARS 患者 被 发 现 后 就 立即 被 隔离 ,被 隔离 者 不 具备 传染 性 ,SARS 患者 只 在
被 发 现 前 可 以 传染 他 人 ;
(4) 假设 SARS 康复 者 不 会 被 再 次 感染 ,并且 不 具备 传染 性 ;
(5) 不 考虑 在 SARS 传播 期 间 人 口 的 自然 出 生 和 自然 死亡 ;
(6) 所 研究 地 区 的 人 口 总 量 一 定 ,不 考虑 该 段 时 间 内 人 口 的 迁 入 迁 出 ;
1.2 ”符号 说 明

<!-- source_page: 2 -->

第 7 期 考虑 自 傅 的 SARS 的 传播 模型 21 . 加
N 一 我 们 所 研究 区 域 的 人 口 总 数 ;
S- 一 易 感 类 ,该 类 成 员 没有 染 上 SARS, 也 没有 免疫 能 力 , 可 以 被 传染 上 SARS;
E-- 一 潜伏 期 类 ,该 类 成 员 已 经 感染 了 SARS 病毒 ,但 尚 处 于 潜伏 期 ,还 不 是 SARS &
者 ,不 能 把 病毒 传染 给 S 类 成 员 ;
了 一 患 病 未 被 发 现 类 ,该 类 成 员 已 经 成 为 真正 的 SARS 患者 ,能 够 把 病毒 传染 给 S
类 成 员 ，
1 一 一 患 病 已 被 发 现 类 ,该 类 成 员 虽然 是 SARS 患者 ,但 由 于 发 现 后 立即 被 严格 隔离
不 能 传染 给 S 灿 成 员 ;R 一 一 免疫 类 ,该 类 成 员 为 SARS 康复 者 或 因 患 SARS 死亡 ,已 经 具
有 免疫 力 , 不 再 对 其 它 成 员 产生 任何 影响 ; =
下 一 -潜伏 期 天 数 ; 。。 工 一 一 传染 期 天 数 ; -从 ，
P——SWN 模型 中 每 条 和 连接 边 “ 断 键 重 连 "的 概率 ; -CN
CeaeaTiatatanmciasoar 和 一
Q—s oo
AS)
2 ”微分 方程 模型 ， 2
2 1 杰 开 建立
我 们 把 一 个 封 闲 区 域内 的 人 群 完备 的 分 成 5 类 :全 类. 眉 类, 忆 类 \ 二 类 和 及 类, 设 第
天 时 五 类 成 员 的 人 数 分 别 为 S(D).E
(DLL(D (DR(CD ,该 地 区 总 内 DF -ee
为 N。 入 和 WaxRIS [so P{ ro |
的 流动 情况 如 下 图 所 示 ;
So RSARERA
易 感人 群 的 比例 系数 ; 时 区
是 SARS 感 漠 者 的 且 发 病 率 ,w 是
SARS 感染 考 的 朋 n La ] ok [ae
at
是 锡 Vi NS
WRuns reasiansange aasuross SARS 传播 的
SETJNR 向 分 方程 模型 ，
3 S+E+I+L+R=N
[sa js E=0, I,20, [[=0, R2>0
I',=gE-zl, 其 中 ， 1
图 丈 罗
R'=cl,+ uE 0<g, z, c<1
2.2 模型 求解 及 结果 分 析
2.2.1 参数 意义 及 确定
(D 是 患 病人 群 每 天 接触 并 传染 易 感人 群 的 比例 系数

<!-- source_page: 3 -->

口 | 上 日
22 工 程 数 学 学 报 第 20 卷 =
人 一
易 知 o = 1g。 其 中 , 1 为 一 天 内 一 个 患 病 者 与 他 人 的 接触 率 , ;=
BARITERBAM | 为 一 个 易 感 者 接触 一 个 中 病 者 后 被 感染 的 概率
(2) e 是 SARS 感染 者 的 日 发 病 率 ,z 是 SARS 感染 者 的 日 自 傅 率
假定 每 个 SARS 感染 者 的 实际 潜伏 期 天 数 服从 区 间 [1 ,五 ] 上 的 均匀 分 布 。 也 就 是
说 ,SARS 感染 者 以 均等 的 概率 在 这 H 天 之 中 的 任何 一 天 发 病 或 者 自 僵 。( 为
光 伏 期 天 数 上 限 ) 容 易 得 到 :5+z = 二
(3) = 是 患 病人 群 每 天 被 隔离 的 比率 ,反映 了 社会 的 警觉 程度 及 政府 措施 的 力度 。
(4) “是 免疫 率 ,也 就 是 患 病人 群 每 天 病死 率 和 治愈 率 之 和 。 -从
_ 每 天 治 您 和 病死 的 人 数 本 眼 加 评 玫 和 二
易 知 !c= 三 人 沁 训 请 大头 妇 全 芝 , 可 以 根据 实际 数据 得 到 。 Z Shiaa
天 值 ,其 平均 值 即 为 所 求 ) A

2.2.2 模型 求解 及 结果 分 析 &

RA1GBE AT500 ZFH T0SIA0R B 52, O8 AR Mol 软件 中 的 oedS R
BETRIM. HILFAE, TURRERRARAE -RORR, FLRAGE
过 不 断 调整 非 确定 性 参数 (*,g ,wz) 来 使 实际 图 象 生理 论 图 条 赵 于 一 致 。 需 要 注意 的 是 ，
公布 的 SARS 日 黑 计 患 病人 数 是 (1) + R(1) - AE 从 |) 前 值 , 不 包括 未 被 发 现 的 SARS 串
病 者 (7) 的 值 。

(1) 与 公布 数据 的 比较 Ap 9e

我 们 以 香港 数据 为 例 。 人 670 万 ,把 N= 6.7x 10° 代入 微 分 方程 组 约
束 条 件 ,并 取 初 值 1.(0) = 1,S(0) = N21, B(0) = 1,(0) = R(0) = 0( 即 认为 起 初 有 一 个 人
突然 得 病 )。 人 和 根据 相关 资料 取 妞 = 10。 在 香港 这 样 一 个 大 都
BEPHEABCERAL s 总 人 口 为 670 万 , 旦 根据 概率 的 定义 9 值 应 该 在 0 到
0 -5 调整 参数 得 到 如 图 1 结果 。

-YY

TI
图 1 对 香港 疫情 的 分 析 ( 实 际 数据 从 4 月 25 日 开始 》 图 2 假设 不 存在 自 愈 对 结果 的 影响

可 以 看 出 方程 的 解 较 好 的 符合 了 实际 数据 。 此 时 各 参数 的 值 为 :z= 0.0000382,5 = 0，
0001,2=0.0999,2=0.4,c=0.014. ¢ 值 基本 符合 我 们 的 估计 ,结果 是 合理 的 。 同 时 得 到
5<w, 也 就 是 说 绝 大 多 数 SARS 感染 者 是 自 全 的 ,只 有 一 小 部 分 SARS 感染 者 病 发 成 为 丰
正 的 SARS 患者 ,这 与 钙 南 山 院 士 最 新 的 研究 成 果 也 是 一 致 的 Di

(2) 自 念 现象 对 结果 的 影响

<!-- source_page: 4 -->

第 7 期 考虑 自 愈 的 SARS 的 传播 模型 23 7

如 果 不 考虑 自 合 的 情况 , 即 = 0( 此 时 g= 0.1) , 仍 以 香港 为 例 (c=0.014)。 我 们 采取
极其 严厉 的 措施 , 取 = = 100% (此 时 基本 上 每 个 SARS 感染 者 一旦 发 病 就 立即 被 隔离 )。 在
这 种 最 不 利于 SARS 传播 的 情况 下 调整 o 值 , 在 o 的 意义 允许 的 范围 内 ,即使 将 其 调 到 非 党
小 (zc=0.0000002) ,仍然 得 到 如 图 2 所 示 结 果 。 即 :如 果 不 存 在 自 例 , 则 SARS 流行 时 间 的
跨度 成 倍增 加 ,起 初 疫情 发 展 组 慢 ,后 来 突然 恢 发 , 患 病人 数 激增 至 2. 1 x 105, 也 就 是 说 ,在
如 此 严 历 的 隔离 措施 作用 下 ,最终 仍 然 有 三 分 之 一 的 成 员 都 染 上 了 SARS。 这 ~ 结果 显然

是 与 实际 不 符 的 ,这 正 说 明了 自 愈 现象 是 确实 存在 的 ,而 且 对 结果 影响 相当 大 。

(3) 对 其 他 地 区 数据 的 拟 合

我 们 利用 对 香港 的 分 析 方 法 对 其 他 城市 的 SARS 传播 进行 分 析 。 以 台湾 为 例 (台湾 人
口 为 2270 万 ) ,得 到 以 下 结果 , 此 时 参数 取 值 为 = 0.000001128, g -op
09999,z=0.4,c=0.045。( 图 略 ) _ “\)

中 可以 出 我 们 的 不 人 和 人 和光 情 况 电 可 以 和 和 二 过 的 疫情 传播
对 于 不 同 地 区 ,只 要 选 到 合适 的 参数 都 可 以 用 该 模型 来 分 析 ， 人 / 多

任

3 基于 Small-World Network 的 模拟 模 =

roomaoa TasuenygROse Ens
, BLEL SARS 具体 传播 过 程 的 角度 出 发 ,提出 了 对 外 靳 的 模型 ; 即 基于 Sall- World Ner-
work, 并 吸收 Sznajd 和 元 胞 自动 机 (cellular automation) 模 型 思想 的 的 模拟 模型 。

3.1 模型 建立 及 算法 设计 , %

3.1.1 人 群 接触 情况 的 搬 述

用 Small World Nework 模型 模 作 说 代 注 会 网 络 m-m ,把 社会 中 的 人 们 看 成 网 络 的 节
上 各 人 们 之 的 天 的 起 行 有 客机 和
究 - 苛 上 取得 了 不 少 成 果 。 Y

我 们 从 一 个 含 NAFAGOTORANFATEG, B10 505 ERAEH K 个 节点 连
出 玖 条 边 。 风向 它 与 时 针 方 的 K/2 个 邻居 节点 以 妆 率 P“ 断 键 重
和 aas ga
重复 的 按 册 更 SN 这 是 对 人 群 接触 的 静态 描述。

祖上 你 构造 好 的 SWN 网 络 基础 上 ,每 隔 一 段 时 间 后 ,使 所 有 节点 都 以 概率 ) 被 选中 ，
eta 注意 不 能 与 处 于 陋 离 期 和 免疫 期 (死亡 者
无 法 接 危 ,而 病 愈 者 人 们 则 会 自动 琉 远 ) 的 节点 相连 。 这 是 对 人 群 接触 的 动态 描述 ,J 度量
了 网 络 内 部 节点 间 的 流动 程度 。

3.1.2 模型 建立

设 潜伏期 上 限 为 有 天 ,假定 SARS 感染 者 等 可 能 的 在 这 H 天 中 的 任 一 天 发 病 或 自 念 ，
根据 概率 知识 计算 得 到 ,处 于 潜伏 期 第 T 天 的 SARS 感染 考 转 变 的 概率 为 下 -二 , 设 每
天 转变 的 SARS 感染 者 中 自 傅 的 概率 为 了 ,自然 的 ,发 病 的 概率 为 1 - V.

设 第 ;天 时 五 类 成 员 的 人 数 分 别 为 S(i)、E(t)、 且 (5)、F(tD)、R(1) ,该 地 区 总 人 口 为
N。 一 个 易 感 者 楼 触 一 个 患 病 者 后 被 感染 的 概率 为 Q,SARS 患者 从 发 病 到 被 发 现 所 经 历
的 平均 时 间 ,也 就 是 传染 期 天 数 为 L SARS 患者 从 被 发 现 到 最 终 治 禽 或 死亡 所 需要 的 平均

<!-- source_page: 5 -->

二
a
24 工程 数学 学 报 第 20 卷
天 数 为 M , 则 各 关 成 员 之 问 的 流动 情况 如 右 图
所 示 : fad
加 一 Er 一。
根据 对 SARS 传播 的 具体 分 析 ,我们 按照
以 下 步 又 建立 SARS 传播 的 模拟 模型: 区 到
第 一步 ,构建 一 个 总 节点 数 为 N ,每 个 节 1xs
点 的 度 为 KBAIREENEEY 已 ,流动  f= L
程度 为 了 的 SWN 网 络 ;
第 二 步 ,初始 化 所 有 节点 的 状态 1STATE,EFT,IET,TRT1 ,随机 地 选 二 介 节 点 为
类 ,其 他 节点 艾 为 S 类 ;(STATE 为 节点 的 状态 ;EFT\IET.TRT 分 中 为 认 人 站 和
间 ， 即 为 节点 变 成 ELT, 类 后 经 历 的 时 间 ) =
第 三 步 ,在 当前 时 刻 ; 下 人 遍历 所 有 节点 : 2
1) 如 果 节 点 为 1,%,0 人 。 [六
4a) 饥 历 该 [类 节点 所 有 的 邻居 节点 , 若 邻 居 节 点 为 信人 1 S 类 节点 以 概率 Q
转变 成 下 类 ,同时 PFT 变 为 1; N %;
b) IFT 变 成 IFT+1, 若 此 时 IFT>L WEEE 类 ,同时 TRT 变 为 1;
2) 如 果 节 点 为 忆 类 , 风 外
a) 该 节 点 以 模 率 让 -RETT 被 选中 ,选中 的 节点 以 概率 V 转变 成 RR 类 , 知 则 转变 成
o
人 类 (同时 IFT 变 为 DJ
0) EFT 变 成 REFT+ 1 MA
3) 如 果 节点 为 了 类 , 则 TRT 肥 成 TRT+ 1, 若 此 时 TRT > M , 则 该 节点 转变 成 R 类 ;
人 在 此 记过 程 中 ,S BINGPRAUAR] WE EH0TALEE P HRTE:
5) 当前 时 刻 ， 变 成 1+ 1
6) 加 到 第 三 步 民 于 得 序 ，
3.2 人 V
2\% QuL 的 讨论
FR 四 遇 呈 . ) 多
ay y-..
并 7 INNER 网 E 4 T 0
”人
， AN A 5
双 四 ER 0 四 9
对 间 (天 ) 2 aa ~ a 时 间 〈 天 ) om 加 人
(1) L=10 (2) Q=0.1
图 3 SARS 的 实际 传播 率 Q ,传染 期 天 数 L 对 疫情 的 影响
(1) Q.L 对 结果 的 影响

<!-- source_page: 6 -->

第 7 期 考虑 自 愈 的 SARS 的 传播 模型 25 2
根据 Z 中 对 构建 SWN 网 络 的 要 求 ,N 六 KK 六 In(N) 1, 我 们 取 N= 105,K=20。 取 了
=0.02,M=30,H=10,% SARS 的 实际 传染 率 Q 传染 期 天 数 了 、 区 域内 人 们 的 流动 程度
JSARS 感染 者 的 自 您 率 V 作为 可 调 参数 。 用 当前 实际 患 病人 数 1. (+) + (1 来 表示
SARS 传播 的 实际 情况 。
取 了 = 0, = 0( 即 暂 不 考虑 人 员 流动 性 及 自 傅 ) ,固定 Q.L 中 的 一 个 ,讨论 另 一 个 取 不
同 值 时 对 结果 的 影响 。 图 4(1)、(2) 为 分 别 改变 Q 、L 的 情形 。
从 图 3(1) 可 以 看 出 , 当 工 一 定 的 时 候 , 随 着 Q 的 增加 , 患 病 高 峰 期 逐渐 提前 , 患 病人 数
的 峰值 逐渐 增 大 。 也 就 是 说 ,如 果 病毒 实际 传播 性 较 强 , Q 值 绞 大 ,该 区 域内 一 旦 有 人 患
病 , 病 帮 很 快 地 就 传播 开 来 。 值 得 注意 的 是 , Q 有 一 个 阅 值 Q., 只 有 Q > Q 时 该 传染 病 才
会 在 该 区 域内 开始 流行 , 否 划 该 传染 病 就 不 能 流行 。 如 图 ,在 二 = 10 sa
04。
从 图 3(2) 可 以 看 出 , 当 Q 一 定 的 时 候 , 随 着 L 的 也
就 是 说 ,SARS B (€ L 的 增加 将 加 蜀 SARS 的 传播 。 我 但 发 现 到 有 一 个 网 值 ,，
如 果 工 > , 则 SARS 将 大 规模 流行 ,否则 就 不 能 流行 。 5
综 上 可 得 ， .
Q@ 患 病人 数 的 峰值 随 着 Q 内 有 大 .人 人
非常 明显 的 改变 。 也 就 是 说 , 患 病人 数 峰值 对 Q 人 的 改变 更 加 敏感 ;
@ Q 的 减 小 将 使 高 峰 期 推迟 ,而 L 对 高 峰 期 影响 不 大 ;
@ Q 都 存在 一 个 阅 值 , 当 其 值 小 于 阅 值 时 ,SARS 不 会 大 范围 传播 , 当 大 于 阅 值 时 将
大 规模 流行 ; < ”
(2) 在 移 代 过 程 中 Q.L 变化 对 绪 全 的 影响
下
Er |
: 一 人 = 上 号 — } -1 四 :
SAT 人 于
他 N ? 全 人) 2 时 间 【天 )
SN (1) Q 改变 工 不 变 (2) 工 改变 Q 不 变
图 4 一 段 时 间 后 采取 措施 对 疫情 的 影响
初期 人 们 对 SARS 并 没有 任何 防范 , Q 和 :的 值 都 很 大 ,一 段 时 间 后 采取 措施 使 得 Q
和 工 减 小 。Q 和 上 的 值 碱 小 的 越 多 ,代表 相应 的 措施 力度 越 大 。 我 们 仍 取 J= 0,V= 0: 取
工 =12，, 分 别 取 0.09.0.11.0.13.0.15, 保 留 =0.2 的 曲线 作为 对 比 ,不 同 的 对 应 的 曲线 见
图 4(1); 取 Q= 0.2，, 分 别 取 3.6.7.8`.10 ,保留 = 12 的 曲线 作为 对 比 , 不 同 的 对 应 的 曲线 见
图 4(2); 从 图 4(1) 中 可 以 看 出 , 不 变 Q 减 小 时 ,在 Q* = 0.1 附近 出 现 突变 :Q* <0.1 时
患 病人 数 在 采取 相应 措施 后 立刻 减少 ,并 很 全 碱 到 0; 而 Q" >0.1 时 患 病人 数 在 采取 措施
后 仍然 继续 增加 ,只 是 上 升 的 速度 有 所 减缓 , 患 病人 数 峰 值 有 所 减 小 , 且 高 峰 期 推迟 出 现 。
从 图 4(2) 中 可 以 看 出 ,Q 不 变 上 减 小 时 ,在 工 " = 5 附近 出 现 突变 , 工 ">5 时 采取 相应 措施
能 使 患 病人 数 峰值 有 所 减 小 ,但 对 高 峰 期 影响 不 大 。

<!-- source_page: 7 -->

a
2

26 工程 数学 学 报 第 20 兰 oo

3.2.2 ”对 参数 ] 的 讨论

(1) 参数 ] 对 结果 的 影响

取 Q=0.1,L=12,Y=0, 改 变 / 的 值 ,得 到 如 图 5 结果。 可 以 看 出 ,区 域内 人 口 流动
性 越 强 ,病毒 蔓延 得 越 快 ,传染 的 人 越 多 ,疫情 越 严重 。

(2) 在 选 代 过 程 中 改变 对 结果 的 影响

Pv- § Th
§ eq - g os s 和 人
LE: &
Tn = 4 ° )  3° 写 辣 全 xm
人

图 5 区 域内 人 们 的 流动 程度 | 对 疫情 的 影响 图 ny 疫情 的 影响

取 Q=0.1,L=12,V=0,!=18 前 J=0.2, 因 为 时 间 震 因 , 这 里 仅 给 出 != 18 后 J= 0，
2 和 J=0.1 的 患 病人 数 峰 值 :Max[1L(t)+E(D] 2 类 Max[L (¢)+ 1,(¢)1J
=0.1=4.8104 ie

可 以 看 出 ,区 域内 人 们 流动 程度 J 的 减 小 也 使 患 病 兴 数 大 大 减少 ,疫情 得 以 缓解

3.2.3 对 参数 Y 的 讨论

BQ=0.2,L=10,]=0, ARAMA Y 的 值 ,得 到 如 图 6 结果 。 从 图 中 可 以 看 册 , 当
RCI VY 的 增 大 , 患 病人 数 减 少 ,高 峰 期 推迟 ,Y
超过 一 个 值 了 . 后 ,SARS 忆 能 传播 开 。 刀 图 得 -= 0.78。

3.2.4 的 人 和

在 初始 人 群 中 以 一 定 的 出 于 引入 已 接 各 闪 攻 的 成 员 ,将 这 个 比率 称 为 疫苗 接种 W,
BECRURHBARSTRUTAR LRLIRIA SRL2 & 类 成 员 。 按 照 与
RARD8 pi 则 /只 是 在 初始 化 时 赋 以 R 类 成 员 初 值 WN 即 可 。 取 Q=0.1.L=
10,7=0. ee 久 值 ,可 得 到 不 同 的 友 对 SARS 传播 情况 的 影响 。

和 不 同 的 疫苗 接种 率 多 下 ,SARS 传播 的 规模 相差 很 大 ,疫苗 接种 率 W
REL 5 站 百分点 ,相应 的 患 病人 数 峰 值 就 有 大 幅度 的 下 降 高峰 期 也 延迟 相当 一 段 时 间 。
值得 注 潮 的 是 , 当 史 为 20% 时 , 患 病人 数 非常 少 ,SARS 病毒 根本 不 能 够 大 范围 的 传播 开
来 。 这 一 结果 说 明 接种 疫苗 不 仅仅 是 使 单个 成 员 免 于 病毒 的 感染 ,更 是 切断 了 病毒 进一步
传播 的 途径 ,因而 能 够 出 现 SARS 病毒 从 一 开始 就 不 能 传播 开 的 情况 。 所 以 说 接种 疫苗 能
够 从 根本 上 杜绝 SARS 的 大 范围 传播 。

从 图 7 我 们 观察 到 凤 有 一 个 临界 值 , 当 超过 该 值 时 , 患 病人 数 基 本 为 符 。 下 面 我 们 讨
论 不 同 流动 性 的 区 域 对 这 一 临界 W 值 的 要 求 。 仍 取 Q = 0.1, = 10, Y= 0, 仅 改变 ,对
于 每 组 参数 组 合 ,都 有 相应 的 临界 W 值 , 当 大 于 该 值 时 患 病人 数 非常 少 ( 我 们 取 患 病人 数
峰值 小 于 50 为 标准 )。 结 果 如 图 8 所 示 。 也 就 是 说 ,要 狠 完 全 杜绝 病毒 的 传播 ,流动 性 越 强
的 区 域 所 要 求人 群 的 疫苗 接种 率 越 高 。 越 是 经 济 发 达 的 大 城市 , 越 是 需要 大 范围 接种 疫苗 。

3.3 对 北京 疫情 的 分 析

<!-- source_page: 8 -->

第 7 其 考虑 自 傅 的 SARS 的 传播 模型 27 机

2 H H H 外 ET 0.40

a er 人 30
1 站 . oa

EEC 0 0.10 020 § 030 0.40 0.50

图 7 引入 接种 疫苗 人 群 对 疫情 的 影响 图 8 区 域 成 员 间 流 动 性 / 与 疫苗 接种 率 W 的 关系

3.3.1 对 实际 数据 的 拟 合

综合 以 上 提 到 的 所 有 因素 ,下 面 拟 合 北京 的 疫情 发 展 情况 。 取 N =10",K=20,P=0.
02, M=30, 末 =10。 北 京 市 第 一 例 SARS 出 现在 3 月 1 的
25 日 起 公布 数据 ,近似 认为 从 此 时 (+= 56) 开 始 采取 措施 ,用 厂 (:) 的 累 下 值 搞 人 公布 数字
(从 采取 措施 起 参数 发 生变 化 ,未 取 采 措施 前 采用 10g 和 ee 调整
参数 拟 合 实际 数据 ,我 们 取 了 =0.1, 了 =0.6,, 得 到 图 9 结果 。 SA

- LAN

| ; ; : : 本 FE
L in 下 一
人 日 由

: 后 = 1 @ ， ee H ; ;

% 4 ais © wNL i * ”时 疝 ( 天 ) ” 多
图 9 对 北京 疫情 的 分 析 (实际 数据 从 4 月 25 人 图 10 提前 或 延迟 采取 措施 的 影响

3.3.2 We

保持 上 述 参数 不 变 , 仅 的 也 有 人 时间 统一 基 iD 可 和 前 (
退 )5 天 采取 措施 的 结果 ( 闫 疼 10) 。 可 以 看 出 ,仅仅 推迟 5 天 采取 措施 ,就 会 使 患 病人 数 峰
值 从 2523 增加 到 / 64 让 蕊 入 衣 终 得 以 控制 的 时 间 ( 即 内 线 开 始 趋 于 水 平 的 时 间 ) 往 后 推 。
CO 也 就
是 说 ， ww 程度 对 SARS 疫情 的 影响 很 大 ,政府 部 门 能 否 尽 早 认识 到 问题 的 严重
人 和 错 施 对 SARS 疫情 的 发 展 起 到 了 至 关 重 要 的 作用 。

3 人 模型 评价 及 改进

3.4.1 模型 评价

(1) 本 模型 首先 采用 SWN 模型 构建 区 域 结构 , 较 好 的 模拟 了 现实 中 人 们 之 间接 触 情
况 ,为 问题 的 进一步 的 解决 建立 了 较为 合理 的 基础 ;

(2) 本 模型 在 模拟 SARS 的 实际 传播 过 程 时 ,同时 吸收 了 Sznajd 和 元 胞 自动 机 模型 中
的 合理 之 处 , 按 弃 了 其 中 不 符合 本 题 实际 问题 的 成 分 。 做 到 了 既 从 每 个 成 员 影 响 他 人 的 角
度 考虑 问题 ,又 能 实现 同步 更 新 ,认为 一 个 成 员 下 一 时 刻 的 状态 是 受到 当前 与 其 接触 的 多 个
成 员 影 响 累 加 的 结果 ,这 些 都 是 非常 符合 现实 情况 的 ;

3.4.2 模型 改进

(1) 可 以 采用 Scale-free Network 模型 49 , 它 更 能 反映 现实 中 人 们 之 间 联 系 的 先 取 连 接

<!-- source_page: 9 -->

直人
28 工程 数学 学报 第 20 卷 —
性 (Preferential Connectivity) ,也 就 是 说 ,实际 中 每 个 节点 的 度 并 不 都 是 相同 的 ,而 是 存在 一
些 关 键 节点 ,和 它们 相连 的 节点 数 比 其 他 节点 多 。 可 以 对 这 些 关键 节点 进行 研究 ,比如 ,这
些 关 键 节点 如 果 患 病 或 者 接种 疫苗 会 对 结果 产生 什么 影响 ;

(2) 在 运用 SWN 模型 时 ,对 于 和 一 个 节点 相连 的 2K 个 节点 ,到 该 节点 的 路 径 权 值 应
该 是 不 相同 的 , 即 和 某 成 员 有 联系 的 2K 个 成 员 有 亲密 朴 远 的 差别 ,他 们 被 传染 上 SARS 的
概率 是 不 同 的 。 我 们 可 以 使 节点 与 其 原 邻 居 节 点 之 间 的 路 径 权 值 取 do ,与 非 原 邻居 节点 之
间 的 路 径 权 值 取 凡 ,自然 的 ,2o> 凡 ;
参考 文献 :

一
[1] Wartts, D.J. and Strogatz，S.H，Collective dynamics of "small-world” networks(]] Ra

440-442 全 一 \)

[2] Dietrich Stauffer. Sociophysics: the Sznajd model and its applications[]]. Hare Communica-

tions 146(2002) . 93-98 人
[3] G. Ch. Sirakoulis. I. Karafyllidis. A. Thanailakis. A cellular AR for the effects of popula-

tion movement and vaccination on epidemic propagation[J] Ecolog cal fodeling, 133(2000), 209-223
[4] 唐 焕 文 贺 明峰 ,数学 模型 引 论 ( 第 二 版 )[M], 北京 : 和 这 和 2001
[5] 姜 启 源 数学 模型 (第 二 版 )[M]j , 北京 :高 等 教育 出 版 beg93
[6] Jan Medlock, Mark Kot, Spreading disease: integro-differe equations old and new[]], Mathematical

Biosciences, 184(2003), 201-222 @

[7] Eco sn 和 on [EB/OL]
[8] Francesc Comellas. Michael Sampels: Deget ninistic small-world networks[]], Physica A 309(2002),

231-235 2002 4 )

[9] Barrat and Weigr, On  pi of small-world network models[J], Europhysics Journal B, 13

(2000), 547-560. 全
[10] L. A. N. Amaral"A:Scalas M，Barthe le'my, and H. E. Stanley Classes of small-world networks

[1]. PNAS, -Y RE21(2000) 11149-11152
[11] M. E. §7 Newm Ys J. Watts, Scaling and percolation in the small-world network model[J].

ron E gacom. 7332-7342
[12]_ Tangtba M. Read.Matt ]，Keeling，Disease evolution on networks: the role of contact structure[J]，

1 Soc. Lond. B, 270(2003), 699-708
119 Woo T. Britton, Epidemics: Stochastic models and their statistical analysis[]], Springer Lec-
ture Notes in Statistics, Vol. 151(2000), Springer, New York
[14] Damian H. Zanette * . Marcelo Kuperman, Effects of immunization in small-world epidemics[J] Physi-

ca A 309(2002) , 445-452
[15] Octavio Miramontes. Bartolo Luque. Dynamical small-world behavior in an epidemical model of mobile in-

dividuals(]], Physica D, 168-169(2002) : 379-385
[16] Romualdo Pastor-Satorras and Alessandro Vespignani, Epidemic Spreading in Scale-Free Networks[]].

Physical Review E, 86(2001), 3200-3203 (下 转 44 页 )

<!-- source_page: 10 -->

:
站 加
可
a
Cha
44 工程 数学 学 报 第 20 卷 Te
ggrs
参考 文献 :
[1] 姜 启 源 . 数学 模型 [M]. 北京 :高 等 教育 出 版 社 ,1993
[2] 赵 达 纲 , 朱 迎 善 . 应 用 随机 过 程 [Mj, 北京 :机 械 工 业 出 版 社 ,1993
[3] 疗 新 等 ,Matlab 神经 网 络 应 用 设计 [M] , 北京 :科学 出 版 社 ,2000
[4] Shi Yaolin，Stochastic dynamic model of SARS spreading[]] .www science.com,2003;9
The Study of the Spread of SARS
一
XIAO Hong-jiang， WU Tong， LI Ming-ke 一 SS
Advisor: HE Zu-guo 人 由
=
(Beijing University of Posts and Telecommunications, Beijing 大 AN
Abstract: This article compares the model in the attachment 1 ,and exa ns ts ethod lled "Half - [mitation —
Circulation - Calculation” . The advantage of the model is itsease ,its high| pi the aspect of imitation ,and
3
its reasonable change of the value of "K".At the same time, we SAVA hat its main drawback is that it de-
pends on the data excessively and is not able to predict the sir latio 也 for, longer time. In the second question, we
bring up four models which are based on four different core metheds: (1) he model based on differential and dif-
ference equation; (2) the controling — model based on filter; (3) the model of neural network; (4) the simulation
model based on Branching Process. In Model 2 ,we conclude that SARS will last 99 days in Beijing; the earlier it
is controlled, the better it will become;and SARS 让 品 cbreak out preodically. In the third question ,we are en-
lighted by the ”consequense function” in sp 人 we bring in three different influential functions to draw out
"an influential model of the foreign visitors 护 4 ce draw a conclusion that the city of Beijing will lose 1 ,382 ，
110 foreign visitors due to SARSaFEinally ，we give a short composition to be printed on the local newspapers.
Keywords: filter; neural network Te process
(上 接 28 页 ) ”一 y
oo the SARS Epidemic Considering Self-cure
下 4 LI Bei，XU Haixuan， GUO Jiajia
¥ ( Dalian University of Technology, Dalian 116024, China )
V¥/,
Ai this paper, a SEIuliR (susceptible, exposed, unisolated infectious, isolated infectious, recovered)
model with self-cure is built to model the SARS epidemic. The problem is solved with two methods: one is ordi-
nary differential equation which we then come to a conclusion that self-cure indeed exists in the SARS transmis-
sion; the other is computer simulation based on the small-work network which we also absorb the basic ideas of
the Sznajd and the cellular automation model, and then we discuss some parameters and the effects of vaccina-
tion. At last we analyze the epidemic situation in Beijing and estimate the results if control measures are taken 5
days later or earlier.
Keywords: SARS; Self-cure; ordinary differential equation; Small-World Network; the Sznajd model; the cellu-
lar automation model; simulation

