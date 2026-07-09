#!/usr/bin/env python3
"""Apply the modern re-voicing overlay to the v3 draft:
- swap each lesson's text for its re-voiced version
- drop lessons marked keep:false (un-modernizable metaphysics/ritual)
- re-embed the NEW texts in the E5 retrieval space and recompute near-dup flags
Rewrites lessons_v3_draft.json + lessons_v3_review.json in place."""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[0] / "outputs"
REV = Path("/tmp/claude-501/-Users-snehal-Desktop-Software-Projects-Gita-Project/757d2111-2ca0-4174-84d5-e80cd327676f/scratchpad/revoice")
VERSES = ROOT / "Bhagavad-Gita-Verses-iOS-App/Shared/Resources/verses-formatted.json"
NEAR_DUP_TH = 0.93

def main():
    draft = json.load(open(OUT / "lessons_v3_draft.json"))
    verse_text = {(int(r["chapterNumber"]), int(r["verseNumber"])): r["text"] for r in json.load(open(VERSES))}

    overlay = {}
    for f in sorted(REV.glob("grp_*_revoiced.json")):
        for L in json.load(open(f))["lessons"]:
            overlay[int(L["id"])] = L
    missing = [L["cluster_id"] for L in draft["lessons"] if L["cluster_id"] not in overlay]
    if missing:
        print(f"WARNING: {len(missing)} lessons had no re-voicing overlay: {missing[:20]}")

    kept = []
    dropped = []
    for L in draft["lessons"]:
        ov = overlay.get(L["cluster_id"])
        if ov is None:
            kept.append(L); continue           # no overlay -> keep original text
        if not ov.get("keep", True):
            dropped.append({"orig_id": L["cluster_id"], "chapter": L["chapter"],
                            "old_text": L["text"], "reason": ov.get("note", "")})
            continue
        L = dict(L)
        L["orig_id"] = L["cluster_id"]
        L["old_text"] = L["text"]
        L["text"] = ov["text"].strip()
        if ov.get("note"): L["revoice_note"] = ov["note"]
        kept.append(L)

    # renumber sequentially
    for i, L in enumerate(kept):
        L["cluster_id"] = i

    # re-embed new texts + near-dups
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("intfloat/e5-small-v2")
    emb = np.asarray(model.encode([f"passage: {L['text']}" for L in kept],
                     normalize_embeddings=True, batch_size=64, show_progress_bar=False), dtype="float32")
    S = emb @ emb.T; np.fill_diagonal(S, -1)
    dup = defaultdict(list)
    n = len(kept)
    for i in range(n):
        for j in range(i + 1, n):
            if S[i, j] >= NEAR_DUP_TH:
                dup[i].append({"id": j, "score": round(float(S[i, j]), 3)})
                dup[j].append({"id": i, "score": round(float(S[i, j]), 3)})
    for L in kept:
        L["near_dups"] = sorted(dup.get(L["cluster_id"], []), key=lambda d: -d["score"])

    covered = set()
    for L in kept:
        for cv in L["verse_cvs"]:
            c, v = cv.split(":"); covered.add((int(c), int(v)))
    total_app = len({(int(r["chapterNumber"]), int(r["verseNumber"])) for r in json.load(open(VERSES))})
    flagged = sum(1 for L in kept if L["near_dups"])
    audit = {
        "total_lessons": len(kept), "dropped_in_revoice": len(dropped),
        "app_verse_count": total_app, "verses_in_a_lesson": len(covered),
        "lesson_coverage_pct": round(100 * len(covered) / total_app, 1),
        "near_dup_threshold": NEAR_DUP_TH, "similarity_method": f"E5 semantic (passage:), threshold {NEAR_DUP_TH}, MODERN re-voiced texts",
        "lessons_flagged_near_dup": flagged,
        "per_chapter_counts": {ch: sum(1 for L in kept if L["chapter"] == ch) for ch in range(1, 19)},
    }
    json.dump({"audit": audit, "lessons": kept, "skipped": draft.get("skipped", []), "dropped_in_revoice": dropped},
              open(OUT / "lessons_v3_draft.json", "w"), indent=1, ensure_ascii=False)

    review = {"audit": audit, "chapters": [], "id_text": {L["cluster_id"]: L["text"] for L in kept}}
    for ch in range(1, 19):
        chl = [L for L in kept if L["chapter"] == ch]
        review["chapters"].append({
            "chapter": ch,
            "lessons": [{
                "id": L["cluster_id"], "text": L["text"], "best_verse": L["best_verse"],
                "rationale": L.get("rationale", ""), "old_text": L.get("old_text", ""),
                "verses": [{"ref": cv, "text": verse_text.get((int(cv.split(':')[0]), int(cv.split(':')[1])), "")} for cv in L["verse_cvs"]],
                "near_dups": L["near_dups"],
            } for L in chl],
            "skipped": [s for s in draft.get("skipped", []) if s["chapter"] == ch],
        })
    json.dump(review, open(OUT / "lessons_v3_review.json", "w"), indent=1, ensure_ascii=False)

    print("=== re-voiced v3.1 ===")
    for k, v in audit.items():
        if k != "per_chapter_counts": print(f"  {k}: {v}")
    print("  per_chapter:", audit["per_chapter_counts"])
    print(f"  dropped {len(dropped)} lessons in re-voicing")

if __name__ == "__main__":
    main()
