#!/usr/bin/env python3
"""
Import quiz sentences from level-based CSV files.

This script uses the new level-based data model.
Quiz sentences are linked to vocabulary items by word.

CSV Format:
    level,word,sentence

Usage:
    python scripts/import_quiz_sentences_levels.py
    python scripts/import_quiz_sentences_levels.py --dry-run
    python scripts/import_quiz_sentences_levels.py --level 1
"""
import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables before importing app modules
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from sqlalchemy import func

from app.database import SessionLocal
# Import all models to ensure SQLAlchemy can resolve relationships
from app.models.quiz_sentence import QuizSentence
from app.models.vocabulary import VocabularyItem
from app.models.level import Level, VocabularyLevel  # noqa: F401
from app.models.progress import UserProgress  # noqa: F401
from app.models.user import User  # noqa: F401


def get_vocabulary_items(db) -> Dict[str, VocabularyItem]:
    """Get all vocabulary items indexed by lowercase word."""
    items = db.query(VocabularyItem).all()
    return {item.word.lower(): item for item in items}


def import_quiz_sentences_for_level(
    db,
    csv_path: Path,
    vocab_items: Dict[str, VocabularyItem],
    level: int,
    dry_run: bool = False,
    clear_existing: bool = False,
):
    """Import quiz sentences for a specific level."""
    print(f"\n📝 Importing quiz sentences from {csv_path.name}...")
    
    if not csv_path.exists():
        print(f"  ⚠️  File not found: {csv_path}")
        return
    
    # Clear existing sentences for this level if requested
    if clear_existing and not dry_run:
        # Get all vocab items for this level and clear their sentences
        # For now, we'll just proceed without clearing since sentences
        # are linked to vocab items, not levels directly
        pass
    
    stats = {
        "total": 0,
        "inserted": 0,
        "skipped_no_vocab": 0,
        "skipped_no_blank": 0,
        "skipped_duplicate": 0,
    }
    
    # Track existing sentences to avoid duplicates
    existing_sentences = set()
    for qs in db.query(QuizSentence).all():
        vocab = db.query(VocabularyItem).filter(VocabularyItem.id == qs.vocabulary_item_id).first()
        if vocab:
            existing_sentences.add((vocab.word.lower(), qs.sentence))
    
    sentences_to_add = []
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            stats["total"] += 1
            
            word = row.get("word", "").strip().lower()
            sentence = row.get("sentence", "").strip()
            
            if not word or not sentence:
                continue
            
            if word not in vocab_items:
                stats["skipped_no_vocab"] += 1
                continue
            
            if "_____" not in sentence:
                stats["skipped_no_blank"] += 1
                continue
            
            if (word, sentence) in existing_sentences:
                stats["skipped_duplicate"] += 1
                continue
            
            if not dry_run:
                quiz_sentence = QuizSentence(
                    vocabulary_item_id=vocab_items[word].id,
                    sentence=sentence,
                )
                sentences_to_add.append(quiz_sentence)
            
            existing_sentences.add((word, sentence))
            stats["inserted"] += 1
    
    if not dry_run and sentences_to_add:
        db.add_all(sentences_to_add)
        db.commit()
    
    print(f"  Level {level}: Total: {stats['total']}, Inserted: {stats['inserted']}")
    print(f"    Skipped - No vocab: {stats['skipped_no_vocab']}, No blank: {stats['skipped_no_blank']}, Duplicate: {stats['skipped_duplicate']}")
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Import quiz sentences from level-based CSV files",
    )
    
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=project_root / "data",
        help="Directory containing quiz sentence CSV files"
    )
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3, 4],
        help="Import only for specific level (1-4)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying database"
    )
    parser.add_argument(
        "--clear-existing",
        action="store_true",
        help="Clear existing quiz sentences before import"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("📝 Quiz Sentence Import (Level-based)")
    print("=" * 60)
    print(f"Data directory: {args.data_dir}")
    if args.level:
        print(f"Level filter: {args.level}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Get vocabulary items
        print("\n📚 Loading vocabulary items...")
        vocab_items = get_vocabulary_items(db)
        print(f"  Found {len(vocab_items)} vocabulary items")
        
        if not vocab_items:
            print("\n❌ Error: No vocabulary items found")
            print("Run vocabulary import first!")
            sys.exit(1)
        
        # Determine which levels to import
        levels = [args.level] if args.level else [1, 2, 3, 4]
        
        total_stats = {
            "total": 0,
            "inserted": 0,
        }
        
        for level in levels:
            csv_path = args.data_dir / f"quiz_sentences_level{level}.csv"
            stats = import_quiz_sentences_for_level(
                db, csv_path, vocab_items, level,
                dry_run=args.dry_run,
                clear_existing=args.clear_existing,
            )
            if stats:
                total_stats["total"] += stats["total"]
                total_stats["inserted"] += stats["inserted"]
        
        print("\n" + "=" * 60)
        print(f"📊 Total: {total_stats['total']} rows, {total_stats['inserted']} inserted")
        if args.dry_run:
            print("⚠️  DRY RUN - No changes were made")
        else:
            print("✅ Import completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
