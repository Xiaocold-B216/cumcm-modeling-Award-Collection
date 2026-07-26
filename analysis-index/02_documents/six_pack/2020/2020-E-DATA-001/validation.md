# 验证与数据质量

## 自动结构审计

```json
{
  "sheet": "一季度",
  "header": [
    "水表名",
    "水表号",
    "采集时间",
    "上次读数",
    "当前读数",
    "用量"
  ],
  "rows": 729283,
  "unique_meters": 91,
  "unique_names": 91,
  "date_min": "2019-01-01T00:15:00",
  "date_max": "2019-03-31T23:45:00",
  "missing_by_column": {
    "水表名": 0,
    "水表号": 0,
    "采集时间": 0,
    "上次读数": 0,
    "当前读数": 0,
    "用量": 0
  },
  "usage_sum": 147107.05,
  "negative_usage_rows": 0,
  "zero_usage_rows": 381472,
  "zero_usage_rate": 0.5230781466179796,
  "read_difference_mismatch_gt_0_011": 0,
  "current_below_previous_rows": 0,
  "consecutive_duplicate_meter_time_rows": 0,
  "interval_minutes_top": [
    [
      15.0,
      725620
    ],
    [
      60.0,
      3572
    ]
  ],
  "meter_row_count_quantiles": {
    "0": 574,
    "0.25": 8124.0,
    "0.5": 8639.0,
    "0.75": 8639.0,
    "1": 8639
  },
  "meter_usage_quantiles": {
    "0": 0.0,
    "0.25": 81.48000000000161,
    "0.5": 354.2699999999969,
    "0.75": 1484.5300000000097,
    "1": 33809.49000000005
  },
  "elapsed_sec": 27.35
}
```

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
