#!/usr/bin/env python3
"""
Quick quality examination of Level 1 regenerated quiz sentences.
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

def analyze_sentence_quality(sentence, word, meaning):
    """Analyze a single sentence for quality indicators"""
    issues = []
    word_lower = word.lower()
    
    # Check for generic templates
    generic_patterns = [
        "They decided to _____ when the situation became difficult",
        "She had to _____ quickly to solve the urgent problem",
        "He learned to _____ after many years of practice",
        "We should _____ before it's too late",
        "The team worked together to _____ the challenge successfully",
    ]
    
    for pattern in generic_patterns:
        if sentence.lower().startswith(pattern.lower()[:30]):
            issues.append("GENERIC_TEMPLATE")
            break
    
    # Check for contextual clues
    if len(sentence) < 40:
        issues.append("TOO_SHORT")
    
    # Check for blank presence
    if "_____" not in sentence:
        issues.append("NO_BLANK")
    
    return issues

def main():
    data_dir = Path(__file__).parent.parent / 'data'
    
    print("=" * 70)
    print("LEVEL 1 QUALITY EXAMINATION")
    print("=" * 70)
    print()
    
    # Load vocabulary meanings
    vocab_meanings = {}
    with open(data_dir / 'vocabulary_content_new.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vocab_meanings[row['word'].lower()] = row['meaning']
    
    # Analyze sentences
    total_sentences = 0
    issues_by_type = defaultdict(int)
    words_with_issues = []
    
    with open(data_dir / 'quiz_sentences_level1.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        current_word = None
        word_issues = []
        
        for row in reader:
            word = row['word']
            sentence = row['sentence']
            total_sentences += 1
            
            if current_word != word:
                if current_word and word_issues:
                    words_with_issues.append((current_word, word_issues))
                current_word = word
                word_issues = []
            
            meaning = vocab_meanings.get(word.lower(), "")
            issues = analyze_sentence_quality(sentence, word, meaning)
            
            for issue in issues:
                issues_by_type[issue] += 1
                word_issues.append((sentence, issues))
    
    # Final word
    if current_word and word_issues:
        words_with_issues.append((current_word, word_issues))
    
    # Report
    print(f"📊 Analysis Results:")
    print(f"   Total sentences: {total_sentences}")
    print(f"   Total words: {total_sentences // 10}")
    print()
    
    if issues_by_type:
        print(f"⚠️  Issues found:")
        for issue_type, count in sorted(issues_by_type.items(), key=lambda x: -x[1]):
            pct = (count / total_sentences) * 100
            print(f"   {issue_type}: {count} ({pct:.1f}%)")
    else:
        print("✅ No issues detected!")
    
    print()
    
    if words_with_issues:
        print(f"📝 Words with issues: {len(words_with_issues)}")
        print(f"   Showing first 5:")
        for word, issues in words_with_issues[:5]:
            print(f"   - {word}: {len(issues)} sentences with issues")
    else:
        print("✅ All words have high-quality sentences!")
    
    print()
    print("=" * 70)
    
    # Calculate quality grade
    if not issues_by_type:
        grade = "A+"
    elif sum(issues_by_type.values()) < total_sentences * 0.1:
        grade = "A"
    elif sum(issues_by_type.values()) < total_sentences * 0.2:
        grade = "B"
    else:
        grade = "C"
    
    print(f"📈 OVERALL QUALITY GRADE: {grade}")
    print("=" * 70)

if __name__ == '__main__':
    main()
