#!/usr/bin/env python3
"""
Vocabulary Quality Examination Script
Examines all vocabulary entries for quality, consistency, and accuracy.
"""

import csv
import re
from collections import defaultdict
from typing import Dict, List, Tuple

class VocabularyQualityExaminer:
    def __init__(self):
        self.issues = defaultdict(list)
        self.statistics = {
            'total_words': 0,
            'level1': 0,
            'level2': 0,
            'level3': 0,
            'level4': 0,
            'missing_fields': 0,
            'short_meanings': 0,
            'repetitive_synonyms': 0,
            'repetitive_antonyms': 0,
            'weak_examples': 0,
            'excellent_entries': 0,
        }
        
    def examine_all(self):
        """Main examination method"""
        print("=" * 80)
        print("VOCABULARY QUALITY EXAMINATION REPORT")
        print("=" * 80)
        print()
        
        # Load all vocabulary data
        vocab_list = self.load_csv('../data/vocabularyList.csv')
        vocab_content = self.load_csv('../data/vocabulary_content_new.csv')
        vocab_levels = self.load_csv('../data/vocabulary_levels.csv')
        
        # Create lookup dictionaries
        content_dict = {row['word'].lower(): row for row in vocab_content}
        levels_dict = {row['word'].lower(): row for row in vocab_levels}
        list_dict = {row['word'].lower(): row for row in vocab_list}
        
        # Examine each vocabulary entry
        for row in vocab_content:
            word = row['word']
            self.examine_entry(word, row, levels_dict.get(word.lower()), list_dict.get(word.lower()))
        
        # Generate report
        self.generate_report()
        
    def load_csv(self, filepath):
        """Load CSV file"""
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    
    def examine_entry(self, word, content_row, level_row, list_row):
        """Examine a single vocabulary entry"""
        self.statistics['total_words'] += 1
        issues_found = []
        
        # Check level distribution
        if level_row:
            level = level_row.get('level', '')
            if level == 'level1':
                self.statistics['level1'] += 1
            elif level == 'level2':
                self.statistics['level2'] += 1
            elif level == 'level3':
                self.statistics['level3'] += 1
            elif level == 'level4':
                self.statistics['level4'] += 1
        
        # 1. Check for missing or empty fields
        required_fields = ['meaning', 'synonym1', 'synonym2', 'antonym1', 'antonym2', 'example_sentence']
        for field in required_fields:
            value = content_row.get(field, '').strip()
            if not value or value == '':
                issues_found.append(f"Missing {field}")
                self.statistics['missing_fields'] += 1
        
        # 2. Check meaning quality
        meaning = content_row.get('meaning', '').strip()
        if meaning:
            if len(meaning) < 15:
                issues_found.append(f"Very short meaning: '{meaning}'")
                self.statistics['short_meanings'] += 1
            elif len(meaning) < 25:
                issues_found.append(f"Short meaning: '{meaning}'")
                self.statistics['short_meanings'] += 1
        
        # 3. Check synonyms
        syn1 = content_row.get('synonym1', '').strip().lower()
        syn2 = content_row.get('synonym2', '').strip().lower()
        if syn1 and syn2:
            if syn1 == syn2:
                issues_found.append(f"Identical synonyms: {syn1}")
                self.statistics['repetitive_synonyms'] += 1
            # Check if synonym is just the word with different form
            word_lower = word.lower()
            if syn1 == word_lower or syn2 == word_lower:
                issues_found.append(f"Synonym is the word itself")
                self.statistics['repetitive_synonyms'] += 1
        
        # 4. Check antonyms
        ant1 = content_row.get('antonym1', '').strip().lower()
        ant2 = content_row.get('antonym2', '').strip().lower()
        if ant1 and ant2:
            if ant1 == ant2:
                issues_found.append(f"Identical antonyms: {ant1}")
                self.statistics['repetitive_antonyms'] += 1
            # Check if antonym accidentally matches synonym
            if (syn1 and ant1 == syn1) or (syn2 and ant1 == syn2) or (syn1 and ant2 == syn1) or (syn2 and ant2 == syn2):
                issues_found.append(f"Antonym matches synonym!")
                self.statistics['repetitive_antonyms'] += 1
        
        # 5. Check example sentence quality
        example = content_row.get('example_sentence', '').strip()
        if example:
            # Check if word appears in example
            word_lower = word.lower()
            example_lower = example.lower()
            
            # Check for various forms of the word
            word_variants = [
                word_lower,
                word_lower + 's',
                word_lower + 'ed',
                word_lower + 'ing',
                word_lower + 'd',
            ]
            
            word_found = any(variant in example_lower for variant in word_variants)
            
            if not word_found:
                issues_found.append(f"Word '{word}' not in example: '{example}'")
                self.statistics['weak_examples'] += 1
            
            # Check sentence length
            if len(example) < 30:
                issues_found.append(f"Very short example: '{example}'")
                self.statistics['weak_examples'] += 1
            
            # Check if sentence ends with proper punctuation
            if not example.endswith(('.', '!', '?')):
                issues_found.append(f"Example missing punctuation: '{example}'")
                self.statistics['weak_examples'] += 1
            
            # Check if sentence starts with capital letter
            if not example[0].isupper():
                issues_found.append(f"Example doesn't start with capital: '{example}'")
                self.statistics['weak_examples'] += 1
        
        # 6. Identify excellent entries (no issues)
        if not issues_found:
            self.statistics['excellent_entries'] += 1
        else:
            self.issues[word] = issues_found
    
    def generate_report(self):
        """Generate comprehensive quality report"""
        print("\n" + "=" * 80)
        print("OVERALL STATISTICS")
        print("=" * 80)
        print(f"Total vocabulary words examined: {self.statistics['total_words']}")
        print(f"  Level 1 words: {self.statistics['level1']}")
        print(f"  Level 2 words: {self.statistics['level2']}")
        print(f"  Level 3 words: {self.statistics['level3']}")
        print(f"  Level 4 words: {self.statistics['level4']}")
        print()
        print(f"Excellent entries (no issues): {self.statistics['excellent_entries']} "
              f"({self.statistics['excellent_entries']/self.statistics['total_words']*100:.1f}%)")
        print(f"Entries with issues: {len(self.issues)} "
              f"({len(self.issues)/self.statistics['total_words']*100:.1f}%)")
        print()
        
        print("\n" + "=" * 80)
        print("ISSUE BREAKDOWN")
        print("=" * 80)
        print(f"Missing fields: {self.statistics['missing_fields']}")
        print(f"Short/weak meanings: {self.statistics['short_meanings']}")
        print(f"Synonym issues: {self.statistics['repetitive_synonyms']}")
        print(f"Antonym issues: {self.statistics['repetitive_antonyms']}")
        print(f"Example sentence issues: {self.statistics['weak_examples']}")
        print()
        
        # Categorize issues by severity
        critical_issues = []
        moderate_issues = []
        minor_issues = []
        
        for word, issues_list in sorted(self.issues.items()):
            has_critical = any('Missing' in issue or 'not in example' in issue or 'matches synonym' in issue 
                             for issue in issues_list)
            has_moderate = any('short' in issue.lower() or 'Identical' in issue for issue in issues_list)
            
            if has_critical:
                critical_issues.append((word, issues_list))
            elif has_moderate:
                moderate_issues.append((word, issues_list))
            else:
                minor_issues.append((word, issues_list))
        
        print("\n" + "=" * 80)
        print("CRITICAL ISSUES (Requires immediate attention)")
        print("=" * 80)
        print(f"Total: {len(critical_issues)} words")
        if critical_issues:
            print()
            for word, issues_list in critical_issues[:20]:  # Show first 20
                print(f"• {word.upper()}")
                for issue in issues_list:
                    print(f"  - {issue}")
                print()
            if len(critical_issues) > 20:
                print(f"... and {len(critical_issues) - 20} more words with critical issues")
        
        print("\n" + "=" * 80)
        print("MODERATE ISSUES (Should be improved)")
        print("=" * 80)
        print(f"Total: {len(moderate_issues)} words")
        if moderate_issues:
            print()
            for word, issues_list in moderate_issues[:15]:  # Show first 15
                print(f"• {word.upper()}")
                for issue in issues_list:
                    print(f"  - {issue}")
                print()
            if len(moderate_issues) > 15:
                print(f"... and {len(moderate_issues) - 15} more words with moderate issues")
        
        print("\n" + "=" * 80)
        print("MINOR ISSUES (Low priority)")
        print("=" * 80)
        print(f"Total: {len(minor_issues)} words")
        if minor_issues:
            print()
            for word, issues_list in minor_issues[:10]:  # Show first 10
                print(f"• {word.upper()}")
                for issue in issues_list:
                    print(f"  - {issue}")
                print()
            if len(minor_issues) > 10:
                print(f"... and {len(minor_issues) - 10} more words with minor issues")
        
        print("\n" + "=" * 80)
        print("QUALITY ASSESSMENT")
        print("=" * 80)
        
        excellent_pct = self.statistics['excellent_entries'] / self.statistics['total_words'] * 100
        issues_pct = len(self.issues) / self.statistics['total_words'] * 100
        critical_pct = len(critical_issues) / self.statistics['total_words'] * 100
        
        print(f"Overall Quality Score: {excellent_pct:.1f}%")
        print()
        
        if excellent_pct >= 90:
            grade = "EXCELLENT (A)"
            comment = "The vocabulary dataset is of outstanding quality with minimal issues."
        elif excellent_pct >= 80:
            grade = "VERY GOOD (B+)"
            comment = "The vocabulary dataset is of very good quality with some minor issues."
        elif excellent_pct >= 70:
            grade = "GOOD (B)"
            comment = "The vocabulary dataset is of good quality but needs some improvements."
        elif excellent_pct >= 60:
            grade = "SATISFACTORY (C)"
            comment = "The vocabulary dataset is satisfactory but requires notable improvements."
        else:
            grade = "NEEDS IMPROVEMENT (D)"
            comment = "The vocabulary dataset requires significant improvements."
        
        print(f"Grade: {grade}")
        print(f"Assessment: {comment}")
        print()
        
        print("Key Strengths:")
        if excellent_pct > 50:
            print(f"  ✓ {excellent_pct:.1f}% of entries have no issues")
        if self.statistics['missing_fields'] < self.statistics['total_words'] * 0.05:
            print(f"  ✓ Very few missing fields ({self.statistics['missing_fields']} total)")
        if critical_pct < 5:
            print(f"  ✓ Low critical issue rate ({critical_pct:.1f}%)")
        
        print()
        print("Areas for Improvement:")
        if self.statistics['short_meanings'] > self.statistics['total_words'] * 0.1:
            print(f"  ⚠ Many meanings are too short or weak ({self.statistics['short_meanings']} entries)")
        if self.statistics['weak_examples'] > self.statistics['total_words'] * 0.1:
            print(f"  ⚠ Many example sentences need improvement ({self.statistics['weak_examples']} issues)")
        if self.statistics['repetitive_synonyms'] > 0:
            print(f"  ⚠ Some synonym issues ({self.statistics['repetitive_synonyms']} cases)")
        if self.statistics['repetitive_antonyms'] > 0:
            print(f"  ⚠ Some antonym issues ({self.statistics['repetitive_antonyms']} cases)")
        if critical_pct > 5:
            print(f"  ⚠ High critical issue rate ({critical_pct:.1f}%)")
        
        print("\n" + "=" * 80)
        print("RECOMMENDATIONS")
        print("=" * 80)
        print("1. Priority: Fix all critical issues (words missing content or with major errors)")
        print("2. Review and enhance short/weak meanings to be more descriptive")
        print("3. Ensure all example sentences contain the vocabulary word")
        print("4. Check for duplicate or conflicting synonyms/antonyms")
        print("5. Standardize sentence formatting (capitalization, punctuation)")
        print()
        
        # Save detailed report to file
        with open('../VOCABULARY_EXAMINATION_REPORT.md', 'w', encoding='utf-8') as f:
            f.write("# VOCABULARY QUALITY EXAMINATION REPORT\n\n")
            f.write(f"**Examination Date:** Generated automatically\n\n")
            f.write(f"**Total Vocabulary Words:** {self.statistics['total_words']}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(f"- **Overall Quality Score:** {excellent_pct:.1f}%\n")
            f.write(f"- **Grade:** {grade}\n")
            f.write(f"- **Assessment:** {comment}\n\n")
            
            f.write("## Statistics\n\n")
            f.write(f"- Excellent entries (no issues): {self.statistics['excellent_entries']} ({excellent_pct:.1f}%)\n")
            f.write(f"- Entries with issues: {len(self.issues)} ({issues_pct:.1f}%)\n")
            f.write(f"  - Critical issues: {len(critical_issues)} ({critical_pct:.1f}%)\n")
            f.write(f"  - Moderate issues: {len(moderate_issues)}\n")
            f.write(f"  - Minor issues: {len(minor_issues)}\n\n")
            
            f.write("## Level Distribution\n\n")
            f.write(f"- Level 1: {self.statistics['level1']} words\n")
            f.write(f"- Level 2: {self.statistics['level2']} words\n")
            f.write(f"- Level 3: {self.statistics['level3']} words\n")
            f.write(f"- Level 4: {self.statistics['level4']} words\n\n")
            
            f.write("## Issue Breakdown\n\n")
            f.write(f"- Missing fields: {self.statistics['missing_fields']}\n")
            f.write(f"- Short/weak meanings: {self.statistics['short_meanings']}\n")
            f.write(f"- Synonym issues: {self.statistics['repetitive_synonyms']}\n")
            f.write(f"- Antonym issues: {self.statistics['repetitive_antonyms']}\n")
            f.write(f"- Example sentence issues: {self.statistics['weak_examples']}\n\n")
            
            f.write("## Critical Issues\n\n")
            for word, issues_list in critical_issues:
                f.write(f"### {word.upper()}\n\n")
                for issue in issues_list:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            if moderate_issues:
                f.write("## Moderate Issues\n\n")
                for word, issues_list in moderate_issues[:50]:  # Save first 50
                    f.write(f"### {word.upper()}\n\n")
                    for issue in issues_list:
                        f.write(f"- {issue}\n")
                    f.write("\n")
        
        print(f"\nDetailed report saved to: VOCABULARY_EXAMINATION_REPORT.md")
        print("=" * 80)

def main():
    examiner = VocabularyQualityExaminer()
    examiner.examine_all()

if __name__ == '__main__':
    main()
