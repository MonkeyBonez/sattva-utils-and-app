#!/usr/bin/env python3
"""Generate a self-contained lesson-corpus review page from lessons_v3_review.json.
The page lets you keep/cut/edit each drafted lesson, see its source verses and
semantic near-duplicates, filter, search, and export your decisions as JSON."""
import json, html
from pathlib import Path

OUT = Path(__file__).resolve().parents[0] / "outputs"
data = json.load(open(OUT / "lessons_v3_review.json"))

# --- attach dedup recommendations (id -> suggestion) ---
rec_path = OUT / "dedup_recommendations.json"
suggestions = {}
if rec_path.exists():
    for c in json.load(open(rec_path))["recommendations"]:
        mi = c.get("merge_into", {}) or {}
        survivors = {}
        for cut_id, into_id in mi.items():
            suggestions[int(cut_id)] = {"action": "cut", "into": int(into_id), "why": c["why"]}
            survivors.setdefault(int(into_id), []).append(int(cut_id))
        for keep_id in c.get("keep", []):
            if keep_id in survivors:
                suggestions[int(keep_id)] = {"action": "keep", "absorbs": survivors[keep_id], "why": c["why"]}
            elif c["decision"] in ("keep",):
                suggestions[int(keep_id)] = {"action": "distinct", "why": c["why"]}
            elif c["decision"] == "review":
                suggestions.setdefault(int(keep_id), {"action": "review", "why": c["why"]})
for ch in data["chapters"]:
    for L in ch["lessons"]:
        if L["id"] in suggestions:
            L["suggestion"] = suggestions[L["id"]]

payload = json.dumps(data, ensure_ascii=False)

CHAPTER_NAMES = {
    1: "Arjuna's Despair", 2: "Sankhya Yoga", 3: "Karma Yoga", 4: "Knowledge & Action",
    5: "Renunciation & Action", 6: "Meditation", 7: "Knowledge & Realization",
    8: "The Imperishable", 9: "The Royal Secret", 10: "Divine Glories",
    11: "The Cosmic Vision", 12: "Devotion", 13: "Field & Knower", 14: "The Three Gunas",
    15: "The Supreme Person", 16: "Divine & Demonic", 17: "The Threefold Faith",
    18: "Freedom & Surrender",
}
names_js = json.dumps(CHAPTER_NAMES)

HTML = """<title>Sattvic — Lesson Corpus Review</title>
<style>
  :root{
    --bg:#efe9da; --panel:#f7f3e8; --panel-2:#efe8d6; --ink:#233028; --ink-soft:#5c6b5f;
    --line:#d9cfb8; --peacock:#1f4735; --peacock-soft:#2f6a4f; --lav:#7b5cc4; --lav-soft:#efe9fb;
    --gold:#b08a3e; --cut:#b0483e; --keep:#2f6a4f;
    --shadow:0 1px 2px rgba(35,48,40,.06),0 6px 20px rgba(35,48,40,.06);
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --ui:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  }
  @media (prefers-color-scheme:dark){:root{
    --bg:#141a16; --panel:#1c241e; --panel-2:#222b24; --ink:#e7e3d4; --ink-soft:#a3ab9f;
    --line:#2f3a31; --peacock:#7fcfa6; --peacock-soft:#9bdcbb; --lav:#b9a3ee; --lav-soft:#2a2340;
    --gold:#d8b56a; --cut:#e58a80; --keep:#7fcfa6;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
  }}
  :root[data-theme="light"]{
    --bg:#efe9da; --panel:#f7f3e8; --panel-2:#efe8d6; --ink:#233028; --ink-soft:#5c6b5f;
    --line:#d9cfb8; --peacock:#1f4735; --peacock-soft:#2f6a4f; --lav:#7b5cc4; --lav-soft:#efe9fb;
    --gold:#b08a3e; --cut:#b0483e; --keep:#2f6a4f; --shadow:0 1px 2px rgba(35,48,40,.06),0 6px 20px rgba(35,48,40,.06);
  }
  :root[data-theme="dark"]{
    --bg:#141a16; --panel:#1c241e; --panel-2:#222b24; --ink:#e7e3d4; --ink-soft:#a3ab9f;
    --line:#2f3a31; --peacock:#7fcfa6; --peacock-soft:#9bdcbb; --lav:#b9a3ee; --lav-soft:#2a2340;
    --gold:#d8b56a; --cut:#e58a80; --keep:#7fcfa6; --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35);
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.5;
    -webkit-font-smoothing:antialiased}
  .wrap{max-width:920px;margin:0 auto;padding:0 20px 120px}
  header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 90%,transparent);
    backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:14px 0;margin-bottom:26px}
  .top .wrap{padding-top:0;padding-bottom:0}
  .brand{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
  .brand h1{font-family:var(--serif);font-weight:600;font-size:22px;margin:0;letter-spacing:.2px}
  .brand .sub{color:var(--ink-soft);font-size:13px}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-top:12px}
  .stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 12px;box-shadow:var(--shadow)}
  .stat .n{font-family:var(--serif);font-size:22px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.1}
  .stat .l{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--ink-soft);margin-top:3px}
  .stat.keep .n{color:var(--keep)} .stat.cut .n{color:var(--cut)} .stat.flag .n{color:var(--gold)}
  .controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:14px}
  .controls input[type=search]{flex:1;min-width:180px;padding:9px 12px;border-radius:10px;border:1px solid var(--line);
    background:var(--panel);color:var(--ink);font-size:14px;font-family:var(--ui)}
  .seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--panel)}
  .seg button{border:0;background:transparent;color:var(--ink-soft);padding:8px 12px;font-size:13px;cursor:pointer;font-family:var(--ui)}
  .seg button[aria-pressed=true]{background:var(--peacock);color:var(--bg)}
  .btn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:10px;padding:8px 14px;
    font-size:13px;cursor:pointer;font-family:var(--ui)}
  .btn.primary{background:var(--lav);color:#fff;border-color:transparent;font-weight:600}
  :root[data-theme="dark"] .btn.primary,@media (prefers-color-scheme:dark){.btn.primary{color:#191426}}
  .note{color:var(--ink-soft);font-size:12.5px;margin-top:10px}
  section.chapter{margin:30px 0}
  .chead{display:flex;align-items:baseline;gap:10px;cursor:pointer;user-select:none;padding:6px 0;border-bottom:1px solid var(--line)}
  .chead .num{font-family:var(--serif);font-size:13px;color:var(--gold);font-weight:600;letter-spacing:.06em}
  .chead h2{font-family:var(--serif);font-size:19px;font-weight:600;margin:0;flex:1}
  .chead .cnt{font-size:12px;color:var(--ink-soft);font-variant-numeric:tabular-nums}
  .cards{display:flex;flex-direction:column;gap:12px;margin-top:14px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 15px;box-shadow:var(--shadow);
    transition:opacity .15s,border-color .15s}
  .card[data-decision=cut]{opacity:.5;border-color:var(--cut)}
  .card[data-decision=cut] .lesson{text-decoration:line-through;text-decoration-color:var(--cut)}
  .card.dupflag{border-left:3px solid var(--gold)}
  .cardhead{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}
  .chip{font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid var(--line);color:var(--ink-soft);
    font-variant-numeric:tabular-nums;white-space:nowrap}
  .chip.best{color:var(--peacock);border-color:color-mix(in srgb,var(--peacock) 40%,var(--line))}
  .chip.id{color:var(--ink-soft);background:var(--panel-2)}
  .chip.dup{color:var(--gold);border-color:color-mix(in srgb,var(--gold) 45%,var(--line));cursor:pointer}
  .spacer{flex:1}
  .lesson{font-family:var(--serif);font-size:18px;line-height:1.35;color:var(--ink);border:1px solid transparent;
    border-radius:8px;padding:3px 6px;margin:-3px -6px;outline:none}
  .lesson:focus{border-color:var(--lav);background:var(--panel-2)}
  .lesson.edited{border-color:color-mix(in srgb,var(--lav) 50%,transparent)}
  .rationale{color:var(--ink-soft);font-size:13px;margin-top:7px;font-style:italic}
  .wasline{color:var(--ink-soft);font-size:12px;margin-top:5px;opacity:.75}
  .wasline span{text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--cut) 50%,transparent)}
  .chip.sug{font-weight:600}
  .chip.sug.s-cut{color:var(--cut);border-color:color-mix(in srgb,var(--cut) 45%,var(--line))}
  .chip.sug.s-keep{color:var(--keep);border-color:color-mix(in srgb,var(--keep) 45%,var(--line))}
  .chip.sug.s-distinct{color:var(--peacock-soft)} .chip.sug.s-review{color:var(--gold)}
  .suggestion{margin-top:8px;font-size:12.5px;line-height:1.45;padding:7px 10px;border-radius:9px;background:var(--panel-2);border-left:2px solid var(--line)}
  .suggestion.s-cut{border-left-color:var(--cut)} .suggestion.s-keep{border-left-color:var(--keep)}
  .suggestion.s-review{border-left-color:var(--gold)} .suggestion.s-distinct{border-left-color:var(--peacock-soft)}
  .verses{margin-top:9px;border-top:1px dashed var(--line);padding-top:9px;display:none}
  .verses.open{display:block}
  .verse{display:flex;gap:9px;font-size:13.5px;margin:5px 0;color:var(--ink-soft)}
  .verse .ref{color:var(--peacock);font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600;min-width:44px}
  .verse.isbest .ref{color:var(--gold)}
  .cardfoot{display:flex;align-items:center;gap:8px;margin-top:11px}
  .toggle{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden}
  .toggle button{border:0;background:transparent;color:var(--ink-soft);padding:5px 12px;font-size:12.5px;cursor:pointer;font-family:var(--ui)}
  .toggle button.keep[aria-pressed=true]{background:var(--keep);color:var(--bg)}
  .toggle button.cut[aria-pressed=true]{background:var(--cut);color:#fff}
  .linkish{background:none;border:0;color:var(--lav);font-size:12.5px;cursor:pointer;font-family:var(--ui);padding:0}
  .cardnote{width:100%;margin-top:9px;padding:7px 10px;border-radius:9px;border:1px solid var(--line);
    background:var(--panel-2);color:var(--ink);font-size:13px;font-family:var(--ui);resize:vertical;display:none}
  .cardnote.open{display:block}
  .skipped{background:var(--panel-2);border:1px dashed var(--line);border-radius:12px;padding:10px 13px;margin-top:12px;font-size:12.5px;color:var(--ink-soft)}
  .skipped summary{cursor:pointer;color:var(--ink-soft)}
  .skipped .sv{margin:4px 0}
  .flash{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:var(--peacock);color:var(--bg);
    padding:10px 18px;border-radius:10px;font-size:13px;box-shadow:var(--shadow);opacity:0;transition:opacity .2s;pointer-events:none;z-index:50}
  .flash.show{opacity:1}
  .hidden{display:none!important}
  a.themebtn{margin-left:auto}
  @media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<header class="top"><div class="wrap">
  <div class="brand">
    <h1>Sattvic · Lesson Corpus Review</h1>
    <span class="sub" id="subline"></span>
    <button class="btn themebtn" id="themebtn" title="Toggle theme">◐ Theme</button>
  </div>
  <div class="stats" id="stats"></div>
  <div class="controls">
    <input type="search" id="search" placeholder="Search lessons, verse text, rationale…" autocomplete="off">
    <div class="seg" role="group" aria-label="Filter">
      <button data-filter="all" aria-pressed="true">All</button>
      <button data-filter="flagged">Near-dups</button>
      <button data-filter="cut">Cut</button>
      <button data-filter="undecided">Undecided</button>
    </div>
    <button class="btn" id="applysug" title="Set every suggested-cut lesson to Cut">Apply dedup suggestions</button>
    <button class="btn primary" id="export">Export decisions</button>
  </div>
  <div class="note" id="method"></div>
</div></header>

<div class="wrap" id="root"></div>
<div class="flash" id="flash"></div>

<script>
const DATA = __PAYLOAD__;
const NAMES = __NAMES__;
const LS_KEY = "sattvic_lesson_review_v1";
let decisions = JSON.parse(localStorage.getItem(LS_KEY) || "{}"); // id -> {d:'keep'|'cut', text, note}
let filter = "all", query = "";

const $ = (s,el=document)=>el.querySelector(s);
const esc = s => (s||"").replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function sugChip(L){
  if(!L.suggestion) return "";
  const a=L.suggestion.action, m={cut:"suggest cut",keep:"suggest keep",distinct:"keep — distinct",review:"review"};
  return `<span class="chip sug s-${a}">${m[a]||a}</span>`;
}
function sugText(L){
  const s=L.suggestion;
  if(s.action==="cut") return `Suggested merge → keep #${s.into}. ${s.why}`;
  if(s.action==="keep") return `Survivor — absorbs #${(s.absorbs||[]).join(", #")}. ${s.why}`;
  return s.why;
}

function counts(){
  let keep=0,cut=0,undec=0,edited=0;
  for(const ch of DATA.chapters) for(const L of ch.lessons){
    const d=decisions[L.id];
    if(!d||!d.d){undec++} else if(d.d==='cut'){cut++} else {keep++}
    if(d&&d.text&&d.text!==L.text)edited++;
  }
  return {keep,cut,undec,edited};
}

function renderStats(){
  const a=DATA.audit, c=counts();
  $("#subline").textContent = `${a.total_lessons} drafted lessons · ${a.lesson_coverage_pct}% verse coverage`;
  $("#method").textContent = `Near-duplicate flags: ${a.similarity_method}. ${a.lessons_flagged_near_dup} lessons flagged. Decisions autosave to this browser; Export downloads JSON.`;
  $("#stats").innerHTML = [
    ['n', a.total_lessons, 'Lessons'],
    ['keep', c.keep, 'Kept'],
    ['cut', c.cut, 'Cut'],
    ['flag', a.lessons_flagged_near_dup, 'Near-dup flags'],
    ['n', c.undec, 'Undecided'],
    ['n', a.total_skipped, 'Verses skipped'],
  ].map(([cls,n,l])=>`<div class="stat ${cls==='keep'?'keep':cls==='cut'?'cut':cls==='flag'?'flag':''}">
     <div class="n">${n}</div><div class="l">${l}</div></div>`).join("");
}

function cardMatches(L){
  if(query){
    const hay=(L.text+" "+L.rationale+" "+L.verses.map(v=>v.ref+" "+v.text).join(" ")).toLowerCase();
    if(!hay.includes(query)) return false;
  }
  const d=decisions[L.id];
  if(filter==="flagged") return L.near_dups && L.near_dups.length;
  if(filter==="cut") return d&&d.d==='cut';
  if(filter==="undecided") return !(d&&d.d);
  return true;
}

function render(){
  const root=$("#root"); root.innerHTML="";
  for(const ch of DATA.chapters){
    const visible=ch.lessons.filter(cardMatches);
    if(!visible.length && filter!=="all") continue;
    const sec=document.createElement("section"); sec.className="chapter";
    sec.innerHTML=`<div class="chead" data-ch="${ch.chapter}">
        <span class="num">CH ${ch.chapter}</span>
        <h2>${esc(NAMES[ch.chapter]||"")}</h2>
        <span class="cnt">${visible.length}/${ch.lessons.length}</span>
      </div><div class="cards"></div>`;
    const cards=$(".cards",sec);
    for(const L of visible) cards.appendChild(cardEl(L));
    if(ch.skipped && ch.skipped.length){
      const sk=document.createElement("details"); sk.className="skipped";
      sk.innerHTML=`<summary>${ch.skipped.length} verses intentionally given no lesson</summary>`+
        ch.skipped.map(s=>`<div class="sv"><b>${ch.chapter}:${s.v}</b> — ${esc(s.reason)}</div>`).join("");
      cards.appendChild(sk);
    }
    root.appendChild(sec);
  }
  if(!root.children.length) root.innerHTML=`<p class="note">No lessons match.</p>`;
}

function cardEl(L){
  const d=decisions[L.id]||{};
  const el=document.createElement("div"); el.className="card"; el.id="lesson-"+L.id;
  if(L.near_dups && L.near_dups.length) el.classList.add("dupflag");
  el.dataset.decision=d.d||"";
  const dupChips=(L.near_dups||[]).slice(0,4).map(nd=>
    `<span class="chip dup" data-goto="${nd.id}" title="${esc(DATA.id_text[nd.id]||'')}">≈ #${nd.id} · ${nd.score}</span>`).join("");
  el.innerHTML=`
    <div class="cardhead">
      <span class="chip id">#${L.id}</span>
      <span class="chip best">best ${esc(L.best_verse||"")}</span>
      ${dupChips}
      <span class="spacer"></span>
      ${sugChip(L)}
    </div>
    <div class="lesson" contenteditable="true" spellcheck="false">${esc(d.text||L.text)}</div>
    <div class="rationale">${esc(L.rationale)}</div>
    ${L.old_text?`<div class="wasline">was: <span>${esc(L.old_text)}</span></div>`:""}
    ${L.suggestion?`<div class="suggestion s-${L.suggestion.action}">${esc(sugText(L))}</div>`:""}
    <div class="verses">${L.verses.map(v=>`<div class="verse ${v.ref===L.best_verse?'isbest':''}"><span class="ref">${v.ref}</span><span>${esc(v.text)}</span></div>`).join("")}</div>
    <div class="cardfoot">
      <span class="toggle">
        <button class="keep" aria-pressed="${d.d==='keep'}">Keep</button>
        <button class="cut" aria-pressed="${d.d==='cut'}">Cut</button>
      </span>
      <button class="linkish vtoggle">${L.verses.length} source verse${L.verses.length>1?'s':''}</button>
      <span class="spacer"></span>
      <button class="linkish ntoggle">Note${d.note?" •":""}</button>
    </div>
    <textarea class="cardnote ${d.note?'open':''}" placeholder="Reviewer note (optional)…">${esc(d.note||"")}</textarea>`;

  const lessonEl=$(".lesson",el);
  if(d.text&&d.text!==L.text) lessonEl.classList.add("edited");
  lessonEl.addEventListener("input",()=>{
    const t=lessonEl.textContent.trim();
    setDec(L.id,{text:t}); lessonEl.classList.toggle("edited",t!==L.text);
  });
  $(".keep",el).addEventListener("click",()=>{setDec(L.id,{d:decisions[L.id]?.d==='keep'?'':'keep'});sync(el,L);});
  $(".cut",el).addEventListener("click",()=>{setDec(L.id,{d:decisions[L.id]?.d==='cut'?'':'cut'});sync(el,L);});
  $(".vtoggle",el).addEventListener("click",()=>$(".verses",el).classList.toggle("open"));
  $(".ntoggle",el).addEventListener("click",()=>$(".cardnote",el).classList.toggle("open"));
  $(".cardnote",el).addEventListener("input",e=>setDec(L.id,{note:e.target.value}));
  el.querySelectorAll(".chip.dup").forEach(c=>c.addEventListener("click",()=>{
    const t=document.getElementById("lesson-"+c.dataset.goto);
    if(t){t.scrollIntoView({behavior:"smooth",block:"center"});t.style.outline="2px solid var(--lav)";setTimeout(()=>t.style.outline="",1200);}
  }));
  return el;
}

function sync(el,L){
  const d=decisions[L.id]||{};
  el.dataset.decision=d.d||"";
  $(".keep",el).setAttribute("aria-pressed",d.d==='keep');
  $(".cut",el).setAttribute("aria-pressed",d.d==='cut');
  renderStats();
}
function setDec(id,patch){
  decisions[id]=Object.assign({},decisions[id],patch);
  if(!decisions[id].d) delete decisions[id].d;
  localStorage.setItem(LS_KEY,JSON.stringify(decisions));
  renderStats();
}
function flash(msg){const f=$("#flash");f.textContent=msg;f.classList.add("show");setTimeout(()=>f.classList.remove("show"),1600);}

$("#export").addEventListener("click",()=>{
  const out={generated:new Date().toISOString(),summary:counts(),decisions};
  const blob=new Blob([JSON.stringify(out,null,1)],{type:"application/json"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);
  a.download="lesson_review_decisions.json";a.click();
  flash("Exported "+Object.keys(decisions).length+" decisions");
});
$("#applysug").addEventListener("click",()=>{
  let n=0;
  for(const ch of DATA.chapters) for(const L of ch.lessons){
    if(L.suggestion && L.suggestion.action==="cut"){ setDec(L.id,{d:"cut"}); n++; }
    else if(L.suggestion && (L.suggestion.action==="keep"||L.suggestion.action==="distinct")){ if(!decisions[L.id]?.d) setDec(L.id,{d:"keep"}); }
  }
  render(); flash("Applied "+n+" suggested merges (cut). Review 'review' flags manually.");
});
$("#search").addEventListener("input",e=>{query=e.target.value.trim().toLowerCase();render();});
document.querySelectorAll(".seg button").forEach(b=>b.addEventListener("click",()=>{
  filter=b.dataset.filter;
  document.querySelectorAll(".seg button").forEach(x=>x.setAttribute("aria-pressed",x===b));
  render();
}));
document.addEventListener("click",e=>{const h=e.target.closest(".chead");if(h){const cs=h.nextElementSibling;cs.classList.toggle("hidden");}});
$("#themebtn").addEventListener("click",()=>{
  const cur=document.documentElement.getAttribute("data-theme");
  const next=cur==="dark"?"light":cur==="light"?"dark":(matchMedia("(prefers-color-scheme:dark)").matches?"light":"dark");
  document.documentElement.setAttribute("data-theme",next);
});

renderStats(); render();
</script>
"""

out_html = HTML.replace("__PAYLOAD__", payload).replace("__NAMES__", names_js)
dest = OUT / "lessons_v3_review.html"
dest.write_text(out_html, encoding="utf-8")
print("wrote", dest, f"({len(out_html)} bytes)")
