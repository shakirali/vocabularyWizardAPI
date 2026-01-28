#!/usr/bin/env python3
"""
Generate quiz sentences to ensure ALL words have exactly 10 sentences.

This script:
1. Reads vocabulary_content_new.csv to get all words
2. Checks how many sentences each word currently has
3. Generates additional sentences using AI to bring each word to 10 sentences
4. Updates the level CSV files with all sentences
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service


def load_vocabulary_content(data_dir: Path) -> Dict[str, Dict]:
    """Load vocabulary content from vocabulary_content_new.csv"""
    vocab_content = {}
    vocab_file = data_dir / 'vocabulary_content_new.csv'
    
    with vocab_file.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word_lower = row['word'].strip().lower()
            vocab_content[word_lower] = {
                'word': row['word'].strip(),
                'meaning': row['meaning'].strip(),
                'synonym1': row.get('synonym1', '').strip(),
                'synonym2': row.get('synonym2', '').strip(),
                'antonym1': row.get('antonym1', '').strip(),
                'antonym2': row.get('antonym2', '').strip(),
                'example_sentence': row.get('example_sentence', '').strip()
            }
    
    return vocab_content


def load_vocabulary_levels(data_dir: Path) -> Dict[str, Dict]:
    """Load vocabulary levels from vocabulary_levels.csv"""
    vocab_levels = {}
    levels_file = data_dir / 'vocabulary_levels.csv'
    
    with levels_file.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word_lower = row['word'].strip().lower()
            vocab_levels[word_lower] = {
                'word': row['word'].strip(),
                'level': row['level'].strip()
            }
    
    return vocab_levels


def load_existing_sentences(data_dir: Path) -> Dict[str, List[Dict]]:
    """Load existing sentences grouped by level"""
    sentences_by_level = defaultdict(list)
    
    for level_num in [1, 2, 3, 4]:
        quiz_file = data_dir / f'quiz_sentences_level{level_num}.csv'
        if quiz_file.exists():
            with quiz_file.open('r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sentences_by_level[level_num].append({
                        'word': row['word'].strip(),
                        'sentence': row['sentence'].strip()
                    })
    
    return sentences_by_level


def generate_quiz_sentence_ai(
    word: str, 
    meaning: str, 
    level: str,
    example_sentence: str = "",
    synonym1: str = "",
    antonym1: str = "",
    existing_sentences: Set[str] = None
) -> str:
    """
    Generate a single unique quiz sentence using AI.
    Returns a sentence with the word replaced by "_____"
    """
    if existing_sentences is None:
        existing_sentences = set()
    
    # Try AI generation first
    sentence = ai_content_service.generate_sentence_with_blank(word, meaning)
    
    if sentence and "_____" in sentence and sentence not in existing_sentences:
        return sentence
    
    # Generate based on meaning and context
    meaning_lower = meaning.lower()
    word_lower = word.lower()
    
    # Determine word type
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving"
    ])
    
    # Generate contextually appropriate sentence
    import random
    
    if is_verb:
        templates = [
            f"They had to _____ the situation before it got worse.",
            f"She decided to _____ the problem quickly and efficiently.",
            f"He tried to _____ what was happening, but it was difficult.",
            f"We need to _____ this matter carefully and thoughtfully.",
            f"You should _____ before making any important decisions.",
            f"It's crucial to _____ properly in such circumstances.",
            f"They managed to _____ successfully despite many obstacles.",
            f"She learned to _____ effectively through careful practice.",
            f"He refused to _____ without thinking it through completely.",
            f"We must _____ to resolve this challenging problem.",
            f"The team worked together to _____ the difficult challenge.",
            f"She was determined to _____ despite the setbacks.",
            f"They had no choice but to _____ in that situation.",
            f"He wanted to _____ but didn't know how to begin.",
            f"We decided to _____ after careful consideration.",
        ]
    elif is_adjective:
        templates = [
            f"The situation was very _____ and quite concerning to everyone.",
            f"She showed a _____ attitude that impressed her teachers.",
            f"His behaviour was quite _____ and rather unexpected.",
            f"It was a _____ experience that everyone remembered fondly.",
            f"The _____ nature of the event surprised us all greatly.",
            f"They found it _____ and quite interesting to observe.",
            f"Her response was _____ and very thoughtful indeed.",
            f"The _____ quality made it truly special and unique.",
            f"It seemed _____ to all who witnessed the event.",
            f"The _____ aspect was clear from the very beginning.",
            f"Everyone noticed how _____ the situation had become.",
            f"The _____ appearance caught everyone's attention.",
            f"His _____ manner made him popular with everyone.",
            f"The _____ feeling was evident throughout the room.",
            f"She had a _____ way of solving problems.",
        ]
    else:  # noun
        templates = [
            f"The _____ was clear to everyone present at the meeting.",
            f"She understood the _____ of the situation immediately.",
            f"His _____ surprised those around him greatly.",
            f"The _____ became evident very quickly to all observers.",
            f"Everyone noticed the _____ in the way he spoke.",
            f"The _____ provided important context for the story.",
            f"Her _____ was obvious from her actions.",
            f"The _____ helped explain what had happened.",
            f"People discussed the _____ at length.",
            f"The _____ was the key to understanding everything.",
            f"Everyone was aware of the _____ in the room.",
            f"The _____ became the focus of their discussion.",
            f"She explained the _____ to everyone clearly.",
            f"The _____ revealed important information.",
            f"His understanding of the _____ was impressive.",
        ]
    
    # Try templates until we find one not in existing sentences
    for template in templates:
        if template not in existing_sentences:
            return template
    
    # If all templates are used, create a variation
    return random.choice(templates).replace("_____", word_lower).replace(word_lower, "_____", 1)


def generate_additional_sentences(
    word: str,
    meaning: str,
    level: str,
    example_sentence: str,
    synonym1: str,
    antonym1: str,
    existing_sentences: List[str],
    count: int
) -> List[str]:
    """Generate additional sentences to reach the target count"""
    existing_set = set(existing_sentences)
    new_sentences = []
    
    for i in range(count):
        sentence = generate_quiz_sentence_ai(
            word, meaning, level, example_sentence, synonym1, antonym1, existing_set
        )
        if sentence and sentence not in existing_set:
            new_sentences.append(sentence)
            existing_set.add(sentence)
        
        # If we can't generate more unique sentences, break
        if len(new_sentences) >= count:
            break
    
    return new_sentences


def main():
    """Main function to ensure all words have 10 sentences"""
    print("=" * 70)
    print("GENERATE QUIZ SENTENCES - ENSURE ALL WORDS HAVE 10 SENTENCES")
    print("=" * 70)
    print()
    
    if not ai_content_service.is_available():
        print("❌ AI Content Service is not available")
        return
    
    print("✅ AI Content Service is available")
    print()
    
    # Setup paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    # Load data
    print("📚 Loading vocabulary data...")
    vocab_content = load_vocabulary_content(data_dir)
    print(f"  ✓ Loaded {len(vocab_content)} words from vocabulary_content_new.csv")
    
    vocab_levels = load_vocabulary_levels(data_dir)
    print(f"  ✓ Loaded {len(vocab_levels)} words from vocabulary_levels.csv")
    
    existing_sentences_by_level = load_existing_sentences(data_dir)
    print(f"  ✓ Loaded existing sentences from quiz files")
    
    # Count current sentences per word
    sentences_per_word = defaultdict(list)
    for level_num, sentences in existing_sentences_by_level.items():
        for entry in sentences:
            word_lower = entry['word'].strip().lower()
            sentences_per_word[word_lower].append(entry['sentence'])
    
    # Find words needing more sentences
    words_to_process = []
    for word_lower in vocab_content.keys():
        if word_lower not in vocab_levels:
            continue
        
        current_count = len(sentences_per_word.get(word_lower, []))
        if current_count < 10:
            words_to_process.append({
                'word': vocab_levels[word_lower]['word'],
                'word_lower': word_lower,
                'level': vocab_levels[word_lower]['level'],
                'current_count': current_count,
                'needed': 10 - current_count,
                'content': vocab_content[word_lower],
                'existing_sentences': sentences_per_word.get(word_lower, [])
            })
    
    total_needed = sum(w['needed'] for w in words_to_process)
    print(f"\n📊 Analysis:")
    print(f"  Total words: {len(vocab_content)}")
    print(f"  Words needing more sentences: {len(words_to_process)}")
    print(f"  Total sentences to generate: {total_needed}")
    
    if total_needed == 0:
        print("\n✅ All words already have 10 sentences!")
        return
    
    # Group by level
    words_by_level = defaultdict(list)
    for word_data in words_to_process:
        level = word_data['level']
        level_num = int(level.replace('level', ''))
        words_by_level[level_num].append(word_data)
    
    print(f"\n📝 Breakdown by level:")
    for level_num in sorted(words_by_level.keys()):
        words = words_by_level[level_num]
        needed = sum(w['needed'] for w in words)
        print(f"  Level {level_num}: {len(words)} words, {needed} sentences needed")
    
    print(f"\n⏳ Generating sentences using AI (this will take a while)...\n")
    
    # Process each level
    total_generated = 0
    for level_num in sorted(words_by_level.keys()):
        words = words_by_level[level_num]
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        print(f"📝 Processing Level {level_num} ({len(words)} words)...")
        
        # Collect all sentences for this level
        all_sentences_for_level = []
        
        # Add existing sentences
        for entry in existing_sentences_by_level.get(level_num, []):
            all_sentences_for_level.append({
                'level': str(level_num),
                'word': entry['word'],
                'sentence': entry['sentence']
            })
        
        # Generate new sentences
        for i, word_data in enumerate(words, 1):
            word = word_data['word']
            content = word_data['content']
            existing = word_data['existing_sentences']
            needed = word_data['needed']
            
            if i % 50 == 0 or i == 1:
                print(f"  [{i}/{len(words)}] {word}: {word_data['current_count']} existing, need {needed} more")
            
            # Generate additional sentences
            new_sentences = generate_additional_sentences(
                word=word,
                meaning=content['meaning'],
                level=word_data['level'],
                example_sentence=content.get('example_sentence', ''),
                synonym1=content.get('synonym1', ''),
                antonym1=content.get('antonym1', ''),
                existing_sentences=existing,
                count=needed
            )
            
            # Add new sentences
            for sentence in new_sentences:
                all_sentences_for_level.append({
                    'level': str(level_num),
                    'word': word,
                    'sentence': sentence
                })
            
            total_generated += len(new_sentences)
        
        # Write all sentences to file
        with filename.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
            writer.writeheader()
            writer.writerows(all_sentences_for_level)
        
        print(f"  ✅ Level {level_num}: {len(all_sentences_for_level)} total sentences written")
    
    print("\n" + "=" * 70)
    print("✅ GENERATION COMPLETE")
    print("=" * 70)
    print(f"\n📈 Summary:")
    print(f"  • Total sentences generated: {total_generated}")
    print(f"  • Words processed: {len(words_to_process)}")
    print(f"  • All words should now have 10 sentences each")


if __name__ == '__main__':
    main()
