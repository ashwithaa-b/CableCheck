from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from google import genai
from google.genai import types

from app.config import Settings, get_settings
from app.schemas import ChatRequest, ChatResponse
from app.usage import get_usage_summary, record_usage
from app.streaming import router as streaming_router


app = FastAPI(title="CableCheck AI", version="0.1.0")

app.include_router(streaming_router)

SettingsDep = Annotated[Settings, Depends(get_settings)]


# Health check endpoint
@app.get("/health")
def health(settings: SettingsDep) -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


# Gemini API usage endpoint
@app.get("/usage")
def usage() -> dict:
    return get_usage_summary()


# AI Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, settings: SettingsDep):

    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured",
        )

    try:
        # Create Gemini client with a 15-second HTTP timeout
        client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options=types.HttpOptions(timeout=15000),
        )

        try:
            # Try primary Gemini model
            print(
                f"Trying primary model: {settings.gemini_model}",
                flush=True,
            )

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=request.message,
            )

            used_model = settings.gemini_model

        except Exception as e:
            # Show the primary model error
            print(
                f"Primary model failed: {type(e).__name__}: {e}",
                flush=True,
            )

            print(
                f"Trying fallback model: {settings.gemini_fallback_model}",
                flush=True,
            )

            # Try fallback Gemini model
            response = client.models.generate_content(
                model=settings.gemini_fallback_model,
                contents=request.message,
            )

            used_model = settings.gemini_fallback_model

        # Check Gemini response
        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response",
            )

        # Record token usage
        try:
            record_usage(used_model, response)
        except Exception as e:
            print(
                f"Usage tracking failed: {type(e).__name__}: {e}",
                flush=True,
            )

        print(
            f"Gemini response successful using: {used_model}",
            flush=True,
        )

        return ChatResponse(
            answer=response.text,
            model=used_model,
        )

    except HTTPException:
        raise

    except Exception as e:
        print(
            f"Gemini API error: {type(e).__name__}: {e}",
            flush=True,
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to generate an AI response",
        ) from None