# G8 DOC Batch Extraction

Status: `USER_ACTION_REQUIRED`

- Frozen targets: 17 rows / 17 unique Paper IDs.
- Preflight: missing=0, SHA mismatch=0, format drift=0, eligibility drift=0, membership drift=0.
- Pilot reuse: 3 (hash drift=0); Word conversion required: 14.
- The runner is resumable, uses one stage-owned Word session per pending DOC, opens sources ReadOnly, disables macros, exports only to isolated derivatives, and never force-kills Word.
- This Codex session did not start Word, convert DOCs, run PDF QA, extract text, OCR, generate Formal Artifacts, or modify backlog/Eligibility/Q3/Image/G3/G9/G10.

Run the single user command below in a normal logged-in Windows desktop PowerShell, then resume this stage for PDF QA and Artifact closure.

`Set-Location 'D:\cumcm-modeling-Award-Collection'; powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.\tools\52_g8_doc_batch_extraction.ps1'`
