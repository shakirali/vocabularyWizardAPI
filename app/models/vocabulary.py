import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.database import Base
from app.models.common import UUIDType


def utc_now():
    """Return current UTC datetime. Used as default for SQLAlchemy columns."""
    return datetime.now(UTC)


# Use JSONB for PostgreSQL, JSON for SQLite
if "postgresql" in settings.DATABASE_URL:
    JSONType = JSONB
else:
    JSONType = JSON


class VocabularyItem(Base):
    """
    Vocabulary item representing a unique word with its definition.
    
    Words are globally unique - the same word should not appear multiple times.
    Level associations are managed through the VocabularyLevel relationship table.
    """
    __tablename__ = "vocabulary_items"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    word = Column(String(255), nullable=False, unique=True, index=True)  # Now globally unique
    meaning = Column(Text, nullable=False)
    synonyms = Column(JSONType, default=list)
    antonyms = Column(JSONType, default=list)
    example_sentences = Column(JSONType, default=list)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    progress = relationship(
        "UserProgress", back_populates="vocabulary_item", cascade="all, delete-orphan"
    )
    quiz_sentences = relationship(
        "QuizSentence", back_populates="vocabulary_item", cascade="all, delete-orphan"
    )
    vocabulary_levels = relationship(
        "VocabularyLevel", back_populates="vocabulary_item", cascade="all, delete-orphan"
    )

    @property
    def levels(self):
        """Get all levels this vocabulary item belongs to."""
        return [vl.level for vl in self.vocabulary_levels]

    @property
    def level_numbers(self):
        """Get list of level numbers (1, 2, 3, 4) this vocabulary item belongs to."""
        return sorted([vl.level.level for vl in self.vocabulary_levels])
