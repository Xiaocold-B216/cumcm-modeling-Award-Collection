"""Replay the frozen DOC effective-PDF text contract with Poppler 26.05.0."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
POPPLER_BIN = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin")
PDFINFO = POPPLER_BIN / "pdfinfo.exe"
PDFTOTEXT = POPPLER_BIN / "pdftotext.exe"
PY = Path(r"D:\python\python.exe")
REFERENCE = SCALE / "g8_doc_effective_pdf_closure_manifest.csv"
PAGES = SCALE / "g8_doc_effective_pdf_page_audit.csv"
EXTRACTION = SCALE / "g8_doc_effective_pdf_extraction_manifest.csv"
OUT_REF = SCALE / "g8_poppler_26_05_0_reference_replay.csv"
OUT_PAGES = SCALE / "g8_poppler_26_05_0_page_comparison.csv"
OUT_BODY = SCALE / "g8_poppler_26_05_0_body_comparison.csv"
CONTRACT = SCALE / "g8_poppler_compatibility_contract_v1.json"
RESULT = SCALE / "g8_q3_pdf_toolchain_version_reconciliation_result.json"
REPORT = ROOT / "reports" / "scale" / "G8_Q3_PDF_TOOLCHAIN_VERSION_RECONCILIATION.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(records[0]) if records else ["paper_id"]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(records)


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest().upper()


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\x00", "")).strip()


def command_version(executable: Path) -> str:
    result = subprocess.run([str(executable), "-v"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    return (result.stdout + result.stderr).splitlines()[0].replace("pdfinfo version ", "").replace("pdftotext version ", "").strip()


def pdf_pages(path: Path) -> int:
    result = subprocess.run([str(PDFINFO), str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("PDFINFO_FAILED")
    match = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("PDFINFO_PAGE_COUNT_MISSING")
    return int(match.group(1))


def poppler_pages(path: Path, count: int) -> list[str]:
    values = []
    for number in range(1, count + 1):
        result = subprocess.run([str(PDFTOTEXT), "-f", str(number), "-l", str(number), "-layout", "-enc", "UTF-8", str(path), "-"], capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(f"PDFTOTEXT_FAILED={number}")
        values.append(norm(result.stdout.decode("utf-8", errors="replace")))
    return values


def inspector_pages(path: Path, count: int) -> list[str]:
    relative = os.path.relpath(path, ROOT).replace("\\", "/")
    code = """import json,sys,pdf_inspector
p=sys.argv[1]; n=int(sys.argv[2]); x=pdf_inspector.extract_text_in_regions(p,[(i,[[0,0,100000,100000]]) for i in range(n)]); print(json.dumps([r.regions[0].text for r in x],ensure_ascii=False))"""
    env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run([str(PY), "-c", code, relative, str(count)], cwd=ROOT, env=env, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("PDF_INSPECTOR_FAILED")
    return [norm(item) for item in json.loads(result.stdout.decode("utf-8"))]


def baseline_counts() -> dict[str, int]:
    artifacts = rows(SCALE / "g8_artifact_manifest.csv")
    backlog = rows(SCALE / "g8_manual_backlog.csv")
    eligibility = rows(SCALE / "g8_artifact_eligibility.csv")
    return {"ARTIFACT_SETS": len(artifacts) // 3, "PRIMARY_ARTIFACTS": len(artifacts), "DOC_MANUAL_BACKLOG": sum(row.get("category") == "DOC_REPAIR_MANUAL" for row in backlog), "Q3_MANUAL_BACKLOG": sum(row.get("category") == "Q3_REPAIR_MANUAL" for row in backlog), "ELIGIBLE": sum(row.get("artifact_eligible") == "1" for row in eligibility), "INELIGIBLE": sum(row.get("artifact_eligible") != "1" for row in eligibility)}


def main() -> int:
    reference = sorted(rows(REFERENCE), key=lambda row: row["paper_id"])
    page_rows = rows(PAGES); extraction = {row["paper_id"]: row for row in rows(EXTRACTION)}
    by_paper: dict[str, list[dict[str, str]]] = {}
    for row in page_rows:
        by_paper.setdefault(row["paper_id"], []).append(row)
    result: dict[str, object] = {
        "STAGE": "G8-Q3-PDF-TOOLCHAIN-VERSION-RECONCILIATION", "STATUS": "BLOCKED",
        "BRANCH": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(), "HEAD": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "BASELINE_POPPLER_VERSION": "25.02.0", "CANDIDATE_POPPLER_VERSION": command_version(PDFINFO), "PDF_INSPECTOR_VERSION": importlib.metadata.version("pdf-inspector"),
        "CANDIDATE_PDFINFO_PATH": str(PDFINFO), "CANDIDATE_PDFTOTEXT_PATH": str(PDFTOTEXT), "CANDIDATE_PDFTOTEXT_PRESENT": int(PDFTOTEXT.is_file()),
        "REFERENCE_IDENTITY_COUNT": len(reference), "REFERENCE_PAGE_COUNT": sum(int(row["page_count"]) for row in extraction.values()), "REFERENCE_PDF_SHA_MISMATCH_COUNT": 0,
        "STORED_REFERENCE_PAGE_HASH_COUNT": sum(bool(row.get("text_sha256")) for row in page_rows), "STORED_REFERENCE_BODY_HASH_COUNT": sum(bool(row.get("normalized_text_sha256")) for row in extraction.values()),
        "PAGE_COUNT_MATCH_COUNT": 0, "PAGE_COUNT_MISMATCH_COUNT": 0, "PAGE_TEXT_HASH_MATCH_COUNT": 0, "PAGE_TEXT_HASH_MISMATCH_COUNT": 0,
        "BODY_TEXT_HASH_MATCH_COUNT": 0, "BODY_TEXT_HASH_MISMATCH_COUNT": 0, "BODY_CHAR_COUNT_MATCH_COUNT": 0, "BODY_CHAR_COUNT_MISMATCH_COUNT": 0,
        "PAGE_SEQUENCE_MISMATCH_COUNT": 0, "PAGE_TEXT_PRESENCE_CLASS_MISMATCH_COUNT": 0, "CANDIDATE_POPPLER_COMPATIBLE": 0,
        "POPPLER_COMPATIBILITY_CONTRACT_PREPARED": 0, "APPROVED_POPPLER_VERSION_COUNT": 1, "APPROVED_POPPLER_VERSIONS": "25.02.0", "ACTIVE_POPPLER_VERSION": "", "Q3_PILOT_RUNNER_APPROVED_VERSION_GATE_UPDATED": 0,
        "MISMATCH_PAPER_IDS": "", "MISMATCH_PAGE_IDS": "", "PILOT_TARGET_COUNT": 0, "OCR_RUN": 0, "Q3_OCR_RUN": 0, "FULL_Q3_BATCH_RUN": 0, "FORMAL_ARTIFACTS_GENERATED": 0,
        "EXISTING_ARTIFACT_MODIFICATION_COUNT": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "G9_RUN": 0, "G10_RUN": 0, "GIT_OPERATIONS": 0,
    }
    result.update(baseline_counts())
    replay_records: list[dict[str, object]] = []; page_compare: list[dict[str, object]] = []; body_compare: list[dict[str, object]] = []
    mismatch_papers: set[str] = set(); mismatch_pages: list[str] = []
    try:
        if result["PDF_INSPECTOR_VERSION"] != "1.15.0" or result["CANDIDATE_POPPLER_VERSION"] != "26.05.0":
            raise RuntimeError("CANDIDATE_TOOLCHAIN_VERSION_UNEXPECTED")
        if not PDFTOTEXT.is_file():
            raise RuntimeError("CANDIDATE_PDFTOTEXT_MISSING_FROM_RUNTIME_TREE")
        if result["REFERENCE_IDENTITY_COUNT"] != 17 or result["REFERENCE_PAGE_COUNT"] != 606 or result["STORED_REFERENCE_PAGE_HASH_COUNT"] != 606 or result["STORED_REFERENCE_BODY_HASH_COUNT"] != 17:
            raise RuntimeError("HISTORICAL_REFERENCE_EVIDENCE_INCOMPLETE")
        for ref in reference:
            paper_id = ref["paper_id"]; pdf = ROOT / ref["effective_pdf_path"]; expected_pages = sorted(by_paper.get(paper_id, []), key=lambda row: int(row["logical_page_number"]))
            expected_body = extraction.get(paper_id)
            sha_ok = pdf.is_file() and digest_file(pdf) == ref["effective_pdf_sha256"]
            if not sha_ok:
                result["REFERENCE_PDF_SHA_MISMATCH_COUNT"] += 1; mismatch_papers.add(paper_id); continue
            count = pdf_pages(pdf); count_ok = count == int(expected_body["page_count"])
            result["PAGE_COUNT_MATCH_COUNT"] += int(count_ok); result["PAGE_COUNT_MISMATCH_COUNT"] += int(not count_ok)
            if not count_ok:
                mismatch_papers.add(paper_id); continue
            inspector = inspector_pages(pdf, count); poppler = poppler_pages(pdf, count); chosen = [left or right for left, right in zip(inspector, poppler)]
            sequence_ok = len(chosen) == count == len(expected_pages) and list(range(1, count + 1)) == [int(row["logical_page_number"]) for row in expected_pages]
            result["PAGE_SEQUENCE_MISMATCH_COUNT"] += int(not sequence_ok)
            page_hash_ok = True
            for number, (historic, text, candidate_poppler) in enumerate(zip(expected_pages, chosen, poppler), 1):
                hash_ok = digest_text(text) == historic["text_sha256"]
                expected_presence = int(historic.get("poppler_text_chars", "0") or 0) > 0
                presence_ok = bool(candidate_poppler) == expected_presence and len(candidate_poppler) == int(historic.get("poppler_text_chars", "0") or 0)
                result["PAGE_TEXT_HASH_MATCH_COUNT"] += int(hash_ok); result["PAGE_TEXT_HASH_MISMATCH_COUNT"] += int(not hash_ok)
                result["PAGE_TEXT_PRESENCE_CLASS_MISMATCH_COUNT"] += int(not presence_ok)
                page_hash_ok = page_hash_ok and hash_ok and presence_ok
                if not hash_ok or not presence_ok:
                    mismatch_papers.add(paper_id); mismatch_pages.append(f"{paper_id}:{number}")
                page_compare.append({"paper_id": paper_id, "page_number": number, "baseline_page_text_sha256": historic["text_sha256"], "candidate_page_text_sha256": digest_text(text), "baseline_page_text_chars": historic["text_chars"], "candidate_page_text_chars": len(text), "baseline_poppler_text_chars": historic.get("poppler_text_chars", ""), "candidate_poppler_text_chars": len(candidate_poppler), "page_text_hash_result": "EXACT_MATCH" if hash_ok else "MISMATCH", "text_presence_result": "EXACT_MATCH" if presence_ok else "MISMATCH", "first_bounded_normalized_diff": "" if hash_ok else (text[:200])})
            body = norm(" ".join(chosen)); body_hash_ok = digest_text(body) == expected_body["normalized_text_sha256"]; chars_ok = len(body) == int(expected_body["normalized_text_chars"])
            result["BODY_TEXT_HASH_MATCH_COUNT"] += int(body_hash_ok); result["BODY_TEXT_HASH_MISMATCH_COUNT"] += int(not body_hash_ok); result["BODY_CHAR_COUNT_MATCH_COUNT"] += int(chars_ok); result["BODY_CHAR_COUNT_MISMATCH_COUNT"] += int(not chars_ok)
            if not body_hash_ok or not chars_ok or not page_hash_ok or not sequence_ok:
                mismatch_papers.add(paper_id)
            body_compare.append({"paper_id": paper_id, "baseline_body_sha256": expected_body["normalized_text_sha256"], "candidate_body_sha256": digest_text(body), "baseline_normalized_text_chars": expected_body["normalized_text_chars"], "candidate_normalized_text_chars": len(body), "body_hash_result": "EXACT_MATCH" if body_hash_ok else "MISMATCH", "char_count_result": "EXACT_MATCH" if chars_ok else "MISMATCH"})
            replay_records.append({"paper_id": paper_id, "effective_pdf_path": ref["effective_pdf_path"], "effective_pdf_sha256": ref["effective_pdf_sha256"], "reference_page_count": expected_body["page_count"], "candidate_page_count": count, "page_count_result": "EXACT_MATCH" if count_ok else "MISMATCH", "candidate_pdfinfo_version": result["CANDIDATE_POPPLER_VERSION"], "candidate_pdftotext_version": command_version(PDFTOTEXT)})
        strict_ok = result["REFERENCE_PDF_SHA_MISMATCH_COUNT"] == 0 and result["PAGE_COUNT_MISMATCH_COUNT"] == 0 and result["PAGE_TEXT_HASH_MISMATCH_COUNT"] == 0 and result["BODY_TEXT_HASH_MISMATCH_COUNT"] == 0 and result["BODY_CHAR_COUNT_MISMATCH_COUNT"] == 0 and result["PAGE_SEQUENCE_MISMATCH_COUNT"] == 0 and result["PAGE_TEXT_PRESENCE_CLASS_MISMATCH_COUNT"] == 0
        if strict_ok:
            result.update({"STATUS": "PASS", "CANDIDATE_POPPLER_COMPATIBLE": 1, "POPPLER_COMPATIBILITY_CONTRACT_PREPARED": 1, "APPROVED_POPPLER_VERSION_COUNT": 2, "APPROVED_POPPLER_VERSIONS": "25.02.0,26.05.0", "ACTIVE_POPPLER_VERSION": "26.05.0", "NEXT": "G8-Q3-CONTRACT-PILOT-RESUME", "BLOCKER": "NONE"})
            contract = {"contract_version": "1", "baseline_version": "25.02.0", "approved_versions": ["25.02.0", "26.05.0"], "active_version": "26.05.0", "compatibility_reference_corpus": "17 DOC effective PDFs", "compatibility_reference_identity_count": 17, "compatibility_reference_page_count": 606, "required_semantics": ["PDF readability", "page count", "pdftotext page-scoped -layout UTF-8 extraction", "text-layer presence", "page ordering", "normalized page/body text SHA-256"], "page_hash_match_count": result["PAGE_TEXT_HASH_MATCH_COUNT"], "body_hash_match_count": result["BODY_TEXT_HASH_MATCH_COUNT"], "approval_status": "APPROVED", "historical_normalization_contract": "NUL removal; whitespace normalization; trimmed page join with single spaces; UTF-8 SHA-256"}
            CONTRACT.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            result.update({"STATUS": "BLOCKED", "CANDIDATE_POPPLER_COMPATIBLE": 0, "NEXT": "G8-Q3-POPPLER-25-02-0-RESTORE-DECISION", "BLOCKER": "CANDIDATE_POPPLER_REPLAY_MISMATCH"})
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        result.update({"STATUS": "BLOCKED", "CANDIDATE_POPPLER_COMPATIBLE": 0, "NEXT": "G8-Q3-POPPLER-25-02-0-RESTORE-DECISION", "BLOCKER": str(exc)})
    result["MISMATCH_PAPER_IDS"] = ",".join(sorted(mismatch_papers)); result["MISMATCH_PAGE_IDS"] = ",".join(mismatch_pages)
    write_csv(OUT_REF, replay_records); write_csv(OUT_PAGES, page_compare); write_csv(OUT_BODY, body_compare)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True); REPORT.write_text("# G8 Q3 PDF Toolchain Version Reconciliation\n\n" + "\n".join(f"{key}={value}" for key, value in result.items()) + "\n", encoding="utf-8")
    print("\n".join(f"{key}={value}" for key, value in result.items())); print(f"OUTPUTS={OUT_REF}; {OUT_PAGES}; {OUT_BODY}; {CONTRACT if CONTRACT.exists() else ''}; {RESULT}; {REPORT}")
    return 0 if result["STATUS"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
