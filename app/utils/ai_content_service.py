"""
AI Content Generation Service

This service uses AI models to generate vocabulary content including:
- Enhanced meanings
- Example sentences
- Complete vocabulary entries (meaning, synonyms, antonyms, examples)

All generation uses AI models rather than local templates.

NOTE: This service requires AI generation capabilities. The generation methods
will use AI models to create high-quality vocabulary content.
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Import the AI generation helper
try:
    from app.utils.ai_generation_helper import (
        generate_enhanced_meaning_ai,
        generate_example_sentence_ai,
        generate_complete_vocabulary_content_ai,
        generate_sentence_with_blank_ai,
    )
    AI_HELPER_AVAILABLE = True
except ImportError:
    AI_HELPER_AVAILABLE = False
    logger.warning("AI generation helper not available")


class AIContentService:
    """
    Service for generating vocabulary content using AI models.
    
    This service provides methods to generate high-quality vocabulary content
    including meanings, synonyms, antonyms, and example sentences.
    """

    def __init__(self):
        """Initialize the AI content service."""
        self._available = True
        logger.info("AI Content Service initialized")

    def is_available(self) -> bool:
        """Check if AI content service is available."""
        return self._available

    def generate_enhanced_meaning(
        self, word: str, current_meaning: str
    ) -> Optional[str]:
        """
        Generate an enhanced, richer meaning for a vocabulary word.
        
        Takes a short meaning and expands it to provide more context and
        clarity for learners, while keeping it concise (35-60 characters).
        
        Args:
            word: The vocabulary word
            current_meaning: The current (short) meaning to enhance
            
        Returns:
            Enhanced meaning string, or None if generation fails
        """
        if not self._available:
            logger.error("AI Content Service is not available")
            return None

        if not AI_HELPER_AVAILABLE:
            logger.error("AI generation helper is not available")
            return None

        logger.info(f"Generating enhanced meaning for '{word}' using AI")
        try:
            enhanced = generate_enhanced_meaning_ai(word, current_meaning)
            if enhanced:
                logger.info(f"Successfully generated enhanced meaning for '{word}'")
            return enhanced
        except Exception as e:
            logger.error(f"Error generating enhanced meaning for '{word}': {e}")
            return None

    def generate_example_sentence(
        self, word: str, meaning: str, level: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate an age-appropriate example sentence using the vocabulary word.
        
        Args:
            word: The vocabulary word to use in the sentence
            meaning: The meaning/definition of the word for context
            level: Optional level (level1-level4) to adjust complexity
            
        Returns:
            Example sentence string, or None if generation fails
        """
        if not self._available:
            logger.error("AI Content Service is not available")
            return None

        if not AI_HELPER_AVAILABLE:
            logger.error("AI generation helper is not available")
            return None

        logger.info(f"Generating example sentence for '{word}' using AI")
        try:
            sentence = generate_example_sentence_ai(word, meaning, level)
            if sentence:
                logger.info(f"Successfully generated example sentence for '{word}'")
            return sentence
        except Exception as e:
            logger.error(f"Error generating example sentence for '{word}': {e}")
            return None

    def generate_complete_vocabulary_content(
        self, word: str, level: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """
        Generate complete vocabulary content for a word.
        
        Generates:
        - Meaning/definition
        - Two synonyms
        - Two antonyms
        - One example sentence
        
        Args:
            word: The vocabulary word
            level: Optional level (level1-level4) to adjust complexity
            
        Returns:
            Dictionary with keys: word, meaning, synonym1, synonym2,
            antonym1, antonym2, example_sentence
            Returns None if generation fails
        """
        if not self._available:
            logger.error("AI Content Service is not available")
            return None

        if not AI_HELPER_AVAILABLE:
            logger.error("AI generation helper is not available")
            return None

        logger.info(f"Generating complete vocabulary content for '{word}' using AI")
        try:
            content = generate_complete_vocabulary_content_ai(word, level)
            if content:
                logger.info(f"Successfully generated vocabulary content for '{word}'")
            return content
        except Exception as e:
            logger.error(f"Error generating vocabulary content for '{word}': {e}")
            return None

    def generate_sentence_with_blank(
        self, word: str, meaning: str
    ) -> Optional[str]:
        """
        Generate a sentence with a blank placeholder for the word.
        
        Used for fill-in-the-blank quiz questions.
        The word is replaced with "_____" (5 underscores).
        
        Args:
            word: The vocabulary word
            meaning: The meaning/definition for context
            
        Returns:
            Sentence with blank placeholder, or None if generation fails
        """
        if not self._available:
            logger.error("AI Content Service is not available")
            return None

        if not AI_HELPER_AVAILABLE:
            logger.error("AI generation helper is not available")
            return None

        logger.info(f"Generating sentence with blank for '{word}' using AI")
        try:
            sentence = generate_sentence_with_blank_ai(word, meaning)
            if sentence:
                logger.info(f"Successfully generated sentence with blank for '{word}'")
            return sentence
        except Exception as e:
            logger.error(f"Error generating sentence with blank for '{word}': {e}")
            return None


# Global instance
ai_content_service = AIContentService()
