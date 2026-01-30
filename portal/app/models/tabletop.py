"""
Tabletop exercise models.
"""

from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class TabletopStatus(str, PyEnum):
    """Status of a tabletop exercise."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class QuestionType(str, PyEnum):
    """Types of questions in the tabletop creation flow."""
    OVERVIEW = "overview"           # Q1: Game overview and scenario
    CHALLENGES = "challenges"       # Q2: Issues and problems to solve
    TWISTS = "twists"              # Q3: Unexpected events/information
    CONCLUSION = "conclusion"       # Q4: Expected conclusion


class Tabletop(Base):
    """Tabletop exercise model."""

    __tablename__ = "tabletops"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TabletopStatus), default=TabletopStatus.DRAFT)

    # Creator relationship
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="tabletops")

    # The initial story prompt
    story_prompt = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    questions = relationship("TabletopQuestion", back_populates="tabletop", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="tabletop", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tabletop(id={self.id}, title='{self.title}', status='{self.status}')>"

    @property
    def is_complete(self) -> bool:
        """Check if all 4 questions have been answered."""
        if not self.questions:
            return False
        answered_types = {q.question_type for q in self.questions if q.answer}
        required_types = {qt for qt in QuestionType}
        return required_types.issubset(answered_types)


class TabletopQuestion(Base):
    """Questions and answers for tabletop creation flow."""

    __tablename__ = "tabletop_questions"

    id = Column(Integer, primary_key=True, index=True)
    tabletop_id = Column(Integer, ForeignKey("tabletops.id"), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    question_text = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)

    # AI-generated content based on the answer
    ai_generated_content = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tabletop = relationship("Tabletop", back_populates="questions")

    def __repr__(self):
        return f"<TabletopQuestion(id={self.id}, type='{self.question_type}', tabletop_id={self.tabletop_id})>"


# Default questions for each type
DEFAULT_QUESTIONS = {
    QuestionType.OVERVIEW: (
        "Describe the game's overview and scenario. What is the setting, "
        "who are the main characters or factions, and what is the central narrative? "
        "Examples: A Lord of the Rings quest following elves to the boats dealing with orcs; "
        "A hospital operating without power and running out of batteries; "
        "A region facing critical infrastructure failure."
    ),
    QuestionType.CHALLENGES: (
        "What are the main issues, problems, and challenges that players will need to address? "
        "List the key decisions they'll have to make and obstacles they'll need to overcome."
    ),
    QuestionType.TWISTS: (
        "What unexpected events, information, or twists will be thrown at the players during the exercise? "
        "These should challenge their assumptions and force them to adapt their strategies."
    ),
    QuestionType.CONCLUSION: (
        "What is the expected or ideal conclusion of the game? "
        "Describe the learning outcomes, resolution scenarios, and how success should be measured."
    ),
}
