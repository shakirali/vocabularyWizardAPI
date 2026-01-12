import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.common import UUIDType


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    vocabulary_item_id = Column(UUIDType, ForeignKey("vocabulary_items.id", ondelete="CASCADE"), nullable=False, index=True)
    year_group = Column(String(10), nullable=False, index=True)
    is_mastered = Column(Boolean, default=False, nullable=False, index=True)
    mastered_at = Column(DateTime, nullable=True)
    times_practiced = Column(Integer, default=0, nullable=False)
    last_practiced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="progress")
    vocabulary_item = relationship("VocabularyItem", back_populates="progress")

    __table_args__ = (
        UniqueConstraint('user_id', 'vocabulary_item_id', name='uq_user_progress'),
    )

