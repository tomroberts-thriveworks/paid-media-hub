# Google Ads account review and plan

**Prepared for:** Melanie, Kabir
**Prepared by:** Tom Roberts (Paid Media)
**Account:** Thriveworks Google Ads (689-013-0035)
**Status:** Draft, November 17, 2026

## Summary

The account spent **$820k in the last 30 days for 3,444 Bookings\*, a $238 CPB**. Non-brand Search is 62% of spend at $262 CPB, non-brand PMax 34% at $250, and brand 4.5% at $92.

The structure matches the spend calculator sheet state by state. The problems are in how campaigns are built inside that structure:

1. **About $70k a month was serving outside our target states**, at a $313 CPB against $230 in-state. This came from a location setting on six campaigns. **Fixed November 16.**
2. **Spend concentrates around offices.** 71% of non-brand spend is within 10 miles of an office, and CPCs there are about double ($4.90 vs. $2.71 at 35–40 miles). CPB is flat by distance, so near-office clicks aren't worse, but every campaign has location assets, so we have never seen the account without them. **A Tier 1 test is being built to measure this.**
3. **Campaigns bid on different goals.** Our best non-brand campaign, ExactMatch Tier 1 ($191 CPB), bids on call-based account goals. Most others bid on Event 1 + Event 4. That is worth understanding before we standardize.
4. **Brand isn't all brand.** About 40% of brand spend is on "thrive …" keywords that mostly match other practices or generic searches. That flatters brand CPB and hides non-brand cost.
5. **ExactMatch Tier 1 is overbuilt.** It has 801 enabled keywords, but 190 of them carry about 80% of spend and bookings. Four couples/relationship keywords spent $24.5k in 90 days for 4.5 Bookings\*.

**The plan:** rebuild Tier 1 talk therapy as three new campaigns (Phrase, Broad, and an away-from-offices test), keep the state campaigns for volume, and keep cleaning up negatives and brand.

## Scope and definitions

- **Data:** Google Ads API, read directly. 30-day figures are Oct 18 – Nov 16, 2026 unless noted. Some analyses use 90 days (Aug 19 – Nov 16) for volume.
- **Bookings\*:** Event 1 + Event 4, using Google's all-conversions counts. **CPB:** spend ÷ Bookings\*. Campaigns that bid on proxy goals (calls) are judged on Bookings\*, not on their own conversion counts.
- **"Tier":** the supply tier from the Marketing Ad Spend Decision Calculator (TT Spending Recos / NP Spending Recos tabs), not a goal type. Talk therapy Tier 1 is FL, GA, MA, NC, NJ, PA, SC, TX, VA.
- **Caveats:**
  - These are Google-attributed Bookings\*. They haven't been reconciled to the ROI tracker or AMD.
  - How Event 4 is assigned to a campaign, given shared location-asset phone numbers, is still an open question.
  - Microsoft, Meta, ChatGPT and ZocDoc aren't covered yet.
- **Data handling:** aggregate ad data only. No patient-level data was used.

## Account snapshot (last 30 days)

| Area | Campaigns | Spend | Share | Bookings\* | CPB |
|---|---|---|---|---|---|
| Non-brand Search | 17 | $504k | 61.5% | 1,923 | $262 |
| Non-brand PMax | 3 | $278k | 34.0% | 1,115 | $250 |
| Brand Search | 1 | $37k | 4.5% | 406 | $92 |
| **Total** | **21** | **$820k** | | **3,444** | **$238** |

Best non-brand CPB: ExactMatch Tier 1 ($191) and ExactMatch Tier 1 Psych ($197).
Weakest at scale: BroadMatch Tier 1 Pennsylvania ($359), Geo Virginia ($298) and ExactMatch Tier 3 Tier 4 ($299). Two small Massachusetts campaigns are above $400.

## Findings

### 1. Campaign structure vs. the spend calculator
- **Targeting matches the sheet in every state** for Google broad, PMax, exact, brand and psychiatry columns. No state is on where the sheet says off, or the reverse.
- **One mismatch:** the sheet has TalkTherapy Demand Gen ON for NC, SC and VA. The only Demand Gen campaign is paused.
- **Campaign names don't follow the tiers.** ExactMatch Tier 1 includes IL and MI (TT Tier 2) and leaves out SC (Tier 1). SC's exact match runs in ExactMatch Tier 2. PMax TalkTherapy V2 is Tier 1 minus MA and PA, plus CT. This makes reporting by tier unreliable.

### 2. Out-of-state serving (fixed)
- Six campaigns were set to "Presence or interest", which also shows ads to people outside the target states: four BroadMatch campaigns and both PMax TalkTherapy campaigns.
- Over 30 days, **$70k of $776k (9%)** went to users outside target states, at a **$313 CPB vs. $230 in-state**. The largest amounts were in TN, NM, MD, AL and OH, states the sheet has off or paused for that channel.
- No location targets were changed in that period, so the leak was the setting, not old targeting.
- **Action (Nov 16):** all six switched to "Presence". Every enabled campaign is now on Presence. Re-check around Nov 30.

### 3. Spend concentration around offices
- **Distance from the nearest office (90 days, non-brand):** 41% of spend within 5 miles, 71% within 10, 98% within 40.
- **Office cities:** 262 cities with an office (2% of cities with spend) take 45% of spend.
- **Tier 1 counties:** the 91 counties with an office take 75% of Tier 1 spend.
- **CPC falls with distance:** $4.90 at 1–5 miles, $3.44 at 20–25 miles, $2.71 at 35–40 miles. **CPB is flat at $245–$273 in every distance band**, and also by city size.
- **What this means:** bidding pays more near offices because those clicks convert better, so efficiency holds. What we can't tell is whether near-office bookings are incremental, or whether location assets are what's driving the concentration. **Every enabled campaign has location assets attached**, so there's no comparison group in the account.
- **Next step:** the Tier 1 test below. Questions sent to the Google rep (Nov 17 call); answers pending.

### 4. Bidding goals are inconsistent
- **ExactMatch Tier 1 and ExactMatch Tier 1 Psych** bid on account-level goals: mostly CallRail local click-to-calls (about 11k a month), phone calls and Event 1. Most other campaigns bid on the "Event 1 & Event 4" custom goal.
- ExactMatch Tier 1 has the best CPB on Bookings\* ($191 over 30 days). Its Event 4 share is 71%, in line with other campaigns, so the result isn't inflated by call credit.
- **Risk:** a call-goal campaign can buy cheap calls that don't book. Any target change on these campaigns should be judged on Bookings\* CPB, not in-platform CPA.

### 5. Search terms and negatives
- **PMax:** the top 100 search terms by impressions are mostly medication and condition lookups ("vyvanse", "lexapro side effects", "stages of grief"). They are 25% of PMax impressions but only 1.7% of PMax cost, and book at $181 CPB. Negating them cleans up impressions, not budget.
- **Themes losing money across the account (90 days):**
  - Sex therapy: $2.7k at $596 CPB.
  - "Kids"-type searches: about $4.2k at about $644 CPB.
  - Other practices' names: $6.4k at $454 CPB.
  - "In my area": $1.1k, 0 Bookings\*.
- **Action (Nov 13):** new shared list "All campaigns (potential future test)", attached to 89 of 90 campaigns. Broad `kid`, `kids`, `sex`, plus phrase sex-therapy terms. Kids and sex therapy are noted as candidates for a separate test later rather than permanent exclusions.
- **Pending:**
  - Informational phrases (`side effects`, `vs`, `uses`, `what are`…), with `what is` on PMax only, because it blocks booking Search terms.
  - Competitor names leaking into PMax (blue umbrella psychiatry $242, emerald psychiatry $225).
  - Bare drug names are deliberately kept: $156 CPB in PMax.
- **Housekeeping:**
  - The account-level negative list is empty.
  - "GGL_NBD_PMAX_TalkTherapy | Universal Keyword Negative" (756 terms) isn't attached anywhere. It contains phrase `therapy` and `therapist`, so it shouldn't be attached as it stands.

### 6. Brand
- 30-day brand spend: $37k, 406 Bookings\*, $92 CPB. `thriveworks` alone is about 40% of brand spend and 47% of brand bookings.
- **About $17k over 30 days sits on "thrive …" keywords** that don't contain "thriveworks":
  - Broad keywords (`thriving counseling`, `thrive marriage counseling`, `thriveworks couples therapy`) match generic searches such as "therapy near me".
  - Exact keywords (`thrive counseling`, `thrive therapy`) mostly match other practices with those names.
  - These have 10–17% impression share and about 5% CTR, against 92% and 36% for `thriveworks`.
- They still book at about $90–$190 CPB, so the recommendation is to separate them, not pause them. Brand reporting should reflect real brand demand.
- **Action (Nov 13):** `thriveworks` exact moved into its own ad group. The old duplicate should be paused.

### 7. ExactMatch Tier 1 keyword build
- 801 enabled keywords (plus about 1,550 paused). The top 190 carry about 80% of spend and 79% of bookings.
- The long tail (611 keywords) still books at about the same CPB, so moving it is a structure decision, not a savings play.
- **Four couples/relationship keywords:** $24.5k in 90 days for 4.5 Bookings\*. "relationship counseling near me" alone is $12.9k for 2. Similar keywords ("couples therapy near me", "marriage counseling") book normally.
- **In progress (Tom):** breaking the top search terms out into their own ad groups.

## Changes made so far

| Date | Change | Why |
|---|---|---|
| Nov 13 | New shared negative list "All campaigns (potential future test)": kid/kids/sex (broad) + 5 sex-therapy phrases, attached to all campaigns | Long-tail themes at 2–3× CPB |
| Nov 13 | `thriveworks` exact moved to its own brand ad group | Clean brand structure |
| Nov 16 | 6 campaigns switched from "Presence or interest" to "Presence" | $70k/30d serving outside target states |
| Nov 17 | 3 Tier 1 campaigns created, paused (below) | Tier 1 rebuild + office test |
| Ongoing | Top search terms broken out into exact ad groups | Concentrate budget on proven terms |

## Plan: Tier 1 talk therapy rebuild

Three new campaigns sit alongside the state campaigns. The state campaigns stay for volume.

| Campaign | ID | Role | Keywords |
|---|---|---|---|
| GGL_NBD_GSE_Tier 1_TalkTherapy_Phrase | 24470038974 | City/location searches | 121 phrase keywords in 27 city ad groups |
| GGL_NBD_GSE_Tier 1_TalkTherapy_Broad | 24470038980 | Service/specialty searches near offices | 157 broad keywords in 16 ad groups |
| GGL_NBD_GSE_Tier 1_TalkTherapy_Virtual | 24470038992 | Same searches, away from offices, no location assets | Same as Broad (proposed) |

**Built so far (all paused):**
- 9 Tier 1 states, by Presence.
- Search only, English.
- Ad schedule copied from ExactMatch Tier 1.
- The same 12 shared negative lists.
- Phrase and Broad carry the office location group.
- Virtual has no location group and excludes the account-level Business Profile locations.
- Budgets are placeholders.

**Office test design (proposed):**
- Broad and Phrase target the 91 Tier 1 counties with an office. These were 75% of Tier 1 spend, at $251 CPB.
- Virtual targets the other 712 counties (25% of spend, $242 CPB), with no location assets.
- Google can't exclude a radius, so counties are the closest workable unit.
- Because the two sides don't overlap, the campaigns don't compete with each other, and we get a clean near-vs-far read on CPC, conversion rate and CPB. The state campaigns still run across both areas.

**Launch steps (per the paid search launch SOP):**
- NICE numbers requested Nov 17: 6 numbers, a pool number and a call-asset number per campaign.
- Next: Marketing Channel mapping rows, CallRail pools and EXT numbers, the CallRail swap-target ticket (1–2 business days), Online Channel and Paid Search mapping rows, the CallRail workflow, then QA.
- After launch: pause ExactMatch Tier 1 after about 2 weeks of overlap.
- **Coverage note:** IL and MI lose exact-match coverage when ExactMatch Tier 1 is paused. IL has no other talk therapy coverage.

**How we'll judge it:**
- Bookings\* CPB by campaign, and combined with the state campaigns.
- Near-vs-far CPC and CPB.
- Out-of-state share after the Presence fix.
- Read at 2 and 4 weeks.

## Decisions and questions for this group

1. **Bidding goal for the new campaigns:** use Event 1 & Event 4 on both Broad and Virtual (a clean test), or keep account goals on Broad (what makes ExactMatch Tier 1 efficient)?
2. **Office test unit:** county split as proposed, or city level?
3. **Budgets and tCPA ceilings:** the sheet shows $240/$205, earlier guidance said $200/$250. Which is current, and what's the current LTV:CAC (1.87 vs. 1.99)?
4. **Brand "thrive …" keywords:** move to a separate ambiguous-brand ad group, or into non-brand?
5. **Demand Gen:** turn on per the sheet (NC, SC, VA), or update the sheet?
6. **SC and IL/MI:** align ExactMatch campaign states with the tiers in the sheet?
7. **Event 4 attribution:** how Event 4 is credited to campaigns, which determines how far we can trust campaign-level Bookings\*. Question for Diego / Anfernee.
8. **Kids and sex therapy:** minimum client age and clinician coverage, before any separate test.
