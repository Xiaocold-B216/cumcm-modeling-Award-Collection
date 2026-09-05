# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
B
第 19 卷 建 模 专辑 工程 数学 学 报 Vol. 19 Supp.
2002 年 0 月 JOURNAL OF EN GINEERING MATHEMATICS Feb. 2002
文章 编号 11005-3085 (2002) 05-0089-06
AY AN FRR N 让 忆 下 日
关于 公交 车 调度 的 优化 问题 -
人 人 A
傅 昌 建 ， 杨 彩 霞 ， 秦 人 敏 = 蛋
指导 老师 : Wel 2XG
(四 川 大 学 数学 学 院 ,成 都 610064) ~
SBe ASCOUA FLREE ERER B DURR ABO FIZS 1  arT selgmie . on F supi senya
用 了 过 于 简化 的 线性 规划 模型 ,因而 答案 稍 大 一 些 。 WA \
等 车 时 间 超过 10 分 钟 (或 者 超过 5 4H00) 10Tes JSLLE R AE M  0 Le TT— AE  s OBMi o.
首先 ,利用 最 小 二 乘法 拟 合 出 各 站 上 (下 ) 车 人 数 的 非 参数 分 布 讨 故 求解 讨 先 用 一 种 简单 方法 估算 出 最 小 配 车 数 43
辆 。 然 后 依 此 为 参照 值 , 利 用 Maple 优化 工具 得 到 一 个 整体 最 优 解 瀑 小 配 车 数 为 48 辆 ,并 给 出 了 在 公交 车 载 客 量
不 同 条 件 下 的 最 优 车 辆 调度 方案 ,使 得 公司 的 收益 得 到 最 大 ,并且 乘 客 等 车 的 时 间 不 宜 过 长 ,最 后 对 整个 模型 进行
了 推广 和 评价 ,指出 了 有 效 改进 方向 。 O
关键 词 : 公交 车 调度 ; 优化 模型 ; 最 小 二 乘法 他 H ©
分 类 号 : AMS(2000) 90C08 中 图 分 类 SEEB )Y 文献 标识 码 : A
4 区
1 问题 的 重 述 ( 略 ) 运
3 用
2 基本 假设 . ¥
1) HATHATAR BAELAKTL ,不 存在 超车 现象 。
2) 0 载 后 ,乘客 不 能 再 上 ,只 得 等 待 下 一 辆 车 的 到 来 。
3) k CA
) i < 路线 上 行 方向 共 14 站 ,下 行 方向 共 13 站 。
] V 公交 车 均 为 同一 型 号 ,每 辆 标准 载 客 100 名 ,车 辆 满载 率 不 应 超过 120 % ,一 般 也 不
昌 慌 书 50 % 。
国 ” 客 车 在 该 路 线 上 运行 的 平均 速度 为 20 公里 /小 时 ,不 考虑 乘客 上 下 车 时 间 。
7) “乘客 侯 车 时 间 一 般 不 超过 10 分 钟 , 早 高 峰 时 一 般 不 超过 5 分 钟 。
8) 一 开始 从 An 出 发 的 车 辆 ,与 一 开始 从 Ao 出 发 的 车 辆 不 发 生 交 蔡 ,两 循环 独立 。
3 ”符号 说 明
Ne :从 总 站 An3 始 发 出 的 公交 车 的 总 次 数 ( 上 行 方向 )
Ni :从 总 站 Ag 始 发 出 的 公交 车 的 总 次 数 (下 行 方向 )
Ti :上 行 方向 早 高 峰 发 车 间隔 时 间
4 1994-2006 China Academic Journal Electronic Publishing House 1 rights reser t ww.cnki.n

<!-- source_page: 2 -->

ERi
SANE
90 工程 数学 学 报 第 19 全
:上行 方向 平时 发 车 间隔 时 间
7 :上 行 方向 晚 高 峰 发 车 间隔 时 间
Ti :下 行 方向 早 高 峰 发 车 间隔 时 间
5 :下 行 方向 平时 发 车 间隔 时 间
7T6 :下 行 方向 晚 高 峰 发 车 间隔 时 间
TL(i,) :第 了 辆 车 到 达 第 /站 的 时 刻
Nif7 放 :在 7 站 离开 第 ; 辆 车 的 乘客 数
和 (iD 放 : 在 了 站 上 第 ? 辆 车 的 乘客 数 -
DO - :第 7 站 与 第 (1 - JU 站 间距 -从 >
方 (7 :上 行 方向 第 / 站 的 上 和 车 乘客 的 密度 函数 = 蛋
gi(7) :上 行 方向 第 / 站 的 下 车 乘客 的 密度 函数 2XG
户 (7) :下 行 方向 第 / 站 的 上 和 车 乘客 的 密度 函数 H
@()) :下 行 方向 第 / 站 的 下 车 乘客 的 密度 函数
G :一 天 内 公交 公司 的 总 收入 As
4 :公交 车 出 车 一 次 的 支出 ,为 定 值
有 :公交 公司 每 天 的 固定 支出 ,为 定 值 DC
qi:7 = 1.2.3 ,为 一 小 概率 事件 的 概率 K
NI) : 某 车 站 全 天 的 上 (下 ) 车 乘客 数
9 :第 /时 间 段 此 站 的 上 (下 ) 车 人 数
or :第 和
4 建 模 前 的 准备 MY
1D) “对 问题 的 初步 分 析 | 亏 _
我 们 考虑 三 组 相关 的 因 员 ; 代 共 汽车 汽车 站 与 乘客 对 模型 的 影响 。
i“ 与 公共 汽车 有 关 的 因素 :离开 公共 汽车 总 站 的 时 间 ,到 达 每 一 站 的 时 间 ,在 每 一 站 下
生得 站 在 年- 于 人 ai , 裁 客 总 数 ,行进 速度 等 。
i) 与 车 疾 有 关 的 因素 :线路 上 汽车 的 位 置 ,车 站 间距 ,乘客 到 来 的 函数 表示 ,等 车 的 乘客
数 AR 的 时 间 等 。
浊 ， 县 泥 索 有 关 的 因素 :到 达 某 一 车 站 的 时 间 , 乘 车 距离 (站 数 ) ,全 车 时 间 等 。
A
1 本 数据 ,可知 对 于 某 车 站 全 天 的 上 (下 ) 车 乘客 数 N (0 是 时 间 t 的 递增 函数 ，
NEON= wrr- D + 9 ,其 中 四 为 第 :时间 内 此 站 的 上 (下 ) 车 人 数 我们 可 以 由 此 来 拟 合 其 分
布 函数 。 由 样本 数据 知 每 一 车 站 每 天 有 两 次 波峰 , 故 根据 最 小 二 乘法 将 分 布 函数 拟 合 为 关于
7 的 五 次 多 项 式 。
5 “分 析 与 建 模
分 析 样本 数据 ,在 上 行 方向 22 :00 -23 :00 和 下 行 方向 5:00 -6:00 的 上 \ 下 车 人 数 较 其 它
时 段 偏 小 ,为 使 模型 更 好 地 体现 普遍 性 ,我 们 单独 讨论 上 面 的 两 个 时 段 。 易 知 各 站 只 需 一 辆 车
就 可 以 满足 需求 。
2 © 1994-2006 China Academic Journal Electronic Publishing House. Allrights reserved.  http:/www.cnki

<!-- source_page: 3 -->

ERi
T
建 模 专辑 关于 公交 车 调度 的 优化 问 是 oo
由 题 设 要 求 可 知 ,所 求 方案 须 兼顾 乘客 和 公交 公司 的 利益 ,但 实际 上 ,不 可 能 同时 使 双方
都 达到 最 优 值 。 因 此 我 们 将 公司 利益 作为 目标 函数 ,将 乘客 利益 作为 约束 条 件 。
公司 利益 Z = G- (N,+ Ny) X4 - B
其 中 G 为 总 收入 , 因 样本 数据 为 典型 工作 日 ,因而 可 以 看 作 定 值 , (N。 + Nw X4 + 为
支出 。
N。 二
7 x60 ， 3 _x60 ，4 x60  4 X60 o
No =1 Ts * Ty * Ts * Te 7 -从
乘客 的 利益 在 此 处 即 为 侯 车 时 间 ,由 于 乘客 侯 车 时 间 带 有 随机 性 TO
某 个 定 值 ,因而 可 用 概率 来 描述 乘客 的 利益 ,得 如 下 模型 : 2XG
I'maxZ = G- (N,+ Ny X4- B 】
s 7 以 等 待 时 间  > 10 分 钟 的 人 < ai
PDTNeD- Ni(ij) >120) < a
PIO(ij) + Ne(i,j) - NO <50 <
或 尺 等 待 时 间 ! > 5 分 钟 的 人 < ai 人
PLO(i)) + N(ij) - Ni(ij) > 20 5¢
PLO(i) + N(ij) - Ni(i.j) <50) < &
o]
6 模型 的 简化 与 求解 7
Ta .给 实际 求解 过 程 中 带 来 相当 大
的 困难 ,因而 对 其 简化 。 人
D 和 EN 的 和 FS
分 析 原 目 标 值 Z, 易 知 rn T 为 发 车 间距 时 间 , 它 因 不 同 的 时 间 段 而 不 同 。
下 面 我 们 就 以 每 小 时 汶 一 时 间 自 来 求解 , 且 假 设 乘客 上 下 车 瞬间 完成 , 即 不 考虑 上 下 车 时 间 。
天 区 要 表征 人 Ps 可 不过 10 分 名 商业 全 他 不 二 过 分钟。 我 们 引进 概率
多 站 < 用 b 人 时间 超过 10 分 钟 (或 5 分 钟 ) 的 人 数 在 总 侯 车 人 数 的 比重 。 对 于 满载 率
不 低 于 WO max Z , 则 可 以 忽略 不 考虑 ,可 得 如 下 模型 :
v,
汪
R 人 可 Du
DT <a
人 方太 帮
1 (i+1,))
0(ij) + 人 万 (J di - 人 &(j) di <120
(i+1,j)-5
人 Fili) dt
或 ”一 =«a
I 本
?  ©1994-2006 China Academic Journal Electronic Publishing Hous ights reserved.  http://www.cnki

<!-- source_page: 4 -->

回 叶 这
疙 -这
92 工程 数学 学 报 第 19 T
(i+1,)) (i+1.))
0(ij) + 由， fuli) d - 人 &(j) di <120
t>0, i=1,2
分 析 样本 数据 可 以 发 现 :
i” 对 于 上 行车 道 , 4 4, 4n ,4io As 的 上 车 人 数 > 下 车 人 数 ,对 于 其 余 站 点 则 相
反 :
刘 ” 对 于 下 行车 道 ,4o, 4 43, 44 的 上 车 人 数 > 下 车 人 数 ,而 其 余 站 点 则 相反 :
因而 对 于 约束 条 件 ,只 需 取 前 5 个 (或 4 个 ) ,对 于 模型 贡 , 我 们 可 以 根据 独 全 分 布 函数
所 G 将 约束 条 件 转化 为 工 的 函数 ,利用 Matlab 软件 容易 求解 ， 解 路 。 一 户
分 析 IJ 所得 结果 , 易 知 在 高 峰 时 间 段 中 ,结果 T 有 较 大 误差 全
起 的 。 为 了 减 小 误差 ,可 以 分 段 拟 合 分 布 函数 FL G 。 为 计算 方便 和 生 小 时 内 ,每
站 的 到 达 人 数 与 时 间 成 正比 ,每 站 的 下 车 人 数 亦 与 时 间 成 正比 , 即 F, 何 光 -局
1 厂 , 广 为 斜率 , 令 a = 5 % ,于 是 将 模型 简化 为 :
IILmax 7 = ¢ X
st 197-200 <0(E 19¢- 100 <0) As
kit - 120 <0 DA
kit + kat- pat- 120 =0 多
kit +kat- pat +kat- pyt- 120 三 0
kit +kat - pat +kat- pst + kat- pr- 120 三 0
kit +kat- pot +ksu-_pit +Ryt - pat + kst - pr- 120 <0
t>0 $, AN 9
(平时 及 晚 高 峰 取 191 - 200 全 0, 早 高 峰 取 197- 100 <0)
当 上 行 时 , 取 所 有 约束 条 件 RATIECHT 5 个 约束 条 件 。 模 型 TI 线 性 规划 ,利用 Matlab
求解 ,结果 如 下 : i%
\ne 发 车 间距 时 间 表
ooooloan 本 oa
3
， m, | 2o | >2| | ss
DINofrn alrowfmnel omon hon fes
站 本 本
1 二 ze | as | 2 [ so | as]| us]| na]
EECTEETIEETIEES
注 :第 2 5 排 为 上 行 ,3 .6 排 为 下 行 (单位 皆 为 分 钟
对 模型 ITT 坦 行 误差 分 析
在 上 文中 ,我 们 已 提 及 到 模型 [的 误差 , 究 其 原因 主要 是 由 于 拟 合 函 数 的 误差 引起 的 。 如
上 行 方向 Al3 站 的 7:00 - 8:00 ,发 车 间距 T= 5.26 分 ,显然 此 时 的 工 无 法 使 3626 名 乘客 正
常 运行 ,而 此 时 由 拟 合 函 数 算出 来 的 乘客 总 数 为 2023 。 误差 A=3626 - 2023 = 1603( 人 ) 。
为 使 误差 减 小 ,因而 可 以 对 函数 进行 分 段 拟 合 。 如 模型 IT 了 ,以 每 小 时 为 一 段 。 此 时 求解
的 结果 ,能 很 好 的 使 样本 数据 的 乘客 正常 运行 。 当 然 此 时 的 解 亦 有 误差 s ,因而 了 可 有 一 波动
%x
)4-2006 China Acad ectronic Publishing A erved. ht cnki

<!-- source_page: 5 -->

ERi
SANE
建 模 专 辑 关于 公交 车 调度 的 优化 问题
范围 。
在 此 解 的 情况 下 ,容易 知 道 客车 满载 率 <120 %( 约 束 条 件 ) 。 乘客 等 待 时 间 过 长 的 概率 <
5 %。 空 载 情 形 ,大 部 分 只 有 在 最 后 一 站 方 出 现 空 载 情形 ( 满 裁 率 <50 9 。
2) “对 无 滞留 乘客 条 件 下 的 最 小 配 车 数 初步 求解
我 们 对 数据 作 进一步 的 处 理 ,估算 出 每 一 段 上 \ 下 行 所 需 的 最 小 配 车 数 ,从 而 得 出 一 天 内
所 需 配备 的 最 小 车 辆 数 。 为 最 小 配 车 数 的 求解 找到 一 个 参照 值 。
我 们 首先 考虑 以 一 小 时 为 时 间 间距 来 考查 一 天 的 最 小 配 车 数 ( 即 设 公交 车 在 各 车 站 所 个
的 时 间 为 一 定 值 ) 。 分 析 数 据 可 知 满足 各 站 均 无 滞留 乘客 ,各 发 车 时 刻 均 有 车 可 发 的 最 小 配 车
数 应 为 65 辆 车 。 这 只 是 一 个 初步 解 ,为 得 到 进一步 的 精确 解 .我 们 考虑 以 性
距 ,通过 拟 侣 的 分 布 函数 得 到 各 车 满载 时 各 时 段 的 所 需 最 小 配 车 数 。 满 足 各 站 艺 ; 曙 针 客 ,各
发 车 时 刻 均 有 车 可 发 的 最 小 配 车 数 为 43 辆 。 2XG 、
3) “公交 公司 调度 方案 模型 的 建立 与 求解 中
汶 ” 我 们 制订 调度 方案 ,应 使 公交 公司 和 乘客 双方 的 利益 远 移 移 三 方面 公交 公司 希
望 配置 尽 可 能 少 的 汽车 以 降低 固定 成 本 ,又 要 在 保证 接送 全 前科 效 揭 前 提 下 尽 局 能 减 小 出 车
次 数 ,以 降低 可 变 成 本 :; 另 一 方面 ,应 实现 乘客 满意 , 印 0
短 等 车 时 间 。 X
过。 制订 调度 方案 时 我 们 发 现 有 下 难点 : xK
扣 ) 一 方 车 站 到 了 发 车 时 间 但 没有 车 可 发 , 另 一 方面 才 有 围 积 。 此 问题 有 两 种 解法 :一 是
购置 新 车 ,二 是 调节 班次 。 前 者 使 成 本 变 高 ,后 者 引起 连锁 反应 ,使 整个 计算 量变 大 且 有 可 能
、 O
求 不 出 最 优 解 。 Ap“e
B) Ran ,全 局 最 优化 。
这 是 一 个 最 优 问题 。 ANY 》
C) 总 配置 数 一 定 ,调理 总 御 班 次 使 总 车 次 数 增加 越 少 ,总 车 班次 数 越 小 , 则 求 得 的 解 越
优 。 这 又 是 一 个 极 值 优化 问 SA
为 解决 以 上 难点 an .用 Maple 优化 软件 求解 。 设 某 j 时 间 自
RAHH x, 和 c
| 未 行 始 视 癌 发 车 aa
1 2 全。 于 为 总 配置 数 ,= 为 总 班次
号
更 2
| 汐 - + Ci = 7
NY Xi = C - Xi =0
Xoo = Co- Xo =0
和
Xoj = Co 十 mv - ww =0
Daov =- xi,
1 60 - 120 调度 方案 模型
23 1994-2006 China Academic Journal Electro shing House. Allrights reserved. http://www-.cnki

<!-- source_page: 6 -->

ERi
有
94 工程 数学 学 报 第 19 全

若 考虑 到 各 站 点 乘客 上 下 车 时 间 相 等 ,总 行程 总 需 耗 时 60 分 ,每 辆 车 都 载 120 人 。 在 初
步 解 的 模型 中 ,配置 最 小 车 辆 为 60 ,用 Maple 软件 包 开始 搜索 优化 选择 ,/ -= 2.3 …18。

搜索 出 整体 最 优 解 为 : Cy- 62, Ci -= 4, mm - 66, Z - 476 ,调度 方案 时 刻 表 略 。

2) 44—120 调度 方案 模型

考虑 乘客 上 下 车 瞬间 完成 ,公交 车 驶 完全 程 需 4 分 。 每 辆 车 均 载 120 人 ,此 模型 中 步 长
为 44 分 钟 ,所 考虑 时 段 的 乘客 数 均 由 拟 合 函 数 给 出 ,初始 值 为 43 辆 ,由 Maple 软件 包 优化 先
择 ,得 到 :

m =48,Cy =42,CI =6,z = 590。 调 度 方 案 略 。 次
7 模型 的 推广 与 改进 -VS

在 设计 公交 车 调度 方案 时 ,并 未 充分 考虑 乘客 利益 ,在 进行 改进 果 %EE 以 试 着 相 其 它 办 法
找到 一 些 更 好 的 规则 来 进行 对 比 与 评价 ,从 而 得 到 更 加 优化 的 方案 箱 芭 游 利 答 达 到 充分 均
衡 ,这 是 模型 改进 的 方向 。 另 外 ,模型 求 得 的 数据 相对 精确 度 边 高 & 在 现 穴 生 活 中 不 太 实 用 。
问题 的 关键 是 所 给 的 数据 太 少 ,所 得 到 的 调度 方案 稳定 性 很 美 v 二 伍 并 较 高 ,可 以 试 着 找 其 它
方法 解决 ,从 而 求解 。 SN ， N

我 们 建立 了 一 个 调度 方案 的 一 般 模型 Jeth TEMBE 55 F J7v: ,故此 模型 可 用
于 现实 生活 中 其 它 运输 业 的 调配 美 似 交通 运输 之 关 的 调 中 问题 ,从 而 达到 资源 的 优化 配置 。

8 ”模型 的 自我 评价 .

我 们 通过 一 些 合理 的 假设 SALAAAISAE 3L T —OT . SEXTHUREAT T RIAL,
采用 由 简单 到 复杂 AN 和 Maple 优化 软件 包 进 行 搜索 优化 求解 ,从 而 得
到 一 个 整体 最 优 解 .在 求解 (2) 小 题 闪 名 请 一 个 方法 , 即 每 次 都 从 每 段 时 间 的 起 点 均 有 和 车 改
出 ,到 最 后 一 班车 持续 等 时 俱 发 表 ,最 后 剩余 小 段 时 间 委 去 不 子 考虑 。

列 昌 了 不 同时 段 的 公交 后 抽 刻 表 。 同 时 引入 概率 来 刻 划 顾客 利益 ,从 而 可 以 使 抽象
概念 定性 分 析 定 量化 -也 是 本 模型 的 一 大 优点 。

全 信人 和 人 ,具有 与 型 性 ,得 出 的 结果 在 长 时 间 内 可 行 性
较 差 ,其 次 设 ij 调度 方案 竺 着 重 考虑 公司 利益 与 大 部 分 顾客 利益 ,使 双方 利益 趋 于 均衡 ,并 未
Po 。

pe
2 本
让 卫生 学 模型 [M] 北京 :高 等 教育 出 版 社
ROOT 长 沙 :湖南 教育 出 版 社
[3] EVEAR - Matlab5. 0 与 科学 计算 [M]. 北京 :清华 大 学 出 版 社
[4] 费 培 之 , 程 中 王 . 数学 模型 实用 教程 [M]. 成 都 :四 川 大 学 出 版 社

(下 转 100 页 )
3 ol1994 China Academic Journal Electronic Publishing House. Allrights reser http:/www.cnki

<!-- source_page: 7 -->

回 叶 这
EU
|
EEEE
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
(上 接 曙 页 ) 2XG
Optimization of Dispatching Buse S )
FU Changjian Yang Carxia Qin Mi SS
Advisr: “CHEN Jin'mi
全
(SiChuan University , Chenlgdu610064)
AS
Abstract :is to find out the best way to dispatch buses. We set a optimized model whose target function is the profit of bus comr
pany. At the same time , it guarantee the proportion that the passengers waiting for their buses more than 10 min (or 5 min)in the
total is less than qd given before. First , every station s nonparameter distribution function about the number of passengers is fitted by
method of least squares. We use a simple method to_estimate tha at least 43 buses are needed ,and then , we use Maple to get the
optimal solution refer to it. It shows the best pa d patching buses in different conditions of the number of passengers. It can
help bus companny to get the top profit , meamvhile jj assengers may not wait for their busforalong time. In the end , we evalur
CA
ate and popularize the model , and point out the effective ) to improve it.
Key words : dispatching buses ; optimized“fodel ; mathod of least squares
] NA
一 -一 j
% ]
所
2 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved.  http:/www.cnk

