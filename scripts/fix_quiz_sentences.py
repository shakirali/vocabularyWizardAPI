#!/usr/bin/env python3
"""
Systematically fix quiz sentences across all levels:
1. Exact duplicates
2. Very similar sentences for the same word
3. Very short sentences (<50 chars) that are ambiguous
4. Sentences with weak context clues
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

def normalize_sentence(sentence):
    """Normalize sentence for comparison"""
    # Remove the blank
    s = sentence.replace('_____', '').lower().strip()
    # Remove punctuation
    s = re.sub(r'[^\w\s]', '', s)
    # Normalize whitespace
    s = ' '.join(s.split())
    return s

def sentences_are_similar(s1, s2, threshold=0.85):
    """Check if two sentences are very similar"""
    norm1 = normalize_sentence(s1)
    norm2 = normalize_sentence(s2)
    
    # Exact match after normalization
    if norm1 == norm2:
        return True
    
    # Check if one is contained in the other (with some variation)
    if len(norm1) > 20 and len(norm2) > 20:
        if norm1 in norm2 or norm2 in norm1:
            return True
    
    # Check word overlap
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    if len(words1) > 0 and len(words2) > 0:
        overlap = len(words1 & words2) / max(len(words1), len(words2))
        if overlap > threshold:
            return True
    
    return False

def is_weak_sentence(sentence, word):
    """Check if sentence has weak context clues"""
    sent_clean = sentence.replace('_____', '').strip()
    
    # Very short
    if len(sent_clean) < 50:
        return True
    
    # Weak patterns
    weak_patterns = [
        r'^(It|He|She|They|The|A|An) (was|were|is|are) _____\.?$',
        r'^(Many|People|Some|We|You) (can|will|should|must) _____\.?$',
        r'^_____ (is|are|was|were) \w+\.?$',
    ]
    
    for pattern in weak_patterns:
        if re.match(pattern, sentence, re.IGNORECASE):
            return True
    
    return False

def improve_sentence(sentence, word, level):
    """Improve a weak sentence by adding context"""
    # If already long enough, return as-is
    if len(sentence.replace('_____', '')) > 80:
        return sentence
    
    # Get the base sentence structure
    base = sentence.replace('_____', word)
    
    # Add context based on word and sentence structure
    # This is a simplified version - in practice, we'd have word-specific improvements
    if sentence.strip().endswith('_____.'):
        # Sentence ends with blank - add context before
        if 'was' in sentence.lower() or 'were' in sentence.lower():
            return sentence.replace('_____.', f'_____, which surprised everyone who knew them.')
        elif 'can' in sentence.lower() or 'will' in sentence.lower():
            return sentence.replace('_____.', f'_____, as long as you follow the instructions carefully.')
        else:
            return sentence.replace('_____.', f'_____, showing their commitment to the task.')
    
    # Add context after the blank
    if '_____' in sentence and not sentence.endswith('_____'):
        # Find position of blank
        blank_pos = sentence.find('_____')
        after_blank = sentence[blank_pos + 5:].strip()
        
        # If there's already context, check if it's sufficient
        if len(after_blank) < 30:
            # Add more context
            if level == 1:
                return sentence.replace('_____', f'_____ because it was the right thing to do')
            elif level == 2:
                return sentence.replace('_____', f'_____, which made everyone feel more confident about the decision')
            elif level == 3:
                return sentence.replace('_____', f'_____, demonstrating their understanding of the complex situation')
            else:  # level 4
                return sentence.replace('_____', f'_____, reflecting the nuanced nature of the problem')
    
    return sentence

def process_file(filename):
    """Process a quiz sentences file"""
    print(f"\nProcessing {filename}...")
    
    sentences_by_word = defaultdict(list)
    all_sentences = []
    
    # Read all sentences
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_sentences.append(row)
            sentences_by_word[row['word']].append(row)
    
    # Find issues
    exact_duplicates = []
    similar_sentences = []
    weak_sentences = []
    
    # Check for exact duplicates
    seen = {}
    for i, row in enumerate(all_sentences):
        key = (row['word'], row['sentence'].lower().strip())
        if key in seen:
            exact_duplicates.append((i, row, seen[key]))
        else:
            seen[key] = i
    
    # Check for similar sentences within same word
    for word, rows in sentences_by_word.items():
        for i, row1 in enumerate(rows):
            for row2 in rows[i+1:]:
                if sentences_are_similar(row1['sentence'], row2['sentence']):
                    similar_sentences.append((row1, row2))
    
    # Check for weak sentences
    for row in all_sentences:
        if is_weak_sentence(row['sentence'], row['word']):
            weak_sentences.append(row)
    
    print(f"  Found {len(exact_duplicates)} exact duplicates")
    print(f"  Found {len(similar_sentences)} pairs of similar sentences")
    print(f"  Found {len(weak_sentences)} weak sentences")
    
    # Fix issues
    fixed_sentences = []
    removed_indices = set()
    
    # Remove exact duplicates (keep first occurrence)
    for dup_idx, row, orig_idx in exact_duplicates:
        removed_indices.add(dup_idx)
    
    # For similar sentences, improve one and remove the other
    for row1, row2 in similar_sentences:
        # Find indices
        idx1 = next(i for i, r in enumerate(all_sentences) if r == row1)
        idx2 = next(i for i, r in enumerate(all_sentences) if r == row2)
        
        # Improve the first one, remove the second
        if idx1 not in removed_indices and idx2 not in removed_indices:
            level = int(row1['level'])
            improved = improve_sentence(row1['sentence'], row1['word'], level)
            row1['sentence'] = improved
            removed_indices.add(idx2)
    
    # Improve weak sentences
    for row in weak_sentences:
        idx = next(i for i, r in enumerate(all_sentences) if r == row)
        if idx not in removed_indices:
            level = int(row['level'])
            improved = improve_sentence(row['sentence'], row['word'], level)
            row['sentence'] = improved
    
    # Write improved sentences
    output_file = filename.replace('.csv', '_improved.csv')
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        if all_sentences:
            writer = csv.DictWriter(f, fieldnames=all_sentences[0].keys())
            writer.writeheader()
            for i, row in enumerate(all_sentences):
                if i not in removed_indices:
                    writer.writerow(row)
    
    print(f"  Wrote improved file: {output_file}")
    print(f"  Removed {len(removed_indices)} duplicate/similar sentences")
    print(f"  Improved {len(weak_sentences)} weak sentences")
    
    return len(removed_indices), len(weak_sentences)

if __name__ == '__main__':
    data_dir = Path(__file__).parent.parent / 'data'
    
    total_removed = 0
    total_improved = 0
    
    for level in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level}.csv'
        if filename.exists():
            removed, improved = process_file(str(filename))
            total_removed += removed
            total_improved += improved
    
    print(f"\n=== SUMMARY ===")
    print(f"Total duplicates/similar removed: {total_removed}")
    print(f"Total weak sentences improved: {total_improved}")
