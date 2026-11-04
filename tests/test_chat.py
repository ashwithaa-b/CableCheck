from types import SimpleNamespace
from unittest.mock import MagicMock

from app import main
from app.config import Settings, get_settings


def configure_test_settings():
    """Provide a fake API key so tests never use a real key."""
    main.app.dependency_overrides[get_settings] = lambda: Settings(
        gemini_api_key="fake-test-key",
        gemini_model="gemini-3.6-flash",
        gemini_fallback_model="gemini-3.5-flash-lite",
        _env_file=None,
    )


def test_chat_without_api_key(client):
    """TEST 11: Missing Gemini API key returns 503."""

    main.app.dependency_overrides[get_settings] = lambda: Settings(
        gemini_api_key="",
        _env_file=None,
    )

    response = client.post(
        "/chat",
        json={"message": "Hello"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == ("Gemini API key is not configured")


def test_chat_success(client, monkeypatch):
    """TEST 12: Successful Gemini response."""

    configure_test_settings()

    mock_client = MagicMock()

    mock_client.models.generate_content.return_value = SimpleNamespace(text="Copper has better conductivity.")

    monkeypatch.setattr(
        main.genai,
        "Client",
        MagicMock(return_value=mock_client),
    )

    monkeypatch.setattr(
        main,
        "record_usage",
        MagicMock(),
    )

    response = client.post(
        "/chat",
        json={"message": "What is a copper cable?"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == ("Copper has better conductivity.")
    assert response.json()["model"] == "gemini-3.6-flash"

    mock_client.models.generate_content.assert_called_once()


def test_chat_fallback(client, monkeypatch):
    """TEST 13: Fallback works when primary model fails."""

    configure_test_settings()

    mock_client = MagicMock()

    mock_client.models.generate_content.side_effect = [
        RuntimeError("Primary model unavailable"),
        SimpleNamespace(text="Fallback model response"),
    ]

    monkeypatch.setattr(
        main.genai,
        "Client",
        MagicMock(return_value=mock_client),
    )

    monkeypatch.setattr(
        main,
        "record_usage",
        MagicMock(),
    )

    response = client.post(
        "/chat",
        json={"message": "Explain cable insulation"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == ("Fallback model response")
    assert response.json()["model"] == "gemini-3.5-flash-lite"

    assert mock_client.models.generate_content.call_count == 2


def test_ask_uses_fallback_model_when_primary_fails(client, monkeypatch):
    """The /ask fallback uses a supported model after a primary failure."""

    configure_test_settings()

    monkeypatch.setattr(
        main,
        "search_documents",
        MagicMock(
            return_value=[
                {
                    "document": "annual-report.pdf",
                    "page": 12,
                    "text": "The segment generated income of 100.",
                }
            ]
        ),
    )

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = [
        RuntimeError("Primary model unavailable"),
        SimpleNamespace(text="The report states income was 100. [Source 1]"),
    ]

    monkeypatch.setattr(main.genai, "Client", MagicMock(return_value=mock_client))
    monkeypatch.setattr(main, "record_usage", MagicMock())

    response = client.post("/ask", json={"question": "What income was reported?"})

    assert response.status_code == 200
    assert response.json()["model"] == "gemini-3.5-flash-lite"
    assert response.json()["citations"] == [{"document": "annual-report.pdf", "page": 12}]
    assert mock_client.models.generate_content.call_count == 2


def test_ask_includes_retrieved_segment_evidence_in_prompt(client, monkeypatch):
    """The answer-bearing annual-report passage reaches Gemini and is cited."""

    configure_test_settings()
    segment_evidence = (
        "The Company has three reportable segments as follows: "
        "Wires and Cables; Fast moving electrical goods (FMEG); "
        "Engineering, Procurement and Construction (EPC)."
    )
    monkeypatch.setattr(
        main,
        "search_documents",
        MagicMock(
            return_value=[
                {
                    "document": "polycab_fy2025_annual-report.pdf",
                    "page": 426,
                    "text": segment_evidence,
                }
            ]
        ),
    )

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = SimpleNamespace(
        text=(
            "The report identifies Wires and Cables, Fast Moving Electrical Goods "
            "(FMEG), and Engineering, Procurement and Construction (EPC) as its "
            "three reportable segments. [Source 1]"
        )
    )
    monkeypatch.setattr(main.genai, "Client", MagicMock(return_value=mock_client))
    monkeypatch.setattr(main, "record_usage", MagicMock())

    response = client.post(
        "/ask",
        json={"question": "What are Polycab India's major business segments?"},
    )

    assert response.status_code == 200
    assert segment_evidence in mock_client.models.generate_content.call_args.kwargs["contents"]
    assert response.json()["citations"] == [{"document": "polycab_fy2025_annual-report.pdf", "page": 426}]


def test_ask_prompt_distinguishes_financial_metrics_and_restated_comparatives(client, monkeypatch):
    """Financial answers must label metric, basis, and restated status."""

    configure_test_settings()
    sources = [
        {
            "document": "polycab_fy2026_annual-report.pdf",
            "page": 211,
            "text": ("(H in million). FY2025 standalone revenue from operations (Restated): 2,20,515."),
        },
        {
            "document": "polycab_fy2025_annual-report.pdf",
            "page": 367,
            "text": (
                "Standalone Statement of Profit & Loss, FY2025 (Audited): "
                "revenue from operations 219,139.52; other income 2,189.09; "
                "total income 221,328.61 (H million)."
            ),
        },
        {
            "document": "polycab_fy2025_annual-report.pdf",
            "page": 268,
            "text": (
                "Consolidated Statement of Profit & Loss, FY2025 (Audited): "
                "revenue from operations 224,083.13; other income 2,076.36; "
                "total income 226,159.49 (H million)."
            ),
        },
    ]
    monkeypatch.setattr(main, "search_documents", MagicMock(return_value=sources))

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = SimpleNamespace(
        text=(
            "FY2025 consolidated revenue from operations was ₹224,083.13 million "
            "(total income ₹226,159.49 million). The FY2025 standalone audited "
            "statement reports revenue from operations of ₹219,139.52 million "
            "(total income ₹221,328.61 million); a later FY2026 report lists "
            "₹220,515 million as the FY2025 standalone restated comparative. "
            "[Source 1] [Source 2] [Source 3]"
        )
    )
    monkeypatch.setattr(main.genai, "Client", MagicMock(return_value=mock_client))
    monkeypatch.setattr(main, "record_usage", MagicMock())

    response = client.post(
        "/ask",
        json={"question": "What was Polycab India's total revenue in FY2024-25?"},
    )

    assert response.status_code == 200
    prompt = mock_client.models.generate_content.call_args.kwargs["contents"]
    assert "Distinguish revenue from operations from total income" in prompt
    assert "whether a comparative is marked" in prompt
    assert "State materially different reported and restated figures" in prompt
    assert "Explain a restatement's cause only when the excerpts say" in prompt
    assert all(source["text"] in prompt for source in sources)
    assert response.json()["citations"] == [
        {"document": "polycab_fy2026_annual-report.pdf", "page": 211},
        {"document": "polycab_fy2025_annual-report.pdf", "page": 367},
        {"document": "polycab_fy2025_annual-report.pdf", "page": 268},
    ]


def test_ask_falls_back_when_primary_response_has_no_text(client, monkeypatch):
    """A successful but unusable primary response should not prevent fallback."""

    configure_test_settings()
    monkeypatch.setattr(
        main,
        "search_documents",
        MagicMock(
            return_value=[
                {
                    "document": "polycab_fy2025_annual-report.pdf",
                    "page": 11,
                    "text": "The company operates Wires & Cables, FMEG, and EPC businesses.",
                }
            ]
        ),
    )

    mock_client = MagicMock()
    fallback_response = SimpleNamespace(text="Polycab's major businesses are W&C, FMEG and EPC. [Source 1]")
    mock_client.models.generate_content.side_effect = [
        SimpleNamespace(text=None),
        fallback_response,
    ]
    monkeypatch.setattr(main.genai, "Client", MagicMock(return_value=mock_client))
    mock_record_usage = MagicMock()
    monkeypatch.setattr(main, "record_usage", mock_record_usage)

    response = client.post(
        "/ask",
        json={"question": "What are Polycab India's major business segments?"},
    )

    assert response.status_code == 200
    assert response.json()["model"] == "gemini-3.5-flash-lite"
    assert response.json()["citations"] == [{"document": "polycab_fy2025_annual-report.pdf", "page": 11}]
    assert mock_client.models.generate_content.call_count == 2
    mock_record_usage.assert_called_once_with(
        "gemini-3.5-flash-lite",
        fallback_response,
    )


def test_ask_does_not_call_identical_fallback_model(client, monkeypatch):
    """Do not spend a duplicate request when both model settings are equal."""

    main.app.dependency_overrides[get_settings] = lambda: Settings(
        gemini_api_key="fake-test-key",
        gemini_model="gemini-3.6-flash",
        gemini_fallback_model="gemini-3.6-flash",
        _env_file=None,
    )
    monkeypatch.setattr(
        main,
        "search_documents",
        MagicMock(
            return_value=[
                {
                    "document": "polycab_fy2025_annual-report.pdf",
                    "page": 11,
                    "text": "The company operates Wires & Cables, FMEG, and EPC businesses.",
                }
            ]
        ),
    )

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = SimpleNamespace(
        text="Polycab's major businesses are W&C, FMEG and EPC. [Source 1]"
    )
    monkeypatch.setattr(main.genai, "Client", MagicMock(return_value=mock_client))
    monkeypatch.setattr(main, "record_usage", MagicMock())

    response = client.post(
        "/ask",
        json={"question": "What are Polycab India's major business segments?"},
    )

    assert response.status_code == 200
    assert response.json()["model"] == "gemini-3.6-flash"
    mock_client.models.generate_content.assert_called_once()


def test_ask_logs_each_model_failure(client, monkeypatch, capsys):
    """A 502 should identify which configured model attempts failed in server logs."""

    configure_test_settings()
    monkeypatch.setattr(
        main,
        "search_documents",
        MagicMock(
            return_value=[
                {
                    "document": "polycab_fy2025_annual-report.pdf",
                    "page": 11,
                    "text": "The company operates Wires & Cables, FMEG, and EPC businesses.",
                }
            ]
        ),
    )

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("Service unavailable")
    monkeypatch.setattr(main.genai, "Client", MagicMock(return_value=mock_client))

    response = client.post(
        "/ask",
        json={"question": "What are Polycab India's major business segments?"},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "Unable to generate a document-grounded answer"
    assert mock_client.models.generate_content.call_count == 2
    log_output = capsys.readouterr().out
    assert "primary generation (gemini-3.6-flash) error: RuntimeError" in log_output
    assert "fallback generation (gemini-3.5-flash-lite) error: RuntimeError" in log_output


def test_chat_api_failure(client, monkeypatch):
    """TEST 14: Both Gemini models failing returns 502."""

    configure_test_settings()

    mock_client = MagicMock()

    mock_client.models.generate_content.side_effect = RuntimeError("Gemini API unavailable")

    monkeypatch.setattr(
        main.genai,
        "Client",
        MagicMock(return_value=mock_client),
    )

    response = client.post(
        "/chat",
        json={"message": "Explain cable sizing"},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == ("Unable to generate an AI response")
