from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str
    model: str

    # --------------------------------------------------
# RAG Question Answering Models
# --------------------------------------------------

class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class Citation(BaseModel):
    document: str
    page: int


class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
    citations: list[Citation]