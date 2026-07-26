# 2019 年数学建模国赛资料分析报告

## 远端状态对账

- 2007、2008、2009：年度报告、quality gate 与 checkpoint 相互一致，按已验证 `pass` 处理。
- 2010：实际 quality gate 为 `conditional_pass`，不能按旧 `progress.json` 记为完成。
- 2011：本轮未观察到年度报告、quality gate 和 checkpoint，不列入已验证完成年度。
- 2019：本地分析、测试和上传包已完成，等待用户上传及远端读回，因此为 `conditional_pass_pending_user_upload`。
- `progress.json` 已据此纠正：`completed_years` 截止 2009，`last_verified_complete_year` 为 2009。

## 处理范围

- 物理载体：34 个；逻辑文档：34 个；representation：34 个。
- 解答论文：17 篇（A 题 3、B 题 3、C 题 3、D 题 4、E 题 4）。
- 题面：5 个；支撑数据/格式规范：12 个；PDF 页面：562 页，其中论文 554 页。
- 所有 34 个物理载体均计算完整文件 SHA-256；处理前后原始哈希一致。

## 关键纠错

- 旧的 20 载体阶段性统计已撤销；新增 14 篇论文合并后，年度解答论文总数为 17。
- 题面、附件和格式规范与参赛论文严格分开，不按文件数量直接统计论文。
- 2019 年 E 题附件 (1).csv 的中文字段值应按 GB18030 解码；按 Latin-1 读取会形成伪乱码。
- 17 篇论文 SHA-256 均不同，未将同题不同论文误归并为一个 logical document。
- 奖项等级、作者和学校未从当前文件中观察到，统一写 unknown/not_observed，不依据目录或文件名推断。

## 模型与算法谱系

- A 题：质量守恒常微分方程 → 压力/密度物性拟合 → 差分或数值积分 → 参数遍历/多重搜索 → 单阀、柱塞泵、双喷嘴和减压阀控制。
- B 题：一维分段碰撞 → 三维平动/转动与力矩 → 二阶微分方程时间离散 → 四元数/欧拉刚体旋转 → 模拟退火或最优还原策略。
- C 题：司机净收益决策 → 排队生灭过程/队列模拟 → 航班和需求预测 → 上车点单目标优化/蒙特卡洛 → 长短途优先队列。
- D 题：数据清洗与时间对齐 → EDA/相关分析/灰关联 → 漂移与气象因素分析 → 多元回归、插值、BP/RBF 网络 → 校准前后误差评价。
- E 题：销售流水清洗与成本补全 → 日级营业额/利润聚合 → 折扣力度特征 → 线性、分段、加权或多元回归 → 价格弹性和商品类别策略。
- 方法族频次（实例级）：preprocessing=6；optimization=4；regression=4；feature_engineering=4；search_optimization=3；eda=3；correlation_analysis=3；financial_aggregation=3；category_analysis=3；mechanistic_ode=2；finite_difference=2；geometry_model=2；robustness_analysis=2；mechanics=2；moment_model=2；ode_model=2；decision_model=2；priority_queue=2；sensitivity_analysis=2；multiple_regression=2；cost_imputation=2；numerical_integration=1；curve_fitting=1；interpolation=1；least_squares=1；phase_optimization=1；control_model=1；piecewise_dynamics=1；rigid_body_dynamics=1；numerical_simulation=1；time_discretization=1；quaternion=1；conservation_law=1；rigid_body_rotation=1；simulated_annealing=1；simulation=1；time_series=1；queueing_model=1；forecasting=1；monte_carlo=1；binary_decision=1；queue_simulation=1；traffic_flow_optimization=1；priority_rule=1；temporal_alignment=1；piecewise_interpolation=1；grey_relational_analysis=1；weighted_average=1；rbf_network=1；stepwise_regression=1；time_aggregation=1；bp_neural_network=1；hyperparameter_search=1；model_evaluation=1；sensor_drift_analysis=1；calibration_model=1；robust_regression=1；elasticity_analysis=1。

## 专家评审知识

当前提供资料中未观察到专家评述、命题说明或评委意见文档。该状态记录为 not_observed，而不是 absent；因此专家反馈知识库仅保留年度观察记录，不虚构评语。

## 高价值可视化模式

- 机制图 + 控制变量 + 目标函数 + 优化结果的四段式图链，适用于 A、B、C 题。
- 基线与校准/优化结果叠加的时序曲线，并辅以残差、敏感性或稳健性图。
- D 题中直方图、箱线图、散点矩阵、相关热图、网络结构与预测对比构成完整校准证据链。
- E 题中经营指标时序、折扣分布、折扣—销售/利润散点回归和类别柱状图可形成从总体到分组的分析链。
- C 题中的机场布局、排队流程、队列曲线和灵敏度表适合作为管理决策型论文的标准组合。

## 数据质量限制

- 论文多数为图像化页面，原生文本层不完整；本轮以全页渲染、页面级证据、摘要和选定模型/结果页人工核验为主。
- 未重新运行论文全部 MATLAB、Python、SPSS、SAS 或 Mathematica 程序，数值结果按论文报告记录。
- 未通过 GitHub 连接器获得可信基线中 2019 原始目录的完整树列表，因此“与基线目录逐路径完全对账”记为 not_observed；当前 34 个上传载体内部处理完整。
- 未观察到专家评述、官方奖项清单、作者与学校信息。

## 质量结论

本地结构、哈希、关系、六件套和年度测试全部通过。由于可信基线的 2019 原始目录无法逐路径独立读出，年度 quality gate 标记为 conditional_pass；该限制不阻塞上传，待用户提交后进行远端读回验证。
