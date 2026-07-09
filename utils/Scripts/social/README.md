# Sattvic social content pipeline

Turns lessons from the corpus into ready-to-post, on-brand images + captions for Instagram
and X, plus a scheduling manifest. Built to be driven by a scheduled cloud agent (roadmap #8).

## Run

```sh
python utils/Scripts/social/generate_posts.py \
  --lessons utils/Scripts/outputs/lessons_v3_draft.json \
  --count 7 --start-date 2026-07-13 --platforms ig,x --out utils/Scripts/social/out
```

Produces, per day:
- `ig/<date>_lesson<id>.png` — 1080×1350 portrait (Instagram feed)
- `x/<date>_lesson<id>.png` — 1600×900 landscape (X)
- `manifest.json` — one entry per post: `{date, platform, format, lesson_id, verse, image, caption}`

Content selection is **deterministic**, seeded by `--start-date` (a hash rotation over the
corpus) — the same date always yields the same queue, so re-runs are idempotent and a scheduler
can regenerate without drift.

## Design

Echoes the app's identity: parchment ground with a subtle gradient, the lavender feather-eye
mark, `SATTVIC` wordmark and the lesson in **EB Garamond** (the app's serif), verse reference and
`@sattvic.app` handle in Source Sans. Lesson font-size auto-fits to ≤4 lines. See `samples/`.

Captions: Instagram gets a hook + one-line reflection + follow CTA + 10 hashtags; X gets a tight
≤280-char form with 3 hashtags.

## Notes / next steps

- **Corpus dependency**: defaults to the modern re-voiced lessons (`lessons_v3_draft.json` from
  the corpus regen). Point `--lessons` at any corpus with `{lessons:[{cluster_id,text,best_verse}]}`.
- **Posting** is intentionally out of scope here — the manifest is the hand-off. A scheduled agent
  can read `manifest.json` and post via the IG Graph API / X API on each `date`. That's the
  "plumbing once the format is designed" noted in the ideas doc.
- Story (1080×1920) and carousel formats are easy additions to `FORMATS`.
