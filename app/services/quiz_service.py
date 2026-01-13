import uuid

from sqlalchemy.orm import Session

from app.repositories.progress_repository import ProgressRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.quiz import (GenerateQuizRequest, GenerateSentenceRequest,
                              SubmitQuizRequest, SubmitSentenceRequest)
from app.utils.quiz_generator import (generate_quiz_questions,
                                      generate_sentence_questions)


class QuizService:
    def __init__(self, db: Session):
        self.vocab_repo = VocabularyRepository(db)
        self.progress_repo = ProgressRepository(db)

    def generate_quiz(self, user_id: uuid.UUID, request: GenerateQuizRequest) -> dict:
        """Generate quiz questions from mastered words."""
        # Get mastered word IDs
        mastered_ids = self.progress_repo.get_mastered_word_ids_by_year(
            user_id, request.year
        )

        if not mastered_ids:
            return {
                "quiz_id": uuid.uuid4(),
                "year": request.year,
                "questions": [],
                "total_questions": 0,
            }

        # Get vocabulary items for mastered words
        vocabulary_items = []
        for word_id in mastered_ids:
            item = self.vocab_repo.get(str(word_id))
            if item:
                vocabulary_items.append(item)

        # Generate questions
        questions = generate_quiz_questions(vocabulary_items, request.question_count)

        # Convert to response format
        quiz_id = uuid.uuid4()
        question_responses = [
            {
                "id": q.id,
                "prompt": q.prompt,
                "options": q.options,
                "correct_index": q.correct_index,
                "type": q.type,
            }
            for q in questions
        ]

        return {
            "quiz_id": quiz_id,
            "year": request.year,
            "questions": question_responses,
            "total_questions": len(question_responses),
        }

    def submit_quiz(self, user_id: uuid.UUID, request: SubmitQuizRequest) -> dict:
        """Submit quiz answers and get results."""
        # In a real implementation, we'd store the quiz questions and retrieve them
        # For now, we'll return a placeholder response
        # This would require storing quiz sessions in the database
        return {
            "quiz_id": request.quiz_id,
            "total_questions": len(request.answers),
            "correct_answers": 0,
            "incorrect_answers": 0,
            "score_percentage": 0.0,
            "results": [],
        }

    def generate_sentences(
        self, user_id: uuid.UUID, request: GenerateSentenceRequest
    ) -> dict:
        """Generate sentence fill-in-the-blank questions."""
        # Get all vocabulary items for the year (not just mastered)
        vocabulary_items, _ = self.vocab_repo.get_all_with_filters(
            year=request.year, limit=1000
        )

        if not vocabulary_items:
            return {
                "session_id": uuid.uuid4(),
                "year": request.year,
                "questions": [],
                "total_questions": 0,
            }

        # Generate sentence questions
        questions = generate_sentence_questions(
            vocabulary_items, request.question_count
        )

        session_id = uuid.uuid4()
        question_responses = [
            {
                "id": q["id"],
                "sentence_template": q["sentence_template"],
                "display_sentence": q["display_sentence"],
                "correct_word": q["correct_word"],
                "options": q["options"],
            }
            for q in questions
        ]

        return {
            "session_id": session_id,
            "year": request.year,
            "questions": question_responses,
            "total_questions": len(question_responses),
        }

    def submit_sentences(
        self, user_id: uuid.UUID, request: SubmitSentenceRequest
    ) -> dict:
        """Submit sentence fill answers."""
        # In a real implementation, we'd store the sentence questions and retrieve them
        # For now, we'll return a placeholder response
        return {
            "session_id": request.session_id,
            "total_questions": len(request.answers),
            "correct_answers": 0,
            "incorrect_answers": 0,
            "score_percentage": 0.0,
            "results": [],
        }
