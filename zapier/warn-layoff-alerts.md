# Zapier: WARN Layoff Notices API: 7 States (TX CA WA OR MD VA NC) $3/1k

WARN Act layoff notices from 7 official state sources (TX, CA, WA, OR, MD, VA, NC), verified by 89 passing tests. Clean rows: employer, workers affected, city, notice and layoff dates. Deduped across...

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `https://api.apify.com/v2/acts/transparent_meteorite~warn-layoff-alerts/run-sync-get-dataset-items`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{
  "states": [
    "TX"
  ],
  "daysBack": 365,
  "maxResults": 5,
  "onlyNewSinceLastRun": false
}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/transparent_meteorite~warn-layoff-alerts/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: https://apify.com/transparent_meteorite/warn-layoff-alerts
