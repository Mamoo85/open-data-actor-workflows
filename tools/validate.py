#!/usr/bin/env python3
"""Offline validation: JSON parses, n8n connections reference real nodes, types are n8n-nodes-base.*.
Optional: --types FILE (JSON list of valid node type names from n8n-nodes-base package.json)."""
import glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errs = []
valid = None
if "--types" in sys.argv:
    valid = set(json.load(open(sys.argv[sys.argv.index("--types") + 1])))
cat = json.load(open(f"{ROOT}/data/catalog.json", encoding="utf-8"))
slugs = [a["slug"] for a in cat]

def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        errs.append(f"{p}: parse error {e}")

n_ok = 0
for s in slugs:
    d = load(f"{ROOT}/n8n/{s}.json")
    if d:
        names = [n["name"] for n in d["nodes"]]
        if len(set(names)) != len(names):
            errs.append(f"{s}: duplicate node names")
        for n in d["nodes"]:
            t = n["type"]
            if not t.startswith("n8n-nodes-base."):
                errs.append(f"{s}: bad type {t}")
            elif valid is not None and t not in valid:
                errs.append(f"{s}: unknown n8n type {t}")
            if not isinstance(n.get("typeVersion"), (int, float)):
                errs.append(f"{s}: {n['name']} no typeVersion")
        for src, outs in d["connections"].items():
            if src not in names:
                errs.append(f"{s}: connection source missing {src}")
            for branch in outs.get("main", []):
                for link in branch:
                    if link["node"] not in names:
                        errs.append(f"{s}: connection target missing {link['node']}")
        http = [n for n in d["nodes"] if n["type"].endswith("httpRequest")][0]
        if f"transparent_meteorite~{s}/run-sync-get-dataset-items" not in http["parameters"]["url"]:
            errs.append(f"{s}: wrong URL")
        try:
            json.loads(http["parameters"]["jsonBody"])
        except Exception as e:
            errs.append(f"{s}: jsonBody invalid {e}")
        if not any(n["type"].endswith("googleSheets") for n in d["nodes"]):
            errs.append(f"{s}: no sheets node")
        n_ok += 1
    m = load(f"{ROOT}/make/{s}.blueprint.json")
    if m and [x["module"] for x in m["flow"]] != ["http:ActionSendData", "builtin:BasicIterator", "google-sheets:addRow"]:
        errs.append(f"{s}: make flow shape")
    if not os.path.exists(f"{ROOT}/zapier/{s}.md"):
        errs.append(f"{s}: zapier md missing")
for p in glob.glob(f"{ROOT}/data/*.json"):
    load(p)
print(f"n8n workflows checked: {n_ok}/{len(slugs)}; make: {len(glob.glob(ROOT + '/make/*.json'))}; zapier: {len(glob.glob(ROOT + '/zapier/*.md'))}")
if errs:
    print("\n".join(errs))
    sys.exit(1)
print("OK")
