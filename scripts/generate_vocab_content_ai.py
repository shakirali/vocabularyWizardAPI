#!/usr/bin/env python3
"""
Generate vocabulary content using AI models.

This script generates complete vocabulary content (meaning, synonyms, antonyms, 
example sentence) for words using AI generation capabilities.

Usage:
    python3 scripts/generate_vocab_content_ai.py <word> [level]
    python3 scripts/generate_vocab_content_ai.py --file <words_file.csv>
"""

import csv
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service


def generate_word_content(word: str, level: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Generate complete vocabulary content for a single word using AI.
    
    This function uses AI models to generate:
    - Meaning/definition
    - Two synonyms
    - Two antonyms
    - One example sentence
    """
    print(f"\n{'='*60}")
    print(f"Generating content for: {word}")
    if level:
        print(f"Level: {level}")
    print(f"{'='*60}")
    
    if not ai_content_service.is_available():
        print("❌ AI Content Service is not available")
        return None
    
    # Generate complete vocabulary content
    content = ai_content_service.generate_complete_vocabulary_content(word, level)
    
    if content:
        print(f"\n✅ Generated content:")
        print(f"  Word: {content.get('word', '')}")
        print(f"  Meaning: {content.get('meaning', '')}")
        print(f"  Synonym 1: {content.get('synonym1', '')}")
        print(f"  Synonym 2: {content.get('synonym2', '')}")
        print(f"  Antonym 1: {content.get('antonym1', '')}")
        print(f"  Antonym 2: {content.get('antonym2', '')}")
        print(f"  Example: {content.get('example_sentence', '')}")
        return content
    else:
        print("❌ Failed to generate content")
        return None


def generate_from_file(input_file: Path, output_file: Optional[Path] = None):
    """
    Generate vocabulary content for words listed in a CSV file.
    
    Expected CSV format:
    word,level
    abandon,level2
    abundant,level3
    """
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    words_to_generate = []
    with input_file.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row.get('word', '').strip()
            level = row.get('level', '').strip() or None
            if word:
                words_to_generate.append({'word': word, 'level': level})
    
    if not words_to_generate:
        print("❌ No words found in input file")
        return
    
    print(f"Found {len(words_to_generate)} words to generate content for")
    
    generated_content = []
    failed_words = []
    
    for i, word_data in enumerate(words_to_generate, 1):
        word = word_data['word']
        level = word_data.get('level')
        
        print(f"\n[{i}/{len(words_to_generate)}] Processing: {word}")
        content = generate_word_content(word, level)
        
        if content:
            generated_content.append(content)
        else:
            failed_words.append(word)
    
    # Write output
    if generated_content:
        if output_file is None:
            output_file = input_file.parent / f"{input_file.stem}_generated.csv"
        
        fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
        with output_file.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(generated_content)
        
        print(f"\n✅ Generated content for {len(generated_content)} words")
        print(f"✅ Saved to: {output_file}")
    
    if failed_words:
        print(f"\n⚠️  Failed to generate content for {len(failed_words)} words:")
        for word in failed_words:
            print(f"  - {word}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate vocabulary content using AI models'
    )
    parser.add_argument(
        'word',
        nargs='?',
        help='Single word to generate content for'
    )
    parser.add_argument(
        '--level',
        help='Level (level1, level2, level3, level4)'
    )
    parser.add_argument(
        '--file',
        type=Path,
        help='CSV file with words to generate (format: word,level)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output CSV file (default: <input>_generated.csv)'
    )
    
    args = parser.parse_args()
    
    if args.file:
        # Generate from file
        generate_from_file(args.file, args.output)
    elif args.word:
        # Generate for single word
        content = generate_word_content(args.word, args.level)
        if content:
            print("\n✅ Content generated successfully!")
            # Optionally save to file
            if args.output:
                fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
                with args.output.open('w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(content)
                print(f"✅ Saved to: {args.output}")
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 scripts/generate_vocab_content_ai.py abandon level2")
        print("  python3 scripts/generate_vocab_content_ai.py --file words.csv")


if __name__ == '__main__':
    main()
