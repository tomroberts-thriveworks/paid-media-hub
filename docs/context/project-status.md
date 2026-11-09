# Project status and decisions
- Owner/user: Tom Roberts, Sr. Growth Marketing Manager, paid media. ~95% of use is Tom's; needs management + reporting access.
- Order: Google Ads first, then Microsoft Ads, then Meta Ads.
- **Decision (2026-11-09): audit first, no dashboard yet.** Read-only API pulls -> local files -> written findings. Dashboard only if something earns recurring use.
- Google Cloud: Google Ads API enabled; OAuth client (Desktop app) created. Client secret/refresh token/developer token are NOT in chat or repo; generate and store in local .env on the company laptop.
- Developer token: Explorer access GRANTED (~2,880 ops/day cap, verify); Basic access applied for, pending. Plan around the cap: wide search_stream queries, cache locally.
- Currently on a personal browser/device; company laptop arrives later this week. Everything portable via git + .env.example + SETUP.md. Hold credentials and real data pulls until the laptop.
- Never store PHI/client-level data; aggregate ad data only.
- Next: update naming parser for real names; account-map audit; conversion setup audit; refresh-token helper script (for laptop).

## Cloud API setup (2026-11-09)
- Running the audit in the cloud session (user decision), not waiting for laptop.
- Network secrets: googleads.googleapis.com -> `developer-token` header; oauth2.googleapis.com -> Basic auth with the **Web application** OAuth client (Desktop client's secret was exposed in a screenshot; that client is to be deleted).
- Env vars: GOOGLE_ADS_REFRESH_TOKEN (from OAuth Playground, own credentials), GOOGLE_ADS_LOGIN_CUSTOMER_ID, GOOGLE_ADS_CUSTOMER_IDS.
- Allowed domains: googleads.googleapis.com, oauth2.googleapis.com.
- Next: `PYTHONPATH=src python -m paidmedia.audit check`, then pull campaigns + conversion_actions, fix first-run issues, full pull, then deep structure review (user's first priority).
- When moving to the laptop: revoke this refresh token, create a new one there.
