# 2017处理前远端状态对账

## 结论

远端 `progress.json` 不能作为唯一事实来源。年度报告、quality gate和checkpoint显示：

- 1992-2009可视为连续、远端读回验证通过的可信区间；
- 2010仅为`conditional_pass`，仍有19项人工复核；
- 2011虽然被旧progress声明为完成，但年度报告、gate和checkpoint未观察到；
- 2012-2016年度quality gate未观察到；
- 因而2017按“非连续独立年度”处理，不能把连续完成年份推进到2017。

## 控制策略

1. `last_verified_complete_year`保持2009。
2. 2017即便收到子集全部通过，也因12个可信基线论文载体缺失而只能为`conditional_pass`。
3. 2017上传并远端读回前，`remote_readback_verified=false`。
4. 不覆盖或美化2010-2016的缺口状态。
