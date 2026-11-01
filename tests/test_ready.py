from unittest.mock import MagicMock

import psycopg

from app import main


def test_ready_without_database(client, monkeypatch):
    """Return 503 when DATABASE_URL is missing."""

    monkeypatch.delenv("DATABASE_URL", raising=False)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["detail"] == "Database is not configured"


def test_ready_with_database(client, monkeypatch):
    """Return 200 when PostgreSQL responds successfully."""

    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://test:test@localhost:5432/test",
    )

    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = (
        MagicMock()
    )

    mock_connect = MagicMock(return_value=mock_connection)

    monkeypatch.setattr(main.psycopg, "connect", mock_connect)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "database": "connected",
    }

    mock_connect.assert_called_once()


def test_ready_database_failure(client, monkeypatch):
    """Return 503 when PostgreSQL cannot be reached."""

    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://test:test@localhost:5432/test",
    )

    def failed_connection(*args, **kwargs):
        raise psycopg.OperationalError("Connection refused")

    monkeypatch.setattr(
        main.psycopg,
        "connect",
        failed_connection,
    )

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["detail"] == "Database is unavailable"