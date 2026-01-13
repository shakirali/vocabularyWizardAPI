import uuid
from datetime import UTC, datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import VocabularyNotFoundError
from app.models.progress import UserProgress
from app.repositories.progress_repository import ProgressRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.progress import MarkMasteredRequest, PracticeRequest


class ProgressService:
    def __init__(self, db: Session):
        self.progress_repo = ProgressRepository(db)
        self.vocab_repo = VocabularyRepository(db)

    def get_progress_summary(
        self, user_id: uuid.UUID, year: Optional[str] = None
    ) -> dict:
        """Get user's progress summary."""
        return self.progress_repo.get_progress_stats_by_year(user_id, year)

    def get_mastered_word_ids(self, user_id: uuid.UUID, year: str) -> List[uuid.UUID]:
        """Get list of mastered word IDs for a year."""
        return self.progress_repo.get_mastered_word_ids_by_year(user_id, year)

    def mark_mastered(
        self, user_id: uuid.UUID, request: MarkMasteredRequest
    ) -> UserProgress:
        """Mark a word as mastered."""
        # Verify vocabulary item exists
        vocab_item = self.vocab_repo.get(str(request.vocabulary_item_id))
        if not vocab_item:
            raise VocabularyNotFoundError(str(request.vocabulary_item_id))

        # Check if progress already exists
        progress = self.progress_repo.get_by_user_and_vocabulary(
            user_id, request.vocabulary_item_id
        )

        if progress:
            # Update existing progress
            progress.is_mastered = True
            progress.mastered_at = datetime.now(UTC)
            progress.year_group = request.year
            return self.progress_repo.update(progress)
        else:
            # Create new progress
            progress = UserProgress(
                id=uuid.uuid4(),
                user_id=user_id,
                vocabulary_item_id=request.vocabulary_item_id,
                year_group=request.year,
                is_mastered=True,
                mastered_at=datetime.now(UTC),
            )
            return self.progress_repo.create(progress)

    def unmark_mastered(
        self, user_id: uuid.UUID, vocabulary_item_id: uuid.UUID, year: str
    ) -> None:
        """Unmark a word as mastered."""
        progress = self.progress_repo.get_by_user_and_vocabulary(
            user_id, vocabulary_item_id
        )
        if progress:
            progress.is_mastered = False
            progress.mastered_at = None
            self.progress_repo.update(progress)

    def record_practice(
        self, user_id: uuid.UUID, request: PracticeRequest
    ) -> UserProgress:
        """Record a practice session for a word."""
        # Verify vocabulary item exists
        vocab_item = self.vocab_repo.get(str(request.vocabulary_item_id))
        if not vocab_item:
            raise VocabularyNotFoundError(str(request.vocabulary_item_id))

        # Get or create progress
        progress = self.progress_repo.get_by_user_and_vocabulary(
            user_id, request.vocabulary_item_id
        )

        if progress:
            progress.times_practiced += 1
            progress.last_practiced_at = datetime.now(UTC)
            progress.year_group = request.year
            return self.progress_repo.update(progress)
        else:
            progress = UserProgress(
                id=uuid.uuid4(),
                user_id=user_id,
                vocabulary_item_id=request.vocabulary_item_id,
                year_group=request.year,
                times_practiced=1,
                last_practiced_at=datetime.now(UTC),
            )
            return self.progress_repo.create(progress)
