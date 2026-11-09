# Running the Google Ads audit (company laptop)
1. Setup: see SETUP.md (clone, venv, `pip install -e ".[google,dev]"`, `cp .env.example .env`).
2. Fill `.env`: developer token, client ID + secret, login (MCC) customer ID, customer IDs. Leave refresh token blank.
3. `python scripts/get_refresh_token.py` (browser sign-in; token saved to .env, not shown).
4. Smoke test (2 API requests per account):
   `python -m paidmedia.audit pull --end 2026-11-08 --only campaigns conversion_actions`
5. Full pull (4 requests per account; stays well inside Explorer's daily cap):
   `python -m paidmedia.audit pull --end 2026-11-08`
6. Offline analysis, free to re-run: `python -m paidmedia.audit report` -> `data/reports/`
   1_account_map.md, 2_conversion_setup.md, 3_efficiency.md (data/ is gitignored).

Read `2_conversion_setup.md` first: if Event 1/Event 4 are not matched by name, fix
`BOOKING_EVENT_NAMES` in `src/paidmedia/metrics.py`, re-run `report`, then trust the CPB numbers.
Status: report logic tested on synthetic data only; the API pull has not run against a live account,
so expect small fixes on first run. Raw data and reports stay on the company laptop.
