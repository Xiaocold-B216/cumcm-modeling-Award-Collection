# Extracted Paper

<!-- source_page: 1 -->

Sw
第 20 卷 第 7 期 工 程 数 学 学 报 Vol.20 No.7 2
2003 年 1 月 JOURNAL OF ENGINEERING MATHEMATICS De 200
一
文章 编号 :1005-3085(2003)07-0115-08

» N 1) HH
抢 渡 长 江 的 数学 模型
李 祥 镇 ， 何 秀珍 ， 朱 荣华 次
指导 老师 。 陈 雪 如 -NV
(集美 大 学 ,福建 厦门 361021) 2G \)
RE: 本 文物 再 思想 清晰 , 设 定 长 江 两 内 同 不 同 的 水 流速 度 分 布 和 法 江 二 由 asssss.
离散 化 数值 逼近 由 编程 实现 ,模拟 计算 完备 ,得 到 了 最 优 解 (AS
捕 要: 选手 在 “ 抢 流 长 江 "比赛 中 如 何以 最 短 的 时 间 顺 利 到 达 终 点 建 策 了 上 个 通用 的 约束 性 最 优 解 模型 。
考虑 一 般 的 情况 , 妈 小 沪 者 的 速度 U 、 游 肖 度 下 涨 流速 度 V 的 变化 规律 都 未 知 。 用 y 表
示 游泳 者 离 央 边 的 委 直 距离 ,把 U、0 均 看 作 关 于 2/ 阮 通 数 ,办 别 记 作 U(y) ,4(>) 。 本 文 所 给 出
的 幼 束 性 最 优化 模型 如 下 ;
. _ 1160 cd
minT 一 | SA 。
了 有 2 7 YA 1
在 模型 的 求解 中 ,为 了 辐 题 的 简化 * 委 六 U 一 定 , 即 滩 汪 者 始终 保持 小 站 的 这 度 恒定 。 将 江
面 的 宽度 作 细 分 , 记 每 上 和 。 设 在 任意 的 一 段 [y,y + 1) 中 ,游泳 者 的 角度 为 pi
- 1.2,，… 必 -1) .水 流通 度 为 沿 离 岸 边 距 离 的 线性 连续 函数 ; Vi(y) = po + g(i 12
-De 这 其， DY -VCD) -ww ，
#Hk 可 以 采用 拉 格 朗 日 条 件 极 值 的 求解 方法 和 二 分 法 来 求解 。 本 文中 我 们 利用
SG” 而 且 , 对 江面 宽度 所 作 的 细 分 y1,5;, y, 将 大 大 影响 到 模型 的 最 优 解 。 当
RELRARS , 即 前 分 越 细 时 ,模型 得 到 的 结果 越 优 。 对 于 问题 4 中 描述 的 水 流速 度 连续 变化 的
W, ,我 们 得 到 具体 的 结果 如 下
NY
的 段 数 n T sec) 的 段 救 n T( SEC 的 段 数 开 T SEC
3 891.4781 9 883.2587 1160 881.6862
关键 词 : 运动 的 分 解 ; 拉 格 朗 日 条 件 极 值 ;最 优 问 是
分 类 号 ; AMS(2000) 中 图 分 类 号 : 文献 标识 码 ; A
1 问题 的 重 述 ( 略 ) :
2 基本 假设
a 选手 在 抢 滤 过 程 中 的 状态 保持 良好 。 c: 把 选手 看 成 一 个 质点 。

<!-- source_page: 2 -->

116 工 程 数 学 学 报 第 20 着 =
b 不 考虑 当天 的 天 气 状况 对 选手 成 绩 的 影响 。 d: 假 设 资 渡 区 域 两 岸 平行 。
e 游 沪 者 的 绝对 速度 = 游泳 者 自身 的 游泳 速度 vi+ 水 流速 度 2。
3 符号 说 明
u 游泳 者 的 速度 大 小 0 #AERAFOERAFANEA
\% 长 江水 流 的 速度 大 小 H FAZAGERES
L 起 点 正 对 岸 到 终点 的 水 平 距离 U。 游泳 者 过度 在 水 流 方向 上 的 分 量
U, 游泳 者 速度 在 两 岸 重 直 方向 上 的 分 量 工 游泳 者 游 到 终点 总 共 所 用 的 时 间
了 在 验 直 两 岸 的 方向 上 距离 起 点 的 距离 四
SS
4 问题 的 分 析 和 模型 的 准备 2 \)
这 是 一 道 依据 物体 运动 的 合成 与 分 解 求 最 优 解 的 问题 。  rod
问题 ! 在 假设 成 立 的 前 提 下 ,由 于 0 1 保持 不 变 ,因此 质
点 在 水 平方 向 上 和 竖 直 方向 上 都 做 匀速 直线 运动 。 根 据 运 动 的 疹 鼎 : 质 点 的 合 运动 也 是 匀
速 直线 运动 。 由 于 第 一 名 游 流 者 顺利 到 达 了 终 占 ,所 [大 2002 取 比 赛 的 起 点 和 终点 都 是 他 运
动 轨迹 上 的 点 。 综 合 匀速 直线 运动 和 运动 委 迹 上 的 饥 作 可 号角 此 古 。
问题 2 在 问题 1 的 假设 下 , 游 沪 者 始终 以 和 岸 过 硬 吉 的 方向 游泳, 这 时 4 = r/2 。 因 此 游
泳 者 能 否 顺利 到 达 终 点 取决 于 U = 1.5 米 / 秒 ,9 = r/2 是 否 为 问题 1 几 个 等 式 的 公共 解 。1934
年 和 2002 和 的 人 数 分 5 磊 别 的 一 个 重要 原因 是 ;1934 年 和 2002 年 的 终点
不 同 。 由 于 终点 位 置 的 不 同 引起 了 水 人 Weern 因此 ,如 果 参 赛 者 仍然 按照 1934 年 的
参赛 者 的 路 线 必然 到 不 了 终点 。 假 设 参赛 者 在 不 同比 赛 中 的 速度 变化 不 是 很 大 , 则 影响 参赛 者
关外 有 择 的 游 瀛 方向 ( 即 9 的 大 小 )。
问题 3 和 4 当 问题 1 诗人 过 又
由 于 U.O、Y 三 个 人 让 人 人 本人 人 人
竖 直 方向 上 的 这 到 段 ,各 个 分 段 点 的 离 岸 位 移 依次 ym ,ya，…y% » BET—IE
上 we 再 根据 定理 : 作 直线 运动 的 质点 在 任意 时 刻 的
距 时 如 度 都 等于 他 移 对 时 间 的 一 阶 导 。 推 广 到 整个 范围 ,全 可 得 到 一 个 以 总 时 间 了 为 函数
“全 函数 等 式 。 再 以 水 平方 向 上 的 运动 为 约束 条 件 ,问题 3 和 问题 4 就 可 根据 一 个 目标 函
下 最 拓 角 模型 求解 。
5 模型 的 建立 与 模型 的 求解
首先 建立 一 个 直角 坐标 系 :以 起 点 为 原点 ,水 流 方向 为 x 轴 正 方向 ,起 点 垂直 到 对 岸 的
方向 为 y 轴 正 方向 。
问题 1 根据 候 设 的 条 件 和 问题 的 分 析 , 可 得 到 下 列 等 式 ;
在 水 平方 向 上 质点 的 运动 满足
L=(.89+U)XT (1)
在 竖 直方 向 上 质点 的 运动 满足
H=UXT (2)

<!-- source_page: 3 -->

第 7 期 抢 渡 长 江 的 数学 模型 117 并
根据 速度 的 正 交 分 解 可 得 :
U, = Ux co (3)
U, = UX sinf (4)

1. 对 于 2002 HEREARDHE—LEBLRAMIKETE: T = 848 秒

把 全 全 分 别 代 人 @@ 得 : 工 = (1.89 + U X cosf) x 848 H = U X sinf x 848

利用 MATLAB 求 解 ,得 出 : U = 1.5416 K/B  0 = 117.4558 度

2. 当 了 不 确定 时 , 联 立 (1) ~ (4) 式 可 得

工 _1L89+ Uxcog 1000
H U x sind 1160 _

由 已 知 条 件 可 得 : Ux (sinf -1.16 xcos6) = 2.1924 (6€(0,m)) _ 仅

因此 ,由 U >0 可 知 : sinf -1.16x cosg > 0=>rand > 1.16=>6 > 0 全 让

同时 ,对 于 LU、0 满足 的 三 = LELUE0l 丽 数 关系 利用 区 or
系 ,如 图 1 所 示 。 &v

3. 已 知 速 度 U = 1.5 米 /各 人

HHAEOQORDE: L = (1.89+1.5x cosd) » 4 Sxsind x 个

得 到 两 组 解 : b, = 121.8548F TI = 910.5 3 By =.156.6179 FF T, = 1948.6 #

因此 ， 游 泳 者 有 两 种 选择 。 但 T; 5 2 秒 。 因 此 游泳 者 应 选择 0 =
121.8548 度 。

问题 2 1 依据 前 而 的 分 析 可 希 ， 阅 题 1 和 问题 2 的 模型 荐 一 致 的 ， 此 时 0 = x/2 。
当 9 = x/20E, sinf = ro 代入 问题 1 中 所 建立 的 模型 求 得 U = 2.1924 米
ALT = 529 1 秒 。 所 以 只 有 当 洲 生 着 的 速度 达到 2 1924 米 /各 才 能 到 达 终 点 。 当 避 =
1.5 米 / 秒 时 ， 依 据 1160 = 15% 解 得 T = 773.3333 秒 。 当 T = 773.3333 秒 时 ， 游
SPOAIMTE  edol T = 1461.6 % >1000 米 。 因 此 当 U = 1.5 米 /
秒 时 ， 若 游泳 者 垂直 于 河源 游 ， 不 可 能 到 达 终点 。

2. eugpa) Vornak ios cusRRRS, 选手 们 往往 党 得 越 版 着 水
六 的 本 本人 全 但 选手 忽略 了 一 个 重要 因素 : 竖 直 方向 上 的 位 移 也 是
确定 的 在 埠 版 宕 水 沉 方向 游 时 ， 并 不 代表 就 能 在 最 短 时 则 内 到 达 对 岸 。 由 前 曾 问 题 中
:1 当世 = 1000 米 时 ,6 必须 在 (0.859337, x) 的 范围 内 ， 游 泳 者 才能 顺利 地
ARF 所 以 由 于 路 线 选择 的 错误 ， 很 多 选手 (特别 是 业余 选手 ) 被 冲 到 下 游 。 而
1934 年 9 在 (0.234133266 ，r) 范围 内 ， 很 明显 1934 年 6 的 范围 比 2002 年 6 的 范围 大
了 很 多 。( 如 图 2 所 示 )

进一步 推广 到 任意 的 ， 选 手 要 顺利 到 达 终点 满足 的 等 式 是 相同 的

了 _ 1L89+Uxcosg
五 U x sinf

BE—RAERL, BU0VIERHRRAN, B U.0 均 看 作 关于 y 的 函数 分 别
记 作 U(y) ,6(y) ， 但 在 整个 况 小 过 程 中 游泳 者 的 平均 速度 是 由 其 自身 的 素质 决定 的 。 同
时 ， 游 泳 者 由 于 受 自身 素质 的 限制 ， 游 泳 者 的 速度 总 不 会 超过 其 所 能 达到 的 最 大 游泳 速
度 。 设 U 为 游泳 者 的 平均 速度 ，M 为 游泳 者 所 能 达到 的 最 大 速度 。 因 此 ， 对 于 关于 y 的
函数 U 和 6 ， 它 们 有 如 下 的 限制 条 件 :

<!-- source_page: 4 -->

EliAl
E
118 工程 数学 学 报 第 20 着
BEIIITT L ER TL
“ B -
了 | fo i -
| 加 3
本 人
和
E | -:
本 人 :|
村 : 中 | 站
人 本
本 \ 2 人 品
人 _、 -3
-1
. 2
1160 】
上 Uldy &¢
0 nn 7  Qam, Do)SW NS
根据 微分 的 性 盾 有 :; dy = Usinbdt 一 必 = < 人
《-
因此 ， 模 型 的 目标 函数 ， os 7T-|
在 游 瀛 者 游 到 对 岸 时 ， 水 平方 向 上 的 位 移 达到 L 。 于 是 有 约束 条 件
6 VY(y) + Ucog _ oO
| Usinf 和 dy -人 OA
所 以 ， wa 束 性 最 优化 模型
. 1160 d
minT = | 上
5 国有 = 1000
了 而 付 ov as， 即 游泳 者 始终 保持 游 瀛 的 速度 恒定 。 将 江面 的 宽度
作 细 分 ， An 设 在 任意 的 一 段 [y ,ysi) 中 ， 游 瀛 者 的 角度 为 0(i =
1.2x 消 叶 - DJN 访 速 为 沿 高 岸 边 距离 的 线性 连续 函数
证 ¥)= py+ali=1,2,n —1),5 € [yiryin)
VOD mVG)  Vi) - Vi)
其 中 太一 Or17 站 Yo Yis1 T Yi
则 可 以 将 约束 条 件 转换 为
bi
a-t 1 “(yha 一 好 ) 十 Gy 一 ¥) 十 Ucosd; (ya 一 2)
2 Vily) + Do 2 _
| ， 人 人 = 100> 2 [7 =
1000
et BR  9D + a(inr — 3) + Ueodi( — 30)
令 8000-D = 之 一 000

<!-- source_page: 5 -->

了
第 7 其 抬 深 长 江 的 数学 模型 119 机
ev = S 人 dy _ $: Yis1 一半
re E
所 以 该 模型 转化 为
人
minf(61,8,,7,0,1)
根据 拉 格 朗 日 条 件 极 值 的 求法 ， 定 义 拉 格 朗 日 函数 上 = 三 + 1- 5, 为 常数 。
使 得 几 b1 ,6:,… ,2 -1) 取 到 最 小 什 的 必要 条 件 是 ; 2 = 0 = 12， 一 1)
这 样 就 得 到 (n - 1) 个 关于 6 WEH coy = 一 二 下 进而 可 以 求
1+ 1(8  + DA
出 sinb(i = 1,2,…, -1) 关 于 ?的 表达 式 。 7 “小
这 个 求解 过 程 ， 可 以 利用 二 分 法 或 其 它 方法 计算 。 在 此 我 们 乔 用 VC P + 编程 实 现 。
由 于 是 求解 一 元 方程 ， 所 以 当 ” 取 有 限 大 时 ， 都 可 以 保证 其 计算 昨 和 评 算 时 间 。 且 当 "
取信 越 大 时 ， 说 胃 考 永 的 情况 越 多 ， 了 的 值 越 会 楼 近 最 优 AS
下 面 就 可 以 利用 这 个 闪 型 分 别 解 次 了 问题 3 和 问题 44 |
问题 3 (1) 假设 UBKE. ) 在 整个 过 各 中 保 捷 不 变 。 这 时 原 方程 组 只 有 一 个 解 ，
不 存在 最 优 解 的 问题 。 由 约束 条 件 ， 氏
三 Yix) + Ueosh ay = 1000 = 1160U + cosd ~ 1000U ,sing+ 2191.6 = 0
所 以 当 U = 1.5 米 / 秒 时 ， = To1.7882 度 , T=909.8%
(2) 假设 U 为 常量 , n =4
约束 条 件 : |。 了 (0 = 1000
] = 一 7 .
此 时 ，y = 0,3, = 2 =960,5 = 1100  py= pr= ps= 0,q1= 1.4T.q =
2.11,q; = 1.47 一
模型 为 )
“ Vi + Ucost; Vi + Ucosh;
人 ， 0 dy - 1000 = 之 人 (ya-y)-1000=0
SN 册 本
AS\ 本 2 Ji 二 和
09) 一 2 [7 之 Usind
根据 前 面 一 般 模型 的 解法 ， 可 以 求 得 ; coxg; = 关 全- 世 (i = 1,2,0,0-1) ， 进 而 求
得 最 优 时 间 了 。
当 U = 1.5 米 / 秒 , wm = 4 时 通过 运行 程序 〔 源 程序 见 附录 Prog 1.c ) 求 得 的 最 优 值
为，
, = 126.051268 度 , 0, = 118.059889 度 ,， 6, = 126.051268 度 ，T = 903.987610 秒
这 说 明 游泳 者 在 前 200 米 的 游 沪 方 向 是 6， 中间 760 米 是 6; ， 后 面 200 米 是 b3 。
所 花 的 时 间 是 903.987610 秒 。
问题 4 也 是 模型 的 一 个 应 用 。 与 问题 3 -- 样 ， 分 两 种 情况 讨论 :
(1) 假设 U 为 常量 ,0 在 竞 湾 过 程 中 保持 不 变 ， 依 据 方程 组 可 以 求 出 唯一 的 解 。

<!-- source_page: 6 -->

口 | 到 口 |
EY
120 工 香 数 学 学 报 第 20 郑
了 Pagus = 1000 把 Y(y) 代入 到 上 式 约束 条 件 中 得 到 ;
当 U = 1.5 米 / 秒 时 , 求 出 9 = 121.5568 度 , T = 904.097229 秒
(2)》 假设 U 为 常量 ， 江 面 的 宽度 划分 为 - 工段 ， 每 段 上 角度 看 作 保持 不 变 。
@ 首 先 ， 取 ”= 4 的 方案 。
2.28
_ 2.28 _ 万 = 二 双全
= 生生 =0 3
o=0yy = 200,y; =960, = 1160 14” 20 性 各
-0 om =228 |，_ 2.28x1l60
91 93 200
刀 -1 n~1
. 了 1 dy _ Yiv1 T Mi 一
模型 为 ma pj| , Usindy ~ 之 Using -从 >
约束 条件 “外
呈 [ 7 gaa -ioon 2
i=17, Using; ?一 A
0
利用 一 般 模型 的 解 有 : cosbi = 人 -1)
L+[5 (ye + 3) + Ne
令 U =1.5 米 / 秒 ， 通 过 调用 程序 CBRITRMSEP ag2.c ) 解 得 :
0, 127. 36192 入 892. 4781
b2 114. 538623 工 单位 ，( 秒 )
3 127. 361936 @
SR 全
@ 进 一 步 ， 取 ，= 10 的 方案 。 兄 pFNY， =0.y, = 66,% = 132,y, = 200,y = 400,
y = 640,y; = 960,y8 = 1026, y, = 1083, yo = 1160
】 AT 2.28
万 1.2 ,3 = 228 ,6 二 0 加 .89 一 一 200
—o lgese=2.28 _ 2.28 x 1160
91,2,3 一 由 97,8,9 一 200
m, TonEfiE 让 Prog3.c ) 求解 得 到 :
路》 97 550940 b7 114. 988766
AR 5 SN。 122. 712537 Gs 121._76065
AS 115. 074804 0 135. 981494
N \ 6, 112. 455848 8557
05 112. 455848 工 位 ，( 弄
Og 112. 455848
图 进行 更 细 的 划分 ， 取 2” = 1161 ( 即 江面 被 划分 为 1160 段 )。 使 用 程序 Progd.c 求
解 。
此 时 ,yw = 工 - 1 。 则 可 以 将 游泳 者 游泳 的 角度 与 离开 岸 边 距 离 的 关系 如 图 4 所 示 。
从 以 上 两 种 情况 可 以 看 出 方案 四 比方 案 人 中 ， 游 泳 者 所 花 的 时 间 更 少 。
游泳 者 在 这 两 种 情况 下 的 游泳 轨迹 如 图 3 所 示 :

<!-- source_page: 7 -->

第 7 期 抢 滤 长 江 的 数学 模型 121 wasn
ET
TS 一
—
: ES
ETEEEEEEEESEEES SEE
ES
图 3 图 中 更 加 宠 曲 的 那 条 出线 是 方案 四 的 游 沪 路线 。 图 上 总 时 间 工 次 ah #)
6  FLISRIEJRESC kx H
从 十 至 今 ， meetAnoaTtabEageh 人 hraawaoan
好 的 策略 是 成 功 的 开始 。 俗 话说 :“ 知 己 知 彼 ， RUAAC, 庆生 好 的 策略 来 源 于 对 环境 的 充分
了 解 ， 对 一 名 渡 江 选手 来 说 也 不 例外 。 因 此 ， ss 选手 首先 必须 要 做 的 事 是 :
知已 = 了 解 自身 的 游 瀛 速度 ， 知 彼 = 明确 当天 比赛 时 外 i 速度 + 比赛 全 程 。 面 对 着 不 同 的 水
流速 度 和 比赛 路 线 ， 并 受 自身 游泳 速度 大 小 的 限制 ， 选 手 应 及 时 调整 游泳 的 方向 。
ns 首先 ， 选 手 必 须根 据
自身 特定 的 速度 ， 求 出 游泳 区 域 的 宽度 与 自身 游泳 速度 的 比值 和 水 平方 向 上 的 距离 与 水 流
速度 比值 。 如 果 前 者 的 比值 大 于 后 车 ， 5 只 能 选择 逆 游 ， 否 则 选手 将 会 被 水 流 冲 到 终点
的 下 游 。 接 着 ， 直达 选手 的 速度 越 大 ， 选 手 应 越 偏离 水 流 方
向 前 进 。 而 且 这 样 的 偏离 有 kr 这 个 特定 值 的 大 小 因 水 流 方向 上 距
离 的 变化 而 改变 ， 的 增 大 这 个 特定 值 会 减 小 。
7 和
_ NA 题 前 出 发 ， 分 析 了 应 该 考虑 的 各 种 情况 ， 建 立 了 一 般 的 数学 模型 ， 并 进行 理
ee 从 而 证 明 ， 我 们 建立 的 数学 模型 能 较 好 地 解决 问题 。
吡 寞 型 的 优点 在 于 模型 极为 广泛 的 使 用 性 ， 它 建立 的 前 提 条 件 对 U、V、0 三 者 没有 任
何 的 约束 。 对 每 一 个 具体 的 情况 ， 都 可 以 在 模型 中 求解 出 来 。
同时 ， 模 型 也 存在 着 一 些 缺 点 。 主 要 体现 在 : 四 对 整个 竞渡 阶段 的 细 分 是 由 人 为 因素
决定 的 ， 不 同 的 划分 会 得 到 不 同 的 最 优 解 ， 因 此 就 会 产生 误差 问题 。 四 在 论文 中 ， 求 解 都
是 在 假设 U 不 变 的 情形 下 进行 的 。 若 U 在 竞渡 过 程 中 时 刻 改变 ， 且 为 离 岸 垂直 距离 y 的
函数 ， 模 型 的 求解 将 会 变 得 很 复杂 ， 需 重新 编程 求解 。
8 模型 的 推广
我 们 建立 模型 的 方法 和 思想 对 其 它 类 似 的 问题 也 很 适用 ， 本 文 所 建立 的 模型 不 但 能 指
导 竞 渡 者 在 竞 度 比赛 中 如 何以 最 短 的 时 间 游 到 终点 ， 对 其 它 一 些 水 上 的 竞赛 也 具有 参考 意

<!-- source_page: 8 -->

是 刘
122 工程 数学 学 报 第 20 卷 7
II
义 。 例 如 : 皮 划 艇 比赛 和 飞机 降落 的 分 析 等 问题 。 此 外 还 能 对 一 些 远洋 航行 的 船只 的 路 线
规划 问题 给 予 指导 ， 使 船只 能 在 最 短 的 时 间 内 到 达 目 的 地 。
参考 文献 :
[1 王 沫 然 . MATLAB6， 0 与 科学 计算 [M]. 北京 ; 电子 工业 出 版 社 ，2001
[2] 。 薛 嘉 庆 ， 最 优化 原理 与 方法 [M]， 东北 : 治 金工 业 出 版 社 ，1991
{3] 。 陈 传 弄 ， 金 柱 临 ， 朱 学 炎 ， 欧 阳光 中 . 数学 分 析 [M]， 北京 ; 高 等 教育 出 版 社 ，1990
[4] ” 谭 举 强 ，C 语言 程序 设计 [M], 北京 : 清华 大 学 出 版 社 ，1999
一
-多 >
Mathematical Model of Swimming Across the Epu
全 /一
LI Xiang-zhen， HE Xiu-zhen， ZHU Rong-h 一
Advisor: CHEN Xue-juan
(Jimei University Xiamen Chi 他 )
X
Abstract: This paper establishes a common mathematical model 人 es a strategy to swim across the river
in the shortest time. The model divides the river into several segments and set the consumed time in swimming as
a target function. The restriction is that the distance in the horizontal direction should be the horizontal distance
between the jumping - off point and the destination” O 〇
For the most common situation, or of the swimmer, as the angle of the swimmer's di-
Tection against the bank and V as the velocity of thestream. Denote y as the vertical distance between the swim-
mer and the bank,and take U,6 "> of y and denoted as U(y) and 8(y). All the above could be sum-
11460 1
min T -|
marized as: | 6 ) + Up
2 沙 有 Te = 1100
In resolvi blem this paper assumes that U be invariable, which means the swimmer would swim
with the oo the competition. The width of the river is divided into little segments. Denote
过 ya yand in every segment [ 3; ,yi+1] :the angle of the swimmeris0(i = 1,2，
人 认 e velocity could be expressed as: Vi(y) = py +eg= 12 一 1)7E[yysnD
na
Lagrange conditional extremum theory and dichotomy are used to solve the above problem. VC+ +is also
used in realizing the method, What's more the division y,,2,**,, will highly affect the final result,the more
segments are divided the better result could be get. Under the assumption of question No. 4 this paper gets the fol-
lowing results:
The number of  |Best time: The number of  |Best time: The number of  |Best time:
L_— 3 — [eof4781[ 9 '[883.2587] 160 _ |881.6882]
Keywords: decomposition of movement; Lagrange conditional extremum thery; optimization

