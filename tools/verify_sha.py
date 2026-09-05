import csv, hashlib
from pathlib import Path

REPO_ROOT = Path(r"D:\cumcm-modeling-Award-Collection")

def calculate_sha256(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for c in iter(lambda: f.read(8192), b""):
            h.update(c)
    return h.hexdigest().upper()

rows_2025 = []
with open(REPO_ROOT / "catalog" / "files.csv", "r", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if row.get("year") == "2025" and row.get("file_extension") == ".pdf":
            rows_2025.append(row)

print(f"Verifying {len(rows_2025)} PDFs...")
mismatch = 0
for row in rows_2025:
    fp = REPO_ROOT / row["path"]
    g1_sha = row["sha256"].upper()
    current_sha = calculate_sha256(fp)
    match = current_sha == g1_sha
    if not match:
        mismatch += 1
        print(f"MISMATCH: {row['path']}")
    else:
        print(f"OK: {row['path'][:60]}... SHA={current_sha[:16]}...")

print(f"\nFINAL_SHA_VERIFICATION: {len(rows_2025)} files checked, {mismatch} mismatches")
