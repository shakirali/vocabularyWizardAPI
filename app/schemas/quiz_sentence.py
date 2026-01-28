import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class QuizSentenceBase(BaseModel):
    """Base schema for quiz sentences."""
    sentence: str


class QuizSentenceCreate(QuizSentenceBase):
    """Schema for creating a quiz sentence."""
    vocabulary_item_id: uuid.UUID


class QuizSentenceResponse(QuizSentenceBase):
    """Schema for quiz sentence response."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vocabulary_item_id: uuid.UUID
    created_at: datetime


class QuizSentenceWithWord(QuizSentenceBase):
    """Schema for quiz sentence with word information."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vocabulary_item_id: uuid.UUID
    word: str
    created_at: datetime


class VocabularyQuizSentencesResponse(BaseModel):
    """Response schema for quiz sentences of a vocabulary item."""
    vocabulary_item_id: uuid.UUID
    word: str
    sentences: List[QuizSentenceResponse]
    total: int


class QuizSentenceListResponse(BaseModel):
    """Response schema for list of quiz sentences with pagination."""
    items: List[QuizSentenceWithWord]
    total: int
    skip: int
    limit: int
