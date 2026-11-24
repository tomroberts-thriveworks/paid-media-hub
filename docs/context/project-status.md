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
- The proxy breaks the `Authorization` header to googleads.googleapis.com. What works: POST oauth2.googleapis.com/token with only grant_type=refresh_token + refresh token (proxy adds client auth), then call v23 `googleAds:search` with `?access_token=` plus the `login-customer-id` header. The repo client (`src/paidmedia/google_ads/rest.py`) does this in cloud mode since 2026-11-24 (no GOOGLE_ADS_DEVELOPER_TOKEN set); tested with `python -m paidmedia.audit check`.

## Brand restructure (2026-11-13)
- Tom moved `thriveworks` [exact] into its own ad group "Brand - Thrivewors Keyword" (GGL_BRD_GSE_National; 1 keyword, 1 RSA enabled + approved). At check time, `thriveworks` [exact] was still ENABLED in "Brand - Thriveworks EM" too (duplicate).
- Holding for now: splitting `thriveworks counseling` and the misspellings (thrivework / thrive work) into their own groups; moving the ambiguous `thrive …` keywords (~$17k/30d, mostly non-brand or other-practice traffic) out of brand.

## GGL_NBD_GSE_ExactMatch_Tier 1 target raise (2026-11-13)
- Tom plans to take it off portfolio "TW Non-brand | EM Tier 1 Only | tCPA | Account Goals" (only campaign in that portfolio; tCPA $36) and raise the target.
- Baseline, Oct 14 - Nov 12: $44.3k spend; bids on account-level goals (1,008 conv: 796 CallRail local click-to-calls, 145 phone calls, 66 Event 1) = $44 per bidding conversion, already above the $36 target. Bookings* 224 (E1 66 / E4 158) -> CPB $198 vs $265 for all non-brand Search; Event 1-only CPB $672, also among the best. Search IS 16%, 84% lost to rank, 0% to budget ($4,800/day budget).
- Same setup on GGL_NBD_GSE_ExactMatch_Tier 1_PsychMedication (portfolio tCPA $38, CPB $205).
- Judge the change on Bookings* CPB, not the campaign's own CPA.

## Sheet vs account location audit (2026-11-16)
TT/NP Spending Recos tabs are meant to track what's on/off by state. Checked against enabled Google campaigns with spend (Nov 9-15):
- **Targeting matches the sheet** for TT broad, TT PMax, TT exact, brand (27 states), NP broad, NP PMax and NP exact (T1/T2). 0 state-level mismatches.
- **Mismatch: Demand Gen.** The sheet says TalkTherapy Demand Gen is ON for NC, SC, VA; the only Demand Gen campaign is paused.
- **Out-of-state serving:** $70k of $776k (9%), Oct 17-Nov 15, came from users outside the campaign's target states, at $313 CPB vs $230 in-state. Mostly from 5 campaigns set to "Presence or interest" (BroadMatch T3T4, SC, NC, PA; PMax TalkTherapy V2 and T3T4); the rest use "Presence". Biggest out-of-state users: TN, NM, MD, AL, OH (sheet off or paused for most channels). Recommend switching those to Presence.
- Not checked: Bing, Meta, ChatGPT, ZocDoc columns (no API access yet).
- **2026-11-16: switched 6 campaigns from "Presence or interest" to "Presence"** via API (Tom approved): BroadMatch_Tier 3 Tier 4, BroadMatch_South Carolina, BroadMatch_Tier 1_Pennsylvania, BroadMatch_Tier 1_North Carolina, PMAX_TalkTherapy V2, PMAX_TalkTherapy Tier 3 Tier 4. All enabled campaigns are now Presence. Change history (Oct 18-Nov 16) showed no location-target edits in these campaigns, so the out-of-state baseline wasn't caused by old targeting. Baseline: $70k/30d out-of-state at $313 CPB. Re-check ~Nov 30: out-of-state share, total Bookings*, CPB.

## Tier 1 rebuild (decided 2026-11-17)
- Two new campaigns, one match type each: `GGL_NBD_GSE_Tier 1_TalkTherapy_Phrase` (city/location keywords) and `GGL_NBD_GSE_Tier 1_TalkTherapy_Broad` (service/specialty keywords). They sit alongside the state-only campaigns (Geo_ / BroadMatch_), which stay for volume.
- States = TT Tier 1 per the spend calculator: FL, GA, MA, NC, NJ, PA, SC, TX, VA (drops IL, MI vs ExactMatch_Tier 1).
- Each campaign needs the full Paid Search Campaign Launch SOP (2 NICE numbers, CallRail pool + EXT, swap ticket, mapping sheets, workflow keyed on campaign ID, since utm_campaign={campaignid}).
- Draft keywords from ExactMatch_Tier 1 history: Phrase 27 city ad groups / 121 kws; Broad 16 ad groups / 157 kws (keep rule: >=1,000 impr or >=3 Bookings* in 90d). 12 kids/sex keywords dropped (blocked by the "All campaigns" negative list).
- Routing: add Phrase campaign city names as negatives on the Broad campaign (and consider on state campaigns), otherwise broad keywords compete for city searches.

## Region PsychMedication changes (2026-11-23)
- Region's role (per Tom's team): broad + phrase layer for any state with at least 3 psychiatry providers; EM Tier 1 Psych = exact match for the highest-supply psych states.
- **2026-11-23, via API (Tom approved):** AI Max turned OFF on GGL_NBD_GSE_Region_PsychMedication_LC (PMax expected to pick up the expansion traffic). Added states FL, NC, NM, DE, IN, LA, ID, OK (open psychiatry capacity per NP utilization). Region now targets 22 states; CO, OH, OR are still excluded (reason unknown, left as is).
- Baseline before the change (Aug 19 - Nov 22): AI Max-matched terms in Region $6.8k at $236 CPB vs $250 for keyword-matched terms. Re-check ~Dec 7: Region spend mix by state, CPB, and whether PMax psych volume rose.
- California held: the paused GGL_NBD_GSE_Psych_GEO_California ($1,000/day budget) should be audited and relaunched instead.
- Psychologist keywords always belong in therapy campaigns, not psychiatry (Tom, 2026-11-23).
- Drafts (not built): psych EM catch-all breakout and Region city phrase ad groups (34 cities, 204 phrase keywords), Google Sheet "Psych Exact Match (T1 and T2) ad group breakout draft".

## California psych relaunch prep (2026-11-23)
- GGL_NBD_GSE_Psych_GEO_California (ID 22470345054) last ran Oct 15, 2025. Jul-Oct 2025 (after Event 4 tracking started): $10.3k, 63 Bookings*, ~$163 CPB. Audit: Google Sheet "CA Psych relaunch audit (GGL_NBD_GSE_Psych_GEO_California)".
- **2026-11-23, via API (Tom approved), campaign still PAUSED:** budget $1,000 -> $300/day; bidding Target ROAS portfolio "TW Non-Brand California Psych" (1.1) -> Maximize conversions; campaign goal set to "CG: Event 1 & Event 4"; ad-group tROAS (payer groups) and $110 tCPA (Service - Psychiatry) cleared; Service - Child/Psychiatry enabled; 41 keywords paused (psychologist/therapy intent, plus "psychiatrist near me accepting new patients" and "psychiatrist for teens near me" broad); "psychiatrist newport news" removed; 12 phrase negatives (kaiser, medi cal, medi-cal, molina, psicologo/psicólogo(s), psychologist, psychology, therapist, counseling); 35 ads moved from /book-online/ and /psychiatry/ to /find-help/psychiatry-care/ (insurance-page ads unchanged); 16 office-city ad groups "Loc - {City}, CA" with 6 phrase keywords each (HEALTH_IN_PERSONALIZED_ADS exemption requested) and one RSA copied from Service - Psychiatry.
- Before enabling: CA call center hours (schedule is in ET, runs ~5am-5pm PT weekdays), Carelon/Lucet CA network, CA min patient age, ad copy fixes + in-network plan count, call asset 855-470-2956 / NICE / CallRail / channel mapping, psych sitelinks, which CA offices have psychiatry providers.
- **2026-11-23 (later), via API (Tom approved): ENABLED** (serving, learning). Also paused Payers - Carelon and Payers - Lucet; fixed RSA headlines in 15 ads ("Psychiatry & Psychiatry", "Find an Carelon/Medicare", "Psychiatrists Who Accepts UHC"; "360+/585+ Plans In-Network" -> "Most Insurance Accepted"). Kept: ET ad schedule (Tom OK'd), all phone numbers as-is, paused campaign sitelinks. Open: CA minimum patient age (Child group enabled); which CA offices have psychiatry providers (city groups left on; psych is mostly online).
- **2026-11-24, via API (Tom asked):** day 1 (Nov 23) spent $439, 18 clicks, $24.40 avg CPC, 0 Bookings*. Added a $10 CPC cap: new portfolio "TW Non-Brand CA Psych | Max Conv | $10 CPC cap" (Maximize conversions, cpc_bid_ceiling $10), campaign moved onto it. Paused 56 of 69 Service - Psychiatry keywords (no 2025 bookings, plus "mental health psychiatrist" broad at $41 CPC); 13 left. Negatives: stanford, mental health clinic, mental health facility/facilities.
- **2026-11-24, via API (Tom approved):** payer groups de-duplicated: 57 keywords paused (same wording in exact/phrase, accept/take/accepting variants); 3-4 phrase-led keywords left per payer group (Aetna, Anthem, BCBS, Cigna, Humana, Medicare, Tricare, UHC).
- After launch: add tCPA (~$200) once ~30 bookings; watch EM T1 Psych CA CPB (baseline $296, Aug 24-Nov 22).

## Michigan exact/phrase test (2026-11-24)
- Geo_Michigan traffic fell from ~4,000 clicks/mo (Q1) to 1,200-2,600 (Apr-Oct); bookings held (73 Jan, 85 Oct). Causes: "find a therapist" [phrase] (Q1: 3,682 clicks, 56 Bookings*) did not serve Jul-Oct and is back at 32% IS; ~70% IS lost to rank with tCPA $200 vs ~$244 actual CPB; everything consolidated into Service - Psychology. Draft: Google Sheet "Michigan (GGL_NBD_GSE_Geo_Michigan) restructure draft".
- **2026-11-24, via API (Tom asked):** added 32 ad groups alongside the 8 existing live ones (left unchanged): 9 "EM | ..." exact groups (31 keywords with 3+ Bookings* in Q1 or last 90d), 12 "PH | ..." phrase groups (all 57 keep keywords) and 11 "PH | Loc: {City}, MI" groups (9 offices + Lansing, Kalamazoo; 6 phrase kws each). RSAs copied from the matching live groups. AI Max search-term matching disabled on all 32 new groups (campaign-level AI Max still on). Not changed: tCPA $200, budget, schedule (weekdays only).
- **2026-11-24 (Tom asked):** removed all 118 paused ad groups in Geo_Michigan (none had impressions in the last 30 days). Campaign now has 40 ad groups, all enabled (8 original + 32 new).
- Compare new vs old groups after 2-3 weeks: clicks, impression share, CPB.

## Spend vs distance to offices (distance_view, Aug 19 - Nov 16, 2026; non-brand)
- Distance from the user to the nearest location asset (cumulative buckets differenced): 41% of spend within 5 mi, 71% within 10 mi, 84% within 15 mi, 98% within 40 mi.
- CPB is flat across distance: $245-$273 in every band (Event 1-only CPB also flat, $760-$1,200, no trend). Same pattern for PMax and Search separately.
- Conclusion: spend is concentrated near offices, but near-office traffic books at the same efficiency as distant traffic, so an office-exclusion duplicate isn't supported on efficiency. The open question is incrementality (would near-office bookings happen anyway via GBP/organic?), which needs a geo holdout, not a duplicate campaign.
- Double-check (2026-11-17): distance_view total ($2,518k) reconciles with enabled non-brand spend ($2,523k); buckets are cumulative. CPC falls with distance ($4.90 at 1-5 mi, $3.44 at 20-25 mi, $2.71 at 35-40 mi, $1.02 at 40+ mi) while CPB stays flat, so Google is bidding up near offices because conversion rates are higher there. Every enabled campaign has location asset sets attached, so there's no internal control; the planned Tier 1 Virtual campaign (location assets excluded) is the first clean comparison.
- City report (geographic_view, 90d non-brand, $2.10M with city): spread across 13.9k cities; top 25 = 20% of spend, top 100 = 39%. CPB flat by city size ($249-$262 in every rank band). Top cities: Houston, San Antonio, Jacksonville, Philadelphia, Virginia Beach.
- Office vs non-office cities (90d non-brand, $2.10M with city; office cities from the SiteID Phone Numbers tab matched to the 340 active location-asset store codes, 16 codes unmapped): 262 office cities = 45% of spend and 46% of Bookings*, CPB $254, CPC $4.81. The other 13,654 cities = 55% of spend, CPB $259, CPC $3.83.
