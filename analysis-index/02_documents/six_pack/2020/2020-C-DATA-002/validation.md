# 验证与数据质量

## 自动结构审计

```json
{
  "sheets": {
    "企业信息": {
      "header": [
        "企业代号",
        "企业名称"
      ],
      "rows": 302,
      "unique_enterprises": 302,
      "rating_counts": {},
      "default_counts": {},
      "missing_by_column": {
        "企业代号": 0,
        "企业名称": 0
      },
      "elapsed_sec": 0.0
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
      "rows": 330835,
      "unique_enterprises": 302,
      "status_counts": {
        "有效发票": 303280,
        "作废发票": 27507,
        " 作废发票": 48
      },
      "date_min_raw": "42651",
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
      "amount_sum": 17333156760.47,
      "tax_sum": 1539221913.54,
      "total_sum": 18872378674.0,
      "numeric_min": [
        -999047.62,
        -160029.59,
        -1101380.0
      ],
      "numeric_max": [
        999999.99,
        169601.44,
        1167257.0
      ],
      "negative_total_rows": 5697,
      "zero_total_rows": 2340,
      "amount_tax_total_mismatch_gt_0_02": 0,
      "duplicate_invoice_numbers_within_contiguous_enterprise_block": 3793,
      "elapsed_sec": 13.35,
      "date_min": "2016-10-08",
      "date_max": "2020-02-21"
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
      "rows": 395175,
      "unique_enterprises": 302,
      "status_counts": {
        "有效发票": 377939,
        "作废发票": 17236
      },
      "date_min_raw": "42651",
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
      "amount_sum": 9241193913.22,
      "tax_sum": 961148146.8,
      "total_sum": 10202342059.13,
      "numeric_min": [
        -970873.79,
        -141102.76,
        -1022995.0
      ],
      "numeric_max": [
        7579487.18,
        1288512.82,
        8868000.0
      ],
      "negative_total_rows": 3630,
      "zero_total_rows": 0,
      "amount_tax_total_mismatch_gt_0_02": 2,
      "duplicate_invoice_numbers_within_contiguous_enterprise_block": 4718,
      "elapsed_sec": 15.76,
      "date_min": "2016-10-08",
      "date_max": "2020-02-21"
    }
  }
}
```

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
