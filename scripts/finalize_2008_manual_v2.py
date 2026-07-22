#!/usr/bin/env python3
from pathlib import Path

source = Path(__file__).with_name("finalize_2008_manual.py")
text = source.read_text(encoding="utf-8")
old = '''    problem_paths = [
        r["relative_path"] for r in nonpdf
        if r["extension"].lower() in {".doc", ".docx", ".wps", ".rtf"}
        and ("赛题" in r["relative_path"] or problem_code(r["relative_path"]) != "unknown")
    ]'''
new = '''    problem_paths = [
        r["relative_path"] for r in nonpdf
        if r["extension"].lower() in {".doc", ".docx", ".wps", ".rtf"}
        and "data_full" not in r["relative_path"].lower()
        and ("赛题" in r["relative_path"] or problem_code(r["relative_path"]) != "unknown")
    ]'''
if old not in text:
    raise RuntimeError("2008 patch target not found")
text = text.replace(old, new, 1)
namespace = {"__name__": "__main__", "__file__": str(source)}
exec(compile(text, str(source), "exec"), namespace)
