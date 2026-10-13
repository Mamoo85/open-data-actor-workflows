#!/usr/bin/env python3
"""Generate n8n / Make / Zapier assets for every actor in data/catalog.json."""
import json, os, re, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = "transparent_meteorite"
cat = json.load(open(os.path.join(ROOT, "data/catalog.json"), encoding="utf-8"))
inputs = json.load(open(os.path.join(ROOT, "data/sample_inputs.json"), encoding="utf-8"))


def short(desc, n=200):
    d = re.sub(r"\s+", " ", desc).strip()
    d = re.sub(r"\s*\d+ automated checks\.?$", "", d)
    return d if len(d) <= n else d[:n].rsplit(" ", 1)[0] + "..."


def url(slug):
    return f"https://api.apify.com/v2/acts/{USER}~{slug}/run-sync-get-dataset-items"


def store(slug):
    return f"https://apify.com/{USER}/{slug}"


CODE = """// Drop empty rows, flatten nested values so Google Sheets accepts them, cap the batch.
const MAX_ROWS = 500;
const out = [];
for (const item of $input.all()) {
  const row = {};
  let filled = 0;
  for (const [k, v] of Object.entries(item.json)) {
    if (v === null || v === undefined || v === '') { row[k] = ''; continue; }
    filled++;
    row[k] = (typeof v === 'object') ? JSON.stringify(v) : v;
  }
  if (filled > 0) out.push({ json: row });
  if (out.length >= MAX_ROWS) break;
}
return out;"""


def node(name, typ, ver, pos, params, **kw):
    nid = hashlib.md5(name.encode()).hexdigest()[:12]
    d = dict(parameters=params, id=nid, name=name, type=typ, typeVersion=ver, position=pos)
    d.update(kw)
    return d


def n8n(a):
    slug, title = a["slug"], a["title"]
    body = json.dumps(inputs[slug], indent=2)
    note = (f"## {title}\n{short(a['description'])}\n\n"
            "**Setup (about 3 minutes)**\n"
            "1. Credentials > New > *Header Auth*. Name it `Apify API token`. Header name `Authorization`, value `Bearer YOUR_APIFY_TOKEN` (token: Apify Console > Settings > Integrations).\n"
            "2. Open *Append to Google Sheet*, connect Google Sheets OAuth2, set your spreadsheet (replace `YOUR_SHEET_ID`) and tab.\n"
            f"3. Edit the JSON body in *Run Apify actor* to your own filters (see {store(slug)}).\n"
            "4. Click *Execute workflow* to test, then activate. The schedule trigger runs daily at 07:00.\n\n"
            "Maintained by the author of this actor. Pay-per-result pricing; the free Apify plan credit covers a trial. Sample input uses a small result limit.")
    nodes = [
        node("Setup notes", "n8n-nodes-base.stickyNote", 1, [-80, -140], {"content": note, "height": 380, "width": 520}),
        node("Schedule Trigger", "n8n-nodes-base.scheduleTrigger", 1.2, [480, 160], {"rule": {"interval": [{"triggerAtHour": 7}]}}),
        node("Manual Trigger", "n8n-nodes-base.manualTrigger", 1, [480, 340], {}),
        node("Run Apify actor", "n8n-nodes-base.httpRequest", 4.2, [720, 250], {
            "method": "POST", "url": url(slug), "authentication": "genericCredentialType",
            "genericAuthType": "httpHeaderAuth", "sendBody": True, "specifyBody": "json",
            "jsonBody": body, "options": {"timeout": 300000}},
            credentials={"httpHeaderAuth": {"id": "REPLACE_ME", "name": "Apify API token"}},
            retryOnFail=True, maxTries=3, waitBetweenTries=5000, onError="continueErrorOutput"),
        node("Clean rows", "n8n-nodes-base.code", 2, [960, 230], {"jsCode": CODE}),
        node("Append to Google Sheet", "n8n-nodes-base.googleSheets", 4.5, [1200, 230], {
            "operation": "append",
            "documentId": {"__rl": True, "value": "YOUR_SHEET_ID", "mode": "id"},
            "sheetName": {"__rl": True, "value": "Sheet1", "mode": "name"},
            "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": []},
            "options": {}},
            credentials={"googleSheetsOAuth2Api": {"id": "REPLACE_ME", "name": "Google Sheets account"}}),
        node("Run failed", "n8n-nodes-base.stopAndError", 1, [960, 440],
             {"errorMessage": f"Apify run failed for {slug}. Check the token credential, plan credit and input JSON."}),
    ]

    def c(n):
        return [[{"node": n, "type": "main", "index": 0}]]
    conn = {
        "Schedule Trigger": {"main": c("Run Apify actor")},
        "Manual Trigger": {"main": c("Run Apify actor")},
        "Run Apify actor": {"main": [[{"node": "Clean rows", "type": "main", "index": 0}],
                                     [{"node": "Run failed", "type": "main", "index": 0}]]},
        "Clean rows": {"main": c("Append to Google Sheet")},
    }
    return {"name": f"{title} to Google Sheets", "nodes": nodes, "connections": conn,
            "active": False, "settings": {"executionOrder": "v1"}, "pinData": {},
            "meta": {"templateCredsSetupCompleted": False}, "tags": []}


def make(a):
    slug = a["slug"]
    return {"name": f"{a['title']} to Google Sheets", "flow": [
        {"id": 1, "module": "http:ActionSendData", "version": 3, "parameters": {"handleErrors": True},
         "mapper": {"url": url(slug), "method": "post",
                    "headers": [{"name": "Authorization", "value": "Bearer YOUR_APIFY_TOKEN"}],
                    "bodyType": "raw", "contentType": "application/json", "data": json.dumps(inputs[slug]),
                    "parseResponse": True, "timeout": 300, "shareCookies": False},
         "metadata": {"designer": {"x": 0, "y": 0}}},
        {"id": 2, "module": "builtin:BasicIterator", "version": 1, "mapper": {"array": "{{1.data}}"},
         "metadata": {"designer": {"x": 300, "y": 0}}},
        {"id": 3, "module": "google-sheets:addRow", "version": 2, "parameters": {"__IMTCONN__": 0},
         "mapper": {"mode": "select", "valueInputOption": "USER_ENTERED", "insertUnformatted": False,
                    "spreadsheetId": "YOUR_SHEET_ID", "sheetId": "Sheet1", "includesHeaders": True,
                    "values": {}},
         "metadata": {"designer": {"x": 600, "y": 0}}}],
        "metadata": {"version": 1,
                     "scenario": {"roundtrips": 1, "maxErrors": 3, "autoCommit": True, "sequential": False,
                                  "confidential": False, "dataloss": False, "dlq": False},
                     "designer": {"orphans": []}, "zone": "us1.make.com"}}


def zap(a):
    slug = a["slug"]
    return f"""# Zapier: {a['title']}

{short(a['description'])}

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `{url(slug)}`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{json.dumps(inputs[slug], indent=2)}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/{USER}~{slug}/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: {store(slug)}
"""


def main():
    for d in ("n8n", "make", "zapier"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    for a in cat:
        s = a["slug"]
        json.dump(n8n(a), open(f"{ROOT}/n8n/{s}.json", "w", encoding="utf-8"), indent=2)
        json.dump(make(a), open(f"{ROOT}/make/{s}.blueprint.json", "w", encoding="utf-8"), indent=2)
        open(f"{ROOT}/zapier/{s}.md", "w", encoding="utf-8").write(zap(a))
    rows = "\n".join(
        f"| [{a['title'].split(':')[0]}]({store(a['slug'])}) | {short(a['description'], 110)} | "
        f"[n8n](n8n/{a['slug']}.json) | [Make](make/{a['slug']}.blueprint.json) | [Zapier](zapier/{a['slug']}.md) |"
        for a in cat)
    open(f"{ROOT}/data/table.md", "w", encoding="utf-8").write(rows + "\n")
    print("generated", len(cat))


if __name__ == "__main__":
    main()
