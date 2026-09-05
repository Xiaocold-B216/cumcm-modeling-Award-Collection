# Knowledge Card

## Basic Information

- Paper ID: CUMCM-2016-C-001
- Year: 2016
- Problem: C

## Evidence-based Content

The following excerpt is copied deterministically from the generated paper body; no method or conclusion is inferred beyond this source evidence.

> 摘要 本文是关于电池剩余放电时间的预测问题。根据题目所给的附件，分别考虑 不同电流对应的放电曲线，我们首先通过最小二乘法建立不同电流放电曲线的指 数函数模型，然后利用 *MATLAB* 计算出各放电曲
> 线的平均相对误差（ *MRE* ）， 最后预测了衰减状态 3 的剩余放电时间。 基本上是开始变化较慢，而到了某个阶段突然变化加快，这符合指数函数模型， *dut* =*btu* = *abt* +*c
> t* + *d* 即 *dt* *ae* + *c*。对其求积分即可得到电压和时间的关系为 *t* *b e* ，利用最小二 乘法求出各系数，得到 20A、30A 等电流时电压和时间关系。利用求得关系
> 式， 231 *R*t-*R₀* å*REi* 把电压带入即可得到各电压对应的时间，然后利用*RE* = *R* ，*MRE* =*i*=1 计算各电 t231 流强度的 MRE 分别为：（0.060
> 1、0.0508、 0.0367、0.0338、0.0631、0.0069、 0.0773、0.0063、0.0050）。把电压等于 9.8V 时带入模型可求得 30A、40A、50A、 60A 和 
> 70A 对应的剩余放电时间：（1918.1226min、1224.3761min、929.2559min、 739.6344min、615.8148min）。 针对问题二：首先，对问题 1 中的不同电
> 流对应的参数进行分析，发现参数 2 与电流的关系在 20A 到 50A 之间符合二次函数模型 *f* (*I*) = *gI* +*hI* + *r* ，在 50A 到 100A 之间符合一次函数模型
>  *f* (*I*) = *hI* + *r*，进一步根据最小二乘法，利用 MATLAB 计算出各参数的值，建立了各参数和电流之间的关系式。这样建立了电压和电流 *b*(*I*)*t* 强度及放电时间

## Evidence

- Evidence granularity: page
- Source pages represented: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22

## G11 Repair Evidence

This block records deterministic repair provenance only; no semantic claim is inferred.

- Repair stage: G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR
- Repair attempt: 20260905T045418589698Z_557724fba657
- Route categories: MARKER_ONLY_DIAGNOSTIC_OCR_REUSE
- Repaired source pages: 7
- Preserved legitimate noncontent pages: none
- Candidate paper artifact SHA-256: F6D924F7C205B05804C6D3371F96D8AA883AE9A20131FA6EDE6426072099A0C5
- Source binding: PASS
