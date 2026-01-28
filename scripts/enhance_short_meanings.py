#!/usr/bin/env python3
"""
Enhance short meanings in vocabulary_content_new.csv using AI models.

This script:
- Scans all entries in data/vocabulary_content_new.csv
- Identifies meanings that are too short (default: < 25 characters)
- Uses AI models to generate richer but concise meanings
- Writes an updated CSV: data/vocabulary_content_new_enhanced.csv
  (the original file is left untouched)

Run from the project root:
    python3 scripts/enhance_short_meanings.py
"""

import csv
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.ai_content_service import ai_content_service


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "vocabulary_content_new.csv"
OUTPUT_FILE = DATA_DIR / "vocabulary_content_new_enhanced.csv"
BACKUP_FILE = DATA_DIR / "vocabulary_content_new.backup.csv"


def load_rows() -> List[dict]:
    if not INPUT_FILE.exists():
        print(f"[ERROR] Input file not found: {INPUT_FILE}")
        sys.exit(1)

    with INPUT_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if "word" not in reader.fieldnames or "meaning" not in reader.fieldnames:
        print("[ERROR] CSV must contain 'word' and 'meaning' columns.")
        sys.exit(1)

    return rows


def identify_short_meanings(
    rows: List[dict], min_length: int = 25
) -> List[Tuple[int, dict]]:
    """Return list of (index, row) for rows with short meanings."""
    short = []
    for idx, row in enumerate(rows):
        meaning = (row.get("meaning") or "").strip()
        if meaning and len(meaning) < min_length:
            short.append((idx, row))
    return short


def enhance_meaning_with_ai(word: str, current_meaning: str) -> Optional[str]:
    """
    Enhance a short meaning using AI models.
    Returns an enhanced meaning or None if generation fails.
    """
    if not ai_content_service.is_available():
        print("[ERROR] AI Content Service is not available.")
        return None
    
    return ai_content_service.generate_enhanced_meaning(word, current_meaning)


def enhance_rows(rows: List[dict]) -> None:
    short_entries = identify_short_meanings(rows)
    total_short = len(short_entries)

    if total_short == 0:
        print("[INFO] No short meanings found. Nothing to enhance.")
        return

    print(f"[INFO] Found {total_short} entries with short meanings.")
    print("[INFO] Enhancing meanings using AI models...")

    if not ai_content_service.is_available():
        print("[ERROR] AI Content Service is not available.")
        print("[ERROR] Cannot proceed with enhancement.")
        return

    enhanced_count = 0
    skipped_count = 0

    for idx, row in short_entries:
        word = (row.get("word") or "").strip()
        current_meaning = (row.get("meaning") or "").strip()

        if not word or not current_meaning:
            skipped_count += 1
            continue

        print(f"\n---\nWord: {word}")
        print(f"Current meaning: {current_meaning}")

        new_meaning = enhance_meaning_with_ai(word, current_meaning)

        if not new_meaning:
            print("[WARN] AI generation failed, keeping original.")
            skipped_count += 1
            continue

        # Basic sanity check – must be at least as long as original
        if len(new_meaning) <= len(current_meaning):
            print(
                "[WARN] Enhanced meaning not longer than original, "
                "keeping original."
            )
            skipped_count += 1
            continue

        print(f"Enhanced meaning: {new_meaning}")
        rows[idx]["meaning"] = new_meaning
        enhanced_count += 1

    print("\n[INFO] Enhancement complete.")
    print(f"[INFO] Enhanced meanings for {enhanced_count} entries.")
    print(f"[INFO] Kept original meanings for {skipped_count} entries.")


def write_output(rows: List[dict], fieldnames: List[str]) -> None:
    # Safety: create a backup of the original file the first time this runs
    if not BACKUP_FILE.exists():
        INPUT_FILE.replace(BACKUP_FILE)
        print(f"[INFO] Backed up original file to: {BACKUP_FILE.name}")
        # Re-write INPUT_FILE from backup contents so we don't lose it
        with BACKUP_FILE.open("r", encoding="utf-8", newline="") as src, INPUT_FILE.open(
            "w", encoding="utf-8", newline=""
        ) as dst:
            dst.write(src.read())

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[INFO] Wrote enhanced CSV to: {OUTPUT_FILE}")


def main() -> None:
    print("[INFO] Loading vocabulary content...")
    rows = load_rows()

    # Preserve original header order
    with INPUT_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

    enhance_rows(rows)
    write_output(rows, fieldnames)


if __name__ == "__main__":
    main()

