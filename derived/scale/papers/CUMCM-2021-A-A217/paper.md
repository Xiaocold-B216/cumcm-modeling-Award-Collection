# Extracted Paper

<!-- source_page_kind: image_sequence -->

## Logical image page 1

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 1 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A1.jpg -->
<!-- source_image_sha256: 161768AEB1E9D258E31A46F476DE676A22F57AE9AEA27978BA88DCB20CAC22D5 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

"FAST" 工 作 抛物 面 的 优化 设计
摘 要

本 文 基于 FAST 的 工作 原理 ， 通 过 机 理 分 析 、 坐 标 变换 、 非 线性 最 小 二 乘 优化 等 方
法 ， 建 立 了 反射 面板 调节 优化 模型 ， 并 利用 BFGS 算法 、 蒙 特 卡 洛 积分 算法 等 算法 ， 对
不 同 条 件 下 反射 光线 吸收 比率 进行 了 研究 -

问题 一 中 ， 首 先 基于 固定 的 仰角 B、 观 测 目标 9 、 圆 心 C 和 焦点 己 ， 利 用 旋转 拢 物
面 的 中 心 对 称 性 ， 选 取 焦 距 作为 自由 度 控制 变量 ， 构 建 在 极 坐 标 系 下 开口 竖 直 向 上 的 二
维 扼 物 线 方程 ， 得 到 不 同 偏转 角度 下 原点 到 抛物 线 的 距离 ， 进 而 导出 三 维 下 的 旋转 抛物
面 方程 。 其 次 ， 以 焦距 为 决策 变量 ， 将 口径 300 米 的 抛物 面 作为 积分 域 ， 将 理想 拢 物 面
到 原点 的 距离 与 基准 球面 半径 差 值 平方 作为 被 积 函 数 进行 积分 作为 最 小 化 目标 函数 ， 建
立 了 确定 理想 抛物 面 的 优化 模型 。 最 后 ， 使 用 二 分 法 求 得 目标 函数 导 函 数 在 定义 区 间 上
的 零点 ， 得 到 理想 抛物 面 焦距 的 精确 值 为 280.854， 误 差 平方 积分 的 最 小 值 为 10.112。
此 时 对 应 理想 抛物 面 的 解析 式 为 ?一 (= 十 切 ?/561.708 一 300.841 -

问题 二 中 ， 首 先 利用 球 坐标 下 不 同 轴线 方向 抛物 面 的 旋转 不 变性 ， 在 原 从 标 系 和 问
题 一 的 坐标 系 之 间 建 立 了 双向 可 逆 的 变换 关系 , 得 到 了 不 同方 位 角 下 理想 抽 物 面 到 原点
的 距离 。 其 次 ， 以 主 索 节点 的 工作 坐标 和 促 动 器 的 伸缩 长 度 为 痰 莹 变量,j 以 积分 域 费 兰
的 主 索 节点 到 原点 的 距离 与 理想 抛物 面 到 原点 的 距离 之 差 的 逆 方 和 为 最 小 化 目标 函数 ，
分 别 考虑 下 拉 索 长 度 固定 、 相 邻 节点 的 距离 变化 幅度 不 超过 007%、 促 动 器 的 伸缩 范围
在 土 0.6m 为 约束 条 件 ,建立 反射 面板 调节 优化 模型 .最 后 , 使 用 拉 格 朗 日 乘 子 法 和 BFGS
算法 进行 求解 , 得 到 误差 平方 在 抛物 面 扣 从 上 的 积分 的 最 小 值 为 5.1353 X10?, 理想 抛
物 线 的 顶点 坐标 为 (-49.3925j- 36.943, -294.450) ， 调 节 后 反射 面 300 米 口径 内 的 主
索 节 点 编号 、 位 置 坐标 、 各 促 动 器 的 伸缩 量 等 结果 见 文件 resultxlsx。

问题 三 5- 首 先 通过 旋转 变换 ， 将 反射 问题 的 倾斜 入 射 光 线 转化 为 重 直 入 射 光 线 。
其 次 -通过 求解 线性 方程 组 ， 依 次 确定 出 入 射 光 线 与 三 角形 面板 的 相交 判 定式、 交点 举
标 : 至 角形 面板 的 法 线 向 量 ， 并 利用 光线 垂直 入 射 的 性 质 ， 使 用 法 线 向 量 简化 计算 得 到
出 射 光线 的 方向 角 。 再 次 ， 通 过 联 立 射线 方程 与 馈 源 舱 所 在 的 目标 高 度 ， 得 出 射线 方程
的 步 长 和 出 射 光 到 达 目 标高 度 时 的 坐标 ， 并 与 馈 源 舱 的 有 效 区 域 进行 比 对 ， 作 为 入 射 光
线 是 否 被 有 效 接收 的 判定 式 。 最 后 ， 将 300 米 口径 内 实际 接收 区 域 作为 积分 域 ， 将 入 射
光线 有 效 接收 判别 式 作为 被 积 函数 ， 使 用 蒙特 卡 洛 算法 进行 积分 ， 得 到 有 效 接收 的 光源
面积 ， 并 计算 出 调节 前 接收 比 0.811%6， 调 节 后 接收 比 1.1039%6， 提 升 了 36%6， 调 节 工作
抛物 面 的 过 程 使 有 效 光 源 的 光斑 可 以 尽量 完整 地 出 现在 每 个 三 角形 面板 内 〈 图 11)。

本 文 的 特色 在 于 将 机 理 分 析 与 非 线性 最 小 二 乘 优化 相 结 含 ， 并 灵活 采用 二 分 法 、
BFGS 算法 和 蒙特 卡 洛 积分 算法 进行 求解 ， 在 大 规模 、 高 维 且 带 有 非 线性 约束 的 求解 中
仍然 以 接近 二 阶 的 速度 收敛 至 最 优 解 ， 为 FAST 在 不 同情 况 下 的 调节 与 设计 提供 了 参考
依据 。

关键 词 : 坐标 旋转 、 非 线性 最 小 二 乘 、BFGS 算法 、 蒙 特 卡 洛 积分

1

## Logical image page 2

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 2 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A2.jpg -->
<!-- source_image_sha256: 08D5F1F1E77B7F84872D87F90AC7AE1B08ECF0033302560FFBA1D6FF2CF4D25B -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

一 、 问 题 重 述
1.1 问题 背景
中 国 天 眼 (FAST) 由 主动 反射 面 、 馈 源 舱 及 其 他 系统 组 成 ， 其 中 主动 反射 面 是 由 主
索 网 、 反 射 面 权 、 下 拉 索 、 促 动 器 及 支承 结构 等 构成 的 可 调节 球面 。 主 索 网 由 和 柔性 主 索
按 短 程 线 三 角 网 格 方式 构成 ,每 个 主 索 节点 连接 一 根 下 端 与 固定 在 地 表 的 促 动 器 连接 的
下 拉 索 。 促 动 器 沿 基准 球面 径 向 安装 ， 可 沿 径 向 伸缩 。
主动 反射 面 有 两 个 状态 : 基准 态 时 反射 面 为 半径 约 300 米 、 口 径 为 500 米 的 球面 ;
工作 态 时 反射 面 为 一 个 300 米 口径 的 近似 旋转 抛物 面 。 馈 源 能 接收 中 心 在 与 基准 球面 同
心 、 半 径 差 为 的 一 个 球面 上 移动 。 当 观测 某 个 方向 的 目标 S 时 ， 馈 源 舱 接收 中 心 被 移
动 到 直线 SC 与 焦 面 的 交点 P 处 ， 调 节 基准 球面 上 的 反射 板 形成 以 直线 SC 为 对 称 轴 、
以 了 为 焦点 的 近似 旋转 抛物 面 ， 从 而 将 来 自 S 的 平行 电磁 波 汇聚 到 有 效 区 域 。
1.2 问题 提出
在 反射 面板 调节 约束 下 ， 确 定 一 个 理想 扼 物 面 ， 调 节 促 动 器 ， 使 工作 抛物 面 尽量 贴
近 理 想 抛物 面 ， 以 获得 反射 后 的 最 佳 接收 效果 。 建 立 模型 解决 以 下 问题 :
“问题 一 : 当 待 观测 天 体 呈 位 于 基准 球面 正 上 方 ， 即 a 一 0，B=90" 时 ， | 结合 考
虑 反射 面 板 调节 因素 ， 确 定理 想 抛物 面 -
@ ”问题 二 当 待 观测 天 体 8 位 于 a 一 36.765"; 轨 三 98.16 风 时 ， 确 定理 想 抛物 面 。
建立 反射 面 调节 模型 ， 调 节 相关 促 动 器 的 售 缩 量 所 使 到 射 面 尽量 贴近 该 理想 抛
物 面 。
@” 问 题 三 : 基于 问题 三 方案 ,“ 评 算 调节 后 馈 源 能 接收 比 ， 与 基准 球面 接收 比 作 比
较 。
》 二 、 问 题 假设
下 W 根 设 光线 在 反射 面 不 存在 二 次 反射 。
2， 假设 不 考虑 板 间 间隙 给 反射 带 来 的 影响 -
3， 假设 电磁 波 在 大 气 中 的 传播 为 直线 传播 -
4 ， 假设 反射 面板 不 会 发 生 弯曲 ， 始 终 维持 一 个 平面 。
5 假设 电磁 波 的 反射 为 全 反射 ， 不 考虑 反射 时 的 损耗 。
6. 假设 主 索 节点 调节 后 ， 相 邻 节点 之 间 的 距离 会 发 生 微小 变化 ， 变 化 幅度 不 超过
0.07%.
2

## Logical image page 3

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 3 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A3.jpg -->
<!-- source_image_sha256: 6DA0105DE4A945DF87EA3382C812A74419AF4F457D14D84D0A8C1E5FA719B841 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

三 、 符号 说 明
序号 ”符号 意义 单位
1 Ly 抛物 线 及 旋转 抛物 面 的 焦距 m
2 L, 从 原点 出 发 到 理想 抛物 面 的 距离 m
3 L.G) 序号 为 ?的 促 动 器 的 伸缩 量 m
4 LG) 序号 为 ?的 下 拉 索 的 长 度 m
5 I 所 有 主 索 节点 的 下 标 集合 9
6 J 一 块 反射 面板 所 用 到 的 下 标 集合 ——
7 E 所 有 三 角形 的 所 有 边 的 集合 —
8 (@o(@,%0(),20()) 序号 为 ?的 主 索 节点 的 基准 坐标 和
9 [CORTORIO)] 序号 为 ?的 主 索 节点 的 工作 坐标 =
10 @ @w @Dz @) 序号 为 ;的 促 动 器 底 端的 坐标
1n EOY O@)  FTRINEHBTRILE ~
12 Gy Ga) 序号 为 ?的 促 动 器 顶端 基准 状态 的 瑟 标 ”一
13 (ow @Dyyw (@),2w 人) 序号 汶 的 主 案 节点 旋转 后 的 工作 坐标 ”一 一

四 ,问题 分 析
4.1 问题 一 的 分 析

问题 一 要 求 当 G 本 08， DB 二 90? 时 ， 结 合 反 射 面板 调节 因素 ， 确 定理 想 抛 物 面 。

其 汽 B 一 2， 且 观测 目标 89、 圆 心 C 和 焦点 尸 固定 , 确定 所 求 剖面 抛物 线 的 自由 度
只 有 荆 注 意 到 能 转 抛物 面 的 中 心 对 称 性 ， 故 所 求 抛物 面 是 其 剖面 上 的 抛物 线 的 复合 。
故 可 利用 焦距 作 最 优化 控制 变量 ， 进而 构建 在 直角 坐标 系 下 开口 紧 直 向 上 的 二 维 拢 物 线
方程 , 将 其 代入 极 坐标 进行 变换 .可 导出 旋转 掀 物 面 的 方程 。 最 后 对 理想 抛物 面 到 原点 的
距离 与 基准 球面 半径 的 差 值 平方 进行 积分 ， 并 进行 最 小 二 乘 最 优化 求解 ， 使 得 基准 球面
与 最 终 确定 的 抛物 面 之 间 的 总 调节 距离 的 平方 和 最 小 ， 从 而 求 出 理想 抛物 面 。

42 问题 二 的 分 析

问题 二 要 求 当 a 一 36.795"， 8 一 78.169? 时 ， 确 定理 想 抛 物 面 。 并 建立 反射 面板 调
节 模 型 ， 调 节 相关 促 动 器 的 伸缩 量 ， 使 反射 面 尽量 贴近 该 理想 抛物 面 。

注意 到 球 坐标 下 不 同 轴线 方向 的 抛物 面 为 各 同 向 性 这 一 性 质 ， 本 文 考虑 在 原 有 空间
坐标 系 和 问题 一 已 建立 的 坐标 系 之 间 建 立交 互 的 旋转 变换 关系 ,使 得 问题 二 中 可 部 分 沿
用 问题 一 中 所 得 有 关 理 想 抛物 面 的 数学 关系 ,进而 可 以 确定 本 问 的 目标 函数 和 决策 变量 。
然后 引入 下 拉 索 固定 长 度 、 节 点 之 间 的 伸缩 变动 率 、 促 动 器 的 伸缩 量 等 约束 ， 再 引入 相
邻 节点 的 距离 变化 三 度 的 约束 和 促 动 器 伸缩 范围 的 约束 , 求 出 相关 促 动 器 的 伸缩 量 优化
解 。

43 问题 三 的 分 析
问题 三 要 求 基 于 问题 二 的 反射 面 调节 方案 ， 计 算 调 节 后 馈 源 舱 的 接收 比 ， 并 与 基准
3

## Logical image page 4

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 4 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A4.jpg -->
<!-- source_image_sha256: 5395CC798E0187E826A37B3B74E9F0B718C48571DAC03F6D8C20A1A5CFB5CA02 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

球面 接收 比 作 比较 。

本 文 拟 采用 与 问题 二 相同 的 坐标 旋转 方法 , 将 入 射 的 光线 从 斜 射 变 为 垂直 于 水 平面
入 射 。 接 着 ， 本 文 拟 通过 构建 以 一 块 反 射 面板 上 三 个 主 索 节 点 坐标 为 基准 的 参数 方程 ，
利用 参数 方程 判断 入 射 光 与 任意 一 决 反射 面 板 的 几何 关系 ， 从 而 确定 交点 坐标 。 然 后 ，
本 文 拟 利用 待定 系数 法 确定 反射 平面 的 法 向 量 ， 从 而 利用 向 量 方向 角 的 关系 确定 反射 光
的 指向 。 然 后 ， 可 以 利用 方程 联 立 求 得 的 反射 光 与 接 收 平面 的 交点 判断 该 光线 是 否 被 有
效 接收 。 最 终 ， 可 将 入 射 光 的 照射 区 域 作为 积分 域 ， 是 否 接收 到 光线 的 判别 式 作为 被 积
函数 进行 积分 ， 将 积 出 的 结果 与 照射 面积 做 比值 ， 从 而 计算 出 馈 源 舱 的 接收 比 。

五 、 问 题 一 模型 的 建立 与 求解
5.1 问题 一 模型 的 建立
5.1.1 直角 坐标 系 下 二 维 抛物 线 方程 的 构建

题目 要 求 给 出 考虑 反射 面板 调节 因素 下 的 理想 抛物 面 。 根 据 推 述 ，FAST 的 抛物 面
由 二 维 抛物 线 旋转 得 来 ， 因 此 本 文 首先 基于 有 = /2 ， 讨 论 在 二 维 平面 内 ， 抛 物 线 开口
方向 竖 直 向 上 的 抛物 线 方程 ， 再 通过 旋转 确定 三 维 的 旋转 批 物 面 。

AN
SAE
X2 e
RSS
I SS
内 | Se 二 |
aa F
图 1: FAST 剖面 示意 图

本 文 基于 题目 附件 8 给 出 的 空间 直角 坐标 ， 以 C 为 坐标 原点 ， 构 建 剖面 图 上 的 二 维
直角 坐标 系 。 则 水 平 向 右 方向 为 > 轴 正 向 ， 竖 直 向 上 为 z 轴 正 向 。 图 1 为 FAST 的 剖面
示意 图 ， 其 中 抛物 线 的 焦点 为 点 已。 由 于 讨论 的 是 开口 方向 竖 直 向 上 的 抛物 线 ， 故 其 焦
点 三 的 坐标 为 :

(zw 2)=(0, -(R—F)) 《5
根据 抛物 线 的 几何 性 质 ， 设 该 抛物 线 的 焦距 为 志 。 则 焦点 与 项 点 的 距离 为 0.577 ，
则 该 抛物 线 项 点 @ 坐 标 为:
@0r7) = (0, - -由 -950 Ga
由 于 掀 物 线 焦点 与 准 线 的 距离 为 一 倍 焦距 ， 故 可 得 抛物 线 准 线 方程 为:
4

## Logical image page 5

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 5 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A5.jpg -->
<!-- source_image_sha256: BBE8158EC8C9EDB94EA8C6C7D926A8073F2CB89DC0509949750B6B0BD783FDE8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

2=-(R-F)—1L, 《53)
根据 抛物 线 的 几何 性 质 ， 可 知 抛物 线 上 的 任意 一 点 到 准 线 的 距离 等 于 该 点 到 焦点 的
距离 。 利 用 该 性 质 构建 抛物 线 方程 :
CE 下 ?= Ca 《G
其 中 ， 加 一 (及 一 四 —L 为 点 的 z 轴 坐标， 由 准 线 方程 (5.3) 得 出
zz 一 - ( 尽 一 到 ) 为 点 己 的 z 轴 举 标 。
接着 ， 将 杂 和 z 的 值 代入 式 (5-9)， 可 得 :
[z 十 (R—F) +L)*=2*+ [3+ (R—F)]? (5-9)
两 边 平方 项 展开 后 ， 移 项 整理 可 得 方程 :
—g-g-@-p 6
以 上 ， 得 到 了 二 维 直 角 坐 标 系 下 ， 开 口 竖 直 向 上 的 抛物 线 方程 。
S12 极 坐标 系 下 二 维 地 物 线 方程 的 构建
由 于 需要 将 计算 得 到 的 抛物 面 与 球面 进行 对 比 导 舍得 工作 的 物 面 尽量 贴近 理想 拢 物
面 。 因 此 为 方便 求解 ， 将 上 述 抛物 线 方程 转换 成 极 从 标 形式 。
] 区
1 而
让 / 原点 C 一
V/ 1
7 上
SC
(Lycosar-L,sinc) 4
图 2， 极 坐标 系 下 抛物 线 示意 图
如 图 2， 以 C 点 为 原点 ， 以 原 z 轩 为 极 帖 ， 构 建 机 坐标 系 ， 有 :
(人 司 二 CEoosw - Lusinu) 《GD
其 中 , 瑟 是 从 原点 出 发 ， 到 抛物 线 的 距离 。 将 式 (5- 刀 代入 直角 坐标 下 的 抛物 线 方程 并 整
理 可 得 :
an- 全 -下 -0 9
为 了 得 到 不 同 偏转 角度 w 与 区 的 表达 式 ， 需 要 对 式 (5.8) 的 方程 进行 求解
(CD Sw#n/28f, THAGHEEUL 为 未 知 量 的 一 元 二 次 方程 ， 故 有
5

## Logical image page 6

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 6 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A6.jpg -->
<!-- source_image_sha256: 4877BA2CB6637C302DBF501C02C7F72356ECED32F1A6D2FB93BF212A73A834F8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

A=sno+45( 全 + 有 >0 5-9)

此 时 方程 始终 有 两 个 不 同 的 根 。 根 据 韦 达 定 理 :

-2Lsinw _ 2L;sinw
Ta Go
oL,(-%—R-F)) -ar hi
将- 癌 ) - -2525C- 中 < 本
故 可 知 ， 此 时 对 于 每 一 个 w， 都 会 产生 取 值 一 正 一 负 的 两 个 根 。 售 去 负 根 ， 得 到 正
根 的 解析 式 :
~Lysinw + Ly[sin* 二
ea 本。
@ 当 四 一 W/2 时 ， 可 将 式 (5-9) 看 作 以 马 为 未 知 量 的 一 元 一 次 方程 ， 故 有
五 = 了 + 二 eh)
经 过 化 简 ， 可 得 基于 偏转 角度 由 与 环 的 表达 式 :
ED 有
人 ) wit )
pon [二 2 (s14)
L R-F Ed
2sinw * sim 2 2
由 于 闫 式 (5-14) 中 含有 未 知 参数 ， 则 将 该 函数 记 为 :
~Lysinw + Lyyfsiatw + 2 (4 + R— F) EEC
JID = cosz 人。 wwE19
2
2sinw sinw * 2

以 上 , 得 到 了 在 不 同 的 偏转 角度 下 , Z4EMmR b  S8R Si5E0 L, 的 表达 式 ，
接着 将 此 二 维 抛物 线 进行 旋转 即 可 得 到 三 维 的 旋转 抛物 面 :

5.1.3 理想 抛物 面 与 基准 球面 的 相似 度 计 算 -

将 5.1.2 节 得 到 的 二 维 扫 物 线 以 极 办 为 中 轴线 旋转 ， 得 到 反射 面板 的 旋转 抛物 面 ，
该 抛物 面 可 使 得 沿 着 中 轴线 平行 射 入 的 电磁 波 可 以 被 反射 到 焦点 已 处 。 为 比较 这 一 理想
拓 物 面 与 基准 球面 的 相似 程度 ， 需 要 在 球 坐 标 系 下 ， 以 口径 为 300 米 的 抛物 面 在 基准 球
面 上 的 投影 所 围 成 的 区 域 为 积分 域 ， 对 理想 抛物 面 到 原点 的 距离 与 基准 球面 半径 的 差 值
平方 进行 积分 ， 即 :

6

## Logical image page 7

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 7 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A7.jpg -->
<!-- source_image_sha256: E7B9DEE20642BD980DBDFD6CA96C8B40146469A7AFDF0E52B2CFEFE4A7CF63D7 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

em-mao ng
积分 数值 的 大 小 是 评价 相似 程度 的 准则 。 其 中 ， 尽 为 基准 球面 半径 : 为 抛物 面 上
的 点 与 原点 的 连 线 和 中 垂 线 所 形成 的 空间 角 的 大 小 ; dc 为 曲面 微 元 ;4 为 积分 域 , 可 表
示 如 下 :
《Gaga e=-VE —2—¢?, 2? +y* <150°) GD
加 «
四
二
条 亲 击 而 码
L
六
图 3: 极 坐标 系 下 FAST 剖面 及 积分 区 域 示 省 图
由 于 殷 物 面 的 中 轴线 是 竖 直 的 所 以 在 球 坐 标 系 下 可 转化 为 二 重 积分 ， 故 该 积分 式
可 化 简 为 :
Jem —R]*dadf (5-18)
小
其 下 "2G 为 方位 朋 :; 有 为 仰角 ;mm 一 尽 cos8 是 在 B 角 给 定时 ，ax 角 在 基准 球面 上 的 轨迹
投影 出 的 图 形 的 半径 。 根 据 题目 要 求 的 工作 口径 ， 可 知 B 的 取 值 范围 满足 :
leos| - £(B,L;) =150 ©-19)
根据 几何 关系 ， 易 知 式 (5-19) 有 两 个 解 Be 和 Bi + 有 < Bw ， 且 这 两 个 解 的 均值 为
mW/2 。 为 防止 对 有 指向 的 圆 环 重复 积分 ， 可 设 的 取 值 范围 为 BE (Bo， m/2)。 结 合 上 述
分 析 ， 对 式 (5-18) 进 一 步 化 简 得 :
和
am 有 8 Ga
以 上 ， 得 到 了 球 坐 标 系 下 ， 计 算 理想 抛物 面 和 基准 球面 之 间 相 似 程度 的 准则 。
5.1.4 理想 抛物 面 优化 模型 的 建立
由 于 在 现 有 约束 条 件 下 ;可 求解 出 多 个 不 同 焦距 的 理想 扫 物 面 ， 故 需要 对 于 理想 殷
物 面 进行 最 优化 的 选取 。 故 构建 目标 函数 如 下 :
学

## Logical image page 8

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 8 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A8.jpg -->
<!-- source_image_sha256: 672EFB154E4FD1F43F3468D3D725AA3A0DFB9FD35B1E6F5DF50C0B6ECE1AFAE3 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

. n
-am 人 2rrs[f(wLD 一 忆 ?d8 Ga2D
结合 式 (5.6)， 确 定形 成 最 优 理想 拢 物 面 的 抽 物 线 方 各 为:
s=gm-4-@-p (5-22)
5.2 问题 一 模型 的 求解
5.2.1 算法 设计
首先 对 目标 函数 (5-20) 的 数值 特性 进行 定性 分 析 ， 可 知 焦距 蕊 决定 了 理想 抛物 面 和
基准 球面 之 间 的 相似 程度 ， 焦 下 过 大 ， 则 理想 抛物 面 会 整体 低 于 基准 球面 ， 焦 下 过 小 ，
则 理想 抛物 面 会 整体 高 于 基准 球面 。 易 知 目标 示 数 的 梯度 函数 在 区 间 内 为 一 个 单调 连续
函数 , 且 区 间 两 端 对 应 的 梯度 值 异 号 , 即 目标 勇 数 (5-20) 在 区 间 (100，400) 上 是 一 个 存在
极 小 信 点 的 凸 函数 。 因 此 ， 本 文 基于 该 性 质 设计 针对 梯度 函数 零点 的 二 分 查找 法 对 极 小
值 点 进 和 求解。 具体 求解 算法 如 下
算法 1 二 分 查找 算法
1 选 定 边 界 值 。 首 先 根据 题目 设 定 与 实际 情况 ， 适 取 T00 与 00 作 尖 二 分 查找 区 间
的 左右 端点 。
2 取 二 分 查找 区 间 的 中 点 从 标 代 天 会 趟 (5-23) 的 梯度 函数 中 ， 计 算得 到 该 点 所 对 应
的 梯度 什 ， _
3 关 梯 度 信 远 大 于 0. 将 二 分 查找 区 间 的 右 端点 设置 为 当前 中 点 .并 返回 第 2 行 。
4 赣 痢 度 信 远 小 于 07 将 二 分 查找 区 则 的 左 端点 设置 为 当前 中 点 .并 返回 第 2 行 。
5 牙科 度 值 的 绝对 值 小 于 机 器 精度 epsilon， 则 中 点 即 为 待 求解 的 极 小 值 点 ， 程 序 结
束 ，
5.2.2 理想 抛物 面 的 求解 与 分 析
基于 算法 1， 在 MATLAB 中 编程 进行 求解 ， 给 出 求解 出 的 理想 掀 物 面 的 剖面 视图
《图 4 左 ) 及 理想 掀 物 而 与 基准 球面 的 径 向 高 度 高 低 差 《 图 4 右 ):
局 PP
0 四
2 -ET |
TS 人 |)|
1 \w
~/  |:
隔 ， 人 |
_ A5 .1 2 网
图 4: FAST 2D 剖面 最 优 抛物 线 〔〈 左 )、3D 最 优 抛物 面 径 向 高 度 高 低 差 《 右 )
最 终结 果 求解 出 理想 抛物 面 的 焦距 Z 的 精确 什 为 280.854， 误 差 平方 在 口径 上 的 积
8

## Logical image page 9

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 9 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A9.jpg -->
<!-- source_image_sha256: 6B086AC70BA8E0C02DFBDD07E2FA5C0CEE9082987F5927DA755987C46EC859ED -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

分 的 最 小 值 为 10.112， 将 万 一 280.854, R=300.4, 下 一 0.466 尽 带 入 式 (5-6) 可 得 剖 切
平面 上 的 抛物 线 方程 为 :
300.841 G23)

将 抽 物 线 绕 z 轴 旋转 一 周 后 ， 可 知 其 旋转 抛物 面 的 方程 为:

zc 十 切 ?一 300.841 G29)
5.2.3 结果 检验
基于 5.2.2 节 中 的 精确 结果 ， 对 所 得 理想 抛 物 面 的 剖面 上 的 径 向 高 度 与 基准 球面 半
径 的 高 低 差 进行 检验 ， 可 得 最 优 抛物 面 与 基准 球面 的 偏 移 量 ;
04
02
i 人
0
中
.oz| 上 |
加 |
个人-
To 0 01001590
图 5: 最 优 抛物 面 与 基准 球面 的 偏 移 量

让 图 .5 可 颗 ， 最 优 所 物 面 与 基准 球面 的 偏 移 量 在 (-0.6, 十 0. 色 的 范围 内 。 因 此 此
最 优 捧 物 面 在 实际 应 用 中 ， 促 动 器 顶端 上 下 拉动 下 拉 索 的 长 度 范围 也 较 小 ， 结 合 反射 板
调节 效率 因素 ， 可 得 本 结果 合理 且 较 优 。

六 、 问题 二 模型 的 建立 与 求解
6.1 问题 二 模型 的 建立

问题 二 要 求 基于 问题 一 所 建立 的 模型 ， 求 解 当 a = 36.795"， B 一 78.169? 时 的 理想
抛物 面 ， 并 以 工作 抛物 面 尽量 贴近 理想 抛物 面 为 目标 ， 在 下 拉 索 固定 长 度 、 节 点 之 间 的
伸缩 变动 率 、 促 动 器 的 伸缩 量 约束 下 ， 优 化 相关 促 动 器 的 伸缩 量 。

为 简化 计算 ， 本 文 首先 建立 在 标准 坐标 系 上 旋转 得 到 的 新 坐标 系 ， 使 得 主 索 节点 与
理想 撤 物 面 在 径 向 方向 的 距离 差 值 可 沿用 问题 一 中 的 式 (5-15)， 从 而 构建 本 问 的 目标 函
数 。 然 后 通过 分 析 促 动 器 底 端 坐标 、 基 准 状态 与 工作 状态 的 促 动 器 顶端 坐标 、 主 索 节点
的 基准 坐标 与 工作 坐标 以 及 促 动 器 伸缩 量 等 变量 之 间 的 几何 关系 , 构建 本 问题 的 约束 条
件 ， 得 到 反射 面板 调节 优化 模型。 最后， 设计 BFGS 算法 进行 模型 求解

9

## Logical image page 10

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 10 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A10.jpg -->
<!-- source_image_sha256: 493490E8AEB125188B5A8D5E997C61F919997456E642838251B2AEFF0DE6204D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

6.1.1 基于 坐标 系 旋转 的 理想 抛物 面 与 反射 面板 相似 度 计算
本 是 中 ， 由 于 观测 天 体 8 的 方位 对 于 基准 球 心 C 存在 与 坚 直 方向 的 倾角 ， 这 给 构建
新 的 理想 拓 物 面 带 来 了 一 定 的 困难 。 但 在 求解 理想 抛物 面 时 ， 对 于 不 同 轴线 方向 的 地 物
面 来 说 ， 其 焦距 、 焦 点 等 性 质 都 是 不 变 的 。 故 将 现 有 空间 坐标 系 ， 以 基准 球面 的 球 心 C
为 中 心 、 沿 基准 球面 的 前 面 方向 进行 族 转 ， 使 得 问题 二 中 理想 扫 物 面 的 轴线 与 族 转 后 空
间 直 角 坐标 系 z 轴 所 在 直线 重合 ， 此 时 主 索 节 点 与 理想 抛物 面 在 径 向 方向 的 距离 关 值 可
沿用 问题 一 中 的 式 (5-15)。
s .
2 人/ 2 人 2
影 /
1 /17 | 网 上 全 7
Ah 多 4 ¥
Yl y Vir
7ic 2 4C xz 人 x
原生 后 al。 抽动 3-
图 6: 坐标 系 旋转 示意 图
设 第 个 主 索 节 点 的 工作 坐标 为 (z(b),y (6),z() 。 将 原先 的 坐标 辑 络 着 灶 沿 正方
向 旋转 角度 ( 正 向 旋转 方向 与 坐标 轴 指 向 满足 右手 定 则 , 下 六 同 义 ), 则 举 标 相对 于 坐标
系 绕 z 轴 反 向 族 转角 度 a; 再 将 此 时 的 坐标 轴 绕 着 y 畏 沿 直 方面 旋转 角 厦 m/2 一 6， 则 坐
标 相对 于 坐标 系统 Y 轴 反 向 族 转 my/2 一 有 根据 三 维 台 标 引 族 转 短 阵 的 定义 , 可 得 旋转 坐
标 系 下 ， 第 ?个 主 索 节 点 的 工作 坐标 (25 (9 (zw 的 ) 为:
"
co [@EA0 -可 全 -有 骨 /ese une 0)s0
w@)]— 0 1 0 -sina cosa 0||yG) 人 GD
2 0), (和 -月 o ou 他- 有 0 0 1/Nz@
如 图 6, 不 难看 出 旋转 后 坐标 系 的 z 轴 正方 向 指向 被 观测 体 8 。 接着 球 心 C 为 原点 ，
在 新 的 空间 直角 坐标 系 上 建立 空间 极 坐标 系 。 再 将 变换 后 的 主 索 节点 的 直角 作 坐 标 转化
为 新 的 空间 极 坐 标 系 下 的 坐标 ， 得 到 第 ?个 主 索 节点 的 坐标 为 (F(D),B(,a()， 具 体形
式 为 ;
7 = V 本 本 于 交加 于 冯 人 5
3 — aren ®
pg ~arcsn(-220)
ar 人 主帅 二 0 rwG'rolwO> 人 Ga
< au 高 昌 ) wow0'yroavo<o
0,25 *  ©?-0
接着 ， 根 据 问题 一 中 理想 抛物 面 上 偏转 角度 w 5 L 的 表达 式 (5-15)， 得 到 在 新 的 从
10

## Logical image page 11

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 11 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A11.jpg -->
<!-- source_image_sha256: F513E0FBE920FC8C8A4A0AFA893C3436EB169558DCF738078574AC1E722D0E38 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

标 系 中 ， 理 抱 抽 物 面 上 仰角 为 8( 人 的 点 与 原点 C 的 距离:
ET
ap VH HR_DLE0, pg 和
zu0=-1 ,  F 5 ©
-和
为 保证 反射 面 在 工作 状态 下 与 理想 抛物 面 尽量 贴 合 ， 需 要 使 得 在 同一 径 向 方向 上 的
主 索 节点 与 理想 抛物 面 上 的 点 距离 原点 C 的 距离 差 尽量 小 。 故 可 构建 如 下 优化 目标 :
COwrzO)= mmin 工 GO-160) 《9
2
其 中 ， 工 为 所 有 主 案 节点 所 用 到 的 下 标 集合 ， 有 为 新 的 极 些 标 下 仰角 取 值 的 最 小 值 。 由
于 理想 折 物 面具 有 照明 区 域 的 限制 ,5.1.3 节 中 已 经 据 此 给 出 了 仰角 的 取信 范围 式 , 这 在
本 问题 中 也 同样 具有 约束 效果 。 注 意 到 ， 在 基于 促 动 器 伸缩 完成 的 主要 节点 位 置 变化 过
程 中 ， 第 引 个 主 过 节点 的 华 标 (ar (gr (ar 人) 可 以 由 促 动 器 的 介 缩 晶 叭 一 确定 。 根
据 附件 2 中 数据 ， 可 知 促 动 器 底 端 的 坐标 (z- ()y (,z- ()) 与 促 动 器 顶端 基准 状态 下
的 从 标 (ze 人 ,ye ,ze 全 ) 。 设 促 动 器 在 工作 状态 时 的 顶端 标 为 z2 全 到 :(;zf ©)-
由 于 促 动 器 底 汕 与 促 动 器 顶 问 始 终 在 一 条 直线 上 ， 故 存在 比例 关系 :
下- us 一， co
国 二 全 F ORP O E P ORO)  FORF OI )
Jtt, L,G)REGEABAG BINS, y 斩 和 办 方向 均 同 在 相同 的 比例 关系 ，
因此 有 :
TAR 五 (er 一 2G) eg
VCO-OTO-TOTEO- OO
人 LOGE ~y ©)
YOTVee wor OPTERO OO ©
+ 人 二 大 人 (z" 国 一 2 全 ) o
FONEe sor ve vor me GO 人
ChE, Sidil SRAE] T RdAG2508 00 M4 I L, 人 与 对 应 主 索 节点 的 坐标
(zw (gw (6),zw D) ZIH%R . BIMAL G) (ERR(6-4yh 5 T 552 E n TiAd
似 度 计算 目标 函数 的 决策 变量 ， 整 理 可 得 :
COrOLOLEO ~  wemn  F [LO-IO7  6D)
Co
612 约束 条 件 的 确定
《CD 节点 之 同 的 伸缩 变动 率 约 束
根据 假设 6, 相 邻 节点 之 间 的 距离 可 能 会 发 生 微小 变化 , 变化 幅度 的 极限 为 00796，
的 可 构建 如 下 约束 条 件 ;
n

## Logical image page 12

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 12 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A12.jpg -->
<!-- source_image_sha256: 7F9E2235974AEE6EE9ED9EABF1BBA67B1427546E3E7332ED14BB6232596AC64C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

[的 一 = 后] ?二 VIORSTC) ?+ [z 二 一 z 提 ] ”0 人
栅 的 一 二 于 基 的 一 的 区 何 二 5 的 > 和 <
区 的 一 = 的 ]?+ [的 一 3 的 ]?+ [Ex 的 一 z]? 0 0 07gGa
村 国 一 的 ] 行 若 的 二 的  [ro) m@P ~ OTOTRNRD E
其 中 ， 已 = 《Guia €IXT}.
(2) 促 动 器 伸缩 范围 约束
根据 题 设 ， 促 动 器 伸缩 量 只 能 在 -0.6m 到 十 0.6m 之 间 ， 故 具有 如 下 约束 条 件 ;
~0.6<L() =0.6 (6-9)
G3) 下 拉 索 长 度 约束
主 索 节点 与 促 动 器 顶端 是 由 固定 长 度 的 下 拉 索 连接 的 ,可 通过 基准 状态 下 的 主 索 节
点 的 举 标 与 促 动 器 顶端 基准 坐标 ， 计 算出 每 一 段 下 拉 索 的 长 度 。 设 每 一 段 下 拉 索 的 长 度
为 环 ( 念 ， 基 准 状态 下 主 索 节点 坐标 为 (zo 人 ,yo(8),zo 全 ) ， 促 动 器 顶端 基准 坐标 为
(@@.y @,2°@). Wt:
LO=Vim® —=@ ® —vOF ® —#OFeT io
设 促 动 器 在 工作 状态 时 的 顶端 坐标 为 (z+ (6),3+( 全 ) 出 存 在 站 下 约束 条 件 ，
[的 一 二 的 ]+ ¥®) —y O1+ 30 ~#O*~LO GD
613 反射 面板 调节 优化 模型 的 构 如
综 上 所 述 ， 本 文 建兰 的 网 射 面板 调节 优化 模型 为 :
GD) = argmin > L®-16)? (6-12)
Co
[的 一 = 的 ]?+ [Gy 的 ]?+ [266) 一 的 |
于 网 一 网 ] 于 他 的 二 的 JE 全 一 ma 的 和 >G 0907 和 "0 们 <
区 的 一 = 的 ]?+ [8 2 的 ]?+ [266) 一 z 的 | 了 7 别
TESTORITORESOUIISCESCD E
-0.6 三 五 全 三 0.6, ViE 工
的 一 一 的 12 区 —v* O)+ 6O) —# O1-LOAieT
62 问题 二 模型 的 求解
62.1 算法 设计
由 于 问题 二 共计 顺 要 求解 2226 个 主 过 节点 的 zyz 储 标 , 以 及 其 对 应 的 促 动 器 伸缩 量
五 ， 需 要 求解 的 决策 变量 数量 庞大 且 其 中 带 有 非 线性 的 等 式 和 不 等 式 约束 , 因此 必须 寻
找 适 应 于 高 维 大 规模 问题 求解 的 算法 。
对 于 模型 中 非 线性 约束 ， 首 先 基于 拉 格 朗 日 乘 子 法 的 思想 ， 引 入 一 个 乘 数 入 ， 将 等
12

## Logical image page 13

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 13 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A13.jpg -->
<!-- source_image_sha256: 56D54E01E6B3CDB0D253E874F62AFCC70957D35BF8B24BF90B4BB3E24C1BED18 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

式 非 线性 约 东 转化 为 目标 函数 的 一 部 分 。 接着 , 在 不 考虑 不 等 式 约 束 的 情况 下 进行 求解 ，

当 结果 秆 反 不 等 式 约束 时 ， 将 其 转化 为 等 式 约束 并 再 此 求解 ， 直 到 得 到 不 违反 约束 的 最

优 解 。 注 意 到 待 求解 的 模型 中 的 非 线性 约束 都 能 表示 为 决策 变量 的 二 次 型 ， 具 有 光滑 和

凸 的 性 质 ， 且 容许 在 数值 定义 域 上 轻微 违反 约束 时 稳定 求 值 ， 因 此 此 处 使 用 拟 牛 顿 方法

中 的 BFGS 方法 ， 以 在 不 直接 计算 Hessian 第 阵 的 情况 下 实现 这 一 高 维 问题 的 超 线性 收

仇 。 具 体 求解 算法 如 下

和 一

1: 初始 化 参数 。 为 循环 变量 必 赋 初始 值 # 王 0 ， 为 切线 刚度 矩阵 Bo 冉 初始 值 为 单位
阜 阵 ， 设 置 初始 解 zo 为 主 索 网 节点 在 附件 中 的 基准 态 举 标 。

2: 循环 : 根据 条 件 杞 Pr 一 -Vf(za， 计 算 ps-

3 由 式 aa 一 因 十 os 天 得 到 zxsa, 其 中 au 的 信 从 1.0 开始 折 半 查找 ， 直 到 步

长 足够 小 时 ， 函 数值 低 于 上 一 步 。

“ ia=ap. 1=VSG@) 一 VC
; 下 Basisg Be ， ng
四 计算 新 的 切线 刚度 乱 阵 及 4 一 及 一 号 光世
6: FURT: A6SRTARNRASE, %1ak BIEA ARESAMLRENT
cpsilon. WHBSItERIE, FiFFLA FHBEEN 2 行 。
622 反射 面 调节 情况 的 求解 与 分 析 :

由 于 问题 二 中 使 用 到 了 族 转 的 坐标 系 ， 故 本 问 理想 抛物 面 的 结果 可 以 在 旋转 坐标 变
换 的 条 件 下 ,得 到 了 顶点 坐标 为 (-49.392, - 36.943, - 294.450) 的 扫 物 面 。 接着 ,基于
算 湛 寻 在 MATLAB 中 编程 进行 求解, 给 出 求解 出 的 3D 的 促 动 器 提升 量 图 (图 7 72)
及 3D 的 理 业 掀 特 面 的 拟 合 误差 图 《图 7 右 ):

RE o _— e
”AAA v
me w A a .

£d . \B | 下
人 Ci |
mm |

上 |
 _ 本 * S

ow 。 w TY

图 7: 3D 促 动 器 提升 量 〈 左 )、3D 理想 曲面 拟 合 误差 《 右 》

由 图 7 左 可 知 , 此 状态 下 促 动 器 的 提升 量 处 于 =0.4m 到 0.6m 的 范围 内 , 此 时 反射
面 较为 贴近 所 求 理 想 摔 物 面 ， 且 促 动 器 顶端 上 下 拉动 下 拉 索 的 长 度 范围 也 较 小 。 由 图 7
《 右 ) 可 知 , 此 状态 下 理想 拢 物 面 的 拟 合 误差 处 于 0 到 7X10“ 的 范围 内 , 拟 合 误差 也 较
小 ， 说 明 此 时 的 结果 为 合理 最 优 解

13

## Logical image page 14

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 14 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A14.jpg -->
<!-- source_image_sha256: 30C608BD9B58C8A074572A4BD6E6116D79D9E7392B1D622BF84A86828ECCCAC2 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

6.2.3 结果 检验

基于 6.2.2 节 中 的 结果 ， 求 出 主 网 节点 与 理想 抛物 面 间 的 球面 径 向 误差 以 及 主 网 节
点 间距 离 的 变化 率 :

下 中

图 8: 主 网 节点 与 理想 抛物 面 球面 径 向 误差 〈 左 )、 主 网 节点 各 距离 变化 率 〈 单 位 ， 百 分 数 )《 右 )

由 图 8〈 左 ) 可 知 ， 此 状态 下 主 网 节点 与 理想 抛物 面 间 的 球面 径 向 误差 处 于
-8X10* 到 6X104 的 范围 内 ， 可 见 此 径 向 误差 非常 小 ， 此 时 反射 面 较为 贴近 所 求 理想
抛物 面 。 由 图 8〈 右 ) 可 知 ， 此 状态 下 主 网 节点 间距 离 的 变化 率 处 于 -0.0696 到 有 0.06% 的
范围 内 ， 充 分 利用 而 并 没有 违反 0.07% 的 裕 度 ， 说 明 此 时 的 结果 是 合理 的 w

七 、 问 题 三 模型 的 建立 与 求解

7.1 问题 三 模型 的 建立

问题 三 要 求 基于 问题 二 的 反射 面 谓 节 访 案 ， 计 算 调节 后 馈 源 舱 的 接收 比 ， 并 与 基准
球面 接收 比 作 比 较 。 由 生 该 问题 闪 本 文 首先 通过 使 用 旋转 变换 ， 将 倾斜 入 射 光 线 转化 为
垂直 入 射 光线 时 其 次 ,通过 求解 线性 方程 组 ， 依 次 确定 出 入 射 光 线 与 三 角形 面板 的 相交
判定 式 S 交点 坐 丢 、 三 角形 面板 的 法 线 向 量 ， 并 利用 光线 垂直 入 射 的 性 质 ， 使 用 法 线 向
量 简化 计算 得 到 红 射 光线 的 方向 角 。 再 次 , 通过 联 立 射线 方程 与 馈 源 舱 所 在 的 目标 高 度 ，
得 出 射线 方程 的 步 长 和 出 射 光 到 达 目 标高 度 时 的 坐标 ， 并 与 馈 源 舱 的 有 效 区 域 进行 比 对 ,，
作为 入 射 光线 是 否 被 有 效 接收 的 判定 式 。 最 后 ， 将 300 米 口径 内 实际 接收 区 域 作 为 积分
域 ， 将 入 射 光 线 有 效 接收 判别 式 作为 被 积 函 数 ， 使 用 蒙特 卡 洛 算法 进行 积分 ， 计 算 有 效
接收 的 光源 面积 和 调节 前 后 的 信号 接收 比 。

7.1.1 反射 光线 几何 模型 的 建立

首先 ， 要 在 新 坐标 系 中 计算 反射 点 在 反馈 面板 三 角形 区 域内 的 坐标 。 设 新 坐标 系 的
空间 变量 为 (zw;,gwr,zwr)， 在 萄 十 蓄 和 150? 的 范围 内 ， 沿 着 z 轴 负 方 向 均 有 来 自 于 被 观
物体 的 电磁 波 照 射 在 反射 面 上 。 记 反射 面板 上 一 三 角形 三 个 顶点 忌 , Ba Be 的 坐标 分 别 为
B, (zw (和 gw (Da (3) + Ba(zw (yw (jz (52))  Ba (zw (jywr(a),zm(ja))，
表示 三 角形 了 访问 的 主 家 节点 的 坐标 。 其 中 编号 7E IT= 1 攻 = (, ti) €IXIXT}.

## Logical image page 15

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 15 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A15.jpg -->
<!-- source_image_sha256: 8148C85D05AE47CE0E456151041516883665806141BA37BE970DB692A3B57015 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

和 ta)
和 rr(h)emor(A) (ojegB 用
志 rr) 3
人 Toe030 sOD)
Na 人 -severeUDjraert
rsjrsvO)
& 上 stmCD)as0)
BNB (ae(1).3e ().203)
图 9， 反馈 面板 三 角形 区 域 示意 图
设 一 点 (zwgw;zm) 在 线段 及 Bs 上 ， 则 其 在 z 轴 的 坐标 可 以 表示 为 :
aw =niaw (§) + razw (说 CD
其 中 ,mu 加 >0 且 站 十 突 一 1。 接 着 ， 设 另 一 点 (zyzt ) 在 点 (zw;gywyztr) 与 忆 为 端点
的 线段 上 ， 该 点 在 > 轴 上 的 坐标 可 以 表示 为 :
anmz( 让 十 amazw( 说 十 ozw( 襄 a
it, 8,8,>0Ha +8=1.
ian=t, sra=t, s=ts. Hilt+h+t=106>0,L>0, t,>0. @Ed
WZATEY B5 2 BAEAR. LLL, 1931T —A7ELLBLBy By Ja TNSUR ARAY = itTE09 HF
面 上 的 坐标 为:
ap ze- (说 2w Go)) (0
wr |=|wwG) Ga wGo) || & -3)
欧 ) Na( 侣 各 加 种 ( 间 人 \ta
将 外 一 1 一 丘 一 刀 代 入 式 (7-3) 约 去 z 轴 的 坐标 ， 并 根据 矩阵 运算 法 则 可 得 :
(“) s (=2 —aw (G) 2w(id) TRON(wa) 人
t) (说 一 如 ww (G) —ww (G)) \wiw —ww (is)
注意 到 三 个 点 B, BaB。 为 三 角形 的 三 个 项 点 ， 式 (7-4) 中 的 逆 矩 阵 总 是 存在 。 因 此 ，
当 坐 标 (zy;g 多 ) 给 定时 ， 可 以 根据 式 (7-4) 计 算 丰 和 如 的 值 ， 进 而 判断 该 点 的 水 平面 投影
是 否 在 三 角形 的 水 平面 投影 的 内 部 。 根 据 实 际 条 件 ， 对 于 任意 在 驳 十 娩 寺 150? 范 围 内
的 (zy,gy)， 都 有 一 个 了 E :7 使 得 其 在 了 所 指 代 的 三 角形 内 部 。 故 可 进一步 根据 式 (7-3) 求
得 (zy,yy) 对 应 的 z 轴 坐标 为:
2ie =tuzw (3) + taz (32) + taz (is) a-5
JW, BHERE ERMMBTRIAR, IHRIAT L=45ByBy B ARV
向 量 地 一 (euieziea， 有 :
aw (n) —zw(2) ww () —uw (a) 各 (条 一 种 (和 Ne 0
2w (i) —aw (is) ww(G) —ww(Go) 2w() —awCin) [| e2|=[O) oo
2w (a) —2w (5) w (Gs) —vw () 2w (Ga) — 2w (3)/ \es, 0，
15

## Logical image page 16

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 16 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A16.jpg -->
<!-- source_image_sha256: 490348FC5770AF3B6BD0D572B754C2F69DAA0D9E6E48287C89DFD801EF2FD865 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

，
1
1 法 线 万 iA
20 A 到
到 到
入 射线 二 机
二
反射 点
图 10: 各 角度 三 维 示意 图
注意 到 ， 法 向 量 没有 归 一 化 且 式 (7.6) 左 便 短 阵 的 秩 为 2。 且 考虑 到 问题 所 求 的 拢 物
面 开口 向 上 ， 即 > 0， 故 令 es 一 1， 将 式 (7-6) 进 行 化 简 并 根据 短 阵 运算 法 则 可 得 ，
( 区 内 一 (条 ww(G) 2 的 (= G2) 2 on
人。 \aw(i) —2w (io) ww(i) —ww (G)) \aw (io) — 2a (3)
BFASAELTATFEAT, draaln, = 0,0,1); Bitn 5mik:
9 一 arccos 了 0
网 :四
接着 ， 将 法 向 量 元 投 影 到 水 面 后生 轴 的 方向 向 量 过 = (1, 0, 0) 的 夹 角 a 表 示 为 :
二 ea 三 0
=- lind, om
arccos 3 - 全 ea<0
四 :ma
另外 , 由 于 出 射 光 与 入 射 光 所 在 平面 垂直 于 反射 面 , 可 知 出 射 光 与 z 轴 的 赤 角 为 29 。
因此 出 射 光 的 方向 向 量 :
7 = (sin(26)cosa, sin (20)sina, cos (26)) a10)
以 上 ， 可 得 出 射 光 所 在 的 直线 的 标准 方程 为 :
mg\、 1/ 芭 、，1sinl2b)cosa
ww | =| vho | +r sin@0)sina am
w)  \a. 0s(26)
最 后 ， 要 确定 馈 浙 舱 接 收 平面 的 解析 表达 式 。 根 沁 题 目 ， 饭 源 能 接收 平面 的 法 线 方
向 指向 理想 抽 物 面 的 顶点 ; 距离 原点 的 距离 为 。 考 虑 到 由 于 馈 源 能 接收 信号 有 效 区 域 为
直径 1 米 的 中 心 圆 盘 ， 因 此 其 平面 方程 为
16

## Logical image page 17

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 17 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A17.jpg -->
<!-- source_image_sha256: 62A49AEF15902BE3A7C5D225E9F8D901BC8FDD2CEC472984784A0B01C9ACECBD -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

“|
{ 人 和 .
综 上 ， 在 新 坐标 系 中 构建 了 反射 光线 所 在 直线 与 局 源 能 接 收 平面 的 解析 表达 式 。
7.1.2 反射 光线 吸收 与 信号 比 计算 模型 的 建立
在 确定 了 反射 光线 与 馈 源 能 接收 平面 的 解析 表达 式 后 ， 即 可 判断 反射 光线 是 否 被 接
收 并 计算 反射 信号 比 。
首先 ， 将 接收 面 平面 方程 与 出 射 光 所 在 直线 方程 进行 联 立 ， 可 以 得 到 出 射 光线 命中
馈 源 能 所 在 z 平 面 的 行进 步 长 :
= CD9)
结合 式 (10) 和 (7-13)， 整 理 可 得 :
mg 一 区 十 2 sin (20) coscx
a feary
= +  in ()concx
$di, TTULET ABHARHEKTT  094Calpi) IFARAE R(-14)R B F0
如 。 因 此 可 以 通过 :
是 记 二 0.5? 且 28 十 好 二 0.52
rei +{ St =0 Hlzi + 4i3 >0.5 本
判断 反射 移 线 是 否 能 够 狼 接 受 面 吸收 。 进 一 步 ， 对 判断 函数 T(zwigm) 在
确 二 编 <1502 范 国内 积分 ， 可 以 得 到 被 局 源 航 吸 收 的 光线 所 占 的 面积 ;
人 rwamaaram CH
接着 ， 注 意 到 有 效 口径 内 的 每 一 个 点 都 必然 有 且 仅 有 一 个 相应 的 三 角形 ， 则 平面 内
接收 到 的 光线 面积 为 150?r 。 最 后 ， 可 得 接收 与 反射 信号 之 比 为 ;
n= s5077 .1y orrdowi CT
72 问题 三 模型 的 求解
72.1 算法 设计
对 于 问题 三 所 求 的 积分 数值 ， 如 果 直 接 对 整个 口径 贺 面 进行 积分 ， 则 对 于 每 个 输入
的 光线 坐标 ， 算 法 都 将 消耗 大 量 时 间 饥 历 =0y 平面 上 的 各 个 投影 三 角形 ， 以 确定 这 一 华
标 所 属 的 三 角形 法 线 ， 用 于 计算 出 射 光线 的 射线 方程 。 为 了 避免 这 一 逐 点 依次 进行 三 角
形 遍历 的 时 间 成 本 , 我 们 将 圆 形 口径 积分 域 分 解 为 各 个 互 不 重 登 的 z0y 投影 三 角形 积分
域 ， 通 过 对 各 个 三 角形 积分 域内 均匀 地 采样 各 个 光线 的 接收 判定 信息 ， 使 得 一 次 性 遍历
到 各 个 投影 三 角形 时 ,可 以 大 批量 地 使 用 同一 个 法 线 向 量 处 理 多 个 投影 到 该 三 角形 上 的
17

## Logical image page 18

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 18 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A18.jpg -->
<!-- source_image_sha256: 905D4C8CDE837B8A2650C0E225883FA82DE08810D136504165F0E9310B229682 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

入 射 光 线 ， 甚 至 使 用 足够 高 密度 的 采样 从 入 射 光线 的 接收 信息 还 原 出 馈 源 器 有 效 区 域 在
各 个 投影 三 角形 上 的 像 。 为 了 实现 三 角形 区 域 的 均匀 采样 式 积分 ， 我 们 设计 了 包含 对 边
界 条 件 精细 修正 的 蒙特 卡 洛 积分 算法 ， 算 法 细节 如 下 :
算法 3: 蒙特 卡 洛 算法

1， 设 置 接收 面积 近似 值 a: =0;
2: 遍历 三 角形 Je 了 7;
3: 设置 接收 次 数 初始 值 必 一 0:
4 抽样 次 数 10000， 循 环 :
® 每 次 在 0 到 1 之 间 平均 随机 抽样 生成 一 个 各 和 一 个 如 :
6 如 果 自 十 如 > 1
7 ti=l-t:
8: 如 :一 1 一 如
9: t=1-t—ts

10: 使 用 式 (7-3) 从 (bta, 妈 计算 出 (zz

Hs 使 用 z 和 9 计算 出 zOy 平 面 上 的 投影 向 量 长 度 ;

12: 如 果 向 量 长 度 超过 口径 的 一 半 150 米 ;

13: 跳 过 这 次 接收 计算 ， 跳 转 到 第 16 往 ;

14: 使 用 (z,, 妇 计算 出 是 否 接收 ， 如 果 接 收 :

15; d:=d+1;

16: 如 果 质 样 次 数 没 满 ， 跷 转 到 第 4 行 循环 :

17:)J 1 计算 出 三 角形 了 在 zOy 平 面 上 的 投影 面积 ，

1 ay:=a, +d/10000 (阴影 面积 )

19:” 如果 遍 历 三 角形 没 结束 ， 跳 转 到 第 2 行 继续 饥 历
20: 输出 ayGL50?m) 即 为 所 求 接收 率 ;

7.2.2 问题 三 的 结果 与 分 析

基于 算法 3， 在 MATLAB 中 编程 进行 求解 ， 给 出 求解 出 的 在 相同 区 间 下 ， 工 作 态
《 左 ) 与 基准 态 〈 右 ) 中 ， 反 射 面板 与 有 效 入 射 点 区 域 的 纹理 对 比 图 。 其 中 ， 黑 点 表示
光波 经 反射 后 ， 可 以 被 馈 源 能 接受 平面 的 中 心 有 效 区 域 吸收 的 反射 面板 的 入 射 点 区 域 。
图 11 中 所 选取 的 区 间 横 坐 标 范围 为 (-90 - 30?)， 对 照 图 5， 可 得 此 区 间 基 准 态 和 工作
春之 间 偏 移 量 的 相对 斜率 最 大 ， 夹 角 差异 最 大 ， 导 致 基准 态 时 部 分 反射 面板 中 的 “有 效
接受 反射 命中 点 ”逐渐 偏 移 至 反射 面板 外 部 ， 进 而 反射 率 也 相应 降低 。 因 此 工作 态 和 基
准 态 下 ， 最 终 产生 的 反射 效果 相差 较 大 。 最 终 计算 得 到 的 调节 前 接收 比 0.81196， 调 节 后
接收 比 1.10396， 提 升 了 36"6。

18

## Logical image page 19

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 19 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A19.jpg -->
<!-- source_image_sha256: C39C9583D439EADCD759B3E9AA8412ED06F3A8DD866BE7A434684340B22D5F5F -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

mso S——
aVR 2 A7 SAAS
DCDCDC NA 村
AAS 此 OCX
DA DC
CCDG 水 XCDOG
和
图 11: 在 相同 区 间 下 ， 工 作 态 〈 左 ) 与 基准 态 〈 右 ) 纹理 对 比
将 计算 得 到 的 此 情况 下 反射 光线 聚焦 于 焦点 的 状态 进行 可 视 化 处 理 ， 得 到 图 12。
人
0
“ee
-300 L NY
2003 . 四 加
0 As 200
3
-oo 55%
图 2 反射 光线 聚焦 于 焦点 的 示意 图
由 图 这 可 观察 到 ,- 泪 上 情 况 下 ， 由 观测 点 8 方向 射出 的 平行 均匀 光波 被 精准 地 反
射 到 子 馈 源 和 能 有 效 接收 区 域 ， 故 所 得 结果 符合 题 设 。
723 问题 三 结果 检验
基于 7.22 节 中 的 结果 ， 对 蒙特 卡 洛 积分 的 稳定 性 进行 检验 。 在 工作 态 与 基准 态 下
各 积分 100 次 ， 得 到 数值 波动 量 如 图 12:
Le RE
00104 | 出 了 sd 有
oot0s L
oo 0 w o 0 io
元 io 3 -一
7.65Ty 二 和
加 和 4e™ Bil -
0 320 4 6 8 10
图 13， 工 作 态 《上 ) 与 基准 态 〈 下 ) 下 多 次 蒙特 卡 洛 积分 的 数值 波动 量
19

## Logical image page 20

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 20 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A20.jpg -->
<!-- source_image_sha256: 7E2F4A4E8D662B15514C300B3330824EE116C382D6E648486CE75DD46FE24D7D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

观察 光 班 分 布 偏 移 ， 由 图 13 可 得 工作 态 下 与 基准 态 下 ， 多 次 蒙特 卡 洛 积分 的 数值

波动 量 范围 都 在 10- 的 维度 上 ， 波 动量 较 小 ， 可 以 认为 结果 合理 。
八 、 模型 的 评价 与 推广
8.1 模型 的 评价

本 文 构建 的 FAST 射电 望远镜 的 工作 抽 物 面 调整 模型 ， 对 于 利用 促 动 器 调整 工作 摧
物 面 的 过 程 进行 了 合理 假设 ， 在 保证 模型 求解 结果 精确 性 的 条 件 下 ， 有 效 降 低 了 模型 的
复杂 程度 。 在 求解 过 程 中 ， 利 用 了 二 分 法 ，BFGS 法 ， 蒙 特 卡 洛 积分 等 方法 对 于 模型 进
行 求解 ， 使 得 算法 的 收 敏 速度 快 且 结果 精确 。

在 第 一 问 的 理想 扼 物 面 求解 过 程 中 ， 考 虑 到 摔 物 面 是 由 抛物 线 滞 轴线 旋转 得 来， 故
将 空间 的 问题 转化 为 平面 从 标 系 下 的 问题 ， 使 得 模型 措 述 更 为 简便 。 对 于 限定 了 焦距 的
抛物 线 方程 ， 本 文 以 使 其 与 基准 球面 的 近似 程度 最 大 为 最 优化 条 件 ， 对 于 其 焦距 进行 了
优化 ， 从 而 确定 了 最 优 的 掀 物 面 方程

在 第 二 间 的 工作 抛物 面 调整 过 程 中 , 考虑 到 拓 物 面 的 开口 方向 与 原先 的 从 标 和 方 向
并 不 相同 ， 本 文 将 原先 的 直角 举 标 系 进行 旋转 ， 使 得 原先 的 储 标 负 方 向 依然 指 何 狼 测 物
体 ， 使 得 摔 物 面 方程 的 拱 述 更 为 简化 ， 构 建 出 的 模型 更 加 简明 。 并 且 奏 紫 过程 息 和 通过
极 坐标 变换 , 利用 了 第 一 问 得 出 的 结论 , 节省 了 公式 推导 的 工作 性。 在 未 解 时 利用 BFGS
法 ， 将 约束 条 件 转化 为 二 次 型 ， 提 高 了 算法 的 收 仇 速度 互 精确 度 [

在 第 三 问 的 馈 源 能 接收 比 计算 模型 中 ， 本 文 将 直角 下 称 ， 施 位 角 等 概念 结合 使 用 ，
在 旋转 后 的 直角 坐标 中 通过 构建 参数 性 判断 三 角形 平面 与 直线 的 相交 关系 ， 使 得 模型
的 推导 过 程 更 加 简单 。 在 求解 有 效 接受 的 光源 面积 时 ， 使 用 蒙特 卡 洛 积分 的 方法 进行 求
解 ， 在 一 定 程度 上 提高 卫 解 算 的 速度 。

82 模型 的 改 迁

与 亦 际 情 况 相 比 ， 题 目 中 缺乏 边界 结构 如 何 因 定 的 相关 信息 ， 如 支撑 结构 等 ， 这 就
使 得 在 确定 整个 工作 摔 物 面 时 约束 条 件 是 不 够 充分 的 。 若 能 够 提供 最 外 转 反 射 面板 的 国
定 方式 ， 并 且 合理 假设 在 边界 的 节点 之 间 的 距离 约束 等 条 件 ， 可 以 对 于 工作 挑 物 面 的 边
界 条 件 进行 建 模 ， 并 且 通过 各 个 节点 之 间 的 连接 关系 间接 地 传递 约束 ， 从 而 给 出 FAST
射电 望远镜 所 有 促 动 器 伸缩 量 的 调整 策略 , 构建 出 可 以 投入 实际 调度 的 工作 抛物 面 调整
模型

九 、 参 考 文献

[1] 杨 凡 , 李 广 云 , 王 力 ， 三 维 符 标 转换 方法 研究 [测绘 通报 ;2010 (6): 57

[2) 压 纯 ， 王 正 林 . 精通 MATLAB 最 优化 计算 [M]. 电子 工业 出 版 社 , 2009.

3] Beavis B, Debbs 1. Optimisation and_ stability theory for economic analysis[M].

Cambridge university press, 1990.
20

## Logical image page 21

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 21 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A21.jpg -->
<!-- source_image_sha256: D58D819D3E91FD2E6F4AC7C56C3BA440B3D749C4461E8FE19E5118C88F6ACB59 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

十 、 附 录
10.1 主要 计算 程序 : 基于 MATLAB R2019a 开发
10.1. 1 主要 计算 程序
prob1_calc.m: 问题 1 的 求解 核心 算法
function [Lf angle300] = probl_eale0
% 问题 1 的 核心 计算 部 分
%% 积分 给 出 最 优 焦距
% 并 且 与 Constant 中 固定 的 焦距 做 比较
waming(ofr,.MATLAB:integral:MaxIntervalCountReached':
‘warning(off "MATLAB:integral: MinStepSize').
angle_min = acos(150/Constant sphere_radius);
LE= fzero(@(Lbint_dL(LE, angle_min), [100, 400]);
disp(" 问 题 1 最 优 焦 距 LE "+mat2ste(LE17));
disp(" 问 题 1 最 小 误差 平方 积分 : "+mat2strinf CIXDE atiBiLniingif7)
assert(abs(int_dL(Lf, angle_min) < sqri(eps)):
assert(Lf == Constant.Lf);
[~ ~ angle] = Constant.get_rad_angle(),
£= @(angle)abs(Polar para(Lf, angle)*cos(angle))-150;
angle300 = frero(f, [pi/2, angleend)]);
assert(abs(f(angle300) <= sqri(eps));
end
function v = int_I(L, angle_min)
v = integral(@f, angle_min, pi/2),
function err = f(angle)
[L, ~] = Polarpara(Lf angle);
em = (L-Constant.sphere_radius).*(L-Constant sphere_radius);
radius = Constant.sphere_radius.*cos(angle);
erm = erm.*(2.*pi.*radius);
end
end
function v = int_dL(L, angle_min)
v ~ integral(@f, angle_min, pi/2).
21

## Logical image page 22

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 22 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A22.jpg -->
<!-- source_image_sha256: 892E7C77F07C926BE4DF9B3238CEDCE8E882A251F9C5330647C73688CE33FC3C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

function derr = Wangle)
[L dL] = Polarpara(Lf angle);
derr =2*dL.*(L-Constant sphere_radius);
radius = Constant.sphere._radius.*cos(angle):
derr = derr*(2.*pi.*radius);
end
end
prob2_calc.m: 问题 2 的 求解 核心 算法
function [fval, opt_X, opt_XYZ, opt_Lz opt_ABR, index W Winv,
edge, edge_distSQ. motor hi motor unit motor distSQ] = prob2_cale()
elfreset’;
‘mg(default);
clear global
% 初始 化 数据 集
data = Data();
% 初始 化 旋转 变换 矩阵
[W, Winy] = Polar.compose_rotate(Constant.alpha, Constant beta);
% 选择 300 口径 内 的 节点
人 angle300] = probl_calc();
mnain XYZ = data.main_node_coordinate;
main_ ABR = Polar.xyz2abr(main_XYZ*W');
index = main_ABR(:.2) >= pi-angle300;
N_nodes = sum(index).
main XYZ =main_XYZ(index, :: % 过 滤 主 网 节点
edge = data.edge(all(index(data.edge).2),:); % 过 小节 点 之 间 的 连 边
index2(index) = 1:sum(index): % 构建 过 滤 之 后 的 新 的 节点 下 标 顺序
edge = index2(edge); 9% 使 用 新 的 节点 下 标 对 连 边 节点 序号 重 定向
assert(all(all(edge))): % 连 边 节点 序号 不 能 有 空 泡
% 初始 化 邻 边 长 度
edge_distSQ = main XYZ(edgeC:D):)-main XYZ(edge(:2).):
edge_distSQ = sum(edge_distSQ.*edge distSQ.2);
% 促 动 器 预 处 理
motor hi = datamotor higher base(index, :);
motor lo = datamotor lowertindex 小
22

## Logical image page 23

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 23 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A23.jpg -->
<!-- source_image_sha256: 00FF6506B2E5DA072E903BA1657DD6605956B738B097FA8BF2B916C12529C095 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

motor_ unit = motor himotor lo;
motor_ unit = motor_unit./sqri(sum(motor_unit.*motor_unit.2));
motor_distSQ = main_ XYZ-motor hi;
motor_distSQ = sum(motor_distSQ.*motor_distSQ, 2):
objeetive = @(X)obj_SSECX, W N_nodes):
nonlcon = @(X)onstraints(X, edge， edge_distSQ， motor hi， motor unit,
motor_distSQ. N_nodes);
 testhit(..
pack(main_XYZ, rand(N_nodes, 1)).
objective,..
nonleon.
天
opts = optimoptions(fimincon, Display’, iter-detailed);
opts. FunValCheck = ‘on';
opts.SpecifyObjectiveGradient = rue;
opts.SpecifyConstraintGradient ~ true;
opts. MaxFunctionE valuations = inf;
opts. Maslterations 二 inf
opts. HonorBounds = false;
% opts SubproblemAlgorithm = cg'
opts. Hessian Approximation = Ibfes’
saved ~ load(prob2);
iftrue,
opLX = saved.opt_X;
else
opt_X = fimincon(objective, pack(main XYZ, zeros(N_nodes, D) 中 [1 [1. [1...
pack(-inf{size(main_XYZ)). repmat(-0.6, N_nodes, 1))... %Ib
pack( inf{size(main_XYZ)), repmat( 0.6,N_nodes, 1)... % ub
‘nonlcon, opts): %#ok<UNRCH>
end
val = obj_SSE(opt_X, W, N_nodes);
[opt XYZ, opt_Lz] = unpack(opt_X, N_nodes).
23

## Logical image page 24

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 24 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A24.jpg -->
<!-- source_image_sha256: 275B44DB820A38156550107057565AD163AC28432D7377AD9C67676A2A40AE1C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

opL ABR = Polar.xyz2abr(opt XYZ*W'):
end
function [SSE, dSSE_dXYZ] = obj_SSE(X. W, N_nodes)
% 目标 函数
% 球面 径 向 投影 Dw《 理 想 拢 物 面 ) 和 主 网 节点 实际 投影 位 置 L 之 间 的 误差 平
方 和
%
[XYZ, Lz] ~unpack(X, N_nodes);
[abr ~ db, dr] = Polar.xyz2abr(XYZ*W');
[Lw, ~ dangle] = Polarpara(ConstantLf abr(:.2.1):
err = Lw-abr(;3);
SSE = err*err;
SSE_dXYZ = 2.¥err* (dangle.*db-dr);
dSSE_dXYZ = dSSE_dNYZ*W;
ASSE_AXYZ = [dSSE_AXYZ(); zeros(size(L2))ly
end
function [¢.ceq,ge.goeq] = constraints(..
Y
edge, edge distSQ, .
motor_hi, motor_unit, motor distSQ, N_nodes)
%
% 约束 条 件 〈 二 次 型 )
% 条 件 1: 保持 主 网 节点 之 间 的 连接 索 的 距离 保持 固定
% 条 件 2: 保持 主 网 节点 与 相应 的 促 动 器 之 间 的 距离 〈 下 拉 索 ) 保持 固定
[XYZ, Lz] =anpackCX. N_nodes);
errdist = XYZ(edge(:,1))-XYZ(edge(:2),):
edist = sum(errdist *errdist.2);
©= [edist-edge_distSQ*(1.0007+1.0007); edge_distSQ*(0.9993%0.9993)-cdist]:
11 = sub2ind(size(XYZ), repmat(edge(:.1).1,3). repmat(1:3.numel(edist). 1)):
12 = sub2ind(size(XYZ), repmat(edge(.2).1.3). repmat(1:3.numel(edist).1)):
J= repmat(1:numel(edist)., 1, 3);
E
24

## Logical image page 25

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 25 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A25.jpg -->
<!-- source_image_sha256: 9E92AAC934FAB1844A8E13E7C8958C14BC012F8C50586D05312B0749ADBB71AE -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

sparse(...
reshape([11 12}[].1)....
reshape[J IL[1.1).
reshape(2.* ferrdist -errdist}[].1)....
namelCX)numeledisD),，
-sparse(
reshape([11 12J{J,1)....
reshape([J IL{J.1)..
reshape(2.*ferrdist -erndist] [11)..
numel(X),numel(edist)
上
motor_hi_new =motor_hi+Lz *motor_unit;
errdist = XYZ-motor_hi_new;
edist = sum(errdist. *errdist, 2);
ceq = edist-motor_distSQ;
J= repmat((1:numel(edist).. 1, 4);
geeq = sparsed...
reshape(1:mumel(X).[1.1)...
restiape()).1)..
reshape(2 *ferrdist -sum(errdist *motor_unit,2)L[},1).
numel(X),mumel(edist):
end
function [SSE, dSSE] = constr_test_ceq(X, constraints)
[-ceq.~gceq] = constraints(X);
SSE = ceq*ceq;
SSE = full(2*goeq®eeq);
end
function [SSE, dSSE] = constr_test_c(X, constraints)
[sg = constraints(X);
SSE =c*e;
SSE = full(2*gete)
end
function f testkit(data, objective, constraints)
25

## Logical image page 26

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 26 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A26.jpg -->
<!-- source_image_sha256: 80B813412D43EAA75AA5851903D91528117E09D23AB5A3F48C4D60175AA1969A -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

% 函数 微分 正确 性 检查

人 = objective;

fori= 110
index = randi(numel(data) 4*3).
ratio = linspace(0.1, 10.0, 20);
dif_ =armyfun(@(rderr_difr index), ratio);
ana_~ amayfun(@(rderr_ana(r, indexh, ratio);
disp(" 信 品 比 : "fnormtdiff -ana_)norm(ana 六
plot(ratio, diff -ana );
hold on

end

£=@(X)constr_test_ceq(X, constraints);

fori= 1:10
index = randi(numel(data));
ratio = linspace(0.1, 10.0, 20);
ana_~ arrayfun(@(r)derr_ana(r, index), ratio):
dif_= arrayfun(@(r)derr_dil(s, index), ratio);
disp(" 信 品 比 : "snorm(dift -ana )norm(dift ));
plot(ratio, 直人 -ana 小
hold on

and

£=@(X)constr_test_c(X, constraints);

fori= 110
index =randinumeldatay4*3)
ratio = linspace(0.1, 10.0, 20);
ana_= arrayfun(@(derr_ana(r, index), ratio);
GT_~ arrayfun(@(r)ders diff(r index), ratio):
disp(" 信 噪 比 : "fnormtdiff -ana )mormtdiff 六
plot(ratio, dif -ana );
hold on

end

function dSSE = derr_diff(ratio, index)
assen(isscalar(ratio));
ASSE = (f(set(index, ratio e-4))-fiset(index, ratio-1e-4). 2e-4;

end

26

## Logical image page 27

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 27 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A27.jpg -->
<!-- source_image_sha256: 413DC723997E69C7027496759FF07AF68BF627626390D94F68426B6CBD5BCBE9 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

function dSSE = derr_ ana(ratio index)
asset(isscalar(ratio));
[~ dSSE] ~ fsettindex ratio)):
dSSE = dSSE(index)* dataindex);
end
function newdata = set(index, ratio)
newdata = data;
newdata(index) = newdata(index)*ratio;
end
end
function X = pack(XYZ, 1.2)
X= [XYZ(): IT
end
function [XYZ, Lz] = unpack(X, N_nodes)
assert(numel(X) 一 4*N_nodes);
XYZ = reshape(X(1:3*N_nodes), [J, 3);
12= XG*N_nodes* Liend);
End
prob3_cale.m: 问题 3 的 求解 核心 算法 〈 含 画图 输出 ， 检 验 等 )
9
aear0)
‘mg(defaule);
close(all),
clear global
lobal opt XYZ index W
[~ 0ptXYZ, ~~ index, W, ~] = prob2_calc(lfireset);
% 画图
elfreset);
“% plot_working illu_3d(true);
elfreset);
2% plot_2d.texture(true);
elfCreset’;
9% plot_2d_texture(false);
rec_ratio_work = [0.011020300922443 0.0110003218576217 0.0110518782939506
27

## Logical image page 28

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 28 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A28.jpg -->
<!-- source_image_sha256: E0E78E02095F4D591E24317CA9C7C9BD21B2DB9CC859C6F9AD80ED4A388395B8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

0.0110643817438084 ”0.0109730660550652 0.0110257601080111 0.0110223227972293
0.0110485078071177 “0.0110240151884694 0.0110130230869417 0.0110164104558229
0.0110550668326781 0.0110459270545307 ”0.0109882612985835 ”0.0110436769357324
0.0110367034749252 0.0110481766120668 0.0110321572590037 0.0110749365711392
0.0110386802631623 0.0110153292520637 ”0.0110192330970475 0.0109874238643901
0.0110296311887876 0.0109757385346491 0.0109755111105056 0.0110288022004406
0.0109799794453533 0.0110238540462687 0.0110453042446409 ”0.0110284372401636
0.0110669362584378 ”0.0110526144686468 ”0.0110334430375848 0.0109741922281317
0.0110478434113818 ”0.0110341899191246 ”0.0110517591813282  0.0110496603830398
0.0110046254841212 0.0110235600140406 “0.0110550698235744 ”0.0110649714478939
0.0110474009766273 0.0110420096870245 ”0.0110365756602061 0.0110091725112358
0.0110382613793932 0.0110600521586413 0.0110028232503258 0.0110465102463241
0.0110136604630215 0.0110101135220489 0.0110183405377215 ”0.0110043363971838
0.0109958279906651 ”0.0110837873612865 ”0.011065917248056 0.0110277008429329
0.0110127664607068 0.0110545986531244 ”0.0110345008277633 ”0.0110429260222507
0.0110505079293461 ”0.011039406367263  0.0110103799922359  0.0110289593537192
0.0110541998462448 0.0110513385417147 ”0.0110529854247001 0.0110445898913447
0.0110180088017255 0.011022189720714  0.0110627343553963 0.0110285841846507
0.0110817414943682 ”0.0109907491678801 0.0110200180167431 “0.0110311268543086
0.0110146584529961 0.0110255093771213 0.0110528637613645 0.0110777319262726
0.0110169034101532 ”0.0110789763845019 0.011086907752962 0.0110068509917417
0.0110202757278154 0.0110403474743263， 0.0110425429291141 0.0110162286817121
0.0110382443277745 “0.0110068533880955。 0.0110452395673006 0.010996333441479
0.011000327429337 】0.0110230589753898  0.0110471891212048 0.0110296744899169
0.0110090500347684];

ree_ratio_base - [0.00809957344004469 0.00816030276752031 0.00815114719028782
0.00809170932206714 0.00813359107499093 0.00815073014613017 0.00808926197249174
0.00808170453150241 0.00806468281488732 0.0081182224458027 0.00809664564432054
0.00803929331956928 0.00813862975913561 0.00812651614405913 0.00807548662594117
0.00809838752451361 0.00809400286528839 0.00811009080826381 0.00810822712967782
0.00809315525807824  0.00806486974020875 0.008134630287794 0.00807892790322006
0.00805598714908852 0.00813180369790822 0.00810668350665907 0.00807828088140091
0.00811052825834018 0.00810927517071732 0.00811143502132163 0.00810309576115239
0.00810982854434356 0.00811344740473194 0.00814411524881943 0.00810455307681079
0.00806302524392838 0.00808600818409412 0.00812354564034997 0.00811186777478928
0.00809026737854994 0.00808663956574123 0.00814128338195877 0.00807940794169834
0.00812115941770167 0.0081024286210036 0.0080924217013025 0.00809501225610337
0.00809902994305578 0.00812940497617186 0.00809554341149597 0.00809631643018426.
0.00804895426011689 0.00809575027496546 0.00812928273720676 0.00811334164853845
0.00812004359958459 0.00810587906967159 0.00807971230125123 0.00810458060650855
0.00809081157217132 0.00807630129046536 0.00812220517987459 0.00811206634654426
0.00810709806891063 0.00815164906999222 0.00813766254713846 0.00814321524369861
0.00810908041014188 0,00812934844902824 0.00810621605696549 0.00811063002236979

28

## Logical image page 29

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 29 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A29.jpg -->
<!-- source_image_sha256: 4E45EEA1A53569F2B396B7131B3357986BCF5B248DB46DD5EF9B73A6D84C128A -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

0.00812537388975942 0.00809493844001929 0.00811284919748417 0.00812982625291347
0.00811444175548698 0.00812948462742588 0.00812471872392731 0.00809515370106578
0.00810070201885477 0.00809154975241786 0.00809924616852124 0.00808220053817524
0.00812402217146259 0.00811192024738402 0.00806217864697205 0.00809729197336589
0.00814243000329029 0.00814908482651054 0.00805549860700152 0.00812911963465325
0.00809820772628644 0.0080799192180059 0.00812099010446983 0.00811185636211377
0.00810677088931511 0.00812457458272667 0.00811715912091946 0.00810254234380183
0.00812512633851956];
subplot(2,1.1);
hold on
plot([1:100:1:100) [repmat(mean(rec_ratio_work),size(ree_ratio_work))irec_ratio_work]
MLineWidth 2);
plot(1:100,rec_ratio_work,ko' LineWidth'2);
boxon
grid on
style(fontmame' ‘fontsize’),
%y1im([0.01033, 0.01045]);
subplot(2,1,2);
hold on
plot([1:100:1:100} [repmat(mean(ree_ratio_base).size(rec_ratio_base))rec_ratio_base]k
-LineWidth' 2);
plot(1:100,rec._ratio_base Ko, LineWidth' 2);
boxon
gridon
styleCfontname’, fontsize’),
fastprint(, 图 片 /prob3. 检 验 .多 次 蒙特 卡 洛 积分 的 数值 波动 量 让
function [data, XYZ, tri, tri_area] = get_data( WORKING)
% 提取 工作 态 或 者 非 工作 态 下 需要 使 用 的 所 有 数据
data = Data();
lobalopt XYZindex W
XYZ = data.main_node_coordinate; 9% 产生 一 个 对 齐 到 光线 入 射 角度 的 坐标 格式
if WORKING
XYZGindex,?) = opt XYZ; % 主 索 网 调整 到 工作 抛物 面
end
XYZ =-XYZeW;
29

## Logical image page 30

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 30 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A30.jpg -->
<!-- source_image_sha256: 29BE3AEA48BC18430FC83725FDCE75A55184F0B90FC8D0231CA30808512C7FA5 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

% 计算 三 角形 的 面积
triangle = data.triangle:
X = reshape(XYZ(triangle, 1)sizetriangle));
Y = reshape(XY Z(triangle 2).size(triangle)):
%7 = reshape(XY Z(triangle.3) size(triangle)):
triangls area = 0.52abs(X(DAYC2RYCI) + XGAEIHNE) +
PEOR(BIR(ENT
%6 Jik th BTA A AESRESP T SUH RARH =FE
tri ~ triangle(any(index(triangle).2).-y.
tri_area = triangle_area(any(index(triangle).2));
end
function [rec._ratio, xyz, uvw data, XYZ] = me_integral(WORKING)
% 提取 出 当前 有 效 工 作 界 面 《 由 有 效 三 角形 定义 ) 中 竟
% 所 有 xyz 映射 到 uvw 的 射线 关系
% (蒙特 卡 洛 法 ， 顺 便 就 完成 了 积分 )
[data, XYZ. tristri_areal = get_data(WORKING);
area =zeros(size(tr, 1),1);
xyz = cell(size(tri)):
vv = cell(size(iri);
N=10000;
fori = Lisize(tri,1)
X=XYZ(riG2)D;
Y=XYZ(rili32
Z=XYZ(rii).3):
1123 = rand(N.2);
1123(t123(.Dttl23(:2)1.3) = [1, 1] - 123E123G,1)1236.2)°1,);
tl123(send+ 1D) = 1-t123(.1)-t123(:.2 %#ok=AGROW>
[syz_avw_vnatiol = cale tfastttl232XYZ
xyzdi} = xyz_(-isnan(ratio),);
uvw i} ~ uvw_(-isnanratio)..):
area(i) = mean(-isnan(ratio));
end
assert(-any(isnan(area))):
30

## Logical image page 31

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 31 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A31.jpg -->
<!-- source_image_sha256: 6EF12600D751B81B98236A5E6F7690F563E06CFAECF5A76FFE60611E64C54EC7 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

% area = area(-isnan(area));
6tri_area  tri_area(-isnan(area));
rec_ratio = sum(tri_area *area)./(150%150°pi);
if WORKING
disp(" 工 作 接收 比 : "+mat2strtree_ratio.17))
else
disp(" 基 准 接收 比 : "+mat2strtrec_ratio.17))
end
end
function plot_2d_texture( WORKING)
% 画图
% 24， 放 大 界面 纹理 ， 工 作 界面 和 基准 态 都 要 绘制
%
[xyz ~ data, XYZ] = me_integral WORKING);
Hi datatriangle(:[13 1])
plot(reshape(XYZ(tri,1) size(tri))reshape(XYZ(tr, 2)size(tri) K):
hold on;
AZz = vertea(syz{:});
Plol(xyz(:. 1)xy2(:,2) 下 并
axis equal
Mim(-90.30]):
lim([-30.30]),
styleCfontname’, ‘fontsize");
if WORKING
fastprint( 图 片 /prob3. 结 果 . 纹 理 对 比 ( 工 作 态 )7
else
fastprint( 图 片 /prob3. 结 果 . 纹 理 对 比 ( 基 准 态 )7,
end
end
function plot_working_illu_3d(WORKING)
% 画图
%3d, 体现 出 工作 界面 的 反射 光 聚 焦 于 焦点
% 这 张 图 只 在 工作 界面 时 绘制 ， 不 在 基准 态 绘制
31

## Logical image page 32

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 32 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A32.jpg -->
<!-- source_image_sha256: 27A05A87E52254F4CB4B83A4EC4B50675D0AF9DA4C72AD24D1CAD8494A1EF1F1 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

assert(WORKING);
[xyz uvw data, XYZ] = me_integral(WORKING);
xy7z = verteat(syz{:});
uvw = verteat(uvwi:):
xy7 = xyz(1:100:¢nd.);
avw =uvw(Ll100:end );
P=plot3(...
Exyz(CDsYzG.Druvw(G:D]
szG2)syz(2)HuvwC22
[syzC3)syzG3)ruvwG.3)1
eolor = mat2celltrepmattrand(numelp).1)1.3)ones(numelp).D).3)
[p.Color] = color{:}:
holdCon').
X=XYZ(A) Y = XYZ(.2): Z= XYZ(3):
trisurf(data triangle, X.YZ FaceGolor None').
axis(equal);
colormap(‘gray’),
colorbar():
ridCon’;
boxCon'),
style(fontsize' fontname’);
fastprint( 图 片 /prob3. 结 果 . 反 射 光线 聚焦 于 焦点 的 示意 图 》
end
function [xyz, uvw ratio] = cale_t_fast(t123,X.Y,Z)
%
% 寻找 距离 入 射 (xy) 最 近 的 XYZ 坐标 点 ， 并 提取 出 以 该 点 为 顶点 的 所 有 三 角
形
% 傅 次 求解 它们 的 t, 2.3
xyz=t1238 [XYZ:
32

## Logical image page 33

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 33 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A33.jpg -->
<!-- source_image_sha256: AE9C27492287E5369E5E1E8EF94D99A12B940BB17BE9317AC58A5FC95D64FF23 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

% 分 界线 : 上 面 是 命中 点 ， 下 面 是 法 线
a=X()-X@): b= Y()-YQ):
©=X@)X@): d= Y2)YO):
uvw = ([ab; ¢ dN[Z2)-Z(1): ZBYZ2))'s
uvwCeendrD =
uvw_abr= Polar.xyz2abr(-uvw);
uvw_abr(.2) = pi/2-(pi/2-uvw_abr(:2)).*2;
uvw_abrG3) =
uvw = -Polarabr2syz(uvw_abr);
ratio = (-(1-Constant FR_ratio).* Constant.sphere_radius-xyz(:.3))vw(:3):
ratio(ratio < 0) = NaN; % 同 向 达 不 到 馈 源 舱 的 情况 下 pass
dst= xyztratio wuvw;
assertalltabsdst(:.3)+(1-ConstantFR_ratio).*Constantsphersuraidiasj-<-sdrteps)
isnan(ratio)));
ratio(sum(dst(:,1:2)#dst(:,1:2),2) > 0.5.20.5) = NaN; % 反射 馈 源 舱 平 面 时 超过 馈
源 舱 圆 圈 的 情况 下 pass
ratio(sum(xyz(;,1:2).*%y2(:.1:2).2) 三 0.5.*0.5) = NaN: % 入 射 被 馈 源 舱 遮 挡 的 情况
下 pass
ratio(sum(xyz(:.1:2).*xyz(:1:2).2) > 150.4150) = NaN: % 超出 150 口径 圆 面 pass
zsnantmatio)D)= NaN;
uvw = ratio. fuvw;
assert(size(xyz,1) 一 size(wvw.1)),
end
probl.m: 问题 1 的 结果 可 视 化 、 检 验
% 本 文件 原名 probl.m
Gok<*DEFNU>
clear
elear global
close all
[LE angle300] = probl_cale():
elf reset
33

## Logical image page 34

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 34 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A34.jpg -->
<!-- source_image_sha256: 866F9163CE3DA6787DDD9ABE4D4F524A53FE75D60AB9D973C1BFEB82D83F6239 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

inu2d(Lf angle300);
lfreset
plot3d(Lf angle300)
elf reset
eror_plot(Lf angle300)
function error_plot(Lf angle300) % 横向 剖面 高 低 差
angle = linspace(angle300, -angle300+pi. 100);
Lw = Polarpara(Lf angle);
err = Constant sphere_radius-Lw:
plot([-Lw.*cos(angle); -Lw ycos(anglejj [0.err; er “K, ‘LineWidih'2);
holdCon'):.
gridCon’);
plot(-Lw.*cos(angle), err, ‘ok', ‘LineWidih' 2),
Xlim(j-150, 150])
ylim([L-0.6.0.6J%
styleCfontsize'"fontname’),
% fastPiint( 图 片 /probl1. 检 验 .剖面 上 的 高 低 差 ( 径 向 高 度 vs 基准 球面 半径 )7;
end
Function plot3d(Lf, angle300) % 3d 高 低 差
d= Datag'
XYZ = dmain_node_coordinate;
ABR = Polar. xyz2abr(XYZ);
index = ABR(.2) > pi-angle300;
X=XYZCA)Y = XYZ(.2)Z = XYZ(.3),
err= -Polarpara(Lf, ABR(: 2)):
erf-index) = NaN;
trisurf(d.triangle,X. Y,Z,err+ Constant.sphere_radius, FaceColor’interp’);
view(2);
colorbar();
axisCequal);
styleCfontsize!, fontname’),
colormap('gray’).
34

## Logical image page 35

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 35 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A35.jpg -->
<!-- source_image_sha256: 5BABF3C454193A38D108D2CEEB30C6347A84C815DB463AE05E6AC4CDACDCEE51 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

boxCon');
% fastprint( 图 片 /prob1. 结 果 .3D 最 优 挑 物 面 高 低 差 ( 径 向 高 度 )》;
end
function illu2d(Lf angle300) % 横向 剖面 最 优 示意 图

font_opts = frVerticalAlignment, 'middle’, ‘Horizontal Alignment’ ‘center', "FontSize’,
13, Tnterpreter’, latex’};

elfreset’);

hold on

[spher_rad, focal_rad angle] = Constant.get_rad_angle();

P_S =inup_S:

PP= IO -focal_rad]:

_Q =[0-focal_rad-0.5Lf];

P_T=[0-focal_rad-Lf];

holdCon'):.

% 基准 圆 弧

plot(-spher radscos(angle)-spher radsin(angle) ', LineWidih', 2);

% 焦 面 圆 弧

plot(-focal_rad*cos(angle),-focal_rad*sin(angle), K', LineWiddh', 2);

% 标记 定点

plot(p_S(1), p_S(2).*K., MarkerSize, 14LineWidth, 2);

Plot(p.P(1), p_P2)"K, "MarkerSize', 22, "LineWidth', 2);

Plot(p_Q(1), p_ Q(2)."K' MarkerSize', 22, "LineWidth', 2).

plot(p.T(1), p_T(2),"K. MarkerSize’, 22, LineWidtl', 2);

Plot(0.0,:K, MarkerSize’, 22, LineWidth, 2);

text(p_S(1)+20, p_S(2), "boldmathSSS. font_opts{:});

text(p_P(1)+15. p_P(2)+18, "boldmathSPS' font_opts{:});

fext(p_Q(1)+15., p_Q(2)*18, "boldmath$SQS. font_opts{:}):

text(p_T(1)-18, p_T(2)+18, "boldmathSTS, font_opts{:}):

1€x1(0+20, 0, "boldmathSCS, font_opts{:}):

% SCPQT 中 轩 线

plot(fp SG) P_TCDT [p_S(2). p_T)}K:, LineWiddh', 2);

% 淮 线

Plot(p_T(1)+[-300 300], p_T(2)+[0 0], "K’ "LineWidth', 2);

plot(p_T(1)+[0 30 30], p_T(2)+[30 30 0], "K’, LineWidth, 2 %  2

% 计算 抛物 线

Lw = Polarpara(Lf angle);

1.300 = Polarpara(L; angle300);

35

## Logical image page 36

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 36 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A36.jpg -->
<!-- source_image_sha256: 4028F38E1AEEBEFEDA49C3286E00D676B5432B08BF8C1ADAE6137FED383DEDF4 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

P_x= [-L300.*cos(angle300) -L300.*sinangle300)
% 抛物 线
plot(-Lw.*cos(angle), -Lw ssintangle) -k "LineWidth', 2);
plot(p_x(D),P_x(2) "KMarkerSize, 22); % 300 口径 点
plotfp_PCDP_x(CDL [p_P(2) p_x(2)]. sk，LineWidth, 2); % 焦点 连 线
plot(fp_x(D p_x(1)]. [p_T(2) p_x(2)]. sk，LineWidth, 2); % 准 线 连 线
text(p_x(1), p_T(2)-20, vboldmathsx=30012S. font_opts{:});
% 格式
axis(equal);
set(gea, Visible', off);
% ylim([-300, 200]);
style(fontsize, fontname’);
% fastprint( 图 片 /prob1. 结 果 .2D 剖面 最 优 抛物 线 四
end
prob2.m: 问题 2 的 结果 可 视 化 、 检 验
% 本 文件 原名 prob2.m
le
ef
clear
mg(default);
close all
clear(global);
data = Data();
[fval, opt_X, opt_XYZ, opt_Lz, opt_ABR, index, W, Winv .
edge, edge_distSQ, motor_hi, motor unit motor_distSQ] = prob2_calc():
close all
XIsx_output(opt_XYZ opt_Lz, index, Winv)
disp(" 问 题 2 最 小 误差 平方 和 : "+fval);
retum
elf reset
ermplot_3d(data, opt XYZ, opt_ABR, index):
elf reset
plot_3d_lzldata opt XYZ, opt_Lz, index):
36

## Logical image page 37

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 37 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A37.jpg -->
<!-- source_image_sha256: F19A5C593899F1D89A05C2A79F8EE159CBC9698267510B76ABC07379FF4B0A5C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

elf reset
plot_2d_main_node_dist(opt XYZ. edge edge_distSQ):
elf reset
plot_2d.fiterr(opt_ABR);
function xlsx_output(opt XYZ, opt_Lz, index Winv)
if existCresult xls¥, file')
delete(result xlsx');
end
copyfileCHcHE/4. TEMAHI 93:5 15 f.xlsx, result xlsx);
% 理想 抛物 面 顶点 坐标
XYZ = Polarabr2xyz([0 pi/2 Polar para(Constant Lf, pi2)]):
XYZ =XYZ*Winv;
1= able(XYZ(1), XYZ(2), XYZ(3)):
disp(" 理 想 抛物 面 项 点 坐标 ")
disp(head(t1));
writetable(t1, ‘resultxls’, ‘Sheet'; * 32 2 fft # [ T1 4% % #7', ‘Range!, 'A2C2,
"WriteVariablsNames' false);
46 调整 局 主 索 节 点 编号 及 其 坐标
data s FEadtable(' 数 据 /1， 主 索 节 点 坐标 和 编号 .csv;
12= table(data.x___(index), opt XYZ(:1), opt XYZ(:2), opt XYZ(.3):
disp(" 调 整 后 主 索 节点 编号 及 坐标 "
disp(head(12));
writetable(t2, 'result xlsx、'Sheet，' 调 整 后 主 过 节点 编号 及 举 标 Range，[A2:D'
mum2str(height(12)+1)), "WriteVariableNames' false);
% 促 动 器 顶端 伸缩 量
13~ table(data.x___(index), opt_1.2):
disp(" 促 动 器 顶端 伸缩 量 "):
disp(head(13));
writetablet3，'esultxlsx，'Sheet:“， 促 动 器 顶端 伸缩 量 ，'Range，[A2:B'
mum2str(height(t3)+1D) WriteVariableNames' false):
xlsx_check():
end
function xlsx_check()
37

## Logical image page 38

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 38 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A38.jpg -->
<!-- source_image_sha256: 900D94C97AEC5D3F372ECDD91D4E73B9D68424E67072DE2E1EF3E18DF32982AB -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

11= readtable(resultxlsX,Sheet' 理 想 报 物 面 顶 点 坐标 ?
12= readtable(result xlsX,Sheet' 调 整 后 主 索 节 点 编号 及 坐标
昌 =readtable(resultxlsX'Sheet' 促 动 器 顶端 伸缩 量 )
[W.~] ~ Polarcompose_rotate(Constantalpha Constant beta):
% 抛物 面 项 端 W 旋转 后 的 取 值 Lw 要 与 focal_rad+LD2 一 样
ABR = Polar.xyz2abr(t1 {1,13}*W');
emr= ABRG)(1-Constant FR._ratio)*Constant.sphere_radius +Constant L{12);
disp(" 检 查 ; 抛物 面 项 端 旋转 后 是 否 是 focal_rad+LD2 AUILECHIBRR 2): "rerm);
assert(abs(em) < eps);
% 重新 构建 index
Taw_code = readtable(' 数 据 /1. 主 索 节点 坐标 和 编号 .csv)
raw_code -raw codex
index_code = string(2x__);
index = cellfun(@(s)any(s 一 index_code) raw_code):
assert(all(string(raw_code(index)) 一 index_code));
disp( 构 建 index 成 功 小
%0.6
assert(all(3(:2}<0.6));
assert@l(3{:.2}>-0.6)):
disp(Lz 没有 超过 寸 66: 成 功 和
%007
data ~ Data();
edge = data.edge(all(index(data.edge) 2).:): % 过 滤 节 点 之 间 的 连 边
index2(index) = lsum(index): % 构建 过 滤 之 后 的 新 的 节点 下 标 顺 序
edge = index2(edge): 9% 使 用 新 的 节点 下 标 对 连 边 节点 序号 重 定向
assert(all(all(edge))): % 连 边 节点 序号 不 能 有 空 泡
raw_XYZ = datamain node_coordinate(indes..);
opLXYZ =02:243;
raw_edist = raw_XYZ(edge(:.1).}raw XYZ(edge(:2).:
raw_edist = sqri(sum(raw_edist *raw_edist.2)):
opt_edist = opt. XYZ(edge(-1).)-0pt XYZ(edge(:2).:
opt_edist = sqri(sum(opt._edist.*opt_edist.2));
ratio  (opt_edist raw _edist)*100-100;
assert(all(ratio<0.07));
assert(allratio-0.07)):
disp( 节 点 之 间 的 距离 变化 率 没有 超过 土 0.07%6: 成 功 洲
% motor 距离 (下 拉 索 )
38

## Logical image page 39

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 39 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A39.jpg -->
<!-- source_image_sha256: F7E11506B733190F4E245A481AEF99E52B49F75D54760EFD69C8A2F43E9D9433 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

motor unit = datamotor higher base(index.:)datamotor lowertindex
motor_ unit = motor_unit./sqri(sum(motor_unit.*motor_unit.2));
assert(all(abs(sum(motor_unit *motor_unit.2)-1) < sqrt(eps))):
motor top = data.motor_higher_base(index.:)t3{:,2}. *motor_unit;
opt_pdist = opt XYZ-motor top:
opt_pdist = sqrt(sum(opt_pdist.*opt_pdist 2)):
raw_pdist = data.main_node_coordinate(indes,’)-data.motor_higher_base(index.);
raw_pdist = sqri(sum(raw_pdist *raw_pdist.2)):
assert(max(abs(raw_pdist-opt_pdist)) < sqri(eps)):
disp(C 下 拉 索 距离 不 变 : 成 功 );
% 最 优 贴 合 程度
opL_ABR = Polar.xyz2abr(opt XYZ*W'),
err= opLABR(:3)-Polarpara(ConstantLf opt_ABR(.2)):
assert(max(abs(ern) < le-S
disp( 贴 合 程度 至 多 le-5: 成 功 入
end
function plot_ 2d_fiterr(opt_ ABR) %#ok<*DEFNU>
Lw = Polar.para(Constant.L, opt_ABR(.2));
err = opt_ABRG3)-Iaw;
bar(sort(err), K):
ridCon’;
styleCfontsize’, fontname’),
ticks([xticks numel(ern)]);
fastprint( 图 片 /prob2. 检 验 . 主 网 节点 与 理想 抛物 面 之 间 的 球面 径 向 误差 四
end
function plot_2d_main_node_dist(opt_ XYZ, edge, edge_distSQ)
errdist = opt_XYZ(edge(:,1).)-0pt XYZ(edge(:2).):
edist = 100* (sqri(sum(errdist *errdist 2)). sqri(edge_distsQ)-1);
bar(sort(edis), K);
gridCon);
styleCfontsize! fontname’),
ticks([xticks numel(edist)]);
fastprint( 图 片 /prob2. 检 验 . 主 网 节点 之 间距 离 的 变化 率 (百分比 )7;
end
39

## Logical image page 40

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 40 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A40.jpg -->
<!-- source_image_sha256: 8080589F5743DD91B59EE7CA720CA7B4CC7E3263194AF7F78C1731D41D6B89CB -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

function plot_ 3d_lz(data_ opt_ XYZ, opt_Lz,index) % 三 维 促 动 器 提升 量 (FlaD)
raw_XYZ = data.main_node_coordinate;
raw_XYZ(index.:) = opt XYZ:
X = raw_XYZ(:1); Y = raw_XYZ(:2); Z = raw_XYZ(.3);
Lz = NaN(size(index):
Lzindex) = opt_Lz;
trisurf(data.triangle, X,Y,Z, 12);
colorbar();
view(2),
axisCequal);
style(fontsize’, fontname’);
colormap(‘gray’).
ee caxis();
w(2)=06:
caxis(ee);
boxCon');
fastprint( 图 片 /prob2. 结 果 .3D 促 动 器 提升 量 叶
end
function errplot_3d(data, opt XYZ, opt_ABR, index) % 三 维 拟 合 误差 (interp)
raw_XYZ = datamain_node_coordinate;
raw XYZ(index,) = opt XYZ:
Xo= raw_XYZ(,1); Y = raw_XYZ(:2); Z = raw_XYZ(.3);
err= NaN(size(index)).
er(index) = abs(Polar para(Constant L, opt_ABR(:2)) - opt_ABR(3)):
trisurf{data.triangle, X,Y,Z, er "FaceColor’ interp');
colorbar():
view(2),
axis(equal);
styleCfontsize! fontname’),
colommap('gray’).
boxCon');
fastprint(' 图 片 /prob2. 结 果 .3D 理想 曲面 拟 合 误差 7)
end
10. 1. 2 常数 定义 与 数据 处 理
40

## Logical image page 41

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 41 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A41.jpg -->
<!-- source_image_sha256: 7A012887492CED8829E9C3CFD898E1DE607C43591C5F552B8F78DF3792112E2E -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

Constant. m: 程序 用 到 的 所 有 常量 数值 定义
% 本 文件 原名 Constantm
classdef Constant
Properties(Constant)
FR_ratio = 0.466: % 焦 径 比
sphere_radius = 300.4; % 基准 态 球面 半径 ， 单 位 是 米
sphere_half_caliber = 500/2; % 基准 态 球面 的 口径 的 一 半
paraboloid_half caliber = 300/2; % 工作 态 球面 的 口径 的 一 半
L£=280.85417567168855; % 第 一 问 算出 的 最 优 焦距 ， 用 作 求解 完 的 粒 查
alpha = deg2rad(36.795): 96 第 二 问 平面 角
beta = deg2rad(78.169): % 第 二 问 仰角
end
‘methods(Static)
function [spher_rad. focal rad angle] = get_rad_angle0)
spher_rad ~ Constant sphere_radius;
spher_cli = Constant sphere_half caliber:
focal rad = (1-Constant FR_ratio) * spher rad:
angle = pi/2-asin(spher_cli/spher.rad), % 使 用 半径 和 半 口 径 计算 出 依 角 ，
依 角 变 成 仰角
angle = linspace(angle. pi-angle. 100):
end
end
end
Data.m: 将 题目 附件 123 映射 到 程序 内 数组
% 本 文件 原名 Datam
classdef Data
properties
main_node_code % 主 索 节点 的 编号 ，strings 转 序数
a

## Logical image page 42

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 42 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A42.jpg -->
<!-- source_image_sha256: 1764730645CDB98CA462B8E9E2A4E32AEE49F1F7EA1941E133424E3F843AF9C8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

main_node_coordinate % 主 索 节点 的 坐标 ，XYZ
motor lower % 促 动 器 下 端点 的 坐标 ，XYZ
motor_higher_ base % 促 动 器 上 端点 的 坐标 ，XYZ (基准 态 )
triangle 9% 三 角形 反射 面板 的 顶点 序号 ，string 转 序数
edge % 不 重复 的 连 边 项 点 序号 ， 按 照 左 小 右 大 表示 ， 格 式 是 序数
end
methods
function d = Data
main_node = readtable( 数据 /1. 主 索 节点 坐标 和 编号 .csv)
dmain_node_code = string(main_node{:,1});
dmain_node_coordinate = main_nodef:,2:end};
motor = readtable( 数据 /2， 促 动 器 上 下 端点 坐标 和 编号 .csV);
assert(all(d.main_node_code == string(motor{:,1}))):
dmotor lower = motor{: 2:4};
dmotor_higher_base = motor{: S:end}:
triangle = readtable( 数据 B. 反 射 面板 的 顶点 编号 .csv);
dtriangle = string(triangle{:.1});
d.check)
d=d.convert_node_id();
dedge = d.get_edges();
end
function ¢ = get_edges(d)
tri = d triangle;
= [uiCL2):tri(:2:3jtriG:[L3]):
e(e1)7e(2),0) = e(e(1)7e(2)(2,11
©= unique(e,Tows):
assert(size(e.1) == 6525);
assert(-any(e(:1) == €.2):
end
function check(d)
asser(isstring(d.main_node_code));
42

## Logical image page 43

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 43 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A43.jpg -->
<!-- source_image_sha256: CBEE93569C9D411080C6B24155F1605F31A72838D518515CF2AEDBD81BEEADE8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

assert(numel(d.main_node_code) = 2226);
assert(size(d.main_node_coordinate,1) == 2226);
assert(size(dmain_node_coordinate2) = 3);
assert(ismatrix(d motor_lower));
assert(ismatrix(d motor_higher_base));
assert(size(dmotor_Tower,1) 一 2226);
assert(size(d.motor_lower.2) 一 3);
assert(size(dmotor_higher base,1) 一 2226);
assert(size(d.motor_higher_base2) = 3);
asser(isstring(d triangle))
assert(size(d.triangle,1) = 4300);
assert(size(d triangle.2) 一 3)
end
function d = convert_node_id(d)
% 先 给 主 节点 排序 ,确定 一 企 顺序 查 技 表 abe(i)， 并且 有 index(D) 一 [ 原
位 ]
[abe index] = sort(d.main_node_code):
% 再 给 triangle 拌 序 ， 确 定 一 个 顺序 表 xyz0)， 并 且 有 index20) 一 [tri
原 位 ]
[RSz index2] = sort(d.triangle(:)):
i-n
indexed = zeros(size(xy7));
for i = lnumeltabe)
while abe(i) == xyz0)
indexed(j) = index(i):
jjrl
ifj > numel(xyz)
break
end
end
nd
indexed(index2) = indexed;
indexed = reshape(indexed, [J. 3);
assert(all(all(d.main_node_code(indexed) = dtriangle)))
43

## Logical image page 44

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 44 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A44.jpg -->
<!-- source_image_sha256: BD72FA9B0D6664FD115ECC3D57E86B8399AB4E0563C84AD61E679A7F07C9C455 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

dmain node code = I:numel(d.main_node_code);
dmain node code = d.main_node_code(:);
dtriangle =indexed:
end
function length = get_pull_length(d)
main = d.main_node_coordinate;
higher = d.motor_higher_base;
length = sqrt(((main-higher). *(main-higher)) * [11 1]);
end
end
end
Polar.m: 极 坐标 与 直角 坐标 相互 转换 ， 抛 物 面 径 向 距离
% 本 文件 原名 Polarm
classdef Polar
‘methods(Static)
function [L, dL._dL, dI._dangle] = para(LE angle)
% BEAHR T, BEMPRMIE, £45EH omega(angle) F
9 输出 入 应 的 距离 坐标 工
cos_angle = cos(angle); % diff(cos) 一 -sin
sin_angle = sin(angle); % diff(sin) 一 cos
cos2_angle = cos_angle.*cos_angle;
RF =(1-Constant FR_ratio)*Constant.sphere_radius;
index = cos angle == 0 | abs(angle - pi/2) < eps:
delta = LEXLE + 2#REXLE¥cos2_angle;
L= (-L:*sin_angle-+sqri(delta)). /cos2_angle;
L(index) = (L£/2+RF) /sin_angle(index):
ddelta_dLf =2.*Lf + 2.*RE.*cos2_angle;
dL_dLE = -sin_angle./cos2_angle;
adL_dLF= dL_dLF+1/cos2_angle *0.5./sqri(delta)* ddelta_dLE;
44

## Logical image page 45

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 45 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A45.jpg -->
<!-- source_image_sha256: FD74AA095698E9B093ECB17A337BE0006DCFECF35B6F4043108F9CB0EBA26903 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

adL_dLfindes) = 1/2.*sin_angle(index)):
ddelta_dangle = 2.*RF*LF*2.*cos_angle ysin_angler
dL_dangle = -Lf/cos2_angle.*cos_angle - L/cos2_angle.*2.¥cos_angle.*-
sin_angle;
dL dangle = dL_dangle+l.eos2_angle.*0.5.sqrttdelta) ,rddelta_dangle:
dL_dangle(index) = -L(index). sin_angle(index) *cos_angle(index);
end
function [abr dalpha, dbeta, dr] = xyz2abr(XYZ)
% 和 卡尔 坐标 转 极 坐标
% 给 出
% abr  : [alphabetar]
% dalpha dalpha}/d{[X Y Z]}
%  dbeta: d{betab/d{[X Y Z]}
% dr dmAXY Z))
X =XYZ(: 1);
¥ =XYZ(:2);
Z=XYZG3%
nomm2 sq = X.AX+YAY;
iom3 -二 三 norm2 sq+Z.47;
Tomm2 = sqrtnorm2_sq);
norm3 = sqri(norm3_sq);
nom3;
beta = asin(-Z_D;
alpha = acos(-X./norm2);
alpha(Y>=0) = 2*pi-alpha(¥>=0);
alpha(-nom2) = 0;
abr = [alpha, beta, 下
ifnargout =- 1
retum
end
ZEROS = zeros(size(Z)).
dnorm2_sq = 2.*[X Y ZEROS];
45

## Logical image page 46

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 46 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A46.jpg -->
<!-- source_image_sha256: ACE823FAA1722595E4E62BA05DDE65B25D301DF72559BE3A8F280E0CAA889D35 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

dnorm3_sq =2*[X Y Z];
dnorm2 = 0.5.*dnorm2 sqnorm2;
dnorm3 = 0.5. *dnorm3_sq./norm3;
dr = dnorm3;
dbeta = r./norm2.#([ZEROS ZEROS -1./r] + (Z./r). dr./r)).
dalpha  =  -absmorm2/Y).*(|-L/norm2  ZEROS ZEROS]  +
(X/norm2).* (dnorm2. /norm2));
dalpha(Y>=0, ) = dalpha(Y>=0, 站
dalpha(-nom2, = 0;
end
function XYZ = abr2xyz(abr)
%
% 极 坐标 格式 转 笛 卡尔 坐标
alpha = abr(.1);
beta =abr(:2);
ab
也 -resinbeta:
Treeos(beta):
文本 只 costalpha;
¥ = -*sin(alpha);
XYZ=[X,Y, Z);
end
function [W Winy] = compose_rotate(alpha, beta)
% 组 合 旋转 〈3d 旋转 矩阵 )
% 先 道 向 旋转 以 清除 alpha 角 (xOy 平面 上 的 )
% 再 正 向 旋转 以 将 beta 补偿 到 pi2
wy=[
cos(alpha) sin(alpha) 0
~sin(alpha) cos(alpha) 0
0 01
于
WwW _inv=[
cos(alpha) -sin(alpha) 0
46

## Logical image page 47

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 47 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A47.jpg -->
<!-- source_image_sha256: 91F86AB162C24FD3627A187D430A35BFB74FC323DA39BCD06F9BEFC196D8D332 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

sin(alpha) cos(alpha) 0
0 01
上
wsz=[
cos(pil2-beta) 0 -sin(pi/2-beta)
0 1 0
Sin(pi/2-beta) 0  cos(pi/2-beta)
下
wxz_inv=[
os(pil2-beta) 0sin(pil2-beta)
0 1 0
-sin(pil2-beta) 0 cos(pi/2-beta)
上
WwWxzeWxy:
Winv = Wxy_inveWxz_ inv:
assert(all(all(abs(W* Winv-eye(3)) < epsO)):
end
end
end
10.1. 3 画图 程序
Tum* 与 示意 图 有 关 的 常量 定义
% 本 文件 原名 ilum
classdef illu
properties(Constant)
P_S = [0 150]; % 被 观测 点 的 方位
end
end
ilu1. m* 剖面 直角 坐标 示意 图
% 本 文件 原名 iulm
font_opts = {'Vertical Alignment’, 'middle’, Horizontal Alignment, ‘center’, "FontSize’, 10,
Interpreter’, atex 3
close all
hold on
47

## Logical image page 48

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 48 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A48.jpg -->
<!-- source_image_sha256: 52BAF8DBE168397A4AB578BC53819E37B311FCE315F7385EC9A5CCB67DBF4B6D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

[spher_rad, focal_rad angle] = Constant.get_rad_angle();

pspher  = [-spher_rad*cos(angle( 1)) -spher_rad*sin(angle( 1))]:

p_spher_end = [-spher_rad*cos(angle(end)), -spher_rad*sin(angle(end))J;

p_focal [-focal_rad*cos(angle(  1)), -focal_rad*sin(angle(  1));

p_focal_end = [-focal_rad* cos(angle(end)), -focal_rad*sinangle(end))}:

v_sph = [cos(pi/2 tangle(1)) sinpi/2 angle(1))]:

p.S=illups:

p_P= [0-focal_rad];

pP_Q= [0-spher rad+20]:

PT=[0p PC)+2*(p_QC)-P PC

hold(on');

%6 基准 贺 弧

draw_2d_are focal_ and_basespher rad, focal_rad, angle);

%6 焦 径 比 和 R300

standard_distance_tag(angle, p_spher, P_spher end pcal p_focal end, v_sph,
font_opts);

% 标记 定点

plot(p_S(1), p_S);*K, MarkerSize’, 14, "LineWidih', 2),

plot(p_P(1); p_P(2)K' "MarkerSize', 22, LineWidth', 2);

plot(p_Q(1). p_Q(R)"K' 'MarkerSize', 22, 'LineWidth' 2);

plot(p_T(1), p_T(2),"K, MarkerSize’, 22, "LineWidl, 2);

Plot(0,0;K, MarkerSize', 2, "LineWidih, 2),

text(p_S(1)+10, p_S(2)+30, "EAF, font_opis{ Liend-2});

text(p_S(1)+20, p_S(2), "boldmathSSS, font_opts{:}):

text(p_P(1)+15. p_P(2)+15. "boldmathSPS, font_opisf:}):

textp_QCD+15, p_Q(2)+15. "boldmathSQS. font opts{:}):

text(p_T(1)+15, p_T(2)+10, "boldmathSTS, font_opis{:});

1ext(0+15, 0, "boldmathSCS, font_opts{:});

2% SCPQT 中 轴线

plot([p_S(1), P_TCOD [p_S(2). p_T)}~K', LineWidth', 2);

% 文字 tag

text(p_spher_end(1)-40, p_spher_end(2)-70, "基准 球面

48

## Logical image page 49

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 49 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A49.jpg -->
<!-- source_image_sha256: 0FF090010FA6E013DEDE655266B48B11E2B36B7E5903B4273B48B1B8CD375132 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

Rotation' rad2deg(angle(end-11)-pi/2), font_opts{ 1:end-2}):
text(p_focal_end(1), p_focal_end(2)-25, "$47HT...

"Rotation' rad2deg(angle(end-4)-pi/2), font_opts{1:end-23);
1ex(-160, p_T(2)+15, “WMHIHER, font_opts{1:end-23);

% PQ 长 度

plot(p_P(1)+[-350 0]. p_P(2)+{0 0]. “K. "LineWidih, 2):
plot(p_Q(1)#{-350 0], p_Q(2)+[0 0]. "K’, 'LineWidih', 2);
myquiver(8,[p_P(1) p_Q()]-325. [p_P(2)p_Q(2)}"K. LineWidih', 2)
text(p_P(1)p_Q(1))/2-300, (p_P(2)*p_Q(2))'2, "boldmath§ PQI-L._£25.,

"Rotation' 90, font_opts{:});

% QT 长 度 以 及 垂直 的 准 线

plot(p_T(1)+[-350 300]. p_T(2)+[0 0], sk，LineWidth' 2);
‘myquiver(,[p_Q(1) p_T(1}-325, [p_Q(2) p_T)). "K..LineWidih', 2);
text(p_Q(D+p_TUD)2-300, (p_Q(2)+p_T(2))2, "boldmathS|QR“L {25...

"Rotation' 90, font_opts{:});
plot(p_T(1)+[0 30 30]. p_T(2)*[3030 0]. "K' LineWiduh', 2) % 垂 足
% 计算 揣 物 线 ，
tp 了 CrpQO7
TI Polarpara(Lf angle);
xangle = 他 ero(@(angls)abs(Polarpara(Lf angle)*cos(angle))-150, [pil2, angle(end)));
XL= Polarpara(LE xangle);

P_x = [-xL*cos(xangle) -xL *sin(xangle)]:
plot(-L*cos(angle), -L.*sin(angle), -K' "LineWiddh, 2);
plot(p_x(1). p_x(2). "K., MarkerSize', 22);

plot([p_P(1) p_x(D}, [p_P(2) p_x(2)}, "K, LineWidth', 2);
plot((p_x(1) p_x(D]. [p_T@) p_X(2)]. "K, "LineWidih', 2);
text(p_spher_end(1)-50, p._spher_end(2)-10, 抛物 面 …

Rotation' rad2deg(angle(end-14)-pi/2), font_opts{1:end-2});
title("boldmathSy=\frac{x"2}{2L. f}-frac{L._f}{2}-(1-0.46)RS’ Tnterpreter’, Tatex');
text(p_x(1), p_T(2)-15, "boldmath$x-300/25, font_opts{:}):

49

## Logical image page 50

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 50 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A50.jpg -->
<!-- source_image_sha256: 0E6F50E55892DDC8A0F9DA115B6F8DFCD267A2C9D098D75A07C9B3C2256463A3 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

axis(equal);
% ylim([-525. 200])
set(gea, Visible', of
styleCfontname’);
fastprint( 图 片 /probl1. 示 意图 1. 准 线 等 辅助 线 小
function draw_2d_arc_focal and_base(spher_rad, focal_rad, angle)
% 基准 圆 弧
plot(-spherrad*cos(angle).-spher_rad*sinangle), LineWidth, 2);
% HEER
plot(-focal_rad*cos(angle).-focal_rad*sin(angle), K', "LineWiddh', 2);
end
function standard_distance_tag(angle, p_spher, p_spher_end, p_focal, ~, v_sph, font_opts)
% 焦 径 比
plot(p_spher(1)+[0 50*v_sph(1)]. p_spher(2)+[0 50t_sph(2)],":K’, LineWidth', 2);
plot(p_focal(1)+[0 50%v_sph(1)]. p_focal(2)+[0 S0%v_sph(2)}. “K. "LineWidti, 2):
‘myquiver(8.[p_spher(1) p_focal(1)]+25%V_sph(1). [p_spher(2)
p_focal()]+25%_sph(2), "K’ 'LineWidt', 2).
text(
(p_spher(1)+p_focal(1)+80*v_sph(1))2 ..
(p_spher(2)#p_focal(2)+80*V_sph(2))2...
"boldmathSF-0.466RS, font_opts{:}, Rotation’, rad2deg(angle(1)));
% 基准 半径
plottp_spher(D+100*[O v_sphCDh p_spher(2)+100°[0v_sph(2)]."K" LineWidth, 2);
plot 0+100%(0v_sph(D)}, 0+100%[0 v_sph(2)],"K’, LineWiddh',
2
myquiver(15.[p_spher(D) 0]+75*Y_sph(1)， [p_spher(2) 0]+75*V sph(2). "K.
LineWidth' 2);
text(
(p_spher(D)+0+180*V_sph(1D)2、
(p_spher(2)+0+180*V_sph(2))2.
“boldmathSR-300.4\mathrm {m}S', font_opts{(:}. Rotation' rad2deg(angle(1)));
%D=500m
50

## Logical image page 51

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 51 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A51.jpg -->
<!-- source_image_sha256: 5CED248BCA34DC97D1E1716CCEA98A61D72138F9904E7781C764A0A981BF4A04 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

myquiver(20,[-250 250], [-450 -4501:K', LineWidth', 2);
plot([-250 p_spher(1)], [-460 p_spher_end(2)},"K', LineWiddh', 2);
plot([ 250 p_spher_end(1)]. [-460 p_spher_end(2)},"K', 'LineWidih', 2);
1ext(0, ~440, "boldmathSD=500 mathrm {m}S, font_optsf:});

end

function myquiver(r.x.y; varargin)
rad = atan2(y(1)-y(2), X(1)XQ)):
rad = [rad+deg2rad(30) rad-deg2rad 30)J;
plot(x.yvarargin{:});
L = sqrt((x(DX@)HX@)HD5@)F F(Dy@)e:
PIO(S(1)-[0.L}*cos(rad(1)).y(1)-[0.L}#sin(rad(1)).varargin{:}):
PIO(S(1)-[0.L]*cos(rad(2)).y(1)-[0.L]#sin(rad(2)).varargin{:}):
PIOI(XQ)*[0.L]*cos(rad(1)).y(2)[O.LI*sinrad(1)) vararging:):
PIO(X(2)+{0.L]cos(rad(2)).y(2) HO.LI*sin(rad(2)) varargin{:});

end

illuz.m: 剖面 极 坐标 示意 图

% 本 文件 原名 ilu2m

% 剖面 示意 图

font_opts = {"Vertical Alignment’, ‘middle’, Horizontal Alignment, ‘center’, 'FontSize', 18,

Interpreter’, latex'}:

clase all

[spher_rad, focal rad, angle] = Constant.get_rad_angle();

PS=Ipi2inup_ SC 站

P_P= [pil2 focal rad];

P_Q= [-pi/2 spher rad-20]:

P_T= [pi2 P_P(C2)+2*(P_Q(C2)-p_PC2)

% 基准 圆 弧

polarplotlangle+piangle *0+spher rad, LineWidth', 2);

holdcony

% MREEN

polarplot(angle-+pi.angle *0+focal rad, 'K', ‘LineWidtl, 2);

% 标记 定点

polarplot(p_S(1), p_S(2),*K, MarkerSize’, 14, ‘LineWidth', 2);

polarplot(p_P(1), p_P(2)."K 'MarkerSize’, 22, 'LineWidth' 2);

polarplot(p_Q(1), p_Q(2),K, MarkerSize', 22, LineWidth', 2);

polarplot(p_T(1), p_T(2),'K, MarkerSize’, 22, ‘LineWidth', 2);

51

## Logical image page 52

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 52 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A52.jpg -->
<!-- source_image_sha256: B154D736FFC953E03B803DC5DF28BB31A0F59028485B241C4BE02957A41E3515 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

polarplot(0.0,'K', MarkerSize’, 22, LineWidth, 2);

text(p_S(110.20, p_S(2), "boldmathSSs, font_opts{:}):

text(p_P(1)+0.12, p_P(2)-18, "boldmathSPS' font_opts{:});

text(p_Q(1)+0.08, p_Q(2)-23, "boldmath$QS, font_opts{:});

text(p_T(1)+0.06, p_T(2)-18. "boldmathSTS. font_opts{:}):

1ex1(0.15, -30, "boldmathSCS’, font_opts{:}):

% SCPQT 中 轴线

polarplot([p_S(1), p_T(D], [p_S(2). p_T(2)}~~K: "LineWidth', 2);

% 计算 抛物 线

LE=2%(p_Q2)-p_P2)):

工 = Polarpara(Lf angle):

xangle =。 fzero(@(anglejabs(Polarpara(LE anglej*costangle)-150， [pi2*1.01.
angle(end)]):

XL = Polarpara(LE xangle);

theta = linspace(-xangle, xangle-pi, 150);

r= Polarpara(LL, thetapi):

1(2:2:end) = spher rad;

polarplot(reshape(theta,2.[]). reshape(s2.[]), -K. linewidih', 2, ‘color’, [0.7, 0.7, 0.7));

polarplot([0 0], [0 p_T(2)],"’, "inewidth, 2);

‘polarplot(linspace(0.-xangle pi. 100), repmat(60.1,100), *K', Tinewidth', 2);

text((-xangle*pi) 2:0.05, 90, "boldmath$ omegaS', font_opts{:}):

polarplot(angle +pi, L, - K', ‘LineWidth', 2):

polarplot(xangle +pi, xL "K', "MarkerSize’, 22);

polarplot(-xangle, xL,"K, MarkerSize’, 22);

polarplot(-[xangle xangle], [-p_S(2) spher_rad], "K’, linewidd, 2);

polarplot([xangle xangle]+pi [-p_S(2) spher_rad], "&', Tinewidth', 2);

% polarplot(-p_x(1), p_x(2),"K, "MarkerSize', 22);

set(gea RAxisLocation' 0);

Him([0, p_T)]:

% 极 坐标

styleCfontksize fontname’),

fastprint(, 图 片 /prob1. 示 意图 2 极 坐标 下 的 omega 角 与 球面 径 向 误差 平方 积分 和
style.m: 为 输出 图 片 统一 文字 大 小 和 字体

% 本 文件 原名 stylem

function style(varargin)

52

## Logical image page 53

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 53 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A53.jpg -->
<!-- source_image_sha256: 8F155EB72F7898D942715A5285D5FB2EDD5C28EC31B8D94349EE416DC4B2592D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

forv= varargin
switch lower(char(v))
case fontsize
set(gea), fontsize’, 22);
case fontmame
set(gea(), fontname’, imes new roman');
end
end
end
fastprint.m: 简易 绘图 输出
% 本 文件 原名 fastprintm
fanetionr = fastprintfilename)
assert(isequal(elasstfilenamej'ehar) 。 |。 (isequal(class(filenamej'stringj 二 &&
isscalartfilename))
ifisstring(filename)
filename = char(filename);
end
if numel(filename) >~ 4 && isequal(filename(end-3:end), png)
filename ~filename(1:end-4);
end
filename = [filename,’ "datestr(now(), yyyy.mm.dd. HH_MM),"png’}:
print(-dpng. 300" ilename);
dispfilename);
= @Qsystem(['open filename]);
end
10.2 附件 resultxlsx 数据
Te xa vaa xz x2  Ya  zz x3 xs vs _z3
M omw wom owe © @Gl 030 Zme OB 2T 7
B ems  ew 3018 ED mzs nom -235 DO Wes mTs mes
|
pl -oo :1041 -30030 2 1BXS 。 209 WOT 86。 -和 9963 -19174 -294394
日 (osa| an \owam A ei faie Ta e7 ssis 7e0s -天 三
人 -62  eW -0029 Ad 一 600” 4207 -207175 El sis 3974 2610
两 ”-oom tws om AE WE 205 -0 6 -9 15602 -2626
@ Lm eme -向 o4 ell。 30365 4 -23056009 ED -4320327198 205913
os B2 MXT IT mee @1 A0IT 6S 500
7 es aWes WI 区 120 190 207154 AIG S6H 500  -25E2
53

## Logical image page 54

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 54 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A54.jpg -->
<!-- source_image_sha256: 3B5A49D4DC35F8301AA036D5B5A8D106610B340C06C2CBD9E462063622AF2057 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

站
06
下
eol -845 memo Cl2 sowe 22-26719 MA26 600 5900 29012771
外 0 4 000 on mes 人 -2 820 8
多 5 Cl 11。 we mwms 20 50302500。 -2205
站
估 ml 2 0 23690020
机 0 00
本 ”20m 950 212 po -96 3 207706 625 196， 24018 204312
让
G omms ome em O Sm as awm wn nss  omn  ows
© m ws omm en aes dsow owaw sw mow  om wew
的 ge -ak 20365 2 asmo -4 amwe cr me 2mo 204
1
bs wks -al09 man fw mwe  meme omas on dn 乱 8 -260819
和
昌 ap ee 。zoon Al at0 47 zt cn es ine shis
ES
的 22447135 -2038 Al8 -12215 S040 -3660 CE\ UmS 全 2 -zsoo7
As 2515 -10 Ag -002 5055  <286dn lozd 714
AM。 -12207 。 39580 。 -28174 AD  1ASL  S0A7  MSBT “Do3 。 -9973  65265 -299252
ol 6 23 机 全 贡 而 到 殉
EDEEEESRE 全
可 2 a B JW ew am sa on w aa
%  mw —nwl 站 8 4247 27215 -205655 O -49405 -36946 -294447
下 中 Chde Towm we wen me mses on wos mmo men
Ye 1212 -298090 B20 。 5L780 。 4002 。 -295650 。 E22  -68508 。 -22304 -291995
|
名 0 ew co sm dow 各 JE， ele0 oms | wml
5
0 eg -ak -2 cmo mwr weo ms os sm mws zsm
oo au mc ms ows 和 丽 _ -90 砚 50 ol
7 -30 -区 59 on wm dast “25809 多。 -0370 46908 20292
0
Dog -0 aetz0 0  0M 6109， om A00 时 7 的 10 -mom
 oum mew ams om amssow msos An d oon 291597
 mms ioe cese om mm am uo Ae 120 Ga wan
as oosetass sas 6 丽人 和 “gois su oizs eew -206202
io。 eme owsn el 一 5 mm aeswm ws wim om wm
[证 oam 证 而 am sd Driwe po meso os wx2 uso mme
区
oo ou mxs 52 -0 co 273 4669 -5064
®o mas ww momo M5 Mns moe wes co wms we nos
54

## Logical image page 55

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 55 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A55.jpg -->
<!-- source_image_sha256: 8CFF3D5E8F60DA3ECB90111B8F7B74FBD450E0B7C6437B839A7DA9327F32725F -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

w wme aw ms Gr wss mes mes Go wse  oml mme
有 ol was was Go mws  won -2507 Gi Gm  a meom
w mw mw mm co ew mw omws co sm mss mm
eyei0 om  wus co wam  wen omen Go wms wsi 0100
让
E owee mms om op we Gon ww 5 em  es i
oo .520 mws 0 mms mo mes o  oms inms aas
©o msi  wmw mas cu le  Ts wow by 10007 oms asw
se 0 -la 06 swe  wm mee 0 200 wme meis
Go wm au mws ow oms  wwo 22， Di 20 如 602 -204
0
n men ly 0 0 -1006 Tew man 051 4900、 0529、
人
06 ol 区。 全 13 mowe 0 6 Sas -2760
ma Wo 5 0
or 人 0 人 055 won -31 -2
的
-al -ao5 05 00 ol， 区， sin -ol 和
现 丰 区 二 本 天 人 w sClnls  hes
ER 站 SLC
ol 00 20 乓 齐 苛 -52 un -mca
-an wm -age co _mes  ow mew w 本 全 26125 ma
加 ae mes aemspen vwr me m mer sme mer
EPE
ancient
Cr EPwd tA Sie Tein m fES se 1i EBOS
二

人 an zz。 zsn  wes m w ar oe oa
aa mr ww wx owon Ae aws wus we
0 smoe dows Me Wm won 大， Ae wa7  wws  me
人 25
az 0 2 5
0 0 ML omo ao0 1 大 6 msss
的
人 天 和 AT oa5 owa
2 mes moms AM wen wme mem so sm wms mwo
aaa。 mos me wse somo mesos 0Bk zao6 -mes
站
Ms 站 25 恒 7 owe mo 元 05， wmims “gums su  em ozm -2 人
w wi mss mms mess  Bie owwn ws oow im mie
meows wen wen mp Jsime use mn 上 wes -008 -ant
go ww mm m wm owe oww 55。 97305 ow mom
oe wme .e 各 ft oem sie mes 上 soms wmo ms
Go mus mau mes on oon mas Tess ow ewn ass zss

55

## Logical image page 56

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 56 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A56.jpg -->
<!-- source_image_sha256: C565776DDC853640EFB26942A51F092D57405C66445D29C029BDC94524A29961 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

1
oo 7 0000、 3000-l0y0ot -2700 009、 es 1090 ma
pt 0 we ime mor oe wms m am
ptl  mus owBo OT 0900。 的 970 mM DO oien -区 70 m2
0
0f mwe mm omee on we mu omew oo anim -39 210 人
Go sw ws mox n eml Tis mer m pis mue zms
oz hg mus Of ws ene mes el -119179 760 215125
o oms ss omem on msn wws mwe me uews em zoss
ao wws wme om oes @mw omus B0 Amw sus  mow
go DR 650 S10 55 而 dwis 1659 mee
-00 -25 多 -15224， 45291064 1 的。 zean
的 -gg -on 大厅 遇 -ie 0 omae 晴 -7 sew mam
0 le 0992 -HT 1007， @ wm 5L2 27
5
-pz5 -92 wus el -10990813 omiew eg45 、 740 2760
的
人
的
Te
鳃 10 -6 2080 E6 抽 6  05519 0 16806127
B “-oy609 -025 -2014 ET7 TB -项 g Wo5 “4762 116759 -273140
可 -om nwo as es 6
ER mman REED
人
区
om 人 ai is om sws wne 了

Cops os。 -zs Am -lx lastz -73 clol eez4 -IDa416 -512L_
w Tois Tem mosm A ews uews omz cle wom isme 2WG
Me wsm wo ome ms oin oms mes o6 omr -i2m z0s
090242724 Cm  wiew 04 26 co 20028 aa ne
ogg -Zn06 cm。 后 7  Toms 202 CI05 10013 -ISkeo -290357
hao ina -am ol nan eiz meenll ocooio] -ims To
0 008 的 4 21030009 -10000 -1419020831
1072
AR ows oms mmn op  domy 罗列， 2 005 ows miw zmse
an。 ome me om sews -iooiss rmesow ow -tisws .25
ol m oman ae won 1259 me on -人 8。 -08419 2152
Co js6 由 -6 mom 0 而 oa -070 “aser oo -505065 -102770 -275911
Cap -7 mee cnow Te2 2280 Do。 的- -216178
em 本 两 -oz7 0 用 oa -as6 037 Da -0 men amom
CR gm。 ez8 mes ow dow -27877286 DI0L wms mz -2155
low wme wds’ ez om age .nr -005 bile -9907 190274281
让

56

## Logical image page 57

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 57 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A57.jpg -->
<!-- source_image_sha256: F6657A8DD6F0D2707D9683ADEBEF29FD2FAECF5D0C307ECC08232CE4C429546D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

二 了 om me o do ouke Zeil oi ise sne 交大
5
机关 0 二 本 病史
rz ask euy il 0 -3090 cl 00ol lg ”2522
本 二 天 6 moms t dom weo mws bi .00 ew
本
Bo mm um zme om wss oio we owo mm wse
 ows gg mm om 1005 ems zw0 DY won 16110252
o e——
ip 52 mes cl swen was zwas bit ol 55 zos
二 天 现下 机 omes o eso i ss bus we sw wa
eol oot 92。 00 cl、 wos -ton 2039 DIM 的 NI -1052
for was ma zwes os oe elow e bus e e0 2ars
lg “ol pt om mok ews ozs bue 的、 11231925
fo oum wuo ;se om won wss muo ow ww wshs mie
fo om wws sm olzl ows wen zeus ous uem sel 23
cur mrs en mwos om woe wmas m ous ws wsE
EEC 二 -HTCO
Gu ms men mie oni soon woss man ourChso Joim | hvae
CHS 和 0657 。 -112567 -272007 DIZS -39967 -134874 -266480) DISACMST-617R2  -254763
二 Di 0 ieo AEGnNOEAMhstus wma 三 本
ty” 和 0 -58028407 _Em -R10 NI0 EI -19 -34 -24979
5 二 砚 肌 0 下 人 而 二 本
ago yes wen ni 有 meo -zsz tm onwiezmn
0 二 请 二 0 了 ai Dot 珊 友 80 mmn wm 区 大
Di ， -00 一 | 20TH olsl -人 7 Siish TTI EL -51016 6955  -20%
 CTber” sun ou soo im are  sam union
OI8\.20080  13763 -266005 DISI -115963 T9ES -265267 El43 -145166 。 15861 。 -262271
oud® oon iem aeow oi  milo mws fa ds 2 aw
oo ous sea de ows mes son mos fe es sws me
DIl -49871 -119090 -271080 DI% -141877 -56641 -258406 El146 -146W0  50297  -263505
ow se zs mes fn mus wm mw ET in ee mas
ns go36 0670 27240762 -0 wen meon fu usen Tas men
oe maw ww omw fm vewe ma mon fe mm wws mus
和
herg ant 85 大 3 二 天 了 ogg 1 nr .290
Di -07005 7689  aeses Ei AsTrs 752 6-cioy i -162605 -25130
he Heat 的 5L 地 31 ED wgs NI “寡人 Gn woow mse -eou
Die jat74 请 -lan 是 AoE 和 2 | “Heme pl5 -oo -lasl -246 人
-116l3 司 -20607 E10 天 加 90 5679  28203 DIST -30110 -162373 -250884
Er im
站 上 训 n -2 和 fano ez -15g6 Te0  wr Ole -ao .0320 25972
0
57

## Logical image page 58

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 58 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A58.jpg -->
<!-- source_image_sha256: 6E15EAAF6612FDC1E2DC0B3FF574C1A074965C075EF3180B084CD41EB225E858 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

En
En psen ne 7logl cy en 1ag9I0 me7 DIE -9T17 -13080 25154
8
fis men ay mm Cg 159 -ly75 26369DI6 9T8 ，-116222 25104
fie amm wme mm c ome usw meen Ows wm ows ssn
fis awse mee omen cm oms mes  Ows me o ses
本 0 est bi wim ion ine odo em -iws 2
pool -46L 206 ol ws -8651 -2067  2s 106195 2597
07 mns mowr Di Tomw mn asw o wew m wa
om ssas mur ec Ome won wik ew 0s Alos -wwe z
om wi m eis omo omi sx awme o 5
tl  l DoOI 10030 IBGO 260 D265 120127 13709128612
多
0 327 29006009 “11904122009 240130267 -8615121009 -291136
8
Le ome 25907 Da05 “130409 108224 27 D249 16476108029 “228070
锯末 关 天天
RIPPER HE -mz 6 SR 和
击 吏 大 而 一 而 而 6 两 一 吉 可 六 全 而 丙 _0 交 5 y
ol” 2 Do “150 165， 256 0 放生 各 oot 7 272
让 而 下 本 上 ER 二 二 三 泡 区 ha 二
-ug gog -za Elol _uewe wm mige Dme -lg0z0 -52057 25416
6 mete er am aw
 G e
ove om _yerdias [Eiiamse 到 本 三
Dn5 -comRl<frotie |-ahaT f195 -1607m。 -18623940
sri)oon en siss coamassuaanm
pieoag zeso hy 7657， 625 .296
orid! wozm swams zon ewe mms wosszs
om ow wem m aw wee wo0 ea
D180  -79924 -141563 -252350 E0 -166254 40907 -247114 et
lo -tao -27 El -98528224
pm
pa naan nz 人 45 pz a
oms mass wse 20u0 Dmo wws -sen 20wm
os Lp -97 dewo om wmeo aes -ao 下
5
Dife -ie8S1 05 重 20 0 120343. -1SA002 |“Hhoseh
EE T —
loe mas esim alg- px 天 theos -na 227
pptea sems gwms Haog ao 01117522
[eims avhacs snise’ 0147 D27 -isoen -10se 友人
ce mon sss ume oms usw ssus zsa

58

## Logical image page 59

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 59 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文A题-A217/A59.jpg -->
<!-- source_image_sha256: 582A19F6477E9C0CED2BF7F6EDF73784654C06D354F316AEEE762DD2A103F52C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

5 2oes o dws ewmo duwe
:zz
SEE
Ca = =
本 ae
el
Gy5 ao
