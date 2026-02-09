#!/usr/bin/env python3
"""
Check quality of quiz sentences for levels 1-4 against the vocabulary spec.

Criteria (from specifications/vocabularySpecification.md):
- Exactly one <blank> per sentence
- Use <blank> (not underscores) as placeholder
- Strong context clues; short, natural, story-like
- British English
- No repetitive patterns across the set
- No synonym giveaways in the same sentence

This script runs structural and heuristic checks and writes a report.
"""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

# American spellings that should be British in spec
AMERICAN_PATTERNS = [
    (r"\bcolor\b", "colour"),
    (r"\bbehavior\b", "behaviour"),
    (r"\bhonor\b", "honour"),
    (r"\bfavor\b", "favour"),
    (r"\blabor\b", "labour"),
    (r"\bcenter\b", "centre"),
    (r"\bfiber\b", "fibre"),
    (r"\btheater\b", "theatre"),
    (r"\brealize\b", "realise"),
    (r"\borganize\b", "organise"),
    (r"\brecognize\b", "recognise"),
    (r"\banalyze\b", "analyse"),
    (r"\bdefense\b", "defence"),
    (r"\boffense\b", "offence"),
    (r"\blicense\b", "licence"),  # noun
    (r"\bpractice\b", "practise"),  # verb
]


def get_sentence_column(row: dict) -> str | None:
    if "quiz_sentence" in row:
        return "quiz_sentence"
    if "sentence" in row:
        return "sentence"
    return None


def check_level(path: Path, level: int) -> dict[str, Any]:
    issues: list[dict] = []
    blank_ok = 0
    blank_wrong = 0
    underscore_placeholder = 0
    empty_or_very_short = 0
    american_spelling = []
    sentence_starts: Counter = Counter()
    word_counts: Counter = Counter()
    pairs: set[tuple[str, str]] = set()
    duplicates: list[tuple[str, str]] = []
    rows_with_commas_no_quote: list[int] = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        sent_col = None
        for i, row in enumerate(reader):
            if sent_col is None:
                sent_col = get_sentence_column(row)
                if not sent_col:
                    issues.append({"row": i + 2, "issue": "No quiz_sentence or sentence column"})
                    break
            raw = row.get(sent_col, "")
            word = (row.get("word") or "").strip()
            word_counts[word] += 1

            # Normalise: treat _____ as wrong placeholder
            if "_____" in raw:
                underscore_placeholder += 1
            n_blank = raw.count("<blank>")
            if n_blank == 1:
                blank_ok += 1
            else:
                blank_wrong += 1
                issues.append({
                    "row": i + 2,
                    "word": word,
                    "issue": "blank_count",
                    "count": n_blank,
                    "snippet": (raw[:60] + "…") if len(raw) > 60 else raw,
                })

            if len(raw.strip()) < 10:
                empty_or_very_short += 1
                issues.append({"row": i + 2, "word": word, "issue": "very_short", "snippet": raw[:80]})

            # Duplicate (word, sentence)
            key = (word, raw)
            if key in pairs:
                duplicates.append((word, raw[:50]))
            pairs.add(key)

            # Sentence start (first ~25 chars) for pattern diversity
            start = re.sub(r"\s+", " ", raw.strip())[:25]
            sentence_starts[start] += 1

            # American spelling
            for pat, brit in AMERICAN_PATTERNS:
                if re.search(pat, raw, re.I):
                    american_spelling.append({"row": i + 2, "word": word, "expected": brit, "snippet": raw[:80]})

    # Per-word count (should be 10)
    expected_per_word = 10
    wrong_count_words: list[tuple[str, int]] = []
    for w, c in word_counts.items():
        if c != expected_per_word:
            wrong_count_words.append((w, c))
    wrong_count_words.sort(key=lambda x: -x[1])

    # Repetitive starts: same start used too often (e.g. > 20)
    repetitive_starts = [ (start, cnt) for start, cnt in sentence_starts.most_common(20) if cnt > 15 ]

    return {
        "path": str(path),
        "level": level,
        "total_rows": blank_ok + blank_wrong,
        "blank_ok": blank_ok,
        "blank_wrong": blank_wrong,
        "underscore_placeholder": underscore_placeholder,
        "empty_or_very_short": empty_or_very_short,
        "duplicate_pairs": len(duplicates),
        "duplicate_examples": duplicates[:5],
        "wrong_per_word": wrong_count_words,
        "unique_words": len(word_counts),
        "american_spelling": american_spelling[:20],
        "repetitive_starts": repetitive_starts,
        "issues": issues[:50],
        "issues_truncated": len(issues) > 50,
    }


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    for level in (1, 2, 3, 4):
        path = DATA_DIR / f"quiz_sentences_level{level}.csv"
        if not path.exists():
            results[level] = {"error": f"File not found: {path}"}
            continue
        results[level] = check_level(path, level)

    # Summary report
    lines = [
        "# Quiz sentences quality check (Levels 1–4)",
        "",
        "Criteria: exactly one `<blank>` per sentence, no _____ placeholder, 10 sentences per word,",
        "no duplicate (word, sentence), British English, varied patterns.",
        "",
    ]
    for level in (1, 2, 3, 4):
        r = results[level]
        if "error" in r:
            lines.append(f"## Level {level}\n\n**Error:** {r['error']}\n")
            continue
        lines.append(f"## Level {level}")
        lines.append("")
        lines.append(f"- **Total rows:** {r['total_rows']}")
        lines.append(f"- **Unique words:** {r['unique_words']}")
        lines.append(f"- **Rows with exactly one `<blank>`:** {r['blank_ok']}")
        lines.append(f"- **Rows with wrong blank count:** {r['blank_wrong']}")
        lines.append(f"- **Rows with `_____` placeholder:** {r['underscore_placeholder']}")
        lines.append(f"- **Empty or very short sentences:** {r['empty_or_very_short']}")
        lines.append(f"- **Duplicate (word, quiz_sentence) pairs:** {r['duplicate_pairs']}")
        if r["wrong_per_word"]:
            lines.append(f"- **Words with ≠10 sentences:** {len(r['wrong_per_word'])} (e.g. {r['wrong_per_word'][:5]})")
        else:
            lines.append(f"- **Words with ≠10 sentences:** 0")
        if r["american_spelling"]:
            lines.append(f"- **Possible American spellings:** {len(r['american_spelling'])} (see report)")
        if r["repetitive_starts"]:
            lines.append(f"- **Repetitive sentence starts (count > 15):** {len(r['repetitive_starts'])}")
        lines.append("")
        if r["issues"]:
            lines.append("### Sample issues")
            lines.append("")
            for iss in r["issues"][:15]:
                lines.append(f"- Row {iss.get('row')}: {iss.get('issue', '')} {iss.get('snippet', '')}")
            if r.get("issues_truncated"):
                lines.append(f"- … and more (total {len(r['issues'])})")
            lines.append("")
        if r["american_spelling"]:
            lines.append("### American spelling examples")
            for a in r["american_spelling"][:10]:
                lines.append(f"- Row {a['row']}: expected {a['expected']} — {a['snippet'][:60]}…")
            lines.append("")
        if r["repetitive_starts"]:
            lines.append("### Most repeated sentence starts")
            for start, cnt in r["repetitive_starts"][:10]:
                lines.append(f"- ({cnt}x) `{start}…`")
            lines.append("")
        lines.append("---")
        lines.append("")

    report_path = REPORTS_DIR / "quiz_sentences_quality_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(report_path.read_text(encoding="utf-8"))

    # JSON for programmatic use
    import json
    json_path = REPORTS_DIR / "quiz_sentences_quality_report.json"
    def _serialise(obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, (tuple, list)):
            return [_serialise(x) for x in obj]
        if isinstance(obj, dict):
            return {k: _serialise(v) for k, v in obj.items()}
        return obj
    json_path.write_text(json.dumps(_serialise(results), indent=2), encoding="utf-8")
    print(f"\nJSON report: {json_path}")


if __name__ == "__main__":
    main()
