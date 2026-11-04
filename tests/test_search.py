from unittest.mock import MagicMock

from app.rag import search


def test_search_includes_answer_two_chunks_after_match(monkeypatch):
    """Include evidence that falls two chunks after the nearest vector match."""

    document = "polycab_fy2025_annual-report.pdf"
    monkeypatch.setenv("DATABASE_URL", "postgresql://test")

    model = MagicMock()
    model.encode.return_value = [0.1, 0.2]
    monkeypatch.setattr(search, "get_embedding_model", lambda: model)

    connection = MagicMock()
    connection.__enter__.return_value = connection
    cursor = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.side_effect = [
        [(document, 426, 1, "Nearest matching chunk", 0.75)],
        [
            (document, 426, 1, "Nearest matching chunk"),
            (document, 426, 2, "Unrelated continuation"),
            (document, 426, 3, "Three reportable segments: W&C, FMEG, EPC"),
        ],
    ]
    connect = MagicMock(return_value=connection)
    monkeypatch.setattr(search.psycopg, "connect", connect)

    results = search.search_documents("What are Polycab India's major business segments?")

    assert [result["text"] for result in results] == [
        "Nearest matching chunk",
        "Unrelated continuation",
        "Three reportable segments: W&C, FMEG, EPC",
    ]
    assert cursor.execute.call_args_list[1].args[1] == (document, 426, 0, 3)
