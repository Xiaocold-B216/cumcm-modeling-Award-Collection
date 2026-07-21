#!/usr/bin/env python3
"""Normalize evidence geometry to each source PDF page's real MediaBox.

Older manual-review helpers used an A4-sized working canvas.  The reviewed
locations were also stored as normalized coordinates, so those judgments can
be preserved while correcting absolute PDF-point coordinates.  Stable entity
and segment identifiers deliberately do not change during this migration.
"""
from __future__ import annotations

import ast
import csv
import json
from pathlib import Path
from typing import Any

try:
    import fitz
except ImportError:  # pragma: no cover
    fitz = None


ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
DOCS = AI / "02_documents"
CARDS = DOCS / "cards"
CAT = AI / "05_catalogs"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _manifest(year: int) -> tuple[list[dict[str, str]], dict[str, str]]:
    path = DOCS / f"{year}_carrier_manifest.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows, {row["carrier_document_id"]: row["relative_path"] for row in rows}


def _geometry(paths: dict[str, str]) -> dict[tuple[str, int], tuple[float, float, int]]:
    if fitz is None:
        raise RuntimeError("PyMuPDF is required to normalize page geometry")
    result: dict[tuple[str, int], tuple[float, float, int]] = {}
    for carrier_id, relative_path in paths.items():
        path = ROOT / relative_path
        if path.suffix.lower() != ".pdf" or not path.exists():
            continue
        document = fitz.open(path)
        try:
            for index, page in enumerate(document):
                result[(carrier_id, index + 1)] = (float(page.rect.width), float(page.rect.height), int(page.rotation))
        finally:
            document.close()
    return result


def _norm(box: list[float], old_width: float, old_height: float) -> list[float]:
    if not box or not old_width or not old_height:
        return []
    return [box[0] / old_width, box[1] / old_height, box[2] / old_width, box[3] / old_height]


def _box(normalized: list[float], width: float, height: float) -> list[float]:
    if not normalized:
        return []
    return [round(normalized[0] * width, 4), round(normalized[1] * height, 4),
            round(normalized[2] * width, 4), round(normalized[3] * height, 4)]


def _normalized(row: dict[str, Any], box_key: str) -> list[float]:
    normalized = row.get("normalized_bbox") or []
    if len(normalized) == 4:
        return [float(x) for x in normalized]
    box = row.get(box_key) or []
    return _norm([float(x) for x in box], float(row.get("page_width") or 0), float(row.get("page_height") or 0))


def normalize_year_geometry(year: int) -> dict[str, int]:
    """Correct all persisted page/bbox geometry for one year."""
    _, paths = _manifest(year)
    actual = _geometry(paths)
    segments_path = DOCS / f"page_segments_{year}.jsonl"
    segments = _read_jsonl(segments_path)
    old_segment_geometry: dict[tuple[str, int], tuple[float, float]] = {}
    by_document_page: dict[tuple[str, int], dict[str, Any]] = {}
    for row in segments:
        key = (row["carrier_document_id"], int(row["page"]))
        if key not in actual:
            continue
        old_segment_geometry[(row["logical_document_id"], int(row["page"]))] = (
            float(row.get("page_width") or actual[key][0]), float(row.get("page_height") or actual[key][1]))
        normalized = _normalized(row, "include_bbox")
        width, height, rotation = actual[key]
        row["include_bbox"] = _box(normalized, width, height)
        row["normalized_bbox"] = [round(x, 6) for x in normalized]
        row["page_width"], row["page_height"], row["page_rotation"] = width, height, rotation
        by_document_page[(row["logical_document_id"], int(row["page"]))] = row
    _write_jsonl(segments_path, segments)

    boundaries_path = DOCS / f"article_boundaries_{year}.jsonl"
    boundaries = _read_jsonl(boundaries_path)
    for row in boundaries:
        page = int(row.get("before_page") or row.get("after_page") or 1)
        key = (row["carrier_document_id"], page)
        if key not in actual:
            continue
        width, height, rotation = actual[key]
        if row.get("same_page_boundary"):
            normalized = _normalized(row, "boundary_bbox")
            if not normalized and row.get("boundary_y") is not None:
                old_height = float(row.get("page_height") or height)
                normalized = [0.0, float(row["boundary_y"]) / old_height, 1.0, 1.0]
            row["boundary_bbox"] = _box(normalized, width, height)
            row["normalized_bbox"] = [round(x, 6) for x in normalized]
            row["boundary_y"] = round(normalized[1] * height, 4)
        row["page_width"], row["page_height"], row["page_rotation"] = width, height, rotation
    _write_jsonl(boundaries_path, boundaries)

    global_orphans_path = DOCS / "orphan_segments.jsonl"
    global_orphans = _read_jsonl(global_orphans_path)
    year_carriers = set(paths)
    for row in global_orphans:
        if row.get("carrier_document_id") not in year_carriers:
            continue
        page = int(row.get("page") or 1)
        key = (row["carrier_document_id"], page)
        if key not in actual:
            continue
        width, height, rotation = actual[key]
        normalized = _normalized(row, "bbox")
        row["bbox"] = _box(normalized, width, height)
        row["normalized_bbox"] = [round(x, 6) for x in normalized]
        row["page_width"], row["page_height"], row["page_rotation"] = width, height, rotation
    _write_jsonl(global_orphans_path, global_orphans)
    year_orphans = [row for row in global_orphans if row.get("carrier_document_id") in year_carriers]
    if (DOCS / f"orphan_segments_{year}.jsonl").exists():
        _write_jsonl(DOCS / f"orphan_segments_{year}.jsonl", year_orphans)

    documents = _read_jsonl(DOCS / f"logical_documents_{year}.jsonl")
    for document in documents:
        document_id = document["logical_document_id"]
        folder = CARDS / document_id
        page_map_path = folder / "page_map.json"
        old_map: dict[str, Any] = {}
        if page_map_path.exists():
            old_map = json.loads(page_map_path.read_text(encoding="utf-8"))
        pages = []
        for row in segments:
            if row.get("logical_document_id") != document_id:
                continue
            pages.append({"page": row["page"], "width": row["page_width"], "height": row["page_height"],
                "rotation": row["page_rotation"], "valid_bbox": row["include_bbox"],
                "excluded_bbox": row.get("exclude_bbox", []), "segment_id": row["segment_id"],
                "carrier_document_id": row["carrier_document_id"], "manually_verified": row.get("manually_verified", False)})
        if pages:
            old_map.update({"logical_document_id": document_id, "page_number_basis": "carrier local, 1-based",
                "coordinate_origin": "top-left", "coordinate_unit": "PDF point", "pages": pages})
            _write_json(page_map_path, old_map)

        evidence_path = folder / "evidence.jsonl"
        evidence = _read_jsonl(evidence_path)
        for row in evidence:
            page = int(row.get("source_page") or 1)
            segment = by_document_page.get((document_id, page))
            box = row.get("source_bbox") or []
            if not segment or len(box) != 4:
                continue
            old_width, old_height = old_segment_geometry.get((document_id, page),
                (float(segment["page_width"]), float(segment["page_height"])))
            row["source_bbox"] = _box(_norm([float(x) for x in box], old_width, old_height),
                                      float(segment["page_width"]), float(segment["page_height"]))
        _write_jsonl(evidence_path, evidence)

        metadata_path = folder / "metadata.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            for feature in metadata.get("feature_statistics", []):
                box = feature.get("source_bbox") or []
                source_pages = feature.get("source_pages") or []
                if len(box) != 4 or not source_pages:
                    continue
                page = int(source_pages[0])
                segment = by_document_page.get((document_id, page))
                if not segment:
                    continue
                old_width, old_height = old_segment_geometry.get((document_id, page),
                    (float(segment["page_width"]), float(segment["page_height"])))
                feature["source_bbox"] = _box(_norm([float(x) for x in box], old_width, old_height),
                                               float(segment["page_width"]), float(segment["page_height"]))
            _write_json(metadata_path, metadata)

    visual_path = CAT / f"visualization_catalog_{year}.csv"
    if visual_path.exists():
        with visual_path.open(encoding="utf-8-sig", newline="") as handle:
            visual_rows = list(csv.DictReader(handle))
            fieldnames = handle and list(visual_rows[0]) if visual_rows else []
        for row in visual_rows:
            segment = by_document_page.get((row.get("logical_document_id", ""), int(row.get("page") or 1)))
            if not segment:
                continue
            try:
                box = ast.literal_eval(row.get("bbox") or "[]")
            except (SyntaxError, ValueError):
                continue
            if len(box) != 4:
                continue
            old_width, old_height = old_segment_geometry.get((row["logical_document_id"], int(row["page"])),
                (float(segment["page_width"]), float(segment["page_height"])))
            row["bbox"] = json.dumps(_box(_norm([float(x) for x in box], old_width, old_height),
                                           float(segment["page_width"]), float(segment["page_height"])), separators=(",", ":"))
        if fieldnames:
            with visual_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader(); writer.writerows(visual_rows)

    return {"year": year, "segments": len(segments), "boundaries": len(boundaries),
            "orphans": len(year_orphans), "cards": len(documents)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    args = parser.parse_args()
    print(json.dumps(normalize_year_geometry(args.year), ensure_ascii=False, sort_keys=True))
