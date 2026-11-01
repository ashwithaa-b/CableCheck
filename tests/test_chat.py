from types import SimpleNamespace
from unittest.mock import MagicMock

from app import main
from app.config import Settings, get_settings


def configure_test_settings():
    """Provide a fake API key so tests never use a real key."""
    main.app.dependency_overrides[get_settings] = lambda: Settings(
        gemini_api_key="fake-test-key",
        gemini_model="gemini-3.6-flash",
        gemini_fallback_model="gemini-3.7-flash",
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
    assert response.json()["detail"] == (
        "Gemini API key is not configured"
    )


def test_chat_success(client, monkeypatch):
    """TEST 12: Successful Gemini response."""

    configure_test_settings()

    mock_client = MagicMock()

    mock_client.models.generate_content.return_value = (
        SimpleNamespace(text="Copper has better conductivity.")
    )

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
    assert response.json()["answer"] == (
        "Copper has better conductivity."
    )
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
    assert response.json()["answer"] == (
        "Fallback model response"
    )
    assert response.json()["model"] == "gemini-3.7-flash"

    assert mock_client.models.generate_content.call_count == 2


def test_chat_api_failure(client, monkeypatch):
    """TEST 14: Both Gemini models failing returns 502."""

    configure_test_settings()

    mock_client = MagicMock()

    mock_client.models.generate_content.side_effect = (
        RuntimeError("Gemini API unavailable")
    )

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
    assert response.json()["detail"] == (
        "Unable to generate an AI response"
    )