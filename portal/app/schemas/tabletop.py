"""
Tabletop schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.tabletop import TabletopStatus, QuestionType


class QuestionAnswer(BaseModel):
    """Schema for answering a tabletop question."""
    question_type: QuestionType
    answer: str = Field(..., min_length=10)


class TabletopQuestionResponse(BaseModel):
    """Schema for tabletop question response."""
    id: int
    question_type: QuestionType
    question_text: str
    answer: Optional[str] = None
    ai_generated_content: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TabletopBase(BaseModel):
    """Base tabletop schema."""
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    story_prompt: Optional[str] = None


class TabletopCreate(TabletopBase):
    """Schema for creating a new tabletop."""
    pass


class TabletopUpdate(BaseModel):
    """Schema for updating a tabletop."""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    story_prompt: Optional[str] = None
    status: Optional[TabletopStatus] = None


class TabletopResponse(TabletopBase):
    """Schema for tabletop response."""
    id: int
    status: TabletopStatus
    creator_id: int
    created_at: datetime
    updated_at: datetime
    questions: List[TabletopQuestionResponse] = []
    is_complete: bool

    class Config:
        from_attributes = True


class TabletopListResponse(BaseModel):
    """Schema for listing tabletops."""
    id: int
    title: str
    description: Optional[str] = None
    status: TabletopStatus
    creator_id: int
    created_at: datetime
    is_complete: bool

    class Config:
        from_attributes = True
