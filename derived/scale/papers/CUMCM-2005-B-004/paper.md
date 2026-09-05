# Extracted Paper

<!-- source_page: 1 -->

第 22 卷 第 7 期 工 程 数 学 学 报 Vol. 22 No. 7
2005 年 12 月 CHINESE JOURNAL OF ENGINEERING MATHEMATICS Dec. 2005
文章 编号 :1005-3085(2005)07-0101-07
. B :
DVD 在 线 租 赁 问题
范 浩 ， 薛 世 坤 ， 战 东 元
指导 教师 ; 武汉 大 学 指导 组
(武汉 大 学 ， 武 汉 430072)
编者 按 ， 本 文思 中 清晰， 解法 简练 有 效 。 利 用 一 项 分 布 对 DVD 购买 最 进行 了 合理 锯 测 ， 对 DVD 购买 与 分 发 建立 了
使 顾客 达到 最 大 满意 度 又 使 服务 商 取得 最 大 利 涧 的 双 目 标 优化 问题 ， 以 使 顾客 达到 足够 满意 度 的 购买 量 为 随
机 变量 ， 建 立 随机 搜索 模型 ， 利 用 计算 机 搜索 得 到 好 的 解答 。
# B 本 文 就 DVD 在 线 租赁 问题 建立 了 数学 模型 。 我 们 假设 会 员 在 每 月 初审 报 订单 ， 只 申报 一 次 的 会 员 在 月 末 归
还 DVD， 申 报 两 次 的 会 员 在 月 中 归还 DVD 并 进行 二 次 申报 ， 月 未 笛 次 归还 。 对 问题 一 本 文 秆 立 了 于 于 二
项 分 的 随机 模拟 模型， 发 现 了 DVD 的 最 小 购买 量 与 会 员 需 求 量 之 间 的 正比 关系 。 问 题 三 先 将 订单 中 会 员
对 光盘 的 偏好 程度 转化 为 满意 度 矩 阵 ， 再 建立 DVD 分 配 的 0 一 1 规划 模型 ， 用 -Linge 求解 得 到 最 大 满意 度
以 及 对 应 的 最 优 解 。 此 外 ， 文 中 还 给 册 了 一 种 高 效率 的 食 林 算法 ， 也 能 求 得 满意 度 较 天 的 分 配方 案 。 问 题 三
先 根据 给 出 的 1000 位 会 员 对 每 种 DVD 的 满意 度 求 出 每 种 DVD 的 需求 人 数 ， 利 用 第 一 问 最 小 购买 重 与 会 员
需求 量 成 正比 关系 的 结论 ， 运 用 计算 机 模拟 的 方法 ， 先 确定 一 较 小 的 购买 量 ， 再 用 贷 标 算法 作为 策略 进行 分
配 ， 计 算 满意 的 会 员 所 占 的 百分比 。 按 照 需求 比 逐 渐 增 加 购买 重 直至 满意 的 会 员 达到 95 色 为 止 。 此 时 的 购买
量 即 为 最 小 购买 量 。 问 题 四 中 我 们 提出 网 站 如 何 进行 信息 预测 并 决策 DVD 的 购买 量 ， 通 过 减少 订单 周期 和
对 会 员 还 妇 时 间 的 随机 化 处 理 ， 模 型 更 加 切 从 实际。
关键 词 : 二 项 分 布 ，0 一 1 规划 ， 讽 杞 算法 ， 随 机 模拟
分 类 号 : AMS(2000) 90C10 中 图 分 类 号 : 0221.4 文献 标识 码 : A
1 问题 分 析 和 模型 假设
1.1 “需求 预测
假设 抽样 调查 的 1000 个 样本 精确 地 反映 了 10 万 个 会 员 的 喜好 。 根 据 极 大 似 然 估计 ， 愿 意
看 5 种 DVD 的 人 数 分 别 为 20000，10000，5000，2500，1000;
1.2 会员 结构
网 站 60 多 的 会 员 每 月 租赁 DVD 两 次 ， 我 们 称 其 为 A 类 会 员 ; 另外 的 40 允 只 租 一 次 ， 称 其
为 B 类 会 员 。A、B 类 会 员 的 人 数 只 具有 统计 意义 ;
1.3 ”网 站 运营 规则
假设 网 站 规定 会 员 只 能 在 月 初 〈 每 月 1 号 》 和 月 中 〈 每 月 16 号 ) 提交 订单 ， 随 后 网 站 立即 根
据 订 单 发 放 DVD (一 次 3 张 ) ，A 类 会 员 在 月 中 归还 DVD 并 进行 二 次 申报 ， 在 月 末 归 还 第 二
次 发 放 的 DVD，B 类 会 员 只 在 月 末 归 还 DVD。
2 符号 说 明
oj 编号 为 ;的 会 员 对 编号 为 了 的 DVD 的 满意 度 ，

<!-- source_page: 2 -->

相 - 险 普 资讯 http:/ vipe9 cqvip.com|
1 102 工 程 数 学 学 报 第 22 着

1 Tij 0 一 1 变量 ; ， 了

| 。 _ | o， 表示 编号 为 ;的 会 员 未 得 到 编号 为 ;的 DVD ]

1 “” 15。 表示 编号 为 了 的 会 员 得 到 编号 为 1 的 DVD 2

| 已 ”编号 为 小 的 DVD 的 库存 数量 ， 单 位 ， 张

1 m 编号 为 了 的 DVD 的 购买 数量 ， 单 位 ; 张 。 =

i (1<i<1000,1< j < 100) 四

了 3 ”模型 的 建立 和 求解 a

E 3.1 ”问题 一 〈 购 买 新 的 DVD) -

| 我 们 认为 会 员 喜 欢 何 种 DVD 与 他 属于 A、B 中 哪 一 类 是 不 相关 的 ， 腺 意 看 某 种 DVD 的 |

人 中 A、B 两 类 会 员 人 数 之 比 亦 为 6: 4。 :

E 为 满足 一 定时 间 内 给 定 比例 的 会 员 看 到 他 喜欢 的 新 片 ， 网 站 要 综合 考虑 DVD 分 配给 两 类 ，
会 员 的 情况 。 如 果 新 片 分 配给 A 类 会 员 ， 他 们 会 在 月 中 归还 DVD， 这 些 DVD 又 可 分 配给 其 四

1 他 的 尚未 看 到 该 片 的 A 类 会 员 以 满足 他 们 的 需要 ， 因 此 这 些 DVD 在 二 个 月 中 被 利用 了 两 次 。 1

| 如 果 新 片 分 配给 B 类 会 员 ， 他 们 将 在 月 末 归 还 ， 这 些 DVD 在 一 个 月 中 只 被 利用 了 一 次 。 |
311 ”一 个 月 内 保证 至 少 50% 会 员 看 到 喜欢 的 DVD《 仅 以 DVD1 为 例 进行 分 析 ) =

1 设 网 站 购买 了 m & DVD1， 得 到 DVDI 的 .A 类 会 员 的 人 数 〈 不 妨 记 为 各 , ) 服从 一 项 分 aa

1 布 ，A，w B(na,0.6)，A 类 会 员 得 到 的 光 稻 可 以 利用 两 次 ， 得 到 DVD1 的 B 类 会 员 的 人 数 可 本
为 m - 各,， 故 一 个 月 中 共有 ni 二 si 会 员 看 到 这 张 光盘 。 若 在 99%% 的 置信 度 下 保证 一 个 月 内 |

1 至 少 50% 会 员 满意 二 则 认为 达到 预定 的 目的 。 模 型 如 下 3

， minn, : :

[ si Po = P(fna + bo > 10000}) 2 0.99 =

1 es : B(ny,0.6).

| 显然 P(m) 是 mi 的 不 减 函数 ， 可 采取 计算 机 模拟 方法 求解, 为 此 建立 如 下 算法 ;

: Stepl: 给 定 m 的 一 个 较 小 的 初 值 ， 如 取 ni = 5000; |

| (2~.4 步 检测 约束 条 件 是 否 满足 |
Step2; 令 。 = 0， 作 为 计数 变量 ; |
Step3; 让 计算 机 产生 一 个 服从 B(ny,0.6) 的 随机 数 ， 判 断 是 否 满足 m + ba，> 10000, 0
: 若是 则 令 。 = s 上 + 1 否则 。 保持 不 变 ，

| Step4; ”重复 Step3 共 10000 次 。 判 类 是 否 有 。 > 9900， 若 是 ， 认 为 约 东 条件 可 以 满足 ，- |

1 ， 进入 Steps; BZ4 m =ny+1, 回 到 Step2; 7
Step5:。 记 下 此 时 的 m 值 ， 上

i 以 上 算法 可 运用 Matlab 编程 实现 目 ， 结 果 由 表 1 给 出 。 到
结果 的 分 析 : 】

| 从 表 1 中 不 难 发 现 ，DVD 的 最 小 购买 量 〈 近 似 ) 与 其 需求 最 《愿意 观看 的 人 数 ) 呈 正比 关
系 ; ， -

4 小 _ 需求 最 X 保 证 满足 的 百分比 ，
人 .

<!-- source_page: 3 -->

第 7 期 范 浩 等 ，DVD 在 线 租赁 问题 103
表 1 一 个 月 内 保证 至 少 50% 会 员 看 到 喜欢 的 DVD
[ovoi [ ovoa | bvet | ovoe | ovs
Rai ck| mon | ooo | sow | aow0 | ioo
天主 | oor | ao | | wo | om

这 一 关系 可 以 用 下 检验 法 四 进一步 验证 。

3.1.2 ”三 个 月 内 保证 至 少 95 多 会 员 看 到 喜欢 的 DVD ( 仅 以 DVD1 为 例 )

与 3.1.1 类 似 ， 只 需 注 意 月 中 只 有 A 类 会 员 返 还 DVD， 此 时 也 只 能 将 返还 的 DVD 分 配给
没有 看 过 该 片 的 A 类 会 员 ， 月 末 所 有 会 员 都 返还 DVD， 下 月 初 分 配给 所 有 需要 该 片 〈( 没 有 看
过 而 且 喜 欢 该 片 ) 的 会 员 。 在 月 初 的 分 配 中 ， 二 项 分 布 由 目前 需要 该 片 的 A、B 两 类 会 员 人 数
决定 。 仍 采用 Matlab 编程 模拟 求解 ， 结 果 由 表 2 给 出 。

表 2: 三 个 月 内 保证 至 少 95% 会 员 看 到 喜欢 的 DVD ，
[5vbi [ovoa | ovis | ovbe [ ovos
Raaei | awo | oom | swo | w0 | ioo
和 | 7 |zm | nw | w | m

3.2 ”问题 二 〈 在 线 订 单 的 处 理 )

3.2.1 -满意 度 的 确定

为 了 体现 会 员 对 光 表 的 满意 程度 ， 应 建立 合适 的 满意 度 函 数 。 近 似 的 认为 会 员 对 自己 喜
欢 DVD 的 偏好 级 差 是 相同 的 ， 采 用 线性 的 满意 度 函 数 。 而 若 光盘 并 未 出 现在 会 员 的 订单 中 ，
此 时 满意 度 值 取 0。 认 为 0 与 会 员 申 报 的 最 后 一 个 DVD 的 满意 度 差 值 显著 地 大 于 他 所 喜欢 的 相
邻 两 个 DVD 之 间 的 满意 度 差 值 。 建 立 满意 度 函数 如 下 ;

ay = fi —@ij, 6 #0
0, G;=0

mi 为 题 表 中 编号 为 宇 的 会 员 对 编号 为 了 的 DVD 的 偏爱 程度 ， 偏 爱 程度 越 高 ， 满 意 度 越
大 。

3.2.2 ”订单 处 理 模型

我 们 试图 据 此 寻求 一 种 最 佳 分 配方 案 ， 使 得 所 有 会 员 对 获得 光 查 的 满意 度 之 和 最 大 。
按照 “问题 分 析 ” 中 网 站 的 运营 规则 ， 每 名 会 员 每 次 应 获得 0 或 3 张 DVD。 当 某 名 会 员 未 获
得 DVD 时 ， 一 定 可 以 通过 向 他 任意 分 发 3 张 DVD 而 使 得 目标 函数 值 不 减 。 因 此 模型 的 最 优 解
一 定 在 每 名 会 员 都 获得 3 张 DVD 时 取 到 。 另 外 分 配给 会 员 的 某 种 DVD 的 总 数 不 应 超过 网 站 的

<!-- source_page: 4 -->

3 医 Eve
104 工 程 数 学 学 报 第 22 着
库存 量 。 根 据 上 述 目标 及 约束 条 件 建立 0 一 1 规划 模型 如 下 : :

. i 1000 100 i 本

E maxw 一 > > aiz :
A i=1 j=1 ]

ia 100 . 本

开 S @y=3 如

3 i=1 -

E st. 时 os <

E i=t Po

: : zi 一 0 或 二 下

1 3.2.3 ”模型 的 求解 : ，

| 切 。 求 精确 解 ， 用 Lingo8.0 求解 0 一 1 规划 得 到 最 优 的 分 配方 案 和 最 大 满意 度 值 。 下 才 具
体 列 出 前 30 位 会 员 〔C1vC30) 所 获得 的 DVD 《用 序号 表示 ， 下 同 ) 。 本
| 表 3: 前 30 位 会 员 获得 的 DVD (lingo 结果 ) ，

| 全 | DVDlvs | ce | 3 5[ mfowlwl[sor] co 全 [ma =

| ci|s|afem] 0 | 本 | 可 | 0 cm | 生 | 下 | 村 | cas] ofos]oe |
@2|ofujefoo]alsw|s|os|ajeolnfoln|esles a

| G Jaalsofef culsofes| 6 ciofessess] cor|so]es]ors =x

1 ca|rls]ufoe|z|ulafon/elale]os|s]uls

Cs | 也 | 66| 人 | cl 2 | 6 | co | 全 | 和 | 呈 | ca | 26| 30| 本 ，

| C6 | 查 | 8| .66 cl4 | 283| 到 | 昌 | co2 | a8| 西 | 呈 | cao| 对 | 轻 | 台 ，

or | 和] 6 | 二 cs 131 52| 是 ca 2 ss | [ | ，

1 满意 度 ，39681 量

。 2) 贪 菊 算 法 〈 求 近似 解 ) ， 按 照 如 下 步 又， 可 以 得 到 一 种 近似 最 优 的 分 配方 案 ，

Stepl: 对 于 库存 的 100 种 光盘 ， 首 先 满足 所 有 对 它 俯 爱 顺序 为 1 的 会 员 的 各 要 ， 即 将 每 种 |

| 光盘 分 配给 所 有 对 其 偏爱 顺序 为 1 的 会 员 ， 如 果 该 光盘 的 数目 偏 少 无 法 完成 此 次 分 配 ， 则 先 分 ， -

| 配给 其 中 编号 较 小 的 那些 会 员 ， 上

， Step2: 对 于 剩余 光盘 ， 再 优先 满足 对 它 偏爱 顺序 为 2 的 会 员 需要 ， 同 样 地 ， 如 果 该 光盘 的 =

i 数目 偏 少 无 法 完成 此 次 分 配 ， 则 先 分 配给 其 中 编号 较 小 的 那些 会 员 ， |

Step3:  vos

依 此 类 推 分 配 下 去 ， 在 Step3 以 后 分 配 时 ， 已 经 拥有 3 张 光盘 的 会 员 不 参加 分 配 ;
] Stepll: 如果 还 有 剩 下 的 光盘 ， 随 机 分 配给 尚未 分 满 的 会 员 ， 分 配 结束 。 E
1 这 种 仿效 算法 计算 量 较 小 ， 速 度 很 快 。 由 于 上 述 步骤 尽量 保证 了 偏爱 程度 较 高 的 匹配 ， 可
以 保证 结果 的 近似 最 优 。 据 此 编程 计算 ， 前 30 名 会 员 的 分 配 结果 见 表 4。 -

E 满意 度 ，37519 3

| 3) 结果 比 较 ， 贪 于 算法 的 结果 比 精确 解 差 了 5.45%。 通 过 改变 光盘 的 初始 库存 多 次 进行 对 ，

| 比 ， 认 为 贫 末 算法 可 以 较 好 的 保证 近似 最 优 ， 而且 时 效 性 远 好 于 天 规模 的 0 一 1 规划 ， 因 此 可

| 以 将 这 种 委 法 作为 一 种 有 效 的 分 配 策略 。

3.3 ”问题 三 (DVD 的 购买 与 分 配 ) 8

<!-- source_page: 5 -->

第 7 期 范 浩 等 ，DVD 在 线 租赁 问题 105

表 4 前 30 位 会 员 款 得 的 DVD (食材 算 法 结果 )
#R] DVDla [cs|ws|n] w[owe|or]6sfculafm]ar
ci[s]os[m| cols|m[w|crlafafe|cs|olea
c2[6 aaf2] cwo|ss[e] ss[cs|a1|eo]s] ca|2]6s]0
cs [s0[s0] 4 | cn 下 | es| colse|es|er] cor| :] ss| 和
ca|7|uslafo|2]7]afcnln|esfcnlsluls
cs | 是 | 86| | cis[on|7s| 上 | cor[as|sa| 2 | co| 30| 全 | 本
ce.[19]ss|16] c4| 各]| 到 | 各 | omlss|ss|or| cwar|e2] 1
co | 8| 28 os s cs aalol [ [ |

3.3.1 ”模型 的 准备

1) 由 第 一 问 结果 可 知 ， 新 光盘 最 小 购买 量 与 需求 量 成 正比 关系 。 为 满足 客户 需要 ， 使 得
一 个 月 内 95% 的 会 员 得 到 他 们 想 看 的 光盘 ， 网 站 经 营 人 员 应 考虑 按 每 种 光盘 需求 量 的 一 定 比例
购买 光盘 。 设 最 小 购买 量 与 需求 量 的 比例 系数 为 放 9 > 0。

2) 只 要 会 员 在 申报 中 选择 了 某 光 盘 ， 就 认为 该 光盘 是 该 会 员 所 需要 的 统计 题目 订
单 中 每 列 非 零 元 素 的 个 数 ， 得 到 预订 该 DVD 的 会 员 数目 ”认为 它 较 客观 地 反 歇 了 会 员 对
该 DVD 的 需求 量 。 记 结果 为 D = {d，. ,dioo}，d 表示 第 了 种 光盘 的 需求 量 。 光 盘 的 最 小
购买 量 n; 应 与 由 BIEH: 2 = 9 为 定 值

3) 采取 3.2.3 中 贫 禁 算法 作为 分 配 策略 。

4) 假设 网 站 在 月 初 、 月 中 两 次 集中 处 理 订单 。 月 初时 网 站 按照 订单 对 所 有 会 员 分 配 一 次
光盘 。 月 中 时 ， 认 为 A 类 会 员 对 已 经 看 过 的 DVD 满意 度 变 为 0， 得 到 新 的 虚拟 满意 度 矩阵 。
按 此 虚拟 渍 意 度 第 阵 ， 将 A 交会 员 归还 的 DVD 进行 重新 分 配 。

5) 某 名 会 员 是 否 满意 取决 于 在 该 月 中 所 有 获得 的 光盘 都 是 他 们 希望 看 到 的 。 具 体 的 说 ，
当 且 仅 当 人 类 会 员 获 得 6 张 满意 的 盘 ，B 类 会 员 获 得 3 张 满意 的 光盘 ， 才 认为 该 会 员 满意 。

3.3.2 ”模型 的 建立

沿用 3.1.1 的 思想 ， 具 体 每 名 会 员 属于 哪 一 类 事先 无 法 预知 ， 因 此 应 建立 具有 统计 意义 的 模
型 。 如 果 购 买 和 分 配方 案 使 得 在 99% 的 置信 度 下 保证 一 个 月 内 至 少 95 色 会 员 满意 ， 则 认为 满足
约束 条 件 。 设 T(7) 表示 以 比例 系数 n 购买 DVD， 按 照 贪 禁 策 略 进行 两 次 分 配 后 使 95% 以 上 的
会 员 满意 的 事件 ， 建 立 模型 如 下

ming st g() = P(T(1)) > 0.99.

显然 ，g(m) 是 单 增 函数 ， 通 过 购买 更 多 的 DVD 可 以 使 满足 85%% 会 员 的 概率 变 大 。 采 用 计
算 机 搜索 的 方法 求解 ， 算 法 如 下

Stepl: 给 定 n 的 一 个 较 小 的 初 值 ， 如 令 9 = 0.2;

(2~4 步 检测 约束 条 件 是 否 满足 )

Step2: 。 令 s = 0， 作 为 计数 变量 ;

Step3: ”让 计算 机 随机 产生 600 个 人 作为 这 个 月 内 潜在 的 A 类 会 员 ，

Step4: 按照 3.2.3 中 贪 末 算 法 计算 月 初 的 分 配方 案 。 统 计 B 类 会 员 满意 的 人 数 ;

Step5: 月 中 收回 A 类 会 员 的 DVD， 并 继续 按照 贪 楚 方 案 再 次 分 配 DVD 。 统 计 2 次 中 均
满意 的 A 类 会 员 的 人 数 ;

<!-- source_page: 6 -->

、 ， ETEIITE 开
， 106 工 程 数 学 学 报 第 22 着 |
| Step6: 根据 Step4、Step5 中 的 统计 结果 计算 总 的 满意 人 数 ， 并 判断 满意 人 数 否 超过 会
1 员 总 数 的 95 铬 〈 即 1000 x 95% = 950 A) 。 若 是 则 计 s = s + 1， 否 则 s 不 变 ;
| Step7: 重复 Step3~.Step6 共 1000 次 。 判 断 是 否 有 s > 990。 若 是 ， 认 为 约束 条 件 可 以 满
j 足 ， 进 入 Step8; KZ4 n=n+001, FIF Step2:
， Step8: 。 记 下 最 终 的 值 。
| 按 上 述 算法 运用 Matlab 语言 编程 ， 解 得 四 = 0.32， 最 小 购买 量 见 表 5 ( 表 略 ) 。 ;
; 购买 DVD 的 总 数量 。2983 张 ，DVD 分 配方 案 ， 同 3.2.3 食 焚 算 法 。
| 3.4 ”问题 四 模型 的 扩展 ) |
| 绪 合 实际 问题 ， 模 型 的 扩展 可 从 以 下 儿 个 方面 展开 ;
， 1) 网 站 对 顾客 的 消费 习惯 作 市 场 调查 ， 预 测 在 未 来 -- 段 时 间 内 会 员 归还 的 DVD 数目 ;
， 2) 建立 一 套 订单 的 排队 等 候 系统 以 及 集中 处 理 系统 ， 缩 短 订单 处 理 的 周期 ;
| 3) 网 站 在 经 营 中 既 要 保证 当期 的 收益 以 维持 生存 ， 又 要 兼顾 潜在 收益 以 求 得 长 远 发 展 。
; 基于 以 上 3 个 假设 ， 我 们 就 网 站 决定 新 增 DVD 的 购买 量 的 问题 建立 了 动态 随机 模型 。 ，
补充 符号 说 明
， i 考察 的 阶段 数 ， 这 里 取 一 周 ， 即 每 周 新 购 买 一 批 DVD; |
， 加 第 ;期 购买 DVD 的 数目 ， 模 型 中 的 决策 变量 |
1 % 第 ;期 库存 DVD 的 数 日， 模型 中 的 状态 变量 ， |
| " 第 ;期 会 员 归还 的 DVD %H, TTHREELSGRERIGIRR, WiESHEL
1 tu 第 ; 期 派发 的 DVD 数目 ， 与 会 员 对 DVD 的 带 求 和 库存 量 有 关 ， |
uitaa z) 第 计 期 的 效益 ， 效 益 应 综合 考虑 函数 当前 经 济 效益 这 里 仅 用 购买 DVD 的 成 本 |
， 代替 ) 和 潜在 经 济 效益 〈 满 意 度 造 成 的
， p 将 未 来 的 效益 折算 到 当期 的 贴现 因子 ， 通 常 取 为 利息 率 。 ，
根据 经 济 学 的 原理 ， 商 家 总 是 最 大 化 期 望 效益 思 ， 所 以 对 效用 取 期 望 作为 目标 函数 。 另 外 |
i 为 商家 会 受到 资金 等 方面 的 客观 约束 。 据 此 ， 建 立 带 有 贴现 率 的 模型 如 下 ， ，
II ARtYWSNTY a t
max U =- 相 > etoaa] |
; 从 ,zn) =0
: 8.t. H
j mi>z0  (0<i<n). |
库存 数量 = 满足 随机 过 程 轩 ; ;
w=2z (z > (为 给 定 的 自然 数 )
3 一 站 十 于 十 路 一 人 (> 0). |
上 式 中 0 表示 系统 初始 状态 ， 递 推 关 系 atl = 2+20+ s 一 邮 表示 : 下 一 期 库存 = 当期
; 库存 + 当期 购买 量 + 会 员 归还 DVD 数量 -当期 派发 DVD 数量 。 ，
模型 的 求解 建议 ， 对 于 两 期 情形 可 采用 拉 格 朗 日 法 ， 对 于 多 期 情形 应 采用 变 分 法 及 动态 规 |
， 划 方 法 求解。 |
: 由 于 该 模型 考虑 了 现实 中 的 诸多 因素 ， 因 此 可 以 更 精确 的 估计 当期 购买 量 对 来 来 的 影响 ， |
| 从 而 更 有 利于 网 站 对 DVD 的 购买 量 进 行 决策 。 当 然 ， 由 于 随机 因素 的 加 入 ， 模 型 的 求解 变 得 |
; 更 加 复杂 ， 而 且 对 于 革 些 情形 不 一 定 能 求 得 解析 解 ， 可 以 考虑 求 近似 的 数值 解 。 ! |
i

<!-- source_page: 7 -->

.
第 ?期 范 浩 等 ，DVD 在 线 租 赁 问题 107
参考 文献 :

[1] 张 志 涌 . 精通 Matlab 6.5 版 [M]. 北京 :北京 航空 航天 大 学 出 版 社 ，2003

[2] 刘 承 平 . 数学 建 模 方法 [M], 北京 :高 等 教育 出 版 社 ，2002

(3] David Romer. Advanced Macroeconomics (2nd edition)[M]. Columbus, Ohio: McGraw-Hill, 2000

[4] Sheldon M. Ross. Stochastic Processes (2nd Edition)[M]. New York: John Wily & Sons, 1995

[5] 李 贤 平 . 概率 论 基 础 (第 二 版 )IM]. 北京 ， 高 等 教育 出 版 柱 ，1997

Online DVD Rental Business
FAN Hao, XUE Shi-kun, ZHAN Dong-yuan
Advisor: Wuhan University Instructor Group
( Wuhan University, Wuhan 430072 )

Abstract: In this article, we set Up a series of mathematical models for DVD online rental service. We assume
that customers should submit their orders at the beginning of each month; customers who rent DVDs only once
a month should give them back at the end of the month, while those who rent DVDs twice a month should
return them at mid-month and place new orders for the next half month. For Problem 1, by putting forward
and applying a random simulation model, we discover that the minimum purchasing quantities are in direct
ratio to the required quantities among all kinds of DVDs. For Problem 2, we convert the priority of customers’
preference for DVDs into satisfaction matrix, develop a 0-1 programming model for the assignment of DVDs, and
Work out the exact maximum happiness quotient and corresponding scheme of assignment by Lingo. Moreover,
we design a greedy algorithm to deal with the problem efficiently and satisfactorily. As to Problem 3, we take
advantage of the conclusions of the former two problems. We decide an appropriately small number of DVDs
at first. Then, by using the greedy algorithm to assign DVDs, and by keeping the purchasing quantities in
proportion to the required quantities among all kinds of DVDs, we increase the purchasing quantities step by
step until 95% customers can be satisfied within one month. Accordingly, we obtain the minimum purchasing
quantities. Finally, based on economic theory, we put forward a more realistic method to forecast the demand
of customers dynamically and determine the corresponding purchasing quantities.
Keywords: binomial distribution; 0-1 integer programming; greedy algorithm; random simulation

