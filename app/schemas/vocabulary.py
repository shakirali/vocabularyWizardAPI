import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class YearGroupInfo(BaseModel):
    value: str
    display_name: str
    short_code: str


class VocabularyItemBase(BaseModel):
    year: str
    word: str
    meaning: str
    antonyms: List[str] = []
    example_sentences: List[str] = []


class VocabularyItemCreate(VocabularyItemBase):
    pass


class VocabularyItemUpdate(BaseModel):
    year: Optional[str] = None
    word: Optional[str] = None
    meaning: Optional[str] = None
    antonyms: Optional[List[str]] = None
    example_sentences: Optional[List[str]] = None


class VocabularyItemResponse(VocabularyItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
