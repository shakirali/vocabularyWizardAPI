"""Service for interacting with Ollama to generate quiz sentences."""
import logging
from typing import Optional

from ollama import Client

from app.core.config import settings

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for generating sentences using Ollama models."""

    def __init__(self):
        """Initialize Ollama client."""
        try:
            self.client = Client(host=settings.OLLAMA_BASE_URL)
            self.model = settings.OLLAMA_MODEL
            self.timeout = settings.OLLAMA_TIMEOUT
            self._available = True
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama client: {str(e)}")
            self._available = False
            self.client = None

    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        return self._available

    def generate_sentence_with_blank(
        self, word: str, meaning: str, max_retries: int = 2
    ) -> Optional[str]:
        """
        Generate a sentence using the word, with a blank placeholder.

        Args:
            word: The vocabulary word to use in the sentence
            meaning: The meaning/definition of the word for context
            max_retries: Maximum number of retry attempts if generation fails

        Returns:
            Sentence with blank placeholder (e.g., "The _____ was very beautiful.")
            Returns None if generation fails after retries
        """
        if not self._available or not self.client:
            logger.error("Ollama service is not available")
            return None

        prompt = f"""Generate a simple, clear sentence using the word "{word}" (meaning: {meaning}).
The sentence should be appropriate for educational purposes and suitable for children.
Replace the word "{word}" with a blank placeholder "_____" in your response.

Requirements:
- The sentence must use the word "{word}" naturally
- Replace "{word}" with exactly "_____" (5 underscores)
- Keep the sentence simple and clear
- Make it educational and age-appropriate

Example format: "The _____ was very beautiful."

Your response (sentence only, no explanation):"""

        for attempt in range(max_retries):
            try:
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    options={
                        "temperature": 0.7,  # Balance between creativity and consistency
                        "num_predict": 100,  # Limit response length
                    },
                )

                # Extract the generated text
                generated_text = response.get("response", "").strip()

                # Clean up the response - remove any extra text or explanations
                sentence = self._clean_sentence(generated_text, word)

                # Validate that the sentence contains the blank placeholder
                if "_____" in sentence:
                    logger.info(f"Successfully generated sentence for word: {word}")
                    return sentence
                else:
                    logger.warning(
                        f"Generated sentence missing blank placeholder for word: {word}. "
                        f"Attempt {attempt + 1}/{max_retries}"
                    )
                    if attempt < max_retries - 1:
                        continue

            except Exception as e:
                logger.error(
                    f"Error generating sentence for word '{word}': {str(e)}. "
                    f"Attempt {attempt + 1}/{max_retries}"
                )
                if attempt < max_retries - 1:
                    continue

        logger.error(f"Failed to generate sentence for word '{word}' after {max_retries} attempts")
        return None

    def _clean_sentence(self, text: str, word: str) -> str:
        """
        Clean and extract the sentence from the generated text.

        Args:
            text: Raw text from Ollama
            word: The word that should be replaced with blank

        Returns:
            Cleaned sentence with blank placeholder
        """
        # Remove common prefixes/suffixes that models might add
        text = text.strip()
        
        # Remove quotes if present
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        if text.startswith("'") and text.endswith("'"):
            text = text[1:-1]

        # If the word is still in the text, replace it with blank
        if word.lower() in text.lower():
            # Case-insensitive replacement
            import re
            text = re.sub(re.escape(word), "_____", text, flags=re.IGNORECASE)

        # Take only the first sentence if multiple sentences are generated
        sentences = text.split(".")
        if sentences:
            first_sentence = sentences[0].strip()
            # Add period if it was removed
            if not first_sentence.endswith((".", "!", "?")):
                first_sentence += "."
            return first_sentence

        return text


# Global instance
ollama_service = OllamaService()
