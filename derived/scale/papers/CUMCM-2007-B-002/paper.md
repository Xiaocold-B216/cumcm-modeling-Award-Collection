# Extracted Paper

<!-- source_page: 1 -->

全
2007 高 教 社 杯 全 国 大 学 生 数学 建 模 竞赛
承 庶 书
我 们 仔细 阅读 了 中 国 大 学 生 数 学 建 模 竞赛 的 竞赛 规则
我 们 完全 明白 ， 在 竞赛 开始 后 参赛 队员 不 能 以 任何 方式 〈 和 包括 电话 、 电 子 邮
件 、 网 上 咨询 等 ) 与 队 外 的 任何 人 《包括 指导 教师 研究、 讨论 与 守 央 有 关 的 问
二
日 全 SS
四 z °\)
我 们 知道 ， 抄 效 别 人 的 成 果 是 违反 竞赛 规则 的 ， os
公开 的 资料 《包括 网 上 查 到 的 资料 )， 必 须 按照 规定 的 大考 文献 的 表述 方式 在 正
文 引用 处 和 参考 文献 中 明确 列 出 。 As ) \
RAGTRIE, PH 000, CORERIATE, ATH. 如 有 违反
竞赛 规则 的 行为 ， 我 们 将 受到 严肃 处 理 。 JS
) ©
我 们 参赛 选择 的 题 号 是 2 B
我 们 的 参赛 报名 号 为 如 果 多 没 置 报名 号 的 话 );
所 属 学 校 RS 区 人 6 重庆 大 学
参赛 从 员 (打印 并 答 特 | 1 能 国 刚
1 六 > 王 杰
\ Zn 3 黎明
指导 吕 了 指导 教 证 组 负责 人 (打印 并 答 针 和 二
R 日 期 ， 2007 年 9 月 21 日
赛区 评阅 编号 〈 由 赛区 组 委 会 评阅 前 进行 编号 ) :
1

<!-- source_page: 2 -->

Ee
2007 高 教 社 杯 全 国 大 学 生 数学 建 模 竞赛
编号 专用 页
赛区 评阅 编号 〈 由 赛区 组 委 会 评阅 前 进行 编号 ) : 次
ER
yA v
赛区 评阅 记录 所 可 供 赛区 评阅 时 使 用 ) : ] 于
阅 | |
人 <
2 、
|
0
备 2
_|
Y%
人 统一 编号 〈 由 赛区 组 委 会 送 交 全 国 前 编号 ) ;
R
全 国 评阅 编号 〈 由 全 国 组 委 会 评阅 前 进行 编号 ) :
2

<!-- source_page: 3 -->

EiiEE
乘 公交 ， 看 奥运
【摘要 了】 本文 要 解决 的 问题 是 以 即将 举行 的 08 年 北京 奥运 会 为 背景 而 提出 的 。
人 们 为 了 能 现场 观看 奥运 会 ,必然 会 面 对 出 行 方式 与 路 线 选 择 的 问题 。 因 此 如 何
快速 、 高 效 地 从 众多 可 行路 线 中 选 出 最 优 路 线 成 为 了 解决 此 问题 的 关键 。
鉴于 公交 系统 网 络 的 复杂 性 ， 我 们 没有 采用 常规 的 Dijkstra 算法 ， 而 采用 了
高 效 的 广度 优先 算法 。 其 基本 思想 是 从 经 过 起 〈 始 ) 点 的 路 线 出 发 ， 搜 寻 出 转 乘
次 数 不 超 过 两 次 的 可 行路 线 ， 然 后 对 可 行 解 进行 进一步 处 理 。 为 满足 不 同 查询 者
要 求 ， 我 们 对 三 个 问题 都 分 别 建立 了 以 时 间 、 转 乘 次 数 、 费 用 最 小 为 目标 的 优化
模型。
针对 问题 一 〈 只 考虑 公 汽 系统 )， 我 们 建立 了 模型 一 并 通过 na
了 任意 两 个 站 点 间 的 多 种 最 优 路 线 ， 并 得 出 所 求 站 点 间 最 优 路 线 的 最 就 秆 , 如 下
表 所 下: VAWD
出 发 站 S$S3359 | S1557 | S0971 008 [1sg 二 8 | S0087
1 | 1 1 | AKC / |
终点 站 S1828 | S0481 | S0485 CRN S3676
最 短 耗 时 min) | 64 | 406 | 106, |, 6 | 106 | 46 |
最 少 转 乘 次 数 "次 )| 1 | 2 | RAR2SL | 2 2
| 最 少 费用 (CO)- | 3 | 3 | BN] 2 | 3 | 3 |
模型 二 是 根据 问题 三 《同时 考虑 公 汽 和 地 铁 系 统 ) 建立 的 ， 同 样 用 VC++ 编
程 得 到 所 求 站 点 间 的 最 优 路 线 ， 如 下 表 上 所 未 :
出 发 站 $3359 /1,31557 中 S0971 | 0008 | S0148 | 50087
| | “hp | | | j
终点 站 sl8284 Gods1 | so4ss | S0073 | s04ss | sa676
最 短 耗 时 Cmin) | 和 | 106 ] 96 | 55 | 875 | 33 |
最 少 转 末 次 数 (次 ) | | 2 二 1 1 2 0
| 最 少 费用 Cs 3 | 3 | 3 | 2 | 3 | 3 |
对 问题 三 % b f 记 在) 我 们 建立 了 模型 三 的 优化 模型 ， 然 后 在 模型 改
进 里 又 建立 不 图 论 模型 。
本 六 汪 要 特点 在 丁 ， 所 用 算法 的 效率 十 分 显著 。 在 对 原始 数据 仅 做 简单 预
处 理 的 条 1 N 搜索 任意 站 点 间 的 最 优 路 线 所 需 的 平均 时 间 不 超过 0.5 秒 。 另 外 ，
人 所 建立 的 模型 简单 、 所 用 算法 比较 清晰 ， 易 于 程序 实现 ， 对 公交 线路 自主 查
和 saRA 夫 8 作用，
关键 字 : 转 乘 次 数 ”广度 优先 算法 查询 效率 实时 系统
3

<!-- source_page: 4 -->

一 问题 的 重 述

传承 华夏 五 千年 的 文明 ， 梦 圆 十 三 亿 华夏 儿女 的 畅想 ，2008 年 8 月 8 日 这
个 不 平凡 的 日 子 终于 离 我 们 越 来 越 近 了 ! 在 观看 奥运 的 众多 方式 之 中 , 现场 观看
无 疑 是 最 激动 人 心 的 。 为 了 迎接 2008 年 奥运 会 ， 北 京 公交 做 了 充分 的 准备 ， 首
都 的 公交 车 大 都 焕然 一 新 ， 增 强 了 交通 的 安全 性 和 舒适 性 ， 公 交 线路 已 达 800
条 以 上 ， 使 得 公众 的 出 行 更 加 通畅 、 便 利 。 但 同时 也 面临 多 条 线路 的 选择 问题 。
为 满足 公众 查询 公交 线路 的 选择 问题 , 某 公 司 准备 研制 开发 一 个 解决 公交 线路 先
择 问 题 的 自主 查询 计算 机 系统 。

这 个 系统 的 核心 是 线路 选择 的 模型 与 算法 ， 另 外 还 应 该 从 实际 情况 出 发 考
虑 ， 满 足 查询 者 的 各 种 不 同 需求 。 需 要 解决 的 问题 有 ， =
1、 仅 考虑 公 汽 线 路 ,给 出 任意 两 公 汽 站 点 之 间 线 路 选择 问题 的 一 般 救 号 借读 与
算法 。 并 根据 附录 数据 , 利用 模型 算法 , 求 出 以 下 6 对 起 始 站 到 终 到 站 右 佳 路 线 。
(1D)、S3359 一 S1828”/ (2)、S1557 一 S0481  (3). S097150485 7
(4). S0008—50073 (5)< S0148—S50485  (6). S0087—~S53676
2、 同 时 考虑 公 汽 与 地 铁 线路 解决 以 上 问题 。 7ASXK
3、 假 设 又 知道 所 有 站 点 之 间 的 步行 时 间 ， 请 你 给 出 性 意 页 站 点 之 问 线路 选择 问
题 的 数学 模型 。 汉

= BEUH
1， RAVUARERRT Bim1,2 ...10400,4 i<S20M, L 表示 上 行 公 汽 路 线 , 当
Le

i>S20 时 ， Ce
S，，: ee Hssane
T，: 第 j 条 地 钦 路 线 标 导 让 1.2

一 一”

D,,: 经 过 第 加 二 舌 线 路 的 第 个 地 铁 站 点 标 导

” 2A
Ls, : Km
光 择 第 k 种 路 线 的 总 时 间 ，
兴
NT 选择 第 k 种 路 线 公 汽 换 乘 公 汽 的 换 乘 次 数 ;
N2，: 选择 第 种 路 线 地 铁 换 乘 地 铁 的 换 乘 次 数 ;
N3, : 选择 第 种 路 线 地 铁 换 乘 公 汽 的 换 乘 次 数 ;
N4，: 选择 第 K 种 路 线 公 汽 换 乘 地 铁 的 换 乘 次 数 ;
W，。， 第 K 种 路 线 、 乘 坐 第 m 辆 公 汽 的 计 费 方式 ， 其 中 ，

4

<!-- source_page: 5 -->

下
村
WAR 一] 表示 实 行 单一 票 价 ，WK 一 2 表示 实行 分 段 计价 ;
CL,,¢ 第 k 种 路 线 ， 乘 坐 第 mm 辆 公 汽 的 费用
C， :选择 第 k 种 路 线 的 总 费用
MS，, :选择 第 k 种 路 线 ， 乘 坐 第 m 辆 公 汽 需要 经 过 的 公 汽 站 个 点 数 ;
MD , :选择 第 种 路 线 ， 乘 坐 第 mn 路 地 铁 需 要 经 过 的 地 铁 站 个 点 数 ;
FS，。: 表示 对 于 第 上 种 路 线 的 第 mm 路 公 汽 的 路 线 是 否 选择 步行， 葡 入
变量 ，FS。。 二 0 表示 不 选择 步行 ，
FD, ,: T 变量 ，
FD, =- 表示 不 选择 步行 ， me
9
= Ra
3.1 基本 假设
1、 相 邻 公 汽 站 平均 行驶 时 间 (包括 停 站 时 间 站 ，3 分 名
2、 相合 地 铁 着 下 均 行驶 时 间 (和 停 站 时 间 ): 2.5 分钟
3、 公 汽 换 乘 公 汽 平均 耗 时 :了 频 钟 ( 工 中 步行 时 间 2 分 名
4、 地 铁 换 乘 地铁 平 均 耗 时 :4 务 钴 (其中 步行 时 间 2 分 钟 )
5、 地 铁 换 乘 公 汽 平均 三 时 机 7 分 钟 (其 中 步行 时 间 4 分 钟
6、 公 汽 换 乘 地 铁 平均 :分 名 其 中 步行 时 间 4 分钟
7、 公 汽 票 价 ， 分 为 单 天 价 与 分 段 计 价 两 种 ;
单一 票 价 ，1W 全
sorgrfoinn 0 一 20 站 : 1 元
// 21~40 站 : 2 元
发 多
Ss3l 铁 京 价 ，3 元 (无论 地 铁 线路 问 是 否 换 乘 )
5 候 认同 一 地 铁 站 对 应 的 任意 两 个 公 汽 站 之 问 可 以 通过 地 铁 站 换 乘 ， 上 且 无 需 支
1
3.2 其 它 假设
10、 查 询 者 转 乘 公交 的 次 数 不 超 过 两 次 ;
11、 所 有 环行 公交 线路 都 是 双向 的 ;
12、 地 铁 线 T2 也 是 双向 环行 的 ;
13、 各 公交 车 都 运行 正常 ， 不 会 发 生 堵车 现象
14、 公 交 、 列 车 均 到 站 停车
四 问题 的 分 析
5

<!-- source_page: 6 -->

EEEE
在 北京 举行 奥运 会 期 间 , 公众 如 何在 众多 的 交通 路 线 中 选择 最 优 乘 车 路 线 或
转 乘 路 线 去 看 奥运 ， 这 是 我 们 要 解决 的 核心 问题 。 针 对 此 问题 ， 我 们 考虑 从 公交
线路 的 角度 来 寻求 最 优 线路 。 首 先 找 出 过 任意 两 站 点 《公众 所 在 地 与 奥运 场地 )
的 所 有 路 线 , 将 其 存储 起 来 , 形成 数据 文件 。 这 些 路 线 可 能 包含 有 直达 公交 线路 ，
也 有 可 能 是 两 条 公交 线路 通过 交汇 而 形成 的 〈 此 时 需要 转 乘 公 交 一 次 )， 甚 至 更
多 公交 线路 交汇 而 成 。 然 后 在 这 些 可 行路 线 中 搜寻 最 优 路 线 。
对 于 路 线 的 评价 , 我 们 可 以 分 别 以 总 行程 时 间 , 总 转 乘 次 数 , 总 费用 为 指标 ，
也 可 以 将 三 种 指标 标准 化 后 赋 以 不 同 权 值 形成 一 个 综合 指标 。 而 最 优 路 线 则 应 是
总 行程 时 间 最 短 ， 总 费用 最 少 或 总 转 乘 次 数 最 少 ， 或 者 三 者 此 有 之 。 之 所 以 这 样
考虑 目标 ， 是 因为 对 于 不 同年 龄 阶段 的 查询 者 ， 他 们 追求 的 目标 会 有 所 不 同 ， 比
如 青年 人 比较 热衷 于 比赛 ， 因 而 他 们 会 选择 最 短 时 间 内 到 达 奥 运 赛 场 观看 比赛 。
而 中 年 人 则 可 能 较 倾 向 于 综合 指标 最 小 ， 即 较 快 、 较 省 ， 转 乘 次 数 不 多 。 老年
人 总 愿意 以 最 省 的 方式 看 到 奥运 比赛 。 而 对 于 残疾 人 士 则 总 转 乘 ; H 最 少 为 好 。
不 同 的 路 线 查 询 需 求 用 图 4. 1 表示 如 下 : 2XG \)
人
hh
AeX
图 4. 1 公交 线路 查询 目标 图
经 分 析 ， 过 的 可 和 人 个 求 最 短路 径 的 问题 ， 但 是 传统 的 Dijkstra
最 短路 径 算 法 并 不 适用 于 本 总 B Ds 和 的 人 和 让
难以 应 付 公 交 线 路 网 络 拓扑 的 复 Ht) 而 且 由 于 执行 效率 的 问题 ， 其 很 难 满足 实
时 系统 对 时 间 的 严格 要 求法
BEBEATRWENTE 采用 了 效率 高 效 得 广度 优先 算法 ， 其 基本 思
路 是 每 次 搜索 指定 点 sz7 并 将 其 所 有 未 访问 过 的 近邻 点 加 入 搜索 队列 ,循环 搜索 过
0 全
_ 五 建 模 前 的 准备
为 靖 多 shair 的 7 他 在 建立 此 模型 前 ”我 们 有 必要 做 一 些 准 备
ERA ，
于 民 数 据 的 存 依
SN 由 于 所 给 的 数据 格式 不 是 很 规范 , 我 们 需要 将 其 处 理 成 我 们 需要 的 数据 存储
格式 。 从 所 给 文件 中 读 出 线路 上 的 站 点 信息 ， 存 入 txt 文档 中 ， 其 存储 格式 为 :
两 行 数据 ， 第 一 行 表示 上 行 线 上 的 站 点 信息 ， 第 二 行 表 示 下 行 线 的 站 点 信息 ， 其
中 下 行路 线 标号 需要 在 原 标 号 的 基础 上 加 上 520， 用 以 区 分 上 行 线 和 下 行 线 。
如 果 上 行 线 与 下 行 线 的 站 点 名 不 完全 相同 , 那么 存储 的 两 行 数据 相应 的 不 完
全 相同 ， 以 公交 线 L009 为 例 ;
1L009:3739 0359 1477 2159 2377 2211 2482 2480 3439 1920 1921 0180 2020
3027 2981
1.529:2981 3027 2020 0180 1921 1920 3439 3440 2482 2211 2377 2159 1478
6

<!-- source_page: 7 -->

本
国 呈 RN
0359 3739
1529 为 L009 所 对 应 的 下 行 线路 。
如 果 下 行 线 是 上 行 线 原 路 返回 , 那么 存储 的 两 行 数据 中 的 站 点 信息 刚好 顺序
颠倒 ， 以 公交 线路 L001 为 例 :
L001:0619 1914 0388 0348 0392 0429 0436 3885 3612 0819 3524 0820 3914
0128 0710
L521:0710 0128 3914 0820 3524 0819 3612 3885 0436 0429 0392 0348 0388
1914 0619
如 果 是 环线 的 情况 〈 如 图 5. 1 所 示 )， 则 可 以 等 效 为 两 条 线路 :
顺 时 针 方向 : S1 一 S$2 一 S3 一 S4 一 S1 一 S2 一 S3 一 S4;
逆 时 针 方向 : S1 一 S4 一 S3 一 S2 一 S1 一 S4 一 S3 一 S2。
经 过 分 析 ， 此 两 条 ”单行 路 线 ” 线 路 的 作用 等 同 于 原 环形 路 线 % >
S2 ° W
2XA
从 A
f &
S1 As NS
和 4
<
图 5.1 环行 线路 示意 图
以 环形 公交 线 L158 为 例 ， 下 于 形 路 线 存储 数 据 如 下 ，
L153: 534 649 2355 1212 WA 811 2600 172 1585 814 264 3513 1215
1217 251 2604 2606"534-649 2355 1212 812 171 170 811 2600 172
1585 814 264 35] 3 1215 1217 251 2604 2606
L673: 534 2606 2604125) 217 1215 3513 264 814 1585 172 2600 811 170
171 812.1212 2355 649 534 2606 2604 251 1217 1215 3513 264 814
1585 和 人 811 170 171 812 1212 2355 649
在 这 里 ,153 被 看 作成 上 行路 线 ，L673 被 当成 下 行路 线 。 这 样 对 于 每 条 公交
线路 都 人
5. : 23eiln 个 站 点 的 公交 路 线
< 处理 5. 所 得 信息 ， 找 出 通过 每 个 站 点 的 所 有 公交 路 线 ， 并 将 它们 存 入 数据
Selery
PNBil, SEE F A Ze 3  S0001 的 线路 和 经 过 站 点 S0002 的 线路 如 下 :
经 过 S0001 的 线路 有 : L421
经 过 S0002 的 线路 有 : L027 L152 L365 L395 1.485
5. 3 统计 任意 两 条 公交 线路 的 相交 〈 相 近 ) 站 点
依次 统计 出 任意 两 条 公交 线路 之 间 相交 (相近 ) 的 站 点 ， 将 其 存 入 1040X
1040 的 矩阵 A 中 ， 但 是 这 个 矩阵 的 元 素 是 维 数 不 确 定 的 向 量 ， 具 体 实现 的 时 候
可 以 将 用 队列 表示 。
例如 :公交 线路 L001 与 公交 线路 L025 相交 的 站 点 为 ALI] [25]= {S0619，
S1914, S0388, S0348}.
7

<!-- source_page: 8 -->

Ee
六 模型 的 建立 与 求解
6.1 模型 一 的 建立
该 模型 针对 间 题 一 , 仅 考虑 公 汽 线路 , 先 找 出 经 过 任意 两 个 公 汽 站 点 $，, 与
$ ;最 多 转 乘 两 次 公 汽 的 路 线 , 然后 再 根据 不 同 查询 者 的 需求 搜寻 出 最 优 路 线 。
6. 1. 1 公 汽 路 线 的 数学 表示
任意 两 个 站 点 间 的 路 线 有 多 种 情况 ,如果 最 多 允许 换 乘 两 次 , 则 换 乘 路 线 分
别 对 应 图 6. 1 的 四 种 情况 。 该 图 中 的 A、B 为 出 发 站 和 终点 站 ，C、 % F 为 转
乘 站 点 。 = ks
D D 全 &, \)
/ 人 下放
> ”ASK  /
(a) o 个， 和
图 6441 从
对 于 任意 两 个 公 汽 站 点 $，, 与 8 ,  LHS ,的 公 汽 线路 表示 为 1 ， 有
SeeLi 经 过 $ 。， 的 公 汽 线路 表示 洪 [ ;有 S。。 EL
， ) D 7 0 1 名 i
1) 直达 的 路 线 LS，( 如 图 6. 人 Jr 表示 为 ;
SEE 5
Sus
2) 转 乘 一 次 的 路 线 E! 和 6.1 (b) 所 示 ) 表示 为 ;
也 产
于 EPE 有 于 ER:
/ = 了 三
xd [的 一 个 交点 ;
忆 R-
人 责 次 的 路 线 LS，( 如 图 6. 1 (ec) 所 示 ) 表示 为 :
通过 以 上 转 乘 路 线 的 建 模 过 程 ， 可 以 看 出 不 同 转 乘 次 数 间 可 作成 迭代 关系 ，
进而 对 更 多 转 乘 次 数 的 路 线 进行 求 寻 。 不 过 考虑 到 实际 情况 , 转 乘 次 数 以 不 超过
2 次 为 佳 ， 所 以 本 文 未 对 转 乘 三 次 及 三 次 以 上 的 情形 做 讨论 。
6. 1. 2 最 优 路 线 模型 的 建立
找 出 了 任意 两 个 公 汽 站 点 间 的 可 行路 线 , 就 可 以 对 这 些 路 线 按 不 同 需求 进行
8

<!-- source_page: 9 -->

你
选择 ， 找 出 最 优 路 线 了 :
1) 以 时 间 最 短 作 为 最 优 路 线 的 模型 ; 行程 时 间 T, 等 于 乘 车 时 间 与 转车 时 间 之 和 。
¥
Ti 下 全 9 下 (61 式 )
ma2geN H: ke12aaR
其 中 ， 第 K 路 线 是 以 上 转 乘 路 线 中 的 一 种 或 几 种 。
2) 以 转 乘 次 数 最 少 作 为 最 优 路 线 的 模型 ，
Min N (6.2 式 )
此 模型 等 效 为 以 上 转 乘 路 线 按 直达 、 转 乘 一 次 、 两 次 的 优先 次 友 米 必 人
3) 以 费用 最 少 作为 最 优 路 线 的 模型 ， = LkK2
Ni Can- 7 \b3 3)
1 AR ERN20N, 一
Hf, as= 2 WNr=2. 2=NFR, —=0)\ (6.4 式 )
3 As -Da 人 |
6. 1. 3 模型 的 算法 描述 2
针对 该 问题 的 优化 模型 ,我 们 采用 广度 优 锋 侈 法 技 出 任意 两 个 站 点 间 的 可 行
路 线 , 然后 搜索 出 最 优 路 线 。 现 将 此 算法 运用 到 该 问题 中 , 结合 图 6. 2 叙述 如 下 :
(该 图 中 的 9 ，、$ ，， 5 人 3， 、@， 表 示 公 汽 站 点 ，L DLL、
i,8 AH [e)
1，、L， 表示 公 汽 线路 。 其 中 AAA (o) 图 分 别 表 示 了 从 点 S，, 到 点 8$ ，, 直
达 、 转 乘 一 次 、 转 乘 两 吹 的 俏 况 )
|
一 vv ER
il0AJR si
和 LS 1 所 5
i 谎 - (a) ®) T4 (c) Ls
图 6. 2 公交 直达 、 转 乘 图
1) 首先 输入 需要 查询 的 两 个 站 点 $，, 与 $ ，，( 假 设 $，, 为 起 始 站 ，$ 。，
为 终点 站 );
(2) 搜索 出 经 过 $ ,的 公 汽 线路 !， (=12,…,m) 和 经 过 $ ，， 的 公 汽 线路
1 (1 =12, …， 上 四， 存 入 数据 文件 ， 判 断 是 !， 与 L 是 耕 存 在 相同 路 线 ， 若
9

<!-- source_page: 10 -->

你
有 则 站 点 $ ，, 与 $ 。; 之 间 有 直达 路 线 (如 图 6. 2 中 的 !,) ， 则 该 路 线 是 换 冬 次数
最 少 ( 换 乘 次 数 等 于 0) 的 路 线 ， 若 有 多 条 直达 路 线 ， 则 可 以 在 此 基础 上 找 出 时 间
最 省 的 路 线 ， 这 样 可 以 找 出 所 有 直达 路 线 ， 存 入 数据 文件 ;

(3) 找 出 经 过 $ ，, 的 公 汽 线路 !，( 如 图 6. 2 中 的 1 ) 中 的 另 一 站 点 Si 。 和 经
过 8 ，， 的 公 汽 线路 T ， 中 的 另 一 站 点 $ 4 。 判断 S，。 与 8 4 ii 中 是 否 存在 相
同 的 点 ， 着 存在 (如 图 6. 2 中 的 $，) 则 站 点 $，, 与 8 。; 间 有 一 次 换 冬 的 路 线 (如
图 6. 2 中 的 1 , 与 !, ) ， 该 相同 点 即 为 换 乘 站 点 ; 0T 存
入 数据 文件 ; =

(4) 再 搜索 出 经 过 (如 图 6.2 的 1 全 上 除了 六 内
RS
的 其 他 站 点 SG JURT, TISRS 。 sy 与 经 过 8 本 RN ， 中 的 其 他 站 点
S ;io 存在 相同 的 页 (如 图 6. 2 中 的 Si RS 4 ; 间 有 二 次 换 乘 的 路 线
(如 图 6. 2 中 的 L，、1 <) ， 该 相同 点 和 点 8$55 是 换 乘 站 点 ! 将 此 二 次 换 乘 的

Le
路 线 存 入 数据 文件 中 HA ©

(5) 区、 4 ; 的 不 同 路 线 ， 根 据 不 同 模型 进
行 最 优 路 线 进 行 搜索 ， 基 包 香 询 者 满意 的 最 优 路 线 。

6，1. 4 模型 一 的 求解 |_|

根据 以 上 算法 和 六 面 星 上 的 模型 一， 用 VCi+ 进 行 编程 (程序 见 附录 ) 就 可
以 得 出 不 同 目标 亚 的 最 优 路 线 。

1) 以 耗 时 最 少 溪 目 标的 最 优 路 线
起 始 站 $3359/ 到 终 到 站 S1828 耗 时 最 少 为 64 min， 耗 时 最 少 的 最 优 路 线 〈 转 乘
交办 MK 有 28 条 ( 注 ， 表 6.1 选择 了 其 中 的 10 条 表示 ) ;
思 始 请 S1557 到 终 到 站 S0481 耗 时 最 少 为 106 min, 耗 时 最 少 的 最 优 路 线 有 2 条 ;
RQUAAE 50071 到 终 到 站 S0485 耗 时 最 少 为 106 min 耗 时 最 少 的 最 优 路 线 有 2 条 ;
PA3A S0008 到 终 到 站 S0073 耗 时 最 少 为 67 min， 耗 时 最 少 的 最 优 路 线 有 2 条 ;
起 始 站 S0148 到 终 到 站 S0485 耗 时 最 少 为 106 min, 耗 时 最 少 的 最 优 路 线 有 3 条 ;
起 始 站 S0087 到 终 到 站 S3676 耗 时 最 少 为 46 min, 耗 时 最 少 的 最 优 路 线 有 12 条 ;
其 耗 时 最 少 的 最 优 路 线 如 表 6. 1 所 示 。

表 6.1 耗 时 最 少 的 最 优 路 线 表
起 娩 | ARE INeT 公 汽 线 | 终 到 | B | 所 需
站 | 路 路 路 | 站 | 次 数 | 费用
| S3359 |10535 | S2903 |L1005 | S1784 | L0687 [S1s28 | 2 | 3 |
1S3359 |10535 | S2903 [L1005 | S1784 [L0737 |Sl828 | 2 | 3 |
10

<!-- source_page: 11 -->

EygaE
| S3359 |L0123 [$2903 [L1005 [S1784 [L0687 [s1828 | 2 | 3 |
| S3359 | L0123 | S2903 |L1005 | S1784 |L0737 |Sl828 | 2 | 3 |
| S3359 |L0652 | S2903 [L1005 [S1784 |L0687 |Sl828 | 2 | 3 |
| S3359 |L0652 | S2903 |L1005 | S1784 |L0737 |Sl828 | 2 | 3 |
| S3359 | L0844 “| S2027 |L1005 | S1784 |L0687 |Sl828 | 2 | 3 |
| S3359 [L0844 [S2027 [L1005 [S1784 |L0737 |Sl828 | 2 | 3 |
| S3359 [L0844 [S1746 |L1005 |S1784 |L0687 [S1828 | 2 | 3 |
| S3359 [L0844 [S1746 |L1005 |S1784 [L0737 |Sl828 | 2 | 3 |
| S1557 |L0604 |S1919 [10709 | S3186 |L0980 | SO481 | 2 | 3 |
| S1557 | L0883 [S1919 [L0709 | S3186 [L0980 [S0481 | 2 | 3 |
| S0971 [L0533 | S2517 |L0810 | S2480 [L0937 |S0485 | 2 ,| 3 |
| S0008 | L0198 |$3766 | L0296 “| S2184 | 10345 [S0073 | 2VSS 3 |
| S0008 | L0198 | S3766 [10296 [S2184 | L0345 [S00737], 2 | 3 |
| S0087 | L0541 | S0088 | L0231 -| S0427 | LQ097 下 S8676 | 2 | 3 |
| S0087 | L0541 | S0088 |L0901 |S0427 | JIog2 |S3676 | 2 | 3 |
| S0087 | L0206 “| S0088 |L0231 |S0427 [LO097 [S3676 | 2 | 3 |
| S0087 | L0206 “| S0088 [10231 | S0427 |L0982 [S3676 | 2 | 3 |
| S0087 | L0206 “| S0088 | L09017 JS0427 |L0982 |S3676 | 2 | 3 |
| S0087 | L0974 | S0088<| L0231 | S0427 | L0982 |S3676 | 2 | 3 |

二

2) oa 目标 的 最 优 路 线

起 始 站 88359 到 终 到 站 S1828 的 最 少 转 乘 次 数 为 1 次 , 转 乘 次 数 最 少 的 最 优
路 线 J 所 震 计 间 较 短 ， 费 用 较 省 的 路 线 ) 有 2 条 ;
] 芭 抬 站 S1557 到 终 到 站 S0481 的 最 少 转 乘 次 数 为 2 次 , 转 乘 次 数 最 少 的 最 优
2 条 是 的 地 做 线 (表示 在 表 6. 1 中 ， 下 同 );

忆 始 站 S0971 到 终 到 站 S0485 的 最 少 转 乘 次 数 为 1 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 1 条 ;

起 始 站 S0008 到 终 到 站 S0073 的 最 少 转 乘 次 数 为 1 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 9 条;

起 始 站 S0148 到 终 到 站 S0485 的 最 少 转 乘 次 数 为 2 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 3 条 与 耗 时 最 少 的 最 优 路 线 相同 ;

起 始 站 S0087 到 终 到 站 S3676 的 最 少 转 乘 次 数 为 2 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 6 条 与 耗 时 最 少 的 最 优 路 线 相同 ;

11

<!-- source_page: 12 -->

各

其 余 转 乘 次 数 最 少 的 最 优 路 线路 线 如 表 6. 2 所 示 。

表 6.2” 转 乘 次 数 最 少 的 最 优 路 线 表

| 起 始 站 | 公 汽 线路 | 中 转 站 | 公 汽 线路 | 终 到 站 | 耗 时 | B  |

| S3359 | L0956 [S1784 | L0687 [S1828 | 101 | 3 |

| S3359 |L0956 | S1784 [10737 |S1828 | 101| 3 |

| S0971 |L0533 | S2184 | L0937 |S0485 | 128 | 3 |

| S0008 |L0679 [S0291 |L0578 [s0073 | 83 | 2 |

| S0008 |L0679 | S0491 |L0578 |S003 | 83 | 2 |

| S0008 |L0679 |S2559 |L0578 |S003 | 83 | 2 |

| S0008 |L0679 | S2683 |L0578 |S003 | 83 | 2 |

| S0008 |L0679 | S3614 |L0578 |S0073 | 83 | 2 。 |

| S0008 |L0875 | S2263 | L0345 | S0073 | 83 | 247,

| S0008 | L0875. 一 | S2303 | L0345 | S0073 | 83 | 2

| S0008 |L0875 一 | S3917 | L0345  [50073 | 8 人 = 2 |

| S0008 | L0983 一 | S2083 | L0057 [s0073 | 83J 2 |

3) 以 忱 用 最 少 为 目标 的 最 优 路 线 &r“/)

起 始 站 $3359 到 终 到 站 S1828 有 天生 全 人 全
需 时 间 较 短 ,/ 转 滋 次 数 较 少 的 路 线 ) 有 30, 条 , 其 中 28 区 路 线 所 需 时 间 为 6 mim，
转 乘 次 数 为 2 次 ;另外 两 条 路 线 所 需 时 间 为 CR 转 乘 次 数 为 1 次 ;

起 始 站 S1557 到 终 到 站 S0481 0 外， 最 少 费 用 的 最 优 路 线 有 2
条 ， 所 需 时 间 为 106 miny 转 乘 次 数 为 2 次 fj SS

起 始 站 $0971 到 终 到 站 :80485 的 最 少 费用 为 3 元 ,最少 费用 的 最 优 路 线 有 3
条 ,其 中 两 条 所 需 时 间 为 106wiin 转 乘 况 数 为 2 次 , 另外 一 条 所 需 时 间 为 128 min，
转 乘 次 数 为 1 次 ; 3/

起 始 站 S0008 到 终 到 站 :人 3 多 最 少 费用 为 2 元 ， 最 少 费用 的 最 优 路 线 有 8
条 ， 所 需 时 间 为 83 ming SERVCH 1 次 ;
ms 最 少 费 用 的 最 优 路 线 有 3 条 ，
所 需 时 间 为 106min， 转 轨 次 数 为 2 次 ;

起 始 站 S0087 到 终 到 站 S3676 的 最 少 费用 为 -3 元 ， 最 少 费用 的 最 优 路 线 有
12 条 ， 所 有 时 人 Fi 转 乘 次 数 为 2 次 ;

最 少 咒 用 的 最 优 路 线 表示 在 表 6. 1 和 表 6.2 中
6. 2. 了 模型 瑟 的 建立

寻访 模型 人 涌 问 题 二 ， 将 公 汽 与 地 铁 同时 考虑 ， 找 出 可 行路 线 ， 然 后 寻找 最 优
这 。 和 地 亿 线 路 ， 也 可 以 将 其 作为 公交 线路， 本 质 上 没有 什么 区 别 ， 只 不 过
民企 费用 、 时 间 ， 换 乘 时 间 不 一 样 村 了 。 因 此 地 铁 站 可 等 效 为 公交 站 ， 地 铁 和 公
次 的 转 乘 站 即 可 作为 两 者 的 交汇 点 。 因 此 该 模型 的 公交 换 乘 路 线 模型 与 模型 一 中
的 基本 相同 。 现 建立 模型 二 下 的 最 优 路 线 模型 。

1) 以 时 间 最 短 的 路 线 作为 最 优 路 线 的 横 型 ， 可 行路 线 的 总 时 间 为 乘 公交 〈 公 汽
和 地 铁 ) 时 间 与 公 汽 与 地 铁 换 乘 、 公 汽 间 、 地 铁 间 换 乘 时 间 之 和 。
Ta 工 耻 他 三 区
1 二 06.5 式 )
其 中 ， 第 上 路 线 为 同时 考虑 公 汽 与 地 铁 的 转 乘 路 线 中 的 一 种 或 几 种 。
2) 以 转 乘 次 数 最 少 的 路 线 作为 最 优 路 线 的 模型
12

<!-- source_page: 13 -->

Eli
y u
mEEE
TNxR T PS3, TF 《6.6 式 )

此 模型 等 效 为 以 上 转 乘 路 线 按 直达 、 转 乘 一 次 、 两 次 (包括 公交 与 地 铁 间 的 转 乘 )

的 优先 次 序 来 考虑 。

3) 以 费用 最 少 的 路 线 作 为 最 优 路 线 的 模型 ;可 行路 线 的 费用 为 乘 公交 和 地 铁 费

用 的 总 和 。

NhES 4 > 到 (6.7 式 )

其 中 ，CL。。 仍 满足 (6.4 式 )。

6. 2.，2 模型 二 的 求解

不 难 发 现 ， 问 题 一 是 问题 二 解 的 一 部 分 。 在 问题 二 中 ， 新 产生 天 从 人 多 主

要 源 于 在 通过 换 乘 地 铁 * 换 乘 附近 相近 站 点 的 路 线 上 ， 如 下 图 所 亲 : LS
31 Se \!
L4 ? 地) 下
四 5 i2 b 要
入 3 二 一。 LN Li A CA 3 二
Lil S1 A 工 这 T 种 KK SS Lij
(a) (b) 1 [5] ”

从 点 A 到 B， 站 才 示 的 是 通信 人 和 xi S1, S2 进行 一 次
转 乘 ; 图 (b) 表示 利用 地 铁 站 进行 二 次 转 乘 , 图 (时 表示 利用 另 一 条 公 汽 路 线 为 中
介 进 行 二 次 转 乘 。

铁路 线路 引入 给 题目 的 求解 增加 了 难度 ,为 了 形象 了 解 为 数 不 多 的 两 条 铁路
间 的 交叉 关系 ， 我 们 通过 maligh g 呈 《〈 程 序 见 附录 ) 作出 了 两 条 铁路 的 位 置 关
系 图 ， 如 图 6. 3 所 示 。 (A

钱 示 站 图
10 =
8 ) = 一
< 二 = ¥ 29 30
4 8 3
V
从
9 123 4567 89 1011121314151617 181920212223
下 2 旨
W, -4 25 i4
N = 2
-8
0 0 5 10 15 20 25 30 35 40 45 50
图 6.3 TIl 与 T2 铁路 位 置 关系 图
注 : 图 四 中 的 直线 表示 T1 铁路 线 ， 圆 表示 T2 铁路 线 ， 数 值 表示 站 点 ， 例 如 1
表示 T1 铁路 线 上 的 D1 铁路 站 ，26 表示 T2 铁路 线 上 的 D26 铁路 站 。 此 图 与 网 上
查询 到 的 北京 地 铁 示 意图 〈 如 图 6.4 所 示 ) 相 吻 合 。
13

<!-- source_page: 14 -->

加
隐 人
北京 地 铁 示意 图 和 人 和 m
西直门 ( 东直门
车 公庄 (1 本 GD 东 四 十 条
时 提成 门 ©% 人 和 . QERN
§ UaOsOaOaCOaCOaCOaCOCODC — CmOmOm Om(O)
EiEaE FizrE
图 6. 4 北京 地 铁 示 意图
2
函数 分 别 用 模型 二 建立 的 模型 表达 式 表达 ， 用 VCi+ 进 行 编程 〈 程 序 划 9 求
得 出 考虑 地 铁 情况 的 最 优 路 线 。 -AN
1) 以 转 乘 次 数 最 少 为 目标 的 最 优 路 线 x b
起 始 站 S0008 到 终 到 站 -S0073 的 最 少 转 乘 次 数 为 1 次 , SERYCHU  fyJett
路 线 有 1 条; 1
起 始 站 S0087 到 终 到 站 '$S3676 A N- 直达
下 的 最 优 路 线 有 了 条 ，
起 始 站 S0148 到 终 到 站 S0485 的 最 少 转 乘 次 疼 为 2 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 10 条 ; AS
起 始 站 S0971 到 终 到 熙 $0485 的 最 少 转 乘 次 数 为 2 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 20 条 〈 注 表 6. 不 中 罗列 其 中 10 杀 );
起 始 站 $1557 到 终 到 站 80481 的 最 少 转 乘 次 数 为 2 次 , 转 乘 次 数 最 少 的 最 优
路 线 有 17 条 〈 注 表 6.4 1 有
起 始 站 S3359 到 终 到 站 S1628 的 最 少 转 乘 次 数 为 2 次, 转 乘 次 数 最 少 的 最 优
路 线 有 2 条 。
2) 以 耗 时 最 少 为 目 人
起 始 站 S3359. 到 终 到 站 S1828 耗 时 最 少 为 6tmin， 耗 时 最 少 的 最 优 路 线 ( 转
乘 次 数 较 少 ， 2 有 :28 条 ( 注 , 表 6)1 选择 了 其 中 的 10 条 表示 ) 5
的 0155 到 作 到 站 S0481 耗 时 最 少 为 109 mim， 耗 时 最 少 的 最 优 路 线 有
17 条 与 |
.起 始 站 $0971 到 终 到 站 S0485 耗 时 最 少 为 96 min; 耗 时 最 少 的 最 优 路 线 有
20 条 息 转 芍 次 数 最 少 的 最 优 路 线 相同 ，
村 /起 始 政 50008 到 终 到 站 S0073 耗 时 最 少 为 55 min， 耗 时 最 少 的 最 优 路 线 有 3
AN S0148 到 终 到 站 S0485 耗 时 最 少 为 87.5 min， 耗 时 最 少 的 最 优 路 线
有 10 条 与 转 乘 次 数 最 少 的 最 优 路 线 相同 ;
起 始 站 S0087 到 终 到 站 S3676 耗 时 最 少 为 33 min， 耗 时 最 少 的 最 优 路 线 有 1
条 与 转 乘 次 数 最 少 的 最 优 路 线 相同 ，
3) 最 少 费用 的 最 优 路 线
起 始 站 $3359 到 终 到 站 S1828 的 最 少 费 用 为 3 元 ,最 少 费 用 的 最 优 路 线 (所
需 时 间 较 短 ， 转 乘 次 数 较 少 的 路 线 ) 有 2 条 ;
起 始 站 S1557 到 终 到 站 S0481 的 最 少 费 用 为 3 元 ， 最 少 费 用 的 最 优 路 线 有
14

<!-- source_page: 15 -->

Sa
17 条 ;
起 始 站 S0971 到 终 到 站 S0485 的 最 少 费用 为 5 元 ， 最 少 费用 的 最 优 路 线 有
20 条 ;
起 始 站 S0008 到 终 到 站 S0073 的 最 少 费用 为 2 元 ， 最 少 费用 的 最 优 路 线 有 1
条
起 始 站 S0148 到 终 到 站 S0485 的 最 少 费用 为 5 元 ， 最 少 费用 的 最 优 路 线 有
10 条 ;
起 始 站 S0087 到 终 到 站 S3676 的 最 少 费用 为 2 元 ， 最 少 费用 的 最 优 路 线 有 1
条
在 此 种 情况 下 , 我 们 就 只 考虑 可 以 通过 地 铁 站 换 乘 的 情况 ,不 通过 地 铁 站 的
情况 即 为 模型 1 的 求解 结果 。 模 型 2 的 求解 结果 见 附件 1。
6. 3. 1 模型 三 的 建立
该 模型 针对 问题 大， 将 步行 方式 考虑 在 了 出 行 方式 当中 ， 更 符合 余 际 》 因
为 当 出 发 点 与 换 乘 点 5 终点 站 或 转 乘 站 与 转 乘 站 之 间 只 相隔 几 站 本 和 当然 访 有
选择 步行 方式 更 优 : -
因此 作出 如 下 假设 : [一
一 、 如 果 存 在 某 段 路 线 ， SERT 处 等 # 2 ( 即 至 多 经 过
4 个 站 点 六 则 该 段 线路 选择 步行 方式 到 达 目 的 地 。 划 人 的 情况 用 模型 二 来 处 理 。
其 中 路 线 的 两 端点 站 之 间 相 隔 站 点 数 是 根据 公 妆 直达 插 乘 路 线 来 确定 的 。
二 、 相 邻 公交 站 点 〈 包 括 地 铁 站 )》 间 平 场 步 往 时 间 为 5 分 钟 。
三 、 如 果 在 公 汽 线路 上 选择 步行 ， 则 公 汽 | 斋 黎 乘 次 数 减少 1， 如 果 在 地 铁 线
路 上 选择 步行 ， 则 地 铁 间 换 乘 次 数 减 少 ]4 直达 线路 除外 。
直达 和 转 乘 一 次 、 两 次 的 路 线 需 要 步行 的 路 段 示 意图 如 图 6. 5 所 示 。 图 中 (ay
表示 出 发 点 A 与 终点 站 B 间 能 直达 4 相隔 的 站 点 数 等 于 2 所 以 选择 步行 ; 图 中 (b)
表示 出 发 点 A 与 终点 站 B 间 通过 录 换 乘 能 到 达 ， 其 中 路 段 AC 的 站 点 数 等 于 2
所 以 选择 步行 , 同样 如 果 CB 路 段 前 站 点 数 小 等 于 2 ， 则 也 采取 步行 的 方式 ; 图 中
Ce) 兴 反 上行 方 式 的 全 攻 和 凶
下
of R)a ] 步行 ，
// 步行 1
2
[NA<sf s, B S1
NS A B A
人 L : »
洽 TVAN.
图 6. 5 “步行 示意 图
是 否 选择 步行 方式 的 函数 :
1Ng| =A 1 和 和 >
二 ao HR 计 ° (6.8 式 )
其 中 FS，。 表 示 第 凸 路 公交 路 线 是 否 步行 , FD ,表示 第 mn 路 地 铁 线路 是 否 步行 ;
15

<!-- source_page: 16 -->

Ee
对 于 直达 路 线 ， 如 果 出 发 点 与 终点 站 之 间 相隔 站 点 数 小 等 于 2 WAT,
则 乘 车 。 对 于 需要 转 乘 的 路 线 的 最 优 路 线 模型 讨论 如 下 :
1) 以 时 间 最 短 的 路 线 作为 最 优 路 线 的 模型 ， 路 线 总 时 间 等 于 乘 车 时 间 加 上 步行
时 间 ， 再 加 上 转 乘 时 间 。
Mn 工 =3> (1-F5, .JOY +25x>1 -ED. .zx(MD —D
+SxyjSu  <(VB, ,,~D+5xS FD, , <(VD, ,—D
二 Sx(NL 一 > S..)+4xCP。 一 > 了 D. )+7<Ng, +OxNH. 《6.9 式 )
一 >13+2FS. mm)x(GVMB —D+D(25+25D, ,) <(MD, ,—1D)
+SxGN —D FS, )HING —> FD, )+7NB +6NE, 与
1 -从 >
其 中 ， 第 K 路 线 为 届时 考虑 公 汽 与 地 铁 的 转 乘 路 线 中 的 一 种 或 几 种 "小 ])
2) 以 转 乘 次 数 最 少 的 路 线 作为 最 优 路 线 的 模型 ， 每 步行 一 次 8 换季 一 次 车 。
ERFEEEEEEREES = (62050)
此 模型 等 效 为 以 上 转 乘 路 线 按 直 达 、 转 乘 一 次 、 mdf 鸭 包括 公交 与 地 铁 间
的 转 乘 ) 的 优先 次 序 来 考虑 。 s
3) 以 费用 最 少 的 路 线 作为 最 优 路 线 的 模型 : 用
二 王 -划一 全 一 EN (6.21 式 )
其 中 ，CL。 仍 满足 (6.4 °
后 模型 的 全 矶 点 及 改进
7.1 模型 的 评价 一 了
7.1.1 模型 优点 9 4 二
1、 模 型 AR — 使 得 更 贴近 实际 。
2、 本 交 的 楼 于 简单 ， 其 算法 直观 ， 容 易 编程 实现 。
3、 本 文 模型 二 核 注重 数据 的 处 理 和 存储 方式 ， 大 大 提高 了 查询 效率 。
4 湖广 模 列 注重 效率 的 提高 ， 通 过 大 量 的 特征 信息 的 提取 ， 并 结合 有 效 的 算法 ，
禄 工时 浴 可 以 满足 实时 系统 的 要 求 。
\
7.1.2 模型 缺点
在 建 模 与 编程 过 程 中 ， 使 用 的 数据 只 是 现实 数据 的 一 种 近似 ， 因 而 得 出 的 结
果 可 能 与 现实 情况 有 一 定 的 差距 。
7. 2 模型 的 改进
以 上 模型 主要 是 从 公交 线路 出 发 ， 寻找 公 交 线路 的 交叉 站 作为 换 乘 站 点 ， 进
而 找 出 经 过 任意 两 个 站 点 的 可 能 乘 车 路 线 。 我 们 也 可 以 从 公交 站 点 的 角度 出 发，
用 图 论 的 方法 建立 有 向 赋 权 图 如 图 7. 1 所 示 )， 此 向 赋 权 图 是 针对 问题 三 建立
16

<!-- source_page: 17 -->

加
性
的 图 论 模型 ， 问 题 一、 问题 二 只 是 此 模型 的 简化 。 图 7. 1 中 1 表示 公 汽 线路 标
号 ， 该 线路 是 公 汽 线路 ! ,的 上 行 线 或 下 行 线 ，;， 、ggg、$ ，、 、$ ggg、1，
是 公 汽 线路 !, 上 的 站 点 标号 ;，T, 表示 地 铁 线路 标号 ， 该 地 铁 线路 是 双向 行驶 的 ，
)， 、gggD , 、D ,，、ggg、D ,是 地 铁 线路 1 上 的 站 点 标号 ; AKL 与 地 铁 T, 可
以 在 公 汽 站 ;和 地 铁 站 , 间 换 乘 。 如 果 图 7. 1 中 的 地 铁 线路 替换 成 公 汽 线路 ，
为 了 表示 公 汽 间 换 乘 所 需 的 时 间或 者 费用 , 应 将 同一 个 换 乘 站 点 用 两 个 站 点 来 表
%
=LkD
和 -下
DO 2XG
有 向 赋 权 图 1 ¥~
4 | | 、 和合
痪 几 SX
S1 Si LS Sn
”OO kgOs- 0
&)
Z0
R nS
~ ， ¥, 公交 线路 的 有 向 赋 权 图

各 本 不 同 的 人 各 和 辐 的 站 点 同 的 过 克 上 阅 的 权 人 然后 利用 图 论 的 相
关 算法 , 找 出 相应 的 最 短路 径 。

1) 交大 转 间 最 短 为 目标 时 ， 给 每 条 边 虐 上 时 间 的 权 值 : 给 同一 线路 上 任意
两 个 站 点 间 的 边 研 值 时 ， 其 权 值 等 于 站 点 间 的 公交 线路 段 数 与 平均 时 间 的 乘积 。
当 厌 民 线路 的 两 段 点 间 间 隔 站 点 数 小 等 于 3 时 ， 选 择 步行 ， 该 线路 的 权 值 等 于 步
重 ( 交 不 同 会 汽 和 地 铁 间 进行 换季 时 需要 给 不 同 的 权 值 以 表示 换 乘 时 间 。

例如 〈 如 图 7. 1);

当 访 4 时，y) 到 》 的 边 权 值 <SS—GDE: »

从 $ ， 到 } 不 需要 的 转车 ， 但 根据 假设 应 选择 步行 ， 其 边 权 值 全 ,SS> 一 S:，

从 $ ,到 ) 要么 乘 公交 ， 然 后 转车 ， 要 么 步行 ， 根 据 步行 的 假设 条 件 ，$

到 ) ， 的 站 点 间隔 数 小 于 2， 因 此 选择 步行 ， 其 边 权 值 登 ,I2=-S:，

17

<!-- source_page: 18 -->

村

当 g4 时 ，) 与 ] ,之 间 的 边 权 值 <CAEEIE—= ，

;到 D ,的 边 权 值 信 . 忆 =-6;

D ,到 ,的 边 权 值 <C.S> 一 7;

当 j>4、g>4 时 ，$， 到 0 的 路 径 长 度 为 :

当 jx4、g>4 时 ， 则 从 到 D , 选择 步行 ， 再 乘 地 铁 到 ) ，， 和

LRCPIEEEEDEPRDe RE， 一 Si
Se CC AN

接 出 任意 两 志 间 可 行路 线 的 路 径 长 度 后 , 再 搜索 出 其 中 丽人 短路 径 的 的 可 行
路 线 作为 时 间 的 最 优 路 线 。 “ 门 一

2) 当 以 费用 最 省 为 目标 时 ， 则 给 每 条 边 风 上 费用 克 狐 值 。

公 汽 站 点 癌 的 边 权 按 〈6.4 式 ) 赋值 。 W)\

当 公 汽 线路 L/ 按 单一 标价 计 费 ， 对 于 1， AR 和 间 ，
# 休 HL<4， 则 选择 步行 全 ,Si 一 0; 了 1>4， 则 全.S;)=1;

当 公 汽 线路 1 按 分 壬 计价 , 荐 了 定 H<4 则 人 ,Si)-0， 若 3 本 -0 ，

7e, V4
W(S,S,y=1; # I<5—G==ki, 出 4S;S;>=2; # T—i>40, NS,S,>=3;
地 铁 线路 T， 上 全 训 个 拓 生 6 ， 间 7 % 宁 HL<4， 则 选择 步行
ROLE 则 <LBE-<AEEBCD> =: 换 乘 站 点 ，
omega 即 < 一 和 BC- 刚 从 ; 通过 站 点 换 乘 ) , 到
, 间 的 说 = = ，
从

D st 线 的 路 径 长 度 为 ;

外
民生 g>4， 则 从 ) 到 ;选择 步行 ，CBICD-ADD>-，

若 j>4，g>4， 则 KPISSPREESEPREEDIGEEESE3S

同样 可 以 找 出 任意 两 点 间 可 行路 线 的 路 径 长 度 ， 然 后 再 搜索 出 最 短路 径 作为
费用 的 最 优 路 线 。

以 上 从 公交 站 点 出 发 , 将 公交 站 点 作为 网 络 图 中 顶点, 得 出 公交 的 拓扑 结构 ，
进而 寻求 不 同 目标 下 的 最 短路 径 ， 为 我 们 提供 了 另外 一 种 思路 。 但 是 从 以 上 图 形
的 结构 ,我们 已 经 看 得 出 其 复杂 程度 是 不 可 预知 的 ， 尤 其 随 着 数据 的 增多 ， 图 的
复杂 度 随 之 上 升 。 如 果 不 寻求 一 个 好 的 算法 ， 而 用 常规 的 Dijkstra 算 法 ， 将 有 可

18

<!-- source_page: 19 -->

回 8 昌国
能 在 可 以 忍受 的 时 间 范 围 内 得 不 出 有 效 结果 。

经 过 参考 相关 资料 ， 我 们 发 现 用 蚂蚁 算法 可 能 比较 有 效 。 该 算法 利用 了 蚂蚁
寻 食 出 行路 径 选 择 的 行为 特点 ,通过 线路 激素 强度 的 更 新 机 制 ， 实现 了 以 换 乘 次
数 最 少 和 公交 出 行 站 点 最 少 的 公交 出 行路 径 选择 优化 目标 。

八 参考 文献

[1] 344000 温 小 文 臧 德 庆 ， 城 市 公交 信息 查询 系统 设计 初探 ， 江 西 测绘 ， 第
65 期 ，2006

[2] Z&f) 图 论 与 网 络 最 优化 算法 重庆 大 学 出 版 社 ，2000

[3] 1671-4512(2003)S1-0313 张 帅 彭 玉 青 赵 镇 李志强 ， 蚂 蚁 算法 在 公交 查
询 最 短路 径 求 法 中 的 应 用 ， 华 中 科技 大 学 学 报 〈 自 然 科 学 报 ) ， 和 3 大 2003

E\
九 附件 人行-
转 乘 0 次 的 情况 AX
人 oa 和 mv
点 站 点 站 点 ANY 几 站 点 耗 时 /min 转 乘 次 数
E C C2 ." N B HE C
转 乘 工 次 的 情况
[二
[|
[|
人 as |
[二 | 本 由 | | 8 和 | we |
-7 |
转 乘 2 关 的 逢 咒
ECOECSCOEGEGSCOIEOCOECEEI
F¥ [co [wme [oo [12 [o [som [owwwn|  |  | +
有 CCC 生生 国
EECIEIICIEGEECCOCIRECINRECIIE
EN E E C Ca K E NT
ws[vr | son [sr[co [sar[sos [ww [won | w | 3| @
ECOEGEICOIEIECSCOIESCIIECEIEG
EECIEEGEIEIEZIRRECINEEIIEDI
[“owr[n [sown [oz [12 [wo [swrs [wr [wo| m5 | 5 | 2|
19

<!-- source_page: 20 -->

a
$0087 L28 | S0608 D12 T2 D36 S3676 | L209 | S3676 33.5 5 2
or|o [wa| we | v|[w [srs |aw [wre| me | 5 | 2
EArCCCEar Ea D e
or| [na| wie | v[[w [srs |ua[woe| 3s | 5 | 2
or|m [wa| we | v| w [srs [s[woe| ms | 5 | 2
EECOEGEICOEGESCOIEOECIOECECZI
[ae [maow mmlaalalasl as ls | |
EECIECIECEEIEEZICIESEEZNEGIEE
[ae elselaelaslss es |
EECIECIEEEIEEZICOES 本 天 三 99 和 9
IIEZIEEEEIEZCI 区 卫 本 也 因 本 5 恬 加 到
EZCOICIESENEIECIIECIEZNRESNNEI
ERE aEC E  E, ~0 ME
ones|a [sr| b| | wa [ower |om [es |_3n# J47 |2
oris[rar [or| or [1 |osos|o[soms [Zas [)5 | &
EZEICOKIEIENEIEICIEC RE
EECIEEEOICOIEEEOCZOSIGEDIROEE
EECOENEISCOIEGESCIEOEEOECECZI
[ww ww BE
攻 硬 COIEEIEERESREIESEICIEECIIEEGI EEC
[| 本 才 mealaas 人 |
[ls nilwwlwlss ww |
[|
on[urw [or | o Tom Jsor om [soms |e |5 | &|
[wall ww RE
[al  RE E
EEETAE  f E [0
com{eyf sbrl o | 1v |[or |sotrao [ss| oo | s | o|
[ownlalaelwlss 人 |
EECIEIIOEEE 生 本 到 本 3
[ea mn mass wa
8 [o owr [o [ on sos o[som |w|5 | 2|
ER C C E E  E  RO EEC
EREC R C E  E  RE RE
下 COIECIECREIEEZICOIECIRCIIRO RE
匡 ZCOIEEIICEEIEEZICGEIEECINIEEG EEC
[else ws |
owJm [or| o [w |oa [owor ao [os| wo| 5 | RE
EECOIEECICOEGEGCOIEGOECIOECEZZI
20

<!-- source_page: 21 -->

p—-
是

S1557 L84 | S1919 | S2079 | L417 | S2424 | S2424 | L254 | S0481 109 3 2
改写 大 COIEEIIEOCIEIEICIEIEECZNEDI RE
EECIEIIEICOEOECOIEIEECNREI RE
改写 本 CEIIEOCOEIEICOIEIEECNEES RE
rr|to ow som vrsue s| vs[sor | w0| 5| RE
rsr[sn [ow om| vrsues| vs[sor | w0| 5| RE
EECIEOEIOICOEOEIICIEIRCIREI RE
EECIEIIEICOEOEICOIEIEECIEEI EEC
医 二 硬 EIEIIEICOEIIEICOIEIEECZNEE RE
EECIEIIECICOEOEIICIEIRCIIRE RE
EECIEIIEICOEOECOIEIEECIEE IE
rsro ow [spe im [sesves | a [sor | w0|3 A7REy
EDGEOIOECOECOICIECIEEONRESNNEI
EECOEIEOCOEOEOGCOIEIEECSIESEI IE
医 E 有 EIEDIEOICUEOIIEOICICCIERC SEE
EE 二 有 COIEIIEIEOEOEGCOIEORECNINEI RE
EECOROEORIECIEOICIEC RISE
EECOEDEICOEOEGCICAEIIOECEZZI
IE P [Y  R  C  IN RE
EECIEIECOEOEOEICXEIEECIIREIIEEI

% °
, |] 记

10.1 Ci 的 程序
fplotC 0 , [2746] 人 直线 作为 T1 铁 路 线
Ya Wo 3; \

isones(size(y))

hold on;

plot (il, y) ; % 给 站 点 作 标记

istr=int2str(i/2) ;

text (i-0. 5, -0. 5, istr) ; % 给 每 个 站 点 标 上 铁路 站 号
end
x1=24:0. 005:36;yl=(36-(30-xl). 2). 0.5;y2=-yl;
plot (xl, yl, xl, y2，b  ) ; % 画 圆 作为 T2 铁 路 线

21

<!-- source_page: 22 -->

ERE
27 FE
1
for j=1:6
x2(j)=30-6xcos (pi*j/7) ;y3(j)=6%sin(pi*j/7) ;
plot (x2(3), y3(3), r); %&rili fEhRid
jstr=int2str (j+26) ;
text (x2 (j)-0. 5, y3 (j)-0. 8, jstr) ; % 给 每 个 站 点 标 上 铁路 站 号
end
for j=1:10
x2(j)=30-6%cos (pi*j/11) ;y3(j)=-6#sin (pi#j/1l) ;
plot (x2 (jy3 (，rx# ) ，% 给 站 点 作 标记
end b
for j=1:3 - <
jstr=int2str(27-j) ; “\
text (x2 (j)-0. 5, y3(§)=0.8, jstD) 4% 给 每 个 站 点 标 上 铁路 站 号 3/ 人
end
for j=4:10
jstr=int2str (43-j) ;
text (x2(j)-0.5,y3(j)=0.8, jstr); TRK
end -
axis([-2 50 -10 10]); % 修 改 坐 标 畏
title( 地 铁 示意 图  ) ; % 注 明 标题 @@
hold off; Ve, A [o]
10. 2 问题 一 的 相关 源 程 序
10.2. 1 (文件 名 : Calcula ars.h)
#include “vectorDs r
#include <map>
#include <fs SV
#includey” sage. h”
CC
#aaeluge <iomanip>
和 h”
using namespace std;
// 计算 经 过 各 路 线 的 所 花费 的 时 间
multimap<{float, vector<int> > TimeCalculate(
vector<vector<int> > & FeasibleSolve,
vector<{LoadMessage> & AllLines
)
22

<!-- source_page: 23 -->

回 成 革 动 国
后
0
BRLLT]
四
{
multimap<{float, vector<int> > Respond; // 返回 值
for (int i=0; i<FeasibleSolve.size(); ++i) // 遍历 每 一 种 方案
{
float fTotalTime = 0; // 总 花 时
vector<int> CurrWay; // 行车 路 线
int nLineName = FeasibleSolve[i][1];
// 第 一 段 路
fTotalTime = 3. 0*(FeasibleSolve[i][2] - FeasibleSolve[ 订 [0]); “
=:iK2
=
int a = FeasibleSolve[i][2]; 全 \
int b = FeasibleSolve[i][0]; 准 -
CurrWay. push_back (Al1Lines[nLineName-1]. Lineln ibleSolve[i][0]]);
CurrWay. push_back (nLineName) ;
全
if (FeasibleSolve[il.size() ==3) |
{
CurrWay. push_back (Al1Lines [nLineNamez1] .LinelInfo[FeasibleSolve[i][2]]);
AAA
Respond. insert ( mal i#(fTotalTime, CurrWay) );
continue;
y
int nlineNamel = 一 了
for, Root iae0; jf=3)7 力 计算 剩余 每 一 段 路 花费 的 时
间 2
loat fEachTime = 0;
fEachTime = 3.0%(FeasibleSolve[i][j+2] - FeasibleSolvelil[jl); // 乘 车
用 时
fEachTime += 5.0; // 换 乘 时 间
fTotalTime+= fEachTime;
nLineNamel = FeasibleSolve[i][j+1];
CurrWay. push_back (Al1Lines[nLineNamel-1]. LineInfo[FeasibleSolve[i][j]]);
23

<!-- source_page: 24 -->

回 成 革 动 国
后
0
BRLLT]
半生 二
CurrWay. push_back (nLineNamel) ;
}
CurrWay. push_back (Al1Lines[nLineNamel-1]. LineInfo[FeasibleSolve[i] [FeasibleSol
velil.size()-111);
Respond. insert ( make pair(fTotalTime, CurrWay) );
}
return Respond;
} 全
>
// 文件 输出 花费 时 间 二 \
void OutPutTimeCal (ofstream & fout, 全
multimap<{float, vector<int> >& FeasibleSol
{
multimap<{float, vector<int> >::iterator iter;
iter = FeasibleSolve.begin(); 全
全
while ( iter != FeasibleSolve.end() )
{
fout 《《“ 用 时 :“ 愉 人 setw(4) << SENIC 让 《Citer->first ”min :“;
(ej
fout << ” §” 《< setw(4 £i11(C0") << iter->second[0];
for (int i=1; i >second. size(); i+=2)
{
foutadC 一 《4 setw(4) << setfill(C0") << iter—>second[il;
fout \'a << setw(4) << iter—>second[i+1];
v/
Kx.
证
}
// 计算 经 过 各 路 线 的 所 花费 的 费用
multimap<float, vector<int> > CostCalculate(
vector<vector<int> > & FeasibleSolve,
vector<{LoadMessage> & AllLines
)
{
24

<!-- source_page: 25 -->

回 成 革 动 国
后
0
BRLLT]
半生 二
multimap<{float, vector<int> > Respond; // 返回 值
for (int i=0; i<FeasibleSolve.size(); ++i) // 遍历 每 一 种 方案
{
int nTotalCost = 0;
vector<int> CurrWay; // 行车 路 线
int nFirstLineName = FeasibleSolve[i][1];
CurrWay. push_back ( AllLines[ nFirstLineName-l ]. LineInfo[ FeasibleSolve[i][0] 1);
全
for (int j=0; j<FeasibleSolveli].size(); j+=3) // 每 一 段 路 二 <
1 \
全
int nEachCost = 0; 1
int nLineName = =1;
nLineName = FeasibleSolve[i][j+1]; 余
S / 单一 票 价 路 段
if (‘AllLines[nLineName-1].strPri 三 一 票 制 1 元 。”)
{
nEachCost = 1;
} [o]
else 2 ee // 分 段 票 价 路 段
{
int nDistance casibleSolve[i] [j+2]-FeasibleSolvel[i][j];
if (nDis = 20)
ebpch St = 1;
if( nDistance <= 40)
人 achCost = 2;
为 else
下 4 nEachCost = 3;
% nTotalCost += nEachCost;
CurrWay. push_back ( nLineName ) ;
CurrWay. push_back ( AllLines[ nLineName-1 ].LineInfo[ FeasibleSolve[il[j+2] 1);
}
Respond. insert ( make pair(nTotalCost, CurrWay) );
}
25

<!-- source_page: 26 -->

回 成 革 动 国
后
0
BRLLT]
四
Teturn Respond;
}
// 文件 输出 费用
void OutPutCostCal (ofstream & fout,
multimap<float, vector<int> > & FeasibleSolve)
{
multimap<float, vector<int> >::iterator iter;
iter = FeasibleSolve.begin();
全
while ( iter != FeasibleSolve.end() ) “ <
a
CA \
fout 《《“ 费 用 : 7 Ksetw(d) 《《 setfillC  ) « “有 一 的
fout << ” 8” << setw(4) <<setfill(07) « We ;
for (int i=1; i<iter->second.size(); i+=
{ 全
fout <<.” L” << setw(4) << setfil <<iter—»second[i];
fout << ” §” KCsetw(4) << iter—>second[i+1];
} [o]
XIA 。
fout << endl;
iter ++;
}
} 一 一
// 综合 处 理 时 间 ， 有 we 并 将 结果 分 别 存 入 文件 中 。
void Time 06sUBusChangeTimes_Pro
4
int nStart, int nEnd, // 起 始点 和 目标
vector<LoadMessage> & AllLines, // 所 有 路 线
信息
vector<vector<int> > & AllBuses, // 所 有 公 汽
站 信息
vector<vector<vector<int> > > &RoadCrossInfo /任意 两 路 线 的
交叉 信息
)
{
char char_1[20];
26

<!-- source_page: 27 -->

杞 所
Efes
wsn
char char_2[20];
itoa( nStart, char 1, 10 );
itoa( nEnd , char 2, 10 );
string * pStr_1 = new string(char 1);
string * pStr 2 = new string(char 2);
string strPartName = ”("+ * pStr_1+"="+ * pStr 2+")";
ofstream fout Cost ( (strPartName+“ 费 用 . txt”).c_str() );
ofstream fout_Time( (strPartName+“ 用 时 . txt”).c_str() ); #7
o NY
vector<vector<int> > FeasibleSolve 0; // 直达 一 一 \)
vector<vector<int> > FeasibleSolve 1; // 一 次 转 乘 2
vector<vector<int> > FeasibleSolve 2; // 二 次 转 乘
SS

Direct or not ( nStart，nEnd FeasibleSolve 0, ou RoadCrossInfo) ;
OnceBusChange UnStart，nEnd，FeasibleSolve_1， Hee Al1Buses, RoadCrossInfo);
TwiceBusChange (nStart, nEnd, YY es, AllBuses, RoadCrossInfo) ;
multimap<float, vector<int> > Cost 0 =CostCalculate ( FeasibleSolve 0, AllLines);
multimap<{float, vector<int>> Cost 1 FCostCalculate ( FeasibleSolve 1, AllLines);
multimap<{float, vector<int> 3323 =C6stCalculate (FeasibleSolve 2，Al1Lines ) ;
multimap<float， oo TimeCalculate( FeasibleSolve 0，Al11Lines ) ;
multimap<float, vector<int> »” #ed = TimeCalculate (FeasibleSolve 1, AllLines ) ;
multimap<float, S =TimeCalculate (FeasibleSolve 2, AllLines );
fout _Cost << < 起 始点 ; ¥ nStart << endl;
fout _Cost << 祭 点 : “《《 nEnd  << endl;
fout_Costr<< A << endl;
fou %, “直达 情况 下 : 7 << endl;
aa ” << FeasibleSolve 0.size() 《< 种 ”《《 endl;

W [tPutCostCal (fout Cost, Cost 0);

1 New 《《 THEHHERITHERRIHEHE RBE HE R t H  B ” 《< end] ;

TS “<“ 一 次 换 乘 下 : “《《 endl ;
fout Cost《《“ 总 共有 : ” << FeasibleSolve 1.size() << ” Ff” << endl;
OutPutCostCal (fout_Cost, Cost 1);
fout_Cost << "HEHHHRUHHTRIBHIHERRIBEEHERSHERI BBBIIEIE” 《< end];
fout Cost《《“ 二 次 换 乘 下 : ” < endl;
fout Cost《《“ 总 共有 : ” << FeasibleSolve 2.size() 《(” 种 ”< endl;
OutPutCostCal (fout_ Cost，Cost 2) ;

27

<!-- source_page: 28 -->

ERE
RE
wsn
fout _Time 《《“ 起 始点 : ” << nStart << endl;
fout Time “《《“ 目 标点 : ” << nEnd 《< endl;
fout Time << "HEHHHBHHHERBIHERERIBEEHERERER BBBRIIEIE” 《< end];
fout Time “《“ 直 达 情 况 下 : ” <C endl;
fout Time 《《“ 总 共有 : ” << FeasibleSolve 0.size() 《“(” 种 ”< endl;
OutPutTimeCal (fout Time，Time_0) ;
fout_Time << "HEHHHBHHHERBIHERERIBEEHERERER BBBRIIEIE” 《< end];
fout Time “《《“ 一 次 换 乘 下 : ” < endl;
fout Time 《《“ 总 共有 : ” << FeasibleSolve 1.size() 《(” 种 ”< endl;
OutPutTimeCal (fout Time, Time 1) ;
fout_Time << "HEHHHHEHERHIHEHTHRIBHERERIHERUBREBEERERIIIINE” 《< end];
fout Time “《《“ 二 次 换 乘 下 : ” < endl; A7
fout Time 《《“ 总 共有 :: ”《《 FeasibleSolve 2.size() <<” Ff” << endl; NY
OutPutTimeCal (fout Time, Time 2); 2G \)
H~
/% ofstream fout BusChange( (strPartNamet“ 转 乘 .txt ) . 人
multimap<{float, vector<int> > BusT 0 = CostCalcul ANR AllLines ) ;
multimap<{float, vector<int> > BusT 1= CostCal oulate (FeasibleSolve 1, AllLines ) ;
multimap<{float, vector<int> > BusT 2 = AllLines ) ;
Le
fout_BusChange “《《“ 起 始点 : MA% nStart(«< endl;
fout_BusChange “《“ 目 标点 : << endl;
fout_BusChange << EPRI£ A —— << endl;
fout_BusChange << ” EL 异 见 下 ”<“< endl;
fout BusChange << ”4ik 有 jj 《《 FeasibleSolve 0. size() ”种 ”《“《 endl;
OutputCostCaLtout_ Bus ange, BusT 0) ;
fout_BusChan CHESHEHERHHREHEHE R  S  H  B ” 《< end] ;
fout_BusCl oo 人 sm ” << endl;
fou 0 < “总 共有 :“《《 FeasibleSolve 1.size() <<” ff” << endl;
oo (fout_BusChange，BusT_1) ;
SU ange 《《 HEHEHHHEEREEHIREHHRIHEERERERHERHES BRSREHIER” 《< end] ;
1 BOsChange <“ 二 次 换 乘 下 :“《《 endl;
Te < “总 共有 :“《《 FeasibleSolve 2.size() <<7 ff” << endl;
OutPutCostCal (fout_BusChange，BusT 2) ;
*/
/%
ofstream fout (“ 换 乘 二 次 的 解决 方案 .txt ”) ;
ofstream fout1( “测试 费 用 .txt ) ;
28

<!-- source_page: 29 -->

回 成 革 动 国
后
0
BRiE]
半生 二
for (int j=0; j<200; ++j)
{
vector<vector<int> > FeasibleLine;
cout 《《“ 请 输入 起 始 站 点 和 目标 站 点 : ”;
cin >> nStart >> nEnd;
fout 《《 "HHHBHHEEHERIHHERTHIBEHERHRUBEREERERIEIE” 《< end];
fout 《《“ 起 始 站 点 : ” << nStart 《< endl;
fout 《《“ 目 标 站 点 : ”《< nEnd 《< endl;
全
// Direct or not(nStart, nEnd, FeasibleSolve, AllLines, Al1BuseS, <
RoadCrossInfo) ; \
2/ 一
OnceBusChange (nStart, nEnd, FeasibleSolve, AllLings, Al s,
RoadCrossInfo) ; AX
// TwiceBusChange (nStart, nEnd, FeasibleSolve, 1Lines, AllBuses,
RoadCrossInfo) ; 人
multimap<{float, vector<int> > SolveList = CostCalculate( FeasibleLine,
AllLines ); 人 @
(ej
OutPutCostCal (foutl, So ist) ;
fout 《《“ 连 线 情 ; << FeasibleLine. size() ”种 : ” << end];
]/ 输出 线路 -了
for (int 访 ” size(); ++i)
{e
下 和 - k=0; k<{FeasibleLine[il.size(); +tk)
fout << FeasibleLine[i][k] << ” ”;
Wa-
fout << endl;
}
}
*/
}
10.2.2 (文件 名 : CalulateWays. h)
#include <map>
29

<!-- source_page: 30 -->

回 成 革 动 国
ae 汪
时
和
#include <iostream»
#include <vector>
#include “LoadMessage. h”
#include <fstream>
using namespace std;
// 判断 一 条 线 上 两 点 间 是 否 是 上 下 层次 关系 ， 如 果 是 ， 确 定位 置
bool find(vector<int> &Line, const int NFIRST，const int NSECOND,
int &pos_ 1，int &pos 2)
{
if (NFIRST == NSECOND) 二
， =\sS
int i =0;
2/ 一
while (Line[i] != NFIRST)
{
+
} 全
全
pos_ 1 = pos-2 = i;
return true; 和 @
9K )
bool bHaveFound ”= false;
bool IsDirectTo 1 = ;
for (int i=0;miLine. size(); ++1)
{
< NFIRST)
下 Ge = true;
s 1 = ii
1 // continue;
}
if (IsDirectTo 1 && Line[i] == NSECOND)
{
pos 2 = i;
bHaveFound = true;
break;
}
}
30

<!-- source_page: 31 -->

ERE
后
0
BRLLT]
: a El
if ( !bHaveFound )
{
pos_1 = pos 2 = -1;
}
return bHaveFound;
}
// 找 出 两 点 间 是 否 有 连 线 直接 连接
// 如 果 有 ， 则 返回 所 有 可 能 的 连 线
全
bool Direct_or_not (const int NSTART，const int NEND, < 标
点
. 人 “二 和
vector<vector<int> > &FeasibleSolve, / 可 行 的 解
决 方案 ， 是 返回 值
vector<LoadMessage> & AllLines, // 所 有 路 线
信息
vector<vector<int> > & AllBuses // 所 有 公 汽
站 信息 7
vector<vector<vector<int> oadCrossInfo)  // 任意 两 路 线 的
交叉 信息
{ [o]
int i, j ; 2 ee
i=j=0;
bool bHaveFound = fa
vector<int> Possiblel.i ;7V/ 存储 可 能 的 解
// 搜 起 Rs 目标 站 点 线路 间 是 否 为 同一 线路
for«(i 11Buses [NSTART-1]. size () ; ++i)
{
for (j=0; j<AllBuses[NEND-1].size(); ++j)
if (AllBuses[NSTART-1][i] == AllBuses[NEND-1][j])
{
PossibleLine. push_back (A11Buses [NSTART-1] [i]) ;
}
}
}
bool bIsDirect 1 = false;
int nCurLineName = -1; // 可 行路 线 的 编号
31

<!-- source_page: 32 -->

回 成 革 动 国
二
时
wsn
int nStart_pos = -1; // 起 始点 在 可 行 线路 中 的 位 置
int nEnd_pos =-1; // 目标 点 在 可 行 线路 中 的 位 置
vector<int> FeasibleLine(3, 0);
for (i=0; i<PossibleLine.size(); ++i)
{
nCurLineName = PossibleLine[i];
for (j=0; j<AllLines[ nCurLineName-1 ].LineInfo.size(); ++j)
{
if (AllLines[nCurLineName-1].LineInfo[j] == NSTART)
{ 全
bIsDirect 1 = true; “ <
_ a
nStart_pos  = j; 二 \
continue; 全
}
if (bIsDirect 1 & 八
AllLines[nCurLineName-1]. LineIn of j] == NEND)
{ 全
bHaveFound = true;
nEnd pos” = j;
[o]
Fonst etn rt pos;
FeasibleLine[1 LineName;
FeasibleLine[2] nEnd. pos;
— FeasibleLine ) ;
一 一
AL
Rh = false;
return bHaveFound;
}
// 一 次 换 乘 的 情况
bool OnceBusChange (const int NSTART, const int NEND, // 起 始点 和 目标
点
vector<vector<int> > & FeasibleSolve, // 可 行 的 解决 方
32

<!-- source_page: 33 -->

ERE
和
RE
案 ， 是 返回 值
vector<LoadMessage> & AllLines, // 所 有 路 线
信息
vector<vector<int> > & AllBuses, // 所 有 公 汽
站 信息
vector<vector<vector<int> > > &RoadCrossInfo) // 任意 两 路 线 的
交叉 信息
{
bool bHaveFound = false;
vector<int> FeasibleLine(6, 0);
全
int i, j, k; - <
i=j=k=0; 二 “\
和
int nFirstLine = -1; 从 一
int nSecondLine = -1;
int nCurBridge = -1;
:
bool IsDirectToBridge = false; 人 // 起 始点 是 否 能 直达 中 转
点 R
bool IsBridgeDirectToDest = false; // 中 转 点 是 否 能 直达 目标
点 @
2 外
// 搜索 相交 的 两 条 线路 3
for (i=0; i<Al1Buses[NSTART-1].size(); ++i) // 经 过 起 始点 的 所 有 线路
{
nFirstLine = oo [il;
—~
for (j=0 司 j uses[NEND-1]. size() ; ++j) // 经 过 终点 的 所 有 线路
2 训
ondLine = AllBuses[NEND-1][j];
X% // 两 路 线 的 公有 站 点
t nLinel = -1;
1 // int nLine2 = -1;
if ( nFirstLine < nSecondLine )
{
nLinel = nFirstLine;
nLine2 = nSecondLine;
}
else
{
nLine2 = nFirstLine;
33

<!-- source_page: 34 -->

回 成 革 动 国
有
时
和
nLinel = nSecondLine;
}
for (k=0; k<RoadCrossInfo[nLinel-1][nLine2-1].size(); ++k)
{
nCurBridge = RoadCrossInfolnLinel-1][nLine2-1] [k];
int a=0, b=0, c=0 d=0;
bool IsDirectToBridge
= find(Al1Lines[nFirstLine-1]. LineInfo, NSTART, nCurBridge, a,
b) ;
全
bool IsBridgeDirectToDest = false; “ <
o,
if ( IsDirectToBridge ) 全
{
IsBridgeDirectToDest
= find(Al1Lines[nSecondLine-1]. L , “nCurBridge, NEND, c,
} 全
if ( IsDirectToBridge && IsBridgeDirectToDest)
{ (|
FeasibleLingl0] # a; FeasibleLine[1] = nFirstLine;
FeasibleLin b; FeasibleLine[3] = ci
FeasibleLi SecondLine; FeasibleLine[5] = d;
oj push_back(FeasibleLine) ;
人 VWoraiae = false;
LA— = false;
|
// cout《 FeasibleSolve. size() << endl;
if ( !FeasibleSolve.empty() )
bHaveFound = true;
return bHaveFound;
}
34

<!-- source_page: 35 -->

ERE
1
// 二 次 换 乘 的 情况
bool TwiceBusChange(const int NSTART，const int NEND, // 起 始点 和 目标
点
vector<vector<int> > & FeasibleSolve, // 可 行 的 解决 方
案 ， 是 返回 值
vector<LoadMessage> & AllLines, // 所 有 路 线
信息
vector<vector<int> > & AllBuses, // 所 有 公 汽
站 信息
vector<vector<vector<int> > > &RoadCrossInfo) // 任意 两 路 线 的
交叉 信息 “
Hoo
bool bHaveFound = false; “\
2/ 一
vector<int> FeasibleLine(9, 0); 从 一
int nCurLineName = = 二
int nFirstBusChangeStation = -1; 换 乘 的 车 站 名
全
int i, j, k; »
i=j=k=0; 外
for (i=0; i<AllBuses[NSTART-1].sizeQ; ++i) // 经 过 起 始 站 点 的 所 有 线
路 2 外
狼
nCurLineName = AllBusesNSTART=1][i];
j=0;
int nStart.pos~ -1;
/A Ran LineInfo[j] != NSTART)
%
4 = j;
人 NV/ // 当前 线路 上 的 所 有 站 点
for (j=j+1; j<AllLines[nCurLineName-1].LineInfo.size(); ++j)
{
nFirstBusChangeStation = AllLines[nCurLineName-1]. LineInfolj];
vector<vector<int> > temp;
bool IsConnected
= OnceBusChange (nFirstBusChangeStation,
NEND, temp, AllLines, AllBuses, RoadCrossInfo );
35

<!-- source_page: 36 -->

回 成 革 动 国
后
0
BRLLT]
四
if ( IsConnected )
{
int m = temp[0][0];
int n = temp[0][1];
int d = AllLines[n-1].LineInfo[m];
for (k=0; k<temp.size(); ++k)
{
FeasibleLine[0] = nStart pos; FeasibleLine[1] = nCurLineName;
FeasibleLine[2] = j ; FeasibleLine[3] = temp[k][0];
FeasibleLine[4] = temp[k][1]; FeasibleLine[5] = te [2] ;
FeasibleLine[6] = temp[k][3]; FeasibleLine[7] = ，
FeasibleLine[8] = temp[k][5]; \
2/ 一
FeasibleSolve. push_back( FeasibleLiney) ;
}
}
| 外
} 全
cout << FeasibleSolve.size() << endl;
[o]
if ( !FeasibleSolve. 2 (ee
bHaveFound = true; 从
return bHaveFound;
}
一 一”
10.2.3 (文件 名 : ge.h)
#ifndef _ROADMESSAGE H
#define W&™
#ie 人 string>
& iclude<vector>
using namespace std;
// 线路 信息
class LoadMessage
{
public:
LoadVessage ()
{
nLineName = -1;
36

<!-- source_page: 37 -->

ERE
A
ee 了
StrPrice= "";
bRoundLoad = false;
}
int nLineName; // 公交 线路 名
String strPrice ; // 计 费 信息
vector<int> LineInfo;  // 线路 信息 , 里 面 存储 的 是 当前 公交 线路
// 沿线 公 汽 站 点 。
bool  bRoundLoad; // 判别 是 否 为 环形 路 。
】;
合
#endif 全 人 >
-个
全 /一
10. 2.4( 文 件 名 : ShortPathCalculate. cpp)
[LA NAAAAAAAAAAAAAAAAAAAAAN Mj 风 AH
//
// ”此 程序 计算 最 小 公交 线路
/
//， 有 关 要 求 : 用 户 输入 起 始 站 点 和 终点 ,在 满足 换 l 数 丰 超过 某 一 限度 的 情况 下
// 程序 输出 所 有 可 能 的 行车 路 线 AS
//
[AAA[ 久 AMNAUMAAAAAAAAAAAAAAAAA
O 〇
#pragma warning(disable: 4786) 5
#include <map> S
#include <iostream> )
#include fstreamie. » ¥
#include <{strstream>
#include <{stui 2 \/
#includ co
ro 人
#igre) ide "ULtity. h”
#il ¢lude “CalculateStandars. h”
//#ing lude “CalulateWays. h”
using namespace std;
void main()
{
ifstream fin("1.1 公 汽 线路 信息 . txt”);
// 经 过 实现 的 计算 ， 总 共有 520 条 公 汽 线路 , 3957 个 公 汽 站 点
37

<!-- source_page: 38 -->

ERE
0
EEEE
//
// 将 同一 路 线 的 上 、 下 行路 线 看 成 两 个 不 同 的 路 线
// 将 环形 路 线 换算 成 两 个 与 之 等 价 的 单行 路 线
vector<LoadMessage> AllLines (1040) ;
vector<vector<int> > AllBuses(3957);
string strCurrLine ="7;
string strBusLine = // 公交 线路
String StrPrice = // 票 价 信息
string strUpLoad = ””; // 上 行路 线
string strDownLoad = 人; // 下 行路 线 “
string strRoundLoad = ""; // 环形 路 线 二 <
bool ”IsRoundWay” = false; // 判断 当前 读 入 的 路 线 是 否 为 环形 线 \
和
for (int nCount=0; nCount<520; ++nCount)
{
IsRoundWay = false;
全
// 读 入 路 线 各 7
do {
getline(fin, strCurrLine,” \n’);
} while(strCurrLine ==""); 人 @
AAA
StrBusLine = strCurrLin
// 读 入 计 费 标准
do {
getline(fin, strCurrLine,” \n');
} 这 ="");
o,
人 和 strCurrLine;
/ VRAN EATHZ
Te:
getline (fin，strCurrLine，ANm ) ;
} while(strCurrLine == "");
string temp(strCurrLine, 0, 6);
// 环形 线路
if (temp ==“ 环 行 : ”)
{
strUpLoad ="
38

<!-- source_page: 39 -->

杞 所
和
wsn
strDownLoad = "";
strRoundLoad = string(strCurrLine, 6, strCurrLine.length());
IsRoundWay  = true;
}
// 下 行 线路 不 是 上 行 线路 的 逆 方 向
else if( temp ==“ 上 行 : ”)
{
strUpLoad = string(strCurrLine, 6, strCurrLine.length());
strRoundLoad = ””;
// 读 入 下 行路 线
do 1{ 多
getline (fin，strCurrLine，Nn ) ; 二 A7
} while(strCurrLine == ""); ZX \)
一
StrDownLoad = string(strCurrLine, 6, strCurrLine. Chefr”
代
/大 下 行 线路 是 上 行 线路 的 逆 方 向
else DA
{ 全
StrUpLoad = strCurrLine; K
strDownLoad 一人;
strRoundLoad = ””; O
的
// 构造 同一 路 线 分 成 的 两 全 路 线 汉 并 把 它们 存 入 容器 中
LoadMessage S currLoad up; // 当前 路 线 的 上 行路 线
LoadMessage 一 currLoad_down; // 当前 路 线 的 下 行路 线
—r
currLoad Sup.nLineName = StrTolnt ( string(strBusLine, 1, 3) );
CUIET Te = strPrice;
o bRoundLoad = IsRoundWay;
3 N nLineName = currLoad _up. nLineName + 520;
1 // rrLoad down. strPrice = strPrice;
SA， currLoad_down. bRoundLoad = IsRoundWay;
// 环形 路
if ( IsRoundWay )
{
RoundRoadCal (strRoundLoad, currLoad up.nLineName, AllBuses,
currLoad_up. LineInfo, currLoad down.LineInfo) ;
}
39

<!-- source_page: 40 -->

回 成 革 动 国
二
ER
wsn
// 非 环形 路 的 上 行路
if (strUpLoad != "")
{
BusRoadCal (strUpLoad, currLoad _up. nLineName, AllBuses,
currLoad up.LineInfo) ;
}
// 非 环形 路 的 下 行路
if (strDownLoad != "")
{
BusRoadCal (strDownLoad, currLoad_down. nLineName, AllBuses,
currLoad_down. LineInfo) ; “
- 欠 >
a
else if ( !IsRoundWay ) \
{ 72
ReverseRoadCal (strUpLoad, currLoad_down. nLine AllBuses,
currLoad_down. LineInfo) ;
}
全
Al1LinesfcurrLoad_up. nLineName=1] 二 = up;
AllLines[currLoad down. nLineName-1] = ad_down;
}
o p fa
// 520%520 的 矩阵， 里 面 存 储 避 的 线路 它 间 的 重合 站 点 信息
vector<vector<int> > (520) ;
vector<vector<vector<int> > 0 ossInfo(520，vTemp) ;
// 任意 两 条 线路 间 相 页 点 信息
RoadCrossInfo.= CalRoa rossInfo( AllBuses );
int =y Yy
int 下 4 一 1;
(int 村 =0; i<200; ++i)
cout 《《“ 请 输入 起 始 站 点 : ” ;
cin >>nStart >> nEnd;
Time_Cost_BusChangeTimes_Pro (nStart， nEnd, AllLines, AllBuses,
RoadCrossInfo) ;
}
}
40

<!-- source_page: 41 -->

回 成 革 动 国
IE
二
BRiE]
四
/# ofstream fout( “各 公 汽 站 信息 . txt”);
for (int i=0; i<AllBuses.size(); ++i)
{
fout << i+l < 7%
for (int j=0; j<AllBuses[i].size(); ++j)
{
fout << AllBuses[i][j] <<”” ;
]
a
fout << endl; \
} Z 7
of stream foutl(“ 各 公路 线路 重合 站 点 信息 . txt”); 任
全
for (int i=0; i<520; ++i) 人
{
for (int j=i; j<520; ++j)
(ACT e
for (int k=0; 0 nfol@] [j]. size(); ++k)
{
foutl << RoadCrossinfeli][j1[k] << ” 7;
o
foutlatC endl;
}
1 信
W
三 的 相关 程序
10 文件 名 : CalculateStandars. h)
#include <vector>
#include <map>
#include <fstream>
#include “LoadMessage. h”
#include <string>
#include <iomanip>
#include “CalulateWays.h”
41

<!-- source_page: 42 -->

回 成 革 动 国
后
0
BRiE]
回 共 Sakn
using namespace std;
float BusPrice(int nLineName, int nDistance,
vector<{vector<int> > & FeasibleSolve,
vector{LoadMessage> & AllLines)
{
float nEachCost = 0;
if ( AllLines[nLineName-1].strPrice ==“ 单 一 票 制 1 元 。”)
{
nEachCost = 1; 全
- 丛 ，
else // 分 段 票 价 路 段 \
2/ 一
{
if (nDistance <= 20)
nEachCost = 1;
else if( nDistance <= 40)
nEachCost = 2;
全
else -
nEachCost = 3;
}
[o]
return nEachCost; 2 (ee
}
// 计算 经 过 各 路 线 的 所 花费 的 辐 问
vector<vector<float> > Ti SS st_Calculate(
_— vector<{vector<int> > & FeasibleSolve,
vector<{LoadMessage> & AllLines
%)7
C V
vect 人 > Respond; // 返回 值
襄 * i=0; i<FeasibleSolve.size(); ++i) // 遍历 每 一 种 方案
float fTotalTime = 0; // 总 花 时
float fTotalCost = 0; // 总 花费
float fCost A =0;
float fCost B =0;
float fCost C =0;
vector<{float> CurrWay; // 行车 路 线
42

<!-- source_page: 43 -->

回 成 革 动 国
后
0
BRLLT]
=E Sakn
int A_1 = FeasibleSolve[i][0];
int A = FeasibleSolve[i][1];
int A 2 = FeasibleSolve[i][2];
float Time A = 3.0%(A 2 - A 1);
int B 1 = FeasibleSolve[i][3];
int B = FeasibleSolve[i] [4] H
int B 2 = FeasibleSolve[i][5];
float Time B = 0.0; “
Hoo
int C_1 = FeasibleSolve[i][6]; 一 \
int C = FeasibleSolve[i] [7] H 全
int C 2 = FeasibleSolve[i][8];
float Time C = 3.0x(C 2 - C 1); A
全
float fTime B C = 0; 人
float fTime A B = 0;
if (B > 1040) ee】
{ Ve, 外
fTime A B = 6.0;
fTime BC = 7.0;
Time B = B 2-B 1);
fCosteB__73.0;
}
y/A ) y
下 人 =5.0;
ime B C = 5.0;
1 // Time B =3.0%(B 2-B 1);
fCost_B = BusPrice(B, B 2-B 1, FeasibleSolve, AllLines);
}
if (Al1!=A2)
fCost_A = BusPrice(A, A 2-A 1, FeasibleSolve, AllLines);
else
fCost_A = 0;
43

<!-- source_page: 44 -->

Eii
和
和
if (C1!=C2)
fCost_C = BusPrice(C, C 2-C 1，FeasibleSolve，Al1Lines) ;
else
fCost C = 0;
fTotalTime = Time A + Time B + Time C + fTime A B + fTime B C;
fTotalCost = fCost A + fCost B + fCost Ci
int nA_1 = AllLines[A-1].LineInfo[A 1];
int nA 2 = AllLines[A-1].LineInfo[A 2];
int nB_1 = AllLines[B-1].LineInfo[B 1]; #7
int nB 2 = AllLines[B-1].LineInfo[B 2]; “ A7
int nC_1 = AllLines[C-1].LineInfo[C 1]; 2XG
int nC 2 = AIILines[G=l].LineInfo[C 2];
SS
CurrWay. push_back (nA 1) CurrWay. ah ;
CurrWay. push_back(nB_1); CurrWay. 是 你 UrrWay. push_back CnB_2) ;
CurrWay.push-back (nC_1) ; CurrWay. push | CurrWay. push_back (nC_2) ;
CurrWay. push_back (fTotalTime) ; 洒
CurrWay. push_back(fTotalCost) ;
o
Respond. push_back ( 和 O 〇
】
return Respond; S
) 站
一
// 文件 输出 花费 时
void OutPutTi 中 & fout,
7, vector<vector<float> > & FeasibleSolve)
| 下
3 (inti=0; i<FeasibleSolve.size(); ++i)
VY/,
1S% for (int j=0; j<FeasibleSolvelil.size(); ++j)
{
fout << setw(3) << left <<setfill(C ’) << FeasibleSolve[il[j] <<” 7;
}
if (FeasibleSolve[i][3] == 3984 &&
FeasibleSolve[i][5] == 3993 &&
FeasibleSolve[i][2] == 87 &&
FeasibleSolve[i][6] == 3676)
44

<!-- source_page: 45 -->

回 成 革 动 国
后
0
BRLLT]
四
{
int a = i+l;
cout << a << endl;
}
fout << endl;
}
}
// 综合 处 理 时 间 ， 人 花费 ， 转 乘 次 数 。 并 将 结果 分 别 存 入 文件 中 。
void Time Cost_BusChangeTimes_Pro 二
-从 >
int nStart, int nEnd, // E-" 和 目标
/一
点
vector<LoadMessage> & AllLines, 人行 所 有 路 线
信息
vector<vector<int> > & AllBuses, // 所 有 公 汽
站 信息 S
vector<vector<vector<long> dCrossInfo // 任意 两 路 线 的
交叉 信息
)
{ [o]
char char_1[20]; 2 ee
char char 2[20] ; 从
itoa( nStart, char I, ;
itoa( nEnd ，char 2, ;
一 一
string * pStril.=.new string(char 1);
We string(char 2);
cs ="("+ * pStr_1+"="+ % pStr 2+")";
P fout ( (strPartName+“ 用 时 _ 费用. txt”).c_str() );
vector<vector<int> > FeasibleSolve 2; // 二 次 转 乘
TwiceBusChange (nStart，nEnd，FeasibleSolve 2, AllLines, AllBuses, RoadCrossInfo);
vector<vector<float> > A
= Time Cost Calculate (FeasibleSolve 2, AllLines);
OutPutTime Cost Cal (fout, A);
45

<!-- source_page: 46 -->

回 成 革 动 国
IE
0
BRiE]
EEn
}
10. 3. 2 (文件 名 : CalulateWays. h)
#include <map>
#include <iostream>
#include <vector>
#include “LoadMessage. h”
#include <fstream>
#include <queue>
using namespace std; 全
， =\sN
int aaaaaa ; 二
int bbbbbb ; 从 N
// 判断 一 条 线 上 两 点 间 是 否 是 上 下 层次 关系 ， 如 果 是 ， 确 定 EN
bool find(vector<int> &Line, const int NFIRST, const “NSECOND,
int &pos 1, int &pos 2) 全
{ 全
if (NFIRST == NSECOND)
{
int i =0; 和 @
IAAM
while (Line[i] != NFIR
{
+H;
}
~
pos_1 = \a i;
o,
下 好
1 aveFound ”= false;
01 IsDirectTo 1 = false;
for (int i=0; i<Line.size(); ++i)
{
if (Linel[i] == NFIRST)
{
IsDirectTo 1 = true;
pos 1 = i;
continue;
46

<!-- source_page: 47 -->

ERE
v u
EEEE
}
if (IsDirectTo 1 && Line[i] == NSECOND)
{
pos 2 = i;
bHaveFound = true;
break;
}
}
if ( !bHaveFound )
{ 全
pos_1 = pos_2.= -1; “ <
} =
return bHaveFound;
|
// 找 出 两 点 间 是 否 有 连 线 直接 连接 全
// 如 果 有 ， 则 返回 所 有 可 能 的 连 线 7
bool Direct_or_not (const int NSTART, const int NEND; // 起 始点 和 目标
点 @
0 > &ReasibleSolve, // 可 行 的 解
决 方案 ， 是 返回 值 5
vector<LoadMessag & AllLines, // 所 有 路 线
信息
vect or<int> > & AllBuses, // 所 有 公 汽
站 信息 ~
rvector<{vector<long> > > &RoadCrossInfo) // 任意 两 路 线 的
交叉 信息 “%, 了
( YL
mt
Jj=0
\b/
01 bHaveFound = false;
return bHaveFound;
}
// 一 次 换 乘 的 情况
bool OnceBusChange (const int NSTART，const int NEND, // 起 始点 和 目标
点
47

<!-- source_page: 48 -->

回 成 革 动 国
后
0
BRLLT]
半生 二
vector<vector<int> > & FeasibleSolve, // 可 行 的 解决 方
案 ， 是 返回 值
vector<LoadMessage> & AllLines, // 所 有 路 线
信息
vector<vector<int> > & AllBuses, // 所 有 公 汽
站 信息
vector<vector<vector<long> > > &RoadCrossInfo) // 任意 两 路 线 的
交叉 信息
{
bool bHaveFound = false;
vector<int> FeasibleLine(6, 0); 全
-Ke
=
int i, j, k; 二 \
和 %i
int nFirstLine = -1;
int nSecondLine = -1;
long nCurrValue = -1; 全
long nCurBridgel = -1;  // 上 行 方向 的 桥接 点 ~
long nCurBridge2 = -1;  // 下 行 方向 的 桥接 点
bool IsDirectToBridge =false; 自 // 起 始点 是 否 能 直达 中 转
点 (ej
bool IsBridgeDirectToDest = // 中 转 点 是 否 能 直达 目标
点
// 搜索 相交 的 两 条 线
for (i=0; i<ALlBuses[NSTART-1].size(); ++i) // 经 过 起 始点 的 所 有 线路
{
oo Joser [il;
和 经 j<Al1Buses[NEND-1]. size (); ++j) // 经 过 终点 的 所 有 线路
1 // nSecondLine = AllBuses[NEND-1][j];
// 两 路 线 的 公有 站 点
int nLinel = -1;
int nLine2 = -1;
if ( nFirstLine < nSecondLine )
{
nLinel = nFirstLine;
nLine2 = nSecondLine;
}
48

<!-- source_page: 49 -->

Ehis
asi
wsn
else
{
nLine2 = nFirstLine;
nLinel = nSecondLine;
}
for (k=0; k<RoadCrossInfo[nLinel-1][nLine2-1].size(); ++k)
{
// 桥接 点
nCurrValue = RoadCrossInfo[nLinel-1][nLine2-1] [k];
if (nCurrValue >= 10000) 二
2
if (npFirstLine == nLinel ) “\
{ 从 7
nCurBridge2 = nCurrValue % 10000;
nCurBridgel = (nCurrValue-nCu 2) //10000;
} 从 \
else 全
-
nCurBridgel = nCurrVa 10000;
nCurBridge2 = (nCurrValue-nCurBridgel) / 10000;
) @
} 2 外
else 从
{
nCu el = nCurBridge2 = nCurrValue;
}
一 一
=0, b=0, ¢=0, d=0;
人 和 en
为 = find (Al1Lines[nFirstLine-1]. LineInfo, NSTART, nCurBridgel, a,
下 和
e bool IsBridgeDirectToDest = false;
if ( IsDirectToBridge )
{
IsBridgeDirectToDest
= find(AllLines[nSecondLine-1].LineInfo, nCurBridge2, NEND, c,
d);
}
if ( IsDirectToBridge && IsBridgeDirectToDest)
49

<!-- source_page: 50 -->

马 :二
u
EeE
{
FeasibleLine[0] = a; FeasibleLine[1] = nFirstLine;
FeasibleLine[2] = b; FeasibleLine[3] = ci
FeasibleLine[4] = nSecondLine; FeasibleLine[5] = di;
FeasibleSolve. push back (FeasibleLine) ;
}
IsDirectToBridge = false;
IsBridgeDirectToDest = false;
}
} 全
全
:人 v
. . 2/ 一
if ( !FeasibleSolve.empty() )
bHaveFound = true;
return bHaveFound; A
} 全
全
op 多 和 mn
//
// 三 次 换 乘 的 情况 @
// A [¢]
// 由 于 第 一 问 解 是 第 二 题解 的 一 音 多 ersoomonmom
//
bool TwiceBusChange (cons NSTART, const int NEND, // 起 始点 和 目标
点
eecyor ector<int> > & FeasibleSolve, // 可 行 的 解决 方
案 ， 是 返回 值
人 aaaessaee & AllLines, // 所 有 路 线
信息 为
下 4 vector<vector<int> > & AllBuses, // 所 有 公 汽
村 = AS
1 // N| vector<vector<vector<long> > > &RoadCrossInfo) // 任意 两 路 线 的
ZREE
{
bool bHaveFound = false;
vector<int> FeasibleLine(9, 0);
int nCurLineName = -1;
int nFirstBusChangeStation = -1; // 第 一 次 换 乘 的 车 站 名
int i, j, k;
50

<!-- source_page: 51 -->

马 :二
u 3
EeE
i=j=k=0;
for (i=0; i<Al1Buses[NSTART-1].size(); ++i) // 经 过 起 始 站 点 的 所 有 线
路
{
nCurLineName = AllBuses[NSTART-1][i]; // 当前 路 线 名
for (j=1040; j<1044; ++j)
{
map<int, int> ToRailWay;
bool IsExist = false;
全
for (k=0; k<RoadCrossInfo[nCurLineName-1][j]. size(); HH <
of, \
if ( RoadCrossInfo[nCurLineName-1][j][k] >= 1
{
long nValue “= RoadCrossInfo[nCu e-1)15][k];
long nSecond = nValue % 10000;
long nFirst = (nValue-nSecor ) 000;
全
ToRailWay. insert ( make pai irst, nSecond) );
if (nFirst==87 && nSecond==3984)
{ ve, 外
int 5
}
ai.
}
-25 \V
X2" int>::iterator iter;
/
1 // [NA
// int nSize = ToRailWay.size();
// iter = ToRailWay. begin();
// cout << "Htf#gHEpHREHEIAE" (C end];
// while (iter != ToRailWay.end())
// {
// cout << iter—>first <<” ” << iter—>second << endl;
// iter ++;
// }
51

<!-- source_page: 52 -->

ERE
.
BRLLT]
回 共 Sakn
wsn
if ( !IsExist )
continue;
int m=0;
int nStart pos = -1;
iter = ToRailWay. begin();
for (mn=0; m<AllLines[nCurLineName-1].LineInfo.size() ; ++m)
{
if (AllLines[nCurLineName-1].LineInfo[m] == NSTART)
{ 全
nStart pos = mi “ <
a
break; \
】 7 8
iter = ToRailWay. To LineInfo[m]);
if ( iter != ToRailWay.end() ) 全
{ 全
ToRailWay.erase( iter ) ;
}
} [o]
/ |
while ( !ToRailWay. Enpty O)
{
int a = ay. size();
~
) Fali find( AllLines[nCurLineName-1].LineInfo[m] );
o,
MA int a= iter->first ;
下 20. _b = iter->second;
// if (iter->second == 3984 && iter->first == 87)
// {
// int y =0;
// }
if ( iter == ToRailWay.end() )
{
+m;
continue;
}
52

<!-- source_page: 53 -->

ERE
多
RE
vector<{vector<int> > temp;
OnceBusChange (iter->second,
NEND, temp, AllLines, AllBuses, RoadCrossInfo );
int c = temp.size();
for (int kk=0; kk<temp. size() ; ++kk)
{
FeasibleLine[0] = nStart pos ; FeasibleLine[1] = nCurLineName;
FeasibleLine[2] = m ; FeasibleLine[3] = temp[kk][0];
FeasibleLine[4] = temp[kk][1]; FeasibleLine[5] = k][2];
FeasibleLine[6] = temp[kk][3]; FeasibleLine[7] ts 1;
FeasibleLine[8] = temp[kk][5]; \
2/ 一
// int s = temp[kk][1]; 从 一
// int sl = temp[kk][0];
// int s2 = temp[kk][1];
// int s3 = temp[kk][2]; 全
// int s4 = temp[kk][3]; 人
// int s5 = temp[kk][4];
//
// if (M1Lines[FeasibleLine[4]-1]. LineInfo[FeasibleLine[3]] ==
3984 && [o]
// eereomrm ==
3993 )
// {
// =0;
[/ 一 -7
人 YVosiesoee push_back ( FeasibleLine ) ;
%
ToRailWay. erase ( iter );
WS~-
}
}
if ( !FeasibleSolve.empty() )
bHaveFound = true;
return bHaveFound;
}
53

<!-- source_page: 54 -->

回 成 革 动 国
后
0
BRiE]
四
10. 3. 3 (文件 名 : DataPreProcess.h)
#include <vector>
#include <iostream>
#include <string>
#include “LoadMessage.h”
#include “Utility.h”
using namespace std;
全
// 将 公 汽 线路 信息 及 公 汽 站 点 信息 存 入 数 组 中 。 二 <
void AddBusStationsAndLines(vector<LoadMessage> & AllLines, 二 \
vector<vector<int> > & AllBuses) /
{
ifstream fin("1.1 AR&EHEE. txt”); A
string strCurrLine ="7;
全
全
String StrBusLine ="" // ARE
string strPrice = // 票 价 信息
string strUpLoad = ”; // 上 行路 线
string strDownLoad = ""; 2 // 下 硬 路 线
string strRoundLoad = ""; ran
bool  IsRoundWay ”= false; /判断 当前 读 入 的 路 线 是 否 为 环形 路 线
for (int nCount=0; nC ; ++nCount)
{ 一
IsRoundW. 访 ”
o,
// i y 11Lines[1403]. LineInfo. size() ;
// N
/ if (e==2)
// c = ci
// }
// 读 入 路 线 名
do {
getline (fin，strCurrLine，ANm ) ;
} while(strCurrLine == "");
strBusLine = strCurrLine;
54

<!-- source_page: 55 -->

Ehis
EeE
wsn

// 读 入 计 费 标准

do {

getline (fin，strCurrLine，ANm ) ;

} while(strCurrLine == "");

strPrice = strCurrLine;

// 读 入 上 行路 线

do {

getline (fin，strCurrLine，ANm ) ;

} while(strCurrLine == ""); 从
=iK2
=\SS

string temp(strCurrLine, 0, 6); \

2/ 一

// 环形 线路 3

if ( temp ==“ 环 行 : ”) 任

{

strUpLoad = 人; 全

strDownLoad = ""; |

strRoundLoad = string(strCurrLine, trCurrLine. length()) ;
IsRoundWay 一 = true;

} [o]

// 开行 全 放下 二 区 (ej

else if( temp == 2

{

strUpLoad ring(strCurrLine, 6, strCurrLine.length());
strRoundLoad
一 一
LA] 征 路 线
一 A)Y
% getline(fin, strCurrLine,’ \n');
下 Green ="");
1 // strDownLoad = string(strCurrLine, 6, strCurrLine.length());

}

// 下 行 线路 是 上 行 线路 的 逆 方 向

else

{

strUpLoad = strCurrLine;
strDownLoad = "";
strRoundLoad = ””;

}

55

<!-- source_page: 56 -->

回 成 革 动 国
ME 用
;这 2
ER
// 构造 同一 路 线 分 成 的 两 个 路 线 ， 并 把 它们 存 入 容器 中
LoadMessage currLoad up; // 当前 路 线 的 上 行路 线
LoadMessage currLoad_down; // 当前 路 线 的 下 行路 线
currLoad_up. nLineName = StrTolnt ( string(strBusLine, 1, 3) );
currLoad up. strPrice = strPrice;
currLoad_up. bRoundLoad = IsRoundWay;
currLoad_down. nLineName = currLoad _up. nLineName + 520;
currLoad_down. strPrice = strPrice;
currLoad_down. bRoundLoad = IsRoundWay;
o
]/ 环形 路 全 “ 伏 >
if ( IsRoundWay ) \)
2
RoundRoadCal (strRoundLoad, currLoad up. nLineName， 国志
currLoad up. LineInfo, currLoad down.Li ) ;
| 各
// 非 环形 路 的 二 行路 DA
if (strUpLoad != "")
{
BusRoadCal (strUpLoad, ( currLoad_up. nLineName, AllBuses,
currLoad up.LineInfo) ; Ve, |
A
// 非 环形 路 的 下 各 路 过
if (strDownLoad q
1 一 )
BusR trDownLoad, currLoad_down. nLineName, AllBuses,
currLoad_downgLinelnfo) ;
7
e /is TRI )
Ye-
1 // ReverseRoadCal (strUpLoad, currLoad_down. nLineName, AllBuses,
oh on LineInfo) ;
}
AllLines[currLoad up.nLineName-1]  = currLoad up;
AllLines[currLoad down.nLineName-1] = currLoad down;
】
}
// 将 地 铁 线路 信息 及 地 铁 站 点 信息 存 入 数组 中 。
56

<!-- source_page: 57 -->

回 成 革 动 国
后
0
BRLLT]
回 共 Sakn
void AddRailWayStationsAndLines (vector{LoadMessage> & AllLines,
vector<vector<int> > & AllBuses)
{
// T1 线路
for (int i=1; i<24; ++i)
{
AllLines[1040]. LineInfo. push_back (3957 + i);
AllLines[1041]. LineInfo. push_back (3957 + 24 - i);
Al1Buses[3956+i]. push_back (1041) ;
Al1Buses[3956+i]. push_back (1042) ;
} 全
>
ifstream fin( 地铁 线 路 了 2 信息 . txt”); \
. 2/ 一
int nValue = -1; 从 一
for (i=3956+24; 1<3996; ++i)
{
AllBuses[i]. push_back (1043) ; 全
AllBuses[i]. push_back(1044) ; 人
}
Al1Buses[3956+12]. push_back (1043) ; °)
Al1Buses[3956+12]. push_back 4 [o]
Al1Buses[3956+18]. push_back
Al1Buses[3956+18]. push_back (1044)
vector<int> temp_1;
vector<int> temp_2;-
// T2 ) V
for«(i 8; ++i)
{
fin nValue;
1 // mp_1. push_back ( 3957+nValue );
int nLSize = temp l.size();
AllLines[1042]. LineInfo. resize ( nLSize#x2，-1 ) ;
AllLines[1043]. LineInfo. resize ( nLSize*2, -1 );
for (i=0; i<nLSize; ++i)
{
57

<!-- source_page: 58 -->

马 :二
了
AllLines[1042].LineInfo[i] = temp_1[i];
All1Lines[1042].LineInfo[nLSize+ 订 = temp 1[i];
AllLines[1043]. LineInfo[nLSize-1-i] = temp_1[il;
AllLines[1043]. LineInfo[nLSize+nLSize-1-i] = temp 1[il;
】
}
10. 3. 3 (文件 名 :ShortPathCalculate. cpp)
[LU
%
//。 此 程序 计算 最 小 公交 线路 =“
[/ z “AN
// 有 关 要 求 : 用 户 输 六 起 始 站 点 和 终点 ， 在 满足 换 乘 次 数 不 超 过 某 一 自 度 的 情 闸 下
// 程序 输出 所 有 可 能 的 行车 路 线 ]
// /人
[LUIANNMAAAAAAAAAL 和 [AAA 全 JI1111117117
#pragma warning(disable: 4786) JR
#include “map>
#include <iostream» @
#include 《fstream> 4 |
#include <strstream> 多
#include <string>
#include <queue> S
#include <vector> )
//#include “Utility ¥
#include “DataPr h”
#include “Ca 中
KE h”
Us Danes e std;
1 J/ \=
No
{
// 经 过 事先 的 计算 ， 总 共有 520 条 公 汽 线路 , 3957 个 公 汽 站 点
// 2 条 地 铁 线路 ，39 个 地 铁 站 点
//
// 将 同一 路 线 的 上 、 下 行路 线 看 成 两 个 不 同 的 路 线
// 将 环形 路 线 换算 成 两 个 与 之 等 价 的 单行 路 线
// 将 地 铁 线 等 同 于 公 汽 站
vector<LoadMessage> AllLines (1040+4) ;
58

<!-- source_page: 59 -->

回 成 革 动 国
和 让
0
BRiE]
四
vector<vector<int> > AllBuses(3957+39) ;
// 从 文件 读 入 公交 线路 和 站 点 信息 ， 并 存 入 数组 。
AddBusStationsAndLines (Al1Lines, AllBuses);
// 将 地 铁 站 点 信息 和 地 铁 线路 信息 存 入 数组 中 。
AddRailWayStationsAndLines (AllLines, AllBuses);
// 1044%1044 的 矩阵 ， 里 面 存 储 相对 应 的 线路 之 问 的 重合 站 点 信息
vector<vector<vector<long> > > RoadCrossInfo;
// 任意 两 条 线路 间 相 交 间 相交 项 点 信息 “
RoadCrossInfo = CalRoadCrossInfo( AllBuses ) ; “ <
o,
int nStart = -1; <
int nEnd = -1;
for (int i=0; i<200; ++i) A
{ 全
cout << “请 输入 起 始 站 点 : ” ; |
cin >>nStart >> nEnd;
Time Cost BusChangeTimes_Pro (nStart, nEnd, AllLines, AllBuses,
RoadCrossInfo) ; Ve, (ee
”3
}
一 一
7 "
59

