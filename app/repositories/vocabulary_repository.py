from typing import List, Optional, Tuple

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.level import Level, VocabularyLevel
from app.models.vocabulary import VocabularyItem
from app.repositories.base import BaseRepository


class VocabularyRepository(BaseRepository[VocabularyItem]):
    """Repository for VocabularyItem operations."""

    def __init__(self, db: Session):
        super().__init__(VocabularyItem, db)

    def get_by_word(self, word: str) -> Optional[VocabularyItem]:
        """Get a vocabulary item by word (case-insensitive)."""
        return (
            self.db.query(VocabularyItem)
            .filter(func.lower(VocabularyItem.word) == func.lower(word))
            .first()
        )

    def get_by_level(
        self, level: int, skip: int = 0, limit: int = 100
    ) -> List[VocabularyItem]:
        """
        Get vocabulary items by level number (1-4).
        
        This replaces the old get_by_year method.
        """
        return (
            self.db.query(VocabularyItem)
            .join(VocabularyLevel)
            .join(Level)
            .filter(Level.level == level)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_year(
        self, year: str, skip: int = 0, limit: int = 100
    ) -> List[VocabularyItem]:
        """
        DEPRECATED: Use get_by_level instead.
        
        Get vocabulary items by old year format.
        Converts year to level: year3->1, year4->2, year5->3, year6->4
        """
        level_mapping = {
            "year3": 1,
            "year4": 2,
            "year5": 3,
            "year6": 4,
        }
        level = level_mapping.get(year.lower(), 1)
        return self.get_by_level(level, skip, limit)

    def search(
        self,
        search_term: str,
        level: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[VocabularyItem]:
        """
        Search vocabulary items by word or meaning.
        
        Optionally filter by level.
        """
        query = self.db.query(VocabularyItem).filter(
            or_(
                VocabularyItem.word.ilike(f"%{search_term}%"),
                VocabularyItem.meaning.ilike(f"%{search_term}%"),
            )
        )
        
        if level:
            query = (
                query
                .join(VocabularyLevel)
                .join(Level)
                .filter(Level.level == level)
            )
        
        return query.offset(skip).limit(limit).all()

    def get_all_with_filters(
        self,
        level: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[VocabularyItem], int]:
        """
        Get vocabulary items with optional filters.
        
        Returns tuple of (items, total_count).
        """
        query = self.db.query(VocabularyItem)

        if level:
            query = (
                query
                .join(VocabularyLevel)
                .join(Level)
                .filter(Level.level == level)
            )

        if search:
            query = query.filter(
                or_(
                    VocabularyItem.word.ilike(f"%{search}%"),
                    VocabularyItem.meaning.ilike(f"%{search}%"),
                )
            )

        total = query.count()
        items = (
            query
            .order_by(VocabularyItem.word)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total

    def get_with_levels(self, item_id) -> Optional[VocabularyItem]:
        """Get a vocabulary item with its levels eagerly loaded."""
        return (
            self.db.query(VocabularyItem)
            .options(
                joinedload(VocabularyItem.vocabulary_levels)
                .joinedload(VocabularyLevel.level)
            )
            .filter(VocabularyItem.id == item_id)
            .first()
        )

    def create_with_levels(
        self,
        word: str,
        meaning: str,
        level_ids: List,
        synonyms: List[str] = None,
        antonyms: List[str] = None,
        example_sentences: List[str] = None,
    ) -> VocabularyItem:
        """Create a vocabulary item and associate it with levels."""
        vocab_item = VocabularyItem(
            word=word,
            meaning=meaning,
            synonyms=synonyms or [],
            antonyms=antonyms or [],
            example_sentences=example_sentences or [],
        )
        self.db.add(vocab_item)
        self.db.flush()  # Get the ID without committing

        # Create level associations
        for level_id in level_ids:
            vocab_level = VocabularyLevel(
                vocabulary_item_id=vocab_item.id,
                level_id=level_id,
            )
            self.db.add(vocab_level)

        self.db.commit()
        self.db.refresh(vocab_item)
        return vocab_item

    def update_levels(
        self, vocab_item: VocabularyItem, level_ids: List
    ) -> VocabularyItem:
        """Update the level associations for a vocabulary item."""
        # Remove existing associations
        self.db.query(VocabularyLevel).filter(
            VocabularyLevel.vocabulary_item_id == vocab_item.id
        ).delete()

        # Add new associations
        for level_id in level_ids:
            vocab_level = VocabularyLevel(
                vocabulary_item_id=vocab_item.id,
                level_id=level_id,
            )
            self.db.add(vocab_level)

        self.db.commit()
        self.db.refresh(vocab_item)
        return vocab_item

    def get_level_numbers_for_word(self, vocab_item_id) -> List[int]:
        """Get the list of level numbers (1-4) for a vocabulary item."""
        levels = (
            self.db.query(Level.level)
            .join(VocabularyLevel)
            .filter(VocabularyLevel.vocabulary_item_id == vocab_item_id)
            .order_by(Level.level)
            .all()
        )
        return [level[0] for level in levels]
