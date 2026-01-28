#!/usr/bin/env python3
"""
Generate quiz sentences for all words in vocabulary_levels.csv that don't have quiz sentences yet.
Generates 10 sentences per word following the vocabulary specification.
"""

import csv
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def generate_quiz_sentences(word, meaning, example_sentence, level):
    """
    Generate 10 quiz sentences for a word based on its meaning and example.
    Uses British English and follows the specification requirements.
    """
    word_lower = word.lower()
    
    # Generate sentences based on the word's meaning and context
    # This is a comprehensive dictionary of quiz sentences for each word
    # Following British English and 11+ exam standards
    
    sentences = []
    
    # Get base sentences based on word meaning and part of speech
    # We'll generate contextually appropriate sentences
    
    # This is a placeholder - in a real implementation, this would use
    # the word's meaning, synonyms, antonyms, and example to generate
    # 10 unique, contextually appropriate sentences
    
    # For now, I'll create a comprehensive generation function
    # that creates sentences based on common patterns and the word's meaning
    
    # Generate sentences with strong contextual clues
    base_patterns = [
        f"The {word_lower} was clear from the context.",
        f"She showed great {word_lower} in the situation.",
        f"His {word_lower} surprised everyone around him.",
        f"The {word_lower} became evident as the story unfolded.",
        f"They demonstrated {word_lower} throughout the challenge.",
        f"Her {word_lower} was obvious to all who watched.",
        f"The situation required {word_lower} from everyone involved.",
        f"His {word_lower} made a significant difference.",
        f"The {word_lower} was apparent in their actions.",
        f"She expressed {word_lower} in her response."
    ]
    
    # This is a simplified version - we need to generate proper sentences
    # based on the actual word meaning. Let me create a better approach.
    
    return sentences

# Read vocabulary data
vocab_content = {}
with open('data/vocabulary_content_new.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row['word'].strip()
        vocab_content[word.lower()] = {
            'word': word,
            'meaning': row['meaning'].strip(),
            'synonym1': row['synonym1'].strip(),
            'synonym2': row['synonym2'].strip(),
            'antonym1': row['antonym1'].strip(),
            'antonym2': row['antonym2'].strip(),
            'example_sentence': row['example_sentence'].strip()
        }

# Read vocabulary levels
vocab_levels = {}
with open('data/vocabulary_levels.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row['word'].strip()
        level = row['level'].strip()
        vocab_levels[word.lower()] = {
            'word': word,
            'level': level
        }

# Get words that already have quiz sentences
existing_quiz_words = set()
for level_num in [1, 2, 3, 4]:
    filename = f'data/quiz_sentences_level{level_num}.csv'
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word'].strip().lower()
            existing_quiz_words.add(word)

# Find words missing quiz sentences
missing_words = []
for word_lower, level_data in vocab_levels.items():
    if word_lower not in existing_quiz_words:
        if word_lower in vocab_content:
            missing_words.append({
                'word': level_data['word'],
                'level': level_data['level'],
                'content': vocab_content[word_lower]
            })

print(f"Found {len(missing_words)} words missing quiz sentences")
print(f"Will generate 10 sentences per word = {len(missing_words) * 10} total sentences")

# This script structure is ready, but we need to implement the actual
# sentence generation logic. Since generating 13,240 sentences programmatically
# requires a comprehensive approach, I'll create a more complete implementation.

if __name__ == '__main__':
    print("Script structure created. Need to implement sentence generation logic.")
