#!/usr/bin/env python3
"""
Examine Level 2 quiz sentences using Ollama (gemma3) and the project's spec.

Reads:
  - data/quiz_sentences_level2.csv
  - specifications/vocabularySpecification.md

Writes:
  - reports/quiz_sentences_level2_ollama_report.json
  - reports/quiz_sentences_level2_ollama_summary.md

Notes:
  - The current Level 2 CSV is not spec-compliant (uses `sentence` column + `_____`).
    This script reports those as issues and also provides a normalised view that
    replaces `_____` with `<blank>` for semantic evaluation.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _safe_json_loads(s: str) -> Any:
    s = s.strip()
    # Ollama sometimes returns extra whitespace; occasionally models wrap JSON.
    # Try strict first, then a best-effort slice from first '{'/'[' to last '}'/']'.
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        starts = [i for i in (s.find("{"), s.find("[")) if i != -1]
        if not starts:
            raise
        start = min(starts)
        end_obj = s.rfind("}")
        end_arr = s.rfind("]")
        end = max(end_obj, end_arr)
        if end == -1 or end <= start:
            raise
        return json.loads(s[start : end + 1])


def _coerce_results_list(parsed: Any) -> List[Dict[str, Any]]:
    """
    Accept either:
      - a JSON array of result objects, or
      - a JSON object containing a list under a common key (e.g. {"results":[...]}).
    """
    if isinstance(parsed, list):
        return [x for x in parsed if isinstance(x, dict)]
    if isinstance(parsed, dict):
        for k in ("results", "items", "output", "data"):
            v = parsed.get(k)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]
    raise RuntimeError("Model output was valid JSON but not a results list or container object.")


def _post_json(url: str, payload: Dict[str, Any], timeout_s: int) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to reach Ollama at {url}: {e}") from e


def ollama_chat(
    *,
    base_url: str,
    model: str,
    system: str,
    user: str,
    timeout_s: int,
    temperature: float = 0.2,
    response_format: Optional[Dict[str, Any]] = None,
) -> str:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", "api/chat")
    payload: Dict[str, Any] = {
        "model": model,
        "stream": False,
        "format": response_format or "json",
        "options": {"temperature": temperature},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    res = _post_json(url, payload, timeout_s=timeout_s)
    msg = (res.get("message") or {}).get("content")
    if not isinstance(msg, str) or not msg.strip():
        raise RuntimeError(f"Unexpected Ollama response shape (no message.content). Keys: {list(res.keys())}")
    return msg


def extract_spec_excerpt(spec_text: str) -> str:
    """
    Keep the examiner focused by extracting the quiz-sentence-specific rules + the examiner section.
    We still read the spec from file (as requested) but avoid sending 100% of it each call.
    """
    lines = spec_text.splitlines()

    def grab_section(start_marker: str, end_marker: str) -> List[str]:
        start = None
        for i, ln in enumerate(lines):
            if ln.strip() == start_marker:
                start = i
                break
        if start is None:
            return []
        out = []
        for ln in lines[start:]:
            if ln.strip() == end_marker:
                break
            out.append(ln)
        return out

    # British English requirement
    british = grab_section("## British English Requirement (mandatory)", "---")

    # Quiz sentences criteria (shared criteria subsection)
    quiz_criteria = grab_section("### Quiz sentences must", "---")

    parts = []
    if british:
        parts.append("\n".join(british).strip())
    if quiz_criteria:
        parts.append("\n".join(quiz_criteria).strip())
    # Examiner mandatory self-check (short)
    examiner = grab_section("### Mandatory self-check", "---")
    if examiner:
        parts.append("\n".join(examiner[:12]).strip())

    excerpt = "\n\n---\n\n".join([p for p in parts if p])
    if not excerpt:
        # fallback: send whole spec if markers ever change
        excerpt = spec_text
    return excerpt


def ollama_output_schema() -> Dict[str, Any]:
    """
    JSON Schema to strongly constrain model output and avoid empty `{}` responses.
    """
    return {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "word": {"type": "string"},
                        "overall": {
                            "type": "object",
                            "properties": {
                                "pass": {"type": "boolean"},
                                "notes": {"type": "array", "items": {"type": "string"}},
                            },
                            "required": ["pass", "notes"],
                            "additionalProperties": True,
                        },
                        "sentences": {
                            "type": "array",
                            "minItems": 10,
                            "maxItems": 10,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "index": {"type": "integer", "minimum": 1, "maximum": 10},
                                    "row_index": {"type": "integer", "minimum": 2},
                                    "pass": {"type": "boolean"},
                                    "issues": {"type": "array", "items": {"type": "string"}},
                                    "scores": {
                                        "type": "object",
                                        "properties": {
                                            "accuracy": {"type": "integer", "minimum": 1, "maximum": 5},
                                            "clarity": {"type": "integer", "minimum": 1, "maximum": 5},
                                            "educational_usefulness": {"type": "integer", "minimum": 1, "maximum": 5},
                                        },
                                        "required": ["accuracy", "clarity", "educational_usefulness"],
                                        "additionalProperties": True,
                                    },
                                },
                                "required": ["index", "row_index", "pass", "issues", "scores"],
                                "additionalProperties": True,
                            },
                        },
                    },
                    "required": ["word", "overall", "sentences"],
                    "additionalProperties": True,
                },
            }
        },
        "required": ["results"],
        "additionalProperties": True,
    }


@dataclass(frozen=True)
class SentenceRow:
    level: str
    word: str
    sentence_raw: str
    row_index: int  # 1-based row number in file (including header as row 1)


def normalise_placeholder(s: str) -> Tuple[str, Dict[str, Any]]:
    """
    Normalise common placeholders to <blank> for semantic evaluation.
    Returns (normalised_sentence, placeholder_metadata)
    """
    meta: Dict[str, Any] = {
        "raw_blank_count": s.count("<blank>"),
        "raw_underscore_runs": s.count("_____"),
        "uses_blank_tag": "<blank>" in s,
        "uses_underscores": "_____" in s,
    }

    # Replace underscore blanks with <blank> for model evaluation.
    s2 = s.replace("_____", "<blank>")
    meta["normalised_blank_count"] = s2.count("<blank>")
    return s2, meta


def load_level2_csv(path: Path) -> Tuple[List[str], List[SentenceRow]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        # Find the sentence field name
        sentence_key = None
        for k in ("quiz_sentence", "sentence"):
            if k in headers:
                sentence_key = k
                break
        if sentence_key is None:
            raise RuntimeError(f"Could not find a sentence column in headers: {headers}")

        # level field should be present; word too
        if "level" not in headers or "word" not in headers:
            raise RuntimeError(f"CSV must contain 'level' and 'word' columns. Found: {headers}")

        rows: List[SentenceRow] = []
        # DictReader starts after header; treat header as row 1
        row_num = 1
        for row in reader:
            row_num += 1
            rows.append(
                SentenceRow(
                    level=(row.get("level") or "").strip(),
                    word=(row.get("word") or "").strip(),
                    sentence_raw=(row.get(sentence_key) or "").strip(),
                    row_index=row_num,
                )
            )
    return headers, rows


def chunked(xs: List[Any], n: int) -> Iterable[List[Any]]:
    for i in range(0, len(xs), n):
        yield xs[i : i + n]


def build_prompt_payload(words_batch: List[str], per_word_sentences: Dict[str, List[SentenceRow]]) -> Dict[str, Any]:
    payload_words = []
    for w in words_batch:
        items = per_word_sentences[w]
        sents = []
        for idx, row in enumerate(items, start=1):
            normalised, meta = normalise_placeholder(row.sentence_raw)
            required_issues: List[str] = []
            if meta.get("uses_underscores"):
                required_issues.append("placeholder_not_<blank>")
            if meta.get("normalised_blank_count") != 1:
                required_issues.append("blank_count_not_1")
            sents.append(
                {
                    "index": idx,
                    "row_index": row.row_index,
                    "sentence_normalised": normalised,
                    "required_issues": required_issues,
                }
            )
        payload_words.append({"word": w, "sentences": sents})
    return {"words": payload_words}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "data/quiz_sentences_level2.csv"))
    ap.add_argument("--spec", default=str(ROOT / "specifications/vocabularySpecification.md"))
    ap.add_argument("--model", default="gemma3:latest")
    ap.add_argument("--ollama-url", default=os.environ.get("OLLAMA_URL", "http://localhost:11434"))
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--batch-size", type=int, default=5, help="Words per Ollama request")
    ap.add_argument("--max-words", type=int, default=0, help="0 = all words")
    ap.add_argument("--retries", type=int, default=1, help="Retries per request on invalid/incomplete model output")
    ap.add_argument("--sleep-ms", type=int, default=0, help="Optional pause between requests")
    ap.add_argument("--debug", action="store_true", help="Print raw model outputs on parse/shape errors")
    ap.add_argument(
        "--out-jsonl",
        default=str(ROOT / "reports/quiz_sentences_level2_ollama_results.jsonl"),
        help="Append-only per-word results (for resume).",
    )
    ap.add_argument("--resume", action="store_true", help="Resume from --out-jsonl if it exists.")
    ap.add_argument("--out-json", default=str(ROOT / "reports/quiz_sentences_level2_ollama_report.json"))
    ap.add_argument("--out-md", default=str(ROOT / "reports/quiz_sentences_level2_ollama_summary.md"))
    args = ap.parse_args()

    input_path = Path(args.input)
    spec_path = Path(args.spec)
    out_jsonl = Path(args.out_jsonl)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)

    spec_text = _read_text(spec_path)
    spec_excerpt = extract_spec_excerpt(spec_text)

    headers, rows = load_level2_csv(input_path)

    # Group by word (only level==2 rows are expected, but we don't assume)
    per_word: Dict[str, List[SentenceRow]] = defaultdict(list)
    level_counts = Counter()
    for r in rows:
        level_counts[r.level] += 1
        per_word[r.word].append(r)

    words = sorted([w for w in per_word.keys() if w])
    if args.max_words and args.max_words > 0:
        words = words[: args.max_words]

    # Resume support (append-only JSONL of per-word results)
    results_by_word: Dict[str, Dict[str, Any]] = {}
    if args.resume and out_jsonl.exists():
        with out_jsonl.open("r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    obj = json.loads(ln)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict) and isinstance(obj.get("word"), str) and obj["word"]:
                    results_by_word[obj["word"]] = obj

    words_to_process = [w for w in words if w not in results_by_word]
    if args.resume and results_by_word:
        print(f"Resuming: {len(results_by_word)} words already in {out_jsonl}. Remaining: {len(words_to_process)}.")

    # Pre-checks
    count_not_10 = sum(1 for w in words if len(per_word[w]) != 10)
    underscore_rows = 0
    blank_tag_rows = 0
    blank_bad_rows = 0
    for w in words:
        for r in per_word[w]:
            normalised, meta = normalise_placeholder(r.sentence_raw)
            if meta["uses_underscores"]:
                underscore_rows += 1
            if meta["uses_blank_tag"]:
                blank_tag_rows += 1
            if normalised.count("<blank>") != 1:
                blank_bad_rows += 1

    system = (
        "You are a Vocabulary examiner.\n"
        "Use the provided specification excerpt as the authoritative rules.\n"
        "Return STRICT JSON only (no markdown, no extra commentary).\n"
        "You are evaluating existing sentences; do not rewrite unless specifically asked.\n"
    )

    user_prefix = (
        "Specification excerpt (authoritative):\n"
        + spec_excerpt
        + "\n\n"
        + "Task:\n"
        + "- Evaluate the quiz sentences for each word against the spec.\n"
        + "- Each sentence should be short, natural, story-like, with strong context clues.\n"
        + "- Spec requires exactly one <blank> per sentence. Some inputs use '_____' instead; treat that as a spec violation.\n"
        + "- Use sentence_normalised (where '_____' has been replaced with '<blank>') to judge context/meaning, but still flag the placeholder mismatch.\n"
        + "- For each input word, return one result object. For each input sentence, return one sentence result.\n"
        + "- Do not return an empty response. If something is unclear, mark pass=false and explain in notes/issues.\n"
        + "- IMPORTANT: Every sentence has a required_issues list.\n"
        + "  - You MUST include ALL required_issues in the output issues for that sentence.\n"
        + "  - If required_issues is non-empty, pass MUST be false.\n"
        + "  - Even if required_issues is empty, pass should still be false if quality is below spec.\n"
        + "\n\n"
        + "Issue tags you may use (only when applicable):\n"
        + "- placeholder_not_<blank>\n"
        + "- blank_count_not_1\n"
        + "- missing_context\n"
        + "- not_story_like\n"
        + "- definition_style\n"
        + "- grammar\n"
        + "- ambiguity\n"
        + "- too_vague\n"
        + "- uses_direct_synonym\n"
        + "- repetitive_pattern\n"
        + "- american_spelling\n"
        + "\n"
        + "Score each sentence 1–5 for accuracy, clarity, and educational usefulness (per spec).\n"
        + "Treat any score < 4 as below spec.\n"
    )

    # Run batches through Ollama
    start = time.time()

    def run_request(words_batch: List[str], req_label: str) -> List[Dict[str, Any]]:
        payload = build_prompt_payload(words_batch, per_word)
        user = user_prefix + "\n\nInput:\n" + json.dumps(payload, ensure_ascii=False)

        last_err: Optional[Exception] = None
        last_msg: Optional[str] = None
        for attempt in range(args.retries + 1):
            try:
                msg = ollama_chat(
                    base_url=args.ollama_url,
                    model=args.model,
                    system=system,
                    user=user,
                    timeout_s=args.timeout,
                    temperature=0.0,
                    response_format=ollama_output_schema(),
                )
                last_msg = msg
                parsed = _safe_json_loads(msg)
                out = _coerce_results_list(parsed)
                return out
            except Exception as e:
                last_err = e
                last_msg = msg if "msg" in locals() else None
                if args.debug:
                    print(f"[{req_label}] attempt {attempt+1} error: {e}", file=sys.stderr)
                    if last_msg:
                        print("\n--- raw model output (truncated) ---", file=sys.stderr)
                        print(last_msg[:2000], file=sys.stderr)
        raise RuntimeError(f"{req_label} failed after retries: {last_err}")

    # Ensure JSONL parent exists early
    _ensure_parent(out_jsonl)

    for b_idx, words_batch in enumerate(chunked(words_to_process, args.batch_size), start=1):
        try:
            batch_out = run_request(words_batch, req_label=f"batch {b_idx}")
        except Exception as e:
            print(f"[batch {b_idx}] ERROR: {e}", file=sys.stderr)
            print("Tip: ensure Ollama is running (e.g. `ollama serve`) and the model is installed (`ollama pull gemma3`).", file=sys.stderr)
            # Keep whatever was already written to JSONL; exit non-zero so caller knows it stopped early.
            break

        expected = set(words_batch)
        returned = {str(o.get("word")) for o in batch_out if isinstance(o, dict) and o.get("word")}
        # Keep only results for expected words
        kept = [o for o in batch_out if isinstance(o, dict) and str(o.get("word")) in expected]
        missing = sorted(expected - returned)

        # Persist kept results immediately (checkpoint)
        with out_jsonl.open("a", encoding="utf-8") as f:
            for obj in kept:
                w = str(obj.get("word"))
                if w:
                    results_by_word[w] = obj
                    f.write(json.dumps(obj, ensure_ascii=False) + "\n")
                    f.flush()

        # If the model omitted some words, fall back to per-word calls for the missing ones
        for w in missing:
            try:
                one_out = run_request([w], req_label=f"batch {b_idx} fallback word={w}")
                # take first matching word result
                match = next((o for o in one_out if isinstance(o, dict) and str(o.get("word")) == w), None)
                if match:
                    results_by_word[w] = match
                    with out_jsonl.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(match, ensure_ascii=False) + "\n")
                        f.flush()
                else:
                    results_by_word[w] = {"word": w, "overall": {"pass": False, "notes": ["Model did not return an entry for this word."]}, "sentences": []}
            except Exception as e:
                results_by_word[w] = {"word": w, "overall": {"pass": False, "notes": [f"Model request failed: {e}"]}, "sentences": []}

        if args.sleep_ms and args.sleep_ms > 0:
            time.sleep(args.sleep_ms / 1000.0)

        elapsed = time.time() - start
        done = len([w for w in words if w in results_by_word])
        print(f"Processed batch {b_idx} ({len(words_batch)} words). Total words processed: {done}/{len(words)}. Elapsed: {elapsed:.1f}s")

    # Summarise model results
    # Index results by word (last one wins if duplicates)
    by_word: Dict[str, Dict[str, Any]] = dict(results_by_word)

    per_word_overall: Dict[str, bool] = {}
    per_word_overall_ignoring_placeholder: Dict[str, bool] = {}
    total_sentence_results = 0
    total_sentence_fail = 0
    total_sentence_fail_ignoring_placeholder = 0
    issue_counts = Counter()
    for w in words:
        obj = by_word.get(w) or {"word": w, "overall": {"pass": False, "notes": ["No model output for this word."]}, "sentences": []}

        overall = obj.get("overall") or {}

        # Validate sentence coverage and merge required_issues as a backstop.
        sents_out = obj.get("sentences") or []
        if not isinstance(sents_out, list):
            sents_out = []

        # Build a quick map of required issues from input
        required_map: Dict[int, List[str]] = {}
        for idx, row in enumerate(per_word[w], start=1):
            _, meta = normalise_placeholder(row.sentence_raw)
            req = []
            if meta.get("uses_underscores"):
                req.append("placeholder_not_<blank>")
            if meta.get("normalised_blank_count") != 1:
                req.append("blank_count_not_1")
            required_map[idx] = req

        expected_n = len(per_word[w])
        seen_indexes: set[int] = set()

        # Count issues + enforce required issues + recompute pass based on spec
        sentence_pass_flags: List[bool] = []
        sentence_pass_flags_ignoring_placeholder: List[bool] = []
        for s in sents_out:
            total_sentence_results += 1
            idx = s.get("index")
            if isinstance(idx, int):
                seen_indexes.add(idx)
            issues = s.get("issues") or []
            if not isinstance(issues, list):
                issues = []
            # Enforce required issues being present
            if isinstance(idx, int) and idx in required_map:
                for req_issue in required_map[idx]:
                    if req_issue not in issues:
                        issues.append(req_issue)
            # If any required issues exist, consider sentence failing
            if isinstance(idx, int) and required_map.get(idx):
                s["pass"] = False
            s["issues"] = issues

            # Treat any score < 4 as below spec
            scores = s.get("scores") or {}
            if not isinstance(scores, dict):
                scores = {}
            acc = scores.get("accuracy")
            cla = scores.get("clarity")
            edu = scores.get("educational_usefulness")
            if all(isinstance(v, int) for v in (acc, cla, edu)):
                if min(acc, cla, edu) < 4:
                    s["pass"] = False
                    if "below_spec_score" not in issues:
                        issues.append("below_spec_score")
                    s["issues"] = issues

            sentence_pass_flags.append(bool(s.get("pass", False)))

            if not s.get("pass", False):
                total_sentence_fail += 1
            for issue in issues:
                issue_counts[str(issue)] += 1

            # Compute alternate pass/fail ignoring placeholder format mismatch
            issues_wo_placeholder = [i for i in issues if i != "placeholder_not_<blank>"]
            alt_pass = True
            if "blank_count_not_1" in issues_wo_placeholder:
                alt_pass = False
            if "below_spec_score" in issues_wo_placeholder:
                alt_pass = False
            # Any other issue is also considered a fail for the alternate metric
            other = [i for i in issues_wo_placeholder if i not in ("blank_count_not_1", "below_spec_score")]
            if other:
                alt_pass = False
            sentence_pass_flags_ignoring_placeholder.append(bool(alt_pass))
            if not alt_pass:
                total_sentence_fail_ignoring_placeholder += 1

        # Account for missing model outputs for some sentence indices
        missing_indices = [i for i in range(1, expected_n + 1) if i not in seen_indexes]
        if missing_indices:
            # Missing outputs are failures (not enough evidence to pass)
            for _ in missing_indices:
                total_sentence_results += 1
                total_sentence_fail += 1
                issue_counts["missing_model_output"] += 1
            sentence_pass_flags.extend([False] * len(missing_indices))
            sentence_pass_flags_ignoring_placeholder.extend([False] * len(missing_indices))
            total_sentence_fail_ignoring_placeholder += len(missing_indices)

        # Recompute word-level pass strictly
        per_word_overall[w] = (expected_n == 10) and bool(sentence_pass_flags) and all(sentence_pass_flags)
        per_word_overall_ignoring_placeholder[w] = (expected_n == 10) and bool(sentence_pass_flags_ignoring_placeholder) and all(
            sentence_pass_flags_ignoring_placeholder
        )
        if not per_word_overall[w]:
            notes = overall.get("notes") if isinstance(overall, dict) else None
            if not isinstance(notes, list):
                notes = []
            if expected_n != 10:
                notes.append(f"Word has {expected_n} rows in CSV (expected 10).")
            if missing_indices:
                notes.append(f"Model output missing indices: {missing_indices}")
            if not isinstance(overall, dict):
                overall = {"pass": False, "notes": notes}
            else:
                overall["pass"] = False
                overall["notes"] = notes
            obj["overall"] = overall

    # Write outputs
    report = {
        "generated_at": _now_iso(),
        "input_csv": str(input_path),
        "spec_file": str(spec_path),
        "ollama": {"base_url": args.ollama_url, "model": args.model},
        "csv_headers": headers,
        "csv_level_counts": dict(level_counts),
        "words_examined": len(words),
        "prechecks": {
            "words_not_10_sentences": count_not_10,
            "rows_using_underscores": underscore_rows,
            "rows_using_blank_tag": blank_tag_rows,
            "rows_with_blank_count_not_1_after_normalisation": blank_bad_rows,
        },
        "model_summary": {
            "words_pass": sum(1 for v in per_word_overall.values() if v),
            "words_fail": sum(1 for v in per_word_overall.values() if not v),
            "words_pass_ignoring_placeholder_not_blank": sum(1 for v in per_word_overall_ignoring_placeholder.values() if v),
            "words_fail_ignoring_placeholder_not_blank": sum(1 for v in per_word_overall_ignoring_placeholder.values() if not v),
            "sentence_results": total_sentence_results,
            "sentence_fail": total_sentence_fail,
            "sentence_fail_ignoring_placeholder_not_blank": total_sentence_fail_ignoring_placeholder,
            "top_issues": issue_counts.most_common(20),
        },
        "results": [by_word[w] for w in words if w in by_word],
    }

    _ensure_parent(out_json)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    _ensure_parent(out_md)
    md = []
    md.append("# Level 2 Quiz Sentences — Ollama Examination Report\n")
    md.append(f"- Generated at: `{report['generated_at']}`\n")
    md.append(f"- Input: `{report['input_csv']}`\n")
    md.append(f"- Spec: `{report['spec_file']}`\n")
    md.append(f"- Model: `{args.model}` via `{args.ollama_url}`\n")
    md.append("\n## Pre-checks\n")
    md.append(f"- Words examined: **{report['words_examined']}**\n")
    md.append(f"- Words not having exactly 10 sentences: **{report['prechecks']['words_not_10_sentences']}**\n")
    md.append(f"- Rows using `_____` (spec violation): **{report['prechecks']['rows_using_underscores']}**\n")
    md.append(f"- Rows already using `<blank>`: **{report['prechecks']['rows_using_blank_tag']}**\n")
    md.append(f"- Rows whose normalised `<blank>` count != 1: **{report['prechecks']['rows_with_blank_count_not_1_after_normalisation']}**\n")
    md.append("\n## Model summary\n")
    ms = report["model_summary"]
    md.append(f"- Words pass: **{ms['words_pass']}**\n")
    md.append(f"- Words fail: **{ms['words_fail']}**\n")
    md.append(f"- Words pass (ignoring placeholder_not_<blank>): **{ms['words_pass_ignoring_placeholder_not_blank']}**\n")
    md.append(f"- Words fail (ignoring placeholder_not_<blank>): **{ms['words_fail_ignoring_placeholder_not_blank']}**\n")
    md.append(f"- Sentence evaluations: **{ms['sentence_results']}**\n")
    md.append(f"- Sentences failing: **{ms['sentence_fail']}**\n")
    md.append(f"- Sentences failing (ignoring placeholder_not_<blank>): **{ms['sentence_fail_ignoring_placeholder_not_blank']}**\n")
    md.append("\n### Top issues\n")
    for issue, cnt in ms["top_issues"]:
        md.append(f"- **{issue}**: {cnt}\n")
    out_md.write_text("".join(md), encoding="utf-8")

    print(f"\nWrote JSON report: {out_json}")
    print(f"Wrote summary MD: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

