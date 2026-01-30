"""
Scenario Brief document generation agent.
"""

from app.agents.base import BaseDocumentAgent
from app.models.document import DocumentType


class ScenarioBriefAgent(BaseDocumentAgent):
    """
    Agent specialized in creating Scenario Brief documents.

    The Scenario Brief is the main document that sets the stage for the
    tabletop exercise, providing participants with the narrative context
    and initial situation.
    """

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.SCENARIO_BRIEF

    @property
    def role_description(self) -> str:
        return """You are an expert scenario designer specializing in creating
compelling tabletop exercise narratives. You excel at crafting immersive
scenarios that engage participants while clearly communicating the exercise
context and objectives. Your scenarios balance realism with educational value."""

    @property
    def document_purpose(self) -> str:
        return "Scenario Brief"

    def get_content_guidelines(self) -> str:
        return """
Create a Scenario Brief document with the following sections:

1. **Executive Summary** (2-3 paragraphs)
   - Brief overview of the scenario
   - Key stakeholders involved
   - Primary objectives

2. **Background & Context**
   - Historical context leading to the current situation
   - Relevant organizational/environmental factors
   - Key relationships and dynamics

3. **Current Situation**
   - Detailed description of the present state
   - Immediate challenges facing participants
   - Available resources and constraints

4. **Key Characters/Entities**
   - Description of major players in the scenario
   - Their roles, motivations, and relationships

5. **Timeline**
   - Key events leading to current situation
   - Critical upcoming deadlines or events

6. **Initial Intelligence**
   - Known facts and verified information
   - Unconfirmed reports or rumors
   - Gaps in knowledge

7. **Success Criteria**
   - What does success look like?
   - Key metrics or outcomes to achieve

Make the scenario engaging and realistic while ensuring it aligns with the
learning objectives of the exercise.
"""
