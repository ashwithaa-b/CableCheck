from app.rag.parser import parse_pdf


def chunk_pages(pages, chunk_size=1000, overlap=200):
    """
    Split PDF pages into smaller text chunks.
    Preserve document names and page numbers.
    """

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and 0 <= overlap < chunk_size")

    chunks = []

    for page in pages:
        text = page["text"]
        start = 0
        chunk_number = 1

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "document": page["document"],
                        "page": page["page"],
                        "chunk_id": chunk_number,
                        "text": chunk_text,
                    }
                )

            if end == len(text):
                break

            start = end - overlap
            chunk_number += 1

    return chunks


if __name__ == "__main__":
    pdf_path = "data/raw/polycab/polycab_fy2024_annual-report.pdf"

    pages = parse_pdf(pdf_path)
    chunks = chunk_pages(pages)

    print("Document:", pdf_path)
    print("Pages parsed:", len(pages))
    print("Total chunks:", len(chunks))

    if chunks:
        print("\nFirst chunk:")
        print("Document:", chunks[0]["document"])
        print("Page:", chunks[0]["page"])
        print("Chunk ID:", chunks[0]["chunk_id"])
        print("Text:", chunks[0]["text"][:300])
