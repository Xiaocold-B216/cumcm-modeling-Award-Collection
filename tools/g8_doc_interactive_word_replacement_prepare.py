from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"
STATE = SCALE / "g8_run_state.json"


def main() -> int:
    state = json.loads(STATE.read_text(encoding="utf-8-sig"))
    state.update(
        {
            "current_stage": "G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT",
            "status": "USER_ACTION_REQUIRED",
            "g8_doc_replacement_runner_ready": 1,
            "g8_doc_replacement_preflight_pass": 1,
            "g8_doc_replacement_user_action_required": 1,
            "g8_doc_replacement_conversion_run": 0,
            "g8_doc_replacement_paper_id": "CUMCM-2014-D-003",
            "g8_doc_replacement_source_sha256": "2C45B7888C43355B39D0BC01726D842D4744C55DC1E2F8AF829B7DB9D8D4AA35",
            "g8_doc_replacement_source_size": 568832,
            "g8_doc_replacement_existing_paper_conversion_rerun": 0,
            "g8_doc_replacement_existing_paper_pdf_qa_rerun": 0,
            "g8_doc_replacement_existing_paper_extraction_rerun": 0,
            "g8_doc_replacement_existing_paper_determinism_rerun": 0,
            "g8_doc_replacement_word_com_run": 0,
            "g8_doc_replacement_doc_batch_run": 0,
            "g8_doc_replacement_formal_artifact_generation_run": 0,
            "g8_doc_replacement_source_sha_mismatch": 0,
            "g8_doc_replacement_g3_modified": 0,
            "g8_doc_replacement_q3_run": 0,
            "g8_doc_replacement_image_run": 0,
            "g8_doc_replacement_g9_run": 0,
            "g8_doc_replacement_g10_run": 0,
            "next_resume_action": "USER_RUN_DOC_REPLACEMENT_PILOT",
        }
    )
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_DOC_INTERACTIVE_WORD_PILOT_REPLACEMENT.md").write_text(
        "# G8 DOC Interactive Word Pilot Replacement\n\n"
        "Status: USER_ACTION_REQUIRED\n\n"
        "- Replacement: CUMCM-2014-D-003.\n"
        "- Deterministic source preflight passed: size 568832, SHA256 and OLE D0CF11E0A1B11AE1.\n"
        "- Replacement mode is implemented in the existing runner and PowerShell 5.1 parsing passed.\n"
        "- No Word COM, DOC open, PDF conversion, PDF QA, extraction, OCR, or formal Artifact generation was run in this session.\n"
        "- Existing PAPER samples were not rerun.\n\n"
        "Run exactly once in a normal logged-in Windows desktop PowerShell:\n\n"
        "Set-Location D:\\cumcm-modeling-Award-Collection\n"
        "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\tools\\51_g8_doc_interactive_word_pilot.ps1 -ReplacementPaperId CUMCM-2014-D-003\n",
        encoding="utf-8",
    )
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "g8_doc_interactive_word_replacement.log").write_text(
        "stage=G8-DOC-INTERACTIVE-WORD-PILOT-REPLACEMENT\n"
        "status=USER_ACTION_REQUIRED\n"
        "replacement_paper_id=CUMCM-2014-D-003\n"
        "replacement_preflight_pass=1\n"
        "replacement_runner_ready=1\n"
        "replacement_conversion_run=0\n"
        "word_com_run=0\n"
        "existing_paper_conversion_rerun=0\n"
        "doc_batch_run=0\n"
        "formal_artifact_generation_run=0\n"
        "next=USER_RUN_DOC_REPLACEMENT_PILOT\n",
        encoding="utf-8",
    )
    print("REPLACEMENT_PREPARATION_OUTPUTS_WRITTEN=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
