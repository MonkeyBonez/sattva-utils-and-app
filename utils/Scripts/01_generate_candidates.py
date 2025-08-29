#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_generate_candidates.py
-------------------------
Read units.jsonl (verse ranges), call GPT-4o-mini to generate candidate lessons,
and write to candidates.jsonl. Uses caching so we never re-call for the same unit.

Each candidate has:
  - lesson_id (UUID)
  - unit {chapter, start, end}
  - raw text (lesson or NONE)

If NONE → skipped.

Supports a --mock mode to generate deterministic fake lessons for testing without API calls.
"""

# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {
    "units_file": "units.jsonl",          # Input: verse ranges
    "out_file": "candidates.jsonl",       # Output: generated lessons
    "model_name": "gpt-4o-mini",          # OpenAI model
    "temperature": 0.2,                    # Lower = more deterministic
    "min_words": 3,                        # Sentence length limits
    "max_words": 14
}

# ============================================================
# SCRIPT
# ============================================================

import argparse
import json
import os
import re
import sys
import uuid
import hashlib
import time
from pathlib import Path
from typing import Dict, Iterable, Tuple, Optional

CLIENT = None  # OpenAI client singleton (initialized on first non-mock call)


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_path(repo_root: Path, path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else (repo_root / p).resolve()


def normalize(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def md5(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def word_count(s: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", s))


def is_one_sentence_short(s: str, min_words: int, max_words: int) -> bool:
    if s.count(".") + s.count("!") + s.count("?") > 1:
        return False
    wc = word_count(s)
    return min_words <= wc <= max_words


def make_prompt(unit_text: str, min_words: int, max_words: int) -> str:
    return (
        "The passage is from the Bhagavad Gita.\n"
        "Examples of valid lessons:\n"
        "• Act for duty, not reward.\n"
        "• Keep a steady flame of awareness.\n"
        "• See the same Self in all beings.\n"
        "• Restrain the senses; let reason guide.\n"
        "• Embrace impermanence; remain steady in joy and sorrow.\n"
        "• Cultivate compassion to free yourself from attachment.\n"
        "• Practice moderation for inner peace.\n"
        "• Attachment fades through self-knowledge.\n\n"
        "Extract exactly ONE short lesson from the passage below.\n"
        "Rules:\n"
        f"• Output exactly one sentence ({min_words}-{max_words} words).\n"
        "• If no clear lesson is present, output exactly: NONE\n"
        "• Write in plain, universal language. Do not use names, dialogue, or scripture references.\n"
        "• Do NOT output purely descriptive or metaphysical claims (e.g., 'The soul is eternal').\n"
        "• The lesson must be practical, timeless, and universally applicable.\n"
        "• Avoid situational statements tied to characters.\n"
        "• Express the lesson in positive, guiding language (e.g., “Act with clarity” not “Killing leads to sin”).\n"
        "• Do not describe events or doctrines; only output a universal practice or principle.\n"
        "• Express only ONE idea — do not join ideas with 'and', 'or', 'but', or ';'. \n"
        "• Output only the lesson sentence or NONE — nothing else.\n"
        "• Favor simplicity and clarity over completeness — capture the core lesson, not every dimension.\n"
        "• Do not include quotes, references, or extra text.\n\n"
        f"Passage:\n{unit_text}\n\n"
        "Answer with ONE sentence or NONE."
    )


def call_openai(prompt: str, cfg: dict) -> str:
    # Import here to avoid requiring the dependency in mock mode
    global CLIENT
    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:  # pragma: no cover - import guard
        raise RuntimeError(
            "openai package not available. Install openai or use --mock mode."
        ) from e

    if CLIENT is None:
        CLIENT = OpenAI()
    resp = CLIENT.chat.completions.create(
        model=cfg["model_name"],
        temperature=cfg["temperature"],
        max_tokens=40,
        messages=[
            {"role": "system", "content": "Extract a single short lesson or NONE."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content.strip()


def mock_generate(unit_text: str) -> str:
    """Deterministic, one-sentence dummy lesson for testing without API calls.

    Uses a hash of the text to pick a template and some keywords from the passage.
    Ensures 6-24 words and single sentence.
    """
    # Simple keyword extraction: take first 3 non-trivial words
    words = re.findall(r"[A-Za-z']{3,}", unit_text)
    keywords = [w.lower() for w in words[:3]] or ["duty", "mind", "self"]
    digest = int(md5(unit_text)[:8], 16)
    templates = [
        "Act with steady {0} and without attachment to results.",
        "Cultivate {0}, guide your {1}, and serve with sincerity.",
        "Let {0} lead, keep the {1} calm, and honor your duty.",
        "Choose disciplined {0}; avoid {1}; remain devoted to truth.",
        "Perform your duty with {0} and release desire for outcomes.",
    ]
    tpl = templates[digest % len(templates)]
    # Fill placeholders safely
    filled = tpl.format(*(keywords + ["heart", "action"]))
    # Ensure final punctuation and constraints
    sentence = filled.strip()
    if not sentence.endswith("."):
        sentence += "."
    # Adjust if out of bounds
    min_w, max_w = 6, 24
    if not is_one_sentence_short(sentence, min_w, max_w):
        sentence = "Act with discipline and without attachment to results."
    return sentence


def load_units(path: Path, limit: Optional[int]) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if limit is not None and idx >= limit:
                break
            yield json.loads(line)


def load_existing(path: Path) -> Dict[Tuple[int, int, int], dict]:
    if not path.exists():
        return {}
    seen: Dict[Tuple[int, int, int], dict] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            unit = row.get("unit", {})
            key = (int(unit["chapter"]), int(unit["start"]), int(unit["end"]))
            seen[key] = row
    return seen


def write_row(fp, row: dict) -> None:
    fp.write(json.dumps(row, ensure_ascii=False) + "\n")
    fp.flush()


def main() -> None:
    repo_root = resolve_repo_root()

    parser = argparse.ArgumentParser(
        description="Generate one-sentence lesson candidates for each verse unit (cached)"
    )
    parser.add_argument("-i", "--units-file", default=str(repo_root / CONFIG["units_file"]))
    parser.add_argument("-o", "--out-file", default=str(repo_root / CONFIG["out_file"]))
    parser.add_argument("--model-name", default=CONFIG["model_name"]) 
    parser.add_argument("--temperature", type=float, default=CONFIG["temperature"]) 
    parser.add_argument("--min-words", type=int, default=CONFIG["min_words"]) 
    parser.add_argument("--max-words", type=int, default=CONFIG["max_words"]) 
    parser.add_argument("--limit", type=int, default=None, help="Process only first N units")
    parser.add_argument("--mock", action="store_true", help="Use deterministic mock generation (no API)")
    parser.add_argument("--debug", action="store_true", help="Log filtering reasons and actions")
    # Rate limiting and retries
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls")
    parser.add_argument("--max-retries", type=int, default=4, help="Max retries on transient errors")
    parser.add_argument("--backoff-initial", type=float, default=1.0, help="Initial backoff seconds")
    parser.add_argument("--backoff-multiplier", type=float, default=2.0, help="Exponential backoff factor")
    # Optional unit filters to target specific spans and reduce API usage
    parser.add_argument("--chapter", type=int, default=None, help="Only process units from this chapter")
    parser.add_argument("--start", type=int, default=None, help="Only process units with this start verse")
    parser.add_argument("--end", type=int, default=None, help="Only process units with this end verse")
    args = parser.parse_args()

    units_path = resolve_path(repo_root, args.units_file)
    out_path = resolve_path(repo_root, args.out_file)

    # Load existing cache
    seen = load_existing(out_path)

    # Prepare output file (append mode)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_fp = out_path.open("a", encoding="utf-8")

    total_processed = 0
    total_skipped_cached = 0
    total_written = 0
    total_filtered = 0

    def debug(msg: str) -> None:
        if args.debug:
            print(f"[debug] {msg}", file=sys.stderr)

    def extract_first_sentence(text: str) -> str:
        # Capture first sentence ending with . ! or ?
        m = re.search(r"(.+?[\.\!\?])(?:\s|$)", text.strip())
        if m:
            return m.group(1).strip()
        return text.strip()

    def generate_with_retries(unit_text: str, prompt: str, key: Tuple[int, int, int]) -> Optional[str]:
        if args.mock:
            return mock_generate(unit_text).strip().strip('"')
        backoff = max(0.0, args.backoff_initial)
        for attempt in range(args.max_retries + 1):
            try:
                cfg = {"model_name": args.model_name, "temperature": args.temperature}
                return call_openai(prompt, cfg).splitlines()[0].strip().strip('"')
            except Exception as e:
                if attempt < args.max_retries:
                    debug(f"retry {attempt+1} after error: {e}")
                    time.sleep(backoff)
                    backoff = max(0.0, backoff * max(1.0, args.backoff_multiplier))
                    continue
                print(f"Error generating after retries for unit {key}: {e}", file=sys.stderr)
                return None

    processed_matches = 0
    for u in load_units(units_path, None):
        # Apply optional unit filters
        if args.chapter is not None and int(u.get("chapter")) != args.chapter:
            continue
        if args.start is not None and int(u.get("start")) != args.start:
            continue
        if args.end is not None and int(u.get("end")) != args.end:
            continue

        # Enforce post-filter limit
        if args.limit is not None and processed_matches >= args.limit:
            break

        processed_matches += 1
        total_processed += 1
        key = (int(u["chapter"]), int(u["start"]), int(u["end"]))
        if key in seen:
            total_skipped_cached += 1
            debug(f"cache-skip unit={key}")
            continue

        # Build prompt and generate
        prompt = make_prompt(u["text"], args.min_words, args.max_words)
        try:
            ans = generate_with_retries(u["text"], prompt, key)
        except Exception as e:
            print(f"Error generating for unit {key}: {e}", file=sys.stderr)
            total_filtered += 1
            continue
        if ans is None:
            total_filtered += 1
            continue

        if ans.upper() == "NONE":
            total_filtered += 1
            debug(f"filtered-none unit={key}")
            continue

        # If multi-sentence, fallback to first sentence
        if not is_one_sentence_short(ans, args.min_words, args.max_words):
            first = extract_first_sentence(ans)
            if first != ans:
                debug(f"fallback-first-sentence unit={key}")
            ans = first
            if not is_one_sentence_short(ans, args.min_words, args.max_words):
                total_filtered += 1
                debug(f"filtered-length unit={key} wc={word_count(ans)}")
                continue

        row = {
            "lesson_id": str(uuid.uuid4()),
            "unit": {"chapter": key[0], "start": key[1], "end": key[2]},
            "raw": ans,
        }
        write_row(out_fp, row)
        seen[key] = row
        total_written += 1
        debug(f"written unit={key} wc={word_count(ans)}")
        if args.sleep > 0 and not args.mock:
            time.sleep(args.sleep)

    out_fp.close()

    print(
        f"✅ Candidates written to {out_path} | processed={total_processed}, "
        f"cached_skipped={total_skipped_cached}, filtered={total_filtered}, written={total_written}"
    )


if __name__ == "__main__":
    main()


