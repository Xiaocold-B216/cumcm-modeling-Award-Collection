#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parts = sorted((ROOT / ".bootstrap").glob("build_index.part*"))
if not parts:
    raise SystemExit("No parser payload parts found")
payload = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
data = gzip.decompress(base64.b64decode(payload))
out = ROOT / "scripts" / "build_index.py"
out.write_bytes(data)
out.chmod(0o755)
print(f"restored {out} ({len(data)} bytes) from {len(parts)} part(s)")
