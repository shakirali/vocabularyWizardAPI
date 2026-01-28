#!/usr/bin/env python3
"""
Generate vocabulary content from vocabularyList.csv following the specification.

This script generates:
1. Vocabulary content CSV (meaning, 2 synonyms, 2 antonyms, 1 example sentence)
2. Quiz sentences CSV files split by level (10 sentences per word)
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def read_vocabulary_list(csv_path: Path) -> List[Dict[str, str]]:
    """Read vocabulary list CSV and return list of word dictionaries."""
    words = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word'].strip().lower()
            level = row['assigned_level'].strip()
            words.append({
                'word': word,
                'level': level,
                'original': row['word'].strip()  # Keep original capitalization for reference
            })
    return words

def write_vocabulary_content_csv(words: List[Dict], output_path: Path):
    """Write vocabulary content CSV with meaning, synonyms, antonyms, example sentence."""
    fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # This will be populated by the content generation
        # For now, we'll write a template that needs to be filled
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

def write_quiz_sentences_csv(words_by_level: Dict[str, List[Dict]], output_dir: Path):
    """Write quiz sentences CSV files split by level."""
    fieldnames = ['word', 'quiz_sentence']
    
    for level in ['level1', 'level2', 'level3', 'level4']:
        if level not in words_by_level:
            continue
            
        output_path = output_dir / f'quiz_sentences_{level}.csv'
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # Generate 10 sentences per word
            for word_data in words_by_level[level]:
                word = word_data['word']
                # Write 10 rows per word (10 quiz sentences)
                for i in range(10):
                    writer.writerow({
                        'word': word,
                        'quiz_sentence': ''  # To be generated with <blank> placeholder
                    })

def group_words_by_level(words: List[Dict]) -> Dict[str, List[Dict]]:
    """Group words by their assigned level."""
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
    """Main function to generate vocabulary content."""
    # Paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    vocab_list_path = data_dir / 'vocabularyList.csv'
    
    # Output paths
    output_dir = data_dir
    vocab_content_path = output_dir / 'vocabulary_content_generated.csv'
    quiz_sentences_dir = output_dir
    
    # Read vocabulary list
    print(f"Reading vocabulary list from {vocab_list_path}...")
    words = read_vocabulary_list(vocab_list_path)
    print(f"Found {len(words)} words")
    
    # Group by level
    words_by_level = group_words_by_level(words)
    for level, level_words in words_by_level.items():
        print(f"  {level}: {len(level_words)} words")
    
    # Generate vocabulary content CSV
    print(f"\nGenerating vocabulary content CSV...")
    write_vocabulary_content_csv(words, vocab_content_path)
    print(f"Template written to {vocab_content_path}")
    print("NOTE: Content needs to be generated following the specification guidelines.")
    
    # Generate quiz sentences CSV files
    print(f"\nGenerating quiz sentences CSV files...")
    write_quiz_sentences_csv(words_by_level, quiz_sentences_dir)
    print("Quiz sentence templates written to data/quiz_sentences_level*.csv")
    print("NOTE: Sentences need to be generated with <blank> placeholders.")
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Generate content for vocabulary_content_generated.csv")
    print("2. Generate quiz sentences for each level CSV file")
    print("3. Follow the specification guidelines for quality")
    print("="*60)

if __name__ == '__main__':
    main()
