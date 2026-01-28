#!/usr/bin/env python3
"""
Demonstration script showing AI content generation in action.

This script demonstrates how the AI content generation service works
by generating sample vocabulary content.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service


def demo_enhanced_meaning():
    """Demonstrate enhanced meaning generation."""
    print("=" * 60)
    print("DEMO: Enhanced Meaning Generation")
    print("=" * 60)
    
    test_cases = [
        ("absolute", "complete or total"),
        ("miniscule", "extremely small"),
        ("abashed", "embarrassed or ashamed"),
    ]
    
    for word, short_meaning in test_cases:
        print(f"\nWord: {word}")
        print(f"Original meaning: {short_meaning}")
        
        enhanced = ai_content_service.generate_enhanced_meaning(word, short_meaning)
        
        if enhanced:
            print(f"Enhanced meaning: {enhanced}")
            print(f"Length: {len(short_meaning)} -> {len(enhanced)} characters")
        else:
            print("❌ Generation failed")
    
    print()


def demo_example_sentences():
    """Demonstrate example sentence generation."""
    print("=" * 60)
    print("DEMO: Example Sentence Generation")
    print("=" * 60)
    
    test_cases = [
        ("abandon", "to leave behind or give up completely", "level2"),
        ("abundant", "existing in large quantities", "level3"),
        ("acute", "very serious or severe", "level1"),
    ]
    
    for word, meaning, level in test_cases:
        print(f"\nWord: {word} (Level: {level})")
        print(f"Meaning: {meaning}")
        
        sentence = ai_content_service.generate_example_sentence(word, meaning, level)
        
        if sentence:
            print(f"Example sentence: {sentence}")
        else:
            print("❌ Generation failed")
    
    print()


def demo_sentence_with_blank():
    """Demonstrate sentence with blank generation."""
    print("=" * 60)
    print("DEMO: Sentence with Blank Generation")
    print("=" * 60)
    
    test_cases = [
        ("abandon", "to leave behind or give up completely"),
        ("abundant", "existing in large quantities"),
    ]
    
    for word, meaning in test_cases:
        print(f"\nWord: {word}")
        print(f"Meaning: {meaning}")
        
        sentence = ai_content_service.generate_sentence_with_blank(word, meaning)
        
        if sentence:
            print(f"Sentence with blank: {sentence}")
        else:
            print("❌ Generation failed")
    
    print()


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("AI CONTENT GENERATION DEMONSTRATION")
    print("=" * 60)
    print()
    
    if not ai_content_service.is_available():
        print("❌ AI Content Service is not available")
        return
    
    print("✅ AI Content Service is available")
    print()
    
    # Run demonstrations
    demo_enhanced_meaning()
    demo_example_sentences()
    demo_sentence_with_blank()
    
    print("=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print()
    print("Note: Complete vocabulary content generation requires")
    print("      connection to an AI model for meaning, synonyms, and antonyms.")


if __name__ == "__main__":
    main()
