#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "scripts" / "build_index.py"
if not out.exists():
    raise SystemExit("scripts/build_index.py is missing; truncated legacy payload is intentionally not used")
compile(out.read_text(encoding="utf-8"), str(out), "exec")
out.chmod(0o755)
print(f"validated tracked parser {out} ({out.stat().st_size} bytes)")
