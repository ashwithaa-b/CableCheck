from pathlib import Path
from datetime import date
import hashlib
import csv

raw_folder = Path("data/raw")
manifest_path = Path("data/manifest.csv")

manifest_path.parent.mkdir(parents=True, exist_ok=True)

rows = []

for pdf in sorted(raw_folder.rglob("*.pdf")):
    sha256 = hashlib.sha256(pdf.read_bytes()).hexdigest()

    rows.append([
        pdf.as_posix(),
        "https://polycab.com/investors",
        "2026-10-23",
        pdf.stat().st_size,
        sha256
    ])

with open(manifest_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "file",
        "source_url",
        "downloaded_on",
        "bytes",
        "sha256"
    ])

    writer.writerows(rows)

print("Manifest created successfully!")
print("PDF files recorded:", len(rows))