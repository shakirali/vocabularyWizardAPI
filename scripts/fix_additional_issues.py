#!/usr/bin/env python3
"""
Fix additional quality issues:
1. Possessive forms (_____'s)
2. Duplicate sentences
"""

import csv
from pathlib import Path
from collections import defaultdict

def fix_possessive(sentence):
    """
    Fix possessive forms - remove them as they make answers ambiguous
    Return None if sentence should be removed
    """
    if "_____'" in sentence:
        # These sentences are problematic - the possessive form
        # makes the answer unclear. Remove these sentences.
        return None
    return sentence

def main():
    print("=" * 80)
    print("FIXING ADDITIONAL QUALITY ISSUES")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    possessive_removed = 0
    duplicates_removed = 0
    
    for level_num in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        print(f"Processing Level {level_num}...")
        
        # Read all sentences
        sentences = []
        seen_combinations = set()  # Track (word, sentence) to detect duplicates
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word']
                sentence = row['sentence']
                level = row['level']
                
                # Fix 1: Check for possessive forms
                if "_____'" in sentence:
                    print(f"  Removed possessive for '{word}': {sentence[:60]}...")
                    possessive_removed += 1
                    continue  # Skip this sentence
                
                # Fix 2: Check for duplicates
                combination = (word.lower(), sentence.lower())
                if combination in seen_combinations:
                    print(f"  Removed duplicate for '{word}': {sentence[:60]}...")
                    duplicates_removed += 1
                    continue  # Skip duplicate
                
                seen_combinations.add(combination)
                sentences.append({
                    'level': level,
                    'word': word,
                    'sentence': sentence
                })
        
        # Write cleaned sentences
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
            writer.writeheader()
            writer.writerows(sentences)
        
        print(f"  ✓ Level {level_num} processed: {len(sentences)} sentences")
    
    print()
    print("=" * 80)
    print(f"✅ Possessive forms removed: {possessive_removed}")
    print(f"✅ Duplicates removed: {duplicates_removed}")
    print(f"📊 Total removed: {possessive_removed + duplicates_removed}")
    print("=" * 80)

if __name__ == '__main__':
    main()
