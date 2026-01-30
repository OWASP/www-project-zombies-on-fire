"""
Document generation orchestration service.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.tabletop import Tabletop
from app.models.document import Document, DocumentType, DocumentStatus
from app.agents import get_agent_for_document_type
from app.services.llm_service import LLMService, get_llm_service
from app.services.pdf_service import PDFService, get_pdf_service


class DocumentGenerationService:
    """
    Service that orchestrates document generation using specialized agents.

    Each document type is handled by a dedicated agent that knows how to
    create that specific type of content.
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        pdf_service: Optional[PDFService] = None,
    ):
        self.llm_service = llm_service or get_llm_service()
        self.pdf_service = pdf_service or get_pdf_service()

    async def generate_document(
        self,
        db: Session,
        tabletop: Tabletop,
        document_type: DocumentType,
    ) -> Document:
        """
        Generate a single document for a tabletop exercise.

        Args:
            db: Database session
            tabletop: The tabletop exercise
            document_type: Type of document to generate

        Returns:
            The generated Document record
        """
        # Check if document already exists
        existing = db.query(Document).filter(
            Document.tabletop_id == tabletop.id,
            Document.document_type == document_type,
        ).first()

        if existing:
            document = existing
            document.status = DocumentStatus.GENERATING
        else:
            document = Document(
                tabletop_id=tabletop.id,
                document_type=document_type,
                status=DocumentStatus.GENERATING,
            )
            db.add(document)

        db.commit()
        db.refresh(document)

        try:
            # Get the appropriate agent for this document type
            agent = get_agent_for_document_type(document_type)
            document.agent_name = agent.name

            # Generate content using the agent
            content = await agent.generate(tabletop, self.llm_service)

            # Update document with generated content
            document.title = content.title
            document.description = content.description
            document.content = content.content
            document.learning_goals = content.learning_goals

            # Generate PDF
            pdf_path = self.pdf_service.generate_pdf(
                title=content.title,
                description=content.description,
                content=content.content,
                learning_goals=content.learning_goals,
            )
            document.pdf_file_path = pdf_path

            # Mark as completed
            document.status = DocumentStatus.COMPLETED
            document.generated_at = datetime.utcnow()

        except Exception as e:
            document.status = DocumentStatus.FAILED
            document.error_message = str(e)

        db.commit()
        db.refresh(document)

        return document

    async def generate_all_documents(
        self,
        db: Session,
        tabletop: Tabletop,
        document_types: Optional[List[DocumentType]] = None,
    ) -> List[Document]:
        """
        Generate multiple documents for a tabletop exercise.

        Args:
            db: Database session
            tabletop: The tabletop exercise
            document_types: List of document types to generate (all if None)

        Returns:
            List of generated Document records
        """
        if document_types is None:
            document_types = list(DocumentType)

        documents = []
        for doc_type in document_types:
            document = await self.generate_document(db, tabletop, doc_type)
            documents.append(document)

        return documents

    async def regenerate_document(
        self,
        db: Session,
        document: Document,
    ) -> Document:
        """
        Regenerate an existing document.

        Args:
            db: Database session
            document: The document to regenerate

        Returns:
            The regenerated Document record
        """
        tabletop = document.tabletop
        return await self.generate_document(db, tabletop, document.document_type)


def get_document_service() -> DocumentGenerationService:
    """Get the document generation service instance."""
    return DocumentGenerationService()
