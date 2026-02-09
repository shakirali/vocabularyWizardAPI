#!/usr/bin/env python3
"""Append rows (level, word, quiz_sentence) to a quiz sentences CSV.
Usage: python append_quiz_batch.py --level 3 < path_to_batch.csv
       python append_quiz_batch.py --level 2 < path_to_batch.csv
Reads CSV from stdin; each row: level,word,quiz_sentence (or word,quiz_sentence with level from --level).
"""
import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", type=str, default="2", help="Level (1-4) for output path and default level")
    args = ap.parse_args()
    level = args.level.strip()
    out_path = ROOT / "data" / f"quiz_sentences_level{level}_new.csv"
    if not out_path.exists():
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write("level,word,quiz_sentence\n")
    rows = []
    reader = csv.reader(sys.stdin)
    for r in reader:
        if len(r) >= 3:
            rows.append((r[0].strip(), r[1].strip(), r[2].strip()))
        elif len(r) == 2:
            rows.append((level, r[0].strip(), r[1].strip()))
    if not rows:
        print("No rows to append", file=sys.stderr)
        sys.exit(1)
    with open(out_path, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for lev, word, sent in rows:
            w.writerow([lev, word, sent])
    print(f"Appended {len(rows)} rows to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
