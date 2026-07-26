# 验证与数据质量

## 文档结构审计

```json
{
  "pages": 2,
  "paragraphs": 24,
  "tables": 0,
  "inline_shapes": 0,
  "media_assets": 12,
  "ole_objects": 13,
  "text_characters": 1450,
  "core_properties": {
    "title": "穿越沙漠",
    "creator": "user",
    "lastModifiedBy": "lenovo",
    "revision": "66",
    "lastPrinted": "2020-08-26T14:42:00Z",
    "created": "2020-07-23T04:49:00Z",
    "modified": "2020-09-08T00:27:00Z"
  }
}
```

## 已确认限制

- 含13个MathType OLE对象与11个WMF预览；常规文本提取会漏掉公式
- WMF预览可恢复2、3、n、k(2≤k≤n)、B≠A、2k、1/k、4、0、1等规则符号

## 原始载体完整性

SHA-256 已记录；分析过程中未修改原始文件。
