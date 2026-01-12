from typing import List, Optional
from pydantic import BaseModel
import uuid


class QuizQuestionResponse(BaseModel):
    id: uuid.UUID
    prompt: str
    options: List[str]
    correct_index: int
    type: str

    class Config:
        from_attributes = True


class GenerateQuizRequest(BaseModel):
    year: str
    question_count: Optional[int] = None


class GenerateQuizResponse(BaseModel):
    quiz_id: uuid.UUID
    year: str
    questions: List[QuizQuestionResponse]
    total_questions: int


class QuizAnswer(BaseModel):
    question_id: uuid.UUID
    selected_index: int


class SubmitQuizRequest(BaseModel):
    quiz_id: uuid.UUID
    answers: List[QuizAnswer]


class QuizResultItem(BaseModel):
    question_id: uuid.UUID
    correct: bool
    selected_index: int
    correct_index: int


class SubmitQuizResponse(BaseModel):
    quiz_id: uuid.UUID
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score_percentage: float
    results: List[QuizResultItem]


class SentenceQuestionResponse(BaseModel):
    id: uuid.UUID
    sentence_template: str
    display_sentence: str
    correct_word: str
    options: List[str]

    class Config:
        from_attributes = True


class GenerateSentenceRequest(BaseModel):
    year: str
    question_count: Optional[int] = None


class GenerateSentenceResponse(BaseModel):
    session_id: uuid.UUID
    year: str
    questions: List[SentenceQuestionResponse]
    total_questions: int


class SentenceAnswer(BaseModel):
    question_id: uuid.UUID
    selected_word: str


class SubmitSentenceRequest(BaseModel):
    session_id: uuid.UUID
    answers: List[SentenceAnswer]


class SentenceResultItem(BaseModel):
    question_id: uuid.UUID
    correct: bool
    selected_word: str
    correct_word: str


class SubmitSentenceResponse(BaseModel):
    session_id: uuid.UUID
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score_percentage: float
    results: List[SentenceResultItem]

