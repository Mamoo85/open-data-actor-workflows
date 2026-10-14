# Open data actor workflows: n8n, Make and Zapier templates for Apify actors

Ready-made automation workflows for 24 open-data and lead-generation actors on Apify. Each one calls an actor, cleans the rows and appends them to Google Sheets, on a schedule or on demand. Formats: **n8n** (importable JSON), **Make** (blueprint, best effort), **Zapier** (copy-paste recipe).

**Disclosure:** these workflows are maintained by the author of the Apify actors they call. The actors use pay-per-result pricing; the free Apify plan credit covers a trial. The workflows themselves are MIT licensed and free.

## Status, honestly

| Platform | State |
|---|---|
| n8n | Node types checked against `n8n-nodes-base` 2.15.1 and connections checked by `tools/validate.py` (CI runs the offline part). The exact HTTP request (URL + body) of 3 workflows was run live against the Apify API (HTTP 201, rows returned). A full import into an n8n instance with Google Sheets credentials was not run by the author. |
| Make | Blueprints are **not import-tested, no Make login**. Treat as a starting point; the Google Sheets column mapping must be set by hand. |
| Zapier | No importable JSON exists. Recipes use Webhooks by Zapier (paid) and are untested in a Zapier account. |

## The 24 workflows

| Actor (Store page) | What it does | n8n | Make | Zapier |
|---|---|---|---|---|
| [FMCSA New Motor Carrier Leads](https://apify.com/transparent_meteorite/fmcsa-new-carrier-leads) | New motor carrier leads from the official FMCSA census: new USDOT/MC trucking companies with officer names,... | [n8n](n8n/fmcsa-new-carrier-leads.json) | [Make](make/fmcsa-new-carrier-leads.blueprint.json) | [Zapier](zapier/fmcsa-new-carrier-leads.md) |
| [WARN Layoff Notices API](https://apify.com/transparent_meteorite/warn-layoff-alerts) | WARN Act layoff notices from 7 official state sources (TX, CA, WA, OR, MD, VA, NC), verified by 89 passing... | [n8n](n8n/warn-layoff-alerts.json) | [Make](make/warn-layoff-alerts.blueprint.json) | [Zapier](zapier/warn-layoff-alerts.md) |
| [Website Tech Stack Lookup](https://apify.com/transparent_meteorite/website-tech-stack-detector) | 2,392 technology fingerprints with version and confidence, tested on 19,393 checks. Find the CMS, ecommerce... | [n8n](n8n/website-tech-stack-detector.json) | [Make](make/website-tech-stack-detector.blueprint.json) | [Zapier](zapier/website-tech-stack-detector.md) |
| [Career Site Jobs API](https://apify.com/transparent_meteorite/ats-open-roles) | Career-site jobs at $0.002 each, with seniority, department and ready-made company presets. Open roles from... | [n8n](n8n/ats-open-roles.json) | [Make](make/ats-open-roles.blueprint.json) | [Zapier](zapier/ats-open-roles.md) |
| [City Council Meetings & Agendas](https://apify.com/transparent_meteorite/city-council-agendas) | City council meetings and agenda items from 18 US cities via the official Legistar Web API. Meeting date and... | [n8n](n8n/city-council-agendas.json) | [Make](make/city-council-agendas.blueprint.json) | [Zapier](zapier/city-council-agendas.md) |
| [Company Enrichment by Domain](https://apify.com/transparent_meteorite/company-enrichment-by-domain) | Company enrichment from each company's own site and DNS only, verified by 73 passing tests. Domains in; name,... | [n8n](n8n/company-enrichment-by-domain.json) | [Make](make/company-enrichment-by-domain.blueprint.json) | [Zapier](zapier/company-enrichment-by-domain.md) |
| [SEC Form D Startup Funding Leads](https://apify.com/transparent_meteorite/sec-form-d-funding-leads) | Startup funding leads from official SEC EDGAR Form D filings at $0.0025 per filing. Issuer, industry,... | [n8n](n8n/sec-form-d-funding-leads.json) | [Make](make/sec-form-d-funding-leads.blueprint.json) | [Zapier](zapier/sec-form-d-funding-leads.md) |
| [Technical SEO Page Audit](https://apify.com/transparent_meteorite/technical-seo-page-audit) | Technical SEO audit verified by 130 passing tests: title, meta, canonical, H1-H3, internal/external and... | [n8n](n8n/technical-seo-page-audit.json) | [Make](make/technical-seo-page-audit.blueprint.json) | [Zapier](zapier/technical-seo-page-audit.md) |
| [Domain Intelligence](https://apify.com/transparent_meteorite/domain-intelligence-lookup) | Bulk domain lookup verified by 94 passing tests: RDAP registration (registrar, created, expires, age), DNS... | [n8n](n8n/domain-intelligence-lookup.json) | [Make](make/domain-intelligence-lookup.blueprint.json) | [Zapier](zapier/domain-intelligence-lookup.md) |
| [New Business Filings](https://apify.com/transparent_meteorite/new-business-filings) | New LLCs and corporations from official state open data (CO, NY, OR, CT), verified by 57 passing tests. Name,... | [n8n](n8n/new-business-filings.json) | [Make](make/new-business-filings.blueprint.json) | [Zapier](zapier/new-business-filings.md) |
| [App Store Reviews Scraper](https://apify.com/transparent_meteorite/app-store-reviews) | Apple App Store reviews at $0.50 per 1,000, verified by 85 passing tests. Review text, stars, app version,... | [n8n](n8n/app-store-reviews.json) | [Make](make/app-store-reviews.blueprint.json) | [Zapier](zapier/app-store-reviews.md) |
| [Website Contact Details Scraper](https://apify.com/transparent_meteorite/website-contact-extractor) | Website contact extractor: get emails, phone numbers and social media profiles from any list of business... | [n8n](n8n/website-contact-extractor.json) | [Make](make/website-contact-extractor.blueprint.json) | [Zapier](zapier/website-contact-extractor.md) |
| [Shopify Leads](https://apify.com/transparent_meteorite/shopify-store-leads) | Shopify leads with 60+ installed apps and theme detected per store. Store name, myshopify domain, country,... | [n8n](n8n/shopify-store-leads.json) | [Make](make/shopify-store-leads.blueprint.json) | [Zapier](zapier/shopify-store-leads.md) |
| [Local Business Leads](https://apify.com/transparent_meteorite/local-business-leads) | Local business leads at $0.003 per place, including businesses with no website listed. Name, phone, website,... | [n8n](n8n/local-business-leads.json) | [Make](make/local-business-leads.blueprint.json) | [Zapier](zapier/local-business-leads.md) |
| [Workday Jobs Scraper](https://apify.com/transparent_meteorite/workday-jobs-scraper) | Workday jobs from 165+ verified employers or any myworkdayjobs.com site, verified by 64 passing tests.... | [n8n](n8n/workday-jobs-scraper.json) | [Make](make/workday-jobs-scraper.blueprint.json) | [Zapier](zapier/workday-jobs-scraper.md) |
| [Company News Monitor](https://apify.com/transparent_meteorite/company-news-monitor) | Company news monitoring at $0.002 per article from 75 publisher RSS feeds (Bloomberg, CNBC, FT, TechCrunch,... | [n8n](n8n/company-news-monitor.json) | [Make](make/company-news-monitor.blueprint.json) | [Zapier](zapier/company-news-monitor.md) |
| [Building Permits Leads](https://apify.com/transparent_meteorite/building-permits-leads) | Building permits leads from official city open-data portals (Chicago, NYC, LA, SF, Seattle, Austin, Baton... | [n8n](n8n/building-permits-leads.json) | [Make](make/building-permits-leads.blueprint.json) | [Zapier](zapier/building-permits-leads.md) |
| [Sitemap Link Inventory](https://apify.com/transparent_meteorite/sitemap-link-inventory) | Find every sitemap for a domain (robots.txt, nested indexes, .gz, .txt, common paths) and return all URLs... | [n8n](n8n/sitemap-link-inventory.json) | [Make](make/sitemap-link-inventory.blueprint.json) | [Zapier](zapier/sitemap-link-inventory.md) |
| [Hacker News, npm & PyPI Developer Signals](https://apify.com/transparent_meteorite/developer-signals) | Track Hacker News mentions, Show HN and Launch HN posts, plus npm and PyPI package versions, repo links and... | [n8n](n8n/developer-signals.json) | [Make](make/developer-signals.blueprint.json) | [Zapier](zapier/developer-signals.md) |
| [Sanctions Screening](https://apify.com/transparent_meteorite/sanctions-screening) | Screen names of people, companies and vessels against the official OFAC SDN, OFAC Consolidated, UN, EU and UK... | [n8n](n8n/sanctions-screening.json) | [Make](make/sanctions-screening.blueprint.json) | [Zapier](zapier/sanctions-screening.md) |
| [Federal Grants & Contracts Finder](https://apify.com/transparent_meteorite/federal-grants-contracts) | Open and forecasted federal grant opportunities from Grants.gov plus contract and grant awards from... | [n8n](n8n/federal-grants-contracts.json) | [Make](make/federal-grants-contracts.blueprint.json) | [Zapier](zapier/federal-grants-contracts.md) |
| [Amazon Product Search](https://apify.com/transparent_meteorite/amazon-product-search) | Amazon product data at $0.004 per product, 20% below the alternative we tested (free plan), with 41 filled... | [n8n](n8n/amazon-product-search.json) | [Make](make/amazon-product-search.blueprint.json) | [Zapier](zapier/amazon-product-search.md) |
| [LinkedIn Public Jobs Scraper (no login) | Salary & Level](https://apify.com/transparent_meteorite/linkedin-public-jobs) | 28 filled fields per LinkedIn job vs 23 in our side-by-side test, at a lower price per job. Search public... | [n8n](n8n/linkedin-public-jobs.json) | [Make](make/linkedin-public-jobs.blueprint.json) | [Zapier](zapier/linkedin-public-jobs.md) |
| [Meta Ad Library Scraper](https://apify.com/transparent_meteorite/meta-ad-library) | Image or video URL on 100% of ads vs 70% in our side-by-side test, at $0.00065 per ad. Search the public Meta... | [n8n](n8n/meta-ad-library.json) | [Make](make/meta-ad-library.blueprint.json) | [Zapier](zapier/meta-ad-library.md) |

## Quick start (n8n)

1. Get an Apify API token: Apify Console > Settings > Integrations.
2. In n8n create a *Header Auth* credential named `Apify API token`: name `Authorization`, value `Bearer <your token>`.
3. Import `n8n/<actor>.json` (Workflows > Import from file).
4. Open *Append to Google Sheet*, connect Google, replace `YOUR_SHEET_ID`, pick your tab.
5. Edit the JSON body in *Run Apify actor* to your filters, click Execute, then activate.

Each workflow: Schedule Trigger (daily 07:00) + Manual Trigger, HTTP Request (3 tries, 5 min timeout, error output to a Stop and Error node), Code node (drops empty rows, flattens nested values, caps at 500 rows), Google Sheets append.

More: [docs/n8n.md](docs/n8n.md), [docs/make.md](docs/make.md), [docs/zapier.md](docs/zapier.md), [docs/SUBMISSION.md](docs/SUBMISSION.md).

## Regenerate and validate

```
python tools/generate.py   # rebuilds n8n/, make/, zapier/ from data/
python tools/validate.py   # JSON parse + connection integrity (CI runs this)
```

The sample inputs in `data/sample_inputs.json` are small, live-verified inputs. Raise the result limits for production use; results are billed per result.

## License

MIT, see [LICENSE](LICENSE).
