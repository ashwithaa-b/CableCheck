from pathlib import Path
from pypdf import PdfReader


def parse_pdf(pdf_path: str):
    """
    Extract text from a PDF while preserving
    document name and page numbers.
    """

    reader = PdfReader(pdf_path)
    document_name = Path(pdf_path).name

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        pages.append({
            "document": document_name,
            "page": page_number,
            "text": text.strip()
        })

    return pages


if __name__ == "__main__":
    pdf_path = "data/raw/polycab/polycab_fy2024_annual-report.pdf"

    pages = parse_pdf(pdf_path)

    print("Document:", Path(pdf_path).name)
    print("Total pages with text:", len(pages))

    if pages:
        print("First page:", pages[0]["page"])
        print("Sample text:", pages[0]["text"][:200])