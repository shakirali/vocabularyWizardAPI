from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.database import get_db
from app.models.user import User
from app.schemas.quiz import (GenerateQuizRequest, GenerateQuizResponse,
                              SubmitQuizRequest, SubmitQuizResponse)
from app.services.quiz_service import QuizService

router = APIRouter()


@router.post("/generate", response_model=GenerateQuizResponse)
def generate_quiz(
    request: GenerateQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Generate quiz questions from mastered words."""
    quiz_service = QuizService(db)
    result = quiz_service.generate_quiz(current_user.id, request)
    return GenerateQuizResponse(**result)


@router.post("/submit", response_model=SubmitQuizResponse)
def submit_quiz(
    request: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Submit quiz answers and get results."""
    quiz_service = QuizService(db)
    result = quiz_service.submit_quiz(current_user.id, request)
    return SubmitQuizResponse(**result)
