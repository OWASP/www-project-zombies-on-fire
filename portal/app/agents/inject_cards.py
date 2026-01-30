"""
Inject Cards document generation agent.
"""

from app.agents.base import BaseDocumentAgent
from app.models.document import DocumentType


class InjectCardsAgent(BaseDocumentAgent):
    """
    Agent specialized in creating Inject Cards documents.

    Inject Cards contain the unexpected events and information that are
    introduced during the exercise to challenge participants.
    """

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.INJECT_CARDS

    @property
    def role_description(self) -> str:
        return """You are a creative scenario writer who specializes in plot
twists, complications, and unexpected developments. You understand how to create
tension and challenge assumptions while keeping scenarios realistic and
educational. You excel at timing surprises for maximum impact."""

    @property
    def document_purpose(self) -> str:
        return "Inject Cards"

    def get_content_guidelines(self) -> str:
        return """
Create a set of 8-12 Inject Cards. Each inject should be formatted as follows:

---
## INJECT #[Number]: [Brief Title]

**Timing:** [When to introduce - early/mid/late exercise, or specific trigger]

**Type:** [Information | Event | Complication | Resource Change | External Factor]

**Delivery Method:** [How facilitator presents: verbal announcement, written memo, phone call simulation, news report, etc.]

### The Inject
[2-3 paragraphs describing the new information or event in detail. Write as if this is being delivered to participants in real-time.]

### Facilitator Notes
- Expected participant reactions
- Key discussion points this should raise
- Potential follow-up questions
- How this connects to learning objectives

### Escalation Options
- Mild version (if group is struggling)
- Severe version (if group needs more challenge)
---

Create a mix of inject types:
- 2-3 information reveals (new intelligence, reports, data)
- 2-3 unexpected events (incidents, developments)
- 2-3 resource changes (constraints, new capabilities)
- 2-3 external pressures (media, stakeholders, time)

Ensure injects:
- Build on each other where appropriate
- Create meaningful decisions
- Align with the twists outlined in the scenario
- Have realistic timing and delivery methods
- Challenge different aspects of participant decision-making
"""
