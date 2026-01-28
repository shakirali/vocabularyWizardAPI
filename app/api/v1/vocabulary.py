import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_current_admin_user
from app.database import get_db
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.vocabulary import (
    VocabularyItemCreate,
    VocabularyItemResponse,
    VocabularyItemUpdate,
)
from app.services.vocabulary_service import VocabularyService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[VocabularyItemResponse])
def get_vocabulary(
    level: Optional[int] = Query(None, ge=1, le=4, description="Filter by level (1-4)"),
    search: Optional[str] = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get vocabulary items with optional filters."""
    vocab_service = VocabularyService(db)
    items, total = vocab_service.get_all(
        level=level, search=search, skip=skip, limit=limit
    )
    
    # Convert items to response format with levels
    response_items = []
    for item in items:
        level_numbers = vocab_service.vocab_repo.get_level_numbers_for_word(item.id)
        item_dict = {
            "id": item.id,
            "word": item.word,
            "meaning": item.meaning,
            "synonyms": item.synonyms or [],
            "antonyms": item.antonyms or [],
            "example_sentences": item.example_sentences or [],
            "levels": level_numbers,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }
        response_items.append(item_dict)
    
    return PaginatedResponse(items=response_items, total=total, skip=skip, limit=limit)


@router.get("/{vocabulary_id}", response_model=VocabularyItemResponse)
def get_vocabulary_item(
    vocabulary_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a specific vocabulary item by ID."""
    vocab_service = VocabularyService(db)
    item = vocab_service.get_by_id(uuid.UUID(vocabulary_id))
    
    # Get level numbers
    level_numbers = vocab_service.vocab_repo.get_level_numbers_for_word(item.id)
    
    return {
        "id": item.id,
        "word": item.word,
        "meaning": item.meaning,
        "synonyms": item.synonyms or [],
        "antonyms": item.antonyms or [],
        "example_sentences": item.example_sentences or [],
        "levels": level_numbers,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


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
    item = vocab_service.create(item_data)
    
    # Get level numbers for response
    level_numbers = vocab_service.vocab_repo.get_level_numbers_for_word(item.id)
    
    return {
        "id": item.id,
        "word": item.word,
        "meaning": item.meaning,
        "synonyms": item.synonyms or [],
        "antonyms": item.antonyms or [],
        "example_sentences": item.example_sentences or [],
        "levels": level_numbers,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


@router.put("/{vocabulary_id}", response_model=VocabularyItemResponse)
def update_vocabulary_item(
    vocabulary_id: str,
    item_data: VocabularyItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Update a vocabulary item. Requires admin privileges."""
    vocab_service = VocabularyService(db)
    item = vocab_service.update(uuid.UUID(vocabulary_id), item_data)
    
    # Get level numbers for response
    level_numbers = vocab_service.vocab_repo.get_level_numbers_for_word(item.id)
    
    return {
        "id": item.id,
        "word": item.word,
        "meaning": item.meaning,
        "synonyms": item.synonyms or [],
        "antonyms": item.antonyms or [],
        "example_sentences": item.example_sentences or [],
        "levels": level_numbers,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


@router.delete("/{vocabulary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vocabulary_item(
    vocabulary_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Delete a vocabulary item. Requires admin privileges."""
    vocab_service = VocabularyService(db)
    vocab_service.delete(uuid.UUID(vocabulary_id))
