#!/usr/bin/env python3
"""Sattvic social content pipeline.

Turns lessons from the corpus into ready-to-post, on-brand images + captions for
Instagram and X, plus a scheduling manifest. Designed to be run by a scheduled agent:

    python generate_posts.py --count 7 --start-date 2026-07-13 --platforms ig,x --out out/

Brand: parchment ground, peacock-green serif (EB Garamond), a lavender feather-eye mark
— echoing the app's identity.
"""
from __future__ import annotations
import argparse, json, textwrap, hashlib
from pathlib import Path
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[3]
FONT_DIR = REPO / "Bhagavad-Gita-Verses-iOS-App/Shared/Resources/Fonts"
SERIF = FONT_DIR / "EB_Garamond/EBGaramond-VariableFont_wght.ttf"
SANS = FONT_DIR / "EB_Garamond/SourceSans3-VariableFont_wght.ttf"

# Brand palette (from the app)
PARCHMENT = (237, 232, 216)
PARCHMENT_DEEP = (228, 221, 200)
PEACOCK = (31, 71, 53)
PEACOCK_SOFT = (61, 106, 79)
LAVENDER = (123, 92, 196)
INK_SOFT = (92, 107, 95)

FORMATS = {
    "ig_square":   (1080, 1080),
    "ig_portrait": (1080, 1350),
    "x_landscape": (1600, 900),
}

def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)

def load_lessons(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    out = []
    for L in data["lessons"]:
        out.append({"id": L["cluster_id"], "text": L["text"], "verse": L.get("best_verse", "")})
    return out

def wrap_to_width(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def fit_lesson(draw, text, w, max_w, start=96, min_size=52):
    """Largest serif size that keeps the lesson to <= 4 lines within max_w."""
    size = start
    while size >= min_size:
        fnt = font(SERIF, size)
        lines = wrap_to_width(draw, text, fnt, max_w)
        if len(lines) <= 4:
            return fnt, lines, size
        size -= 4
    fnt = font(SERIF, min_size)
    return fnt, wrap_to_width(draw, text, fnt, max_w), min_size

def feather_mark(draw, cx, cy, r):
    """A small lavender 'feather-eye' dot inside a peacock ring — the app's motif."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PEACOCK, width=max(2, r // 10))
    dr = int(r * 0.42)
    draw.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=LAVENDER)

def render(lesson: dict, fmt: str, out_path: Path):
    W, H = FORMATS[fmt]
    img = Image.new("RGB", (W, H), PARCHMENT)
    d = ImageDraw.Draw(img)
    # subtle vertical parchment gradient
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=tuple(int(PARCHMENT[i] + (PARCHMENT_DEEP[i] - PARCHMENT[i]) * t) for i in range(3)))
    margin = int(W * 0.11)

    # wordmark + mark (top)
    feather_mark(d, W // 2, int(H * 0.16), int(W * 0.035))
    wm = font(SERIF, int(W * 0.032))
    wtext = "SATTVIC"
    d.text(((W - d.textlength(wtext, font=wm)) / 2, int(H * 0.16) + int(W * 0.05)),
           wtext, font=wm, fill=PEACOCK_SOFT)

    # lesson (centered block)
    fnt, lines, size = fit_lesson(d, lesson["text"], W, W - 2 * margin)
    line_h = int(size * 1.28)
    block_h = line_h * len(lines)
    y = (H - block_h) // 2
    for ln in lines:
        d.text(((W - d.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=PEACOCK)
        y += line_h

    # verse ref + handle (bottom)
    ref = font(SANS, int(W * 0.026))
    handle = font(SANS, int(W * 0.022))
    handle_y = int(H * 0.92)
    if lesson["verse"]:
        rtext = f"Bhagavad Gita {lesson['verse']}"
        # keep the ref comfortably above the handle regardless of aspect ratio
        d.text(((W - d.textlength(rtext, font=ref)) / 2, handle_y - int(W * 0.06)),
               rtext, font=ref, fill=INK_SOFT)
    htext = "@sattvic.app"
    d.text(((W - d.textlength(htext, font=handle)) / 2, handle_y), htext, font=handle, fill=PEACOCK_SOFT)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")

HASHTAGS = ["#BhagavadGita", "#Gita", "#dailywisdom", "#mindfulness", "#stoicism",
            "#selfimprovement", "#philosophy", "#spirituality", "#Sattvic", "#innerpeace"]

def caption(lesson: dict, platform: str) -> str:
    verse = f"Bhagavad Gita {lesson['verse']}" if lesson["verse"] else "Bhagavad Gita"
    if platform == "x":
        # <=280 chars, tight
        base = f"{lesson['text']}\n\n— {verse}"
        tags = " ".join(HASHTAGS[:3])
        if len(base) + len(tags) + 2 <= 280:
            base += "\n" + tags
        return base
    # instagram: hook + reflection + tags
    return (f"{lesson['text']}\n\n"
            f"A 2,000-year-old idea that still lands today. {verse} reminds us to focus on "
            f"what's ours to control — the effort, not the outcome.\n\n"
            f"Follow @sattvic.app for a daily line from the Gita, in plain modern words.\n\n"
            + " ".join(HASHTAGS))

def pick(lessons, count, seed):
    """Deterministic rotation seeded by a string (e.g. start date) — no RNG needed."""
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    start = h % len(lessons)
    return [lessons[(start + i) % len(lessons)] for i in range(count)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lessons", default=str(REPO / "utils/Scripts/outputs/lessons_v3_draft.json"))
    ap.add_argument("--count", type=int, default=7)
    ap.add_argument("--start-date", default="2026-07-13")
    ap.add_argument("--platforms", default="ig,x")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "out"))
    args = ap.parse_args()

    lessons = load_lessons(Path(args.lessons))
    platforms = [p.strip() for p in args.platforms.split(",")]
    chosen = pick(lessons, args.count, args.start_date)
    y0, m0, d0 = map(int, args.start_date.split("-"))
    out = Path(args.out)

    manifest = []
    for i, lesson in enumerate(chosen):
        post_date = (date(y0, m0, d0) + timedelta(days=i)).isoformat()
        slug = f"{post_date}_lesson{lesson['id']}"
        for platform in platforms:
            fmt = "x_landscape" if platform == "x" else "ig_portrait"
            img_path = out / platform / f"{slug}.png"
            render(lesson, fmt, img_path)
            manifest.append({
                "date": post_date, "platform": platform, "format": fmt,
                "lesson_id": lesson["id"], "verse": lesson["verse"],
                "image": str(img_path.relative_to(out)),
                "caption": caption(lesson, platform),
            })
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    print(f"generated {len(manifest)} posts for {args.count} days across {platforms} -> {out}")
    print(f"manifest: {out / 'manifest.json'}")

if __name__ == "__main__":
    main()
