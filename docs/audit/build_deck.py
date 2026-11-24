exec(open("helpers.py").read())
def hdr_note(s,t): pass
# 1 Title
s=new(dark=True,notes="Purpose: show what's limiting the account, what's already changed, what's being implemented and tested, and get decisions. Data is pulled directly from the Google Ads API (30 days = Oct 18 to Nov 16 unless noted), plus the Google reps' analysis from their Nov 17 email.")
text(s,"Google Ads account review and plan",0.8,2.3,11.7,1.6,44,WHITE,bold=True,font=HEAD,anchor=MSO_ANCHOR.BOTTOM,name="Title")
text(s,"For Melanie and Kabir  |  Tom Roberts, Paid Media  |  November 2026",0.8,4.1,11.7,1.0,20,SAGE,name="Subtitle")
# 2 Summary
s=new(title="Efficient overall; structure is what's holding it back",notes="Headline: $820k, 3,444 Bookings*, $238 CPB over 30 days. Bookings* = Event 1 + Event 4 using Google all-conversions; not yet reconciled to the ROI tracker, and Event 4 campaign attribution is still an open question. The main message: we lose 59 to 90% of non-brand impression share to rank, not budget, and the structure (oversized ad groups, thin data) is a big part of why.")
stat(s,0.6,1.5,3.8,"$820k","Spend, last 30 days"); stat(s,4.75,1.5,3.8,"3,444","Bookings* (Event 1 + Event 4)"); stat(s,8.9,1.5,3.8,"$238","Cost per booking")
finds=[("Best keywords are buried: ","184 keywords beat target at $151 CPB but lose 78% of impressions to rank"),("Data is spread thin: ","71% of ad groups get under 5 bookings a month"),("Rank, not budget: ","non-brand loses about 75% of impressions to rank, 5% to budget"),("Office pull: ","66% of Search clicks are within 10 miles of an office"),("Leaks fixed: ","$70k a month out-of-state serving stopped Nov 16")]
for i,(a,b) in enumerate(finds):
    y=3.5+i*0.66; circle_num(s,0.6,y+0.05,i+1); text(s,[[(a,{"bold":True}),(b,{})]],1.25,y+0.05,11.4,0.45,16,anchor=MSO_ANCHOR.MIDDLE)
# 3 snapshot
s=new(title="Where the money goes: CPB by campaign",notes="Top 13 non-brand campaigns by 30-day spend. Non-brand Search 62% of spend at $262 CPB, PMax 34% at $250, brand 4.5% at $92. Two small Massachusetts campaigns run above $400 CPB but spend under $10k combined.")
camps=[("PMax Psychiatry",140.0,257),("PMax TalkTherapy V2",101.2,238),("Region PsychMedication",84.7,285),("Geo Texas",48.0,261),("Geo Florida",43.2,280),("ExactMatch Tier 1",42.4,191),("BroadMatch T3 T4",41.1,250),("PMax TalkTherapy T3 T4",37.3,259),("BroadMatch SC",31.8,275),("Geo Virginia",29.9,298),("BroadMatch NC",29.3,289),("ExactMatch Tier 2",29.3,228),("BroadMatch PA",28.5,359)]
chart(s,XL_CHART_TYPE.BAR_CLUSTERED,[f"{c[0]} (${c[1]:.0f}k)" for c in camps],[c[2] for c in camps],0.6,1.4,7.9,5.45,"Non-brand CPB, last 30 days (label: spend)",SEA,'"$"#,##0',"Chart CPB by campaign",vmax=400,vmin=0,reverse=True)
card(s,8.9,1.5,3.8,2.4); text(s,[[("Spend mix",{"bold":True})],"Non-brand Search 62%, $262 CPB","Non-brand PMax 34%, $250 CPB","Brand 4.5%, $92 CPB"],9.15,1.7,3.3,2.0,15)
card(s,8.9,4.2,3.8,2.4); text(s,[[("Best: ",{"bold":True}),("ExactMatch Tier 1 ($191) and Tier 1 Psych ($197)",{})],[("Weakest at scale: ",{"bold":True}),("BroadMatch PA ($359), Geo VA ($298)",{})]],9.15,4.4,3.3,2.0,15,space=10)
# 4 buried keywords
s=new(title="Our best keywords are buried in oversized ad groups",notes="Definition: non-brand Search keywords in ad groups with more than 20 keywords, at least 2 bidding conversions in 30 days, bidding CPA below their campaign's target, and losing at least half their impression share to rank. For ExactMatch Tier 1 and Tier 1 Psych the target is per call-based conversion ($44 and $38), so CPA is compared in those units. These 184 keywords are 12% of non-brand Search spend but 21% of its bookings. Smart Bidding sets bids per auction, so ad group size doesn't cap bids directly; the next slide shows the likely mechanism: weaker ad relevance in big ad groups lowers ad rank.")
stat(s,0.6,1.5,2.9,"184","keywords beating target",TEAL); stat(s,3.65,1.5,2.9,"$151","their CPB (vs $262 average)",SEA)
stat(s,0.6,3.3,2.9,"21%","of non-brand Search bookings",TEAL); stat(s,3.65,3.3,2.9,"78%","impressions lost to rank (median)",CORAL)
card(s,0.6,5.1,5.95,1.55); text(s,[[("Median home: ",{"bold":True}),("an ad group with 90 keywords. Median impression share: 21%.",{})]],0.85,5.3,5.45,1.2,15,anchor=MSO_ANCHOR.MIDDLE)
table(s,[["Keyword","Campaign","AG size","CPB","IS"],["therapist near me","ExactMatch T2","149","$131","10%"],["mental therapist","BroadMatch T3 T4","55","$165","29%"],["psych consult near me","Region Psych","108","$194","19%"],["find a therapist","Geo Michigan","28","$137","32%"],["therapy near me","ExactMatch T1","237","$183","10%"],["couples therapy","ExactMatch T1","90","$105","10%"],["couples counseling","ExactMatch T2","58","$115","20%"]],6.9,1.5,5.85,[1.95,1.6,0.85,0.75,0.7],"Table buried keywords",13,0.55)
text(s,"30 days, non-brand Search. AG size = enabled keywords in the ad group.",6.9,6.0,5.85,0.4,11,SLATE)
# 5 ad relevance
s=new(title="Big ad groups have weaker ad relevance, which costs rank",notes="Spend-weighted, enabled non-brand Search keywords with spend in 30 days. In ad groups of 51+ keywords, 56% of spend sits on keywords Google rates below average for ad relevance, against 22% in ad groups of 10 or fewer. One set of ads can't match 90 different keywords well. Lower ad relevance lowers Quality Score and ad rank, which is where most of our lost impression share comes from. Spend-weighted Quality Score: 6.0 (10 or fewer keywords) vs 5.5 (51+).")
chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,["10 or fewer","11-20","21-50","51+"],[22,34,21,56],0.6,1.4,7.0,5.2,"Share of spend with below-average ad relevance, by ad group size",CORAL,'0"%"',"Chart ad relevance by size",vmin=0,vmax=70)
stat(s,8.0,1.5,4.75,"62%","of non-brand Search spend sits in 38 ad groups with 20+ keywords")
stat(s,8.0,3.3,4.75,"6.0 vs 5.5","Quality Score: small vs 51+ keyword ad groups")
card(s,8.0,5.1,4.75,1.5); text(s,[[("Fix: ",{"bold":True,"color":TEAL}),("5 to 10 keywords per ad group with ads written for them.",{})]],8.25,5.3,4.25,1.1,15,anchor=MSO_ANCHOR.MIDDLE)
# 6 data spread
s=new(title="Conversion data is spread too thin",notes="Ad groups in enabled non-brand Search campaigns, 30 days. 87 ad groups had less than 1 booking and 104 had 1 to 5: 71% of ad groups, 14% of spend. Google's guidance for Target CPA bidding is roughly 15 to 30+ conversions in 30 days. That applies at the campaign or portfolio level, which our campaigns mostly meet; the bigger cost of spreading data thin is at the ad group and keyword level, where we can't test ads or read performance. 135 keywords produce half of non-brand Search bookings; 4,477 of 5,322 keywords with impressions had none. Search terms: 923 terms booked in 30 days, and 809 of them booked once or less, together 53% of bookings.")
chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,["<1","1-5","5-15","15-30","30+"],[87,104,44,18,15],0.6,1.4,6.4,5.2,"Ad groups by Bookings* in 30 days (non-brand Search)",SEA,'0',"Chart ad groups by bookings",vmin=0,vmax=120)
for i,(a,b) in enumerate([("268","non-brand Search ad groups; only 33 get 15+ bookings a month"),("135","keywords produce half of bookings; 4,477 of 5,322 have none"),("53%","of bookings come from search terms that booked once or less")]):
    y=1.5+i*1.75; card(s,7.35,y,5.4,1.55); text(s,a,7.6,y+0.15,1.6,1.25,32,TEAL,bold=True,font=HEAD,anchor=MSO_ANCHOR.MIDDLE); text(s,b,9.3,y+0.15,3.25,1.25,15,anchor=MSO_ANCHOR.MIDDLE,space=0)
# 7 rank not budget
s=new(title="We lose impressions to rank, not budget",notes="Search impression share lost to rank vs budget, last 30 days, enabled non-brand Search campaigns. Google's reps put it at about 75% lost to rank and 5% to budget across non-brand, which matches. That makes targets and ad rank (ad relevance, structure) the first lever, before adding budget. ExactMatch Tier 1's target was raised from $36 to $44; it still loses 84% to rank.")
rk=[("ExactMatch T3 T4",87,0),("ExactMatch T1 Psych",86,0),("ExactMatch T1",84,0),("ExactMatch T2",77,3),("Geo Florida",76,0),("Geo Texas",72,0),("BroadMatch PA",72,9),("BroadMatch T3 T4",70,0),("Geo Georgia",70,3),("Region Psych",68,16),("BroadMatch NC",67,10),("Geo Virginia",59,12),("BroadMatch SC",59,0)]
cd=CategoryChartData(); cd.categories=[r[0] for r in rk]; cd.add_series("Lost to rank",[r[1] for r in rk]); cd.add_series("Lost to budget",[r[2] for r in rk])
gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED,Inches(0.6),Inches(1.4),Inches(8.0),Inches(5.45),cd); gf.name="Chart lost IS"; ch=gf.chart
style_chart(ch,"Impression share lost, last 30 days (%)",TEAL,'0',vmin=0,vmax=100,labels=False)
ch.plots[0].series[1].format.fill.solid(); ch.plots[0].series[1].format.fill.fore_color.rgb=H(CORAL)
ch.category_axis.reverse_order=True; ch.has_legend=True; from pptx.enum.chart import XL_LEGEND_POSITION; ch.legend.position=XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(11)
ch.plots[0].has_data_labels=True; ch.plots[0].data_labels.font.size=Pt(10); ch.plots[0].data_labels.font.color.rgb=H(WHITE); ch.plots[0].data_labels.position=XL_LABEL_POSITION.CENTER
from lxml import etree
from pptx.oxml.ns import qn
ser=ch.plots[0].series[1]._element
dl=ser.find(qn('c:dLbls'))
if dl is None: dl=etree.SubElement(ser,qn('c:dLbls'))
for t in ('c:showLegendKey','c:showVal','c:showCatName','c:showSerName','c:showPercent','c:showBubbleSize'):
    e=etree.SubElement(dl,qn(t)); e.set('val','0')
ser.remove(dl); idx=[i for i,c in enumerate(ser) if c.tag in (qn('c:cat'),qn('c:val'))][0]; ser.insert(idx,dl)
stat(s,9.0,1.5,3.75,"~75%","lost to rank (Google reps)",CORAL); stat(s,9.0,3.3,3.75,"~5%","lost to budget",SEA)
card(s,9.0,5.1,3.75,1.6); text(s,[[("So: ",{"bold":True,"color":TEAL}),("fix ad rank and targets before adding budget.",{})]],9.25,5.3,3.25,1.2,15,anchor=MSO_ANCHOR.MIDDLE)
# 8 office
s=new(title="Google confirms spend over-indexes near offices",notes="Left stats are from the Google reps' distance report (non-brand Search). The chart is our own 90-day distance report across all non-brand (Search + PMax), which reconciles to total spend within 0.2%; the CPC levels differ from Google's because it includes PMax, but the pattern is the same. Google's explanation: Smart Bidding bids higher near offices because those users book more often, and location assets plus local competition push CPCs up. Cost per booking is close, so judge the outside-office test on CPB and keep the two campaigns geographically separate. Every enabled campaign has location assets, so we have no control group today. This may also be part of the low impression share.")
for i,(a,b) in enumerate([("66%","of non-brand Search clicks within 10 mi of an office"),("$7.17 vs $5.97","CPC near vs farther out"),("2.7% vs 2.4%","conversion rate near vs far"),("$269 vs $248","cost per booking near vs far")]):
    y=1.5+i*1.3; card(s,0.6,y,4.6,1.15); text(s,a,0.85,y+0.1,4.1,0.55,24,TEAL,bold=True,font=HEAD); text(s,b,0.85,y+0.65,4.1,0.4,13,SLATE)
text(s,"Source: Google reps' distance report, Nov 17",0.6,6.7,4.6,0.3,11,SLATE)
chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,["<1","1-5","5-10","10-15","15-20","20-25","25-30","30-35","35-40","40+"],[4.34,4.90,4.71,4.33,3.83,3.44,3.16,2.94,2.71,1.02],5.6,1.4,7.15,5.3,"Our data: CPC by miles from nearest office (90 days, all non-brand)",TEAL,'"$"0.00',"Chart CPC by distance",vmin=0,vmax=6)
# 9 out of state
s=new(title="$70k a month served outside our states (fixed)",notes="Six campaigns were set to Presence or interest: four BroadMatch campaigns and both PMax TalkTherapy campaigns. Biggest out-of-state users were in TN, NM, MD, AL and OH, mostly states the sheet has off. Change history showed no location-target edits in the window, so the leak was the setting. All enabled campaigns are now on Presence. Re-check around Nov 30.")
oos=[("BroadMatch T3 T4",16.8),("PMax TalkTherapy V2",15.2),("PMax TalkTherapy T3 T4",11.1),("PMax Psychiatry*",7.4),("BroadMatch SC",7.2),("BroadMatch PA",5.7),("BroadMatch NC",3.5)]
chart(s,XL_CHART_TYPE.BAR_CLUSTERED,[o[0] for o in oos],[o[1] for o in oos],0.6,1.4,7.4,5.0,"Spend from users outside target states, last 30 days",CORAL,'"$"0.0"k"',"Chart out-of-state spend",vmin=0,vmax=20,reverse=True)
text(s,"*PMax Psychiatry was already on Presence; its leak comes from Google's location detection.",0.6,6.45,7.4,0.4,11,SLATE)
stat(s,8.5,1.5,4.2,"$313","Out-of-state CPB vs $230 in-state",CORAL); stat(s,8.5,3.3,4.2,"9%","Of spend ($70k of $776k)",CORAL)
card(s,8.5,5.1,4.2,1.5); text(s,[[("Fixed Nov 16: ",{"bold":True}),("6 campaigns moved to Presence.",{})]],8.75,5.3,3.7,1.1,15,anchor=MSO_ANCHOR.MIDDLE)
# 10 other findings grid
s=new(title="Other findings",notes="Targeting vs the spend calculator: every state and Google column matches; the only mismatch is Demand Gen (sheet ON for NC, SC, VA, campaign paused). Campaign names don't track tiers: ExactMatch Tier 1 has IL and MI (Tier 2) and no SC. Brand: about $17k a month of brand spend is on 'thrive' terms that mostly match other practices or generic searches; they book at $90 to $190, so separate rather than pause. Bidding goals: ExactMatch Tier 1 and Tier 1 Psych bid on call-based account goals; most others on Event 1 + Event 4. Search terms: PMax top 100 terms are drug and condition lookups, 25% of impressions but 1.7% of cost.")
grid=[("Targeting vs spend calculator","Every state matches. Demand Gen is ON in the sheet for NC, SC, VA but paused. Campaign names don't follow tiers."),("Brand isn't all brand","About 40% of brand spend is on generic \"thrive\" terms that match other practices. Separate, don't pause."),("Mixed bidding goals","ExactMatch T1 and T1 Psych bid on call-based goals; most others on Event 1 + 4. Judge on Bookings* CPB."),("Search-term junk is cheap","PMax top 100 terms: 25% of impressions, 1.7% of cost. Kids and sex-therapy themes cost 2 to 3x CPB.")]
for i,(a,b) in enumerate(grid):
    x=0.6+(i%2)*6.15; y=1.5+(i//2)*2.65; card(s,x,y,5.95,2.45); circle_num(s,x+0.25,y+0.25,i+1,0.45)
    text(s,a,x+0.9,y+0.27,4.85,0.45,19,TEAL,bold=True,font=HEAD); text(s,b,x+0.9,y+0.85,4.8,1.45,15)
# 11 implementing
s=new(title="What we're implementing now",notes="These are in progress in the existing exact match campaigns, starting with Tier 1. Items 1 and 3 go straight at the buried-keyword and ad relevance findings. Item 2 cleans out keywords that don't get enough volume to justify their own exact slot. Item 4 is the Tier 1 rebuild on the next slides.")
impl=[("Top search terms into their own ad groups","In the exact match campaigns, so proven terms get their own ads and budget"),("Low-volume exact keywords out of exact campaigns","Let broad and phrase pick them up instead of thinning exact"),("5 to 10 keywords per ad group","Tighter ad relevance and cleaner data"),("Exact / phrase / broad campaign variations","Starting with Tier 1 talk therapy")]
for i,(a,b) in enumerate(impl):
    x=0.6+(i%2)*6.15; y=1.5+(i//2)*2.65; card(s,x,y,5.95,2.45); circle_num(s,x+0.25,y+0.25,i+1,0.45,TEAL)
    text(s,a,x+0.9,y+0.27,4.85,0.9,19,TEAL,bold=True,font=HEAD); text(s,b,x+0.9,y+1.2,4.8,1.1,15,SLATE)
# 12 tests
s=new(title="Tests we want to run",notes="Each test answers one question and should run with separate geographies or a Google experiment, so campaigns don't bid against each other. Inefficient-state candidates on 30-day CPB: BroadMatch PA $359, the two Massachusetts campaigns $409 to $473, Geo Virginia $298. Brand on manual CPC: brand books at $92 CPB on Maximize Conversions; manual CPC tests whether we're overpaying for our own name.")
table(s,[["Test","Question it answers","Status"],["Office vs away-from-office","Do location assets and office proximity drive cost? (Tier 1 Virtual)","Built, paused"],["State vs multi-state","Do state campaigns beat a multi-state campaign with the same keywords?","To design"],["PMax vs broad / phrase","PMax runs on Search only: does a broad or phrase Search campaign do better?","To design"],["Brand on manual CPC","Are we overpaying for our own name on Maximize Conversions?","To design"],["Inefficient states on their own","Can PA, MA and VA get to target in their own campaigns?","To design"],["Match type variations","Exact vs phrase vs broad, starting with Tier 1","Built, paused"]],0.6,1.5,12.15,[3.2,7.0,1.95],"Table tests",15,0.7)
# 13 tier 1 plan
s=new(title="Tier 1 rebuild: three campaigns plus an office test",notes="Campaign IDs: Phrase 24470038974, Broad 24470038980, Virtual 24470038992. All paused. Built: 9 Tier 1 states by Presence, Search only, English, ExactMatch Tier 1 ad schedule, same 12 shared negative lists. Budgets are placeholders. Proposed geography: Broad and Phrase in the 91 Tier 1 counties with an office, Virtual in the other 712 with no location assets, so the two sides don't overlap. One gap: the account-level static location group can't be excluded on Virtual through the API; confirm with Google.")
for i,(n,a,b,c) in enumerate([("Phrase","City searches","121 phrase keywords in 27 city ad groups","Office counties, with location assets"),("Broad","Service searches near offices","157 broad keywords in 16 ad groups","91 office counties (75% of Tier 1 spend, $251 CPB)"),("Virtual","Same searches, away from offices","Same keywords as Broad","712 non-office counties (25%, $242 CPB), no location assets")]):
    x=0.6+i*4.1; card(s,x,1.5,3.9,3.9,MINT if i==2 else PALE)
    text(s,n,x+0.25,1.7,3.4,0.6,26,SEA if i==2 else TEAL,bold=True,font=HEAD); text(s,a,x+0.25,2.35,3.4,0.5,16,bold=True)
    text(s,[b,c],x+0.25,2.95,3.4,2.3,14,bullets=True,space=8)
card(s,0.6,5.65,12.15,1.05,ROSE); text(s,[[("Why counties: ",{"bold":True,"color":CORAL}),("Google can't exclude a radius. Near and far don't overlap, so the campaigns don't compete with each other. State campaigns keep running across both areas.",{})]],0.9,5.75,11.6,0.85,15,anchor=MSO_ANCHOR.MIDDLE)
# 14 launch
s=new(title="Launch steps and how we'll judge it",notes="Launch follows the Paid Search Campaign Launch SOP: a NICE pool number and call-asset number per campaign, a CallRail pool keyed on utm_campaign = campaign ID, an EXT number, one shared swap-target ticket, mapping sheet rows and a workflow branch.")
for i,(a,b,done) in enumerate([("Campaigns built (paused)","Nov 17",True),("NICE numbers requested (6)","Nov 17",True),("Mapping sheet rows","Next",False),("CallRail pools, EXT, swap ticket","1-2 business days",False),("Workflow + QA","After swaps",False),("Launch, then pause ExactMatch T1","About 2 weeks later",False)]):
    x=0.6+i*2.05; card(s,x,1.6,1.9,1.9,TEAL if done else PALE,name=f"Step {i+1}")
    text(s,str(i+1),x+0.15,1.72,1.6,0.45,20,WHITE if done else TEAL,bold=True,font=HEAD); text(s,a,x+0.15,2.2,1.6,0.85,13,WHITE if done else INK,bold=True,space=0); text(s,b,x+0.15,3.05,1.6,0.4,12,SAGE if done else SLATE)
text(s,"How we'll judge it (read at 2 and 4 weeks)",0.6,3.95,12.1,0.5,20,TEAL,bold=True,font=HEAD)
for i,(a,b) in enumerate([("Bookings* CPB","By campaign, and combined with the state campaigns"),("Near vs far","CPC, conversion rate and CPB with and without location assets"),("Coverage","IL and MI lose exact match when ExactMatch Tier 1 pauses")]):
    x=0.6+i*4.1; card(s,x,4.6,3.9,1.95); text(s,[[(a,{"bold":True})],b],x+0.25,4.8,3.4,1.6,15)
# 15 changes
s=new(title="What's already changed",notes="All account changes were approved by Tom before they were made. Location targeting and negatives were changed through the API; the brand ad group, the ExactMatch Tier 1 target and the search-term breakouts were done by Tom in the UI.")
ln=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(1.55),Inches(1.75),Inches(1.55),Inches(6.4)); ln.line.color.rgb=H(SAGE); ln.line.width=Pt(2); ln.name="Timeline line"
for i,(d,a,b) in enumerate([("Nov 13","New shared negative list on all campaigns","kid, kids, sex, plus 5 sex-therapy phrases"),("Nov 13","thriveworks exact in its own ad group","Cleaner brand structure"),("Nov 16","6 campaigns switched to Presence","Stops about $70k a month of out-of-state serving"),("Nov 17","3 Tier 1 campaigns created, paused","Tier 1 rebuild plus office test"),("Ongoing","Top search terms broken out into ad groups","ExactMatch Tier 1 target raised from $36 to $44")]):
    y=1.5+i*1.0; o=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(1.4),Inches(y+0.17),Inches(0.3),Inches(0.3)); o.fill.solid(); o.fill.fore_color.rgb=H(SEA); o.line.color.rgb=H(WHITE); o.shadow.inherit=False; o.name=f"Dot {i+1}"
    text(s,d,0.3,y+0.17,1.0,0.35,14,SLATE,bold=True,align=PP_ALIGN.RIGHT); text(s,a,2.0,y+0.05,10.6,0.45,18,bold=True); text(s,b,2.0,y+0.5,10.6,0.4,14,SLATE)
# 16 decisions
s=new(dark=True,notes="Items 1 and 2 block the final build of the Tier 1 campaigns. Item 3 sets their budgets and targets. Item 4 decides which tests run first. The rest can follow.")
text(s,"Decisions we need from this group",0.8,0.5,11.7,1.0,36,WHITE,bold=True,font=HEAD,anchor=MSO_ANCHOR.MIDDLE,name="Title")
text(s,["Bidding goal for the new campaigns: Event 1 + 4 everywhere, or keep account goals on Broad?","Office test: county split, or city level?","Current tCPA ceilings ($240/$205 vs $200/$250) and LTV:CAC (1.87 vs 1.99)","Test priority: which of the five tests run first?","Brand \"thrive\" terms: separate ad group, or move to non-brand?","Demand Gen: turn on for NC, SC, VA, or update the sheet?","Event 4 attribution by campaign (Diego / Anfernee)","Kids and sex therapy: minimum age and clinician coverage before any test"],0.8,1.7,11.8,5.2,18,WHITE,numbered=True,space=10)
prs.core_properties.title="Google Ads account review and plan"; prs.core_properties.author="Tom Roberts"
lst=prs.slides._sldIdLst; ids=list(lst); el=ids[14]; lst.remove(el); lst.insert(10,el)
for i,sl in enumerate(prs.slides,1):
    for sh in sl.shapes:
        if sh.name=="Slide number": sh.text_frame.paragraphs[0].runs[0].text=str(i)
prs.save("google-ads-review-nov-2026-v2.pptx"); print("saved",state["n"])
