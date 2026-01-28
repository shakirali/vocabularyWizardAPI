import uuid
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.quiz_sentence import QuizSentence
from app.models.vocabulary import VocabularyItem
from app.repositories.base import BaseRepository


class QuizSentenceRepository(BaseRepository[QuizSentence]):
    def __init__(self, db: Session):
        super().__init__(QuizSentence, db)

    def get_by_vocabulary_item_id(
        self, vocabulary_item_id: uuid.UUID
    ) -> List[QuizSentence]:
        """Get all quiz sentences for a vocabulary item."""
        return (
            self.db.query(QuizSentence)
            .filter(QuizSentence.vocabulary_item_id == vocabulary_item_id)
            .all()
        )

    def get_by_year(
        self, year: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[QuizSentence], int]:
        """Get quiz sentences for a specific year with pagination."""
        query = (
            self.db.query(QuizSentence)
            .join(VocabularyItem)
            .filter(VocabularyItem.year == year)
        )
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        
        return items, total

    def get_all_with_filters(
        self,
        year: Optional[str] = None,
        vocabulary_item_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[QuizSentence], int]:
        """Get quiz sentences with optional filters."""
        query = self.db.query(QuizSentence).join(VocabularyItem)

        if year:
            query = query.filter(VocabularyItem.year == year)

        if vocabulary_item_id:
            query = query.filter(
                QuizSentence.vocabulary_item_id == vocabulary_item_id
            )

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return items, total

    def get_random_sentences(
        self, year: str, count: int = 10
    ) -> List[QuizSentence]:
        """Get random quiz sentences for a year."""
        return (
            self.db.query(QuizSentence)
            .join(VocabularyItem)
            .filter(VocabularyItem.year == year)
            .order_by(func.random())
            .limit(count)
            .all()
        )

    def bulk_create(self, sentences: List[QuizSentence]) -> List[QuizSentence]:
        """Create multiple quiz sentences at once."""
        try:
            self.db.add_all(sentences)
            self.db.commit()
            for sentence in sentences:
                self.db.refresh(sentence)
            return sentences
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_by_vocabulary_item_id(self, vocabulary_item_id: uuid.UUID) -> int:
        """Delete all quiz sentences for a vocabulary item."""
        count = (
            self.db.query(QuizSentence)
            .filter(QuizSentence.vocabulary_item_id == vocabulary_item_id)
            .delete()
        )
        self.db.commit()
        return count
