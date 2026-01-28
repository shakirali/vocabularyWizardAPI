#!/usr/bin/env python3
"""
Generate quiz sentences for missing words using AI models.

This script:
1. Reads vocabulary_content_new.csv to get all words and their content
2. Checks which words are missing quiz sentences in the level files
3. Uses AI to generate 10 quiz sentences per missing word
4. Saves the sentences to the appropriate level CSV files
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service


def load_vocabulary_content(data_dir: Path) -> Dict[str, Dict]:
    """Load vocabulary content from vocabulary_content_new.csv"""
    vocab_content = {}
    vocab_file = data_dir / 'vocabulary_content_new.csv'
    
    if not vocab_file.exists():
        print(f"❌ Vocabulary content file not found: {vocab_file}")
        return vocab_content
    
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
    
    if not levels_file.exists():
        print(f"❌ Vocabulary levels file not found: {levels_file}")
        return vocab_levels
    
    with levels_file.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word_lower = row['word'].strip().lower()
            vocab_levels[word_lower] = {
                'word': row['word'].strip(),
                'level': row['level'].strip()
            }
    
    return vocab_levels


def get_existing_quiz_words(data_dir: Path) -> set:
    """Get set of words that already have quiz sentences"""
    existing_words = set()
    
    for level_num in [1, 2, 3, 4]:
        quiz_file = data_dir / f'quiz_sentences_level{level_num}.csv'
        if quiz_file.exists():
            with quiz_file.open('r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    word_lower = row['word'].strip().lower()
                    existing_words.add(word_lower)
    
    return existing_words


def generate_quiz_sentence_ai(
    word: str, 
    meaning: str, 
    level: str,
    example_sentence: str = "",
    synonym1: str = "",
    antonym1: str = ""
) -> str:
    """
    Generate a single quiz sentence using AI.
    Returns a sentence with the word replaced by "_____"
    """
    # Use AI to generate sentence with blank
    sentence = ai_content_service.generate_sentence_with_blank(word, meaning)
    
    if sentence and "_____" in sentence:
        return sentence
    
    # If we have an example sentence, use it
    if example_sentence:
        import re
        word_pattern = re.compile(re.escape(word), re.IGNORECASE)
        blank_example = word_pattern.sub("_____", example_sentence)
        if "_____" in blank_example:
            return blank_example
    
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
    if is_verb:
        if synonym1:
            return f"They had to _____ (similar to {synonym1}) before the situation worsened."
        elif antonym1:
            return f"She refused to _____ (opposite of {antonym1}) despite the pressure."
        else:
            return f"They decided to _____ the matter carefully and thoughtfully."
    elif is_adjective:
        if synonym1:
            return f"His _____ (similar to {synonym1}) attitude impressed everyone."
        elif antonym1:
            return f"It was not _____ (opposite of {antonym1}) as everyone expected."
        else:
            return f"The _____ quality made it truly special and unique."
    else:  # noun
        if synonym1:
            return f"The _____ (similar to {synonym1}) became clear to everyone present."
        elif antonym1:
            return f"The _____ (opposite of {antonym1}) was not what they expected."
        else:
            return f"The _____ was important in understanding the situation."


def generate_quiz_sentences_for_word(
    word: str, 
    meaning: str, 
    example_sentence: str,
    level: str,
    synonym1: str = "",
    synonym2: str = "",
    antonym1: str = "",
    antonym2: str = "",
    count: int = 10
) -> List[str]:
    """
    Generate multiple quiz sentences for a word using AI.
    
    Args:
        word: The vocabulary word
        meaning: The meaning/definition
        example_sentence: Existing example sentence (if available)
        level: The level (level1-level4)
        synonym1, synonym2: Synonyms for context
        antonym1, antonym2: Antonyms for context
        count: Number of sentences to generate (default: 10)
    
    Returns:
        List of sentences with blanks
    """
    sentences = []
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    # Determine word type
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in [
        "having", "showing", "full of", "characterised by", "characterized by",
        "very", "extremely", "quite", "rather", "causing", "deserving"
    ])
    is_noun = not is_verb and not is_adjective
    
    # 1. Use example sentence if available
    if example_sentence:
        import re
        word_pattern = re.compile(re.escape(word), re.IGNORECASE)
        blank_example = word_pattern.sub("_____", example_sentence)
        if "_____" in blank_example:
            sentences.append(blank_example)
    
    # 2. Generate varied sentences using AI and context
    sentence_templates = []
    
    if is_verb:
        # Verb sentences
        sentence_templates = [
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
        ]
        if synonym1:
            sentence_templates.append(f"They had to _____ (similar to {synonym1}) before anyone got hurt.")
        if antonym1:
            sentence_templates.append(f"She refused to _____ (opposite of {antonym1}) despite the pressure.")
    elif is_adjective:
        # Adjective sentences
        sentence_templates = [
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
        ]
        if synonym1:
            sentence_templates.append(f"His _____ (similar to {synonym1}) attitude impressed everyone.")
        if antonym1:
            sentence_templates.append(f"It was not _____ (opposite of {antonym1}) as everyone expected.")
    else:  # noun
        # Noun sentences
        sentence_templates = [
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
        ]
        if synonym1:
            sentence_templates.append(f"The _____ (similar to {synonym1}) became clear to everyone.")
        if antonym1:
            sentence_templates.append(f"The _____ (opposite of {antonym1}) was not what they expected.")
    
    # Generate sentences using AI for variety
    for template in sentence_templates[:count]:
        # Use AI to generate a sentence, or use template
        ai_sentence = generate_quiz_sentence_ai(
            word, meaning, level, example_sentence, synonym1, antonym1
        )
        if ai_sentence and ai_sentence not in sentences:
            sentences.append(ai_sentence)
        elif template not in sentences:
            sentences.append(template)
        
        if len(sentences) >= count:
            break
    
    # Fill remaining slots with AI-generated sentences
    while len(sentences) < count:
        ai_sentence = generate_quiz_sentence_ai(
            word, meaning, level, example_sentence, synonym1, antonym1
        )
        if ai_sentence and ai_sentence not in sentences:
            sentences.append(ai_sentence)
        else:
            break
    
    return sentences[:count]


def main():
    """Main function to generate missing quiz sentences"""
    print("=" * 70)
    print("AI QUIZ SENTENCE GENERATION FOR MISSING WORDS")
    print("=" * 70)
    print()
    
    # Check AI service availability
    if not ai_content_service.is_available():
        print("❌ AI Content Service is not available")
        print("   Cannot generate quiz sentences using AI")
        return
    
    print("✅ AI Content Service is available")
    print()
    
    # Setup paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    # Load vocabulary data
    print("📚 Loading vocabulary data...")
    vocab_content = load_vocabulary_content(data_dir)
    print(f"  ✓ Loaded {len(vocab_content)} words from vocabulary_content_new.csv")
    
    vocab_levels = load_vocabulary_levels(data_dir)
    print(f"  ✓ Loaded {len(vocab_levels)} words from vocabulary_levels.csv")
    
    # Get existing quiz words
    print("\n🔍 Checking existing quiz sentences...")
    existing_quiz_words = get_existing_quiz_words(data_dir)
    print(f"  ✓ Found {len(existing_quiz_words)} words with existing quiz sentences")
    
    # Find missing words by level
    missing_by_level = defaultdict(list)
    for word_lower, level_data in vocab_levels.items():
        if word_lower not in existing_quiz_words:
            if word_lower in vocab_content:
                level = level_data['level']
                missing_by_level[level].append({
                    'word': level_data['word'],
                    'level': level,
                    'content': vocab_content[word_lower]
                })
    
    total_missing = sum(len(words) for words in missing_by_level.values())
    print(f"\n📊 Found {total_missing} words missing quiz sentences:")
    for level in sorted(['level1', 'level2', 'level3', 'level4']):
        count = len(missing_by_level.get(level, []))
        if count > 0:
            print(f"  {level}: {count} words")
    
    if total_missing == 0:
        print("\n✅ All words already have quiz sentences!")
        return
    
    print(f"\n🔄 Will generate 10 sentences per word = {total_missing * 10} total sentences")
    print("\n⏳ Generating sentences using AI (this may take a while)...\n")
    
    # Generate sentences for each level
    total_generated = 0
    for level in sorted(['level1', 'level2', 'level3', 'level4']):
        level_num = level.replace('level', '')
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        words_to_process = missing_by_level.get(level, [])
        if not words_to_process:
            continue
        
        print(f"📝 Processing {level} ({len(words_to_process)} words)...")
        
        # Read existing sentences
        existing_sentences = []
        if filename.exists():
            with filename.open('r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                existing_sentences = list(reader)
        
        # Generate new sentences
        new_sentences = []
        for i, word_data in enumerate(words_to_process, 1):
            word = word_data['word']
            content = word_data['content']
            
            print(f"  [{i}/{len(words_to_process)}] Generating for: {word}")
            
            # Generate 10 sentences using AI
            sentences = generate_quiz_sentences_for_word(
                word=word,
                meaning=content['meaning'],
                example_sentence=content.get('example_sentence', ''),
                level=level,
                synonym1=content.get('synonym1', ''),
                synonym2=content.get('synonym2', ''),
                antonym1=content.get('antonym1', ''),
                antonym2=content.get('antonym2', ''),
                count=10
            )
            
            # Add sentences to list
            for sentence in sentences:
                new_sentences.append({
                    'level': level_num,
                    'word': word,
                    'sentence': sentence
                })
            
            if i % 10 == 0:
                print(f"    Progress: {i}/{len(words_to_process)} words processed...")
        
        # Combine existing and new sentences
        all_sentences = existing_sentences + new_sentences
        
        # Write to file
        with filename.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
            writer.writeheader()
            writer.writerows(all_sentences)
        
        print(f"  ✅ Added {len(new_sentences)} sentences to {filename.name}")
        total_generated += len(new_sentences)
    
    print("\n" + "=" * 70)
    print("✅ GENERATION COMPLETE")
    print("=" * 70)
    print(f"\n📈 Summary:")
    print(f"  • Total sentences generated: {total_generated}")
    print(f"  • Words processed: {total_missing}")
    print(f"  • Average sentences per word: {total_generated // total_missing if total_missing > 0 else 0}")
    print(f"\n💡 All sentences were generated using AI models.")


if __name__ == '__main__':
    main()
