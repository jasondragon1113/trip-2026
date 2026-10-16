#!/usr/bin/env python3
# Build every roadbook page + hub into dist/site/, downloading Commons photos locally (resized with sips)
# 把所有 data/*.json 做成 dist/site/<id>.html，照片抓下來縮圖放 dist/site/img/
import json, pathlib, subprocess, hashlib, urllib.request, sys, re
ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "docs"; IMG = SITE / "img"; IMG.mkdir(parents=True, exist_ok=True)  # GitHub Pages serves /docs
ORDER = ["ginzan","tokyo","hakodate_aomori","busan","seoul","danang","chiangmai","bangkok_huahin","kyushu","jeju","cebu_bohol","penang"]
TPL = (ROOT / "roadbook-template.html").read_text(encoding="utf-8")
HEAD = "<!doctype html><html lang=\"zh-Hant\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\"><style>body{margin:0}</style></head><body>"
TAIL = "</body></html>"
UA = {"User-Agent": "trip-roadbook/1.0 (personal travel planner)"}

def fetch(url):
    """Download + resize to 900px wide jpg; return local relative path or None. 失敗回 None 不中斷"""
    h = hashlib.md5(url.encode()).hexdigest()[:12]
    out = IMG / f"p_{h}.jpg"
    if out.exists(): return f"img/{out.name}"
    try:
        req = urllib.request.Request(url, headers=UA)
        raw = IMG / f"raw_{h}"
        with urllib.request.urlopen(req, timeout=30) as r, open(raw, "wb") as f: f.write(r.read())
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "72", "-Z", "900", str(raw), "--out", str(out)], check=True, capture_output=True)
        raw.unlink(missing_ok=True)
        return f"img/{out.name}"
    except Exception as e:
        print(f"  !! photo fail {url[:80]}: {e}", file=sys.stderr); return None

def localize(d):
    items = [s for day in d.get("days", []) for s in day.get("stops", [])] + d.get("food", []) + d.get("challenges", [])
    n = 0
    for it in items:
        p = it.get("photo")
        if p and p.get("url") and "upload.wikimedia.org" in p["url"] or (p and p.get("url") and "commons.wikimedia.org" in p["url"]):
            loc = fetch(p["url"])
            if loc: p["local"] = loc; n += 1
            else: it["photo"] = None
        elif p and p.get("url"):
            it["photo"] = None  # 非 Commons 不放，避免版權與 CSP
    return n

# Taichung (RMQ) summary, hand-checked from each data file's flights / 台中出發摘要（逐筆看過 flights 後手填）
RMQ = {
 "busan": {"kind": "direct", "price": 8668}, "seoul": {"kind": "direct", "price": 12688},
 "tokyo": {"kind": "direct", "price": 38740}, "bangkok_huahin": {"kind": "maybe", "price": 10000},
 "jeju": {"kind": "transfer", "price": 11000}, "danang": {"kind": "transfer", "price": 9742},
 "penang": {"kind": "transfer", "price": 12824}, "chiangmai": {"kind": "transfer", "price": 13930},
 "kyushu": {"kind": "transfer", "price": 17046}, "cebu_bohol": {"kind": "transfer", "price": 17950},
 "ginzan": {"kind": "transfer", "price": 24107}, "hakodate_aomori": {"kind": "none", "price": None},
}
built = []
for f in sorted(ROOT.glob("data/*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    cover = ROOT / "data" / "img" / f"{d['id']}.jpg"
    if cover.exists():
        tgt = IMG / f"cover_{d['id']}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", "-Z", "1400", str(cover), "--out", str(tgt)], check=True, capture_output=True)
        d["cover"] = f"img/{tgt.name}"
    n = localize(d)
    html = TPL.replace("__TITLE__", d["name"] + "小旅行").replace("__DATA__", json.dumps(d, ensure_ascii=False).replace("</", "<\\/"))
    (SITE / f"{d['id']}.html").write_text(HEAD + html + TAIL, encoding="utf-8")
    built.append(d); print(f"ok {d['id']}: {len(d.get('days',[]))} days, {n} photos, cover={'cover' in d}")
# Placeholders for destinations still being researched (cover if ready)
# 還沒查完的目的地先放佔位卡
NAMES = {"ginzan":("東北雪國","日本","onsen","銀山溫泉・天童・山寺"),"tokyo":("東京","日本","tower","跨年與初詣"),"hakodate_aomori":("函館＋青森","日本","snow","夜景、朝市、樹冰"),"busan":("釜山","韓國","wave",""),"seoul":("首爾","韓國","tower","跨年敲鐘"),"danang":("峴港＋會安","越南","lantern","燈籠與海灘"),"chiangmai":("清邁","泰國","leaf","古城與大象"),"bangkok_huahin":("曼谷＋華欣","泰國","market","美食與海邊"),"kyushu":("九州北部","日本","onsen","屋台與溫泉"),"jeju":("濟州島","韓國","car","自駕與黑豬肉"),"cebu_bohol":("宿霧＋薄荷島","菲律賓","whale","溪降與鯨鯊"),"penang":("檳城","馬來西亞","coffee","美食之都")}
have = {d["id"] for d in built}
for pid, (nm, ct, mo, tg) in NAMES.items():
    if pid in have: continue
    cover = ROOT / "data" / "img" / f"{pid}.jpg"; cv = None
    if cover.exists():
        tgt = IMG / f"cover_{pid}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", "-Z", "1400", str(cover), "--out", str(tgt)], check=True, capture_output=True); cv = f"img/{tgt.name}"
    built.append({"id": pid, "name": nm, "country": ct, "motif": mo, "tagline": tg, "placeholder": True, "cover": cv, "palette": {"primary": "#B8A58F", "secondary": "#E8DCC8"}})
built.sort(key=lambda d: ORDER.index(d["id"]) if d["id"] in ORDER else 99)
json.dump([{k: d.get(k) for k in ("id","name","subtitle","country","flag","motif","palette","tagline","summary","dates","budget","cover","getting_around")} | {"min_flight": min([f.get("price_pp_twd") or 10**9 for f in d.get("flights", []) if f.get("verified")] or [f.get("price_pp_twd") or 10**9 for f in d.get("flights", [])] or [10**9]), "rmq": RMQ.get(d["id"]), "n_days": len(d.get("days", [])), "challenges": [c["name"] for c in d.get("challenges", [])][:3], "foods": [x["name"] for x in d.get("food", [])][:3]} for d in built], open(SITE / "plans.json", "w", encoding="utf-8"), ensure_ascii=False)
plans = json.load(open(SITE / "plans.json", encoding="utf-8"))
for p in plans:
    src = next((d for d in built if d["id"] == p["id"]), {})
    if src.get("placeholder"): p["placeholder"] = True
hub = (ROOT / "hub-template.html").read_text(encoding="utf-8")
(SITE / "index.html").write_text(hub.replace("__DATA__", json.dumps({"checked": "2026-10-16", "plans": plans}, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
# first-round comparison page, with a back link
# 第一輪比價表，加回首頁連結
cmp = (ROOT / "dist" / "compare-public.html").read_text(encoding="utf-8")  # 公開版比價表
(SITE / "compare.html").write_text(HEAD + cmp + TAIL, encoding="utf-8")
print("built", len(built), "pages; placeholders:", sum(1 for d in built if d.get("placeholder")))
