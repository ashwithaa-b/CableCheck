import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from google import genai
from google.genai import types

from app.config import get_settings
from app.schemas import ChatRequest

# Create the streaming router
router = APIRouter()


def generate_stream(message: str):
    """Stream Gemini AI responses."""

    settings = get_settings()

    models = [
        settings.gemini_model,
        settings.gemini_fallback_model,
    ]

    for model in models:
        response_started = False

        try:
            client = genai.Client(
                api_key=settings.gemini_api_key,
                http_options=types.HttpOptions(timeout=15000),
            )

            print(f"Streaming with model: {model}", flush=True)

            stream = client.models.generate_content_stream(
                model=model,
                contents=message,
            )

            for chunk in stream:
                if chunk.text:
                    response_started = True

                    data = {
                        "text": chunk.text,
                        "model": model,
                    }

                    yield f"data: {json.dumps(data)}\n\n"

            yield 'data: {"done": true}\n\n'
            return

        except Exception as e:
            print(
                f"Streaming error ({model}): {type(e).__name__}: {e}",
                flush=True,
            )

            if response_started:
                yield ('data: {"error": "Streaming interrupted", "done": true}\n\n')
                return

    yield ('data: {"error": "Unable to generate an AI response", "done": true}\n\n')


@router.post("/chat/stream")
def stream_chat(request: ChatRequest):
    settings = get_settings()

    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured",
        )

    return StreamingResponse(
        generate_stream(request.message),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
