import uuid
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.progress import UserProgress
from app.models.vocabulary import VocabularyItem
from app.repositories.base import BaseRepository


class ProgressRepository(BaseRepository[UserProgress]):
    def __init__(self, db: Session):
        super().__init__(UserProgress, db)

    def get_by_user_and_vocabulary(
        self, user_id: uuid.UUID, vocabulary_item_id: uuid.UUID
    ) -> Optional[UserProgress]:
        return (
            self.db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.vocabulary_item_id == vocabulary_item_id,
            )
            .first()
        )

    def get_mastered_by_user_and_year(
        self, user_id: uuid.UUID, year: str
    ) -> List[UserProgress]:
        return (
            self.db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.year_group == year,
                UserProgress.is_mastered.is_(True),
            )
            .all()
        )

    def get_mastered_word_ids_by_year(
        self, user_id: uuid.UUID, year: str
    ) -> List[uuid.UUID]:
        results = (
            self.db.query(UserProgress.vocabulary_item_id)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.year_group == year,
                UserProgress.is_mastered.is_(True),
            )
            .all()
        )
        return [row[0] for row in results]

    def get_progress_stats_by_year(
        self, user_id: uuid.UUID, year: Optional[str] = None
    ) -> dict:
        query = self.db.query(
            VocabularyItem.year,
            func.count(VocabularyItem.id).label("total_words"),
            func.count(UserProgress.id)
            .filter(UserProgress.is_mastered.is_(True))
            .label("mastered_words"),
        ).outerjoin(
            UserProgress,
            (UserProgress.vocabulary_item_id == VocabularyItem.id)
            & (UserProgress.user_id == user_id),
        )

        if year:
            query = query.filter(VocabularyItem.year == year)

        query = query.group_by(VocabularyItem.year)
        results = query.all()

        year_stats = []
        total_words = 0
        total_mastered = 0

        for row in results:
            year_total = row.total_words or 0
            year_mastered = row.mastered_words or 0
            total_words += year_total
            total_mastered += year_mastered

            year_stats.append(
                {
                    "year": row.year,
                    "total_words": year_total,
                    "mastered_words": year_mastered,
                    "mastered_percentage": (
                        (year_mastered / year_total * 100) if year_total > 0 else 0.0
                    ),
                }
            )

        overall_percentage = (
            (total_mastered / total_words * 100) if total_words > 0 else 0.0
        )

        return {
            "year_progress": year_stats,
            "overall_progress": {
                "total_words": total_words,
                "mastered_words": total_mastered,
                "mastered_percentage": overall_percentage,
            },
        }
