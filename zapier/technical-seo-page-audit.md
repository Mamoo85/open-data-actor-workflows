# Zapier: Technical SEO Page Audit: Broken Links, Hreflang, $3/1k

Technical SEO audit verified by 130 passing tests: title, meta, canonical, H1-H3, internal/external and broken links, missing alt, Open Graph, hreflang, JSON-LD, redirect chain, TTFB, and a...

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `https://api.apify.com/v2/acts/transparent_meteorite~technical-seo-page-audit/run-sync-get-dataset-items`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{
  "urls": [
    "https://example.com"
  ],
  "maxPages": 3,
  "checkBrokenLinks": true,
  "maxLinksToCheck": 15
}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/transparent_meteorite~technical-seo-page-audit/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: https://apify.com/transparent_meteorite/technical-seo-page-audit
