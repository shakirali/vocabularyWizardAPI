#!/usr/bin/env python3
"""
Script to generate quiz sentences using Ollama.

This script demonstrates the sentence generation functionality
using a local Ollama model (e.g., Gemma).

Usage:
    python scripts/generate_quiz_sentence.py
    python scripts/generate_quiz_sentence.py --word "abundant" --meaning "existing in large quantities"
    python scripts/generate_quiz_sentence.py --interactive
"""
import argparse
import random
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables before importing app modules
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from app.utils.ollama_service import OllamaService


# Sample distractor words for demo purposes
SAMPLE_DISTRACTORS = [
    "happy", "sad", "quick", "slow", "bright", "dark", "large", "small",
    "ancient", "modern", "gentle", "harsh", "simple", "complex", "rare",
    "common", "brave", "timid", "calm", "anxious", "clever", "foolish",
    "honest", "deceitful", "generous", "selfish", "patient", "restless"
]


def get_random_distractors(correct_word: str, count: int = 3) -> list:
    """Get random distractor words (excluding the correct word)."""
    available = [w for w in SAMPLE_DISTRACTORS if w.lower() != correct_word.lower()]
    return random.sample(available, min(count, len(available)))


def format_quiz_question(sentence: str, correct_word: str, distractors: list) -> str:
    """Format a complete quiz question with options."""
    options = [correct_word] + distractors
    random.shuffle(options)
    correct_index = options.index(correct_word)
    
    output = [f"\n📝 Sentence: {sentence}\n"]
    output.append("   Options:")
    for i, opt in enumerate(options):
        marker = "✓" if opt == correct_word else " "
        output.append(f"     {chr(65+i)}) {opt} {marker}")
    output.append(f"\n   Correct Answer: {chr(65+correct_index)}) {correct_word}")
    
    return "\n".join(output)


def generate_single_sentence(word: str, meaning: str) -> None:
    """Generate a single quiz sentence for the given word."""
    print(f"\n{'='*60}")
    print(f"Word: {word}")
    print(f"Meaning: {meaning}")
    print(f"{'='*60}")
    
    service = OllamaService()
    
    if not service.is_available():
        print("\n❌ Error: Ollama service is not available.")
        print("Make sure Ollama is running: ollama serve")
        return
    
    print(f"\n🔄 Generating sentence using model: {service.model}...")
    
    sentence = service.generate_sentence_with_blank(word=word, meaning=meaning)
    
    if sentence:
        distractors = get_random_distractors(word)
        print(f"\n✅ Generated Quiz Question:")
        print(format_quiz_question(sentence, word, distractors))
    else:
        print("\n❌ Failed to generate sentence.")


def interactive_mode() -> None:
    """Run in interactive mode, allowing multiple sentence generations."""
    print("\n" + "="*60)
    print("🎯 Quiz Sentence Generator - Interactive Mode")
    print("="*60)
    print("Enter vocabulary words to generate quiz sentences.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    service = OllamaService()
    
    if not service.is_available():
        print("❌ Error: Ollama service is not available.")
        print("Make sure Ollama is running: ollama serve")
        return
    
    print(f"✅ Connected to Ollama (model: {service.model})\n")
    
    while True:
        try:
            word = input("Enter word (or 'quit'): ").strip()
            if word.lower() in ('quit', 'exit', 'q'):
                print("\nGoodbye! 👋")
                break
            
            if not word:
                continue
                
            meaning = input("Enter meaning: ").strip()
            if not meaning:
                print("⚠️  Meaning is required. Try again.\n")
                continue
            
            print(f"\n🔄 Generating sentence...")
            sentence = service.generate_sentence_with_blank(word=word, meaning=meaning)
            
            if sentence:
                distractors = get_random_distractors(word)
                print(f"\n✅ Quiz Question Generated:")
                print(format_quiz_question(sentence, word, distractors))
                print()
            else:
                print("❌ Failed to generate sentence. Try again.\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break


def demo_mode() -> None:
    """Run demo with sample vocabulary words."""
    print("\n" + "="*60)
    print("🎯 Quiz Sentence Generator - Demo Mode")
    print("="*60)
    
    # Sample vocabulary words
    sample_words = [
        {"word": "abundant", "meaning": "existing in large quantities; plentiful"},
        {"word": "cautious", "meaning": "careful to avoid potential problems or dangers"},
        {"word": "diligent", "meaning": "showing care and effort in work or duties"},
        {"word": "eloquent", "meaning": "fluent or persuasive in speaking or writing"},
        {"word": "fragile", "meaning": "easily broken or damaged; delicate"},
    ]
    
    service = OllamaService()
    
    if not service.is_available():
        print("\n❌ Error: Ollama service is not available.")
        print("Make sure Ollama is running: ollama serve")
        return
    
    print(f"✅ Connected to Ollama (model: {service.model})")
    print(f"\nGenerating quiz questions for {len(sample_words)} sample words...\n")
    
    for i, item in enumerate(sample_words, 1):
        print(f"{'─'*60}")
        print(f"[{i}/{len(sample_words)}] Word: {item['word']} ({item['meaning']})")
        
        sentence = service.generate_sentence_with_blank(
            word=item["word"], 
            meaning=item["meaning"]
        )
        
        if sentence:
            distractors = get_random_distractors(item["word"])
            print(format_quiz_question(sentence, item["word"], distractors))
        else:
            print(f"   ❌ Failed to generate sentence")
        print()
    
    print("="*60)
    print("Demo complete! 🎉")


def main():
    parser = argparse.ArgumentParser(
        description="Generate quiz sentences using Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Run demo with sample words
  %(prog)s --interactive                      # Interactive mode
  %(prog)s --word "happy" --meaning "joyful"  # Generate for specific word
        """
    )
    
    parser.add_argument(
        "--word", "-w",
        help="The vocabulary word to generate a sentence for"
    )
    parser.add_argument(
        "--meaning", "-m",
        help="The meaning/definition of the word"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run demo with sample vocabulary words"
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.word and args.meaning:
        generate_single_sentence(args.word, args.meaning)
    elif args.word or args.meaning:
        parser.error("Both --word and --meaning are required together")
    else:
        # Default to demo mode
        demo_mode()


if __name__ == "__main__":
    main()
