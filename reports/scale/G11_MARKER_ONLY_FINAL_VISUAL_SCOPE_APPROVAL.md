# G11 Marker-Only Final Visual Scope Approval

## 1. Human decisions

- `CUMCM-2007-A-003` p.19: `LEGITIMATE_NONCONTENT` — 源页面无应进入论文正文数据库的实质论文内容。
- `CUMCM-2007-B-006` p.41: `SUBSTANTIVE_CONTENT` — 源页面包含应进入论文正文数据库的实质论文内容。
- `CUMCM-2007-B-011` p.2: `LEGITIMATE_NONCONTENT` — 源页面无应进入论文正文数据库的实质论文内容。

These three classifications were explicitly supplied by the user. Codex only transcribed and validated them; no independent visual judgment or automated visual classification was performed.

## 2. Final page closure

- Preexisting confirmed defective pages: `3030`.
- User-confirmed substantive page: `CUMCM-2007-B-006` p.41, classified as `CONFIRMED_DEFECTIVE`.
- User-confirmed legitimate noncontent pages: `CUMCM-2007-A-003` p.19 and `CUMCM-2007-B-011` p.2.
- Final accounting: `3031` confirmed defective + `2` confirmed legitimate noncontent + `0` unresolved = `3033` marker-only pages.
- The defective count is `3031`, not `3033`, because the two legitimate noncontent pages are excluded from repair scope.

## 3. Identity-level scope

The final marker-only repair identity set remains `245`. The two legitimate pages do not remove `CUMCM-2007-A-003` or `CUMCM-2007-B-011` because each identity also has other confirmed defective marker-only pages; `CUMCM-2007-B-006` also remains defective through p.41 and its other pages. The final identity aggregation is `245` defective identities, `2` mixed page-class identities, `0` legitimate-only identities, and `0` unresolved identities.

The complete marker-only scope is frozen. `CUMCM-2020-D-003` remains a separate `Q3_OCR_PAGE` repair target; it does not overlap the 245 marker-only identities, so the total G11 repair target population is `246` identities.

## 4. Gate status

G11 remains `PARTIAL`: scope approval is complete, but formal repair and post-repair human rereview have not been executed. G12 is not run.

Next: `G8-TARGETED-MULTI-ROUTE-FORMAL-ARTIFACT-REPAIR`.

## Outputs

- `catalog/scale/g11_marker_only_final_visual_scope_decisions.csv`
- `catalog/scale/g11_marker_only_final_scope_manifest.csv`
- `catalog/scale/g11_marker_only_final_repair_targets.csv`
- `catalog/scale/g11_marker_only_final_visual_scope_approval_result.json`
