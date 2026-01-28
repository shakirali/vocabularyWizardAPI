#!/usr/bin/env python3
"""
Import vocabulary items and level associations from CSV files.

This script uses the new level-based data model:
- vocabulary.csv: Unique words with definitions
- vocabulary_levels.csv: Word-level associations

CSV Format for vocabulary.csv:
    word,meaning,synonyms,antonyms,example_sentences

CSV Format for vocabulary_levels.csv:
    word,level

Usage:
    python scripts/import_vocabulary_levels.py
    python scripts/import_vocabulary_levels.py --dry-run
    python scripts/import_vocabulary_levels.py --vocab-file vocabulary.csv --levels-file vocabulary_levels.csv
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables before importing app modules
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from sqlalchemy import func

from app.database import SessionLocal
# Import all models to ensure SQLAlchemy can resolve relationships
from app.models.level import Level, VocabularyLevel
from app.models.vocabulary import VocabularyItem
from app.models.progress import UserProgress  # noqa: F401
from app.models.quiz_sentence import QuizSentence  # noqa: F401
from app.models.user import User  # noqa: F401
from app.repositories.level_repository import LevelRepository


def parse_list_field(value: str) -> List[str]:
    """
    Parse a field that can be semicolon-separated, comma-separated, or JSON array.
    """
    if not value or not value.strip():
        return []
    
    value = value.strip()
    
    if value.lower() in ("n/a", "na", "none", "-"):
        return []
    
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    
    if ";" in value:
        return [item.strip() for item in value.split(";") if item.strip() and item.strip().lower() not in ("n/a", "na")]
    
    return [item.strip() for item in value.split(",") if item.strip() and item.strip().lower() not in ("n/a", "na")]


def ensure_levels_exist(db) -> Dict[int, Level]:
    """Ensure all 4 levels exist in the database."""
    level_repo = LevelRepository(db)
    level_repo.create_default_levels()
    
    levels = db.query(Level).all()
    return {level.level: level for level in levels}


def find_vocabulary_item(db, word: str) -> Optional[VocabularyItem]:
    """Find a vocabulary item by word (case-insensitive)."""
    return (
        db.query(VocabularyItem)
        .filter(func.lower(VocabularyItem.word) == func.lower(word))
        .first()
    )


def import_vocabulary(
    db,
    vocab_path: Path,
    dry_run: bool = False,
) -> Dict[str, VocabularyItem]:
    """Import vocabulary items from CSV."""
    print(f"\n📚 Importing vocabulary from {vocab_path.name}...")
    
    vocab_items: Dict[str, VocabularyItem] = {}
    
    stats = {
        "total": 0,
        "inserted": 0,
        "updated": 0,
        "errors": 0,
    }
    
    with open(vocab_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            stats["total"] += 1
            
            word = row.get("word", "").strip().lower()
            meaning = row.get("meaning", "").strip()
            
            if not word or not meaning:
                stats["errors"] += 1
                continue
            
            synonyms = parse_list_field(row.get("synonyms", ""))
            antonyms = parse_list_field(row.get("antonyms", ""))
            example_sentences = parse_list_field(row.get("example_sentences", ""))
            
            existing = find_vocabulary_item(db, word)
            
            if existing:
                if not dry_run:
                    existing.meaning = meaning
                    existing.synonyms = synonyms
                    existing.antonyms = antonyms
                    existing.example_sentences = example_sentences
                    db.flush()
                vocab_items[word] = existing
                stats["updated"] += 1
            else:
                if not dry_run:
                    new_item = VocabularyItem(
                        word=word,
                        meaning=meaning,
                        synonyms=synonyms,
                        antonyms=antonyms,
                        example_sentences=example_sentences,
                    )
                    db.add(new_item)
                    db.flush()
                    vocab_items[word] = new_item
                else:
                    vocab_items[word] = None  # Placeholder for dry run
                stats["inserted"] += 1
    
    if not dry_run:
        db.commit()
    
    print(f"  Total: {stats['total']}, Inserted: {stats['inserted']}, Updated: {stats['updated']}, Errors: {stats['errors']}")
    
    return vocab_items


def import_vocabulary_levels(
    db,
    levels_path: Path,
    vocab_items: Dict[str, VocabularyItem],
    levels: Dict[int, Level],
    dry_run: bool = False,
):
    """Import word-level associations from CSV."""
    print(f"\n🔗 Importing vocabulary-level associations from {levels_path.name}...")
    
    stats = {
        "total": 0,
        "inserted": 0,
        "skipped_no_vocab": 0,
        "skipped_no_level": 0,
        "skipped_duplicate": 0,
    }
    
    # Get existing associations
    existing_associations = set()
    for vl in db.query(VocabularyLevel).all():
        vocab = db.query(VocabularyItem).filter(VocabularyItem.id == vl.vocabulary_item_id).first()
        level = db.query(Level).filter(Level.id == vl.level_id).first()
        if vocab and level:
            existing_associations.add((vocab.word.lower(), level.level))
    
    associations_to_add = []
    
    with open(levels_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            stats["total"] += 1
            
            word = row.get("word", "").strip().lower()
            level_num = int(row.get("level", 0))
            
            if word not in vocab_items or vocab_items[word] is None:
                stats["skipped_no_vocab"] += 1
                continue
            
            if level_num not in levels:
                stats["skipped_no_level"] += 1
                continue
            
            if (word, level_num) in existing_associations:
                stats["skipped_duplicate"] += 1
                continue
            
            if not dry_run:
                vocab_level = VocabularyLevel(
                    vocabulary_item_id=vocab_items[word].id,
                    level_id=levels[level_num].id,
                )
                associations_to_add.append(vocab_level)
            
            existing_associations.add((word, level_num))
            stats["inserted"] += 1
    
    if not dry_run and associations_to_add:
        db.add_all(associations_to_add)
        db.commit()
    
    print(f"  Total: {stats['total']}, Inserted: {stats['inserted']}")
    print(f"  Skipped - No vocab: {stats['skipped_no_vocab']}, No level: {stats['skipped_no_level']}, Duplicate: {stats['skipped_duplicate']}")


def main():
    parser = argparse.ArgumentParser(
        description="Import vocabulary items and level associations",
    )
    
    parser.add_argument(
        "--vocab-file",
        type=Path,
        default=project_root / "data" / "vocabulary.csv",
        help="Path to vocabulary CSV file"
    )
    parser.add_argument(
        "--levels-file",
        type=Path,
        default=project_root / "data" / "vocabulary_levels.csv",
        help="Path to vocabulary levels CSV file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying database"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("📚 Vocabulary Import (Level-based)")
    print("=" * 60)
    print(f"Vocabulary file: {args.vocab_file}")
    print(f"Levels file: {args.levels_file}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)
    
    if not args.vocab_file.exists():
        print(f"\n❌ Error: Vocabulary file not found: {args.vocab_file}")
        print("Ensure vocabulary.csv exists in the data/ directory.")
        sys.exit(1)
    
    if not args.levels_file.exists():
        print(f"\n❌ Error: Levels file not found: {args.levels_file}")
        print("Ensure vocabulary_levels.csv exists in the data/ directory.")
        sys.exit(1)
    
    db = SessionLocal()
    
    try:
        # Ensure levels exist
        print("\n🎯 Ensuring levels exist...")
        levels = ensure_levels_exist(db)
        print(f"  Found {len(levels)} levels")
        
        # Import vocabulary
        vocab_items = import_vocabulary(db, args.vocab_file, args.dry_run)
        
        # Re-fetch vocab items after commit
        if not args.dry_run:
            vocab_items = {}
            for item in db.query(VocabularyItem).all():
                vocab_items[item.word.lower()] = item
        
        # Import level associations
        import_vocabulary_levels(db, args.levels_file, vocab_items, levels, args.dry_run)
        
        print("\n" + "=" * 60)
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
