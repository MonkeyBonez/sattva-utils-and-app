#!/usr/bin/env python3
"""On-device explainer model bake-off.

Runs candidate small MLX models against the app's REAL explanation prompt
(mirrored verbatim from Shared/Inference/llm/VerseExplainer.swift) over a spread
of verse + user-situation cases, then writes a JSON dump and an HTML comparison
page for side-by-side quality review.

Usage:
    python bakeoff.py --models qwen1_5 llama1b llama3b
    python bakeoff.py --list          # show model registry and exit

The point is to judge OUTPUT QUALITY locally on the Mac before committing a model
to the app (where the iPhone 14 Pro / A16 test measures speed + memory, not text).
"""
import argparse
import json
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (repo layout)
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[3]          # .../Gita Project
APP = REPO / "Bhagavad-Gita-Verses-iOS-App"
VERSES = APP / "Shared/Resources/verses-formatted.json"
V2L = APP / "Shared/Inference/swift/verse_to_lesson.json"
META = APP / "Shared/Inference/Retriever/Index/lessons_meta.json"
OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Model registry — MLX community 4-bit builds (what would ship on-device)
# ---------------------------------------------------------------------------
MODELS = {
    "llama1b": ("Llama-3.2-1B-Instruct", "mlx-community/Llama-3.2-1B-Instruct-4bit", "~0.7 GB"),
    "qwen1_5": ("Qwen2.5-1.5B-Instruct", "mlx-community/Qwen2.5-1.5B-Instruct-4bit", "~0.9 GB"),
    "llama3b": ("Llama-3.2-3B-Instruct", "mlx-community/Llama-3.2-3B-Instruct-4bit", "~1.8 GB"),
    "qwen3b":  ("Qwen2.5-3B-Instruct",   "mlx-community/Qwen2.5-3B-Instruct-4bit",   "~1.8 GB"),
}

# ---------------------------------------------------------------------------
# App prompt, mirrored verbatim from VerseExplainer.swift
# ---------------------------------------------------------------------------
# --- Mode A: verse-first (the as-built #5 prompt) ---
INSTRUCTIONS = """\
You explain how a single line from the Bhagavad Gita applies to an ordinary person's life today.
Rules:
- Be concrete and practical. No preaching, no religious jargon, no "thou".
- 2–3 short sentences, plain modern English.
- Ground your explanation in the scene provided (who is speaking, what is happening), but speak to the reader's own life.
- If the reader shared a situation, connect the verse directly to it."""

# --- Mode B: lesson-first (the decided #6 "lesson spotlight") ---
# The LESSON is the subject; the verse is only its source. The task is to connect
# the reader's guidance moment to the lesson — not to explain the verse.
INSTRUCTIONS_LESSON = """\
You help a reader take in a single life lesson and connect it to what they are going through right now.
Rules:
- The lesson is the point. Speak about the lesson and the reader's moment.
- Be concrete and practical. No preaching, no religious jargon, no "thou".
- 2–3 short sentences, plain modern English, addressed to "you".
- Do not quote or restate the verse, and do not mention chapter or verse numbers. No sign-off."""

CAST = ("Cast: Arjuna, a warrior prince paralyzed by doubt on a battlefield; Krishna, his "
        "charioteer and guide, who delivers the teaching; Sanjaya, who narrates the scene to the "
        "blind king Dhritarashtra.")

CHAPTERS = {
    1:  ("Arjuna's despair", "Facing his own kin across the battlefield, Arjuna loses his nerve and refuses to fight.", "Arjuna to Krishna"),
    2:  ("The nature of the self and steady action", "Krishna begins the core teaching: act without clinging to results.", "Krishna to Arjuna"),
    3:  ("Action as service", "Krishna argues no one can avoid action, so act selflessly.", "Krishna to Arjuna"),
    4:  ("Knowledge behind action", "Krishna explains how wisdom frees action from its grip.", "Krishna to Arjuna"),
    5:  ("Renunciation and action reconciled", "Krishna shows that acting selflessly and renouncing lead to the same peace.", "Krishna to Arjuna"),
    6:  ("Meditation and self-mastery", "Krishna teaches how to steady a restless mind.", "Krishna to Arjuna"),
    7:  ("Knowledge and realization", "Krishna describes how the divine underlies all things.", "Krishna to Arjuna"),
    8:  ("The imperishable and the final moment", "Krishna on what endures and how a life's focus shapes its end.", "Krishna to Arjuna"),
    9:  ("The royal secret of devotion", "Krishna reveals that sincere devotion, however humble, is enough.", "Krishna to Arjuna"),
    10: ("Divine glory in all things", "Krishna names where his presence shows most vividly in the world.", "Krishna to Arjuna"),
    11: ("The cosmic vision", "Krishna reveals his overwhelming universal form; Arjuna is awed and humbled.", "Krishna and Arjuna"),
    12: ("The path of devotion", "Krishna describes the qualities of a steady, good-hearted person.", "Krishna to Arjuna"),
    13: ("The field and its knower", "Krishna distinguishes the body from the awareness that observes it.", "Krishna to Arjuna"),
    14: ("The three forces that drive us", "Krishna maps clarity, restlessness, and inertia as the forces behind behavior.", "Krishna to Arjuna"),
    15: ("The supreme person", "Krishna on cutting attachment and finding what is highest.", "Krishna to Arjuna"),
    16: ("Divine and destructive traits", "Krishna contrasts the qualities that free a person with those that ruin them.", "Krishna to Arjuna"),
    17: ("Faith in three forms", "Krishna shows how temperament shapes what we eat, say, and give.", "Krishna to Arjuna"),
    18: ("Freedom through surrender", "Krishna's closing summation: do your own duty, release the results.", "Krishna to Arjuna"),
}


def build_prompt(chapter, verse, verse_text, lesson, situation):
    """Mode A — verse-first. Mirror of ExplanationPrompt.prompt(_:userSituation:)."""
    theme, scene, speakers = CHAPTERS.get(
        chapter, ("A teaching from the Gita", "Krishna counsels Arjuna.", "Krishna to Arjuna"))
    p = (f"{CAST}\n\n"
         f"Chapter {chapter} — {theme}.\n"
         f"Scene: {scene} ({speakers})\n"
         f'Verse {chapter}:{verse}: "{verse_text}"')
    if lesson:
        p += f'\nThe app frames this as: "{lesson}"'
    s = (situation or "").strip()
    if s:
        p += f'\n\nThe reader says: "{s}"\nExplain how this verse speaks to their situation.'
    else:
        p += "\n\nExplain why this verse still matters for someone's everyday life."
    return p


def build_prompt_lesson(chapter, verse, verse_text, lesson, situation):
    """Mode B — lesson-first (#6 lesson spotlight). Lesson is the headline the reader
    was pointed to; the verse is only a parenthetical source note to prevent hallucination.
    The task is to connect the reader's guidance moment to the lesson."""
    theme, scene, speakers = CHAPTERS.get(
        chapter, ("A teaching from the Gita", "Krishna counsels Arjuna.", "Krishna to Arjuna"))
    headline = lesson or verse_text
    p = (f'The lesson: "{headline}"\n'
         f"(Source, do not quote: Gita {chapter}:{verse}, {speakers} — {scene})")
    s = (situation or "").strip()
    if s:
        p += f'\n\nThe reader came here feeling / seeking: "{s}"'
        p += "\n\nWrite the connection: how this lesson meets their moment, and what it asks of them today."
    else:
        p += "\n\nWrite the connection: why this lesson matters in an ordinary life today, and what it asks of someone."
    return p


# ---------------------------------------------------------------------------
# Test cases — realistic guidance queries a user would type / land on
# (chapter, verse, situation-or-None). Verse text + lesson pulled from app data.
# ---------------------------------------------------------------------------
CASES = [
    (2, 47, "I'm anxious about a big work deadline and whether it'll be good enough."),
    (2, 22, "I just lost my grandmother and I can't stop grieving."),
    (2, 14, "Everything feels overwhelming and I can't calm down."),
    (6, 5,  "I keep beating myself up over my mistakes."),
    (3, 35, "I feel pressure to follow the career my parents want, not mine."),
    (2, 62, "I can't stop being angry at a coworker who wronged me."),
    (18, 66, "I feel guilty and scared I've made too many wrong choices."),
    (12, 13, None),   # no situation — generic everyday relevance
    (6, 35,  "My mind races at night and I can't focus during the day."),
    (2, 48, "I'm afraid to start my project because I might fail."),
]


def load_data(mode):
    verses = json.load(open(VERSES))
    vmap = {(v["chapterNumber"], v["verseNumber"]): v["text"] for v in verses}
    v2l = json.load(open(V2L))
    texts = json.load(open(META))["texts"]
    builder = build_prompt_lesson if mode == "lesson" else build_prompt

    def lesson_for(ch, vs):
        idx = v2l.get(f"{ch}:{vs}")
        return texts[idx] if idx is not None and 0 <= idx < len(texts) else None

    cases = []
    for ch, vs, sit in CASES:
        vt = vmap.get((ch, vs))
        if vt is None:
            print(f"  ! no verse text for {ch}:{vs}, skipping")
            continue
        cases.append({
            "chapter": ch, "verse": vs, "verseText": vt,
            "lesson": lesson_for(ch, vs), "situation": sit,
            "prompt": builder(ch, vs, vt, lesson_for(ch, vs), sit),
        })
    return cases


def run_model(key, cases, max_tokens, temp, system):
    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler
    name, repo, size = MODELS[key]
    print(f"\n=== {name} ({repo}, {size}) ===")
    t0 = time.time()
    model, tok = load(repo)
    load_s = time.time() - t0
    sampler = make_sampler(temp=temp)
    rows = []
    for i, c in enumerate(cases, 1):
        msgs = [{"role": "system", "content": system},
                {"role": "user", "content": c["prompt"]}]
        chat = tok.apply_chat_template(msgs, add_generation_prompt=True)
        g0 = time.time()
        out = generate(model, tok, prompt=chat, max_tokens=max_tokens,
                       sampler=sampler, verbose=False)
        dt = time.time() - g0
        n_tok = len(tok.encode(out))
        tps = n_tok / dt if dt else 0
        print(f"  [{i}/{len(cases)}] {c['chapter']}:{c['verse']}  {dt:.1f}s  {tps:.0f} tok/s")
        rows.append({**c, "output": out.strip(), "gen_s": round(dt, 2),
                     "tok": n_tok, "tok_s": round(tps, 1)})
    return {"key": key, "name": name, "repo": repo, "size": size,
            "load_s": round(load_s, 2), "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["llama1b", "qwen1_5", "llama3b"])
    ap.add_argument("--max-tokens", type=int, default=200)
    ap.add_argument("--temp", type=float, default=0.5)   # matches app GenerationOptions
    ap.add_argument("--mode", choices=["verse", "lesson"], default="verse",
                    help="verse = as-built #5 prompt; lesson = #6 lesson-spotlight (lesson-first)")
    ap.add_argument("--out", default="bakeoff_results.json")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for k, (n, r, s) in MODELS.items():
            print(f"  {k:10s} {n:28s} {s:8s} {r}")
        return

    system = INSTRUCTIONS_LESSON if args.mode == "lesson" else INSTRUCTIONS
    cases = load_data(args.mode)
    print(f"Loaded {len(cases)} test cases. Mode: {args.mode}")
    results = [run_model(k, cases, args.max_tokens, args.temp, system) for k in args.models]

    (OUT / args.out).write_text(json.dumps(
        {"cases": cases, "results": results, "temp": args.temp,
         "max_tokens": args.max_tokens, "mode": args.mode}, indent=2))
    print(f"\nWrote {OUT / args.out}")


if __name__ == "__main__":
    main()
