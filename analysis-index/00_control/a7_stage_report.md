# A7 基础设施修复与最终验收

## 输入与边界

- 仓库分支：`analysis/corpus-index`
- 基线输入提交：`d830e61908334e194cdd5b6a669400fb9d367f75`
- A7 先前阻塞提交：`b4d31fc6bb3b0373464f1f7f92322390e0ab446b`
- 先前格式修复提交：`d07dcfdd41fc778947e768835a13f9e3029f79cd`
- 本轮基础设施修复提交：`d830e61908334e194cdd5b6a669400fb9d367f75`
- 执行使用固定绝对解释器和 `-p no:cacheprovider`；未安装、升级或降级依赖。
- 使用了仓库外、`%TEMP%` 下的 ASCII detached worktree；测试日志不写入仓库。
- A8 未启动。

## 先前阻塞与批准修复

基线对象 `a042ecf898feaba6fc81d543a10e0188db8b2b12` 已通过一次有界 SHA fetch 恢复，最终对象类型为 commit，`cat-file` 回读成功。

先前 `tests/test_infrastructure.py` 为 9 passed、2 failed、0 errors。两项失败分别是：

1. 源保护检查把以下六个根目录派生控制文件误判为源差异：
   `2016_missing_files.txt`、`2017_missing_files.txt`、`2018_missing_files.txt`、`2021_PACKAGE_README.md`、`2022_missing_files.txt`、`2024_missing_files.txt`。
2. Git `-z` 输出使用文本模式读取，在 Windows 默认代码页下解码真实中文路径时失败。

本轮只修改 `scripts/build_index.py`：

- 增加六个精确根目录路径的派生文件集合；统一先规范 Git 路径分隔符，再由同一个谓词用于基线条目和源保护检查。
- 增加字节模式 Git 输出读取，并对 `ls-tree -z`、`status -z`、`diff --name-only -z` 结果执行严格 UTF-8 解码；未使用忽略错误的解码。
- 六个控制文件内容未改动。其当前 blob SHA 与长度为：

| 文件 | blob SHA | 字节数 | 相对基线 |
|---|---|---:|---|
| `2016_missing_files.txt` | `7354a765bd1426f06c14b0c5c3106964df3080ea` | 664 | 新增、派生控制文件 |
| `2017_missing_files.txt` | `9fa1a0b2acf2cc79f306b3275e8c7c974dbdbd2c` | 2309 | 新增、派生控制文件 |
| `2018_missing_files.txt` | `2417d2bad5a91958a99edc38a4fca8ddde3975f6` | 2292 | 新增、派生控制文件 |
| `2021_PACKAGE_README.md` | `a314f561bd8c549a239c87d2276c11b532d090c2` | 460 | 新增、派生控制文件 |
| `2022_missing_files.txt` | `9d9ec11fa9c4f3d09453216f3f6ef6102556495d` | 1648 | 新增、派生控制文件 |
| `2024_missing_files.txt` | `fc3cef9e2f2311cb2fd42e2c8394a293dfc01afe` | 1284 | 新增、派生控制文件 |

## 回归与基础设施验证

- 年度收集：267；其中 2017 年 24；收集、导入、语法错误均为 0。
- 全量收集：306；收集、导入、语法错误均为 0。
- 定向基础设施节点：2 passed、0 failed、0 errors。
- `tests/test_infrastructure.py`：11 passed、0 failed、0 skipped、0 errors，exit 0。
- 平台豁免：未使用；基础设施测试在 ASCII detached worktree 中完整通过。
- 独立基线探针：3614 条；真实中文相对路径未加 Git 引号且对应 checkout 路径存在；原始源修改 0；提交源修改 0；源 blob 哈希差异 0。

年度回归保持既有失败基线：

- 年度 267：240 passed、25 retained failed、2 skipped、0 errors、0 timeout、exit 1。
- 额外正式回归 28：16 passed、12 retained failed、0 errors、exit 1。
- 全量 306：267 passed、37 failed、2 skipped、0 errors、exit 1。
- 基础设施修复没有新增年度失败、额外失败、skip、xfail、timeout 或 collection error；保留失败未被改写或压制。

## 质量门与一致性审计

- Schema：4 个 Draft 2020-12 定义，5314 个映射实例，0 validation errors；计数为 logical 326、feature 4238、representation 367、relation 383。
- 严格结构审计：1620 JSON、570 JSONL、96 分析 CSV、2346 Markdown 均可按既定范围解析；JSON/JSONL 无 BOM，Markdown 无 BOM、均以 LF 结束；JSON 重复键和非有限数为 0。
- Gate/Checkpoint 共享数值差异：0；2021 和 2023 的已记录 remote-readback scope 差异保持不变。
- 队列：global manual review open 1、global missing-segment open 12 且 blocking 12、A5 human-review open 11；重复 ID 0；A5 证据路径孤立项 0。
- 2015—2025 manifest：2157 条；直接可解析路径 107，已验证 107，哈希差异 0；其余 2050 条保持 unresolved/external scope，不被误判为差异。
- A7 范围索引数据相对先前 A7 提交无变化；索引重复 ID 集合 0、field-aware 外键孤立项 0、年份字段差异 0、缺少首选表示 0。
- 风险扫描：未新增 skip/xfail，测试文件无修改，无凭据、个人绝对路径、缓存/临时绝对路径或语法错误。

## 最终判定

`A7 = passed_with_recorded_failures`

该状态表示基础设施验证、全量收集、分类记录、质量门、跨文件一致性和 A7 远端交付条件已完成；不表示全部回归测试通过。必须继续保留并公开记录：25 个年度失败、12 个额外失败、2 个 skip，以及全量汇总中的 37 个失败和 2 个 skip。

`A8 = ready_to_start`

A8 仅被判定为满足前置条件，本轮没有执行 A8，也没有创建 A8 产物。
