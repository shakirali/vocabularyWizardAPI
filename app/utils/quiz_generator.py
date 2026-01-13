import random
import uuid
from typing import List, Optional

from app.models.quiz import QuizQuestion
from app.models.vocabulary import VocabularyItem


def generate_quiz_questions(
    vocabulary_items: List[VocabularyItem], question_count: Optional[int] = None
) -> List[QuizQuestion]:
    """
    Generate quiz questions from vocabulary items.
    Each question asks for the meaning of a word with 3 distractors.
    """
    if question_count:
        vocabulary_items = random.sample(
            vocabulary_items, min(question_count, len(vocabulary_items))
        )

    questions = []
    all_meanings = [item.meaning for item in vocabulary_items]

    for item in vocabulary_items:
        # Create options: correct answer + 3 distractors
        options = [item.meaning]

        # Get distractors from other words
        distractors = [m for m in all_meanings if m != item.meaning]
        if len(distractors) >= 3:
            options.extend(random.sample(distractors, 3))
        else:
            options.extend(distractors)

        # Shuffle options
        random.shuffle(options)
        correct_index = options.index(item.meaning)

        question = QuizQuestion(
            id=uuid.uuid4(),
            vocabulary_item_id=item.id,
            prompt=item.word,
            options=options,
            correct_index=correct_index,
            type="meaning",
        )
        questions.append(question)

    return questions


def generate_sentence_questions(
    vocabulary_items: List[VocabularyItem], question_count: Optional[int] = None
) -> List[dict]:
    """
    Generate sentence fill-in-the-blank questions.
    Returns list of dicts with question data (not SQLAlchemy models).
    """
    # Filter items with example sentences
    items_with_sentences = [item for item in vocabulary_items if item.example_sentences]

    if question_count:
        items_with_sentences = random.sample(
            items_with_sentences, min(question_count, len(items_with_sentences))
        )

    questions = []
    all_words = [item.word for item in vocabulary_items]

    for item in items_with_sentences:
        # Pick a random example sentence
        sentence = random.choice(item.example_sentences)

        # Replace the word with placeholder
        sentence_template = sentence.replace(item.word, "{word}")
        display_sentence = sentence.replace(item.word, "_____")

        # Create options: correct word + 3 distractors
        options = [item.word]

        # Get distractors from other words
        distractors = [w for w in all_words if w != item.word]
        if len(distractors) >= 3:
            options.extend(random.sample(distractors, 3))
        else:
            options.extend(distractors)

        # Shuffle options
        random.shuffle(options)

        questions.append(
            {
                "id": uuid.uuid4(),
                "vocabulary_item_id": item.id,
                "sentence_template": sentence_template,
                "display_sentence": display_sentence,
                "correct_word": item.word,
                "options": options,
            }
        )

    return questions
