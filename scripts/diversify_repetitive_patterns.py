#!/usr/bin/env python3
"""
Diversify repetitive patterns in quiz sentences.
Identifies words with similar sentence structures and creates more varied alternatives.
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

def create_blank_sentence(sentence: str, word: str) -> str:
    """Convert a sentence with the word into a fill-in-the-blank format."""
    if not sentence or not word:
        return ""
    
    word_lower = word.lower()
    patterns = [word, word_lower]
    
    # Add word variations
    if word_lower.endswith('y'):
        patterns.extend([word_lower[:-1] + "ies", word_lower[:-1] + "ied"])
    elif word_lower.endswith('e'):
        patterns.extend([word_lower[:-1] + "ed", word_lower[:-1] + "ing"])
    
    patterns.extend([word_lower + "s", word_lower + "ed", word_lower + "ing", 
                    word_lower + "ly", word_lower + "ness"])
    
    result = sentence
    for pattern in sorted(set(patterns), key=len, reverse=True):
        regex = re.compile(r'\b' + re.escape(pattern) + r'\b', re.IGNORECASE)
        result = regex.sub("_____", result)
    
    return result

def generate_diverse_sentences(word: str, meaning: str, example_sentence: str,
                               synonym1: str, synonym2: str, existing_patterns: list,
                               level: str, num_needed: int = 10) -> list:
    """
    Generate diverse sentences across different contexts and structures.
    """
    word_lower = word.lower()
    meaning_lower = meaning.lower()
    
    is_verb = meaning_lower.startswith("to ")
    is_adjective = any(marker in meaning_lower for marker in 
                      ["having", "showing", "full of", "characterized by", 
                       "causing", "deserving", "very", "extremely"])
    
    # Create diverse sentence templates across different categories
    diverse_templates = []
    
    if is_verb:
        # Verbs: Various action contexts
        diverse_templates = [
            # Academic/formal contexts
            f"The professor asked students to _____ their findings before presenting them to the class.",
            f"Researchers must _____ the data carefully to draw accurate conclusions from their experiments.",
            
            # Everyday situations
            f"My grandmother showed me how to _____ properly when I visited her last summer.",
            f"The children learned to _____ through practice and patient guidance from their teacher.",
            
            # Professional/work contexts
            f"The manager needs to _____ the budget before submitting it to the board of directors.",
            f"She was hired specifically to _____ the new system and train all the staff members.",
            
            # Historical/narrative contexts
            f"In medieval times, people would _____ using methods that seem strange to us today.",
            f"The explorer had to _____ quickly when faced with unexpected challenges in the wilderness.",
            
            # Instructional contexts
            f"To _____ effectively, you should first read the instructions and gather all necessary materials.",
            f"The manual explains step by step how to _____ without making common mistakes."
        ]
    elif is_adjective:
        # Adjectives: Various descriptive contexts
        diverse_templates = [
            # Weather/nature descriptions
            f"The _____ weather made it perfect for our planned outdoor activities and picnic lunch.",
            f"Despite the _____ conditions, the hikers continued their journey up the mountain path.",
            
            # Character/personality descriptions
            f"Her _____ personality made her popular with everyone she met at the new school.",
            f"The _____ young man impressed the interview panel with his thoughtful answers.",
            
            # Event/situation descriptions
            f"The _____ ceremony attracted hundreds of guests from across the country and beyond.",
            f"Everyone agreed it was a _____ performance that would be remembered for years to come.",
            
            # Object/place descriptions
            f"The museum displayed a _____ collection of artifacts from ancient civilisations around the world.",
            f"They discovered a _____ garden hidden behind the old stone wall at the manor house.",
            
            # Comparative descriptions
            f"The contrast was striking: one side appeared _____ while the other seemed quite ordinary.",
            f"Although initially _____, the situation improved dramatically once they found a solution."
        ]
    else:
        # Nouns: Various contexts
        diverse_templates = [
            # Abstract concepts
            f"The _____ of ancient wisdom continues to shape how people think about important questions today.",
            f"Understanding the _____ requires careful study and analysis of all the relevant factors.",
            
            # Concrete objects/events
            f"The _____ took place in the town square where hundreds of excited spectators had gathered.",
            f"She kept the precious _____ safely locked away in a special box in her bedroom.",
            
            # Personal experiences
            f"His _____ for adventure led him to explore remote parts of the world most people never see.",
            f"The _____ lasted throughout the night, with people discussing the topic until dawn broke.",
            
            # Social/community contexts
            f"The community organised a _____ to celebrate their heritage and share it with younger generations.",
            f"Everyone contributed to the _____, working together to achieve their common goal successfully.",
            
            # Historical/cultural contexts
            f"The _____ has been passed down through generations, keeping the old traditions alive today.",
            f"Historians study the _____ to understand how people lived and thought in earlier times."
        ]
    
    # Generate sentences and check they're different from existing patterns
    generated = []
    for template in diverse_templates:
        blank_sent = create_blank_sentence(template, word)
        if "_____" not in blank_sent:
            continue
        
        # Check pattern isn't too similar to existing ones
        pattern = re.sub(r'\b\w+\b', '<w>', blank_sent.lower())
        pattern = re.sub(r'_____', '<blank>', pattern)
        
        # Check this pattern is sufficiently different
        is_different = True
        for existing in existing_patterns:
            # Simple similarity check
            if pattern == existing:
                is_different = False
                break
        
        if is_different and len(blank_sent.split()) >= 10:
            generated.append(blank_sent)
        
        if len(generated) >= num_needed:
            break
    
    # If we still need more and have example sentence, use it
    if len(generated) < num_needed and example_sentence:
        blank_example = create_blank_sentence(example_sentence, word)
        if "_____" in blank_example and len(blank_example.split()) >= 8:
            generated.insert(0, blank_example)
    
    return generated[:num_needed]

def main():
    """Main function to diversify repetitive patterns."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    print("=" * 70)
    print("DIVERSIFYING REPETITIVE PATTERNS")
    print("=" * 70)
    
    # Load vocabulary content
    print("\n📖 Loading vocabulary data...")
    vocab_content = {}
    with open(data_dir / 'vocabulary_content_new.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word'].strip().lower()
            vocab_content[word] = {
                'word': row['word'].strip(),
                'meaning': row['meaning'].strip(),
                'synonym1': row['synonym1'].strip(),
                'synonym2': row['synonym2'].strip(),
                'example_sentence': row['example_sentence'].strip()
            }
    
    print(f"  ✓ Loaded {len(vocab_content)} words")
    
    # Identify words with repetitive patterns
    print("\n🔍 Identifying repetitive patterns...")
    word_sentences = defaultdict(list)
    
    for level_num in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip().lower()
                sentence = row['sentence'].strip()
                word_sentences[word].append({
                    'level': level_num,
                    'word': row['word'].strip(),
                    'sentence': sentence
                })
    
    # Find words with repetitive patterns
    repetitive_words = []
    for word, sentences in word_sentences.items():
        if len(sentences) >= 10:
            # Extract patterns
            patterns = []
            for sent_data in sentences:
                pattern = re.sub(r'\b\w+\b', '<w>', sent_data['sentence'].lower())
                pattern = re.sub(r'_____', '<blank>', pattern)
                patterns.append(pattern)
            
            unique_patterns = len(set(patterns))
            total_sentences = len(sentences)
            
            # If less than 50% unique patterns, it's repetitive
            if unique_patterns < total_sentences * 0.5:
                repetitive_words.append((word, total_sentences, unique_patterns))
    
    print(f"  ✓ Found {len(repetitive_words)} words with repetitive patterns")
    
    # Fix repetitive words
    print(f"\n🔄 Diversifying sentences for {len(repetitive_words)} words...")
    total_diversified = 0
    
    for word, total_sents, unique_pats in sorted(repetitive_words, key=lambda x: x[1], reverse=True):
        if word not in vocab_content:
            continue
        
        content = vocab_content[word]
        
        # Get existing patterns
        existing_patterns = []
        for sent_data in word_sentences[word]:
            pattern = re.sub(r'\b\w+\b', '<w>', sent_data['sentence'].lower())
            pattern = re.sub(r'_____', '<blank>', pattern)
            existing_patterns.append(pattern)
        
        # Generate diverse replacements
        # Keep some original sentences, replace the most repetitive ones
        num_to_replace = max(5, total_sents - unique_pats)
        
        diverse_sentences = generate_diverse_sentences(
            word=content['word'],
            meaning=content['meaning'],
            example_sentence=content['example_sentence'],
            synonym1=content['synonym1'],
            synonym2=content['synonym2'],
            existing_patterns=list(set(existing_patterns)),
            level="",
            num_needed=num_to_replace
        )
        
        if diverse_sentences:
            # Replace some sentences with diverse ones
            # Organize by level
            level_sentences = defaultdict(list)
            for sent_data in word_sentences[word]:
                level_sentences[sent_data['level']].append(sent_data)
            
            # Replace across levels proportionally
            diverse_idx = 0
            for level_num in sorted(level_sentences.keys()):
                sents = level_sentences[level_num]
                # Replace up to half the sentences for this word in this level
                num_replace = min(len(diverse_sentences) - diverse_idx, len(sents) // 2)
                
                for i in range(num_replace):
                    if diverse_idx < len(diverse_sentences):
                        sents[i]['sentence'] = diverse_sentences[diverse_idx]
                        diverse_idx += 1
                
                level_sentences[level_num] = sents
            
            # Update word_sentences
            updated_sents = []
            for level_num in sorted(level_sentences.keys()):
                updated_sents.extend(level_sentences[level_num])
            word_sentences[word] = updated_sents
            
            total_diversified += len(diverse_sentences)
    
    # Write back all sentences
    print("\n💾 Saving diversified sentences...")
    for level_num in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        # Collect sentences for this level
        level_rows = []
        for word, sentences in word_sentences.items():
            for sent_data in sentences:
                if sent_data['level'] == level_num:
                    level_rows.append({
                        'level': str(level_num),
                        'word': sent_data['word'],
                        'sentence': sent_data['sentence']
                    })
        
        # Write to file
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['level', 'word', 'sentence'])
            writer.writeheader()
            writer.writerows(level_rows)
        
        print(f"  ✅ Saved level {level_num}")
    
    print("\n" + "=" * 70)
    print("✅ PATTERN DIVERSIFICATION COMPLETE")
    print("=" * 70)
    print(f"\nWords diversified: {len(repetitive_words)}")
    print(f"Sentences replaced: {total_diversified}")
    print("\n💡 Sentences now have more varied structures and contexts")

if __name__ == '__main__':
    main()
