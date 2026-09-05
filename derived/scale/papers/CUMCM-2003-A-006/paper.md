# Extracted Paper

<!-- source_page: 1 -->

第 20 养 第 7 期 工程 数学 学 报 Vol.20 No.7 Hi
?03 年 1 月 JOURNAL OF ENGINEERING MATHEMATICS Dee 2003
文章 编号 :1005-3085$(2003)07-0029-06
\)
SARS 传播 的 数学 原理 及 预测 与 控制
邹 字 庭 ， 郑 晓 练 ， 继 旭 盈 _
指导 教师 ， 齐 吊 -从
( 必 门 大 学 ， 福 建 诈 门 361005) 2 =\)
编者 按 :本 文 建立 了 SARS 传播 的 具有 负 反 馈 的 差分 方程 模型 。 个
2 合理 性 ,是 本 文 的 突出 优
点 。 OO NS
摘要 : 众所周知 ,SARS 对 中 国 社会 带 来 了 重大 的 影响 。 我 人 4 月 到 6 月 有 关 SARS 的 数据
OO SARS 传播 的 负
反馈 系统 ,并 在 分 析 该 系统 参数 实际 意义 的 情况 下 , 建 了 时 间 序 列 的 模型 。 该 模型 将 传染 率 定义
为 时 间 的 函数 ,以 拟 合 数据 和 实际 数据 之 间 的 总 残 差 最 小 为 目标 ,利用 marlab 中 的 fminsearch 函
数 模 拟 得 到 最 优 的 模型 参数 。 访 模型 可 以 加 汪 的 预测 SARS 的 发 展 趋势 , 且 可 以 就 此 趋势 提出 如
何 控制 SARS 传播 的 措施 。 er 日 期 提前 或 潮 后 5 天 实施 隔离 政策 所 引
起 SARS 发 展 趋势 变 化 的 阳线 ,分 析 也 半生 哮 门 实施 隔 训 政策 的 日 期 对 SARS 发 展 趋势 的 影响 。
TH
疗 板块 指数 ,以 此 测度 医疗 业 的 苔 济 表 现 。 在 传统 的 CAPM 模型 中 ,我 们 引入 了 虚拟 变量 ,利用
ors 妇 术 进 人 kk 的 到 SARS 这 一 事件 对 医药 业 的 经 济 影响 是 正 影响 。 该 影响 反映 在 医
的 上 但 这 个 影响 是 由 SARS 引起 的 ,会 随 着 SARS 的 结束 而 结束 。
关键 词 : re ra
分 类 号 : AMS(2000 人 中 图 分 类 号 ; 0212.3 文献 标识 码 ; A
SAANS
1 让 an 分 析 与 建立
1.1 外 设 与 符号 说 明
1) 统 计数 据 是 可 靠 的 ;2) 病 人 处 于 潜伏 期 时 不 传染 他 人 ;3) 采 取 的 所 有 控制 措施 对 于 阻
止 SARS 病毒 的 传播 都 是 有 效 的 。I,: 到 第 n 天 为 止 累 计 确 诊 的 病人 数 ;D,: 到 第 n 天 为 止
累计 的 死亡 人 数 ;Su: 第 n 天 的 疑似 病人 数 ;Ca: 到 第 n 天 为 止 治愈 病人 数 ;d: 死亡 率 ;g: 治
愈 率 ;Si :新 着 肖 人 与 新 增 疑似 病人 的 比值 ;S :疑似 病人 转化 为 正常 人 的 比率 ;Ko: 区 域内
的 自 反 馈 参 量 ;F,: 反馈 变量 ;Ki: 反 馈 系数 。
1.2 现在 我 们 分 析 问 题 并 建立 相应 的 数学 模型 :
社会 的 反应 往往 是 一 个 渐变 的 过 程 ,会 哆 疫情 的 变化 而 变化 ,是 一 个 负 反 馈 过 程 , 比 如 ，

<!-- source_page: 2 -->

30 工程 数学 学 报 第 20 郑 es
当 疫 情 严重 时 人 们 会 自觉 地 减少 与 他 人 接触 ,相反 的 当 疫 情 不 显 著 时 人 们 会 放松 警惕 而 增
加 与 他 人 接触 的 机 会 。 为 此 我 们 建立 如 下 负 反 馈 系 统 (图 1)。 将 实际 情况 与 控制 力度 的 关
系 通过 反馈 系数 实现 自动 调节 ,这 样 就 能 及 时 采取 控制 措施 ,使 得 病情 传播 速度 迅速 碱 小 ，
以 求 最 后 达到 消灭 病情 的 目的 。

在 以 上 系统 中 ;
© A 是 开 环 增益 (Open Loop Gain) ,表示 基本 ® X, | EENAS Jo
放大 器 的 放大 倍率 , 即 为 输出 信号 与 输入 信号 的 比 二 EHTTN
值 。 在 研究 SARS 传播 的 模型 中 ,我 们 将 此 定义 为
SARS 病毒 在 未 受 榨 制 情况 下 的 自然 传播 速度 , 即
病毒 的 基本 传播 率 。@KIi 是 反馈 网 络 中 的 反馈 系 CIREYSS o
数 , 即 反馈 信号 与 输出 信号 的 比值 。 人 人 办
负 反 馈 可 以 减 小 病毒 传播 速度 。@ 和 输 和 人 信号 X 定义 为 当前 情况 下 SRS 的 人 莉 情 况 。@@
输出 信号 X, 定义 为 【时间 后 社会 上 SARS 的 传播 情况 。 Ji
令 通 过 以 上 系统 ,我 们 得 到 参量 A,Ki 与 输入 信号 (XXXS; 答 出 信号 (Xo) 以 及 反馈 信
号 Xf 之 间 的 关系 : WNs
Xo=4'X (1), X;=K;X, (2), PS + 和 (3)
定义 闭环 增益 (Closed Loop Gain)A 为 病毒 的 委 际 传播 率 , 定 义 反馈 深度 F ,表示 对 调
节 元 件 灵 敏 度 的 折 中 ,并 将 式 (0021G3) 代 人 则
-Zoo_- 4 p_  X_gX Xo_ _A
Ah= 守 = 一 F=1t 交 全 向 于 XoSITKeA A=
上 于 办
由 上 式 分 析 得 到
@ 当 反馈 系数 Ki<0 时 ,项 是 负 反 僻 的 ,这 正 是 我 们 需要 的 系统 。 这 样 社会 上 病毒 传播 束
度 即 系统 中 的 输出 量变 化 时 ,系统 参数 自我 调节 为 ; X 一 X 1 —=X  —K  —=A} =X|
@ 当 反馈 系数 区 > 时 ,系统 是 正 反馈 的 ,由 于 控制 措施 的 目的 是 阻止 病毒 传播 ,因此 Ki 不
sr 的 方法 是 错误 的 。 对 于 这 个 系统 来 说 ,可 以 不 考虑 这 种 情况 。
介 基 以 系统 的 分 析 , 我 们 考虑 建立 现实 的 SARS 传播 模 型:
和 SARS 确诊 病人 数 , 因 此 X 就 为 K,Xo 为 Ki,I 表示 到 第
FALRBEHHAL
| 请 人 时 间 , 以 天 为 单位 。
@ 选 定 某 一 区 域 为 研究 区 域 , 在 模型 中 建立 各 反馈 参量 ;
a) 设 该 区 域内 的 自 反馈 参量 为 K0 ,表示 该 地 区 在 未 采取 榨 制 措施 时 SARS 的 传播 能 力 。
b) 设 该 地 区 反馈 量 F。 的 变化 率 为 f, 即 每 增加 一 个 病人 引起 反馈 量 F, 的 变化 量 。f，
表示 该 地 区 的 病情 榨 制 情况 。
由 此 ,建立 以 下 时 间 序 列 模型 ，
F,=K¢+ f-(1,+S,) (1)
In=1,+FI,-C,—(D,-D,.,) (2)
Di=D+d(T-D-C (3)
SI=S,+(TL -TD) :SI -SS， (4)

<!-- source_page: 3 -->

二
第 7 期 SARS 传播 的 数学 原理 及 预测 与 控制 31
Ca Cg (9)
其 中 式 (1) 表 示 反 馈 量 是 自 反馈 参量 和 人 为 控制 后 的 反馈 参量 的 和 ; 式 (2) 表 示 确 诊 病
人 总 数 的 变化 情况 ; 式 (3) 表 示 死亡 人 数 的 变化 情况 ; 式 (4) 表 示 疑 似 病 例 数量 的 变化 情况 ;
式 (5) 表 示 治愈 病人 数 的 变化 情况 。 如 果 病情 得 到 控制 , 既 病人 不 再 增加 ,那么 反馈 量 应 该
是 0, 易 得 人 必须 为 负数 。 所 以
LimF,~0  Liml,.;~I,  LimD,,,~D,  LimS,,,~0
CT TTT
1.3 问题 的 求解 标准 关
设 实际 数据 为 Ta, 拟 合 数据 为 f， 则 我 们 确 | 2 -一 )
| 30 内 天 下
定 参数 的 目标 是 使 总 残 差 最 小 , 即 : minE = 二 | 20 入
(了 一 了 0)2。 我 们 用 matlab 中 的 fminsearch 函数 10 L_ = 一 | A
来 求解 ,得 到 总 残 差 最 小 时 的 参数 ko, 并 由 宽 ， 0 vaJ-
BER) QERRE 1, 发 展 欧 势 的 曲线 。 取 《江村 有
=) \ VAE SS
用 实际 数据 量 不 同 ,各 参数 以 及 最 小 总 残 差 便 不
同 。 模 拟 时 ,只 要 达到 一 定 的 数据 量 就 可 以 很 好 地 全线 ,我 们 以 标准 差 来 类 数据 量
是 否 已 经 足够 。 数 据 量 从 10 天 变化 到 64 天 ,标准 关 池 化 的 则 线 如 图 2 所 示 ;
将 标准 差 接近 平稳 状态 的 数据 量 取 值 区 间 抽 出 :
ER¥GO] B | 5i [5 [% [» [ s [% [ % [ a
村 水 症 14.097| 5.894  15.558 | 13 801 (15.76 | 5.762| 3.782] 15.80 13.816
可 见 ,数据 量 取 到 25 天 以 上 后 称 准 演 已 经 稳定 。 因 此 ,可 以 认为 拟 合 北京 市 SARS 发
展 趋势 线 只 要 取 其 从 4 月 1 日 开始 所 25 坟 数 据 即 可 。 因 篇 幅 有 限 贿 除 具体 计算 程序 。 取
前 25 天 数据 拟 合 出 的 各 发 展 本 各 姐 图 3 所 示
y|
—_~/
= 1 坟
男 v/ 中
NAY. AN “ ~ et
Te。 二 要 委员 本 | 一 一 一 一 全
IN 次 中
00  fn …- 死亡 病例 实际 发 展 曲线 和 d
4 es — 拟 合 的 死亡 交 例 发 展 曲线 ， 的
1000 f RNY ， h
ae 中
. = /
有 00012 oo
De 坝 丰 的 汐 轴 区 w 一 站
图 3 发 展 曲线 图 4 广州
该 曲线 图 不 仅 措 绘 出 25 天 的 发 展 情况 ,而 且 通过 预测 描绘 出 25 天 以 后 的 发 展 傅 况 。
对 比 25 天 后 预测 数据 和 实际 数据 :四 对 于 累计 确诊 病人 数 ,它们 之 问 的 标准 差 稳定 在 13，

<!-- source_page: 4 -->

二 ”这
32 工程 数 学 学 报 第 20 着 加
586 附近 ,因此 两 者 是 十 分 易 合 的 。@@ 对 于 自 似 病人 数 , 由 于 疑似 病例 的 判断 受 主观 因素 的
影响 , 拟 合 情 况 不 如 其 他 两 条 曲线 。@ 对 于 死亡 病人 数 ,吻合 程度 依然 比较 高 ,误差 产生 的
原因 可 能 是 个 人 的 免疫 能 力 不 同 这 个 原因 无 法 在 定义 的 反馈 系数 中 体现 出 来 。 由 此 可 以 看
出 以 上 的 预测 十 分 成 功 。
人 为 验证 该 方法 的 有 效 性 , 我 们 分 别 计算 了 广州 ， 山西 和 香港 的 累积 确诊 病例 发 展 趋势 ，
得 到 的 预测 数据 和 实际 数据 吻合 程度 很 高 , 可 见 该 方法 是 十 分 有 效 的 。 具 体 见 图 4- 6;
1.4 对 卫生 部 门 措施 的 评论
A) 对 发 展 趋 势 曙 线 的 影响 :
四 -次 ，
| 一 一
Soe 本 他 人
和 四 2
本 本 ADN
本 机 X
上
af 儿
机 -
人
CO 。 .
图 5 山西 %, 图 6 香港
图 7 体现 了 从 不 同时 间 点 到 提 前 或 潜 后 5 天 实施 限 离 政策 ,得 到 的 总 种 病人 数 随 日 其 的
发 展 变化 ,如 图 中 取 了 GD、@@、G) 鲍 个 时 间 点 。 原 始 数 据 反 哆 的 总 患 消 人 数 的 曲线 为 (), 若 提
早 5 天 采取 隔离 攻 策 , 则 册 应 四 个 时 间 点 的 总 患 病人 数 的 曲线 分 别 为 品 \ 四 \ 中 、 人 ,车 推迟 5 天 ，
ARHGH PRPHUBAL15..0 0. 从 图 中 可 以 很 明显 地 看 到 从 任 一
给 定时 刻 起 提前 号 天 采取 大 策 比 正常 情况 下 可 碱 少 一 定 的 患 靖 者 ,而 小 后 5 天 则 会 增加 惠 病 者
这 一 时 刻 取得 起 时 可 使 起 多 的 人 旬 于 得 病 , 因 而 政策 的 下 用 就 上 大 。
本 数 的 影响 ;( 图 8 中 的 每 一 对 点 对 应 统一 的 横 坐 标 )
Te 第 7 天 第 8 天 第 9 天 第 10 天 第 11 天
N WES5X 1.899 1.837 1.767 1.692 1.613
提前 5 天 0.62 0.653 0.689 0.727 0.766
影响 值 第 12 天 第 13 天 第 14 天 第 15 天 第 16 天
洁 后 5 天 1.532 1.452 1.376 1.306 1.245
提前 5 天 0.803 0.839 0.87 0.898 0.921
影响 什 第 17 天 第 18 天 第 19 天 第 20 天 第 21 天
滞后 5 天 1.192 1.149 1.114 1.086 1.065
提前 5 天 0.939 0.954 0.966 0.974 0.981
影响 值 第 22 天 第 23 天 第 24 天 第 25 天 第 26 天
滞后 5 天 1.048 1.036 1.026 1.019 1.014
提前 5 天 0.986 0.99 0.993 0.995 0.996
影响 值 第 27 天 第 28 天 第 29 天 第 30 天 第 31 天
滞后 5 天 1.011 1.008 1.006 1.004 1.003
提前 5 天 0.997 0.998 0.999 0.999 0.999
上 表 为 从 第 5 个 时 间 点 即 第 5 天 开始 考虑 提前 和 滞后 5 天 采取 隔离 措施 带 来 的 癌 确 诊
人 数 的 影响 ,影响 值 以 影响 后 的 总 确诊 人 数 与 无 影响 下 的 总 确诊 人 数 的 比值 表示 。 由 上 表

<!-- source_page: 5 -->

二
本
第 7 期 SARS 传播 的 数学 原理 及 预测 与 控制 33 0
本
和 图 7-8 可 见 , 越 早 实施 隔离 政策 ,最 后 总 确诊 病例 数 就 越 少 ,而 且 新 增 病人 数 就 越 快 接近
0, 这 意味 着 SARS 病情 越 早 得 以 控制 。
2 SARS 对 经 济 影响 的 数学 模型 分 析 与 建立
SARS 对 国民 经 济 的 各 方面 均 带 来 冲击 ,并 给 国民 经 济 带 来 重大 损失 ,但 同时 SARS 也
给 某 些 行业 ,如 医疗 业 带 来 正面 的 影响 。 下 面 构建 带 虚拟 变量 的 CAPM 模型 实证 检验
人 E |
L ci 四 - ; 本 J 本 :个 .
四 L 行 一
Le
四 得 和 1
 . 1 加 . kr . ’
站
下 本 一 ® 四 ” 由 习 加 团 加
图 7 对 发 展 趋势 曲线 的 影响 同 图 8 提前 或 滞后 5 天 的 总 确诊 病人 数
SARS 是 否 给 医疗 业 带 来 影响 和 多 太 称 度 的 影响 。 行业 的 股票 指数 在 一 定 程度 上 反映 了 整
个 行 业 在 大 经 济 环境 下 的 业绩 表现 sj/ 错开 数据 的 获取 从 hetp: //www. moneywise. com.
en/downsp. hum 取得 ,选取 的 时 段 从 2002 年 9 月 2 号 到 2003 年 6 月 30 号 。 选 取 的 股票
水 医疗 ,洒洒 区, 到 京介 人 有, 上 让 , 华 东 攻 , 二 思 医 ,
济 药 业 ,金陵 药 业 ,新 华 制 药 ,百科 药 业 ,四 环 药 业 ,东北 药 ,ST 海 药 , 恒 和 制药 ,云南 白药 。
定义 ; 为 入 1 肛 二 at B ARARERE 日 的 收盘 价 ;re, 医 疗 股指 的
半 收 益 率 。 构 建 医疗 业 板块 的 股票 指数 :以 等 权重 法 计算 医疗 业 股
BARARCRGAT HARR BA RERR Riisty
ZP Pr, Pue
Se 六 FE; = In Pg-1 Mt 二 2 Py -1
建立 模 型 如 下
(mi=a+RrxrrhtryD+e
p-|， t 处 于 2002 年 9 月 2 号 到 2003 年 2 月 11 号
1 t 处 于 2002 年 2 月 11 号 到 SARS 结束 以 后
其 中 D, 为 虚拟 变量 , 当 有 SARS 影响 时 D, 为 1 ,无 影响 则 为 0。 由 于 SARS 开始 的 日 期
为 2003 年 2 月 11 日 ,因此 采集 的 数据 时 往 前 至 2002 年 9 月 2 号 往 后 到 2003 年 6 月 30 号 。
a8,7 为 待 估计 系数 ,其 中 :a 为 截 距 项 ;jp 即 为 CAPM 中 的 “ 妈 系 数 ,用 以 衡量 个 股 (板块 ) 的
系统 风险 ;7 为 分 析 的 重点 ,如 果 y 统计 上 显著 异 于 零 , 则 说 明 SARS 对 医疗 业 发 生 了 显著
影响 ,并 且 影 响 程度 为 yiet 为 扰动 项 ;rr 为 无 风险 利率 ,在 本 模型 中 用 银行 3 月 期 存款 利率
测度 ;rw 为 市 场 指数 收益 ,本 模型 中 用 深圳 成 份 指数 测度 。

<!-- source_page: 6 -->

口 HRR3] 口 |
村
主人
a
34 工程 数学 学 报 第 20 卷
Ia
2.2.3 模型 求解
Variable Coefficient Std，Error t — Statistic Prob.
C —0.001428 0.001497 一 0.954424 0.3413
RM - RF 0.292576 0.088641 3.300665 0.0012
D 0.000213 0.002555 3.860554 0.0126
R — squared 0.766419 Mean dependent var -0.00137
Adjusted R - squared 0.7763 S.D. dependent var 0.01566
S.E. of regression 0.015227 Akaike info criterion 一 5.51277
Sum squared resid 0.036172 Schwarz criterion 一 5.45487
Log likelihood 441.2653 下 一 statistic 5.549341
Durbin - Watson stat 1.991851 Prob(F - statistic) .0.004697
从 表 中 可 以 看 出 :SARS 的 爆发 对 医疗 设备 ,医疗 药物 的 需求 带 来 了 冲击 性 的 影响 , 反 忠 在 医
疗 版 指数 的 日 收益 上 , 带 来 了 0.0213% 的 额外 日 收益 。 当然, 这 些 收 益 是 由 于 SS 乱 的 , 随 才
、 、 有 Y
SARS 的 平息 ,这 个 正 的 效益 也 会 随 之 平息 。 这 全 是 SARS 对 医疗 行业 的 经 济 影 响 SN
2
参考 文献  n
[1] 姜 启 源 , 数学 模型 . 北京 :高 等 教育 出 版 社 ,2002
[2] 邓 聚 龙 , 郭 洪 . 灰色 理论 .北京 :全 华 出 版 ,2002 )
0] HER BTAR- ABRR LRASUNLIL GING
[4] james D.Hamilton. 时 间 序列 分 析 . 北京 :中国 社 会 科学 迎 版 村 SN1999
/ TS
The Mathematical Principle Of The Spread Of SARS and Its
Application On Foreagy g and.Controlling SARS Epidemic
/
4 人情 |
ZOU Yu-ting, “ZHENG Xiao-lian, MIAO Xu-hui
_Advisor: TAN Zhong
(Xia en.| niversity, Xiamen, Fujian 361005)
和 =
Abstract: It is well kno 人 has a tremendous effect on Chinese society. Based on the statistics related
to SARS in Beijing/f1 om pril to June in 2003, we modeled the Negative Feedback system of the spreading of
SARS by introduci 7% concept of Negative Feedback System in electro - circuit and the nature of the SARS
virus. Mareov 品 b alyzing the practical meanings of the parameters in this system, a complete Time Se-
quel sr model is presented. It defines the spreading rate as a function of time, and adopts the fminsearch
fun fonin natlab to give the best parameters. with the object of minimum total difference between the actual
statist 中 nd computed results. This model well forecasts the spreading trend of SARS, according to which prop-
er advices can be put forward on controlling policies. Further, curves are drawn that simulate the different devel-
opment trends as the result of the quarantine carried out five days ahead of or five days later than a series of differ-
ent dates. Comparison between these curves makes it possible to analyze the impact exerted by the date when the
sanitary department carried out a quarantine.

Concerning the influence of SARS on economy, 17 representative stocks of medicine industry are chasen in
order to measure specifically and indirectly the overall trend of this industry in spreading of SARS. Dummy varia-
tions are introduced to the traditional CAMP model in order to verify the positive effect imposed on medicine in-
dustry by SARS epidemic, employing OLS technique. This positive effect was reflected by the daily interest cal-
culated from these stocks. Yet, this impact would be gone when its cause, the SARS epidemic, comes to an end.
Keywords: SARS epidemic; negative feedback system; time sequences; CAMP model

