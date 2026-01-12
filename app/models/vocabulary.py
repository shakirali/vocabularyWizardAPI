import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, UniqueConstraint, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database import Base
from app.core.config import settings
from app.models.common import UUIDType

# Use JSONB for PostgreSQL, JSON for SQLite
if "postgresql" in settings.DATABASE_URL:
    JSONType = JSONB
else:
    JSONType = JSON


class YearGroup:
    YEAR3 = "year3"
    YEAR4 = "year4"
    YEAR5 = "year5"
    YEAR6 = "year6"

    @classmethod
    def get_display_name(cls, year: str) -> str:
        mapping = {
            cls.YEAR3: "Year 3",
            cls.YEAR4: "Year 4",
            cls.YEAR5: "Year 5",
            cls.YEAR6: "Year 6",
        }
        return mapping.get(year, year)

    @classmethod
    def get_short_code(cls, year: str) -> str:
        mapping = {
            cls.YEAR3: "Y3",
            cls.YEAR4: "Y4",
            cls.YEAR5: "Y5",
            cls.YEAR6: "Y6",
        }
        return mapping.get(year, year)

    @classmethod
    def all(cls):
        return [cls.YEAR3, cls.YEAR4, cls.YEAR5, cls.YEAR6]


class VocabularyItem(Base):
    __tablename__ = "vocabulary_items"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    year = Column(String(10), nullable=False, index=True)
    word = Column(String(255), nullable=False)
    meaning = Column(Text, nullable=False)
    antonyms = Column(JSONType, default=list)
    example_sentences = Column(JSONType, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    progress = relationship("UserProgress", back_populates="vocabulary_item", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('year', 'word', name='uq_vocabulary_year_word'),
    )

