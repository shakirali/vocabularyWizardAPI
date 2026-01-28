#!/usr/bin/env python3
"""
Generate vocabulary content for specific words using AI.

This script generates complete vocabulary content (meaning, synonyms, antonyms,
example sentence) for words you provide.

Usage:
    python3 scripts/generate_words_now.py word1 word2 word3 ...
    python3 scripts/generate_words_now.py --interactive
"""

import csv
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service


def generate_word_content_ai(word: str, level: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Generate complete vocabulary content for a word using AI.
    
    This function will use AI to generate:
    - Meaning/definition
    - Two synonyms
    - Two antonyms
    - One example sentence
    """
    print(f"\n{'='*70}")
    print(f"Generating content for: {word.upper()}")
    if level:
        print(f"Level: {level}")
    print(f"{'='*70}")
    
    # Use the AI content service to generate complete content
    # This will use AI models to generate all fields
    content = ai_content_service.generate_complete_vocabulary_content(word, level)
    
    if content and content.get('meaning') and content.get('example_sentence'):
        print(f"\n✅ Generated Content:")
        print(f"  Word: {content.get('word', '')}")
        print(f"  Meaning: {content.get('meaning', '')}")
        print(f"  Synonym 1: {content.get('synonym1', '') or '(not generated)'}")
        print(f"  Synonym 2: {content.get('synonym2', '') or '(not generated)'}")
        print(f"  Antonym 1: {content.get('antonym1', '') or '(not generated)'}")
        print(f"  Antonym 2: {content.get('antonym2', '') or '(not generated)'}")
        print(f"  Example: {content.get('example_sentence', '')}")
        return content
    else:
        print("❌ Failed to generate complete content")
        print("   Note: Complete content generation requires AI model connection")
        return None


def save_to_csv(content_list: List[Dict[str, str]], output_file: Path):
    """Save generated content to CSV file."""
    if not content_list:
        print("No content to save")
        return
    
    fieldnames = ['word', 'meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
    
    file_exists = output_file.exists()
    mode = 'a' if file_exists else 'w'
    
    with output_file.open(mode, encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(content_list)
    
    print(f"\n✅ Saved {len(content_list)} entries to: {output_file}")


def interactive_mode():
    """Interactive mode for generating content word by word."""
    print("\n" + "="*70)
    print("INTERACTIVE VOCABULARY CONTENT GENERATION")
    print("="*70)
    print("\nEnter words to generate content for (one per line).")
    print("Type 'done' or 'exit' when finished.")
    print("Type 'save <filename>' to save current results.\n")
    
    generated_content = []
    
    while True:
        try:
            word = input("Enter word (or 'done'/'save <file>'): ").strip()
            
            if not word:
                continue
            
            if word.lower() in ['done', 'exit', 'quit']:
                break
            
            if word.lower().startswith('save '):
                filename = word[5:].strip()
                if filename:
                    output_file = Path(filename)
                    save_to_csv(generated_content, output_file)
                    generated_content = []  # Clear after saving
                continue
            
            # Generate content
            content = generate_word_content_ai(word)
            if content:
                generated_content.append(content)
                save_choice = input("\nSave this word? (y/n): ").strip().lower()
                if save_choice == 'y':
                    # Save immediately
                    output_file = Path("generated_vocabulary.csv")
                    save_to_csv([content], output_file)
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except EOFError:
            break
    
    if generated_content:
        save_choice = input(f"\nSave {len(generated_content)} generated words? (y/n): ").strip().lower()
        if save_choice == 'y':
            output_file = Path("generated_vocabulary.csv")
            save_to_csv(generated_content, output_file)


def main():
    parser = argparse.ArgumentParser(
        description='Generate vocabulary content for specific words using AI'
    )
    parser.add_argument(
        'words',
        nargs='*',
        help='Words to generate content for'
    )
    parser.add_argument(
        '--interactive',
        '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--level',
        help='Level for all words (level1, level2, level3, level4)'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=Path,
        default=Path('generated_vocabulary.csv'),
        help='Output CSV file (default: generated_vocabulary.csv)'
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.words:
        # Generate for provided words
        print("\n" + "="*70)
        print("GENERATING VOCABULARY CONTENT")
        print("="*70)
        
        generated_content = []
        failed_words = []
        
        for word in args.words:
            content = generate_word_content_ai(word, args.level)
            if content:
                generated_content.append(content)
            else:
                failed_words.append(word)
        
        # Save results
        if generated_content:
            save_to_csv(generated_content, args.output)
        
        # Summary
        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        print(f"✅ Successfully generated: {len(generated_content)} words")
        if failed_words:
            print(f"❌ Failed: {len(failed_words)} words")
            for word in failed_words:
                print(f"   - {word}")
        print()
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 scripts/generate_words_now.py abandon abundant acute")
        print("  python3 scripts/generate_words_now.py --interactive")
        print("  python3 scripts/generate_words_now.py word1 word2 --level level2 --output output.csv")


if __name__ == '__main__':
    main()
