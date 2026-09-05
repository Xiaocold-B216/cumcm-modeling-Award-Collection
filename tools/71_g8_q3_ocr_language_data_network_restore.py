"""Restore only the frozen G8 Q3 OCR language-data baseline.

This runner intentionally does not create an OCR worker or process any paper.
It downloads exactly two pre-approved jsDelivr resources to an external,
same-volume staging directory, verifies their historical SHA256 values, then
atomically promotes the complete language-data root.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_ROOT = Path(r"D:\cumcm-modeling-Award-Collection.bootstrap")
OCR_ROOT = BOOTSTRAP_ROOT / "ocr"
LANGUAGE_ROOT = OCR_ROOT / "tesseract-data"
STAGING_ROOT = OCR_ROOT / "staging" / "g8_q3_language_restore"
QUARANTINE_ROOT = OCR_ROOT / "quarantine" / "g8_q3_language_restore"
RESULT_PATH = ROOT / "catalog" / "scale" / "g8_q3_ocr_language_data_restore_result.json"
PROVENANCE_PATH = ROOT / "catalog" / "scale" / "g8_q3_ocr_language_data_provenance.json"
REPORT_PATH = ROOT / "reports" / "scale" / "G8_Q3_OCR_LANGUAGE_DATA_NETWORK_RESTORE.md"
REPAIR_MANIFEST = ROOT / "catalog" / "repair_manifest.jsonl"
HISTORICAL_TOOLS = [ROOT / "tools" / "21_g5_25_ocr_2025.py", ROOT / "tools" / "22_g5_25d_ocr_dependency_smoke.py"]
NODE_MODULES = Path(r"C:\Users\WRZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules")
TESSERACT_PACKAGE = NODE_MODULES / "tesseract.js" / "package.json"
TESSERACT_CORE_PACKAGE = NODE_MODULES / "tesseract.js-core" / "package.json"
EXPECTED = {
    "chi_sim": {"filename": "chi_sim.traineddata.gz", "sha256": "B8A23F10C7DE500891EB458A8ADC9CC58AB7F242F08B7D149F5E9AEA4AD5DB7C"},
    "eng": {"filename": "eng.traineddata.gz", "sha256": "45B4CB346724AC1774F1C36F42F182B887BCDB28EBE63E6FFF90AC41F3FCFF91"},
}
APPROVED_HOSTS = {"cdn.jsdelivr.net", "data.jsdelivr.com"}
FLAVOR = "4.0.0_best_int"
RETRY_LIMIT = 3


class GateError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def read_package_version(path: Path) -> str:
    if not path.is_file():
        raise GateError(f"RUNTIME_PACKAGE_MISSING={path}")
    return str(json.loads(path.read_text(encoding="utf-8")).get("version", ""))


def is_approved_url(url: str) -> bool:
    return urlparse(url).scheme == "https" and (urlparse(url).hostname or "").lower() in APPROVED_HOSTS


def get_json(url: str) -> tuple[dict, str]:
    if not is_approved_url(url):
        raise GateError(f"NETWORK_SCOPE_VIOLATION={url}")
    request = Request(url, headers={"User-Agent": "CUMCM-G8-language-restore/1"})
    with urlopen(request, timeout=30) as response:  # nosec B310: host is allowlisted above
        final_url = response.geturl()
        if not is_approved_url(final_url):
            raise GateError(f"NETWORK_REDIRECT_SCOPE_VIOLATION={final_url}")
        return json.loads(response.read().decode("utf-8")), final_url


def resolve_source(language: str) -> dict[str, str]:
    package = f"@tesseract.js-data/{language}"
    metadata, metadata_final_url = get_json(f"https://data.jsdelivr.com/v1/package/npm/{package}")
    versions = metadata.get("versions", [])
    if not isinstance(versions, list) or not versions:
        raise GateError(f"PACKAGE_VERSION_METADATA_MISSING={language}")
    matches: list[dict[str, str]] = []
    expected_path = f"{FLAVOR}/{EXPECTED[language]['filename']}"
    for version in versions:
        if not isinstance(version, str) or version == "latest":
            continue
        listing, listing_final_url = get_json(f"https://data.jsdelivr.com/v1/package/npm/{package}@{version}/flat")
        files = listing.get("files", [])
        if any(isinstance(item, dict) and item.get("name") == f"/{expected_path}" for item in files):
            matches.append({
                "package": package,
                "package_version": version,
                "requested_url": f"https://cdn.jsdelivr.net/npm/{package}@{version}/{expected_path}",
                "metadata_url": metadata_final_url,
                "listing_url": listing_final_url,
            })
    if len(matches) != 1:
        raise GateError(f"FROZEN_FLAVOR_SOURCE_NOT_UNIQUE={language}:{len(matches)}")
    return matches[0]


def download(source: dict[str, str], candidate: Path) -> str:
    requested_url = source["requested_url"]
    if not is_approved_url(requested_url):
        raise GateError(f"NETWORK_SCOPE_VIOLATION={requested_url}")
    last_error: Exception | None = None
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            request = Request(requested_url, headers={"User-Agent": "CUMCM-G8-language-restore/1"})
            with urlopen(request, timeout=90) as response:  # nosec B310: host is allowlisted above
                final_url = response.geturl()
                if not is_approved_url(final_url):
                    raise GateError(f"NETWORK_REDIRECT_SCOPE_VIOLATION={final_url}")
                with candidate.open("wb") as stream:
                    shutil.copyfileobj(response, stream, length=1024 * 1024)
            source["final_url"] = final_url
            source["download_attempts"] = str(attempt)
            return sha256(candidate)
        except GateError:
            raise
        except (OSError, socket.timeout) as exc:
            last_error = exc
            candidate.unlink(missing_ok=True)
    raise GateError(f"DOWNLOAD_FAILED={source['package']}:{last_error}")


def historical_contract_resolved() -> bool:
    repair = REPAIR_MANIFEST.read_text(encoding="utf-8") if REPAIR_MANIFEST.is_file() else ""
    tools = "\n".join(path.read_text(encoding="utf-8") for path in HISTORICAL_TOOLS if path.is_file())
    return (
        '"traineddata_sha256"' in repair
        and "chi_sim.traineddata.gz" in tools
        and "eng.traineddata.gz" in tools
        and "actual = digest(local)" in tools
        and "gzip: true" in tools
        and "4.0.0_best_int" in tools
    )


def classify_final_root() -> str:
    if not LANGUAGE_ROOT.exists():
        return "ABSENT"
    if not LANGUAGE_ROOT.is_dir():
        return "UNKNOWN_EXISTING_CONTENT"
    names = {path.name for path in LANGUAGE_ROOT.iterdir()}
    expected_names = {"manifest.json", *(item["filename"] for item in EXPECTED.values())}
    if names != expected_names:
        return "UNKNOWN_EXISTING_CONTENT"
    try:
        if all(sha256(LANGUAGE_ROOT / EXPECTED[key]["filename"]) == EXPECTED[key]["sha256"] for key in EXPECTED):
            return "COMPLETE_FROZEN_VALID"
    except OSError:
        pass
    return "UNKNOWN_EXISTING_CONTENT"


def counts() -> dict[str, int]:
    artifact = ROOT / "catalog" / "scale" / "g8_artifact_manifest.csv"
    backlog = ROOT / "catalog" / "scale" / "g8_manual_backlog.csv"
    eligibility = ROOT / "catalog" / "scale" / "g8_artifact_eligibility.csv"
    with artifact.open(encoding="utf-8-sig", newline="") as stream:
        primary = sum(1 for _ in csv.DictReader(stream))
    with backlog.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    with eligibility.open(encoding="utf-8-sig", newline="") as stream:
        eligible_rows = list(csv.DictReader(stream))
    return {"PRIMARY_ARTIFACTS": primary, "ARTIFACT_SETS": primary // 3, "DOC_MANUAL_BACKLOG": sum(row.get("category") == "DOC_REPAIR_MANUAL" for row in rows), "Q3_MANUAL_BACKLOG": sum(row.get("category") == "Q3_REPAIR_MANUAL" for row in rows), "ELIGIBLE": sum(row.get("artifact_eligible") == "1" for row in eligible_rows), "INELIGIBLE": sum(row.get("artifact_eligible") != "1" for row in eligible_rows)}


def write_evidence(result: dict) -> None:
    for path in (RESULT_PATH, PROVENANCE_PATH, REPORT_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    provenance = {key: result.get(key) for key in result if key.startswith(("FROZEN_", "CHI_SIM_", "ENG_", "EXPECTED_", "DOWNLOADED_", "FINAL_", "LANGUAGE_", "RESTORED_"))}
    provenance.update({"historical_frozen_language_data_missing_locally": True, "restored_from_historical_approved_source": result.get("STATUS") == "PASS"})
    PROVENANCE_PATH.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# G8 Q3 OCR Language Data Network Restore", "", *[f"{key}={value}" for key, value in result.items()], ""]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    result: dict[str, object] = {
        "STAGE": "G8-Q3-OCR-LANGUAGE-DATA-NETWORK-RESTORE", "STATUS": "BLOCKED",
        "USER_NETWORK_RESTORE_AUTHORIZATION": 1, "Q3_IDENTITY_COUNT": 128, "PILOT_TARGET_COUNT": 0,
        "TESSERACT_JS_VERSION": read_package_version(TESSERACT_PACKAGE), "TESSERACT_JS_CORE_VERSION": read_package_version(TESSERACT_CORE_PACKAGE),
        "FROZEN_TESSDATA_FLAVOR": FLAVOR, "FROZEN_HASH_REPRESENTATION": "GZIP_FILE_BYTES" if historical_contract_resolved() else "UNRESOLVED",
        "FROZEN_HASH_REPRESENTATION_RESOLVED": int(historical_contract_resolved()), "LANGUAGE_DATA_ROOT": str(LANGUAGE_ROOT),
        "CHI_SIM_FROZEN_FILENAME": EXPECTED["chi_sim"]["filename"], "ENG_FROZEN_FILENAME": EXPECTED["eng"]["filename"],
        "EXPECTED_CHI_SIM_SHA256": EXPECTED["chi_sim"]["sha256"], "EXPECTED_ENG_SHA256": EXPECTED["eng"]["sha256"],
        "EXPECTED_LANGUAGE_FILE_COUNT": 2, "DOWNLOADED_LANGUAGE_FILE_COUNT": 0, "DOWNLOAD_RETRY_LIMIT": RETRY_LIMIT,
        "NETWORK_ACCESS_USED": 0, "DOWNLOAD_RUN": 0, "NETWORK_SCOPE_VIOLATION_COUNT": 0,
        "NEW_DEPENDENCY_INSTALLED": 0, "OCR_RUN": 0, "Q3_OCR_RUN": 0, "Q3_OCR_PAGE_COUNT": 0, "FULL_Q3_BATCH_RUN": 0,
        "FORMAL_ARTIFACTS_GENERATED": 0, "EXISTING_ARTIFACT_MODIFICATION_COUNT": 0,
        "WORD_RUN": 0, "WORD_COM_RUN": 0, "DOC_CONVERSION_RUN": 0, "PRINT_JOB_RUN": 0, "G9_RUN": 0, "G10_RUN": 0, "GIT_OPERATIONS": 0,
    }
    result.update(counts())
    try:
        if result["FROZEN_HASH_REPRESENTATION"] != "GZIP_FILE_BYTES":
            raise GateError("FROZEN_HASH_REPRESENTATION_UNRESOLVED")
        state = classify_final_root()
        result["LANGUAGE_DATA_ROOT_STATE_BEFORE"] = state
        if state == "UNKNOWN_EXISTING_CONTENT":
            raise GateError("LANGUAGE_DATA_ROOT_UNKNOWN_EXISTING_CONTENT")
        if state == "COMPLETE_FROZEN_VALID":
            result["REUSE_EXISTING_LANGUAGE_DATA"] = 1
            existing_manifest = json.loads((LANGUAGE_ROOT / "manifest.json").read_text(encoding="utf-8"))
            sources = {item["language"]: item["source"] for item in existing_manifest.get("languages", [])}
            normalized_languages = []
            for language, expected in EXPECTED.items():
                final_file = LANGUAGE_ROOT / expected["filename"]
                result[f"{language.upper()}_SOURCE_URL"] = sources.get(language, "")
                result[f"{language.upper()}_REQUEST_FINAL_URL"] = sources.get(language, "")
                result[f"DOWNLOADED_{language.upper()}_SHA256"] = sha256(final_file)
                result[f"{language.upper()}_SHA_MATCH"] = 1
                normalized_languages.append({"language": language, "local_path": str(final_file), "filename": final_file.name, "size": final_file.stat().st_size, "sha256": sha256(final_file), "source": sources.get(language, "")})
            existing_manifest["languages"] = normalized_languages
            (LANGUAGE_ROOT / "manifest.json").write_text(json.dumps(existing_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result["NETWORK_ACCESS_USED"] = 1
            result["DOWNLOAD_RUN"] = 1
            result["DOWNLOADED_LANGUAGE_FILE_COUNT"] = 2
        else:
            sources = {language: resolve_source(language) for language in EXPECTED}
            result["NETWORK_ACCESS_USED"] = 1
            result["DOWNLOAD_RUN"] = 1
            STAGING_ROOT.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="candidate_", dir=STAGING_ROOT) as temp_name:
                temp = Path(temp_name)
                downloaded: dict[str, Path] = {}
                for language, source in sources.items():
                    candidate = temp / EXPECTED[language]["filename"]
                    actual = download(source, candidate)
                    result[f"{language.upper()}_SOURCE_URL"] = source["requested_url"]
                    result[f"{language.upper()}_REQUEST_FINAL_URL"] = source.get("final_url", "")
                    result[f"DOWNLOADED_{language.upper()}_SHA256"] = actual
                    result[f"{language.upper()}_SHA_MATCH"] = int(actual == EXPECTED[language]["sha256"])
                    if actual != EXPECTED[language]["sha256"]:
                        QUARANTINE_ROOT.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(candidate), str(QUARANTINE_ROOT / f"{language}-{actual}.gz"))
                        raise GateError(f"SHA_MISMATCH={language}")
                    downloaded[language] = candidate
                result["DOWNLOADED_LANGUAGE_FILE_COUNT"] = len(downloaded)
                promotion = OCR_ROOT / "tesseract-data.stage"
                if promotion.exists():
                    raise GateError("PROMOTION_STAGE_ALREADY_EXISTS")
                promotion.mkdir(parents=True)
                language_records = []
                for language, candidate in downloaded.items():
                    final_file = promotion / EXPECTED[language]["filename"]
                    shutil.copy2(candidate, final_file)
                    language_records.append({"language": language, "local_path": str(LANGUAGE_ROOT / final_file.name), "filename": final_file.name, "size": final_file.stat().st_size, "sha256": sha256(final_file), "source": sources[language]["requested_url"]})
                manifest = {"ocr_engine": "tesseract.js", "ocr_engine_version": "7.0.0", "traineddata_revision": FLAVOR, "source_provider": "jsDelivr", "source_family": "@tesseract.js-data", "gzip": True, "languages": language_records, "restored_at": datetime.now(timezone.utc).isoformat(), "restore_stage": result["STAGE"]}
                (promotion / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                if LANGUAGE_ROOT.exists():
                    raise GateError("FINAL_ROOT_COLLISION_BEFORE_PROMOTION")
                promotion.rename(LANGUAGE_ROOT)
        for language, expected in EXPECTED.items():
            final_file = LANGUAGE_ROOT / expected["filename"]
            actual = sha256(final_file)
            result[f"FINAL_{language.upper()}_SHA256"] = actual
            result[f"FINAL_{language.upper()}_SHA_MATCH"] = int(actual == expected["sha256"])
            result.setdefault(f"DOWNLOADED_{language.upper()}_SHA256", actual)
            result.setdefault(f"{language.upper()}_SHA_MATCH", int(actual == expected["sha256"]))
            result.setdefault(f"{language.upper()}_SOURCE_URL", "REUSED_EXISTING_FROZEN_ROOT")
            result.setdefault(f"{language.upper()}_REQUEST_FINAL_URL", "REUSED_EXISTING_FROZEN_ROOT")
        result["LANGUAGE_DATA_ROOT_PRESENT"] = int(LANGUAGE_ROOT.is_dir())
        result["CHI_SIM_LANG_DATA_AVAILABLE"] = int((LANGUAGE_ROOT / EXPECTED["chi_sim"]["filename"]).is_file())
        result["ENG_LANG_DATA_AVAILABLE"] = int((LANGUAGE_ROOT / EXPECTED["eng"]["filename"]).is_file())
        result["RESTORE_MANIFEST_PRESENT"] = int((LANGUAGE_ROOT / "manifest.json").is_file())
        result["RESTORE_PROVENANCE_COMPLETE"] = 1
        result["RESTORED_HISTORICAL_FROZEN_BASELINE"] = 1
        result["NEWLY_ESTABLISHED_LANGUAGE_DATA_BASELINE"] = 0
        result["OCR_RUNTIME_READY"] = int(all(result[f"FINAL_{language.upper()}_SHA_MATCH"] == 1 for language in EXPECTED) and result["TESSERACT_JS_VERSION"] == "7.0.0" and result["TESSERACT_JS_CORE_VERSION"] == "7.0.0")
        if not result["OCR_RUNTIME_READY"]:
            raise GateError("OCR_RUNTIME_REBIND_FAILED")
        if result["ARTIFACT_SETS"] != 325 or result["PRIMARY_ARTIFACTS"] != 975 or result["DOC_MANUAL_BACKLOG"] != 0 or result["Q3_MANUAL_BACKLOG"] != 128 or result["ELIGIBLE"] != 453 or result["INELIGIBLE"] != 189:
            raise GateError("FROZEN_GOVERNANCE_COUNTS_MISMATCH")
        result["STATUS"] = "PASS"
        result["BLOCKER"] = "NONE"
        result["NEXT"] = "G8-Q3-CONTRACT-PILOT-RESUME"
    except (GateError, OSError, ValueError, json.JSONDecodeError) as exc:
        result["BLOCKER"] = str(exc)
        result["OCR_RUNTIME_READY"] = 0
        result["LANGUAGE_DATA_ROOT_PRESENT"] = int(LANGUAGE_ROOT.is_dir())
        result["NEXT"] = "G8-Q3-OCR-LANGUAGE-DATA-SOURCE-RECONCILIATION"
    write_evidence(result)
    for key, value in result.items():
        print(f"{key}={value}")
    print(f"OUTPUTS={RESULT_PATH}; {PROVENANCE_PATH}; {REPORT_PATH}")
    return 0 if result["STATUS"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
