import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.common import UUIDType


def utc_now():
    """Return current UTC datetime. Used as default for SQLAlchemy columns."""
    return datetime.now(UTC)


class QuizSentence(Base):
    """
    Pre-generated fill-in-the-blank quiz sentences for vocabulary items.
    Each vocabulary word has 10 associated quiz sentences.
    """
    __tablename__ = "quiz_sentences"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    vocabulary_item_id = Column(
        UUIDType,
        ForeignKey("vocabulary_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    sentence = Column(Text, nullable=False)  # Sentence with _____ blank placeholder
    created_at = Column(DateTime, default=utc_now, nullable=False)

    # Relationships
    vocabulary_item = relationship("VocabularyItem", back_populates="quiz_sentences")
