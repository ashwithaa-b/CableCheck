import os
from pathlib import Path

import psycopg
from sentence_transformers import SentenceTransformer

from app.rag.chunker import chunk_pages
from app.rag.parser import parse_pdf

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
PDF_FOLDER = Path("data/raw/polycab")
BATCH_SIZE = 32


def ingest_documents():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    pdf_files = sorted(PDF_FOLDER.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found!")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    total_stored = 0
    total_skipped = 0

    with psycopg.connect(database_url) as conn:
        for pdf_path in pdf_files:
            print(f"\nProcessing: {pdf_path.name}")

            pages = parse_pdf(str(pdf_path))
            chunks = chunk_pages(pages)

            print(f"Pages: {len(pages)}")
            print(f"Chunks: {len(chunks)}")

            # Find chunks already stored in PostgreSQL.
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT page_number, chunk_id
                    FROM document_chunks
                    WHERE document_name = %s
                      AND embedding IS NOT NULL
                    """,
                    (pdf_path.name,),
                )
                existing = set(cur.fetchall())

            pending = [chunk for chunk in chunks if (chunk["page"], chunk["chunk_id"]) not in existing]

            skipped = len(chunks) - len(pending)
            total_skipped += skipped

            print(f"Already stored: {skipped}")
            print(f"Remaining: {len(pending)}")

            for start in range(0, len(pending), BATCH_SIZE):
                batch = pending[start : start + BATCH_SIZE]

                texts = [chunk["text"] for chunk in batch]

                embeddings = model.encode(
                    texts,
                    batch_size=BATCH_SIZE,
                    show_progress_bar=False,
                    normalize_embeddings=True,
                )

                with conn.cursor() as cur:
                    for chunk, embedding in zip(batch, embeddings, strict=True):
                        vector = "[" + ",".join(str(float(value)) for value in embedding) + "]"

                        cur.execute(
                            """
                            INSERT INTO document_chunks
                            (
                                document_name,
                                page_number,
                                chunk_id,
                                content,
                                embedding
                            )
                            VALUES (%s, %s, %s, %s, %s::vector)

                            ON CONFLICT (
                                document_name,
                                page_number,
                                chunk_id
                            )
                            DO UPDATE SET
                                content = EXCLUDED.content,
                                embedding = EXCLUDED.embedding
                            """,
                            (
                                chunk["document"],
                                chunk["page"],
                                chunk["chunk_id"],
                                chunk["text"],
                                vector,
                            ),
                        )

                # Save after each batch so progress survives interruptions.
                conn.commit()

                total_stored += len(batch)

                print(f"Stored {start + len(batch)}/{len(pending)} remaining chunks for {pdf_path.name}")

    print("\n================================")
    print("INGESTION COMPLETED")
    print("================================")
    print(f"New chunks stored: {total_stored}")
    print(f"Existing chunks skipped: {total_skipped}")
    print(f"Total chunks processed: {total_stored + total_skipped}")


if __name__ == "__main__":
    ingest_documents()
