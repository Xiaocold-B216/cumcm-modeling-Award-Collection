# 验证与数据质量

## 自动结构审计

```json
{
  "sheet": "三季度",
  "header": [
    "水表名",
    "水表号",
    "采集时间",
    "上次读数",
    "当前读数",
    "用量"
  ],
  "rows": 791844,
  "unique_meters": 91,
  "unique_names": 91,
  "date_min": "2019-07-01T00:00:00",
  "date_max": "2019-09-30T23:45:00",
  "missing_by_column": {
    "水表名": 0,
    "水表号": 0,
    "采集时间": 0,
    "上次读数": 0,
    "当前读数": 0,
    "用量": 0
  },
  "usage_sum": 268394.810001,
  "negative_usage_rows": 0,
  "zero_usage_rows": 365125,
  "zero_usage_rate": 0.4611072382944115,
  "read_difference_mismatch_gt_0_011": 0,
  "current_below_previous_rows": 0,
  "consecutive_duplicate_meter_time_rows": 0,
  "interval_minutes_top": [
    [
      15.0,
      787798
    ],
    [
      60.0,
      3955
    ]
  ],
  "meter_row_count_quantiles": {
    "0": 7836,
    "0.25": 8646.0,
    "0.5": 8832.0,
    "0.75": 8832.0,
    "1": 8832
  },
  "meter_usage_quantiles": {
    "0": 0.30000000000000004,
    "0.25": 123.79500000000121,
    "0.5": 560.3499999999925,
    "0.75": 1933.5099999999716,
    "1": 64573.17999999991
  },
  "elapsed_sec": 29.65
}
```

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
