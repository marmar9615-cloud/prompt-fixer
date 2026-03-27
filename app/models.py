from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field as PydanticField
from sqlmodel import Field, SQLModel


class PromptRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_prompt: str
    improved_prompt: str
    model_name: str
    model_output: str
    rating: int
    rank: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ImproveRequest(BaseModel):
    prompt: str = PydanticField(min_length=3)


class ImproveResponse(BaseModel):
    improved_prompt: str
    consensus_reached: bool
    agent_notes: dict[str, str]


class TestRequest(BaseModel):
    improved_prompt: str
    model: str = "gpt-4o-mini"


class TestResponse(BaseModel):
    output: str
    instruction_followed: bool
    validation_notes: str


class FeedbackRequest(BaseModel):
    original_prompt: str
    improved_prompt: str
    model_name: str
    model_output: str
    rating: int = PydanticField(ge=1, le=5)
    rank: int = PydanticField(ge=1, le=10, default=1)
