# Knowledge Card

## Basic Information

- Paper ID: CUMCM-2017-D-003
- Year: 2017
- Problem: D

## Evidence-based Content

The following excerpt is copied deterministically from the generated paper body; no method or conclusion is inferred beyond this source evidence.

> 本文主要研究化工厂巡检路径规划与排班问题。为提高巡检效率，优化资源 分配，需制定科学合理的巡检路径。通过对化工厂巡检工作内容和特点分析，并 制定相应的目标体系及约束条件，建立了最短路径的多目标规划模型
> ，使用 lingo 和 Excel 求解，得到巡检人员最少的优化方案。 针对问题一：以每班需巡检人员尽可能少，工作量尽可能平衡为目标，以固 时上班、无休息时间、每条线路周期不超过 35min、每天三班
> 制、每班 8 小时左 右为约束，建立多目标规划模型，用图论法求解。先考虑分区，以线路周期内包 含尽可能多巡检点与最短路径为目标，将所给巡检点连通图分组，得到共 5 条巡 检路线，最少需 5 名巡检人员
> ，如路线： 22-21-4-2-1-3-6-14-21 （具体巡检路线见正文图 6，巡检时间表见附录表 1、2、3）。为使每条路线在一 段时间内的总行走时间均衡，引入均衡度，越小越合理。该模型均衡度为
>  0.35 较大，为满足要求，故采用五线三班轮倒制。考虑到该模型在巡检人员每个周期 的回程中浪费大量时间，所以不分区处理，利用最短路径和巡检耗时，得到将巡 检点全部巡检的最少用时。用巡检一周的最少用时
> 与 35min 的比值，得到最少巡 检人数 4 名，该优化模型在固时上班条件下，第二班次巡检人员无法在指定时间 到达指定点，无法形成班次循环，但可在错时上班条件下应用。 针对问题二：在第一问模型基础上
> ，新增每 2 小时左右巡检人员休息 5-10min、 在中午 12 时和下午 6 时需进餐 30 分钟的约束，经分析，巡检人员每 2 小时的休 息时间，可通过减少巡检周期大于 35min 的巡检点巡检
> 次数得到，若线路中无大 于 35min 周期的巡检点或压缩时间太少，可将线路分段并增加巡检人员。最终得 到共 6 条路线，最少需要 6 名巡检人员，如路线: 22-21-4-2-1-2-3-6-14-

## Evidence

- Evidence granularity: page
- Source pages represented: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26

## G11 Repair Evidence

This block records deterministic repair provenance only; no semantic claim is inferred.

- Repair stage: G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR
- Repair attempt: 20260905T045418589698Z_557724fba657
- Route categories: MARKER_ONLY_DIAGNOSTIC_OCR_REUSE
- Repaired source pages: 18
- Preserved legitimate noncontent pages: none
- Candidate paper artifact SHA-256: F8779B61CC13C3C11FED07D5FCF4482B8BF265557B38CC5598E15BC5840CD951
- Source binding: PASS
