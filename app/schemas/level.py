import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LevelBase(BaseModel):
    """Base schema for levels."""
    level: int = Field(..., ge=1, le=4, description="Level number (1-4)")
    name: str = Field(..., description="Display name (e.g., 'Level 1')")
    description: Optional[str] = Field(None, description="Level description")


class LevelCreate(LevelBase):
    """Schema for creating a level."""
    pass


class LevelResponse(LevelBase):
    """Schema for level response."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class LevelInfo(BaseModel):
    """Simplified level info for vocabulary responses."""
    level: int
    name: str


class LevelListResponse(BaseModel):
    """Response schema for list of levels."""
    items: List[LevelResponse]
    total: int


# Level mapping information
class LevelMapping(BaseModel):
    """Mapping between old year system and new level system."""
    level: int
    name: str
    description: str
    old_year: str
    old_year_display: str

    @classmethod
    def get_all_mappings(cls) -> List["LevelMapping"]:
        return [
            cls(
                level=1,
                name="Level 1",
                description="Beginner (Age 7-8)",
                old_year="year3",
                old_year_display="Year 3"
            ),
            cls(
                level=2,
                name="Level 2",
                description="Elementary (Age 8-9)",
                old_year="year4",
                old_year_display="Year 4"
            ),
            cls(
                level=3,
                name="Level 3",
                description="Intermediate (Age 9-10)",
                old_year="year5",
                old_year_display="Year 5"
            ),
            cls(
                level=4,
                name="Level 4",
                description="Advanced (Age 10-11)",
                old_year="year6",
                old_year_display="Year 6"
            ),
        ]
