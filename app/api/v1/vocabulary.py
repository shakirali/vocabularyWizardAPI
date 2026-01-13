import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_current_admin_user
from app.database import get_db
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.vocabulary import (VocabularyItemCreate,
                                    VocabularyItemResponse,
                                    VocabularyItemUpdate)
from app.services.vocabulary_service import VocabularyService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[VocabularyItemResponse])
def get_vocabulary(
    year: Optional[str] = None,
    search: Optional[str] = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get vocabulary items with optional filters."""
    vocab_service = VocabularyService(db)
    items, total = vocab_service.get_all(
        year=year, search=search, skip=skip, limit=limit
    )
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{vocabulary_id}", response_model=VocabularyItemResponse)
def get_vocabulary_item(
    vocabulary_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific vocabulary item by ID."""
    vocab_service = VocabularyService(db)
    return vocab_service.get_by_id(uuid.UUID(vocabulary_id))


@router.post(
    "", response_model=VocabularyItemResponse, status_code=status.HTTP_201_CREATED
)
def create_vocabulary_item(
    item_data: VocabularyItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Create a new vocabulary item. Requires admin privileges."""
    vocab_service = VocabularyService(db)
    return vocab_service.create(item_data)


@router.put("/{vocabulary_id}", response_model=VocabularyItemResponse)
def update_vocabulary_item(
    vocabulary_id: str,
    item_data: VocabularyItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Update a vocabulary item. Requires admin privileges."""
    vocab_service = VocabularyService(db)
    return vocab_service.update(uuid.UUID(vocabulary_id), item_data)


@router.delete("/{vocabulary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vocabulary_item(
    vocabulary_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Delete a vocabulary item. Requires admin privileges."""
    vocab_service = VocabularyService(db)
    vocab_service.delete(uuid.UUID(vocabulary_id))
