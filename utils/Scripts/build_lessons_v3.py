#!/usr/bin/env python3
"""Merge per-chapter draft lessons into a single v3 corpus, validate coverage,
and flag semantic near-duplicates in the real E5 retrieval space.

Inputs:  scratchpad/chapters/chNN_lessons.json  (one per chapter, authored per-chapter)
         Shared/Resources/verses-formatted.json (ground-truth verse text)
Outputs: outputs/lessons_v3_draft.json           (merged corpus + audit metadata)
         outputs/lessons_v3_review.json           (compact payload for the review HTML)
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import defaultdict
import numpy as np

ROOT = Path(__file__).resolve().parents[2]          # repo root
SCRATCH = Path("/tmp/claude-501/-Users-snehal-Desktop-Software-Projects-Gita-Project/757d2111-2ca0-4174-84d5-e80cd327676f/scratchpad/chapters")
VERSES = ROOT / "Bhagavad-Gita-Verses-iOS-App/Shared/Resources/verses-formatted.json"
OUT = ROOT / "utils/Scripts/outputs"
NEAR_DUP_TH = 0.93

def expand(rng: str):
    ch, rest = rng.split(":")
    if "-" in rest:
        a, b = rest.split("-")
        return [(int(ch), v) for v in range(int(a), int(b) + 1)]
    return [(int(ch), int(rest))]

def main():
    verse_text = {}
    per_ch_verses = defaultdict(set)
    for r in json.load(open(VERSES)):
        c, v = int(r["chapterNumber"]), int(r["verseNumber"])
        verse_text[(c, v)] = r["text"]
        per_ch_verses[c].add(v)

    lessons = []
    skipped_all = []
    problems = []
    shared_verses = []
    for ch in range(1, 19):
        f = SCRATCH / f"ch{ch:02d}_lessons.json"
        if not f.exists():
            problems.append(f"MISSING chapter file: {f.name}")
            continue
        doc = json.load(open(f))
        covered_here = set()
        for L in doc.get("lessons", []):
            cvs = []
            for rng in L["verses"]:
                for cv in expand(rng):
                    cvs.append(cv)
            for cv in cvs:
                if cv in covered_here:
                    shared_verses.append(f"{cv[0]}:{cv[1]}")   # intentional: multi-virtue verse mined into several lessons
                covered_here.add(cv)
            lessons.append({
                "chapter": ch,
                "text": L["text"].strip(),
                "verses": L["verses"],
                "best_verse": L.get("best_verse"),
                "rationale": L.get("rationale", ""),
                "verse_cvs": [f"{c}:{v}" for c, v in cvs],
            })
        for s in doc.get("skipped", []):
            skipped_all.append({"chapter": ch, "v": s["v"], "reason": s.get("reason", "")})
            covered_here.add((ch, s["v"]))
        # coverage check for this chapter
        missing = sorted(per_ch_verses[ch] - {v for (c, v) in covered_here if c == ch})
        if missing:
            problems.append(f"ch{ch}: {len(missing)} verses neither in a lesson nor skipped: {missing[:12]}")

    # assign ids
    for i, L in enumerate(lessons):
        L["cluster_id"] = i

    # ---- Embed in the real E5 retrieval space for semantic near-dup flags ----
    dupflags = defaultdict(list)
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("intfloat/e5-small-v2")
        emb = model.encode([f"passage: {L['text']}" for L in lessons],
                           normalize_embeddings=True, batch_size=64, show_progress_bar=False)
        emb = np.asarray(emb, dtype="float32")
        S = emb @ emb.T
        n = len(lessons)
        np.fill_diagonal(S, -1)
        for i in range(n):
            for j in range(i + 1, n):
                if S[i, j] >= NEAR_DUP_TH:
                    dupflags[i].append({"id": j, "score": round(float(S[i, j]), 3)})
                    dupflags[j].append({"id": i, "score": round(float(S[i, j]), 3)})
        sim_note = f"E5 semantic (passage:), threshold {NEAR_DUP_TH}"
    except Exception as e:
        sim_note = f"embedding unavailable ({e}); no semantic flags"

    for L in lessons:
        L["near_dups"] = sorted(dupflags.get(L["cluster_id"], []), key=lambda d: -d["score"])

    total_app_verses = sum(len(vs) for vs in per_ch_verses.values())
    covered_by_lessons = set()
    for L in lessons:
        for cv in L["verse_cvs"]:
            c, v = cv.split(":"); covered_by_lessons.add((int(c), int(v)))
    flagged = sum(1 for L in lessons if L["near_dups"])

    audit = {
        "total_lessons": len(lessons),
        "total_skipped": len(skipped_all),
        "app_verse_count": total_app_verses,
        "verses_in_a_lesson": len(covered_by_lessons),
        "lesson_coverage_pct": round(100 * len(covered_by_lessons) / total_app_verses, 1),
        "near_dup_threshold": NEAR_DUP_TH,
        "similarity_method": sim_note,
        "lessons_flagged_near_dup": flagged,
        "problems": problems,
        "shared_verse_count": len(set(shared_verses)),
        "shared_verses": sorted(set(shared_verses)),
        "per_chapter_counts": {ch: sum(1 for L in lessons if L["chapter"] == ch) for ch in range(1, 19)},
    }

    OUT.mkdir(parents=True, exist_ok=True)
    json.dump({"audit": audit, "lessons": lessons, "skipped": skipped_all},
              open(OUT / "lessons_v3_draft.json", "w"), indent=1, ensure_ascii=False)

    # compact review payload (with verse text inlined)
    review = {"audit": audit, "chapters": []}
    for ch in range(1, 19):
        chl = [L for L in lessons if L["chapter"] == ch]
        review["chapters"].append({
            "chapter": ch,
            "lessons": [{
                "id": L["cluster_id"], "text": L["text"], "best_verse": L["best_verse"],
                "rationale": L["rationale"],
                "verses": [{"ref": cv, "text": verse_text.get((int(cv.split(':')[0]), int(cv.split(':')[1])), "")} for cv in L["verse_cvs"]],
                "near_dups": L["near_dups"],
            } for L in chl],
            "skipped": [s for s in skipped_all if s["chapter"] == ch],
        })
    # id -> text for near-dup rendering
    review["id_text"] = {L["cluster_id"]: L["text"] for L in lessons}
    json.dump(review, open(OUT / "lessons_v3_review.json", "w"), indent=1, ensure_ascii=False)

    print("=== v3 corpus build ===")
    for k, val in audit.items():
        if k != "per_chapter_counts":
            print(f"  {k}: {val}")
    print("  per_chapter_counts:", audit["per_chapter_counts"])
    if problems:
        print("  !! PROBLEMS:"); [print("     -", p) for p in problems]
    else:
        print("  no coverage/overlap problems")

if __name__ == "__main__":
    main()
