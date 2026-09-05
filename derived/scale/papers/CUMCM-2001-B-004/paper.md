# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
多
第 19 卷 建 模 专辑 工程 数学 学 报 Vol. 19 Supp.
2002.02J3 JOURNAL OF ENGINEERING MATHEMATICS feb- 2002
文章 编号 :1005-3085(2002)05-0067-08
公交 车 调度 的 规划 数学 模 再
公交 车 调度 的 规划 数学 模型 -
人 { Se
溥 立 军 ， 要 尉 觅 ， 王 艳 辉 全 W
指导 老师 : 刘 红 卫 2XG
(西安 电子 科技 大 学 ,西安 710071) J
机 、 | SS 《4
编者 按 : 本 文 建立 了 两 种 优化 模型 来 研究 公交 车 调度 问题 。 第 -种 模型 中 使 用 大 sh 人 SS 对 客流 分 布 进行 了 优化 分
类 ,这 使 得 客流 时 间 段 的 划分 更 为 合理 。 第 二 种 模型 基于 随机 服务 系 乡 Arz 由 用 可 GI Mn 排队 系统 的 平均 队
长 及 平均 等 待 时 间 等 基本 公式 。 因 城市 交通 客流 是 随机 的 ， 利 夺 理论 来 研究 公交 车 调度 问题 更 能 刻 划 问 题 的
实质 。 但 单 交 通 线 上 的 公交 车 具有 串联 服务 的 性 质 ,这 与 GUNMf °% 忱 个 大 符合 。 第 二 种 模型 有 明显 的 不 足 。
摘 ， 要 : 本 文 根 据 有 序 样本 聚 类 的 Fisher 算法 ,给 出 一 种 峰值 曲线 的 优 儿 方法 ,通过 该 方法 我 们 得 出 了 上 行 客流 峰值 为 5
个 ,其 峰值 区 间 为 :5:006:00 ,6:009:00 , 9:00-16:00 , 16:00-18 :00 , 18:00-23 :00; 下 行 客流 峰值 为 5 个 ,其 峰值
区 间 为 : 5:00-7:00, 7:009:00. 9:0016:00 ,16:00-19:00,，19:00-23:00。
然后 ,依据 峰值 区 间 建 立 确定 发 车 间隔 的 算法 重 模 型 和 算法 I 模 型 ,对 两 种 算法 模型 计算 结果 进行 比较 分 析 ，
得 出 结论 :两 个 间隔 高 峰 类 时 间 自 用 货 拓 进 乔 求解 丑 余 3 个 类 时 间 段 用 算法 ][ 进 行 求解 。 在 各 个 时 间 段 结合
处 用 光滑 法 进行 优化 处 理 ,并 以 处 理 5 前 短 拓 四 基 而 制定 出 两 个 起 点 站 的 发 车 时 刻 表 ,并 求 出 全 线 共 需 要 47 辆
车 ,乘客 对 方案 的 满意 程度 为 98. 2 % , 氏 安 从 司 药 满意 程度 为 76.23 % 。
最 后 ,运用 随机 服务 系统 的 相关 理论 建立 随机 规划 模型 给 出 概率 灵敏 度 和 误差 分 析 ,进而 得 出 采集 运营 数据
的 较 好 方案 。 \ 7
关键 词 : 有 序 样 本 聚 类 ; 客流 ; 峰值 ; 于 as 随机 服务
分 类 号 : AMS(2000) 90CESSs ”中 同 分 类 号 : TB114.1 文献 标识 码 : A
1 8 串
> 4
《 EN 人 一 、 \ > 一 一 一 证-
SA 公交 和 车 在 该 线路 行进 中 以 20 公里 /小 时 的 速度 匀速 运行 , 即 不 考虑 启动 和 停车 , 每
Ye 夺冠 迟 及 其 他 因素 的 影响
为 ”公交 车 按 发 车 时 刻 表 顺 次 发 车 , 准时 到 达 每 个 站 点
3) “乘客 候车 时 间 一 般 不 超过 10 分 钟 ， 早 高 峰 时 一 般 不 超过 5 分 钟
4) ”满载 率 不 要 超过 120 % , 一 般 也 不 应 低 于 50 %
3 符号 说 明
疡 :工时 段 内 的 配 车 数 ( 时 段 配 车 数 ) (车 次 ) ; pi 时 段 内 的 期 望 满载 率 :
瓦 :时 段 内 的 小 时 最 高 断面 的 通过 量 ( 人 ); Ni: 时段 内 的 期 望 占用 量 ( 人 )
C: 车 容量 (C= 车 型 定员 + 最 大 允许 站 人 数 ) (人 ) : 工 : 路 线 长 度 (km) ;

<!-- source_page: 2 -->

ERi
有
68 工程 数学 学 报 第 19 全
O, ;时 段 内 的 乘客 周转 量 (人 km) ; 5 :7 时 段 内 乘客 的 满意 率 ;
5 : 乘客 的 平均 满意 率 ; 到 : 了 时 段 内 乘客 的 平均 等 待 时 间
na : 公交 公司 的 平均 满意 率 ;
4 问题 (1) 模型 的 分 析 、 建 立 及 求解
下 面 我 们 逐步 以 两 种 不 同 的 方法 对 公交 调度 方案 进行 讨论 , 第 一 种 方法 对 公交 调度 峰值
曲线 进行 优化 , 第 二 种 方法 对 公交 调度 发 车 间隔 进行 确定 ,进而 制定 出 公交 调度 方案 。 最 后
估 抽 定 方案 过 程 中 的 相关 参数 的 随机 特性 ， 抽象 出 明 完 整 的 随机 规划 本 于 江 信
方法 1 优化 公交 调度 峰值 曲线 = 2
公交 调度 人 员 在 制定 线路 本 车 计划 时 , 最 为 重要 的 依据 是 线路 客流 的 每 有 有 分 布 和
线 。 调 度 人 员 进行 这 样 的 峰值 划分 主要 依据 以 下 两 个 原因 : 2
时 段 配置 相同 的 运力 ; @ 划 分 为 若干 峰值 区 间 , 便于 进行 轰 乘 人员 的 班 忆 受 排 (明确 一 点 :
公交 调度 峰值 曲线 中 峰值 代表 一 个 区 间 ,而 不 是 一 个 点 ) 。
人 了 的 人 人 了 上 有 下
所 谓 有 序 样品 是 指 , 样品 按照 一 定 的 要 求 排 成 人 aa，
…。 表示 一 组 有 序 的 样品 则 每 一 类 必须 旺 f xj， 局 Vs wy fi< 力 形态 。， 个 有 序 样品
分 成 上 类 的 一 切 可 能 的 分 法 有 CS 种 ,这 个 数 比 因此 在 某 种 损失 函数 下 , 有
可 能 求 得 最 优 解 。 费 鞭 (Fishen 发 展 了 一 个 有 序 样品 的 桶 类 算法 , 它 可 保证 求 得 最 优 解 。
下 面 给 出 费 鞭 (Fishen 聚 类 算法 :  ©
@@ 基 础 算法 O/ 9
首先 定义 D7, 妃 表 示 美 (71+ 衣 全 的 直 答 。 类 的 直径 吕 7, 妃 这 里 采用 该 美的 值 与
闫 均值 差 的 平方 和 来 表示 直径 的 大 处 。
用 忆 上 表示 人 即
二 "Yeh -人
其 中 ,=1< 忆 -FE< 甩 。
定义 六 内 类 和 Pr，
2X L(biw = ,20 2 1) (
其 中 人
S 损 承 函 数值 越 小 ,分 类 越 合理 。 设 多 ,为 使 式 (1) 达到 极 小 的 解
Te” 的 计算 方法 使 用 下 面 两 个 递 推 公式 :
L(by2) =min/D(l,j-V +D(jn} (2)
Za = min{L(b1 TY DO (3)
在 上 =2 时 ，D2:112 7- 7 由 2 SS <n.
由 式 (0 得 (5 =Dj-1) +D(j.w
最 优 的 分 法 是 上 式 对 712 sy < 由 求 极 小 , 得 到 式 (2) 。 为 证 式 (3), 只 需 注意 到 ”个 有 序
样品 分 成 上 类 , 这 等 价 于 将 它们 先 分 成 两 部 分 :11.2， 和 车 则
其 中 11.2 7- 旦 将 分 成 丰 - 工 类 , 而 /7 + 1 玫 独 成 一 类 , 显然 ， </ <n, 于 得
到 式 (3)
2 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved.  http.//www.cnki

<!-- source_page: 3 -->

加 于
和
建 模 专辑 公交 车 调度 的 规划 数学 模型 0
G@ 算 法 实现
若 tfL< < 吃 已 知 , 应 求 分 类 b,)4, 使 它 的 损失 函数 最 小
由 人 3) 式 , 如 果 大 >2, 找 天 使 二 (大 岂 = 工 (下 DUO n)
于 是 得 到 第 下 类 玉 = 7 ut1, 凤 ， 然 后 找 六 ， 使 它 满足 Zro cy =
了 (0 +DIei 产 - 1), 得 到 第 大 - 1 类 PE1 =Y7J7J+1 天 -7
依次 类 推 得 到 所 有 类 | 2 ， 访 ，… 加] = 丰 由 式 亿 和 人 ) 可 看 出 刀 ,是 最 优 解
我 们 应 用 上 面 的 费 歌 (Fishez) 算法 对 公交 调度 峰值 曲线 进行 聚 类 处 理 ， 具体 步 又 如 下
1 先 将 各 时 段 客流 量 转 化 为 其 占 全 线路 客流 的 比例 。 本 题 中 有 18 l 2 即 18 个
有 序 样本 。 全 SS
2) 计算 所 有 可 能 类 的 直径 Di =- ru- 2 有 2
p ’ p:
3) 计算 最 小 损失 函数 。 用 人 和 有 个人/ 关押
HL(b). / XS
当 / <i sl8,， 2 </ 名 时 ， HR 4 汕 员 失 函数 值 变化 曲线 图
人 ».
1 上 行 方 癌 损 尖 函 驻 1 A o 和 方向 抠 生 本 于
TS
1 。 I:
回 1 人 = 1
F ag ak 局 局
局, 7 局 各
.2 NT |]  。
四 ， 本 有 本 个 风 四 了
“ ) \ 图 (CU ， 最 小 损失 函数 值 变化 曲线
/9 : 在 分 类 数 为 5 时 ,损失 函数 的 值 为 0. 004204 和 0. 002762 ,损失 函数 已
经 < 中 俱 修 T 。 在 分 类 数 为 6 时 , 损失 函数 的 值 为 0.003076 和 0. 002211 。 分 为 $ 类 与 分
迷 上 人 了 者 之 间 损 失 函 数 的 差别 不 大 。 从 方便 调度 管理 的 角度 出 发 ， 期望 划 分 尽 可 能 少 的
ea 业 为 5 个
着 聚 类 个 数 为 5 时 ， 可 以 得 出 ,上行 方向 的 最 优 分 类 为 5:00 -6:00，6:00 -9:00， 9:
00 一 6:00, 16:00 —18:00, 18:00—23:00; 下 行 方向 的 最 优 分 类 为 5:00 :00, 7:00—9 :
00, 9.:00 —16:00, 16:00—9:00, 19:00 一 23 :00 。
方法 工 确定 公交 调度 发 车 间隔
我 们 通过 引入 时 段 配 车 数 的 概念 来 探讨 在 不 同 客流 状态 时 如 何 确定 时 段 配 车 数 和 发 车
间隔 。
定义 “在 某 一 时 间 段 内 需求 的 车 辆 数 称 之 为 时 段 配 车 数 。 确定 原 则 是 ， 既 保证 有 足够 的
服务 质量 ， 又 保证 配 车 数 最 小 。
措 大

<!-- source_page: 4 -->

ERi
SANE

70 工程 数学 学 报 第 19 T

下 面 给 出 两 种 算法 模型 :

算法 模型 1 p -

算法 模型 II p = ua 二 2 | - uax| 2 2|

我 们 对 确定 发 车 间隔 的 模型 采用 两 种 不 同 的 间隔 确定 方法 进行 求解 ,综合 评价 后 得 出 综
合算 法 模型 :( 假 设 每 小 时 被 调查 的 上 车 人 数 基于 均匀 的 达到 率 )

i 参数 分 析

凡 : 对 上 行 方向 和 下 行 方向 分 别 计算 , 将 每 一 时 间 段 内 每 一 站 点 的 上 车 人 数 瑟 夫 下 车 人
数 得 到 该 时 间 段 内 该 站 点 兆 上 车 人 数 ， 然 后 从 每 一 时 间 段 起 始 站 点 开始 累加 得 到 每 SS 点 的
小 时 通过 量 D, (i 时 间 段 内 第 /7 个 站 点 的 小 时 通过 量 ) ,那么 有 .
是 上 行 或 下 行 方向 的 车 站 总 数 3

C: 依据 定义 有 C= 100 X120 %=120(\) Ni “ 玫

L: 上 行 方向 二 = 14.58(km)， 下 行 方向 了 = 14.61(km) X

0ii 0, -= wpy， 四 是 /时间 段 内 第 / -) 一 个 站 点 间 的 距离

pi: 我 们 对 的 估计 值 是 按 综合 考虑 每 一 时 间 须 商 前 六 客流 量 在 全 天 的 总 客流 量 所 占 的
比率 以 及 一 些 可 以 查 到 的 经 验 值 拟 合 出 p 与 局 的 永 布 关系 函数 :pl = 0.0173 X , +
46. 6919

壹 ”结果 分 析 °

分 别 按照 敌 法 模型 T 和 算法 模型 加 症 算 每 从 时 间 段 内 的 发 车 次 数 。 对 这 些 数据 分 析 可
知 ; 算法 T 和 算法 JI 各 自在 不 同 的 类 半 亲 攻 会 出 现 不 稳定 的 结果 , 在 每 个 类 时 间 段 单独 使 用
一 种 算法 得 出 的 结果 都 会 具有 一 定 前 不 可 售 度 。 以 不 同类 时 间 段 上 的 算法 模型 [及 算法 模型
作为 得 出 确定 发 车 间隔 的 综合 算法 模型 。

综合 算法 模型 :在 两 个 | Ts 上 行 方向 类 时 间 段 2， 3, 4 ，112，137 及 下 行
方向 类 时 间 段 /3 .4 记 E28 13)14) 采 用 算法 [进行 求解 而 在 上 下 行 方向 的 其 余 各 3 个 类 时
间 段 则 采用 算法 呈 q 六

优化 模 开 在 清 法

为 而 证 G HBZAIRBMR 我 们 采用 平滑 法 (所 谓 平滑 法 就 是 根
据 让 等 的 时 段 配 插 数 ， 在 前 一 时 段 内 确定 第 一 辆 车 的 发 车 时 间 ， 在 转换 段 内 综合 前 后 两 种 配
人 占用 量 而 不 是 不 均匀 间隔 ) 。
newa 上 行 方向 5:00 -5 :59，6:00 -6:59 两 个 时 段 内 (第 一 辆 车 为 5:00
发 车 彤 时 段 配 车 数 和 发 车 间隔 分 别 为 8. 4260 车 次 ,7. 12min; 29. 9505 车 次 ,2.00min 。 前 一
时 段 所 需要 的 配 车 数 的 0. 4260 车 被 留 在 5:57 之 后 与 下 一 时 段 的 0. 5740 车 结合 。 此 外 ，
0. 4260 车 的 期 望 占用 量 为 Wi = p XC, 0.5740 车 的 期 望 占用 量 为 Wi := p+， XC, 后 一 时
间 段 每 分 钟 需求 的 配 车 数 ( 斜 率 ) 为 29.9505/60, 相应 的 0.5740 车 要 运行 0.5740/ (26. 9505/
60) =1.17min 。 因此 第 二 时 段 内 第 一 辆 车 的 发 车 时 间 为 6:01:17, 其 期 望 占用 量 为 0.4260 X
Ni+0.5760 XXNi+l。

通过 以 上 的 分 析 及 数据 求解 ， 我们 制定 出 上 行 方向 和 下 行 方向 两 个 起 点 站 的 发 车 时 刻 表
( 略 ) ， 并 求 出 需要 的 车 辆 总 数 ( 即 最 小 配 车 数 /) 。 我 们 求 得 : 上 行 方向 为 : 47 ”下 行 方向 为 :
3 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved.  http://www.cnki

<!-- source_page: 5 -->

E
证 时
建 模 专辑 公交 车 调度 的 规划 数学 模型 0
35 故 所 需 车 辆 总 数 N =max(47,35) = 47
根据 题 意 ,我们 定义 ;时段 内 乘客 的 满意 率 为 ;
100% W; <5
. = wi=s FLER
"1(100% w, <10
El
也 > 非 高 峰 其
5
乘客 的 平均 清 意 率 5 - -2 人 一 计算 得 3- 98.2 5% -从 >
“\)
N . 》 H; *p; 、 - — -
公交 公司 的 平均 清 意 府 -一 SI 计算 得 1 0.5fnw + 体 ” 23 %
其 中 ， 上 行 =78.36 %, 下 行 W -74. 09 % X
5 问题 (2) 基本 假设
1 某 站 乘客 到 达 为 泊 松 过 程 , 设 上 (下 ) 行 各 站 乘客 的 到 达 过 程 为 平稳 的 泊 松 过 程 , 乘
客 到 达 率 为 \， 为 第 ?个 乘客 到 达 时 刻 ,， 则 乘客 到 欠 的 间隔 为
Pri 国光 B 1-e¢™ 1>0 网
TH - T 6 0. 7 <0
又 设 公交 车 每 批 运送 的 乘客 数量 鸭 / 扩 该 系 吕 可 变换 为 一 等 效 的 新 系统 。 由 爱尔兰 分 布
与 负 指数 分 布 之 间 的 关系 可 得 , 新 过 关于 窜 到 达 问 隔 服 从 参数 > 的 阶 爱 尔 关 分 布 :
1 evew >0
0 = = 和 i! (9)
0,t<0
式 中 ，rw Ma 后 sa
2 公交 车 对 短 抽 和 冤 服务 时 间 为 相互 独立 的 负 指 数 分 布 ,每 批 服务 时 间 是 指 公交 车 从
各 站 出 大 始 活 所 需 的 时 间 为 war。 设 公交 车 成 批 服务 时 间 az 服从 参数 上 的 负 指
数 分 布 , 即 [ON
< 0 6
人 { trr 7” -10o ，-o0 (6)
Hs ixr 的 关系 为 : = 下 一 = 了 了 一，Txz 为 运行 一 个 行程 的 平均 时 间 。
[trr] Trr
6 问题 (2) 模型 建立 与 求解
定理 1 在 GI/ M/ 系统 中 , 设 各 顾客 的 服务 时 间 相互 独立 且 具 有 公共 的 以 u 为 参数
的 负 指数 分 布 , 则 在 该 顾客 等 待 的 时 间 内 ， 每 台 服 务 设施 的 输出 过 程 ( 即 服务 完成 离开 服务
机 构 的 顾客 ) 是 一 个 以 为 强度 的 泊 松 过 程 。( 参 考 文献 /7
人 阶 爱 尔 兰 分 布 的 分 布 函数 4 (已 见 (3) 式 ,由 (3) 得 到 上 阶 爱尔兰 分 布 的 概率 密度 为
k-1
afy) =4 = 1 ) ee (7)
3

<!-- source_page: 6 -->

ERi
i
四
72 工程 数学 学 报 第 19 ee
则 到 达 间 隔 的 期 望 值 为 :
ETm+l - TmA = [raa (1) -& (8)
由 (9) , (8) 得 概率 密度 的 拉 氏 变换 为
co k
4 (9 = ea400 -[ 司 , res(s) > 0 9)
由 排队 理论 , 可 得 到 公交 车 服务 系统 的 服务 强度 :
Erv1 TAX
?一 E[Twe1 - Ta Toak 从 00
其 中 : 大 为 爱尔兰 分 布 的 阶 数 (公交 车 每 批 运送 的 乘客 数 ) ， 为 公交 车 数量 开 en
务 时 间 的 期 望 值 ，B/Tw+1 - Tv 为 第 n+ 1 批 乘客 与 第 m 批 乘 客 的 到 ; 网 训 二
对 于 服务 强度 p<1 有 下 面 的 定理 : 号
定理 2 U， 设 ww 为 第 m 个 乘客 到 达 时 系统 的 队长 ， 于 是 oa
条 件 无 关 , 其 表达 式 为 :
本
的 - R w,
入 4 本
其 中 0 为 方程 人"(mnrl- 0)) -| 可 在 人 ,六 之 间 的 唯一 解 。
利用 (7) 式 将 上 式 化 为 p 的 方程 : 0
al, 7 L=d t_
的 习 - -
P 1 e) - 有 7
且 Ur =KC ¥ DO 0 (12)
| 用 -1
一 到 Y d ， n(l- €) .| (13)
) 0 XGA 5 a- k
全 Co =1,
2 | ，
ce =TIT k=1,23,n
9 ， (14)
// 入 1 一 pb
R 2 4 (LN o + 大
2) 该 系统 平稳 分 布下 的 平均 队长 为 :
Ela] = 3% = 0 OE +(1- 5 Un 115)
其 中 : Q1，K，0 分 别 由 (12) ，(13) ，(1 细 决定 ，5 二 “|
3) “系统 的 平均 等 待 队 长 为 :
一 k0
Elaw] = 7g (16)
o4 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved.  http://www.cnki

<!-- source_page: 7 -->

ERi
i
se

建 模 专 辑 公交 车 调度 的 规划 数学 模型
4)， 系统 服务 台 平均 占有 数 :
E[1] = E[q] - E[qw] (17)
定理 3 对 GZ M/ 系统 , 在 平衡 状态 下 ,顾客 到 达 时 不 需 等 待 的 概率 为 :
w(0) =1- =5 (18)
平均 等 待 时 间 为 :
六 二 下 -一 KK
w = [xaw(v) =an(l. 0)° (19)
其 中 K、9 分 别 由 (13) ，(1U) 式 确定 。 y
我 们 用 系统 的 平均 等 待 队长 作为 衡量 乘客 满意 度 的 标准 ,用 系统 服务 台 平 欧 竺 有 产 作 为
衡量 公交 公司 利益 的 标准 ， 因 此 ,在 任意 时 间 段 内 都 可 以 建立 目标 规划 模型 一 修 )
1 设置 变量 : 一 -所 需 车 辆 数 ， 。 K 一 -车 容量 ， 3
2) 选择 目标 : P 一 第 一 目标 : 尽 可 能 使 顾客 满意 。 H
户 一 第 二 目标 : 尽量 使 公司 利益 最 大
3) “约束 条 件 的 制定 :
i。 乘客 在 非 高 峰 期 等 待 时 间 不 超过 10min, 在 高 客 期 敌 短 时 间 不 超过 Smin 。
动 《 车 容量 在 区 间 (50,120/ “A\
综 上 我 们 得 到 随机 规划 模型 为 :
| -0
min Exww7 =; -|
min e 7 Al - El[qw];
K €(50,120) AN
w HU
W.= [xdw(x) = waol -095 达 $( 或 10) ;
其 中 k, 8 由 式 和 13) ,01D A 一
对 上 述 模型 进行 系统 分 析 短 到 以 下 结论
1 和 服务 强度 p 对 系统 的 性 能 指标 起 着 至 关 重 要 的 作用 。 由 于
p = 荆 习 ,而 丈 集 数据 赂 rur 无 影响 , 故 所 采集 的 数据 应 尽量 体现 》 的 实际 情况 即 某 站 在 某
期 间 内 指定 任何 负 内 的 到 达 人 数 最 大 值
已， 对 处 辐 移 系统 参数 下 得 出 的 重要 指标 比较 后 , 得 出 : 系统 公交 车 数量 对 系统 性 能 的
arexfaaukttteretoMtur
上 这 的 人 文系 人 本 下 林 用 了 系统 优 全 只 要 赋予 明确 的 优
化 目 鞭 函 数 ,就 可 得 到 相应 的 配置 参数 。 同 时 为 计算 机 仿真 提供 理论 基础 。
7 模型 的 推广
考虑 约束 条 件 下 的 间隔 确 定 。 例 如 以 下 两 种 约束 条 件
i 资金 有 限 , 应 配备 的 车 辆 数 不 足 或 当日 应 配 车 辆 发 生 事故 不 能 上 岗 又 无 普 补 车 辆 供
给 时 ,调度 员 应 及 时 考虑 时 刻 表 的 变动 。
懿 ” 当 运力 充足 时 ,可 以 增加 总 发 车 次 数 ,提高 对 乘客 的 服务 质量 。

<!-- source_page: 8 -->

忌 顽
EU
党
[ohde
74 工程 数学 学 报 第 19 T
参考 文献 :
[1] 徐 光 辉 . 随机 服务 系统 (第 二 版 )[M]. 北京 :科学 出 版 社 ,1986
[2] 周 义 仓 , 赫 孝 良 . 数学 建 模 实验 [M]. 西安 :西安 交通 大 学 出 版 社 ,1999
[3] 李 涛 , 贺 勇 军 , 刘 志 俭 .Matlab 工具 箱 应 用 指南 一 应 用 数学 篇 [M]. 北京 :电子 工业 出 版 社 .2000
The Optimum Mathematical Model on the Bus Dispatch
BO Lijun ， YAO Werpeng， WANG Yarhui
Adviser: LiU Hong wei 全
(XiDian University , Xi"an ?10071) 全 <s 功
A\)
Abstract :This paper prasents an optimal method of peak curve according to the Fisher oem specimen clustering. We
conclude 5 uphill passenger-flow peak ranges: 5:00-6 :00 , 6:00-9:00, 9:00-16:00 , 16:00-18 : b 0 , and 5 downhill
passengerflow peak ranges: 5:007:00,7:009:00.9:0016:00,16:0019:00,19:00 So
Then , under the peak ranges , two algorithm models ， IT and II, are established NS Rue 人 alculated resultsof the fore-
going models, we conclude: model [ is applied to two interval high peaks and Illis applied to three others，With the
smooth method between every two time-sections , we make the bus time schédu wy Starting stations , and get 47 needed buses
全
at least，In this scheme , passengers”satisfaction rate is 98. 2 % , and the bus-ceg Pany sis 76. 23 %.
By the end , we set a random optimum model by the theory of randony séfvice system , and give the probability sensitivity and
error analysis. Further , we get a better scheme for collecting operation data) 司
Key words : serial specimen culstering ; passenger-flow ; peak ; bus number ; smooth method ; random service
o
AAA
(上 接 53 页 )
1 bl anlh of three dimensional blood vessel
-7 |
7 DING Fengping, ZHOU Lifeng, LI Xiao-peng
4 Adviser: Mathematical Modeling Tutor Group
\/ Zhejiang University of Technology , Zhejiang Hangzhou 310032 , China)
A
IyA-
Abstract : The reestablishment of the three dimensional blood vessel is presented in the article. According to the information given
by the problem , 100 pieces of sliced sheet of blood vessel are inputted into the program and transformed into data matrixes. Then
three steps are given to reestablish the blood vessel，Firstly , the radius of the blood vessel is obtained by searching the biggest in-
scribed circle of the sliced sheet and here two solutions are given by using tangent method and the biggest overlay，Secondly , the
track of the centre of the scrolling ball is hunted by grid method , Monte Carlo method and non - linear optimization method respec-
tively. Thirdly, the projection of the central axes is positioned precisely on three planes，At last verifying of the reestablished blood
Vessel and error analysis are carried out to test the precision of the model.
Key words : reestablishment of three dimensional image ; track; overlay
4 ( J E 下 H # 2
© 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved. http://www.cnki z
模 大

