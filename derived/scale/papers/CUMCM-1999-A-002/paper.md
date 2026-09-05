# Extracted Paper

<!-- source_page: 1 -->

回 虽 过
p
数学 的 裤 认识
第 30 郑 第 1 期 数学 的 实践 与 认识 von30 Nu BERAGE
2000 年 ! 月 MATHEMATICS N PRACTICE AND THEORY Jan_ 2000
The M anagem en t of AutomaticLathe
YU Jie, JANGAimin, LIRong-bing
(Nanjing U niversity of A eronautics and A stronautics, Nanjing 210016)
= _
Abstract Optmalmaintenance policy problem in a system is discussed and analysed Sb 为
paper Due to the random variable concerned, one objective mathematicalmodel ofe W
value is developed By using enumerative searchmethod, weobtain op timal po licy 1 cess
is checked once every producing 18 parts W hen the process is checked ines, the'’knife has
to be changed According to this policy, the average mininal cost for I5 cing a part is
4.62¥. 7
Finally, we point out some factors not to be considered in the'n odel, “and analyse the influ-
ence of these factors Moveover, somemodification is X
全 人 r 划
车 床 管 理 优化 模 型
8/ .°
张 继 信 全 方 华 顾 利 龙
指导 栽 谢 。 夏 亚 几
j ee 兰州 730050)
编者 按 : aa
查 周 期 所 满足 的 乔 各 中 人 得 特别 细致 地 注意 到 由 检查 滞后 而 引起 的 成 本 部 分 , 继而 在 定期 更 换 刀 有 具 及 考虑 到
2 章 情况 下 对 成 本 公式 作 了 修正 , 并 用 搜索 法 求 得 了 最 优 解
摘 %: Ha 过 论 了 自动 化 车 床 连续 加 工 零件 工序 定期 检查 和 刀具 更 换 的 最 优 策略
铺 对 问 古方 应 用 管理 成 本 理论 结合 概率 统计 方法 , 建立 定期 检查 调节 零件 的 平均 管理 成 本 的 优化 设计
NN 异型 , 通过 计算 机 求解 、 模拟 , 得 到 工序 设计 效益 最 好 的 检查 间隔 和 刀具 更 换 间隔 针对 问题 二 , 在 问题 一 的
1 也 利用 概率 知识 调整 了 检查 间隔 中 的 不 合格 品 数 带 来 的 平均 损失 , 同时 加 上 了 因 工 序 正常 而 误 认为 有
电 戟 隆 停 机 产生 的 平均 损失 , 然后 建立 起 目标 函数 , 得 到 工序 设计 效益 最 好 的 检查 间隔 和 刀具 更 换 策略 对 于
工序 故障 采用 自动 检查 装置 , 设计 出 了 自动 检查 调节 系统 , 并 给 出 了 算法 框图 , 有 效 地 避免 工序 正常 而 误 认
为 有 故障 停机 损失 , 提高 工序 效益
1 问题 的 重 述 ( 咯 )
2 模型 的 假设
1. 工序 出 现 故 障 是 完全 随机 的 , 生产 任 一 零件 时 出 现 故 障 的 机 会 相同 ;
2. 累积 的 100 次 刀具 故障 记录 中 每 一 个 记录 是 刀具 完成 的 零件 数 , 其 中 有 一 个 不 合格
5)
© 1994-2008 China Academic Jou ectronic Publish e. All rights reserved.  http://www.cnki.net

<!-- source_page: 2 -->

加

1 其 张 继 伟 : 车 床 管理 优化 模型 二
品 ( 即 滞后 数 );

3. 有 完全 充足 的 刀具 可 供 更 换 ;

4. 故障 时 产生 的 零件 损失 费 理解 为 每 产生 不 合格 品 就 损失 的 费用 ;

5. 对 一 个 零件 进行 检查 的 过 程 中 , 生产 并 不 停止 从 生产 开始 到 检查 结束 , 有 1 个 零件
生产 出 来
3 参数 的 说 明

7 一 一 故障 时 产 出 的 每 件 零件 损 撩 嘻 用 , 太 = 200 元 / 件 ; 和 从 》

1 ”一 一 每 次 进行 检查 的 费用 , = 10 元 / 钦 ; evwss

4 一 一 发 现 故 曲 进行 调节 使 恢复 正常 的 平均 费用 , a= 4 AN

丰 一 一 末 发 现 故 障 时 更 换 一 把 新 刀具 的 费用 ,上 = 1000/1K; H

工 “ 一 一 定 间 隔 检查 调节 单位 零件 平均 管理 成 本 ;

7， 一 一 检查 间隔 (生产 多 少 个 零件 检查 一 次 ); X

i re Tnh

厂 ” 一 一 采用 定期 更 换 后 的 平均 故障 间隔 ; 了 X

友 ” 一 一 平均 更 换 刀 具 间 隔 ; %5

三 一 一 考虑 其 它 原因 后 定期 更 换 刀 具 时 的 平均 败 障 间隔 ;

ie 一 由 其 它 原因 产生 的 平均 故障 间隔 ;

7 一 检查 清 后 数 , 即 检查 过 程 中 工 谋 拓 生产 出 的 零件 数

万 一 刀具 寿命 低 于 平均 故 革 证 二 中 的 夫 件 数 的 比率

pi 2
4 问题 分 析 JS-

工序 制造 几 的 棕 作 六 更 是 单 位 进行 计量 要 保持 工序 的 正常 状态 , 就 要 经 常 对 工
序 进 行 检 查 , 所 谓 列 进行 检查 是 通过 对 零件 的 检查 来 施行 的 检查 过 于 频繁 , 自然 能 使
Eiriiopilen % piivirerighy 这 将 使 诊断 费用 过 高 ; 诊断 闻 隔 过 长 , 虽然 可
OCT 这 也 必 将 提高 单
jn 从 而 所 求 问题 就 转化 为 当 检查 间隔 为 多 少时 其 平均 管理 成 本 最 低

YSN
] ar

100 个 数据 进行 统计 分 析 , 利用 X 检验 得 出 这 些 数据 符合 正 态 分 布 V (600，
195.6%).
5.1 问题 1

单位 零件 的 平均 管理 成 本 由 下 列 四 部 分 组 成 ;

IT= 单个 零件 的 平均 检查 费 ;

I= 单个 零件 的 平均 调节 费 ;

IIT= 由 检查 滞后 所 产生 的 不 合格 带 来 的 平均 损失 ;

JIV= 由 检查 间隔 中 的 不 合格 品 带 来 的 平均 损失
o4 @ 1994-2008 C ademic Journal Electronic Publishing House. All rights reserved. http://www.cnkinet

<!-- source_page: 3 -->

加
h,
32 数学 的 实战 与 认识 0 times
因 ， 个 零件 检查 一 次 , 所 以 每 个 零件 所 分 推 到 的 检查 费用 为 pr, 即
广内
由 于 检查 到 故障 时 才 进 行 调节 , 而 平均 每 元 个 零件 出 一 次 故障 , 困 此 , 每 个 零件 所 分 推
到 的 调节 费 是 , 即
I= dA
至 于 JU, 由 于 检查 时 生产 并 不 停止, 而 检查 又 需 一 定时 间 假设 检查 一 个 零件 的 同时 ，
已 又 有 7 个 零件 生产 出 来 因此 , 每 一 次 故障 由 于 检查 滞后 造成 损失 为 /*/, 于 是 每 个 零件
所 分 推 到 的 检查 滞后 损失 为 1 "7 / 亿 即 ; #7
II 7 全 一 A7
最 后 来 分 析 JV, 注意 每 "个 零件 才 检查 一 次 , 在 某 检查 点 一 但 发 释 伯 员 宏 合格 品 —
般 说 来 , 不 合格 品 就 不 只 这 一 个 , 详细 情况 见 下 图
前 一 检查 点 某 of
(1) "oo ”ofOsS、
2) 0 0 0 … 0 Ae
(3) 0 0 0 HA x
(n- 1) 0 X O 机 X X
(n) 4 5 X Q X X pe X
注 1 “0" 代 表 零 件 是 合格 品 :2 代表 不 合格 品
对 于 (D) 情 况 , 恰 在 某 一 检查 点 工序 不 正常, 而 前 面 是 正常 的 因此 , 惟有 一 个 不 合格 :
() 情况 是 在 某 检查 点 的 前 一 全 零件, 工序 开始 不 正常 因此 有 两 个 不 合格 品 , … Cn) 情况 是 ，
在 前 一 个 检查 点 后 , 工序 就 蛮 得 常 了 ， 因 此 , 有 ，” 个 不 合格 品 所 以 , 平均 来 说 , 在 某 个 检查
or 全 个 不 合格 品 由 此 带 来 的 损
失 为 "0 放 友 为 2 个 夫 件 出 一 次 故障 , 因此 每 个 零件 所 分 推 到 的 该 项 损失 是 * 上 。 大 ，
即 : 4
\Y W_ al
所 人 全
NE 可 得 出 定 间隔 检查 调节 单位 零件 的 平均 管理 成 本 的 基本 公式
本
最 好 的 检查 间隔 , 即使 > 达到 最 小 的 w, 两 边 对 ， 求 得
下 和
令 7 = 0, 解 得 :
1 ®
o4 © 1994-2008 China Academic Journal Electronic Publishing House. All rights reserved.  http://www.cnki.net

<!-- source_page: 4 -->

加
人 风
著 天 栓 侯 车 床 衣 再 优化 模 开 13 一
如 果 再 考虑 对 发 现 故 障 进行 调节 等 一 些 细节 , 可 得 最 宣 检查 间隔 ， 的 修正 公式 为
n= 4 2 区 (3)
由 于 检查 滞后 生产 /个 不 合格 品 , 可 取 /= 1 即 生产 出 一 件 不 合格 品 就 确定 工序 不 正
常
由 公式 (D 可 知 要 降低 管理 费用 , 可 让 平均 故障 间隔 增 大 , 定期 更 的 刀具 的 办 法 可 使 平
均 故 障 间隔 增 大 , 不 过 由 于 进行 定期 更 换 刀 具 , 刀具 费 也 将 会 增 训 , 这 样 管理 费用 就 会 增 大 ，
困 此 采用 该 办 法 是 否 合算 的 问题 , 要 通过 计算 米 加 以 验证 A7
由 于 工序 故障 绝 大 部 分 未 自习 具 损 坏 , BLUSf: =Lk
(D 其 它 原因 的 故障 率 Pi= 0.05; 4 \
人 ) 记 刀具 发 生疏 障 时 平均 加 工 的 夫 介 数 低 于 于 伯 的 比率 为 Ph
引入 定期 更 换 后 的 平均 故障 间隔 系数 元 , 那么 ¥
Te
u u u xXY
对 于 普 ,可 作 如 下 估算 2
一 a Xar® JiC
“T e : 深
另外 , 工序 故障 可 能 由 其 它 原因 引起 虽 它 仅 占 5%6 ,但 也 要 考虑 进去 , 则 定期 更 换 刀 具
平均 故障 间隔 7 可 由 下 式 给 出 :
一 关 品 数 网 二  5 总 故障 数 。 ” ，。 工
we = Toe hikdr/b i 六 其 它 故障 数 “““ 吕 /
定期 更 换 刀 具 时 平均 故障 间隔 观 f 最 ,7 的 调和 平均
一 “一 1]
TS 一 开工
u uE
问题 1 的 模型 为 := y
1] o
令 gaaeanmy
SU 0 全 ©
Ya /
AR
N 12( 王 + Dr
_— 人 (7)
对 该 模型 的 求解 可 通过 计算 机 编程 进行 一 维 搜索 实现 , 其 结果 为 : 最 宣 检查 间隔 六
15( 介 ), 最 佳 换 刀 间隔 邱 - 365( 件 ), 最 小 单位 零件 的 平均 管理 成 本 / = 4. 65( 元 )
5.2 问题 2( 咯 )
5.3 问题 3
设计 安装 工序 自动 检查 调节 装置 , 对 每 个 零件 进行 检查 , 假设 检查 费 为 零 下 面 给 出 的
自动 检查 调节 系统 可 以 有 效 导 免 问题 > 中 正常 工序 而 误 认 为 政 障 停机 产生 的 损失 , 从 而 降
-2008 China Academic rnal Electronic Publishing House. All rights reserved ttp， ww.cnki.net

<!-- source_page: 5 -->

加
后
34 数学 的 实践 与 认识 0 着
低 单 位 零件 的 平均 管理 成 本
设 ” 为 自动 检查 调节 装置 统计 的 件数 , 本 系统 按 顺序 检查 ”个 零件 出 现 的 不 合格 品 数
必 ,建立 动态 检查 模式 , 自动 记录 按 顺序 检查 的 ”和 ) 个 零件 中 出 现 的 不 合格 品 数 靖 , 并 且
自动 记录 工序 正常 时 所 检查 的 零件 数 上 有 以 下 四 种 情况 :
1. 顺序 统计 的 ， 个 零件 , 次 品 率 低 于 2% , 认为 工序 正常 , 继续 生产 ;
2. 顺序 统计 的 个 零件 , 次 品 率 高 于 2% 低 于 60% , 但 所 有 已 检查 零件 的 次 品 率 低 于
2% , 认为 工序 正常 , 继续 生产 ;
3. 顺序 统计 的 二 个 零件 , 次 品 率 高 于 60% 四 所 有 已 检查 地 件 的 次 品尝 作 R 认为
工序 正常 , 继续 生产 : AY
4. WRFFGET) n DZAFRGEET 60% , 并 且 所 有 检查 零件 的 痪 来 高 让 jp%% ,认为
工序 故障 , 系统 自动 发 出 信号 并 进行 调节 (算法 框图 略 ) y4 } J
6 模型 的 优 缺 点 X
优点 :
(1) 本文 建 模 思 想 易于 理解 , 模型 可 操作 性 强 ， 有 人
(2) 所 建 两 个 模型 的 平均 管理 成 本 目标 函数 旦 村上 条 绑 形态 , 由 计算 机 求解 极 小 值 , 所
得 结果 稳定 性 强 , 而 且 得 到 的 解 与 实际 情况 相 吻 合 : 能 腹 : 一 般 的 常识 解释
(3) 本 文 用 到 的 数学 方法 (一 般 的 概率 统计 知识 和 一 元 函数 求 极 值 ) 都 比较 简单
(4) 由 对 已 往 数 据 通过 概率 统计 建立 的 异型 , 得 出 的 结论 对 以 后 工序 长 期 生产 有 指导 价
值 $, / ©
缺点 :
人 件 的 影响 , 降低 了 模型 的 实用 性 ;
(2) 零件 生产 过 程 的 过 纪 性 有 所 欠 钠 ， 在 模型 的 改进 上 扩展 性 不 是 太 强
参考 文献 ¥
[1 沈 恒 范 . 概率 论 写 数理 绑 让 教程 (第 三 版 ) 高 等 教育 出 版 社 , 北京, 199s
D] 2 现代 质量 管理 统计 方法 ， 期刊 出 版 社 , 北京, 1988
0G] X. 高 等 教育 出 版 社 ,北京 1998
[4] VSHCRUTRI . 清华 大 学 出 版 社 , 北 京 , 1998
[5 机 晶 松村 SNG 语言 科学 与 工程 程序 库 .电子 工业 出 版 社 , 北京 ,1992
淮
N The Optinum M odel of Lathe Management
ZHANG Jiwei, HAN Fang-hua, GU Lilong
(Gansu U niversity of Technology, Lanzou 730050)
o4 ©1 201 hina Academi u Electronic Publishing Hous 1 rights reserve ttp://www.cnki.net

<!-- source_page: 6 -->

Eiis:
RE
第 30 卷 第 1 其 数学 的 实践 与 认识 Vol30 NO 加”
2000 年 ! 月 MATHEMATICS N PRACTICE AND THEORY Jan 2000.
Abstract 了 the article, theoptmum tactics of the regular check to working procedures and the
replacement of cutting tools in the course of continipus componentprocessing by automatic lathes
has been disscussed
For question one, the optm um modelof average management cost used for regular check and
adjustm ent of component has been made out by applying the theory of management cost and
method of probability statistics, the best designed interval of check and cutting tools replacem ent
in theworking procedure has been obtained
For question two,based on question one, the objective functions has been established, and the
optm um tactics of the best designed interval of check and thd replacem ent of os has
been obtained considering the average loss brought about by unqualified products at the i 让
of check and the average loss of machine stop for being m isregarded as existi rodg)
The autom atic checking and adjusting system the breakdow n oo has been
designed by using autom atic devices, and the algorithm flow chart has AR the
loss ofm achine stop for beingm isregarded as existing breakdow n Way be avoided, and the ben-
efit of working procedure would be increased
RS
自 动 化 车 管理
石 做 “ 柯 友 ， 方 庆
< 佛 卫 教师。 数 模 组
4
Gsr 学 ， 武 汉 430033)
A' = 一 7
编者 按 : ”该 文思 路 正确 ， 1 面 , 对 问题 一 给 出 了 正确 的 模型 和 结果 , 并 对 检查 方式 、 灵敏度 分 析 , 误
差分 析 进 行 了 详细 过 论 本 文 列 -特色 是 进行 了 计算 机 模拟 , 这 对 许多 类 似 的 问题 都 行 之 有 效 本 文 缺 点 是
对 问题 二 的 模型
摘要 : 他 o 中 wonmarraeweamanonaaonoaananrrems
损失 最 守 的 一 个 优化 冰 题 , 并 提供 了 有 效 算法 对 问题 一 , 得 到 检查 间隔 T- 18, 定期 换 刀 间隔 了 = 342, 相应
的 齐 ( 作 j 损失 费用 C= 4. 75 元 的 最 优 解 , 并 用 蒙特 卡 罗 法 对 结果 进行 了 模拟 检验 对 问题 二 , 得 到 检
E0  oe T 定 期 换 万 间隔 站 = 242, 单个 零件 期 望 损失 费用 C= 7. 22 元 对 问题 三 , 我 们 采用 新 的 改进 方
¥y 使 单个 零件 期 望 损 失 费 用 降 为 5. 34 元 本 文 还 对 变 检查 间隔 参数 灵敏 性 , 误差 分 析 等 进行 了 讨论
Na 的 重 述 ( 略 )
2 问题 的 分 析
由 于 刀具 损坏 等 原因 会 使 工序 出 现 故障 , 工序 出 现 故障 是 完全 随机 的 工作 人 员 通 过 检
查 零 件 来 确定 工序 是 否 出 现 故障 , 并 且 计划 在 刀具 加 工 一 定 件数 的 零 件 后 定期 更 新 刀具
因此 , 给 定 检查 间隔 , 对 零件 作 检查 , 当 发 现 零件 不 合格 时 则 认为 工序 发 生 了 故障 并 立
即 进行 停机 检查 , 若 实际 存 在 故障 则 进行 修理 , 无 故障 则 继续 生产 ; 当 检 查 发 现 零件 合格 则
人工 涉 设备 的 工作 当 到 了 定期 更 换 刀 有 具 时 刻 , 即使 设备 未 出 现 故障 , 也 进行 刀具 更 新
6 -2 ina Ac ic Journ ectronic lishing Hou ll right erve tp://w nki.nef

