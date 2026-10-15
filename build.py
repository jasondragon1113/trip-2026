#!/usr/bin/env python3
# Build the single-file site: pull the json block from each research report, merge extras, inline into template.
# 把四份研究報告最後的 json 抓出來，加上 extra.json 的補充，塞進 template 產出 dist/index.html
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).parent
ORDER = ["ginzan", "aomori", "hakodate", "aomori_hakodate", "tokyo", "seoul", "busan", "chiangmai", "danang"]

places = {}
for f in sorted(ROOT.glob("研究-*.md")):
    blocks = re.findall(r"```json\s*(.*?)```", f.read_text(encoding="utf-8"), re.S)
    if not blocks:
        print(f"!! {f.name}: no json block", file=sys.stderr)
        continue
    try:
        arr = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        print(f"!! {f.name}: {e}", file=sys.stderr)
        continue
    for p in (arr if isinstance(arr, list) else [arr]):
        places[p["id"]] = p
        print(f"ok {f.name} -> {p['id']}")

extra_path = ROOT / "extra.json"
extra = json.loads(extra_path.read_text(encoding="utf-8")) if extra_path.exists() else {}
for pid, patch in extra.get("places", {}).items():
    if pid in places:
        places[pid].update(patch)

# Private-only additions live in a gitignored file
# 只給私人連結版的內容放在不進 git 的檔案
priv_path = ROOT / "extra.private.json"
priv = json.loads(priv_path.read_text(encoding="utf-8")) if priv_path.exists() else {}

ordered = [places[k] for k in ORDER if k in places] + [v for k, v in places.items() if k not in ORDER]
html = (ROOT / "template.html").read_text(encoding="utf-8")
(ROOT / "dist").mkdir(exist_ok=True)

def write(name, plist):
    out = ROOT / name
    out.parent.mkdir(exist_ok=True)
    payload = json.dumps({"checked": extra.get("checked", ""), "plans": extra.get("plans", []), "plans_note": extra.get("plans_note", ""), "places": plist}, ensure_ascii=False).replace("</", "<\\/")
    out.write_text(html.replace("__DATA__", payload), encoding="utf-8")

# Public build: drop private-only fields, sections, and lines containing strip words
# 公開版：拿掉私人欄位、標 private 的區塊、含關鍵字的句子
words = priv.get("strip_words", [])
hit = lambda t: any(w.lower() in str(t).lower() for w in words)
pf = priv.get("private_fields", [])
public = []
for p in ordered:
    q = {k: v for k, v in p.items() if k not in pf}
    bad = {u for f in pf for u in ((p.get(f) or {}).get("sources", []) if isinstance(p.get(f), dict) else [])}
    q["sources"] = [u for u in q.get("sources", []) if u not in bad and not hit(u)]
    q["special"] = [s for s in q.get("special", []) if not s.get("private")]
    for k in ("risks", "highlights", "events", "itinerary_1231", "itinerary_0101"):
        q[k] = [r for r in q.get(k, []) if not hit(r)]
    public.append(q)
write("docs/index.html", public)  # GitHub Pages serves /docs

private = [dict(p) for p in ordered]
for p in private:
    p["special"] = list(p.get("special", [])) + priv.get("places", {}).get(p["id"], {}).get("special", [])
write("dist/private.html", private)
pub = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
leaks = [w for w in words if w.lower() in pub.lower()]
print(f"built {len(ordered)} places; public leaks: {leaks or 'none'}")
if leaks:
    sys.exit(1)
