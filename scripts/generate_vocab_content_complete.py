#!/usr/bin/env python3
"""
Complete vocabulary content generator.

Generates vocabulary content and quiz sentences for all words in vocabularyList.csv
following the specification in vocabularySpecification.md.

Output files:
- data/vocabulary_content_new.csv (word, meaning, synonym1, synonym2, antonym1, antonym2, example_sentence)
- data/quiz_sentences_level1_new.csv
- data/quiz_sentences_level2_new.csv
- data/quiz_sentences_level3_new.csv
- data/quiz_sentences_level4_new.csv
"""

import csv
from pathlib import Path
from typing import Dict, List

# Note: This script provides the structure.
# Actual content generation should be done using an LLM API or manual review
# following the specification guidelines for British English and quality criteria.

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

def group_by_level(words: List[Dict]) -> Dict[str, List[Dict]]:
    """Group words by level."""
    by_level = {'level1': [], 'level2': [], 'level3': [], 'level4': []}
    for w in words:
        if w['level'] in by_level:
            by_level[w['level']].append(w)
    return by_level

def main():
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    vocab_list_path = data_dir / 'vocabularyList.csv'
    
    print("Reading vocabulary list...")
    words = read_vocabulary_list(vocab_list_path)
    print(f"Total words: {len(words)}")
    
    by_level = group_by_level(words)
    for level, level_words in by_level.items():
        print(f"  {level}: {len(level_words)} words")
    
    # Generate vocabulary content CSV
    print("\nGenerating vocabulary content CSV...")
    vocab_output = data_dir / 'vocabulary_content_new.csv'
    with open(vocab_output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence'
        ])
        writer.writeheader()
        for word_data in words:
            writer.writerow({
                'word': word_data['word'],
                'meaning': '',  # To be generated
                'synonym1': '',  # To be generated
                'synonym2': '',  # To be generated
                'antonym1': '',  # To be generated
                'antonym2': '',  # To be generated
                'example_sentence': ''  # To be generated
            })
    print(f"Template written to {vocab_output}")
    
    # Generate quiz sentences CSV files
    print("\nGenerating quiz sentences CSV files...")
    for level in ['level1', 'level2', 'level3', 'level4']:
        if level not in by_level:
            continue
        output_path = data_dir / f'quiz_sentences_{level}_new.csv'
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['word', 'quiz_sentence'])
            writer.writeheader()
            for word_data in by_level[level]:
                word = word_data['word']
                # 10 sentences per word
                for i in range(10):
                    writer.writerow({
                        'word': word,
                        'quiz_sentence': ''  # To be generated with <blank> placeholder
                    })
        print(f"  {output_path.name}: {len(by_level[level]) * 10} rows")
    
    print("\n" + "="*60)
    print("Templates created. Content generation needed.")
    print("Follow vocabularySpecification.md for quality guidelines.")
    print("="*60)

if __name__ == '__main__':
    main()
