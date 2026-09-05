# Extracted Paper

<!-- source_page: 1 -->

回 虽 过
同和
. " o pi
第 30 卷 第 1 期 数学 的 实践 与 认识 voL30 N BERAEE
2000 年 ! 月 MATHEMATICS N PRACTICE AND THEORY. Jan 2000 7
problem, the objective functiom is built Wepresent themappingprincple,tomap the locationsof
the originalw ells into aunique unit block of themesh, so as to smplify the solution of the model
U sing themapping algorithm and the ergodic algorithm ,we solve the problem under the direction
constraint Then we generalize the algorithm s to the solution without the direction constraint We
studied the sufficient conditions and give some criteria of the availability on threeparticular condi-
tions Themethod of bisection on perpendicular atm idpoint is presented
4
= 人 Se
米 六 ma 时
钻井 布局 的 数学 模型 “外
yAT
胡 海 洋 ， 陈 建 ， 陆 春  ud
指导 教师 陈  PR
(南京 大 学 ， 南 京 210093) As
摘要 : 。 本文 对 钻井 布局 问题 的 研究 , 是 从 全 局 搜索 入 手 ， i# D A—
杂 性 , 得 到 不 同 条 件 下 求 最 多 可 利用 旧 井 数 的 较 好 算法 J\ SN
对 问题 1, 我 们 给 出 了 全 局 搜索 模型 、 局 部 精 化 模型 与 图 论 模型 , 讨论 了 各 种 算法 的 可 行 性 和 复杂 度 得
到 的 答案 为 : 最 多 可 使 用 4 口 旧 井 , 井 号 为 2, 4. 5, 10 对 问题 2, 我 们 给 出 了 全 局 搜索 , 局 部 精 化 和 旋转 矢量
等 模型, 并 对 局 部 精 化 模型 给 出 了 理论 证 明 , 答案 关 ) 最 多 可 使 用 6 口 旧 间 , 并 号 为 1. 6. 7 8, 9 11, 此 时 的 网
格 逆 时 针 旋 转 44 37 度 , 网 格 原点 坐 杨 5 47.0 所 加
对 问题 3, 给 出 判断 an 口 间 是 否 均 富 % 久生 各 用
J
1 ai 和
2 问 有 Saues 扩
如果 个 吕 二 二 其 人 后 结 点 < 下 让 起 过 给 定 误 郑 el0.09) 单位 , 则 认为 P，
人 用 因此 , 在 棋盘 ( 欧 氏 ) 距离 定义 下 , 可 以 以 忆 , 为 中 心 , 2e 单 位 为 边 长
作 一 个 1 和 cp 加 若 网 络 在 平移 过 程 中 , 网 络 中 的 某 个 结 点 站 落 在 以 忆 , 为 中
心 的 正 5 圆 ; 内 或 边 上 , 可 认为 YX 可 利用 旧 井 已, 的 相应 资料 同样 可 以 以 站 为 中 心 , 2e
意 机 为 边 长 作 一 个 正方 形 ( 圆 ) 若 网 络 在 平移 过 程 中 ,P, 落 在 以 为 中 心 的 正方 形 ( 圆 ) 内
VSRABETTTUON x, 可 利用 旧 并 忆 的 相应 资料 这 两 种 方法 分 别 对 应 于 网 格 移动 和 坐标 平
移 , 温 然 它们 是 等 价 的 以 下 的 讨论 将 不 明显 区 别 这 两 种 方法 为 了 简化 讨论 , 引入 以 下 法
则
映射 法 则 :
将 点 守 映射 至 以 (o,,，(o+ 1,5+ 1) 为 对 角 顶 点 的 正方 形 内 的 点 六 站 = i- [i]+ a
六 = [+ 也 其 中 [x] 为 x 的 整数 部 分
覆盖 法 则 :
将 所 有 旧 井 映射 至 (- 1 - D, (0,0); (- 1,0), (0, D; (0- 1), (1,0); (0,0), (1, 1) 为
对 角 顶 点 的 四 个 正方 形 上 以 2e 为 边 长 作 小 正方 形 , 该 正方 形 形 心 在 以 (- 0.5, - 0.5)，
了?

<!-- source_page: 2 -->

加

人
1 期 刘海 洋 等 钻井 布局 的 数学 模型 证 一
(0. 5, 0.5) 为 对 角 顶 点 的 正方 形 内 移动 , 则 可 被 正方 形 所 覆盖 的 映射 点 为 可 同时 利用 的 点
这 样 的 正方 形 称 为 判决 正方 形 或 判决 方块 相应 的 , 在 第 二 问 中 采用 一 个 半径 为 e 的 圆 移动
来 覆盖 映射 点 , 称 为 判决 贺

映射 法 则 禾 盖 法 则 是 易于 理解 也 是 易于 证 明 的 下 面 我 们 讨论 时 都 应 用 了 映射 法 则
禾 盖 法 则 , 将 点 映射 后 在 映射 区 间 内 判断 旧 井 是 否 可 利用
3 模型 的 建立
3.1 对 问题 一 的 讨论 4

1 目标 函数 的 给 出 -从 >

和 人 0

a+ Ni- €ESP,<a+ N.+ €

且 b+ Ni- €ESP,<b+ Ni+ 6 J
Hn  AIn; 为 非 负 整数 X

s 人

上 a+ Ni- €<X, <a+ N 他 ESY, <bhb+ N.+ €
MX.,Y)= L,=
0， 其 它 《<
有
Fla,b) = may 二 (人 中
人 9

2. 模型 一 : 枚 举 法

在 本 题 中 , 由 于 精度 的 要 求 为 0.01, 生 网 格 可 上 下 \ 左右 平行 移动 因此 可 按 纵 、 横 坐 标
2 12 个 旧 井 点 搜索 , 如 覆盖
旧 井 点 , 则 记录 覆盖 数 最 后 比较 在 这 100X 100 次 平移 中 , 哪 一 次 覆盖 数 最 大 , 则 该 网 格 位
置 为 最 优 一

让 坟 的 所 多 Pt] ,7 为 旧 井 数 , / 为 数值 的 要 求 精度 , 在 本 题 中 为 0. 01

计算 结果 如 下 网 格 节点 为 (0. 36, 0.46), 最 多 可 利用 旧 井 数 为 4, 分 别 是 2, 4, 5, 10 号
井 枚 0 颇 为 有 用 , 但 当 精 度 要 求 很 高 时 , 往往 较为 复杂 在 模型 一 的
了 有
要 网 和 型 一 部 分 男 举 法 1
诺 12 个 旧 井 点 中 的 任 一 个 井 点 都 存在 一 个 网 格 , 使 得 该 井 点 可 被 该 网 格 所 用 因
丝 可 以 在 P, 已 被 该 网 格 利用 的 情况 下 , 再 去 检查 其 它 旧 井 点 能 否 被 该 网 格 所 利用 因此 , 可
将 网 格 中 一 个 结 点 放 在 以 该 点 为 中 心 , 2e 为 边 长 的 一 个 正方 形 区 域 中 , 再 去 测试 其 它 旧 井
点 是 否 满足 条 件 对 于 一 个 而 言 , 网 格 某 个 结 点 , 在 以 该 点 为 中 心 , 2e 为 边 长 的 正方 形 区 域
中 有 (2e/D)” 种 放置 法 这 样 即 得 部 分 穷 举 法 的 复杂 度 为 o (2 (e/P)).

部 分 穷 举 法 抓 住 一 个 旧 井 点 后 考察 其 它 旧 井 点 的 情况 因此 , 它 比 全 部 穷 举 法 优点 在
于 : 避免 了 对 所 有 旧 井 点 均 不 可 利用 的 情形 的 搜索 但 该 算法 的 缺点 在 于 不 能 太 大 , 否则
可 能 得 不 偿 失 , 使 计算 量度 大 为 增加
) 计算 结果 与 模型 一 相同

<!-- source_page: 3 -->

加
全
62 数学 的 实战 与 认识 0 times

4. 模型 三 : 部 分 穷 举 法 1

在 模型 二 中 我 们 根据 至 少 利 用 一 个 点 的 原则 移动 判决 方块 在 本 模型 中 我 们 在 至 少 有
两 口 并 可 用 情况 下 , 由 两 口 井 确定 一 个 判决 方块 , 进而 进一步 缩减 计算 量

定理 1 3 1 在 覆盖 点 数 最 多 的 判决 方块 中 必 有 一 个 方块 4 满足 下 述 两 条 之 一 :

(D 有 两 点 忆 与 P, 分 别 在 4 的 左边 框 和 下 边框 上 ;

C) 有 一 点 忆 在 4 的 左下 项 点 处

该 定理 的 证 明 从 直观 上 看 是 显然 的 , 若 某 判 决 方块 4 黎 盖 的 点 数 最 多 , 将 4 连续 向 右
和 向 上 移动 , 直至 若 继续 移动 将 会 有 点 跑 出 为 止 , 此 时 4 (的 位 置 记 为 4, 则 4 Sr
两 条 件 之 一 , 且 4 中 点 数 也 是 最 多 的 = Ls

由 此 定理 , 我 们 只 需 在 所 有 以 两 点 确定 左边 框 和 下 边框 的 判决 方 光 和 太  T
点 确定 的 判决 方块 的 覆盖 数 之 间 进 行 比较 ， 0

该 方法 对 于 个 并 点 , 需 计算 约 (C+ 四 复杂 度 为 O Co)K 是 与 精 庆 元 关 的 算法

计算 结果 同上

5. 模型 四 : 涂 层 法 As

由 映射 法 则 , P，。 P 的 映射 点 在 正方 形 [(- 有 1 日] 内 为 PP 则 PP
可 用 的 充 要 条 件 是 4(P),P) <26 即 分 别 以 PP H IBNG ze 的 两 个 正方 形 相交 对 于
个 点 , 则 这 ， 个 点 都 可 用 的 充 要 条 件 是 以 这 ， 个 点 久 jie 的 正方 形 都 相 吉 以 相 本 部 分 为 网
格 点 ,总 可 以 利用 这 ， 个 点 本 模型 即 用 这 样 的 思路 , 计算 最 多 有 多 少 正方 形 相 二 , 并 以 相生
部 分 中 的 一 点 以 网 格 结 点 作 网 格 9

算法 思想 : 用 矩阵 4 人 Ce 1+ 9] 将 点 离散 化 , 以 精度 0 取样 则 4
表示 为 二 25 阶 雪 征 陈 用 全 1 EH SA AE£5 p) 为 中 心 , 26 为 边 长 的 小 方形 则 将 这
些小 算 阵 加 到 大 征 阵 的 相配 置 上 去 , 即 相当 于 把 小 正方 形 “ 涂 "到 大 框 里 则 4 中 某 点 上
数字 之 和 即 表 示 该 点 被 多 ” P , t0 BA HE  OS FTRUF  D J 找 出 4
中 数字 最 大 者 , MISAARFEJFAL 该 点 为 最 优 网 格 的 起 始点

ec 在 精度 不 太 高 时 计算 是 迅速 的 精度 高 时 , 对 内 存 和 速度
二 有 1

§

6. 站 论 模型
SA 定理 1 全 1 作 一 无 向 图 GIF,E],F 为 旧 并 点 的 集合 若 第 ;与 第 / 号 井 可 同时 利用 ，
1 间 加 一 条 边 则 可 同时 利用 的 井 点 组 成 一 个 完全 子 图 , 即 团 在 棋盘 距离 下 最 多
可 渊 用 旧 井 数 等 于 最 大 团 的 阶 数

证 明 ( 咯 )

此 定理 对 欧 氏 距离 不 适用 由 此 定理 可 得 到 下 述 推论

推论 在 棋盘 距离 下 , 着 某 些 旧 间 两 两 可 同时 利用 , 则 这 些 旧 井 可 被 同时 利用

由 此 提出 图 论 模型 如 下 : 按 定理 1. 5. 1 构造 图 6, 找 最 大 完全 子 图

首先 , 找 出 可 同时 利用 的 旧 间 对 可 利用 下 述 定理 求 得

定理 1 s 2 PP 均 可 以 在 某 网 络 中 被 利用 的 充 要 条 件 是 存在 非 负 整数 V ,N ,全
得 :
o4 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.  hitp://www.cnki.net

<!-- source_page: 4 -->

加
RE T
1 期 胡 海 洋 等 钻井 布局 的 数学 模型 3 om
di(Pppi) EN- 2eNi+ 26]，
心 (PPpi) E[N2- 26 N2+ 26]，

其 中 与 w 分 别 表示 x 方向 与 ， 方向 距离

证 明 “( 略 )，

下 述 定理 是 图 论 中 熟知 的 定理

定理 1.5.3 设 G 是 ， 阶 无 向 图 ,7 为 G 中 极 大 (最 大 ) 团 当 且 仅 当 六 "为 5 的 中 的 极
大 (最 大 ) 独立 集 ,其 中 G 是 G 的 补 图

因此 , 问题 归结 为 寻找 5 中 的 最 大 独立 集 但 寻找 最 大 独立 集 为 VP 站
的 方法 = ss

图 论 模型 优点 在 于 : 它 在 理论 上 是 完备 与 精确 的 ， Ta

7. 五 个 模型 的 比较

对 于 五 个 模型 的 比较 , 我 们 认为 模型 三 .四 五 是 较 优 的 模 9 复杂 度 为
o[ 癌 .对 于 大 多 数 情况 都 是 适用 的 模型 四 与 精度 有 关 人 让 ,在 本 题 中
ep= 5 在 精度 要 求 不 太 高 , 且 点 数 较 多 时 , 可 获得 比 模型 三 让 快 的 速度 模型 五 是 一 个 VP
问题, 当 点 数 较 多 时 , 甚至 是 不 可 能 求解 的 但 本 模型 提供 宁 一 个 较 完美 的 具有 理论 意义 的
图 论 模型 X2As
3.2 对 问题 二 的 讨论 JIN

1. 模型 一 : 全 局 搜索 法

以 某 一 个 角度 为 步 长 转动 网 格 , 在 每 一 盘 度 下 , 固定 网 格 方向 按 问题 一 的 方法 检验 最 多
有 多 少 旧 井 可 以 利用 再 比较 所 有 所 器 过 的 角 傣 下 可 利用 的 旧 井 数 , 即 可 得 允许 转动 时 可 利
用 最 多 旧 井 数 两 点 疝 的 棋盘 距离 区 全 生动 而 改变 , 故 问题 二 采用 欧 氏 下 离 由 于 方 格 的 对
称 性 , 只 需 从 0" 旋转 到 90" 即 可 , 涯 保证 旋转 小 角度 后 , 点 的 变动 不 超过 精度 P = 0. 01, 使 步
长 Ab< 全 om 和 wweemns 本 题 中 求 出 Ag<1.04X10 。 需要 将
| 司 分 为 2000r 人 = 因 呈 术 题 要 进行 2000 次 问题 一 的 计算 该 模型 简单 可 靠 ,易于 理解 ，
Ai 和 用 因此 有 待 改进

长 赂 逆 时 针 转 动 4.37" 一 个 网 格 点 在 原 坐 标 系 下 的 坐标 为 (0. 47，
0. 62) 这 寺中 有 6 个 井 被 同时 使 用 , 井 号 为 1 6,7, 8, 9, 11

\2 BUG 旋转 矢量 法
合生 aamfwamwRmeokwamabtms usam 至 多 只 能 再 转动 一
下 在 这 个 极 小 的 角度 内 以 步 长 A8 转 动 , 搜索 最 多 可 利用 的 旧 间 数 任意 一 对
可 间 时 利用 的 旧 井 都 需要 进行 以 上 操作

定理 2.2.1 两 旧 间 wz 可 同时 利用 的 充 要 条 件 为 存在 整数 m,n 使 | 几 sy 2|<
26 其 中 他 (多 于 @- 的 ?为 两 旧 间 的 欧 氏 距离

证 明 ( 略 )

定理 2 2 2 设 两 旧 井 wp 可 同时 被 利用 ,a 点 到 网 格 原点 距离 di 与 上 点 到 结 点 @w ,让
距离 4 均 不 超过 € 则 当 网 格 转动 角度 超过 4( 其 中 4 a 到 4 的 距离 ) 弧 度 时 , 则 di 与
23 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved  http://www.cnki.net

<!-- source_page: 5 -->

加
旺 语
64 数学 的 实践 与 认识 0 times
中 至 少 一 个 将 超过 e
证 “ 因 ec < 4, 以 原点 为 旋转 中 心 , 将 网 格 旋转 A6 弧 度 ,5 点 相对 结 点 on , m) 至 少 移动
LA8 于 是 当 A6 25 时 ,do> € 同样 以 On ,中 为 旋转 中 心 , 旋转 A626 时 ,di> € 考虑 最 不 利 情
形 , 当 网 格 转动 A8 和 时 ,4 与 v 中 至 少 一 个 超过 <
依据 该 定理 , 先 将 网 格 旋转 与 平移 到 某 一 位 置 , 使 。 两 旧 间 均 被 利用 , 在 该 位 置 , 网 格
最 多 多 许 再 旋转 些 弧度 我 们 只 需要 在 该 小 范围 内 检查 其 它 井 是 否 可 被 利用 y N
作 上 述 讨论 , 即 可 求 得 可 利用 的 井 数 的 最 大 什 sk
3. 模型 三 : 全 局 搜索 “局 部 精 化 PN
本 模型 的 思想 是 先 以 较 大 步 长 进行 全 局 搜索 , 找到 一 个 大 概 范 围 y 本 竹 该 范围 内 精确 搜
索 , 直至 得 到 最 优 结果 ) 放 到
将 网 格 放 转 菜 一 角度 B( 以 弧度 为 单位 ), 再 将 所 有 旧 指 恋人 方 法 人 对 到 原点 周 轩 四
个 单位 网 格 内 现 将 误差 扩大 为 er (1+ e 其 中 & 0 RERIN e 与 的 同心 国 @ 与
,使 得 @ 内 覆盖 的 陨 射 点 数 最 大 , 设 为 4! 若 网 格 认 计 角度 有 ”个 小 的 改变 量 AB 则 各 上
并 在 网 格 中 的 位 置 将 移动 |R,A6| , 其 中 R, 为 第 ; 晤 十 到底 转 中 心 的 距离, 此 时 它们 的 映射
点 也 将 移动 |&Ab| 距离 设 R= maxR ,Raz Ri 六 国 lRAbl<e- e 到 即
1Ag6| < de/, (*)
则 原来 在 @ 外 的 点 不 可 能 移入 至 @ 中 (这 是 因为 这 两 个 同心 圆 边界 的 距离 G K TFsg A¢
SIER), 于 旦 当 (*”) 成 立时 ,器 六 的 上 出 需 数 (sk
基于 上 述 分 析 , 算法 思想 为: 5 和 当 的 5 以 er (1+ 日 6 为 允许 误差
= ?148|= 2564 为 步 坎 从 9 到 闻 进 行 搜索 , 求 得 可 利用 旧 间 数 的 上 界 M. 将 允许 误 半 仍
回 到 上 求 得 加 吕 覆盖 的 点 央 为 江 著 mW , 则 可 利用 的 旧 间 数 就 是 M/ ,问题 已 解决 若 m<
M， 则 适当 减 小 @ 此 时 步 长 外形 相 应 减 小 , 进行 精细 搜索 搜索 的 范围 可 以 减少 很 多 这 是
因为 若 对 某 一 个 角度 6. 第 一 次 以 e 为 允许 误差 求 得 的 覆 益 点 数 小 于 wm , 则 显然 旋转 角度 在
区 间 [6- 1A9| , 84 1%6[ 内 时 , 可 利用 的 点 数 也 小 于 m , 因此 在 第 二 次 精细 搜索 时 , 该 区 间
WALQES)
从 个 本 全 着 能 减 小 上 值 , 则 在 相同 多 许 误 状 c- (1+ 器 条 件 下 , 步 长 p- 2
| 骆 可 丧 汰 ,我们 的 做 法 是 选择 旋转 中 心 使 得 各 旧 井 到 旋转 中 心 的 最 远 距 高 最 小 , 目标
1 对
7 GD 人 = 有 GD 0 和，
S tt minf (x,v),
其 中 Ce,y) 为 新 坐标 原点 ( 即 旋转 中 心 )
这 是 非 线性 无 约束 最 优 规划 问题, 我 们 用 SA S 软件 , 采用 单纯 形 法 计算 , 结果 为 *=
5.04,y= 70,R= f GyJ- 4.55 此 时 R 比 以 原 坐标 原点 为 旋转 中 心 减少 一 半 以 上
我 们 取 检 查 次 数 N = 120, 步 长 为 90120= 0.75° 此 时 &= 杰 0.6 es 1.66 得 到
可 利用 旧 井 的 上 界 M = 6
了?

<!-- source_page: 6 -->

加
后

1 其 胡 海 洋 等 : 钻井 布局 的 数学 模型 5 om

另 一 方面 , 取 任 一 步 长 , 以 半径 为 e 的 判决 圆 搜索 可 得 到 可 利用 旧 井 数 的 下 界 六 .

显然 若 上 界 与 下 界 相 等 , 则 可 利用 的 旧 井 数 最 多 为 m. 而 网 格 的 方向 就 随 之 可 确定

对 于 本 题 , 步 数 取 120, 判决 圆 半 径 为 e= (1+ D。6e 时 ,可 得 上 界 M = 6 再 取 步 数 为
2, 判决 圆 半 径 为 e 时 , 步 长 为 45 度 , 得 下 界 m= 6 故 可 知 最 多 可 利用 旧 井 数 为 6, 旋转 角度
即 为 45 度 仅 需 122 次 左右 问题 一 的 计算 , 可 以 较 大 的 削减 计算 量

算法 结果 : 可 利用 的 旧 井 数 的 上 限 为 6 网 络 逆 时 针 旋 转 45°, 其 中 一 个 苘 点 坐标 为
(0.46,0.56), 可 利用 旧 井 序号 为 (1, 6, 7, 8, 9, 11).

4. 对 问题 二 各 模型 的 评价 2

模型 一 是 直观 和 易于 理解 的 , 但 搜索 步 数 过 多 , 耗 时 过 长 ， EN
向 , 再 在 该 方向 附近 进行 搜索 在 二 较 小 时 , 可 较 大 的 削减 计算 量 y<8 HURHE (9 KEX
方向 数 过 多 , 有 可 能 得 不 偿 失 , 反而 增加 计算 复杂 性

模型 三 我 们 认为 是 较 好 的 , 先 以 较 大 的 步 长 搜索 , 再 以 小 步 长 ao
算 量
3.3 问题 三 的 解答 各

在 解决 问题 一 问题 二 的 基础 上 , 解决 问题 三 0 个 点 是 否 均 可 利用

1. 棋盘 距离 下 C

因 坐 标 旋转 会 改变 两 点 间 的 棋盘 距离 ， SS - 以 某 一 口 旧 井 为
坐标 原点 建立 平面 直角 坐标 系 , 再 将 各 旧 井 映射 到 以 (- 0.5, - 0.5) 与 (0.5, 0.5) 为 对 角 顶
点 的 正方 形 内 , 即 若 昌 井 PiGi= 1,2, …, n) 的 给 标 为 (cy , 它 的 映射 象 P， 的 坐标 (7y 人
满足 人 / ®

(1)- 0.5<x'<05, -0 5 5;

(C) xx 与 yy 生 均 为 整数

显然 我 们 有 : ) Ang

定理 31 dd.- 本 1 af | 则 在 模 盘 距 离 下 ， 口
旧 井 均 可 利用 的 二 和 为 "<2c d, <2¢

2. AT

区 离 的 映射 方法 , 我 们 有 :

定理 3 XI 网 络 不 可 旋转 的 条 件 下 , 采用 欧 氏 距离 ,” 口 旧 井 均 可 利用 的 充 要 条 件 为
它 估 的 映射 旬 PP2…Pu% 可 被 一 判决 圆 所 覆盖
] 1. 和沙 移 动 判决 圆 ， 总 可 使 该 判决 圆周 上 至 少 含 两 个 映射 点 据 此 , 算法 思想 为 : 以 任意 两
于 昌吉 确定 西 个 半径 为 的 加 ,检查 是 否 所 有 的 映射 点 艾 在 凑 加 上 最 多 检查 2C*=
mnO- JJ) 次 算法 的 时 间 复 杂 度 为 O (n).

我 们 还 可 给 出 欧 氏 距离 下 , 不 可 旋转 时 口 旧 井 均 可 利用 的 充分 条 件 与 必要 条 件 :

定理 3 2 2 充分 条 件 为 任意 两 个 映射 象 P' 与 己 / 的 距离 均 不 超过 | 3 e

证 明 ( 略 )

定理 3 2 3 必要 条 件 为 任意 两 个 映射 象 P “与 忆 / 的 距离 均 不 超过 2¢

证 明 ( 略 )

3. 欧 氏 距离 下 网 格 可 旋转 的 情况
o4 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.  hitp://www.cnki.net

<!-- source_page: 7 -->

说
FE]
Dr
66 数学 的 实践 与 认识 后 oa
选择 一 口 旧 井 , 使 各 旧 井 到 它 的 最 远 距 离 最 小 , 以 这 口 井 为 坐标 原点 和 旋转 中 心 设 旋
转 了 某 一 角度 6 后 , 各 井 按 旋 转 后 的 新 坐标 映射 到 以 (- 0. 5, 0. 5) 与 (0. 5, 0.5) 为 对 角 顶 点
的 正方 形 内 , 它们 的 映射 象 为 己 i= 1 2, …, 半 则 我 们 有
定理 3 3 1 存在 一 个 角度 gs [0, rw2], 使 得 旋转 6 角 后 , 各 旧 并 的 映射 象 P",P*，
…,P "被 一 判决 圆 全 部 覆盖
计算 可 利用 井 数 在 问题 二 中 已 有 详细 讨论 , 我 们 建立 的 模型 与 算法 均 可 用
例如 由 定理 2. 2. 1 可 知 , 若 对 两 旧 井 a, b, 不 存在 整数 m ,使 得 |4- 1 放 于 克 | 码 26 成
立 , 则 ao, 中 最 多 只 能 利用 一 口 井 因此 该 定理 可 作为 判别 口 井 均 可 利用 的 一 珀 必要 条 件
让 人 本 > - < Jdg
对 于 该 问题 , 我 们 认为 有 效 的 一 个 充 要 条 件 是 难 找 的 , FA %0 S  REA 未 他 计 算 来
下 一 PDF NT
it 2 人
4 模型 结论 改进 方向 及 建议 ( 略 ) J
参考 文献 4 ‘
[1] 姜 启 源 数学 模型 .高 等 教育 出 版 社 , 北京 , 1993 全
[2] 叶 其 学 . 大 学 生 数学 建 模 竞 赛 辅导 教材 . 湖南 教育 出 版 社 , 长 网
[3] 朱 道 元 . 数学 建 模 精品 . 东南 大 学 出 版 社 , 南京 , 1999
O 〇
The ML athemat}6y odel of Borehole Layout
HU Hai-yang, -/CHEN Jian, LU Xin
(Po niversity，N anjing 210093)
Abstract  In 下 begin our research of mathematicalmodel of borehole layout w ith
an eye to we 是 analyze step by step the effeciency, flexibility and complexity of all
ae6 gmethods Atlastwegeta relativity bettermethod to make out the number
of (gr can be utilized under different circum ferences
thesfirst question, after the demonstration of an overall research model, precise local
站 fdel and a graphizalmodle，and after the discussion of the flexibility and comp lexity of various
] // leulating methods, we come to the answer ramedy, that only four used boredho les can be ut
人 Nk atmost, numbered 2,4,5,and 10
To the second question, we offer an overall research model, a precise bocalmodel as well
as a revolving vectormodel In particular, we give a theoretical demonstration of the localmod-
el The answerwe get is thatonly 6 used boreholes can be utilized atmost, numbered 1, 6, 7, 8,
9,and 11 and that the net w ill revolve 44.37 w ith a coordinate (0.47,0.67).
To the third question, in order to judge w hether all of the given boreholes can be used, we
enum erate the ample requirements and the compulsory requirements together w ith the approri-
ately effective calculating m ethod
4 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.  http.://www.cnki.net

