from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.progress_service import ProgressService
from app.schemas.progress import (
    ProgressSummaryResponse,
    MasteredWordsResponse,
    MarkMasteredRequest,
    UserProgressResponse,
    PracticeRequest
)

router = APIRouter()


@router.get("", response_model=ProgressSummaryResponse)
def get_progress(
    year: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's progress summary."""
    progress_service = ProgressService(db)
    stats = progress_service.get_progress_summary(current_user.id, year)
    return ProgressSummaryResponse(
        user_id=current_user.id,
        year_progress=stats["year_progress"],
        overall_progress=stats["overall_progress"]
    )


@router.get("/mastered", response_model=MasteredWordsResponse)
def get_mastered_words(
    year: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of mastered word IDs for a year."""
    progress_service = ProgressService(db)
    word_ids = progress_service.get_mastered_word_ids(current_user.id, year)
    return MasteredWordsResponse(year=year, mastered_word_ids=word_ids)


@router.post("/mastered", response_model=UserProgressResponse, status_code=status.HTTP_201_CREATED)
def mark_mastered(
    request: MarkMasteredRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark a word as mastered."""
    progress_service = ProgressService(db)
    progress = progress_service.mark_mastered(current_user.id, request)
    return progress


@router.delete("/mastered/{vocabulary_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def unmark_mastered(
    vocabulary_item_id: str,
    year: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Unmark a word as mastered."""
    import uuid
    progress_service = ProgressService(db)
    progress_service.unmark_mastered(current_user.id, uuid.UUID(vocabulary_item_id), year)


@router.post("/practice", status_code=status.HTTP_200_OK)
def record_practice(
    request: PracticeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Record a practice session for a word."""
    progress_service = ProgressService(db)
    progress_service.record_practice(current_user.id, request)
    return {"message": "Practice recorded"}

