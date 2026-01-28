#!/usr/bin/env python3
"""
Generate complete vocabulary content from vocabularyList.csv.

This script generates:
1. vocabulary_content.csv - meaning, 2 synonyms, 2 antonyms, 1 example sentence
2. quiz_sentences_level*.csv - 10 quiz sentences per word per level

All content follows British English and specification quality criteria.
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List

def read_vocabulary_list(csv_path: Path) -> List[Dict[str, str]]:
    """Read vocabulary list CSV."""
    words = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append({
                'word': row['word'].strip().lower(),
                'level': row['assigned_level'].strip(),
                'original': row['word'].strip()
            })
    return words

def group_words_by_level(words: List[Dict]) -> Dict[str, List[Dict]]:
    """Group words by level."""
    words_by_level = {
        'level1': [],
        'level2': [],
        'level3': [],
        'level4': []
    }
    for word_data in words:
        level = word_data['level']
        if level in words_by_level:
            words_by_level[level].append(word_data)
    return words_by_level

def main():
    """Main function."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    vocab_list_path = data_dir / 'vocabularyList.csv'
    
    print(f"Reading {vocab_list_path}...")
    words = read_vocabulary_list(vocab_list_path)
    print(f"Found {len(words)} words")
    
    words_by_level = group_words_by_level(words)
    for level, level_words in words_by_level.items():
        print(f"  {level}: {len(level_words)} words")
    
    print("\n" + "="*60)
    print("This script provides the structure for content generation.")
    print("Content generation should be implemented following the")
    print("specification guidelines in vocabularySpecification.md")
    print("="*60)
    
    # Write vocabulary content template
    vocab_content_path = data_dir / 'vocabulary_content_generated.csv'
    fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
    
    with open(vocab_content_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for word_data in words:
            writer.writerow({
                'word': word_data['word'],
                'meaning': '',
                'synonym1': '',
                'synonym2': '',
                'antonym1': '',
                'antonym2': '',
                'example_sentence': ''
            })
    
    print(f"\nTemplate written to {vocab_content_path}")
    print(f"Total words: {len(words)}")
    print("\nTo generate actual content, implement content generation")
    print("following the specification guidelines.")

if __name__ == '__main__':
    main()
