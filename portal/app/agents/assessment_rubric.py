"""
Assessment Rubric document generation agent.
"""

from app.agents.base import BaseDocumentAgent
from app.models.document import DocumentType


class AssessmentRubricAgent(BaseDocumentAgent):
    """
    Agent specialized in creating Assessment Rubric documents.

    The Assessment Rubric provides criteria for evaluating participant
    performance and exercise outcomes.
    """

    @property
    def document_type(self) -> DocumentType:
        return DocumentType.ASSESSMENT_RUBRIC

    @property
    def role_description(self) -> str:
        return """You are an assessment and evaluation specialist who designs
fair, comprehensive evaluation criteria. You understand competency-based
assessment and how to measure both individual and team performance. You create
rubrics that are objective, clear, and actionable."""

    @property
    def document_purpose(self) -> str:
        return "Assessment Rubric"

    def get_content_guidelines(self) -> str:
        return """
Create a comprehensive Assessment Rubric with the following sections:

1. **Assessment Overview**
   - Purpose of the assessment
   - How results will be used
   - Assessment philosophy

2. **Core Competencies Evaluated**
   For each competency, provide:
   - Competency name and description
   - Why it matters in this context
   - Observable behaviors

3. **Rubric Matrix**
   Create a detailed rubric with 4-5 performance levels:
   - Exemplary (4)
   - Proficient (3)
   - Developing (2)
   - Beginning (1)
   - Not Demonstrated (0)

   Include these assessment areas:

   **Situational Awareness**
   - Information gathering
   - Threat/opportunity identification
   - Pattern recognition

   **Decision Making**
   - Analysis quality
   - Timeliness
   - Risk consideration
   - Creativity/innovation

   **Communication**
   - Clarity
   - Appropriateness
   - Information sharing
   - Active listening

   **Collaboration**
   - Team coordination
   - Resource sharing
   - Conflict resolution
   - Leadership

   **Adaptability**
   - Response to changes
   - Flexibility
   - Learning from feedback

4. **Key Decision Points**
   - List critical decisions in the exercise
   - Optimal responses for each
   - Common mistakes to watch for
   - Scoring criteria

5. **Team Performance Metrics**
   - Collective decision quality
   - Process effectiveness
   - Time management
   - Resource utilization

6. **Individual Contribution Tracking**
   - Participation quality
   - Role fulfillment
   - Peer interaction

7. **Scoring Guide**
   - How to calculate scores
   - Weighting of different areas
   - Interpretation guidelines

8. **Observation Checklist**
   - Specific behaviors to look for
   - Timestamps for key decisions
   - Notes sections

Make the rubric practical and usable during a live exercise.
"""
