# Zapier: Sitemap Link Inventory: All URLs + Broken-Link Check, $1/1k

Find every sitemap for a domain (robots.txt, nested indexes, .gz, .txt, common paths) and return all URLs with lastmod, priority, images, hreflang, path groups and duplicates. Optional broken-link,...

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `https://api.apify.com/v2/acts/transparent_meteorite~sitemap-link-inventory/run-sync-get-dataset-items`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{
  "startUrls": [
    "https://crawlee.dev"
  ],
  "maxUrlsPerSite": 10,
  "checkMode": "sitemapUrls",
  "maxLinksToCheck": 10
}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/transparent_meteorite~sitemap-link-inventory/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: https://apify.com/transparent_meteorite/sitemap-link-inventory
