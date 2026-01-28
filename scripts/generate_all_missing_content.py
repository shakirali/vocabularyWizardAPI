#!/usr/bin/env python3
"""
Generate vocabulary content for all 419 missing excellent words.
Follows British English and specification quality criteria.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def generate_vocab_content(word_lower: str, word_original: str, level: str) -> dict:
    """
    Generate vocabulary content for a word.
    Returns dict with meaning, synonyms, antonyms, example_sentence.
    Content follows specification: British English, clear meanings, true synonyms/antonyms.
    """
    # This function will be populated with actual content generation
    # For now, return structure
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
                'level': row['level'].strip()
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
    
    # Generate content for all missing words
    new_content = []
    for word_info in missing_words:
        content = generate_vocab_content(
            word_info['word_lower'],
            word_info['word'],
            word_info['level']
        )
        new_content.append(content)
    
    # Combine and write
    all_content = existing_content + new_content
    
    with open(data_dir / 'vocabulary_content_new.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_content)
    
    print(f"✓ Updated vocabulary_content_new.csv")
    print(f"  Total words: {len(all_content)}")

if __name__ == '__main__':
    main()
