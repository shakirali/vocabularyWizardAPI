#!/usr/bin/env python3
"""
Generate vocabulary content for missing words using AI models.

This script:
1. Reads the list of missing words
2. Uses AI models to generate complete vocabulary content:
   - meaning, 2 synonyms, 2 antonyms, 1 example sentence
3. Appends the generated content to vocabulary_content_new.csv
"""

import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service

def read_missing_words(csv_path: Path) -> List[Dict[str, str]]:
    """Read missing words from CSV."""
    words = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word'].strip()
            level = row.get('level', '').strip()
            words.append({
                'word': word.lower(),
                'original': word,  # Keep original capitalization
                'level': level
            })
    return words

def generate_content_with_ai(word: str, original: str, level: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Generate complete vocabulary content using AI models.
    
    Returns a dictionary with all required fields, or None if generation fails.
    """
    if not ai_content_service.is_available():
        print(f"[ERROR] AI Content Service is not available for {original}")
        return None
    
    content = ai_content_service.generate_complete_vocabulary_content(original, level)
    
    if content:
        # Ensure word field matches expected format
        content['word'] = word
        return content
    
    return None

def read_existing_content(csv_path: Path) -> set:
    """Read existing words from vocabulary_content_new.csv to avoid duplicates."""
    existing_words = set()
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip().lower()
                existing_words.add(word)
    return existing_words

def append_to_csv(content_list: List[Dict[str, str]], csv_path: Path):
    """Append generated content to vocabulary_content_new.csv."""
    fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
    
    # Check if file exists and has header
    file_exists = csv_path.exists()
    
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        # Write all content rows
        for content in content_list:
            writer.writerow(content)

def main():
    """Main function."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    missing_words_path = data_dir / 'words_missing_from_vocabulary_content.csv'
    output_path = data_dir / 'vocabulary_content_new.csv'
    
    print("Reading missing words...")
    missing_words = read_missing_words(missing_words_path)
    print(f"Found {len(missing_words)} missing words")
    
    # Read existing content to avoid duplicates
    existing_words = read_existing_content(output_path)
    print(f"Found {len(existing_words)} existing words in vocabulary_content_new.csv")
    
    # Filter out words that already exist
    words_to_generate = [
        w for w in missing_words 
        if w['word'].lower() not in existing_words
    ]
    print(f"Words to generate: {len(words_to_generate)}")
    
    if not words_to_generate:
        print("All words already have content!")
        return
    
    # Generate content using AI
    generated_content = []
    failed_words = []
    
    print(f"\nGenerating content using AI models...")
    
    if not ai_content_service.is_available():
        print("[ERROR] AI Content Service is not available.")
        print("[ERROR] Cannot generate vocabulary content.")
        return
    
    for i, word_data in enumerate(words_to_generate, 1):
        word = word_data['word']
        original = word_data['original']
        level = word_data.get('level', '')
        
        print(f"[{i}/{len(words_to_generate)}] Generating content for: {original}")
        
        content = generate_content_with_ai(word, original, level)
        
        if content:
            generated_content.append(content)
            print(f"  ✓ Generated content for {original}")
        else:
            failed_words.append(original)
            print(f"  ✗ Failed to generate content for {original}")
    
    # Append to CSV
    if generated_content:
        print(f"\nAppending {len(generated_content)} entries to {output_path}...")
        append_to_csv(generated_content, output_path)
        print("✓ Content appended successfully!")
    
    if failed_words:
        print(f"\n⚠ Failed to generate content for {len(failed_words)} words:")
        for word in failed_words[:10]:  # Show first 10
            print(f"  - {word}")
        if len(failed_words) > 10:
            print(f"  ... and {len(failed_words) - 10} more")
    
    print(f"\nSummary:")
    print(f"  Total missing words: {len(missing_words)}")
    print(f"  Words to generate: {len(words_to_generate)}")
    print(f"  Successfully generated: {len(generated_content)}")
    print(f"  Failed: {len(failed_words)}")

if __name__ == '__main__':
    main()
