# Make setup (not import-tested)

The blueprints in `make/` were written from Make's blueprint format without access to a Make account, so they are **not import-tested**. If import fails, build the same three modules by hand:

1. **HTTP > Make a request**: POST to the URL in the blueprint, header `Authorization: Bearer YOUR_APIFY_TOKEN`, body type Raw / JSON, body from the blueprint, parse response = yes, timeout 300.
2. **Iterator** over the response `data` array.
3. **Google Sheets > Add a row**: connect Google, choose the spreadsheet (replace `YOUR_SHEET_ID`), map columns from the iterator.

Make's HTTP module has a maximum timeout, so for slow actors use the async run endpoint and a webhook.
