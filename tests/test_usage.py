import json
from types import SimpleNamespace

import pytest

import app.usage as usage
from app.usage import calculate_cost


# TEST 1: Verify API cost calculation
def test_cost_calculation():
    """Test the estimated cost for known token usage."""

    cost = calculate_cost(
        model="gemini-3.6-flash",
        input_tokens=2,
        output_tokens=9,
        thinking_tokens=144,
    )

    assert cost == pytest.approx(0.00057525)


# TEST 2: Verify zero-token cost
def test_zero_token_cost():
    """Test that zero tokens produce zero cost."""

    cost = calculate_cost(
        model="gemini-3.6-flash",
        input_tokens=0,
        output_tokens=0,
        thinking_tokens=0,
    )

    assert cost == 0.0


# TEST 3: Verify unknown model pricing
def test_unknown_model_cost():
    """Test that unknown model pricing returns None."""

    cost = calculate_cost(
        model="unknown-model",
        input_tokens=100,
        output_tokens=200,
        thinking_tokens=50,
    )

    assert cost is None


# TEST 4: Verify thinking-token cost
def test_thinking_token_cost():
    """Test that thinking tokens are included in output costs."""

    cost = calculate_cost(
        model="gemini-3.6-flash",
        input_tokens=0,
        output_tokens=0,
        thinking_tokens=1000,
    )

    assert cost == pytest.approx(0.00375)


# TEST 5: Verify usage recording
def test_record_usage(tmp_path, monkeypatch):
    """Test that Gemini token usage is saved correctly."""

    test_file = tmp_path / "usage.jsonl"

    monkeypatch.setattr(usage, "USAGE_FILE", test_file)

    metadata = SimpleNamespace(
        prompt_token_count=2,
        candidates_token_count=9,
        thoughts_token_count=144,
        total_token_count=155,
    )

    response = SimpleNamespace(usage_metadata=metadata)

    usage.record_usage("gemini-3.6-flash", response)

    assert test_file.exists()

    record = json.loads(test_file.read_text(encoding="utf-8").strip())

    assert record["model"] == "gemini-3.6-flash"
    assert record["input_tokens"] == 2
    assert record["output_tokens"] == 9
    assert record["thinking_tokens"] == 144
    assert record["total_tokens"] == 155

    assert record["estimated_cost_usd"] == pytest.approx(0.00057525)


# TEST 6: Verify usage summary
def test_usage_summary(tmp_path, monkeypatch):
    """Test that usage totals are calculated correctly."""

    test_file = tmp_path / "usage.jsonl"

    monkeypatch.setattr(usage, "USAGE_FILE", test_file)

    records = [
        {
            "model": "gemini-3.6-flash",
            "input_tokens": 10,
            "output_tokens": 20,
            "thinking_tokens": 30,
            "total_tokens": 60,
            "estimated_cost_usd": 0.000195,
        },
        {
            "model": "gemini-3.6-flash",
            "input_tokens": 5,
            "output_tokens": 10,
            "thinking_tokens": 15,
            "total_tokens": 30,
            "estimated_cost_usd": 0.0000975,
        },
    ]

    test_file.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    summary = usage.get_usage_summary()

    assert summary["total_requests"] == 2
    assert summary["input_tokens"] == 15
    assert summary["output_tokens"] == 30
    assert summary["thinking_tokens"] == 45
    assert summary["total_tokens"] == 90

    assert summary["estimated_cost_usd"] == pytest.approx(0.0002925)
