#!/usr/bin/env python3
"""Evidence-first, resume-safe CUMCM corpus index builder (1992-2010).

The trusted source tree is immutable.  This program does not run OCR and does
not execute code or macros found in the corpus.  Automatic yearly output is a
conservative candidate layer; only records with explicit manual evidence may
be promoted to verified status.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover - Actions installs this dependency
    fitz = None


ROOT = Path(__file__).resolve().parents[1]
SOURCE_BASELINE = "a042ecf898feaba6fc81d543a10e0188db8b2b12"
SCHEMA_VERSION = "1.4.1"
PARSER_VERSION = "0.5.1"
YEARS = tuple(range(1992, 2011))

ANALYSIS = ROOT / "analysis-index"
CONTROL = ANALYSIS / "00_control"
INVENTORY = ANALYSIS / "01_inventory"
DOCUMENTS = ANALYSIS / "02_documents"
EVIDENCE = ANALYSIS / "03_evidence"
RELATIONS = ANALYSIS / "04_relations"
KNOWLEDGE = ANALYSIS / "05_knowledge"
STATISTICS = ANALYSIS / "06_statistics"
REPORTS = ANALYSIS / "07_reports"
QUALITY = ANALYSIS / "08_quality"
CHECKPOINTS = ANALYSIS / "09_checkpoints"
CACHE = ANALYSIS / "cache"

DERIVED_PREFIXES = (
    "analysis-index/", "scripts/", "tests/", "schema/", ".github/",
    ".bootstrap/", "README_ANALYSIS.md", "README_PIPELINE.md", ".gitignore",
)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".webp"}
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz"}
CODE_EXTS = {".py", ".m", ".r", ".c", ".cc", ".cpp", ".h", ".java", ".ipynb"}
DATA_EXTS = {".csv", ".tsv", ".xls", ".xlsx", ".json", ".mat", ".dat", ".sav"}
DOC_EXTS = {".doc", ".docx", ".wps", ".rtf"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".wmv", ".mkv"}

ROLES = {"award_paper", "expert_commentary", "problem_statement", "solution_summary", "other_related", "unknown"}
SUBTYPES = {"validation_summary", "solution_outline", "editorial_note", "problem_background", "method_note", "none"}
FIELD_STATUSES = {"present", "absent", "unknown", "not_applicable"}
PARSE_STATUSES = {"parsed", "partially_parsed", "pending_ocr", "pending_manual_review", "metadata_only", "unsupported", "corrupted", "duplicate"}
EVIDENCE_STATUSES = {"verified", "key_content_verified", "content_verified_partial", "unverified"}
COMPLETENESS_STATUSES = {"complete", "missing_start", "missing_end", "missing_middle", "missing_segment", "unknown"}
SEGMENTATION_STATUSES = {"not_required", "candidate", "segmented", "pending_manual_review"}
RELATION_TYPES = {
    "contains", "partial_copy_of", "duplicate_representation_of", "answers_problem",
    "comments_on", "evaluates_solution", "adjacent_to", "contaminated_by",
    "continuation_of", "resolved_alias", "same_solution_lineage",
}
ELIGIBILITY_KEYS = {
    "metadata_statistics", "structure_statistics", "model_statistics", "algorithm_statistics",
    "visualization_statistics", "result_pattern_statistics", "reviewer_feedback_statistics",
    "full_text_statistics", "lexical_statistics", "formula_completeness_statistics",
}
CORPUS_KEYS = {"award_paper_patterns", "reviewer_feedback", "problem_analysis", "validation_patterns", "visualization_patterns"}

FEATURES = {
    "abstract": ("structure_statistics", ["摘要", "abstract"]),
    "model_assumptions": ("structure_statistics", ["模型假设", "基本假设", "假设"]),
    "symbol_definitions": ("structure_statistics", ["符号说明", "符号定义", "记号说明"]),
    "model_validation": ("model_statistics", ["模型检验", "模型验证", "结果检验", "验证"]),
    "sensitivity_analysis": ("model_statistics", ["敏感性", "灵敏度"]),
    "error_analysis": ("model_statistics", ["误差分析", "误差估计"]),
    "final_solution": ("result_pattern_statistics", ["最终方案", "最优方案", "结论", "结果"]),
    "final_answer_summary_table": ("result_pattern_statistics", ["汇总表", "结果表", "答案表"]),
    "flowchart": ("visualization_statistics", ["流程图", "技术路线"]),
    "visualization": ("visualization_statistics", ["图1", "图 1", "表1", "表 1", "见图", "见表"]),
    "references": ("structure_statistics", ["参考文献", "references"]),
    "appendix": ("structure_statistics", ["附录", "appendix"]),
    "code_description": ("structure_statistics", ["程序", "算法实现", "代码", "源程序"]),
}
MODEL_TERMS = {
    "linear_programming": ["线性规划", "linear programming"],
    "integer_programming": ["整数规划", "0-1规划", "integer programming"],
    "nonlinear_programming": ["非线性规划", "nonlinear programming"],
    "dynamic_programming": ["动态规划", "dynamic programming"],
    "graph_model": ["图论", "最短路", "网络流", "图模型"],
    "regression": ["回归分析", "回归模型", "regression"],
    "time_series": ["时间序列", "ARIMA", "灰色预测"],
    "queueing": ["排队论", "排队模型"],
    "simulation": ["仿真", "模拟", "simulation"],
    "markov": ["马尔可夫", "Markov"],
    "ahp": ["层次分析法", "AHP"],
    "neural_network": ["神经网络", "BP网络"],
    "petri_net": ["Petri网", "Petri net"],
}
ALGORITHM_TERMS = {
    "enumeration": ["枚举", "穷举"],
    "genetic_algorithm": ["遗传算法", "genetic algorithm"],
    "simulated_annealing": ["模拟退火"],
    "gradient_method": ["梯度法", "梯度下降"],
    "simplex": ["单纯形法"],
    "branch_and_bound": ["分支定界"],
    "monte_carlo": ["Monte Carlo", "蒙特卡洛"],
}


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run(*args: str, check: bool = True) -> str:
    cp = subprocess.run(args, cwd=ROOT, check=check, capture_output=True, text=True)
    return cp.stdout


def stable_id(prefix: str, *parts: object) -> str:
    raw = "\x1f".join(str(p) for p in parts).encode("utf-8", "surrogatepass")
    return prefix + hashlib.sha256(raw).hexdigest()[:16]


def ensure_dirs() -> None:
    for path in (
        CONTROL, INVENTORY, DOCUMENTS, EVIDENCE, RELATIONS, KNOWLEDGE,
        STATISTICS / "yearly", STATISTICS / "cross_year",
        REPORTS / "recovery", REPORTS / "yearly", REPORTS / "cross_year",
        QUALITY / "gates", QUALITY / "regression", QUALITY / "unresolved",
        CHECKPOINTS, CACHE / "hashes", CACHE / "pdf", CACHE / "text",
    ):
        path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str] | None = None) -> None:
    materialized = list(rows)
    if fields is None:
        fields = sorted({k for row in materialized for k in row})
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow({k: csv_value(row.get(k)) for k in fields})
    tmp.replace(path)


def csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    return value


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def baseline_entries() -> list[dict[str, Any]]:
    output = run("git", "ls-tree", "-r", "-l", SOURCE_BASELINE)
    rows = []
    for line in output.splitlines():
        meta, path = line.split("\t", 1)
        mode, obj_type, sha, size = meta.split(" ", 3)
        if path.startswith(DERIVED_PREFIXES):
            continue
        rows.append({"mode": mode, "git_object_type": obj_type, "git_sha": sha,
                     "git_blob_size": int(size) if size != "-" else None, "relative_path": path})
    return rows


def verify_source() -> dict[str, Any]:
    baseline_type = run("git", "cat-file", "-t", SOURCE_BASELINE).strip()
    head = run("git", "rev-parse", "HEAD").strip()
    changed = []
    for line in run("git", "status", "--porcelain").splitlines():
        path = line[3:].strip('"')
        if path and not path.startswith(DERIVED_PREFIXES):
            changed.append(path)
    committed_changes = [path for path in run("git", "diff", "--name-only", SOURCE_BASELINE, "HEAD").splitlines()
                         if path and not path.startswith(DERIVED_PREFIXES)]
    if baseline_type != "commit":
        raise RuntimeError("trusted source baseline is not a commit")
    if changed:
        raise RuntimeError(f"original source paths modified: {changed[:10]}")
    if committed_changes:
        raise RuntimeError(f"analysis branch contains committed source changes: {committed_changes[:10]}")
    return {"source_baseline_commit": SOURCE_BASELINE, "baseline_type": baseline_type,
            "analysis_head": head, "original_source_modifications": 0,
            "committed_source_modifications": 0}


def detect_lfs(path: Path) -> dict[str, Any]:
    try:
        data = path.read_bytes()[:1024]
    except OSError:
        return {"lfs_status": "unreadable", "lfs_oid": "", "lfs_declared_size": None}
    text = data.decode("utf-8", "ignore")
    if text.startswith("version https://git-lfs.github.com/spec/v1"):
        oid = re.search(r"oid sha256:([0-9a-f]{64})", text)
        size = re.search(r"size (\d+)", text)
        return {"lfs_status": "pointer_only", "lfs_oid": oid.group(1) if oid else "",
                "lfs_declared_size": int(size.group(1)) if size else None}
    return {"lfs_status": "not_lfs", "lfs_oid": "", "lfs_declared_size": None}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_year(path: str) -> int | None:
    match = re.search(r"(?<!\d)(19\d{2}|20\d{2})(?!\d)", path)
    return int(match.group(1)) if match else None


def problem_code(path: str, text: str = "") -> str:
    source = f"{PurePosixPath(path).name} {path} {text[:500]}"
    matches = re.findall(r"(?:^|[^A-Za-z])([ABCDE])(?:题|Problem|[^A-Za-z])", source, re.I)
    return matches[0].upper() if matches else "unknown"


def file_category(path: str) -> str:
    lower, ext = path.lower(), Path(path).suffix.lower()
    if ext == ".pdf":
        if any(x in path for x in ("赛题", "真题", "题目")) or re.search(r"[/\\][A-E]题(?:[/\\]|\.)", path):
            return "problem_statement"
        return "paper_related_pdf"
    if ext in IMAGE_EXTS: return "image"
    if ext in ARCHIVE_EXTS: return "archive"
    if ext in CODE_EXTS: return "source_code"
    if ext in DATA_EXTS: return "dataset"
    if ext in DOC_EXTS: return "document"
    if ext in VIDEO_EXTS: return "video"
    if "模板" in path or "format" in lower: return "template"
    return "unknown"


def candidate_pdf(path: str) -> bool:
    if Path(path).suffix.lower() != ".pdf":
        return False
    year = extract_year(path)
    if year is None:
        return False
    markers = ("优秀论文", "优秀答卷", "赛题", "真题", "评注", "评述", "论文")
    return any(marker in path for marker in markers) or year <= 1995


def pdf_probe(path: Path, cache_key: str, resume: bool) -> tuple[dict[str, Any], bool]:
    cache_path = CACHE / "pdf" / f"{cache_key}.json"
    if resume and cache_path.exists():
        return read_json(cache_path, {}), True
    result: dict[str, Any] = {"page_count": None, "pdf_status": "unprobed", "encrypted": False,
                              "sample_text_chars": 0, "text_layer_status": "unknown", "image_count_sample": 0}
    if fitz is None:
        result["pdf_status"] = "dependency_missing"
    else:
        try:
            doc = fitz.open(path)
            result["page_count"] = doc.page_count
            result["encrypted"] = bool(doc.needs_pass)
            if doc.needs_pass:
                result["pdf_status"] = "encrypted"
            else:
                samples = sorted({0, max(0, doc.page_count // 2), max(0, doc.page_count - 1)}) if doc.page_count else []
                chars = images = 0
                for index in samples:
                    page = doc[index]
                    chars += len(page.get_text("text"))
                    images += len(page.get_images(full=True))
                result.update({"pdf_status": "readable", "sample_text_chars": chars,
                               "image_count_sample": images,
                               "text_layer_status": "native_text" if chars >= 120 else "scanned_or_no_text"})
            doc.close()
        except Exception as exc:  # malformed PDFs remain explicit
            result.update({"pdf_status": "corrupted_or_unsupported", "error": f"{type(exc).__name__}: {exc}"})
    write_json(cache_path, result)
    return result, False


def safe_zip_manifest(path: Path, parent_id: str) -> list[dict[str, Any]]:
    rows = []
    try:
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                member = PurePosixPath(info.filename.replace("\\", "/"))
                unsafe = member.is_absolute() or ".." in member.parts
                rows.append({"archive_id": parent_id, "archive_path": str(path.relative_to(ROOT)),
                             "member_path": str(member), "compressed_size": info.compress_size,
                             "uncompressed_size": info.file_size, "is_directory": info.is_dir(),
                             "unsafe_path": unsafe, "member_extension": member.suffix.lower()})
    except (zipfile.BadZipFile, OSError):
        pass
    return rows


def build_inventory(resume: bool) -> dict[str, Any]:
    ensure_dirs()
    source = verify_source()
    entries = baseline_entries()
    old_cache = {row["relative_path"]: row for row in read_jsonl(CACHE / "hashes" / "files.jsonl")}
    rows, hash_cache, pdf_rows, archive_rows = [], [], [], []
    reused_hashes = reused_pdf = 0
    for index, entry in enumerate(entries, 1):
        rel = entry["relative_path"]
        path = ROOT / rel
        ext = path.suffix.lower()
        lfs = detect_lfs(path)
        checkout_size = path.stat().st_size if path.exists() else None
        signature = f"{entry['git_sha']}:{checkout_size}:{lfs['lfs_status']}"
        cached = old_cache.get(rel)
        if resume and cached and cached.get("signature") == signature:
            digest = cached["sha256"]
            reused_hashes += 1
        elif path.exists():
            digest = sha256_file(path)
        else:
            digest = ""
        hash_cache.append({"relative_path": rel, "signature": signature, "sha256": digest})
        status = "metadata_only"
        error = ""
        probe = {}
        if ext == ".pdf" and path.exists():
            probe, reused = pdf_probe(path, entry["git_sha"], resume)
            reused_pdf += int(reused)
            if probe.get("pdf_status") == "corrupted_or_unsupported":
                status, error = "corrupted", probe.get("error", "")
            pdf_rows.append({"file_id": stable_id("file_", rel), "relative_path": rel, **probe})
        elif not path.exists():
            status, error = "unsupported", "tracked path not materialized"
        row = {"file_id": stable_id("file_", rel), "relative_path": rel, "filename": path.name,
               "extension": ext, "year": extract_year(rel), "problem_code": problem_code(rel),
               "file_category": file_category(rel), "parse_status": status,
               "sha256": digest, "hash_scope": "checkout_bytes", "checkout_size": checkout_size,
               "logical_size": lfs["lfs_declared_size"] or checkout_size,
               "error_message": error, "candidate_related": candidate_pdf(rel),
               "last_processed_at": now(), **entry, **lfs, **probe}
        rows.append(row)
        if ext == ".zip" and path.exists():
            archive_rows.extend(safe_zip_manifest(path, row["file_id"]))
    groups: dict[tuple[str, int | None], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["sha256"]:
            groups[(row["sha256"], row["checkout_size"])].append(row)
    duplicates = []
    for members in groups.values():
        if len(members) < 2:
            continue
        gid = stable_id("duplicate_", members[0]["sha256"], members[0]["checkout_size"])
        for pos, row in enumerate(sorted(members, key=lambda x: x["relative_path"])):
            row["duplicate_group"] = gid
            if pos:
                row["parse_status"] = "duplicate"
        duplicates.append({"duplicate_group": gid, "file_count": len(members),
                           "size_bytes": members[0]["checkout_size"], "sha256": members[0]["sha256"],
                           "paths": [x["relative_path"] for x in members]})
    for row in rows:
        row.setdefault("duplicate_group", "")
    write_jsonl(CACHE / "hashes" / "files.jsonl", hash_cache)
    write_csv(INVENTORY / "repository_inventory.csv", rows)
    write_csv(INVENTORY / "duplicate_files.csv", duplicates)
    write_csv(INVENTORY / "pdf_manifest.csv", pdf_rows)
    write_csv(INVENTORY / "archive_manifest.csv", archive_rows)
    write_csv(INVENTORY / "lfs_files.csv", [r for r in rows if r["lfs_status"] != "not_lfs"])
    write_csv(INVENTORY / "unparsed_files.csv", [r for r in rows if r["parse_status"] not in {"metadata_only", "duplicate"}])

    carriers = discover_carriers(rows, archive_rows)
    write_csv(INVENTORY / "candidate_carriers.csv", carriers)
    physical = sum((r["checkout_size"] or 0) for r in rows)
    logical = sum((r["logical_size"] or 0) for r in rows)
    summary = {**source, "schema_version": SCHEMA_VERSION, "parser_version": PARSER_VERSION,
               "tracked_source_files": len(rows), "checkout_bytes": physical, "logical_bytes": logical,
               "candidate_carriers": len(carriers), "candidate_pdf_carriers": sum(c["carrier_type"] == "pdf" for c in carriers),
               "direct_image_groups": sum(c["carrier_type"] == "image_group" for c in carriers),
               "zip_image_groups": sum(c["carrier_type"] == "zip_image_group" for c in carriers),
               "lfs_files": sum(r["lfs_status"] != "not_lfs" for r in rows),
               "duplicate_groups": len(duplicates), "duplicate_files": sum(d["file_count"] for d in duplicates),
               "hashes_reused": reused_hashes, "pdf_probes_reused": reused_pdf, "updated_at": now()}
    write_json(CONTROL / "inventory_summary.json", summary)
    write_inventory_reconciliation(summary)
    write_json(CHECKPOINTS / "inventory_checkpoint.json", {"checkpoint_type": "inventory", **summary})
    return summary


def discover_carriers(rows: list[dict[str, Any]], archive_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    carriers = []
    for row in rows:
        if row["candidate_related"] and row["extension"] == ".pdf":
            carriers.append({"carrier_document_id": stable_id("carrier_", row["relative_path"]),
                "relative_path": row["relative_path"], "carrier_type": "pdf", "year": row["year"],
                "source_file_ids": [row["file_id"]], "archive_parent": "", "existing_cache_status": "unknown"})
    image_groups: dict[tuple[int | None, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["extension"] in IMAGE_EXTS and extract_year(row["relative_path"]):
            image_groups[(row["year"], str(PurePosixPath(row["relative_path"]).parent))].append(row)
    for (year, parent), members in image_groups.items():
        if any(x in parent for x in ("优秀论文", "论文", "扫描")):
            carriers.append({"carrier_document_id": stable_id("carrier_img_", parent), "relative_path": parent,
                "carrier_type": "image_group", "year": year, "source_file_ids": [m["file_id"] for m in members],
                "archive_parent": "", "existing_cache_status": "unknown"})
    zip_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for member in archive_rows:
        if member["member_extension"] in IMAGE_EXTS and not member["unsafe_path"]:
            parent = str(PurePosixPath(member["member_path"]).parent)
            zip_groups[(member["archive_path"], parent)].append(member)
    for (archive, parent), members in zip_groups.items():
        year = extract_year(archive)
        if year:
            carriers.append({"carrier_document_id": stable_id("carrier_zipimg_", archive, parent),
                "relative_path": f"{archive}!/{parent}", "carrier_type": "zip_image_group", "year": year,
                "source_file_ids": [], "archive_parent": archive, "existing_cache_status": "unknown"})
    return sorted(carriers, key=lambda x: (x["year"] or 0, x["relative_path"]))


def write_inventory_reconciliation(summary: dict[str, Any]) -> None:
    anchors = {"tracked_source_files": 3614, "checkout_bytes_materialized_lfs": 2757912015,
               "candidate_carriers": 546, "candidate_pdf_carriers": 506,
               "direct_image_groups": 24, "zip_image_groups": 16, "lfs_files": 1,
               "duplicate_groups_approx": 75, "duplicate_files_approx": 166}
    lines = ["# Inventory灾难恢复对账\n\n",
             "本报告由可信基线重新扫描生成；历史数字仅作为对账锚点。\n\n",
             "| 指标 | 新扫描 | 历史锚点 | 判定 |\n|---|---:|---:|---|\n"]
    for key in ("tracked_source_files", "candidate_carriers", "candidate_pdf_carriers", "direct_image_groups", "zip_image_groups", "lfs_files", "duplicate_groups", "duplicate_files"):
        anchor_key = key if key in anchors else f"{key}_approx"
        actual, expected = summary.get(key), anchors.get(anchor_key)
        verdict = "完全一致" if actual == expected else "需解释"
        lines.append(f"| {key} | {actual} | {expected} | {verdict} |\n")
    lines.extend(["\n## 容量口径\n\n",
                  f"当前检出字节为 `{summary['checkout_bytes']}`；LFS保持指针时不得与历史物化容量直接比较。",
                  f" 按LFS声明容量计算的逻辑字节为 `{summary['logical_bytes']}`。\n"])
    (REPORTS / "recovery" / "inventory_reconciliation.md").write_text("".join(lines), encoding="utf-8")


def load_inventory() -> list[dict[str, Any]]:
    path = INVENTORY / "repository_inventory.csv"
    if not path.exists():
        build_inventory(True)
    with path.open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load_carriers() -> list[dict[str, Any]]:
    path = INVENTORY / "candidate_carriers.csv"
    if not path.exists():
        build_inventory(True)
    with path.open(encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        for key in ("source_file_ids",):
            try: row[key] = json.loads(row[key])
            except (ValueError, TypeError): row[key] = []
        row["year"] = int(row["year"]) if row.get("year") else None
    return rows


def classify_role(path: str, text: str = "") -> tuple[str, str, float, list[str]]:
    joined = f"{path}\n{text[:3000]}"
    signals = []
    if any(x in joined for x in ("评注", "评述", "点评", "答卷评", "专家评论")):
        return "expert_commentary", "none", .94, ["commentary language/title"]
    if any(x in joined for x in ("方案检验摘要", "模型的检验", "结果复核摘要")):
        return "solution_summary", "validation_summary", .90, ["validation-summary title"]
    if any(x in path for x in ("真题", "赛题", "题目")) or re.search(r"(?:^|[/：])(?:19\d{2}|20\d{2})?[A-E]题(?:[/：.]|$)", path):
        return "problem_statement", "none", .91, ["problem path/title"]
    if any(x in path for x in ("优秀论文", "优秀答卷")):
        return "award_paper", "none", .78, ["award-paper directory", "requires content confirmation"]
    if "论文" in path:
        return "other_related", "none", .62, ["paper-related path only"]
    if text:
        signals.append("native first-page text available")
    return "unknown", "none", .35, signals or ["insufficient signals"]


def corpus_eligibility(role: str) -> dict[str, str]:
    result = {key: "excluded" for key in CORPUS_KEYS}
    mapping = {"award_paper": ["award_paper_patterns", "visualization_patterns"],
               "expert_commentary": ["reviewer_feedback"], "problem_statement": ["problem_analysis"],
               "solution_summary": ["validation_patterns"]}
    if role == "unknown":
        return {key: "pending" for key in CORPUS_KEYS}
    for key in mapping.get(role, []): result[key] = "included"
    return result


def extract_pdf_pages(path: Path, cache_key: str, resume: bool) -> tuple[list[dict[str, Any]], bool]:
    cache_path = CACHE / "text" / f"{cache_key}.json"
    if resume and cache_path.exists():
        return read_json(cache_path, []), True
    pages = []
    if fitz is None:
        return pages, False
    try:
        doc = fitz.open(path)
        if doc.needs_pass:
            return pages, False
        for index, page in enumerate(doc):
            rect = page.rect
            text = page.get_text("text", sort=True)
            pages.append({"page": index + 1, "width": rect.width, "height": rect.height,
                          "rotation": page.rotation, "text": text, "text_chars": len(text),
                          "image_count": len(page.get_images(full=True))})
        doc.close()
    except Exception:
        pages = []
    write_json(cache_path, pages)
    return pages, False


def feature_records(text: str, page_texts: list[str], text_status: str, role: str) -> list[dict[str, Any]]:
    records = []
    enough = text_status == "native_text" and len(text.strip()) >= 500
    for name, (category, terms) in FEATURES.items():
        if role == "problem_statement" and name in {"abstract", "model_assumptions", "model_validation", "sensitivity_analysis", "error_analysis", "references", "appendix", "code_description"}:
            status, value, eligible, reason = "not_applicable", None, False, "field not applicable to problem statement"
            pages = []
        elif not enough:
            status, value, eligible, reason, pages = "unknown", None, False, "native full text unavailable", []
        else:
            hits = [i + 1 for i, body in enumerate(page_texts) if any(term.lower() in body.lower() for term in terms)]
            status, value, eligible = ("present", True, True) if hits else ("absent", False, True)
            reason, pages = "", hits
        records.append({"field_name": name, "value": value, "value_status": status,
                        "evidence_status": "unverified" if status in {"unknown", "absent"} else "content_verified_partial",
                        "source_pages": pages, "source_bbox": [], "analysis_category": category,
                        "eligible_for_statistics": eligible, "exclusion_reason": reason})
    return records


def terms_found(text: str, dictionary: dict[str, list[str]]) -> list[str]:
    lower = text.lower()
    return [name for name, aliases in dictionary.items() if any(alias.lower() in lower for alias in aliases)]


def preserve_manual(existing: dict[str, dict[str, Any]], generated: dict[str, Any]) -> dict[str, Any]:
    old = existing.get(generated["logical_document_id"])
    if not old or not old.get("manual_overrides"):
        return generated
    protected = {"document_role", "document_subtype", "role_classification", "corpus_eligibility",
                 "segmentation_status", "completeness_status", "evidence_status", "feature_statistics",
                 "problem_id", "solution_lineage_id", "manual_overrides"}
    return {**generated, **{key: old[key] for key in protected if key in old}}


def build_year(year: int, resume: bool) -> dict[str, Any]:
    ensure_dirs()
    verify_source()
    inventory = load_inventory()
    by_path = {row["relative_path"]: row for row in inventory}
    carriers = [c for c in load_carriers() if c["year"] == year]
    existing_docs = {r["logical_document_id"]: r for r in read_jsonl(DOCUMENTS / "logical_documents.jsonl")}
    all_existing = [r for r in existing_docs.values() if int(r.get("year", 0)) != year]
    docs, representations, segments, boundaries, review_queue = [], [], [], [], []
    reused_text = 0
    for order, carrier in enumerate(carriers, 1):
        rel = carrier["relative_path"]
        inv = by_path.get(rel, {})
        pages: list[dict[str, Any]] = []
        if carrier["carrier_type"] == "pdf" and (ROOT / rel).exists():
            pages, reused = extract_pdf_pages(ROOT / rel, inv.get("git_sha", stable_id("x", rel)), resume)
            reused_text += int(reused)
        page_texts = [p["text"] for p in pages]
        text = "\n".join(page_texts)
        text_status = "native_text" if len(text.strip()) >= 500 else "scanned_or_no_text"
        role, subtype, confidence, basis = classify_role(rel, text)
        code = problem_code(rel, text)
        cid = carrier["carrier_document_id"]
        logical_id = stable_id("logical_", year, rel)
        representation_id = stable_id("representation_", cid, logical_id)
        likely_multi = any(x in rel for x in ("全集", "合集", "分卷", "合订"))
        segmentation = "pending_manual_review" if likely_multi else "not_required"
        completeness = "unknown" if likely_multi else "complete"
        parse_status = "partially_parsed" if pages else "metadata_only"
        evidence_status = "content_verified_partial" if text_status == "native_text" else "unverified"
        if text_status != "native_text" and pages:
            parse_status = "pending_manual_review"
        problem_id = f"problem_cumcm_{year}_{code.lower()}" if code != "unknown" else None
        lineage = stable_id("lineage_", year, code, logical_id) if role == "award_paper" else None
        features = feature_records(text, page_texts, text_status, role)
        enabled = sorted({"metadata_statistics"} | {r["analysis_category"] for r in features if r["eligible_for_statistics"]})
        document = {"schema_version": SCHEMA_VERSION, "parser_version": PARSER_VERSION,
            "entity_type": "logical_document", "logical_document_id": logical_id,
            "carrier_document_ids": [cid], "segment_ids": [], "article_order": order,
            "title": Path(rel).stem, "authors": [], "year": year, "problem_code": code,
            "problem_id": problem_id, "solution_lineage_id": lineage, "document_role": role,
            "document_subtype": subtype, "role_classification": {"predicted_role": role,
                "confidence": confidence, "classification_basis": basis, "conflicting_signals": [],
                "manually_verified": False}, "corpus_eligibility": corpus_eligibility(role),
            "parse_status": parse_status, "evidence_status": evidence_status,
            "segmentation_status": segmentation, "completeness_status": completeness,
            "corpus_status": "candidate", "representation_quality": "candidate",
            "analysis_eligibility": enabled, "feature_statistics": features,
            "models": terms_found(text, MODEL_TERMS), "algorithms": terms_found(text, ALGORITHM_TERMS),
            "source_path": rel, "page_count": len(pages) or inv.get("page_count") or None,
            "text_layer_status": text_status, "manual_overrides": False, "updated_at": now()}
        document = preserve_manual(existing_docs, document)
        docs.append(document)
        for p in pages:
            seg_id = stable_id("segment_", cid, p["page"], "whole")
            segment = {"segment_id": seg_id, "carrier_document_id": cid, "logical_document_id": logical_id,
                "page": p["page"], "include_bbox": [0, 0, p["width"], p["height"]], "exclude_bbox": [],
                "normalized_bbox": [0, 0, 1, 1], "page_width": p["width"], "page_height": p["height"],
                "page_rotation": p["rotation"], "coordinate_origin": "top-left", "coordinate_unit": "PDF point",
                "reason": "whole-page automatic candidate", "segmentation_status": segmentation,
                "manually_verified": False}
            segments.append(segment); document["segment_ids"].append(seg_id)
        representations.append({"representation_id": representation_id, "logical_document_id": logical_id,
            "carrier_document_id": cid, "segment_ids": document["segment_ids"], "page_coverage": [p["page"] for p in pages],
            "completeness": completeness, "visual_quality": "unreviewed", "text_layer_quality": text_status,
            "table_quality": "unreviewed", "formula_quality": "unreviewed", "page_order_quality": "unreviewed",
            "contamination_level": "unknown", "preferred_representation": True,
            "preference_reason": "only representation currently identified; pending comparative review"})
        if likely_multi or role in {"unknown", "other_related"} or text_status != "native_text":
            review_queue.append({"logical_document_id": logical_id, "carrier_document_id": cid, "year": year,
                "reason": "multi-article carrier" if likely_multi else "role/text requires visual review",
                "priority": "high" if likely_multi else "normal", "status": "pending_manual_review"})
        write_document_bundle(document, pages, representations[-1])

    merged_docs = sorted(all_existing + docs, key=lambda x: (int(x.get("year", 0)), x["logical_document_id"]))
    write_jsonl(DOCUMENTS / "logical_documents.jsonl", merged_docs)
    write_jsonl(DOCUMENTS / f"logical_documents_{year}.jsonl", docs)
    write_jsonl(DOCUMENTS / f"page_segments_{year}.jsonl", segments)
    write_jsonl(DOCUMENTS / f"article_boundaries_{year}.jsonl", boundaries)
    write_jsonl(DOCUMENTS / f"representations_{year}.jsonl", representations)
    write_csv(DOCUMENTS / f"{year}_carrier_manifest.csv", yearly_carrier_manifest(carriers, by_path))
    write_csv(DOCUMENTS / f"{year}_logical_document_manifest.csv", docs)
    update_global_relations_and_lineages(year, docs, representations)
    write_jsonl(QUALITY / "unresolved" / f"{year}_manual_review_queue.jsonl", review_queue)
    stats = yearly_statistics(year, carriers, docs, representations, segments, review_queue)
    write_year_report(year, stats, docs, review_queue)
    gate = year_gate(year, carriers, docs, representations, stats, review_queue)
    checkpoint = {"checkpoint_type": "year", "year": year, "status": gate["status"],
                  "schema_version": SCHEMA_VERSION, "parser_version": PARSER_VERSION,
                  "source_baseline_commit": SOURCE_BASELINE, "documents": len(docs),
                  "carriers": len(carriers), "text_caches_reused": reused_text,
                  "known_issues": [r["reason"] for r in review_queue], "created_at": now()}
    write_json(CHECKPOINTS / f"{year}_checkpoint.json", checkpoint)
    update_progress(year, gate["status"])
    return {"year": year, "status": "reused" if resume and reused_text == len([c for c in carriers if c["carrier_type"] == "pdf"]) else "processed",
            "carriers": len(carriers), "logical_documents": len(docs), "manual_review": len(review_queue),
            "quality_gate": gate["status"], "text_caches_reused": reused_text}


def yearly_carrier_manifest(carriers: list[dict[str, Any]], by_path: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for carrier in carriers:
        inv = by_path.get(carrier["relative_path"], {})
        result.append({**carrier, "filename": Path(carrier["relative_path"]).name,
            "file_type": carrier["carrier_type"], "file_size": inv.get("checkout_size"),
            "page_count": inv.get("page_count"), "image_count": "unknown",
            "text_layer_status": "see_pdf_manifest", "preclassified_role": classify_role(carrier["relative_path"])[0],
            "classification_confidence": classify_role(carrier["relative_path"])[2],
            "contains_multiple_articles": any(x in carrier["relative_path"] for x in ("全集", "合集", "分卷", "合订")),
            "toc_present": "unknown", "boundary_candidates": "pending", "same_page_boundary_candidates": "pending",
            "needs_segmentation": any(x in carrier["relative_path"] for x in ("全集", "合集", "分卷", "合订")),
            "needs_ocr": "unknown", "quality_warnings": "automatic preflight only",
            "possible_duplicate_carriers": [], "existing_cache_status": carrier.get("existing_cache_status", "unknown")})
    return result


def write_document_bundle(doc: dict[str, Any], pages: list[dict[str, Any]], representation: dict[str, Any]) -> None:
    folder = DOCUMENTS / "cards" / doc["logical_document_id"]
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "metadata.json", doc)
    page_map = {"logical_document_id": doc["logical_document_id"], "page_number_basis": "carrier-local, 1-based",
                "representation_id": representation["representation_id"],
                "pages": [{k: p[k] for k in ("page", "width", "height", "rotation", "text_chars", "image_count")} for p in pages]}
    write_json(folder / "page_map.json", page_map)
    evidence = [{"logical_document_id": doc["logical_document_id"], "source_page": r["source_pages"][0],
                 "source_bbox": [], "evidence_type": "feature_keyword", "text_excerpt": "keyword occurrence",
                 "normalized_claim": f"{r['field_name']} present", "confidence": .65,
                 "extraction_method": "native_text_keyword", "manual_review_required": True}
                for r in doc["feature_statistics"] if r["value_status"] == "present" and r["source_pages"]]
    write_jsonl(folder / "evidence.jsonl", evidence)
    extracted = [f"# {doc['title']}\n\n> Local native-text cache; not tracked in Git.\n"]
    for page in pages:
        extracted.append(f"\n## Page {page['page']}\n\n{page['text']}\n")
    (folder / "extracted_text.md").write_text("".join(extracted), encoding="utf-8")
    card = [f"# {doc['title']}\n\n", f"- 年份：{doc['year']}\n", f"- 角色：{doc['document_role']}\n",
            f"- 状态：{doc['parse_status']} / {doc['evidence_status']} / {doc['completeness_status']}\n",
            f"- 题号：{doc['problem_code']}\n", f"- 模型候选：{', '.join(doc['models']) or '待核验'}\n",
            f"- 算法候选：{', '.join(doc['algorithms']) or '待核验'}\n",
            "\n> 本卡片为自动保守候选；未标记 manually_verified 前不得作为人工结论。\n"]
    (folder / "document_card.md").write_text("".join(card), encoding="utf-8")
    (folder / "review_record.md").write_text(
        f"# Review record\n\n- logical_document_id: `{doc['logical_document_id']}`\n"
        f"- title_and_identity: pending\n- article_boundary: pending\n- core_model: pending\n"
        f"- key_formula: pending\n- key_table_or_figure: pending\n- final_result: pending\n"
        f"- manually_verified: false\n", encoding="utf-8")


def update_global_relations_and_lineages(year: int, docs: list[dict[str, Any]], reps: list[dict[str, Any]]) -> None:
    relations = [r for r in read_jsonl(RELATIONS / "document_relations.jsonl") if int(r.get("year", 0)) != year]
    lineages = [r for r in read_jsonl(RELATIONS / "solution_lineages.jsonl") if int(r.get("contest_year", 0)) != year]
    problems = {d["problem_code"]: d for d in docs if d["document_role"] == "problem_statement" and d["problem_code"] != "unknown"}
    for rep in reps:
        relations.append({"relation_id": stable_id("relation_", rep["carrier_document_id"], "contains", rep["logical_document_id"]),
            "year": year, "source_document_id": rep["carrier_document_id"], "target_document_id": rep["logical_document_id"],
            "relation_type": "contains", "evidence": "physical representation mapping",
            "confidence": .8, "verified_by": "automatic_candidate", "status": "candidate"})
    for doc in docs:
        code = doc["problem_code"]
        if doc["document_role"] == "award_paper" and code in problems:
            relations.append({"relation_id": stable_id("relation_", doc["logical_document_id"], "answers", problems[code]["logical_document_id"]),
                "year": year, "source_document_id": doc["logical_document_id"], "target_document_id": problems[code]["logical_document_id"],
                "relation_type": "answers_problem", "evidence": "same year/problem-code candidate; content review required",
                "confidence": .55, "verified_by": "automatic_candidate", "status": "candidate"})
        if doc["document_role"] == "award_paper":
            lineages.append({"lineage_id": doc["solution_lineage_id"], "contest_year": year, "problem_code": code,
                "primary_paper": doc["logical_document_id"], "paper_representations": doc["carrier_document_ids"],
                "commentaries": [], "problem_statement": [problems[code]["logical_document_id"]] if code in problems else [],
                "validation_summaries": [], "partial_segments": [], "unresolved_members": [doc["logical_document_id"]],
                "canonical_solution_description": "pending manual model review", "status": "candidate"})
    write_jsonl(RELATIONS / "document_relations.jsonl", relations)
    write_jsonl(RELATIONS / "solution_lineages.jsonl", lineages)


def yearly_statistics(year: int, carriers: list[dict[str, Any]], docs: list[dict[str, Any]], reps: list[dict[str, Any]],
                      segments: list[dict[str, Any]], queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    def add(scope: str, metric: str, numerator: int, denominator: int, note: str = "") -> None:
        rows.append({"year": year, "counting_scope": scope, "metric": metric, "numerator": numerator,
                     "denominator": denominator, "percentage": round(100*numerator/denominator, 1) if denominator else None,
                     "note": note})
    add("carrier_document", "carrier_count", len(carriers), len(carriers))
    add("logical_document", "logical_document_count", len(docs), len(docs))
    for role in sorted(ROLES): add("logical_document", f"role:{role}", sum(d["document_role"] == role for d in docs), len(docs))
    awards = [d for d in docs if d["document_role"] == "award_paper"]
    problems = {d["problem_id"] for d in docs if d["document_role"] == "problem_statement" and d["problem_id"]}
    add("unique_award_paper", "award_paper_count", len(awards), len(awards))
    add("unique_problem", "problem_count", len(problems), len(problems))
    add("solution_lineage", "lineage_count", len(awards), len(awards), "candidate lineages pending manual deduplication")
    add("representation", "representation_count", len(reps), len(docs), "count, not a paper percentage")
    add("orphan_segment", "orphan_count", 0, len(segments), "automatic layer cannot assert absence; manual review pending")
    add("logical_document", "manual_review_queue", len(queue), len(docs))
    for feature in FEATURES:
        records = [next(r for r in d["feature_statistics"] if r["field_name"] == feature) for d in awards]
        eligible = [r for r in records if r["eligible_for_statistics"]]
        for status in ("present", "absent"):
            add("unique_award_paper", f"{feature}:{status}", sum(r["value_status"] == status for r in eligible), len(eligible), "field-specific eligible denominator")
        for status in ("unknown", "not_applicable"):
            add("unique_award_paper", f"{feature}:{status}", sum(r["value_status"] == status for r in records), len(records), "reported separately")
        add("unique_award_paper", f"{feature}:eligible_denominator", len(eligible), len(records))
    write_csv(STATISTICS / "yearly" / f"{year}_statistics.csv", rows)
    return rows


def write_year_report(year: int, stats: list[dict[str, Any]], docs: list[dict[str, Any]], queue: list[dict[str, Any]]) -> None:
    roles = Counter(d["document_role"] for d in docs)
    report = f"""# {year}年优秀论文语料候选报告

> 本报告由相同可信基线重新构建。自动结果是保守候选，不等同于人工全文核验。

## 对象构成

- logical documents：{len(docs)}
- award papers候选：{roles['award_paper']}
- expert commentaries候选：{roles['expert_commentary']}
- problem statements候选：{roles['problem_statement']}
- solution summaries候选：{roles['solution_summary']}
- unknown/other：{roles['unknown'] + roles['other_related']}

## 状态边界

- 待人工复核：{len(queue)}
- 扫描或无完整文本层的文档保持 `pending_manual_review` 或 `partially_parsed`。
- 自动未命中的字段记为 `unknown`；仅完整原生文本的字段允许进入present/absent分母。
- 合集和分卷尚未人工确认边界时，不将载体数解释为论文数。

## 模型与算法候选

模型标签与算法标签仅来自原生文本关键词，用于复核排序，不作为最终方法结论。
"""
    (REPORTS / "yearly" / f"{year}_report.md").write_text(report, encoding="utf-8")
    quality = [f"# {year}数据质量\n\n", "| logical_document_id | role | parse | evidence | segmentation | completeness |\n",
               "|---|---|---|---|---|---|\n"]
    for d in docs:
        quality.append(f"| `{d['logical_document_id']}` | {d['document_role']} | {d['parse_status']} | {d['evidence_status']} | {d['segmentation_status']} | {d['completeness_status']} |\n")
    (REPORTS / "yearly" / f"{year}_data_quality.md").write_text("".join(quality), encoding="utf-8")


def year_gate(year: int, carriers: list[dict[str, Any]], docs: list[dict[str, Any]], reps: list[dict[str, Any]],
              stats: list[dict[str, Any]], queue: list[dict[str, Any]]) -> dict[str, Any]:
    checks = {"carrier_manifest_exists": (DOCUMENTS / f"{year}_carrier_manifest.csv").exists(),
        "candidate_carriers_accounted": len(carriers) >= 0,
        "logical_document_six_pack": all(all((DOCUMENTS / "cards" / d["logical_document_id"] / name).exists()
            for name in ("document_card.md", "metadata.json", "extracted_text.md", "page_map.json", "evidence.jsonl", "review_record.md")) for d in docs),
        "roles_valid": all(d["document_role"] in ROLES for d in docs),
        "corpus_eligibility_complete": all(set(d["corpus_eligibility"]) == CORPUS_KEYS for d in docs),
        "object_layers_separate": all(d["entity_type"] == "logical_document" for d in docs),
        "one_preferred_representation": all(sum(r["preferred_representation"] for r in reps if r["logical_document_id"] == d["logical_document_id"]) == 1 for d in docs),
        "unknown_not_absent": all(not r["eligible_for_statistics"] for d in docs for r in d["feature_statistics"] if r["value_status"] == "unknown"),
        "field_status_enum": all(r["value_status"] in FIELD_STATUSES for d in docs for r in d["feature_statistics"]),
        "statistics_scoped": all(r["counting_scope"] for r in stats),
        "source_unmodified": verify_source()["original_source_modifications"] == 0}
    status = "pass" if all(checks.values()) and not queue else "conditional_pass" if all(checks.values()) else "fail"
    gate = {"year": year, "status": status, "checks": checks, "manual_review_items": len(queue),
            "note": "conditional_pass permits later years; candidate evidence is not promoted to verified", "updated_at": now()}
    write_json(QUALITY / "gates" / f"{year}_gate.json", gate)
    return gate


def update_progress(year: int, status: str) -> None:
    progress = read_json(CONTROL / "progress.json", {})
    completed = sorted(set(progress.get("completed_years", [])) | {year})
    progress.update({"source_baseline_commit": SOURCE_BASELINE, "analysis_branch": "analysis/corpus-index",
        "schema_version": SCHEMA_VERSION, "parser_version": PARSER_VERSION, "completed_years": completed,
        "year_status": {**progress.get("year_status", {}), str(year): status},
        "next_recommended_year": next((y for y in YEARS if y not in completed), None), "target_end_year": 2010,
        "remote_publish_status": "pending_phase_commit", "updated_at": now()})
    write_json(CONTROL / "progress.json", progress)


def build_summary() -> dict[str, Any]:
    rows = []
    unresolved = []
    for year in YEARS:
        path = STATISTICS / "yearly" / f"{year}_statistics.csv"
        if path.exists():
            with path.open(encoding="utf-8-sig") as fh: rows.extend(csv.DictReader(fh))
        unresolved.extend(read_jsonl(QUALITY / "unresolved" / f"{year}_manual_review_queue.jsonl"))
    write_csv(STATISTICS / "cross_year" / "1992_2010_statistics.csv", rows)
    completed = [y for y in YEARS if (CHECKPOINTS / f"{y}_checkpoint.json").exists()]
    summary = {"scope": "1992-2010", "completed_years": completed, "unresolved_items": len(unresolved),
               "conclusion_level": "descriptive_observation", "updated_at": now()}
    write_json(CHECKPOINTS / "summary_checkpoint.json", summary)
    (REPORTS / "cross_year" / "1992_2010_rebuild_and_analysis_summary.md").write_text(
        "# 1992—2010重建与分析汇总\n\n"
        f"已生成年度候选层：{completed}。跨年结论仅标记为 `descriptive_observation`；"
        "不得把收录规模、扫描质量或OCR可用性差异解释为方法趋势。\n", encoding="utf-8")
    (REPORTS / "cross_year" / "1992_2010_data_quality.md").write_text(
        f"# 1992—2010数据质量\n\n待人工复核记录：{len(unresolved)}。\n", encoding="utf-8")
    (REPORTS / "cross_year" / "1992_2010_unresolved_items.md").write_text(
        "# 未决项目\n\n" + "\n".join(f"- {r['year']} `{r['logical_document_id']}`：{r['reason']}" for r in unresolved) + "\n", encoding="utf-8")
    for name, title in (("1992_2010_model_patterns.md", "模型模式"), ("1992_2010_review_patterns.md", "评审模式"),
                        ("1992_2010_visualization_patterns.md", "可视化模式")):
        (REPORTS / "cross_year" / name).write_text(f"# {title}\n\n当前仅有自动候选；等待页面证据核验后蒸馏。\n", encoding="utf-8")
    (REPORTS / "recovery" / "disaster_recovery_report.md").write_text(
        "# 灾难恢复报告\n\n原临时工作区不可恢复。本成果依据相同源资料基线重新构建，不宣称恢复旧工作树。\n", encoding="utf-8")
    return summary


def write_schema_files() -> None:
    schema_dir = ROOT / "schema"
    schema_dir.mkdir(exist_ok=True)
    common = {"$schema": "https://json-schema.org/draft/2020-12/schema", "schema_version": SCHEMA_VERSION}
    write_json(schema_dir / "logical_document.schema.json", {**common, "type": "object",
        "required": ["logical_document_id", "carrier_document_ids", "document_role", "document_subtype",
                     "parse_status", "evidence_status", "segmentation_status", "completeness_status",
                     "feature_statistics", "analysis_eligibility"],
        "properties": {"document_role": {"enum": sorted(ROLES)}, "document_subtype": {"enum": sorted(SUBTYPES)},
            "parse_status": {"enum": sorted(PARSE_STATUSES)}, "evidence_status": {"enum": sorted(EVIDENCE_STATUSES)},
            "completeness_status": {"enum": sorted(COMPLETENESS_STATUSES)},
            "segmentation_status": {"enum": sorted(SEGMENTATION_STATUSES)}}})
    write_json(schema_dir / "feature.schema.json", {**common, "type": "object",
        "required": ["field_name", "value_status", "evidence_status", "source_pages", "source_bbox", "eligible_for_statistics"],
        "properties": {"value_status": {"enum": sorted(FIELD_STATUSES)}}})
    write_json(schema_dir / "relation.schema.json", {**common, "type": "object",
        "required": ["relation_id", "source_document_id", "target_document_id", "relation_type", "evidence", "confidence", "verified_by", "status"],
        "properties": {"relation_type": {"enum": sorted(RELATION_TYPES)}}})
    write_json(schema_dir / "representation.schema.json", {**common, "type": "object",
        "required": ["representation_id", "logical_document_id", "carrier_document_id", "preferred_representation", "preference_reason"]})
    manifest_path = CONTROL / "schema_version_manifest.json"
    previous_manifest = read_json(manifest_path, {})
    migration_timestamp = (
        previous_manifest.get("updated_at")
        if previous_manifest.get("schema_version") == SCHEMA_VERSION
        and previous_manifest.get("parser_version") == PARSER_VERSION
        else now()
    )
    write_json(manifest_path, {"schema_version": SCHEMA_VERSION, "parser_version": PARSER_VERSION,
        "compatible_from": "1.4.0", "migration": "add document_subtype and algorithm/reviewer eligibility without changing prior semantics",
        "updated_at": migration_timestamp})
    (ROOT / "schema" / "migration_notes.md").write_text(
        "# Schema migration notes\n\n## 1.4.1\n\n向后兼容增加 `document_subtype`、算法统计资格和字段级bbox。"
        "未改变carrier、segment、logical document、problem、lineage或representation的含义。\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", required=True, help="inventory, summary, all, or 1992-2010")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    ensure_dirs(); write_schema_files()
    if args.year == "inventory":
        result = build_inventory(args.resume)
        result["status"] = "reused" if args.resume and result["hashes_reused"] == result["tracked_source_files"] else "processed"
    elif args.year == "summary":
        result = build_summary(); result["status"] = "processed"
    elif args.year == "all":
        inventory = build_inventory(args.resume)
        yearly = [build_year(year, args.resume) for year in YEARS]
        result = {"inventory": inventory, "yearly": yearly, "summary": build_summary(), "status": "processed"}
    else:
        try: year = int(args.year)
        except ValueError: parser.error("--year must be inventory, summary, all, or 1992-2010")
        if year not in YEARS: parser.error("implemented years are 1992-2010")
        result = build_year(year, args.resume)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
