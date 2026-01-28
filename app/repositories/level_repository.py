from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.level import Level, VocabularyLevel
from app.models.vocabulary import VocabularyItem
from app.repositories.base import BaseRepository


class LevelRepository(BaseRepository[Level]):
    """Repository for Level operations."""

    def __init__(self, db: Session):
        super().__init__(Level, db)

    def get_by_level_number(self, level: int) -> Optional[Level]:
        """Get a level by its level number (1-4)."""
        return self.db.query(Level).filter(Level.level == level).first()

    def get_all_levels(self) -> List[Level]:
        """Get all levels ordered by level number."""
        return self.db.query(Level).order_by(Level.level).all()

    def create_default_levels(self) -> List[Level]:
        """Create the default 4 levels if they don't exist."""
        levels = []
        for level_num in Level.all_levels():
            existing = self.get_by_level_number(level_num)
            if not existing:
                level = Level(
                    level=level_num,
                    name=Level.get_display_name(level_num),
                    description=Level.get_description(level_num),
                )
                self.db.add(level)
                levels.append(level)
        
        if levels:
            self.db.commit()
            for level in levels:
                self.db.refresh(level)
        
        return levels


class VocabularyLevelRepository(BaseRepository[VocabularyLevel]):
    """Repository for VocabularyLevel (word-level association) operations."""

    def __init__(self, db: Session):
        super().__init__(VocabularyLevel, db)

    def get_by_vocabulary_and_level(
        self, vocabulary_item_id, level_id
    ) -> Optional[VocabularyLevel]:
        """Get a specific vocabulary-level association."""
        return (
            self.db.query(VocabularyLevel)
            .filter(
                VocabularyLevel.vocabulary_item_id == vocabulary_item_id,
                VocabularyLevel.level_id == level_id,
            )
            .first()
        )

    def get_vocabulary_items_by_level(
        self, level_id, skip: int = 0, limit: int = 100
    ) -> List[VocabularyItem]:
        """Get all vocabulary items for a specific level."""
        return (
            self.db.query(VocabularyItem)
            .join(VocabularyLevel)
            .filter(VocabularyLevel.level_id == level_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_vocabulary_items_by_level_number(
        self, level_number: int, skip: int = 0, limit: int = 100
    ) -> List[VocabularyItem]:
        """Get all vocabulary items for a specific level number (1-4)."""
        return (
            self.db.query(VocabularyItem)
            .join(VocabularyLevel)
            .join(Level)
            .filter(Level.level == level_number)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_vocabulary_items_by_level(self, level_number: int) -> int:
        """Count vocabulary items for a specific level number."""
        return (
            self.db.query(VocabularyItem)
            .join(VocabularyLevel)
            .join(Level)
            .filter(Level.level == level_number)
            .count()
        )

    def add_word_to_level(
        self, vocabulary_item_id, level_id
    ) -> VocabularyLevel:
        """Associate a vocabulary item with a level."""
        existing = self.get_by_vocabulary_and_level(vocabulary_item_id, level_id)
        if existing:
            return existing
        
        vocab_level = VocabularyLevel(
            vocabulary_item_id=vocabulary_item_id,
            level_id=level_id,
        )
        self.db.add(vocab_level)
        self.db.commit()
        self.db.refresh(vocab_level)
        return vocab_level

    def remove_word_from_level(self, vocabulary_item_id, level_id) -> bool:
        """Remove a vocabulary item from a level."""
        result = (
            self.db.query(VocabularyLevel)
            .filter(
                VocabularyLevel.vocabulary_item_id == vocabulary_item_id,
                VocabularyLevel.level_id == level_id,
            )
            .delete()
        )
        self.db.commit()
        return result > 0

    def get_levels_for_vocabulary(self, vocabulary_item_id) -> List[Level]:
        """Get all levels associated with a vocabulary item."""
        return (
            self.db.query(Level)
            .join(VocabularyLevel)
            .filter(VocabularyLevel.vocabulary_item_id == vocabulary_item_id)
            .order_by(Level.level)
            .all()
        )
