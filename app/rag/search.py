import os
from functools import lru_cache

import psycopg
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def search_documents(question, top_k=5):
    """
    Search document chunks using pgvector.

    For each retrieved chunk, include its immediate neighboring
    chunks from the same document and PDF page.

    Returns:
        document, page, chunk_id, text, similarity
    """

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL environment variable is not set"
        )

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # Step 1: Generate the question embedding
    model = get_embedding_model()

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    vector = "[" + ",".join(
        str(float(value)) for value in question_embedding
    ) + "]"

    matches = []
    seen = set()

    # Step 2: Retrieve the top matching chunks
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    document_name,
                    page_number,
                    chunk_id,
                    content,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM document_chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (vector, vector, top_k),
            )

            results = cur.fetchall()

            # Step 3: Include each match and its neighboring chunks
            for row in results:

                document = row[0]
                page = row[1]
                chunk_id = row[2]
                similarity = round(float(row[4]), 4)

                cur.execute(
                    """
                    SELECT
                        document_name,
                        page_number,
                        chunk_id,
                        content
                    FROM document_chunks
                    WHERE document_name = %s
                      AND page_number = %s
                      AND chunk_id BETWEEN %s AND %s
                    ORDER BY chunk_id
                    """,
                    (
                        document,
                        page,
                        max(0, chunk_id - 1),
                        chunk_id + 1,
                    ),
                )

                neighboring_chunks = cur.fetchall()

                for neighbor in neighboring_chunks:

                    key = (
                        neighbor[0],
                        neighbor[1],
                        neighbor[2],
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    matches.append({
                        "document": neighbor[0],
                        "page": neighbor[1],
                        "chunk_id": neighbor[2],
                        "text": neighbor[3],
                        "similarity": similarity,
                    })

    return matches


if __name__ == "__main__":

    question = (
        "What was Polycab India's W&C segment "
        "operating profit margin in FY2024-25?"
    )

    print("\nQuestion:", question)
    print("\nSearching annual reports...")

    results = search_documents(question, top_k=5)

    print("\nTotal retrieved chunks:", len(results))

    for index, result in enumerate(results, start=1):

        print("\n" + "=" * 50)
        print(f"RESULT {index}")
        print("=" * 50)

        print("Document:", result["document"])
        print("Page:", result["page"])
        print("Chunk ID:", result["chunk_id"])
        print("Similarity:", result["similarity"])
        print("Text:", result["text"][:500])