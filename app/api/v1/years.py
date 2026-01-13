from fastapi import APIRouter

from app.models.vocabulary import YearGroup
from app.schemas.vocabulary import YearGroupInfo

router = APIRouter()


@router.get("", response_model=list[YearGroupInfo])
def get_year_groups():
    """Get all available year groups."""
    return [
        YearGroupInfo(
            value=year,
            display_name=YearGroup.get_display_name(year),
            short_code=YearGroup.get_short_code(year),
        )
        for year in YearGroup.all()
    ]
