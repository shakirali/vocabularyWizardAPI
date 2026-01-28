import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LevelInfo(BaseModel):
    """Level information for vocabulary items."""
    level: int
    name: str


class VocabularyItemBase(BaseModel):
    """Base schema for vocabulary items."""
    word: str = Field(..., description="The vocabulary word (unique)")
    meaning: str = Field(..., description="Definition of the word")
    synonyms: List[str] = Field(default=[], description="List of synonyms")
    antonyms: List[str] = Field(default=[], description="List of antonyms")
    example_sentences: List[str] = Field(default=[], description="Example sentences")


class VocabularyItemCreate(VocabularyItemBase):
    """Schema for creating a vocabulary item."""
    levels: List[int] = Field(
        ...,
        min_length=1,
        description="List of levels (1-4) this word belongs to"
    )


class VocabularyItemUpdate(BaseModel):
    """Schema for updating a vocabulary item."""
    word: Optional[str] = None
    meaning: Optional[str] = None
    synonyms: Optional[List[str]] = None
    antonyms: Optional[List[str]] = None
    example_sentences: Optional[List[str]] = None
    levels: Optional[List[int]] = Field(
        None,
        description="List of levels (1-4) to associate with this word"
    )


class VocabularyItemResponse(VocabularyItemBase):
    """Response schema for a vocabulary item."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    levels: List[int] = Field(
        default=[],
        description="List of level numbers this word belongs to"
    )
    created_at: datetime
    updated_at: datetime


class VocabularyItemWithLevelDetails(VocabularyItemBase):
    """Response schema with full level details."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    level_details: List[LevelInfo] = Field(
        default=[],
        description="Full level information"
    )
    created_at: datetime
    updated_at: datetime


class VocabularyListResponse(BaseModel):
    """Response schema for list of vocabulary items."""
    items: List[VocabularyItemResponse]
    total: int
    skip: int
    limit: int


class VocabularySearchResponse(BaseModel):
    """Response schema for vocabulary search results."""
    items: List[VocabularyItemResponse]
    total: int
    query: str
    level: Optional[int] = None
