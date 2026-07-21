# Schema migration notes

## 1.4.1

向后兼容增加 `document_subtype`、算法统计资格和字段级bbox。未改变carrier、segment、logical document、problem、lineage或representation的含义。

## Parser 0.5.2

修复人工复核脚本曾使用固定A4画布导致的绝对bbox偏差。迁移以已保存的normalized_bbox为准，按每个PDF页面实际MediaBox重算PDF point坐标；稳定ID和人工边界判断不变。
