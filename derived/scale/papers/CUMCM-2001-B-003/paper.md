# Extracted Paper

<!-- source_page: 1 -->

ES
口 [RE ] 口
a
和
第 19 卷 建 模 专辑 工程 数学 学 . 报 Vol 19 Sappa
2 年 吧 有 有 JOURNAL OF ENGINEERING MATHEMATICS
区
文章 编号 :1005-3085(2002)05-0089-06
Au 1
关于 公交 车 调度 的 优化 问题
傅 昌 建 ， 杨 彩 起 ， 素 级
指导 老师 ; 际 获 敏
《四 川 大 学 数学 学 路 ,成 部 5610064)
加 者 失 ; 本 文 以 公司 刑 才 作 为 目标 本 数 , 忆 李 率 错 述 的 匀 客 和 痊 作为 约束 条 件 ,建立 了 完 间 更 沦 坟 旬 由 于 具体 计算 时 使
用 了 过 于 简化 的 线性 规划 模型 .因而 答案 稍 火 一 些 。 oYAY
WOEEXTERFALTEMEORARGIE, ANELT— PUARER yah
等 车 时 间 超过 10 分 钟 (或 者 超过 5 分钟 ] 的 臣 客 人 数 在 总 的 等 车 薪 客 用 折 占 的 比重 外 于 一 个 事先 给 定 的 园 小 值 v。
首先 ,利用 最 小 二 薪 法 拟 合 出 各 站 上 (下 ) 千 人数 的 非 参数 分 布 郴 数 , 求 策 时 计时 一 种 简单 方法 估算 由 入 小 本 车 数 43
稍 。 畏 后 依 此 为 参 折 作 ,和 记 Mopk 优化 工具 得 到 一 个 整体 最 傣 半 RARFRRY $S.SAH TELXTAER
不 同 条 件 下 的 最 优 车 辆 调 庶 方 案 ,使 得 公司 的 收益 得 到 最 大 # 措 目 染 客 尘 硅 的 时 间 不 直 过 长 ,最 后 对 整个 模型 进行
了 推广 和 评价 ,指出 了 有 效 攻 进 方向 。 43)
基 链 说 ， 公交 车 调度 : 优化 模型 ; 是 小 二 萄 法
分 类 号 AMS(2000) 90008 中 国 分 类 号 : “名 文献 标识 码 : A
1 问题 的 重 述 ( 咯 )
2 基本 假设 @
4AAA
1) 该 公交 路 线 不 存 此 增 赛 现象 , 旦 公共 汽车 之 间 依 次 行进 ,不 存在 超车 现象
2) 公共 汽车 满 慢 后 ,乘客 家 再 上 ,只 得 等 待 下 一 辆 车 的 到 来 。
3) LA7 TATh lf J) 头 班车 同时 从 起 始 站 出 发 。
4) 该 公交 路 线 f 向 共 14 站 ,下 行 方向 共 13 站 。
5) 公交 对 均 为 同一 型 号 ,每 辆 标准 载 客 100 名 ,车 辆 满载 率 不 应 超过 1209% ,一 般 也 不
要 低 于 50%
6) Aob  - S 20 公里 /小 时 ,不 考虑 蒋 客 上 下 车 时 间 。
Rs 10 分 钟 , 早 商 峰 时 一 般 不 超过 5 分 钟 。
\ 了 始 从 Au 出 发 的 车 辆 ,与 一 开始 从 ao 出 发 的 车 辆 不 发 生 交 蔡 , 两 循环 独立 。
人
人 号 说 明
N
N N, :从 总 站 Al3 始 发 出 的 公交 车 的 总 次 数 《 上 行 方向 )
Ny :从 总 站 Ao 始 发 出 的 公交 车 的 总 次 数 ( 下 行 方向 ?
Ti :上 行 方向 旱 高 峰 发 车 间隔 时 间

<!-- source_page: 2 -->

a
90 工 程 数 学 学报 第 19 兰 ed
Ta :上 行 方向 平时 发 车 间隔 时 间
Ty :上 行 方向 晚 高 峰 发 车 问 隔 时 间
T4 :下 行 方向 早 高 峰 发 车 间隔 时 间
Ts :下 行 方向 平时 发 车 间 陋 时 间
Te :下 行 方向 晚 高 峰 发 车 间隔 时 间
Ti :第 ; 辆 车 到 达 第 ji 站 的 时 刻
NiGi 7 :在 站 离开 第 ; 辆 车 的 屁 客 数
NG 让 :在 站 上 第 ;i 辆 车 的 匀 客 数
DG 7 - 1 :第 7 站 与 第 (7 - 1) WEE
FUGY :上 行 方向 第 ; 站 的 上 车 乘客 的 密度 函数
&a(7) :上 行 方向 第 ) 站 的 下 车 乘客 的 密度 函数
户 (1) :下 行 方向 第 ; 站 的 上 车 乘客 的 密度 函数 %
£203) :下 行 方向 第 ; 站 的 下 车 乘客 的 密度 函数 =
G :一 天 内 公交 公司 的 总 收 人 “\)
A ;公交 车 出 车 一 次 的 支出 ,为 定 值 2
日 :公交 公司 每 天 的 固定 支出 ,为 定 值
ui = 1,2,3, 为 一 小 概率 事件 的 概率
NG) : 某 车 站 全 天 的 上 (下 ) 车 乘客 数 As
o ;第 : 时 间 段 此 站 的 上 (下 ) 车 人 数 SS ，
Qti ,1) :第 ; 辆 车 到 达 第 ee
4 建 模 前 的 准备
”对 问题 的 初步 分 析 oO
我 们 才 谨 三 组 相 关 的 因素 :人 . 汽 率 站 与 匀 容 对 模型 的 影响 。
D， 与 公共 汽车 有 关 的 因素 : 离 并 慌 共 汽车 总 站 的 时 间 ,到 达 每 一 站 的 时 间 , 在 每 一 站 下
车 的 乘客 数 ,在 每 一 站 的 停留 时 间 ? 载 窜 关 数 ,行进 速度 等 。
这 “与 车 站 有 关 的 因素 ;发 路 上 汽车 的 位 置 , 车 站 同 距 , 乘 客 到 来 的 函数 表示 ,等 车 的 乘客
数 ,上 一 辆 车 离开 车 站 过 去 而 四 问 等 。
过 ) “与 乘客 有 关 的 因素 上 到 达 某 一 车 站 的 时 间 , 乘 车 距离 (站 数 ) ,候车 时 间 等 。
2) 由 红 的 4 人 丰
np 可 知 对 于 某 车 站 全 天 的 上 (下 ) 车 乘客 数 N(z) 是 时 间 + 的 递增 函 琢 ，
NIt) = NC/Zn) + q ,其 中 9 为 第 z 时 间 内 此 站 的 上 (下 ) 车 人 数 ,我 们 可 以 由 此 来 拟 合 其 分
人
人 多 1
5 Dpiaens
分 析 样 本 数据 ,在 上 行 方向 22:00 一 23:00 和 下 行 方向 5:00—6:00 的 上 、\ 下 车 人 数 较 其 它
时 段 偏 小 ,为 使 模型 更 好 地 体现 普遍 性 ,我 们 单独 讨论 上 面 的 两 个 时 段 。 易 知 各 站 只 需 一 辆 车
就 可 以 满足 需求 。

<!-- source_page: 3 -->

二
旋光
建 模 专辑 关于 公交 车 调度 的 优化 问题 2
由 题 设 要 求 可 知 , 所 求 方案 须 兼 顾 染 客 和 公交 公司 的 利益 ,但 实际 上 ,不 可 能 同时 全
都 达到 最 优 值 。 因 此 我 们 将 公司 利益 作为 目标 函数 ,将 科 客 利益 作为 约束 条 件 。
公司 利益 Z = G—(N,+ N,) » A~ B
其 中 G 为 总 收入 , 因 样本 数据 为 典型 工作 日 ,因而 可 以 看 作 定 值 , (N。 + N,)<A+BX
支出 。
Mi -= [和 名 + 7 站 旬 ， 260, 5x60,
人 昌 和
乘客 的 利益 在 此 处 即 为 候车 时 间 ,由 于 急 客 候车 时 间 带 有 随机 性 ,不 可 能 总 小 于 (或 大 于 )
某 个 定 值 , 因 而 可 用 概率 来 描述 科 客 的 利益 ,得 如 下 模型，
T:maxZ = G— (N,+ NJ)%xA-B ~
s.o.PLSRERIE * > 10 SFEMAL < ai -从
PIQG 站 +N 门 一 ii) > 1201 < az =\)
PiQUi,z) + Ne — Ni(iyy) <50) < as 2XG
或 “P{ 等 待 时 间 * > 5 分钟 的 人 | < ai ， H
PHQ(i.j) + N(4,5) — Nilinj) > XpK
ec0vve00ra00xa 胃 ，
6 模型 的 简化 与 求解 人
对 于 原 模型 ,由 于 约束 条 件 难以 表示 为 贿 哆 的 语 数 表达 式 , 给 实际 求解 过 程 中 带 来 相当 大
的 困难 ,因而 对 其 简化 。
1) “发 生 间 焉 时 间 的 求解 自
分 折 原 目标 值 7, 史 知 piaxZomaw T 其 中 工 为 发 车 间 上 距 时 间 , 它 因 不 同 的 时 间 眉 而 不 同 。
站 -在
应 题 设 要 求 , 乘 窜 局 车 时 间 允 般 不 超过 10 分 钟 , 早 高 峰 时 一 般 不 超过 5 分 钟 。 我 们 引进 概率
参数 2 10 分 钟 (或 5 分 钟 ) 的 人数 在 总 侯 车 人 数 的 比重 。 对 于 满载 率
不 能 于 50% ,由 于 日 生 全 为 maxZ , 则 可 以 忽略 不 考虑 ,可 得 如 下 模型，
Il :max~T="¢
全
o 0
~) | filjar
R Qi 让 + 人 -Da =<120
T (141,0-5
Da
或 Srang  Se
|- fililde
了 Tb

<!-- source_page: 4 -->

2
= 至 一 -二 各 监 半 学报 第 19 着 加 只
Qli.j)+ 人 ce - [ atia < 120

t>0, i=1,2 )

分 析 样 本 数据 可 以 发 现 :

) ”对 于 上 行车 道 , Aba,Ala,AliAio,As 的 上 车 人 数 > 下 车 人 数 ,对 于 其 余 站 点 则 相
到 ;

让 ”对 于 下 行车 道 , Au,Az,As,A44 的 上 车 人 数 > 下 车 人 数 ,而 其 余 站 点 则 相反

因而 对 于 约束 条 件 , 只 需 取 前 5 个 (或 4 个 ), 对 于 模型 工 ,我 们 可 以 根据 拟 合 分 布 函数
FE,G; 将 约束 条 件 转化 为 工 的 范 数 ,利用 Matlab 软件 窜 易 求解 。 解 格 。

分 析 工 所 得 结果 , 易 知 在 高 峰 时 间 段 中 ,结果 有 较 大 误差 ,是 由 于 拟 合 函数 的 误差 而 引
起 的 。 为 了 碱 小 误差 ,可 以 分 狠 拟 合 分 布 函数 F,,Gi 。 为 计算 方便 ,可 以 认为 在 每 小 时 内 ,每
站 的 到 达 人 数 与 时 间 成 正比 ,每 站 的 下 车 人 数 亦 与 时 间 成 正比 , 即 Fift) =ks%1,G;(t) = p,
x 全 太 , 记 为 糙 率 , 令 e = 5% ,于 是 将 模型 简化 为 ， ARD

下 Ona 其 T 二 下 o 站

s.t. 19 -~ 200 委 0( 或 19: — 100 < 0) 2 \

kit —120<0 H
kit + kyt ~ par —120=0

Bit+ kat 一 pat + kst — pyt — 120<C0 人

kit + kat ~ pat + kyt — pat + kyt 一 Ae 0

KR1E 十 kat 一 pat + kyu — pat 十 天 4 人 pit 一 pst —120<0
t>0 X%

CEat BBRREI 19: — 200 <<O, E&oEH19: — 100 <0 )

当 上 行 时 , 取 所 有 约束 条 件 ,下 行 时 取 前 $ 个 约 东 条 件 。 模 型 于 为 线性 规划 ,利用 Matlab
求解 ,结果 如 下 ， O

LA/ 改定 本 是 时 间 家
RS

CEIREEEEIIECIICTIEENEZIEZ

EECIEEZIITZZ ET
Eapaa 相 panalaaaleea

EITHER
ZTEEEEEHCZIECIRZZIEZZIEEEIIZZ
EA \S HEA E1T.3.6 HERTFATCRR r Boa 5)
| 3 计 铺 型 册 、 加 进行 避 关 分析
Nr anenananinas RarmRLs THABRNRLILE. 如
上 向 Al13 站 的 7:00 -8:00, 发 车 间距 T=5.26 分 ,显然 此 时 的 工 无 法 便 3626 名 乘客 正
常 运行 ,而 此 时 由 拟 合 函数 算出 来 的 恨 客 总 数 为 2023。 误 差生 =3626 一 2023= 1603( 人 )。

为 使 误差 减 小 ,因而 可 以 对 函数 进行 分 妖 拟 合 。 如 模型 正中 ,以 每 小 时 为 一 段 。 此 时 求解

的 结果 ,能 很 好 的 使 样本 数据 的 乘客 正常 运行 。 当 然 此 时 的 解 亦 有 误差 e, 因 而 T 可 有 一 波动

<!-- source_page: 5 -->

E
Hi 寺
建 模 专 辑 关于 公交 车 调度 的 优化 问题
范围 。
在 此 解 的 情况 下 ,容易 知道 客车 满载 率 二 120% (约束 条 件 )。 习 客 等 待 时 间 过 长 的 概率 去
5% 。 空 载 情形 ,大 部 分 只 有 在 最 后 一 站 方 出 现 空 载 情形 (满载 率 <50% )。
2) 对 无 清国 乘客 条 件 下 的 最 小 配 车 数 初步 求解
我 们 对 数据 作 进 一 步 的 处 理 . 侍 算出 每 一 段 上 、 下 行 所 需 的 最 小 配 车 数 ,从 而 得 出 一 天 内
所 需 配备 的 最 小 车 辆 数 。 为 最 小 配 车 数 的 求解 找到 一 个 参照 值 。
我 们 首先 考虑 以 一 小 时 为 时 间 间 距 来 考查 一 天 的 最 小 配 车 数 ( 即 设 公交 车 在 各 车 站 所 停
的 时 间 为 一 定 值 ) 。 分 析 数 据 可知 满 足 各 站 均 无 滞 国 滋 客 .各 发 车 时 刻 均 有 车 可 发 的 最 小 配 车
数 应 为 65 辆 车 。 这 只 是 一 个 初步 解 , 为 得 到 进一步 的 精确 解 ,我 们 考虑 以 44 分 为 一 时 间 辣
距 , 通 过 拟 合 的 分 布 函数 得 到 各 车 满载 时 各 时 段 的 所 需 最 小 配 车 数 。 满 足 各 站 无 兴国 滋 客 .各
发 车 时 刻 均 有 车 可 发 的 最 小 配 车 数 为 43 辆 。
3) 公交 公司 调度 方案 模型 的 建立 与 求解 人体
上 HTE e A  R
总 可 四 大 可 能 少 的 汽车 以 降低 固定 成 本 ,又 要 在 保 还 接送 全 部 末 窜 了 二 六 下 尽 可 能 大 小 出
当权 本, 另 一 方 , 地 实现 玉 和 汪 意 , 色 搞定 村 段 必 定 有 车 可 肤 , 尽 可 能 缩
短 等 车 时 间 。 p. ~
W WITEETRN, RAKAA FHE: SA
A) 一 方 车 站 到 了 发 车 时 间 但 没有 车 可 发 , 另 一 闲 困 师 有 固 积 。 此 问题 有 两 种 解法 :一
购置 新 车 ,二 是 调节 班次 。 前 者 使 成 本 变 高 ,后 者 引起 连 寅 反应 ,使 整个 计算 量变 大 且 有 可 能
求 不 出 最 优 解 。 3
B) 不 人 要- 人 时 同人 和 全 人 本 ,全 所-
这 是 一 个 最 优 问题 。
C) 总 配置 数 一 定 ,调节 总 车 班次 使 总 车 次 数 增加 越 少 ,总 车 班次 数 越 小 , 则 求 得 的 解 越
优 。 RxR-HBUTLAR, O
为 解决 以 上 难点 ,我 人 二 人 HR 用 Maple 优化 软件 求解 。 设 某 时间 段
发 车 数 为 X，, 车 站 内 车 辆 总 朋 为 这 。
一 下 es 了
i= | 和 m 为 总 配置 数 ,z 为 总 班次
min 入 全 汪 7 4
2 qd m
7 和 1 = Cy -Xi 之 0
下 4 =Co— Xol 之 0
以 S- Xi = Ci+ 二 Xon 一 Xe >>0
N Xa, = Co+ SXin= 33¥an 0
二 xoo = PIEE
1) 60-120 调度 方案 模型

<!-- source_page: 6 -->

p
an
94 工 程 数学 学 报 194 人
若 考虑 到 各 站 点 乘客 上 下 车 时 间 相 等 ,交行 程 总 需 耗 时 60 分 ,每 辆 车 都 载 120 人 。 在 初
步 解 的 模型 中 ,配置 最 小 车 辆 为 60 ,用 Maple 软件 包 开 始 搜索 优化 选择 , ) = 2,3…18。
搜索 出 整体 最 优 解 为 : Ce = 62,C, = 4,m = 66,Z = 476 ,调度 方案 时 刻 表 略 。
2) ”44 一 120 调度 方案 模型
考虑 匀 客 上 下 车 肯 间 完成 ,公交 车 驶 完全 程 需 44 分 。 每 辆 车 均 载 120 人 ,此 模型 中 步 长
为 44 分钟, 所 考虑 时 段 的 乘客 数 均 由 拟 合 函 数 给 出 ,初始 值 为 43 辆 ,由 Maple 软件 包 优 化 选
择 , 得 到 ，
m = 48,Co = 42,C = 6,z = 590。 调 度 方案 略 。
7 模型 的 推广 与 改进
在 设计 公交 车 调度 方案 时 ,并 未 充分 考虑 乘客 利益 ,在 进行 收 进 时 ,可 以 试 头 想 其 它 办 法
找到 一 些 更 好 的 规则 来 进行 对 比 与 评价 ,从 而 得 到 更 加 优化 的 方案 ,使 驭 方 和 益 达 到 充分 均
衡 ,这 是 模型 改进 的 方向 。 另外 ,模型 求 得 的 阔 据 相对 精确 度 较 高 ,在 更 包 生涯 中 不 太 实 用 。
问题 的 关键 是 所 给 的 数据 太 少 ,所 得 到 的 调度 方案 稳定 性 很 差 ,灵敏 天 %w,m 久 试 着 找 其 它
方法 解决 ,从 而 求解 。 渗
表 们 事 立 了 一 个 方案 风 一 入 ,并 提 岂 了 一 个 名 全, 放 可 用
于 现实 生 话 中 其 它 运 输 业 的 调配 ,类 似 交通 运输 之 类 的 调配 间 题 ,从 而 达到 资源 的 优化 配置 。
WANs
8 ”模型 的 自我 评价 JSYV
我 们 通过 一 些 合理 的 很 设 , 针 对 公交 车 调度 问题 章 闷 了 一 般 模 型 。 先 对 模型 进行 了 简化 ，
采用 由 简单 到 复杂 ,逐步 深 人 的 方法 ,充分 利用 约 语 绾 做 软 件 包 进行 搜索 ,优化 求解 ,从 而 得
到 一 个 整体 最 优 解 。 在 求解 (2)? 小 题 时 ,提出 一 个 方法 , 即 每 歌 都 从 每 段 时 间 的 起 点 均 有 车 发
出 ,到 最 后 一 班车 持续 等 时 段 发 出 ,最 后 剩余 小 段 时 间 竺 去 不 予 考虑 。
列 出 了 不 同时 县 的 公交 车 调 讶 时 刻 表 。 同时 引 人 概 率 来 刻 划 顾客 利益 ,从 而 可 以 使 抽象
概念 定性 分 析 定 量化 ,也 是 本 模 蛋 药 7 赤 优 点 。
但 本 题 中 因 只 给 了 某 一 个 工作 日 的 数据 样本 ,具有 典型 性 ,得 出 的 结果 在 长 时 间 内 可 行 性
较 差 , 其 次 设计 调度 方案 时 蓟 年 考虑 公司 利益 与 大 部 分 顾客 利 益 ,使 双方 利益 趋 于 均衡 ,并 未
同时 达到 双方 满意 ,这 是 我 仙 杭 型 的 缺点 所 在 。
一
参考 文献 :
[] 要 月 新 - 数 assawaa
La] 时 其 孝 - 人 长 沙 :湖南 教育 出 版 福
i3] ce 北京 :清华 大 学 出 版 社
134] 之 枉 宁 下 - 效 学 模 王 实用 教 各 [M]. 成 者 :四川 大 学 出 版 社
洽 - { 下 转 100 页 ]
_ -

<!-- source_page: 7 -->

口 | ] 口
和
100 工 程 数学 学 # 第 19 郑 EER
————————————————————————————————————————
-| 科研 交流
of buses “fle in and out”during aperation period while we have mainly doue the research on the uneven vatiation of the passen
flow in ume and space, the research on the laws of how to dispatch buses and we have established atarget planning model whuch has
realized the dispatching Plan of "some carly and some late”and when there are more ,when there are fewer . Under the circum-
stances of ensuring certain banefits and the satisfaction of passengers, the overall operating time of the buses in operation has beea
made the shortest, the dispatching rimetable has been got ,while the nnmber for rhe least buses is 42 and the ratio of satisfaction be-
tween passengers and bus companies is 0.48:0 46
Key words:Bus Dispatching; Passenger Flow; Target-Planning
(上 接 94 页
P
Optimization of Dispatching Buses _ sv》
o\\
FU Chang-jian Yang Cai-xia Qin Min 一 \
Advisor:  CHEN Jip-min : (一
(SiChuan Universtty，Chengdu 610064) of
A/
Abstract :it to find out the best way to dispatch buses. We set a optumized mod | whose target function is the profit of bus com-
pany. At the same time, 1t guarantee the proportion that the passengers waiting - Ni more than 10 min [or S min)in the
toral la Jess than a given before First, every station’s nonparameter fisl nn funetion about the number of passengers js fitted by
method of least squares. We use a simple method to estimate that at least 4; SC are needed, and then, we use Maple to get the
optimal solution refer to it。 It shows the best plans for dispatching b Loss conditions of the number of hassengers，Ir can
help bus companny to get the top profic, meanwhile the passengers mm 二 wait for their bus for along time. In the end, we evalu-
ate and populsrize the model, and point out the effective way to smprove 1t
Key words: dispatching buses: optimized model; mathod of 有 squares
%A |
_— )
-一

