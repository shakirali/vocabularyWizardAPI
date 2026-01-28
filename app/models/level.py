import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.common import UUIDType


def utc_now():
    """Return current UTC datetime. Used as default for SQLAlchemy columns."""
    return datetime.now(UTC)


class Level(Base):
    """Levels for vocabulary difficulty."""
    __tablename__ = "levels"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    level = Column(Integer, unique=True, nullable=False, index=True)  # 1, 2, 3, 4
    name = Column(String(50), nullable=False)  # "Level 1", "Level 2", etc.
    description = Column(String(255), nullable=True)  # Optional description
    created_at = Column(DateTime, default=utc_now, nullable=False)

    # Relationships
    vocabulary_levels = relationship(
        "VocabularyLevel", back_populates="level", cascade="all, delete-orphan"
    )

    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4

    @classmethod
    def get_display_name(cls, level: int) -> str:
        mapping = {
            cls.LEVEL_1: "Level 1",
            cls.LEVEL_2: "Level 2",
            cls.LEVEL_3: "Level 3",
            cls.LEVEL_4: "Level 4",
        }
        return mapping.get(level, f"Level {level}")

    @classmethod
    def get_description(cls, level: int) -> str:
        mapping = {
            cls.LEVEL_1: "Beginner (Age 7-8)",
            cls.LEVEL_2: "Elementary (Age 8-9)",
            cls.LEVEL_3: "Intermediate (Age 9-10)",
            cls.LEVEL_4: "Advanced (Age 10-11)",
        }
        return mapping.get(level, "")


    @classmethod
    def all_levels(cls):
        return [cls.LEVEL_1, cls.LEVEL_2, cls.LEVEL_3, cls.LEVEL_4]


class VocabularyLevel(Base):
    """
    Association table linking vocabulary items to levels.
    
    This allows:
    - A word to be associated with multiple levels (if desired)
    - Querying vocabulary by level
    - Maintaining unique words in the vocabulary table
    """
    __tablename__ = "vocabulary_levels"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    vocabulary_item_id = Column(
        UUIDType,
        ForeignKey("vocabulary_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    level_id = Column(
        UUIDType,
        ForeignKey("levels.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime, default=utc_now, nullable=False)

    # Relationships
    vocabulary_item = relationship("VocabularyItem", back_populates="vocabulary_levels")
    level = relationship("Level", back_populates="vocabulary_levels")

    __table_args__ = (
        UniqueConstraint("vocabulary_item_id", "level_id", name="uq_vocabulary_level"),
    )
