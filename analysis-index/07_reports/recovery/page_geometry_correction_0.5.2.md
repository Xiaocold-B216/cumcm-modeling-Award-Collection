# 页面证据几何校正（Parser 0.5.2）

## 问题

早期人工复核辅助脚本中的部分页面区域使用固定的 595.22×842 pt 工作画布。实际载体并不统一：例如1997年代表页为584×789 pt、1998年代表页为598×793 pt、1999年代表页为475×705 pt。页码、人工边界判断及 `normalized_bbox` 未丢失，但部分绝对PDF point坐标存在比例偏差。

## 修复

- Schema保持1.4.1；Parser以兼容补丁升级至0.5.2。
- 以各物理PDF每一页的实际MediaBox为准。
- 以既有 `normalized_bbox` 作为人工判断的权威位置，重算segment、boundary、orphan、page map、evidence及可视化目录的绝对坐标。
- 不改变logical document、segment、relation或representation的稳定ID。
- 不改变人工确认的文章身份、边界归属和字段结论。

## 回归结果

- 1992—1998全部页面segment已重新核对。
- segment与实际PDF MediaBox不一致数：0。
- 原始资料修改数：0。
- 单元测试：34/34通过。
- `--resume`复跑复用了既有哈希和文本缓存，没有执行全库OCR。

本报告记录的是坐标实现错误修复，不表示扩大了人工全文解析范围。
