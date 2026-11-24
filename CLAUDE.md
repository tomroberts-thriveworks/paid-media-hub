# paid-media-hub
Read docs/context/ first: project-status.md, onboarding-guide.md, data-sources.md, open-questions.md.
Key rules: Bookings* = Event 1 + Event 4; CPB = spend/Bookings*; never report proxy-goaled campaigns' own "conversions" as bookings; "Tier" = supply tier, not goal type; HIPAA - aggregate data only, no PHI; never commit secrets (.env is gitignored).
Audit-first: read-only API use until told otherwise.
Google Ads API (cloud): use the repo client `src/paidmedia/google_ads/rest.py` (run `PYTHONPATH=src python -m paidmedia.audit check` first). The proxy overwrites any Authorization header to googleads.googleapis.com, so the client sends the token as `?access_token=`; don't "fix" the network secret. Read-only unless the user approves a change; log account changes in docs/context/project-status.md.
