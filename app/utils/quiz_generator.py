import logging
import random
import uuid
from typing import List, Optional

from app.models.quiz import QuizQuestion
from app.models.vocabulary import VocabularyItem

logger = logging.getLogger(__name__)


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
    vocabulary_items: List[VocabularyItem],
    question_count: Optional[int] = None,
) -> List[dict]:
    """
    Generate sentence fill-in-the-blank questions.
    Uses existing example sentences where possible, and falls back to
    simple, locally generated sentences based on the word and meaning.

    Args:
        vocabulary_items: List of vocabulary items to generate questions from
        question_count: Optional limit on number of questions to generate

    Returns:
        List of dicts with question data (not SQLAlchemy models).
    """
    # Select items to use for questions
    selected_items = vocabulary_items
    if question_count:
        selected_items = random.sample(
            vocabulary_items, min(question_count, len(vocabulary_items))
        )

    questions = []
    all_words = [item.word for item in vocabulary_items]

    def _generate_local_sentence(word: str, meaning: str) -> str:
        """
        Generate a simple, deterministic sentence for a word using only
        local templates (no external AI services).
        """
        meaning_lower = (meaning or "").lower()
        is_verb = meaning_lower.startswith("to ")
        is_adjective = any(
            marker in meaning_lower
            for marker in [
                "having ",
                "showing ",
                "full of",
                "characterised by",
                "characterized by",
                "very ",
                "extremely ",
                "quite ",
                "rather ",
                "causing ",
                "deserving ",
            ]
        )

        if is_verb:
            template = (
                f"They decided to {word} carefully because of the situation."
            )
        elif is_adjective:
            template = (
                f"It was a very {word} moment that everyone remembered."
            )
        else:
            template = (
                f"The {word} was important in understanding the story."
            )

        return template

    for item in selected_items:
        display_sentence = None
        sentence_template = None

        # Try to use existing example sentences first
        if item.example_sentences:
            sentence = random.choice(item.example_sentences)
            # Replace the word with placeholder
            sentence_template = sentence.replace(item.word, "{word}")
            display_sentence = sentence.replace(item.word, "_____")
            logger.debug(f"Using existing example sentence for word: {item.word}")
        else:
            # Fall back to a locally generated sentence
            logger.debug(
                "No example sentences for word '%s', using local template",
                item.word,
            )
            base_sentence = _generate_local_sentence(item.word, item.meaning)
            sentence_template = base_sentence.replace(item.word, "{word}")
            display_sentence = base_sentence.replace(item.word, "_____")

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
