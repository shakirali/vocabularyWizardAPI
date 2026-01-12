from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.vocabulary import VocabularyItem
from app.repositories.base import BaseRepository


class VocabularyRepository(BaseRepository[VocabularyItem]):
    def __init__(self, db: Session):
        super().__init__(VocabularyItem, db)

    def get_by_year(self, year: str, skip: int = 0, limit: int = 100) -> List[VocabularyItem]:
        return (
            self.db.query(VocabularyItem)
            .filter(VocabularyItem.year == year)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(self, search_term: str, year: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[VocabularyItem]:
        query = self.db.query(VocabularyItem).filter(
            or_(
                VocabularyItem.word.ilike(f"%{search_term}%"),
                VocabularyItem.meaning.ilike(f"%{search_term}%")
            )
        )
        if year:
            query = query.filter(VocabularyItem.year == year)
        return query.offset(skip).limit(limit).all()

    def get_all_with_filters(
        self, year: Optional[str] = None, search: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> tuple[List[VocabularyItem], int]:
        query = self.db.query(VocabularyItem)
        
        if year:
            query = query.filter(VocabularyItem.year == year)
        
        if search:
            query = query.filter(
                or_(
                    VocabularyItem.word.ilike(f"%{search}%"),
                    VocabularyItem.meaning.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        
        return items, total

