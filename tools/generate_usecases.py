#!/usr/bin/env python3
"""Generate the 5 use-case n8n workflows (Maps leads, TikTok stats, YouTube comment sentiment,
LinkedIn jobs digest, Amazon price tracker). Output: n8n/<name>.json. Same node style as generate.py."""
import json, os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = "transparent_meteorite"


def url(slug):
    return f"https://api.apify.com/v2/acts/{USER}~{slug}/run-sync-get-dataset-items"


def node(name, typ, ver, pos, params, **kw):
    d = dict(parameters=params, id=hashlib.md5(name.encode()).hexdigest()[:12], name=name, type=typ,
             typeVersion=ver, position=pos)
    d.update(kw)
    return d


def c(*names):
    return [[{"node": n, "type": "main", "index": 0} for n in names]]


def apify(slug, body):
    return node("Run Apify actor", "n8n-nodes-base.httpRequest", 4.2, [720, 250], {
        "method": "POST", "url": url(slug), "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth", "sendBody": True, "specifyBody": "json",
        "jsonBody": json.dumps(body, indent=2), "options": {"timeout": 300000}},
        credentials={"httpHeaderAuth": {"id": "REPLACE_ME", "name": "Apify API token"}},
        retryOnFail=True, maxTries=3, waitBetweenTries=5000, onError="continueErrorOutput")


def sheet(name, pos, match=None, tab="Sheet1"):
    p = {"operation": "appendOrUpdate" if match else "append",
         "documentId": {"__rl": True, "value": "YOUR_SHEET_ID", "mode": "id"},
         "sheetName": {"__rl": True, "value": tab, "mode": "name"},
         "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": match or [], "schema": []},
         "options": {}}
    return node(name, "n8n-nodes-base.googleSheets", 4.5, pos, p,
                credentials={"googleSheetsOAuth2Api": {"id": "REPLACE_ME", "name": "Google Sheets account"}})


def slack(name, pos):
    return node(name, "n8n-nodes-base.slack", 2.3, pos, {
        "resource": "message", "operation": "post", "select": "channel",
        "channelId": {"__rl": True, "value": "YOUR_CHANNEL_ID", "mode": "id"},
        "text": "={{ $json.text }}", "otherOptions": {}},
        credentials={"slackApi": {"id": "REPLACE_ME", "name": "Slack account"}})


def code(name, pos, js):
    return node(name, "n8n-nodes-base.code", 2, pos, {"jsCode": js})


def note(title, what, extra_steps, actor_slug):
    steps = ("**Setup (about 3 minutes)**\n"
             "1. Credentials > New > *Header Auth*. Name it `Apify API token`. Header name `Authorization`, value `Bearer YOUR_APIFY_TOKEN` (token: Apify Console > Settings > Integrations).\n")
    for i, s in enumerate(extra_steps, 2):
        steps += f"{i}. {s}\n"
    steps += (f"{len(extra_steps) + 2}. Click *Execute workflow* to test with the small sample input, then activate.\n\n"
              f"Runs the Apify actor https://apify.com/{USER}/{actor_slug} (pay-per-result; the free Apify plan credit covers a trial). "
              "Maintained by the author of the actor.")
    return node("Setup notes", "n8n-nodes-base.stickyNote", 1, [-80, -140],
                {"content": f"## {title}\n{what}\n\n{steps}", "height": 400, "width": 540})


def triggers(interval):
    return [node("Schedule Trigger", "n8n-nodes-base.scheduleTrigger", 1.2, [480, 160], {"rule": {"interval": [interval]}}),
            node("Manual Trigger", "n8n-nodes-base.manualTrigger", 1, [480, 340], {})]


def fail(slug, pos=(960, 440)):
    return node("Run failed", "n8n-nodes-base.stopAndError", 1, list(pos),
                {"errorMessage": f"Apify run failed for {slug}. Check the token credential, plan credit and input JSON."})


def wf(name, nodes, conn):
    return {"name": name, "nodes": nodes, "connections": conn, "active": False,
            "settings": {"executionOrder": "v1"}, "pinData": {}, "meta": {"templateCredsSetupCompleted": False}, "tags": []}


SHEET_STEP = "Open the Google Sheets node(s), connect Google Sheets OAuth2, and replace `YOUR_SHEET_ID` (and the tab name if needed)."

# ---------------------------------------------------------------- 1. Google Maps leads
def maps():
    slug = "google-maps-places-scraper"
    body = {"searchStringsArray": ["coffee shop"], "locationQuery": "Detroit, MI", "maxCrawledPlacesPerSearch": 20}
    js = """// One clean lead row per place. Re-runs update the same row (matched on placeId) instead of duplicating.
const out = [];
for (const it of $input.all()) {
  const p = it.json;
  if (!p.placeId) continue;
  out.push({ json: {
    placeId: p.placeId,
    name: p.title || '',
    category: p.categoryName || '',
    address: p.address || '',
    city: p.city || '',
    state: p.state || '',
    phone: p.phone || '',
    website: p.website || '',
    rating: p.totalScore ?? '',
    reviews: p.reviewsCount ?? '',
    claimedByOwner: p.claimedByOwner ?? '',
    permanentlyClosed: p.permanentlyClosed ?? '',
    googleMapsUrl: p.url || '',
    searchedFor: p.searchString || '',
    scrapedAt: p.scrapedAt || new Date().toISOString(),
  } });
}
return out;"""
    n = [note("Google Maps leads to Google Sheets",
              "Search Google Maps like a customer would (keyword + city) and drop every business into a sheet: name, category, address, phone, website, rating, review count. Re-runs update existing rows, so the sheet stays one row per place.",
              [SHEET_STEP, "Edit `searchStringsArray` and `locationQuery` in *Run Apify actor* (more options: the actor page)."], slug),
         *triggers({"field": "weeks", "weeksInterval": 1, "triggerAtDay": [1], "triggerAtHour": 7}),
         apify(slug, body),
         code("Build lead rows", [960, 230], js),
         sheet("Append or update lead in Google Sheet", [1200, 230], match=["placeId"]),
         fail(slug)]
    k = {"Schedule Trigger": {"main": c("Run Apify actor")}, "Manual Trigger": {"main": c("Run Apify actor")},
         "Run Apify actor": {"main": [[{"node": "Build lead rows", "type": "main", "index": 0}], [{"node": "Run failed", "type": "main", "index": 0}]]},
         "Build lead rows": {"main": c("Append or update lead in Google Sheet")}}
    return "google-maps-leads-to-google-sheets", wf("Google Maps leads (phone, website, rating) to Google Sheets", n, k)


# ---------------------------------------------------------------- 2. TikTok profile stats
def tiktok():
    slug = "tiktok-public-profile-scraper"
    body = {"profiles": ["natgeo", "nba"], "resultsType": "profiles", "resultsPerPage": 10, "maxItems": 10}
    js = """// One row per profile per day: a follower / engagement history you can chart in Sheets.
const day = new Date().toISOString().slice(0, 10);
const out = [];
for (const it of $input.all()) {
  const p = it.json;
  if (p.type !== 'profile' && p.fans === undefined) continue;
  out.push({ json: {
    date: day,
    username: p.username || p.name || '',
    nickName: p.nickName || '',
    followers: p.fans ?? '',
    following: p.following ?? '',
    totalLikes: p.heart ?? '',
    videos: p.video ?? '',
    avgPlaysLatest: p.avgPlaysLatest ?? '',
    medianPlaysLatest: p.medianPlaysLatest ?? '',
    avgEngagementRateLatest: p.avgEngagementRateLatest ?? '',
    postsPerWeekLatest: p.postsPerWeekLatest ?? '',
    lastPostTime: p.lastPostTimeISO || '',
    verified: p.verified ?? '',
    profileUrl: p.profileUrl || '',
  } });
}
return out;"""
    n = [note("TikTok profile stats to Google Sheets",
              "Daily snapshot of public TikTok accounts: followers, total likes, video count, average and median plays, engagement rate and posting cadence of the latest posts. One new row per profile per day, so the sheet becomes a growth history.",
              [SHEET_STEP, "Edit the `profiles` list in *Run Apify actor* (usernames or profile URLs; public accounts only)."], slug),
         *triggers({"triggerAtHour": 7}),
         apify(slug, body),
         code("Build profile rows", [960, 230], js),
         sheet("Append to Google Sheet", [1200, 230]),
         fail(slug)]
    k = {"Schedule Trigger": {"main": c("Run Apify actor")}, "Manual Trigger": {"main": c("Run Apify actor")},
         "Run Apify actor": {"main": [[{"node": "Build profile rows", "type": "main", "index": 0}], [{"node": "Run failed", "type": "main", "index": 0}]]},
         "Build profile rows": {"main": c("Append to Google Sheet")}}
    return "tiktok-profile-stats-to-google-sheets", wf("TikTok profile stats (followers, plays, engagement) to Google Sheets", n, k)


# ---------------------------------------------------------------- 3. YouTube comments sentiment
def youtube():
    slug = "youtube-comments-scraper"
    body = {"startUrls": [{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}], "maxComments": 100,
            "sortBy": "TOP", "includeReplies": False}
    js = """// Quick keyword sentiment (no external API, no cost). Replace with an LLM node if you want nuance.
const POS = ['love','great','amazing','awesome','best','good','nice','beautiful','perfect','thank','thanks','legend','classic','favorite','favourite','brilliant','fantastic','wonderful','happy','enjoy','enjoyed','excellent','cool','fun','masterpiece'];
const NEG = ['hate','bad','worst','terrible','awful','boring','trash','garbage','stupid','annoying','disappointed','disappointing','waste','sucks','cringe','scam','fake','horrible','ugly','broken','useless','overrated'];
const words = (t) => (String(t || '').toLowerCase().match(/[a-z']+/g) || []);
const out = [];
for (const it of $input.all()) {
  const c = it.json;
  if (!c.commentId) continue;
  const w = words(c.text);
  let score = 0;
  for (const x of w) { if (POS.includes(x)) score++; if (NEG.includes(x)) score--; }
  out.push({ json: {
    commentId: c.commentId,
    videoTitle: c.videoTitle || '',
    videoUrl: c.videoUrl || '',
    comment: c.text || '',
    likes: c.likeCount ?? 0,
    replies: c.replyCount ?? 0,
    isReply: c.isReply ?? false,
    publishedAtApprox: c.publishedAtApprox || c.publishedTimeText || '',
    sentimentScore: score,
    sentiment: score > 0 ? 'positive' : score < 0 ? 'negative' : 'neutral',
  } });
}
return out;"""
    js2 = """// Roll the scored comments up into one summary row per video.
const by = {};
for (const it of $input.all()) {
  const r = it.json;
  const k = r.videoUrl || r.videoTitle;
  by[k] = by[k] || { date: new Date().toISOString().slice(0, 10), video: r.videoTitle, videoUrl: r.videoUrl, comments: 0, positive: 0, neutral: 0, negative: 0, likesOnComments: 0 };
  by[k].comments++; by[k][r.sentiment]++; by[k].likesOnComments += Number(r.likes) || 0;
}
return Object.values(by).map((s) => ({ json: { ...s, positivePct: Math.round(100 * s.positive / s.comments), negativePct: Math.round(100 * s.negative / s.comments) } }));"""
    n = [note("YouTube comments to Google Sheets for sentiment",
              "Pull the comments from any public YouTube video(s) (top or newest), score each as positive / neutral / negative, write one row per comment to the *Comments* tab and a roll-up per video to the *Summary* tab. Commenter names and channel links are intentionally not stored.",
              [SHEET_STEP + " Create two tabs: `Comments` and `Summary`.", "Edit `startUrls` (videos, Shorts, playlists or channels) and `maxComments` in *Run Apify actor*."], slug),
         *triggers({"triggerAtHour": 7}),
         apify(slug, body),
         code("Score sentiment", [960, 230], js),
         sheet("Append comments (Comments tab)", [1200, 160], match=["commentId"], tab="Comments"),
         code("Roll up per video", [1200, 330], js2),
         sheet("Append summary (Summary tab)", [1440, 330], tab="Summary"),
         fail(slug)]
    k = {"Schedule Trigger": {"main": c("Run Apify actor")}, "Manual Trigger": {"main": c("Run Apify actor")},
         "Run Apify actor": {"main": [[{"node": "Score sentiment", "type": "main", "index": 0}], [{"node": "Run failed", "type": "main", "index": 0}]]},
         "Score sentiment": {"main": c("Append comments (Comments tab)", "Roll up per video")},
         "Roll up per video": {"main": c("Append summary (Summary tab)")}}
    return "youtube-comments-sentiment-to-google-sheets", wf("YouTube comments sentiment to Google Sheets", n, k)


# ---------------------------------------------------------------- 4. LinkedIn jobs daily
def linkedin():
    slug = "linkedin-public-jobs"
    body = {"keywords": "data analyst", "location": "Chicago, IL", "datePosted": "24h", "maxItems": 25,
            "includeDescription": False, "onlyNewSinceLastRun": True, "stateStoreName": "n8n-linkedin-jobs-daily"}
    js = """// Belt and braces: skip jobs this workflow already reported (remembers the last 5000 ids).
const sd = $getWorkflowStaticData('global');
const seen = new Set(sd.seenJobIds || []);
const out = [];
for (const it of $input.all()) {
  const j = it.json;
  if (!j.jobId || seen.has(String(j.jobId))) continue;
  seen.add(String(j.jobId));
  out.push({ json: {
    jobId: j.jobId,
    title: j.title || '',
    company: j.company || '',
    location: j.location || '',
    postedAt: j.postedAt || '',
    seniority: j.seniority || '',
    employmentType: j.employmentType || '',
    salary: j.salaryText || '',
    applicants: j.applicantsText || '',
    jobUrl: j.jobUrl || '',
    companyUrl: j.companyUrl || '',
    foundAt: new Date().toISOString(),
  } });
}
sd.seenJobIds = Array.from(seen).slice(-5000);
return out;"""
    js2 = """// One Slack message per run (max 15 jobs listed). Returns nothing when there are no new jobs, so Slack stays quiet.
const jobs = $input.all().map((i) => i.json);
if (!jobs.length) return [];
const lines = jobs.slice(0, 15).map((j) => `- <${j.jobUrl}|${j.title}> at ${j.company} (${j.location})${j.salary ? ' - ' + j.salary : ''}`);
const more = jobs.length > 15 ? `\\n...and ${jobs.length - 15} more in the sheet.` : '';
return [{ json: { text: `*${jobs.length} new LinkedIn job(s)*\\n` + lines.join('\\n') + more } }];"""
    n = [note("LinkedIn jobs: daily new-jobs digest to Slack and Google Sheets",
              "Every morning, search public LinkedIn job listings (no login) for your keywords and location. Only jobs not seen before are appended to the sheet and posted to Slack as a single digest message.",
              [SHEET_STEP, "Slack node: create a Slack credential, replace `YOUR_CHANNEL_ID`. Delete the Slack branch if you only want the sheet.",
               "Edit `keywords`, `location`, `datePosted`, `maxItems` in *Run Apify actor*."], slug),
         *triggers({"triggerAtHour": 8}),
         apify(slug, body),
         code("Keep new jobs only", [960, 230], js),
         sheet("Append to Google Sheet", [1200, 160], match=["jobId"]),
         code("Build Slack digest", [1200, 330], js2),
         slack("Post to Slack", [1440, 330]),
         fail(slug)]
    k = {"Schedule Trigger": {"main": c("Run Apify actor")}, "Manual Trigger": {"main": c("Run Apify actor")},
         "Run Apify actor": {"main": [[{"node": "Keep new jobs only", "type": "main", "index": 0}], [{"node": "Run failed", "type": "main", "index": 0}]]},
         "Keep new jobs only": {"main": c("Append to Google Sheet", "Build Slack digest")},
         "Build Slack digest": {"main": c("Post to Slack")}}
    return "linkedin-jobs-daily-to-slack-and-google-sheets", wf("LinkedIn jobs daily digest to Slack and Google Sheets", n, k)


# ---------------------------------------------------------------- 5. Amazon price tracker
def amazon():
    slug = "amazon-product-search"
    body = {"asins": ["B07CMS5Q6P", "B09B8V1LZ3"], "marketplace": "US", "maxItems": 20, "includeDetails": False}
    js = """// Price log row per product per run, with the change since the previous run (remembered in workflow static data).
const sd = $getWorkflowStaticData('global');
sd.lastPrice = sd.lastPrice || {};
const day = new Date().toISOString().slice(0, 10);
const out = [];
for (const it of $input.all()) {
  const p = it.json;
  if (!p.asin) continue;
  const price = typeof p.price === 'number' ? p.price : parseFloat(String(p.price ?? '').replace(/[^0-9.]/g, ''));
  const prev = sd.lastPrice[p.asin];
  const has = Number.isFinite(price);
  const change = has && Number.isFinite(prev) ? Math.round((price - prev) * 100) / 100 : '';
  const pct = has && Number.isFinite(prev) && prev ? Math.round(1000 * (price - prev) / prev) / 10 : '';
  if (has) sd.lastPrice[p.asin] = price;
  out.push({ json: {
    date: day, asin: p.asin, title: p.title || '', brand: p.brand || '',
    price: has ? price : '', currency: p.currency || '', previousPrice: Number.isFinite(prev) ? prev : '',
    change, changePct: pct, listPrice: p.listPrice ?? '', rating: p.rating ?? '', reviewCount: p.reviewCount ?? '',
    availability: p.availability || '', url: p.url || '',
  } });
}
return out;"""
    n = [note("Amazon product price tracker to Google Sheets",
              "Track the Amazon price of any list of ASINs. Each run appends one row per product with the price, the previous price and the change, so the sheet is a price history you can chart or filter for drops.",
              [SHEET_STEP, "Edit the `asins` list and `marketplace` (US, UK, DE, CA) in *Run Apify actor*."], slug),
         *triggers({"triggerAtHour": 7}),
         apify(slug, body),
         code("Add price change", [960, 230], js),
         sheet("Append to Google Sheet", [1200, 230]),
         fail(slug)]
    k = {"Schedule Trigger": {"main": c("Run Apify actor")}, "Manual Trigger": {"main": c("Run Apify actor")},
         "Run Apify actor": {"main": [[{"node": "Add price change", "type": "main", "index": 0}], [{"node": "Run failed", "type": "main", "index": 0}]]},
         "Add price change": {"main": c("Append to Google Sheet")}}
    return "amazon-price-tracker-to-google-sheets", wf("Amazon product price tracker to Google Sheets", n, k)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "n8n"), exist_ok=True)
    for fn in (maps, tiktok, youtube, linkedin, amazon):
        name, w = fn()
        with open(os.path.join(ROOT, "n8n", name + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(w, f, indent=2, ensure_ascii=False)
        print("wrote", name)
