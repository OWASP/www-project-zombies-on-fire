"""
After Action Review Template document generation agent.
"""

from app.agents.base import BaseDocumentAgent
from app.models.document import DocumentType


class AfterActionAgent(BaseDocumentAgent):
    """
    Agent specialized in creating After Action Review Template documents.

    The After Action Template provides a structured format for conducting
    post-exercise reviews and capturing lessons learned.
    """

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.AFTER_ACTION_TEMPLATE

    @property
    def role_description(self) -> str:
        return """You are an organizational learning expert who specializes in
extracting maximum value from training experiences. You understand how to
facilitate productive debriefs that lead to actionable improvements. You design
reflection processes that balance accountability with psychological safety."""

    @property
    def document_purpose(self) -> str:
        return "After Action Review Template"

    def get_content_guidelines(self) -> str:
        return """
Create an After Action Review (AAR) Template with the following sections:

1. **AAR Overview**
   - Purpose and importance
   - Ground rules for the debrief
   - Expected duration
   - Roles (facilitator, note-taker, participants)

2. **Exercise Summary**
   [Template section with fields for:]
   - Exercise name and date
   - Scenario summary
   - Participants
   - Duration
   - Key events timeline

3. **The Four Key Questions**
   Structure the AAR around these questions:

   **What was supposed to happen?**
   - Planned objectives
   - Expected outcomes
   - Success criteria
   - Discussion prompts for this section

   **What actually happened?**
   - Timeline of events
   - Key decisions made
   - Challenges encountered
   - Discussion prompts for this section

   **Why was there a difference?**
   - Gap analysis
   - Root cause exploration
   - Contributing factors
   - Discussion prompts for this section

   **What can we do better next time?**
   - Lessons learned
   - Actionable improvements
   - Training needs identified
   - Discussion prompts for this section

4. **Decision Analysis**
   [Template for analyzing 3-5 key decisions:]
   - Decision point description
   - Options considered
   - Decision made
   - Outcome
   - Lessons learned
   - What would we do differently?

5. **Strengths Identified**
   [Template section for:]
   - What worked well
   - Effective practices to continue
   - Individual/team highlights

6. **Areas for Improvement**
   [Template section for:]
   - Gaps identified
   - Process improvements needed
   - Skill development opportunities
   - Resource needs

7. **Action Items**
   [Template table with:]
   - Action item description
   - Owner
   - Due date
   - Priority
   - Status tracking

8. **Lessons Learned Summary**
   [Template for documenting:]
   - Key insight
   - Context
   - Recommendation
   - Applicability to real operations

9. **Participant Feedback**
   [Survey/feedback template:]
   - Exercise realism rating
   - Learning value rating
   - Facilitation quality
   - Suggestions for improvement
   - Open comments

10. **Follow-Up Plan**
    - Next steps
    - Training recommendations
    - Future exercise ideas
    - Knowledge sharing plan

Design templates that are easy to fill out and produce actionable documentation.
"""
