#!/usr/bin/env python3
"""
Generate vocabulary content for missing excellent words.
Follows British English and specification quality criteria.
"""

import csv
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_content_for_word(word: str, word_lower: str, level: str, difficulty: float) -> dict:
    """
    Generate vocabulary content for a word following specification.
    Returns dict with meaning, synonyms, antonyms, example_sentence.
    """
    # This will be populated with actual content generation
    # For now, return structure - content will be generated in batches
    return {
        'word': word_lower,
        'meaning': '',
        'synonym1': '',
        'synonym2': '',
        'antonym1': '',
        'antonym2': '',
        'example_sentence': ''
    }

def main():
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    # Read missing words
    missing_words = []
    with open(data_dir / 'missing_words_with_levels.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            missing_words.append({
                'word': row['word'].strip(),
                'word_lower': row['word_lower'].strip(),
                'level': row['level'].strip(),
                'difficulty': float(row['difficulty'])
            })
    
    print(f"Generating content for {len(missing_words)} words...")
    
    # Read existing content
    existing_content = []
    fieldnames = None
    with open(data_dir / 'vocabulary_content_new.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_content.append(row)
    
    # Generate content for missing words
    new_content = []
    for word_data in missing_words:
        content = generate_content_for_word(
            word_data['word'],
            word_data['word_lower'],
            word_data['level'],
            word_data['difficulty']
        )
        new_content.append(content)
    
    # Append new content to existing
    all_content = existing_content + new_content
    
    # Write updated content
    with open(data_dir / 'vocabulary_content_new.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_content)
    
    print(f"✓ Updated vocabulary_content_new.csv")
    print(f"  Total words: {len(all_content)}")

if __name__ == '__main__':
    main()
