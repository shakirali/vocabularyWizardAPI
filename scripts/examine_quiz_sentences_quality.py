#!/usr/bin/env python3
"""
Eleven Plus Quiz Sentence Quality Examination

As an eleven plus examiner, this script examines all quiz sentences for:
- Educational quality standards
- Contextual clarity and strong clues
- Age-appropriateness
- British English usage
- Sentence variety
- Unambiguous answers
- Proper difficulty progression
"""

import csv
import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


class QuizSentenceExaminer:
    """Eleven Plus examiner for quiz sentence quality"""
    
    def __init__(self):
        self.issues = defaultdict(list)
        self.statistics = {
            'total_sentences': 0,
            'total_words': 0,
            'excellent_sentences': 0,
            'good_sentences': 0,
            'poor_sentences': 0,
            'critical_issues': 0,
        }
        
        # Generic templates that indicate poor quality
        self.generic_templates = [
            "The committee decided to _____ the proposal after careful consideration of all factors.",
            "They had to _____ the situation before it got worse.",
            "She decided to _____ the problem quickly and efficiently.",
            "He tried to _____ what was happening, but it was difficult.",
            "We need to _____ this matter carefully and thoughtfully.",
            "You should _____ before making any important decisions.",
            "It's crucial to _____ properly in such circumstances.",
            "They managed to _____ successfully despite many obstacles.",
            "She learned to _____ effectively through careful practice.",
            "The _____ was clear to everyone present at the meeting.",
            "She understood the _____ of the situation immediately.",
            "His _____ surprised those around him greatly.",
            "The _____ became evident very quickly to all observers.",
            "Everyone noticed the _____ in the way he spoke.",
            "The _____ provided important context for the story.",
            "Her _____ was obvious from her actions.",
            "The _____ helped explain what had happened.",
            "The _____ provided crucial context for understanding the broader implications.",
            "The situation was very _____ and quite concerning to everyone.",
            "She showed a _____ attitude that impressed her teachers.",
            "His behaviour was quite _____ and rather unexpected.",
            "It was a _____ experience that everyone remembered fondly.",
            "The _____ nature of the event surprised us all greatly.",
            "They found it _____ and quite interesting to observe.",
            "Her response was _____ and very thoughtful indeed.",
            "The _____ quality made it truly special and unique.",
            "His _____ approach to the problem showed remarkable insight and understanding.",
        ]
        
    def examine_all(self):
        """Examine all quiz sentences across all levels"""
        print("=" * 80)
        print("ELEVEN PLUS QUIZ SENTENCE QUALITY EXAMINATION")
        print("=" * 80)
        print()
        
        all_sentences = {}
        vocab_content = self.load_vocabulary_content()
        
        # Examine each level
        for level_num in [1, 2, 3, 4]:
            level_sentences = self.load_quiz_sentences(level_num)
            all_sentences[level_num] = level_sentences
            
            print(f"\n{'='*80}")
            print(f"EXAMINING LEVEL {level_num} SENTENCES")
            print(f"{'='*80}")
            
            self.examine_level(level_num, level_sentences, vocab_content)
        
        # Cross-level analysis
        self.analyze_repetition(all_sentences)
        
        # Generate comprehensive report
        self.generate_report(vocab_content)
    
    def load_vocabulary_content(self) -> Dict[str, Dict]:
        """Load vocabulary content for context"""
        vocab_content = {}
        vocab_file = DATA_DIR / 'vocabulary_content_new.csv'
        
        if not vocab_file.exists():
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
    
    def load_quiz_sentences(self, level_num: int) -> List[Dict]:
        """Load quiz sentences for a level"""
        sentences = []
        quiz_file = DATA_DIR / f'quiz_sentences_level{level_num}.csv'
        
        if not quiz_file.exists():
            return sentences
        
        with quiz_file.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sentences.append({
                    'word': row['word'].strip(),
                    'sentence': row['sentence'].strip(),
                    'level': level_num
                })
        
        return sentences
    
    def examine_level(self, level_num: int, sentences: List[Dict], vocab_content: Dict):
        """Examine sentences for a specific level"""
        print(f"\nTotal sentences in Level {level_num}: {len(sentences)}")
        
        words_seen = set()
        sentences_by_word = defaultdict(list)
        
        for entry in sentences:
            word = entry['word']
            sentence = entry['sentence']
            word_lower = word.lower()
            words_seen.add(word_lower)
            sentences_by_word[word_lower].append(sentence)
            self.statistics['total_sentences'] += 1
        
        self.statistics['total_words'] += len(words_seen)
        
        print(f"Unique words: {len(words_seen)}")
        print(f"Average sentences per word: {len(sentences) / len(words_seen) if words_seen else 0:.1f}")
        
        # Examine each word's sentences
        issues_found = 0
        for word_lower, word_sentences in sentences_by_word.items():
            word_issues = self.examine_word_sentences(
                word_lower, 
                word_sentences, 
                level_num,
                vocab_content.get(word_lower, {})
            )
            if word_issues:
                issues_found += len(word_issues)
                self.issues[word_lower].extend(word_issues)
        
        print(f"\nIssues found: {issues_found}")
    
    def examine_word_sentences(
        self, 
        word: str, 
        sentences: List[str], 
        level: int,
        vocab_data: Dict
    ) -> List[str]:
        """Examine sentences for a specific word"""
        issues = []
        word_lower = word.lower()
        meaning = vocab_data.get('meaning', '').lower() if vocab_data else ''
        
        # Check for generic templates
        generic_count = 0
        for sentence in sentences:
            if sentence in self.generic_templates:
                generic_count += 1
                issues.append(f"Uses generic template: '{sentence[:60]}...'")
        
        if generic_count > 0:
            issues.append(f"CRITICAL: {generic_count}/{len(sentences)} sentences use generic templates")
            self.statistics['critical_issues'] += generic_count
        
        # Check for repetition
        if len(sentences) != len(set(sentences)):
            duplicates = len(sentences) - len(set(sentences))
            issues.append(f"Has {duplicates} duplicate sentences")
        
        # Check for contextual clues
        weak_clue_count = 0
        for sentence in sentences:
            if not self.has_strong_contextual_clues(sentence, word_lower, meaning):
                weak_clue_count += 1
        
        if weak_clue_count > len(sentences) * 0.5:  # More than 50% weak
            issues.append(f"WEAK CLUES: {weak_clue_count}/{len(sentences)} sentences lack strong contextual clues")
        
        # Check sentence variety
        if len(set(sentences)) < 5 and len(sentences) >= 10:
            issues.append(f"LOW VARIETY: Only {len(set(sentences))} unique sentences out of {len(sentences)}")
        
        # Check for proper blank placement
        for sentence in sentences:
            if sentence.count("_____") != 1:
                issues.append(f"INCORRECT BLANKS: Sentence has {sentence.count('_____')} blanks: '{sentence[:60]}...'")
        
        # Check for age-appropriateness
        inappropriate_count = 0
        for sentence in sentences:
            if not self.is_age_appropriate(sentence, level):
                inappropriate_count += 1
        
        if inappropriate_count > 0:
            issues.append(f"AGE INAPPROPRIATE: {inappropriate_count} sentences may be too complex for level {level}")
        
        # Check British English
        american_spellings = self.check_british_english(sentences)
        if american_spellings:
            issues.append(f"AMERICAN ENGLISH: Found {len(american_spellings)} sentences with American spellings")
        
        # Score sentence quality
        excellent = 0
        good = 0
        poor = 0
        
        for sentence in sentences:
            score = self.score_sentence_quality(sentence, word_lower, meaning, level)
            if score >= 4:
                excellent += 1
                self.statistics['excellent_sentences'] += 1
            elif score >= 3:
                good += 1
                self.statistics['good_sentences'] += 1
            else:
                poor += 1
                self.statistics['poor_sentences'] += 1
        
        return issues
    
    def has_strong_contextual_clues(self, sentence: str, word: str, meaning: str) -> bool:
        """Check if sentence has strong contextual clues"""
        # Remove the blank to analyze context
        context = sentence.replace("_____", "").lower()
        meaning_lower = meaning.lower()
        
        # Strong clues include:
        # 1. Specific actions/outcomes that relate to meaning
        # 2. Descriptive words that hint at meaning
        # 3. Cause-effect relationships
        # 4. Contrast or comparison
        
        # Check for vague generic phrases
        vague_phrases = [
            "was clear to everyone",
            "was evident",
            "surprised those around",
            "provided important context",
            "helped explain",
            "was obvious from",
            "became evident",
            "was important in understanding",
        ]
        
        if any(phrase in context for phrase in vague_phrases):
            return False
        
        # Check for generic action phrases
        generic_actions = [
            "decided to",
            "tried to",
            "managed to",
            "learned to",
            "had to",
            "need to",
            "should",
            "must",
        ]
        
        # If sentence is mostly generic phrases, it's weak
        generic_word_count = sum(1 for phrase in generic_actions if phrase in context)
        if generic_word_count >= 2:
            return False
        
        # Good sentences have specific context
        specific_indicators = [
            "because", "when", "after", "before", "so that",
            "in order to", "despite", "although", "while"
        ]
        
        if any(indicator in context for indicator in specific_indicators):
            return True
        
        # Check for descriptive context
        if len(context.split()) > 8:  # Longer sentences often have more context
            return True
        
        return True  # Default to true, but flag if too generic
    
    def is_age_appropriate(self, sentence: str, level: int) -> bool:
        """Check if sentence is age-appropriate for the level"""
        # Level 1: Ages 7-8 - simple sentences
        # Level 2: Ages 8-9 - slightly more complex
        # Level 3: Ages 9-10 - intermediate complexity
        # Level 4: Ages 10-11 - advanced complexity
        
        word_count = len(sentence.split())
        
        if level == 1:
            # Should be simple, under 15 words typically
            if word_count > 18:
                return False
            # Check for complex structures
            if any(phrase in sentence.lower() for phrase in [
                "despite", "although", "furthermore", "moreover", "consequently"
            ]):
                return False
        
        elif level == 2:
            if word_count > 22:
                return False
        
        elif level == 3:
            if word_count > 25:
                return False
        
        # Level 4 can be more complex
        
        return True
    
    def check_british_english(self, sentences: List[str]) -> List[str]:
        """Check for American English spellings"""
        american_spellings = {
            'color': 'colour',
            'favor': 'favour',
            'honor': 'honour',
            'labor': 'labour',
            'organize': 'organise',
            'realize': 'realise',
            'recognize': 'recognise',
            'center': 'centre',
            'theater': 'theatre',
            'defense': 'defence',
            'license': 'licence',
            'practice': 'practise',  # verb form
        }
        
        issues = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for american, british in american_spellings.items():
                if american in sentence_lower and british not in sentence_lower:
                    issues.append(f"American spelling '{american}' should be '{british}'")
        
        return issues
    
    def score_sentence_quality(
        self, 
        sentence: str, 
        word: str, 
        meaning: str, 
        level: int
    ) -> int:
        """Score sentence quality from 1-5"""
        score = 5
        
        # Deduct for generic templates
        if sentence in self.generic_templates:
            score -= 3
        
        # Deduct for weak contextual clues
        if not self.has_strong_contextual_clues(sentence, word, meaning):
            score -= 1
        
        # Deduct for incorrect blank count
        if sentence.count("_____") != 1:
            score -= 2
        
        # Deduct for age-inappropriateness
        if not self.is_age_appropriate(sentence, level):
            score -= 1
        
        # Deduct for American English
        if self.check_british_english([sentence]):
            score -= 1
        
        return max(1, score)  # Minimum score of 1
    
    def analyze_repetition(self, all_sentences: Dict[int, List[Dict]]):
        """Analyze repetition across all levels"""
        print(f"\n{'='*80}")
        print("CROSS-LEVEL REPETITION ANALYSIS")
        print(f"{'='*80}")
        
        # Count sentence frequency across all levels
        sentence_frequency = defaultdict(list)
        
        for level_num, sentences in all_sentences.items():
            for entry in sentences:
                sentence = entry['sentence']
                word = entry['word']
                sentence_frequency[sentence].append((level_num, word))
        
        # Find highly repeated sentences
        highly_repeated = {
            sent: words for sent, words in sentence_frequency.items() 
            if len(words) > 3
        }
        
        if highly_repeated:
            print(f"\n⚠️  Found {len(highly_repeated)} sentences used for 3+ different words:")
            for sentence, occurrences in sorted(highly_repeated.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
                print(f"\n  Sentence: '{sentence[:70]}...'")
                print(f"  Used for {len(occurrences)} words: {[w[1] for w in occurrences[:5]]}")
                if len(occurrences) > 5:
                    print(f"  ... and {len(occurrences) - 5} more")
        else:
            print("\n✅ No highly repeated sentences found")
    
    def generate_report(self, vocab_content: Dict):
        """Generate comprehensive examination report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE QUALITY REPORT")
        print("=" * 80)
        
        total_issues = sum(len(issues) for issues in self.issues.values())
        words_with_issues = len(self.issues)
        words_total = self.statistics['total_words']
        
        print(f"\n📊 OVERALL STATISTICS")
        print(f"  Total words examined: {words_total}")
        print(f"  Total sentences examined: {self.statistics['total_sentences']}")
        print(f"  Words with issues: {words_with_issues} ({words_with_issues/words_total*100:.1f}%)")
        print(f"  Total issues found: {total_issues}")
        print()
        
        print(f"📈 SENTENCE QUALITY DISTRIBUTION")
        excellent_pct = self.statistics['excellent_sentences'] / self.statistics['total_sentences'] * 100
        good_pct = self.statistics['good_sentences'] / self.statistics['total_sentences'] * 100
        poor_pct = self.statistics['poor_sentences'] / self.statistics['total_sentences'] * 100
        
        print(f"  Excellent (4-5/5): {self.statistics['excellent_sentences']} ({excellent_pct:.1f}%)")
        print(f"  Good (3/5): {self.statistics['good_sentences']} ({good_pct:.1f}%)")
        print(f"  Poor (1-2/5): {self.statistics['poor_sentences']} ({poor_pct:.1f}%)")
        print()
        
        print(f"🔴 CRITICAL ISSUES")
        print(f"  Generic template usage: {self.statistics['critical_issues']} sentences")
        print()
        
        # Categorize issues
        critical_words = []
        moderate_words = []
        minor_words = []
        
        for word, issues_list in self.issues.items():
            has_critical = any("CRITICAL" in issue or "generic template" in issue.lower() 
                            for issue in issues_list)
            has_moderate = any("WEAK CLUES" in issue or "LOW VARIETY" in issue 
                            for issue in issues_list)
            
            if has_critical:
                critical_words.append((word, issues_list))
            elif has_moderate:
                moderate_words.append((word, issues_list))
            else:
                minor_words.append((word, issues_list))
        
        print(f"📋 ISSUE BREAKDOWN")
        print(f"  Critical issues: {len(critical_words)} words")
        print(f"  Moderate issues: {len(moderate_words)} words")
        print(f"  Minor issues: {len(minor_words)} words")
        print()
        
        # Show examples
        if critical_words:
            print(f"🔴 CRITICAL ISSUES - Examples (showing first 20)")
            print("=" * 80)
            for word, issues_list in critical_words[:20]:
                print(f"\n{word.upper()}")
                for issue in issues_list[:3]:  # Show first 3 issues
                    print(f"  ⚠️  {issue}")
        
        # Quality assessment
        overall_quality = (excellent_pct + good_pct * 0.7) / 100
        
        print(f"\n{'='*80}")
        print("ELEVEN PLUS EXAMINER'S ASSESSMENT")
        print(f"{'='*80}")
        
        if overall_quality >= 0.85:
            grade = "EXCELLENT (A)"
            comment = "The quiz sentences meet high eleven plus standards with strong contextual clues and appropriate difficulty."
        elif overall_quality >= 0.75:
            grade = "VERY GOOD (B+)"
            comment = "The quiz sentences are of good quality but some improvements needed for generic templates."
        elif overall_quality >= 0.65:
            grade = "GOOD (B)"
            comment = "The quiz sentences are satisfactory but require significant improvements in contextual clues and variety."
        elif overall_quality >= 0.55:
            grade = "SATISFACTORY (C)"
            comment = "The quiz sentences need substantial improvement to meet eleven plus standards."
        else:
            grade = "NEEDS IMPROVEMENT (D)"
            comment = "The quiz sentences require major revision to meet educational standards."
        
        print(f"\nOverall Quality Score: {overall_quality*100:.1f}%")
        print(f"Grade: {grade}")
        print(f"Assessment: {comment}")
        print()
        
        print("KEY FINDINGS:")
        if self.statistics['critical_issues'] > 0:
            print(f"  ⚠️  {self.statistics['critical_issues']} sentences use generic templates (CRITICAL)")
        if poor_pct > 20:
            print(f"  ⚠️  {poor_pct:.1f}% of sentences are of poor quality")
        if len(critical_words) > words_total * 0.1:
            print(f"  ⚠️  {len(critical_words)} words ({len(critical_words)/words_total*100:.1f}%) have critical issues")
        
        if excellent_pct > 50:
            print(f"  ✅ {excellent_pct:.1f}% of sentences are excellent quality")
        if len(critical_words) < words_total * 0.05:
            print(f"  ✅ Only {len(critical_words)} words have critical issues")
        
        print()
        print("RECOMMENDATIONS:")
        print("1. Replace all generic template sentences with contextually rich sentences")
        print("2. Ensure each sentence provides strong clues through specific context")
        print("3. Increase sentence variety - avoid repetitive patterns")
        print("4. Verify all sentences match the word's meaning accurately")
        print("5. Review age-appropriateness for each level")
        print("6. Ensure British English spelling throughout")
        
        # Save detailed report
        self.save_detailed_report(critical_words, moderate_words, minor_words)
    
    def save_detailed_report(self, critical_words, moderate_words, minor_words):
        """Save detailed report to file"""
        report_file = PROJECT_ROOT / "QUIZ_SENTENCES_QUALITY_EXAMINATION_REPORT.md"
        
        with report_file.open('w', encoding='utf-8') as f:
            f.write("# QUIZ SENTENCES QUALITY EXAMINATION REPORT\n\n")
            f.write("**Examiner:** Eleven Plus Vocabulary Specialist\n")
            f.write(f"**Date:** Generated automatically\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(f"- **Total Words Examined:** {self.statistics['total_words']}\n")
            f.write(f"- **Total Sentences Examined:** {self.statistics['total_sentences']}\n")
            f.write(f"- **Words with Issues:** {len(self.issues)}\n")
            f.write(f"- **Critical Issues:** {len(critical_words)} words\n")
            f.write(f"- **Moderate Issues:** {len(moderate_words)} words\n")
            f.write(f"- **Minor Issues:** {len(minor_words)} words\n\n")
            
            f.write("## Critical Issues\n\n")
            for word, issues_list in critical_words:
                f.write(f"### {word.upper()}\n\n")
                for issue in issues_list:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            if moderate_words:
                f.write("## Moderate Issues\n\n")
                for word, issues_list in moderate_words[:50]:  # First 50
                    f.write(f"### {word.upper()}\n\n")
                    for issue in issues_list:
                        f.write(f"- {issue}\n")
                    f.write("\n")
        
        print(f"\n📄 Detailed report saved to: {report_file}")


def main():
    examiner = QuizSentenceExaminer()
    examiner.examine_all()


if __name__ == '__main__':
    main()
