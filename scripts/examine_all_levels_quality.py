#!/usr/bin/env python3
"""
Comprehensive quality examination of ALL regenerated quiz sentences.
Acting as an eleven plus examiner.
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

def has_generic_template(sentence):
    """Check if sentence uses generic template"""
    generic = [
        "They decided to _____ when the situation became difficult",
        "She had to _____ quickly to solve the urgent problem",
        "He learned to _____ after many years of practice",
        "We should _____ before it's too late",
    ]
    lower = sentence.lower()
    for pattern in generic:
        if lower.startswith(pattern.lower()[:35]):
            return True
    return False

def analyze_contextual_clues(sentence, word, meaning):
    """Assess if sentence provides contextual clues"""
    # Remove the word and blank
    context = sentence.replace("_____", "").lower()
    meaning_words = set(meaning.lower().split())
    
    # Check for meaning-related words in context
    overlap = sum(1 for w in meaning_words if len(w) > 3 and w in context)
    
    if len(context) < 40:
        return "WEAK"
    elif overlap >= 2:
        return "STRONG"
    elif len(context) >= 60:
        return "MODERATE"
    else:
        return "WEAK"

def main():
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    print("=" * 80)
    print("COMPREHENSIVE QUALITY EXAMINATION - ALL LEVELS")
    print("Acting as Eleven Plus Examiner")
    print("=" * 80)
    print()
    
    # Load vocabulary meanings
    vocab_meanings = {}
    with open(data_dir / 'vocabulary_content_new.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vocab_meanings[row['word'].lower()] = row['meaning']
    
    # Analyze each level
    results_by_level = {}
    
    for level_num in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        print(f"📚 Examining Level {level_num}...")
        
        total = 0
        generic_count = 0
        no_blank = 0
        contextual_strength = {"STRONG": 0, "MODERATE": 0, "WEAK": 0}
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word']
                sentence = row['sentence']
                total += 1
                
                # Check for issues
                if has_generic_template(sentence):
                    generic_count += 1
                
                if "_____" not in sentence:
                    no_blank += 1
                
                # Assess contextual clues
                meaning = vocab_meanings.get(word.lower(), "")
                strength = analyze_contextual_clues(sentence, word, meaning)
                contextual_strength[strength] += 1
        
        results_by_level[level_num] = {
            'total': total,
            'generic': generic_count,
            'no_blank': no_blank,
            'contextual': contextual_strength
        }
        
        print(f"   Total sentences: {total}")
        print(f"   Generic templates: {generic_count} ({100*generic_count/total:.1f}%)")
        print(f"   Missing blanks: {no_blank} ({100*no_blank/total:.1f}%)")
        print(f"   Strong contextual clues: {contextual_strength['STRONG']} ({100*contextual_strength['STRONG']/total:.1f}%)")
        print(f"   Moderate contextual clues: {contextual_strength['MODERATE']} ({100*contextual_strength['MODERATE']/total:.1f}%)")
        print(f"   Weak contextual clues: {contextual_strength['WEAK']} ({100*contextual_strength['WEAK']/total:.1f}%)")
        print()
    
    # Overall summary
    print("=" * 80)
    print("OVERALL ASSESSMENT")
    print("=" * 80)
    
    grand_total = sum(r['total'] for r in results_by_level.values())
    total_generic = sum(r['generic'] for r in results_by_level.values())
    total_strong = sum(r['contextual']['STRONG'] for r in results_by_level.values())
    
    print(f"\n📊 Statistics:")
    print(f"   Total sentences examined: {grand_total:,}")
    print(f"   Generic templates: {total_generic} ({100*total_generic/grand_total:.1f}%)")
    print(f"   Strong contextual clues: {total_strong} ({100*total_strong/grand_total:.1f}%)")
    
    # Grade calculation
    generic_pct = 100 * total_generic / grand_total
    strong_pct = 100 * total_strong / grand_total
    
    if generic_pct < 5 and strong_pct > 70:
        grade = "A+"
        assessment = "EXCELLENT - Meets eleven plus standards"
    elif generic_pct < 10 and strong_pct > 60:
        grade = "A"
        assessment = "VERY GOOD - Suitable for eleven plus"
    elif generic_pct < 20 and strong_pct > 50:
        grade = "B"
        assessment = "GOOD - Generally suitable"
    else:
        grade = "C"
        assessment = "NEEDS IMPROVEMENT"
    
    print(f"\n🎓 FINAL GRADE: {grade}")
    print(f"   Assessment: {assessment}")
    print()
    print("=" * 80)
    
    # Write summary report
    report_file = base_dir / 'QUIZ_SENTENCES_REGENERATION_REPORT.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Quiz Sentences Regeneration - Quality Report\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"**Grade: {grade}**\n\n")
        f.write(f"**Assessment:** {assessment}\n\n")
        f.write(f"- Total sentences: {grand_total:,}\n")
        f.write(f"- Generic templates: {100*total_generic/grand_total:.1f}%\n")
        f.write(f"- Strong contextual clues: {100*total_strong/grand_total:.1f}%\n\n")
        
        f.write("## Results by Level\n\n")
        for level_num in [1, 2, 3, 4]:
            r = results_by_level[level_num]
            f.write(f"### Level {level_num}\n\n")
            f.write(f"- Sentences: {r['total']}\n")
            f.write(f"- Generic: {100*r['generic']/r['total']:.1f}%\n")
            f.write(f"- Strong context: {100*r['contextual']['STRONG']/r['total']:.1f}%\n\n")
    
    print(f"✅ Report saved to: {report_file.name}")

if __name__ == '__main__':
    main()
