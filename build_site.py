#!/usr/bin/env python3
# Build every roadbook page + hub into dist/site/, downloading Commons photos locally (resized with sips)
# 把所有 data/*.json 做成 dist/site/<id>.html，照片抓下來縮圖放 dist/site/img/
import json, pathlib, subprocess, hashlib, urllib.request, sys, re
ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "docs"; IMG = SITE / "img"; IMG.mkdir(parents=True, exist_ok=True)  # GitHub Pages serves /docs
ORDER = ["ginzan","tokyo","hakodate_aomori","busan","seoul","danang","chiangmai","bangkok_huahin","kyushu","jeju","cebu_bohol","penang","sydney","newyork"]
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
RMQ = {}  # filled per destination from data after is_direct is defined / 從資料算台中直飛
def is_direct(f):
    """Direct flight only / 只算直飛：kind=transfer 或文字寫轉機、經某地的都排除"""
    txt = (f.get("airline","") + f.get("out","") + f.get("basis","") + f.get("note","") + f.get("back",""))
    return f.get("kind") != "transfer" and not re.search(r"轉機|經.{1,6}(轉|HKG|KUL|SIN|HAN|ICN)|香港快運|國泰|無直飛", txt)
def rmq_summary(d):
    fs = [f for f in d.get("flights", []) if f.get("from") == "RMQ" and f.get("price_pp_twd") and is_direct(f)]
    if not fs: return {"kind": "none", "price": None}
    ver = [f for f in fs if f.get("verified")]
    pick = min(ver or fs, key=lambda f: f["price_pp_twd"])
    return {"kind": "direct" if ver else "maybe", "price": pick["price_pp_twd"]}
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
    RMQ[d["id"]] = rmq_summary(d)
    built.append(d); print(f"ok {d['id']}: {len(d.get('days',[]))} days, {n} photos, cover={'cover' in d}")
# Placeholders for destinations still being researched (cover if ready)
# 還沒查完的目的地先放佔位卡
NAMES = {"ginzan":("東北雪國","日本","onsen","銀山溫泉・天童・山寺"),"tokyo":("東京","日本","tower","跨年與初詣"),"hakodate_aomori":("函館＋青森","日本","snow","夜景、朝市、樹冰"),"busan":("釜山","韓國","wave",""),"seoul":("首爾","韓國","tower","跨年敲鐘"),"danang":("峴港＋會安","越南","lantern","燈籠與海灘"),"chiangmai":("清邁","泰國","leaf","古城與大象"),"bangkok_huahin":("曼谷＋華欣","泰國","market","美食與海邊"),"kyushu":("九州北部","日本","onsen","屋台與溫泉"),"jeju":("濟州島","韓國","car","自駕與黑豬肉"),"cebu_bohol":("宿霧＋薄荷島","菲律賓","whale","溪降與鯨鯊"),"penang":("檳城","馬來西亞","coffee","美食之都"),"sydney":("雪梨","澳洲","wave","夏天看港灣煙火"),"newyork":("紐約","美國","tower","時代廣場跨年")}
have = {d["id"] for d in built}
for pid, (nm, ct, mo, tg) in NAMES.items():
    if pid in have: continue
    cover = ROOT / "data" / "img" / f"{pid}.jpg"; cv = None
    if cover.exists():
        tgt = IMG / f"cover_{pid}.jpg"
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", "-Z", "1400", str(cover), "--out", str(tgt)], check=True, capture_output=True); cv = f"img/{tgt.name}"
    built.append({"id": pid, "name": nm, "country": ct, "motif": mo, "tagline": tg, "placeholder": True, "cover": cv, "palette": {"primary": "#B8A58F", "secondary": "#E8DCC8"}})
built.sort(key=lambda d: ORDER.index(d["id"]) if d["id"] in ORDER else 99)
json.dump([{k: d.get(k) for k in ("id","name","subtitle","country","flag","motif","palette","tagline","summary","dates","budget","cover","getting_around")} | {"min_flight": min([f.get("price_pp_twd") for f in d.get("flights", []) if f.get("price_pp_twd") and is_direct(f)] or [10**9]), "rmq": RMQ.get(d["id"]), "n_days": len(d.get("days", [])), "challenges": [c["name"] for c in d.get("challenges", [])][:3], "foods": [x["name"] for x in d.get("food", [])][:3]} for d in built], open(SITE / "plans.json", "w", encoding="utf-8"), ensure_ascii=False)
plans = json.load(open(SITE / "plans.json", encoding="utf-8"))
for p in plans:
    src = next((d for d in built if d["id"] == p["id"]), {})
    if src.get("placeholder"): p["placeholder"] = True
hub = (ROOT / "hub-template.html").read_text(encoding="utf-8")
(SITE / "index.html").write_text(hub.replace("__DATA__", json.dumps({"checked": "2026-10-16", "plans": plans}, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
# first-round comparison page, with a back link
# 第一輪比價表，加回首頁連結
# Comparison page built from the same 12 data files / 比價表直接從 12 本手帳資料產生
import re as _re
def md(s):
    m = _re.search(r"(\d{1,2})/(\d{1,2})", s or ""); 
    if not m: return None
    mo, dy = int(m.group(1)), int(m.group(2)); return (2027 if mo == 1 else 2026, mo, dy)
rows = []
for i, d in enumerate([x for x in built if not x.get("placeholder")]):
    fl = d.get("flights", [])
    tpe = [f for f in fl if f.get("from") == "TPE" and f.get("price_pp_twd") and is_direct(f)]
    tpe_v = [f for f in tpe if f.get("verified")] or tpe
    # flight used by the budget (direct, any origin) / 預算用的那班：直飛、價格＝flights_for2÷2
    directs = [f for f in fl if f.get("price_pp_twd") and is_direct(f)]
    half = (d.get("budget", {}).get("flights_for2") or 0) / 2
    best = min(directs, key=lambda f: (abs(f["price_pp_twd"] - half), not f.get("verified"))) if directs else None
    r = RMQ.get(d["id"]); o, b = md(d["dates"]["out"]), md(d["dates"]["back"])
    stays = d.get("stays") or [{}]
    st = next((x for x in stays if "有" in (x.get("availability") or "") and "滿" not in (x.get("availability") or "")), stays[0]); av = st.get("availability") or "未知"
    av = "有空房" if "有" in av and "滿" not in av else ("滿房" if "滿" in av else "未知")
    chk = sorted({f.get("checked","") for f in fl if f.get("verified")})
    flight_min = min([x for x in [best and best["price_pp_twd"], r and r.get("kind") == "direct" and r.get("price")] if x] or [None])
    rows.append({"id": d["id"], "order": i, "name": d["name"], "country": d["country"], "tagline": d.get("tagline",""), "motif": d.get("motif","star"),
      "color": (d.get("palette") or {}).get("primary","#E8743B"), "out": d["dates"]["out"].split("（")[0], "back": d["dates"]["back"].split("（")[0], "nights": d["dates"].get("nights"),
      "total": d["budget"]["total_for2"], "nye": bool(o and b and o <= (2026,12,31) and b >= (2027,1,1)), "car": bool(_re.search("自駕|混合", d.get("getting_around",{}).get("mode",""))),
      "mode": d.get("getting_around",{}).get("mode",""), "high": d.get("weather",{}).get("high_c"), "low": d.get("weather",{}).get("low_c"),
      "tpe_min": best and best["price_pp_twd"], "best_from": best and best.get("from"), "flight_min": flight_min, "rmq": r, "verified": bool(chk), "flight_checked": (chk[-1] if chk else "")[5:].replace("-","/"),
      "flight_line": (f"{best.get('airline','')} {best.get('out','')}／{best.get('back','')}，每人 NT${best['price_pp_twd']:,}" if best else "待確認"),
      "stay_name": st.get("name",""), "stay_avail": av, "stay_price": st.get("price_night_for2_twd"),
      "stay_line": f"{st.get('name','')}（{av}{'，每晚 NT$' + format(st['price_night_for2_twd'], ',') if st.get('price_night_for2_twd') else ''}）"})
picks = json.loads((ROOT / "compare-picks.json").read_text(encoding="utf-8"))
cheap = min(rows, key=lambda x: x["total"][0])
for pk in picks:
    if pk["id"] == "auto_cheapest":
        pk["id"] = cheap["id"]; pk["why"] = pk["why"] or f"12 個裡兩人總花費最低。{cheap['tagline']}"
picks = [pk for i, pk in enumerate(picks) if pk["id"] not in [q["id"] for q in picks[:i]]]
latest = max([d.get("checked","") for d in built if not d.get("placeholder")] or [""])
hub_art = hub[hub.index('<svg class="art"'):hub.index('</svg>', hub.index('<svg class="art"'))+6]
ctpl = (ROOT / "compare-template.html").read_text(encoding="utf-8").replace("__ART__", hub_art)
(SITE / "compare.html").write_text(HEAD + ctpl.replace("__DATA__", json.dumps({"checked": latest, "picks": picks, "places": rows}, ensure_ascii=False).replace("</", "<\\/")) + TAIL, encoding="utf-8")
print("built", len(built), "pages; placeholders:", sum(1 for d in built if d.get("placeholder")))
