import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import VocabularyNotFoundError
from app.models.vocabulary import VocabularyItem
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.vocabulary import VocabularyItemCreate, VocabularyItemUpdate


class VocabularyService:
    def __init__(self, db: Session):
        self.vocab_repo = VocabularyRepository(db)

    def get_all(
        self,
        year: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[VocabularyItem], int]:
        """Get vocabulary items with optional filters."""
        return self.vocab_repo.get_all_with_filters(
            year=year, search=search, skip=skip, limit=limit
        )

    def get_by_id(self, vocabulary_id: uuid.UUID) -> VocabularyItem:
        """Get a vocabulary item by ID."""
        item = self.vocab_repo.get(str(vocabulary_id))
        if not item:
            raise VocabularyNotFoundError(str(vocabulary_id))
        return item

    def create(self, item_data: VocabularyItemCreate) -> VocabularyItem:
        """Create a new vocabulary item."""
        item = VocabularyItem(
            id=uuid.uuid4(),
            year=item_data.year,
            word=item_data.word,
            meaning=item_data.meaning,
            antonyms=item_data.antonyms or [],
            example_sentences=item_data.example_sentences or [],
        )
        return self.vocab_repo.create(item)

    def update(
        self, vocabulary_id: uuid.UUID, item_data: VocabularyItemUpdate
    ) -> VocabularyItem:
        """Update a vocabulary item."""
        item = self.get_by_id(vocabulary_id)

        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        return self.vocab_repo.update(item)

    def delete(self, vocabulary_id: uuid.UUID) -> None:
        """Delete a vocabulary item."""
        item = self.get_by_id(vocabulary_id)
        self.vocab_repo.delete(item)
