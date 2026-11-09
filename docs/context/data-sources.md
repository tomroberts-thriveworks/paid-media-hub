# Data sources reviewed (2026-11-09, via Google Drive connector)
Note: the connector returned tab structure and sample rows only, not full tables. Anything quantitative needs a CSV export.

## 1. EMT Dashboard (management reporting workbook) - only the SOP tab reviewed
- Nearly every data tab is updated manually (download + "drag formula"), by Diego Spaudo (backup Kaitlin; Bing backup Melanie; Marketing x BizOps x COE workbook owned by Afton Boyd).
- Weekly (Monday): GA, GA transactional traffic, GA email submissions, Trans. web traffic, Qual vs Unq calls, Qualified (no availability) calls, First-time callers [IB & OB], Paid Social reporting, All emails, TT vs Psych first bookings.
- Daily M-F: **SEM Ads** (cost downloaded from Google), **SEM Ads 2.0** (checks conversion action "Local search ad click..." present; purpose unclear), Conversion action by Day, All Calls [IB only], ROI tracker, PSG, Appts, **BING Ads** (cost downloaded from Bing).
- QA for SEM tabs: ensure BRD and NBRD campaigns show and ad cost isn't missing.
- Status-checker column showed 0 / #N/A / "52" for several weekly tabs while current week is 45 -> some tabs may be stale/broken (unverified).
- **PSG** (paid search Google granular, Looker table built by Nolan via marketing channel mapping sheet): about 90% close to trusted data. Location-asset phone numbers are shared across campaigns, so internal data cannot tie a call to a campaign. Only ONLINE bookings and WEBSITE phone calls+bookings attribute accurately by campaign.
- **Appts** (AMD = business appointment database): 10-15% of first bookings/new sessions have unknown marketing/master channel. The **ROI Tracker** re-proportions these and is the best source for bookings/new sessions by channel (has state, most channels).
- **All Calls [IB only]**: new-client calls by phone number, master/marketing channel, state.

## 2. Optimization Tracker ("TW Copy: Thriveworks Locations + Optimization Tracker") - only tab "Old, Location targeting"
- Aug-Dec 2024 history of state-level location bid adjustments and conversion value rules.
- Value rule multipliers by state moved 0.5 -> removed -> 1.05-1.25 by Dec 2024 (e.g. GA 1.15, FL/NC/TX 1.25 on 12/12/2024). Location bid adjustments were mostly removed 12/3/2024.
- UNKNOWN whether value rules are still live. Check in account; they affect reported conversion value and value-based bidding.
- Real campaign names seen: GGL_NBD_GSE_Geo_<FullStateName>, GGL_NBD_GSE_Psych_GEO_Texas, GGL_NBD_GSE_Geo_USA_Therapy_LC, GGL_NBD_GSE_Geo_USA_LC, GGL_BRD_GSE_National, GGL_NBD_GSE_Geo _USA_P_Broad_LC, GGL_NBD_GSE_Region_PsychMedication_LC. (Full state names, "Psych", "LC" suffix: parser must handle.)
- Melanie's own framing: a rough starting point, built on fractional time.

## 3. Marketing Ad Spend Decision Calculator (~40 tabs; owner taehwan@)
- Tabs: TT/NP Spending Recos (tCPA tiers "$240 TCPA" and "$205 TCPA", keyed to LTV:CAC "High L:C"), LTV Cac (All States 1.87, VA 3.32), TT & NP (headcount, brand on/off, psychiatrist present), TT Board Callout, Hiring Recos/Model, Geo Expansion Matrix, Affiliate (VeryWell tiers/CPL), Blackout for B2B, Jun-25 State Update, utilization/intake-slot/headcount/first-booking data tabs for TT and NP, PS Ad Spend Regression, State List.
- Cross-check candidates once API is live: **John's Daily Paid Report** (state x day Google Ads spend + first bookings, ~4.7k rows) and **GGL First Bookings By Service** (weekly first bookings by state, channel, tactic, ~9.5k rows).
- Discrepancies vs onboarding guide: tCPA $240/$205 vs guide $200/$250; LTV:CAC all-states 1.87 vs guide 1.99 (date/definition unknown).
