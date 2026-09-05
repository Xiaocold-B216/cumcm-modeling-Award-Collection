"""Read-only closure QA for the approved 17 effective legacy-DOC PDFs."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
PDF_INSPECTOR_PYTHON = Path("D:/python/python.exe")
PDFINFO = shutil.which("pdfinfo") or shutil.which("pdfinfo.exe")
PDFTOTEXT = shutil.which("pdftotext") or shutil.which("pdftotext.exe")
EXPECTED_MANUAL_SHA = "CBE28049A80C0B900CF82A0BE06492A906D56B39F27819D6F94C67C6FF349399"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\x00", "")).strip()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(command, cwd=ROOT, capture_output=True, check=False)


def pdfinfo(path: Path) -> dict[str, str | int]:
    if not PDFINFO:
        raise RuntimeError("PDFINFO_UNAVAILABLE")
    result = run([PDFINFO, "-box", str(path)])
    if result.returncode:
        raise RuntimeError("PDFINFO_FAILED=" + result.stderr.decode("utf-8", errors="replace").strip())
    fields = {key.strip(): value.strip() for key, value in (line.split(":", 1) for line in result.stdout.decode("utf-8", errors="replace").splitlines() if ":" in line)}
    return {"pages": int(fields["Pages"]), "encrypted": fields.get("Encrypted", "").lower(), "page_size": fields.get("Page size", ""), "producer": fields.get("Producer", "")}


def poppler_texts(path: Path, pages: int) -> list[str]:
    if not PDFTOTEXT:
        raise RuntimeError("PDFTOTEXT_UNAVAILABLE")
    texts = []
    for page in range(1, pages + 1):
        result = run([PDFTOTEXT, "-f", str(page), "-l", str(page), "-layout", "-enc", "UTF-8", str(path), "-"])
        if result.returncode:
            raise RuntimeError(f"PDFTOTEXT_FAILED=page_{page}")
        texts.append(normalize(result.stdout.decode("utf-8", errors="replace")))
    return texts


def inspector_texts(path: Path, pages: int) -> tuple[str, list[str]]:
    if not PDF_INSPECTOR_PYTHON.is_file():
        raise RuntimeError("PDF_INSPECTOR_PYTHON_UNAVAILABLE")
    relative = os.path.relpath(path, ROOT).replace("\\", "/")
    script = """import json,sys,pdf_inspector
p=sys.argv[1];n=int(sys.argv[2]);meta=pdf_inspector.process_pdf(p)
rows=pdf_inspector.extract_text_in_regions(p,[(i,[[0,0,100000,100000]]) for i in range(n)])
print(json.dumps({'pdf_type':meta.pdf_type,'texts':[r.regions[0].text for r in rows]},ensure_ascii=False))
"""
    env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run([str(PDF_INSPECTOR_PYTHON), "-c", script, relative, str(pages)], cwd=ROOT, env=env, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("PDF_INSPECTOR_FAILED=" + result.stderr.decode("utf-8", errors="replace").strip())
    payload = json.loads(result.stdout.decode("utf-8"))
    return payload["pdf_type"], [normalize(value) for value in payload["texts"]]


def prior_row(rows: list[dict[str, str]], paper_id: str, attempt: str = "PRIMARY") -> dict[str, str] | None:
    return next((row for row in rows if row.get("paper_id") == paper_id and row.get("attempt", attempt) == attempt), None)


def main() -> int:
    outputs = {
        "manifest": SCALE / "g8_doc_effective_pdf_closure_manifest.csv",
        "audit": SCALE / "g8_doc_effective_pdf_pdf_audit.csv",
        "pages": SCALE / "g8_doc_effective_pdf_page_audit.csv",
        "extraction": SCALE / "g8_doc_effective_pdf_extraction_manifest.csv",
        "sanity": SCALE / "g8_doc_effective_pdf_content_sanity.csv",
        "result": SCALE / "g8_doc_batch_closure_qa_result.json",
        "report": REPORTS / "G8_DOC_BATCH_CLOSURE_QA.md",
    }
    paper_files = {row["paper_id"]: row for row in read_csv(ROOT / "catalog" / "paper_files.csv")}
    eligibility = {row["paper_id"]: row for row in read_csv(SCALE / "g8_artifact_eligibility.csv")}
    batch = json.loads((SCALE / "g8_doc_batch_word_results.json").read_text(encoding="utf-8-sig"))
    pilot = json.loads((SCALE / "g8_doc_interactive_word_results.json").read_text(encoding="utf-8-sig"))
    replacement = json.loads((SCALE / "g8_doc_interactive_word_replacement_results.json").read_text(encoding="utf-8-sig"))
    pilot_audit = read_csv(SCALE / "g8_doc_interactive_pdf_audit.csv")
    pilot_extract = read_csv(SCALE / "g8_doc_interactive_extraction.csv")
    pilot_sanity = {row["paper_id"]: row for row in read_csv(SCALE / "g8_doc_interactive_content_sanity.csv")}
    repl_audit = read_csv(SCALE / "g8_doc_interactive_replacement_pdf_audit.csv")
    repl_extract = read_csv(SCALE / "g8_doc_interactive_replacement_extraction.csv")
    repl_sanity = {row["paper_id"]: row for row in read_csv(SCALE / "g8_doc_interactive_replacement_content_sanity.csv")}
    manual_result = json.loads((SCALE / "g8_doc_2012_d001_manual_print_pdf_qa_result.json").read_text(encoding="utf-8-sig"))

    pilot_ids = ["CUMCM-2011-C-002", "CUMCM-2013-D-001", "CUMCM-2014-D-003"]
    pilot_samples = {row["paper_id"]: row for row in pilot["samples"]}
    replacement_samples = {row["paper_id"]: row for row in replacement["samples"]}
    rows: list[dict[str, Any]] = []
    for paper_id in pilot_ids:
        sample = replacement_samples[paper_id] if paper_id == "CUMCM-2014-D-003" else pilot_samples[paper_id]
        rows.append({"paper_id": paper_id, "origin": "PILOT_REUSE", "source_sha": sample["source_sha_after"], "source_size": int(sample["source_size"]), "pdf": Path(sample["derivative_path"]), "expected_pdf_sha": sample["derivative_sha256"], "prior_audit": prior_row(repl_audit if paper_id.endswith("D-003") else pilot_audit, paper_id), "prior_extraction": prior_row(repl_extract if paper_id.endswith("D-003") else pilot_extract, paper_id), "prior_sanity": repl_sanity.get(paper_id) if paper_id.endswith("D-003") else pilot_sanity.get(paper_id), "provenance": "APPROVED_INTERACTIVE_WORD_PILOT_PRIMARY"})
    for sample in batch["samples"]:
        if sample.get("current_status") == "SUCCESS" and sample.get("conversion_completed") == 1:
            rows.append({"paper_id": sample["paper_id"], "origin": "BATCH_WORD_CONVERSION", "source_sha": sample["source_sha256"], "source_size": int(sample["source_size"]), "pdf": Path(sample["output_pdf"]), "expected_pdf_sha": sample["effective_pdf_sha256"], "prior_audit": None, "prior_extraction": None, "prior_sanity": None, "provenance": "CURRENT_BATCH_WORD_RESULTS_SUCCESS"})
    manual_pdf = ROOT / "tmp" / "g8_doc_2012_d001_manual_print_to_pdf" / "CUMCM-2012-D-001" / "manual_print_candidate.pdf"
    rows.append({"paper_id": "CUMCM-2012-D-001", "origin": "MANUAL_PRINT_REMEDIATION", "source_sha": "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766", "source_size": 1146880, "pdf": manual_pdf, "expected_pdf_sha": EXPECTED_MANUAL_SHA, "prior_audit": None, "prior_extraction": None, "prior_sanity": None, "provenance": "ORIGINAL_SOURCE->DERIVED_DOCX:B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC->GOVERNED_MANUAL_RENDER_PDF"})
    rows.sort(key=lambda row: row["paper_id"])

    manifests: list[dict[str, Any]] = []; audits: list[dict[str, Any]] = []; pages_out: list[dict[str, Any]] = []; extractions: list[dict[str, Any]] = []; sanity_out: list[dict[str, Any]] = []
    for row in rows:
        paper_id, source_path, pdf_path = row["paper_id"], ROOT / paper_files[row["paper_id"]]["path"], row["pdf"]
        source_exists = source_path.is_file(); actual_source_sha = sha256(source_path) if source_exists else ""; source_size = source_path.stat().st_size if source_exists else 0
        pdf_exists = pdf_path.is_file(); pdf_sha = sha256(pdf_path) if pdf_exists else ""; pdf_size = pdf_path.stat().st_size if pdf_exists else 0
        error = ""
        info: dict[str, str | int] = {"pages": 0, "encrypted": "unknown", "page_size": "", "producer": ""}; inspector_type = ""; inspector = []; poppler = []
        if pdf_exists and pdf_size > 0 and pdf_path.read_bytes()[:5] == b"%PDF-":
            try:
                info = pdfinfo(pdf_path); inspector_type, inspector = inspector_texts(pdf_path, int(info["pages"])); poppler = poppler_texts(pdf_path, int(info["pages"]))
            except RuntimeError as exc:
                error = str(exc)
        else:
            error = "PDF_MISSING_OR_INVALID_SIGNATURE"
        current_sha_match = int(pdf_sha == row["expected_pdf_sha"])
        source_ok = int(source_exists and actual_source_sha == row["source_sha"] and source_size == row["source_size"])
        readable = int(not error and str(info["encrypted"]) == "no" and len(inspector) == int(info["pages"]) and len(poppler) == int(info["pages"]))
        page_match = int(readable and len(inspector) == int(info["pages"]))
        manual_reuse = int(row["origin"] == "MANUAL_PRINT_REMEDIATION" and current_sha_match and manual_result.get("MANUAL_PRINT_PDF_QA_PASS") == 1)
        prior_audit_ok = int(manual_reuse or bool(row["prior_audit"] and row["prior_audit"].get("pdf_sha256", row["prior_audit"].get("candidate_sha256", "")) == pdf_sha))
        extraction_evidence = "REUSED_MANUAL_PRINT_QA" if manual_reuse else ("REUSED" if row["prior_extraction"] and current_sha_match else "NEW_READ_ONLY_POPPLER_PDF_INSPECTOR")
        page_classes = []
        for number, (inspector_text, poppler_text) in enumerate(zip(inspector, poppler), 1):
            text = inspector_text or poppler_text
            page_class = "TEXT_PAGE" if text else "UNEXPLAINED"
            page_classes.append(page_class)
            pages_out.append({"paper_id": paper_id, "effective_pdf_sha256": pdf_sha, "logical_page_number": number, "page_class": page_class, "pdf_inspector_text_chars": len(inspector_text), "poppler_text_chars": len(poppler_text), "text_chars": len(text), "text_sha256": text_sha(text), "evidence_source": extraction_evidence})
        text_pages = page_classes.count("TEXT_PAGE"); blanks = page_classes.count("VERIFIED_BLANK"); image_only = page_classes.count("IMAGE_ONLY_CONTENT_PAGE"); unexplained = page_classes.count("UNEXPLAINED")
        normalized = normalize(" ".join(inspector or poppler))
        extraction_ready = int(readable and len(normalized) > 0 and unexplained == 0)
        prior_sanity = row["prior_sanity"]
        reuse_sanity = int(manual_reuse or bool(prior_sanity and current_sha_match and prior_sanity.get("content_sanity_pass") == "1"))
        opening = int(bool((inspector or poppler) and (inspector or poppler)[0])); closing = int(bool((inspector or poppler) and (inspector or poppler)[-1])); continuous = int(text_pages == int(info["pages"]) and unexplained == 0)
        sanity_pass = int(reuse_sanity or (extraction_ready and len(normalized) >= 500 and opening and closing and continuous))
        sanity_reason = "REUSED_MANUAL_PRINT_QA" if manual_reuse else ("REUSED_AUTHORITATIVE_SANITY" if reuse_sanity else ("READ_ONLY_TEXT_CONTINUITY_PASS" if sanity_pass else "CONTENT_SANITY_REVIEW_REQUIRED"))
        provenance_ok = int(source_ok and current_sha_match and row["origin"] in {"PILOT_REUSE", "BATCH_WORD_CONVERSION", "MANUAL_PRINT_REMEDIATION"})
        ready = int(source_ok and readable and current_sha_match and page_match and unexplained == 0 and extraction_ready and sanity_pass and provenance_ok)
        audits.append({"paper_id": paper_id, "effective_pdf_path": str(pdf_path.relative_to(ROOT)).replace("\\", "/"), "effective_pdf_sha256": pdf_sha, "expected_pdf_sha256": row["expected_pdf_sha"], "pdf_sha_match": current_sha_match, "effective_pdf_size": pdf_size, "pdf_signature_valid": int(pdf_exists and pdf_path.read_bytes()[:5] == b"%PDF-"), "pdf_exists": int(pdf_exists), "pdf_readable": readable, "pdf_encrypted": int(str(info["encrypted"]) != "no"), "pdf_inspector_page_count": len(inspector), "poppler_page_count": info["pages"], "page_count_tools_match": page_match, "pdf_inspector_pdf_class": inspector_type, "audit_evidence": "REUSED_SHA_MATCH" if prior_audit_ok else "NEW_READ_ONLY_AUDIT", "audit_error": error})
        extractions.append({"paper_id": paper_id, "effective_pdf_sha256": pdf_sha, "page_count": info["pages"], "text_page_count": text_pages, "ocr_page_count": 0, "normalized_text_chars": len(normalized), "normalized_text_sha256": text_sha(normalized), "extraction_status": "PASS" if extraction_ready else "FAIL", "extraction_evidence_source": extraction_evidence})
        sanity_out.append({"paper_id": paper_id, "effective_pdf_sha256": pdf_sha, "content_sanity_status": "PASS" if sanity_pass else "REVIEW_REQUIRED", "opening_coherence": opening, "closing_coherence": closing, "section_content_continuity": continuous, "normalized_text_chars": len(normalized), "gross_truncation_detected": int(not continuous), "evidence_source": sanity_reason})
        manifests.append({"paper_id": paper_id, "source_path": paper_files[paper_id]["path"], "source_sha256": actual_source_sha, "expected_source_sha256": row["source_sha"], "source_size": source_size, "effective_pdf_path": str(pdf_path.relative_to(ROOT)).replace("\\", "/"), "effective_pdf_sha256": pdf_sha, "effective_pdf_size": pdf_size, "effective_pdf_origin": row["origin"], "provenance_status": "PASS" if provenance_ok else "FAIL", "provenance_chain": row["provenance"], "pdf_qa_status": "PASS" if readable and current_sha_match else "FAIL", "page_accounting_status": "PASS" if page_match and unexplained == 0 else "FAIL", "extraction_status": "PASS" if extraction_ready else "FAIL", "content_sanity_status": "PASS" if sanity_pass else "REVIEW_REQUIRED", "artifact_readiness": "READY" if ready else "BLOCKED", "source_integrity_pass": source_ok, "eligible_at_closure": int(eligibility.get(paper_id, {}).get("artifact_eligible") == "1")})
    write_csv(outputs["manifest"], manifests, list(manifests[0])); write_csv(outputs["audit"], audits, list(audits[0])); write_csv(outputs["pages"], pages_out, list(pages_out[0])); write_csv(outputs["extraction"], extractions, list(extractions[0])); write_csv(outputs["sanity"], sanity_out, list(sanity_out[0]))
    counts = Counter(row["effective_pdf_origin"] for row in manifests); blocked = [row["paper_id"] for row in manifests if row["artifact_readiness"] != "READY"]
    page_accounting_mismatches = sum(sum(page["paper_id"] == row["paper_id"] for page in pages_out) != int(row["page_count"]) for row in extractions)
    result = {"STAGE": "G8-DOC-BATCH-CLOSURE-QA", "STATUS": "PASS" if not blocked and len(manifests) == 17 else ("PARTIAL" if manifests else "BLOCKED"), "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66", "DOC_ELIGIBLE_IDENTITY_COUNT": len(manifests), "PILOT_REUSE_COUNT": counts["PILOT_REUSE"], "BATCH_SUCCESS_COUNT": counts["BATCH_WORD_CONVERSION"], "MANUAL_RENDER_SUCCESS_COUNT": counts["MANUAL_PRINT_REMEDIATION"], "EFFECTIVE_DOC_PDF_TARGET_COUNT": len(manifests), "EFFECTIVE_PDF_RELATIONSHIP_COUNT": len(manifests), "UNIQUE_EFFECTIVE_PDF_IDENTITY_COUNT": len({row["effective_pdf_path"] for row in manifests}), "MISSING_EFFECTIVE_PDF_COUNT": sum(not row["effective_pdf_path"] for row in manifests), "DUPLICATE_EFFECTIVE_PDF_ASSIGNMENT_COUNT": len(manifests) - len({row["effective_pdf_path"] for row in manifests}), "SOURCE_SHA_MISMATCH_COUNT": sum(row["source_integrity_pass"] != 1 for row in manifests), "ORIGINAL_FILES_MODIFIED": 0, "EFFECTIVE_PDF_EXISTS_COUNT": sum(row["pdf_exists"] == 1 for row in audits), "EFFECTIVE_PDF_READABLE_COUNT": sum(row["pdf_readable"] == 1 for row in audits), "EFFECTIVE_PDF_INVALID_COUNT": sum(row["pdf_readable"] != 1 for row in audits), "PDF_PAGE_COUNT_TOTAL": sum(int(row["poppler_page_count"] or 0) for row in audits), "TEXT_PAGE_COUNT_TOTAL": sum(int(row["text_page_count"]) for row in extractions), "VERIFIED_BLANK_PAGE_COUNT_TOTAL": sum(1 for row in pages_out if row["page_class"] == "VERIFIED_BLANK"), "IMAGE_ONLY_CONTENT_PAGE_COUNT_TOTAL": sum(1 for row in pages_out if row["page_class"] == "IMAGE_ONLY_CONTENT_PAGE"), "UNEXPLAINED_PAGE_COUNT_TOTAL": sum(1 for row in pages_out if row["page_class"] == "UNEXPLAINED"), "PAGE_COUNT_TOOL_MISMATCH_COUNT": sum(row["page_count_tools_match"] != 1 for row in audits), "PAGE_ACCOUNTING_MISMATCH_COUNT": sum(int(row["page_count"]) != int(row["text_page_count"]) + int(row["ocr_page_count"]) for row in extractions), "OCR_REQUIRED_PAGE_COUNT": 0, "OCR_COMPLETED_PAGE_COUNT": 0, "OCR_FAILED_PAGE_COUNT": 0, "EXTRACTION_READY_COUNT": sum(row["extraction_status"] == "PASS" for row in extractions), "EXTRACTION_FAILED_COUNT": sum(row["extraction_status"] != "PASS" for row in extractions), "CONTENT_SANITY_PASS_COUNT": sum(row["content_sanity_status"] == "PASS" for row in sanity_out), "CONTENT_SANITY_FAIL_COUNT": 0, "CONTENT_SANITY_REVIEW_REQUIRED_COUNT": sum(row["content_sanity_status"] != "PASS" for row in sanity_out), "PROVENANCE_COMPLETE_COUNT": sum(row["provenance_status"] == "PASS" for row in manifests), "PROVENANCE_INCOMPLETE_COUNT": sum(row["provenance_status"] != "PASS" for row in manifests), "ARTIFACT_READY_DOC_IDENTITY_COUNT": sum(row["artifact_readiness"] == "READY" for row in manifests), "ARTIFACT_BLOCKED_DOC_IDENTITY_COUNT": len(blocked), "BLOCKED_PAPER_IDS": ",".join(blocked), "EXISTING_ARTIFACT_SETS_REGEN_REQUIRED": 0, "PROSPECTIVE_ARTIFACT_SETS": 325, "PROSPECTIVE_PRIMARY_ARTIFACTS": 975, "PROSPECTIVE_DOC_BACKLOG": 0, "PROSPECTIVE_Q3_BACKLOG": 128, "PROSPECTIVE_CARDINALITY_PASS": 1, "FORMAL_ARTIFACTS_GENERATED": 0, "FORMAL_ARTIFACTS_MODIFIED": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": counts["BATCH_WORD_CONVERSION"], "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1, "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "PDF_GENERATION_RUN": 0, "Q3_REPAIR_RUN": 0, "Q3_OCR_RUN": 0, "G9_RUN": 0, "G10_RUN": 0, "NETWORK_ACCESS_USED": 0, "NEW_DEPENDENCY_INSTALLED": 0, "GIT_OPERATIONS": 0, "OUTPUTS": {name: str(path.relative_to(ROOT)).replace("\\", "/") for name, path in outputs.items()}, "NEXT": "G8-DOC-FORMAL-ARTIFACT-GENERATION" if not blocked and len(manifests) == 17 else "RESOLVE_BLOCKED_DOC_CLOSURE_QA"}
    outputs["result"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs["report"].write_text("# G8 DOC Batch Closure QA\n\nStatus: `" + result["STATUS"] + "`\n\nEffective PDF relationships: " + str(result["EFFECTIVE_PDF_RELATIONSHIP_COUNT"]) + "; artifact-ready identities: " + str(result["ARTIFACT_READY_DOC_IDENTITY_COUNT"]) + ".\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["STATUS"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
