# G11 Post-Repair Human Rereview Guide

Stage: `G11-POST-REPAIR-HUMAN-REREVIEW-PREP`

This guide prepares a human rereview of exactly the 11 original G11 MAJOR identities. It does not expand the scope to all 246 repair targets and does not make a severity decision.

## Required question

For each identity, answer: **Has the issue that originally caused MAJOR now been resolved in the repaired Formal Artifact?**

The prepared evidence contains `33` original review units across `11` identities. Each packet binds the historical review render/excerpt, the current repaired `paper.md` page evidence, and the persisted repair audit.

## Severity contract

- `PASS`: the original MAJOR issue is resolved and the current rereview scope has no substantive quality problem.
- `MINOR`: the original MAJOR issue is resolved, but an isolated minor issue remains that does not change the main content meaning. MINOR may be accepted for final closure, but it must be recorded.
- `MAJOR`: material omission, meaning-changing OCR/digit/formula error, serious page-content loss, or major table/body defect remains.
- `CRITICAL`: identity/source mismatch, unrelated content, broad body corruption, or serious binding failure is found.

## Review procedure

1. Open the packet in the fixed order shown in `00_OVERVIEW.md`.
2. Inspect the existing source render and historical formal excerpt for each Page A/B/C unit. These are authoritative before-state evidence; do not infer the old state from the current artifact.
3. Inspect the linked `current_formal_p<N>.md` excerpt. For marker-route papers it is bounded by strict `source_page` markers. For CUMCM-2020-D-003 it is a deterministic page-text anchor window from current `paper.md`, because that Q3 body has no source-page markers.
4. Compare only the original MAJOR symptom with the repaired content. Do not re-review the entire paper's modeling quality, novelty, or writing style.
5. Write one identity-level decision in `catalog/scale/g11_post_repair_human_rereview_decisions.csv`. Set `new_severity` to one of PASS/MINOR/MAJOR/CRITICAL, write `reviewer_comment`, and change `review_status` to `REVIEWED` only after the human decision is complete.

## Frozen constraints

- This preparation leaves the original G11 decision sheet unchanged.
- The prepared new decision sheet is intentionally 11 rows with all `new_severity=PENDING`, empty `reviewer_comment`, and `review_status=PENDING`.
- G11 remains `PARTIAL` until the human rereview approval stage is completed.
- G10 PASS is a binding and consistency gate; it is not an automatic human PASS for the repaired content.

## Targets

| # | paper_id | original root cause | repaired pages | packet | status |
|---:|---|---|---|---|---|
| 1 | CUMCM-2020-D-003 | TRUE_CONTENT_QUALITY_MAJOR | 1;68;135 | `reports/scale/g11_post_repair_human_rereview/01_CUMCM-2020-D-003` | PENDING |
| 2 | CUMCM-1999-B-003 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5;6 | `reports/scale/g11_post_repair_human_rereview/02_CUMCM-1999-B-003` | PENDING |
| 3 | CUMCM-2008-C-004 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5;6;7;8;9;10;11;12;13;14 | `reports/scale/g11_post_repair_human_rereview/03_CUMCM-2008-C-004` | PENDING |
| 4 | CUMCM-1992-A-003 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5 | `reports/scale/g11_post_repair_human_rereview/04_CUMCM-1992-A-003` | PENDING |
| 5 | CUMCM-1993-B-001 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2 | `reports/scale/g11_post_repair_human_rereview/05_CUMCM-1993-B-001` | PENDING |
| 6 | CUMCM-1996-B-001 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5 | `reports/scale/g11_post_repair_human_rereview/06_CUMCM-1996-B-001` | PENDING |
| 7 | CUMCM-1997-A-008 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5 | `reports/scale/g11_post_repair_human_rereview/07_CUMCM-1997-A-008` | PENDING |
| 8 | CUMCM-1998-A-007 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5 | `reports/scale/g11_post_repair_human_rereview/08_CUMCM-1998-A-007` | PENDING |
| 9 | CUMCM-2000-A-005 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5;6;7;8;9 | `reports/scale/g11_post_repair_human_rereview/09_CUMCM-2000-A-005` | PENDING |
| 10 | CUMCM-2001-A-001 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5;6 | `reports/scale/g11_post_repair_human_rereview/10_CUMCM-2001-A-001` | PENDING |
| 11 | CUMCM-2002-B-005 | FORMAL_ARTIFACT_PAGE_CONTENT_MISSING | 1;2;3;4;5;6;7 | `reports/scale/g11_post_repair_human_rereview/11_CUMCM-2002-B-005` | PENDING |
