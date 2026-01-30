"""
Document schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.document import DocumentType, DocumentStatus


class DocumentCreate(BaseModel):
    """Schema for creating a document generation request."""
    document_type: DocumentType


class DocumentGenerateRequest(BaseModel):
    """Schema for batch document generation request."""
    document_types: List[DocumentType]


class DocumentResponse(BaseModel):
    """Schema for document response."""
    id: int
    tabletop_id: int
    document_type: DocumentType
    status: DocumentStatus
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    learning_goals: Optional[str] = None
    pdf_file_path: Optional[str] = None
    agent_name: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for listing documents."""
    id: int
    tabletop_id: int
    document_type: DocumentType
    status: DocumentStatus
    title: Optional[str] = None
    pdf_file_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
