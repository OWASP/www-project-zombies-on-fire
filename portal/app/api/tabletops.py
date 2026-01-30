"""
Tabletop exercise API routes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.tabletop import Tabletop, TabletopQuestion, TabletopStatus, QuestionType, DEFAULT_QUESTIONS
from app.schemas.tabletop import (
    TabletopCreate,
    TabletopUpdate,
    TabletopResponse,
    TabletopListResponse,
    QuestionAnswer,
    TabletopQuestionResponse,
)
from app.security import get_current_user

router = APIRouter()


@router.post("/", response_model=TabletopResponse, status_code=status.HTTP_201_CREATED)
def create_tabletop(
    tabletop_data: TabletopCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new tabletop exercise.

    This initializes a tabletop with the 4 default questions that need to be answered:
    1. Overview - The game's scenario and setting
    2. Challenges - Issues and problems players must solve
    3. Twists - Unexpected events/information
    4. Conclusion - Expected resolution and outcomes
    """
    # Create the tabletop
    db_tabletop = Tabletop(
        title=tabletop_data.title,
        description=tabletop_data.description,
        story_prompt=tabletop_data.story_prompt,
        creator_id=current_user.id,
        status=TabletopStatus.DRAFT,
    )
    db.add(db_tabletop)
    db.flush()  # Get the tabletop ID

    # Create the 4 default questions
    for question_type in QuestionType:
        question = TabletopQuestion(
            tabletop_id=db_tabletop.id,
            question_type=question_type,
            question_text=DEFAULT_QUESTIONS[question_type],
        )
        db.add(question)

    db.commit()
    db.refresh(db_tabletop)

    return db_tabletop


@router.get("/", response_model=List[TabletopListResponse])
def list_tabletops(
    skip: int = 0,
    limit: int = 100,
    status_filter: TabletopStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all tabletops for the current user."""
    query = db.query(Tabletop).filter(Tabletop.creator_id == current_user.id)

    if status_filter:
        query = query.filter(Tabletop.status == status_filter)

    tabletops = query.order_by(Tabletop.created_at.desc()).offset(skip).limit(limit).all()
    return tabletops


@router.get("/{tabletop_id}", response_model=TabletopResponse)
def get_tabletop(
    tabletop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific tabletop by ID."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    return tabletop


@router.put("/{tabletop_id}", response_model=TabletopResponse)
def update_tabletop(
    tabletop_id: int,
    tabletop_data: TabletopUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a tabletop's basic information."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    update_data = tabletop_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tabletop, field, value)

    db.commit()
    db.refresh(tabletop)
    return tabletop


@router.delete("/{tabletop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tabletop(
    tabletop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a tabletop and all associated data."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    db.delete(tabletop)
    db.commit()


# Question endpoints

@router.get("/{tabletop_id}/questions", response_model=List[TabletopQuestionResponse])
def get_tabletop_questions(
    tabletop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all questions for a tabletop."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    return tabletop.questions


@router.get("/{tabletop_id}/questions/{question_type}", response_model=TabletopQuestionResponse)
def get_question(
    tabletop_id: int,
    question_type: QuestionType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific question by type."""
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    question = db.query(TabletopQuestion).filter(
        TabletopQuestion.tabletop_id == tabletop_id,
        TabletopQuestion.question_type == question_type
    ).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    return question


@router.put("/{tabletop_id}/questions/{question_type}", response_model=TabletopQuestionResponse)
def answer_question(
    tabletop_id: int,
    question_type: QuestionType,
    answer_data: QuestionAnswer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Answer a specific question for the tabletop.

    This is part of the 4-question creation flow:
    1. overview - Game scenario and setting
    2. challenges - Problems to solve
    3. twists - Unexpected events
    4. conclusion - Expected outcomes
    """
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    if answer_data.question_type != question_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question type in URL does not match request body"
        )

    question = db.query(TabletopQuestion).filter(
        TabletopQuestion.tabletop_id == tabletop_id,
        TabletopQuestion.question_type == question_type
    ).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    question.answer = answer_data.answer

    # Update tabletop status based on progress
    if tabletop.status == TabletopStatus.DRAFT:
        tabletop.status = TabletopStatus.IN_PROGRESS

    db.commit()
    db.refresh(question)

    # Check if all questions are answered
    db.refresh(tabletop)
    if tabletop.is_complete and tabletop.status != TabletopStatus.COMPLETED:
        tabletop.status = TabletopStatus.COMPLETED
        db.commit()

    return question


@router.post("/{tabletop_id}/complete", response_model=TabletopResponse)
def complete_tabletop(
    tabletop_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a tabletop as completed.

    Requires all 4 questions to be answered.
    """
    tabletop = db.query(Tabletop).filter(
        Tabletop.id == tabletop_id,
        Tabletop.creator_id == current_user.id
    ).first()

    if not tabletop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tabletop not found"
        )

    if not tabletop.is_complete:
        unanswered = [
            q.question_type.value for q in tabletop.questions
            if not q.answer
        ]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot complete tabletop. Unanswered questions: {', '.join(unanswered)}"
        )

    tabletop.status = TabletopStatus.COMPLETED
    db.commit()
    db.refresh(tabletop)

    return tabletop
