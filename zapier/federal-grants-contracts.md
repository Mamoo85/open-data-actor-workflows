# Zapier: Federal Grants & Contracts Finder: Grants.gov + USAspending

Open and forecasted federal grant opportunities from Grants.gov plus contract and grant awards from USAspending.gov, in one unified schema: deadlines, ceilings, amounts, agency, NAICS/PSC, recipient,...

Zapier has no importable workflow JSON, so this is a recipe. It uses **Webhooks by Zapier** (a paid Zapier feature). Not tested end to end in a Zapier account.

1. Trigger: *Schedule by Zapier* (every day), or any trigger you like.
2. Action: *Webhooks by Zapier* > **Custom Request**.
   - Method: `POST`
   - URL: `https://api.apify.com/v2/acts/transparent_meteorite~federal-grants-contracts/run-sync-get-dataset-items`
   - Data Pass-Through: No
   - Data (raw JSON):

```json
{
  "keywords": [
    "cybersecurity"
  ],
  "mode": "both",
  "maxItems": 5,
  "awardKinds": [
    "contracts"
  ],
  "awardsLookbackDays": 365,
  "minAwardAmount": 1000000
}
```

   - Headers:
     - `Content-Type`: `application/json`
     - `Authorization`: `Bearer YOUR_APIFY_TOKEN`
   - Unflatten: Yes
3. The response is a list of result rows. Add *Looping by Zapier* (create loop from line items), then **Google Sheets > Create Spreadsheet Row** per item.
4. Caveat: Zapier webhooks wait only a limited time for a response, and the sync endpoint can take longer. If the request times out, start the run asynchronously (`POST https://api.apify.com/v2/acts/transparent_meteorite~federal-grants-contracts/runs`) and trigger a second Zap from an Apify "run succeeded" webhook, then fetch the dataset items.

Store page: https://apify.com/transparent_meteorite/federal-grants-contracts
