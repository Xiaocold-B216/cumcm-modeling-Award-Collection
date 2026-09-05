# Extracted Paper

<!-- source_page: 1 -->

# 风电场运行状况分析及优化模型

摘要

风力发电是风能最主要的应用形式之一，对风电场的运行状况问题进行合理分析及 优化，对于充分利用风能资源、提高风电场的经济效益具有较大的实际意义。本文围绕 风电场运行状况的分析及优化问题，利用参数分析的方法对风能资源参数进行处理，利 用启发式算法对维修人员进行安排，综合利用 MATLAB 软件求解，分析出分能资源及其 利用情况、判断出新型号风机是否比现有风机更为适合、制定出对维修人员的排班方案 与风机维护计划，较为完善的解决了此问题。 针对问题一，对该风场的风能资源及其利用情况进行评估。其中对风能资源的评估， 首先对附件 1 的测风数据进行修正检验处理，利用修正处理后的数据对与风能资源相关 的各个参数进行量化计算，主要资源参数有平均风速、风速频率、有效小时数、年平均 风功能密度、风能密度、最大及最小风速、威布尔分布等。利用 MATLAB 软件求解各个 参数值，综合分析出该风电场的风能资源整体上较为稳定，风能资源较丰富，风能资源 利用空间较大；但部分参数波动较大，风能资源变化幅度较大，可利用效率不够可靠。 对于风能资源利用情况，风能资源的利用情况即为风能资源的实际输出功率占总装机容 量的比例，利用 MATLAB 软件求解，得出风能资源可利用率为 21.42%，与一般风电场极 限利用率 59.3%相差较大，风能利用率相对较低。

|针对问题二，从风能资源与风机匹配角度判断新型号风机是否比现有风机更为适合。|
|---|
|其中从风能资源角度判断，即利用两种风机的总发电量来进行比较，先利用附件 2 的风|
|速数据得出风速的威布尔分布函数，结合威布尔分布函数利用总发电量公式计算出新型|
|风机与现有风机的总发电量，具体结果见表 14。分析出机型Ⅲ比现有机型总发电量更少，|
|机型Ⅲ没有现有机型适合，机型Ⅳ比现有机型总发电量更多，机型Ⅲ比现有机型更适合，|
|机型Ⅴ大于机型Ⅰ的总发电量，机型Ⅴ比机型Ⅱ总发电量更多，新型机型Ⅴ比现有机型|
|Ⅱ更适合，总体上新型风机总发电量比现有风机总发电量更高，说明新型风机比现有风|
|机更适合。从风机匹配角度判断，计算出实际功率，将实际功率与不同种机型的额定功|
|率进行比较，结果见表 15。比较新型风机的实际功率与额定功率的差值比现有风机的差|
|值更小，说明新型风机更适合。综合两种角度的判断结果，可说明新型风机比现有风机|
|更为适合。|

针对问题三，制定维修人员的排班方案与风机维护计划，使各组维修人员的工作任 务相对均衡，且风电场具有较好的经济效益，这是个双目标优化问题。在模型的建立方 面，以较好的经济效益即总维护天数最少为第一目标，以各组维修人员的工作任务相对 均衡即各组最大总工作天数与最小总工作天数的差值最小为第二目标，以每次维护需一 组维修人员连续工作 2 天和每组维修人员连续工作时间（值班或维护）不超过 6 天为约 束条件，建立双目标优化模型。在模型的求解方面，由于双目标求解困难继而利用启发 式算法得出维修人员的排班方案与风机维护计划，具体结果见表 16、17。 本文最后对模型的结果进行了分析，综合分析结果的合理性，以及对模型进行了推 广，较好地应用于各个领域。 关键词：风电场运行 启发式算法 双目标优化模型

<!-- source_page: 2 -->

1.问题重述

|风能是一种最具活力的可再生能源，风力发电是风能最主要的应用形式。我国某风|
|---|
|电场已先后进行了一、二期建设，现有风机 124 台，总装机容量约 20 万千瓦。请建立|
|数学模型，解决以下问题：|
|1. 附件 1 给出了该风电场一年内每隔 15 分钟的各风机安装处的平均风速和风电场|
|日实际输出功率。试利用这些数据对该风电场的风能资源及其利用情况进行评估。|
|2. 附件 2 给出了该风电场几个典型风机所在处的风速信息，其中 4#、16#、24#风|
|机属于一期工程，33#、49#、57#风机属于二期工程，它们的主要参数见附件 3。风机生|
|产企业还提供了部分新型号风机，它们的主要参数见附件 4。试从风能资源与风机匹配|
|角度判断新型号风机是否比现有风机更为适合。|
|3. 为安全生产需要，风机每年需进行两次停机维护，两次维护之间的连续工作时|
|间不超过 270 天，每次维护需一组维修人员连续工作 2 天。同时风电场每天需有一组维|
|修人员值班以应对突发情况。风电场现有 4 组维修人员可从事值班或维护工作，每组维|
|修人员连续工作时间（值班或维护）不超过 6 天。请制定维修人员的排班方案与风机维|
|护计划，使各组维修人员的工作任务相对均衡，且风电场具有较好的经济效益，试给出|
|你的方法和结果。|
|附件 1 平均风速和风电场日实际输出功率表。|
|附件 2 风电场典型风机报表。|
|附件 3 风电场风机型号及其参数。|
|附件 4 风机生产企业提供的新型号风机主要参数。|

2.问题分析

|针对问题一，依据题意，结合附件 1 所给出的该风电场各风机安装处的平均风速和|
|---|
|风电场日实际输出功率，对该风电场的风能资源及其利用情况进行评估。其中，对于风|
|能资源的评估，是指通过对某一区域的风速、风向观测时间序列进行分析，估算出该区|
|域的风能资源储量，并对其风能资源多寡、质量和分布状况作出判断、评价。由中华人|
|民共和国国家标准风电场风能资源评估方法可知，评估风能资源的标准规定评估风能资|
|源应收集的气象数据、测风数据的处理及主要参数的计算方法、风功率密度的分级、评|
|估风能资源的参考判据、风能资源评估报告的内容和格式等，由此需先对附件 1 的测风|
|数据进行修正检验处理，进而将订正后的数据处理成评估风场风能资源所需要的各种参|
|数，包括不同时段的平均风速和风功率密度、风速频率分布和风能频率分布、风向频率|
|和风能密度 方向分布、风切变指数和湍流强度等。由于附件所给数据资料有限，因此|
|对于此问题资源评估参数只需考虑平均风速、风速频率、有效小时数、年平均风功能密|
|度、风能密度、最大及最小风速、威布尔分布等，对上述参数进行量化后则可依据其结|
|果相应的评估该风电场的风能资源。|
|对于该风电场的风能资源的利用情况进行评估，一方面，风能资源利用情况与风能|
|资源有关，由此可依据与风能资源相关的参数对风能资源利用情况进行相应评估；另一|
|方面，风能资源利用情况直接关联着实际输出功率与理论功率，由此需对利用情况进行|
|量化定义，风能资源的利用情况即由风能资源的实际输出功率占总装机容量的比例来反|
|应，比例越大风能资源可利用量率高，利用效率越高，由此对风能资源的利用情况进行|
|评估。|
|针对问题二，依据附件 2 给出了该风电场几个典型风机所在处的风速信息及附件 4|
|风机生产企业还提供了部分新型号风机的主要参数，试从风能资源与风机匹配角度判断|

<!-- source_page: 3 -->

|新型号风机是否比现有风机更为适合。其中从风能资源角度判断，即判断新型号风机与|
|---|
|现有风机所产生的风能资源的多寡，所产风能资源更多者更适合，因此可从两种风能机|
|的总发电量进行评估。由于总发电量与威布尔分布函数有关，因此可利用附件 2 的风速|
|信息得出该风电场的威布尔分布函数，继而利用总发电量公式可计算出新型号风机与现|
|有风机的总发电，总发电量大的更适合，得出新型风机与现有风机哪种更适合。|
|从风机匹配角度判定，即可将新型风机与现有风机的额定功率与实际输出功率进行|
|比较，额定功率与实际输出功率相差更小风机更适合。对于风机实际输出功率，由于风|
|速越大功率越大，进而可依据附件 3 的风速与功率的关系数据拟合出风速与功率的关系|
|函数式，利用该函数关系式得出附件 2 的风速对应的功率，得出年平均功率与新型风机|
|和现有风机的额定功率进行比较，差别更小的风机更适合。|
|针对问题三，依据题意要求满足维修人员安排的前提下，制定维修人员的排班方案|
|与风机维护计划，使各组维修人员的工作任务相对均衡，且风电场具有较好的经济效益。|
|这是个双目标优化问题，以较好的经济效益即总维护天数最少为第一目标，以各组维修|
|人员的工作任务相对均衡即各组最大总工作天数与最小总工作天数的差值最小为第二|
|目标，以每次维护需一组维修人员连续工作 2 天和每组维修人员连续工作时间（值班或|
|维护）不超过 6 天为约束条件，建立双目标优化模型。以结合题意为了安全生产的需要，|
|风机每年需进行两次停机维护，两次维护之间的连续工作时间不超过 270 天，考虑到要|
|保证风电场具有较好的经济效益且维修人员安全维修，由此应选择风力较小的两个季节|
|开始维修，且保证两次开始维修相隔时间小于 270 天，选择风力较小时间维修，风力越|
|小风机在维修时所浪费发电量越小，对于维修人员也相对更安全。对于题中要求每次维|
|护需一组维修人员连续工作 2 天，则以 2 天为一个工作日，同时风电场每天需有一组维|
|修人员值班以应对突发情况，则在每个工作日都安排一组维修人员进行值班。结合风电|
|场现有 4 组维修人员可从事值班或维护工作，每组维修人员连续工作时间（值班或维护）|
|不超过 6 天的要求，可引入相应算法对其进行安排。|

3.模型假设
（1）假设新型号风机与现有风机的轴轮横扫面积相同； （2）假设新型号风机与现有风机的直径大小一致； （3）假设附件中所给的数据都是真实可靠的。

4.符号说明

|r|:空气密度；||||||
|---|---|---|---|---|---|---|
|3 V j|j :第||个风速区间的风速值的立方；||||
|t j||:某扇区域全方位第|j||个风速区间的风速发生的时间；||
|W₁||：月风能资源总量；|||||
|D WE i,|：第个|i|月的风能密度 (|i|= 1, 2,...,12) ；||
|d ：第 i|i|个月的总天数 (|i|= 1, 2,...,12) ；|||
|t ：第 ij|i||个月某扇区域全方位第||j 个风速区间的风速发生的时间 (|i = 1, 2,...,12) ；|

<!-- source_page: 4 -->

|m|：风速区间数目；|||||
|---|---|---|---|---|---|
|T ：第 i|i|个月的有效小时数 (|i|= 1, 2,...,12) ；||
|p ：第 i|i|个月的月风资源可利用率 (||i|= 1, 2,...,12) ；|
|p ix,|i ：第 个月第|x|天的风资源可利用率 (||i = 1, 2,...,12) ；|
|fv||()：风速的概率分布函数；||||
|V₁||：风电机组切入风速；||||

*V₂* ：风电机组切出风速；

*p*¢(*v*) ：有效风速范围内的条件概率分布密度函数；

## T ：全年有效小时数；

*v* *i* ：切入风速；

*v* *r*：额定风速；

*v* *f*：切出风速；

*A*：风能横扫面积；

*C* *p*：风能利用系数；

*fv* ()：威布尔分布函数。

5.模型的建立与求解
5.1 模型准备 由中华人民共和国国家标准风电场风能资源评估方法可知，评估风能资源的标准规 定评估风能资源应收集的气象数据、测风数据的处理及主要参数的计算方法、风功率密 度的分级、评估风能资源的参考判据、风能资源评估报告的内容和格式等，由此需先对 附件 1 的测风数据进行修正检验处理，进而将订正后的数据处理成评估风场风能资源所 需要的各种参数。
5.1.1 测风数据完整性检验 对测风数据完整性检验可从预期记录数据的数量和时间顺序两方面进行，对缺失数 据进行修复，对完整数据进行检验。 （1）预期记录数据的数量 由附件 1 的测风数据可知，2015 年 3 月 30 日 6 时的风速数据缺失，对此进行缺失 数据的修复。注意到风速每隔 15 分钟变化幅度不大，由此采用将这一小时内前 3 个时 段的风速数据进行求平均值，得到的均值代替第 4 个时段的风速。已知前 3 个时段的风 速分别为 7 *ms*、6.9 *ms*、6.8*ms*，进而得出起平均值 6.9*ms*，所以 3 月 30 日 6 时 的风速为 6.9 *ms*。

<!-- source_page: 5 -->

（2）时间顺序 由附件 1 的数据可知，给出了该风电场一年内每隔 15 分钟的各风机安装处的平均 风速，数据的时间顺序符合预期的开始、结束时间、中间风速数据连续，符合风速的时 间顺序。

5.1.2 测风数据合理性检验 对于风速数据的合理性检验可对风速的各个参数进行计算，并与规定参考参数进行 比较看是否符合风速的合理性，对此可从风速的范围检验和趋势检验两方面进行检验。 （1）风速范围检验 由于附件 1 所给的数据只有风速和实际输出功率，因此风速范围检验的主要参数只 考虑平均风速，由此对该风电场的月平均风速进行计算，得出结果见表 1。
表 1 该风电场的月平均风速 月份（月） 1 2 3 4 5 6 月平均风速

6.0321 6.5151 5.4765 5.5859 5.6884 5.8933
*ms* （ ）

月份（月） 7 8 9 10 11 12 月平均风速

5.3469 4.6410 6.0436 5.3129 5.3316 6.1320
*ms* （ ）

## 结合参考资料可知，合理的平均风速参数范围为 0≤小时平均风速＜40ms，而上

述 12 个月的月平均风速都居于该范围内，由此通得过风速范围检验。 （2）风速趋势检验 由于附件 1 所给的数据只有风速和实际输出功率，因此风速趋势检验的主要参数只 考虑一小时平均风速变化，由此对该风电场月每天的一小时平均风速变化进行计算， 得出结果见表 2。

## 表 2 月每天 1 h平均风速变化（单位：ms）

月份（月） 1 2 3 4 5 6 一小时平均风

1.4836 2.1148 1.4635 1.8269 1.7449 2.0943
速变化 月份（月） 7 8 9 10 11 12 一小时平均风

1.2416 1.0907 1.8552 1.7100 1.9282 1.2689
速变化 有参考资料可知，一小时平均风速的合理变化趋势范围为 6*ms*，由上述计算结果 可看出每月的一小时平均风速变化范围居于该合理变化趋势范围内，所以风速数据通得 过风速趋势检验。

5.1.3 计算测风有效数据完整率 对附件 1 的有效数据完整率进行计算，进而对该数据进行合理利用。由资料可知测 风有效数据完整率等于应测数目减缺测数目减无效数据数目，除以应测数目，该风电场 的具体测风数据数目见表 3。
表 3 测风有效数据完整率 有效数据完整 测风类型 应测数目 缺测数目 无效数据数目 率

<!-- source_page: 6 -->

<u>测风数目（个）</u> 35040 99.99% 由表 3 可知，测风有效数据完整率为 99.99%，符合测风有效数据完整率达到 90%的 标准，同时说明该风电场的测风数据准确性非常高，可合理利用。

5.2 问题一的模型建立与求解 由中华人民共和国国家标准风电场风能资源评估方法可知，应确定出资源评估的主 要参数。由于附件所给数据资料有限，因此对于此问题资源评估参数只需考虑平均风速、 风速频率、有效小时数、年平均风功能密度、风能密度、最大及最小风速、威布尔分布 等，对上述参数进行量化后则可依据其结果相应的评估该风电场的风能资源。对于风能 利用情况评估则可定义为实际输出功率效率，即为该风电场的实际输出功率占总装机容 量的比例。
5.2.1 利用评估参数对风能资源评估 （1）平均风速的确定 平均风速为给定时间内瞬时风速的平均值，给定时间从几秒到数年不等。由资料可 得出平均风速为给定时间内的总风速除以相应时间段，即为
*n* 1 *V* ==å*V* (*i* 1, 2,...,*n*) （1） *Ei* *ni*=1

利用 MATLAB 软件，结合附件 1 的风速数据及上述（1）式的平均风速计算公式，可 得出该风电场的月平均风速和年平均风速，见表 4。 表 4 该风电场月平均风速 月份（月） 1 2 3 4 5 6 月平均风速

6.4589 6.8330 5.8484 6.2352 6.2549 6.2873
*ms* （ ）

月份（月） 7 8 9 10 11 12 月平均风速

5.7187 5.1309 6.4338 5.7854 5.8036 6.6747
*ms* （ ）

## 由表 4 得出的月平均风速，继而得出该风电场的年平均风速为 6.1221ms，由此可

知该风电场的平均风速分布较为均匀，全年发电量较为均匀，全年的风能资源较稳定； 12 月、1 月、2 月的月平均风速更大且分布较均匀，风能资源较丰富，风能资源的可利 用空间较大。 （2）最大最小风速 最大最小风速为特定观测时段内（通常指日、月、季或年）出现的最大最小风速。 利用 MATLAB 软件对附件 1 的平均风速进行筛选，得出最大最小风速见表 5。

## 表 5 该风电场最大最小风速（单位： ms）

## <u>月份（月）</u> 最大风速 最小风速 <u>月份（月）</u> 最大风速 最小风速

|1|14.4|0.2|7|12.2|1.1|
|---|---|---|---|---|---|
|2|13.7|0.4|8|14.3|0.7|
|3|15.2|1.0|9|24.1|0.6|
|4|15.0|0.7|10|13.9|0.4|
|5|17.8|0|11|15.4|0.4|

<!-- source_page: 7 -->

|6||15.9|||0.7||12|||15.8||0.6|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|用风能资源。||（3）年平均风功率密度 的一个指标，由此年平均风功率密度为||由表 5 可知，该风电场全年的最大风速为 24.1|= WP|速相差较大，各月最大风速分布较为均匀，各月风能资源分布较为稳定，更能合理的利 12 1 2 n|风功率密度为一个地方风能资气流垂直通过单位截面积的风能，是表征源多少 n ki, DV r åå k ki == 11|ms 3 () k i,||，全年最小风速为 0||ms ，两风 （2）|
|n 其中 V 时数， 为第 ki,||k 个月的风速序列。|为计算时段内风速序列个数，r|得出年平均风功率密度和各个月的风功率密度，见表 6。||k 表 6 月平均风功率密度（单位：|结合附件 1 所给的数据和（2）式年平均风功率密度的公式，利用 MATLAB 软件求解，|为月平均空气密度，|2 wm ）|n k 为第 ki,||个月的观测小|
|月份（月）||1|||2||3|4||5||6|
|月平均风功率 密度||203.6221|||248.8855||164.3096|197.5432||197.0274||211.8533|
|月份（月）||7|||8||9|10||11||12|
|月平均风功率 密度 表示为||143.1618 （4）风能密度的确定|||98.8740 DWE =|风能资源在单位截面积上风能变化波动大，由此风能资源的利用情况不稳定。 m 1 å 2 j =1|207.1258 由表 6 可知，各个月平均风功率密度分布不均匀，且变化落差较大，反应该风电场 风能密度为在设定时段与风向垂直的单位面积中风所具有的能量，由此风能密度可 3 (r)(V) j|150.7643 t j||164.6777||274.8312 （3）|
|m 其中 为某扇区域全方位第 平均风能密度，见表 7。||j||为风速区间数目， r 为空气密度，||个风速区间的风速发生的时间。 表 7 该风电场月平均风能密度|3 V 为第 j 结合附件 1 所给的数据和（3）式风能密度的公式，利用 MATLAB 软件求解，得出月|j||个风速区间的风速值的立方，||t j|
|月份（月）||1|||2||3|4||5||6|
|月平均风能 密度||5963.4544|||7929.1707||5061.6574|6969.9997||6541.6645||6646.2686|
|月份（月）||7|||8||9|10||11||12|

<!-- source_page: 8 -->

月平均风能

5033.2545 3230.4450 6457.6908 4410.4992 4981.5699 8341.7707
<u>密度</u> 风功率密度 280 260 240 220 200 180 160 140 120 100 80 0 2 4 6 8 10 12

||||||||图 1 月风功率密度变化|||
|---|---|---|---|---|---|---|---|---|---|
||用平均风速|由此风能资源的利用情况不稳定。 （5）威布尔（Weibull）分布 参数分布函数簇，风速 对威布尔（Weibull）分布参数 V 威布尔（Weibull）两参数|v fv = 估计 m ，以标准差|k v (c c kv k -1 () e cc = k 、|-1) v k -() c c k 、 SV 1 = n c|上半年的月平均风能密度波动较为均匀，风能密度较为稳定，风能资源较为稳定；下半 年的相对波动较大，7、8、9 月和 11-12 月风能密度变化幅度较大，风能资源不稳定， 的威布尔分布概率密度函数表达式为 () =- exp[( m == n SV å Vi i =1|由表 7 月平均风能密度得出年平均风能密度为 5963.9538，由图 1 可看出该风电场 威布尔（Weibull）分布用于描述风速分布的概率函数，是一个单峰的 2 参数或 3 v kk)] c 进行估算。 n 1 å n i =1 sm -|估计s ，所以 m 、s 分别表示为 VV i 2 () 按下式估计，保留两位。|（4） （5） （6）|

<!-- source_page: 9 -->

|||||k|s -1.086 = () m||||（7）|
|---|---|---|---|---|---|---|---|---|---|
|||||c =|m G+ (1 1 k)||||（8）|
|(1 1 其中 G+|k||) 为伽马函数，当 G+|(1|1 k) <1 时， G +|(1 1 k) =|G+ (x 1) x||(1 1 k) >2 ,当 G+|
|(1 1 k) = (1+1 时 G +||k - •G + 1) (1|1 k （6）、（7）、（8）式分别得出威布尔分布参数 m 、s 、||-1),由此可得出 k 对于风能资源的威布尔分布参数的确定，依据附件 1 所给的平均风速数据和上述（5试 表 8 威布尔分布参数|c 和 c k 、||，进而得出相应的威布尔分布。 的值，见表 8。||
|分布参数||m|||s|k|||c|
|数值结果 依据表 8||5.6666|||1.6726 的威布尔分布参数的计算结果，可得出威布尔分布的解析式为|0.2658|||2.5460|
|0.2658 f (v) = (2.5460|（6）有效小时数的确定|v 0.2658-1) 2.5460|v -() 2.5460 e 有效小时数为统计出代表年测风序列中风速在 3-25|0.2658|速概率分布以及风能发动机要求的可利用风速区间，可以求得风能发动机的实际可工作|ms||之间的累计小时数，根据风||
|时数，即风能可利用时数 fv 其中 月有效小时数，见表 9||T ()为风速的概率分布函数。|T|为有效风能在统计时段 = T 0|T₀ v₂ f () v dv] ò [v₁ 由附件 1 中的数据并结合（9）式的有效小时数，利用 MATLAB 软件求解得出全年的 表 9 有效小时数||内的累计小时数，则可表示为||（9）|
|月份（月）||1|2||3|4|5||6|
|有效小时数||654|594||656|590|643||618|
|月份（月）||7|8||9|10|11||12|
|有效小时数||636|606||635|618|594||610|

<!-- source_page: 10 -->

||||图 2 月有效小时数|||
|---|---|---|---|---|---|
|||图 2 可看出每月风能可利用时数较为均匀，风能资源较为稳定，风能资源利用效率较高，|由表 9 得出风能发动机每月的实际可工作时数，即每月风能可利用时数。由表 9 及|||
|风能资源利用空间较大。|（7）风速频率的确定|||||
|风速频率为以 1|ms 出现的频率。每个风速区间的数字代表中间值，如 5|由附件 1 中的数据，利用 MATLAB 软件求解得出全年的月风速频率，见表 10。 表 10 月风速频率|为一个风速区间，统计代表年测风序列中每个风速区间内风速 ms|ms 风速区间为 4.6|ms 到 5.5 。|
|风速区间|[0,3)|[3, 4)|[4,5)|[5,6)|[6,7)|
|风速频率(%)|14.53|15.59|16.11|13.24|11.15|
|风速区间|[7,8)|[8,9)|[9,10)|[10, 25)||
|风速频率(%)|9.29 由表 10 风速频率可知，月风速频率居于 频率最小，风速频率较为分散。 5.2.2 利用能源资源储量对风能资源评估 （1）风能资源总量|7.28 估算出该区域的风能资源储量，并对其风能资源多寡、质量和分布状况作出判断、评价。 其中风能资源储量包含风能资源总量和风能资源有效储量，由此分别对其进行量化。 以月风能资源总量等于月平均风能资源密度乘以每月小时数，即为|5.21 [4,5) 对于风能资源的评估，是指通过对某一区域的风速、风向观测时间序列进行分析， 风能资源总量与平均风能密度和总小时数有关，由于附件所给数据是一年内的，所|7.60 区间的频率最大，居于|[9,10) 区间的|
||W =|= D ´ d ´ 24 1, WE i i m 1 3 (r)(V) t å ij ij 2 j =1|´ d ´ 24 i||（10）|

<!-- source_page: 11 -->

|W₁ 其中|为月风能资源总量，|D 为第个 WE i,|i 月的风能密度，|d i 为第 i|t 个月的总天数， ij|
|---|---|---|---|---|---|
|i 为第|个月某扇区域全方位第 区间的风速值的立方， r 为空气密度， 同理年风能资源总量即可表示为|j m|个风速区间的风速发生的时间， 为风速区间数目。|3 V i 为第 j|j 个月第 个风速|
||W =|= D ´ ´ g 24 2, WE i 12 m 1 3 [(r)(V åå ij 2 ij == 11|) t]´ ´ g 24 ij||（11）|
|W₂ 其中 即表示为|为年风能资源总量， （2）风能资源有效储量|g W =´ D T 3, WE i m 1 (r)(V å ij 2 j =1|为一年的总天数。 风能资源有效储量与平均风能密度和风速有效小时数有关，由于附件所给数据是一 年内的，所以月风能资源有效储量等于月平均风能资源密度乘以每月风速有效小时数， i 3 =´) t T ij i||（12）|
|W₃ 其中|为月风能资源有效储量， 同理年风能资源有效储量 W|T 为第 i W₄ 为 12 =´ () D åå 4, WE i 12 m 1 3 [(r)(V å å ij 2 i =1 j =1 式得出每月的风能资源有效储量和年风能资源有效储量，具体结果见表 11。 表 11 每月的风能资源总储量与有效储量（单位：百万|i 个月的有效小时数。 12 T i ii == 11 12 =´) t] T å ij i i =1 依据上述月平均风能资源密度与月小时数，结合（10）、（11）式得出每月风能资源 总储量和年风能资源总出储量，由平均风能资源密度与风速有效小时数，结合（12）、（13）|kw ）|（13）|
|月份（月）|月资源总储 量|月资源有效 储量|月份（月）|月资源总储 量|月资源有效 储量|
|1|4.4368|3.9001|7|3.7447|3.2011|
|2|5.3084|4.7099|8|2.4035|1.9576|
|3|3.7659|3.3204|9|4.6495|4.1006|
|4|5.0184|4.1123|10|3.2814|2.7257|
|5|4.8670|4.2063|11|3.5867|2.9591|
|6|4.7853|4.1074|12|6.2063|5.0885|

<!-- source_page: 12 -->

||5.5 5 4.5 4 3.5 3 2.5 2 1.5 0|2 4|有效风能密度 6|8 10|12||
|---|---|---|---|---|---|---|
||||图 3 有效小时数变化||||
|由表 11 kw 44.3891 百万|分布较为均匀，风能资源较为稳定合理。 5.2.3 对风能资源利用情况的定义及评估 实际输出功率占总装机容量的比例。 的比例，则风能资源可利用率表示为|可得出年风能资源总储量为|52.0739 风能资源有效性较大；由表 12 可知，月资源总储量与月资源有效储量变化幅度不大， 对风能资源利用情况进行评估，一方面可依据风能资源的参数进行相应的评估；另 一方面，需对风能资源的利用情况进行量化定义，风能资源的利用情况即由风能资源的 实际输出功率占总装机容量的比例来反应即为风能资源可利用率，比例越大风能资源可 利用率越高，利用效率越高，由此来评估风能资源的利用情况。注意到附件 1 的平均风 速与实际日输出功率存在不合理数据，由此先对不合理数据剔除，进而计算风能资源的 由上述分析可知，风能资源的利用情况即由风能资源的实际输出功率占总装机容量 n p å ix, x =1 p = i n|kw 百万 ，有图 3 可看出年风能资源有效储量与年风能资源有效储量相差不大，|，年风能资源有效储量为|（14）|
|p 其中 i|为月风资源可利用率， 出全年 12 个月的风能资源可利用率，见表 12。|p ix,|i 为第 个月第 依据附件 1 所给的数据结合上述（14）式风能资源可利用率，利用 MATLAB 软件得 表 12 每月风能资源可利用率|x|天的风资源可利用率。||
|月份（月）|1|2|3|4|5|6|
|可利用率（%）|30.88|29.16|22.82|26.68|26.03|18.21|
|月份（月）|7|8|9|10|11|12|
|可利用率（%）|12.21|13.10|17.85|16.56|18.61|24.95|

<!-- source_page: 13 -->

# 风能利用率

35.00%
30.88%

|30.00%|30.88% 29.16%|||||
|---|---|---|---|---|---|
|25.00%||26.68% 26.03% 22.82%|||24.95%|
|20.00%|||18.21%|17.85% 18.61% 16.56%||
|15.00% 10.00% 5.00% 0.00%|||12.21% 13.10%|||
||1 2 3|4 5 6|7 8 9|10 11|12|

系列1

图 4 风能利用率变化 由表 12 可得出年风能资源可利用率为 21.42%，与一般风电场极限利用率 59.3%相 差较大，风能利用率相对较低，由图 4 可看出月风能可利用率较为稳定。

5.3 问题二的模型建立与求解 依据附件所给的数据资料，试从风能资源与风机匹配角度判断新型号风机是否比现 有风机更为适合，由此应两方面进行判定。对于风能资源角度，可依据两种风机的总发 电量与有效风功率密度来评判，其中总发电量计算可利用附件 2 的风速数据得出为布尔 分布函数，进而利用总发电量公式计算出新型风机与现有风机的总发电量，总发电量更 大的风机更适合。对于风机匹配角度，将两种风机的额定功率与实际功率进行比较判定， 而实际功率可依据附件 3 的风速与功率关系数据拟合出风速与功率的关系式，利用该关 系式得出附件 2 风速对应的实际功率，将实际年平均功率与两种风机的额定功率进行比 较，相差更小的更适合。
5.3.1 从风能资源角度判断 从风能资源角度判断即考虑新型风机与现有风机的总发电量，分别对其进行比较， 来判定新型风机是否比现有风机更适合。 （1） 总发电量的比较 总发电量与风速的威布尔分布有关，由此先依据附件 2 的风速数据确定出风速的威 布尔分布函数。威布尔（Weibull）分布用于描述风速分布的概率函数，是一个单峰的 2 参数或 3 参数分布函数簇，风速*v*的威布尔分布概率密度函数表达式为
*k vkk*-1*v* *fv* ( ) =-() exp[ ()] *c c c* *vk*（15） *kvk*-1-() *c* = () *e* *cc*

## 对威布尔（Weibull）分布参数k 、 c进行估算。

用平均风速*V* 估计 m ，以标准差 *SV* 估计s ，所以 m 、s 分别表示为

*n* 1 m == *VV*å（16） *i* *ni*=1

*n* sm = *SV* =å()-（17） *Vi* *ni*=1

<!-- source_page: 14 -->

||||威布尔（Weibull）两参数|k 、|c 按下式估计||||||
|---|---|---|---|---|---|---|---|---|---|---|
||(1 其中 G+|1 k||) 为伽马函数，当 G+|s k = () m c = G+ (1 (1 1 k|-1.086 m 1 k) ) <1 时， G +|(1 1|G+ (x 1) k) = x||（18） （19） (1 1 k) >2 ,当 G+|
|时 G +|(1 1 k 其中 T 分布参数|) = (1+1|k - •G + 1) (1 利用上述所得的威布尔分布函数得出总发电量 W T (t 为全年有效小时数， 能横扫面积， r 为空气密度， m|1 k v i 数据，利用 MATLAB 软件得出威布尔参数值见表 13。|-1),由此可得出 AC v f (v dv) p 为切入风速， C p 表 13 年威布尔分布参数值 s|k 和 W vv 11 rf =+ rr òò vv ir 22 v r 为风能利用系数， 综合上述（15）、（16）、（17）、(18)、（19）、（20）式，结合附件 2 的风速|c 公式为 t 33 C v f p r 为额定风速，|(v dv)) v f fv ()为威布尔分布函数 k|，进而得出相应的威布尔分布。 为切出风速，|（20） 为风 A c|
||数值结果 见表 14。||6.7114 f () v 表 14|根据所求出威布尔分布参数值，得年威布尔概率密度函数为 2.543|2.0317 v = 0.2732 ´ æö 2.543|-0.7268 ´ ç÷ èø 利用表 13 的参数值和附件 3 是数据代入（20）式，得出各种风机所产的总发电量， 各种风机所产的总发电量（单位：万|v - 2.543 e|0.2735 0.2732 æö ç÷ èø w ）||2.5430 （21）|
|机型|||机型Ⅰ|机型Ⅱ||机型Ⅲ||机型Ⅳ||机型Ⅴ|
|总发电量|风机更适合。 5.3.2 从风机匹配角度判断 小的更适合。||2.2065|2.2016|Ⅳ比现有机型总发电量更多，机型Ⅲ现有机型适合，机型Ⅴ大于机型Ⅰ的总发电量，机 型Ⅴ比机型Ⅱ总发电量更多，新型机型Ⅴ比现有机型Ⅱ更适合，总体上新型风机比现有 可依据附件 3 的风速与功率关系数据拟合出风速与功率的关系式，利用该关系式得出附 件 2 风速对应的实际功率，将实际年平均功率与两种风机的额定功率进行比较，相差更|1.9448 由表 14 可知，机型Ⅲ比现有机型总发电量更少，机型Ⅲ没有现有机型适合，机型 对于风机匹配角度，将两种风机的额定功率与实际功率进行比较判定，而实际功率||2.2065||2.4845|

<!-- source_page: 15 -->

|||对附件 3 的风速与功率数据进行拟合，得出拟合图像，见图 5。||||
|---|---|---|---|---|---|
||1600 1400 1200 1000 800 600 400 200 0 3 4|5 6 图 5 风速与功率的拟合关系|机型2 7 8 9 由图 5 可知，功率随着风速的增大而增大，大体呈幂函数分布，由此得出风速与功|10 11||
|率的关系式为||y =- a v|b () v r||（22）|
|v r 其中|a 为额定功率， 、 3 的新型风机与现有风机进行比较，具体结果见表 15。|b 为拟合函数系数。 表 15 新型号现有风机与实际功率的比较|依据附件 2 的风速数据，代入上述（22）式，得出年实际功率为 360.7469，将附件|||
|机型|机型Ⅰ|机型Ⅱ|机型Ⅲ|机型Ⅳ|机型Ⅴ|
|额定功率|2000|1500|1500|1500|1500|
|差值|1639.2531|1139.2531|1139.2531 由表 15 可知，新型风机的实际功率与额定功率的差值比现有风机的差值更小，说|1139.2531|1139.2531|
|明新型风机更适合。|5.4 问题三的模型建立与求解|||||

依据题意要求满足维修人员安排的前提下，制定维修人员的排班方案与风机维护计 划，使各组维修人员的工作任务相对均衡，且风电场具有较好的经济效益。根据题意， 要制定维修人员的排班方案与风机维修计划，以各组维修人员的工作任务相对均衡、风 电场具有较好的经济效益为目标。以风电场每天需要一组维修人员值班以应对突发情况、 每组维修人员连续工作时间（值班或维护）不超过 6 天为约束条件，以此来建立双目标 优化模型。针对第一个目标，要使各组维修人员的工作任务相对均衡，可以用各组最大 的总工作天数和最小总工作天数的差值进行定义，该差值越小，说明各组维修人员的工 作任务相对均衡。针对第二个目标，要使风电场具有较好的经济效益，可以使总的维修 天数最少来进行定义，总的维修天数越少，说明经济效益越好。

5.4.1 目标函数的确定 各组维修人员的工作任务相对均衡的目标,该目标转化为以各组最大的总工作天数 和最小总工作天数的差值最小为目标函数。

<!-- source_page: 16 -->

min(*UL*-) （23）

其中：*U* 为所有组的总工作天数的最大值，*L*为所有组的总工作天数的最小值。 风电场具有较好的经济效益的目标，该目标转化为总的维修天数最少。

minN （24）

其中：*N* 为总的维修天数。

5.4.2 决策变量的确定 引入决策变量为
ì1，第*i*次维修时选第j组维修人员进行维护 *x* *ij*
= í (*i* = 1, 2,... ;*e j* = 1, 2,...*m*)
î0，第*i*次维修时不选第j组维修人员进行维护

ì1，第*i*次维修时选第j组维修人员进行值班 *x* *ik*
= í (*i* = 1, 2,... ;*e j* = 1, 2,...*m*)
î0，第*i*次维修时不选第j组维修人员进行值班

5.4.3 约束条件的确定 所有组的总工作天数的最大值和最小值都要大于 0。
*UL*,0 ³ （25）

所有组的总天数都要小于所有组总天数的最大值，所有组的总天数都要大于所有组 总天数的最小值。 *e*

# åxij´2£U ( j = 1, 2,...m)

（26） *i*=1

*e*

# åxij´2³ L ( j = 1, 2,...m)

（27） *i*=1

## 其中U 为所有组的总工作天数的最大值，L为所有组的总工作天数的最小值，e 为

所有风机维修的总天数，*x* *ij* 为决策变量。

两个决策变量要满足

*x* *ij* Î" {0,1 ,} *i*, *j* （28）

*xi* *ik* Î" {0,1 ,}, k （29） 每组维护人员连续工作时间（值班或维护）不超过 6 天。 *f* *j* ´2£ 6 （30）

其中 *f* *j* 为第 *j* 组维修人员连续维护的天数。

每天需要一组维修人员值班以应对突发情况的约束。 *m*

# åxik== t (i 1, 2,...,e)

*k*=1（31）

<!-- source_page: 17 -->

5.4.4 优化模型的建立 结合以上的目标函数和约束条件，建立双目标优化模型，即
min(*UL*-)

minN

ì *e* ïå *x* *ij* ´£ *t U* ï *i*=1 ï *e* ïå *x* *ij* ´³ *t L* ï *i*=1 ï *x* Î" 0,1, *i*, *j*
*s t*. .í *ij*{} ( *j* == 1, 2,...*m i*; 1, 2,...,*e*)
ï *xi* Î" 0,1,, k ï *ik*{} ï *ft* *j* ´£6 ï *m* ï ï å*xtik*= î *k*=1

5.4.5 普适性的启发式算法

|由于上述模型求解较困难，由此引入启发式算法。|||
|---|---|---|
|结合题意为了安全生产的需要，风机每年需进行两次停机维护，同时到要保证风电|||
|场具有较好的经济效益且维修人员安全维修，由此应选择风力较小的两个季节开始维修，|||
|选择风力较小的时间开始维修，风力越小风机在停机进行维修时所浪费发电量越小，对|||
|于维修人员也相对更安全。由相关文献可知，当风速大于等于 10|ms|时维护人员不宜维|
|护作业，利用附件 1 全年风速数据，统计风速大于等于 10|ms|的风速数据，由此得出风|
|ms 速大于等于 10 的频数折线图，见图 6。|||
|风速 >10m/s 的频数折线图 600 500 400 的频数 300 200 100 >10m/s 0 风速 1 2 3 4 5 6 7 8 9 10 月份|系列1 11 12||
|ms 图 6 风速大于等于 10|的频数折线图||
|ms 由图 6 可知，风速大于等于 10|的频数在 3 月后和 8 月后两时段相对更小，即春||
|季和秋季风力较小，两季节相隔时间为 100 天满足了两次开始维护相隔时间小于 270 天|||
|的要求。对此风机每年第一次开始维护时间为 3 月 1 日，第二次开始维护时间为 9 月 1|||
|日。|||

<!-- source_page: 18 -->

|||||||||结合题意每次维护需一组维修人员连续工作两天，则以两天为一个工作日，同时还|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Step1:将 为 1，2，…，|n m Step3:依据题意总共有|。||Step2:假设一组维修人员在连续工作两天内能维修 m|台风机进行编号，依次为 1，2，…，|工作时间（值班或维护）不超过 6 天，由此可写出相应算法，具体步骤如下。|要满足风电场每天需有一组维修人员值班以应对突发情况，则在每个工作日都安排一组 维修人员进行值班。风电场现有 4 组维修人员可从事值班与维护工作，每组维人员连续|n n 组维修人员，每次维护需一组维修人员连续工作|m ，将 台风机。|||组维修人员进行编号依次|t 天，在|
|ab,|a ,(b-k 维修， 应风机编号为 Step4:在 行维修，第|+ t f a ,( k|) 时间段内安排第 -[n m ( b ++ t|- k) - 1) - a|j 组人员值班，每次维护一组维修人员可维修 f] ,(b 2|++ t 组 人 员 值 班 ， 总 共 维 修||组维修人员进行维修和值班，安排|n 1) 时间段内，继续安排 Step3 中第 n m-k|()|mk - 台，则总共维修|n m j 台 ， 所 剩 风 机 编 号 为|- k|组维修人员进行 () 台，对 组维修人员进|
|[n m (|- k) - Step5:在 休息，使第|f + - 1] a ,( k|[2 n m ( b 2 t|- k ++ 1) -|) - f +1] a ,(b|++ 3 t 组维修人员继续进行维修，则总共能维修||2) 时间段内，使|mk -|n ´|组维修人员中的 mk - 2||mk - 2|组人员 台，风机编号为|
|[2|n m (- k 休息过的|) - f a Step6: 在 mk - 2|+ 2] -[2 ,(b|n m (- ++ 3 t 3) -|k) - f a ,(b 组人员维修风机和值班。|+ + ´ 2 ++ 4 t Step7:重复 Step3、Step4、Step5 、Step6 直达风机维修完。|n|mk -] 。 2|3) 时间段内，让未休息的||mk - 2|||组的人员休息，|

在满足风电场每天需要一组维修人员值班以应对突发情况、风电场现有 4 组维修人 员可从事值班或维修工作、每组维修人员连续工作时间不超过 6 天等约束，为了使各组 维修人员的工作相对均衡，且使风电场具有较好的经济效益。在保证维修人员的安全， 风越大时，进行维护风机就越不安全；为了使风电场具有较好的经济效益，尽量选择在 风小的季节进行风机的维护，此时损失的效益就更小。 为了使各组维修人员的工作任务相对均衡，则先将所有组都安排去工作，再进行轮 换工作，用以下具体步骤来制定维修人员的排班方案与风机维护计划。 第一步:将 124 台风机进行编号，依次为 1,2,…,124,将 4 组维修人员进行编号，依次为

<!-- source_page: 19 -->

*A*, *B*, *C* ， *D* 。 第二步：在 3 月 1 日至 3 月 2 日时间段内，安排 *A*, *B*, *C* 维修人员进行维护风机，安排 *D*维修人员进行值班。则总共能维修 3 ´ 3 台风机，这些风机编号为 1-9。 第三步：在 3 月 3 日至 3 月 4 日时间段内，继续安排 *A* ，*B* ，*C* 维修人员进行维护风机， 继续安排*D*维修人员值班。则总共能维修 3 ´ 3 台风机，这些风机编号为 10-18。 第四步:在 3 月 5 日至 3 月 6 日时间段内，让 *A* 和 *B* 维修人员休息两天，让 *A*维修人员 继续进行维护风机，*D*维修人员继续进行值班。则总共能维修 3 ´ 1 台风机，这些风机 编号为 19-21。 第五步：在 3 月 7 号至 3 月 8 号时间段内，让连续工作 6 天的 *A* ， *D*休息，让休息过的 *B* ，*C* 来工作。即让*B*维修人员进行维护风机，让*C* 维修人员进行值班。则总共能维修 3´1 台风机，这些风机编号为 22-24。 第六步：按照第一步至第五步的方法，以此类推，直到把所有的风机都维护完，即得到 维修人员的排班方案与风机维护计划。

|||利用上述算法并结合步骤，4 组维修人员对 124 台风能机进行一年的维护，得出第||
|---|---|---|---|
||一次夏季维修人员的排班方案与风机维护计划，具体结果见表 18。 表 16|春季维修人员的排班方案与风机维护计划||
|风机编号|维护日期（月，日）|维修人员组别|值班人员组别|
|1-9|3.1-3.2|A、B、C|D|
|10-18|3.3-3.4|A、B、C|D|
|19-21|3.5-3.6|A|D|
|22-24|3.7-3.8|B|C|
|25-33|3.9-3.10|A、B、D|C|
|34-42|3.11-3.12|A、B、D|C|
|43-45|3.13-3.14|D|A|
|46-48|3.15-3.16|C|B|
|49-57|3.17-3.18|A、C、D|B|
|58-66|3.19-3.20|A、C、D|B|
|67-69|3.21-3.22|A|D|
|70-72|3.23-3.24|B|C|
|73-81|3.25-3.26|A、B、D|C|
|82-90|3.27-3.28|A、B、D|C|
|91-93|3.29-3.30|D|A|
|94-96|3.31-4.1|C|B|
|97-105|4.2-4.3|A、C、D|B|
|106-114|4.4-4.5|A、C、D|B|
|115-117|4.6-4.7|A|D|
|118-120|4.8-4.9|B|C|
|121-124|4.10-4.11 为 3 月 1 日-4 月 11 日，工作时间为 42 个工作日，该风机维护较为合理，有效保证各组 维修人员的工作任务相对均衡，且使风电场具有较好的经济效益。|A、B、D 由表 16 可知，得出一年中第一次春季维修人员的排班方案与风机维护计划，计划 同理结合上述算法得出一年中第二次秋季维修人员的排班方案与风机维护计划，具|C|
|体结果见表 17。|表 17|秋季维修人员的排班方案与风机维护计划||

<!-- source_page: 20 -->

|风机编号|维护日期（月，日）|维修人员组别|值班人员组别|
|---|---|---|---|
|1-9|9.1-9.2|A、B、C|D|
|10-18|9.3-3.4|A、B、C|D|
|19-21|9.5-9.6|A|D|
|22-24|9.7-9.8|B|C|
|25-33|9.9-9.10|A、B、D|C|
|34-42|9.11-9.12|A、B、D|C|
|43-45|9.13-9.14|D|A|
|46-48|9.15-9.16|C|B|
|49-57|9.17-9.18|A、C、D|B|
|58-66|9.19-9.20|A、C、D|B|
|67-69|9.21-9.22|A|D|
|70-72|9.23-9.24|B|C|
|73-81|9.25-9.26|A、B、D|C|
|82-90|9.27-9.28|A、B、D|C|
|91-93|9.29-9.30|D|A|
|94-96|10.1-10.2|C|B|
|97-105|10.3-10.4|A、C、D|B|
|106-114|10.5-10.6|A、C、D|B|
|115-117|10.7-10.8|A|D|
|118-120|10.9-10.10|B|C|
|121-124|10.11-10.12 为 9 月 1 日-10 月 12 日，工作时间为 42 个工作日，该风机维护较为合理，有效保证各 组维修人员的工作任务相对均衡，且使风电场具有较好的经济效益。|A、B、D 由表 17 可知，得出一年中第一次秋季维修人员的排班方案与风机维护计划，计划|C|

6.结果分析

|6.1 问题一的结果分析|
|---|
|结合风能资源的相关参数，利用 MATLAB 软件求解，得出参数数据并就此评估出该|
|风电场的风能资源整体上较为稳定，风能资源利用效率较高，风能资源利用空间较大；|
|但同时存在部分参数波动较大，风能资源变化幅度较大，可利用效率不够可靠。通过计|
|算风能资源可利用率，得出年风能资源可利用率为 21.42%，与一般风电场极限利用率|
|59.3%相差较大，风能可利用率相对较低，该风电场的风能资源利用情况不够。|
|6.2 问题二的结果分析|
|结合附件 3 和 4 的相关数据，利用 MATLAB 软件求解，得出总发电量并对各个机型|
|进行比较，得出新型风机比现有风机更为适合；得出实际功率与各个机型的额定功率进|
|行比较分析，得出新型风机比现有风机更为适合。|
|6.3 问题三的结果分析|
|结合 4 组风机维修人员和 124 台风机，得出第一次和第二次的维修人员的排班方案|
|与风机维护计划。第一次从 3 月 1 日开始，耗用时间为 42 个工作日，该风机维护较为|
|合理，有效保证各组维修人员的工作任务相对均衡，且使风电场具有较好的经济效益；|
|第二次从 9 月 1 日开始，耗用时间 42 个工作日，有效使各组维修人员的工作任务相对|
|均衡，且风电场具有较好的经济效益，该风机维护较为合理。|

7.模型的评价与推广

<!-- source_page: 21 -->

|7.1 模型的评价|
|---|
|7.1.1 模型的优点|
|（1）在处理资源的利用率时，对原数据的合理性进行了检验，从而提高了数据的|
|实用性与科学性。|
|（2）问题一中利用风能资源参数对风能资源进行评估，利用风能资源可利用率对|
|风能资源的利用情况进行评估，具有一定的合理和科学性。|
|（3）问题三中利用启发式算法，得出较优的维修人员的排班方案与风机维护计划，|
|结果较为全面优化，具有一定的合理性。|
|7.1.2 模型的缺点|
|（1）由于附件 1 所给的资料较为单一，对风能资源的参数数目考虑的不够全面，|
|由此评估的风能资源存在一定的局限性。|
|（2）问题一中计算新型风机的实际功率，通过现有风速与功率的关系拟合出风速|
|与功率的关系式，用该关系式得出实际功率代替新型风机的实际功率，具有一定的误差，|
|结果缺乏一定的准确性。|
|（3）问题三中对维修人员的排班方案与风机维护计划进行排列，具有一定的人工|
|干预，缺乏一定的说服力。|
|7.3 模型的推广|
|对于风电场的风能资源的相关分析及优化可运用于水利发电、潮汐发电以及火力发|
|电等广泛领域，可较好的解决诸多领域的问题。|

8.参考文献
[1]陈练，李栋梁，吴洪宝，中国风速概率分布及在风能评估中的应用，2016 年。 [2]郑崇伟，全球海域风能资源储量分析 2016 年。 [3]张义斌，王胜伟，风电场输出功率的概率分布及其应用，2016 年。 [4] 牟聿强,王秀丽，风电场风速分布及风速功率曲线分析,2016 年。 [5]潘慧慧，李永光，风力发电机组额定风速的选择研究，2016 年。

<!-- source_page: 22 -->

附录

附录一:计算平均风速程序： clear;clc %%%附件 1 每个月平均风速 for i=1:31 shuju=xlsread('201501.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%1 月 end pingjunfensu=[pingjunfengsu]; xlswrite('D2015.xls',pingjunfengsu,'A1:AE1')

for i=1:28 shuju=xlsread('201502.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%2 月 end pingjunfensu=[pingjunfengsu]; xlswrite('D2015.xls',pingjunfengsu,'A2:AE2')

for i=1:31 shuju=xlsread('201503.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%3 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A3:AE3')

for i=1:30 shuju=xlsread('201504.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%4 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A4:AE4')

<!-- source_page: 23 -->

for i=1:31 shuju=xlsread('201505.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%5 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A5:AE5')

for i=1:30 shuju=xlsread('201506.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%6 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A6:AE6')

for i=1:31 shuju=xlsread('201507.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%7 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A7:AE7')

for i=1:31 shuju=xlsread('201508.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%8 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A8:AE8')

for i=1:30 shuju=xlsread('201509.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10);

<!-- source_page: 24 -->

fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%9 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A9:AE9')

for i=1:31 shuju=xlsread('201510.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%10 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A10:AE10')

for i=1:30 shuju=xlsread('201511.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%11 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A11:AE11')

for i=1:31 shuju=xlsread('201512.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); pingjunfengsu(i)=mean(fengsu); %%%12 月 end pingjunfensu=[pingjunfengsu]'; xlswrite('D2015.xls',pingjunfengsu,'A12:AE12') 附录二:计算风速频率程序： clear;clc %%%风速区间 for i=1:31 %%%一月 shuju=xlsread('201501.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3));

<!-- source_page: 25 -->

shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:28 %%%二月 shuju=xlsread('201502.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian);

<!-- source_page: 26 -->

qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:31 %%%三月 shuju=xlsread('201503.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4)

<!-- source_page: 27 -->

sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:30 %%%四月 shuju=xlsread('201504.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:31 %%%五月 shuju=xlsread('201505.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3));

<!-- source_page: 28 -->

shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:30 %%%六月 shuju=xlsread('201506.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian);

<!-- source_page: 29 -->

qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:31 %%%七月 shuju=xlsread('201507.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4)

<!-- source_page: 30 -->

sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:31 %%%八月 shuju=xlsread('201508.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:30 %%%九月 shuju=xlsread('201509.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3));

<!-- source_page: 31 -->

shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:31 %%%十月 shuju=xlsread('201510.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian);

<!-- source_page: 32 -->

qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:30 %%%十一月 shuju=xlsread('201511.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4)

<!-- source_page: 33 -->

sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9)

for i=1:31 %%%十二月 shuju=xlsread('201512.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); qujian=fengsu(find(fengsu<3)); shuliang1(i)=length(qujian); qujian=fengsu(find(fengsu<4&fengsu>=3)); shuliang2(i)=length(qujian); qujian=fengsu(find(fengsu<5&fengsu>=4)); shuliang3(i)=length(qujian); qujian=fengsu(find(fengsu<6&fengsu>=5)); shuliang4(i)=length(qujian); qujian=fengsu(find(fengsu<7&fengsu>=6)); shuliang5(i)=length(qujian); qujian=fengsu(find(fengsu<8&fengsu>=7)); shuliang6(i)=length(qujian); qujian=fengsu(find(fengsu<9&fengsu>=8)); shuliang7(i)=length(qujian); qujian=fengsu(find(fengsu<10&fengsu>=9)); shuliang8(i)=length(qujian); qujian=fengsu(find(fengsu>=10)); shuliang9(i)=length(qujian); end sl1=sum(shuliang1) sl2=sum(shuliang2) sl3=sum(shuliang3) sl4=sum(shuliang4) sl5=sum(shuliang5) sl6=sum(shuliang6) sl7=sum(shuliang7) sl8=sum(shuliang8) sl9=sum(shuliang9) 附录三:计算风能密度程序： clear;clc %%%计算风能密度 p=1.293; t=0.25; for j=1:31

<!-- source_page: 34 -->

shuju=xlsread('201501.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa1(j)=sum(fengneng)/2; end bb1=mean(aa1)

p=1.293; t=0.25; for j=1:28 shuju=xlsread('201502.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa2(j)=sum(fengneng)/2; end bb2=mean(aa2)

p=1.293; t=0.25; for j=1:31 shuju=xlsread('201503.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa3(j)=sum(fengneng)/2; end bb3=mean(aa3)

for j=1:30 shuju=xlsread('201504.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3));

<!-- source_page: 35 -->

for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa4(j)=sum(fengneng)/2; end bb4=mean(aa4)

for j=1:31 shuju=xlsread('201505.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa5(j)=sum(fengneng)/2; end bb5=mean(aa5)

for j=1:30 shuju=xlsread('201506.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa6(j)=sum(fengneng)/2; end bb6=mean(aa6)

for j=1:31 shuju=xlsread('201507.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa7(j)=sum(fengneng)/2; end bb7=mean(aa7)

for j=1:31

<!-- source_page: 36 -->

shuju=xlsread('201508.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa8(j)=sum(fengneng)/2; end bb8=mean(aa8)

for j=1:30 shuju=xlsread('201509.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa9(j)=sum(fengneng)/2; end bb9=mean(aa9)

for j=1:31 shuju=xlsread('201510.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa10(j)=sum(fengneng)/2; end bb10=mean(aa10)

for j=1:30 shuju=xlsread('201511.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa11(j)=sum(fengneng)/2;

<!-- source_page: 37 -->

end bb11=mean(aa11)

for j=1:31 shuju=xlsread('201512.xls',j,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); fengsu=fengsu(find(fengsu>3)); for i=1:96 fengneng(i)=fengsu(i).^3.*p.*t; end aa12(j)=sum(fengneng)/2; end bb12=mean(aa12)

ss=(bb1+bb2+bb3+bb4+bb5+bb6+bb7+bb8+bb9+bb10+bb11+bb12)/12 附录四:计算风功率密度程序： clear;clc %%%计算风功率密度 shuju=xlsread('Dpingjunfengsu.xls','A1:A31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp1=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','B1:B28'); p=1.293; for i=1:28 dwp(i)=p.*(shuju(i,1))^3; end Dwp2=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','C1:C31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp3=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','D1:D30'); p=1.293; for i=1:30 dwp(i)=p.*(shuju(i,1))^3;

<!-- source_page: 38 -->

end Dwp4=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','E1:E31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp5=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','F1:F30'); p=1.293; for i=1:30 dwp(i)=p.*(shuju(i,1))^3; end Dwp6=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','G1:G31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp7=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','H1:H31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp8=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','I1:I30'); p=1.293; for i=1:30 dwp(i)=p.*(shuju(i,1))^3; end Dwp9=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','J1:J31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp10=sum(dwp)/(2*31)

<!-- source_page: 39 -->

shuju=xlsread('Dpingjunfengsu.xls','K1:K30'); p=1.293; for i=1:30 dwp(i)=p.*(shuju(i,1))^3; end Dwp11=sum(dwp)/(2*31)

shuju=xlsread('Dpingjunfengsu.xls','L1:L31'); p=1.293; for i=1:31 dwp(i)=p.*(shuju(i,1))^3; end Dwp12=sum(dwp)/(2*31) 计算风能利用率程序： clear;clc %%%每日平均风能利用率

k=200; for i=1:31 %%%一月 shuju=xlsread('201501.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A1:AE1')

for i=1:28 %%%二月 shuju=xlsread('201502.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A2:AE2')

<!-- source_page: 40 -->

for i=1:31 %%%三月 shuju=xlsread('201503.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A3:AE3')

k=200; for i=1:31 %%%四月 shuju=xlsread('201504.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A4:AE4')

k=200; for i=1:31 %%%五月 shuju=xlsread('201505.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A5:AE5')

k=200; for i=1:31 %%%六月

<!-- source_page: 41 -->

shuju=xlsread('201506.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A6:AE6')

k=200; for i=1:31 %%%七月 shuju=xlsread('201507.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A7:AE7')

k=200; for i=1:31 %%%八月 shuju=xlsread('201508.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A8:AE8')

k=200; for i=1:30 %%%九月 shuju=xlsread('201509.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11);

<!-- source_page: 42 -->

fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A9:AE9')

for i=1:31 %%%十月 shuju=xlsread('201510.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A10:AE10')

for i=1:30 %%%十一月 shuju=xlsread('201511.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率 liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A11:AE11')

for i=1:31 %%%十二月 shuju=xlsread('201512.xls',i,'B4:L27'); fengsu=shuju(:,2:3:11); fengsu=fengsu(:); gonglv=shuju(:,1:3:10); gonglv=gonglv(:); gonglv=gonglv(find(fengsu>3)); %%%筛选有效功率 pingjungonglv(i)=mean(gonglv); %%%日平均功率

<!-- source_page: 43 -->

liyonglv(i)=pingjungonglv(i)./k; %%%风能利用率 end liyonglv=[liyonglv]; xlswrite('C201503.xls',liyonglv,'A12:AE12') 附录五:计算最大最小风速程序： clear;clc %%%月最大最小值 for i=1:31 shuju=xlsread('201501.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm1(i)=max(fengsu); mm11(i)=min(fengsu); end mmm1=max(mm1) mmm11=min(mm11) %%%

for i=1:28 shuju=xlsread('201502.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm2(i)=max(fengsu); mm22(i)=min(fengsu); end mmm2=max(mm2) mmm22=min(mm22) %%%

for i=1:31 shuju=xlsread('201503.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm3(i)=max(fengsu); mm33(i)=min(fengsu); end mmm3=max(mm3) mmm33=min(mm33) %%%

for i=1:30 shuju=xlsread('201504.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm4(i)=max(fengsu); mm44(i)=min(fengsu); end

<!-- source_page: 44 -->

mmm4=max (mm4)

mmm44=min (mm44)  %%%

for i=1:31
shuju=xlsread( 201505. x1s’, i,  C4:1.27");
fengsu=shuju(:, 1:3:10) ;
fengsu=fengsu(:) ;
mm5 (i) =max (fengsu) ;
mm55 (i) =min (fengsu) ;

end

mmm5=max (mm5)

mmm55=min (mm55)  %%%

for i=1:30
shuju=xlsread( 201506. x1s’, i, C4:1.27");
fengsu=shuju(:, 1:3:10) ;
fengsu=fengsu(:) ;
mm6 (i) =max (fengsu) ;
mm66 (i) =min (fengsu) ;

end

mmm6=max (mm6)

mmm66=min (mm66)  %%%

for i=1:31
shuju=xlsread ( 201507. x1s’, i, C4:1.27");
fengsu=shuju(:, 1:3:10) ;
fengsu=fengsu(:) ;
mm7 (i) =max (fengsu) ;
mm77 (i)=min (fengsu) ;

end

mmm7=max (mm7)

mmm77=min (mm77)  %%%

for i=1:31
shuju=xlsread( 201508. x1s’, i, C4:1.27");
fengsu=shuju(:, 1:3:10) ;
fengsu=fengsu(:) ;
mm8 (i) =max (fengsu) ;
mm88 (i) =min (fengsu) ;

end

mmm8=max (mm8)

mmm88=min (mm88)  %%

44

<!-- source_page: 45 -->

for i=1:30 shuju=xlsread('201509.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm9(i)=max(fengsu); mm99(i)=min(fengsu); end mmm9=max(mm9) mmm99=min(mm99) %%%

for i=1:31 shuju=xlsread('201510.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm10(i)=max(fengsu); mm1010(i)=min(fengsu); end mmm10=max(mm10) mmm1010=min(mm1010) %%%

for i=1:30 shuju=xlsread('201511.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm11(i)=max(fengsu); mm1111(i)=min(fengsu); end mmm11=max(mm11) mmm1111=min(mm1111) %%%

for i=1:31 shuju=xlsread('201512.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); mm12(i)=max(fengsu); mm1212(i)=min(fengsu); end mmm12=max(mm12) mmm1212=min(mm1212) %%% 附录六:计算威布尔参数程序： clear;clc %%%威布尔分布 计算标准差参数

<!-- source_page: 46 -->

for i=1:31 shuju=xlsread('201501.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb1(i)=std(fengsu); end b01=mean(bb1) %%%

for i=1:28 shuju=xlsread('201502.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb2(i)=std(fengsu); end b02=mean(bb2) %%%二月

for i=1:31 shuju=xlsread('201503.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb3(i)=std(fengsu); end b03=mean(bb3) %%%三月

for i=1:30 shuju=xlsread('201504.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb4(i)=std(fengsu); end b04=mean(bb4) %%%四月

for i=1:31 shuju=xlsread('201505.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb5(i)=std(fengsu); end b05=mean(bb5) %%%五月

for i=1:30 shuju=xlsread('201506.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:);

<!-- source_page: 47 -->

bb6(i)=std(fengsu); end b06=mean(bb6) %%%六月

for i=1:31 shuju=xlsread('201507.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb7(i)=std(fengsu); end b07=mean(bb7) %%%七月

for i=1:31 shuju=xlsread('201508.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb8(i)=std(fengsu); end b08=mean(bb8) %%%八月

for i=1:30 shuju=xlsread('201509.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb9(i)=std(fengsu); end b09=mean(bb9) %%%九月

for i=1:31 shuju=xlsread('201510.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb10(i)=std(fengsu); end b010=mean(bb10) %%%十月

for i=1:30 shuju=xlsread('201511.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb11(i)=std(fengsu); end b011=mean(bb11) %%%十一月

<!-- source_page: 48 -->

for i=1:31 shuju=xlsread('201512.xls',i,'C4:L27'); fengsu=shuju(:,1:3:10); fengsu=fengsu(:); bb12(i)=std(fengsu); end b012=mean(bb12) %%%十二月

xx=(b01+b02+b03+b04+b05+b06+b07+b08+b09+b010+b011+b012)/12 附录七:拟合幂函数系数程序： clear;clc %%%I 型号拟合 x=[3 3.5 4 4.5 5 5.5 6 6.5 7 7.5 8 8.5 9 9.5 10 10.5 11 11.5 12]; y=[27 56.41 96.76 140.1 191.13 254.97 355.13 423.64 527.61 650.08 789.66 951.86

1120.18 1308.91 1516.25 1730.77 1912.29 2003.52 2010]; beta0=[1 1]; [beta,r,J]=nlinfit(x,y,'ff',beta0); beta xx=3.1:0.1:11.5; q=ff(beta,xx)'; plot(x,y,'o',xx,q,'r-') hold on xx=[3.5 4 5 6 7 8 9 10 11]; yy=[40 74 164 293 471 702 973 1269 1544]; beta0=[1 1]; [beta,r,J]=nlinfit(xx,yy,'ff1',beta0); beta aa=3.5:0.1:11; qq=ff1(beta,aa)'; plot(xx,yy,'o',aa,qq,'r-') hold off
