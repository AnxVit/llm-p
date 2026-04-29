from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    system: Optional[str] = Field(None, max_length=2000)
    max_history: Optional[int] = Field(None, ge=0, le=50)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)

    model_config = {"from_attributes": True}

class ChatResponse(BaseModel):
    answer: str


class Message(BaseModel):
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}

class ChatHistory(BaseModel):
    messages: list[Message] = Field(default_factory=list)

class DeletedResponse(BaseModel):
    message: str