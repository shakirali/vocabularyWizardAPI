#!/usr/bin/env python3
"""
Fix identified quality issues:
1. Incorrect blank patterns (_____s, _____ed, etc.)
2. Generic template sentences for specific words
"""

import csv
import re
from pathlib import Path

def fix_blank_pattern(sentence, word):
    """Fix sentences where word endings are outside the blank"""
    if "_____" not in sentence:
        return sentence
    
    # Common patterns to fix
    patterns = [
        (r'_____s\b', '_____'),  # plurals
        (r'_____ed\b', '_____'),  # past tense
        (r'_____ing\b', '_____'),  # gerunds
        (r'_____ation\b', '_____'),  # -ation
        (r'_____ment\b', '_____'),  # -ment
        (r'_____ion\b', '_____'),  # -ion
        (r'_____ful\b', '_____'),  # -ful
        (r'_____al\b', '_____'),  # -al
        (r'_____ous\b', '_____'),  # -ous
        (r'_____d\b', '_____'),  # -d
    ]
    
    result = sentence
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)
    
    return result

def is_generic_template(sentence):
    """Check if sentence is a generic template"""
    generic = [
        "they had to _____ when the situation became dangerous",
        "she decided to _____ after realising it was the best choice",
        "he refused to _____ even when everyone else suggested it",
        "the team worked together to _____ the difficult challenge",
        "nobody wanted to _____ in such circumstances",
        "she managed to _____ despite facing many obstacles",
        "they were forced to _____ when they had no other option",
        "he learned to _____ after many years of practice",
        "we should _____ before it's too late",
    ]
    
    lower = sentence.lower()
    for template in generic:
        if template in lower:
            return True
    return False

def generate_replacement_sentence(word, meaning, level, index):
    """Generate a proper replacement sentence"""
    word_lower = word.lower()
    
    # Word-specific replacements
    replacements = {
        'alienate': [
            "His rude behaviour began to _____ his friends.",
            "The politician's harsh words _____ many voters.",
            "Her constant criticism _____ her colleagues at work.",
            "The company's poor service _____ loyal customers.",
            "His arrogant attitude _____ everyone he met.",
            "The new rules _____ students from participating.",
            "Her negative comments _____ potential allies.",
            "The unfair treatment _____ members of the team.",
            "His selfishness _____ his closest friends over time."
        ],
        'alleviate': [
            "The medicine helped to _____ her headache.",
            "The good news _____ their worries about the exam.",
            "A warm bath can _____ muscle pain effectively.",
            "The extra funding will _____ the school's financial problems.",
            "His kind words _____ her anxiety before the test.",
            "The new policy will _____ congestion in the city centre.",
            "A cold compress can _____ swelling and discomfort.",
            "The apology did little to _____ the hurt feelings.",
            "Exercise can _____ stress and improve mood."
        ]
    }
    
    if word_lower in replacements and index < len(replacements[word_lower]):
        return replacements[word_lower][index]
    
    return None

def main():
    print("=" * 80)
    print("FIXING QUALITY ISSUES")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    fixed_count = 0
    removed_count = 0
    
    for level_num in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        print(f"Processing Level {level_num}...")
        
        # Read all sentences
        sentences = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word']
                sentence = row['sentence']
                level = row['level']
                
                # Check for issues
                original_sentence = sentence
                
                # Fix 1: Blank patterns
                sentence = fix_blank_pattern(sentence, word)
                
                # Fix 2: Remove or replace generic templates
                if is_generic_template(sentence):
                    # Try to generate replacement
                    replacement = generate_replacement_sentence(word, "", level, len([s for s in sentences if s['word'] == word]))
                    
                    if replacement:
                        sentence = replacement
                        print(f"  Replaced generic for '{word}': {original_sentence[:50]}...")
                        fixed_count += 1
                    else:
                        # Skip this sentence (don't include it)
                        print(f"  Removed generic for '{word}': {original_sentence[:50]}...")
                        removed_count += 1
                        continue
                
                elif sentence != original_sentence:
                    print(f"  Fixed blank pattern in '{word}': {original_sentence[:40]}...")
                    fixed_count += 1
                
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
    print(f"✅ Fixes applied: {fixed_count}")
    print(f"🗑️  Removed: {removed_count}")
    print("=" * 80)

if __name__ == '__main__':
    main()
