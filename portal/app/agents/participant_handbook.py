"""
Participant Handbook document generation agent.
"""

from app.agents.base import BaseDocumentAgent
from app.models.document import DocumentType


class ParticipantHandbookAgent(BaseDocumentAgent):
    """
    Agent specialized in creating Participant Handbook documents.

    The Participant Handbook provides exercise participants with background
    information, their roles, and reference materials.
    """

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.PARTICIPANT_HANDBOOK

    @property
    def role_description(self) -> str:
        return """You are a training materials developer who creates engaging,
accessible content for diverse audiences. You understand how adults learn and
how to present information in ways that are easy to understand and reference.
You excel at making complex scenarios approachable."""

    @property
    def document_purpose(self) -> str:
        return "Participant Handbook"

    def get_content_guidelines(self) -> str:
        return """
Create a Participant Handbook with the following sections:

1. **Welcome & Introduction**
   - Purpose of the exercise
   - What participants will gain
   - Overview of the experience

2. **Exercise Ground Rules**
   - Participation expectations
   - Confidentiality guidelines
   - Safe space principles
   - How to engage productively

3. **Your Role**
   - Description of participant roles
   - Responsibilities during the exercise
   - How decisions will be made
   - Interaction guidelines

4. **Scenario Background**
   - Context participants need to know
   - Key facts and figures
   - Relevant policies or procedures
   - Organizational structure (if applicable)

5. **Reference Materials**
   - Glossary of key terms
   - Relevant contact information
   - Resource lists
   - Quick reference guides

6. **Decision Framework**
   - How to approach decisions
   - Factors to consider
   - Trade-offs to evaluate
   - Questions to ask

7. **Notes Section**
   - Space for participant notes
   - Guided reflection prompts
   - Key takeaways template

8. **Post-Exercise Resources**
   - Additional learning opportunities
   - Related training
   - Further reading

Write in an engaging, accessible tone. Assume participants may have varying
levels of experience with the subject matter.
"""
