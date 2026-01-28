#!/usr/bin/env python3
"""
Eleven Plus Examiner - Spot Check Quality Assessment
Randomly sample 100 sentences and evaluate against eleven plus standards
"""

import csv
import random
from pathlib import Path
from typing import List, Dict

class ElevenPlusExaminer:
    def __init__(self):
        self.criteria = {
            'contextual_clues': 'Does the sentence provide clear contextual hints?',
            'age_appropriate': 'Is it suitable for 10-11 year olds?',
            'grammar_spelling': 'Is grammar and British English spelling correct?',
            'natural_language': 'Does it sound natural and well-constructed?',
            'word_specific': 'Is it specific to the word (not generic)?',
            'blank_placement': 'Is the blank placement logical and clear?'
        }
    
    def evaluate_sentence(self, word: str, sentence: str, meaning: str, level: int) -> Dict:
        """Evaluate a single sentence against all criteria"""
        issues = []
        strengths = []
        
        # Check 1: Contextual clues
        if len(sentence) < 40:
            issues.append("Too short - may lack context")
        elif self._has_contextual_clues(sentence, word, meaning):
            strengths.append("Strong contextual clues")
        
        # Check 2: Age-appropriateness
        if self._is_age_appropriate(sentence, level):
            strengths.append("Age-appropriate content")
        else:
            issues.append("May not be age-appropriate")
        
        # Check 3: Grammar and spelling
        grammar_issues = self._check_grammar(sentence)
        if grammar_issues:
            issues.extend(grammar_issues)
        else:
            strengths.append("Correct grammar and spelling")
        
        # Check 4: Natural language
        if self._is_natural(sentence):
            strengths.append("Natural, well-constructed")
        else:
            issues.append("Awkward phrasing")
        
        # Check 5: Word-specific (not generic)
        if self._is_generic_template(sentence):
            issues.append("CRITICAL: Generic template detected")
        else:
            strengths.append("Word-specific sentence")
        
        # Check 6: Blank placement
        if "_____" not in sentence:
            issues.append("CRITICAL: No blank placeholder")
        elif sentence.count("_____") > 1:
            issues.append("Multiple blanks detected")
        else:
            strengths.append("Correct blank placement")
        
        # Overall rating
        if len(issues) == 0:
            rating = "EXCELLENT"
        elif len(issues) <= 2 and "CRITICAL" not in str(issues):
            rating = "GOOD"
        elif "CRITICAL" in str(issues):
            rating = "POOR"
        else:
            rating = "FAIR"
        
        return {
            'rating': rating,
            'strengths': strengths,
            'issues': issues
        }
    
    def _has_contextual_clues(self, sentence: str, word: str, meaning: str) -> bool:
        """Check if sentence provides contextual clues"""
        # Remove blank and word
        context = sentence.replace("_____", "").replace(word, "").lower()
        
        # Check length
        if len(context) < 50:
            return False
        
        # Check for meaning-related words
        meaning_words = [w for w in meaning.lower().split() if len(w) > 4]
        overlap = sum(1 for w in meaning_words if w in context)
        
        # Check for specific scenarios/contexts
        specific_markers = [
            'when', 'after', 'because', 'during', 'while',
            'caused', 'made', 'showed', 'revealed', 'demonstrated'
        ]
        has_markers = sum(1 for m in specific_markers if m in context)
        
        return overlap >= 1 or has_markers >= 2
    
    def _is_age_appropriate(self, sentence: str, level: int) -> bool:
        """Check if suitable for 10-11 year olds"""
        # Check for inappropriate content markers
        inappropriate = ['death', 'killing', 'murdered', 'violent', 'sexual']
        if any(word in sentence.lower() for word in inappropriate):
            return False
        
        # Level-appropriate complexity
        word_count = len(sentence.split())
        if level == 1 and word_count > 25:
            return False
        if level == 4 and word_count < 8:
            return False
        
        return True
    
    def _check_grammar(self, sentence: str) -> List[str]:
        """Check for grammar and spelling issues"""
        issues = []
        
        # American spelling check
        american_spellings = {
            'realize': 'realise', 'color': 'colour', 'center': 'centre',
            'organize': 'organise', 'honor': 'honour', 'favor': 'favour'
        }
        for american, british in american_spellings.items():
            if american in sentence.lower() and british not in sentence.lower():
                issues.append(f"American spelling: '{american}' should be '{british}'")
        
        # Basic grammar checks
        if sentence and not sentence[0].isupper():
            issues.append("Should start with capital letter")
        
        if sentence and sentence[-1] not in '.!?':
            issues.append("Should end with punctuation")
        
        # Double spaces
        if '  ' in sentence:
            issues.append("Contains double spaces")
        
        return issues
    
    def _is_natural(self, sentence: str) -> bool:
        """Check if sentence sounds natural"""
        # Check for awkward constructions
        awkward_patterns = [
            'the the', 'a a', 'an an',
            'very very', 'really really',
            'is is', 'was was', 'are are'
        ]
        
        lower = sentence.lower()
        for pattern in awkward_patterns:
            if pattern in lower:
                return False
        
        # Check for overly complex nested clauses
        if sentence.count(',') > 4:
            return False
        
        return True
    
    def _is_generic_template(self, sentence: str) -> bool:
        """Check if sentence uses generic template"""
        generic_patterns = [
            "they decided to _____ when the situation became difficult",
            "she had to _____ quickly to solve the urgent problem",
            "he learned to _____ after many years of practice",
            "we should _____ before it's too late",
            "the team worked together to _____ the challenge",
            "nobody wanted to _____ in such circumstances",
            "she managed to _____ despite the obstacles",
            "they were forced to _____ when they had no other choice",
            "he refused to _____ even when others insisted"
        ]
        
        lower = sentence.lower()
        for pattern in generic_patterns:
            if pattern in lower:
                return True
        
        return False


def main():
    print("=" * 80)
    print("ELEVEN PLUS EXAMINER - SPOT CHECK QUALITY ASSESSMENT")
    print("Random Sample: 100 Sentences (25 per level)")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    # Load vocabulary meanings
    vocab_meanings = {}
    with open(data_dir / 'vocabulary_content_new.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vocab_meanings[row['word'].lower()] = row['meaning']
    
    # Initialize examiner
    examiner = ElevenPlusExaminer()
    
    # Collect random samples from each level
    all_samples = []
    
    for level_num in [1, 2, 3, 4]:
        filename = data_dir / f'quiz_sentences_level{level_num}.csv'
        
        # Load all sentences from this level
        level_sentences = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                level_sentences.append({
                    'level': level_num,
                    'word': row['word'],
                    'sentence': row['sentence'],
                    'meaning': vocab_meanings.get(row['word'].lower(), "")
                })
        
        # Random sample 25 from this level
        samples = random.sample(level_sentences, min(25, len(level_sentences)))
        all_samples.extend(samples)
    
    print(f"📋 Examining {len(all_samples)} randomly selected sentences...\n")
    
    # Evaluate each sample
    ratings = {'EXCELLENT': [], 'GOOD': [], 'FAIR': [], 'POOR': []}
    
    for i, sample in enumerate(all_samples, 1):
        evaluation = examiner.evaluate_sentence(
            sample['word'],
            sample['sentence'],
            sample['meaning'],
            sample['level']
        )
        
        ratings[evaluation['rating']].append({
            'num': i,
            'level': sample['level'],
            'word': sample['word'],
            'sentence': sample['sentence'],
            'evaluation': evaluation
        })
    
    # Generate report
    print("=" * 80)
    print("ASSESSMENT RESULTS")
    print("=" * 80)
    print()
    
    print(f"📊 Overall Ratings:")
    print(f"   EXCELLENT: {len(ratings['EXCELLENT'])} ({len(ratings['EXCELLENT'])}%)")
    print(f"   GOOD:      {len(ratings['GOOD'])} ({len(ratings['GOOD'])}%)")
    print(f"   FAIR:      {len(ratings['FAIR'])} ({len(ratings['FAIR'])}%)")
    print(f"   POOR:      {len(ratings['POOR'])} ({len(ratings['POOR'])}%)")
    print()
    
    # Show examples
    print("=" * 80)
    print("EXCELLENT EXAMPLES (showing first 10)")
    print("=" * 80)
    for item in ratings['EXCELLENT'][:10]:
        print(f"\n#{item['num']} - Level {item['level']} - {item['word']}")
        print(f"   Sentence: {item['sentence']}")
        print(f"   Strengths: {', '.join(item['evaluation']['strengths'])}")
    
    if ratings['GOOD']:
        print("\n" + "=" * 80)
        print("GOOD EXAMPLES (showing first 5)")
        print("=" * 80)
        for item in ratings['GOOD'][:5]:
            print(f"\n#{item['num']} - Level {item['level']} - {item['word']}")
            print(f"   Sentence: {item['sentence']}")
            print(f"   Strengths: {', '.join(item['evaluation']['strengths'])}")
            if item['evaluation']['issues']:
                print(f"   Minor Issues: {', '.join(item['evaluation']['issues'])}")
    
    if ratings['FAIR']:
        print("\n" + "=" * 80)
        print("FAIR EXAMPLES (needs minor improvement)")
        print("=" * 80)
        for item in ratings['FAIR']:
            print(f"\n#{item['num']} - Level {item['level']} - {item['word']}")
            print(f"   Sentence: {item['sentence']}")
            print(f"   Issues: {', '.join(item['evaluation']['issues'])}")
    
    if ratings['POOR']:
        print("\n" + "=" * 80)
        print("⚠️  POOR EXAMPLES (needs immediate attention)")
        print("=" * 80)
        for item in ratings['POOR']:
            print(f"\n#{item['num']} - Level {item['level']} - {item['word']}")
            print(f"   Sentence: {item['sentence']}")
            print(f"   CRITICAL ISSUES: {', '.join(item['evaluation']['issues'])}")
    
    # Final assessment
    print("\n" + "=" * 80)
    print("EXAMINER'S FINAL ASSESSMENT")
    print("=" * 80)
    
    excellent_pct = len(ratings['EXCELLENT'])
    good_pct = len(ratings['GOOD'])
    quality_pct = excellent_pct + good_pct
    
    print(f"\n📈 Quality Score: {quality_pct}% (Excellent + Good)")
    
    if quality_pct >= 90:
        grade = "A+"
        verdict = "OUTSTANDING - Exceeds eleven plus standards"
    elif quality_pct >= 80:
        grade = "A"
        verdict = "EXCELLENT - Meets eleven plus standards"
    elif quality_pct >= 70:
        grade = "B+"
        verdict = "VERY GOOD - Suitable for eleven plus"
    elif quality_pct >= 60:
        grade = "B"
        verdict = "GOOD - Generally suitable"
    else:
        grade = "C"
        verdict = "NEEDS IMPROVEMENT"
    
    print(f"\n🎓 FINAL GRADE: {grade}")
    print(f"   Verdict: {verdict}")
    
    if ratings['POOR']:
        print(f"\n⚠️  Recommendation: Review and replace {len(ratings['POOR'])} poor quality sentences")
    else:
        print(f"\n✅ Recommendation: Database is production-ready")
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    random.seed(42)  # For reproducibility
    main()
