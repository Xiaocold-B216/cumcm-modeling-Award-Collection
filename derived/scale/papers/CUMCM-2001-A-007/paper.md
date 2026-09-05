# Extracted Paper

<!-- source_page: 1 -->

回 叶 这
四
第 19 卷 ，” 建 模 专辑 工程 数学 学 报 Vol. 19 Supp.
2002 年 0 月 JOURNAL OF ENGINEERING MATHEMATICS Feb. 2002
文章 编号 :1005-3085(2002) 05-0047-07
Aets f5 So ty —
血管 管道 的 三 维 重 建 -
一 人 \
耳 峰 平 ， 周 立 丰 ， 李 孝 朋 = W
指导 教师 : 数 模 组 2XG
(浙江 工业 大 学 98 提高 班 ,杭州 310032) H
SN

编者 按 :该 文 作 者 能 正确 运用 几何 方法 重建 了 等 径 管道 序列 切片 的 中 轴线 模型 fofe E SN 所 是 能 用 所 求 得 的 半径 的
球 沿 着 该 中 轴线 滚动 重新 生成 管道 ,并 再 作 截面 图 与 原 切片 图 形 作 比较 , 妓 让 了 异型 放 可 信人 性 。

摘 要 :文章 对 血管 管道 的 三 维 重 建 进行 了 讨论 。 根据 题目 所 给 信息 / Bi 00 张 血 管 切面 图 ,把 它们 转换 成 数据 托
阵 ,然后 分 三 步 进行 处 脖 :第 一 步 ,通过 搜索 切面 最 大 内 切 圆 求 出 管道 更 昔 径 ,提出 两 种 方案 ,分 别 是 切线 法 和 最 大
覆盖 法 ;第 二 步 ,轨迹 的 搜索 ,本 文 提出 了 三 种 方法 ,分 别 为 网 格 法 获 特 卡 罗 法 和 非 线性 规划 法 ;第 三 步 ,中 轴线 在
三 平面 上 投影 的 精确 定位 ,分 别 用 最 小 二 乘 和 分 段 最 小 二 乘 进行 了 曲线 的 拟 合 。 最 后 又 对 三 维 重 建 的 血管 管道 进
行 了 检验 和 误差 分 析 。 利 用 以 上 算法 较 好 地 进行 了 管道 的 重建 ,从 而 得 出 所 求 半 径 为 29. 529 ,中 轴线 上 100 点 的 坐
标 见 表 1 ,其 在 Xy, 7YZ 和 XZ 平 面 上 的 osfesgim 15.

关键 词 : 三 维 图 象 重建 ;轨迹 ;最 大 覆盖 妙

分 类 号 : AMS(2000) 65D17 中 图 分 类 易 4 文献 标识 码 : A

1 问题 的 重 述 j  nd
1.1 问题 下
断面 可 用 于 了 稳 下 果盘 织 器 官 等 的 形态 。 例如 ,将 样本 染色 后 切 成 厚 约 lnm 的 切片 :在

lat- ih . dra 如 果 用 切片 机 连续 不 断 地 将 样本 切 成 数 十 成 百 的

平行 切片 ,可 居 次 逐 片 观察 。 根 据 拍照 并 采样 得 到 的 平行 切片 数字 图 象 ,运用 计算 机 可 重建 组
4 和 作 人

织 .器官 贸 仆 确 的 译 维 形态 。

很 设 某 环 血 癌 可 视 为 一 类 特殊 的 管道 ,该 管道 的 表面 是 由 球 心 沿 着 某 一 曲线 ( 称 为 中 得
镶 汪 pas 例如 圆柱 就 是 这 样 一 种 管道 ,其 中 轴线 为 直线 ,由 半径 固定 的 球 深 动

歼 锟 成 。

襄 有 某 管道 的 相继 100 张 平行 切片 图 象 ,记录 了 管道 与 切片 的 交 。 图 象 文件 名 依次 为 0，
bmp 1. bmp 、…… 99. bmp , 宽 高 均 为 512 个 象 素 (pixel) 。 为 简化 起 见 ,假设 :管道 中 轴线 与 每
张 切 片 有 上 且 只 有 一 个 交点 ; 球 半 径 固定 :切片 间距 以 及 图 象 象 素 的 尺寸 均 为 1。

取 坐 标 系 的 Z 轴 垂直 于 切片 ,第 1 张 切 片 为 平面 Z=0, 第 100 张 切片 为 平面 Z=99。

试 计算 管道 的 中 轴线 与 半径 ,给 出 具体 的 算法 ,并 绘制 中 轴线 在 《7、YZ、ZX 平面 的 投影
图 。

1.2 切片 的 重组

为 了 便于 直观 的 分 析 ,我 们 对 切片 图 象 提取 轮廓 后 进行 三 维 重组 ,得 出 图 ! 为 了 防止 办
4 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved. http:Www ne

<!-- source_page: 2 -->

ERi
LARRT
48 工程 数学 学 报 第 19 全
廊 过 密 而 不 易 观察 ,这 儿 每 三 幅 图 片 提取 一 次 ) 。
80,

2 ”问题 的 分 析 2 ER

由 题 意 可 知 ,整个 管道 的 表面 是 由 "LE SN
球 心 沿 着 某 一 曲线 (中 轴线 ) 的 球 深 动 包 is 民有 有 O)
络 而 成 , 且 管道 中 轴线 与 每 张 切片 有 且 1\ E A>
仅 有 一 个 交点 ,这 样 经 过 这 个 交点 必 切 X 0 长 二，
下 球 的 最 大 国 面 且 这 个 交点 为 球 滚动 时 —50 <=A_
的 球 心 ,又 因为 每 一 个 切面 都 可 以 看 成 : : = AR >
由 无 数 个 球 切 面 王 加 而 成 ,根据 两 个 定 人
理 : 图 1 oa 全 从 7 体 图

定理 1 球 的 任意 切面 都 为 圆 。 站 二

定理 2 TY

所 以 我 们 可 以 得 到 每 张 管道 切 本 的 最 大 内 切 贺 就 是 经 过 球 尼 的 球 切 面 , 而 且 这 样 的 切面
具有 唯一 性 (因为 管道 中 遇 线 与 每 张 切 片 有 呈 仅 有 一 个 变 点 } :| 肉 此 我 们 只 要 在 每 张 切面 图 上
得 的 办 着 风 恩人 .把 所 有 的 球 心 连接 起
来 的 曲线 ,就 是 中 四 线 的 轨迹 。 人
3 ”模型 的 建立 O

根据 以 上 对 问题 的 分 析 我 们 息 用 步 通过 最 闫 覆 羡 法 求 球 单 径 然 后 用 非 约束 优化 算法 搜
索 中 办 线 的 雏 迹 坐标 ,最 后 通过 锁 迹 逢 全 多 而 上 的 投影 的 点 的 坐标 .用 最 小 二 乘法 进行 曙 线 拟
合 就 能 得 到 中 轴线 曲线 在 YY 入 YZ 在 投影 图 。

TORCOOTOOOR 512 x512 的 象 素 重
阵 ,这 儿 我 们 利用 MATLAB Aihcizmzsc mo 函数 得 到 象 素 矩阵 ,其 值 为 0 或 1(0 表示
有 黑 点 ,1 表示 白 点 和 7

3.1 琴 人 RnA

sii 1oyii

SeTVETDURDITI AERS HEATA6F  shBLRR  DE SE 4 0  2  F
个 球 切 面 组 腊 的 而 且 外 围 轮廓 线 与 最 大 内 切 圆 有 且 仅 有 两 个 交点 ,所 以 经 过 这 两 点 的 外 围
家 旨 的 两 条 切线 平行 且 间距 最 大 。 基 于 上 述 分 析 ,我 们 可 以 通过 找到 这 两 条 切线 来 找到 最
下 和 amezY:

实际 操作 中 ,由 于 对 图 片 的 象 素 提取 的 离散 性 ,我们 在 计算 导数 时 是 用 差分 来 代 蔡 。

方法 2 最 大 覆盖 法

最 大 黎 盖 法 就 是 在 切面 中 找到 最 佳 的 圆心 位 置 和 半径 长 度 ,从 而 使 得 由 这 个 圆心 和 半径
所 决定 的 圆 面 , 能 最 大 面积 地 歼 盖 管道 切面 的 图 形 ,这 样 搜索 到 的 圆 一 定 是 最 大 内 切 圆 .这 个
圆 的 圆心 就 是 我 们 所 要 找 的 球 的 球 心 这 个 圆 的 半径 就 是 我 们 所 要 找 的 球 的 半径 。

从 上 述 两 种 方法 分 析 及 考虑 到 我 们 所 使 用 的 工具 和 材料 ,可 以 得 出 方法 二 更 加 直观 ,计算
机 实现 更 容易 ,计算 复杂 度 更 低 ,所 以 我 们 采用 后 者 。

具体 实现 中 我 们 先 得 到 任意 一 张 图 片 的 象 素 矩 阵 ,然后 将 用 于 匹配 的 圆 根据 其 圆心 和 半
4 1994-2i China Academic Journal Electronic Publishi ouse. All rights reserved.  http://www.cnk

<!-- source_page: 3 -->

ERi

,

建 模 专辑 血管 管道 的 三 维 重 建 49 Re

径 将 其 圆周 离散 ( 即 以 象 素 表示 ) ,并 映射 到 512 xs12 的 图 中 ,其 中 圆周 上 的 点 为 0 ,其 余 的 点

为 1 , 即 形成 另 一 个 象 素 矩 阵 。 这 两 个 矩阵 在 相同 位 置 点 上 的 值 进行 逻辑 或 运算 ,如 果 其 值 为

0 , 则 为 匹配 点 , 即 此 点 在 管道 切面 图 形 内 , 理 则 其 在 切面 图 形 外 。 这 样 搜索 到 的 匹配 点 最 多 同

时 半径 最 大 的 就 是 所 要 顺 贡 有 |

找 的 最 大 内 切 圆 。 图 > 是 有 RuR 到 ae 本

和 图 3 就 是 分 别 从 图 请 产 AN 二

1.bmp 和 图 89. bmp 搜 f itEs )i H Fa

索 到 的 最 大 匹配 圆 (内 区 唱 本

部 白色 部 位 为 管道 切面 国 国 全 <

er 本 pe §0UY

配 圆 ) 。 和 站 和 半生 .3

根据 以 上 算法 ,我 图 2 1.bmp 的 最 大 匹配 图 图 3 89youp 的 里 大 匹配 图
们 抽取 了 所 有 的 切片 图 进行 半径 的 提取 ,然后 再 求 其 平声 值 , 求 其 多 值 得 到 奈 的 半径 为
29.529 。

3.2 ”轨迹 的 搜索

3.2.1 目标 函数 的 确立 -

在 求 出 半径 以 后 BUBHOAZ0RAT BLER 7E$  JBa b ,当然 我 们 也 可 以 求 出 每 一
个 切面 图 形 的 最 大 内 切 圆 ,然后 得 到 每 个 圆心 的 坐标 , 即 昔 轴线 坐标 ,但 这 样 做 计算 机 的 运算
量 会 很 大 ,同时 由 于 最 大 内 切 圆 搜索 法 的 稳定 性 不 高 ,从 而 会 造成 搜索 的 不 精确 ,所 以 采用 定
半径 搜索 。 e。

我 们 通过 定 圆 (半径 为 已 来 找 生 站 竹 线 , 也 就 是 用 定 加 覆盖 到 切面 图 形 上 去 ,找到 匹配
点 数 最 多 的 一 个 位 置 , 从 而 得 到 此 定 几 测 心 的 位 置 。

具体 实现 时 只 要 用 定 圆 的 圆心 位 置 进行 变化 , 设 其 为 47x, 岂 , 则 由 4 点 可 以 得 到 整个
贺 周 的 离散 坐标 By : 令 /(R 为 中 配 二 数 的 函数 ,其 计算 方法 与 最 大 内 切 贺 求 法 相同 ,即将
局 根据 圆心 4 的 坐标 和 半径 RIRISE) 离散 化 形成 矩阵 后 和 切面 图 形 矩阵 作 逮 生 与 操作 ,从 而
达到 匹配 最 大 , 则 优 亿 惠 标 函 煞 就 是 ，

max [ f(Ry)] ) & X512 坐标 面 上 的 点

3.2.2 村 时 际 函数 的 求解

上 可 一 上 四 4 ,使 得 定 圆 覆盖 切面 图 形 最 大 , 即 多 元 函数 极 值 最 优 解 ,这
是 到, 以 杀 ,也 为 自 变量 二 元 函数 ,这 样 可 以 通过 以 下 三 种 方法 来 求 得 :
1

总 索 过 程 中 ,对 每 一 个 圆心 的 坐标 X R 了 ,在 其 取 值 的 范围 内 均 取 100 个 步 长 ,分 为 100?
个 网 格 , 这 样 , 在 一 定 的 精度 范围 内 ,可 以 求 的 一 个 较 好 的 最 优 解 。

[2) 蒙特 卡 罗 法

蒙特 卡 罗 法 ,也 就 是 随机 实验 试点 法 。 它 的 基本 思想 是 :在 函数 的 可 行 域内 随机 地 选取 实
验 点 ,由 于 随机 取得 的 点 在 区 域 中 分 配 比较 均匀 ,所 以 对 函数 的 大 致 形态 能 较 好 的 体现 。

模型 中 ,随机 点 用 以 下 方法 产生 的 。

X = X0 十 (x1 一 xo) Xrand(1)

y=yo+ (y1- yo) Xrand(1)

其 中 ,(xo, x0 0 X WOBETEH, (yo. yy) 为 了 的 取 值 范围 。

4 @ 1994-2006 China Academic Journal Electronic Publishing House. All rights reserved， http:/www.cnki.net

<!-- source_page: 4 -->

ERi
SANE
50 工程 数学 学 报 第 19 T

(3) 非 线性 规划

非 线性 规划 即 无 约束 优化 ,以 数值 迁 代 为 基本 思想 ,基本 步骤 为 选取 初 值 4(20， Yo) , 进
行 大 次 迭代 并 求 出 迭代 解 , 由 迁 代 解 得 到 搜索 方向 和 步 长 ,如 果 上 + 1 次 移 代 符合 给 定 的 迁 代
终止 条 件 , 则 停止 迭代 ,得 出 最 优 解 ; 否则 继续 迭代 。

非 线性 规划 的 关键 是 搜索 方向 步 长 和 初 值 。 我 们 用 拟 牛顿 法 来 选 定 搜索 方向 . 拟 牛 顿 法
是 在 牛顿 法 基础 上 ,克服 牛顿 法 中 黑 赛 阵 不 仅 计算 复杂 而 且 会 出 现 变态 ,不 正定 等 情况 ,同时
保持 了 较 快 收敛 的 优点 ,从 而 得 到 最 好 的 下 降 方向 。 搜 索 步 长 的 确定 使 用 线性 搜索 的 方法 -或
更 为 有 效 的 插值 方法 。 由 于 此 搜索 程序 的 初 值 对 于 程序 正确 有 效 的 搜索 影响 很 龙 , 又 因为 相
OOES
的 球 必 作为 下 一 次 搜索 的 起 点 ,从 而 大 大 提高 搜索 的 效率 和 准确 性 。 但 由 于 转角 从 习 大 ，
在 这 种 情况 下 搜索 起 点 会 郴 够 逼近 而 导致 优化 搜索 的 失效 。 RRmfhA Re isHR
象 。 即 当 球 心间 距 前 后 相差 较 大 时 (采用 工程 上 的 观点 ,以 6 fiovely, BLBY% ,并 以
当前 球 心 作为 回 退 搜索 的 起 点 人 从 而 相应 的 消除 了
转角 上 的 搜索 失效 。 SN

从 上 述 对 三 种 方法 的 分 析 可 以 得 到 网 格 法 和 蒙特 上 y 路 简单 ,程序 容易 实现 ,但
网 格 法 搜索 的 精度 不 高 ,误差 较 大 ,搜索 时 ) nmeegEESER
间 长 ,同样 蒙特 卡 罗 法 的 实现 对 采 点 的 数 MSO
目 要 求 很 高 ,计算 量 大 ; 非 线性 规划 法 的 实心 于 汪 7
现 复杂 ,但 搜索 速度 快 ,计算 量 少 ,而 且 通 “| 人 多 150
过 MATLAB 的 优化 工具 箱 的 函数 可 以 很 ! 时 国 诛
方便 地 实现 所 以 非 级 竹 规 旭 计 较 估 耻 = [%

BUB0 2 25 LU ,FfrAT LLRePy o L ; LE
轴线 的 100 个 点 .用 所 求 将 低 的 求 定位 在 -130 -100 -30 0 30 100 150 200
这 些 点 上 和 轮廓 线 相交 就 可 4 图 4 血管 立体 还 原

从 上 图 可 以 看 到 把 图 形 二 站 卜 出 现 了 不 平滑 点 ,也 就 是 说 直接 用 这 些 中 轴线 上 的 点 构成
的 管道 还 不 平滑 所 区 世人 胡 采用 曲线 拟 全 的 方法 来 精确 定位 中 轴线 。

3.3 ”中 轴线 的 这、 全 下 机 了 的 本 确定 人

通过 以 宕 扫 述 的 搜索 /我们 可 以 得 到 中 轴线 上 100 点 的 三 维 坐标 ,然后 转化 成 相应 投影
面 的 二 维基 午 放 此 华 标 做 丛 当 的 处 理 ,就 可 以 减少 由 于 搜索 过 程 半径 的 取 值 和 数值 离散
化 带 纺 的 误 郑 s 比 较 精确 的 对 中 轴线 在 各 个 投影 面 上 进行 定位 。

0

| 浓 覆 最 小 二 乘 拟 合 ,是 在 投影 面 上 对 得 到 的 100 点 二 维 坐 标 进行 一 次 性 最 小 二 乘 拟 合 。
图 5 是 中 轴线 在 冯 平 面 上 投影 点 连 线 ( 左 图 ) 和 投影 点 最 小 二 乘 拟 侣 线 ( 右 图 ) 的 比较 图 ( + 表
示 中 轴线 的 投影 点 ) 。

从 上 图 可 以 看 出 运用 15 阶 多 项 式 最 小 二 乘法 拟 合 后 的 曲线 比 直接 投影 点 的 连 线 光滑 ,更
贴近 实际 的 情况 。 但 是 高 阶 多 节点 的 多 项 式 很 容易 出 现 振荡 ,上 图 中 在 z 方 向 80 到 100 的 曲
线 出 现 了 微弱 的 振荡 。

方法 2 分 段 最 小 二 乘 拟 合

分 段 最 小 二 乘 拟 合 ,是 在 投影 面 上 对 得 到 的 100 点 二 维 坐标 进行 分 区 (我 们 采用 4 个 分
区 ) ,对 各 个 分 区 进行 拟 合 ,在 连接 点 采用 三 次 样 条 插值 技巧 来 避免 由 于 高 阶 多 项 式 引 起 的 龙
4 © 1994-2006 China Academic Journal Electronic Publishing House rights reserved. http://w cnki.net

<!-- source_page: 5 -->

ERi
如 = 虹
建 模 专辑 血管 管道 的 三 维 重建 =
格 现象 。 图 6 是 中 轴线 在 vo 平面 上 投影 点 hmmevorsmenasy  100] nmemsmncs
连 线 ( 左 图 ) 和 投影 点 分 段 最 小 二 乘 拟 合 线 多 到 人
( 右 图 ) 的 比较 图 。 w n
从 图 6 可 以 看 出 拟 合 后 的 曲线 比 直接 NN 8 N 50
投影 点 的 连 线 更 光滑 ,贴近 实际 的 情况 ,而 20 4
且 从 图 6 和 图 5 拟 合 的 投影 曲线 比较 可 以 20 20
发 现 分 段 最 小 二 乘 拟 合 出 来 的 曲线 优 于 直到 t0
接 用 最 小 二 乘 拟 合 的 曲线 ,而且 消 除了 振 一 200 -100 N 100 200 0 100 200
菏 现 象 。 B 图 5 ui-ananaaemd 人 >
所 以 采用 分 段 最 小 二 乘 拟 合 能 更 好 的 =\\\
反映 曲线 上 每 一 点 的 位 置 。 图 7 是 采用 拟 100 人 和 灿 线 在 YOZ 平 面 上 的 投影 区 AN
合 后 曲线 作为 中 轴线 ,并 用 球 来 定位 。 2 v ®
从 图 7 和 图 4 比较 就 可 以 发 现 中 轴线 3 人 信 :
经 过 拟 合 后 形成 的 立体 还 原 图 更 加 光滑 3 A 50
平整 。 a0 4
30 p 30
il 中 1
4 模型 的 求 AN
AN 0 100 200 0036 了? 100 200
片 最 大 内 切 圆 的 搜索 ,分 别 得 到 Ri、R2、 ® 图 6 分 段 最 小 二 乘 拟 合 前 后 投影 曲线 的 比较
……、Ros、Rioo ,为 减少 搜索 过 程 和 离散 化 过 程 各 -
DR ER
球 的 半径 ,可 以 得 到 半径 R 为 .29 52g 1/ ) < 人
管道 的 中 轴线 = -2
sasmaasandhi 1 中 左 G® 人
边 三 列 给 出 了 直接 搜索 到 的 j 疯 点 中 轴线 在 — a
切面 上 的 点 的 坐标 人 依 凌 贡 *、y、) ,右边 三 列 Ow ww
on 图 7 管道 中 轴线 拟 合 后 的 立体 还 原 图
应 点 上 的 难 标 久
_ 分 表 1 中 轴线 的 从 标
ee 直接 得 到 的 ”直接 得 到 的 ”曲线 拟 合 后 的 ”曲线 拟 合 后 的 ”曲线 拟 合 后 的
] \ gr 了 轴 坐 标 Z 轴 坐标 苞 轴 坐标 了 轴 坐 标 Z 轴 坐标
忌 0.94557 - 160.01 0 3.2166 - 160.2 0
1.0959 - 159.95 1 2.4788 - 160. 19 1
(中 间 数 据 略 )
47.72 180.4 99 48.94 179.84 99
中 轴线 在 YY、7Z、ZX 平面 的 投影 图
首先 根据 搜索 到 的 中 轴线 在 每 一 切面 上 的 坐标 投影 到 三 个 平面 上 ,图 8 10 ,12 是 直接 将
这 些 投影 点 相连 得 到 的 曲线 ,图 9 .11 \13 是 投影 点 经 过 拟 合 得 到 的 曲线 。 图 14 和 图 15 分 别
是 中 轴线 的 三 维 直 接 搜索 图 和 拟 合 后 的 立体 图 (其 中 小 圈 中 轴线 的 投影 点 ) 。
3 006 China Academ Electronic Publish use. All rights reserved， http:Wwww.cnkinel
太

<!-- source_page: 6 -->

EiigaE
汪汪 辣
站 共生
52 工程 数学 学 报 第 19 卷 em
100 人 人 100 让 站 4
5 50|  0
TI 3
X X 人
图 8 “搜索 到 的 中 轴线 在 xov 上 的 投影 图 9 后 的 中 在 xy [节庆 Y
 C— 100[ 站 fr
人 本
90 人 90 EEEREEY a
80 | 一 80| Ce 人
70  D ae 70 上 下
0 60 上 上
50| ] Ni 50| 用 现时 风 生 |
3 40| 一 六 天 CS ped
20 庆 村 30 站 外 和 ee
10|… 虹 2 20 站
DO HIE LA NAPN o 上 | 多 让
~200 -~1¢0 0 100 200 0 H | : H H H
v -2 « 00 2 100 ”200
图 10 搜索 到 的 中 轴线 在 voz 上 的 投影 图 11” 拟 合 后 的 中 轴线 在 voz 上 的 投影
100|  woe=  UJ  F O HS W  £
80 人 MP 9. 本
~ et 3FY > 民有
40| ee 40 |
S- Acatilines -下 SL: 20bz 彬 一
“PP 人 = 和 汪汪 罗 汪汪 省 二 于
0 Te 0 人
i 4 -200 一 IO00 0 100 200
20 40 6| 70 _80 100 120
¢ 全 Y
T 所 图 13 “ 拟 合 后 的 中 轴线 在 xoz 上 的 投影
分 1 1
人 人
作 国生 风 浊 和 i Ey S w - I
】 > 下 人
本 交 和
[ 关 0 让
AN 和 ee 0 下 ae Ce
ee 20 l
0 英 2 0
0 0 和 0
50 00 二
, 100 1 基 2Tio 3 100 0 0
图 14 “搜索 到 的 中 轴线 的 立体 图 图 15 拟 合 后 的 中 轴线 的 立体 图
5 管道 的 三 维 重 建
这 儿 通 过 模型 求解 的 中 轴线 的 最 佳 拟 合 线 得 到 管道 的 三 维 重 建 如 图 16 。
斤 工
模 大

<!-- source_page: 7 -->

ERi
ARETY
建 模 专辑 血管 管道 的 三 维 重建 和
从 图 16 可 以 发 现 此 时 的 三 维 重建 已 经 非常 的 好 ,每 个 切面 的 外 轮廓 都 能 在 重建 图 中 看
到 。
6 ”模型 检验 和 误差 分 析 SA
6.1 模型 的 检验 (人 A
从 管道 的 三 维 重建 图 (图 16) 沿 Z 轴 作 切 面 ,就 ®),
可 以 得 到 切面 。 这 样 我 们 可 以 先 从 中 取出 第 5 张 切 AS
片 和 第 50 张 切 片 ,再 和 第 5 张 切面 图 片 ( 即 4. bmp) -DT < in
和 第 50 张 切 面 图 片 ( 即 49. bmp) 的 外 轮廓 线 分 别 作  0 =<MAv》
在 同一 张 图 片上 得 到 图 17 和 18 ,来 验证 模型 的 准确 中 7 小
性 (图 中 深 色 的 为 外 轮廓 线 , 浅 色 的 为 切面 所 截 下 来 图 16 ov 生体 图
的 球 切 面 的 外 轮 廊 线 ) 。 从 这 两 张 可 以 得 出 结论 :按照 我 们 建立 的 让 ES
况 基本 符合 ,切面 得 到 的 球 的 所 有 球 的 切面 构成 了 整 武 的 切 吝 国正 Z 外 纶 说 基本 重合 ,这 有 力
的 证 明了 我 们 的 模型 的 准确 性 和 算法 的 合理 竹 。 As NS
6.2 ”误差 的 分 析 0
当然 整个 模型 存在 - 定 RSX
的 误差 外
(D 切面 图 本 身 存在 象 虹 > 入
素 上 的 误差 (这 是 题目 本 身 用 局 i5
所 带 入 的 ,而 非 模型 所 致 ) 。 人
(2) 数值 离散 化 时 带 入 A 让
误差 ,主要 体现 在 搜索 最 大 as
内 切 圆 和 中 轴线 轨迹 时 国庆 图 17 第 5 切面 的 验证 图 图 18 第 50 切面 的 验证 图
的 离散 化 运算 中 。 ) 机
G) 在 景 小 内 雪 加 搜索 和 拓 [搜索 时 ,由 于 步 长 初始 点 等 因素 的 限制 而 造成 误差 。
7 模型 的 评 从
此 模 和 0
-0D 所 全 立 的 模型 简洁 明了 ,便于 使 用 数学 工具 ,如 MATLAB 等 ,降低 了 编程 求解 的 难
卜 编 三 了 运往 时 间 ,提高 了 工作 效率 。
于 /亲生 同 问题 求解 提出 了 多 种 的 解决 方案 ,并 通过 比较 分 析 找到 最 佳 的 模型 。
G) 凌 型 结果 较 优 , 且 经 过 大 量 数据 模拟 验证 ,与 实际 情况 吻合 得 很 好 。 非 线性 优化 和 分
段 曲 线 拟 合 使 曲线 更 准确 。
当然 ,模型 还 存在 改进 的 地 方 ,比如 可 将 所 给 的 bmp 图 由 512 X512 变 为 1024 X1024 象
素 的 图 ,从 而 提高 精确 度 ,减少 误差 等 等 。
参考 文献 :
[1] 张 宜 华 .精通 MATLAB 5[M]. 北京 :清华 大 学 出 版 社 1999.
[2] 姜 启 源 . 数学 建 模 [M]. 北京 :高 等 教育 出 版 社 1978.
[3] 阿达 玛 芽 著 ,朱德 祥 译 . 几何 (立体 部 分 ) [M]. 上 海 :上 海 科学 技术 出 版 社 ,1980. (下 转 74 页 )
欣
4 © 1994-2006 China Academic Journal Electronic Publishing House. All rights reser ttp://www.cnki.net

<!-- source_page: 8 -->

回 叶 这
EU
人
74 工程 数学 学 报 第 19 T
参考 文献 :
[1] 徐 光 辉 . 随机 服务 系统 (第 二 版 )[M]. 北京 :科学 出 版 社 ,1986
[2] 周 义 仓 , 赫 孝 良 . 数学 建 模 实验 [M]. 西安 :西安 交通 大 学 出 版 社 ,1999
[3] 李 涛 , 贺 勇 军 , 刘 志 俭 .Matlab 工具 箱 应 用 指南 一 应 用 数学 篇 [M]. 北京 :电子 工业 出 版 社 .2000
The Optimum Mathematical Model on the Bus Dispatch
BO Lijun, YAO Werpeng， WANG Yarrhui
Adviser: LIU Hong wei #7
(XiDian University , Xi’an 710071) 全 A7
Abstract :This paper presents an optimal method of peak curve according to the Fisher oem specimen clustering. We
conclude 5 uphill passenger-flow peak ranges: 5:00-6 :00 , 6:00-9:00, 9:00-16:00 , 16:00-18 : b! 0 , and 5 downhill
passengerflow peak ranges: 5:00-7:00, 7:00-9:00, 9:00-16:00, 16:00-19:00 , 19:00423 ;00.
Then , under the peak ranges , two algorithm models, ， IT and IT are established NS 4 ng the calculated results of the fore-
going models, we conclude: model [ is applied to two interval high peaks and 生生 to three others. With the
Smooth method between every two time-sections , we make the bus time schédle ofiwb Starting stations , and get 47 needed buses
at least，In this scheme , passengers”satisfaction rate is 98. 2 % ,and 3 is 76. 23 %.
By the end ,we set a random optimum model by the theory of randogj ice syStem , and give the probability sensitivity and
error analysis. Further , we get a better scheme for collecting operation dataj 司
Key words : serial specimen culstering ; passengerflow; peak ; bus number; smooth method; random service
o
锥 -
(上 接 53 页 )
wo of three dimensional blood vessel
 \¥V
%, DING Fengping, ZHOU Lifeng, LI Xiao-peng
Adviser: Mathematical Modeling Tutor Group
SS， 下 4 University of Technology , Zhejiang Hangzhou 310032 , China)
IyA-
Abstract : The reestablishment of the three dimensional blood vessel is presented in the article. According to the information given
by the problem , 100 pieces of sliced sheet of blood vessel are inputted into the program and transformed into data matrixes. Then
three steps are given to reestablish the blood vessel，Firstly , the radius of the blood vessel is obtained by searching the biggest in-
scribed circle of the sliced sheet and here two solutions are given by using tangent method and the biggest overlay，Secondly , the
track of the centre of the scrolling ball is hunted by grid method , Monte Carlo method and non - linear optimization method respec-
tively. Thirdly, the projection of the central axes is positioned precisely on three planes，At last verifying of the reestablished blood
Vessel and error analysis are carried out to test the precision of the model.
Key words : reestablishment of three dimensional image ; track; overlay
四 oemom oemeeonaaoaos anon mo 撒 因
@ 1994-2006 China Academic Journal Electronic Publishing Ho llrights reserved，  http:/www.cnkine 2
模 大

