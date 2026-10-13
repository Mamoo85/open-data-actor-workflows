# n8n setup

1. Credentials > Create > **Header Auth**. Name: `Apify API token`. Header name `Authorization`. Value `Bearer YOUR_APIFY_TOKEN`.
2. Workflows > Import from file > pick `n8n/<actor>.json`.
3. In *Run Apify actor*, select the credential. Edit the JSON body for your filters.
4. In *Append to Google Sheet*, add a Google Sheets OAuth2 credential, replace `YOUR_SHEET_ID` (the long id in the sheet URL) and choose the tab. Auto-map mode matches columns by header name in the first row of the tab.
5. Execute the workflow manually once, check the sheet, then activate it.

The HTTP node uses Apify's `run-sync-get-dataset-items` endpoint: it starts the actor, waits (up to 300 s here) and returns rows. For long runs, use the async `/runs` endpoint plus a webhook instead.
