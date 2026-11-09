# Project status and decisions
- Owner/user: Tom Roberts, Sr. Growth Marketing Manager, paid media. ~95% of use is Tom's; needs management + reporting access.
- Order: Google Ads first, then Microsoft Ads, then Meta Ads.
- **Decision (2026-11-09): audit first, no dashboard yet.** Read-only API pulls -> local files -> written findings. Dashboard only if something earns recurring use.
- Google Cloud: Google Ads API enabled; OAuth client (Desktop app) created. Client secret/refresh token/developer token are NOT in chat or repo; generate and store in local .env on the company laptop.
- Developer token: Explorer access GRANTED (~2,880 ops/day cap, verify); Basic access applied for, pending. Plan around the cap: wide search_stream queries, cache locally.
- Currently on a personal browser/device; company laptop arrives later this week. Everything portable via git + .env.example + SETUP.md. Hold credentials and real data pulls until the laptop.
- Never store PHI/client-level data; aggregate ad data only.
- Next: update naming parser for real names; account-map audit; conversion setup audit; refresh-token helper script (for laptop).
