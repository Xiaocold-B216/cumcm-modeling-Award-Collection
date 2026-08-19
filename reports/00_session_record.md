# CUMCM 优秀论文仓库修复 - 工作会话记录

> 日期：2026-08-19
> 操作人：byron (Claude Code 辅助)

---

## 1. 项目基本信息

| 项目 | 值 |
|---|---|
| 仓库地址 | https://github.com/Xiaocold-B216/cumcm-modeling-Award-Collection |
| 本地路径 | `C:\Users\byron\cumcm-modeling-Award-Collection` |
| 工作分支 | `library-refactor-v1` |
| 基线 commit | `a042ecf898feaba6fc81d543a10e0188db8b2b12` |
| 基线 commit message | `data: import award papers 2024-2025` |
| 基线日期 | 2026-08-19 |
| 克隆方式 | `git clone --filter=blob:none --sparse` (partial clone) |
| 修复方案文档 | `CUMCM_Award_Collection_Repair_Plan_V1.0.md` |

---

## 2. 已完成的工作

### 2.1 Phase 0: 建立冻结基线

- [x] 克隆仓库（partial clone，tree 对象完整）
- [x] 创建工作分支 `library-refactor-v1`（从 main 分支创建，未修改任何其他分支）
- [x] 记录基线 commit SHA

### 2.2 仓库目录结构盘点（通过 git ls-tree 完成）

仓库顶层包含 34 个年份目录（1992-2025）+ README.md + .gitattributes：

```
1992年数学建模国赛优秀论文/
1993年数学建模国赛真题+优秀论文/
...
2025年数学建模国赛真题+优秀论文/
README.md
.gitattributes
```

---

## 3. 2015 目录详细结构（29 个文件）

### 3.1 2015年优秀论文/

**A题：太阳影子定位**
- 2015A：太阳影子定位 (1).pdf ~ (7).pdf（7篇）

**B题：互联网+时代的出租车资源配置**
- 2015B：互联网+时代的出租车资源配置 (1).pdf ~ (5).pdf（5篇）

**C题：月上柳梢头，人约黄昏后**
- 2015C：月上柳梢头，人约黄昏后 (1).docx, (2).docx（2篇DOCX）
- 2015C：月上柳梢头，人约黄昏后 (3).pdf, (4).pdf（2篇PDF）

**D题：众筹建筑屋顶方案设计**
- 2015D：众筹建筑屋顶方案设计 (1).doc, (2).doc（2篇DOC）
- 2015D：众筹建筑屋顶方案设计 (3).pdf（1篇PDF）

### 3.2 2015年赛题/

- 2015年国赛A题.doc + 附件1-3.xls + 附件4下载说明.doc
- 2015年国赛B题.doc
- 2015年国赛C题.docx
- 2015年国赛D题.doc + 附件1 + 附件2.pdf + 附件3.pdf
- 全国大学生数学建模竞赛论文格式规范.doc

---

## 4. 2025 目录详细结构（107 个文件）

### 4.1 2025年数学建模赛真题！/

**A题/** - A题.pdf + 附件(result1-3.xlsx)
**B题/** - B题.pdf + 附件(附件1-4.xlsx)
**C题/** - C题.pdf + 附件.xlsx
**D题/** - D题.pdf + 附件(附件1-2.xlsx + 附件3/含多个result*.xlsx)
**E题/** - E题.pdf + 附件(附件1/含txt+xlsx+mp4, 附件2.jpg, 附件3/含多个xlsx+mp4)

### 4.2 2025数学建模赛优秀论文/

（结构待确认，tree 对象中存在但未完全列出）

---

## 5. 未完成的工作

### 5.1 阻塞问题：网络连接不稳定

所有尝试均因 `curl 56 Recv failure: Connection was reset` 失败：

| 方法 | 结果 |
|---|---|
| `git clone` (完整) | 失败 - 连接重置 |
| `git clone --depth 1` | 失败 - 连接重置 |
| `git clone --filter=blob:none` | tree 下载成功，blob 失败 |
| `git clone --filter=blob:none --sparse` | **成功** - tree 完整 |
| `git sparse-checkout set` (拉取blob) | 失败 - 连接重置 |
| `curl` 下载 zip | 下载到 ~130MB 后失败 |
| 增大 http.postBuffer | 无效 |
| 断点续传 | GitHub 不支持 |

### 5.2 待完成步骤

1. **拉取 2015 和 2025 文件内容** - 在仓库目录执行：
   ```bash
   cd C:\Users\byron\cumcm-modeling-Award-Collection
   git sparse-checkout set "2015年数学建模国赛真题+优秀论文" "2025年数学建模国赛真题+优秀论文"
   ```

2. **Phase 0 基线报告** - 生成 `reports/00_baseline.md`

3. **Phase 1 全仓库只读盘点** - 生成 `catalog/files.csv`, `catalog/manifest.jsonl`

4. **Phase 2 论文身份体系** - 建立 Paper ID

5. **Phase 3 PDF 健康检查** - 生成 `catalog/pdf_quality.csv`

6. 后续按方案执行...

---

## 6. 下次继续的步骤

### 方案 A：网络恢复后直接继续

```bash
cd C:\Users\byron\cumcm-modeling-Award-Collection

# 1. 确认在正确分支上
git branch --show-current
# 应输出: library-refactor-v1

# 2. 拉取 2015 和 2025 文件
git sparse-checkout set "2015年数学建模国赛真题+优秀论文" "2025年数学建模国赛真题+优秀论文"

# 3. 验证文件
ls "2015年数学建模国赛真题+优秀论文/"
ls "2025年数学建模国赛真题+优秀论文/"

# 4. 开始 Phase 0 基线报告
```

### 方案 B：如果 git 持续失败

手动从 GitHub 网页下载：
1. 访问 https://github.com/Xiaocold-B216/cumcm-modeling-Award-Collection
2. 下载 2015 和 2025 目录的 zip
3. 解压到本地仓库对应目录

### 方案 C：换网络环境重试

- 使用手机热点
- 使用 VPN
- 使用代理

---

## 7. 注意事项

- **不要动 main 分支** - 所有工作在 `library-refactor-v1` 上进行
- **不要删除原始文件** - 按方案，原件永远保留
- **不要静默覆盖** - 所有操作生成新文件
- **SHA-256 必须 100% 覆盖** - 每个文件都要记录哈希
- **不确定的信息标记 unknown** - 不要猜测论文信息

---

*本文件由 Claude Code 自动生成，用于记录工作进度和下次继续的起点。*
