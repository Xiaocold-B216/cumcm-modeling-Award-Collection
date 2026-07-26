# 验证与数据质量

## 自动结构审计

```json
{
  "sheet": "水表层级关系",
  "header": [
    "一级表计编码",
    "二级表计编码",
    "三级表计编码",
    "四级表计编码",
    "水表号",
    "水表名",
    "用户号",
    "用户名",
    "口径"
  ],
  "rows": 93,
  "level_counts": {
    "1": 13,
    "2": 51,
    "3": 25,
    "4": 4
  },
  "unique_meter_ids": 91,
  "duplicate_meter_ids": 0,
  "unique_hierarchy_codes": 94,
  "duplicate_hierarchy_codes": 1,
  "names_suffix_plus": 29,
  "names_suffix_minus": 0,
  "missing_by_column": {
    "一级表计编码": 80,
    "二级表计编码": 40,
    "三级表计编码": 68,
    "四级表计编码": 89,
    "水表号": 2,
    "水表名": 2,
    "用户号": 2,
    "用户名": 2,
    "口径": 2
  },
  "elapsed_sec": 0.0,
  "actual_meter_rows": 91,
  "placeholder_no_record_rows": 2,
  "hierarchy_codes_note": "“无记录”出现2次，是父级占位，不作为重复表计编码。",
  "quarter_meter_coverage": "Q1-Q3的91个表号与层级表91个有效表号完全一致"
}
```

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
