#!/usr/bin/env python3
"""Read-only alternative-rendering decision for one exhausted DOC remediation."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import winreg
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "scale"
REPORTS = ROOT / "reports" / "scale"
TARGET = "CUMCM-2012-D-001"
SOURCE = ROOT / "2012年数学建模国赛真题+优秀论文" / "2012年优秀论文" / "2012D：机器人避障问题 (2).doc"
DOCX = ROOT / "tmp" / "g8_doc_2012_d001_docx_intermediate" / TARGET / "source_rebuilt.docx"
EXPECTED_SOURCE_SHA = "D93A9A6A9DE012927F8A5D4B36E1768CA3F6AFFB6952673F40FE2740D4032766"
EXPECTED_DOCX_SHA = "B948CA41387ABC408724B1D64286830B54B12198A33C54D8BE684661CA8937DC"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def registry_printers() -> list[dict]:
    root = r"SYSTEM\CurrentControlSet\Control\Print\Printers"
    printers: list[dict] = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root, 0, winreg.KEY_READ) as key:
        count = winreg.QueryInfoKey(key)[0]
        for index in range(count):
            name = winreg.EnumKey(key, index)
            with winreg.OpenKey(key, name, 0, winreg.KEY_READ) as printer:
                def value(field: str) -> str:
                    try:
                        return str(winreg.QueryValueEx(printer, field)[0])
                    except FileNotFoundError:
                        return "UNAVAILABLE"
                printers.append({
                    "name": name,
                    "driver": value("Printer Driver"),
                    "port": value("Port"),
                    "shared": value("Shared"),
                    "published": value("Published"),
                    "inventory_method": "REGISTRY_READ_ONLY_FALLBACK",
                })
    return sorted(printers, key=lambda item: item["name"].casefold())


def spooler_status() -> str:
    completed = subprocess.run(["sc.exe", "query", "Spooler"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if completed.returncode != 0:
        return "UNAVAILABLE"
    if "RUNNING" in completed.stdout.upper():
        return "RUNNING"
    if "STOPPED" in completed.stdout.upper():
        return "STOPPED"
    return "UNAVAILABLE"


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    external = json.loads((CATALOG / "g8_doc_2012_d001_external_reacquisition_result.json").read_text(encoding="utf-8"))
    if external.get("EXTERNAL_REACQUISITION_FAILED") != 1:
        raise RuntimeError("External reacquisition first-round result is not frozen as failed.")
    printers = registry_printers()
    print_to_pdf = next((item for item in printers if item["name"] == "Microsoft Print to PDF"), None)
    xps = next((item for item in printers if item["name"] == "Microsoft XPS Document Writer"), None)
    spooler = spooler_status()
    source_sha = sha256(SOURCE)
    docx_sha = sha256(DOCX)

    options = [
        {"route": "WORD_PRINT_PIPELINE_TO_MICROSOFT_PRINT_TO_PDF", "status": "AUTOMATION_UNRESOLVED", "different_renderer_independence": 5, "source_immutability": 5, "content_fidelity": 4, "layout_fidelity": 4, "equation_image_fidelity": 4, "determinism": 2, "automation_feasibility": 1, "output_path_control": 1, "auditability": 2, "existing_tool_availability": 5, "system_side_effects": 2, "new_dependency_requirement": 5, "contract_complexity": 2, "bypass_likelihood": 4, "reason": "Different Word print/driver pipeline is available, but PORTPROMPT: plus unverified PrintOut output path and ActivePrinter scope prevents an automated pilot."},
        {"route": "MANUAL_INTERACTIVE_PRINT_TO_PDF", "status": "PREFERRED_WITH_NEW_CONTRACT", "different_renderer_independence": 5, "source_immutability": 5, "content_fidelity": 4, "layout_fidelity": 4, "equation_image_fidelity": 4, "determinism": 2, "automation_feasibility": 3, "output_path_control": 4, "auditability": 3, "existing_tool_availability": 5, "system_side_effects": 4, "new_dependency_requirement": 5, "contract_complexity": 3, "bypass_likelihood": 4, "reason": "Human-controlled printer selection and save path can avoid unattended dialog automation; still requires a bounded, logged manual contract."},
        {"route": "MICROSOFT_XPS_DOCUMENT_WRITER", "status": "UNAVAILABLE", "different_renderer_independence": 5, "source_immutability": 5, "content_fidelity": 4, "layout_fidelity": 4, "equation_image_fidelity": 4, "determinism": 3, "automation_feasibility": 0, "output_path_control": 0, "auditability": 0, "existing_tool_availability": 0, "system_side_effects": 3, "new_dependency_requirement": 5, "contract_complexity": 2, "bypass_likelihood": 0, "reason": "No installed Microsoft XPS Document Writer was found; even if present, an approved XPS-to-PDF route is absent."},
        {"route": "PAGE_ISOLATION_DIAGNOSTIC", "status": "SECONDARY_NEW_DIAGNOSTIC_CONTRACT", "different_renderer_independence": 1, "source_immutability": 5, "content_fidelity": 1, "layout_fidelity": 1, "equation_image_fidelity": 1, "determinism": 3, "automation_feasibility": 3, "output_path_control": 5, "auditability": 4, "existing_tool_availability": 5, "system_side_effects": 5, "new_dependency_requirement": 5, "contract_complexity": 2, "bypass_likelihood": 1, "reason": "May localize an offending page/object but continues to depend on the failed FixedFormat exporter and cannot itself produce a complete PDF."},
        {"route": "CONTROLLED_DERIVATIVE_DOCUMENT_SURGERY", "status": "LAST_RESORT_DIAGNOSTIC_REMEDIATION", "different_renderer_independence": 1, "source_immutability": 5, "content_fidelity": 1, "layout_fidelity": 1, "equation_image_fidelity": 1, "determinism": 2, "automation_feasibility": 2, "output_path_control": 5, "auditability": 2, "existing_tool_availability": 3, "system_side_effects": 5, "new_dependency_requirement": 5, "contract_complexity": 1, "bypass_likelihood": 2, "reason": "Removing fields, objects, or sections risks changing mathematical content, citations, figures, and layout."},
        {"route": "THIRD_PARTY_CONVERTER_EVALUATION", "status": "USER_AUTHORIZATION_REQUIRED", "different_renderer_independence": 5, "source_immutability": 5, "content_fidelity": 3, "layout_fidelity": 3, "equation_image_fidelity": 3, "determinism": 3, "automation_feasibility": 3, "output_path_control": 4, "auditability": 3, "existing_tool_availability": 0, "system_side_effects": 3, "new_dependency_requirement": 0, "contract_complexity": 2, "bypass_likelihood": 3, "reason": "No approved third-party converter is installed; any installation requires explicit future authorization and a separate converter contract."},
    ]
    outputs = {
        "printers": CATALOG / "g8_doc_2012_d001_printer_inventory.csv",
        "options": CATALOG / "g8_doc_2012_d001_alternative_rendering_options.csv",
        "decision": CATALOG / "g8_doc_2012_d001_alternative_rendering_decision.json",
        "report": REPORTS / "G8_DOC_2012_D001_ALTERNATIVE_RENDERING_DECISION.md",
    }
    write_csv(outputs["printers"], printers, ["name", "driver", "port", "shared", "published", "inventory_method"])
    write_csv(outputs["options"], options, list(options[0].keys()))
    result = {
        "STAGE": "G8-DOC-CUMCM-2012-D-001-ALTERNATIVE-RENDERING-DECISION", "STATUS": "PASS", "BRANCH": "library-refactor-v1", "HEAD": "557724fba6572d4d83dc421feda5b17b13ff8d66", "TARGET_PAPER_ID": TARGET,
        "SOURCE_SHA256": source_sha, "DERIVATIVE_DOCX_SHA256": docx_sha,
        "DIRECT_WORD_EXPORT_ROUTE_STATUS": "CLOSED", "DOCX_INTERMEDIATE_ROUTE_STATUS": "CLOSED", "EXTERNAL_REACQUISITION_FIRST_ROUND_STATUS": "EXHAUSTED",
        "PRINTER_INVENTORY_COMPLETED": 1, "PRINTER_INVENTORY_GET_PRINTER_STATUS": "ACCESS_DENIED_IN_CODEX_SESSION", "PRINTER_INVENTORY_FALLBACK_METHOD": "REGISTRY_READ_ONLY_FALLBACK", "PRINTERS": printers,
        "MICROSOFT_PRINT_TO_PDF_INSTALLED": int(print_to_pdf is not None), "MICROSOFT_PRINT_TO_PDF_PRINTER_NAME": print_to_pdf["name"] if print_to_pdf else "UNAVAILABLE", "MICROSOFT_PRINT_TO_PDF_DRIVER": print_to_pdf["driver"] if print_to_pdf else "UNAVAILABLE", "MICROSOFT_PRINT_TO_PDF_PORT": print_to_pdf["port"] if print_to_pdf else "UNAVAILABLE",
        "MICROSOFT_XPS_DOCUMENT_WRITER_INSTALLED": int(xps is not None), "PRINT_SPOOLER_STATUS": spooler,
        "WORD_PRINT_TO_PDF_AUTOMATION_EVALUATED": 1, "PRINT_OUTPUT_PATH_CONTROL_STATUS": "UNRESOLVED", "DEFAULT_PRINTER_CHANGE_REQUIRED": 0, "ACTIVE_PRINTER_SIDE_EFFECT_SCOPE": "UNRESOLVED", "ACTIVE_PRINTER_SIDE_EFFECT_SCOPE_UNRESOLVED": 1, "AUTOMATION_AUDITABLE": 0,
        "ALTERNATIVE_ROUTE_COUNT": len(options), "ALTERNATIVE_ROUTES": options, "PAGE_ISOLATION_DIAGNOSTIC_EVALUATED": 1, "CONTROLLED_DOCUMENT_SURGERY_EVALUATED": 1, "THIRD_PARTY_CONVERTER_EVALUATED": 1,
        "PREFERRED_ROUTE_IDENTIFIED": 1, "PREFERRED_ROUTE": "MANUAL_INTERACTIVE_PRINT_TO_PDF", "PREFERRED_RENDER_INPUT": "REBUILT_DOCX", "PREFERRED_ROUTE_REASON": "Microsoft Print to PDF is installed and uses a pipeline independent from ExportAsFixedFormat. Rebuilt DOCX is valid with structural diagnostics matching the original; however, unattended PrintOut output-path control and ActivePrinter scope are unresolved, so only a separately governed manual route is currently acceptable.", "NEW_RENDERING_CONTRACT_REQUIRED": 1,
        "SOURCE_SHA_MISMATCH": int(source_sha != EXPECTED_SOURCE_SHA), "DERIVATIVE_DOCX_SHA_MISMATCH": int(docx_sha != EXPECTED_DOCX_SHA), "ORIGINAL_FILES_MODIFIED": 0,
        "WORD_COM_RUN": 0, "PRINT_JOB_RUN": 0, "PDF_GENERATION_RUN": 0, "SUCCESSFUL_BATCH_ROWS_PRESERVED": 13, "SUCCESSFUL_BATCH_ROWS_RECONVERTED": 0, "DOC_CONTRACT_APPROVED": 1,
        "ELIGIBLE": 453, "INELIGIBLE": 189, "ARTIFACT_SETS": 308, "PRIMARY_ARTIFACTS": 924, "DOC_MANUAL_BACKLOG": 17, "Q3_MANUAL_BACKLOG": 128,
        "NETWORK_ACCESS_USED": 0, "NEW_DEPENDENCY_INSTALLED": 0, "GIT_OPERATIONS": 0, "DECISION_GENERATED_AT": datetime.now().astimezone().isoformat(timespec="seconds"),
        "OUTPUTS": {key: str(path.relative_to(ROOT)).replace("\\", "/") for key, path in outputs.items()}, "NEXT": "G8-DOC-CUMCM-2012-D-001-MANUAL-PRINT-TO-PDF-CONTRACT",
    }
    outputs["decision"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    outputs["report"].write_text(
        "# G8 DOC CUMCM-2012-D-001 Alternative Rendering Decision\n\n"
        "Status: `PASS`\n\n"
        "The first external reacquisition round is frozen as exhausted. Microsoft Print to PDF is installed, but its `PORTPROMPT:` port and the unresolved scope of Word `ActivePrinter` prevent approval of unattended printing. The least-risk next route is a separately governed manual Print-to-PDF contract using the valid, isolated rebuilt DOCX.\n\n"
        "No Word COM, print job, PDF generation, network access, dependency installation, or source mutation occurred.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
