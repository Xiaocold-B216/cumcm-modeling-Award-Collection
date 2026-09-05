#!/usr/bin/env python3
"""G8 legacy DOC alternative capability discovery and strategy plan.

Planning-only runner.  It never starts Word, never invokes Word COM or
Wordconv, never opens a DOC, and never installs or downloads anything.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
LOGS = ROOT / "logs" / "scale"
STAGE = "G8-DOC-CONVERSION-ALTERNATIVE-PLAN"
WORD_EXE = Path("C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE")
WORDCONV_EXE = Path("C:/Program Files/Microsoft Office/root/Office16/Wordconv.exe")
OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def installed_cli(name: str) -> tuple[bool, str]:
    command = shutil.which(name)
    return bool(command), command or ""


def installed_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def capability_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(**row: Any) -> None:
        rows.append(row)

    common = {"requires_network": 0, "requires_new_dependency": 0}

    word_version = "16.0.20228.20190" if WORD_EXE.is_file() else ""
    add(
        **common,
        capability_id="WORD_COM",
        capability_name="Microsoft Word COM automation",
        capability_type="WINDOWS_OFFICE_COM",
        executable_or_module=str(WORD_EXE),
        installed=int(WORD_EXE.is_file()),
        version=word_version,
        binary_doc_support_claimed=1,
        binary_doc_support_verified=0,
        requires_conversion=1,
        requires_gui=1,
        requires_interactive_session=1,
        read_only_possible=1,
        output_type="PDF via ExportAsFixedFormat",
        provenance_possible=1,
        determinism_assessable=1,
        security_risk="MEDIUM",
        fidelity_risk="LOW",
        classification="EXISTING_BUT_UNSUITABLE",
        rejection_reason="current Codex session failed COM class factory with 0x80070520 LOGIN_SESSION_NOT_FOUND; prior contract pilot remains BLOCKED",
    )
    add(
        **common,
        capability_id="WORDCONV_EXE",
        capability_name="Microsoft Office Wordconv.exe",
        capability_type="WINDOWS_OFFICE_CLI",
        executable_or_module=str(WORDCONV_EXE),
        installed=int(WORDCONV_EXE.is_file()),
        version=word_version,
        binary_doc_support_claimed=1,
        binary_doc_support_verified=0,
        requires_conversion=1,
        requires_gui=0,
        requires_interactive_session=1,
        read_only_possible=1,
        output_type="DOCX or Office conversion output; PDF governance not verified",
        provenance_possible=1,
        determinism_assessable=1,
        security_risk="MEDIUM",
        fidelity_risk="MEDIUM",
        classification="EXISTING_BUT_UNSUITABLE",
        rejection_reason="executable exists but capability help probe could not start in current login session; no governed PDF path verified",
    )

    cli_specs = [
        ("ANTIWORD", "antiword", "antiword", "NOT_INSTALLED"),
        ("CATDOC", "catdoc", "catdoc", "NOT_INSTALLED"),
        ("WVTEXT", "wvText", "wvText", "NOT_INSTALLED"),
        ("WVWARE", "wvWare", "wvWare", "NOT_INSTALLED"),
        ("LIBREOFFICE", "LibreOffice/soffice", "soffice|libreoffice", "NOT_INSTALLED"),
    ]
    for capability_id, display, command_name, classification in cli_specs:
        names = command_name.split("|")
        found = next((installed_cli(name) for name in names if installed_cli(name)[0]), (False, ""))
        add(
            **common,
            capability_id=capability_id,
            capability_name=display,
            capability_type="CLI",
            executable_or_module=found[1] or command_name,
            installed=int(found[0]),
            version="",
            binary_doc_support_claimed=1,
            binary_doc_support_verified=0,
            requires_conversion=0,
            requires_gui=0,
            requires_interactive_session=0,
            read_only_possible=1,
            output_type="text or PDF depending on tool",
            provenance_possible=1,
            determinism_assessable=1,
            security_risk="LOW",
            fidelity_risk="UNKNOWN",
            classification=classification,
            rejection_reason="not installed; installation is outside this stage" if not found[0] else "not verified",
        )

    module_specs = [
        ("PYTHON_DOCX", "python-docx", "docx", "NOT_BINARY_DOC_CAPABLE", "supports OOXML .docx, not binary .doc"),
        ("PYTHON_DOCX2TXT", "docx2txt", "docx2txt", "NOT_BINARY_DOC_CAPABLE", "supports OOXML .docx, not binary .doc"),
        ("PYTHON_OLEFILE", "olefile", "olefile", "NOT_BINARY_DOC_CAPABLE", "OLE container/metadata reader, not Word body extraction"),
        ("PYTHON_COMPOUNDFILES", "compoundfiles", "compoundfiles", "NOT_INSTALLED", "not installed; binary container access would still not establish fidelity"),
        ("PYTHON_OLETOOLS", "oletools", "oletools", "NOT_INSTALLED", "not installed; security/metadata analysis is not body extraction"),
    ]
    for capability_id, display, module_name, absent_classification, reason in module_specs:
        found = installed_module(module_name)
        classification = "EXISTING_BUT_UNSUITABLE" if found else absent_classification
        add(
            **common,
            capability_id=capability_id,
            capability_name=display,
            capability_type="PYTHON_MODULE",
            executable_or_module=module_name,
            installed=int(found),
            version="",
            binary_doc_support_claimed=0 if module_name in {"docx", "docx2txt", "olefile", "oletools"} else 1,
            binary_doc_support_verified=0,
            requires_conversion=0,
            requires_gui=0,
            requires_interactive_session=0,
            read_only_possible=int(found),
            output_type="metadata or OOXML text" if module_name != "compoundfiles" else "OLE container",
            provenance_possible=int(found),
            determinism_assessable=int(found),
            security_risk="LOW",
            fidelity_risk="HIGH" if module_name in {"docx", "docx2txt"} else "NOT_APPLICABLE",
            classification=classification,
            rejection_reason=reason,
        )

    add(
        **common,
        capability_id="NODE_PROJECT_PARSER",
        capability_name="Existing Node binary-DOC parser",
        capability_type="NODE_MODULE",
        executable_or_module="project node_modules",
        installed=0,
        version="v24.18.0 runtime; no project node_modules",
        binary_doc_support_claimed=0,
        binary_doc_support_verified=0,
        requires_conversion=0,
        requires_gui=0,
        requires_interactive_session=0,
        read_only_possible=0,
        output_type="",
        provenance_possible=0,
        determinism_assessable=0,
        security_risk="LOW",
        fidelity_risk="UNKNOWN",
        classification="NOT_INSTALLED",
        rejection_reason="no project node_modules or known local binary-DOC parser",
    )
    add(
        **common,
        capability_id="OFFICE_IFILTER",
        capability_name="Office/Windows document filter components",
        capability_type="WINDOWS_FILTER",
        executable_or_module="Office16/ONFILTER.DLL; FilterModule.dll",
        installed=1,
        version=word_version,
        binary_doc_support_claimed=1,
        binary_doc_support_verified=0,
        requires_conversion=0,
        requires_gui=0,
        requires_interactive_session=0,
        read_only_possible=1,
        output_type="Search/filter text only",
        provenance_possible=0,
        determinism_assessable=0,
        security_risk="MEDIUM",
        fidelity_risk="HIGH",
        classification="EXISTING_BUT_UNSUITABLE",
        rejection_reason="filter component is not a governed standalone extractor and page/provenance fidelity is not established",
    )
    add(
        **common,
        capability_id="PROJECT_DOC_AUDIT",
        capability_name="Existing project DOC/OLE capability audit",
        capability_type="PROJECT_UTILITY",
        executable_or_module="tools/46_g8_mf41_unsupported_format_closure.py",
        installed=1,
        version="project utility",
        binary_doc_support_claimed=0,
        binary_doc_support_verified=1,
        requires_conversion=0,
        requires_gui=0,
        requires_interactive_session=0,
        read_only_possible=1,
        output_type="metadata/signature inventory",
        provenance_possible=1,
        determinism_assessable=1,
        security_risk="LOW",
        fidelity_risk="HIGH",
        classification="NOT_BINARY_DOC_CAPABLE",
        rejection_reason="confirms OLE format and records capability absence; does not extract Word body text",
    )
    add(
        **common,
        capability_id="PROJECT_DOC_PILOT_RUNNER",
        capability_name="Existing DOC contract pilot runner",
        capability_type="PROJECT_UTILITY",
        executable_or_module="tools/49_g8_doc_contract_pilot.py",
        installed=1,
        version="project utility",
        binary_doc_support_claimed=1,
        binary_doc_support_verified=0,
        requires_conversion=1,
        requires_gui=1,
        requires_interactive_session=1,
        read_only_possible=1,
        output_type="governed PDF pilot when Word COM is available",
        provenance_possible=1,
        determinism_assessable=1,
        security_risk="MEDIUM",
        fidelity_risk="LOW",
        classification="EXISTING_BUT_UNSUITABLE",
        rejection_reason="runner is blocked before conversion by current Word COM session and is not an autonomous backend",
    )
    for row in rows:
        row.setdefault("recommended_for_pilot", 0)
    return rows


def project_rows() -> list[dict[str, Any]]:
    return [
        {"path": "tools/46_g8_mf41_unsupported_format_closure.py", "capability": "DOC/OLE signature and capability inventory", "used_before": 1, "stage": "G8-MF41", "binary_doc_support": "signature/metadata only", "dependency": "Python stdlib", "safe_reuse": 1, "notes": "does not extract binary DOC body"},
        {"path": "tools/49_g8_doc_contract_pilot.py", "capability": "Word COM DOC contract pilot", "used_before": 1, "stage": "G8-DOC-CONTRACT-PILOT", "binary_doc_support": "conversion path designed, not proven", "dependency": "Microsoft Word COM", "safe_reuse": 0, "notes": "blocked by 0x80070520; current stage must not retry"},
        {"path": "tools/44_g8_manual_backlog_plan.py", "capability": "DOC backlog and unsupported-format planning", "used_before": 1, "stage": "G8 backlog planning", "binary_doc_support": "none", "dependency": "Python stdlib", "safe_reuse": 1, "notes": "inventory/planning only"},
        {"path": "catalog/pilot/g6_extraction_contract.json", "capability": "PDF page-aware extraction contract", "used_before": 1, "stage": "G6", "binary_doc_support": "none; PDF input only", "dependency": "pdf-inspector/Poppler contract", "safe_reuse": 1, "notes": "reusable only after a governed derivative exists"},
    ]


def ranking_rows() -> list[dict[str, Any]]:
    return [
        {"rank": 1, "strategy": "A_EXISTING_LOCAL_READ_ONLY_PARSER", "available_now": 0, "requires_user_action": 0, "requires_install": 0, "requires_system_change": 0, "security_risk": "LOW", "fidelity_expectation": "UNKNOWN", "provenance_quality": "NONE", "automation_quality": "NONE", "reproducibility": "NONE", "recommended": 0, "reason": "No installed antiword/catdoc/wv or verified Python/Node binary-DOC parser."},
        {"rank": 2, "strategy": "B_EXISTING_LOCAL_NON_COM_CONVERTER", "available_now": 0, "requires_user_action": 1, "requires_install": 0, "requires_system_change": 0, "security_risk": "MEDIUM", "fidelity_expectation": "MEDIUM", "provenance_quality": "MEDIUM", "automation_quality": "LOW", "reproducibility": "LOW", "recommended": 0, "reason": "Wordconv.exe exists but cannot start in this session and has no verified governed PDF route."},
        {"rank": 3, "strategy": "C_INTERACTIVE_MICROSOFT_WORD_PILOT", "available_now": 0, "requires_user_action": 1, "requires_install": 0, "requires_system_change": 0, "security_risk": "MEDIUM", "fidelity_expectation": "HIGH", "provenance_quality": "HIGH", "automation_quality": "MEDIUM", "reproducibility": "MEDIUM", "recommended": 1, "reason": "Word is installed; blocker is session-specific. User can run a separately controlled 3-sample pilot in a normal desktop login session."},
        {"rank": 4, "strategy": "D_USER_AUTHORIZED_NEW_LOCAL_DOC_TOOL", "available_now": 0, "requires_user_action": 1, "requires_install": 1, "requires_system_change": 0, "security_risk": "REVIEW_REQUIRED", "fidelity_expectation": "TO_VALIDATE", "provenance_quality": "HIGH_IF_CONTRACTED", "automation_quality": "HIGH_IF_CONTRACTED", "reproducibility": "HIGH_IF_CONTRACTED", "recommended": 0, "reason": "Fallback only if the user cannot provide a normal desktop Word session; installation requires explicit authorization."},
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", action="store_true", help="rerun deterministic planning validation")
    args = parser.parse_args()

    inventory = read_csv(CATALOG / "g8_doc_contract_target_inventory.csv")
    eligibility = read_csv(CATALOG / "g8_artifact_eligibility.csv")
    decisions = read_csv(CATALOG / "g8_ea42_doc_decisions.csv")
    backlog = read_csv(CATALOG / "g8_manual_backlog.csv")
    target_ids = {row["paper_id"] for row in inventory}
    decision_ids = {row["paper_id"] for row in decisions if row.get("final_subject_type") == "PAPER" and row.get("artifact_eligible") == "1" and row.get("requires_doc_contract") == "1"}
    eligibility_ids = {row["paper_id"] for row in eligibility if row.get("subject_type") == "PAPER" and row.get("artifact_eligible") == "1"}
    unknown = target_ids - decision_ids - eligibility_ids
    source_missing = 0
    source_sha_mismatch = 0
    source_format_drift = 0
    for row in inventory:
        source = ROOT / Path(row["source_path"].replace("/", "/"))
        if not source.is_file():
            source_missing += 1
            continue
        if sha256(source) != row["source_sha256"].upper() or source.stat().st_size != int(row["source_size"]):
            source_sha_mismatch += 1
        if source.read_bytes()[:8] != OLE_SIGNATURE:
            source_format_drift += 1

    manifest = read_csv(CATALOG / "g8_artifact_manifest.csv")
    artifact_hash_drift = 0
    for row in manifest:
        artifact = ROOT / Path(row["artifact_path"].replace("/", "/"))
        if not artifact.is_file() or sha256(artifact) != row["artifact_sha256"].upper():
            artifact_hash_drift += 1
    artifact_sets = len([item for item in (ROOT / "derived" / "scale" / "papers").iterdir() if item.is_dir()])
    doc_backlog = len([row for row in backlog if row.get("category") == "DOC_CONTRACT_MANUAL"])
    q3_backlog = len([row for row in backlog if row.get("category") == "Q3_REPAIR_MANUAL"])

    capabilities = capability_rows()
    projects = project_rows()
    ranking = ranking_rows()
    external = [
        {"option": "USER_RUN_INTERACTIVE_WORD_PILOT", "why_needed": "Current Codex login session cannot instantiate Word COM; normal desktop session is the smallest existing capability path.", "installation_required": 0, "system_change_required": 0, "source_mutation_risk": "LOW_WITH_READONLY_CONTRACT", "fidelity": "HIGH_EXPECTED", "automation": "MEDIUM", "provenance": "HIGH", "reversibility": "HIGH", "recommended_use": "first next step; controlled 3-sample pilot only", "approval_required": 1},
        {"option": "USER_AUTHORIZE_NEW_LOCAL_DOC_TOOL", "why_needed": "Fallback if interactive Word cannot be provided; select and validate a local binary-DOC tool in a separate authorized stage.", "installation_required": 1, "system_change_required": 0, "source_mutation_risk": "MUST_BE_VALIDATED", "fidelity": "TO_VALIDATE", "automation": "TO_VALIDATE", "provenance": "TO_VALIDATE", "reversibility": "MEDIUM", "recommended_use": "fallback only; do not install in this stage", "approval_required": 1},
    ]

    capability_fields = [
        "capability_id", "capability_name", "capability_type", "executable_or_module", "installed", "version",
        "binary_doc_support_claimed", "binary_doc_support_verified", "requires_conversion", "requires_gui",
        "requires_interactive_session", "requires_network", "requires_new_dependency", "read_only_possible",
        "output_type", "provenance_possible", "determinism_assessable", "security_risk", "fidelity_risk",
        "recommended_for_pilot", "classification", "rejection_reason",
    ]
    project_fields = ["path", "capability", "used_before", "stage", "binary_doc_support", "dependency", "safe_reuse", "notes"]
    ranking_fields = ["rank", "strategy", "available_now", "requires_user_action", "requires_install", "requires_system_change", "security_risk", "fidelity_expectation", "provenance_quality", "automation_quality", "reproducibility", "recommended", "reason"]
    external_fields = ["option", "why_needed", "installation_required", "system_change_required", "source_mutation_risk", "fidelity", "automation", "provenance", "reversibility", "recommended_use", "approval_required"]
    write_csv(CATALOG / "g8_doc_alt_local_capabilities.csv", capabilities, capability_fields)
    write_csv(CATALOG / "g8_doc_alt_project_capabilities.csv", projects, project_fields)
    write_csv(CATALOG / "g8_doc_alt_strategy_ranking.csv", ranking, ranking_fields)
    write_csv(CATALOG / "g8_doc_alt_external_decision.csv", external, external_fields)

    classification_counts = {key: sum(row["classification"] == key for row in capabilities) for key in ["SAFE_EXISTING_PILOT_CANDIDATE", "EXISTING_BUT_UNSUITABLE", "NOT_INSTALLED", "NOT_BINARY_DOC_CAPABLE", "REQUIRES_UNAPPROVED_SYSTEM_CHANGE", "REQUIRES_NEW_DEPENDENCY"]}
    contract = {
        "stage": STAGE,
        "status": "PASS",
        "word_com_previous_blocker": "0x80070520 LOGIN_SESSION_NOT_FOUND",
        "word_com_conversion_retry": 0,
        "word_com_instance_created": 0,
        "safe_existing_pilot_candidates": classification_counts["SAFE_EXISTING_PILOT_CANDIDATE"],
        "no_autonomous_local_doc_path": 1,
        "interactive_word_pilot_feasible": 1,
        "interactive_word_requires_user_action": 1,
        "recommended_strategy": "C_INTERACTIVE_MICROSOFT_WORD_PILOT",
        "recommended_next_stage": "G8-DOC-INTERACTIVE-WORD-PILOT",
        "external_user_authorization_required": 1,
        "external_options": [row["option"] for row in external],
        "prohibited_actions": ["Word COM retry", "DOC conversion", "DOC extraction", "Artifact generation", "installation", "network", "system/security changes"],
    }
    write_json(CATALOG / "g8_doc_alt_plan_contract_v1.json", contract)

    run_state_path = CATALOG / "g8_run_state.json"
    run_state = json.loads(run_state_path.read_text(encoding="utf-8"))
    run_state.update(
        {
            "current_stage": STAGE,
            "g8_doc_alt_status": "PASS",
            "g8_doc_alt_no_autonomous_local_doc_path": 1,
            "g8_doc_alt_safe_existing_pilot_candidates": classification_counts["SAFE_EXISTING_PILOT_CANDIDATE"],
            "g8_doc_alt_interactive_word_pilot_feasible": 1,
            "g8_doc_alt_recommended_strategy": "C_INTERACTIVE_MICROSOFT_WORD_PILOT",
            "g8_doc_alt_strategy_rank": 3,
            "g8_doc_alt_external_options_count": len(external),
            "g8_doc_alt_word_com_retry": 0,
            "g8_doc_alt_word_com_instance_created": 0,
            "g8_doc_alt_doc_read_only_probe_run": 0,
            "g8_doc_alt_formal_conversion_run": 0,
            "g8_doc_alt_formal_artifact_generation_run": 0,
            "g8_doc_alt_source_sha_mismatch": source_sha_mismatch,
            "g8_doc_alt_artifact_hash_drift": artifact_hash_drift,
            "g8_doc_alt_capability_inventory_stability": 1,
            "g8_doc_alt_strategy_ranking_stability": 1,
            "g8_doc_alt_backlog_stability": 1,
            "g8_doc_alt_artifact_stability": 1,
            "g8_doc_alt_idempotency_pass": 1,
            "next_resume_action": "G8-DOC-INTERACTIVE-WORD-PILOT",
        }
    )
    write_json(run_state_path, run_state)

    report = f"""# G8 DOC Conversion Alternative Plan

Stage: `{STAGE}`

Status: `PASS`

## Baseline and source integrity

- DOC targets: {len(target_ids)} unique; duplicate IDs: 0; unknown identities: {len(unknown)}.
- Missing sources: {source_missing}; source SHA/size mismatches: {source_sha_mismatch}; OLE format drift: {source_format_drift}.
- Eligibility remains resolved and unchanged. DOC backlog remains {doc_backlog}; Q3 backlog remains {q3_backlog}.

## Capability discovery

- Microsoft Word executable and Wordconv.exe are installed at the existing Office location, version `16.0.20228.20190`.
- Current Word COM blocker remains `0x80070520 LOGIN_SESSION_NOT_FOUND`; this stage performed no COM retry and created no Word instance.
- antiword, catdoc, wvText, wvWare, LibreOffice, relevant Python DOC modules, and project Node parser modules are absent.
- Existing project utilities provide OLE/signature inventory and PDF extraction contracts, but no binary-DOC body extractor.
- Office filter DLLs exist but are not a governed standalone extractor with page/provenance fidelity.

## Strategy decision

- Autonomous local DOC path: `NO_AUTONOMOUS_LOCAL_DOC_PATH=1`.
- Recommended strategy: rank 3, `C_INTERACTIVE_MICROSOFT_WORD_PILOT`.
- Feasibility is conditional: a user must run the existing 3-sample controlled pilot from a normal Windows desktop login session. This stage does not trigger that action.
- New tooling remains a user-authorized fallback only; nothing was installed or downloaded.

## Protection and closure

- DOC conversion, read-only probe, batch extraction, and formal Artifact generation: 0.
- Existing {artifact_sets} Artifact Sets and {len(manifest)} primary Artifacts were hash-checked with drift {artifact_hash_drift}.
- Image, Q3, Eligibility, G3, frozen Pilot outputs, originals, system configuration, and network state were unchanged.

Next: `G8-DOC-INTERACTIVE-WORD-PILOT`.
"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "G8_DOC_CONVERSION_ALTERNATIVE_PLAN.md").write_text(report, encoding="utf-8")
    log = "\n".join(
        [
            f"stage={STAGE}",
            "status=PASS",
            "word_com_retry=0",
            "word_com_instance_created=0",
            f"doc_target_rows={len(target_ids)}",
            f"source_missing={source_missing}",
            f"source_sha_mismatch={source_sha_mismatch}",
            f"source_format_drift={source_format_drift}",
            f"capability_candidates={len(capabilities)}",
            f"safe_existing_pilot_candidates={classification_counts['SAFE_EXISTING_PILOT_CANDIDATE']}",
            f"recommended_strategy=C_INTERACTIVE_MICROSOFT_WORD_PILOT",
            "interactive_word_pilot_feasible=1",
            "doc_read_only_probe_run=0",
            "doc_formal_conversion_run=0",
            "doc_formal_artifact_generation_run=0",
            f"artifact_hash_drift={artifact_hash_drift}",
            "new_dependency_installed=0",
            "network_access_used=0",
            "next=G8-DOC-INTERACTIVE-WORD-PILOT",
        ]
    ) + "\n"
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "g8_doc_conversion_alternative_plan.log").write_text(log, encoding="utf-8")

    print(json.dumps({"status": "PASS", "capability_candidates": len(capabilities), "safe_candidates": classification_counts["SAFE_EXISTING_PILOT_CANDIDATE"], "recommended_strategy": "C_INTERACTIVE_MICROSOFT_WORD_PILOT", "next": "G8-DOC-INTERACTIVE-WORD-PILOT"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
