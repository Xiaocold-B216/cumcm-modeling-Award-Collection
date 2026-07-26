# 2015-2025 Annual Test Integrity Audit

## Scope and input

- Input HEAD: `66af72432901aec7068942d09aee41c8bf0ac8f2`
- Annual files reviewed: `11`
- Test functions reviewed: `267`
- This stage records recommendations only. No annual test, business fact, gate, checkpoint, report, queue, or progress file was modified.

## Summary

- Functions with a validation-strength risk: `22`
- `bom_handling`: `69`
- `confuses_global_and_annual_queue`: `9`
- `depends_on_total_queue_rows`: `7`
- `narrows_scan_scope`: `1`
- `only_checks_file_existence`: `12`
- `page_upper_bound_checked`: `22`
- `rejects_all_empty_csv`: `2`
- `schema_or_current_fact_conflict`: `13`
- `sheet_actual_upper_bound_checked`: `2`
- `uses_hardcoded_quantities`: `146`

## File inventory

- `tests/test_2015_manual.py` — 36 test functions; SHA-256 `c275c9d04fcd660961d05afaa1680b12773fcc55cf5da160f49f85822fdbcd67`; BOM `false`; LF ending `true`.
- `tests/test_2016_manual.py` — 28 test functions; SHA-256 `5ae4d76c0adc51059cc102b6e014a7861682a115f30040488587ead06da03f1b`; BOM `false`; LF ending `true`.
- `tests/test_2017_manual.py` — 24 test functions; SHA-256 `da40dea3f422650a7c7a8d38987950458e88489482076424a9c223b6b41e87dd`; BOM `false`; LF ending `true`.
- `tests/test_2018_manual.py` — 16 test functions; SHA-256 `c6b61e63db172bf840395a489786e5370a914f0a6d70f9962973b96efab3c6ba`; BOM `false`; LF ending `true`.
- `tests/test_2019_manual.py` — 11 test functions; SHA-256 `3f31a5d09104f194f237b034dded8a5c3df3c3cc62680329e65bab67c06796b7`; BOM `false`; LF ending `true`.
- `tests/test_2020_manual.py` — 32 test functions; SHA-256 `66a55e11aa7948a9169eb25611358ea6ec49739b335c91a3fdd4072cf5ffd6a8`; BOM `false`; LF ending `true`.
- `tests/test_2021_manual.py` — 20 test functions; SHA-256 `ec8622bea1fd7dd984615fa63d6a95f2fa65ef3d3c9625b0c252cbe2ffb4a3fd`; BOM `false`; LF ending `true`.
- `tests/test_2022_manual.py` — 24 test functions; SHA-256 `a9512668697538d339650d26ac81199dd0ca52f87085c3e98779c3f1a9d91e24`; BOM `false`; LF ending `true`.
- `tests/test_2023_manual.py` — 28 test functions; SHA-256 `c68a576bc5cad6a294fc8d0651048622d3bc24ef5e1653d574f09b1d3358e914`; BOM `false`; LF ending `true`.
- `tests/test_2024_manual.py` — 24 test functions; SHA-256 `831ccf061b90c00f9f6bb66eeb33891c6fa579f43b66f629476edd973fa8db39`; BOM `false`; LF ending `true`.
- `tests/test_2025_manual.py` — 24 test functions; SHA-256 `7e42e3ccfdf7589396a669cdddc9bf4a018f6c125d3d3e899cd9d84e2ba88f1d`; BOM `false`; LF ending `true`.

## Function-by-function justification

### tests/test_2015_manual.py

#### `test_01_required_files_exist` (lines 21-25)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert all(p.is_file() for p in required)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:21-25
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_02_json_jsonl_structures` (lines 27-31)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:27-31
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_03_csv_structures` (lines 33-39)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert rows`
- 问题：对扫描到的所有 CSV 要求 rows 非空，可能把语义上允许空的 CSV 判错。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:33-39
- 建议的新断言：按 CSV 文件 schema/语义决定空文件是否允许，并对 header/状态分别断言。
- 是否降低测试强度：`false`

#### `test_04_sha256_coverage_and_format` (lines 41-45)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`c=read_jsonl(AN/'01_inventory/2015_carrier_manifest.jsonl'); assert len(c)==29 and len({x['carrier_id'] for x in c})==29 | assert all(re.fullmatch(r'[0-9a-f]{64}',x['sha256']) for x in c)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:41-45
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_05_source_snapshot_unmodified` (lines 47-51)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`s=json.loads((AN/'00_control/2015_source_hash_snapshot.json').read_text()); assert s['source_modified_count']==0 and len(s['files'])==29 | assert all(x['pre_sha256']==x['post_sha256'] and not x['modified'] for x in s['files'])`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:47-51
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_06_logical_document_count_and_ids` (lines 53-53)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`def test_06_logical_document_count_and_ids(): assert len(docs())==28 and len({x['logical_document_id'] for x in docs()})==28`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:53-53
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_07_roles_legal_and_counts` (lines 55-55)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`def test_07_roles_legal_and_counts(): assert Counter(x['role'] for x in docs())==Counter({'paper':18,'dataset':6,'problem':4})`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:55-55
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_08_problem_distribution` (lines 57-57)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`def test_08_problem_distribution(): assert Counter(x['problem_id'] for x in docs() if x['role']=='paper')==Counter({'2015_A':6,'2015_B':5,'2015_C':4,'2015_D':3})`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:57-57
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_09_unknown_not_absent_policy` (lines 59-61)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert all(x['award_level']=='unknown' and x['authors_status']=='not_observed' for x in docs())`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:59-61
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_10_representation_count_and_references` (lines 63-67)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert len(r)==29 and {x['carrier_id'] for x in r}=={x['carrier_id'] for x in c}`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:63-67
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_11_exactly_one_preferred_representation` (lines 69-75)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert len(by)==28 and all(sum(bool(r['is_preferred']) for r in rs)==1 for rs in by.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:69-75
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_12_duplicate_representation_resolution` (lines 77-81)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert len(g)==2 and len({x['file_sha256'] for x in g})==2 and len({x['normalized_text_or_data_sha256'] for x in g})==1 and len({x['render_sequence_sha256'] for x in g})==1`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:77-81
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_13_no_other_duplicate_group` (lines 83-85)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); assert sum(x.get('duplicate_group_id') is not None for x in r)==2`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:83-85
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_14_lineage_counts_and_links` (lines 87-91)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`l=read_jsonl(AN/'04_relations/2015_solution_lineages.jsonl'); assert len(l)==18 and len({x['solution_lineage_id'] for x in l})==18 | assert all(len(x['logical_document_ids'])==1 for x in l)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:87-91
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_15_problem_paper_relations` (lines 93-97)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`s=[x for x in read_jsonl(AN/'04_relations/2015_relations.jsonl') if x['relation_type']=='solves']; assert len(s)==18 | assert Counter(x['target_document_id'] for x in s)==Counter({'2015_PROBLEM_A':6,'2015_PROBLEM_B':5,'2015_PROBLEM_C':4,'2015_PROBLEM_D':3})`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:93-97
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_16_segment_count_consistency` (lines 99-103)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`s=read_jsonl(AN/'03_segments/2015_segments.jsonl'); r=read_jsonl(AN/'04_relations/2015_representations.jsonl'); assert len(s)==625 | c=Counter(x['representation_id'] for x in s); assert all(c[x['representation_id']]==x['segment_count'] for x in r)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:99-103
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_17_preferred_segment_count` (lines 105-109)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert sum(x['representation_id'] in p for x in s)==599`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:105-109
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_18_page_bounds_valid` (lines 111-117)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`if s['segment_type']=='page': assert b['x0']==0 and b['y0']==0 and b['x1']>0 and b['y1']>0 and s['page_number']>=1`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:111-117
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_19_sheet_bounds_valid` (lines 119-123)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`ss=[s for s in read_jsonl(AN/'03_segments/2015_segments.jsonl') if s['segment_type']=='sheet_region']; assert len(ss)==3 | assert all(1<=s['bounds']['row_start']<=s['bounds']['row_end'] and 1<=s['bounds']['col_start']<=s['bounds']['col_end'] for s in ss)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；工作表区域只检查起点/内部 row-column 关系，没有验证实际 sheet 行列上界。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:119-123
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：从实际 workbook representation 读取 sheet dimensions，并验证 row/column 上界。
- 是否降低测试强度：`true`

#### `test_20_no_duplicate_page_segments` (lines 125-127)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`s=[x for x in read_jsonl(AN/'03_segments/2015_segments.jsonl') if x['segment_type']=='page']; k=[(x['representation_id'],x['page_number']) for x in s]; assert len(k)==len(set(k))`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:125-127
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_21_six_pack_complete` (lines 129-133)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert len(ds)==28 and all(req<={x.name for x in d.iterdir() if x.is_file()} for d in ds)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:129-133
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_22_six_pack_metadata_matches_csv` (lines 135-139)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`m=json.loads((AN/'02_documents/document_cards/2015'/r['logical_document_id']/'metadata.json').read_text()); assert m['logical_document_id']==r['logical_document_id'] and m['role']==r['role']`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:135-139
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_23_card_preferred_rep_matches_relation` (lines 141-145)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`for d,i in p.items(): assert json.loads((AN/'02_documents/document_cards/2015'/d/'metadata.json').read_text())['preferred_representation_id']==i`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:141-145
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_24_methods_have_valid_documents_and_pages` (lines 147-151)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`m=read_jsonl(AN/'05_knowledge/methods/2015_methods.jsonl'); d={x['logical_document_id']:int(x['page_or_region_count']) for x in docs()}; assert len(m)>=100 | assert all(x['logical_document_id'] in d and x['evidence_pages'] and min(x['evidence_pages'])>=1 and max(x['evidence_pages'])<=d[x['logical_document_id']] for x in m)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:147-151
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_25_methods_cover_all_papers` (lines 153-155)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`m=read_jsonl(AN/'05_knowledge/methods/2015_methods.jsonl'); assert {x['logical_document_id'] for x in m}>={x['logical_document_id'] for x in docs() if x['role']=='paper'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:153-155
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_26_expert_feedback_not_fabricated` (lines 157-159)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`r=read_jsonl(AN/'05_knowledge/expert_feedback/2015_feedback.jsonl'); assert len(r)==1 and r[0]['feedback_status']=='not_observed'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:157-159
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_27_visualization_records` (lines 161-163)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`r=read_jsonl(AN/'05_knowledge/visualizations/2015_visualizations.jsonl'); assert len(r)>=20 and all(x['documents'] for x in r)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:161-163
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_28_statistics_consistent` (lines 165-173)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert (int(s['physical_carriers']),int(s['logical_documents']),int(s['representations']))==(29,28,29) | assert (int(s['solution_papers']),int(s['problem_statements']),int(s['datasets_supporting']))==(18,4,6) | assert (int(s['representation_segments']),int(s['logical_preferred_segments']))==(625,599)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:165-173
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_29_quality_gate_conditional_and_blocked` (lines 175-179)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`g=json.loads((AN/'08_quality/gates/2015_gate.json').read_text()); assert g['status']=='conditional_pass' and g['blocking_manual_review_items']==2 | assert not g['checks']['raw_bundle_completeness_verified'] and not g['checks']['all_referenced_attachments_present']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:175-179
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_30_missing_file_is_specific` (lines 181-183)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`t=(AN/'00_control/2015_missing_files.txt').read_text(); assert 'A题附件4原始视频文件' in t and '2015-07-13 08:54:06' in t and '09:34:36' in t and '2015_raw_bundle.zip' in t`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:181-183
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_31_manual_queue_consistency` (lines 185-187)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`q=read_jsonl(AN/'00_control/manual_review_queue.jsonl'); assert len(q)==2 and all(x['status']=='open' and x['severity']=='blocking' for x in q)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。；当前事实/Schema 冲突：当前 manual_review_queue.jsonl 的 A2/A3 输入仅有 2025 非阻塞项，而测试要求全局队列恰有 2 条 2015 阻塞项。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:185-187
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 必须从 gate、checkpoint、报告和证据重建全局队列；测试应按证据和年份映射而非固定总行数。
- 是否降低测试强度：`false`

#### `test_32_progress_reconciliation` (lines 189-191)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`p=json.loads((AN/'00_control/progress.json').read_text()); assert p['last_verified_complete_year']==2009 and p['year_status']['2010']=='conditional_pass' and p['year_status']['2015'].startswith('conditional_pass') and p['stop_after_year']==2015 and p['next_recommended_year'] is None`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；当前事实/Schema 冲突：当前 progress.json 不含 stop_after_year，且 2010 状态为 conditional_pass_pending_manual_review；测试要求 stop_after_year=2015 和 2010=conditional_pass。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:189-191
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A6 应按允许状态枚举重建 progress，测试应验证实际 schema 与保守状态规则。
- 是否降低测试强度：`false`

#### `test_33_original_file_modified_count_zero` (lines 193-193)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`def test_33_original_file_modified_count_zero(): assert json.loads((AN/'00_control/2015_source_hash_snapshot.json').read_text())['source_modified_count']==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:193-193
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_34_all_carrier_hashes_link_to_representations` (lines 195-199)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`for r in read_jsonl(AN/'04_relations/2015_representations.jsonl'): assert r['file_sha256']==c[r['carrier_id']]['sha256']`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:195-199
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_35_late_uploaded_files_included` (lines 201-209)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`assert all(f'2015B：互联网+_时代的出租车资源配置 ({i}).pdf' in names for i in range(1,6)) | assert all(any(n.startswith(f'2015C：月上柳梢头，人约黄昏后 ({i}).') for n in names) for i in range(1,5)) | assert all(any(n.startswith(f'2015D：众筹筑屋规划方案设计 ({i}).') for n in names) for i in range(1,4))`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:201-209
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_36_no_cache_or_compiled_files` (lines 211-211)

- 测试文件：`tests/test_2015_manual.py`
- 原断言：`def test_36_no_cache_or_compiled_files(): assert not any(p.name=='__pycache__' or p.suffix in {'.pyc','.pyo'} or p.name=='.pytest_cache' for p in ROOT.rglob('*'))`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2015_manual.py:211-211
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

### tests/test_2016_manual.py

#### `test_required_files` (lines 15-19)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert all((A/x).exists() for x in req)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:15-19
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_files_parse` (lines 21-23)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:21-23
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_jsonl_files_parse` (lines 25-27)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:25-27
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_carrier_count_and_hashes` (lines 29-33)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`c=jl(A/'01_inventory/2016_carrier_manifest.jsonl'); assert len(c)==35 | assert all(len(x['sha256'])==64 and x['sha256_covered'] for x in c)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:29-33
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_source_unmodified_flags` (lines 35-37)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`c=jl(A/'01_inventory/2016_carrier_manifest.jsonl'); assert sum(not x['source_modified'] for x in c)==35`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:35-37
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_logical_document_count` (lines 43-43)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_logical_document_count(): assert len(docs())==34`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:43-43
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_representation_count` (lines 45-45)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_representation_count(): assert len(jl(A/'04_relations/2016_representations.jsonl'))==35`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:45-45
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_solution_lineage_count` (lines 47-47)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_solution_lineage_count(): assert len(jl(A/'04_relations/2016_solution_lineages.jsonl'))==14`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:47-47
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_paper_count` (lines 49-49)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_paper_count(): assert sum(x['role']=='paper' for x in docs())==14`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:49-49
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_roles_valid` (lines 51-51)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_roles_valid(): assert {x['role'] for x in docs()} <= {'problem','paper','commentary','dataset'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:51-51
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_one_preferred_representation` (lines 53-59)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert all(sum(bool(x['is_preferred']) for x in v)==1 for v in by.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:53-59
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_representation_doc_consistency` (lines 61-63)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`ds={x['document_id'] for x in docs()}; reps=jl(A/'04_relations/2016_representations.jsonl'); assert all(r['document_id'] in ds for r in reps)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:61-63
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_b_duplicate_preserved_and_merged` (lines 65-69)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert len(reps)==2 and sum(r['is_preferred'] for r in reps)==1 and len({r['sha256'] for r in reps})==2`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:65-69
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_six_pack_complete` (lines 71-77)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert {x.name for x in p.iterdir()}=={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:71-77
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_field_status_enum` (lines 79-85)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert set(j(p)['field_status'].values())<=ok`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:79-85
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_unknown_not_absent` (lines 87-91)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`m=j(p); assert not (m['award_level']=='unknown' and m['field_status']['award_level']=='absent')`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:87-91
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_segments_unique_and_legal` (lines 93-105)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`seg=jl(A/'03_segments/2016_segments.jsonl'); assert len(seg)==943 | assert len({s['segment_id'] for s in seg})==len(seg) | x0,y0,x1,y1=s['bbox']; assert 0<=x0<x1 and 0<=y0<y1 | else: assert s['segment_type']=='sheet_region' and s['cell_range']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；工作表区域只检查起点/内部 row-column 关系，没有验证实际 sheet 行列上界。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:93-105
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：从实际 workbook representation 读取 sheet dimensions，并验证 row/column 上界。
- 是否降低测试强度：`true`

#### `test_page_boundaries_nonoverlap` (lines 107-115)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert len(keys)==len(set(keys))`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:107-115
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_problem_distribution` (lines 117-123)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`c=Counter(x['problem_id'][-1] for x in ls); assert c=={'A':5,'B':4,'C':2,'D':3}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:117-123
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_methods_and_visuals` (lines 125-129)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert len(jl(A/'05_knowledge/methods/2016_methods.jsonl'))==14 | assert len(jl(A/'05_knowledge/visualizations/2016_visualizations.jsonl'))==14`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:125-129
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_expert_feedback_not_fabricated` (lines 131-131)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_expert_feedback_not_fabricated(): assert jl(A/'05_knowledge/expert_feedback/2016_feedback.jsonl')==[]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:131-131
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_statistics_counts` (lines 133-137)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`assert r['physical_carriers']=='35' and r['logical_documents']=='34' and r['solution_papers']=='14'`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:133-137
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_gate_conditional` (lines 139-141)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`g=j(A/'08_quality/gates/2016_gate.json'); assert g['status']=='conditional_pass' and g['checks']['all_expected_supporting_files_present'] is False`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:139-141
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_checkpoint_not_remote_verified` (lines 143-143)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_checkpoint_not_remote_verified(): assert j(A/'09_checkpoints/2016_checkpoint.json')['remote_readback_verified'] is False`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:143-143
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_progress_reconciled` (lines 145-147)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`p=j(A/'00_control/progress.json'); assert p['last_verified_complete_year']==2009 and p['year_status']['2010']=='conditional_pass' and p['year_status']['2016'].startswith('conditional_pass')`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:145-147
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_missing_file_precise` (lines 149-151)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`t=(ROOT/'2016_missing_files.txt').read_text(encoding='utf-8'); assert '4#、16#、24#、33#、49#、57#' in t and 'D题附件2' in t`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:149-151
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_monthly_data_audit_in_report` (lines 153-155)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`t=(A/'07_reports/yearly/2016_report.md').read_text(encoding='utf-8'); assert '35040' in t and '10个空白或非数值风速单元格' in t`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:153-155
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_no_award_inference` (lines 157-157)

- 测试文件：`tests/test_2016_manual.py`
- 原断言：`def test_no_award_inference(): assert all(x['award_level'] in {'unknown','not_applicable'} for x in docs())`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2016_manual.py:157-157
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

### tests/test_2017_manual.py

#### `test_01_required_annual_files_exist` (lines 29-33)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert all((ROOT/x).exists() for x in req)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:29-33
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_02_required_control_files_exist` (lines 37-41)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert all((ROOT/x).exists() for x in req)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:37-41
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_03_json_and_jsonl_parse` (lines 45-53)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:45-53
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_04_csv_schema` (lines 57-65)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(rows)==19 | assert {'logical_document_id','role','preferred_representation_id','representation_count'} <= set(rows[0])`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:57-65
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_05_carrier_count` (lines 69-69)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`def test_05_carrier_count(): assert len(jl('analysis-index/01_inventory/2017_carrier_manifest.jsonl'))==20`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:69-69
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_06_sha256_coverage_and_format` (lines 73-79)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert all(len(r['sha256'])==64 and set(r['sha256'])<=set('0123456789abcdef') for r in rows) | assert len({r['sha256'] for r in rows})==20`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:73-79
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_07_trusted_baseline_blob_match` (lines 83-87)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert all(r['baseline_match'] and r['git_blob_sha1']==r['baseline_git_blob_sha1'] for r in rows)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:83-87
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_08_source_unmodified` (lines 91-95)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert x['all_unchanged'] is True and x['source_modified_count']==0 and x['pre_hash_count']==20`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:91-95
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_09_roles_legal` (lines 99-103)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert {r['role'] for r in rows} <= {'problem','paper','commentary','dataset'}`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:99-103
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_10_counts_consistent` (lines 107-115)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(cars)==20 and len(reps)==20 and len(docs)==19 | assert sum(int(d['representation_count']) for d in docs)==20`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:107-115
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_11_one_preferred_representation` (lines 119-125)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(g)==19 and all(sum(bool(x['is_preferred']) for x in xs)==1 for xs in g.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:119-125
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_12_format_spec_merged` (lines 129-133)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(reps)==2 and {r['format'] for r in reps}=={'doc','pdf'} and [r for r in reps if r['is_preferred']][0]['format']=='pdf'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:129-133
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_13_solution_lineages` (lines 137-141)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(l)==6 and all(x['lineage_status']=='distinct_solution' for x in l)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:137-141
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_14_paper_problem_distribution` (lines 145-151)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(papers)==6 and sum(r['problem_id']=='A' for r in papers)==5 and sum(r['problem_id']=='B' for r in papers)==1`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:145-151
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_15_six_pack_complete` (lines 155-165)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert {x.name for x in p.iterdir()}==names`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:155-165
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_16_segments_reference_valid_representations` (lines 169-175)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(segs)==223 and all(s['representation_id'] in reps for s in segs)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:169-175
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_17_page_bbox_legal` (lines 179-185)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`x0,y0,x1,y1=s['bbox']; assert x0>=0 and y0>=0 and x1>x0 and y1>y0`
- 问题：页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:179-185
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_18_page_regions_nonoverlap` (lines 189-197)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert all(len(v)==1 for v in groups.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:189-197
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_19_solution_paper_pages` (lines 201-205)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert sum(r['page_count'] or 0 for r in reps if r['logical_document_id'].startswith('2017_paper_'))==190`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:201-205
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_20_unknown_not_absent` (lines 209-213)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert '"absent"' not in corpus and ',absent,' not in corpus`
- 问题：使用 errors='ignore'，UnicodeDecodeError 会被静默吞掉，可能把不可读证据当作已审计。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:209-213
  - source contains errors='ignore'
- 建议的新断言：使用带路径异常的严格 UTF-8/编码探测工具，解码失败必须失败。
- 是否降低测试强度：`true`

#### `test_21_missing_requests_exact` (lines 217-227)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert len(req)==12 and len(q)==12 and all(x['severity']=='blocking' for x in req) | assert sum('2017B：' in x['requested_repository_path'] for x in req)==6 | assert sum('2017C：' in x['requested_repository_path'] for x in req)==3 | assert sum('2017D：' in x['requested_repository_path'] for x in req)==3`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。；当前事实/Schema 冲突：当前全局 manual_review_queue.jsonl 不是 12 条 2017 项，测试把全局队列总行数等同于 2017 缺失请求数。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:217-227
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应验证 2017 请求与人工复核映射，测试应按 year/request_id 映射而非全局 len。
- 是否降低测试强度：`false`

#### `test_22_gate_conditional_not_pass` (lines 231-237)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert g['status']=='conditional_pass' and g['blocking_manual_review_items']==12 | assert g['checks']['manual_verification_complete_for_full_year'] is False`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:231-237
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_23_progress_conservative` (lines 241-249)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert p['last_verified_complete_year']==2009 | assert p['year_status']['2017']=='conditional_pass_missing_source_carriers' | assert 2017 not in p['completed_years']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；当前事实/Schema 冲突：当前 progress.json 的 year_status 没有 2017 键，测试直接要求 conditional_pass_missing_source_carriers。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:241-249
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A6 应先重建年度状态；测试应验证合法状态集合和 blocking 项不能为 pass。
- 是否降低测试强度：`false`

#### `test_24_no_expert_commentary_fabrication` (lines 253-259)

- 测试文件：`tests/test_2017_manual.py`
- 原断言：`assert jl('analysis-index/05_knowledge/expert_feedback/2017_feedback.jsonl')==[] | assert not any(r['role']=='commentary' for r in rows)`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2017_manual.py:253-259
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

### tests/test_2018_manual.py

#### `test_required_files_exist` (lines 37-51)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert all(p.exists() for p in req)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:37-51
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_jsonl_parse` (lines 55-59)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:55-59
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_counts_and_object_layers` (lines 63-73)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert len(carriers)==27 and len(ds)==27 and len(reps)==27 | assert sum(c['physical_carrier_type']=='archive_container' for c in carriers)==1 | assert len(represented)==26`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:63-73
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_sha256_coverage_and_uniqueness` (lines 77-83)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert all(len(c['sha256'])==64 and all(ch in '0123456789abcdef' for ch in c['sha256']) for c in carriers) | assert len({c['sha256'] for c in carriers})==27`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:77-83
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_source_unmodified` (lines 87-93)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert a['source_modified_count']==0 | assert all(x['initial_sha256']==x['final_sha256'] and not x['modified'] for x in a['hashes'])`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:87-93
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_one_preferred_representation_per_document` (lines 97-107)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert len(rr)==1 and rr[0]['preferred'] is True`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:97-107
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_roles_legal_and_solution_scope` (lines 111-123)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert {d['role'] for d in ds}<=legal | assert sum(d['role']=='paper' for d in ds)==13 | assert sum(d['role']=='problem' for d in ds)==4 | assert sum(d['role']=='commentary' for d in ds)==2 | assert sum(d['role']=='dataset' for d in ds)==8`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:111-123
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_problem_distribution_and_filename_correction` (lines 127-135)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert {p:sum(d['problem_id']==f'2018-{p}' for d in papers) for p in 'ABCD'}=={'A':3,'B':4,'C':3,'D':3} | assert x['problem_id']=='2018-B' and x['filename'].startswith('2018A')`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:127-135
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_unknown_not_absent_policy` (lines 139-147)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert 'award_level,absent' not in raw | assert all(d['award_level']=='unknown' for d in docs()) | assert all(d['expert_feedback_status']=='not_observed' for d in docs())`
- 问题：使用 errors='ignore'，UnicodeDecodeError 会被静默吞掉，可能把不可读证据当作已审计。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:139-147
  - source contains errors='ignore'
- 建议的新断言：使用带路径异常的严格 UTF-8/编码探测工具，解码失败必须失败。
- 是否降低测试强度：`true`

#### `test_segments_have_valid_boundaries` (lines 151-171)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert len(segs)==580 | assert s['page_start']==s['page_end'] and s['page_start']>=1 | assert len(s['bbox'])==4 and s['bbox'][2]>s['bbox'][0] and s['bbox'][3]>s['bbox'][1] | assert key not in seen; seen.add(key) | if s['segment_type']=='worksheet_region': assert s['used_range'] is not None`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:151-171
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_six_pack_complete` (lines 175-183)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert p.is_dir() and names<={x.name for x in p.iterdir()}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:175-183
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_lineages_and_relations` (lines 187-193)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert len(lin)==13 and len({x['solution_document_id'] for x in lin})==13 | assert sum(x['relation_type']=='solves' for x in rel)==13`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:187-193
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_methods_and_visualizations_nonempty` (lines 197-201)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert len(read_jsonl(AI/'05_knowledge/methods/2018_methods.jsonl'))>=95 | assert len(read_jsonl(AI/'05_knowledge/visualizations/2018_visualizations.jsonl'))>=70`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:197-201
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_missing_files_are_exact_and_nonblocking` (lines 205-211)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert len(req)==5 and {x['request_id'] for x in req}=={f'2018-MISS-C-0{i}' for i in range(1,6)} | assert all(x['blocking'] is False for x in req)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。；当前事实/Schema 冲突：当前全局 missing_segment_requests.jsonl 是 2017 请求集合，测试要求其恰有 5 条 2018 请求。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:205-211
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应建立按年份索引并保留各年度请求；测试不能把全局文件当作单年度文件。
- 是否降低测试强度：`false`

#### `test_gate_is_conditional_pass_not_pass` (lines 215-225)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert gate['status']=='conditional_pass' | assert gate['checks']['supporting_data_complete'] is False | assert gate['checks']['source_unmodified'] is True | assert gate['blocking_manual_review_items']==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:215-225
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_progress_reconciliation` (lines 229-239)

- 测试文件：`tests/test_2018_manual.py`
- 原断言：`assert p['last_verified_complete_year']==2009 | assert p['year_status']['2010'].startswith('conditional_pass') | assert p['year_status']['2011']=='unverified_no_year_evidence' | assert p['year_status']['2018']=='conditional_pass_pending_remote_readback'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2018_manual.py:229-239
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

### tests/test_2019_manual.py

#### `test_required_files_exist` (lines 29-43)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert all(p.exists() for p in required)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:29-43
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_jsonl_csv_structures` (lines 47-59)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:47-59
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_counts_and_hash_coverage` (lines 63-81)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert len(carriers)==34 | assert len(docs)==34 | assert len(reps)==34 | assert all(len(x['sha256'])==64 for x in carriers) | assert len({x['carrier_id'] for x in carriers})==34 | assert len({x['logical_document_id'] for x in docs})==34`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:63-81
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_roles_and_solution_counts` (lines 85-97)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert all(x['document_role'] in valid for x in docs) | assert sum(x['document_role']=='paper' for x in docs)==17 | assert sum(x['document_role']=='problem' for x in docs)==5 | assert sum(x['document_role']=='dataset' for x in docs)==12`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:85-97
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_one_preferred_representation` (lines 101-109)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert all(sum(bool(x['is_preferred']) for x in arr)==1 for arr in by.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:101-109
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_six_pack_exactly_once_per_document` (lines 113-125)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert path.is_dir() | assert required.issubset({p.name for p in path.iterdir()})`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:113-125
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_page_boundaries_and_coordinates` (lines 129-151)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert s['page_start']==s['page_end'] and s['page_start']>=1 | assert 0<=x0<x1<=1 and 0<=y0<y1<=1 | assert key not in seen | assert len(seen)==562`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:129-151
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_solution_lineages` (lines 155-163)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert len(ls)==17 | assert all(len(x['solution_document_ids'])==1 for x in ls) | assert all(x['lineage_status']=='verified' for x in ls)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:155-163
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_unknown_not_absent_and_no_award_inference` (lines 167-175)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert all(x['award_level']=='unknown' for x in docs) | assert 'award_level": "absent"' not in corpus`
- 问题：使用 errors='ignore'，UnicodeDecodeError 会被静默吞掉，可能把不可读证据当作已审计。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:167-175
  - source contains errors='ignore'
  - source contains utf-8-sig
- 建议的新断言：使用带路径异常的严格 UTF-8/编码探测工具，解码失败必须失败。
- 是否降低测试强度：`true`

#### `test_source_modification_count_zero` (lines 179-185)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert int(row['source_modifications'])==0 | assert int(row['physical_carriers'])==34`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:179-185
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_gate_is_nonblocking_conditional_pass` (lines 189-197)

- 测试文件：`tests/test_2019_manual.py`
- 原断言：`assert gate['status']=='conditional_pass' | assert gate['blocking_manual_review_items']==0 | assert gate['checks']['local_tests_passed'] is True`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2019_manual.py:189-197
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

### tests/test_2020_manual.py

#### `test_json_control_files_parse` (lines 13-15)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:13-15
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_jsonl_files_parse` (lines 17-19)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:17-19
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_csv_structure` (lines 21-25)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`with (ROOT/p).open(encoding='utf-8-sig') as f: assert list(csv.DictReader(f))`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:21-25
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_counts` (lines 27-33)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`assert len(jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'))==39 | assert len(docs())==39 | assert len(jl('analysis-index/04_relations/2020_representations.jsonl'))==39`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:27-33
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_role_counts` (lines 35-37)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`d=docs(); assert sum(x['role']=='paper' for x in d)==17; assert sum(x['role']=='problem' for x in d)==5; assert sum(x['role']=='dataset' for x in d)==17; assert sum(x['role']=='commentary' for x in d)==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:35-37
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_paper_problem_counts` (lines 39-43)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`assert {k:sum(x['role']=='paper' and x['problem_id']==k for x in d) for k in expected}==expected`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:39-43
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_sha_coverage` (lines 45-47)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`c=jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'); assert all(re.fullmatch('[0-9a-f]{64}',x['sha256']) for x in c); assert len({x['original_filename'] for x in c})==39`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:45-47
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_no_byte_duplicates` (lines 49-51)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`c=jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl'); assert len({x['sha256'] for x in c})==39`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:49-51
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_source_unmodified` (lines 53-55)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`x=json.loads((ROOT/'analysis-index/08_quality/evidence/2020_source_integrity.json').read_text()); assert x['file_count']==39 and x['modification_count']==0 and x['all_sources_unmodified']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:53-55
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_exactly_one_preferred_representation` (lines 57-63)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`assert all(sum(y['preferred'] for y in ys)==1 for ys in g.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:57-63
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_ids_consistent` (lines 65-69)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`assert {x['logical_document_id'] for x in c}=={x['logical_document_id'] for x in r}=={x['logical_document_id'] for x in d}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:65-69
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_misnamed_credit_paper_corrected` (lines 71-73)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`c=[x for x in jl('analysis-index/01_inventory/2020_carrier_manifest.jsonl') if '梯度下降' in x['original_filename']][0]; assert c['associated_problem']=='C' and c['logical_document_id'].startswith('2020-C-PAPER')`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:71-73
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_e_q4_present` (lines 75-77)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`d=docs(); assert any(x['logical_document_id']=='2020-E-DATA-005' for x in d); g=json.loads((ROOT/'analysis-index/08_quality/gates/2020_gate.json').read_text()); assert g['checks']['four_quarters_present_for_problem_E']`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:75-77
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_solution_lineages` (lines 79-79)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`def test_solution_lineages(): assert len(jl('analysis-index/04_relations/2020_solution_lineages.jsonl'))==17`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:79-79
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_observed_methods` (lines 81-83)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`m=jl('analysis-index/05_knowledge/methods/2020_methods.jsonl'); assert sum(x.get('paper_observed',False) for x in m)>=80`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:81-83
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_feedback_not_observed` (lines 85-85)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`def test_feedback_not_observed(): assert jl('analysis-index/05_knowledge/expert_feedback/2020_feedback.jsonl')==[]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:85-85
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_observed_visualizations` (lines 87-89)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`v=jl('analysis-index/05_knowledge/visualizations/2020_visualizations.jsonl'); assert sum(x.get('paper_observed',False) for x in v)==68`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:87-89
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_segments_page_coordinates` (lines 91-97)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`a,b,c,d=x['region']; assert 0<=a<c<=1 and 0<=b<d<=1`
- 问题：页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:91-97
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_page_boundaries_unique` (lines 99-101)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`p=[x for x in jl('analysis-index/03_segments/2020_segments.jsonl') if x['segment_type']=='page']; keys=[(x['representation_id'],x['page_number']) for x in p]; assert len(keys)==len(set(keys))`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:99-101
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_tabular_boundaries` (lines 103-107)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`if x['segment_type']!='page': assert x['row_start']>=1 and x['row_end']>=x['row_start'] and x['column_start']>=1 and x['column_end']>=x['column_start']`
- 问题：工作表区域只检查起点/内部 row-column 关系，没有验证实际 sheet 行列上界。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:103-107
- 建议的新断言：从实际 workbook representation 读取 sheet dimensions，并验证 row/column 上界。
- 是否降低测试强度：`true`

#### `test_six_pack_complete` (lines 109-113)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`for d in docs(): assert names<={x.name for x in (base/d['logical_document_id']).iterdir()}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:109-113
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_six_pack_count` (lines 115-115)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`def test_six_pack_count(): assert len(list((ROOT/'analysis-index/02_documents/six_pack/2020').iterdir()))==39`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:115-115
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_metadata_status_semantics` (lines 117-119)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`txt='\n'.join((p/'metadata.json').read_text() for p in (ROOT/'analysis-index/02_documents/six_pack/2020').iterdir()); assert '"status": "unknown"' in txt and '"status": "not_observed"' in txt and '"status": "absent"' not in txt`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:117-119
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_gate_conditional_pass` (lines 121-123)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`g=json.loads((ROOT/'analysis-index/08_quality/gates/2020_gate.json').read_text()); assert g['status']=='conditional_pass' and g['blocking_items']==0 and g['checks']['solution_paper_corpus_present'] and not g['checks']['remote_readback_verified']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:121-123
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_checkpoint_counts_match_gate` (lines 125-129)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`for k in ['carriers','documents','solution_papers','problem_statements','supporting_objects','representations','segments']: assert g[k]==c[k]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:125-129
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_progress_pending_remote_readback` (lines 131-133)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`p=json.loads((ROOT/'analysis-index/00_control/progress.json').read_text()); assert 2020 not in p['completed_years'] and p['year_status']['2020']=='conditional_pass_pending_remote_readback' and p['next_recommended_year']==2020`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:131-133
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_no_blocking_missing_requests` (lines 135-135)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`def test_no_blocking_missing_requests(): assert all(not x['blocking'] for x in jl('analysis-index/00_control/missing_segment_requests.jsonl'))`
- 问题：把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；当前事实/Schema 冲突：当前 missing_segment_requests.jsonl 含 2017 blocking 请求，且字段使用 severity/status，不是测试所访问的 blocking 布尔字段。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:135-135
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应统一 request schema 并按年份判断阻塞状态，不能假设全局请求为空或字段必为 blocking。
- 是否降低测试强度：`false`

#### `test_missing_files_txt_precise` (lines 137-139)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`t=(ROOT/'analysis-index/00_control/2020_missing_files.txt').read_text(); assert '没有阻塞性缺失文件' in t and '0~3' in t and '10~100万元' in t`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:137-139
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_report_exists_and_has_corrections` (lines 141-143)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`t=(ROOT/'analysis-index/07_reports/yearly/2020_report.md').read_text(); assert '39个物理载体' in t and '17篇参赛论文' in t and 'conditional_pass' in t`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:141-143
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_original_role_enum` (lines 145-145)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`def test_original_role_enum(): assert {x['role'] for x in docs()}<={'problem','paper','commentary','dataset'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:145-145
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_format_spec_present` (lines 147-147)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`def test_format_spec_present(): assert any(x['logical_document_id']=='2020-GLOBAL-RULE-001' for x in docs())`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:147-147
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_q4_audit_rows` (lines 149-151)

- 测试文件：`tests/test_2020_manual.py`
- 原断言：`a=json.loads((ROOT/'analysis-index/08_quality/evidence/2020_data_audit.json').read_text()); q=a['2020年国赛E题附件 (5).xlsx']; assert q['rows']==787466 and q['unique_water_meters']==91`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2020_manual.py:149-151
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

### tests/test_2021_manual.py

#### `test_01_required_files_exist` (lines 39-43)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert all((AI/p).exists() for p in required)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:39-43
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_02_json_jsonl_parse` (lines 47-51)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:47-51
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_03_csv_structure` (lines 55-61)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`ds=docs(); assert len(ds)==37 | assert len(rows)==6 and rows[0]['scope']=='ALL'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:55-61
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_04_sha256_coverage` (lines 65-73)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert len(cs)==754 | assert all(SHA_RE.match(x['sha256']) for x in cs) | assert len({x['carrier_id'] for x in cs})==754`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:65-73
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_05_carrier_layer_counts` (lines 77-87)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert c=={'archive_member':753,'archive_container':1} | assert ext['.jpg']==729 and ext['.xlsx']==15 and ext['.pdf']==5 and ext['.csv']==3 and ext['.doc']==1`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:77-87
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_06_document_role_counts` (lines 91-97)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert c=={'paper':17,'problem':5,'dataset':14,'commentary':1} | assert set(c)<= {'problem','paper','commentary','dataset'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:91-97
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_07_representation_counts_and_preferred` (lines 101-113)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert len(rs)==41 | assert set(by)=={d['logical_document_id'] for d in ds} | assert all(sum(bool(r['preferred']) for r in vals)==1 for vals in by.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:101-113
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_08_representations_reference_carriers` (lines 117-123)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert r['carrier_ids'] and set(r['carrier_ids'])<=cids`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:117-123
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_09_segments_count_and_ids` (lines 127-131)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert len(ss)==769 and len({s['segment_id'] for s in ss})==769`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:127-131
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_10_page_boundaries_valid_no_overlap` (lines 135-151)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`x0,y0,x1,y1=s['bbox_normalized']; assert 0<=x0<x1<=1 and 0<=y0<y1<=1 | assert key not in seen; seen.add(key) | assert 1<=s['row_start']<=s['row_end'] and 1<=s['column_start']<=s['column_end']`
- 问题：页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。；工作表区域只检查起点/内部 row-column 关系，没有验证实际 sheet 行列上界。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:135-151
- 建议的新断言：从实际 workbook representation 读取 sheet dimensions，并验证 row/column 上界。
- 是否降低测试强度：`true`

#### `test_11_paper_page_sequences` (lines 155-165)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert len(by)==17 | for pages in by.values(): assert sorted(pages)==list(range(1,len(pages)+1))`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:155-165
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_12_six_pack_complete` (lines 169-175)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert {x.name for x in p.iterdir()}=={'metadata.json','problem_summary.md','model_summary.md','validation.md','visualization.md','manual_review.json'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:169-175
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_13_relation_and_lineage_counts` (lines 179-183)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert len(lin)==17 and sum(x['relation_type']=='solves' for x in rel)==17 and sum(x['relation_type']=='supports' for x in rel)==14`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:179-183
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_14_unknown_not_absent_policy` (lines 187-195)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert d['award_level'] in {'unknown','not_applicable'} | assert '未观察' in text or 'not_observed' in text`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:187-195
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_15_expert_feedback_not_fabricated` (lines 199-203)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert len(rows)==1 and rows[0]['status']=='not_observed' and rows[0]['expert_commentary_documents']==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:199-203
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_16_duplicate_e_datasets_corrected` (lines 207-219)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert ds[did]['problem_id']=='E' and ds[did]['representation_count']=='2' | assert len(vals)==2 and len({r['byte_identical_group'] for r in vals})==1`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:207-219
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_17_statistics_consistency` (lines 223-231)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert int(allr['physical_carriers'])==754 and int(allr['logical_documents'])==37 and int(allr['representations'])==41 and int(allr['segments'])==769 | assert sum(int(r['solution_papers']) for r in rows[1:])==17`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:223-231
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_18_source_unmodified_evidence` (lines 235-245)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert gate['checks']['source_unmodified'] is True and cp['source_files_modified']==0 | h=hashlib.sha256(p.read_bytes()).hexdigest(); assert h==cp['source_archive_sha256']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:235-245
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_19_quality_gate_conditional_nonblocking` (lines 249-253)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert g['status']=='conditional_pass' and g['blocking_manual_review_items']==0 and g['manual_review_items']==2`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:249-253
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_20_no_raw_source_in_upload_package` (lines 257-263)

- 测试文件：`tests/test_2021_manual.py`
- 原断言：`assert not [p for p in files if p.suffix.lower() in forbidden]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2021_manual.py:257-263
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

### tests/test_2022_manual.py

#### `test_required_paths_exist` (lines 39-83)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert all((ROOT/p).is_file() for p in required)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:39-83
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_files_parse` (lines 87-91)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:87-91
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_jsonl_files_parse` (lines 95-99)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:95-99
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_csv_files_parse_and_have_rows` (lines 103-111)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert rows`
- 问题：对扫描到的所有 CSV 要求 rows 非空，可能把语义上允许空的 CSV 判错。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:103-111
  - source contains utf-8-sig
- 建议的新断言：按 CSV 文件 schema/语义决定空文件是否允许，并对 header/状态分别断言。
- 是否降低测试强度：`false`

#### `test_inventory_sha256_coverage_and_uniqueness` (lines 115-127)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert len(rows)==260 | assert len(pages)==259 | assert all(re.fullmatch(r'[0-9a-f]{64}',r['sha256']) for r in rows) | assert len({r['sha256'] for r in pages})==259`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:115-127
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_object_count_consistency` (lines 131-149)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert len(docs)==7 and len(reps)==7 and len(segs)==259 and len(pages)==259 | assert sum(int(d['page_count']) for d in docs)==259 | assert sum(r['page_count'] for r in reps)==259`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:131-149
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_one_preferred_representation_per_document` (lines 153-161)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert all(sum(1 for r in rs if r['preferred'])==1 for rs in grouped.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:153-161
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_representation_carriers_and_segments_resolve` (lines 165-179)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert all(cid in pages for r in reps for cid in r['carrier_ids']) | assert {s['carrier_id'] for s in segs}==set(pages) | assert all(len(r['carrier_ids'])==r['page_count'] for r in reps)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:165-179
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_legal_document_roles` (lines 183-193)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert {d['document_role'] for d in docs} <= legal | assert {d['document_role'] for d in docs} == {'paper'}`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:183-193
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_unknown_is_not_absent` (lines 197-207)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert 'absent' not in set(m['feature_status'].values()) | assert m['award_level']=='unknown' | assert m['authors']=='not_observed'`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:197-207
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_page_boundaries_valid_and_non_overlapping` (lines 211-225)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert 0<=b['x0']<b['x1']<=1 and 0<=b['y0']<b['y1']<=1 | assert all(len(v)==1 for v in by_carrier.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:211-225
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_page_indices_are_contiguous` (lines 229-237)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert all(sorted(v)==list(range(1,len(v)+1)) for v in by_doc.values())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:229-237
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_six_pack_exactly_present_for_each_document` (lines 241-251)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert len(dirs)==7 | assert all({p.name for p in d.iterdir() if p.is_file()}==required for d in dirs)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:241-251
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_lineage_and_method_document_ids_resolve` (lines 255-267)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert {r['logical_document_id'] for r in lineages}==docs | assert {r['logical_document_id'] for r in methods}<=docs`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:255-267
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_visualization_page_references_resolve` (lines 271-277)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert viz and all(v['segment_id'] in segs for v in viz)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:271-277
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_expert_feedback_empty_because_not_observed` (lines 281-283)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert read_jsonl(ROOT/'analysis-index/05_knowledge/expert_feedback/2022_feedback.jsonl')==[]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:281-283
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_confirmed_content_duplicates_are_retained_not_merged` (lines 287-299)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert len(dup)==2 | assert len(flagged)==4 and len({r['sha256'] for r in flagged})==4`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:287-299
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_statistics_match_counts` (lines 303-311)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert int(y['source_carriers'])==259 and int(y['logical_documents'])==7 and int(y['representations'])==7 and int(y['page_segments'])==259`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:303-311
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_gate_is_conditional_not_pass` (lines 315-323)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert g['status']=='conditional_pass' | assert g['checks']['full_year_source_complete'] is False | assert g['checks']['official_problem_statements_present'] is False`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:315-323
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_missing_file_requests_are_precise` (lines 327-333)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert len(rows)==7 | assert all(r['expected_name_or_role'] and r['recognition_features'] for r in rows)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。；当前事实/Schema 冲突：当前 missing_segment_requests.jsonl 不是 7 条 2022 记录，且当前行不具备该测试要求的 expected_name_or_role/recognition_features 字段。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:327-333
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应以实际证据重建请求 schema，测试应验证字段和年份映射。
- 是否降低测试强度：`false`

#### `test_progress_stops_at_2022_without_claiming_gap_years` (lines 337-345)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert p['stop_after_year']==2022 and p['next_recommended_year'] is None | assert p['year_status']['2012']=='not_observed' and p['year_status']['2021']=='not_observed' | assert p['year_status']['2022']=='conditional_pass_pending_remote_readback'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；当前事实/Schema 冲突：当前 progress.json 不含 stop_after_year、2012、2021、2022 这些测试要求的字段。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:337-345
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A6 应依据 gate/checkpoint 和允许状态重建 progress，不应保留隐含的 stop_after_year 假设。
- 是否降低测试强度：`false`

#### `test_checkpoint_pending_remote_readback` (lines 349-353)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert c['remote_readback_verified'] is False and c['stop_after_year']==2022`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:349-353
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_source_files_unmodified_when_raw_root_available` (lines 357-381)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert mismatches==[]`
- 问题：使用 pytest.skip 在环境变量缺失时跳过原始资料验证，未形成失败或明确的 pending 状态。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:357-381
  - source contains pytest.skip for missing CUMCM_2022_RAW_ROOT/CUMCM_2022_BUNDLE
- 建议的新断言：将缺失原始资料记录为证据化 pending/blocked 状态，专项测试不得静默 skip。
- 是否降低测试强度：`true`

#### `test_transport_bundle_hash_when_available` (lines 385-397)

- 测试文件：`tests/test_2022_manual.py`
- 原断言：`assert sha256(Path(path))==b['sha256']`
- 问题：使用 pytest.skip 在环境变量缺失时跳过原始资料验证，未形成失败或明确的 pending 状态。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2022_manual.py:385-397
  - source contains pytest.skip for missing CUMCM_2022_RAW_ROOT/CUMCM_2022_BUNDLE
- 建议的新断言：将缺失原始资料记录为证据化 pending/blocked 状态，专项测试不得静默 skip。
- 是否降低测试强度：`true`

### tests/test_2023_manual.py

#### `test_required_annual_files_exist` (lines 107-149)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert all((AI / p).is_file() for p in required)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:107-149
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_and_jsonl_parse` (lines 155-163)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:155-163
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_csv_parse` (lines 169-175)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert list(csv.reader(f))`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:169-175
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_expected_counts` (lines 181-189)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len(carriers) == 32 | assert len(documents) == 32 | assert len(reps) == 32 | assert len(segs) == 761`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:181-189
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_roles_and_subtypes` (lines 195-203)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert role_counts == {'paper': 14, 'problem': 5, 'dataset': 13} | assert set(d['role'] for d in documents) <= {'paper', 'problem', 'commentary', 'dataset'} | assert Counter(d['subtype'] for d in documents)['submission_template'] == 4`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:195-203
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_problem_distribution` (lines 209-213)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert counts == {'A': 4, 'B': 3, 'C': 4, 'D': 1, 'E': 2}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:209-213
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_sha256_coverage_and_source_bytes` (lines 219-231)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len({c['source_relative_path'] for c in carriers}) == 32 | assert p.is_file(), p | assert sha256(p) == c['sha256'] | assert c['source_modified'] is False`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:219-231
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_readonly_flags` (lines 237-239)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert all(c['readonly_verified'] for c in carriers)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:237-239
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_byte_duplicate_preserved` (lines 245-263)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len(groups) == 1 | assert len(values) == 2 | assert {Path(v['source_relative_path']).name for v in values} == {'result2.xlsx', 'result3.xlsx'} | assert len({v['logical_document_id'] for v in values}) == 2`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:245-263
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_one_preferred_representation_per_document` (lines 269-285)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len(rs) == 1 | assert sum(bool(r['preferred']) for r in rs) == 1 | assert d['preferred_representation_id'] == rs[0]['representation_id']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:269-285
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_carrier_document_representation_consistency` (lines 291-301)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert {c['logical_document_id'] for c in carriers} == doc_ids | assert {r['logical_document_id'] for r in reps} == doc_ids | assert {r['carrier_id'] for r in reps} == carrier_ids`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:291-301
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_pdf_page_and_xlsx_sheet_segment_counts` (lines 307-311)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert sum(s['segment_type'] == 'page' for s in segs) == 742 | assert sum(s['segment_type'] == 'worksheet' for s in segs) == 19`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:307-311
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_pdf_regions_legal_and_unique` (lines 317-339)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert 0 <= r['x0'] < r['x1'] | assert 0 <= r['y0'] < r['y1'] | assert key not in seen | assert s['boundary_status'] == 'verified'`
- 问题：包含按 segment_type 过滤的 continue；这是结构性分支，不是异常静默通过，但应明确其覆盖边界。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:317-339
  - continue is guarded by an explicit segment_type filter
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_worksheet_regions_legal_and_unique` (lines 345-365)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert 1 <= r['row_start'] <= r['row_end'] | assert 1 <= r['column_start'] <= r['column_end'] | assert key not in seen`
- 问题：包含按 segment_type 过滤的 continue；这是结构性分支，不是异常静默通过，但应明确其覆盖边界。；工作表区域只检查起点/内部 row-column 关系，没有验证实际 sheet 行列上界。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:345-365
  - continue is guarded by an explicit segment_type filter
- 建议的新断言：从实际 workbook representation 读取 sheet dimensions，并验证 row/column 上界。
- 是否降低测试强度：`true`

#### `test_no_blank_or_missing_segments` (lines 371-377)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert all(s.get('blank_status', 'not_applicable') != 'blank' for s in segs) | assert requests[0]['request_count'] == 0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:371-377
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_six_pack_complete` (lines 383-395)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len([p for p in root.iterdir() if p.is_dir()]) == 32 | assert {p.name for p in folder.iterdir() if p.is_file()} == expected`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:383-395
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_six_pack_manual_reviews_closed` (lines 401-415)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert mr['review_status'] == 'complete' | assert mr['open_review_items'] == 0 | assert mr['preferred_representation_count'] == 1 | assert mr['award_level_inferred'] is False`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:401-415
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_relations_referential_integrity` (lines 421-435)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert rels | assert r['subject_id'] in ids | assert r['object_id'] in ids | assert any(r['predicate'] == 'byte_identical_to' for r in rels)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:421-435
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_solution_lineages_complete` (lines 441-451)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len(rows) == 14 | assert {r['paper_document_id'] for r in rows} == papers | assert all(r['sequence'] and r['algorithms'] and r['validation_modes'] for r in rows)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:441-451
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_methods_and_visualizations_cover_papers` (lines 457-467)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert {r['paper_document_id'] for r in methods} == papers | assert {r['paper_document_id'] for r in visuals} == papers`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:457-467
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_expert_feedback_not_fabricated` (lines 473-481)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert len(feedback) == 1 | assert feedback[0]['status'] == 'not_observed' | assert feedback[0]['expert_commentary_documents'] == 0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:473-481
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_unknown_not_counted_as_absent` (lines 487-495)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert set(d['field_status'] for d in documents) <= allowed | assert all(d['award_level'] == 'unknown' and d['award_level_status'] == 'not_observed' for d in documents) | assert not any(d['award_level_status'] == 'absent' for d in documents)`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:487-495
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_statistics_consistent` (lines 501-515)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert int(row['physical_carriers']) == len(carriers) | assert int(row['logical_documents']) == len(documents) | assert int(row['representations']) == len(reps) | assert int(row['segments']) == len(segs) | assert int(row['source_modified_files']) == 0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:501-515
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_quality_gate_pass` (lines 521-531)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert gate['status'] == 'pass' | assert all(gate['checks'].values()) | assert gate['manual_review_items'] == 0 | assert gate['blocking_manual_review_items'] == 0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；当前事实/Schema 冲突：当前 2023 gate 为 pass，但对应 checkpoint 为 pass_pending_remote_readback；单测只看 gate，未验证控制层状态一致性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:521-531
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A6/A10 应要求 gate、checkpoint、progress 和远端回读状态一致。
- 是否降低测试强度：`false`

#### `test_checkpoint_pending_remote_readback` (lines 537-545)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert cp['status'] == 'pass_pending_remote_readback' | assert cp['manual_review_complete'] is True | assert cp['remote_readback_verified'] is False`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:537-545
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_progress_reconciled_conservatively` (lines 551-563)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert p['last_verified_complete_year'] == 2009 | assert p['year_status']['2010'] == 'conditional_pass' | assert p['year_status']['2011'] == 'not_verified' | assert p['year_status']['2023'] == 'pass_pending_remote_readback' | assert 2023 not in p['completed_years']`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:551-563
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_manual_review_queue_closed` (lines 569-575)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert q[0]['open_items'] == 0 | assert q[0]['blocking_items'] == 0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:569-575
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_source_file_count_and_extensions` (lines 581-583)

- 测试文件：`tests/test_2023_manual.py`
- 原断言：`assert Counter(c['extension'] for c in carriers) == {'.pdf': 19, '.xlsx': 13}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2023_manual.py:581-583
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

### tests/test_2024_manual.py

#### `test_required_paths_exist` (lines 27-69)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert all((ROOT/p).exists() for p in req)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:27-69
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_jsonl_parse` (lines 73-81)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:73-81
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_csv_parse_and_counts` (lines 85-97)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len(rows)==29 | assert sum(r['document_role']=='paper' for r in rows)==16 | assert sum(r['document_role']=='problem' for r in rows)==5 | assert sum(r['document_role']=='dataset' for r in rows)==8`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:85-97
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_sha256_coverage_and_uniqueness` (lines 101-115)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len(rows)==820 | assert len({r['carrier_id'] for r in rows})==820 | assert len({r['source_path'] for r in rows})==820 | assert len({r['sha256'] for r in rows})==820 | assert all(len(r['sha256'])==64 and set(r['sha256'])<=set('0123456789abcdef') for r in rows) | assert all(r['source_unmodified'] for r in rows)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:101-115
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_carrier_assignment_consistency` (lines 119-139)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len(assigned)==818 and len(archives)==2 | assert all(bydoc[k]==int(v['carrier_count']) for k,v in docs.items())`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:119-139
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_representations_one_preferred_each` (lines 143-157)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len(reps)==29 | assert len(by)==29 | assert all(sum(x['is_preferred'] is True for x in v)==1 for v in by.values()) | assert sum(r['carrier_count'] for r in reps)==818`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:143-157
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_roles_legal` (lines 161-169)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert roles<=legal`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:161-169
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_unknown_not_absent_policy` (lines 173-181)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert all(r['award_level'] in {'unknown','not_applicable'} for r in rows) | assert not any(r['award_level']=='absent' for r in rows)`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:173-181
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_segments_coordinates_and_unique_pages` (lines 185-211)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len(segs)==826 | assert 0<=reg['x0']<reg['x1']<=1 | assert 0<=reg['y0']<reg['y1']<=1 | assert key not in seen | assert sum(s['segment_type']=='page' for s in segs)==815`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:185-211
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_a242_missing_pages_explicit` (lines 215-231)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert r['missing_page_indices']==[12,15,16] | assert '2024国赛优秀论文/A题/A242/12.jpg' in paths | assert '2024国赛优秀论文/A题/A242/15.jpg' in paths | assert '2024国赛优秀论文/A题/A242/16.jpg' in paths`
- 问题：把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；当前事实/Schema 冲突：当前 missing_segment_requests.jsonl 使用 2017 请求字段，测试要求 2024 expected_path 和 A242 三个路径。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:215-231
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应保留跨年度请求并按 request_id/year 验证；不能读取全局文件后假定只含 2024。
- 是否降低测试强度：`false`

#### `test_missing_official_templates_explicit` (lines 235-243)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert {'2024真题/A题/附件/result4.xlsx','2024真题/C题/附件3/result1_1.xlsx','2024真题/C题/附件3/result1_2.xlsx','2024真题/C题/附件3/result2.xlsx'}<=paths | assert len(req)==7 and all(x['blocking'] for x in req)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。；当前事实/Schema 冲突：当前全局 missing_segment_requests.jsonl 不是 7 条 2024 blocking 请求，测试的 expected_path/blocking schema 与当前文件不一致。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:235-243
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应先建立证据化请求 schema，再由专项测试验证 2024 子集。
- 是否降低测试强度：`false`

#### `test_six_pack_complete` (lines 247-259)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert {p.name for p in d.iterdir()}==names`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:247-259
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_methods_lineages_visualizations` (lines 263-269)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len(read_jsonl(ROOT/'analysis-index/05_knowledge/methods/2024_methods.jsonl'))==16 | assert len(read_jsonl(ROOT/'analysis-index/04_relations/2024_solution_lineages.jsonl'))==16 | assert len(read_jsonl(ROOT/'analysis-index/05_knowledge/visualizations/2024_visualizations.jsonl'))==16`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:263-269
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_expert_feedback_empty_not_fabricated` (lines 273-275)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert read_jsonl(ROOT/'analysis-index/05_knowledge/expert_feedback/2024_feedback.jsonl')==[]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:273-275
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_source_integrity_record` (lines 279-289)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert x['physical_carrier_count']==820 | assert x['unique_sha256_count']==820 | assert x['exact_duplicate_groups']==0 | assert x['modified_files']==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:279-289
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_statistics_match_gate` (lines 293-307)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert int(total['physical_carriers'])==gate['counts']['physical_carriers']==820 | assert int(total['logical_documents'])==gate['counts']['logical_documents']==29 | assert int(total['solution_papers'])==16 | assert int(total['representations'])==29`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:293-307
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_gate_is_conditional_not_pass` (lines 311-321)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert gate['status']=='conditional_pass' | assert gate['blocking_missing_items']==7 | assert gate['checks']['all_expected_attachments_present'] is False | assert gate['checks']['all_observed_page_sequences_complete'] is False`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:311-321
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_checkpoint_consistent` (lines 325-335)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert cp['status']==gate['status']=='conditional_pass' | assert cp['counts']==gate['counts'] | assert cp['remote_readback_verified'] is False`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:325-335
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_progress_does_not_promote_to_pass` (lines 339-347)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert p['year_status']['2024']=='conditional_pass' | assert 2024 not in p['completed_years'] | assert 2024 in p['processed_years']`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:339-347
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_no_raw_source_in_upload_tree` (lines 351-361)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert not (ROOT/'raw').exists() | assert not (ROOT/'2024国赛优秀论文').exists() | assert not (ROOT/'2024真题').exists()`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。；只检查 raw、2024国赛优秀论文和2024真题三个路径，扫描范围由手工白名单决定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:351-361
  - source comment explicitly limits source-like locations
- 建议的新断言：以仓库实际 schema/载体清单驱动扫描，并显式记录允许的分析 CSV 例外。
- 是否降低测试强度：`true`

#### `test_local_actual_hashes_when_sources_available` (lines 365-389)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert h(papers)==arc['2024国赛优秀论文.zip'] | assert h(probs)==arc['2024真题.zip']`
- 问题：原始压缩包不存在时直接 return，导致哈希验证不执行。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:365-389
  - source returns when /mnt/data/2024*.zip inputs are absent
- 建议的新断言：将外部资料缺失明确记录为 pending，并在日志中区分未执行与通过。
- 是否降低测试强度：`true`

#### `test_relation_endpoints_and_ids_valid` (lines 393-409)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len({r['relation_id'] for r in rels})==len(rels) | assert all(r['source_id'] in known and r['target_id'] in known for r in rels)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:393-409
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_segment_references_are_resolvable` (lines 413-431)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert len({s['segment_id'] for s in segs})==len(segs) | assert all(s['logical_document_id'] in docs for s in segs) | assert all(s['representation_id'] in reps for s in segs) | assert all(not s.get('carrier_id') or s['carrier_id'] in carriers for s in segs)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:413-431
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_final_control_readback_provenance` (lines 435-449)

- 测试文件：`tests/test_2024_manual.py`
- 原断言：`assert prov['remote_progress_blob_sha']=='1ac6896e9a80eab95a9b50ad5eb5be54b2648659' | assert len(prov['remote_absent_at_readback'])==4 | assert integrity['rehash_checked_carriers']==820 | assert integrity['rehash_mismatches']==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；当前事实/Schema 冲突：当前 progress.json 不含 control_merge_provenance，测试依赖的远端 blob 和 rehash 字段不存在。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2024_manual.py:435-449
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A6/A10 应从实际远端回读和日志生成 provenance，测试不能硬编码未存在的 blob。
- 是否降低测试强度：`false`

### tests/test_2025_manual.py

#### `test_required_files_exist` (lines 25-47)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert all(p.exists() for p in required)`
- 问题：该函数仅验证路径存在，不能单独证明内容、schema 或证据完整性。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:25-47
- 建议的新断言：保留存在性断言，同时补充/关联内容解析、schema 和证据一致性断言。
- 是否降低测试强度：`false`

#### `test_json_files_parse` (lines 51-53)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:51-53
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_jsonl_files_parse` (lines 57-63)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:57-63
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_csv_files_parse` (lines 67-71)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`无直接 assert（需检查是否仅执行读取）`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:67-71
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_carrier_sha_coverage` (lines 75-87)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert len(rows)==107 | assert len({r['carrier_id'] for r in rows})==107 | assert len({r['source_path'] for r in rows})==107 | assert all(re.fullmatch(r'[0-9a-f]{64}',r['sha256']) for r in rows) | assert all(r['read_only_verified'] for r in rows)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:75-87
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_object_counts_and_roles` (lines 91-101)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert len(docs)==106 | assert c=={'dataset':94,'paper':7,'problem':5} | assert all(d['role'] in {'problem','paper','commentary','dataset'} for d in docs)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:91-101
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_representation_consistency` (lines 105-121)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert len(reps)==107 | assert set(by)=={d['document_id'] for d in docs} | assert all(sum(1 for r in rs if r['preferred'])==1 for rs in by.values()) | assert sum(1 for r in reps if r['logical_document_id']=='2025-PAPER-C023')==2`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:105-121
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
  - source contains utf-8-sig
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_carrier_representation_one_to_one` (lines 125-131)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert {c['carrier_id'] for c in carriers}=={r['carrier_id'] for r in reps}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:125-131
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_every_document_has_exact_six_pack` (lines 135-147)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert folder.is_dir() | assert {p.name for p in folder.iterdir() if p.is_file()}==expected`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:135-147
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_segment_coordinates_valid_and_nonoverlap` (lines 151-171)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert len(segs)==745 | assert s['coordinate_valid'] is True | x0,y0,x1,y1=s['bbox_pdf_points']; assert x1>x0 and y1>y0 | key=(s['representation_id'],s['page_number']); assert key not in page_keys; page_keys.add(key) | assert s['bbox_pdf_points'] is None`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；页码检查未将 page_number/page_index 与实际 representation/page_count 上界绑定。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:151-171
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：增加页码下界、上界、连续性和 representation 实际页数的双向断言。
- 是否降低测试强度：`true`

#### `test_unknown_not_absent_policy` (lines 175-183)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert 'field_status_policy' in text | assert '"status": "absent"' not in text and '"status":"absent"' not in text`
- 问题：使用 errors='ignore'，UnicodeDecodeError 会被静默吞掉，可能把不可读证据当作已审计。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:175-183
  - source contains errors='ignore'
- 建议的新断言：使用带路径异常的严格 UTF-8/编码探测工具，解码失败必须失败。
- 是否降低测试强度：`true`

#### `test_problem_paper_distribution` (lines 187-191)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert Counter(x['problem_id'] for x in lines)=={'A':2,'B':1,'C':2,'D':1,'E':1}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:187-191
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_no_expert_commentary_fabricated` (lines 195-197)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert read_jsonl(AI/'05_knowledge/expert_feedback/2025_feedback.jsonl')==[]`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:195-197
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_duplicate_relations_retained` (lines 201-209)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert len(dup)>=4 | assert any(r.get('duplicate_semantics')=='cross_label_duplicate_requires_source_confirmation' for r in dup)`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:201-209
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_manual_review_is_nonblocking` (lines 213-217)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert len(q)==1 and q[0]['severity']=='nonblocking' and q[0]['status']=='open'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。；把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:213-217
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：按年份和 request_id 筛选并验证跨年度队列映射，避免全局总数假设。
- 是否降低测试强度：`false`

#### `test_missing_segment_requests_empty` (lines 221-223)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert read_jsonl(AI/'00_control/missing_segment_requests.jsonl')==[]`
- 问题：把全局队列/请求文件当作单年度集合使用，未按 year/request_id 建立年度子集。；依赖全局队列总行数或整体为空，容易被其他年度问题破坏或掩盖。；当前事实/Schema 冲突：当前 missing_segment_requests.jsonl 保留 12 条 2017 blocking 请求，测试要求整个全局文件为空。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:221-223
  - current control-state inspection at A3 input HEAD
- 建议的新断言：A5 应按年份筛选并验证 2025 子集，而不是要求全局请求为空。
- 是否降低测试强度：`false`

#### `test_source_unmodified_evidence` (lines 227-233)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert e['source_file_count']==107 and e['modified_file_count']==0 and e['all_hashes_match'] is True | assert all(x['match'] for x in e['files'])`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:227-233
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_gate_conditional_pass_without_blockers` (lines 237-247)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert g['status']=='conditional_pass' | assert g['blocking_manual_review_items']==0 | assert g['manual_review_items']==1 | assert g['upload_ready'] is True`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:237-247
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_progress_reconciled_not_blindly_advanced` (lines 251-259)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert p['last_verified_complete_year']==2009 | assert 2010 not in p['completed_years'] and 2011 not in p['completed_years'] and 2025 not in p['completed_years'] | assert p['year_status']['2025']=='conditional_pass_pending_remote_readback'`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:251-259
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_checkpoint_counts_match` (lines 263-269)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert (c['carriers'],c['documents'],c['representations'])==(107,106,107) | assert c['solution_papers']==7 and c['problem_statements']==5 and c['expert_commentaries']==0`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:263-269
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_statistics_key_counts` (lines 273-285)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert d[('physical_carriers','all')]=='107' | assert d[('logical_documents','all')]=='106' | assert d[('solution_papers','all')]=='7' | assert d[('source_modified_files','all')]=='0'`
- 问题：使用 utf-8-sig 容忍 BOM，没有单独断言输入文件是否符合 UTF-8 without BOM 规范。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:273-285
  - source contains utf-8-sig
- 建议的新断言：读取工具同时报告 BOM；测试需区分可解析与编码规范合规，不用 utf-8-sig 掩盖 BOM。
- 是否降低测试强度：`false`

#### `test_all_representation_page_counts_nonnegative` (lines 289-295)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert all(isinstance(r['page_count'],int) and r['page_count']>=0 for r in reps) | assert sum(r['page_count'] for r in reps if r['format']=='pdf')==524`
- 问题：包含硬编码数量或边界；这些值必须由对应 manifest/gate/checkpoint/原始证据支持。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:289-295
  - AST/source contains numeric equality, len/sum count, or fixed boundary assertions
- 建议的新断言：保留断言但在 justification 中绑定对应 manifest/gate/checkpoint 证据，禁止用旧数字冒充新运行结果。
- 是否降低测试强度：`false`

#### `test_c023_representation_pair` (lines 299-305)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert sorted(r['page_count'] for r in reps)==[122,122] | assert {r['format'] for r in reps}=={'pdf','docx'}`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:299-305
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

#### `test_report_contains_required_sections` (lines 309-315)

- 测试文件：`tests/test_2025_manual.py`
- 原断言：`assert s in text`
- 问题：静态审计未发现本函数明确的弱化、静默跳过或当前事实冲突。
- 事实或 Schema 证据：
  - AST/source evidence: tests/test_2025_manual.py:309-315
- 建议的新断言：保留当前断言；A4 使用严格共享读取工具复核，A3 不修改测试。
- 是否降低测试强度：`false`

## Unresolved items

### Current global queue/request files are cross-year inputs, while several annual tests assert single-year totals or emptiness.

- Evidence: `progress.json`, `manual_review_queue.jsonl`, `missing_segment_requests.jsonl`, `2015/2017/2018/2020/2022/2024/2025 tests`
- Recommended stage: `A5/A6`

### Some tests skip or return when optional raw source archives are unavailable.

- Evidence: `tests/test_2022_manual.py`, `tests/test_2024_manual.py`
- Recommended stage: `A4`

### Several tests tolerate BOMs or ignore decode errors instead of recording encoding evidence.

- Evidence: `utf-8-sig and errors=ignore occurrences in annual tests`
- Recommended stage: `A4`

### Page and worksheet boundary tests are not uniform: some validate only geometry or internal lower bounds, not actual representation/sheet upper bounds.

- Evidence: `2015-2025 page/sheet function records`
- Recommended stage: `A4`

## A3 conclusion

All 11 annual test files and all discovered test functions were audited from their current source text. This file records suggested assertion and framework changes only; implementation belongs to A4 or later and is not performed in A3.
