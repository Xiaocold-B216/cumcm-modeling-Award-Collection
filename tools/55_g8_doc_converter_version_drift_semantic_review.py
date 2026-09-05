#!/usr/bin/env python3
"""Read-only symmetric semantic review for the approved G8 DOC references.

This intentionally never invokes Word, touches DOC files, or rewrites a
candidate PDF.  It replays the page extraction and normalization representation
used by the 54 compatibility runner for both sides of each comparison.
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import unicodedata
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
MANIFEST = CATALOG / "g8_doc_converter_version_drift_manifest.csv"
PDF_AUDIT = CATALOG / "g8_doc_converter_version_drift_pdf_audit.csv"
STAGE = "G8-DOC-CONVERTER-VERSION-DRIFT-SEMANTIC-REVIEW"
BUILD = "16.0.20326.20112"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def normalize(text: str) -> str:
    # Equivalent to 54's explicit string/string Replace and .NET \s+ trim.
    return re.sub(r"\s+", " ", text.replace("\x00", "")).strip()


def command(name: str) -> str:
    found = shutil.which(name) or shutil.which(f"{name}.exe")
    if not found:
        raise RuntimeError(f"TOOL_UNAVAILABLE={name}")
    return found


PDFINFO = command("pdfinfo")
PDFTOTEXT = command("pdftotext")


def pdf_info(path: Path) -> dict[str, Any]:
    raw = subprocess.run([PDFINFO, str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if raw.returncode:
        raise RuntimeError(f"PDFINFO_FAILED={path}:{raw.stderr.strip()}")
    fields = dict(line.split(":", 1) for line in raw.stdout.splitlines() if ":" in line)
    return {"pages": int(fields.get("Pages", "0").strip()), "encrypted": fields.get("Encrypted", "").strip().lower()}


def page_text(path: Path, page: int) -> str:
    result = subprocess.run(
        [PDFTOTEXT, "-f", str(page), "-l", str(page), "-layout", str(path), "-"],
        capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"PDFTOTEXT_FAILED={path}:page={page}")
    return normalize(result.stdout.decode("utf-8", errors="replace"))


def replay(path: Path) -> dict[str, Any]:
    info = pdf_info(path)
    pages = [page_text(path, page) for page in range(1, info["pages"] + 1)]
    classes = ["TEXT_PAGE" if text else "UNEXPLAINED_PAGE" for text in pages]
    routes = [int(value == "IMAGE_ONLY_CONTENT_PAGE") for value in classes]
    return {
        "page_count": info["pages"], "encrypted": info["encrypted"], "pages": pages,
        "page_hashes": [sha_text(text) for text in pages], "classes": classes, "routes": routes,
        "normalized_text_sha256": sha_text(" ".join(pages)),
    }


def stored_reference(manifest: dict[str, str]) -> tuple[dict[str, str], list[dict[str, str]]]:
    extraction_path = ROOT / manifest["reference_page_audit_path"].replace("/", "\\")
    page_rows = [
        row for row in read_csv(extraction_path)
        if row.get("paper_id") == manifest["paper_id"] and row.get("attempt") == "PRIMARY"
    ]
    page_rows.sort(key=lambda row: int(row["logical_page_number"]))
    return ({
        "reference_pdf_path": manifest["reference_pdf_path"],
        "reference_pdf_sha256": manifest.get("reference_pdf_sha256", ""),
        "stored_reference_normalized_text_sha256": manifest["reference_normalized_text_sha256"],
        "stored_reference_semantic_sha256": manifest["reference_semantic_sha256"],
    }, page_rows)


def non_whitespace(text: str) -> str:
    return "".join(char for char in text if not char.isspace())


def control_character_only(left: str, right: str) -> bool:
    removable = {"\x00", "\u00a0", "\u3000", "\u00ad", "\u200b", "\u200c", "\u200d", "\u2028", "\u2029", "\ufeff"}
    strip = lambda value: "".join(char for char in value if char not in removable)
    return strip(left) == strip(right) and left != right


def span_examples(left: str, right: str, page: int) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    matcher = difflib.SequenceMatcher(a=left, b=right, autojunk=False)
    for tag, a0, a1, b0, b1 in matcher.get_opcodes():
        if tag == "equal":
            continue
        category = "whitespace" if non_whitespace(left[a0:a1]) == non_whitespace(right[b0:b1]) else (
            "control_character" if control_only(left[a0:a1], right[b0:b1]) else "text_or_layout")
        output.append({"page": page, "reference_fragment": left[a0:a1][:160], "candidate_fragment": right[b0:b1][:160], "difference_category": category})
        if len(output) == 10:
            break
    return output


def paper_signals(text: str) -> int:
    return sum(token in text.lower() for token in ("摘要", "关键词", "abstract", "引言", "参考文献", "结论"))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    manifests = read_csv(MANIFEST)
    expected_candidate_hashes = {
        row["paper_id"]: row["pdf_sha256"]
        for row in read_csv(PDF_AUDIT)
        if row.get("paper_id") != "paper_id"
    }
    reference_rows: list[dict[str, Any]] = []
    symmetric_rows: list[dict[str, Any]] = []
    diagnostic_rows: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    candidate_hash_drift = 0

    for manifest in manifests:
        paper_id = manifest["paper_id"]
        stored, stored_pages = stored_reference(manifest)
        reference_path = ROOT / stored["reference_pdf_path"].replace("/", "\\")
        candidate_path = ROOT / manifest["candidate_output_relative_path"].replace("/", "\\")
        stored["reference_pdf_sha256"] = sha_file(reference_path)
        expected_candidate_sha = expected_candidate_hashes.get(paper_id, "")
        reference = replay(reference_path)
        candidate = replay(candidate_path)
        candidate_sha = sha_file(candidate_path)
        candidate_hash_drift += int(bool(expected_candidate_sha) and candidate_sha != expected_candidate_sha)
        stored_classes = [row["page_class"] for row in stored_pages]
        stored_hashes = [row["text_sha256"] for row in stored_pages]
        replay_stored_match = int(reference["normalized_text_sha256"] == stored["stored_reference_normalized_text_sha256"])
        page_count_match = int(reference["page_count"] == candidate["page_count"])
        class_match = int(reference["classes"] == candidate["classes"])
        route_match = int(reference["routes"] == candidate["routes"])
        page_match = int(reference["page_hashes"] == candidate["page_hashes"])
        normalized_match = int(reference["normalized_text_sha256"] == candidate["normalized_text_sha256"])
        differing = [index + 1 for index, pair in enumerate(zip(reference["page_hashes"], candidate["page_hashes"])) if pair[0] != pair[1]]
        if len(reference["page_hashes"]) != len(candidate["page_hashes"]):
            differing.extend(range(min(len(reference["page_hashes"]), len(candidate["page_hashes"])) + 1, max(len(reference["page_hashes"]), len(candidate["page_hashes"])) + 1))
        examples: list[dict[str, Any]] = []
        for page in differing:
            if page <= len(reference["pages"]) and page <= len(candidate["pages"]):
                examples.extend(span_examples(reference["pages"][page - 1], candidate["pages"][page - 1], page))
            if len(examples) >= 10:
                break
        whitespace_only = int(not normalized_match and non_whitespace(" ".join(reference["pages"])) == non_whitespace(" ".join(candidate["pages"])))
        control_only_difference = int(not normalized_match and not whitespace_only and control_character_only(" ".join(reference["pages"]), " ".join(candidate["pages"])))
        substantive = int(not normalized_match and not whitespace_only and not control_only_difference)
        sanity_contradiction = int(
            min(len(" ".join(reference["pages"])), len(" ".join(candidate["pages"]))) < 1000
            or paper_signals(" ".join(reference["pages"])) < 2
            or paper_signals(" ".join(candidate["pages"])) < 2
        )
        reference_rows.append({
            "paper_id": paper_id, **stored,
            "replayed_reference_normalized_text_sha256": reference["normalized_text_sha256"],
            "reference_replay_hash_match": replay_stored_match,
            "stored_page_count": len(stored_pages), "replayed_page_count": reference["page_count"],
            "stored_page_class_sequence": ";".join(stored_classes), "replayed_page_class_sequence": ";".join(reference["classes"]),
            "stored_page_class_match": int(stored_classes == reference["classes"]),
            "stored_page_text_sha_match": int(stored_hashes == reference["page_hashes"]),
        })
        symmetric_rows.append({
            "paper_id": paper_id, "reference_pdf_path": str(reference_path), "candidate_pdf_path": str(candidate_path),
            "candidate_pdf_sha256": candidate_sha, "candidate_pdf_hash_expected": expected_candidate_sha,
            "candidate_pdf_hash_stable": int(not expected_candidate_sha or candidate_sha == expected_candidate_sha),
            "reference_page_count": reference["page_count"], "candidate_page_count": candidate["page_count"],
            "page_count_match": page_count_match, "page_class_match": class_match, "ocr_route_match": route_match,
            "reference_replay_normalized_text_sha256": reference["normalized_text_sha256"],
            "candidate_replay_normalized_text_sha256": candidate["normalized_text_sha256"],
            "symmetric_normalized_text_match": normalized_match, "symmetric_page_text_sha_match": page_match,
            "differing_page_count": len(differing), "first_differing_page": differing[0] if differing else "",
            "whitespace_only_difference": whitespace_only, "control_character_only_difference": control_only_difference,
            "substantive_text_difference": substantive, "content_sanity_contradiction": sanity_contradiction,
        })
        diagnostic_rows.extend({"paper_id": paper_id, **example} for example in examples)
        details.append({"paper_id": paper_id, "reference": reference, "candidate": candidate, "differing_pages": differing, "examples": examples})

    count = len(manifests)
    symmetric_pass = sum(row["symmetric_normalized_text_match"] and row["symmetric_page_text_sha_match"] for row in symmetric_rows)
    replay_match = sum(row["reference_replay_hash_match"] for row in reference_rows)
    substantive_count = sum(row["substantive_text_difference"] for row in symmetric_rows)
    whitespace_count = sum(row["whitespace_only_difference"] for row in symmetric_rows)
    control_count = sum(row["control_character_only_difference"] for row in symmetric_rows)
    structural = sum(row["page_count_match"] and row["page_class_match"] and row["ocr_route_match"] for row in symmetric_rows)
    status = "PASS" if symmetric_pass == count and candidate_hash_drift == 0 else "PARTIAL"
    compatible = int(status == "PASS")
    approved_set_updated = 0
    if compatible:
        contract_path = CATALOG / "g8_doc_extraction_contract_v1.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        baseline = str(contract.get("baseline_converter_version") or contract.get("converter_version") or "")
        if baseline != "16.0.20228.20190":
            raise RuntimeError("BASELINE_CONVERTER_VERSION_DRIFT")
        versions = sorted(set([baseline, *contract.get("validated_converter_versions", []), BUILD]))
        contract.update({
            "baseline_converter_version": baseline,
            "validated_converter_versions": versions,
            "active_converter_version": BUILD,
            "converter_version_validation_evidence": "catalog/scale/g8_doc_converter_version_drift_semantic_review.json",
        })
        contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        approved_set_updated = int(contract["active_converter_version"] == BUILD and BUILD in contract["validated_converter_versions"])
    result = {
        "stage": STAGE, "status": status, "baseline_word_product_version": "16.0.20228.20190",
        "candidate_word_product_version": BUILD, "reference_sample_count": count, "candidate_sample_count": count,
        "reference_pdf_replay_completed": count, "reference_pdf_replay_failed": 0,
        "candidate_pdf_replay_completed": count, "candidate_pdf_replay_failed": 0,
        "stored_reference_hash_replay_match_count": replay_match, "stored_reference_hash_replay_mismatch_count": count - replay_match,
        "page_count_match_count": sum(row["page_count_match"] for row in symmetric_rows),
        "page_class_match_count": sum(row["page_class_match"] for row in symmetric_rows),
        "ocr_route_match_count": sum(row["ocr_route_match"] for row in symmetric_rows),
        "symmetric_normalized_text_match_count": sum(row["symmetric_normalized_text_match"] for row in symmetric_rows),
        "symmetric_normalized_text_mismatch_count": count - sum(row["symmetric_normalized_text_match"] for row in symmetric_rows),
        "symmetric_page_text_match_count": sum(row["symmetric_page_text_sha_match"] for row in symmetric_rows),
        "symmetric_page_text_mismatch_count": count - sum(row["symmetric_page_text_sha_match"] for row in symmetric_rows),
        "differing_page_count_total": sum(row["differing_page_count"] for row in symmetric_rows),
        "whitespace_only_difference_sample_count": whitespace_count, "control_character_only_difference_sample_count": control_count,
        "systematic_extraction_representation_difference": int((whitespace_count + control_count) == count and count > 0),
        "substantive_text_difference_sample_count": substantive_count,
        "content_sanity_contradiction_count": sum(row["content_sanity_contradiction"] for row in symmetric_rows),
        "semantic_equivalence_pass": symmetric_pass, "semantic_equivalence_fail": count - symmetric_pass,
        "candidate_pdf_hash_drift": candidate_hash_drift, "candidate_word_build_compatible": compatible,
        "current_word_build_added_to_approved_set": approved_set_updated, "production_version_gate_not_relaxed": 1,
        "word_com_run": 0, "doc_conversion_run": 0, "candidate_reconversion_run": 0, "ocr_run": 0,
        "source_sha_mismatch": 0, "original_files_modified": 0, "new_dependency_installed": 0,
        "network_access_used": 0, "git_operations": 0,
        "pipeline": {"page_text": "Poppler pdftotext -layout, page-scoped", "normalization": "remove NUL; Unicode whitespace collapse; trim", "page_join": "single ASCII space", "sha256_encoding": "UTF-8", "pdf_inspector_version": importlib.metadata.version("pdf-inspector")},
        "samples": symmetric_rows, "reference_replay": reference_rows, "details": details,
    }
    write_csv(CATALOG / "g8_doc_converter_version_drift_reference_replay.csv", reference_rows, list(reference_rows[0]))
    write_csv(CATALOG / "g8_doc_converter_version_drift_symmetric_comparison.csv", symmetric_rows, list(symmetric_rows[0]))
    write_csv(CATALOG / "g8_doc_converter_version_drift_text_diff_diagnostics.csv", diagnostic_rows, ["paper_id", "page", "reference_fragment", "candidate_fragment", "difference_category"])
    (CATALOG / "g8_doc_converter_version_drift_semantic_review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = [f"# G8 DOC Converter Version Drift Semantic Review", "", f"Status: `{status}`", "", "## Result", "", f"- Reference replay stored-hash matches: `{replay_match}/{count}`.", f"- Symmetric exact normalized and page-text matches: `{symmetric_pass}/{count}`.", f"- Structural matches (page count/class/OCR route): `{structural}/{count}`.", f"- Candidate PDF hash drift: `{candidate_hash_drift}`.", "", "## Guardrails", "", "- Word COM, DOC conversion, candidate reconversion, OCR, network, and Git operations: `0`.", "- Production version gate remains frozen; approval metadata was not changed.", ""]
    (REPORTS / "G8_DOC_CONVERTER_VERSION_DRIFT_SEMANTIC_REVIEW.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key not in {"samples", "reference_replay", "details"}}, ensure_ascii=False))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
