# G11 Manual Sample Review Guide

This is a preparation package for independent human manual/visual/semantic QA. Programmatic prechecks do not equal human review PASS.

## Contract

- Sample contract: `DEFAULT_PROMPT_CONTRACT_NO_REPOSITORY_CONTRACT_FOUND`
- Seed: `CUMCM-G11-MANUAL-SAMPLE-V1`
- Sample fingerprint: `677898FA2C0DE5B8229AC310566A2D0A41465790B5F188320CD2EE46C877D4EF`
- Sample size: `30` = Q3 `12` + DOC `6` + OTHER `12`
- Review units: `90` sampled page units
- Sampling is deterministic SHA256 score plus deterministic year/problem coverage and explicit required risk-case inclusion; it is independent of final quality outcome.
- Rendered pages use the frozen Poppler 25.02.0 binding at 180 DPI. No OCR, PDF text extraction, DOC conversion, Word, or formal-data update was run.

## How to review

1. Open each packet in order from 01 through 30.
2. Inspect `page_A.png`, `page_B.png`, and `page_C.png` against the matching artifact excerpt files.
3. Apply the eight review dimensions in each packet.
4. Fill the central decision sheet; do not fill decisions by inference from hashes or precheck results.
5. Use `PASS`, `MINOR`, `MAJOR`, or `CRITICAL` in `overall_severity`; record the defect category and evidence in `reviewer_comment`.
6. When all 30 are genuinely reviewed, a later approval stage may evaluate the completed decision evidence. This preparation stage does not finalize G11.

## Sample order

| Order | Identity | Stratum | Pages | Risk flags | Packet |
|---:|---|---|---|---|---|
| 01 | `CUMCM-2020-B-005` | `Q3_OCR_DERIVED` | `1,25,50` | `MANDATORY_BINARY_MATRIX` | [reports/scale/g11_manual_sample_review/01_CUMCM-2020-B-005/review.md](g11_manual_sample_review/01_CUMCM-2020-B-005/review.md) |
| 02 | `CUMCM-2020-B-002` | `Q3_OCR_DERIVED` | `1,52,104` | `HISTORICAL_TIMEOUT` | [reports/scale/g11_manual_sample_review/02_CUMCM-2020-B-002/review.md](g11_manual_sample_review/02_CUMCM-2020-B-002/review.md) |
| 03 | `CUMCM-2010-A-006` | `Q3_OCR_DERIVED` | `1,74,73` | `VERIFIED_BLANK_PAGE` | [reports/scale/g11_manual_sample_review/03_CUMCM-2010-A-006/review.md](g11_manual_sample_review/03_CUMCM-2010-A-006/review.md) |
| 04 | `CUMCM-2010-B-001` | `Q3_OCR_DERIVED` | `2,1,28` | `VERIFIED_BLANK_PAGE` | [reports/scale/g11_manual_sample_review/04_CUMCM-2010-B-001/review.md](g11_manual_sample_review/04_CUMCM-2010-B-001/review.md) |
| 05 | `CUMCM-2020-D-003` | `Q3_OCR_DERIVED` | `1,68,135` | `LONG_OCR_HEAVY` | [reports/scale/g11_manual_sample_review/05_CUMCM-2020-D-003/review.md](g11_manual_sample_review/05_CUMCM-2020-D-003/review.md) |
| 06 | `CUMCM-1992-A-004` | `Q3_OCR_DERIVED` | `1,2,3` | `NONE` | [reports/scale/g11_manual_sample_review/06_CUMCM-1992-A-004/review.md](g11_manual_sample_review/06_CUMCM-1992-A-004/review.md) |
| 07 | `CUMCM-1993-B-002` | `Q3_OCR_DERIVED` | `1,5,9` | `NONE` | [reports/scale/g11_manual_sample_review/07_CUMCM-1993-B-002/review.md](g11_manual_sample_review/07_CUMCM-1993-B-002/review.md) |
| 08 | `CUMCM-1995-B-004` | `Q3_OCR_DERIVED` | `1,2,3` | `NONE` | [reports/scale/g11_manual_sample_review/08_CUMCM-1995-B-004/review.md](g11_manual_sample_review/08_CUMCM-1995-B-004/review.md) |
| 09 | `CUMCM-1996-B-002` | `Q3_OCR_DERIVED` | `1,3,5` | `NONE` | [reports/scale/g11_manual_sample_review/09_CUMCM-1996-B-002/review.md](g11_manual_sample_review/09_CUMCM-1996-B-002/review.md) |
| 10 | `CUMCM-1997-B-001` | `Q3_OCR_DERIVED` | `1,2,3` | `NONE` | [reports/scale/g11_manual_sample_review/10_CUMCM-1997-B-001/review.md](g11_manual_sample_review/10_CUMCM-1997-B-001/review.md) |
| 11 | `CUMCM-1998-A-004` | `Q3_OCR_DERIVED` | `1,3,6` | `NONE` | [reports/scale/g11_manual_sample_review/11_CUMCM-1998-A-004/review.md](g11_manual_sample_review/11_CUMCM-1998-A-004/review.md) |
| 12 | `CUMCM-2002-A-014` | `Q3_OCR_DERIVED` | `1,5,9` | `NONE` | [reports/scale/g11_manual_sample_review/12_CUMCM-2002-A-014/review.md](g11_manual_sample_review/12_CUMCM-2002-A-014/review.md) |
| 13 | `CUMCM-2011-D-001` | `DOC_REMEDIATED` | `1,11,22` | `DOC_EXISTING_CONVERSION_EVIDENCE` | [reports/scale/g11_manual_sample_review/13_CUMCM-2011-D-001/review.md](g11_manual_sample_review/13_CUMCM-2011-D-001/review.md) |
| 14 | `CUMCM-2012-D-001` | `DOC_REMEDIATED` | `1,12,24` | `DOC_EXISTING_CONVERSION_EVIDENCE` | [reports/scale/g11_manual_sample_review/14_CUMCM-2012-D-001/review.md](g11_manual_sample_review/14_CUMCM-2012-D-001/review.md) |
| 15 | `CUMCM-2013-D-001` | `DOC_REMEDIATED` | `1,41,81` | `DOC_EXISTING_CONVERSION_EVIDENCE` | [reports/scale/g11_manual_sample_review/15_CUMCM-2013-D-001/review.md](g11_manual_sample_review/15_CUMCM-2013-D-001/review.md) |
| 16 | `CUMCM-2014-D-003` | `DOC_REMEDIATED` | `1,17,33` | `DOC_EXISTING_CONVERSION_EVIDENCE` | [reports/scale/g11_manual_sample_review/16_CUMCM-2014-D-003/review.md](g11_manual_sample_review/16_CUMCM-2014-D-003/review.md) |
| 17 | `CUMCM-2011-A-003` | `DOC_REMEDIATED` | `1,8,16` | `DOC_EXISTING_CONVERSION_EVIDENCE` | [reports/scale/g11_manual_sample_review/17_CUMCM-2011-A-003/review.md](g11_manual_sample_review/17_CUMCM-2011-A-003/review.md) |
| 18 | `CUMCM-2012-B-007` | `DOC_REMEDIATED` | `1,17,33` | `DOC_EXISTING_CONVERSION_EVIDENCE` | [reports/scale/g11_manual_sample_review/18_CUMCM-2012-B-007/review.md](g11_manual_sample_review/18_CUMCM-2012-B-007/review.md) |
| 19 | `CUMCM-1999-B-003` | `OTHER_FORMAL_DERIVED` | `1,3,6` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/19_CUMCM-1999-B-003/review.md](g11_manual_sample_review/19_CUMCM-1999-B-003/review.md) |
| 20 | `CUMCM-2008-C-004` | `OTHER_FORMAL_DERIVED` | `1,7,14` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/20_CUMCM-2008-C-004/review.md](g11_manual_sample_review/20_CUMCM-2008-C-004/review.md) |
| 21 | `CUMCM-2022-E-E014` | `OTHER_FORMAL_DERIVED` | `1,12,24` | `MULTI_MEMBERSHIP` | [reports/scale/g11_manual_sample_review/21_CUMCM-2022-E-E014/review.md](g11_manual_sample_review/21_CUMCM-2022-E-E014/review.md) |
| 22 | `CUMCM-2021-C-C085` | `OTHER_FORMAL_DERIVED` | `1,28,56` | `MULTI_MEMBERSHIP` | [reports/scale/g11_manual_sample_review/22_CUMCM-2021-C-C085/review.md](g11_manual_sample_review/22_CUMCM-2021-C-C085/review.md) |
| 23 | `CUMCM-1992-A-003` | `OTHER_FORMAL_DERIVED` | `1,3,5` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/23_CUMCM-1992-A-003/review.md](g11_manual_sample_review/23_CUMCM-1992-A-003/review.md) |
| 24 | `CUMCM-1993-B-001` | `OTHER_FORMAL_DERIVED` | `1,1,2` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/24_CUMCM-1993-B-001/review.md](g11_manual_sample_review/24_CUMCM-1993-B-001/review.md) |
| 25 | `CUMCM-1996-B-001` | `OTHER_FORMAL_DERIVED` | `1,3,5` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/25_CUMCM-1996-B-001/review.md](g11_manual_sample_review/25_CUMCM-1996-B-001/review.md) |
| 26 | `CUMCM-1997-A-008` | `OTHER_FORMAL_DERIVED` | `1,3,5` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/26_CUMCM-1997-A-008/review.md](g11_manual_sample_review/26_CUMCM-1997-A-008/review.md) |
| 27 | `CUMCM-1998-A-007` | `OTHER_FORMAL_DERIVED` | `1,3,5` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/27_CUMCM-1998-A-007/review.md](g11_manual_sample_review/27_CUMCM-1998-A-007/review.md) |
| 28 | `CUMCM-2000-A-005` | `OTHER_FORMAL_DERIVED` | `1,5,9` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/28_CUMCM-2000-A-005/review.md](g11_manual_sample_review/28_CUMCM-2000-A-005/review.md) |
| 29 | `CUMCM-2001-A-001` | `OTHER_FORMAL_DERIVED` | `1,3,6` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/29_CUMCM-2001-A-001/review.md](g11_manual_sample_review/29_CUMCM-2001-A-001/review.md) |
| 30 | `CUMCM-2002-B-005` | `OTHER_FORMAL_DERIVED` | `1,4,7` | `GOVERNED_DUPLICATE` | [reports/scale/g11_manual_sample_review/30_CUMCM-2002-B-005/review.md](g11_manual_sample_review/30_CUMCM-2002-B-005/review.md) |

## Defect levels

- `CRITICAL`: wrong paper/identity/source, unrelated paper content, or large-scale artifact corruption.
- `MAJOR`: material missing section, meaning-changing OCR/formula/number corruption, page-order corruption, or unusable major table.
- `MINOR`: isolated OCR character, line-break, punctuation, or layout issue that does not change main semantics.
- `PASS`: no human-visible substantive issue.

## Non-negotiable handoff

The initial decision sheet is entirely `PENDING`. The human reviewer, not Codex, must supply reviewer identity/decision evidence. Do not proceed to G12 from this preparation package.
