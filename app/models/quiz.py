import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

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


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    vocabulary_item_id = Column(
        UUIDType, ForeignKey("vocabulary_items.id", ondelete="CASCADE"), nullable=False
    )
    prompt = Column(String(500), nullable=False)
    options = Column(JSONType, nullable=False)  # List of strings
    correct_index = Column(Integer, nullable=False)
    type = Column(String(50), default="meaning", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)


class SentenceQuestion(Base):
    __tablename__ = "sentence_questions"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    vocabulary_item_id = Column(
        UUIDType, ForeignKey("vocabulary_items.id", ondelete="CASCADE"), nullable=False
    )
    sentence_template = Column(String(500), nullable=False)
    correct_word = Column(String(255), nullable=False)
    options = Column(JSONType, nullable=False)  # List of strings
    created_at = Column(DateTime, default=utc_now, nullable=False)
