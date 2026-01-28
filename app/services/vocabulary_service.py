import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import VocabularyNotFoundError
from app.models.vocabulary import VocabularyItem
from app.repositories.level_repository import LevelRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.vocabulary import VocabularyItemCreate, VocabularyItemUpdate


class VocabularyService:
    def __init__(self, db: Session):
        self.vocab_repo = VocabularyRepository(db)
        self.level_repo = LevelRepository(db)

    def get_all(
        self,
        level: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[VocabularyItem], int]:
        """
        Get vocabulary items with optional filters.
        
        Args:
            level: Level number (1-4)
            search: Search term for word/meaning
            skip: Pagination offset
            limit: Pagination limit
        """
        return self.vocab_repo.get_all_with_filters(
            level=level, search=search, skip=skip, limit=limit
        )

    def get_by_id(self, vocabulary_id: uuid.UUID) -> VocabularyItem:
        """Get a vocabulary item by ID with levels."""
        item = self.vocab_repo.get_with_levels(str(vocabulary_id))
        if not item:
            raise VocabularyNotFoundError(str(vocabulary_id))
        return item

    def create(self, item_data: VocabularyItemCreate) -> VocabularyItem:
        """Create a new vocabulary item with level associations."""
        # Get level IDs from level numbers
        level_ids = []
        for level_num in item_data.levels:
            level = self.level_repo.get_by_level_number(level_num)
            if not level:
                raise ValueError(f"Level {level_num} does not exist")
            level_ids.append(level.id)
        
        # Check if word already exists
        existing = self.vocab_repo.get_by_word(item_data.word)
        if existing:
            # Update existing word and add level associations
            existing.meaning = item_data.meaning
            existing.synonyms = item_data.synonyms or []
            existing.antonyms = item_data.antonyms or []
            existing.example_sentences = item_data.example_sentences or []
            
            # Update level associations (merge with existing)
            existing_level_ids = [vl.level_id for vl in existing.vocabulary_levels]
            all_level_ids = list(set(existing_level_ids + level_ids))
            self.vocab_repo.update_levels(existing, all_level_ids)
            
            return self.vocab_repo.update(existing)
        
        # Create new vocabulary item with levels
        return self.vocab_repo.create_with_levels(
            word=item_data.word,
            meaning=item_data.meaning,
            level_ids=level_ids,
            synonyms=item_data.synonyms or [],
            antonyms=item_data.antonyms or [],
            example_sentences=item_data.example_sentences or [],
        )

    def update(
        self, vocabulary_id: uuid.UUID, item_data: VocabularyItemUpdate
    ) -> VocabularyItem:
        """Update a vocabulary item."""
        item = self.get_by_id(vocabulary_id)

        # Update basic fields
        if item_data.word is not None:
            item.word = item_data.word
        if item_data.meaning is not None:
            item.meaning = item_data.meaning
        if item_data.synonyms is not None:
            item.synonyms = item_data.synonyms
        if item_data.antonyms is not None:
            item.antonyms = item_data.antonyms
        if item_data.example_sentences is not None:
            item.example_sentences = item_data.example_sentences

        # Update level associations if provided
        if item_data.levels is not None:
            level_ids = []
            for level_num in item_data.levels:
                level = self.level_repo.get_by_level_number(level_num)
                if not level:
                    raise ValueError(f"Level {level_num} does not exist")
                level_ids.append(level.id)
            self.vocab_repo.update_levels(item, level_ids)

        return self.vocab_repo.update(item)

    def delete(self, vocabulary_id: uuid.UUID) -> None:
        """Delete a vocabulary item."""
        item = self.get_by_id(vocabulary_id)
        self.vocab_repo.delete(item)
