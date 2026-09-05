# Extracted Paper

<!-- source_page_kind: image_sequence -->

## Logical image page 1

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 1 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122397.jpg -->
<!-- source_image_sha256: 91A05808CCE3A469785B84B91F738760A6A40CECE36A099CE98E034F29E2FF1F -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

基于 成 分 数据 分 析 的 玻璃 制品 分 析 与 分 类
摘 要

玻璃 是 人 类 最 早 批发 明 的 人 造 材料 之 一 ， 古 代 玻璃 除 少数 天 然 玻璃 外 ， 其 余 均 为 人
造 玻璃 。 虽 外 观 相似 ， 但 化 学 成 分 不 同 。 研 究 琉璃 制品 的 化 学 成 分 及 鉴别 对 古代 玻璃 文
物 的 保护 具有 重要 意义 。 本 文 从 成 分 数据 分 析 视角 出 发 ， 对 玻璃 的 化 学 成 分 进行 分 析 ，
并 对 不 同类 型 的 玻璃 进行 分 类 及 预测 。

首先 对 附件 表单 中 数据 进行 预 处理 。 表单 1 数据 按照 众 数 以 及 热 卡 填充 进行 缺失 值
播 补 。 由 于 玻璃 制品 的 化 学 成 分 属于 成 分 数据 ， 但 因 检测 手段 等 原因 可 能 导致 其 成 分 比
例 的 累加 和 非 1009%6， 另 外 很 多 成 分 检测 不 到 或 为 0 值 。 假 设 这 种 情况 是 由 于 仪器 精度
首先 或 四 舍 五 入 得 到 的 。 因 此 ， 选 用 乘法 葵 换 法 对 表单 2 和 3 中 空白 处 及 0 值 进行 插
补 ， 最 后 得 到 的 玻璃 化 学 成 分 数据 为 成 分 数据 。

对 于 问题 1, 首先 基于 spearman 相关 系数 以 及 卡 方 检验 分 析 玻璃 文物 表面 风化 与 类
型 纹饰、 颜色 的 关系 ， 结 果 均 表明 玻璃 文物 表面 风化 与 玻璃 类 型 有 关 ， 与 纹饰 、 颜 色
无 关 。 其次, 根据 成 分 数据 的 Aitchison 几何 结构 ,在 单 形 空间 分 别 计算 每 种 玻璃 风化 与
无 风化 的 化 学 成 分 均值 ， 结 果 表 明 高 锝 玻璃 风化 后 二 氧化 硅 占 比 增加 较 大 ， 氧 化 钾 显著
减少 ， 氧 化 钠 、 氧 化 铝 、 氧 化 铀 、 氧 化 钢 占 比 均 有 所 上 升 ; 铝 钢 玻 璃 风化 后 二 氧化 硅 古
比 降 低 , 氧化 铅 、 氧 化 钙 升 高 , 五 氧化 二 磷 降 低 。 最后, 以 玻璃 的 化 学 成 分 为 响应 变量 ，
纹饰 、 类 型 、 颜 色 与 表面 风化 为 自 变量 ， 构 建 Dirichlet 回归 模型 忆 进 而 根据 该 模型 预测
风化 点 风化 前 的 化 学 成 分 含量 ， 具 体 结果 见 支撑 材料 ，

对 于 问题 2， 首 先 分 析 高 钾 玻 璃 与 铅 钢 玻 璃 的 分 类 坑 很 ,基于 问题 1 结果 ， 选 择 表
面 风化 、 化 学 成 分 为 分 类 特征 ， 以 玻璃 类 型 为 类 别 。 由 于 化 学 成 分 为 成 分 数据 ， 因 此 对
化 学 成 分 做 对 称 对 数 比率 (clD) 变 换 。 末 用 决策 树 建立 分 类 模型 ， 以 氧化 铝 为 特征 进行 两
类 玻璃 分 类 ， 若 氧化 铅 值 大 于 1.5 则 为 铅 负 琉璃， 反之 为 高 锝 琉璃。 同时 建立 偏 最 小 二
乘 判 别 分 析 (PLS-DAJ;- 通 过 不 同 特征 的 投影 重要 性 ， 得 到 对 分 类 有 影响 的 特征 分 别 为 氧
化 铝 、 氧 化 钾 、 氧 化 钢 和 氧化 锡 。 两 种 方法 得 到 结果 一 致 。 其 次 ， 采 用 kmeans 聚 类 分
析 分 别 对 两 种 类 型 的 玻璃 进行 聚 类 ， 确 定 最 优 聚 类 个 数 都 为 3， 然后 基于 PLS-DA 对 每
种 玻璃 选择 合适 的 化 学 成 分 ， 结 果 为 高 钊 玻璃 以 氧化 钾 、 二 氧化 硅 、 氧 化 钙 、 氧 化 锡 和
氧化 领 为 分 类 特征 分 为 三 类 ， 铅 钢 玻 璃 以 五 氧化 二 磷 、 氧 化 钢 、 氧 化 钠 和 氧化 铁 为 分 类
特征 分 为 三 类 。

对 于 问题 3， 依 据 问题 2 构建 模型 对 未 知 类 别 的 玻璃 进行 划分 。 方 法 一 是 基于 决策
树 模型 ， 选 择 氧化 名 成 分 值 对 未 知 玻璃 进行 划分 。 方 法 二 是 对 表单 3 数据 做 elr 变换 ，
选择 氧化 铅 、 氧 化 鱼 、 氧 化 钢 和 氧化 锡 成 分 为 自 变量 ， 琉 璃 类 型 为 因 变 量 ， 建 立 偏 最 小
二 乘 回 归 (PLS)， 通 过 交叉 验证 法 选择 主 成 分 个 数 为 3， 通 过 预测 值 确定 玻璃 类 型 。 两 种
方法 得 到 的 结果 一 致 ，A1、A6、A7 为 高 钾 玻 璃 ，A2、A3、A4、A5、AS8 为 银 钢 玻 璃 。
进一步 结合 问题 2 中 两 类 玻璃 的 亚 类 划分 特征 ， 基 于 PLS 得 到 AL、A6、A7 都 是 高 钾
玻璃 的 同一 亚 类 , A2 和 A4 是 铅 钢 玻 璃 的 同一 亚 类 , A3 和 Ag8 是 铅 钢 玻 璃 的 同一 亚 类 ,
A5 是 铅 钢 玻 璃 的 另 一 亚 类 。

对 于 问题 4， 首 先 分 别 对 每 种 类 型 玻璃 的 化 学 成 分 计算 相关 系 歼 ， 观 察 和 分 析 相关
性 热力 图 。 然 后 对 两 类 玻璃 化 学 成 分 之 间 的 相关 系数 进行 配对 Wileoxon 检验 ， 结 果 为
两 类 玻璃 化 学 成 分 之 间 的 相关 关系 无 显著 差异 。
关键 词 ， 成 分 数据 ; 决策 树 ， 偏 最 小 二 乘 判 别 分 析 : 聚 类 分 析 : 相 关 分 析

J \

## Logical image page 2

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 2 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122399.jpg -->
<!-- source_image_sha256: 589996526EB80890EDE0AFE59A0D32286752B4AD0E9318853B386EB98ADEED67 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

一 、 问 题 重 述
玻璃 的 发 展 历史 悠久 ， 在 中 国 经 历 了 从 舶 来 品 到 自主 生产 的 过 程 ， 虽 外 观 相似 ， 但
化 学 成 分 不 同 023。 玻璃 主要 化 学 成 分 为 二 氧化 硅 ， 因 其 添加 的 助 焙 剂 不 同 ， 两 者 成 分 比
例 不 同 ， 其 可 分 为 铅 钢 玻璃 〈 助 烤 剂 主要 为 铅 矿 石 ) 与 高 钾 玻璃 〈 助 焙 剂 主要 为 草木 灰
等 含 钾 量 较 高 的 物质 ) 。
由
Wo
氧 人 硅 人 > 政史
稳定 剂
(石英 石 )
图 1 玻璃 制作 过 程
同时 ， 因 古代 玻璃 极 易 受 埋藏 环境 的 影响 产生 风化 ， 导 致 其 内 外 部 元 素 进 行 交 换 ，
成 分 比例 发 生变 化 ， 影 响 其 类 别 判断 。 现 有 已 完成 分 类 的 一 批 铅 钢 玻璃 与 高 钾 玻 璃 制品
的 相关 数据 ， 其 中 附件 表单 1 给 出 了 文物 的 基本 信息 ， 表 单 2 给 出 了 已 分 类 玻璃 文物 的
化 学 成 分 比例 ， 表 单 3 给 出 了 未 分 类 玻璃 文物 的 化 学 成 分 比例 =
本 文 基 以 上 信息 建立 数学 模型 解决 以 下 问题 :
间 题 1: 《1) 分 析 玻 璃 文物 表面 风化 情况 与 玻璃 类 型 沁 纹 饰 、 颜色 是 否 有 关 ; 《2)
以 玻璃 类 型 为 基础 ， 分 析 铅 钢 玻 璃 表面 有 风化 与 无 风化 的 化 学 成 分 的 统计 规律 与 高 钾 玻
璃 表面 有 风化 与 无 风化 的 化 学 成 分 的 统计 规律 : “〈3) 根据 附件 表单 2 数据 中 风化 点 的
检测 数据 ， 预 测 风化 点 未 风化 前 的 化 学 成 分 含量 。
问题 21) 节 据 表单 『 中 玻璃 的 基本 信息 与 表单 2 中 玻璃 检测 点 所 含 化 学 成 分
分 析 玻璃 如 何 进行 分 类 汪 〈2) 已 完成 分 类 的 两 种 玻璃 依据 合适 的 化 学 成 分 再 分 别 进行
更 进一步 的 分 类 ; 〈3) 分 析 分 类 的 合理 性 与 敏感 性 。
问题 3: 《1) 分 析 附件 表单 3 中 未 知 玻璃 类 型 的 化 学 成 分 ， 依 据 问题 2 中 得 出 的
分 类 规律 对 其 类 型 进行 鉴别 : 《2) 分 析 分 类 结果 的 敏感 性 -
问题 4 《〈1)》 分 析 两 种 类 型 的 玻璃 文物 样品 化 学 成 分 之 间 的 关联 关系 ; 〈2)》 比较
酚 种 类 型 的 化 学 成 分 之 间 关联 关系 的 差异 性 。
二 、 问 题 分 析
在 回答 问题 之 前 首先 对 附件 表单 中 数据 进行 预 处 理 。 表 单 1 数据 按照 众 数 以 及 热 卡
填充 进行 缺失 值 插 补 。 表 单 2 和 3 中 空白 处 及 0 值 ， 选 用 乘法 普 换 法 进行 插 补 ， 然 后 将
化 学 成 分 数据 转化 为 成 分 数据 B4。
2.1 问题 1
首先 基于 spearman 相关 系数 以 及 卡 方 检验 分 析 玻璃 文物 表面 风化 与 类 型 纹饰、 颜
色 的 关系 。 其 次 ,根据 成 分 数据 的 Aitchison 几何 结构 ， 在 单 形 空间 分 别 计算 每 种 玻璃 风
化 与 无 风化 的 化 学 成 分 均值 ， 再 通过 环形 图 进行 比较 分 析 。 最 后 ， 以 文物 的 化 学 成 分 为
R

## Logical image page 3

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 3 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122401.jpg -->
<!-- source_image_sha256: A3D0B73C077322935AB50C9D6A4D5E64EDC00CA0588B574AF2106BA5C89FFF36 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

响应 变量 ， 纹 饰 、 类 型 、 颜 色 与 表面 风化 为 自 变量 ， 构 建 Dirichlet 回归 模型 ， 进 而 根据
该 模型 预测 风化 点 风化 前 的 化 学 成 分 含量 。
2.2 问题 2
为 研究 高 睾 玻璃 与 铅 负 玻 璃 的 分 类 规律 ， 基 于 问题 1 的 结果 ， 选 择 玻璃 基本 信息 、
化 学 成 分 为 分 类 特征 ， 以 玻璃 类 型 为 类 别 。 由 于 化 学 成 分 为 成 分 数据 ， 因 此 对 化 学 成 分
做 对 称 对 数 比 率 (clD) 变 换 。 分 别 采 用 决策 树 和 偏 最 小 二 乘 判别 分 析 进行 分 类 ， 选 择 对 于
分 类 重要 的 特征 。 对 每 种 每 种 类 型 的 玻璃 的 亚 类 划分 ， 采 用 kmeans 育 类 分 析 分 别 对 两
种 类 型 的 玻璃 进行 聚 类 分 析 ， 然 后 基于 偏 最 小 二 乘 判 别 分 析 对 每 种 玻璃 选择 合适 的 化 学
成 分 。
23 问题 3
依据 问题 2 构建 的 模型 对 未 知 类 别 的 玻璃 文物 进行 类 别 划分 。 方 法 一 是 基于 决策 村
模型 ， 选 择 短 选 的 特征 对 未 知 和 玻璃 进行 划分 。 方 法 二 是 对 表单 3 数据 做 clr 变换 ， 选 择
偏 最 小 二 乘 判 别 分 析 筛 选 的 特征 为 自 变量 ， 玻 璃 类 型 为 因 变 量 ， 建 立 偏 最 小 二 乘 回 归 ，
通过 交叉 验证 法 确定 主 成 分 个 数 ， 通 过 预测 值 确定 琉璃 类 型
24 问题 4
对 于 每 种 琉璃 类 型 , 我 们 首先 采用 Pearson 相关 系数 分 析 化 学 成 分 之 间 的 相关 关系 ，
并 将 此 相关 性 以 热力 图 的 形式 进行 数据 可 视 化 展示 ， 进 而 通过 配对 Wileoxon 检验 确定
两 类 玻璃 化 学 成 分 之 间 的 相关 关系 有 无 显著 差异 -
三 、 模 型 假设
1 假设 化 学 成 分 指 采样 点 处 的 化 学 成 分 ;
2 假设 未 检测 到 的 化 学 成 分 的 原因 为 仪器 精度 受 限 , 故 暂时 将 化 学 成 分 缺失 值 记 为 0，
后 续 进行 播 补 处 理
3. 假设 检测 到 的 化 学 成 分 0 条 是 由 于 四 合 五 入 得 到 的 ， 后 续 进行 插 补 处 理 。
四 、 符 号 说 明
表 1: 符号 说 明
符号 信义
X 数据 集
c 成 分 数据 的 党 数 和 约束
ee EMTEAE
e 成 分 数据 入 的 第 j 个 部 分 对 应 的 探测 苑 轩
s 一 个 小 于 的 数
D 数据 集 分 为 D 个 部 个
js

## Logical image page 4

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 4 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122403.jpg -->
<!-- source_image_sha256: 44460834781126AC811A22F95C330DC3038DDA540F3F0E393D33DD787D1A27EC -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

五 、 数 据 预 处 理

5.1 附件 表单 1 数据 预 处 理

本 题 附 件 表单 1 给 出 了 玻璃 文物 编号 、 纹 饰 、 类 型 、 颜 色 、 表 面 风化 的 基本 信息 ，
由 于 数据 量 较 大 且 存 在 一 定 的 缺失 值 ， 故 对 所 给 数据 进行 预 处 理 弥补 缺失 值 ， 防 止 因 数
据 缺 失 对 后 续 建 模 产 生 不 利 影响 。

附件 表单 1 中 缺失 值 均 为 琉璃 文物 颜色 , 其 中 具有 铅 失 值 两 个 文物 的 其 他 信息 均 为
“和 八 饰 A、 表 面 风 化 、 铅 钢 "， 其 他 两 个 具有 缺失 值 的 文物 的 其 他 信息 均 为 "纹饰 C、 表 面
风化 、 铝 钢 "， 按 此 分 为 两 个 类 别 分 别 进 行 填补 。

在 所 给 文物 中 符合“ 纹饰 C、 表 面 风化 、 铅 钢 " 条 件 并 已 知 颜色 的 共 15 件 文物 ， 颜
色 分 布 如 下 :
ze

颜色 蓝 绿 线 蓝 线 绿 深 绿 紫
对 应 文物 编号 56，57 ”11，25，43，51，52，54 4 34. 36, 38, 39  08: 26

因数 据 为 定性 数据 ， 故 采用 热 卡 填充 弥补 缺失 值 。 对 15 件 文物 及 待 填充 的 303 S8
号 文物 的 化 学 成 分 进行 比较 ， 用 成 分 相似 的 文物 颜色 进行 填充 《一 件 文物 在 两 个 部 位
进行 采样 时 取 均 值 代 表 ， 在 一 个 部 位 和 严重 分 化 点 采样 时 按 15 2- 的 权重 计算 后 进行 代
表 , 在 一 个 部 位 和 未 分 化 点 采样 时 将 部 位 的 化 学 成 分 作为 代表 ) 经 比较 可 知 : 40 号 与 39
号 成 分 相似 ，58 号 与 11 号 成 分 相似 , 才 将 40 号 ” $8 号 文物 颜色 分 别 填充 为 深 绿 ， 浅
蓝 。

符合 “纹饰 A、 表 面 风化 $ 铅 负 " 条 件 并 已 知 颜色 的 共 9 件 文物 ， 颜 色 分 布 如 下 :
一 xmfm

颜色 、 时 蓝 绿 浅 昔

对 训 文 物 编号 . 50 四 02. 25, 29. 4 和， 43. 53

由 附件 表单 2 可 知 ，9 件 文物 中 有 6 件 文物 在 分 析 化 学 成 分 时 采样 点 为 未 风化 点 ，
所 得 到 的 成 分 含量 参考 性 较 低 ， 故 对 此 采用 众 数 进行 填补 ， 即 19、48 号 文物 颜色 填充
为 浅 蓝 。
5.2 附件 表单 2、3 数据 预 处 理
5.2.1 缺失 值 插 补

因 成 分 比例 累加 和 介 于 859%6 一 105%6 之 间 的 数据 视 为 有 效 数据 ， 故 将 各 成 分 比例 累
加 ， 得 到 无 效 数 据 为 "文物 15 号 、 文 物 17 号 "， 将 其 从 表单 中 去 除 。 表 单 2 和 3 中 出 现
的 空白 为 未 检测 到 该 成 分 。 假 设 因 仪器 精度 受 限 未 检测 到 成 分 ， 所 以 不 能 单纯 将 缺失 值
播 补 为 "0",， 可 看 作 近似 零 值 。 另 外 ,表单 2 和 3 中 有 0 值 ， 假设 是 由 于 四 合 五 入 得 到 ，
属于 近似 零 值 。 采 用 如 下 乘法 普 换 方法 对 近似 零 值 进行 揪 补 ， 具 体 过 程 为 :

考虑 成 分 数据 集

## Logical image page 5

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 5 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122405.jpg -->
<!-- source_image_sha256: 53D57FF0B8A9E1BEAA27FFFB6540061D028A126A9601AE278196AA7665901427 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

EE 3
[| 人 全 4
3
假定 成 分 数据 中 有 近似 零 值 , 近似 零 值 是 由 于 小 于 已 知 的 探测 范围 观测 不 到 而 产生
的 ， 且 不 同 成 分 数据 相同 部 分 对 应 的 探测 范围 是 相同 的 。 记 探测 范围 向 量 为
e= (aasenp】， 其 中 为 成 分 数据 集 X 的 第 j 个 部 分 对 应 的 探测 范围 。 后 提出 乘法
简单 赫 换 法 ，x 葵 换 后 的 数据 为
人 为 =0
玛 = ofi-Zant), 5>0
ee
其 中 态 为 一 个 小 于 er 的 数 ，e 为 成 分 数据 的 常数 和 约束 ， 即
Zm=e
通过 实验 发 现 ， 当 成 分 数据 集中 近似 零 值 比例 不 高 时 ，5 等 于 探测 范围 的 65% 时 可 以 最
小 化 协 方差 阵 的 扭曲 ， 即 品 = 0.65e, 。 记 附件 表单 2、3 中 空 自 处 所 在 列 的 最 小 值 为 临界
值 ， 并 将 其 乘 以 0.65， 得 到 插 补 值 。 (在 此 列 出 部 分 攻 补 信 ， 具 体 数 据 见 支撑 材料 )
未 4 表单 2 成 分 数据 揪 补 缺失 值 分
文物 采样 点 50: NaO Kao Sno， 50:
on 693300。 05275-， 99900 04517 03900
03 部位】 $7050 © 05287 51900 01520  oom7
03 部 售 2 人 7I00 05239 123700 01506 00720
57 254200  0s6  0024 01s13  0om4
s8 30300  05239  03400 01506  00720
RS: 表单 3 成 分 数据 揪 补 缺失 值 《 部 分 》
文物 编号 表面 风化 Si， Na  K© 区
Al 无 风化 784500 。 05277 。 00726 04517 05100
人 2 风化 377500 05298 。 00728 01523 。 00728
A3 无 风化 319500 。 05239 。 13600 01506  00720
Ad4 无 风化 354700 05240 。 07900 01507 | 00721
as 风化 642900 12000 。 03700 04900  00716
A6 风化 93170 05278 。 13500 0517 。 00726
A7 风化 908300 。 05281 09800 01518 01100
As 无 风化 511200 05248 02300 01509 22600
75%

## Logical image page 6

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 6 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122407.jpg -->
<!-- source_image_sha256: E5C568858038FAEB32502F00D8533C1C278F5FC01A78C1F2D48F09634BE961A4 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

5.2.2 成 分 数据 处 理
因 成 分 数据 相 加 需 为 100， 可 利用 相对 信息 对 数据 进一步 处 理 。 相 对 信息 指 的 是 成
分 数据 仅 有 的 信息 反映 在 成 分 间 的 比率 中 ， 每 个 成 分 的 绝对 数据 是 无 关 的 ， 如 果 成 分 数
据 的 每 个 成 分 乘 以 相同 的 正常 数 ， 则 成 分 间 的 比率 是 不 变 的 ， 因 此 成 分 数据 可 以 看 成 是
等 价 类 ， 这 个 类 里 面 的 成 分 数据 含有 相同 的 信息 ， 都 可 以 通过 适合 的 尺度 因子 表示 为 相
同 的 比例 向 量 。 这 可 进行 闭合 运算 ;
C(x)=C(x35,,%,) =| fada.to
(¥)=C(x ) 二 京 5
闭合 运算 就 是 对 初始 向 量 乘 以 合适 的 尺度 因子 ， 使 得 闭合 后 的 成 分 和 为 常数 K《 这 里 为
100) ， 对 于 任意 的 两 个 向 量 x ye 及 ” ， 如 果 C(z)j=C(y)， 则 x 和 y 是 成 分 等 价 的 四 。
故 将 每 个 玫 玉 文物 化 学 成 分 乘 以 相应 计算 出 的 因子 得 到 最 终 数 据 。 表 单 >、3 数据 处 理
结果 见 支撑 材料 。
六 、 模 型 建立 与 求解
6.1 问题 1
4.1.1 玻璃 表面 风化 与 纹饰 、 玻 璃 类 型 、 颜 色 的 相关 性 分 析
鉴于 以 上 分 析 ， 我 们 首先 进行 斯 皮尔 曼 相 关系 数 务 析 二 在 分 析 之 前 对 定性 数据 进行
韦 拟 变量 处 理 ， 见 表 4。 然 后 利用 SPSS 软件 分 别 对 绞 饰 ”玻璃 类 型 、 颜 色 与 文物 表面
风化 进行 spearman 相关 性 检验 ， 得 到 结果 见 表 $ 至 表 7。 结果 表明 纹饰 与 颜色 对 于 玻璃
表面 是 否 风化 无 相关 关系 玻璃 类 型 对 于 玻璃 表面 是 否 风化 存在 相关 关系 。
表 6: 虚拟 变 量 处 理
纹饰 颜色
A 1 浅 直 1
B 2 深蓝 2
C 3 蓝 绿 3
类 型 浅 绿 4
Ha 1 深 绿 5
高 钾 2 绿 6
表面 风化 #® 7
无 风化 0 黑 8
风化 1
表 7: 纹饰 与 表面 风化 相关 性
纹饰 表面 风化
纹饰 1.000 0.080
表面 风化 0.080 1.000
FeS

## Logical image page 7

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 7 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122409.jpg -->
<!-- source_image_sha256: 91100A778052C18235FE54E54856A57AAA8F85804D506DA4BB33991E07CEB0CF -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

表 8$: 玻璃 类 型 与 表面 风化 相关 性
玻璃 类 型 表面 风化
玻璃 类 型 1.000 -0301
表面 风化 -0301 1.000
 mooseswmeexe
颜色 表面 风化
颜色 1.000 0.088
表面 风化 0.088 1.000
其 次 ， 为 保证 结果 的 可 信 度 ， 我 们 同时 利用 了 卡 方 检验 对 数据 进行 了 分 析 ， 在 进行
分 析 之 前 对 数据 进行 了 频数 统计 ， 见 图 2 至 图 4:
机
°f |
本
可
。
nit p
se
图 2: 纹饰
由 图 2 可 知 ， 在 无 风化 与 风化 两 种 情况 下 ， 纹 饰 类 型 A、B、C 变化 差异 较 小 ， 故
可 初步 推断 表面 风化 与 纹饰 类 型 无 关 。
本
站
加
中
=ry 有
2
图 3: 玻璃 类 型
由 图 3 可 知 , 风化 与 无 风化 相 比 , 铅 铀 玻璃 类 型 占 比 增加 , 高 钾 玻 璃 类 型 占 比 减少 ,
且 增加 与 减少 幅度 较 大 ， 故 可 初步 推断 表 面 风化 与 玻璃 类 型 有 关 。
和

## Logical image page 8

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 8 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122411.jpg -->
<!-- source_image_sha256: D20DFC57A5720B88274434E7FDC07A5277892F92A02241455E05345CA380E54E -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

四
»
四
ao
s
Halam_&5.
WE mm gR WR B8 绿 KR
At 风化
图 4 颜色

由 图 4 可知 ,风化 与 无 风化 相 比 ， 各 种 颜色 变化 较 小 ， 故 可 初步 推断 表面 风化 与 颜
色 无 关 。

为 进一步 验证 推 电 是 否 合理 ， 利 用 SPSS 软件 进行 了 卡 方 检验 ， 结 果 见 表 10.
~ 表 10 卡 方 检验 结果
一 和 Gec

纹饰 0.085
玻璃 类 型 0024
颜色 0.325

因 只 有 玻璃 类 型 的 系数 小 于 0.05, EHMANEXMRMANAHELR, Aih5
颜色 的 系数 均 大 于 005， 故 纹饰 、 颜 色 与 文物 表面 风化 无 相关 关系 。
6.1. 2 不 同类 型 玻璃 表面 有 风化 与 无 风化 化 学 成 分 含量 的 统计 规律 分 析

此 问 运用 附件 表单 2 处 理 后 的 成 分 数据 进行 分 析 。 分 别 计算 出 属于 铅 钢 琉璃 的 无 风
化 与 风化 检测 吉 数据 均值 、 属 于 高 印 区 玉 的 无 风化 与 风化 检测 点 数据 均值 具体 计算 方
法 如 下 5

因 成 分 数据 为 几何 结构 ， 故 可 进行 扰动 运算 来 类 似 实数 空间 上 的 加 法 运算 。 对 于 任
意 成 分 数据 Y= (axoj ，》=( 吃 罗 ……sJo 厂 ESex 与 y 的 扰动 运算 定义 为 。

x@y=C(531.%5,. oo es?
故 可 进一步 计算 均值 。 其 可 运用 R 语言 进行 成 分 数据 均值 计算 ， 得 到 结果 如 下 表 :
表 11; 高 钙 玉 到 、 锅 包 玻 现 风 化 与 无 风化 均值
S0: Na Ka0 0， so)

高 钾 未 风化 749529 0.8818 72326 02110 0.1234

高 钾 风 化 93.6615 0.5268 03579 0.1515 0.0724

HERRAL 59.5046 1.3090 0.1851 01871 0.0953

HERIL 27.0317 0.7432 0.1502 0.2105 0.1745

为 更 直观 地 观察 化 学 成 分 变化 ， 作 出 下 图 :

8

## Logical image page 9

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 9 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122413.jpg -->
<!-- source_image_sha256: 3E3FFADB71ED6702ECDF7EDB1D88AEEABB44DB64A70FE1B8771AFEFE145382A9 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

\
)
es
图 5: 高 钾 玻璃 风化 前 后 化 学 成 分 对 比 ， 外 轿 为 风化 ， 内 团 为 无 风化
AR
LN
人
AN 2
aa
人
图 6 高 钾 玻璃 风化 前 后 化 学 对 比 《〈 未 含 Si02) ， 外 圈 为 风化 ， 内 图 为 无 风化
对 于 高 钾 玻 璃 ， 因 二 氧化 硅 占 比较 大 ， 图 5 不 能 很 好 地 体现 其 他 化 学 成 分 的 变化 ，
故 将 二 氧化 硅 去 掉 ， 单 独 制作 图 6 更 好 地 体现 其 他 化 学 成 分 占 比 变化 。 结 合 图 5 与 图 6
进行 分 析 , 风化 后 二 氧化 硅 占 比 增加 较 大 , 氧化 钾 显 著 减 少 , 氧化 销 、 氧 化 铝 、 氧 化 钢 、
氧化 钢 占 比 均 有 所 上 升 。

## Logical image page 10

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 10 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122415.jpg -->
<!-- source_image_sha256: 50C8BC752AA4C35BD0A32AFCBD2A15678DD8418376B50C4EE8690C54A5EFF296 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

¢ \
(1 ~
人
人
图 7， 铅 负 玻 璃 分 化 前 后 元 素 对 比 ， 外 圈 为 风化 ， 内 圈 为 无 风化
下
£p'4
\J
ao Me 和 汉
Ra
图 8: 铅 铀 玻璃 风化 前 后 元 素 对 比 〈 未 含 Si02) ， 外 圈 为 风化 ， 内 圈 为 无 风化
对 于 铅 饥 玻璃， 由 图 7 可 知 ， 无 风化 与 风化 相 比 ， 二 氧化 硅 占 比 降低 ， 氧 化 铅 的 占
比 升 高 二 同样 由 于 二 氧化 硅 占 比 较 大 影响 其 他 化 学 成 分 变化 的 分 析 ， 将 二 氧化 硅 去 除 得
到 图 8 可 分 析 得 出 氧化 钊 ， 五 氧化 二 磷 变 化 程度 较 大 ， 变 化 趋势 分 别 为 升 高 、 降 低 。
6.1.3 风化 前 化 学 成 分 预测
首先 对 附件 表单 1 中 的 数据 进行 取 虚 拟 变量 处 理 ， 见 上 表 4。 将 附件 表单 1 中 的 变
量 作为 自 变 量 ， 附 件 表单 2 中 的 化 学 变量 作为 因 变 量 ， 做 Dirichlet 回归 。 得 到 回归 模型
后 ， 将 自 变量 中 的 风化 〈1) 普 换 为 未 风化 〈0) ， 得 到 预测 部 分 结果 如 下 表 〈 因 预测 结
果 数 据 量 较 大 ， 故 此 处 只 写 出 了 部 分 预测 结果 ， 所 有 预测 结果 见 支撑 材料 ) 。
表 12: 预测 风化 前 的 化 学 成 分 含量 《部 分 )
文物 编号 SiO: NaxO KaO SnO: SO:
让
四 罗 有 有
2 T 机
站 MGn om
2 5
一

## Logical image page 11

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 11 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122417.jpg -->
<!-- source_image_sha256: F382A4F87363FC49A720C9E62CDCA05A18B72CADE94E935D121A61B63A9F02B3 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

.2 问题 2
2.1 防 玉 的 分 类 规律 分 析
在 进行 建 模 之 前 首先 要 对 成 分 数据 进行 ck 变换 ， 对 于 任意 成 分 数据
= (aa ap €57, clr 变换 将 xeS? 变 换 为 &2 上 的 系数 ，clr 系数 为
本
5 0 2
w 人 aa]
记 变换 后 数据 为 cr) =E= (和 ,名所 ， 则 cr 他 变 换 为
3=clr(@©)=C(exp(&).exp(8). exp (60))

用 转化 后 的 成 分 数据 建立 分 类 和 模型， 为 合 分 类 结果 直观 明了 ， 使 用 决策 树 模型 对 其
进行 特征 的 寺 择 与 分 类 ， 进 一 步 探 充 主 要 分 类 特征 从 而 推断 两 种 玻璃 的 分 类 规律 。 在 此
模型 中 ， 本 题 将 附件 表单 1 中 的 表面 风化 与 附件 表单 2 中 各 化 学 成 分 作为 分 类 特征 、 将
玻璃 的 类 型 作为 类 别 构建 决策 树 模 型 ， 且 将 67 个 样本 划分 为 训练 集 与 测试 集 两 类 ， 其
中 47 个 祥 本 为 训练 集 剩 余 则 为 测试 集 。 最 后 采用 有 语言 进行 软件 实现 ， 结 果 如 图 四
再 用 测试 集 数据 进行 顶 测 ， 正 确 率 为 10096-

| |
@a.=.08
图 9: 决策 禁 结果

从 该 图 中 可 知 ” BAURLE 〈PbO) 为 特征 进行 两 类 玻 瑞 分 类 ， 若 氧化 外 值 大 于
15 AARMER, R2ABHER.

下 面 采 用 偏 最 小 二 乘 判 别 分 析 进 行 高 钾 玻璃 和 铀 钢 玻 璃 的 分 类 。 由 于 or 变换 后 数
据 求 和 为 0, 以 琉 六 类 型 为 分 类 变量 风化 二 氧化 奈 (Sio)、 氧 化 钠 (NazO). 氧 化 钾 (KaO)、
氧化 后 (CaO)、 氧 化 镁 (MeO)、 氧 化 铝 (A1203) ,氧化 铁 (Fezo3) .氧化 钢 (CuO) .氧化 名 (PbO)、
氧化 钢 (BaO)、 五 氧化 二 玖 B209、 氧 人 锣 (SrO)、 氧化 锡 (SnO) 、 二 氧化 硫 (SOy 为 特征 变
量 , 建立 偏 最 小 二 乘 判别 分 析 。 由 图 10 可 知 , 高 钾 玻 璃 和 饮 负 琉 现 有 明显 的 分 离 趋势
由 图 11 可 知 ，Q2 左 侧 交 于 了 四 负 站 得 ， 说 明 模型 构建 成 功 -

Hi

## Logical image page 12

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 12 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122419.jpg -->
<!-- source_image_sha256: 6F93A321596CDD75C0F98D7BE4763979C34FBC11C2B9F867DC07232F161A4ED8 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

国 c
o 国 os
2 % o
1
二 0 二 人
Sa
ee .
2 ° °
3
&; 3
5
4 6 4 2 0 12 4 6
t+
图 10: 偏 最 小 二 乘 判 别 分 析 结果
4 or
家 A ee
we
06 2
区
04 2
o 晤 2
0 全 PT 一
La D
041 一 一 -~
-20 02 04 06 08 1
图 11， 偏 最 小 二 乘 判别 分 析 模型 验证
表 13;， 偏 最 小 二 乘 判 别 分 析 的 不 同 特征 的 VIP 值
变量 VIP 变量 VIP
风化 02098 Guo 0.5694
sio; 08907 Pho 4614
NaO 01208 Bao 13472
K0 1.800 P:0s 01226
Cag 0.5095 sr0 TH13
Meo 03871 $10; 03548
AboOs 06157 so; oa247
Fe:0; 07284
Ji

## Logical image page 13

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 13 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122421.jpg -->
<!-- source_image_sha256: B64B68AD926F2BA2DCAF1E61E57D7E9FFEF095C77081DE1D21EBE72C53D76FB2 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

计算 不 同 变量 的 投影 重要 性 (VIP) ， 结 果 见 表 10。 希 先 VIP 值 大 于 1 的 特征 ， 对
于 分 类 有 影响 的 特征 分 别 为 PbO、K2O、BaO 和 SrO。 上 面 图 表 结 果 是 在 simca 软件 抬
作 完 成 -
6.2.2 亚 类 划分 方法 结果 及 敏感 性 分 析
将 两 类 琉 吏 分 别 进行 更 进一步 亚 英 的 划分 ， 本 次 划分 并 不 知 亚 类 划分 的 结果 故 该 批
数据 并 未 有 明确 的 类 型 ， 因 此 该 类 问题 为 无 监 督学 习 问题 没有 已 知 的 因 变 量 ， 且 需 进行
分 类 所 以 选择 聚 类 分 析 模型 . 首先 需要 进行 选择 所 分 类 别 的 个 数 ， 我 们 采用 语言 中 的
friz_nbclust 函数 进 行 判断 ， 如 图 根据 其 间断 点 可 知 两 种 孩 殉 的 亚 分 类 最 终 均 选取 3 类 ;
»  Optimal number of clus Optimal number ofclus
§2001+ 8 70044
8 |\ 人
三 150 划 \
£ \ H 500{ *\
2 100 、 400] \
三 、 £ ss
三 s0 ss 三 300 ”1
2 3 夏 200 Se
此 12345678910 已 12345678910
Number of clusters k Numiber of clusters k
图 12， 高 鲜 分 类 个 数 确 定 加 13。 锁 栅 分 类 个 数 确定
其 次 ， 在 确定 票 区 不 孝 的 情况 下 用 K-means 进行 聚 类 .结果 如 图
Bivariate Cluster Plot Bivariate Cluster Plot
o o
j — 二 下 于
如 § Ce
时 一 起 pEpy
和 9 Ra 和 g >
3 8
4 20 2 -4 0 2 4
Component 1 Component 1
These two components e' These two components e:
图 14; 高 钙 梨 类 情况 图 15， 锁 领 划 类 清 况
分 析 运 行 结果 图 可 知 角钢 玻璃 可 被 明显 的 分 为 三 并 ， 故 其 亚 分 类 包含 三 类 ， BRK
玖 三 类 划分 并 未 有 非常 明显 的 类 别 ， 仅 可 粗略 将 其 分 为 三 区

## Logical image page 14

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 14 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122423.jpg -->
<!-- source_image_sha256: 3AD61A84E1C9451C5A954DEB7A6F93EAC0DC156AE208362141400B0BC407BF6B -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

表 14; 亚 分 类
残 璃 。 亚 分
类 型 ” 贡 文物 编号
% 06 部 位 1，18
到 由 四 四 四 季节
3 01, 03 部 位 1，03 部 位 2，04，05，06 部 位 2，13，14，16
1 20，37，50 未 风化 点 ，08，08 严重 风化 ，11，19，26，26 严重 风化 ，39，40,，
有 部 位 2，50，351 部 位 1，52，54，54 严重 风化 ，56，58
铅 钢 2 28 未 风化 点 ，29 未 风化 点 ，30 部 位 1，30 部 位 2，31，32，35，49 未 风化 点 ，
玻璃 02, 41, 48, 49, 51 部 位 2
23 未 风化 点 ，24，25 未 风化 点 ，33，42 未 风化 点 1，42 未 风化 点 2，44 未 风化
了 点 ，45，46， 和 4，53 未 风化 点 ，55，34，36，38，43 部 位 1，57
在 确定 分 类 个 数 时 ， 不 同 分 类 个 数 的 选择 会 使 得 聚 类 出 现 不 同 的 结果 ， 故 应 对 此 模
型 的 敏感 性 进行 分 析 。 因 高 钾 玻璃 并 未 有 明显 的 分 类 效果 ， 故 尝试 多 个 分 类 个 数 进行 聚
类 从 而 选择 出 较 优 的 聚 类 情况 。
下 面 对 每 类 玻璃 的 亚 类 划分 选择 合适 的 化 学 成 分 。
对 于 高 钾 玻 璃 ， 亚 类 划分 为 3 类 。 由 于 其 中 一 类 只 有 两 个 文物 玻璃 ， 因 此 删除 这 一
类 文物 ， 以 其 余 类 为 分 类 变量 ， 化 学 成 分 为 特征 汪 构 建 偏 景 小 二 乘 判 别 分 析 , 由 图 16 可
知 ， 高 钾 玻 璃 的 亚 类 有 明显 的 分 离 趋势 。 由 图 37 可 知 ”Q2 左 侧 交 于 下 轴 负 半 轴 ， 说 明
模型 构建 成 功 。
1 让
| 上
A .
AF 本
To . ee
" ee
2 -
|
+
图 16: 高 钾 玻 璃 亚 类 偏 最 小 二 乘 判别 分 析 结果
)

## Logical image page 15

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 15 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122425.jpg -->
<!-- source_image_sha256: 3A51E7F02B993DE9EBAAC35A5BA842A66849B9F3BAFCD581A8112B57915DA10B -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

1 ee
hb 着 砷 ee2
06 -一 2
:| 让
02 站 本
IPER
ai
4 上 -
CCC
图 17: 高 钾 到 璃 亚 类 偏 最 小 二 乘 判别 分 析 模型 验证
表 15， 高 钙 骇 璃 亚 类 偏 最 小 二 乘 判别 分 析 的 不 同 特征 的 VIP 值
变量 vie =R 加
Sio: 1.5267 Cuo 0.7509
ao oa815 Pbo 02088
oo 23016 Bao 12188
cao 13078 Poy 00160
MgO 0.0216 Sr0 0.4147
Abos 04654 3 1276
Faoy os3s So 03721

计算 不 同 变量 的 投影 重要 性 (VIP) ， 结 果 见 表 15. E VIP 值 大 于 1 的 特征 ， 对
于 高 钙 下 璃 亚 类 分 类 有 影响 的 特征 分 别 为 K0、SiOx、CaO、SnOy 和 BaO。 上 面 图 表 结
果 是 在 sinica 软件 操作 完成 。

刚 于 铅 贫 玻璃， 亚 类 划分 为 3 类 ， 以 这 3 类 为 分 类 变量 ， 化 学 成 分 为 特征 ， 构 建 信
最 小 二 乘 判 别 分 析 ， 由 图 18 可 知 ， 铅 饥 玻璃 的 三 类 有 明显 的 分 离 趋势 。 由 图 19 可 知 ，
Q2 左 侧 交 于 Y 轴 负 半 轴 ， 说 明 模 型 构建 成 功 -

4 时 co
4 5 |® o
: "ee m
1

到 CACETE
了 eg
-3 二 . =
|
s .
'$43240 12 5,2
4
图 18: 铅 负 玻璃 亚 类 信 最 小 二 乘 判别 分 析 结果
上

## Logical image page 16

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 16 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122427.jpg -->
<!-- source_image_sha256: 6BFA8BD605AFD1F6B955CCC8CD3FBD58B566B3B130ABC51CF8630FE13FB79734 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

os! ea
05 NI 可
有
03 四 Pea
o
oa =
H 地
全 一
.02 )
03
0 0102 03 04 05 06 0.7 08 0.9 1
图 19: 饥 钢 玻璃 亚 类 信 最 小 二 乘 判别 分 析 模型 验证
表 16; 锅 负 玻璃 亚 类 偏 最 小 二 乘 判别 分 析 的 不 同 特征 的 VIP 值
变量 VIP 交 量 证
sio: 09550 cwo 1
Nao 13046 Pho 0
Ko 0s82s Bao 08605
cao 066o6 Pios zs
Meo 7716 so .4435
Abo; saa9 noz 4663
Feoy 1all9 SG o7l93
计算 不 同 变量 的 投影 重要 性 《ViP)-， 结果 见 表 16。 得 选 VIP 值 大 于 1 的 特征 ， 对
于 铅 负 玻璃 亚 类 分 类 有 影响 的 特征 分 别 为 P:0s. CuO. NaxO 和 FeO。 上 面 图 表 结果 是
在 simea 软件 后 作 完 成 <
6.3 问 题 3
方法 一 ， 对 于 表单 3 中 未 知 玻璃 类 型 的 类 别 划分 ， 基 于 问题 2 决策 树 的 结果 ， 以
Pb 秀 特 征 进行 两 类 琉璃 分 类 ， 若 氧化 铝 值 大 于 1.5 则 为 铅 铀 玻璃 ， 反 之 为 高 钙 玉 璃
结果 为 A1、A6、A7 为 高 钾 琉璃，A2、A3、A4、A5、AS8 为 铅 钢 玻璃。
方法 二 : 选取 问题 2 对 于 高 鲜 下 璃 和 钥 钢 玻 璃 第 选 的 特征 PbO、KzO、BaO 和 SrO，
建立 这 四 个 特征 与 玻璃 类 型 的 偏 最 小 二 乘 回归 分 析 , 其 中 因 变 量 玻璃 类 型 中 高 鲜 玻 璃 取
值 为 1， 铝 饥 玻 璃 取 值 为 0。
基于 CV 交叉 验证 方法 计算 RMSEP, 使 用 所 有 主 成 分 进行 回归 得 到 的 结果 如 下 图 :
je

## Logical image page 17

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 17 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122429.jpg -->
<!-- source_image_sha256: 6C386E09EBAD0611BC4A8DBD3F2AD5D544932E380D602A500ECF7A4586C858E5 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

atas x dimension: 67 4
人
Fit method: kernelpls
imer oF Comgonerta’considered: 4
VALIOATION: msEp
CrosavaTdated.using 10 randon segnents.
(Intercept) 1 comps 2 comps 3 comps
ev 0 209
adjcv p 0.45 0.1470 0.1381 0.1365
cv  omn
ie
TRAINING: % variance explained
全 sr 2 cnc 3 camps 4 coms
x Tems dom fems
R
20 FiAA TARD —ReE AR
从 回归 结果 可 以 看 出 ， 主 成 分 个 数 为 3 时 ,模型 在 经 CV 交叉 验证 后 得 到 的 RMSEP
综合 最 小 , 同时 3 个 主 成 分 对 各 变量 的 累计 贡献 已 经 达到 93%6， 因 此 将 信 景 小 二 乘 加
归 的 主 成 分 个 数 设 定 为 3。
主 成 分 个 数 确定 后 计算 得 到 信 最 小 二 乘 回 归 系 数 如 下 图 17, PbO、K30、BaO 和 SrO
回归 系数 分 别 为 00134、-0.1582、-0.0288、-0.0206。
group
H
8
党
了
-人
10 15 20 25 30 35 40
variable
图 21; 偏 最 小 二 乘 回归 系数
将 表单 3 中 PbO、Kx0、Bao 和 SrO 化 学 成 分 数据 带 入 信 最 小 二 乘 回 归 模 型 ， 预 负
得 到 不 同文 物 的 预测 值 ， 如 果 预 负 人 接近 1， 则 为 高 甸 下 玛 ， 预 负 值 接近 0， 则 为 负
丈 病 。 预 测 结果 见 下 表 17。
表 17; 表单 3 未 知 玻 斑 文物 的 类 型 预测
E [ 7
Al 1.0408 高 钾
A2 0.0177 铅 饥
A3 0.0980 wa
Ad4 0.1898 铅 钢
A5 0.2558 加 饥
A6 0.9615 高 钾
A7 0.9631 高 钾
A8 0.1122 LEN
~1y

## Logical image page 18

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 18 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122431.jpg -->
<!-- source_image_sha256: 135DBDF479823E4B62160C55719B599FCA29D89B3A108AA01294792E7C079C10 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

通过 上 面 分 析 ， 可 以 看 出 两 种 方法 预测 结果 一 致 。

为 了 更 进一步 分 析 高 钾 玻 璃 与 铅 钢 玻璃 的 亚 类 划分 ， 基 于 问题 2 的 亚 类 划分 结果 。
对 于 高 钾 玻 珊 ， 以 亚 类 3 类 为 因 变 量 ， 化 学 成 分 Ka0、SiO、CaO、SnO; 和 BaO 为 自 变
量 ， 建 立 偏 最 小 二 乘 回 归 ， 通 过 交叉 验证 确定 主 成 分 个 数 为 2， 对 表单 3 中 A1，A6,
A7 文物 进行 预测 ， 结 果 是 &1，A6，A7 都 是 高 钾 玻璃 的 同一 亚 类 。

对 于 欠 钢 玻 珊 ， 以 亚 类 3 类 为 因 变 量 ， 化 学 成 分 P:05、CuO、Naz0 和 Fez03 为 自 变
量 ， 建 立 偏 最 小 二 乘 回归 ， 通 过 交叉 验证 确定 主 成 分 个 数 为 2， 对 表单 3 中 A2，A3，
4A4，A5，A8 文物 进行 预测 ， 结 果 是 A2 和 A4 是 负 钢 玻璃 的 同一 亚 类 ，43 和 Ag8 £i
钢 玻 璃 的 同一 亚 类 ，AS 是 锥 钢 玻 璃 的 另 一 亚 类 。

《4 问题 4
6 4.1 相关 性 热力 图 分 析

将 玻璃 按照 高 钾 与 锥 饮 玻璃 进行 分 类 讨论 ， 因 为 题目 中 要 求 分 析 不 同类 别 文 物化 学
成 分 之 间 的 关联 关系 ， 且 因 变 量 较 多 ， 热 力图 更 可 直观 地 体现 两 两 化 学 成 分 之 间 的 相关
关系 ,根据 颜色 深浅 比较 相关 关系 的 大 小 ， 故 可 分 别 制作 高 钾 玻璃 与 铅 钢 玻璃 的 化 学 元
素 热力 图 ， 如 下 图 所 示 :

gosgsSgoeg
2
如 本 > 。sem 3
Ca0 m 加 下
Fe203 | 司 »
Cu0 本 图 豆 声 [04
SO2 本 [02
Na20 下 鹿 可 9
|
目 二 对 本 时 |
FS 图 四 国 24
K20 加 加 四 -0.6
加 中 |
图 22， 高 钾 琉璃 热力 图

由 高 钾 玻璃 热力 图 可 知 ， 按 照 热力 图 上 方 从 左 到 右 元 素 顺序 ， 每 个 元 素 与 左右 相 邻

元 素 相关 性 较 强 ，SiO? 与 Bao 关联 性 较 退 ， 其 余 两 两 成 分 之 间 关联 性 相对 较 弱 。
图 23， 铀 饥 玻 璃 热力 图
ji

## Logical image page 19

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 19 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122433.jpg -->
<!-- source_image_sha256: 7576CEB1D86D8F0C3377F03F7D22413D6CB2879053C1B08964E63FDC544D0308 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

由 铅 钢 彼 璃 热力 图 可 知 ，SnO?、SiO?、NazO、Fez03、K2O、MgO、AlO3 这 七 个 成
分 两 两 之 间 均 存在 相关 性 〈Fez0s 和 NazO 之 间 除 外 ) 。CuO、BaO、SO? 两 两 之 间 均 存
在 较为 强烈 的 相关 性 。

6.4.2 差异 性 分 析

为 了 比较 不 同类 别 之 间 的 化 学 成 分 关联 关系 的 差异 性 ， 由 于 热力 图 中 相关 系数 是 对
称 矩 阵 。 因 此 仅 选取 高 钾 玻 璃 相关 系数 上 三 角 矩 阵 与 铅 负 玻 璃 相关 系数 上 三 角 矩 阵 。 由
于 每 个 化 学 成 分 之 间 的 相关 关系 是 配对 的 ,因此 选取 非 参 数 配对 样本 wilcoxon 检验 , 得
到 结果 p 值 为 0.905。 由 于 p 值 大 于 ae (0.05) ， 因 此 不 拒绝 原 假设 ， 即 两 种 琉璃 类 型 的
化 学 成 分 之 间 的 关联 关系 没有 显著 差异 。

七 、 模 型 检验 及 可 靠 性 分 析
7.1 针对 问题 一 的 检验

在 进行 问题 1 之 前 ， 首 先 对 表单 中 数据 进行 预 处 理 。 对 于 玻璃 的 化 学 成 分 ， 近 似 零
值 插 补 后 转换 为 成 分 数据 ， 化 学 成 分 比例 和 为 10096。 数据 预 处 理 合理 。 对 于 问题 1 %
虑 到 成 分 数据 的 特殊 结构 ， 在 成 分 数据 单 形 空间 上 计算 均值 ， 选 择 适 用 于 成 分 数据 的
Dirichlet 回归 模型 ， 分 析 方法 相 比 传统 分 析 方法 更 加 合理 。

7.2 针对 问题 二 的 检验

对 于 问题 2， 选 择 两 种 方法 分 析 高 钾 玻 璃 与 铅 钢 璃 的 分 类 规律 两 种 方法 结果 一
致 ， 进 一 步 验证 了 分 类 模型 合理 性 。 对 每 类 玻璃 亚 类 划分 时 ， 基于 kmeans 聚 类 分 析 确
定 了 最 优 聚 类 个 数 ， 分 析 结果 真实 可 靠 =
73 针对 问题 三 的 检验

偏 最 小 二 乘 回 归 方 法 基于 交叉 验证 确定 了 最 优 主 成 分 个 数 。 基 于 两 种 方法 对 未 知 玻
璃 文物 进行 类 别 预测 风 结果 一 致 。 因 此 预测 结果 合理 。

7.4 针对 问题 四 的 检验

腔 用 Pearson 相关 系数 分 析 化 学 成 分 之 间 的 关联 关系 ， 基 于 wilcoxon 检验 比较 两 种
类 型 玻璃 化 学 成 分 之 间 关联 关系 的 差异 性 。 结 果真 实 可 靠 .

八神 型 评价 与 展望
8.1 模型 的 优点

本 文 优点 是 基于 成 分 数据 分 析 对 玻璃 化 学 成 分 进行 分 析 , 并 对 不 同 琉璃 类 型 进行 分
类 ， 具 体 体现 在 如 下 方面 :

《1) 在 数据 预 处 理 阶段 ， 采 用 乘法 普 换 法 对 空白 处 及 0 值 进行 插 补 。

《2) 结合 成 分 数据 的 几何 结构 ， 计 算 不 同文 物化 学 成 分 的 均值 。

《3) 采用 Dirichlet 回归 模型 对 风化 前 的 化 学 成 分 进行 预测 。

《4) 对 于 不 同 玻璃 类 型 的 分 类 ， 考 虑 到 成 分 数据 求 和 为 100%6 的 约束 在 模型 构

建 前 ， 首 先 对 化 学 成 分 进行 elr 变换 ， 使 得 成 分 数据 变换 为 欧式 空间 上 的 普
通 数 据 。
《5) 采用 不 同 分 类 模型 对 琉璃 类 型 进行 分类 记 不 同 模型 结果 一 致
《6) 对 于 每 种 方法 ， 都 对 参数 进行 敏感 性 分 析 ， 选 择 最 优 参数 。
ev

## Logical image page 20

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 20 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122435.jpg -->
<!-- source_image_sha256: 443E4B65D1E9A6AA9455A86C513FB39F611E482DC74BF0CA874860DA33DFDFB0 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

82 模型 的 缺点
对 于 问题 4， 不 同 玻璃 类 型 的 化 学 成 分 之 间 的 关联 关系 ， 采 用 Pearson 相关 系数 。
但 Pearson 相关 系数 只 能 度量 变量 之 间 的 线性 相关 关系 ， 在 使 用 之 前 未 进行 线性 相关 关
系 检验 。
83 模型 的 展望
对 于 问题 2， 分 析 不 同 玻璃 之 间 的 分 类 规律 时 ， 由 于 两 种 类 型 玻璃 样本 量 不 是 很 接
近 ,， 因此 后 续 可 以 考虑 不 平衡 样本 分 类 模型 ， 通 过 对 训练 集 样 本 重 采样 或 方法 修正 来 进
去 分 类 。 对 于 问题 4， 考 虑 其 他 相关 系数 方法 来 度量 化 学 成 分 之 间 的 关联 关系 ， 例 如 灰
色 关联 分 析 ， 最 大 距离 相关 系数 、 互 信息 等
九 、 参 考 文献
[1] 赵 志 强 , 新 疆 巴 里 坤 石子 沟 遗 直 群 出 土 玻璃 珠 的 成 分 体系 与 制作 工艺 研究 [D] 西
北大 学 , 2016.
(2] 安家 瑶 . 玻璃 器 史话 [M]. 北京 : 社会 科学 文献 出 版 社 , 2011: 7-11
[3] Pawlowsky-Glahn V. Buccianti A. Compositional Data Analysis: Theory and Applica -
tions [M]. Wiley 2011.
[4] Pawlowsky-Glahn V, Egozeue J J, Tolosana-Delgado R. Modeling and Analysis of
Compositional DatalM]. Wiley 2015.
EPAS

## Logical image page 21

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 21 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122437.jpg -->
<!-- source_image_sha256: 3F168BFC06B47839B454D9D3005A68EEC2B06A6A7DA6F96ADBF295FF2645642A -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

附 录
支撑 材料 ;
1 数据 :
加 数据 1: 附件 表单 1 数据 播 补 续 失 值 xlsx
占 数据 2: 附件 表单 3 数据 处 理 xlsx
可 数据 3: 附件 表单 3 据 处 理 xsx
加 数据 4: 风化 点 风化 前 化 学 成 分 蔬 测 数据 xlsx
@) 数据 5: 决策 鸯 Xisx
可 数据 6: 票 关 xlsx
加 数据 7: 热力 图 xsx
避 数据 8: myydataxisx
2. 辅 助 资料 :
&) Dirchlet 回 昌 结果 docx
) 高音 玻 璃 、 银 钢 玻璃 风化 与 无 风化 均值 docx
了. 图:
加 图 1: 玻 克制 ff 过 程 docx
加 图 2: docx
加 图 3: 琉 斑 类 型 doci
加 加 4 颜色 docx
癌 图 5: 高 旦 玻 玛 风化 前 后 化 学 成 分 对 比 ， 外 加 为 风化 ， 内 且 为 无 风化 docx
5) 图 6: 高 摆 玻 斑 风 化 前 后 化 学 对 比 (未 仿 SiO2) ， 外 加 为 风化 ， 内 加 为 无 风化 docx
加 图 7: 铅 锅 玻 下 分 化 前 后 元 素 对 比 ， 外 图 为 风化 ， 内 用 为 无 风化 docx
加 图 8: 名 名 玻 殉 风 化 前 后 元 素 对 比 (未 含 SiO2) ， 外 加 为 风化 ， 内 加 为 无 风化 docx
加 加 9: 决策 树 结果 docx
图 10: 偏 最 小 二 乘 判 分 析 结果 docx
加 图 11: 信 最 小 二 和 判 吕 分 析 模 型 办 证 docx
B) 图 12: 高 区 分 类 个 数 确定 .docx
B) 图 13: 铅 钢 分 类 个 数 确定 docx
加 图 14: 高 郊 取 类 博 况 docx
B) 图 15: 铅 钢 取 类 情况 docx
1

## Logical image page 22

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 22 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122439.jpg -->
<!-- source_image_sha256: 2F941F32B83A3E477B51E6765069132A69110C7DDFAF6BAFA62426918B3406B9 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

加 图 16: 高 曙 玻 殉 亚 类 偏 最 小 二 区 判别 分 析 结 果 docx
B) 图 17: 高 押 玻 确 亚 类 仿 最 小 二 条 关 吕 分 析 模 型 验证 docx
©) 图 18: 铝 钢 玻 殉 亚 类 人 最 小 二 条 判别 分 析 结果 docx
司 图 19: 欠 枫 玻 确 亚 类 他 小 二 乘 判 分 析 模型 验 让 docx
晤 图 20: 所 有 主 成 分 下 久 最 小 二 条 回 昌 结果 docx
辣 图 21: 仿 最 小 二 乘 回 昌 系 数 docx
司 图 22: 高 甸 玻 殉 热力 图 docx
晤 图 23: 铝 负 玻 到 热力 图 docx
4 表 :
加 表 1: 符号 说 明 docx
加 表 2: BES% (1) .docx
癌 %3: BESH (2) .docx
加 表 4: 表单 2 成 分 数据 播 衬 忽 失 值 (部 分 ) .docx
加 表 5: 表单 3 成 分 数据 播 负 失 值 (部 分 ) .docx
加 表 6: 虚拟 变量 处 理 docx
加 表 7: 纹 电 与 表面 风化 相关 性 docx
加 表 8: 琉 到 类 型 与 表面 风化 相关 性 docx
加 %9: 颜 和 与 表面 风化 相关 性 docx
加 表 10: 卡 广 检 次 结 时 docx
可 表 1T 高 摆 玻 璃 、 负 钢 玻 玉 风 化 与 无 风化 均值 docx
加 表 12: 预测 风化 前 的 化 学 成 分 含量 (部 分 ) .docx
加 表 13: 偏 昌 小 二 天 分 析 的 不 同 特征 的 VIP 值 docx
加 表 14: 亚 分 类 docx
加 表 15: 高 多 下 玉 亚 类 全 最 小 二 乘 关 别 分 析 的 不 同 特征 的 VIP 值 docx
加 表 16: 铅 钢 琉璃 亚 类 信 最 小 二 乘 着 分 析 的 不 同 特征 的 VIP 值 docx
加 表 17: 表单 3 未 知 玻 殉 文 物 的 类 型 预 到 docx
和 代码 :
工

## Logical image page 23

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 23 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122441.jpg -->
<!-- source_image_sha256: 8AAF300406FD86966EB4522527582E225809CBD94076BF310BD701DD68679A2E -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

1 1 附录 一 : 数据 处 理 及 问题 1 代码 R
1] 2 澳 录 一: 决策 国人 码 R
] WR=: 取 类 分 析 代码 R
AHRD: 问题 3 代码 R
SHRE: WOBRBR
HRA: 问题 4 检验 代码 R
附录 一 数据 处 理 及 问题 1 代码
Yy -readtable'CNUsers\86182WDesktopWdata tst"header = TskipNul = T)
# 成 分 数据 缺失 值 填补
Tibrary(zCompositions)
library(compositions)
library (DirichletReg)
y_bianhan <-
multRepl(y.label-0,dl-¢(0.0.8.0.11,0.21,0.21,0,0.17.0.11,0.11,0.97,0.07.0.03.0.23,0.11))
write esv(y_bianhan file = "C:/Users/86182/Desktop/datacsv")
¥3 一 readtable'CNUsers\86182NDesktopWdatatxtheader=TskipKul = T)
¥3_bianhan <
‘multRepl(y3.label=0,dI=c(0.0.8,0.11,0.21,0.21,0,0.17.0.11,0.11,0.97,0.07.0.03.0.230.11))
write.csv(y3_bianhan,file = "C:/Users/86182/Desktop/data.csv")
# 成 分 数据 求 均值 及 clr 变 换
gaojia <- y_bianhan[1:18,]
mean(acomp(gaojia))
gianbei <- y_bianhan[19:67.]
‘mean(acomp(gianbei))
X_gacjia0 <- mean(acomp(x_gacjia0))
x_gaojial <- mean(acomp(x_gaojial))
_gianbei0 <- mean(acomp(x_gianbei0))
x_gianbeil <- mean(acomp(x_gianbeil))
el <-elr(y_bianhan)
©2 < olr(y3 _bianhan)
write esve2.file = "C:/Users/86182/Deskiop/data.csv")
#dirichlet 回归
¥_chuli <- read.table("C:\Users\\86182\\Desktop! data.tst" header = TskipNul = T)
 <- read.table("C:\\Users!\86182 Desktop!\data.txt" header = T,skipNul = T)
fenghuadata <- cbind(y_chuli.x)
fenghuadataSy <- DR_data(y_chuli[1:14])
resl <- DirichReg(y ~ emblazonry + class + color + weathering, fenghuadata)
summary(res1)
# 预 测
II

## Logical image page 24

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 24 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122443.jpg -->
<!-- source_image_sha256: C786E790C1DF7B29F2D31590006CC6E682CEFED44A1494860AECEAA4392E1CB4 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

X_yuce <- readtable("C:NUsersN86182NDesktopWdatatxt"header = TskipNul = T)

X_pred <- predici(resLx_yuce)

write.csv(x._pred.file = "C:/Users/86182/Desktop/data.csv")

附录 二 决策 树 代码 CRIEH)

TibraryGrparD

Tibrary(tibble)

Tibrary(bitops)

Tibrary(rattle)

Tibrary(mpartplot

Tibrary(RColorBrewer)

mydata<-read table("clipboard" header=T)

sub<-sample(1:67.47)

train<-mydatafsub.]

test<-mydata[-sub.|

model <- mpart( 类 型 -data = train)

fancyRpartPlot(model)

x<-subset(testselect—-)

pred<-predict(modelx type="class")

k<-test[" 类 型 "

table(pred k)

附录 三 RASHTRT 〈R 语言 )

library(NbClust)

library (factoextra)

library(ggplot2)

mydata<-read table("clipboard” header=T)

head(mydata)

dim(mydata)

fviz_nbelust(mydata, kmeans, method = "wss")

kmeansO<-kmeans(mydatal,-14].centers=4)

print(kmeansO)

fitkm <- kmeans(mydata, 4, nstart-25)

fitkmssize

fitkmScenters

aggregate(mydatal-1], by-list(cluster=fit kmScluster), mean)

library(eluster)

setseed(1234)

fit.pam <- pam(mydatal-1], k-3, stand-TRUE)

fit. pamSmedoids

clusplot(fit pam, main~"Bivariate Cluster Plot")
TY

## Logical image page 25

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 25 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122445.jpg -->
<!-- source_image_sha256: E089B3C05BFEC1E7EF6C868C274CE8ADB7E638D439DD5B07692E52645573DB79 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

附录 四 问题 3 代码
斋 表 单 3 类 型 划分
mydata-read table("clipboard”, header = T, sep ="t)
‘mydata pls <- plsr(group ~K20+PbO+Ba0+Sr0,data-mydata, 4, validation = "CV")
‘summary(mydata pls)
‘mydata.pls <- plsr(group ~K20+PbO+Ba0+$rO data-mydata, 3, validation = "CV")
as matrix(coef(mydata.pls))
as matrix(mydata)].-1]%*%as matrix(coef(mydata.pls))
yuce=as matrix(read.table("clipboard", header = F, sep = 7)
predict(mydata.pls,yuce)
#j# 表 单 3 TE BORAR5y
‘mydata-read table("clipboard”, header = T, sep = AP)
mydata.pls <- plsr(subgroup -SiO2+K2O+CaO+BaO+SnO2
data-mydata, 5, validation ~"CV")
summary(mydata.pls)
mydata.pls <- plsr(subgroup -SiO2+K2O+CaO+BaO+SnO2.data-mydata, 2, validation =
"CVD
yuce=as matrix(read table("clipboard" header = F, sep = At)
predicttmydataplsyuce)
#j# 表 单 3 铅 钢 玻 璃 亚 类 划分
mydata-read table("clipboard”, header = T, sep ="t)
mydata.pls <- plsr(subgroup ~Na20+Fe203+Cu0O+P205,data-mydata, 4, validation = "CV
summary(mydata.pls)
mydata.pls < plsr(subgroup ~Na20-+Fe203+CuO+P205,data-mydata, 2, validation = "CV")
yuce=as. matrix(read.table("clipboard", header ~ F sep = 7)
predict(mydata.pls.yuce)
附录 五 热力 图 代码 〈R 语言 )
mydata<-read table("clipboard" header=T)
library(corrplot)
cor<-cor(mydata)
cormplot(cor,method-"square")
col2 <- colorRampPalette(c("#FFFFFF","white" "#000000")alpha = TRUE)
cormplot(cor, order ~ "helust”.method = "square",

tlcol="black" tlcex = 0.8)
cormplot(cor, order = "helust",col = col2(100).method = "color",

tlcol="black" tlcex = 0.8.¢l.pos = "r" clratio = 0.2,

insig = "blank" addgrid.col-"white")

¥

## Logical image page 26

<!-- source_page_kind: image_sequence -->
<!-- logical_page_number: 26 -->
<!-- source_image_path: 2022年数学建模国赛真题+优秀论文/2022年国赛优秀论文C题C229/8122447.jpg -->
<!-- source_image_sha256: 0B7F23787710FDBAA5E342C52EF9FEB0D94F2B069B03221497A3920414CCE8F1 -->
<!-- ocr_backend: tesseract.js 7.0.0 -->

附录 六 问题 4 检验 代码
gaojia-as matrix(read table("clipboard”, header = F, sep = AD)
pl=cor(gacjia)
PIlupper.i(p] diag-FALSE)]-0
x=as matrix(as.vector(p))
X[which(x!=0)]
qianbeias.matrix(read.table("clipboard”, header = F, sep ="t)
p2-cor(gianbei)
P2[tupper.tri(p2 diag-FALSE)]-0
yeasmatrix(as.vector(p2))
Yiwhich(y!=0)]
wileox test(x.y.paired = T)
vi
