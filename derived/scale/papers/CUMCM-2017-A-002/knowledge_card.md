# Knowledge Card

## Basic Information

- Paper ID: CUMCM-2017-A-002
- Year: 2017
- Problem: A

## Evidence-based Content

The following excerpt is copied deterministically from the generated paper body; no method or conclusion is inferred beyond this source evidence.

> 摘要 本文针对CT系统参数标定和未知介质信息的确定问题，基于黄金分割法、 单目标优化模型、搜索算法、图像重建算法，求出了CT系统的旋转中心、探测 器单元距离和射线的 180 个方向。根据标定的系统参数
> ，求出了与接收数据对应 的未知介质的位置、几何形状和吸收率。最后设计了新模板，对系统参数的精度 和稳定性进行了改进。 对于探测器单元距离的求解问题，根据几何关系可以求出介质厚度的理论值， 基于此建立单
> 目标优化模型，目标函数为相邻接受信息理论比值与实际比值的最 小误差平方和，遍历射线到介质边缘的距离，决策变量为探测器单元距离。通过 黄金分割算法，逐渐缩小探测器单元距离范围直到满足精度要求，求得探测器
> 单 元距离为0.2768𝑚𝑚。 对于CT系统旋转中心位置的确定问题，首先建立以椭圆中心为原点的直角 坐标系，以短轴向右建立𝑥轴，长轴向上建立𝑦轴。建立单目标优化模型，目标 函数为相邻接受信息理论比值与
> 实际比值的最小误差平方和，决策变量为穿透介 质的第一条射线到介质边缘的距离。通过遍历搜索算法，找到最优距离。然后根 据射线之间的间距建立中心线方程组。分别研究射线平行𝑥，𝑦轴入射时的情况， 得到旋转中
> 心的坐标为(−9.3040,6.2149)。 对于射线的 180 个方向的确定问题，首先通过最小二乘法原理求得接收数据 与厚度之间的比例系数为1.7725。对于一个方向的射线，通过Radon变换求得 
> 512 个介质厚度值，通过比例系数得到接收数据的理论值，建立单目标优化模型，目 标函数为接收数据的理论值与实际值的最小误差平方和，决策变量为射线与𝑥轴 正方向的夹角，通过遍历搜索算法，求得误差最小的方
> 向夹角。通过迭代法解得 180 个方向与𝑥轴正方向的夹角。 对于未知介质的位置、几何形状和吸收率的求解问题，基于中心切片定理， 设计了滤波反投影求解算法。首先根据反投影算法重建图像，然后进行滤波和降 

## Evidence

- Evidence granularity: page
- Source pages represented: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29

## G11 Repair Evidence

This block records deterministic repair provenance only; no semantic claim is inferred.

- Repair stage: G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR
- Repair attempt: 20260905T045418589698Z_557724fba657
- Route categories: MARKER_ONLY_DIAGNOSTIC_OCR_REUSE
- Repaired source pages: 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 22
- Preserved legitimate noncontent pages: none
- Candidate paper artifact SHA-256: 6F6D3D34F97A43DCAEF36D41BE488C47AB63E4714968E66E53D83219F71D048D
- Source binding: PASS
