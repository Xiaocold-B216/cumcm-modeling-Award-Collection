# 验证与数据质量

## 自动结构审计

```json
{
  "sheet": "二季度",
  "header": [
    "水表名",
    "水表号",
    "采集时间",
    "上次读数",
    "当前读数",
    "用量"
  ],
  "rows": 778195,
  "unique_meters": 91,
  "unique_names": 91,
  "date_min": "2019-04-01T00:00:00",
  "date_max": "2019-06-30T23:45:00",
  "missing_by_column": {
    "水表名": 0,
    "水表号": 0,
    "采集时间": 0,
    "上次读数": 0,
    "当前读数": 0,
    "用量": 0
  },
  "usage_sum": 225519.44,
  "negative_usage_rows": 0,
  "zero_usage_rows": 377547,
  "zero_usage_rate": 0.4851573191809251,
  "read_difference_mismatch_gt_0_011": 1,
  "current_below_previous_rows": 0,
  "consecutive_duplicate_meter_time_rows": 0,
  "interval_minutes_top": [
    [
      15.0,
      774117
    ],
    [
      60.0,
      3985
    ],
    [
      45.0,
      2
    ]
  ],
  "meter_row_count_quantiles": {
    "0": 6566,
    "0.25": 8424.0,
    "0.5": 8736.0,
    "0.75": 8736.0,
    "1": 8736
  },
  "meter_usage_quantiles": {
    "0": 0.0,
    "0.25": 123.61999999999975,
    "0.5": 502.35000000003055,
    "0.75": 1775.8699999999426,
    "1": 45385.75000000012
  },
  "elapsed_sec": 29.5
}
```

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
