# Gita Project — repo guide

A SwiftUI Bhagavad Gita verses app with home/lock-screen widgets, weekly
notifications, and an on-device ML feature that maps an emotion (typed, picked
from an emotion wheel, or chosen by color) to a relevant verse/lesson.

## Layout

- `Bhagavad-Gita-Verses-iOS-App/` — **git submodule**, the Xcode project. This is
  where all app code lives. Three targets: the app (`Bhagavad Gita Verses`),
  `Widgets`, and `App Intent Extension`. Shared code (models, inference, notifications)
  lives in `Shared/` and is compiled into multiple targets via explicit target
  membership in the pbxproj.
- `utils/Scripts/` — Python ML pipeline that generates the app's inference assets.
- `utils/website/`, `DesignExamples/`, `DemoAnimations/` — non-app design/reference
  material; not part of any build.

The submodule tracks branch `release/3.3-wip` (per `.gitmodules`). The submodule's
`main` is a stale divergent branch — do not base work on it.

## Building & testing (run inside the submodule)

```sh
cd Bhagavad-Gita-Verses-iOS-App
xcodebuild build -scheme "Bhagavad Gita Verses" -destination 'platform=iOS Simulator,name=iPhone 16'
xcodebuild test  -scheme "Bhagavad Gita Verses" -destination 'platform=iOS Simulator,name=iPhone 16'
```

Building the app scheme also builds the embedded Widgets and App Intent extensions.
Unit tests live in `BhagavadGitaVersesTests/` (Swift Testing) and cover the pure,
deterministic logic. The test target is a hosted bundle (`@testable import
Bhagavad_Gita_Verses`); its pbxproj wiring was added via the Ruby `xcodeproj` gem.

Persistence keys are centralized in `Shared/Model/DefaultsKeys.swift` — add new
UserDefaults keys there, never as inline string literals (a typo orphans user data).

## On-device inference

Two independent flows, both consuming assets from the bundle:

- **Weekly pick** (`Shared/Inference/swift/WeeklySelector.swift`): `SattvaWeeklyHeuristic`
  clusters the user's bookmark embeddings and picks a lesson; falls back to
  `ColdStartWeeklyHeuristic` (reads `cold_start_map.json`) when there are no bookmarks.
  `WeeklyPickSync` persists one pick per week (Sunday anchor) in the App Group.
- **Guidance search** (`Shared/Inference/swift/LessonSearchHelper.swift`): E5 retriever
  (`E5SmallV2.mlpackage`) → cosine top-K over `lessons_f32.bin`/`lessons_meta.json`
  → MiniLM cross-encoder rerank (`MiniLML6CE`). Invoked from `VerseView.runGuidanceSearch`.

## ML asset regeneration → app

Source of truth for lessons: `utils/Scripts/outputs/Final V1.1/finalClusters_FINAL_v2.json`
(396 lessons as of the last refresh).

Regeneration chain (from repo root, with the venv active — see `utils/requirements.txt`):

1. `generate_assets_from_final_v2.py` → `Embeddings/lessons.txt` + `outputs/lesson_units.json`
2. `build_embeddings.py` → `Embeddings/lessons_e5_small_v2.npz`
3. `npz_to_modelassets.py` → `Embeddings/ModelAssets/{lessons_meta.json, lessons_f32.bin}`
4. `build_bookmark_map.py` → `outputs/verse_to_lesson.json` (+ `verse_to_lessons_all.json`)
5. `generate_cold_start_map.py` → `outputs/cold_start_map.json`
6. CoreML models: `convert_e5_coreml.py`, `convert_minilm_ce_coreml.py`, verified with
   `parity_check_coreml.py` (models live under `Embeddings/ModelAssets/`).

**Final hop — copy into the app bundle:** `python utils/Scripts/sync_assets_to_app.py`
(dry-run by default; `--write` to apply). It syncs the small JSON/binary index +
map files. The CoreML `.mlpackage` folders and tokenizers are large and change
rarely — copy those manually into `Shared/Inference/Retriever/Model`,
`Shared/Inference/cross-encoder/Model`, and the `Tokenizer` folders when regenerated.

## Known landmines

- **Two notification schedulers coexist** in `Shared/Notifications/WeeklyNotificationScheduler.swift`.
  The legacy weekly-reminder path (`weekly_lesson_reminder_*` IDs) is still wired to
  deeplink opens in `Bhagavad Gita Verses App/BhagavadGitaApp.swift`, while the current
  backlog/streak system (`regular_*`/`streak_*` IDs, `reconcileBacklogAndStreak`) actively
  deletes the legacy IDs via `migrateLegacyIfNeeded`. Reconcile to a single owner before
  doing any notification feature work.
- **`cold_start_map.json` drift**: the copy in the app bundle currently differs from
  `utils/Scripts/outputs/cold_start_map.json` (the sync script's dry-run flags it). Confirm
  which is correct and reconcile deliberately — this is exactly the drift the manual copy
  process caused.
- **Emotion-wheel query templates** (`EmotionQueryBuilder` in `EmotionWheelModel.swift`):
  currently Option B (`overcome X and Y`) for negative roots (Sad/Mad/Scared) and the
  `I feel…` format for positive roots. `utils/Scripts/outputs/template_comparison_analysis.md`
  shows Option C beats the current format for the positive roots (Joyful/Powerful/Peaceful) —
  the data-backed next step if revisiting retrieval quality.
- **App Group migration**: `AppGroupMigration` v2 (`migrateStandardToAppGroupIfNeeded`) fixes a
  v1 bug where the migration read from the App Group instead of `UserDefaults.standard` and so
  never ran. v2 union-merges bookmarks and copies other keys only if absent. Keep it idempotent
  (guarded by `DefaultsKeys.appGroupMigratedV2`).
