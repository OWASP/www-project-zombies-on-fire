"""
Document generation API routes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.tabletop import Tabletop
from app.models.document import Document, DocumentType, DocumentStatus
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse,
    DocumentGenerateRequest,
)
from app.security import get_current_user
from app.services.document_service import DocumentGenerationService

router = APIRouter()


async def generate_document_task(
    db_url: str,
    tabletop_id: int,
    document_type: DocumentType,
):
    """Background task for document generation."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        tabletop = db.query(Tabletop).filter(Tabletop.id == tabletop_id).first()
        if tabletop:
            service = DocumentGenerationService()
            await service.generate_document(db, tabletop, document_type)
    finally:
        db.close()


@router.get("/types", response_model=List[dict])
def list_document_types(current_user: User = Depends(get_current_user)):
    """List all available document types."""
    from app.models.document import DOCUMENT_TYPE_INFO

    return [
        {
            "type": doc_type.value,
            "name": info["name"],
            "description": info["description"],
        }
        for doc_type, info in DOCUMENT_TYPE_INFO.items()
    ]


@router.get("/tabletop/{tabletop_id}", response_model=List[DocumentListResponse])
def list_tabletop_documents(
    tabletop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all documents for a tabletop."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    return tabletop.documents


@router.post("/tabletop/{tabletop_id}/generate", response_model=List[DocumentResponse])
async def generate_documents(
    tabletop_id: int,
    request: DocumentGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate documents for a tabletop exercise.

    Each document type is handled by a specialized agent:
    - scenario_brief: Creates the main scenario overview
    - facilitator_guide: Creates guide for exercise facilitators
    - participant_handbook: Creates materials for participants
    - inject_cards: Creates unexpected event cards
    - assessment_rubric: Creates evaluation criteria
    - after_action_template: Creates post-exercise review template
    """
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    if not tabletop.is_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot generate documents until all questions are answered"
        )

    service = DocumentGenerationService()
    documents = await service.generate_all_documents(
        db, tabletop, request.document_types
    )

    return documents


@router.post("/tabletop/{tabletop_id}/generate/{document_type}", response_model=DocumentResponse)
async def generate_single_document(
    tabletop_id: int,
    document_type: DocumentType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a single document type for a tabletop."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    if not tabletop.is_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot generate documents until all questions are answered"
        )

    service = DocumentGenerationService()
    document = await service.generate_document(db, tabletop, document_type)

    return document


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific document by ID."""
    document = db.query(Document).join(Tabletop).filter(
        Document.id == document_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document


@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download the PDF file for a document."""
    document = db.query(Document).join(Tabletop).filter(
        Document.id == document_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    if not document.pdf_file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF file not available"
        )

    return FileResponse(
        document.pdf_file_path,
        media_type="application/pdf",
        filename=f"{document.title}.pdf" if document.title else "document.pdf",
    )


@router.post("/{document_id}/regenerate", response_model=DocumentResponse)
async def regenerate_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Regenerate a document with updated content."""
    document = db.query(Document).join(Tabletop).filter(
        Document.id == document_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    service = DocumentGenerationService()
    updated_document = await service.regenerate_document(db, document)

    return updated_document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a document."""
    document = db.query(Document).join(Tabletop).filter(
        Document.id == document_id,
        Tabletop.creator_id == current_user.id,
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Delete PDF file if exists
    if document.pdf_file_path:
        import os
        if os.path.exists(document.pdf_file_path):
            os.remove(document.pdf_file_path)

    db.delete(document)
    db.commit()
