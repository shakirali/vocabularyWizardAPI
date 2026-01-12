from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.quiz_service import QuizService
from app.schemas.quiz import (
    GenerateSentenceRequest,
    GenerateSentenceResponse,
    SubmitSentenceRequest,
    SubmitSentenceResponse
)

router = APIRouter()


@router.post("/generate", response_model=GenerateSentenceResponse)
def generate_sentences(
    request: GenerateSentenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate sentence fill-in-the-blank questions."""
    quiz_service = QuizService(db)
    result = quiz_service.generate_sentences(current_user.id, request)
    return GenerateSentenceResponse(**result)


@router.post("/submit", response_model=SubmitSentenceResponse)
def submit_sentences(
    request: SubmitSentenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit sentence fill answers."""
    quiz_service = QuizService(db)
    result = quiz_service.submit_sentences(current_user.id, request)
    return SubmitSentenceResponse(**result)

