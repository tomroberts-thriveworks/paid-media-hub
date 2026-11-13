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

## Negative keyword decisions
- **2026-11-13: Tom is creating a new shared negative keyword list, applied to all campaigns, starting with `kid`/`kids` and `sex`.**
  Basis: 30-day search term review (Oct 14 - Nov 12, 2026, PMax + Search; account CPB $222):
  - `kids` (broad): ~1,600 terms, ~$4.2k, 6.5 Bookings* (~$644 CPB), ~92% Search. `kid`: ~$120, 0 Bookings*.
  - `sex` (broad): ~1,700 terms, ~$2.4k, 3.5 Bookings* (~$690 CPB). Booked terms were real sex-therapy intent ("sex therapist michigan", "christian sex therapist").
  - Broad `sex` also blocks "same sex couples/marriage counseling" and "sex abuse therapist" (~$90/30d). Small spend, but these are real services; phrase negatives (`sex therapist`, `sex therapy`, `sex addiction`, `sex counseling`) would spare them.
  - Not covered by `kids`: child / children / teen / pediatric terms (~$15k/30d, CPB ~$316). Still undecided.
- List created 2026-11-13: "All campaigns (potential future test)" (shared set 12312649365), attached to 89/90 campaigns (all except 1 paused Demand Gen). Members: broad `sex`, `kid`, `kids` (added by Tom); phrase `sex therapist`, `sex therapists`, `sex therapy`, `sex addiction`, `sex counseling` (added via API). The phrase ones are redundant while broad `sex` stays.
- **Revisit later (test, don't just leave excluded):** both themes had some real demand and bookings, just at 2-3x CPB. Possible tests: a dedicated child/teen or sex-therapy campaign with its own landing page, budget cap and tCPA; or re-open in states with child/sex-therapy clinician supply. Check first: minimum client age and which clinicians offer sex therapy.
- Other candidates from the same review, not yet actioned: medication-lookup phrases (`side effects`, `vs`, `uses`, `used for`, `what are`, `stages of grief`, autism levels, etc.); `what is` (PMax only; it blocks booking Search terms); competitor names leaking into PMax (blue umbrella psychiatry, emerald psychiatry). Keep bare drug names: they booked at a ~$156 CPB in PMax.
- Account facts: the ACCOUNT_LEVEL negative list is empty; the "| Exclude Everywhere" shared lists are what's attached to all PMax + Search campaigns. "GGL_NBD_PMAX_TalkTherapy | Universal Keyword Negative" (756 terms, includes phrase `therapy`/`therapist`) is attached to nothing; don't attach it as is.

## API access in the cloud session (2026-11-13)
- The proxy breaks the `Authorization` header to googleads.googleapis.com. What works: POST oauth2.googleapis.com/token with only grant_type=refresh_token + refresh token (proxy adds client auth), then call v23 `googleAds:search` with `?access_token=` plus the `login-customer-id` header. The repo client (`google_ads/rest.py`) does not do this yet.

## Brand restructure (2026-11-13)
- Tom moved `thriveworks` [exact] into its own ad group "Brand - Thrivewors Keyword" (GGL_BRD_GSE_National; 1 keyword, 1 RSA enabled + approved). At check time, `thriveworks` [exact] was still ENABLED in "Brand - Thriveworks EM" too (duplicate).
- Holding for now: splitting `thriveworks counseling` and the misspellings (thrivework / thrive work) into their own groups; moving the ambiguous `thrive …` keywords (~$17k/30d, mostly non-brand or other-practice traffic) out of brand.
