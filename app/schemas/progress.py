from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import uuid


class YearProgress(BaseModel):
    year: str
    total_words: int
    mastered_words: int
    mastered_percentage: float


class OverallProgress(BaseModel):
    total_words: int
    mastered_words: int
    mastered_percentage: float


class ProgressSummaryResponse(BaseModel):
    user_id: uuid.UUID
    year_progress: List[YearProgress]
    overall_progress: OverallProgress


class MasteredWordsResponse(BaseModel):
    year: str
    mastered_word_ids: List[uuid.UUID]


class MarkMasteredRequest(BaseModel):
    vocabulary_item_id: uuid.UUID
    year: str


class UserProgressResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    vocabulary_item_id: uuid.UUID
    year: str
    is_mastered: bool
    mastered_at: Optional[datetime]

    class Config:
        from_attributes = True


class PracticeRequest(BaseModel):
    vocabulary_item_id: uuid.UUID
    year: str
    correct: bool

