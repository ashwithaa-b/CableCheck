from pathlib import Path
from pypdf import PdfReader

folder = Path("data/raw/polycab")
total_pages = 0

for pdf in folder.glob("*.pdf"):
    reader = PdfReader(str(pdf))
    pages = len(reader.pages)

    print(pdf.name, ":", pages, "pages")
    total_pages += pages

print("-----------------------")
print("TOTAL PAGES:", total_pages)