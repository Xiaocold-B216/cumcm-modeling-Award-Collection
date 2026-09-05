# Extracted Paper

<!-- source_page: 1 -->

口 | 到 口
ai
第 20 卷 第 7 期 工 程 数 学 学 报 Vol.20 No 7 2
2003 年 2 月 JOURNAL OF ENGINEERING MATHEMATICS De 2
文章 编号 :1005-308$(2003)07-0083-07
4 六 » FL、
露天 矿 生 产 车 辆 安排 计划 优化 设计
龙 建成 ， 许 鹏 ， 圳 月 明
指导 教师 王 兵团
(北京 交通 大 学 ,北京 100044) 从
一 SS
earenpsoos ngateaTeor ren 一 Mnara
变化 范围 ,这 对 实际 操作 是 有 益 的 ， / ) -AH
摘 要 :本 文 结合 露 天 矿 0 基于 整数 规划 的 线路 车
次 安排 数学 模型 ， 利用 线性 规划 对 电 铲 进行 初始 布点 ,实现 对 模型 人 i fs 加 可 模型 的 求解 考虑 到 电 铲
利用 率 很 难 达到 1 ,为 提高 模型 最 优 解 的 实际 应 用 的 可 行 性 , 增 T  Ih 性 ,设置 了 电 铲 的 最 大 利用 率 。
为 保证 电 铲 有 一 定 的 利用 率 ,设置 了 电 铲 最 小 利用 率 。 (Goewexmoanr
关键 词 :车辆 安排 ;露天 矿 ;整数 规划 ;优化 设计
分 类 号 : AMS(2000) 90C05 中 国 分 类 号 : 0221;P57:P58 文献 标识 码 : A
N O
1 问题 提出 ( 略 ) 4 o
2 基本 假设 %,
DIE SEREAEREH BRK, FERARA—0 ARBA —88
2) 车 载重 ,平均 运行 速 全 二 车 耗 油 量 与 时 间 成 正比
3) 总 体 上 看 ,卡车 空 硅 走 行 时 间 与 重 车 走行 时 间 相同
人 人 区 人 PT 全 生生 ER—FRTE SHETIRE,
H—Ehpn 倒 点 位 置 不 变 ;
中 下 和 人 轩 人
3 向 题 分 析
全 1 通过 对 题 B 的 仔细 分 析 我 们 得 出 以 下 几 点 重要 信息
@ 每 个 铲 位 ( 装 车 点 ) 最 多 只 能 安排 一 台电 铲 并 只 能 为 一 辆 卡车 服务 ;每 个 印 点 也 只 能
同时 服务 一 辆 卡车 , 它 分 为 矿石 印 点 (只 能 印 矿 石 ) 和 岩石 印 点 (只 能 印 着 石 );
@ 对 于 矿石 印 点 ,矿石 铁 含量 要 满足 品位 (已 知 ) 要 求 ;
@@ 在 一 个 计划 内 卡车 原则 上 不 多 许 等 待 , 也 就 是 说 卡车 可 以 充分 有 效 利用 480 分 钟 完
成 装 车 -> 运行 - > 印 车 - > 运行 的 循环 过 程 ;
人 @@ 装 车 点 (外 点 ) 一般 不 能 480 分 钟 都 装 车 ( 印 车 ), 它 要 受到 卡车 接续 的 影响 。
3.2 约束 分 析

<!-- source_page: 2 -->

84 工 B 数 学 学 报 第 20 卷 2

分 析 原 则 1 和 原则 2 ,它们 都 是 以 一 定 的 优化 准则 来 编制 计划 ,优化 过 程 都 要 受到 一 定
的 条 件 约束 ,分析 归 纳 发 现 约束 主要 分 为 以 下 几 类 :

人 @@ 能 力 要 求 : 包 括 装 车 点 ( 铲 位 ) 对 矿石 和 岩石 的 供应 能 力 , 装 车 能 力 ; 务 点 的 卸车 能
力 ; 卡 车 的 运输 能 力 。

@@ 品位 要 求 :一 个 计划 内 同一 外 点 铁 矿 石 的 平均 铁 含量 在 0.285 ~ 0.305 之 间 , 电 铲 的
利用 率 不 能 太 低 ,要 大 于 其 最 低 利用 率 。

@@ 设备 数量 要 求 : 电 铲 数量 和 卡车 数量 不 能 超过 现 有 设备 数量 。

3.3 模型 建立 基本 思路

对 于 优化 模型 一 般 过 程 是 :确定 求解 变量 、 确 定 目标 函数 、 确 定 解 的 可 行 域 (约束 条 件 )。
依据 要 求 我 们 需要 求解 的 变量 有 从 铲 位 7 条 :和 上 的 中 下 从
划 出 动 的 电 铲 台数 ns(B) 和 卡车 辆 数 xce( 辆 )。 如 果 可 以 求 出 rv 的 话 志 也 时 多 定 了 ,因为
蓝天 0 时 , 铲 位 7 分 配 了 电 铲 ; 同 时 Ce 运送 车 次 、
区 aa 480 分
作 和 有 和 化 可 以 从 安 和 -和 上 分 人 人 下 的 核心 是 对 rz; 的 求解 。
zi 表示 的 是 车 次 所 以 zy To
小 和 出 动 最 少 的 卡车 ,同时 实现 这 两 个 目标 是 很 困 的 5 但是: 们 可 通过 求解 满足 运 量 最 小
目标 后 ,对 求 得 的 解 进行 优化 分 析 得 到 最 少 卡 车 数 。 模 型 可 行 域 主要 由 前 述 三 类 约束 确定 。
对 于 原则 2, 要 实现 产量 最 大 在 此 基础 上 使 得 岩石 产量 最 大 化 ,最 后 进一步 优化 使 得 癌 运 量
最 小 * 可 见 该 原则 得 到 的 模型 应 该 是 声 信 朋 有 优先 级 顺序 的 多 目标 规划 问题 第 一 级 目标 函
数 ( 主 目标 函数 ) 的 可 行 域 与 原则 多 aranm acanwaatApa 的 可
行 域 是 主 目标 函数 最 优 的 所 在 解 的 集合 ,第 三 级 目标 函数 (次 从 目标 函数 ) 的 可 行 域 是 从 目
标 函 数 最 优 的 解 所 有 解 的 集合 NI

ns < Ns rs 性 表达 式 描述 ,要 满足 该 约束 ,可 以 对 铲 车 进行 初始 布
点 , 即 初始 设置 zs 7
与 整数 规划 相近 的 解 ) 我 们 认为 铲 车 利用 率 低 的 铲 位 应 该 优先 考虑 不 设 产 车 。

二

RN 折 环 知 铲 车 最 大 利用 率 ) < 1 ,对 》 参数 的 选取 对 最 终 解 的 可 行 性 或 解 的 弹性 有
Tanaeenn TaaEOe 的 选取 可 以 根据
实际 需要 选取 。R = 4804/tw 一 般 取 [0.75,0.95]( 参 考 ) 比较 合适 。 铲 车 设备 昂贵 ,运行 费
用 较 高 ,因此 铲 车 的 利用 率 要 达到 闪 值 w 后 使 用 才 有 利 ,一 般 六 取 [0.35,0.55]( 参 考 ) 比较
合适 。 铲 车 最 大 利用 率 依据 服务 的 卡车 数量 不 同 而 有 差异 ,一 般 服 务 的 卡车 数 越 多 ,其 最 大
可 利用 率 越 大 。 各 印 点 的 最 大 能 力 S 可 以 采用 铲 车 的 标准 取 S = 480 /td。
4 “基本 符号 说 明

i :表示 各 外 点 编号 ,编号 按照 先 矿 石 印 点 后 岩石 外 点 ;

5 :表示 各 铲 位 对 应 的 铲 位 号 ，

U、V、T、D: 分 别 表 示 矿 石 印 点 集合 .岩石 印 点 集合 、. 铲 位 集合 . 铲 车 布点 集合 ;

zi 表示 从 铲 位 ) 到 外 点 ;线路 上 的 运输 次 数 ( 次 );

<!-- source_page: 3 -->

加 车 二 本
第 7 其 露天 矿 生产 车 辆 安排 计划 优化 设计 85
已 :表示 卡车 从 铲 位 ; 到 印 点 ; 的 平均 运行 时 间 (min) ;
o: 表 示 卡 车 从 铲 位 ) 到 印 点 ! 在 一 个 计划 内 的 最 大 运 量 ,也 就 是 一 辆 卡车 在 一 个 计划
内 只 进行 铲 位 ) 到 外 点 ; 的 运输 时 能 够 完成 的 最 大 运 量 (车 次 )
屿 :表示 从 铲 位 ; 到 印 点 ; 需要 的 最 少 卡车 数 ( 辆 );
mu、 站 及 :分 别 表示 铲 位 ) 矿石 量 (车 次 )、 涯 石 量 (车 次 ) 和 铁 含量 ;
dj: 表示 个 点 ; 的 最 低产 量 (车 次 ) 要 求 ;
67.07 :分 别 表示 印 点 ;的 最 低 和 最 高 品位 限制 ,其 中 ieE Us
w\ 地 ;分别 表示 平均 装 车 时 间 和 平均 卸车 时 间 ; _
Ns、Ne :分 别 表示 电 铲 总 台数 和 卡车 总 辆 数 ( 辆 ); -从
nsne :分 别 表示 一 个 班次 的 生产 计划 出 动 的 电 铲 台数 ( 台 ) 和 卡 节 辆 数 (全 让
Pb: 分 别 表示 卡车 载重 和 平均 速度 ; AGE
R、S :分 别 表示 铲 位 最 大 装 车 能 力 (车 /班次 ) 和 印 点 的 最 2 5 /班次 );
》、&: 分 别 表示 铲 车 的 最 大 利用 率 和 最 低 利用 率 ; XSN
CS
5 ”模型 建立 及 模型 优化 算法 多
无 论 是 采用 原则 1 还 是 原则 2 都 需 要 确定 卡车 的 数量 及 运用 ,都 可 以 根据 运 量 合理 安
排 卡车 ;因此 ,卡车 的 数量 及 具体 运用 在 求 得 千张 路 上 各 运输 次 数 前 不 用 考虑 ,通过 求解 得
到 总 运 量 以 及 各 线路 的 运输 量 , 然 夺 用 优化 模型 得 到 卡车 数量 以 及 运用 方案 。
5.1 建立 车 辆 安排 模型 A 】
@ 原则 1 , 即 总 运 量 最 有 动 最 少 的 卡车
因为 卡车 不 等 待 ,所 以 卡 毗 娄 由 总 运 量 确定 确定 了 最 小 运 量 模型 也 就 解决 了 卡车 数 的 派
用 。 由 前 面 分 析 可 知 ,地 辆 安 徘 是 一 整数 规划 问题 ,得 到 总 运 量 最 小 的 车 辆 生产 计划 安排 模型 如
下 : “27 > Sre (0)
IEUUYVIET
sth 73 <m, YieT (1)
OVOIASE
IJA2 ov 过- JET (2)
13 人 多
NA， 2 > 9 ViEUUY (3)
JE 了
ms<R VieT (4)
iEUUYV
>xy=480u VieT (s)
EUUY
> 去 S vieuuv (6)
JET
Ta 一 bi 之 0 VieU (7)
JE 了 JET
2 时 2r 和 0 VieUu (8)
JE 了 JET
ns < Ns (9)
ST SCe + 21,) 1, <480NC (10)
1€EUYVET

<!-- source_page: 4 -->

EE
86 T 程 数学 学 报 第 20 卷 7
2 0, 且 为 整数 ViceUUV,jEeT
(1) (2) 分 别 表示 各 铲 位 对 岩石 和 矿石 的 供应 能 力 约束 ,(3) 描述 了 各 印 点 满足 最 低产
量 的 约束 ,(4) (5) ,(6) 分 别 表示 了 铲 点 和 外 点 装卸 能 力 的 约束 ,(7)、(8) 表示 各 矿石 印 点
对 品位 的 约束 ,(9) (10) 分 别 表示 铲 车 ,卡车 使 用 数量 的 约束 。
@ 原则 2 ,充分 利用 设备 获得 最 大 产量 ,岩石 产量 优先 ;在 产量 相同 的 情况 下 , 取 总 运 量
最 小 ;由 前 面 分 析 可 知 要 解决 的 问题 为 一带 优 先 级 的 多 目标 规划 问题 ,建立 模型 | 如 下 :
产量 最 大 得 到 主 目标 函数 :
max x1 = 之 > ri (11)
elyvyer
岩石 产量 尽 可 能 大 得 到 从 目标 函数 次
max >2 = > > 一 So
i€V,ET
运 量 最 小 得 到 次 从 目标 函数 ， 2
min x3 = >， > Potry p od (13)
EUUV,ET p
该 模型 的 约束 条 件 与 模型 or 又 同时 达到 以 上 三
个 目标 的 解 就 是 最 优 解 。 |
® 卡车 数 的 确定 RD
的 确定 人 车工 人 站 上 于 人 人 所 以 卡车 尽量 用 足 8 x 60 =
480(min) ,卡车 数 确定 如 下 :
me = [ > Do(u +28,)e,/480)5 1 (14)
E€UUV,ET 从 Va O
各 条 线路 上 卡车 数 , on 人 z 和 cj ,有
ny € Lay/eys ay/e, +1 ) (15)
5.2 和 | 一
模型 [不 考虑 约束 条 件 (9 和 snake
后 得 到 的 的 线性 整数 巴 苛 神 型 .为 了 使 得 模型 的 解 满足 约束 条 件 (9) ,可 以 先进 行 铲 位 的 初始 布
eg 个 铲 位 作为 铲 车 的 安置 点 ,此 时 有 内 = No ,然后 对 模型 工 进行 简
化 ,去 掉 不 共和 LINDO 软件 对 简化 后 的 模型 求解 。
3 化 算法
je 车 初始 布点 ,布点 方法 是 对 模型 (10) 去 除 约束 条 件 (5)\(8) 和 去 掉 变 量 整
下 性 规划 的 解 r ,计算 各 铲 位 的 能 力 利用 率 ,按照 利用 率 从 高 到 低 取 Ns 个 铲 位 作
为 初始 点 。
第 2 步 ; 依 据 初 始 布点 对 模型 进行 简化 ,去 掉 没 用 的 变量 和 精简 约束 条 件 。
第 3 步 ; 对 精简 后 的 模型 不 含 约束 条 件 (8) ,含有 约束 条 件 (5); 采 用 LINDO 软件 求 整数
规划 解 。
第 4 步 :利用 得 到 的 最 优 解 求 其 它 值 。
四 模型 | 的 求解 算法
第 1 步 :采用 模型 [的 算法 获得 铲 车 布点 并 精简 模型 ,得 到 模型 的 最 优 解 xy 和 目标 函
数值 7 。
第 2 步 :对 上 一 步 的 精简 后 的 模型 的 约束 条 件 汪 加 约束 >， mn = xy 作为 从 目标 函

<!-- source_page: 5 -->

二
第 7 期 露天 矿 生产 车 辆 安排 计划 优化 设计 87
数 的 约束 条 件 ,并 求解 得 到 模型 的 最 优 解 xy 和 目标 函数 值 *y 。
第 3 步 :对 上 -- 步 模型 的 约束 条 件 加 入 约束 > > 'z = zx; 作为 从 目标 函数 的 约束 条
iEV,ET
件 , 并 求解 得 到 模型 的 最 优 解 xy 和 目标 函数 值 =y 。
6 ”模型 求解
6.1 模型 参数 的 确定
印 点 编号 为 :1 矿石 漏 ,2 个 装 T ,3 个 装 芽 ,4 岩 场 ,5 岩石 漏 ;矿石 印 点 集合 U = 11,2，
3 ,着 石 印 点 集合 V = 14,5| , 铲 位 集合 T = 11,2,，…,101。 依 据 铲 位 和 各 印 点 之 间 的 平均
走行 时 间 与 得 到 卡车 在 一 个 计划 内 的 平均 最 大 运 量 cy 如 表 1 : ARD
£1 铲 孝 点 最 大 运 量 一 览 表 <
[ETTETTFE3TEATESTEOTETTYESTFE9|yED
7e6 15 5 iT 19 | 五 | 324 二 | 下 4
恒 村 动 T| 39 | 3 | 2 [全 3 5 | 为
便于 区 9 2 2 | 六 二 45
着 有 TS
E3338 村 | 35 二 和 | 5
将 上 表 铲 位 矿石 岩石 数量 转化 成 可 运 车 数 wj( 基 次 ) 上 (车 次 ) 如 下 表 2:
表 2 铲 位 最 大 供应 9 AS
[TY 和 全 [$E4] PES [BEG|PET|PRE] FEI[PET
CA EU
[o30 10.58 [59 [p [03 [0% [00 {o3 [05 [om
产量 要 求 ; 矿 石 漏 1.2 万 吨 、 便 装 世 下 1.3 万 吨 \ 合 装 场 1.3 万 吨 、 涯 石 漏 1.9 万 吨 , 涯
场 1.3 万 吨 。 其 它 参 数 :ta = 5(min) 久 由 amin JNs =7、Nc=20、P=154( 吨 /车 )、.v
=28(km/h)\tt =3+5 in);
6.2 求解 模型 站
@ 采用 线性 规划 获得 铲 位 初始 布点
SESRBAL RIRANTERS PRBRRASEIHE HUER = 0.
85 ,对 最 低 利用 多 说 信 控 制 为 k = 0. 50。 殷 模型 参数 代 人 模型 了 ,按照 算法 得 到 线性 规划 的
解 见 表 3 汶 尼 /作坊 中 利用 率 都 是 指 铲 车 的 和 用 率 )，
SSNA 表 3 模型 工 线 性 规划 初始 解
TIEFETTEITYE3TEITESTEETYETTYESTE9TIETIT 于
SR 7 | | | | es 5
ER| 148 35 | ®
便装 45  N  S N N 0X1%
区
85 有 | To TD  Tu
人 计生
AAE [om|07i |0 ow DT
根据 能 力 利用 率 得 到 初始 布点 :D = 11,2,3,4,8,9,101; 用 LIJNDO 求解 简化 模型 得 到
解 见 表 4( 各 线路 上 的 运输 次 数 z ) 为 :
此 时 ,D = 11,2,3,4,8,9,101,z” = 83975.5( 吨 ,公里 ), 电 铲 台 次 ns = 7( 台 ) ,由 公
式 (13) 计算 得 到 卡车 的 使 用 数量 :xx = [12.46] + 1 = 13( 辆 )。
@ 铲 车 最 大 利用 率 为 1
此 时 ) = 1.00, 对 最 低 利用 率 阔 值 控制 为 & = 0.50; 按 照 前 面 的 算法 计算 得 到 铲 车 初

<!-- source_page: 6 -->

了
88 工 程 数 学 学 报 第 20 卷 2
始 布点 结果 :D = {1,2,3,4,8,9,101,2" = 82757.4( 吨 . 公里 ), 电 铲 台 次 mw = 7( 台 ), 由
公式 (13) 计算 得 到 卡车 的 使 用 数量 :nc = [12.39] + 1 = 13( 辆 )。
表 4 模型 [ 各 线路 运输 次 数 一 览 表
[ETTYS3TYRITYS4TEST9EOTATTASTYE9TREIOT 全
358T | 316 ] | | 2 7
ak%T 3 | 人 | |
人 ka | az | | [Ts
5 | [45
3
人 寺  N
利和 | 58 | 05 0s [Gm| | |  low|ow|osow
@ 铲 车 最 大 利用 率 为 1, 最 低 利用 率 为 0 MAR >
即 ;= 1.00, 对 最 低 利用 率 阅 值 控制 为 & = 0.00; 按 照 前 面 的 算法 计算 得 到 鳍 车 初始
布点 结果 :D = 11,2,3,4,8,9,10|,z” = 22412.4( 临 公里) , 电 销 有 次 m 7( 台 ), 由 公
式 (13) 计算 得 到 卡车 的 使 用 数量 ;ne = [12.35] + 1 = 13( 辆 )。 也 一
比较 四 种 解法 会 发现 解 @ 的 目标 值 最 小 ,日 标 的 优化 和 交 和 高 ,但 是 其 部 分 铲 车 利用
率 高 如 铲 位 10 利用 率 达 到 1 了 ,这 种 解 一 般 是 不 可 行 的 ,此 和 侠 诈 章 用 很 不 均衡 ,造成 解 的
RIEDR @ 锐利 用 素 相 对 更 均 有 但是 同样 存 胡 和 小 .可 行 性 差 。 解 © 铲 车 利用
率 相对 比较 均衡 ,可 行 性 良好 、 弹 性 大 且 目 标 函 数值 蓝本 OH 关 不 是 待 别 大 综合 比较 可 以
选取 @ 作为 最 优 解 。 对 结果 的 解释 是 ;要 用 一 定 的 函数 目标 值 的 增 大 来 换取 解 的 弹性 和 铲
车 利用 的 均衡 性 。 .
3 次 计算 得 到 产量 相同 ,矿石 漏 /2012 万 吨 \ 侠 装 场 1.309 万 吨 \ 图 装 场 1.309 万
FER 1.9096 万 吨 、 尝 场 1.309 和 p 红 确 定 各 条 线路 上 的 卡车 数 由 (14) 式 计算 得 ，
< 志 5 模型 工 各 线路 卡车 数 一 览 表
[#61]¢ao] Faalwns | 名 位 5 | 急 位 6 | 锌 位 7 | 全 位 8 | 铲 位 9 | 季 位 10
9A 肖 | | 1 1 | | 3 |
全 攻 芭 I| _ 一 2 | | |
4 RE | | | |:
2 | | 3
#HApI | | 2 | | | | [ 1 ]
6.3 求解 模型 /T
1 交 和 拓 天 和 本 表 了 并 去 的 束 GO) 采用 线性 规划 方法 进行 初始 布点 得 到 :D =
HS,9101;, 用 LINDO 求解 简 化 借 弄 ,设置 = 0.90,w = 0.50, 得 到 最 优 解 有 目标 人 := ~
602( 车 次 ), 更 改 目标 函数 为 (12) 加 入 约束 ) Dz, = 602 用 LINDO 和 解 得 最 优 解 目标 值 :cy =
iEUUVIJED
288( 车 次 ) ,更 改 目标 函数 为 (12) 加 入 约束 > > ,zi = 288 用 LINDO 解 得 最 优 解 ，
IEYJIED
此 时 ,D = 11.2,3,0.8.9,100,2{ = 126258( 吨 /公里 ), 电 铲 台 次 ns = 7( 台 ) ,由 公 趟
(13) 计算 得 到 卡车 的 使 用 入 :ac = [14.92] + 1 = 15( 辆 )。 考 虑 到 电 铲 和 卡车 利用 率 都 和
高 ,为 了 提高 解 的 可 行 任 和 “此 过 议 卡车 数量 增加 一 辆 取 16 辆 。 计 算得 到 产量 相同 :矿石 漏
1.232 万 吨 、 倒 装 场 [2.2176 万 吨 、 倒 装 场 [1.386 万 吨 、 岩 石 漏 2.2176 万 吨 、 岩 场 2.2176
万 吨 。

<!-- source_page: 7 -->

二
第 7 期 露天 矿 生产 车 辆 安排 计划 优化 设计 89 一
未 6 模型 工 各 线路 运输 次 数 一 览 表
[FEITPEITESTREITAESTPROTETTPESTE9 NI
538 |
BR5T SO IT TI
wEL  1 w [ [[ [wl _ww
#  ”  Tlu [owe w
E37-8TO  E H SO
人 证 66- Tw | | 西关 二 而 二 而 十 好
有 10 [Too [DT | | 50500590 097
@ 确 定 各 条 线路 上 的 卡车 数 由 (14) 式 计算 得 :
表 7 模型 卫 各 线路 卡车 数 一 览 表
FEETTE2TE3TEITESTEGTETTESTFEORE
FF | | | >
TI IT
aa 2 | 由
# 区 | TH
2
7 模型 优 缺 点 及 改进 AS)
7.1 模型 的 优点 SN
@ 综 合 利用 了 Mathematica 和 LINDO 两 个 软 传 f 分 别 兴 线性 规划 和 你 数 规划 的 角度 对
模型 进行 综合 求解 简化 模型 N
@ 充 分 利用 模型 目标 函数 约束 条 件 的 线形 关系 ,采用 两 种 方法 分 别 对 模型 简化 ,增加
了 求解 的 对 比 度 ; MA e
有 好几 作 人 因果 和 人
7.2 模型 的 缺点
0 枯 全 本 和 用 有 人, 前 可 一
@ 模 型 尽管 据 供 了 多 方 寅 也 选 , 但 各 方案 独立 ,同一 方法 不 能 得 出 多 重 最 优 解 ;
@@ 模 型 约束 条 人 和 -人 工 计 算 困难 。
7.3 it
@ 对 构 型 约 壳 条 件 的 措 述 ,以 线性 关系 式 描述 铲 车 不 超过 总 铲 车 数 的 要 求 ;
Xe 法 改进 ,选择 更 优秀 的 软件 ,尽量 实现 多 重 最 优 解 的 获取 以 对 多 方案 对 比
二
| 和- 上 简化 模型, 诚 小 模型 的 求解 规模 。
参考 文献
[1] 运筹 学 教材 编写 组 ,运筹 学 [ M] .北京 :清华 大 学 出 版 社 ,1990
[2] 苟 飞 . Mathematica4 实例 教程 [M] .北京 :中 国电 力 出 版 社 ,，2000
[3] 姜 启 源 . 数 学 模型 [ M] .北京 :高 等 教育 出 版 社 ，1993
[4] 时 其 孝 . 数 学 建 模 教育 与 国际 数学 建 模 竞 赛 , 中 国 工业 与 应 用 数学 学 会 (工科 数学 ?杂志 社 ,1994
[5] sky. 走 进 LINDO 世界 .http;//hanqing. yesky. com/20030116/1648793. shtml, 2003
(下 转 142 页 )

<!-- source_page: 8 -->

:
本 吕
中
142 工程 数学 学 报 第 20 卷 7
PNGUPRPRRPPPPRRUU
生 数 学 建 模 竞赛 的 题 型 和 方法 ,在 我 院 举办 了 预赛 ,参赛 队 达到 了 38 个 , 收 到 了 预期 的 效
果 , 达 到 了 提前 练兵 的 目的 。

4) 加 强 学 术 交流 ,举办 全 国盛 会 。 为 了 加 强 我 院 的 数学 建 模 教学 工作 ,吸收 全 国 兄弟 院 校
的 教学 经 验 ,加 强 学 术 交 流 。 今 年 8 月 ,由 我 院 和 大 连理 工大 学 承办 了 中 国 工业 与 应 用 数学 学
会 数学 模型 专业 委员 会 和 全 国 大 学 生 数学 建 模 竞赛 组 委 会 的 “第 八 届 全 国 数学 建 模 教学 与 应
用 会 议 ”全国 的 400 多 名 代表 欢聚 一 党 ,开展 了 广泛 的 学 术 交 流 ,我 们 从 中 获 益 非 浅 。

5 结论

全 国 大 学 生 数学 建 模 竞赛 活动 已 成 为 全 国 高 等 学 校 中 规模 最 大 的 课外 种 技 活动 ,直接
” = | 、 人 MURc h
影响 和 推动 着 全 国 高 等 教育 ,特别 是 数学 科学 与 素质 教育 的 发 展 。 我 院 学 员 通 过 矢 加 这 项

全
竞赛 活动 ,能 够 提高 他 们 的 综合 素质 ,将 对 我 院 创办 综合 性 院 校 . 培 差 高 素质 罕 殴 人 才 产 生
— " £4
积极 深远 的 影响 。 门 5
， 。 ， AAS ,，/
Enhance Student $S Synthesized Quality DY A I'd rticipating the
. . 人
Mathematical Contest 54 eli g
'A 一
Ji 惟
FENG Jie， HU Guang-xu, UANG Li-wei
(Dalian Naval Academy,Dalian 116018)
o
Abstract; The good prizes are awarded althorigh first participating the Mathematical Contest in Modeling. Some
experiences and measures are summed in this pi SN student’s Synthesized Quality in five ways is enhanccd
by participating the contest. Some experien s and neasures are described for improving this year’s scores.
Keywords: mathematical AN quality;creative thought;computer applications
一
一 -一

(上 接 89 页 }

Optmizayjpn Dekign for Vehicle Arrangement Plan of Strip Mine

人
下 LONG Jian-cheng， XU Peng， YUAN Yue-ming
SA Advisor: Wang Bing-tuan

R (Beijing JiaoTong University, Beijing 100044)
Abstract; In this paper, the thinking to solve the problem of optimal design is discussed by summing up the factors of vehicle ar-
rangement plan of strip mine, analyzing the restriction conditions of the vehicle arrangement problem comprehensively, setting
up the mathematical model base on integral programming, arranging the beginning setting of the excavator by using linear pro-
gramming which simplifies the model reasonably and accelerating the solution of the model. In consideration of the utilization rate
which can hardly near to 1 for the sake of promoting the practically applied possibility of the model’s optimized solution and in-
creasing the flexibility of vebicle arrangement, the maximum rate of utilization is established; While the minimum rate of utiliza-
tion is set up given that the excavator must be guaranteed to have certain utilization due to the high expenses of the equipments.
This model is of high quality of practicability and generalizing from the result of calculating.
Keywords: vehicle arrangement; strip mine; integral programming; optimization design

.

