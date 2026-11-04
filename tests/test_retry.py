from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app import main


def test_retry_succeeds_after_temporary_failures(monkeypatch):
    """Gemini succeeds after two temporary failures."""

    mock_client = MagicMock()

    expected_response = SimpleNamespace(text="CableCheck response")

    mock_client.models.generate_content.side_effect = [
        TimeoutError("Temporary timeout"),
        TimeoutError("Temporary timeout"),
        expected_response,
    ]

    mock_sleep = MagicMock()
    monkeypatch.setattr(main.time, "sleep", mock_sleep)
    monkeypatch.setattr(main.random, "uniform", lambda a, b: 0.25)

    response = main.generate_with_retry(
        mock_client,
        "gemini-3.6-flash",
        "Explain EHV cables",
    )

    assert response.text == "CableCheck response"
    assert mock_client.models.generate_content.call_count == 3

    assert mock_sleep.call_count == 2
    assert mock_sleep.call_args_list[0].args[0] == 1.25
    assert mock_sleep.call_args_list[1].args[0] == 2.25


def test_permanent_error_does_not_retry(monkeypatch):
    """Permanent errors should fail immediately."""

    mock_client = MagicMock()

    mock_client.models.generate_content.side_effect = RuntimeError("Invalid request")

    mock_sleep = MagicMock()
    monkeypatch.setattr(main.time, "sleep", mock_sleep)

    with pytest.raises(RuntimeError, match="Invalid request"):
        main.generate_with_retry(
            mock_client,
            "gemini-3.6-flash",
            "Explain cable insulation",
        )

    assert mock_client.models.generate_content.call_count == 1
    mock_sleep.assert_not_called()


def test_retry_stops_after_max_attempts(monkeypatch):
    """Temporary failures should stop after three attempts."""

    mock_client = MagicMock()

    mock_client.models.generate_content.side_effect = TimeoutError("Service unavailable")

    mock_sleep = MagicMock()
    monkeypatch.setattr(main.time, "sleep", mock_sleep)
    monkeypatch.setattr(main.random, "uniform", lambda a, b: 0.0)

    with pytest.raises(TimeoutError, match="Service unavailable"):
        main.generate_with_retry(
            mock_client,
            "gemini-3.6-flash",
            "Explain cable sizing",
        )

    assert mock_client.models.generate_content.call_count == 3
    assert mock_sleep.call_count == 2
