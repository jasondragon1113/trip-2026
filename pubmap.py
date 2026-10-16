#!/usr/bin/env python3
# Files map for files whose content changed since last recorded publish (md5). Usage: pubmap.py [--dry] [--seed name1 name2 ...]
# 用 md5 比對，列出內容有變的檔；--seed 把指定檔名視為已發布
import json, pathlib, sys, hashlib
ROOT = pathlib.Path(__file__).parent; SITE = ROOT / "docs"; REC = ROOT / "dist" / "published.json"
md5 = lambda p: hashlib.md5(p.read_bytes()).hexdigest()
cur = {p.relative_to(SITE).as_posix(): md5(p) for p in SITE.rglob("*") if p.is_file() and p.suffix in (".html", ".jpg") and p.name != "index.html"}
rec = json.loads(REC.read_text()) if REC.exists() else {}
if "--seed" in sys.argv:
    for n in sys.argv[sys.argv.index("--seed")+1:]:
        if n in cur: rec[n] = cur[n]
    REC.write_text(json.dumps(rec)); print("seeded", len(rec), file=sys.stderr); sys.exit()
new = {k: k for k, v in cur.items() if rec.get(k) != v}
print(json.dumps(new)); print(len(new), "to publish", file=sys.stderr)
if "--dry" not in sys.argv:
    rec.update(cur); REC.write_text(json.dumps(rec))
