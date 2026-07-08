#!/usr/bin/env python3
"""Sync generated ML assets from utils/Scripts into the iOS app bundle.

This is the final, previously-manual hop of the asset pipeline: the generator
scripts write to utils/Scripts/{Embeddings/ModelAssets,outputs}, while the app
consumes copies under Bhagavad-Gita-Verses-iOS-App/Shared/Inference. This script
makes that copy explicit and auditable.

By default it runs in DRY-RUN mode and only reports which files would change
(compared by SHA-256). Pass --write to actually copy. Run it from the repo root:

    python utils/Scripts/sync_assets_to_app.py            # report only
    python utils/Scripts/sync_assets_to_app.py --write     # apply changes

Note: the CoreML model packages (E5SmallV2.mlpackage, MiniLML6CE / CrossEncoder)
and tokenizer folders are intentionally NOT synced here — they change rarely and
are large; copy them manually when regenerated. This script covers the small
JSON/binary index + map files that change on every corpus refresh.
"""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

# Repo-root-relative (src, dst) pairs.
ASSET_PAIRS = [
    (
        "utils/Scripts/Embeddings/ModelAssets/lessons_meta.json",
        "Bhagavad-Gita-Verses-iOS-App/Shared/Inference/Retriever/Index/lessons_meta.json",
    ),
    (
        "utils/Scripts/Embeddings/ModelAssets/lessons_f32.bin",
        "Bhagavad-Gita-Verses-iOS-App/Shared/Inference/Retriever/Index/lessons_f32.bin",
    ),
    (
        "utils/Scripts/outputs/lesson_units.json",
        "Bhagavad-Gita-Verses-iOS-App/Shared/Inference/swift/lesson_units.json",
    ),
    (
        "utils/Scripts/outputs/verse_to_lesson.json",
        "Bhagavad-Gita-Verses-iOS-App/Shared/Inference/swift/verse_to_lesson.json",
    ),
    (
        "utils/Scripts/outputs/cold_start_map.json",
        "Bhagavad-Gita-Verses-iOS-App/Shared/Inference/swift/cold_start_map.json",
    ),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def find_repo_root(start: Path) -> Path:
    """Walk up until we find the directory that contains utils/ and the app folder."""
    for candidate in [start, *start.parents]:
        if (candidate / "utils" / "Scripts").is_dir() and (
            candidate / "Bhagavad-Gita-Verses-iOS-App"
        ).is_dir():
            return candidate
    raise SystemExit("Could not locate repo root (needs utils/Scripts and the app folder).")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="apply changes (default: dry-run report only)")
    args = ap.parse_args()

    root = find_repo_root(Path(__file__).resolve().parent)
    changed, missing, unchanged = [], [], []

    for src_rel, dst_rel in ASSET_PAIRS:
        src, dst = root / src_rel, root / dst_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        if dst.exists() and sha256(src) == sha256(dst):
            unchanged.append(dst_rel)
        else:
            changed.append((src, dst, src_rel, dst_rel, dst.exists()))

    mode = "WRITE" if args.write else "DRY-RUN"
    print(f"[{mode}] asset sync — repo root: {root}\n")

    for rel in unchanged:
        print(f"  = unchanged  {rel}")
    for src, dst, src_rel, dst_rel, existed in changed:
        verb = "would update" if not args.write else "updating"
        if not existed:
            verb = "would create" if not args.write else "creating"
        print(f"  ~ {verb}  {dst_rel}\n               from {src_rel}")
        if args.write:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for rel in missing:
        print(f"  ! MISSING source (regenerate first): {rel}")

    print(
        f"\nSummary: {len(unchanged)} unchanged, {len(changed)} "
        f"{'changed' if not args.write else 'written'}, {len(missing)} missing."
    )
    if changed and not args.write:
        print("Re-run with --write to apply.")
    if missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
