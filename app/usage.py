import json
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

USAGE_FILE = Path("data/usage.jsonl")
usage_lock = Lock()

# Standard paid-tier pricing in USD per 1 million tokens.
# Gemini 3.6 Flash rates are valid through December 31, 2026.
MODEL_PRICING = {
    "gemini-3.6-flash": {
        "input": 0.75,
        "output": 3.75,
    },
}


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    thinking_tokens: int,
) -> float | None:
    """Estimate Gemini API cost in USD."""

    pricing = MODEL_PRICING.get(model)

    if pricing is None:
        return None

    billable_output_tokens = output_tokens + thinking_tokens

    cost = (input_tokens * pricing["input"] + billable_output_tokens * pricing["output"]) / 1_000_000

    return round(cost, 10)


def record_usage(model: str, response) -> None:
    """Save token usage and estimated API cost after a Gemini call."""

    metadata = response.usage_metadata

    if metadata is None:
        return

    input_tokens = metadata.prompt_token_count or 0
    output_tokens = metadata.candidates_token_count or 0
    thinking_tokens = metadata.thoughts_token_count or 0
    total_tokens = metadata.total_token_count or 0

    estimated_cost = calculate_cost(
        model,
        input_tokens,
        output_tokens,
        thinking_tokens,
    )

    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "thinking_tokens": thinking_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": estimated_cost,
    }

    with usage_lock:
        USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

        with USAGE_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")

    print(f"Usage recorded: {record}", flush=True)


def get_usage_summary() -> dict:
    """Return total Gemini API usage and estimated cost."""

    summary = {
        "total_requests": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "thinking_tokens": 0,
        "total_tokens": 0,
        "estimated_cost_usd": 0.0,
        "requests_with_unknown_cost": 0,
    }

    if not USAGE_FILE.exists():
        return summary

    with usage_lock:
        with USAGE_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                record = json.loads(line)

                summary["total_requests"] += 1
                summary["input_tokens"] += record.get("input_tokens", 0)
                summary["output_tokens"] += record.get("output_tokens", 0)
                summary["thinking_tokens"] += record.get("thinking_tokens", 0)
                summary["total_tokens"] += record.get("total_tokens", 0)

                cost = record.get("estimated_cost_usd")

                # Calculate cost for older records when possible.
                # Older records do not separately store thinking tokens,
                # so their cost estimates may be incomplete.
                if cost is None:
                    cost = calculate_cost(
                        record.get("model", ""),
                        record.get("input_tokens", 0),
                        record.get("output_tokens", 0),
                        record.get("thinking_tokens", 0),
                    )

                if cost is not None:
                    summary["estimated_cost_usd"] += cost
                else:
                    summary["requests_with_unknown_cost"] += 1

    summary["estimated_cost_usd"] = round(summary["estimated_cost_usd"], 10)

    return summary
