"""
Facilitator Guide document generation agent.
"""

from app.agents.base import BaseDocumentAgent
from app.models.document import DocumentType


class FacilitatorGuideAgent(BaseDocumentAgent):
    """
    Agent specialized in creating Facilitator Guide documents.

    The Facilitator Guide provides exercise leaders with all the information
    they need to effectively run the tabletop exercise.
    """

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.FACILITATOR_GUIDE

    @property
    def role_description(self) -> str:
        return """You are an experienced tabletop exercise facilitator with years
of experience running crisis simulations and training exercises. You understand
the nuances of group dynamics, pacing, and how to guide discussions productively.
You excel at anticipating challenges and providing practical guidance."""

    @property
    def document_purpose(self) -> str:
        return "Facilitator Guide"

    def get_content_guidelines(self) -> str:
        return """
Create a comprehensive Facilitator Guide with the following sections:

1. **Facilitator Overview**
   - Role and responsibilities
   - Key objectives for the facilitator
   - Prerequisites and preparation checklist

2. **Exercise Setup**
   - Room/environment requirements
   - Materials needed
   - Technology requirements
   - Participant preparation instructions

3. **Detailed Agenda**
   - Minute-by-minute timeline
   - Key transition points
   - Suggested time allocations for each phase

4. **Discussion Prompts**
   - Opening questions to set the stage
   - Probing questions for each scenario phase
   - Follow-up questions to deepen discussion
   - Redirection questions if discussion goes off-track

5. **Inject Management**
   - When to introduce each inject
   - How to present injects effectively
   - Adjusting inject timing based on group progress

6. **Facilitation Tips**
   - Managing dominant participants
   - Encouraging quiet participants
   - Handling disagreements
   - Keeping the group on track
   - Managing time effectively

7. **Troubleshooting Guide**
   - Common issues and solutions
   - Backup plans for technical problems
   - How to adapt if exercise runs long/short

8. **Assessment Notes**
   - What to observe during the exercise
   - Key decision points to track
   - Participant behaviors to note

9. **Debrief Guidelines**
   - Structure for after-action discussion
   - Key points to cover
   - Questions to prompt reflection

Provide practical, actionable guidance that helps even first-time facilitators
run the exercise successfully.
"""
