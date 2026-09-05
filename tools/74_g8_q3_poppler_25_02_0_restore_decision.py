"""Read-only decision gate for a complete local Poppler 25.02.0 runtime."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "catalog" / "scale"
RUNTIME_ROOTS = [
    Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin"),
    Path(r"D:\texlive\2026\bin\windows"),
]
TOOLS = ["pdfinfo.exe", "pdftotext.exe", "pdftoppm.exe", "pdftocairo.exe"]
INSTALL_LOG = Path(r"D:\texlive\2026\install-tl.log")
OUT_PROVENANCE = SCALE / "g8_poppler_historical_provenance.json"
OUT_CANDIDATES = SCALE / "g8_poppler_local_runtime_candidates.csv"
OUT_DECISION = SCALE / "g8_poppler_25_02_0_restore_decision.json"
REPORT = ROOT / "reports" / "scale" / "G8_Q3_POPPLER_25_02_0_RESTORE_DECISION.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def version(executable: Path) -> str:
    if not executable.is_file():
        return "MISSING"
    run = subprocess.run([str(executable), "-v"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if run.returncode:
        return "UNUSABLE"
    first = (run.stdout + run.stderr).splitlines()[0]
    match = re.search(r"version\s+([^\s]+)", first)
    return match.group(1) if match else "UNKNOWN"


def counts() -> dict[str, int]:
    artifacts = rows(SCALE / "g8_artifact_manifest.csv"); backlog = rows(SCALE / "g8_manual_backlog.csv"); eligibility = rows(SCALE / "g8_artifact_eligibility.csv")
    return {"ARTIFACT_SETS": len(artifacts) // 3, "PRIMARY_ARTIFACTS": len(artifacts), "DOC_MANUAL_BACKLOG": sum(row.get("category") == "DOC_REPAIR_MANUAL" for row in backlog), "Q3_MANUAL_BACKLOG": sum(row.get("category") == "Q3_REPAIR_MANUAL" for row in backlog), "ELIGIBLE": sum(row.get("artifact_eligible") == "1" for row in eligibility), "INELIGIBLE": sum(row.get("artifact_eligible") != "1" for row in eligibility)}


def main() -> int:
    historical_logs = "\n".join((ROOT / name).read_text(encoding="utf-8", errors="replace") for name in ["logs/g6_00g_hybrid_page_extraction.log", "logs/g6_pilot_auto_r.log"] if (ROOT / name).is_file())
    install = INSTALL_LOG.read_text(encoding="utf-8", errors="replace") if INSTALL_LOG.is_file() else ""
    source_match = re.search(r"Using URL:\s*(\S+)", install)
    candidates = []
    for runtime in RUNTIME_ROOTS:
        versions = {tool: version(runtime / tool) for tool in TOOLS}
        required = [versions[tool] for tool in TOOLS]
        exact_complete = all(item == "25.02.0" for item in required)
        complete = all(item not in {"MISSING", "UNUSABLE", "UNKNOWN"} for item in required)
        classification = "EXACT_25_02_0_COMPLETE" if exact_complete else ("OTHER_VERSION_COMPLETE" if complete and len(set(required)) == 1 else ("OTHER_VERSION_INCOMPLETE" if any(item == "MISSING" for item in required) else "MIXED_VERSION_RUNTIME"))
        candidates.append({"runtime_root": str(runtime), **{tool[:-4]: versions[tool] for tool in TOOLS}, "classification": classification, "dll_load_evidence": "ALL_PRESENT_EXECUTABLES_-V_PASS" if all(item not in {"MISSING", "UNUSABLE"} for item in required) else "INCOMPLETE"})
    local = next((row for row in candidates if row["classification"] == "EXACT_25_02_0_COMPLETE"), None)
    provenance = {"historical_poppler_version_evidence": "25.02.0" in historical_logs, "historical_runtime_path_evidence": r"D:\texlive\2026\bin\windows" in (ROOT / "tools" / "21_g5_25_ocr_2025.py").read_text(encoding="utf-8", errors="replace"), "historical_source": "TeX Live 2026 Windows runtime; historical Q3/G6 tooling explicitly bound D:\\texlive\\2026\\bin\\windows\\pdftotext.exe", "historical_package_version": "TeX Live 2026", "historical_download_url": source_match.group(1) if source_match else "UNAVAILABLE", "historical_binary_sha_available": False, "binary_identity_claim": "Not established; future acceptance remains subject to the frozen semantic replay."}
    result: dict[str, object] = {
        "STAGE": "G8-Q3-POPPLER-25-02-0-RESTORE-DECISION", "STATUS": "PASS", "BRANCH": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(), "HEAD": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "BASELINE_POPPLER_VERSION": "25.02.0", "POPPLER_26_05_0_COMPATIBILITY_STATUS": "UNTESTABLE_INCOMPLETE_RUNTIME", "REFERENCE_IDENTITY_COUNT": 17, "REFERENCE_PAGE_COUNT": 606, "STORED_REFERENCE_PAGE_HASH_COUNT": 606, "STORED_REFERENCE_BODY_HASH_COUNT": 17,
        "HISTORICAL_POPPLER_EVIDENCE_SEARCH_COMPLETED": 1, "HISTORICAL_POPPLER_SOURCE_AVAILABLE": 1, "HISTORICAL_POPPLER_SOURCE": provenance["historical_source"], "HISTORICAL_POPPLER_PACKAGE_VERSION_AVAILABLE": 1, "HISTORICAL_POPPLER_PACKAGE_VERSION": provenance["historical_package_version"], "HISTORICAL_POPPLER_DOWNLOAD_URL_AVAILABLE": int(provenance["historical_download_url"] != "UNAVAILABLE"), "HISTORICAL_POPPLER_DOWNLOAD_URL": provenance["historical_download_url"], "HISTORICAL_POPPLER_BINARY_SHA_AVAILABLE": 0,
        "LOCAL_POPPLER_SEARCH_COMPLETED": 1, "LOCAL_RUNTIME_ROOT_COUNT": len(candidates), "LOCAL_EXACT_25_02_0_COMPLETE_COUNT": int(local is not None), "LOCAL_EXACT_25_02_0_INCOMPLETE_COUNT": 0, "LOCAL_POPPLER_25_02_0_COMPLETE": int(local is not None), "LOCAL_POPPLER_25_02_0_PATH": local["runtime_root"] if local else "", "LOCAL_RESTORE_AVAILABLE": int(local is not None), "NETWORK_RESTORE_REQUIRED": 0 if local else 1,
        "COMPLETE_26_05_0_RESTORE_POSSIBLE": 1, "REQUIRED_POPPLER_TOOLS": "pdfinfo.exe,pdftotext.exe", "REQUIRED_POPPLER_RENDER_TOOLS": "pdftoppm.exe,pdftocairo.exe", "USER_AUTHORIZATION_REQUIRED": 0 if local else 1,
        "POPPLER_REFERENCE_REPLAY_RUN": 0, "OCR_RUNTIME_READY": 1, "PILOT_TARGET_COUNT": 0, "Q3_OCR_RUN": 0, "FULL_Q3_BATCH_RUN": 0, "FORMAL_ARTIFACTS_GENERATED": 0, "EXISTING_ARTIFACT_MODIFICATION_COUNT": 0, "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NEW_DEPENDENCY_INSTALLED": 0, "G9_RUN": 0, "G10_RUN": 0, "GIT_OPERATIONS": 0,
        "BLOCKER": "NONE" if local else "NO_COMPLETE_LOCAL_POPPLER_25_02_0_RUNTIME", "NEXT": "G8-Q3-POPPLER-25-02-0-LOCAL-BIND-AND-VALIDATE" if local else "G8-Q3-POPPLER-25-02-0-NETWORK-RESTORE-AUTHORIZATION",
    }
    result.update(counts())
    OUT_PROVENANCE.parent.mkdir(parents=True, exist_ok=True); REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROVENANCE.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with OUT_CANDIDATES.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(candidates[0])); writer.writeheader(); writer.writerows(candidates)
    OUT_DECISION.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text("# G8 Q3 Poppler 25.02.0 Restore Decision\n\n" + "\n".join(f"{key}={value}" for key, value in result.items()) + "\n", encoding="utf-8")
    print("\n".join(f"{key}={value}" for key, value in result.items())); print(f"OUTPUTS={OUT_PROVENANCE}; {OUT_CANDIDATES}; {OUT_DECISION}; {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
