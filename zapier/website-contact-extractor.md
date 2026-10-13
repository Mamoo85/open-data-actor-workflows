# Zapier: Website Contact Details Scraper: Emails, Phones & Socials $2/1k

Website contact extractor: get emails, phone numbers and social media profiles from any list of business websites. One clean row per site with role/named email tags, E.164 phones, 8 socials and...

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `https://api.apify.com/v2/acts/transparent_meteorite~website-contact-extractor/run-sync-get-dataset-items`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{
  "startUrls": [
    {
      "url": "https://www.shinola.com"
    },
    {
      "url": "https://buddyspizza.com"
    }
  ],
  "maxPagesPerSite": 5,
  "includeNamedEmails": true,
  "sameDomainOnly": true
}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/transparent_meteorite~website-contact-extractor/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: https://apify.com/transparent_meteorite/website-contact-extractor
