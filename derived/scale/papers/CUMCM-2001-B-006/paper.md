# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
多
第 19 卷 ” 建 模 专辑 工程 数学 学 报 Vol. 19 Supp。
2002 £02 7 JOURNAL OF ENGINEERIN G MATHEMA TICS Feb 2002
文章 编号 :1005-3085(2002)05-0075-06
一 N
公交 车 调度 -
-从 >
吕 鹏 ， 张 文 夫 ， 雷 鹏 = 蛋
指导 教师 : 曹 天 林 2XG
(空军 工程 大 学 导弹 学 院 ,陕西 三 原 713800) H
TORRENT
多 目标 规划 数学 模型 。 基 于 多 目标 规划 加 权 分 析 法 ,进行 数值 计算 , 结 风 每 晶 」 但 放权 分 析 时 所 取 权 系数 只 有 一
组 ,最 好 多 取 几 组 权 系数 进行 比较 。 虽 然 , 文 中 最 后 提 及 灵敏 度 入 验 , 便 没 有 实质 性 进行 分 析 .缺乏 理论 指导 。
摘 ， 要 :本文 利用 多 目标 优化 方法 建立 了 公交 车 调度 的 数学 模型 。 2 -天 划
分 为 时 高 峰 前 ,时 高 峰 ,时 高 峰 和 晚 高 峰之 间 , 晚 高 峰 及 晚 高 峰 条 习 人 时段; 引入 和 车辆 的 平均 满载 率 ,乘客 的 等 待 相
怨 程 度 及 拥挤 抱怨 程度 作为 三 个 目标 函数 ,建立 了 三 目标 优化 模型 ;通过 加 权 ,将 三 个 目标 函数 合并 为 一 个 目标 函
数 。 运用 MATLAB 数学 坎 件 计算 出 了 上 行 \ 下 行 各 个 时 段 发 车 的 时 间 间隔 :上 行 各 时 段 时 间 间 隔 分 别 为 5.2 ,4 3、
人 人 了 时 前 分 为 0 本 534 次 公交 公司 的 平均 清
载 率 为 82.094 % , 抱 绝 顾客 的 百分比 流失 部/ 反 通 过 模型 检验 得 出 所 求 模型 较为 稳定 。 最 后 通过 对 原始 数据 的 分
交合
se 本
分 类 号 : AMS(2000) 90C08 q a sy TB114.1 文献 标识 码 : A
1 模型 假设 一 -7 y
1) F LRARRa A LREER
2)  HELATE 下 行 到 达 终点 站 时 ,所 有 的 乘客 必须 全 部 下 车 ;
3) 和 ,车 票 价 为 定 值 ;
) ， 各 公交 车 为 同一 个 型 号 ,公交 和 车 会 按 调 度 表 准 时 到 站 和 出 站 ;
gm raman . 相 邻 两 辆 车 发 车 时 间 间隔 相等 ;
记 车 上 标准 载 客人 数 为 100 人 ,超过 此 数 将 会 造成 乘客 抱怨 ;
时 高峰 时 乘客 等 待 时 间 不 超过 5 分 钟 ,正常 时 不 超过 10 分 钟 ,否则 乘客 将 会 抱怨 ;
8) 早上 5:00 上 下 行 起 点 站 必须 同时 发 车 ;
9) 不 计 乘 客 上 下 车 所 花费 的 时 间 ,公交 和 车 在 行驶 过 程 中 速度 保持 不 变 ;
10) “假设 每 辆 车 经 过 各 个 车 站 时 不 会 留 有 乘客 。
2 问题 分 析
题 中 要 求 照 顾 到 乘客 和 公交 公司 的 双方 利益 ,经 过 分 析 为 使 公交 公司 赚钱 尽 可 能 多 ,乘客
尽早 上 车 和 乘 车 的 舒服 程度 尽 可 能 提高 ,可 用 公交 车 载 客 的 平均 满载 率 来 衡量 公交 公司 的 利
2  ©1994-2006 China Academic Journal Electronic Publishing House. Allrights reserved. http:/www.cnki.n

<!-- source_page: 2 -->

ERi
 Y
76 工程 数学 学 报 第 19 卷 。 wms
益 ,以 乘客 的 等 待 时 间 和 拥挤 程度 作为 衡量 乘客 的 利益 。 从 而 可 以 建立 三 目标 优化 模型 ,进行
求解 。 但 由 于 三 目标 优化 模型 的 求解 较为 困难 ,所 以 简化 起 见 ,可 以 引入 加 权 因 子 ,将 此 三 目
标 优化 模型 转化 为 单 目标 优化 模型 ,从 而 求 得 车 辆 的 平均 满载 率 ,顾客 的 平均 抱怨 程度 和 每 一
个 时 间 段 内 相 邻 两 琐 车 的 发 车 的 时 间 间隔 。 据 此 ,可 排出 公交 车 调度 表 ,得 出 所 需 的 最 小 车 辆
数 。
3 变量 及 符号 说 明
必 : 第 7 时段 内 发 车 次 数 (规定 mm = 0 ; :第 7 时 段 的 起 始 时 间 : 全 A_
刀 第 /时段 内 第 ; 辆 车 的 发 车 时 间 : Ay 第 1 向 的 放 4 二 R、》
作 第 7 时段 内 第 § 辆 车 从 首 站 到 达 第 站 点 所 用 的 时 间 ; Z: 汽 车 的 及 均 泗 载 导 ，
由 第 7 时段 内 第 ; 辆 车 经 过 第 上 站 点 后 车 上 的 人 数 ，
户 : 第 /时段 内 所 有 车 载 客 的 总 和 ;px :第 oa
4 车辆 从 发 车 点 到 达 第 太 站 点 所 花费 的 时 间 ; Ps :所 有 旭 和 6 人才 之 和 ;
px :第 7 时段 单位 时 间 内 第 站 点 新 增加 等 待 上 车 的 人 内
px -第 /时段 内 第 上 站 点 单位 时 间 内 2
Hz: 第 7 了 时段 内 第 ; 辆 车 到 第 上 站 点 时 ,在 第 刀 济 等 很 误 问 超过 忍耐 时 间 的 人 数 ;
矿 : 由 于 等 待 时 间 过 长 而 不 满意 的 人 数 在 总 人 数 中 的 雍 例 ;
cf 第 7 时 段 第 ; 辆 车 离开 第 上 站 点 时 车 上 的 超载 人 数 :
C-: 由 于 超载 而 不 满意 的 人 数 在 放 人 数 中 侈 此 例 ，
7 ti <0 时 ,j(0 =1;
AGif0) :7 时刻 不 在 4 车 场 [ 上 竹 申 炊 让 ) 的 车 辆 总 数 ，
Go(D) :7 时 刻 且 Te 上 的 等 待 发 车 的 车 辆 数 。
4 模型 的 建 寺 ---> 小
NA 护 只 考虑 上 行 段 ) ,对 题目 所 给 数据 进行 分 析 ,将 乘客 一 天 候车 的 时
段 按 高 峰 期 < 党 期 各 此 林 忆 于 手册
os 六 段 ,假设 每 一 段 内 发 车 时 间 间 隔 相 同 ,每 一 段 的 发 车 次 数
分 别 鸭 : 则 [富家 ， mm mm -假设 某 路 段 站 点 数 为 六. 则 :
SO
Tarnanm 凡 = 万 + An 对 于 第 7 时段 第 ; 辆 车 经 过 第 人 站 点 所 花
费 的 时 间 d = £ + 多- 此 时 该 车 上 的 总 人 数 为 : 若 友 < Ti ph = en + Dyy von: 若 贞
> Ti pa = 本 + An pm 汽 车 在 该 时 段 离开 第 人 站 点 时 车 上 的 超载 人 数 为 : cx =
max{ ply - 100,0}
加 PIPIPIEN
ps = TY 5 CT (
假设 乘客 在 A 7 时 间 内 到 站 人 数 服从 均匀 分 布 , 则 在 第 1 辆 车 到 第 上 站 点 前 ,在 第 站 等
23 © 1994-2006 China Academic Jou lectronic Publishing House. All rights reserve tp://www.cnki.n

<!-- source_page: 3 -->

回 叶 这
了
四
建 模 专辑 公交 车 调度 0
候 时 间 超 过 忍耐 时 间 的 人 数 为 (忍耐 时 间 在 早 高 峰 期 为 5 分钟 ,其余 为 10 分 钟 ) : 若 第 7 时段 不
处 在 早 高 峰 期 ,PAY = maxfpEx (Am - 10) ,0 ; 若 第 7 时 段 处 在 早 高 峰 期 ,Ph = maxf pH
“Ai - 9) ,0 同样 可 以 计算 出 :
32
2 = 一 笃 一 (3/
100 Yn, =
通过 以 上 分 析 ,建立 如 下 三 目标 优化 模型 ， 全 人，
> 2 让
maxZ=- .—, min W = 全 min C 拓 |
总 | Py
100 Yn, /
n > 0 _ _ AR
s. t. 下 <120° j=1, SN TD
1 和
引入 三 个 非 负 加 权 因 子 X ,>a, 3 ,将 此 三 目标 优化 模 型 转化 为 单 目标 优化 模型 :
max XNZ - XC 六 普
nj > 0 _， _
s.t. VBNA 机 1 (*)
据 此 进行 求解 与 分 析 , T LASK Hi 香 段 的 耻 车 数量 妃 ,进而 可 求 出 其 余 各 量 。
下 面 来 求 按 最 优 方 案 所 需 最 小 革 策 数 褒 : :加 上 标 ″“ ”的 量 为 下 行 段 各 对 应 量 ) :
ro 1
本 1 - 了
oj
LI 加
2(0 = 一 ”入 Treoal - Treo 9 (二 0
91
o NT 一 1， Fitg =t <t+a
%, ， 加 Tirorl- To
(有 -1 1
p 下 Go(t) + p ns + Tici-8p+1 - Tici-p) "it-®
人 SA_， (0 -1 ， LT 加
Pe - ) PILIE Tvoal - To 若 : 关 +B
1 0-1
Ge (to) - 人 n'yey - 六 1 ， Fitg =t <to+B
其 中 ,4 为 下 行 线 车 辆 运行 时 间 ,8 为 上 行 线 车 辆 运行 时 间 , to = 5. 00 。
令 Gg(t) =0, 可 求 出 min Gecftu 即 为 B 车 场 初始 车 辆 数 , 同时 所 求 最 小 车 辆 数 为
maxAGy(1) 。
5 ”模型 的 求解
通过 对 本 题 所 给 数据 的 分 析 , 取 m = 5, 即 将 全 天 的 行车 时 间 分 为 5 段 , 划 分 表 如 下 :
2 4-2006 China Academic Journal Electronic Publishing House. Allrights reserved.  http:/www.c

<!-- source_page: 4 -->

回味 汉 回
78 工程 数学 学 报 第 19 7
1 5:00 一 6:00 1 5:00 一 7:00
2 6:00 一 9:00 2 7:00 一 10:00
3 9:00 一 16:00 3 10:00 一 16:00
4 16:00 一 18:00 4 16:00 一 19:00
5 18:00 一 23.:00 5 19:00 ~ 23 :00
对 于 上 行 段 ,公式 (LU 、(2) (3) 分 别 化 为 :
Pe 乞 乞 六 2
2Z = 一 全 一 CC=- 人 人 人 7 和
100 3, 全 re 全 SS
令 多 目标 的 权重 系数 分 别 为 :Xi = 0.2,)X = 0.3,》3 05 本 )
max 0.2Z- 0.3C- 0.5W H
n >0 \/
四 | ” = AS .14
7 =120 \
对 下 行 段 可 采取 与 上 行 段 同样 的 方法 处 理 .公式 (7) 论 欠 别 化 为 :
B pEERN  EEEw
2Z -= 一 侍 一 C = -二 一 Wwo= -二
100 Yn, 多 re
此 时 模型 f *) 中 取 5 = 13。 Ap ea
通过 对 上 行 段 以 及 下 行 的 模 负 进行 求解 可 得 全 天
所 需 总 车 辆 数 为 :56 辆 8 平均 满载 率 为 :Z = 85. 468 %
乘客 平均 抱怨 率 为 :1. 于- 余 共 发 车 次 数 为 :511 辆
简单 时 刻 表 如 下 ”人 几 TT
5:00 一 6:00_|5.J23 分 中 /次 5:00 一 7:00 |12.33 分钟 /次
6:00 一 9:00 上 2-226 分 钟 / 次 7:00 一 10:00 |2.874 分 钟 /次
9.:00.--16 :00 4 438 分 钟 / 次 10:00 ~ 16.:00 | 5.253 分 钟 / 次
16:00/718.:00| 3.214 分 钟 / 次 16:00 ~ 19:00 |3.272 分 钟 / 次
18 :0c3 00| 15.256 分 钟 / 次 19:00 ~ 23:00 |7.926 分 钟 / 次
1 NN 1# 上 , 辣 高 峰 时 期 路 上 所 有 和 车辆 数 加 起 来 总 数 不 超 过 51 辆 ,通过 合理 调整 完全 可 使 一
让 人 生生 数 也 不 超过 51 辆 。 造 成 这 种 情况 的 原因 主要 是 前 半天 上 行 段 公交 车 数 普 遍 比 下
行 段 多 ,致使 行 段 公交 车 数量 得 不 到 及 时 补充 ,而 同时 下 行 段 公交 车 在 这 一 时 间 段 内 又 普遍
过 剩 为 此 ,考虑 通过 加 大 下 行 段 的 公交 车 数 来 弥补 上 行 段 的 公交 车 数量 的 不 足 事实 上 ,只 需
通过 少量 合理 调整 即 可 解决 矛盾 ,同时 通过 调整 也 可 使 一 天 内 上 行车 和 下 行车 总 数 保持 平衡 。
调整 结果 如 下 :
所 需 总 车 辆 数 为 :52 辆 公交 车 的 平均 满载 率 为 :82. 094 %
乘客 的 平均 抱怨 度 为 :0.91 % 全 天 发 车 次 数 为 :534 辆
上 下 行 发 车 简单 时 刻 表 为 : (详细 时 刻 表 略 /
1994-2006 C A J 1
) nic Publishing e T e attp://www.cnki 模 大
太

<!-- source_page: 5 -->

回 叶 这
疙 -这
建 模 专 辑 公交 车 调度
5:00 一 6:00 5 分 钟 / 次 5:00 ~7:00 10 分 钟 / 次
6:00 一 9:00 2 分 钟 / 次 7:00 一 10.:00 2 分钟/ 次
9.:00 ~ 16:00 4 分 钟 / 次 10:00 一 16:00 5 分钟 /次

16:00 ~ 18:00 3 分 钟 / 次 16:00 ~ 19:00 3 分 钟 / 次

18:00 一 23.:00 15 分 钟 / 次 19:00 ~ 23:00 8 分钟 /次
6 模型 的 检验 与 结果 分 析 2

在 假设 每 辆 车 过 后 都 将 沿途 车 站 上 所 有 乘客 载 完 , 并 用 pl < 120 作为 绝 束 区 条 的 而
上 , 作 灵敏 度 检验 ,分别 将 ph <120 改 为 砍 125 和 ply <115 得 出 所 和 需 的 总 集 关 和 调度 广
案 基本 保持 不 变 ,从 而 表明 所 建 模型 稳定 。 从 1

加 4

>

sma | “A bf 人

加 | TS

人 人 区

~ 1
GREEN 吉方 @ GREENEOREGEEIEDE
上 行 段 的 客 流量 父 | 人 》 下 行 段 的 客流 量 图

从 一 日 的 客流 量 图 ( 实 线 表 示 上 车 人 数 ,虚线 表示 下 车 人 数 ) 可 以 看 出 ,上 行 段 在 5:00 ~
6:00.6:00 一 7:00、9:00 11:00 ~ 12:00.13 :00 ~ 14.:00 等 处 一 小 时 内 上 车 人
数 和 下 车 人 数 相差 很 大 ,而 在 计 络 过 程 中 上 下 人 数 大 致 相等 是 必要 的 ,下 行 段 也 存在 同样 的 问
题 .解决 办 法 是 在 统计 林 符 时 将 上 下 车 人 数 差异 很 大 的 时 段 细 分 ,使 全 过 程 中 上 下 车 人 数 大 致
相同 。 区

0
7 核 到 从 及 必得
s 了 者 区 型 从 题 中 数据 的 特点 出 发 联系 实际 ,将 全 天 的 行车 时 间 分 为 5 个 时 间 段 , 进 一 步 认为
乓 全 辐 末 委 内 的 发 车 时 间 问 师 相等 .人 而 使 问题 得 到 简化 。 在 一 定 程度 上 解决 了 单 直 车 在
全 地 稳 中 上 下 车 的 总 人 数 不 相 等 的 矛盾 ,同时 降低 调度 方案 的 复杂 度 ,使 调度 表 的 可 操作 性 得
到 有 效 增强 。 在 解 出 最 优 解 的 基础 上 联系 实际 问题 将 数据 进行 了 调整 ,虽然 牺牲 了 部 分 平均
满 裁 率 ,但 可 以 使 所 需 总 公交 车 数 明显 降低 ,同时 照顾 了 一 天 上 下 行 总 车 辆 的 平衡 。

由 于 在 模型 的 建立 过 程 中 ,始终 认为 一 辆 车 经 过 各 个 车 站 时 不 会 留 有 乘客 ,这 样 会 在 一 定
程度 上 增加 了 发 车 数 。 同 时 ,将 一 天 划分 为 几 个 不 同时 段 也 可 能 使 局 部 产生 等 待 过 久 的 现象 ，
不 过 从 长 期 考虑 结果 还 是 理想 的 。 当 然 ,如 果 考虑 公交 车 在 各 个 站 的 留 乘 人 数 ,无 论 是 从 长 远
还 是 从 短期 角度 来 看 结果 都 会 更 为 合理 ,可 以 使 精度 进一步 得 到 提高 。

94-2006 C Journa c Pub House. All rights r p: n
太

<!-- source_page: 6 -->

回 叶 这
EU
|
四
入
80 工程 数学 学 报 第 19 T
参考 文献 :
[1] 杨 普 . 实 用 最 优化 方法 及 计算 机 程序 [M]. 哈尔滨 船舶 工程 学 院 出 版 社 ,1994
[2] 秦 寿 康 . 最 优化 理论 和 方法 [M]. 电子 工业 出 版 社 ,1986
[3] 王 正 民 , 易 东 云 .测量 数据 建 模 与 参数 估计 [M]. 长 沙 :国防 科技 大 学 出 版 社 ,1997
[4] 胡 永 胖 . 数学 模型 [M] .西安 :西北 工业 大 学 出 版 社 ,1996
Buses Dispatching
P
LU Peng, ZHANG Werrfu, LEI Peng - A7
o
Faculty Adviser: CAO Tiarrlin 由
(Missile Institute of Air Force Engineering University , Sanyuan , so 人
Abstract : In this paper , a mathematical model on buses dispatching is presented with t kw hod of 上 on multi-objects.
Firstly , with the data analyses and consideration on feasibility , a typical workday cad’be ivided into five spans: before morning
rush hour , morning rush hour , the span between morning rush hour and evening rush hour, evéning rush hour and its beyond.
Three objective functions are introduced : the average capacity rate ,the degreeiof the passengers’ waiting , and the degree of pas-
SS
sengers” complain on waiting and crowded , to set up a model of perfecting on thrgegbjectives. Weighted average method is used to
combine the three functions as one. MATLAB mathematical software is emplofed to work out the interval of sending buses. Up-go-
ing buses are sent at respectively 5,2 ,4 ,3 ,15 (minutes) and dowrr going buse aré'10 ,2 ,5 .3 8 (minutes) . Altogether , 52 buses are
needed and 534 buses one a workday. The percent of average capacity is 82. 094 % , and the percent of the passengers’ complain is
0.91%. The model is proved to be steady through the test. Lastly shortening the statistical time on partial area is concluded to be
an effective way to improve the dispatching plan 33M ie analyE on original data.
Key vords : buses dispatehing : mathematical modgh Junobjects
MAY 》
一 )
2
5) 7
1994-2006 China Academic Jour lectronic Publishing House ights reserved.  http://www.cnki.n

