import json
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

USAGE_FILE = Path("data/usage.jsonl")
usage_lock = Lock()


def record_usage(model: str, response) -> None:
    """Save token usage information after a Gemini API call."""

    metadata = response.usage_metadata

    if metadata is None:
        return

    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "model": model,
        "input_tokens": metadata.prompt_token_count or 0,
        "output_tokens": metadata.candidates_token_count or 0,
        "total_tokens": metadata.total_token_count or 0,
    }

    with usage_lock:
        USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

        with USAGE_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")

    print(f"Usage recorded: {record}", flush=True)


def get_usage_summary() -> dict:
    """Return the total Gemini API usage recorded so far."""

    summary = {
        "total_requests": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
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
                summary["input_tokens"] += record["input_tokens"]
                summary["output_tokens"] += record["output_tokens"]
                summary["total_tokens"] += record["total_tokens"]

    return summary