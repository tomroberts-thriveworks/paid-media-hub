# Tier 1 Talk Therapy launch: 3 campaigns (created 2026-11-17, PAUSED)
SOP: "SOP- Attribution for Online Channel Mapping and COE calls" > PAUSED SEARCH CAMPAIGN LAUNCH SOP.
Tracking: the account-level template sends `utm_campaign={campaignid}`, so the CallRail landing parameter for each pool is `utm_campaign=<Campaign ID>`.

| Campaign | Campaign ID | CallRail landing param | Pool / NICE name | Call asset name |
|---|---|---|---|---|
| GGL_NBD_GSE_Tier 1_TalkTherapy_Phrase | 24470038974 | utm_campaign=24470038974 | Paid Search - GGL_NBD_GSE_Tier 1_TalkTherapy_Phrase | Paid Search - GGL_NBD_GSE_Tier 1_TalkTherapy_Phrase - EXT |
| GGL_NBD_GSE_Tier 1_TalkTherapy_Broad | 24470038980 | utm_campaign=24470038980 | Paid Search - GGL_NBD_GSE_Tier 1_TalkTherapy_Broad | Paid Search - GGL_NBD_GSE_Tier 1_TalkTherapy_Broad - EXT |
| GGL_NBD_GSE_Tier 1_TalkTherapy_Virtual | 24470038992 | utm_campaign=24470038992 | Paid Search - GGL_NBD_GSE_Tier 1_TalkTherapy_Virtual | Paid Search - GGL_NBD_GSE_Tier 1_TalkTherapy_Virtual - EXT |

## NICE numbers (received 2026-11-20)
Confirmed 2026-11-20: "1" = pool number (CallRail pool and workflow branch forward here), "2" = call-asset number (the " - EXT" CallRail number forwards here).

| Campaign | NICE 1 (pool) | NICE 2 (call asset / EXT) |
|---|---|---|
| GGL_NBD_GSE_Tier 1_TalkTherapy_Phrase | 855-973-6600 | 855-973-7422 |
| GGL_NBD_GSE_Tier 1_TalkTherapy_Broad | 855-973-6925 | 855-973-7596 |
| GGL_NBD_GSE_Tier 1_TalkTherapy_Virtual | 855-973-7227 | 855-973-7711 |

## Built (via API)
- All 3: Search only (no partners/display), English, 9 TT Tier 1 states (FL GA MA NC NJ PA SC TX VA) on Presence, ad schedule copied from ExactMatch_Tier 1 (M-F 8-23, Sa-Su 8-18), the same 12 shared negative lists as ExactMatch_Tier 1, Maximize Conversions with no target.
- Phrase / Broad: account-level goals (same as ExactMatch_Tier 1); "All Locations Practices" location group attached.
- Virtual: campaign goal "CG: Event 1 & Event 4"; no location group; account-level Business Profile locations excluded (LOCATION_SYNC). The account-level "All Locations Practices" static group can't be excluded via API. Check location-asset impressions after launch.
- Placeholder budgets: Phrase $150/day, Broad $1,500/day, Virtual $300/day.

## Still to do in Google Ads
- [ ] Keywords + ad groups (draft: Phrase 27 city ad groups / 121 kws; Broad 16 ad groups / 157 kws). Virtual keyword set TBD.
- [ ] City-name negatives on Broad
- [ ] RSAs per ad group (Virtual: virtual-only copy + online counseling LP)
- [ ] Campaign assets: image + logo (ExactMatch_Tier 1 has 16 images + logo), sitelinks/callouts come from account level
- [ ] Call asset per campaign = the CallRail "- EXT" number
- [ ] Final budgets / tCPA; observation audiences (ExactMatch_Tier 1 has 18) if wanted

## SOP checklist (per campaign x3)
- [x] (2026-11-17) Step 2: NICE ticket for 2 numbers per campaign (pool + call asset) = 6 total. Path: Request a Service > WFM Request/Issues > Nice New Phone Number. G-chat Carlos Cardona.
- [x] (2026-11-20) Marketing Channel tab: 6 rows added at rows 2706-2711 (point_of_contact = name above, state = Other, Paid Search (Nonbrand) (Search)); D resolves to "Paid Search", E = 1
- [ ] Step 3: CallRail pool (On my website > Google Ad Pool > Landing page param above), 804 area code, forward to NICE pool number (or 855-204-2767 until ready), recording ON, delete auto-text, opt out of message routing, then turn texting OFF
- [ ] CallRail support ticket: New Swap Target Bulk Request listing all 3 pools (one ticket)
- [ ] After CallRail closes ticket: set forward-to NICE number; "TBDXYZ" landing-param reset trick; QA in a fresh browser with ?utm_campaign=<ID>
- [ ] CallRail call asset: Somewhere else > Google Ads Assets, name + " - EXT"
- [ ] Online Channel Mapping tab: new row per campaign (UTM campaign = ID)
- [ ] Step 6: Paid Search Mapping sheet (one unique phone number per cell F-M)
- [ ] Step 7: CallRail Workflow branch: Landing contains utm_campaign ID > Dial NICE pool number (not EXT)
- [ ] Enable campaigns; pause ExactMatch_Tier 1 ~2 weeks later
