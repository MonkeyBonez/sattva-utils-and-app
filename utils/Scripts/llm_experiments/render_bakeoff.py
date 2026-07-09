#!/usr/bin/env python3
"""Render one or more bakeoff result files into a self-contained HTML comparison.

Each dataset (verse-first, lesson-first, ...) becomes its own stacked section with
a speed/size summary + per-case side-by-side model outputs, so quality and the
effect of the prompt framing can be judged at a glance before picking a model.

Usage:
    python render_bakeoff.py                                  # default single file
    python render_bakeoff.py bakeoff_results.json:"Verse-first (as-built #5)" \
                             bakeoff_lesson.json:"Lesson-first (#6 spotlight)"
"""
import html
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "outputs"
PAGE = OUT / "bakeoff.html"
ARTIFACT = OUT / "bakeoff.artifact.html"

LIGHT = "--bg:#faf8f3; --ink:#2a2a2e; --muted:#6b6b73; --line:#e6e1d6; --card:#fff; --accent:#6d4aa7; --verse:#8a5a2b;"
DARK = "--bg:#17161a; --ink:#e9e6df; --muted:#a09aa8; --line:#2e2c34; --card:#201e26; --accent:#b79ce6; --verse:#d9a86a;"

STYLE = f"""<style>
  :root {{ {LIGHT} }}
  @media (prefers-color-scheme: dark) {{ :root {{ {DARK} }} }}
  :root[data-theme="dark"] {{ {DARK} }}
  :root[data-theme="light"] {{ {LIGHT} }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  .wrap {{ max-width:1200px; margin:0 auto; padding:32px 20px 80px; }}
  h1 {{ font-size:26px; margin:0 0 4px; }}
  h2 {{ font-size:20px; margin:44px 0 6px; padding-top:18px; border-top:2px solid var(--line); }}
  h2 .tag {{ font-size:13px; font-weight:600; color:var(--accent); }}
  .sub {{ color:var(--muted); margin-bottom:20px; }}
  table {{ width:100%; border-collapse:collapse; }}
  .summary {{ margin:0 0 26px; border:1px solid var(--line); border-radius:12px; overflow:hidden; }}
  .summary th, .summary td {{ padding:10px 14px; text-align:left; border-bottom:1px solid var(--line); }}
  .summary th {{ background:color-mix(in srgb, var(--accent) 10%, transparent); font-size:13px;
    text-transform:uppercase; letter-spacing:.04em; }}
  .summary tr:last-child td {{ border-bottom:none; }}
  .case {{ background:var(--card); border:1px solid var(--line); border-radius:14px;
    padding:18px 18px 8px; margin-bottom:22px; }}
  .casehdr {{ display:flex; gap:10px; align-items:baseline; flex-wrap:wrap; }}
  .ref {{ font-variant-numeric:tabular-nums; font-weight:700; color:var(--accent); }}
  .verse {{ color:var(--verse); font-style:italic; }}
  .lesson {{ font-size:14px; color:var(--muted); margin:8px 0 4px; }}
  .sit {{ font-size:14px; margin:2px 0 12px; padding:6px 10px; border-radius:8px;
    background:color-mix(in srgb, var(--accent) 8%, transparent); display:inline-block; }}
  .sit.none {{ background:none; color:var(--muted); font-style:italic; padding-left:0; }}
  .case table {{ table-layout:fixed; }}
  .case th {{ font-size:13px; text-transform:uppercase; letter-spacing:.03em; color:var(--muted);
    text-align:left; padding:6px 10px; border-bottom:1px solid var(--line); }}
  .case td {{ vertical-align:top; padding:12px 10px; border-right:1px solid var(--line); }}
  .case td:last-child {{ border-right:none; }}
  .out {{ font-family:Georgia,"Times New Roman",serif; }}
  .cellmeta {{ margin-top:8px; font-size:11px; color:var(--muted); font-variant-numeric:tabular-nums; }}
  .missing {{ color:var(--muted); text-align:center; }}
  .tablescroll {{ overflow-x:auto; }}
</style>"""


def esc(s):
    return html.escape(s or "")


def render_section(d, label):
    cases, results = d["cases"], d["results"]
    models = [r["name"] for r in results]
    w = round(100 / max(len(models), 1))

    summ = []
    for r in results:
        toks = [row["tok_s"] for row in r["rows"] if row["tok_s"]]
        gens = [row["gen_s"] for row in r["rows"]]
        avg_len = sum(len(row["output"]) for row in r["rows"]) / max(len(r["rows"]), 1)
        summ.append({
            "name": r["name"], "size": r["size"], "load_s": r["load_s"],
            "tok_s": round(sum(toks) / len(toks), 1) if toks else 0,
            "gen_s": round(sum(gens) / len(gens), 2) if gens else 0,
            "avg_chars": round(avg_len),
        })
    summ_rows = "".join(
        f"<tr><td>{esc(s['name'])}</td><td>{s['size']}</td><td>{s['load_s']}s</td>"
        f"<td>{s['gen_s']}s</td><td>{s['tok_s']}</td><td>{s['avg_chars']}</td></tr>"
        for s in summ)

    rows_html = []
    for i, c in enumerate(cases):
        sit = (f'<div class="sit">“{esc(c["situation"])}”</div>' if c["situation"]
               else '<div class="sit none">no situation — generic relevance</div>')
        cells = []
        for r in results:
            row = r["rows"][i] if i < len(r["rows"]) else None
            if row:
                meta = f'{row["gen_s"]}s · {row["tok_s"]} tok/s · {len(row["output"])} chars'
                cells.append(f'<td style="width:{w}%"><div class="out">{esc(row["output"])}</div>'
                             f'<div class="cellmeta">{meta}</div></td>')
            else:
                cells.append('<td class="missing">—</td>')
        rows_html.append(f"""
        <div class="case">
          <div class="casehdr">
            <span class="ref">{c['chapter']}:{c['verse']}</span>
            <span class="verse">“{esc(c['verseText'])}”</span>
          </div>
          <div class="lesson">Mapped lesson: <b>{esc(c['lesson']) or '—'}</b></div>
          {sit}
          <table><thead><tr>{''.join(f'<th>{esc(m)}</th>' for m in models)}</tr></thead>
          <tbody><tr>{''.join(cells)}</tr></tbody></table>
        </div>""")

    return f"""
  <h2>{esc(label)} <span class="tag">temp={d.get('temp')} · max_tokens={d.get('max_tokens')}</span></h2>
  <div class="tablescroll"><table class="summary">
    <thead><tr><th>Model</th><th>Size (4-bit)</th><th>Load</th><th>Avg gen</th><th>Tok/s</th><th>Avg chars</th></tr></thead>
    <tbody>{summ_rows}</tbody></table></div>
  {''.join(rows_html)}"""


def main():
    args = sys.argv[1:] or ["bakeoff_results.json:Bake-off"]
    datasets = []
    for a in args:
        fn, _, label = a.partition(":")
        datasets.append((json.load(open(OUT / fn)), label or fn))

    sections = "".join(render_section(d, label) for d, label in datasets)
    intro = ('Same inputs the app supplies. <b>Verse-first</b> is the as-built #5 prompt '
             '(verse is the subject, lesson a footnote); <b>lesson-first</b> is the decided #6 '
             '“lesson spotlight” (lesson is the subject, verse only its source). Speeds are on '
             'Mac (M4 Pro) — the phone (A16) will be slower; that’s the sideload test.')
    body = f'<div class="wrap"><h1>On-device explainer — model bake-off</h1><div class="sub">{intro}</div>{sections}</div>'

    PAGE.write_text('<!doctype html><html><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width, initial-scale=1">'
                    f'<title>On-device explainer — model bake-off</title>{STYLE}</head>'
                    f'<body>{body}</body></html>')
    ARTIFACT.write_text(f'<title>On-device explainer — model bake-off</title>{STYLE}{body}')
    print(f"Wrote {PAGE}\nWrote {ARTIFACT}")


if __name__ == "__main__":
    main()
