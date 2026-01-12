import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from app.core.config import settings
from app.models.common import UUIDType

# Use JSONB for PostgreSQL, JSON for SQLite
if "postgresql" in settings.DATABASE_URL:
    JSONType = JSONB
else:
    JSONType = JSON


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    vocabulary_item_id = Column(UUIDType, ForeignKey("vocabulary_items.id", ondelete="CASCADE"), nullable=False)
    prompt = Column(String(500), nullable=False)
    options = Column(JSONType, nullable=False)  # List of strings
    correct_index = Column(Integer, nullable=False)
    type = Column(String(50), default="meaning", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SentenceQuestion(Base):
    __tablename__ = "sentence_questions"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    vocabulary_item_id = Column(UUIDType, ForeignKey("vocabulary_items.id", ondelete="CASCADE"), nullable=False)
    sentence_template = Column(String(500), nullable=False)
    correct_word = Column(String(255), nullable=False)
    options = Column(JSONType, nullable=False)  # List of strings
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

