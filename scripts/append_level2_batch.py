#!/usr/bin/env python3
"""Append rows (level, word, quiz_sentence) to data/quiz_sentences_level2_new.csv.
Usage: python append_level2_batch.py < path_to_batch.csv
Or:    python append_level2_batch.py --rows '2,word,"sentence with <blank>"'
Reads CSV from stdin or --rows, appends to data/quiz_sentences_level2_new.csv.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "quiz_sentences_level2_new.csv"


def main():
    rows = []
    if len(sys.argv) > 1 and sys.argv[1] == "--rows":
        # Single row or multiple rows separated by newline in one arg
        raw = sys.argv[2] if len(sys.argv) > 2 else ""
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Parse CSV line (level,word,quiz_sentence)
            r = next(csv.reader([line]))
            if len(r) >= 3:
                rows.append((r[0].strip(), r[1].strip(), r[2].strip()))
            elif len(r) == 2:
                rows.append(("2", r[0].strip(), r[1].strip()))
    else:
        reader = csv.reader(sys.stdin)
        for r in reader:
            if len(r) >= 3:
                rows.append((r[0].strip(), r[1].strip(), r[2].strip()))
            elif len(r) == 2:
                rows.append(("2", r[0].strip(), r[1].strip()))
    if not rows:
        print("No rows to append", file=sys.stderr)
        sys.exit(1)
    with open(OUT, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for level, word, sent in rows:
            w.writerow([level, word, sent])
    print(f"Appended {len(rows)} rows to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
