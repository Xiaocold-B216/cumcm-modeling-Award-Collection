# 1998年优秀论文语料候选报告

> 本报告由相同可信基线重新构建。自动结果是保守候选，不等同于人工全文核验。

## 对象构成

- logical documents：16
- award papers候选：0
- expert commentaries候选：2
- problem statements候选：14
- solution summaries候选：0
- unknown/other：0

## 状态边界

- 待人工复核：2
- 扫描或无完整文本层的文档保持 `pending_manual_review` 或 `partially_parsed`。
- 自动未命中的字段记为 `unknown`；仅完整原生文本的字段允许进入present/absent分母。
- 合集和分卷尚未人工确认边界时，不将载体数解释为论文数。

## 模型与算法候选

模型标签与算法标签仅来自原生文本关键词，用于复核排序，不作为最终方法结论。
