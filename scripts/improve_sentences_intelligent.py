#!/usr/bin/env python3
"""
Intelligently improve quiz sentences with proper context-aware enhancements
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

def improve_short_sentence(sentence, word, level):
    """Improve a short sentence with appropriate context"""
    sent_clean = sentence.replace('_____', '').strip()
    
    # If already good length, return as-is
    if len(sent_clean) > 70:
        return sentence
    
    # Pattern-based improvements
    patterns = {
        # "X was/were _____"
        r'^(The|A|An|Her|His|Their|Our|My|Your) (\w+) (was|were) _____\.?$': 
            lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)} _____, which surprised everyone who knew them well.",
        
        # "X is/are _____"
        r'^(The|A|An|Her|His|Their|Our|My|Your) (\w+) (is|are) _____\.?$':
            lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)} _____, making it clear to everyone who observed them.",
        
        # "X can/will/should _____"
        r'^(We|You|They|People|Many|Some) (can|will|should|must) _____\.?$':
            lambda m: f"{m.group(1)} {m.group(2)} _____ if they follow the proper steps and take the time to understand what's needed.",
        
        # "X decided/chose to _____"
        r'^(He|She|They|The|A|An) (\w+) (decided|chose) to _____\.?$':
            lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)} to _____, knowing it was the best option available to them.",
        
        # "X _____ Y"
        r'^(The|A|An|Her|His|Their) (\w+) _____ (the|a|an|his|her|their) (\w+)\.?$':
            lambda m: f"{m.group(1)} {m.group(2)} _____ {m.group(3)} {m.group(4)}, taking care to do it properly and thoroughly.",
    }
    
    for pattern, replacer in patterns.items():
        match = re.match(pattern, sentence, re.IGNORECASE)
        if match:
            improved = replacer(match)
            # Make sure it's not too long
            if len(improved.replace('_____', '')) < 120:
                return improved
    
    # Generic improvement for very short sentences
    if len(sent_clean) < 40:
        if sentence.endswith('_____.'):
            return sentence.replace('_____.', f'_____, which was exactly what everyone had been hoping for.')
        elif '_____' in sentence:
            # Add context after blank
            parts = sentence.split('_____')
            if len(parts) == 2 and len(parts[1].strip()) < 10:
                return f"{parts[0]}_____{parts[1].strip()}, showing their commitment and understanding of the situation."
    
    return sentence

def process_file_intelligent(input_file, output_file):
    """Process file with intelligent improvements"""
    print(f"\nProcessing {input_file}...")
    
    sentences_by_word = defaultdict(list)
    all_sentences = []
    seen_sentences = set()
    
    # Read sentences
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_sentences.append(row)
            sentences_by_word[row['word']].append(len(all_sentences) - 1)
            seen_sentences.add((row['word'], row['sentence'].lower().strip()))
    
    # Track what to remove
    to_remove = set()
    improved_count = 0
    
    # Remove exact duplicates (keep first)
    seen = {}
    for i, row in enumerate(all_sentences):
        key = (row['word'], row['sentence'].lower().strip())
        if key in seen:
            to_remove.add(i)
        else:
            seen[key] = i
    
    # Find and fix similar sentences
    for word, indices in sentences_by_word.items():
        if len(indices) < 2:
            continue
        
        # Compare sentences for this word
        for i, idx1 in enumerate(indices):
            if idx1 in to_remove:
                continue
            sent1 = all_sentences[idx1]['sentence']
            
            for idx2 in indices[i+1:]:
                if idx2 in to_remove:
                    continue
                sent2 = all_sentences[idx2]['sentence']
                
                # Check similarity
                norm1 = re.sub(r'[^\w\s]', '', sent1.lower().replace('_____', ''))
                norm2 = re.sub(r'[^\w\s]', '', sent2.lower().replace('_____', ''))
                
                # If very similar (one contains the other or 80% word overlap)
                words1 = set(norm1.split())
                words2 = set(norm2.split())
                if len(words1) > 0 and len(words2) > 0:
                    overlap = len(words1 & words2) / max(len(words1), len(words2))
                    if overlap > 0.8 or (norm1 in norm2 and len(norm1) > 20) or (norm2 in norm1 and len(norm2) > 20):
                        # Improve the first, remove the second
                        level = int(all_sentences[idx1]['level'])
                        improved = improve_short_sentence(sent1, word, level)
                        all_sentences[idx1]['sentence'] = improved
                        to_remove.add(idx2)
                        improved_count += 1
    
    # Improve weak/short sentences
    for i, row in enumerate(all_sentences):
        if i in to_remove:
            continue
        
        sent_clean = row['sentence'].replace('_____', '').strip()
        if len(sent_clean) < 50:
            level = int(row['level'])
            improved = improve_short_sentence(row['sentence'], row['word'], level)
            if improved != row['sentence']:
                row['sentence'] = improved
                improved_count += 1
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        if all_sentences:
            writer = csv.DictWriter(f, fieldnames=all_sentences[0].keys())
            writer.writeheader()
            for i, row in enumerate(all_sentences):
                if i not in to_remove:
                    writer.writerow(row)
    
    print(f"  Removed {len(to_remove)} duplicates/similar sentences")
    print(f"  Improved {improved_count} sentences")
    print(f"  Output: {output_file}")
    
    return len(to_remove), improved_count

if __name__ == '__main__':
    data_dir = Path(__file__).parent.parent / 'data'
    
    total_removed = 0
    total_improved = 0
    
    for level in [1, 2, 3, 4]:
        input_file = data_dir / f'quiz_sentences_level{level}.csv'
        output_file = data_dir / f'quiz_sentences_level{level}_fixed.csv'
        
        if input_file.exists():
            removed, improved = process_file_intelligent(str(input_file), str(output_file))
            total_removed += removed
            total_improved += improved
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total removed: {total_removed}")
    print(f"Total improved: {total_improved}")
