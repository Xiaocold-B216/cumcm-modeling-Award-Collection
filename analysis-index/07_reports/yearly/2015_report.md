# 2015年数学建模国赛语料人工核验报告（29载体重建版）

## 一、年度结论

本轮重新扫描当前聊天中的全部2015输入，上一版17载体结果已作废。新版本对 **29个physical carriers** 完成只读SHA-256、格式解析、页面/区域分段、逻辑文档归并、六件套、知识抽取和本地测试，得到 **28个logical documents、29个representations、18篇参赛解答论文和18条solution lineages**。

A题 `(5)` 与 `(6)` 的文件SHA-256不同，但规范化全文哈希和低分辨率逐页渲染序列哈希相同，因此归并为一个logical document、两个representations；其余B/C/D论文均为独立逻辑文档。

年度质量门为 **`conditional_pass`**：当前29载体集合内部人工核验完成，但A题附件4原始视频未上传，且散装文件无法与可信基线2015目录做完整路径—哈希对账。

## 二、年度对象统计

- physical carriers：29
- logical documents：28
- representations：29
- preferred representations：28
- problem statements：4
- solution papers：18（A 6、B 5、C 4、D 3）
- datasets / supporting references：6
- expert commentaries：0（`not_observed`）
- solution lineages：18
- PDF carriers / pages：17 / 480
- Word carriers / rendered pages：11 / 142
- spreadsheet carriers / sheets / coordinate rows：1 / 3 / 63
- representation-level page/region segments：625
- preferred logical page/region segments：599
- method records：106
- visualization patterns：23

## 三、关键纠错

1. 上一版只统计17个载体，漏掉B题5篇、C题4篇、D题3篇论文，相关统计、gate与ZIP全部作废。
2. 29个文件不能直接等同于29篇论文：最终为18篇solution papers、4个题面、6个数据/规范对象。
3. A题7个PDF对应6篇逻辑论文；`(5)`和`(6)`为字节不同、内容等价的representations。
4. C题两个Word与两个PDF的标题、摘要、定义区间和算法路线均不同，识别为4篇独立论文。
5. D题两个Word和一个PDF分别采用整数规划/分层方案、税负临界调价、归一化非线性规划，识别为3篇独立论文。
6. 所有论文奖项等级保持`unknown`，不凭目录或文件顺序推断。

## 四、模型与算法谱系

### A题：太阳影子定位

天文几何正向模型 → 位置/日期逆问题；分支包括L-M、网格与多重搜索、粒子群、遗传算法、模拟退火、拟牛顿、人工鱼群，以及Hough/Canny/透视变换和动态追踪。

### B题：出租车资源配置

形成四层谱系：

1. 时空供需指标：空驶率、等待时间、里程利用率、供求比、最近邻匹配半径；
2. 数据模型：插值、聚簇、模糊评价、多元回归、S曲线；
3. 行为与路网：Floyd最短路、网格转移、吸引力函数、拒单高斯模型、拼车Logit模型；
4. 政策优化：社会福利最大化、分区域动态补贴、基础补贴步长搜索和热区迁移奖励。

### C题：月上柳梢头，人约黄昏后

统一框架为“太阳黄昏区间＋月球高度角区间＋日期时间交集”。分支包括简化直射点函数、儒略日和恒星时、黄道—赤道—地平坐标转换、球面三角、0—1指示函数与年度城市筛选。

### D题：众筹筑屋规划

统一先做普通宅/非普通宅土地增值税和财务核算，再优化房型套数。算法包括整数线性规划、分式平均满意度、分层双目标、临界增值率调价、归一化最小二乘非线性规划和回报率约束。

## 五、专家评审知识

当前上传集合未观察到独立专家评述、命题专家总结或正式评审记录。论文的“模型评价/优缺点”属于作者自评，不进入专家反馈事实记录。

## 六、高价值可视化模式

- A题：影长U形曲线、参数敏感性、误差面、候选地图、视频处理流程；
- B题：时空热力图/三维曲面、最近邻半径图、供求平衡坐标、回归和补贴响应曲线、路网最短路图；
- C题：天文坐标转换、观察者—树—月投影、黄昏/月高区间叠加、城市年度发生表；
- D题：房型约束表、税负分段表、多方案财务审计表、满意度—回报率权衡表。

## 七、数据质量限制

- A题附件4原始视频缺失，无法做视频与帧级独立核验。
- 当前是29个散装文件，不是`2015_raw_bundle.zip`，无法证明与可信基线2015目录完全一致。
- Word页数来自本地LibreOffice渲染，是representation审计页数，不声明为Word格式固有页码。
- 论文结论和数值为参赛方案结果，不代表官方唯一答案；外部平台数据、网页或程序附件未随论文载体全部提供时，其复现实验能力受限。

## 八、质量门

`conditional_pass`。当前上传集合的哈希、对象分层、角色识别、representation归并、页面边界、六件套和结构测试均通过；完整原始目录对账和A题视频仍为阻塞项。

## 九、本地测试

- 结果：`36 passed, 0 failed`
- 命令：`PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_2015_manual.py`
- 覆盖：JSON/JSONL/CSV、SHA-256、对象数量、角色合法性、preferred representation、重复归并、lineage与solves关系、页面/工作表边界、六件套、方法页码、unknown/not_observed、缺失项、源文件零修改。
