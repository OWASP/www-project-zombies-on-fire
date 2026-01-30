"""
Document generation agents package.

Each document type has its own specialized agent that handles:
1. Generating a description of the document
2. Creating the main content
3. Defining learning goals
4. Producing the final output
"""

from app.agents.base import BaseDocumentAgent
from app.agents.scenario_brief import ScenarioBriefAgent
from app.agents.facilitator_guide import FacilitatorGuideAgent
from app.agents.participant_handbook import ParticipantHandbookAgent
from app.agents.inject_cards import InjectCardsAgent
from app.agents.assessment_rubric import AssessmentRubricAgent
from app.agents.after_action import AfterActionAgent
from app.models.document import DocumentType

# Agent registry - maps document types to their specialized agents
AGENT_REGISTRY = {
    DocumentType.SCENARIO_BRIEF: ScenarioBriefAgent,
    DocumentType.FACILITATOR_GUIDE: FacilitatorGuideAgent,
    DocumentType.PARTICIPANT_HANDBOOK: ParticipantHandbookAgent,
    DocumentType.INJECT_CARDS: InjectCardsAgent,
    DocumentType.ASSESSMENT_RUBRIC: AssessmentRubricAgent,
    DocumentType.AFTER_ACTION_TEMPLATE: AfterActionAgent,
}


def get_agent_for_document_type(document_type: DocumentType) -> BaseDocumentAgent:
    """Get the appropriate agent for a document type."""
    agent_class = AGENT_REGISTRY.get(document_type)
    if not agent_class:
        raise ValueError(f"No agent registered for document type: {document_type}")
    return agent_class()


__all__ = [
    "BaseDocumentAgent",
    "ScenarioBriefAgent",
    "FacilitatorGuideAgent",
    "ParticipantHandbookAgent",
    "InjectCardsAgent",
    "AssessmentRubricAgent",
    "AfterActionAgent",
    "AGENT_REGISTRY",
    "get_agent_for_document_type",
]
