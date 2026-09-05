# Knowledge Card

## Basic Information

- Paper ID: CUMCM-2017-D-001
- Year: 2017
- Problem: D

## Evidence-based Content

The following excerpt is copied deterministically from the generated paper body; no method or conclusion is inferred beyond this source evidence.

> 本文对某化工厂的巡检线路和排班方案进行了研究。 ||首先，为了实现人力资源消耗量尽可能少，需要巡检路线尽可能短。根据图论知识，建| |---|---| ||立无向赋权图，以 26 个巡检点为顶点集，以
> 巡检点间的连线为边，以两个巡检点之间的走路 时间为权。再把调度中心确定为起点和终点，建立最短路模型，求解时，使用 MATLAB 软件， 依次指定几个中间点，分别求解几次，便得到了连接 26 个巡检点的
> 最短回路，最短回路总时 间是 72 分钟。 其次，以最短回路为基础，统计出各个巡检点对应的累计时间（走路时间和巡检时间累 加）作为时间轴，最短回路的终点所对应的累计时间就是最大累计时间，将它作为分割对
> 象， 于是问题转化为：至少需要几段时间，才能将该最大累计时间全部覆盖掉？于是建立背包模 型，以巡检点的周期为约束条件，以最少段数为目标函数。最少的分段数就是巡检人数。 在最短回路和最少人数的基础上，制
> 定了相应的排班方案和时间表。 将巡检耗时作为人力资源消耗量的测量指标，作为评价排班方案优劣的工具。 为了实现每名工人的工作量尽量均衡，以若干天为周期进行轮岗轮班。 排班结果： （1）固定时间上班，不考
> 虑休息时间的情境下，每班至少需要 4 人，每天三班需要 12 人。4 人的人力资源消耗量不均衡，但三班的人力资源消耗量是均衡的，故以 4 天为周期轮 岗，实现了工作量绝对均衡。每天人力资源总耗费时间为
>  1260 分钟。 （2）固定时间上班，考虑休息时间 10 分钟的情境下，每班至少需要 5 人，每天三班需 要 15 人。5 人的人力资源消耗量是均衡的，但三班的人力资源消耗量不均衡，故以三班为周 期
> 轮班。每天人力资源总耗费时间为 2600 分钟。 （3）错时上班，不考虑休息时间的情境下，每班至少需要 4 人，每天三班需要 12 人。4 人的工作量绝对均衡，且三班的人力资源消耗量也均衡。每天人力资

## Evidence

- Evidence granularity: page
- Source pages represented: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48

## G11 Repair Evidence

This block records deterministic repair provenance only; no semantic claim is inferred.

- Repair stage: G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR
- Repair attempt: 20260905T045418589698Z_557724fba657
- Route categories: MARKER_ONLY_DIAGNOSTIC_OCR_REUSE
- Repaired source pages: 20, 21, 23, 25, 39, 42, 43, 45
- Preserved legitimate noncontent pages: none
- Candidate paper artifact SHA-256: 9591EFE6851C9BF7B5B50CEBF8106990F7D66CE23D20699F42E0D8A40D6C430B
- Source binding: PASS
