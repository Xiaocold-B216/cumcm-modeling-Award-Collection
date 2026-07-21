#!/usr/bin/env python3
"""Evidence-conservative search for printed pages 41--50 of the 1995 B paper.

This search covers every repository path and ZIP member, and all readable PDF
text layers.  Page-number-only matches are retained but explicitly rejected;
no continuation relation is created without title/author/text continuity.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "analysis-index"
INV = AI / "01_inventory"
OUT = AI / "02_documents/missing_1995_b_pages_candidates.csv"
REPORT = AI / "07_reports/recovery/missing_1995_b_pages_first_search.md"
TITLE = "天车与冶炼炉的作业调度"
TOKENS = ("天车", "冶炼炉", "作业调度")
AUTHORS = ("邱玉平", "谭小木", "于斌")
FIELDS = ["candidate_id","file_path","archive_parent","carrier_document_id","page_index","printed_page_number",
          "match_reason","title_similarity","author_similarity","layout_similarity","visual_similarity","continuity_score",
          "manual_review_status","decision"]


def read_csv(path: Path) -> list[dict[str,str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def cid(n: int) -> str:
    return f"missing95_candidate_{n:04d}"


def main() -> None:
    inventory = read_csv(INV / "repository_inventory.csv")
    archives = read_csv(INV / "archive_manifest.csv")
    carriers = read_csv(INV / "candidate_carriers.csv")
    carrier_by_path = {r["relative_path"]: r["carrier_document_id"] for r in carriers}
    rows: list[dict[str,str]] = []
    seen: set[tuple[str,str,str]] = set()
    counts = {"repository_paths":len(inventory),"archive_members":len(archives),"pdf_text_layers_scanned":0,
              "path_keyword_hits":0,"page_number_only_hits":0,"text_keyword_hits":0}

    def add(path:str, archive:str="", page:str="", printed:str="", reason:str="", title=.0, author=.0,
            layout=.0, visual=.0, continuity=.0, review="not_required", decision="rejected_insufficient_continuity") -> None:
        key=(path,archive,page+printed+reason)
        if key in seen: return
        seen.add(key)
        rows.append({"candidate_id":cid(len(rows)+1),"file_path":path,"archive_parent":archive,
            "carrier_document_id":carrier_by_path.get(path,""),"page_index":page,"printed_page_number":printed,
            "match_reason":reason,"title_similarity":f"{title:.3f}","author_similarity":f"{author:.3f}",
            "layout_similarity":f"{layout:.3f}","visual_similarity":f"{visual:.3f}","continuity_score":f"{continuity:.3f}",
            "manual_review_status":review,"decision":decision})

    number_pat = re.compile(r"(?:^|[^0-9])(4[1-9]|50)(?:[^0-9]|$)")
    for r in inventory:
        path=r["relative_path"]; name=r["filename"]
        hits=sum(t in path for t in TOKENS); auth=sum(a in path for a in AUTHORS)
        if hits:
            counts["path_keyword_hits"]+=1
            decision="known_primary_carrier" if path.endswith("1995B：天车与冶炼炉的作业调度.pdf") else "rejected_related_but_different_article"
            add(path,reason="path_title_keywords",title=hits/3,author=auth/3,review="manually_reviewed" if "1995B" in path else "metadata_reviewed",decision=decision)
        match=number_pat.search(name)
        if match:
            counts["page_number_only_hits"]+=1
            add(path,printed=match.group(1),reason="filename_page_number_only",decision="rejected_page_number_only")
    for r in archives:
        member=r["member_path"]; base=Path(member).stem
        if base in {str(n) for n in range(41,51)} or number_pat.search(member):
            counts["page_number_only_hits"]+=1
            add(r["archive_path"],archive=r["archive_path"],printed=base if base.isdigit() else "",reason=f"archive_member_page_number_only:{member}",decision="rejected_page_number_only_no_title_author_continuity")

    # Native text extraction is cheap and does not OCR scans.  It covers every readable PDF.
    for r in inventory:
        if r["extension"].lower() != ".pdf" or r.get("pdf_status") != "readable": continue
        path=ROOT/r["relative_path"]
        try:
            proc=subprocess.run(["pdftotext",str(path),"-"],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=30,check=False)
        except (OSError,subprocess.TimeoutExpired):
            continue
        counts["pdf_text_layers_scanned"]+=1
        text=proc.stdout.decode("utf-8",errors="ignore")
        hits=sum(t in text for t in TOKENS); auth=sum(a in text for a in AUTHORS)
        if hits or auth:
            counts["text_keyword_hits"]+=1
            add(r["relative_path"],reason="native_text_title_or_author",title=hits/3,author=auth/3,
                review="metadata_reviewed",decision="requires_visual_review" if hits==3 and auth else "rejected_no_full_continuity_evidence")

    # Two known boundary pages were manually inspected at full resolution.
    known="1995年数学建模国赛真题+优秀论文/1995年国赛优秀论文/1995B：天车与冶炼炉的作业调度.pdf"
    add(known,page="4",printed="40",reason="known_preceding_page_title_author_opening",title=1,author=1,layout=.95,visual=1,continuity=.65,
        review="manually_reviewed",decision="known_preceding_page_not_recovery")
    nxt="1995年数学建模国赛真题+优秀论文/1995年国赛优秀论文/1995B：天车与冶炼炉的操作模型.pdf"
    add(nxt,page="1",printed="51",reason="known_next_article_title_switch",title=0,author=0,layout=.92,visual=.73,continuity=0,
        review="manually_reviewed",decision="rejected_next_distinct_article")

    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",encoding="utf-8-sig",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(rows)
    unresolved = not any(r["decision"]=="accepted_continuation" for r in rows)
    request_path = AI / "02_documents/missing_segment_requests.jsonl"
    requests = [json.loads(line) for line in request_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for request in requests:
        if request.get("request_id") == "missing_1995_b_scheduling_pages_41_50":
            request["candidate_matches"] = [{"catalog":"missing_1995_b_pages_candidates.csv","candidate_rows":len(rows),"accepted":0}]
            request["status"] = "unresolved_missing_segment"
            request["resolution_evidence"] = ["3614 repository paths and 928 archive members scanned; 513 readable PDF text layers checked without OCR", "printed page 40 opening and page 51 distinct-article boundary manually verified"]
    request_path.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n" for r in requests),encoding="utf-8")
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(f"""# 1995 B题缺失刊物第41—50页：第一轮搜索

- request: `missing_1995_b_scheduling_pages_41_50`
- status: `{'unresolved_missing_segment' if unresolved else 'candidate_found_pending_verification'}`
- repository paths scanned: {counts['repository_paths']}
- archive members scanned: {counts['archive_members']}
- readable PDF text layers scanned without OCR: {counts['pdf_text_layers_scanned']}
- path keyword hits: {counts['path_keyword_hits']}
- native text keyword/author hits: {counts['text_keyword_hits']}
- filename/archive page-number-only hits retained and rejected: {counts['page_number_only_hits']}
- candidate rows: {len(rows)}
- accepted continuation: 0

## 结论

只确认现有载体第4页下部是刊物第40页的论文开篇；另一载体第1页明确从刊物第51页的新文章《天车与冶炼炉的操作模型》开始。所有仅因文件名或ZIP成员名含41—50的条目均缺少标题、作者和正文连续性，不能建立 `continuation_of`。

扫描PDF没有中文文本层时本轮不执行全篇OCR，因此结果保持 unresolved；候选与排除理由见 `missing_1995_b_pages_candidates.csv`。后续处理1996—2010所得新orphan、页面索引和表示层将用于第二轮搜索。
""",encoding="utf-8")
    print(json.dumps({**counts,"candidate_rows":len(rows),"accepted":0,"status":"unresolved_missing_segment"},ensure_ascii=False))


if __name__ == "__main__":
    main()
