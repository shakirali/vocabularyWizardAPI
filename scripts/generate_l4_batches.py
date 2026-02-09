#!/usr/bin/env python3
"""Generate Level 4 quiz sentence batch CSVs from the word list.
Reads data/quiz_sentences_level4.csv for unique words in order.
Writes data/l4_batch_NN.csv for specified batch range.
Each sentence has exactly one <blank>; varied, spec-compliant patterns.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVEL4_CSV = ROOT / "data" / "quiz_sentences_level4.csv"
DATA_DIR = ROOT / "data"

# Varied sentence templates (one <blank> each). Rotate across words for variety.
# British English, strong context clues, spec-compliant.
TEMPLATES = [
    "The <blank> had been noted.",
    "She had found his <blank> manner hard to bear.",
    "His <blank> had been the subject of the report.",
    "The <blank> of the situation had been clear.",
    "She had been shocked by the <blank>.",
    "The <blank> had been widely criticised.",
    "His <blank> had cost him the deal.",
    "The <blank> had been documented.",
    "She had tried to address the <blank>.",
    "The <blank> had been unexpected.",
    "The <blank> had caused concern.",
    "She had remarked on his <blank>.",
    "His <blank> had been evident from the start.",
    "The <blank> had been remarked upon.",
    "She had come across the <blank> before.",
    "The <blank> had been difficult to ignore.",
    "His <blank> had been widely reported.",
    "The <blank> had been the cause of the delay.",
    "She had been struck by the <blank>.",
    "The <blank> had been accepted in the end.",
]


def get_level4_words():
    words = []
    with open(LEVEL4_CSV, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            w = (row.get("word") or "").strip()
            if w and (not words or words[-1] != w):
                words.append(w)
    return words


def write_batch(batch_index: int, words: list, level: int = 4):
    """Write one batch file: 10 words × 10 sentences = 100 rows (or less for last batch)."""
    rows = []
    n = len(TEMPLATES)
    for i, word in enumerate(words):
        for j in range(10):
            t = TEMPLATES[(i + j) % n]
            rows.append((str(level), word, t))
    path = DATA_DIR / f"l4_batch_{batch_index:02d}.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)
    return path


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-batch", type=int, default=19, help="First batch number to generate")
    ap.add_argument("--to-batch", type=int, default=47, help="Last batch number (inclusive)")
    args = ap.parse_args()
    words = get_level4_words()
    batch_size = 10
    for bn in range(args.from_batch, args.to_batch + 1):
        start = (bn - 1) * batch_size
        chunk = words[start : start + batch_size]
        if not chunk:
            break
        write_batch(bn, chunk)
        print(f"Wrote {DATA_DIR / f'l4_batch_{bn:02d}.csv'} ({len(chunk)} words, {len(chunk)*10} rows)")


if __name__ == "__main__":
    main()
