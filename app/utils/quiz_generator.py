import logging
import random
import uuid
from typing import List, Optional

from app.models.quiz import QuizQuestion
from app.models.vocabulary import VocabularyItem
from app.utils.ollama_service import ollama_service

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
    use_ollama: bool = True,
) -> List[dict]:
    """
    Generate sentence fill-in-the-blank questions.
    Uses Ollama to generate sentences if example sentences are not available.

    Args:
        vocabulary_items: List of vocabulary items to generate questions from
        question_count: Optional limit on number of questions to generate
        use_ollama: If True, use Ollama to generate sentences when example_sentences are missing

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
        elif use_ollama:
            # Generate sentence using Ollama
            logger.info(f"Generating sentence using Ollama for word: {item.word}")
            generated_sentence = ollama_service.generate_sentence_with_blank(
                word=item.word, meaning=item.meaning
            )

            if generated_sentence:
                display_sentence = generated_sentence
                # Create template with {word} placeholder for potential future use
                sentence_template = generated_sentence.replace("_____", "{word}")
                logger.info(f"Successfully generated sentence for word: {item.word}")
            else:
                logger.warning(
                    f"Failed to generate sentence for word: {item.word}, skipping..."
                )
                continue
        else:
            # Skip items without example sentences if Ollama is disabled
            logger.debug(f"Skipping word '{item.word}' - no example sentences available")
            continue

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
