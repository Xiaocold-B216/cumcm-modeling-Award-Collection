# 验证与数据质量

## 自动结构审计

```json
{
  "sheets": {
    "企业信息": {
      "header": [
        "企业代号",
        "企业名称",
        "信誉评级",
        "是否违约"
      ],
      "rows": 123,
      "unique_enterprises": 123,
      "rating_counts": {
        "A": 27,
        "C": 34,
        "B": 38,
        "D": 24
      },
      "default_counts": {
        "否": 96,
        "是": 27
      },
      "missing_by_column": {
        "企业代号": 0,
        "企业名称": 0,
        "信誉评级": 0,
        "是否违约": 0
      },
      "elapsed_sec": 0.0
    },
    "进项发票信息": {
      "header": [
        "企业代号",
        "发票号码",
        "开票日期",
        "销方单位代号",
        "金额",
        "税额",
        "价税合计",
        "发票状态"
      ],
      "rows": 210947,
      "unique_enterprises": 123,
      "status_counts": {
        "有效发票": 203339,
        "作废发票": 7608
      },
      "date_min_raw": "42647",
      "date_max_raw": "43882",
      "missing_by_column": {
        "企业代号": 0,
        "发票号码": 0,
        "开票日期": 0,
        "销方单位代号": 0,
        "金额": 0,
        "税额": 0,
        "价税合计": 0,
        "发票状态": 0
      },
      "amount_sum": 9673216141.17,
      "tax_sum": 1320091656.31,
      "total_sum": 10993307624.93,
      "numeric_min": [
        -9823008.85,
        -1452991.45,
        -11100000.0
      ],
      "numeric_max": [
        9999984.51,
        1699990.41,
        11699934.0
      ],
      "negative_total_rows": 1751,
      "zero_total_rows": 0,
      "amount_tax_total_mismatch_gt_0_02": 2,
      "duplicate_invoice_numbers_within_contiguous_enterprise_block": 818,
      "elapsed_sec": 8.34,
      "date_min": "2016-10-04",
      "date_max": "2020-02-21"
    },
    "销项发票信息": {
      "header": [
        "企业代号",
        "发票号码",
        "开票日期",
        "购方单位代号",
        "金额",
        "税额",
        "价税合计",
        "发票状态"
      ],
      "rows": 162484,
      "unique_enterprises": 123,
      "status_counts": {
        "有效发票": 151278,
        "作废发票": 11159,
        " 作废发票": 47
      },
      "date_min_raw": "42650",
      "date_max_raw": "43882",
      "missing_by_column": {
        "企业代号": 0,
        "发票号码": 0,
        "开票日期": 0,
        "购方单位代号": 0,
        "金额": 0,
        "税额": 0,
        "价税合计": 0,
        "发票状态": 0
      },
      "amount_sum": 13863248246.74,
      "tax_sum": 1755572022.08,
      "total_sum": 15910964488.47,
      "numeric_min": [
        -999771.52,
        -169961.16,
        -1169732.68
      ],
      "numeric_max": [
        3978956.9,
        636633.1,
        4615590.0
      ],
      "negative_total_rows": 8556,
      "zero_total_rows": 1679,
      "amount_tax_total_mismatch_gt_0_02": 1,
      "duplicate_invoice_numbers_within_contiguous_enterprise_block": 4437,
      "elapsed_sec": 6.29,
      "date_min": "2016-10-07",
      "date_max": "2020-02-21"
    }
  }
}
```

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
