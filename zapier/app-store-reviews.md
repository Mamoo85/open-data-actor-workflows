# Zapier: App Store Reviews Scraper: Ratings, 150+ Countries, $0.50/1k

Apple App Store reviews at $0.50 per 1,000, verified by 85 passing tests. Review text, stars, app version, date, votes, plus rating, rating count, price, genre and release notes. 150+ countries,...

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `https://api.apify.com/v2/acts/transparent_meteorite~app-store-reviews/run-sync-get-dataset-items`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{
  "appIds": [
    "https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580"
  ],
  "countries": [
    "us"
  ],
  "maxReviewsPerApp": 5,
  "includeAppDetails": true
}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/transparent_meteorite~app-store-reviews/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: https://apify.com/transparent_meteorite/app-store-reviews
