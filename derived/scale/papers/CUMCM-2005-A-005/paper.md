# Extracted Paper

<!-- source_page: 1 -->

第 22 卷 第 7 期 工 程 数 学 学 报 Vol. 22 No. 7
2005 年 12 月 CHINESE JOURNAL OF ENGINEERING MATHEMATICS Dec. 2005
文章 编号 :1005-3085(2005)07-0041-06
Z 全 、 |
长 江水 质 的 评价 预测 模型
BER, 张 东 辉 ， 张 ” 敏
指导 教师 : ”教练 组
(成 都 理工 大 学 地 球 科学 学 院 ， 成 都 610059)
编者 搜 : 本 文思 路 清晰 ， 家 述 流畅 ， 文 章 特点 是 ， 对 不 同 水 质 指 标 用 不 同方 法 做 标准 化 处 理 ， 再 综合 评价 ， 主 要 污染
源 位 置 的 确定 和 未 来 水 质 发 展 趋势 预测 等 问题 中 均 有 完整 的 数学 模型 。 不 足 之 处 必 ， 没 有 结合 长 江水 质 的 台
体 评价 。
摘 ， 要 :， 本 问题 是 一 个 对 长 江 的 水 质 进行 综合 评价 、 预 测 和 控制 的 河 题 。 首 先 对 各 项 数据 做 归 一 化 处 理 ， 得 建立 变 权
函数 ， 确 定 四 项 水 质 指标 的 污染 权 值 ， 进 行动 态 加 权 ， 根 据 水 质 污染 的 指标 对 长 江 17 个 观测 站 每 个 月 的 水 质
排序 ， 再 用 决策 分 析 方法 中 的 Borda 法 对 28 个 月 进行 水 质 综合 排序 。 先 假定 排污 口 分 别 位 于 江 段 上 游 和 下
游 的 情况 下 ， 取 均值 作为 江 段 单位 时 间 排污 量 。 在 对 长 江 未 来 水 质 污染 的 发 展 趋 势 作 预测 时 ， 通 过 可 饮用
水 ( 工 类 、 贡 类 、 瑟 美 ) 和 污染 水 (V 类 、Y 类 ) 的 比例 变化 来 进行 分 析 ， 建 立 排污 量 与 时 间 的 灰色 预测 模型，
得 出 未 来 10 年 的 排污 量 。 建 立 可 饮用 水 和 污染 水 与 总 流量 和 排污 量 的 -元 线性 回归 预测 模 起 ， 从 得 到 的 结果
看 ， 可 饮用 水 的 比例 逐年 减少 ， 水 污染 仿 来 你 严重。 关于 未 来 10 年 污水 处 理 量 ， 主 要 在 问题 3 的 基础 上 ， 得
出 长 江 的 极限 城 污 量 ， 与 预测 排 汽 重 相 减 ， 求 得 每 年 过 要 的 污水 基 。
关键 词 , Borda 法 ，-- 维 水 质 模型 ， 灰 色 预 测 ， 二 元 线性 回归 遥测
分 类 号 : AMS(2000) 92C35 中 图 分 类 号 : 0212 文献 标识 码 : A
1 ， 问题 重 述 及 模型 假设 《了 略 )
2 问题 分 析
问题 1 首先 应 采用 合理 的 方法 实现 数据 的 标准 化 。 其 次 建立 变 权 函数 ， 确 定 四 项 标准 物 的 污
染 度 权 值 ， 根 据 水 质 综合 的 指标 ， 对 长 江 从 上 游 到 下 游 的 17 个 观测 点 给 出 每 个 月 的 水 质 排序 。
再 用 决策 分 析 方法 对 28 个 月 进行 水 质 综 合 排序 。
问题 2 通常 认为 一 个 观测 站 〈 地 区 ) 的 水 质 污染 主要 来 自 于 本 地 区 的 排污 和 上 游 的 污水 。
把 7 个 观测 站 点 分 为 6 个 江 段 ， 计 算 各 江 段 的 排污 量 。 利 用 一 维 水 质 模型 可 以 得 到 每 个 江 段 中 污
染 物 浓度 变化 ， 再 通过 假设 排污 口 的 位 置 ， 结 合流 量 计算 各 江 段 的 单位 时 间 排 污 量 ， 以 此 确定
主要 污染 源 所 在 江 段 。
问题 3 分 两 步 解决 本 问题 ， 第 一 步 建 立 长 江 排污 量 与 时 间 ( 年 ) 的 数学 模型 ， 第 二 建立 各 级 别
水 比例 与 总 流量 和 排污 量 的 关系 模型 。 在 问题 3 已 建 模型 的 基础 上 ， 问 题 4 加 上 两 个 约束 条 件 ，
求解 得 出 长 江 的 极限 载 污 量 ， 进 而 求 得 每 年 需要 处 理 的 污水 量 。
3 ”模型 的 建立 与 求解
3.1 “问题 1 的 模型 建立 与 求解
3.1.1 数据 的 归 一 化 处 理

<!-- source_page: 2 -->

! 42 工 程 数 学 学 报 第 22 关 |
1) PH 值 的 谷 形 处 理 ，
由 限 值 表 知 ， 对 于 [VEMRA, PH 值 介 于 6 到 9。 在 数据 处 理 上 ， 我 们 认为 ， 由 于 中
性 液体 的 PH = 7， 随 着 液体 PH 值 远离 7( 即 大 于 和 小 于 ) 的 值 的 墙 加 ， 其 被 污染 的 程度 越 ，
: 大 ， 数 据 处 理应 反映 这 个 近似 谷 形 关 系 。 处 理 方法 为 ，
站 = 本 二 ) |
其 中 ，p 表示 第 ;个 地 区 第 大 个 月 的 PHA (6=1,2, ,17k =1,2,--+,28).
， 2) DO 值 的 归 一 化 处 理 ，
， 对 于 污染 物 而 言 ， 应 该 遵循 值 越 大 ， 污 染 越 严重 的 原则 。 但 对 于 溶解 氧 值 ， 含 量 与 污染 度
， 却 成 反 向 关系 ， 因 此 ， 所 选 的 未 局 度 函数 必须 是 一 个 减 函数 。 经 过 求解 ， 得 到 所 需 的 减 函数 隶 |
| 属 度 函 数 为
; = | 一 0.1348DPik +1, 0< Dy <75 @ |
; 0, Dix >7.5.
， 3) NH3- N 值 和 CODMn 值 的 归 一 化 处 理
! 针对 这 两 组 数据 的 离散 化 程度 并 不 是 很 高 ， 可 以 采用 根 差 变换 法 。
| _ Ny—min{Nu}
， xf 一 mintN ®
i 其 中 ，(G = 12…… ,17;K = 1,2,--,28). 于 是 得 到 17 个 地 区 28 个 月 的 NH3—N 的 归 一 化
， 值 nu。 同 理 ， 得 CODMn 的 归 一 化 值 cu ，
| 和， 归 一 化 处 理 结果 -检测 数据 年 阵 !
通过 上 述 数据 的 处 理 方法 对 附件 3 的 28 张 检测 表 进 行 处 理 ， 就 能 得 到 17 个 地 区 28 个 月 的 检
i 测 数据 矩阵 ， 4 人 三 下 2 ,1Tk=1,2,,28j=1,234)
| 3.1.2” 变 权 函 数 的 确定
分 析 附 件 3， 发 现 某 地 区 的 水 质 类 别 是 由 DO、NH3 - N 和 CODMm 含量 决定 的 ， 且 由
| 三 者 的 最 差 级 别 决定 ， 这 种 现象 定义 为 水 质 类 别 的 不 越界 性 。 定 义 限 值 表 中 工 ~ 劣 V 六 个 等 级
; 的 权 值 分 别 为 {zh zaizazdizs;z6}， 发 现 具 要 权 值 闻 满 足下 列 关系 ; ze : zs > 2 zs : za >
3，(zi zaz3) 相互 接近 可 以 有 效 地 防止 越界 的 发 生 。 ;
经 过 验证 ， 一 种 可 行 的 权 值 定量 化 为 zs = 2,25 = 9,ze = 18。 用 变动 权 值 的 办 法 刻画 模 精
评语 集 { 轻 度 污染 ， 中 度 污染 ， 严 重 污染 } 的 等 级 权 值 。 考 虑 到 人 们 对 于 明显 水 质 优 劣 有 强烈
的 感觉 ， 而 对 于 同一 个 级 别 的 水 质 类 型 感觉 上 的 差异 并 不 明显 。 通 过 心理 函数 ， 求 出 变动 权 ，
值 ri zaz4。 综 合 分 析 选取 Logist 模型 ， 利 用 Matlab 软件 的 非 线性 回归 命令 ， 求 出 曲线 方 ;
程 得 :
: 8
| ! 一 15+TT19GerITSGr059， @ |
其 中 ，y e zi(i = 1 2 …… ,6) 表示 六 个 等 级 的 变动 权 值 ，z 表示 经 离散 化 后 的 数据 。
， 利用 式 (4 处 理 限 值 表 ， 得 到 17 个 地 区 28 个 月 的 变动 权 值 抢 阵 的 。 对 权 值 归 一 化 处 理
; 大
! 一 一 到
5 (下 (5) ，

<!-- source_page: 3 -->

第 7 期 认 程 骏 等 ， 长 江水 质 的 评价 预测 模型 43
其 中 ，( = 4217 二 12 ,28)
3.1.3 17 个 地 区 28 个 月 的 水 质 污染 值
对 检测 数据 矩阵 4 多 和 变动 权 值 矩阵 wj5 进行 加 权 求 和 ， 得 到 水 质 污染 值 8 为
4
Sk=3akAk. (6)
i=1

3.1.4 17 个 地 区 的 水 质 综 合 排序

求解 得 到 17 个 地 区 28 个 月 的 水 质 综合 排序 可 以 得 到 对 长 江 流域 整体 的 污染 程度 进行 更 加 细
教 的 描述 。 现 在 采用 决策 分 析 中 的 Borda 法 进行 水 质 综 合 排序 。 用 Borda 法 处 理 数 据 ， 得
到 17 个 地 区 28 个 月 的 水 质 污 染 综合 排序 ( 见 表 1)。

表 1; 水 质 污染 综合 排名 〔 按 污 染 量 从 小 到 大 进行 排名 )
瑟 [本 [TAR
EEC 三
2 部 | m| [n| wedwex |_m
+ |enamn |n| [a [wigmeecn | we
+|awenwns |a| [n  amenann | w
有 ET
| [w | weeowr | w
站 ET mo| [u [mneomexe| w
ae | 2 | | | wassra | w
"| Ma |

3.2 ”问题 2 的 建 模 与 求解

3.2.1 ”模型 的 建立

某 一 污染 物 扩 散 所 满足 的 微分 方程 是 一 个 抛物 线 方 程 ， 结 合 实际 问题 的 假设 ， 常 可 假定 其
水 流 近 似 地 处 于 稳定 状态 ， 断 面 沿 程 均匀 。 普 遂 对 流 扩 散 方 程 为

BC BC B2C
ot tigr ~ Pam 一 AC， (7)
其 中 ，v 表示 断面 平均 流速 , v = Q/4(m/s)。

上 式 是 解决 污染 物 浓 度 的 一 般 原理 ， 结 合 问题 2 的 实际 情况 ， 进 行进 一 步 地 分 析 。 假 设 观
测 站 干流 的 污染 物 浓 度 在 一 个 月 内 保持 稳定 ， 则 ， 6C/6 = 0。 又 弥散 系数 D 是 分 子 热 运
动 造成 污染 物 扩 散 的 程度 大 小 ， 它 相对 于 江河 流速 w 来 说 是 微不足道 的 ， 可 以 忽略 不 计 ，
即 : 刀 = 0。 所 以 上 式 进一步 简化 为 ，

GC
u=""=kC, (9)

<!-- source_page: 4 -->

四 ENywwevipeon
44 工 程 数 学 学 报 第 22 着
其 中 ， 表示 断面 平均 流速 ，C 为 某 组 分 子 在 > 断面 的 浓度 ,大 为 讲解 常数 。 由 此 求 出 长 江干 |
， 流 污染 物 浓度 Cu 与 距 观测 站 长 度 > 米 的 函数 关系
1 Co = Cie -总 >， (9) ，
在 耻 离 上 游 为 时 河水 浓度 为
Cr = Cie- 二 上 (10) :
由 于 排污 口 的 位 置 难以 确定 ， 为 方便 处 理 ， 现 假设 排污 口 位 于 第 ; 段 干流 的 下 游 某 处 结合 |
| 上 式 ， 可 得 下 游 排污 口 排污 浓度 为 C!， 方 程 为
: 1 CiHLXQGi 一 Cn xd@i
: a N Qiv1 一 Q; ” (GD
1 又 假设 排污 口 位 于 第 ; 江 段 的 上 游 ， 其 排污 浓度 为
， CC = -5 (12)
把 排污 口 位 于 上 游 或 位 于 下 游 不 同情 况 下 的 平均 单位 时 间 排污 量 ! 平均 取 值 作为 此 江 段 上
的 排污 量 。 由 常识 ， 在 下 一 站 点 浓度 不 变 时 ， 排 污 口 位 于 上 游 的 排污 量 显然 高 于 排污 口 位 于 下
游 的 排污 量 ， 并 依次 作为 衡量 排污 量 多 少 的 指标 。 ，
! 综 上 所 述 ， 长 江 第 ; 段 干流 的 污染 物 平均 单位 时 间 的 排放 量 〈 毫 克 / 秒 ) 为
D; 入 al X (Qit1 Qi) 过 CI X (Qir1 一 Qi (13)
3.22 模型 的 求解 ，
对 于 一 维 单 河 段 永 质 模型 ， 两 种 污染 物 浓度 相对 较 高 的 河 段 就 是 高 多 酸 盐 指数 和 氨 握 的 污 ，
: 妇 源 主要 所 在 地 区 。 利 用 Matlab 软件 求解 得 ， 长 江干 流 近 一 年 多 主要 污染 物 高 鳃 酸 盐 指数 的
污染 源 主要 在 湖北 宜昌 到 湖南 呈 阳 段 、 江 西 九 江 到 安徽 安庆 段 。 氨 氨 的 污染 源 主要 在 湖北 宜昌
到 湖南 岳阳 段 、 湖 南 喇 阳 到 江 证 九江 段 。
: 33 ”问题 3 的 建 模 与 求解
3.3.1 ”长 江 总 流量 问题
分 析 长 江 每 年 总 流量 的 数据 ， 发 现 总 流量 是 随 年 份 随机 地 沉浮 变动 ， 总 的 来 说 ， 变 化 要 ，
小 。 因 此 我 们 用 均值 法 得 出 未 来 10 年 的 长 江 每 年 总 流量 ，
10
问
@= 写 (14) ，
; 其 中 ，@ 表示 未 来 10 年 的 长 江 每 年 平均 总 流量 ;4 为 1995 ~ 2004 年 的 长 江 每 年 总 流量 。
1 3.3.2 ”建立 长 江 每 年 排污 量 与 时 间 ( 年 ) 的 灰色 预 测 模型 〈 略 ) ，
3.3.3 ”建立 各 级 别 水 比例 与 总 流量 、 排 污 量 的 二 元 线性 回归 模型 |
，
i ;

<!-- source_page: 5 -->

第 7 期 堆 程 骏 等 ， 长 江水 质 的 评价 预测 模型 45
长 江 流域 地 域 广阔， 水 系 发 过， 属于 区 域 水 质 系 统 。 需 要 预测 枯水期 、 丰 水 期 、 水 文 年 三
段 时 期 的 全 流域 、 干 流 、 支 流 的 排污 情况 。 问 题 总 共 涉及 到 18 种 情况 。 建 立 模型 时 ， 只 需 研究
可 饮用 水 和 中 度 污染 水 的 各 9 种 情况 。
第 一 、 可 饮用 水 比例 的 二 元 线性 回归 模型 为
 = a  6Pn + Pn of). (1)
第 二 、 中 度 污染 水 比例 的 二 元 线性 回归 模型 为
2 =a) +6a + Paa +y2, (16)
其 中 ，y 表示 水 比例 ，( 廿 、(2) 分 别 表示 可 饮用 水 和 中 度 污染 水 ;zl 、z2 分 别 表 示 年 总 流量 和
年 总 排污 量 ;i = 1 2,3 分 别 表示 枯水期 、 丰 水 期 和 水 文 年 j=1,2,3 分 别 表示 全 流域 、 干 流
和 支流 。
由 (16) 式 可 以 得 到 长 江 在 三 时 段 、 三 个 流域 、 可 饮用 水 、 中 度 污染 水 比例 预测 模型 为
20 人 + 一 z00 (k +1) — 20) (k) = (a© (1) - §) (e=0% — e~olk-D)
CJCBPY CPCY JC JOO JYC AC J 3
这 样 求 得 未 来 10 年 的 可 饮用 水 、 中 度 污 染 水 水 量 比例 。 如 2005 ~ 2014 年 枯水期 全 流域 可
饮用 水 比例 分 别 为 ，57.524 54.003 50.29 46.372 42.24 37.881 33.283 28.434 23.317
17.92。 可 看 出 不 采取 治 污 措施 ， 可 饮用 水 比例 将 逐年 递减 。
3.4 “问题 4 的 分 析 、 建 模 与 求解
结合 问题 三 的 (GM(L 1)) 模型 预测 的 2005 ~ 2014 年 10 年 的 排污 量 2O) (k), FEFLEM
污水 量 为
Dr = #O(k) 一 minfzoz 纪 }
求解 得 ， 未 来 10 年 每 年 需要 处 理 的 污水 量 如 表 2 所 示 ;
表 2: 2005 ~ 2014 每 年 需 处 理 的 污水 量 (单位 : 亿 吨 )
秆 份 | 2005 | 2006 | 2007 | 2008 | 2009
EECIICCICGEZ
和 | 0 | an 2 | as | mn
OICIIEIIIEZ
4 ”模型 的 评价 、 改 进 及 推广 〈 赂 )
参考 文献 :
[1] 姜 启 源 ， 谢 金 蛙 ， 叶 俊 , 数学 模型 〈 第 三 版 ) [M]. 北京 ， 高 等 教育 出 版 社 ，2003，
[2] 韩 中 庚 . 数学 建 模 方法 及 其 应 用 [M], 北京 : 高 等 教育 出 版 社 ，2005
[3 王 华 东 ， 万 国 江 等 . 水 环境 污染 概论 [M], 北京 : 北京 师范 大 学 出 版 社 ，1984
[4] 袁 奈 平 ， 孙 志 忠 等 , 计算 方法 与 实习 [M], 南京 : 东南 大 学 出 版 社 ，2000
的 郑 彤 ， 陈 青云 . 环境 系统 数学 模型 [M], 北京 ， 化 学 工业 出 版 社 ，2003，
[6] 能 燕 ， 许 晓 东 . Borda 评 分 法 与 认可 票 法 的 联系 与 比较 [了 ]. 华中 科技 大 学 学 报 ，2005,22( 增 刊 ):132-133

<!-- source_page: 6 -->

: : FE bups ww equipcom]
1 46 本 程 数 学 学 报 第 22 卷 5
[7] 刘 圣 勇 . 一 维 水 质 模型 对 河流 污染 物 扩 散 的 简单 模拟 回 , 水 运 管理 ，2005,27(4):33-35
i The Model of Evaluation and Forecast for :
{ Yangtse River’s Water Quality :
3 QIAO Cheng-jun, ZHANG Dong-hui, ZHANG Min ;
Instructor: Instructor Group
. (Science of Earth Institute, Chengdu University of Technology, Sichuan 610059 ) :
站 Abstract: This issue focuses on making synthetical evaluation. calculation and controlling to Yangtse River's H
i water quality. Firstly, disposing of all data into one category, then establishing changeable value function, and :
: defining the pollution value of four items water quality indexes. We carry on dynamic additional power and ‘
: putting the water quality each month in oder which about Yangtse River's seventeen observatories according to E
H the indexes of water quality pollution. While calculating the development trend to twenty-eight months water

i pollution through Borda method of decision-analysis methodology, making analyze to the proportion change 1
between drinking water ( [ IIlllcategory) and sewage (IV Vcategory) and establishing the weather calculation 1
pattern of discharge sewage volume and time, to get the discharge sewage volume of the future ten years, also we 5
， build the secondary gender regression calculation pattern about drinking water and sewage with total volume :
H and discharge sewage volume. The results showed that, the drinking water’s proportion decreased year after
了 year and water pollution became more and more serious. Concerning the sewage treatment volume in the ten 3
| years future, we can get the limited sewage volume of Yangtse River on the basis of the questoin Three and

i subtract calculation sewage volume to defin. §
和 Keywords: Borda method; ashy calculation; secondary gender regression calculation; primary dimensional ;
; water quality pattern i
F ;
|

1
站

