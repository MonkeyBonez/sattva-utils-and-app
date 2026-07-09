# Lesson corpus v3 — draft for review

A verse-first regeneration of the lesson corpus, replacing `Final V1.1/finalClusters_FINAL_v2.json`
(396 lessons, heavily redundant — 263 lessons fell into near-dup clusters at cosine ≥0.93,
the largest a single ~150-lesson blob).

**v3: 373 distinct lessons, only 30 near-dup-flagged at the same 0.93 threshold.**

## How it was made

Each of the 18 chapters was authored independently from its real verse text
(`Shared/Resources/verses-formatted.json`), grouping verses into distinct imperative lessons
and explicitly flagging narrative/theophany verses that warrant no lesson (all of Ch1's
battlefield roster, Ch10's vibhuti enumeration, Ch11's cosmic-form description). Per-chapter
drafts live in `lessons_v3_chapters/chNN_lessons.json`.

`build_lessons_v3.py` merges them, validates coverage (every verse is in a lesson or explicitly
skipped), and flags semantic near-duplicates by embedding every lesson in the **same E5 space the
app retrieves in** (`intfloat/e5-small-v2`, `passage:` prefix). Output: `lessons_v3_draft.json`.

## How to review  ← start here

Open the review tool (published artifact) **Sattvic · Lesson Corpus Review**, or open
`lessons_v3_review.html` directly in a browser.

- Each card = one drafted lesson: editable text, its **source verses in full**, the best verse,
  the authoring rationale, and any **≈ near-dup** badges (click a badge to jump to the twin).
- **Keep / Cut** each lesson; edit the text inline; add a note. Everything autosaves to your browser.
- I pre-reviewed the 13 near-dup clusters (`dedup_recommendations.json`). Each flagged card shows my
  call — **suggest cut / keep / distinct / review**. Click **Apply dedup suggestions** to set all 10
  suggested merges to Cut in one go, then eyeball the single "review" flag (cluster 1, lesson #81).
- Filter by **Near-dups / Cut / Undecided**, or search verse text.
- When done, click **Export decisions** → downloads `lesson_review_decisions.json`.

## How your decisions get applied (next step, after review)

Hand back `lesson_review_decisions.json`. It will be folded into `lessons_v3_draft.json`
(drop cuts, apply edited text, merge absorbed verses into survivors) to produce the final v3,
then the standard regeneration chain rebuilds every retrieval asset:

`generate_assets_from_final_v2` → `build_embeddings` → `npz_to_modelassets` →
`build_bookmark_map` → `generate_cold_start_map`, then `sync_assets_to_app.py --write`.

Nothing is synced into the app bundle until you approve the draft — this branch only contains the
proposal and tooling.
