from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.vocabulary_service import VocabularyService
from app.schemas.vocabulary import VocabularyItemResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("", response_model=PaginatedResponse[VocabularyItemResponse])
def get_flashcards(
    year: str,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get flashcards for a year (paginated)."""
    vocab_service = VocabularyService(db)
    items, total = vocab_service.get_all(year=year, skip=skip, limit=limit)
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

