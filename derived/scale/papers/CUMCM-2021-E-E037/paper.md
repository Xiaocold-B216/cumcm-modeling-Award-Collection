# Extracted Paper

<!-- source_page_kind: image_sequence -->

## Logical image page 1

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 1 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E1.jpg -->
<!-- source_image_sha256: 17AFC86E098AD0A88D6C75DC699EC70FD5C5848C68CBDB492F970D3DECBBFE27 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

基于 红外 光谱 法 的 中 药材 鉴别
摘要

本 文 对 附件 中 的 数据 进行 了 统计 分 析 , 对 不 同 的 问题 分 别 建立 了 聚 类 和 分 类
模型 , 通过 红外 光谱 数据 实现 了 对 中 药材 的 鉴别 。 首 先 对 附件 1*4 的 所 有 数据 进
行 了 预 处 理 ， 通 过 作 图 发 现 部 分 波长 的 数据 差距 很 小 ,于 是 利用 极 差 ， 将 差异 不
明显 的 波长 数据 别 除 ,再 对 所 有 的 数据 进行 降 维 处 理 ， 将 数据 量 压缩 到 适当 范围
内 。 最 后 对 不 同 题目 的 涌 类 和 分 类 模型 进行 求解 。

问题 一 ， 通 过 对 附件 1 的 中 红外 光谱 数据 进行 探索 性 分 析 ， 发 现 了 其 中 有 3
组 数据 〔 第 64、136、201 号 ) 属于 异常 值 ， 将 其 史 除 。 然 后 利用 极 差 ， 吻 除 挤
极 差 小 于 均值 的 数据 ， 使 得 数据 从 原始 的 3348 维 降 到 了 1331 维 。 在 此 基础 上 ，
通过 比较 研究 发 现 非 线性 隆 维 算法 比 线性 降 维 算法 效果 更 佳 ,于 是 采用 非 线 性 的
等 距离 映射 算法 (lsomap)， 将 数据 维度 降 至 3 维 。 最 后 建立 了 聚 关 模 型 ， 选 择 了
K-means 算法 进行 聚 类 ， 通 过 其 轮 麻 系数 的 计算 ， 发 现 聚 为 3 类 最 为 恰当 。 崭 除
3 组 数据 后 ， 余 下 422 种 药材 ， 被 聚 为 3 类 ， 每 类 分 别 有 96,137,180 组 数据 。

问题 二 ， 采 用 了 与 问题 一 完全 相同 的 数据 预 处 理 方式 】 特征 提取 非 线性 降
维 ， 然 后 建立 了 分 类 模型 。 利 用 支持 向 量 机 进行 寞 型 求解 ， 将 已 知 数据 分 为 训练
集 和 测试 集 ， 通 过 反复 调 参 ， 使 得 模型 训练 集 的 正确 率 达 到 98%， 测 试 集 上 的 正
确 率 达到 93.9%。 最 后 代入 未 知 数据 得 到 如 下 结果 :
| |3[1aasas|ss[7a]79] 86 |e9[ no|14|3152|222|331| 6 |
| op Je[1falMw0l6]e]2a]3s[a[o]2[s[a]3 |

问题 三 ， 癌 题 二 多 出 了 近 红 外 5997 组 数据 ， 林 文采 用 了 特征 提取 ， 非 线
性 降 维 等 与 问题 二 类 似 的 方法 进行 数据 预 处 理 。 研 究 发 现 有 些 中 药材 的 近 红外 区
别 比较 明显 , 另 一 些 则 在 中 红外 区 别 比较 明显 ,通过 支持 向 量 机 及 从 未 知 数据 到
已 知 数据 的 最 短 欧式 距离 的 计算 发 现 , 在 近 红 外 、 中 红外 及 合并 数据 上 的 结果 不
完全 相同 ， 本 文选 择 重复 率 较 高 的 产地 做 为 最 终结 论 :
[op Dllalazla2la6lala1al9| al

间 感 四 ， 通 过 作 图 发 现 ， 不 同 药材 类 别 区 分 度 较 大 ， 可 以 直接 将 A 类 药材 与
BC 类 药材 区 分 开 。 再 研究 BC 类 药材 ， 通 过 先 特征 提取 、LLE 局 部 线性 降 维 方法
建立 分 类 模型 。 进 而 用 支持 向 量 机 ， 得 到 了 比较 明确 的 分 类 ， 不 论 是 训练 集 还 是
测试 集 都 达到 了 100% 的 准确 率 。 这 说 明 不 同 种 类 的 中 药材 的 光谱 区 别 是 比较 明
显 的 。 最 后 ， 采 用 问题 三 完全 相同 的 方法 求 得 药材 的 产地 。 结 果 如 下 :
[No [ salt [ 278 | 308 [ 330 [ 347 |
[aas | AAA [ c | c¢ ec [ B |
[os5 | 3 [ 2 [ 1+ [ 3 14 [ u |
SBE: Isomap 非 线性 降 维 ，K_means 聚 类 ， 分 类 模型 ， 支 持 向 量 机 ，LLE 算法

## Logical image page 2

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 2 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E2.jpg -->
<!-- source_image_sha256: F299F8D1153FA9DE2E877C797FD18AD62245EF2D77925BB9E5F03D4A72664751 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

一 、 问 题 重 述
1.1 问题 背景

中 药 是 中 医 之 本 ,中 药材 的 精准 鉴别 对 于 中 医治 疗 帮 助 巨大 。 随 着 科学 技术
的 不 断 发 展 ， 运用 近 红外 、 中 红外 光谱 的 照射 来 辨别 中 药材 的 种 类 与 产地 已 经 成
为 主流 方法 之 一。

中 药材 的 种 类 鉴别 在 红外 光谱 的 照射 下 比较 明显 ， 在 对 于 中 药材 的 产地 鉴
别 ， 及 样本 量 不 足 的 情况 下 ,我 们 需要 运用 近 红外 与 中 红外 的 光谱 检测 数据 进行
特征 与 差异 性 综合 分 析 ， 得 出 中 药材 的 道 地 性 。

1. 2 已 知 条 件

1. 各 药材 光谱 照射 的 波 数 。

2. 各 药材 在 对 应 波段 光谱 照射 下 的 吸光 度 。
1. 3 需 解决 的 问题

1. 分 析 几 种 药材 在 中 红外 光谱 照射 下 的 吸光 度 特征 ， 比 较 不 同 药材 吸光 度
的 差异 性 ， 并 以 此 对 药材 分 类

2. 结合 不 周 产 地 的 同 种 药材 在 中 红外 光谱 不 同 波段 照射 下 的 吸光 度 ， 分 析
由 产地 不 同 造 成 的 吸光 度 特征 与 差异 ， 并 给 出 各 药材 产地 的 鉴别 结果 。

3. 统计 、 分 析 某 一 种 药材 在 近 红 外 与 中 红外 两 种 光谱 照射 下 产生 的 数据 ，
并 给 出 该 种 药材 产地 的 鉴别 结果 。

4. 不 同 药材 在 近 红外 光谱 照射 下 的 吸光 度 不 同 ， 根 据 给 出 的 数据 特征 ， 分
析 并 得 出 各 药材 的 类 别 与 产地 。

二 、 问 题 分 析
2. 1 问题 一 分 析

附件 1 给 出 的 数据 共有 3348 个 不 同 的 光谱 波 数 ， 其 中 并 不 是 所 有 光谱 波 数
上 不 同 种 药材 的 差异 性 都 很 明显 , 因此 首先 可 以 将 不 同 种 药材 上 差异 性 较 高 的 光
谱 波 数 所 取出 来 作为 特征 区 间 。 而 对 大 量 未 知 种 类 的 药材 数据 进行 鉴别 ， 那 么 将

2

## Logical image page 3

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 3 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E3.jpg -->
<!-- source_image_sha256: 41DE543E3D53DBC2FECC54B005A28AED47652AD90E3DA810440DC12BAE641DF3 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

特征 类 似 的 数据 归 为 一 类 是 较为 不 错 的 做 法 ， 即 聚 类 分 析 。 而 聚 类 分 析 要 求 数据
的 维度 不 能 过 高 ,所 以 在 聚 类 之 前 应 当 将 数据 降 维 处 理 ， 使 用 线性 或 非 线性 降 维
算法 将 数据 维度 降低 到 合适 的 维度 再 聚 类 就 可 以 将 同 种 类 的 药物 鉴别 出 来 。
2. 2 问题 二 分 析

附件 2 中 大 多 数 药材 的 产地 已 经 标明 ， 需 要 鉴别 未 标明 产地 的 15 个 药材 料
本 。 对 于 将 未 知 类 别 样本 归 类 到 已 知 种 类 中 ， 属 于 分 类 问题 ,由 于 不 同 产地 的 同
种 药物 数据 差异 较 小 ,提取 出 特征 区 间 就 更 加 重要 。 同 样 数据 也 需要 降 维 。 在 完
成 数据 处 理 之 后 ,可 以 使 用 随机 森林 或 者 支持 向 量 机 进行 模型 求解 ， 将 已 知 数据
分 为 训练 集 和 测试 集 。 调 整 参数 建立 合适 的 模型 进行 求解。
2. 3 问题 三 分 析

附件 3 中 有 两 个 表 , 包括 中 红外 数据 表 和 近 红 四 数据 表 ; 如 果 将 近 红外 数据
表 去 除 ， 那 么 和 问题 二 没有 区 别 。 由 于 有 些 中 药材 的 近 红外 区 别 比较 明显 ,而 另
一 些 药材 的 中 红外 区 别 比较 明显 ,所 及 我 们 可 以 考虑 先 用 其 中 一 个 数据 表 来 建立
模型 求解 , 再 用 另 一 个 数据 表 及 音 并 两 个 表格 同时 对 鉴别 结果 进行 矫正 和 互相 验
证 以 提高 鉴别 的 准确 变 。
2. 4 问题 四 分 析

附件 4 中 , 除了 有 产地 还 有 类 别 ， 可 以 认为 是 在 问题 二 只 需要 鉴别 产地 的 基
础 上 增加 了 药品 种 类 的 鉴别 ， 而 产地 和 种 类 均 有 较 多 的 数据 缺失 ， 可 以 在 对 照 二
者 缺失 值 后 ， 再 分 别 对 产地 和 种 类 建立 分 类 模型 ， 最 后 将 两 个 模型 分 别 求解 。

三 、 模 型 假设

1， 中 药材 类 别 确定 ;

2. 题目 各 附件 所 给 的 数据 真实 、 可 靠 ;

3. 各 类 中 药材 在 红外 光谱 照射 下 未 受到 其 他 因素 干扰 。

3

## Logical image page 4

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 4 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E4.jpg -->
<!-- source_image_sha256: 0E174B3349FC34F3AB93B369C31713A17BDA029B5272C91E2A295F7074516041 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

四 、 符 号 说 明
符号 定义 符号 定义
Vi 光谱 波 数 Ai 吸光 度
Tilm, n] 特征 区 间 B PAREEE
A 特征 值 矩 阵 S@) BONi KRTRIRBRRL
7, 特征 向 量 X, 曲线 计 间 的 欧 氏 距离
五 、 模 型 建立 与 求解
5.1 问题 一 模型 建立 与 求解
5.1.1 数据 预 处 理
对 于 问题 一 ， 首 先 对 附件 一 中 的 数据 进行 检查 ,使 用 Python 编程 处 理 检 查
以 下 数据 异常 情况 :
1. 是 否 存在 缺失 值
2. 是 否 存在 异常 值
3. 是 否 存在 大 量 重 复 值
经 计算 ， 在 附件 1 中 未 发 现 缺失 值 ， 但 有 3 组 数据 异常 ， 也 未 发 现 重复 值 ，
数据 完整 性 好 。
表 1 附件 1 数据 描述 性 统计 结果
[ew [ee [we [oe |oas [e [e |o|
[| | oswr | omss | oo | oo | aa | oarns |
[ao | oa | oa | omss | ooss | oa | arm | oa |
“os| maoom | oaon | oses | owss | ooss | owes | azm | oa |
“oss| waoom | oass | oo | omss | ooss | ouss | ars | omo |
“oss | waoom | oass | oso | omss | ooss | ouss | arn | om0 |
[| 二
[0 | oous |
[| | oa | oo | aao | soms | omeo | aous | oous |
[| omes | ooms | ooms | omer | aouws | oo |
“om | wacom | oows | omes | ooms | ooms | omer | aows | ooms |
4

## Logical image page 5

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 5 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E5.jpg -->
<!-- source_image_sha256: 7F47EAB2609CE4A8E03C8C9A10A0217C41E3379A19306AE627C07D239CA19A93 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

附件 一 共有 425 条 药材 光谱 记录 ， 每 条 记录 有 3348 个 不 同 的 光谱 波段 数据
项 。 本 文 先 对 3348 个 不 同 的 光谱 波段 进行 了 大 致 的 描述 性 统计 。 结 果 见 表 1。
进行 描述 性 统计 之 后 , 先 将 原始 数据 425 条 药材 记录 的 数据 绘制 在 同一 个 图
表 上 ， 作 出 图 像 如 下 :
SaVNE
0.6 | AAA [|
| 人 | |
Bos i 5 一 | | |
vm | |
0.2 中 DR
0 二 一 | | |
允 E  CEA
波段
图 1 附件 1 原始 数据 图
从 原始 数据 图 像 中 可 以 看 出 有 三 组 明显 异常 的 数据 ， 利 用 3 5 原则 ， 我 们 计
算得 出 异常 数据 分 别 是 编号 为 64、136、201 的 药材 记录 ， 删 除 后 的 图 像 如 图 2.
二 一 一 一
葛 o2 | | 一 | 一 一 |
NA 全
of  — Neemet TN |
& R2 & & & & 区
波段
图 2 附件 1 删除 原始 数据 后 的 图
删除 3 组 异常 数据 后 ， 可 以 看 出 从 图 中 看 出 ，422 条 药材 记录 的 中 红外 光谱
5

## Logical image page 6

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 6 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E6.jpg -->
<!-- source_image_sha256: 46E3AD41DC6681EF0790EEC9D1B9FB1576A7A8A025171B2360F51602F90D9E55 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

数据 图 整体 趋势 差别 不 大 ， 其 图 表 特 征 表 现 为 其 光谱 波 数 区 间 为 [1700，2800] 左
右 时 ,不 同 药材 的 吸光 度 差 异 较 小 ， 其 数据 曲线 贴 合 度 较 高 。 类 似 的 光谱 波 数 区
闻 还 有 [3650，3999] 等 。 而 在 光谱 波 数 区 间 为 [6552，1700] 堪 右 ， 不 同 的 药材 吸光
度 差异 较 大 ， 类 似 的 光谱 波 数 区 间 还 有 [2800，3000] 等 。 此 类 光谱 波 数 区 间 对 于
不 同 的 药材 记录 ， 吸 光度 差异 较 大 ， 其 特征 适合 用 于 分 辨 不 同 药材 种 类 。
5.1.2 问题 一 模型 建立
我 们 定义 ， 当 一 个 光谱 波 数 区 间 [ 到 可 上 每 个 光谱 波 数 玉 (m<z< 人 六 在 所 有 药
材 记 录 中 的 吸光 度 和 最 大 值 减 去 最 小 值 ( 即 极 差 ) 大 于 所 有 波 数 吸光 度 的 平均 极
差 。 则 称 该 区 间 为 特征 区 间 。 记 为 了 [xm 可 ， 即 ;
4 -4 >4  m<i<n
5.1.3 问题 一 模型 求解
使 用 Python 编程 ,最 终 从 附件 工 中 提取 出 特征 区 间 Ti[652，1472]，Tz[1506，
1674] ，Ts[2846，2855]5、Ta[2906，2936]，Ts[3151，3450]。 区 间 总 长 度 为 1331
列 。 即 从 原始 数据 的 3348 维 降低 到 1331 维 ， 降 维 后 的 数据 大 小 为 422x1331。
对 降 维 后 的 数据 使 用 Python 编程 进行 标准 化 处 理 ， 处 理 后 的 结果 如 下 图 :
— 5 T T
\ B |
o RN 一 全
| \ |
晶 。， MAN AS S | | 用- 5
”| UN 局
人 N NS 从 给 | 才 | ER
AAA
人 天 = = LAC"> T _
¢ & &
波段
图 3 提取 特征 向 量 后 的 图 形
6

## Logical image page 7

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 7 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E7.jpg -->
<!-- source_image_sha256: 17B22B294F247140E52202584DBDB96AD799A221D2AE26D460E7E1842EBD24D7 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

经 过 前 期 的 特征 值 提 取 后 已 经 将 数据 从 3348 维 降 低 到 1331 维 , 但 是 尚 不 足
以 进行 聚 类 等 后 续 处 理 ， 还 需要 继续 降低 维度 。 经 过 反复 尝试 ， 我 们 发 现 非 线性
降 维 算法 比 线性 降 维 算法 效果 更 佳 ， 于 是 选择 了 非 线性 的 等 距离 哆 射 算法
(lsomap) 进行 降 维 。

等 距离 卫 射 算法 (lsomap) 是 一 种 非 线性 的 降 维 方法 ， 其 原理 基于 多 维 尺度
变换 算法 (MDSs) ， 是 MDs 的 一 个 变种 ， 试 图 保留 数据 内 在 的 由 测 地 线 距离 列
含 的 几何 结构 。

(1) lsomap 算法 使 用 流程

Step1， 设 置 每 个 点 最 近邻 点 数 k， 构 建 出 连通 图 和 邻接 矩阵 。

step2， 通 过 图 的 最 短路 径 构建 原始 空间 中 的 距离 矩阵 。

step3， 计 算出 内 积 矩 阵 妃 。

Stepd: 对 内 积 矩阵 了 进行 特征 值 分 解 ， 获 得 特征 信 矩 阵 代 和 特征 向 量 矩 阵
V.

step5， 取 特征 值 矩阵 最 大 的 前 鼠 项 及 其 对 应 前 特征 向 量 Z = 用 4 。

利用 Python 编程 实现 该 算法 后 ”数据 维度 降低 到 3 维 ， 处 理 后 的 数据 大 小
为 422 x3 。

对 于 问题 二 7 主要 需要 解决 的 是 识别 不 同 种 药材 的 特征 ， 实 现 对 药材 种 类 的
鉴别 。 使 用 聚 类 算法 可 以 有 效 的 将 具有 同类 特征 的 药材 么 为 一 类 ， 实 现 鉴别 。 本
文采 用 了 经 典 的 Kmeans 聚 类 算法 对 降 维 后 的 数据 进行 聚 类 。

(2) K-means 聚 类 算法 使 用 流程 介绍

Stepl: 指定 需要 划分 的 类 的 个 数 K。

Step2: 随机 地 选择 K 个 数据 对 象 作为 初始 的 聚 类 中 心 。

Step3， 计 算 其 余 的 各 个 数据 对 象 到 这 K 个 初始 聚 类 中 心 的 距离 ， 把 数据 对
象 划 归 到 距离 它 最 近 的 那个 中 心 所 处 在 的 类 中 。

Stepd: 调整 新 类 并 且 重新 计算 出 新 类 的 中 心 。

Step5， 循 环 步骤 三 和 四 ， 看 中 心 是 否 收敛 〈 不 变 ) ， 如 果 收 敛 或 达到 选 代
次 数 则 停止 循环 。

在 进行 means 聚 类 前 关键 一 步 是 确定 一 个 K 值 作为 聚 类 时 类 的 数量 。 因此

7

## Logical image page 8

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 8 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E8.jpg -->
<!-- source_image_sha256: 7C183403660BF9290F5F499ACB7E670ADB18054DE41FD9DE5501BC5050D43309 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

选取 一 个 合理 的 K 值 非常 重要 。 本 文采 取 的 方法 是 枚 举 出 所 有 较为 合理 的 K 值 ，
计算 出 各 自 的 轮 廊 系数 。

轮廓 系数 结合 了 聚 类 的 许 聚 度 和 分 离 度 , 用 于 评估 聚 类 的 效果 。 设 聚 类 结果
中 的 某 个 为 1，i=12,3...N， 该 聚 类 结果 的 轮 廊 系 数 为 S(i)。

ali) = avg( 点 1 到 所 有 它 所 属 的 簇 中 其 它 点 的 距离 )
b(i) = min (点 ij 到 某 一 不 包含 它 的 往 内 的 所 有 点 的 平均 距离 )
SO i=123.N

可 以 知道 轮廓 系数 值 处 于 -11 之 间 ， 轮 廓 系数 值 越 大 ， 表 示 聚 类 效果 越 好 。

使 用 python 编程 计算 出 的 轮 廊 系数 如 下 图 :
聚 类 轮 廊 系 数 图
图 4 K-means 聚 类 轮廓 系数

由 轮 廊 系数 图 容易 知道 ， 选 取 K=3 时 ， 轮 廓 系数 最 高 。 在 此 前 提 下 ， 本 文 使
用 python 编程 对 处 理 后 的 数据 进行 K-means 聚 类 。 最 终 将 附件 一 中 剔除 3 条 异
常数 据 后 的 422 条 药材 记录 聚 类 成 三 类 药材 , 并 按照 数量 高 低 命名 为 A 类 、B 类 、
C 类 ， 最 终 聚 类 结果 如 下 表 所 示 :

表 2 附件 1 药材 分 类 结果

类 别 A 类 B 类 E 关

数量 189 137 96

将 通过 聚 类 分 析 后 鉴别 出 的 三 种 药材 数量 绘制 在 图 表 中 如 下 , 其 中 红色 为 A
类 、 蓝 色 为 B 类、 绿色 为 C 类 。

8

## Logical image page 9

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 9 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E9.jpg -->
<!-- source_image_sha256: 6306A7971766A22EDEF171D2CF0C0885FD2E558C0BA936556D448DD7CB5DB76F -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

0.4
0.3 \ f
|
入 0.2 Y i |
请 :时
| a
01 昌 ， 交 /
:
AL ERA
0.0
& & 2 &
波段
图 5 附件 1 分 类 后 光谱 曲线 图
s1ET 一
5. 2 问题 二 模型 建立 与 求解
5.2.1 数据 预 处 理
对 于 问题 二 ， 首 先 对 附件 二 数据 进行 前 期 处 理 和 检查 :
1. 是 否 存 在 缺失 值 。
2 是 否 存在 异常 值 。
3. 是 否 存在 大 量 重 复 值 。

表 3 附件 2 数据 描述 性 统计 结果
EECOIECOEEICIRCOIECOIEIEOIECOECI
有 EECIREIIEEIEEIEIEEEEZ
EECOEEOIEEOEEOIEOIEEIEZO
EECOEEIEC
EEC
EECOREZIECZIRZIREEEE
EECOECORCOEZOIEIIEZIEEEE
EECOEEG
EECOECORCIETOIECIIECOEEOEE
EECIOEIIECOEIOIECEIEZOIEEIEEG

9

## Logical image page 10

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 10 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E10.jpg -->
<!-- source_image_sha256: E20101D5147A8C5298441898ADCA1822E8C47EC2D21F09E0BAD6B22AD9537ACB -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

附件 2 共有 672 条 药材 记录 , 每 条 记录 有 光谱 波 数 551 至 3998 共 3448 个 数
据 项 , 均 未 发 现 大量 重 复数 据 和 异常 数据 。 其 中 光谱 波 数 的 列 中 未 发 现 缺失 数据 。
表示 产地 的 OP 列 除去 需 鉴定 场地 的 15 个 缺失 项 外 也 无 缺失 项 , 数据 完整 性
良好 。 为 便于 后 续 分 析 ， 本 文 对 表示 光谱 波 数 的 列 做 了 描述 性 统计 ， 统 计 结 果 如
表 3。
5.2.2 问题 二 模型 建立
根据 附件 二 中 已 标明 产地 的 药材 记录 ， 可 以 得 出 该 药材 共有 11 处 产地 ， 其
每 种 药材 的 记录 条 数 如 下 表 所 示 ，
表 4 药材 产地 计数 统计
[计数 | 6 | so | 67 | s8 2 | 87 | s0 | so | 31 | 66 | 55 |
将 附件 2 的 673 条 药材 的 记录 使 用 Python 编程 绘制 出 图 表 , -为 便于 绘图 ，
先 暂时 将 未 分 类 的 15 条 记录 产地 分 类 数据 项 填充 为 0 民 绘图 结果 如 下 :
可 」 tm
1.25 中 一 == SS |
-本 启
1.00 人 呈 r !
一
0.50 e. 了 f # i 4 全
ke: & & o § 只 ES
图 6 附件 2 原始 数据 图
从 图 中 可 以 看 出 ， 来 自 11 个 产地 的 同一 种 药材 的 中 红外 光谱 数据 图 整体 趋
势 差别 不 大 ， 其 图 表 特 征 表 现 为 其 光谱 波 数 区 间 为 [551，1000] 左 右 ， 不 同 产地
的 药材 吸光 度 差异 较 小 ， 其 数据 曲线 贴 合 度 较 高 。 类 似 的 光谱 波 数 区 间 还 有
[1650，2800]、[3500，3998] 等 。 而 在 光谱 波 数 区 间 为 [1000，1700] 左 右 ， 不 同 产
地 的 药材 吸光 度 差异 较 大 ,类 似 的 光谱 波 数 区 间 还 有 [2800，3000]、[3200，3500]
10

## Logical image page 11

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 11 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E11.jpg -->
<!-- source_image_sha256: B8F09204C6D739E70D95DF5AB8EFA2075B5F1AAD1707D898015FAB743ADE9E2C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

等 。 此 类 光谱 波 数 区 闻 对 于 不 同 产地 的 同 种 药材 ， 吸 光度 差异 较 大 ， 其 特征 适合
用 于 分 辨 不 同 产地 的 同 种 药材 。

为 了 放大 图 像 中 的 特征 , 本 文 还 对 附件 1 做 了 一 阶 平滑 处 理 ， 处 理 后 图 像 如

下 ，
让
P 0.02
& 0.00
四 人
波段
图 7 附件 2 做 一 阶 平滑 处 理 后 数据 图

我 们 定义 ,， 当 一 个 光谱 波 数 区 间 | 丈 ,可 上 每 个 光谱 波 数 玉 (mw<z< 太 在 所 有 药
材 记 录 中 的 吸光 度 芭 最 天 值 减 去 最 小 值 ( 即 极 莽 ) 大 于 所 有 波 数 吸 光度 的 平均 极
差 。 则 称 该 区 间 为 特征 区 间 。 记 为 了 [zz] ， 即 ;

4 4 ES

通过 Python 编程 所 计算 出 的 结果 ， 显 示 在 附件 二 光谱 波 数 区 间 [551，3998]
中 ,共有 三 个 特征 区 间 分 别 为 ，Ti[975，1182]、Tz[1293，1732]、Ts[2824，3577]。
三 个 区 间 的 总 长 度 为 1402， 即 包含 1402 个 不 同 且 连 续 的 光谱 波 数 〈 区 间 与 区 间
之 间 波 数 不 连 续 ) 。

在 寻找 到 特征 区 间 之 后 ， 以 光谱 波 数 作为 x 坐标 ， 以 吸光 度 作 为 y 坐标 。 我
们 将 要 分 类 的 15 条 药材 记录 与 已 分 类 的 658 条 药材 记录 在 特征 区 间 上 计算 曲线
间 的 欧式 距离 ，XW，1<i<15， 1<J<658 。

1 1<i<15 1<;<658 n=1402

a
HEd

## Logical image page 12

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 12 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E12.jpg -->
<!-- source_image_sha256: 1FECAC97625BD1846D8C4AD3462AAD98B5038AC7ADF3EE731234E0BD4EE8893B -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

5.2.3 问题 二 模型 求解
使 用 Python 编程 计算 得 出 , 未 分 类 的 15 条 药材 记录 与 已 分 类 的 658 条 记录
之 间 的 距离 矩阵 如 下 。

表 5 未 分 类 记录 与 已 分 类 记录 间 的 距离 矩阵
EECEEOECOECOICOREOEZOIECIECO
| ooo | 11 |0072 | 0176 | 0067 | 0071 | | 0086 | 0121 | 00%9 | oo8o |
| 2000 | 1 |00s7 | o1st | 0093 | 0062 | | o082 | 0122 | oo92 | ooss |
| 4000 | 5 | 00s6| 0203 | 0115 | 0090 | -| 0095 | 0090 | 0133 | 0106 |
| so00 | 7 |00s6| 01a0 | 0156 | olol | | 0128 | oa61 | oo9l | oo97 |
| 6oo0 | 8 |0089 | o11s | 0192 | 0132 | | 0141 | 0354 | ol | oao7 |
I  P I
| 669o00 | 9 |0129] 0216 | 0059 | 0106 | -| 0117 | 0a72 | 0128 | 0125 |
|67000 | 5 | 0087 | 0183 | 0079 | 0072 | | 0067 | 0124 | oo9l | 00s7 |
| eztoo | 4 | 0130 | 0222 | 0036 | 0107 | | 0107 | 01a7 | ol16 | oalz8 |
| 672000 | 5 | 0116| 0222 | 0079 | olo4 | | 0091 | 0089 | 0122 | oa26 |
| 673000 | 1 | 0078 | o145 | 0105 | 0098 | -| 0104 | o144 | 0102 | .0085 |

将 15 条 未 分 类 药材 记录 与 已 分 类 的 药材 记录 对 比 愉 车 两 者 之 间 的 欧式 距离
最 小 , 则 可 以 认为 二 者 的 光谱 波 数 数据 曲线 在 特征 区 间 上 重合 度 较 高 ， 即 二 者 极
大 可 能 产 自 同 一 产地 。

筛选 数据 可 以 得 到 与 未 分 类 的 [3， 14， 38， 48， 58，71， 79, 86, 89,
110, 134, 152, 227, 331,，618] 号 药材 重合 度 最 高 的 光谱 数据 曲线 为 [280， 518，
599， ,124，327，4，193， 505，588，531，497， 75, 251, 537, 154].

对 应 的 产地 分 别 为 [3， 6)，(14， 1), (38, 4), (48, 6), (58. 7), (71, 6)，
(79， 2), (86, 6), (89, 1), (110, 4), (134, 9), (152, 2)，(227， 5)，(331，
8), (618, 6)].

通过 距离 拟 合 已 经 可 以 初步 鉴别 出 15 个 未 分 类 药材 记录 的 产地 ， 为 了 提高
鉴别 准确 率 ， 再 利用 支持 向 量 机 ， 对 15 个 未 确定 产地 的 药材 记录 进行 模型 求解 。

这 次 ， 我 们 选择 了 LLE 降 维 方式 (Locally Linear Embedding) 局 部 线性 降 维 ， 经
过 反复 调 参 ， 我 们 将 数据 维度 降 到 了 35 维 。 这 样 既 保 留 了 原 数 据 的 主要 特征 ，
也 充分 减少 了 计算 量 。

对 于 和 输入 空间 中 的 非 线性 分 类 问题 , 可 以 通过 非 线性 变换 将 它 转化 为 某 个 维
特征 空间 中 的 线性 分 类 问题 ， 在 高 维特 征 空间 中 学 习 线 性 支持 向 量 机 。

输入 训练 数据 集 了 = fa, 攻 ) 05, 芒 ) Copy 站 其 中 <R， 呈 <E 仙 -了

12

## Logical image page 13

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 13 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E13.jpg -->
<!-- source_image_sha256: 8274F903B0ED1FFFA3334FAED79DA2F48EE9ADCBA5597589BFC812A163D6C3CF -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

i = 2..N;

输出 分 类 决策 函数 ;

1. 选取 适当 的 核 函 数 天 (2] 和 惩罚 参数 C > 0 ， 构 造 并 求解 凸 二 次 规划 问
题 :

minyY SewssKex)Sa
st. ya =0 0<w <C,i=12,.N

得 到 最 优 解 w = (ao ,ocxy) 。

2. 计 算 ， 选 择 w 的 一 个 分 量 ww 满足 条 件 0<o<C ， 计 算
b'=y, ->ary ECGoz)

3. 分 类 决策 函数 : F)=sign(D)e yK (x.%)+5)

直接 调用 Python 的 -sklearm: 库 中 的 函数 SVC 编程 计算 , 将 已 知 数据 分 为 训练
集 和 测试 集 ， 通 过 反复 调 参 ， 最 终 我 们 的 模型 在 训练 集 上 达到 98% 的 正确 率 ， 而
在 测试 集 上 达到 93.9% 的 正确 率 。 最 后 带 入 未 知 数据 得 到 结果 如 下 表 所 示 :

| No 3 14|38|48 | 58|71|79 | 86| 89 | 110 | 134 | 152 | 227 | 331 | 618 |
[oplj6|114|7|1016|16|213|4|191215|18|13|

5. 3 问题 三 模型 建立 与 求解

前 期 对 附件 3 数据 处 理 采 用 了 和 问题 二 相同 的 步骤 , 即 检查 数据 、 数 据 降 维 ，
标准 化 等 处 理 。 另外, 由 于 附件 3 有 中 红外 和 近 红 外 两 个 表 , 且 两 个 表 在 产地 (OP)
列 均 有 空缺 值 ， 经 过 编程 对 照 ， 发现 两 个 表 的 空缺 值 一 致 ， 且 与 问题 三 所 需 鉴别
的 10 条 药材 记录 一 致 。 说 明 数 据 完 整 性 良好 ， 其 他 数据 均 标 明了 产地 。

附件 三 的 中 红外 和 近 红 外 在 苑 谱 波 数 为 4000 左右 处 相连 ， 相 连 处 只 存在 4
个 缺失 值 ， 分 别 是 4000，4001，4002，4003， 可 近似 认为 中 红外 和 近 红 外 表 为
连续 ， 将 两 表 连 接 后 画 出 数据 图 如 下 :

13

## Logical image page 14

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 14 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E14.jpg -->
<!-- source_image_sha256: 49FF9EAB57B9F67240ABAB383A5CE876679BEB2E410002C6D42A064691FB8837 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

IIEEEEEFEEEEEEEEEEEEE
- 0.6 =l=0 p¥
二

“ET

山峰 1

了 NU

L|||||||||||I|l|| TI
& SEFFLPELELEEEEESEFS
波段
图 8 附件 3 中 红外 近 红 外 合并 数据 区 ~ <
再 将 中 红外 表 中 数据 作出 图 表 如 F， TU

YE | 疏

oo JA

0.2 e 人 NAN

™Ey

q AN 星

了 | uc 人
[Li 1 1 | | wi | SP

& & & & & & &

波段
图 9 附件 3 中 红外 原始 数据
近 红外 数据 作出 图 表 如 下
14

## Logical image page 15

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 15 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E15.jpg -->
<!-- source_image_sha256: 030ED5E5EDF2BC0525CBE58BB9BD6A999FBE994B4AD1E255552B2BF4EFA9FBDB -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

1.0
os ss A ;
上
2 | | 下 业
0.6 4 SB 全
0.4 | h—— —
FF&FSSFSEEESES
波段
图 10 附件 3 近 红 外 原始 数据
5.3.1 问题 三 模型 建立
观察 上 述 三 个 数据 图 表 , 可 以 看 出 与 问题 二 初始 图 表 非 常 关 似 。 因 此 可 以 采
取 与 问题 二 类 似 的 模型 进行 求解 。
5.3.2 问题 三 模型 求解
首先 ， 我 们 去 求 相 邻 两 个 数据 之 差 ， 相 当 于 是 求 导数 。 再 利用 极 差 大 于 均值
的 方法 提取 特征 向 量 。
然后 我 们 还 是 用 LLE 局 部 线性 降 维 ， 对 数据 降 维 处 理 ， 最 后 利用 支持 向 量 机
进行 求解 。
为 了 得 到 更 加 准确 的 鉴定 结果 ， 本 文 对 三 个 数据 表 〈 连 接 表 、 中 红外 、 近 红
外 ) 进行 分 别 求 解 。 求 解 结果 如 下 ;
| [a] 15 | 2 | 30 | 3a| as | 74a | ma] 170[ 209 ]
| 连接 表 | 1 | 1 | 1 | 9 | 16 | 3 | a |0] 9 [ 10]
| 中 红外 | 4 10 | 1 | 2 |6 | 3 | a |n]o aa
| 近 红 外 | 2 | 1n | 1 [ 2 [16 [ 3 | 4 [10[ o [ 1a]
利用 文 持 向 量 机 发 现 取 得 的 结果 在 不 同 的 数据 集 上 不 完全 相同 , 而 不 论 在 训
练 集 还 是 测试 集 上 其 正确 率 都 不 分 伯仲 。 最 终 以 特征 区 间 差 异 较 大 的 中 红外 数据
所 得 出 的 结果 为 主 , 用 近 红 外 数据 和 连接 表 数 据 得 出 的 结果 加 以 禾 正 ， 经 过 综合
考虑 ， 最 终 对 问题 三 所 给 出 编号 的 药材 记录 的 产地 鉴定 结果 如 下 ;
15

## Logical image page 16

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 16 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E16.jpg -->
<!-- source_image_sha256: 1299B3ADF7AB2B2845FC796CF9E9DEF2DEF1623743B0C3E7FD2A7D6D93FB067D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

[op Da Ta 314 1 319 124
5.4 问题 四 模型 建立 与 求解

对 于 问题 四 ,可 以 考虑 成 在 问题 二 的 基础 上 增加 了 对 药材 类 别 的 鉴定 。 提 供
的 是 近 红 外 光谱 波段 的 数据 , 由 于 要 同时 鉴别 出 未 知 药材 的 类 别 和 产地 。 而 类 别
不 同 显示 出 的 差异 较 大 , 所 以 先 对 类 别 进行 分 类 , 将 未 知 类 别 的 记录 划分 到 已 知
的 类 别 里 面 。

在 数据 预 处 理 中 , 通过 附件 4 数据 可 以 得 到 , 除 class、OP 列 外 无 缺失 数据 ，
其 中 class 列 缺 失 143 条 数据 ， 即 有 143 条 药材 记录 不 能 确定 类 别 : OP 列 缺 失
50 条 数据 ， 即 有 50 条 药材 记录 不 能 确定 产地 :二 者 的 交集 共有 7 项 ， 即 问题 四
需要 确定 类 别 和 产地 的 [94，109，140，278，308，330，347] 号 药材 记录 。

将 已 知 类 别 的 256 条 记录 绘制 出 图 表 如 下 :

|
hn : 2
E IAA WET—
TS 会 t 会 人
党 s & 此 届
图 11 附件 4 按 不 同类 别 着 色 的 数据 图

其 中 红色 为 A 类 ， 绿 色 为 B 类 ， 蓝 色 为 C 类 。 从 此 图 可 以 非常 明显 的 将 A
类 数据 和 B、C 类 数据 进行 区 分 。

这 里 就 可 以 判定 有 53 组 数据 为 A 类 数据 ， 将 所 有 A 类 数据 剔除 ， 仅 余 BC
类 数据 继续 判断 。

于 是 我 们 暂时 剔除 A 类 和 已 分 配 为 A 类 的 数据 ， 将 B、C 类 的 数据 单独 绘制

16

## Logical image page 17

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 17 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E17.jpg -->
<!-- source_image_sha256: 47C55A4623DA69AB27BA026C4B9B2776A2188E8B740005C2D98110795FE38EA8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

作 图 并 放大 ， 如 下 图 :
0.7 下 - ” i T | 二 - B
go 本 : | 8
4 SS = —
一 一
各 二 EN EC
二 m= \ ——
村 & & & & 人 -
波段
图 12 附件 4 中 BC 类 数据 分 色 图
B、C 类 数据 贴 合 程度 较 高 ， 从 图 形 上 面 很 难 区 分 出 来 ,我 们 将 未 分 类 数据
和 B、C 绘制 在 一 起 继续 观察 图 表 ， 绘 制图 像 如 下 :
as 直 有 了 al | | |
07 十 o 十 全 | | | |
可 »
入 W ? | 二
一 _
04 二 十 一 2 一 = ——
S=" =
SS 一 一 全
s 党 & 局 学 «
图 13 附件 4 中 BC 类 数据 及 未 分 类 数据 图
容易 发 现 ，B、5C 类 和 未 分 类 的 数据 也 难以 分 辨 出 来 。 因 此 我 们 还 是 采用 问
题 二 类 似 的 方法 ， 先 提取 特征 癌 量 ， 再 将 数据 降 维 ， 建 立 分 类 模型 ， 最 后 使 用 文
持 向 量 机 进行 求解 。 我 们 将 已 知 数据 分 为 训练 集 和 测试 集 , 将 训练 集 带 入 进行 训
练 ， 并 用 测试 集 带 入 进行 测试 , 这 次 得 到 的 训练 集 和 测试 集 的 正确 率 均 为 100%。
17

## Logical image page 18

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 18 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E18.jpg -->
<!-- source_image_sha256: 221382886A1110A2852D8F75724806B87D07ED71AAC2EFC733E92E732CB09458 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

这 说 明 不 同 种 类 的 中 药材 呈现 的 光谱 的 区 别 明显 ,比较 任意 区 分 。 最 终 我 们 得 出
了 分 类 结果 如 下 表 :
| 种 类 | 药材 标签 号
16, 31, 40, 46, 53, 60, 66, 67, 79, 94, 100, 109, 116, 131, 138, 139,
140, 152, 156, 173, 184, 185, 197, 199, 203, 219, 220, 223, 228, 23
2, 233, 246, 263, 267, 272, 276, 279, 286, 309, 310, 311, 313, 329,
335, 346, 359, 368, 375, 384, 387, 388, 390, 392
3, 6, 11, 18, 21, 32, 34, 35, 51, 55, 58, 59, 70, 71, 73, 76, 82, 89,
91, 106, 107, 128, 129, 143, 144, 146, 157, 158, 167, 168, 180, 181,
182, 201, 202, 210, 216, 217, 221, 247, 248, 251, 258, 259, 265, 27
7, 280, 281, 290, 291, 341, 342, 344, 347, 353, 363, 370, 372, 373,
377, 396, 399
5, 20, 22, 30, 33, 36, 48, 50, 101, 110, 125, 136, 137, 154, 175, 17
7, 186, 212, 214, 266, 278, 303, 304, 308, 330, 350, 364, 376
分 类 结果 将 143 条 未 分 类 数据 归于 A、B、C 三 类 ， 其 中 A 类 53 条 记录 ，B
类 62 条 记录 ，C 类 28 条 记录 。 显 示 为 红色 的 为 问题 4 需要 填写 的 了 条 记录 的 分
类 。
完成 分 类 鉴定 之 后 , 再 进行 产地 的 鉴定 , 先 对 附件 4 产地 数据 进行 初步 统计 ，
结果 如 下 :
[it |
(#& | 10 9 | 9 | oa | u| 8 |s0 | |
进行 初步 统计 后 , 我 们 按照 不 同 产地 着 不 同 的 颜色 , 画 出 附件 4 产地 统计 图
0.8
L
\ o EN A
0.6 NE AN 2
NE =
# SN LU | ANNA __—a
VAN 人 NE 攻关 汗 ——— ——
04 SA 全 关 于
EPE | 一
0.2 ~> —_——————
党 s &
波段
图 14 附件 4 不 同 产地 颜色 图
18

## Logical image page 19

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 19 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E19.jpg -->
<!-- source_image_sha256: 55C5A46D125C872730DE5B2917E06214F55E3D48C9952C1D1F9E31775BDAD273 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

由 于 产地 较 多 ， 共 17 种 ， 肉 眼 难以 分 辨 。 因 此 我 们 采取 与 问题 二 相同 的 方
法 进行 分 类 ， 先 提取 特征 向 量 ， 再 将 数据 降 维 后 利用 支持 向 量 机 求解 ， 由 于 原 数
据 图 表 部 分 光谱 波 数 区 间 特 征 不 明显 ,我 们 先 对 原始 数据 做 一 阶 平滑 处 理 ,， 结果
如 下 图 ;

和 & & s 从 & &
波段
图 15 附件 杰 做 平滑 处 理 后 的 数据 图

完成 数据 的 平滑 处 理 后 > 与 问题 三 类 似 ， 提 取 近 红外 光谱 波 数 的 特征 区 间 ，
并 使 用 非 线性 降 维 算 法 进行 降 维 处 理 , 利用 未 分 类 数据 到 已 分 类 数据 的 最 短 欧 式
距离 来 进行 分 类 ， 最 终 分 类 结果 如 下 ;

CT EL

[11762l8260 262 | 0

[027 356  | 6

[5  |5

2, 27, 113, 126, 155, 188, 207, 209, 330, 336, 349, 3
65, 389, 394

S [weswmsm  a

本 本 上 TO ACE

[as

[OO CT

二 IPT 二

ele TO

Cai aa

[li

19

## Logical image page 20

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 20 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E20.jpg -->
<!-- source_image_sha256: 0657F6E17C6A51E4A87AC975FDBEF4EA88C335D9BCF0F8FCDEFFC25757C5E6E2 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

上 表 中 显示 为 红色 的 药材 编号 即 为 问题 四 需要 填写 产地 的 7 个 药材 记录 。 综
合 种 类 和 产地 结果 ， 问 题 四 最 终结 果 如 下 ，
09 | 22 | 308 | 3a0 [ 37 |
[es | oA | oa | oA | c | c | c | & |
[Lo 5 3 2 73 | 4 | aa

六 、 模 型 评价 与 推广

本 文 针对 题目 分 别 给 出 的 不 同 药材 、 不 同 产地 的 同一 药材 在 近 红外 光谱 与 中
红外 光谱 技术 照射 下 的 吸 苍 度数 据 , 统计 分 析出 了 不 同 药材 在 中 红外 光谱 照射 的
特征 性 和 差异 性 ， 并 依托 又 类 模型 为 药材 进行 分 类 ,运用 分 类 模型 实现 了 不 同 产
地 同一 种 药材 的 监 别 。 值 得 在 大 数据 时 代 ， 帮 助 医 生 精准 识别 中 药材 类 别 进行 治
疗 ， 作 用 巨大 。
6.1 模型 的 优点
〈1) 聚 类 模型 :

考虑 到 了 每 个 光谱 泪 数 上 上 不同 种 药材 的 差异 性 不 明显 的 因素 , 并 提取 出 较为
显著 的 特征 区 间 ” 再 使 用 非 线性 的 等 距离 映射 算法 对 数据 进行 降 至 3 维 ， 有 惑 于
后 续 数 据 分 析 。
(2) 分 类 模型

继承 了 问题 一 的 数据 降 维 , 提取 特征 区 间 , 获得 了 可 以 便于 后 续 分 析 的 数据 ，
再 使 用 支持 向 量 机 对 模型 进行 求解 ， 该 模型 速度 快 、 准 确 率 高 ， 且 具有 普及 性 。
6.1 模型 的 缺点

对 数据 多 次 降 维 和 提取 特征 区 间 后 提高 了 模型 求解 效率 , 但 也 使 得 部 分 差异
不 显著 的 数据 没有 得 到 使 用 ,可 以 改进 将 这 部 分 数据 用 于 矫正 模型 。 其 次 该 鉴别
模型 的 前 期 参数 调试 过 程 较 为 复杂 可 以 进一步 优化 使 模型 更 简洁 , 减低 使 用 模型
时 的 学 习 成 本 。

20

## Logical image page 21

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 21 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E21.jpg -->
<!-- source_image_sha256: 50FBDFD5A5BF82ED8425317A7ADF2B78C3F463E10F5A2C46A60B7290744F8C4D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

七 、 参 考 文献

[1 基于 Tsomap 特征 降 维 的 人 脸 表 情 相似 度 评 佑 方法 [了 . 黄 东 晋 , 肖 栅 , 秦汉 , %
晨 凤 ,本 友和 东 . 现代 电影 技术 . 2019(06).

[2] 支持 向 量 机 损失 函数 分 析 [ 林 . 王 华 军 ， 修 乃 华 . 数学 进展 . 2021(08) .

[3] 基于 SVM 分 类 器 的 瘾 痫 脑 电 时 空 特征 提取 方法 的 研究 [J. 易 芳 吉 ， 钟 丽 莎 ，
李 章 勇 . 重庆 邮电 大 学 学 报 〈 自 然 科学 版 ) . 2021(08) .

[4] 相关 币 量 机 多 分 类 算法 的 研究 与 应 用 [D], 柳 长 源 . 哈尔滨 工程 大 学 2013.

[5] R-means 聚 类 算法 在 通信 运营 商 精 准 营销 中 的 应 用 研究 [D]. 郑 舒 方 . 吉林 大
学 2019.

[6] 基于 LLE 降 维 思想 的 自然 计算 方法 [ 耻 . 张 评 瑶 ， 季 伟 东 ， 程 昊 . 系统 仿真 学
报 .2020《〈10) .

[7) 基于 近 红 外 光谱 法 对 温 郁 金 源 3 种 药材 的 快速 鉴别 [J]. 赵 金 训 ， 罗 云云 ，
杨柳 ， 杜 伟 锋 ， 葛 卫 红 . 中 华中 医药 药 刊 . 2020(09) .

[8] 颜 文 勇 ，《 数 学 建 模 》， 高 等 教育 出 版 社 ，2011.

21

## Logical image page 22

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 22 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E22.jpg -->
<!-- source_image_sha256: C05A2CD9165E06EB6AAD296CBCF3867380573FA19CAFC68626D992803F17996B -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

源 程 序 说 明 :
1. 本 文 所 有 代码 ， 均 在 Jupyter Notebook 中 编写 ， 编 写 完成 后 复制 进 word 文档 。
2. 由 于 所 给 数据 均 为 xlsx 文档 ， 用 python 读 入 较 慢 ， 为 加 快 程序 运行 速度 ， 提 高 效率 ， 我
们 先 将 其 另存 为 csv 格式 ， 再 在 程序 中 读 入 。
一 、 问 题 一 Python 源 代码
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data0 = pd.read_csv(P./ 附 件 / 附 件 1.csv, index_col = 0)
data0.shape
data0.head()
data0.describe()
data0.info()
data0.isnull{).any().any()
def my_plot(x):
plt.plot{x.index, x.values, linewidth = 0.5)
def PlotSpectrum(data, str0):
fontsize = 5
plt.figure(stro, figsize = (5, 3), dpi = 300)
plt.xticks(range(0, 4001, 500), rotation = 45, fontsize = 5)
plt.yticks(fontsize = fontsize)
plt.xlabel( 波 段 , fontsize = 6)
plt.ylabelt 吸 光度 fontsize = 6)
plt.grid(True)
data.aggllambda x: my_plot(x), axis = 1)
plt.show()
PlotSpectrum(data0，' 附 件 一 光谱 数据 曲线 图 ')
def box(x):
small = x.mean() - 3 * x.std()
22

## Logical image page 23

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 23 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E23.jpg -->
<!-- source_image_sha256: 14679088F474C76C908DABA44E7C7F80F95EA98D4E4E20F49326EACD7A04A501 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

large = x.mean() + 3 * x.std{)

return (x < small) | (x> large)
yczhi = data0.agg({lambda x: box(x))
yczhi_index = dataO[{yczhi.sum({axis = 1) > 100)].index
yczhi_index
data0.drop(yczhi_index, axis = 0, inplace = True)
data0.shape
PlotSpectrum(data0，' 附 件 一 光谱 数据 曲线 图 ')
data_corr = data0.corr()
data_corr
data_std = data0.std()
print{data_std.min(), data_std.max())
(data_std<0.05).sum()
max_min = data0.agg(lambda x: x.max() - x.min())
print{max_min.describe())
datal = data0.loc[:,max_min > max_min.mean() + 0 * max_min.std()]
datal.shape
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(datal)
data2 = scaler.transform(datal)
data2 = pd.DataFrame(datal, index = datal.index)
PlotSpectrum(data1，' 附 件 一 光谱 标准 化 处 理 后 数据 曲线 图 '
from sklearn.manifold import lsomap
isomap = lsomap(n_components = 3).fit(datal)
data2 = isomap.transform{datal)
print{data2.shape)
plt.figure()
plt.scatter(data2[:,0], data2[;,1])
plt.show()
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
scores= []
forn_clusters in range(2, 8):

cluster= KMeans(n_clusters = n_clusters, random_state = 0).fit{datal)

23

## Logical image page 24

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 24 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E24.jpg -->
<!-- source_image_sha256: 2BFD24111AED28AE368177F623C7163D481CB4168AD26D83EF99D2426BE9A1A6 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

score = silhouette_score{datal, cluster.labels_)

scores.append(score)
print(scores)
plt.figure( 育 类 数量 的 轮廓 系数 )
plt.plot{range(2, 8), scores, '-0')
plt.show()
cluster = KMeans{n_clusters = 3).fit{datal)
pd.Series(cluster.labels_).value_counts().sort_index()
plt.figure()
plt.scatter(data2[:,0], data2[:1], c = cluster.labels_)
plt.show()
colors = {A":'r, 'B 'g!, 'C: 'b!, De
colors=['r', 'g", 'b']
plt.figure(' 附件 一 分 类 图 ,figsize = (5, 3) dpi = 300)
plt.xticks(range(0, 10000, 1000), rotation = 45, fontsize = 5)
plt.yticks(fontsize = 5)
plt.xlabel( 波 段 , fontsize = 5)
plt.ylabel(' 吸 光度 , fontsize = 5)
foriin range(data0.shape[0]):

plt.plot{data0.columns, data0.ilocli,:], ¢ = colors[cluster.labels_[i]], linewidth = 0.5)
plt.grid(True)
plt.show()
二 、 问 题 二 Python 源 代码
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif] = ['SimHei'] # 用 来 正常 显示 中 文 标签
plt.rcParams['axes.unicode_minus'] = False # 用 来 正常 显示 负 号
data0 = pd.read_csv(P./ 附 件 / 附 件 2.csv, index_col = 0)
data0.shape
data0.head()
data0.describe([0.01, 0.25, 0.75, 0.99]).T
data0.info()
data0.iloc[:, 1:].isnull{).any().any()

24

## Logical image page 25

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 25 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E25.jpg -->
<!-- source_image_sha256: F91E705833B631A1250F834B4F35A4C7E1A919D6312A1113BA3A057B90DBDC9A -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

data0.iloc[:,0].isnull().sum()
data0.iloc[:,0].value_counts().sort_index()
data_X = data0.iloc[:,1:]
print{data_X.shape)
data_X = pd.DataFrame(data_X.iloc[:,1:].values - data_X.iloc[:,:-1].values, index = data0.index)
print{data_X.shape)
print{data_X)
data_y = data0.iloc[:,0]
print{data_X.shape, data_y.shape)
printff 缺失 值 个 数 : {data_y.isnull().sum()}1~")
data_y.fillna(0, inplace = True)  # 暂时 用 0 填充 缺失 值
print(f 缺 失 值 个 数 : {(data_y == 0).sum()} 个 ))
# 转换 为 整数
data_y = data_y.astype('int')
# 保留 缺失 值 的 索引 号
gsz_index = data_y[data_y == 0].index
gsz_index
def my_plot(x):
plt.plot{x.index, x.values, linewidth = 0.5)
def PlotSpectrum(data, str0):
fontsize = 5
pltfigure(stro, figsize = (5, 3) dpi = 300)
plt.xticks(range(0, 4001, 500), rotation = 45, fontsize = 5)
plt.yticks(fontsize = fontsize)
plt.xlabel( 波 段 , fontsize = 6)
plt.ylabel(' 吸 光度 ,fontsize = 6)
plt.grid{True)
data.agg({lambda x: my_plot(x), axis = 1)
plt.show()
Plotspectrum(data0.iloc[:,1:]，' 附 件 二 光谱 数据 曲线 图 ')
PlotSpectrum(data_X, ' 附 件 二 一 阶 平滑 后 数据 曲线 图 '
max_min = data_X.agg(lambda x: x.max() - x.min())
print{max_min.describe())
datal = data_X.loc[:,max_min > max_min.mean() + 0 * max_min.std({)]
# datal = data_X
print{data_X.shape, datal.shape)
25

## Logical image page 26

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 26 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E26.jpg -->
<!-- source_image_sha256: 91148C779357A740E07F9B2ADC88752C83FC66B3FC16927C84472F1B9CEA8019 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

data_X_know = datal.drop{gsz_index)
data_X_unknow = datal.loc[gsz_index,:]
print{data_X_know.index, "\n', data_X_unknow.index)
data_y_know = data_y.drop{gsz_index)
print{data_X_know.shape, data_y_know.shape, data_X_unknow.shape)
test = pd.concat{[data_y_know, data_X_know],axis = 1)
test.shape
from scipy.spatial import distance_matrix
dis = pd.DataFrame(distance_matrix(data_X_know.values, data_X_unknow.values), index =
data_X_know.index, columns = data_X_unknow.index)
dis_group = pd.concat{[data_y_know, dis], axis = 1)
print(dis_group.shape)
print{dis_group.columns)
print(dis_group)
min_index = dis_group.idxmin()
print{min_index)
[*zip{gsz_index, dis_group.loc[min_index[1:], 'OP'])]
dis_groupby = dis_group.groupby('OP').mean()
dis_groupby
by_min_index = dis_groupby.idxmin()
print{by_min_index)
dis = pd.DataFrame(distance_matrix(data_X_know.values, data_X_know.values), index =
data_X_know.index, columns = data_X_know.index)
dis_group = pd.concat{[data_y_know, dis], axis = 1)
print(dis_group.shape)
print{dis_group.columns)
print(dis_group)
OP_index = [0foriin range(12)]
foriin range(1, 12):

OP_index[i] = dis_group[dis_group['OP'] ==i].index
OP_index
dis = pd.DataFrame(distance_matrix(data_X_know.loc[OP_index[1],:].values,
data_X_know.loc[OP_index[1],:].values)).mean().mean()
print(dis)
dis = pd.DataFrame(distance_matrix(data_X_know.loc[OP_index[1],:].values,
data_X_know.loc[OP_index[2],:].values)).mean{).mean()

26

## Logical image page 27

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 27 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E27.jpg -->
<!-- source_image_sha256: BAD2D975E86A72F91CCDB56B2F38A0E5BA88B37CAFA59668D0C929B1781D999C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

dis
dis_g = pd.DataFrame(np.zeros([11,11]), index = range(1, 12), columns = range(1, 12))
foriin range(1, 12):

forjin range(1, 12):

dis_g.loc[i, j] = pd.DataFrame(distance_matrix(data_X_know.loc[OP_index][i],:].values,
data_X_know.loc[OP_index[j],:].values)).mean().mean()
dis_g
dis_g.idxmin()
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
print{data_X.shape)
best_LLE_clf_n_components, best_LLE_clf_n_neighbors = 35, 70
best_params_={'C': 2.438775510204082, 'gamma': 18.420699693267164}
print({f'n_components 二 {best_LLE_clf_n_components}， n_neighbors =
{best_LLE_clf_n_neighbors}')
# print(f'best_params_ = {grid.best_params_}')
lle = LocallyLinearEmbedding(n_components = best_LLE_clf_n_components
, n_neighbors = best_LLE_clf_n_neighbors
, method = 'modified').fit(datal) # LLE 降 维
data_X_lle = lle.transform({datal) # 获取 降 维 后 的 数据
data_X_lle = pd.DataFrame(data_X_lle) # 转换 为 DataFrame
data_y = pd.Series(data_y) # 转换 为 Series
# 将 未 分 类 数据 剥离
data_X_lle_know = data_X_lle.drop(qsz_index, axis = 0) # 删除 未 分 类 的 行
data_X_lle_unknow = data_X_lle.loc[qsz_index, :] # 取出 未 分 类 的 行
print{data_X_lle_know.shape, data_X_lle_unknow.shape, data_y_know.shape)
# cf = SVC(C = best_params_['C'], kernel = 'rbf, gamma = best_params_['gamma'],
decision_function_shape ='ovr', cache_size = 5000 # MB
# )
# cvs = cross_val_score(clf, data_X_lle_know, data_y_know, cv = 10)
# print(f 预 测 平均 准确 率 : {cvs.mean()})
Xtrain, Xtest, Ytrain, Ytest = train_test_split{data_X_lle_know, data_y_know, test_size = 0.3) #
分 离 出 测试 集 和 训练 集
cf = SVC(C = best_params_['C'], kernel = rrbf，gamma = best_params_['gamma'],
decision_function_shape ='ovr', cache_size = 5000 # MB
).fit{Xtrain, Ytrain)
score_r = clf.score(Xtest, Ytest)
print{score_r)
27

## Logical image page 28

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 28 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E28.jpg -->
<!-- source_image_sha256: B5E6F37E2F54837E9C3E11380713BC7AFBF3C041855121B2AD395E18AAFDC075 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

clf = clf.fit{data_X_lle_know, data_y_know)
print{clf.score{data_X_lle_know, data_y_know))
print{clf.predict{data_X_lle_unknow))
三 、 问 题 三 Python 源 代 码
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif] = ['SimHei'] # 用 来 正常 显示 中 文 标签
plt.rcParams['axes.unicode_minus'] = False # 用 来 正常 显示 负 号
datal = pd.read_csv(P./ 附 件 /附件 3 中 红外 .csv, index_col= 0)
data2 = pd.read_csv(r./ 附 件 /附件 3 近 红 外 .csv, index_col= 0)
print(data1.shape, data2.shape)
datal.head()
Data2.head()
print{datal['OP'L.isnull{).any{), data2['OP'Lisnull{).any{))
print{datal['OP'Lisnull{).sum({), data2['OP'].isnull{).sum())
print{datal[datal['OP'l.isnull{)].index, \n', data2[data2['OP'].isnull{)].index)
gsz_index = datal[datal['OP"].isnull{)].index
all{datal['OP'].drop{gsz_index) == data2['OP'].drop{gsz_index))
datal.describe([0.01, 0.25, 0.75, 0.99]).T
data2.describe([0.01, 0.25, 0.75, 0.99]).T
datal.info()
data2.info()
datal.iloc[:, 1:1.isnull{).any().any()
data2.iloc[:,1:].isnull{).any{).any()
datal['OP'].fillna(0, inplace = True)
datal['OP'] = datal['OP'].astype('int')
datal['OP'].value_counts{).sort_index{)

28

## Logical image page 29

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 29 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E29.jpg -->
<!-- source_image_sha256: 536D06B1C8A695F58B944706EA46BA6B42524D28D2E8D71C2CD6B7E97BFD7777 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

print{datal.index, \n', data2.index)
print{datal.columns, \n', data2.columns)
data0 = pd.concat{[datal, data2.iloc[:,1:]], axis = 1)
data0.shape
data0.head()
data_X = data0.iloc[:,1:]
data_y = data0.iloc[:,0]
print{data_X.shape, data_y.shape)
printff 缺失 值 个 数 : {data_y.isnull().sum()}1~")
data_y.fillna(0, inplace = True)  # 暂时 用 0 填充 缺失 值
print(f 缺 失 值 个 数 : {(data_y == 0).sum()} 个 ))
# 转换 为 整数
data_y = data_y.astype('int')
# 保留 缺失 值 的 索引 号
gsz_index = data_y[data_y == 0].index
data_y_unknow = pd.Series([17, 11, 1, 2, 16, 3, 4, 10, 9, 14], index = gsz_index, )
print{gsz_index)
def my_plot(x):
plt.plot{x.index, x.values, linewidth = 0.5)
def PlotSpectrum(data, str0):
plt.figure(stro, figsize = (4, 2.5), dpi = 300)
plt.xticks(range(0, 10001, 500), rotation = 45, fontsize = 5)
plt.yticks(fontsize = 5)
plt.xlabel( 波 段 , fontsize = 6)
plt.ylabel(" 吸 光度 , fontsize = 6)
plt.grid{True)
data.agg({lambda x: my_plot(x), axis = 1)
plt.show()
PlotSpectrum(data_X, ' 附 件 3 光谱 数据 曲线 图
Plotspectrum(datal.iloc[:,1:]，' 附 件 3 光谱 数据 曲线 图 '
Plotspectrum(data2.iloc[:,1:]，' 附 件 3 光谱 数据 曲线 图
max_min = data_X.agg(lambda x: x.max() - x.min())
print{max_min.describe())
data_jw = data_X.loc[:,max_min > max_min.mean() + 0 * max_min.std{)]
29

## Logical image page 30

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 30 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E30.jpg -->
<!-- source_image_sha256: C43A0FE4D68286226E50AB12D3707334ED33CE52B807C15A133D3C6B9D6D755C -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

# datal = data_X

print(data_X.shape, data_jw.shape)

data_X_know = data_jw.loc[index_14,:]

data_X_unknow = data_jw.loc[gsz_index,:]

print{data_X_know.index, "\n', data_X_unknow.index)

data_y_know = data_y.drop{gsz_index)

print{data_X_know.shape, data_y_know.shape, data_X_unknow.shape)

test = pd.concat{[data_y_know, data_X_know],axis = 1)

test.shape

from scipy.spatial import distance_matrix

dis = pd.DataFrame(distance_matrix(data_X_know.values, data_X_unknow.values), index =

data_X_know.index, columns = data_X_unknow.index)

# np.linalg.norm({np.array(data_X_know([0,:]))

dis_group = pd.concat{[data_y_know, dis], axis = 1)

print(dis_group.shape)

print{dis_group.columns)

print(dis_group)

min_index = dis_group.idxmin()

print{min_index)

[*zip(gsz_index, dis_group.loc[min_index[1:], 'OP'])]

dis_groupby = dis_group.groupby('OP').mean()

dis_groupby

by_min_index = dis_groupby.idxmin()

print{by_min_index)

data3_X = pd.DataFrame(datal.iloc[:,2:].values - datal.iloc[:,1:-1].values, index = datal.index)

datad_X = pd.DataFrame(data2.iloc[:,2:].values - data2.iloc[:,1:-1].values, index = data2.index)

print{data3_X.shape, data4_X.shape)

print(all{data3_X.index == datad_X.index))

print{data3_X.columns, data4_X.columns)

max_min3 = data3_X.agg(lambda x: x.max() - x.min())

print{max_min3.describe())

data3_jw = data3_X.loc[:,max_min3 > max_min3.mean() + 0 * max_min3.std()]

print{data3_X.shape, data3_jw.shape)

max_min4 = data4_X.agg(lambda x: x.max() - x.min(})

print{max_mind.describe())

datad_jw = datad_X.loc[:,max_min4 > max_min4.mean() + 0 * max_mind.std()]
30

## Logical image page 31

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 31 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E31.jpg -->
<!-- source_image_sha256: 38C857B933FF9A131D9CDC2579E281E898A071B5D41C4E093476710FFA54FFB5 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

print{datad_X.shape, data4_jw.shape)

data3_X_know = data3_jw.loc[index_14,:]

data3_X_unknow = data3_jw.loc[gsz_index,]

print{data3_X_know.index, "\n', data3_X_unknow.index)

data3_y_know = data_y.drop(gsz_index)

print{data3_X_know.shape, data3_y_know.shape, data3_X_unknow.shape)

print{data3_X_know, data3_X_unknow)

datad_X_know = datad_jw.loc[index_14,:]

datad_X_unknow = data4_jw.loc[gsz_index,:]

print{datad_X_know.index, "\n', datad_X_unknow.index)

datad_y_know = data_y.drop(gsz_index)

print{datad_X_know.shape, data4_y_know.shape, datad_X_unknow.shape)

from scipy.spatial import distance_matrix

dis3 = pd.DataFrame(distance_matrix(data3_X_know.values, data3_X_unknow.alues), index =

data3_X_know.index, columns = data3_X_unknow.index)

dis3_group = pd.concat([data3_y_know, dis3], axis = 1)

print{dis3_group.shape)

print{dis3_group.columns)

print({dis3_group)

dis4 = pd.DataFrame(distance_matrix(datad_X_know.values, data4_X_unknow.values), index =

datad_X_know.index, columns = datad_X_unknow.index)

dis4_group = pd.concat{[datad_y_know, dis4], axis = 1)

print{dis4_group.shape)

print({dis4_group.columns)

print(dis4_group)

print{dis3_group.shape, type(dis3_group))

min_index3 = dis3_group.idxmin()

print{min_index3)

print{[*zip{gsz_index, dis3_group.loc[min_index3[1:], 'OP'])])

min_index4 = dis4_group.idxmin()

print{min_index4)

print{[*zip{gsz_index, dis4_group.loc[min_index4[1:], 'OP'])])

四 、 问 题 四 Python 源 代码

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif] = ['SimHei'] # 用 来 正常 显示 中 文 标签
31

## Logical image page 32

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 32 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E32.jpg -->
<!-- source_image_sha256: A669FD2514FB243418E12268B2890A33308AD57E14F952377B76D247569EFBD8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

plt.rcParams['axes.unicode_minus'] = False # 用 来 正常 显示 负 号
data0 = pd.read_csv(r./ 附 件 / 附 件 4.csv', index_col = 0)
data0.shape
data0.head()
print{dataO['OP"].isnull{).any(), data0['Class'].isnull().any())
data0.describe([0.01, 0.25, 0.75, 0.99]).T
data0.info()
data0.iloc[:,2:].isnull{).any().any()
data0.iloc[:,0].value_counts().sort_index()
data0.iloc[:,1].value_counts().sort_index()
print{dataO['OP"].isnull{).sum(), dataO['Class'].isnull{).sum())
OP_null_index = dataO[data0['OP'].isnull{)].index
Class_null_index = dataO[data0['Class'].isnull{)].index
print{OP_null_index, '\n', Class_null_index)
public_index = []
foriin OP_null_index:

if i in Class_null_index:

public_index.append(i)

public_index
def my_plot(x):

plt.plot{x.index, x.values, linewidth = 0.5)
def PlotSpectrum(data, str0):

fontsize = 5

plt.figure(stro, figsize = (5, 3), dpi = 300)

plt.xticks(range(0, 8001, 500), rotation = 45, fontsize = 5)

plt.yticks(fontsize = fontsize)

plt.xlabel( 波 段 , fontsize = 6)

plt.ylabel( 吸 光度 fontsize = 6)

plt.grid{True)

data.agg(lambda x: my_plot(x), axis = 1)

plt.show()
Plotspectrum(data0.iloc[:,2:]，' 附 件 四 光谱 数据 曲线 图

32

## Logical image page 33

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 33 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E33.jpg -->
<!-- source_image_sha256: 6632FC95230A0226C6EE1104DA7FC9BADC53830917CBCCB5AECFD040911B030A -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

data0['Class'].fillna('D', inplace = True)
data0['OP'].fillina(o, inplace = True)
data0
Colors ={'A":'r','B": 'g','C":'b', 'D' : 'y'}
plt.figuref' 附 件 四 Class', figsize = (5, 3), dpi = 300)
plt.xticks{range(0, 10000, 1000), rotation = 45, fontsize = 5)
plt.yticks(fontsize = 5)
plt.xlabel( 波 段 ,fontsize = 5)
plt.ylabel(' 吸 光度 , fontsize = 5)
foriin range(data0.shape[0]):

if data0.iloc[i,0] !='D':

plt.plot{data0.columns([2:], data0.iloc[i,2:], ¢ = colors[data0.iloc[i,0]], linewidth = 0.5)

plt.grid(True)
plt.show()
colors ={'A":'r','B": 'g','C":'b', 'D' : 'y'}
plt.figuref' 附 件 四 Class', figsize = (5, 3), dpi = 300)
plt.xticks{range(0, 10000, 1000), rotation = 45, fontsize = 5)
plt.yticks(fontsize = 5)
plt.xlabel( 波 段 ,fontsize = 5)
plt.ylabel(' 吸 光度 , fontsize = 5)
foriin range(data0.shape[0]):

if data0.iloc[i,0] == 'B' or data0.iloc[i,0] =='C":

plt.plot{data0.columns([2:], data0.iloc[i,2:], ¢ = colors[data0.iloc[i,0]], linewidth = 0.5)
plt.grid(True)
plt.show()
data_X = dataBCD.iloc[:, 2:]
data_Class = dataBCD.iloc[:, 0]
max_min = data_X.agg(lambda x: x.max() - x.min())
print{max_min.describe())
datal = data_X.loc[:,max_min > max_min.mean() + 0 * max_min.std({)]
print{data_X.shape, datal.shape)
datal
data_Class_know = datal.drop(BC_index)
data_Class_unknow = datal.loc[BC_index,:]
print{data_Class_know.index, "\n', data_Class_unknow.index)
from scipy.spatial import distance_matrix
dis_C = pd.DataFrame(distance_matrix(data_Class_know.values, data_Class_unknow.values),
33

## Logical image page 34

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 34 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E34.jpg -->
<!-- source_image_sha256: 9FBF9DA09265EFFE36D2E97333806673E431CA9344AFE2390D0AE1308CCADA1D -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

index = data_Class_know.index, columns = data_Class_unknow.index)
dis_Cgroup = pd.concat([data_Class, dis_C], axis = 1)
print(dis_Cgroup.shape)
print(dis_Cgroup.columns)
print(dis_Cgroup)
min_Cindex = dis_Cgroup.iloc[:,1:].idxmin()
print{min_Cindex)
[*zip(BC_index, dis_Cgroup.loc[min_Cindex[1:], 'Class'])]
from sklearn.manifold import LocallyLinearEmbedding
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
print{dataBCD.shape)
best_LLE_clf_n_components, best_LLE_clf_n_neighbors = 20, 40
best_params_={'C": 2.438775510204082, ' gamma': 18.420699693267164}
print({f'n_components = {best_LLE_clf_n_components}, n_neighbors =
{best_LLE_clf_n_neighbors}')
# print(f'best_params_ = {grid.best_params_}')
lle = LocallyLinearEmbedding(n_components = best_LLE_clf_n_components
, n_neighbors = best_LLE_clf_n_neighbors
, method = 'modified').fit{(dataBCD.iloc[;,2:]) #LLE 降 维
dataBCD_lle = lle.transform(dataBCD.iloc[:,2:]) # 获取 降 维 后 的 数据
dataBCD_lle = pd.DataFrame(dataBCD_lle, index = dataBCD.index) #
转换 为 DataFrame
print{dataBCD_lle)
X_know = dataBCD_lle[{dataBCD['Class'] == 'B') | {dataBCD['Class'] =="'C')]
X_unknow = dataBCD_lle[{dataBCD]['Class'] == 'D')]
y_know = dataBCD.loc[{dataBCD['Class'] =='B') | (dataBCD['Class'] =='C'),'Class']
print{(X_know.shape, X_unknow.shape, y_know.shape)
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X_know, y_know, test_size = 0.3) # 分 离 出 测试
集 和 训练 集
cf = SVC(C = best_params_['C'], kernel = rrbf，gamma = best_params_['gamma'],
decision_function_shape = 'ovr', cache_size = 5000 # MB
).fit(Xtrain, Ytrain)
score_r = clf.score(Xtest, Ytest)
print(score_r)
clf = clf-fit{X_know, y_know)
print{clf.score(X_know, y_knowy))
print{clf.predict{X_unknow))
resBC = [*zip(BC_index, clf.predict{(X_unknow))]
34

## Logical image page 35

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 35 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E35.jpg -->
<!-- source_image_sha256: DCD79A2AA219FF50DEA79E492E2B4A03512B2CF8F318C8F6CDFBEF2D49A1D947 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

resB, resC=1], []
foriin resBC:

ifi[1] =='B":

resB.append(i[0])
else:
resC.append(i[0])

print{resBC)
print(resB, len{resB))
print({resC, len{resC))
colors = ["r", "g", "b", "c", "m", "y", "navy", "purple", "gold", "gray", "orange", "lime", "pink",
"tomato", "khaki", "azure", "linen", "rose", |
plt.figure(' 附 件 四 Class', figsize = (5, 3), dpi = 300)
plt.xticks(range(0, 10000, 1000), rotation = 45, fontsize = 5)
plt.yticks({fontsize = 5)
plt.xlabel( 波 段 ,fontsize = 5)
plt.ylabel(' 吸 光度 , fontsize = 5)
plt.grid(True)
fori in range(data0.shape[0]):

plt.plot{data0.columns[2:], data0.iloc[i,2:], color = colors[int{data0.ilocli,1])], linewidth = 0.5)
plt.show()
best_LLE_clf_n_components, best_LLE_clf_n_neighbors = 20, 40
best_params_={'C': 2.438775510204082, 'gamma': 18.420699693267164}
print(f'n_components = {best_LLE_clf_n_components}, n_neighbors =
{best_LLE_clf_n_neighbors}')
# print(f'best_params_ = {grid.best_params_}')
lle = LocallyLinearEmbedding(n_components = best_LLE_clf_n_components

, n_neighbors = best_LLE_clf_n_neighbors
, method ='modified').fit{(dataBCD.iloc[;,2:])  # LLE 降 维
dataBCD_lle = lle.transform(dataBCD.iloc[:,2:]) # 获取 降 维 后 的 数据
dataBCD_lle = pd.DataFrame(dataBCD_lle, index = dataBCD.index) #
转换 为 DataFrame
print{dataBCD_lle)
X_know = dataBCD_lle[{(dataBCD['Class'] == 'B') | (dataBCD['Class'] =="'C')]
X_unknow = dataBCD_lle[(dataBCD['Class'] == 'D')]
y_know = dataBCD.loc[{dataBCD['Class'] =='B') | (dataBCD['Class'] == 'C'),'Class']
print{(X_know.shape, X_unknow.shape, y_know.shape)
Xtrain, Xtest, Ytrain, Ytest = train_test_split{X_know, y_know, test_size = 0.3) # 分 离 出 测试
集 和 训练 集
cf = SVC(C = best_params_['C'], kernel = rrbf，gamma = best_params_['gamma'],
decision_function_shape ='ovr', cache_size = 5000 # MB
).fit(Xtrain, Ytrain)
35

## Logical image page 36

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 36 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E36.jpg -->
<!-- source_image_sha256: 5F365D6F87EAF9792442D23229D8DDBAB486C3E00E9A2A3F0785073134B6B0F5 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

score_r = clf.score(Xtest, Ytest)
print(score_r)
clf = clf-fit{X_know, y_know)
print{clf.score(X_know, y_knowy))
print{clf.predict{X_unknow))
[*zip(BC_index, clf.predict(X_unknow))]
dataO['OP'] = dataO['OP'].astype(int)
data0
data_X = pd.DataFrame(data0.iloc[:,3:].values - data0.iloc[:,2:-1].values, index = data0.index)
data_X
colors = ["r", "g", "b", "c", "m", "y", "navy", "purple", "gold", "gray", "orange", "lime", "pink",
"tomato", "khaki", "azure", "linen", "rose", |
plt.figure(' 附 件 四 Class', figsize = (5, 3), dpi = 300)
plt.xticks{range(0, 10000, 1000), rotation = 45, fontsize = 5)
plt.yticks(fontsize = 5)
plt.xlabel(' 波 段 ,fontsize = 5)
plt.ylabel(' 吸 光度 , fontsize = 5)
plt.grid(True)
fori in range(data_X.shape[0]):

plt.plot{data_X.columns[2:], data_X.iloc[i,2:], color = colors[int{data0.iloc[i,1])], linewidth =
0.5)
plt.show()
max_min = data_X.agg(lambda x: x.max() - x.min())
print{max_min.describe())
data_X1 = data_X.loc[:,max_min > max_min.mean() + 0 * max_min.std({)]
# datal = data_X
print{data_X.shape, data_X1.shape)
data_X_know = data_X1.loc[dataO['OP'] != 0]
data_X_unknow = data_X1.loc[data0['OP'] == 0]
print{data_X_know.shape, \n', data_X_unknow.shape)
print{data_X_know.index, "\n', data_X_unknow.index)
data_y_know = data0.loc[dataO['OP'] !=0, 'OP']
print{data_X_know.shape, data_y_know.shape, data_X_unknow.shape)
print{data_y_know.index)
from scipy.spatial import distance_matrix
dis = pd.DataFrame(distance_matrix(data_X_know.values, data_X_unknow.values), index =
data_X_know.index, columns = data_X_unknow.index)
dis_group = pd.concat{[data_y_know, dis], axis = 1)

36

## Logical image page 37

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 37 -->
<!-- source_image_path: 2021年数学建模国赛真题+优秀论文/2021年国赛优秀论文E题-E037/E37.jpg -->
<!-- source_image_sha256: 7919B121FDD74ADA78D492D6835C4C1AD241BDA1CBFA5C105D2F6E0ADA60388E -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

print(dis_group.shape)
print{dis_group.columns)
print(dis_group)
min_index = dis_group.idxmin()
print{min_index)
res = [*zip(OP_null_index, dis_group.loc[min_index[1:], 'OP")]
res
dictl = {i: [] foriin range(17)}
foriin range(len(res)):
dict1[res[i][1]].append(res[i][0])
foriin dictl.keys():
print(i, dict1[i], len{dict1[i]))
37
