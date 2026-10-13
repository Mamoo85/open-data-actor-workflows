# Zapier setup

Zapier cannot import workflow files. Each `zapier/<actor>.md` is a recipe for **Webhooks by Zapier > Custom Request** (a paid Zapier feature) followed by a Looping step and Google Sheets > Create Spreadsheet Row. Not tested in a Zapier account. Zapier limits how long it waits for a webhook response, so slow actors may need the async pattern described in each recipe.
