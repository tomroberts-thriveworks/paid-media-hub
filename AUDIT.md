# Running the Google Ads audit
The connector calls the REST API directly (stdlib only; no google-ads library needed).

## Cloud session setup (current)
Environment > Edit:
- Network secrets:
  - host `googleads.googleapis.com`, Token, header `developer-token`, no prefix = developer token
  - host `oauth2.googleapis.com`, Username/password = OAuth client ID / client secret
- Environment variables: `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID`, `GOOGLE_ADS_CUSTOMER_IDS`
- Allowed domains: `googleads.googleapis.com`, `oauth2.googleapis.com`
Settings load at session start: start a new session after changes.

## Laptop setup (later)
Put all values in `.env` (incl. GOOGLE_ADS_CLIENT_ID/SECRET and DEVELOPER_TOKEN); the client
sends them itself. `scripts/get_refresh_token.py` creates the refresh token (needs `.[google]`).
Revoke the cloud refresh token at myaccount.google.com/permissions when moving.

## Commands (run from repo root with PYTHONPATH=src, or after `pip install -e .`)
1. `python -m paidmedia.audit check`  -> auth + accessible accounts (1-2 requests)
2. `python -m paidmedia.audit pull --end YYYY-MM-DD --only campaigns conversion_actions`
3. `python -m paidmedia.audit pull --end YYYY-MM-DD`  (4 requests per account)
4. `python -m paidmedia.audit report` -> data/reports/ (offline, free to re-run; data/ is gitignored)

Read `2_conversion_setup.md` first: if Event 1/Event 4 are not matched by name, fix
`BOOKING_EVENT_NAMES` in `src/paidmedia/metrics.py` before trusting any CPB.
Status: report logic tested on synthetic data; REST client unit-checked but never run live.
