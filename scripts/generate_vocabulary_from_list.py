#!/usr/bin/env python3
"""
Generate vocabulary content from vocabularyList.csv following the specification.

This script reads vocabularyList.csv and generates:
1. Vocabulary content CSV (word, meaning, synonym1, synonym2, antonym1, antonym2, example_sentence)
2. Quiz sentences CSV files split by level (10 sentences per word with <blank> placeholder)

All content follows British English and the quality criteria from vocabularySpecification.md
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List
import json

# Add parent directory to path
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
                'original': row['word'].strip()
            })
    return words

def generate_vocabulary_content(word: str, level: str) -> Dict[str, str]:
    """
    Generate vocabulary content for a word following the specification.
    
    This function should be implemented to generate:
    - meaning: clear, accurate definition in British English
    - synonym1, synonym2: true synonyms, same part of speech
    - antonym1, antonym2: true opposites, same part of speech
    - example_sentence: natural sentence demonstrating word usage
    
    For now, returns a template structure.
    """
    # This is a placeholder - actual content generation should be implemented
    # following the specification guidelines
    return {
        'word': word,
        'meaning': '',  # To be generated
        'synonym1': '',  # To be generated
        'synonym2': '',  # To be generated
        'antonym1': '',  # To be generated
        'antonym2': '',  # To be generated
        'example_sentence': ''  # To be generated
    }

def generate_quiz_sentences(word: str, level: str, count: int = 10) -> List[str]:
    """
    Generate quiz sentences for a word.
    
    Each sentence should:
    - Contain exactly one <blank> placeholder
    - Be unambiguous (target word is best fit)
    - Use strong contextual clues
    - Be natural and grammatically correct
    - Use British English
    
    Returns list of sentences with <blank> placeholder.
    """
    # This is a placeholder - actual sentence generation should be implemented
    # following the specification guidelines
    return [f'Sentence with <blank> for {word}'] * count

def write_vocabulary_content_csv(words: List[Dict], output_path: Path, generate_content_func):
    """Write vocabulary content CSV."""
    fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for word_data in words:
            content = generate_content_func(word_data['word'], word_data['level'])
            writer.writerow(content)
            print(f"Generated content for: {word_data['word']} ({word_data['level']})")

def write_quiz_sentences_csv(words_by_level: Dict[str, List[Dict]], output_dir: Path, generate_sentences_func):
    """Write quiz sentences CSV files split by level."""
    fieldnames = ['word', 'quiz_sentence']
    
    for level in ['level1', 'level2', 'level3', 'level4']:
        if level not in words_by_level:
            continue
            
        output_path = output_dir / f'quiz_sentences_{level}_generated.csv'
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for word_data in words_by_level[level]:
                word = word_data['word']
                sentences = generate_sentences_func(word, level, count=10)
                
                for sentence in sentences:
                    writer.writerow({
                        'word': word,
                        'quiz_sentence': sentence
                    })
                print(f"Generated 10 quiz sentences for: {word} ({level})")

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
    print("NOTE: This script provides the structure. Content generation needs to be implemented.")
    print("      You can use an LLM API or manual generation following the specification.")
    
    # For demonstration, we'll write the structure
    # In production, you would implement generate_vocabulary_content() to actually generate content
    write_vocabulary_content_csv(words, vocab_content_path, generate_vocabulary_content)
    
    # Generate quiz sentences CSV files
    print(f"\nGenerating quiz sentences CSV files...")
    write_quiz_sentences_csv(words_by_level, output_dir, generate_quiz_sentences)
    
    print("\n" + "="*60)
    print("Generation complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Implement generate_vocabulary_content() to generate actual content")
    print("2. Implement generate_quiz_sentences() to generate actual sentences")
    print("3. Follow the specification guidelines for quality")
    print("4. Review generated content for accuracy and British English compliance")

if __name__ == '__main__':
    main()
