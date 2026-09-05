# Extracted Paper

<!-- source_page: 1 -->

回 大 车 油 国
本
第 31 卷 第 1 期 数学 的 实践 与 认识 Vol31 N
2001 年 ! 月 MATHEMATICS N PRACTICE AND THEORY Jan_2001
have the mathematicalmodel——amodel of indefinite output
After designing themodel firstly we use the method of inproved mininal factors and the
method of mproved algorithm to get an initial solution; Secondlywe use themethod of iteration
and themethod of trial to adjust and modify it; Lastly we draw a conclusion
钢管 订购 和 运输 策 咯 # >》
一
BUET, 会 昌盛 ， 吴 建 德 = 蛋
指导 老 岳 。 张 用 党。 2
(西北 工业 大 学 ， 西 安 710072) H
编者 按 : N, -. N—
小 运 购 费 , 建立 了 问题 求解 的 OCS 问 的 模型 具有 较 强 的 一
般 性 , 适用 于 树 形 结构 的 通常 情形 值得 注意 的 是 , 模型 中 有 关 铺 设 贵 的 假设 和 表达 式 与 常见 情形 略 有 不 同
摘要 : ”在 铺设 管道 为 一 条 线 的 情况 IT 由 于 变
量 较 少 , 约束 条 件 大 都 为 线性 的 , 目标 函数 为 二 次 函数 , 所 以 利用 L ingo 软件 , 可 以 很 快 求 得 比较 满意 的 订购
和 运输 方案 我 们 利用 M atlab 软件 , 对 所 得 到 的 数据 进行 拟 合 , 得 到 相应 的 反映 销 价 变化 对 总 费用 影响 的
曲线 , 然后 比较 各 个 钢 厂 钢管 销 价 变化 对 总 费用 影 全 的 大 小 对 于 钢 厂 钢管 产量 上 限 变 化 对 总 费用 和 购 运
计划 的 影响 ， 2 我 们 对 树 形 图 的 每 条 边 定向 , 建立 了 与
铺设 管道 为 一 条 线 时 类 似 的 数学 模型 , 拓 列 丰 天 拓 广 了 模型 的 使 用 范围 在 论文 中 , 我 们 还 对 所 建立 的 模型
的 优 缺 点 和 需要 改进 的 方向 进行 了 讨 放 “ )
1 符号 说 明 和
“5 钢 厂 en 钢管 的 最 大 产量 ;
“ww 4 到 下 ,这 俩 铺设 管道 的 里 程 数 :
cr owhle 运 到 4 ， 所 需 最 小 订购 和 运输 费用 ;
. 0
-Y ; 运 抵 4， 点 的 钢管 数量 , 不 含 路 过 4 的 部 分 ;
六 六 运 到 4， 的 所 有 钢管 沿 4， 一 4 产 : 铺设 的 数量 ;
] ~ 运 抵 4 的 所 有 钢管 沿 4 ,一 4 铺设 的 数量 :
N 44 ): 树 中 4 的 度数 :
“4 dd): 树 中 4 的 入 度 ;
“4 dd): 树 中 4 的 出 度 ;
“上 单位 钢管 1 公里 的 公路 运输 费用
2 ”基本 假设
根据 题目 的 要 求 , 并 为 达到 简化 问题 的 目的 , 我 们 有 以 下 假设 :
1 假设 运 到 4， 的 钢管 , 只 能 在 4 六 :到 4 广 :之 间 包 含 4， 的 某 个 区 段 内 铺设 并 且 到 达
2 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved. http:/Wwww.cnki.net

<!-- source_page: 2 -->

加
黎 一 这
64 数学 的 实 夏 与 认识 1 卷 m
47 的 钢管 在 4 :到 4 六 :之 间 包 含 4， 的 铺设 区 段 和 到 达 4 六 :的 钢管 在 4 到 4 六 > 之 间 包 含
4 的 铺设 区 段 不 相交 否则 的 话 , 总 可 以 调节 铺设 方案 , 使 得 总 费用 减少
2 在 考虑 问题 2 时 , 假设 钢管 价格 不 可 能 有 太 大 幅度 变化 ”所 以 , 我们 只 考虑 钢管 价格
在 其 原 售 价 10% 的 范围 内 波动 同时 ,我 们 假定 , 钢 厂 的 产量 不 可 能 成 倍 的 增加 或 减少 我
们 在 减少 300 个 单位 , 增加 600 个 单位 的 范围 内 讨论 , 这 意味 着 我 们 不 考虑 钢 厂 破产 或 者 超
大 规模 扩大 生产 的 情况
3 在 具体 铺设 每 一 公里 时 , 我 们 只 把 钢管 运 到 每 一 公里 开始 的 地 方 , 沿 运送 方向 向 前
铺 , 然后 往 前 铺设 的 运送 费用 我 们 不 予 考虑 #7
2“ 必 2
3 模型 建立 2 \
1 问题 1 的 模型 )
(1) 决策 变量 A,
我 们 首先 引入 一 组 0- 1 变量 xx …,xr?, 其 中 多 多 SS 是 否 承担 制造 这 种 钢
管 如 果 钢 厂 S$, 承担 制造 这 种 钢管 , 则 *, = 1 否则 到 一 0
所 有 的 钢管 , 都 是 先 运 到 4 ,4 > …,4. 后 , 忆 于 其 它 地方 , 或 者 在 包含 4， 的 一
个 区 段 内 铺设 ”我们 设 从 钢 厂 S, 运 抵 4， 且 在 包含 前 有 区 段 内 铺设 的 钢管 数量 为 y，，
这 里 1= 1 2,…,7; j= 2,…,1S \
我 们 用 变量 2, 来 表示 从 所 有 的 钢 厂 运 到 4， 的 钢管 总 量 中 沿 4 -4 六， 铺设 的 部 分 , 这
里 7 = 1,2,…,14 @
这 样 ， 我 们 一 共 引入 了 三 组 决 俯 交 站 0
3; zk= 2 1 多
(2) 目标 函数
问题 1 人 上访 使 得 总 费用 最 小 事实 上 , 总 费用 可 以 分 成
两 部 分 第 一 部 分 包括 钢 和 和 风格 和 和 AI 运 抵 454，…,45 所 需 的 运费 ; 我 们
用 大 S 运 抵 4， 所 需 的 最 小 订购 和 运输 费用 , 则 第 一 部 分 费用 为
% V ur = 五 co
第 二 部 east 42 4 后 ,再 运 到 具体 铺设 地 点 的 费用 由 假设 3, 从 4 ，
到 列 队 所 需 的 费用 为
人- 全 有
WA
NN 表示 4， 到 4 *: 铺设 管道 的 长 度 这 样 , 我 们 不 难得 知 第 二 部 分 费用 为
CD
(3) 约束 条 件
首先 , 由 于 一 个 钢 厂 如 果 承 担 制造 这 种 钢管 , 则 至 少 需要 生产 500 个 单位 , 而 钢 厂 8, 在
指定 期 限 内 能 生产 钢管 的 最 大 数量 为 * 个 单位 所 以 ,我 们 得 到 以 下 一 组 约束 条 件
500r, = Yyy Sosar ii 12 7
4 hina Academic Journal Electronic Publishing House. Allrights reserved。  http:/www.cnki.ne

<!-- source_page: 3 -->

加
如
1 期 段 了 军 等 钢管 订购 和 运 答 策略 5 om
由 于 订购 的 所 有 钢管 总 量 等 于 4 一 4 :一 … 一 4 的 里 程 数 , 那么
 Sy,= 5171
很 显然 , 我 们 可 以 设 z 三 wm 因为 如 果 z > wu 则 相当 于 有 2 - wm: 数量 的 钢
管 是 从 4 直接 运送 到 4 *， 后 再 送 到 具体 铺设 地 点
运 抵 4， 的 钢管 总 数量 , 等 于 向 包含 4， 的 区 段 铺设 的 里 程 数 , 那么
= 0 2,3,,14 %
并 且 , 我 们 还 有 = 2 和》 yis= W 1415 - ZI4 = 蛋
全 局 1 会
(4) 数学 模型 %
通过 上 面 的 分 析 , 我 们 得 到 问题 1 的 如 下 模型 )
min3y cp EPNEIOE 1) 十 人 zi- D1]
500x, 三 Yyu < saxs, 江 ' 2. .全
和 和 = 5171 儿
Syi=zit Or- zp),  j= 23,…,14
入 @
Uyst > - %%
TS Z14
0<z 的 了 = 1,2,…,14
zx _0, 1， i= 1,2,…,7
1 三 0， i= 2 15
ons
2. 归 题 2 的 模型
5 和 人 smwmatamaramannmemarafen' , 利用 模型
人 有 R 算出 它 的 钢管 销 价 发 生 一 系列 的 变化 后 , 所 得 到 的 总 费用 和 购 运 计划 ; 并 根
1 各 si, 和 atlab 软件 拟 合 出 销 价 变化 和 总 费用 变化 量 关 系 的 曲线 , 对 所 得 到
的 曲线 进行 分 析 和 对 比 , 找到 钢管 销 价 变化 对 购 运 计划 和 总 费用 影响 最 大 的 钢 厂 “类似 地 ，
我 们 用 同样 的 方法 , 对 钢 厂 产量 上 限 发 生变 化 对 购 运 计 划 和 总 费用 的 影响 进行 了 分 析
3. 问题 3 的 模型
如 果 要 铺设 的 管道 不 是 一 条 线 , 而 是 一 个 树 形 图 ,我 们 首先 给 树 形 图 的 每 条 边 指定 一
个 方向 , 使 得 所 得 到 的 有 向 树 有 一 个 度数 为 1 的 顶点 的 入 度 为 0, 而 其 它 每 个 顶点 的 入 度 均
为 1 与 问题 1 一 样 , 我 们 可 以 引入 0- 1 变量 x,(= 12,…,7) 以 及 变量 (= 1 2,.…,7，
7 = 12,…,21, 它 们 的 含义 与 问题 1 中 的 定义 完全 一 致 类 似 于 问题 1, 对 于 有 向 树 的 有 向
边 U ,4 ,我 们 用 zy 表示 运 抵 4 ,的 所 有 钢管 沿 4 ,一 4 铺设 的 里 程 数 数学 模型 为
2 © 1994-2008 China Academic Journal Electronic Publishing House. Allrights reserved.  http:/www.cnki.net

<!-- source_page: 4 -->

回 大 车 油 国
66 数学 的 实践 与 认识 1 tien
7 15
mi 和 copy 二 DC D+ or zuor 2 D]
| Cn47TEE(T)
21
500x; 三 SSsrn j= 1,2,,7
7
> 7 = 5903
1 全 1 ，
当 dU)> 10, Yy= Y zat bi ,其 中 Uno4)EEO)
= CODEE(CT) 一
B)st 、 ? 多
Hd U)= 0 时 , 2 wo zz 其 中 do4) €E(T)T A7
= 全 由
当 d! d)= 0 时 ， pRY = z 如 其 中 dj49 € coZS
0=zy=wij, “:,4,) EE(T)  ud
xi= 0,1, i= 1,2,,7
yiz0, i=1,2, < … ,21
参考 文献 ; X
一
[1] 甘 应 爱 , 田 丰 等 著 . 运筹 学 . 清华 大 学 出 版 社 , 北京 , 1994 K
[2] 袁 亚 湘 , 孙 文 瑜 著 . 最 优化 理论 与 方法 . 科学 出 版 社 , 北京 , 199
[3] 人 徐 俊明 著 . 图 论 及 其 应 用 . 中 国 科学 技术 大 学 出 版 社 , 合肥 , 1997
O 〇
人 LA °
AAA .
The Strategy of co 给 and Transporting Steel Tubes
DUAN x 一 YU Chang-sheng， WU Jian-de
essGrorfthw 6stern PolytechnicalU niversity，Xian 710072)
Abstraet， NT pipelines are in line-shape, we provide a nonlinear programm ing
mo y/A problem. Since there are not too much variables, most of the constraints are
os goal function is quadratic, one can get satisfactory strategies quickly by using
\ the software L ingo. W ith the softwareM atlab, for each plantwe get the curve that reflects the
W, 和 ae ce of the variation of its steel tubes price to the total cost Comparing these curves, we
SN em ine forwhich plant, the variation of its’ steel tubes'price has the serbus influence to the
tal cost Asto the influences of the variations of the upper bound of the output of the steel
tube to the total cost and the strategy of ordering and transporting, we treat the problem in a
similarway In the case themain pipelines are in tree-shape，we assign a direction to each edge
of the tree and establish amodel sinilar to the model in the line-shape case
2 © 1994-2008 China Acade Journal Electronic Publishing House. All rights reserved 'www.cnki.net

