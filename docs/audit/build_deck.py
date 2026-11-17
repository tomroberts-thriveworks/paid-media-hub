from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_MARKER_STYLE
import copy
H=lambda h: RGBColor.from_string(h)
TEAL,SEA,CORAL,SAGE,SLATE,INK,PALE,WHITE,ROSE,MINT="0F4C5C","5FA8A0","E07A5F","9DB8B4","3D6B73","1F2A30","EEF4F3","FFFFFF","FBEAE5","E6F1EF"
HEAD,BODY="Cambria","Calibri"
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BLANK=prs.slide_layouts[6]
state={"n":0}
def new(dark=False,title=None,notes=""):
    s=prs.slides.add_slide(BLANK); state["n"]+=1
    bg=s.background.fill; bg.solid(); bg.fore_color.rgb=H(TEAL if dark else WHITE)
    if not dark:
        if title: text(s,title,0.6,0.35,12.1,0.9,32,TEAL,bold=True,font=HEAD,anchor=MSO_ANCHOR.MIDDLE,name="Title")
        text(s,"Google Ads review | Nov 2026 | Draft",0.6,7.0,6,0.3,10,SLATE,name="Footer")
        text(s,str(state["n"]),12.2,7.0,0.6,0.3,10,SLATE,align=PP_ALIGN.RIGHT,name="Slide number")
    if notes: s.notes_slide.notes_text_frame.text=notes
    return s
def text(s,content,x,y,w,h,size=16,color=INK,bold=False,font=BODY,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,name=None,bullets=False,space=6,numbered=False):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(tf,m,0)
    tf.vertical_anchor=anchor
    if name: tb.name=name
    paras=content if isinstance(content,list) else [content]
    for i,p in enumerate(paras):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        para.alignment=align; para.space_after=Pt(space)
        runs=p if isinstance(p,tuple) else ((p,{}),) if isinstance(p,str) else p
        if isinstance(p,str): runs=[(p,{})]
        for t,o in runs:
            r=para.add_run(); r.text=t; f=r.font; f.size=Pt(o.get("size",size)); f.bold=o.get("bold",bold); f.name=o.get("font",font); f.color.rgb=H(o.get("color",color))
        if bullets or numbered:
            pPr=para._p.get_or_add_pPr(); pPr.set("marL",str(Emu(Inches(0.3)))); pPr.set("indent",str(-Emu(Inches(0.3))))
            from pptx.oxml.ns import qn
            from lxml import etree
            if numbered:
                b=etree.SubElement(pPr,qn("a:buAutoNum")); b.set("type","arabicPeriod")
            else:
                b=etree.SubElement(pPr,qn("a:buChar")); b.set("char","•")
    return tb
def card(s,x,y,w,h,fill=PALE,name="Card"):
    sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h)); sh.adjustments[0]=0.06
    sh.fill.solid(); sh.fill.fore_color.rgb=H(fill); sh.line.fill.background(); sh.shadow.inherit=False; sh.name=name; return sh
def stat(s,x,y,w,big,label,color=TEAL):
    card(s,x,y,w,1.6,name="Stat "+label)
    text(s,big,x+0.25,y+0.15,w-0.5,0.8,40,color,bold=True,font=HEAD)
    text(s,label,x+0.25,y+1.0,w-0.5,0.5,14,SLATE)
def style_chart(ch,title,color,fmt,vmax=None,vmin=None,labels=True):
    ch.has_legend=False; ch.has_title=True
    ch.chart_title.text_frame.text=title
    tp=ch.chart_title.text_frame.paragraphs[0]; tp.runs[0].font.size=Pt(14); tp.runs[0].font.bold=True; tp.runs[0].font.name=BODY; tp.runs[0].font.color.rgb=H(INK)
    ch.font.size=Pt(11); ch.font.name=BODY; ch.font.color.rgb=H(SLATE)
    va=ch.value_axis; va.has_major_gridlines=True; va.major_gridlines.format.line.color.rgb=H("E3E8E7"); va.major_gridlines.format.line.width=Pt(0.5)
    va.tick_labels.number_format=fmt; va.tick_labels.number_format_is_linked=False; va.format.line.fill.background()
    if vmax is not None: va.maximum_scale=vmax
    if vmin is not None: va.minimum_scale=vmin
    ch.category_axis.format.line.color.rgb=H("C9D3D1"); ch.category_axis.has_major_gridlines=False
    pl=ch.plots[0]
    for ser in pl.series:
        if ch.chart_type in (XL_CHART_TYPE.LINE_MARKERS,):
            ser.format.line.color.rgb=H(color); ser.format.line.width=Pt(3); ser.smooth=False
            ser.marker.style=XL_MARKER_STYLE.CIRCLE; ser.marker.size=8; ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb=H(color); ser.marker.format.line.color.rgb=H(color)
        else:
            ser.format.fill.solid(); ser.format.fill.fore_color.rgb=H(color)
    if labels:
        pl.has_data_labels=True; dl=pl.data_labels; dl.number_format=fmt; dl.number_format_is_linked=False; dl.font.size=Pt(11); dl.font.color.rgb=H(INK); dl.font.name=BODY
        dl.position=XL_LABEL_POSITION.ABOVE if ch.chart_type==XL_CHART_TYPE.LINE_MARKERS else XL_LABEL_POSITION.OUTSIDE_END
    try: pl.gap_width=60
    except Exception: pass
def chart(s,kind,cats,vals,x,y,w,h,title,color,fmt,name,vmax=None,vmin=None,reverse=False):
    cd=CategoryChartData(); cd.categories=cats; cd.add_series("S",vals)
    gf=s.shapes.add_chart(kind,Inches(x),Inches(y),Inches(w),Inches(h),cd); gf.name=name; ch=gf.chart
    style_chart(ch,title,color,fmt,vmax,vmin)
    if reverse: ch.category_axis.reverse_order=True
    return ch
def table(s,rows,x,y,w,colw,name,size=14,rowh=0.5):
    gf=s.shapes.add_table(len(rows),len(rows[0]),Inches(x),Inches(y),Inches(w),Inches(rowh*len(rows))); gf.name=name; t=gf.table
    for j,cw in enumerate(colw): t.columns[j].width=Inches(cw)
    for i,r in enumerate(rows):
        t.rows[i].height=Inches(rowh)
        for j,v in enumerate(r):
            c=t.cell(i,j); c.text=v; c.margin_left=c.margin_right=Inches(0.1)
            c.fill.solid(); c.fill.fore_color.rgb=H(TEAL if i==0 else (WHITE if i%2 else PALE))
            for p in c.text_frame.paragraphs:
                for rr in p.runs: rr.font.size=Pt(size); rr.font.name=BODY; rr.font.bold=(i==0); rr.font.color.rgb=H(WHITE if i==0 else INK)
            c.vertical_anchor=MSO_ANCHOR.MIDDLE
    return t
def circle_num(s,x,y,n,d=0.42,fill=SEA):
    o=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(y),Inches(d),Inches(d)); o.fill.solid(); o.fill.fore_color.rgb=H(fill); o.line.fill.background(); o.shadow.inherit=False; o.name=f"Number {n}"
    tf=o.text_frame; tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0; p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER; r=p.add_run(); r.text=str(n); r.font.size=Pt(14); r.font.bold=True; r.font.color.rgb=H(WHITE); r.font.name=BODY; tf.vertical_anchor=MSO_ANCHOR.MIDDLE

# 1
s=new(dark=True,notes="Purpose: walk through what the account review found, what has already changed, and the Tier 1 rebuild plan, then get decisions on the open items at the end. Data comes directly from the Google Ads API; the 30-day window is Oct 18 to Nov 16 unless noted.")
text(s,"Google Ads account review and plan",0.8,2.3,11.7,1.6,44,WHITE,bold=True,font=HEAD,anchor=MSO_ANCHOR.BOTTOM,name="Title")
text(s,"For Melanie and Kabir  |  Tom Roberts, Paid Media  |  November 2026",0.8,4.1,11.7,1.0,20,SAGE,name="Subtitle")
# 2
s=new(title="Account is efficient overall, with fixable leaks",notes="Headline: $820k, 3,444 Bookings*, $238 CPB over 30 days. Non-brand Search is 62% of spend at $262 CPB, non-brand PMax 34% at $250, brand 4.5% at $92. Bookings* = Event 1 + Event 4 using Google all-conversions; not yet reconciled to the ROI tracker, and Event 4 campaign attribution is still an open question.")
stat(s,0.6,1.5,3.8,"$820k","Spend, last 30 days"); stat(s,4.75,1.5,3.8,"3,444","Bookings* (Event 1 + Event 4)"); stat(s,8.9,1.5,3.8,"$238","Cost per booking")
finds=[("Out-of-state serving: ","$70k a month at $313 CPB. Fixed Nov 16"),("Office concentration: ","71% of spend within 10 miles of an office. Test built"),("Mixed bidding goals: ","best campaign bids on calls, most bid on bookings"),("Brand isn't all brand: ","about 40% of brand spend is generic \"thrive\" terms"),("ExactMatch Tier 1 overbuilt: ","801 keywords, 190 do about 80% of the work")]
for i,(a,b) in enumerate(finds):
    y=3.5+i*0.66; circle_num(s,0.6,y+0.05,i+1); text(s,[[(a,{"bold":True}),(b,{})]],1.25,y+0.05,11.4,0.45,16,anchor=MSO_ANCHOR.MIDDLE)
# 3
s=new(title="Where the money goes: CPB by campaign",notes="Top 13 non-brand campaigns by 30-day spend. Two small Massachusetts campaigns (BroadMatch Tier 1 MA and Geo MA) run above $400 CPB but spend under $10k combined. Brand: $37k, 406 Bookings*, $92 CPB.")
camps=[("PMax Psychiatry",140.0,257),("PMax TalkTherapy V2",101.2,238),("Region PsychMedication",84.7,285),("Geo Texas",48.0,261),("Geo Florida",43.2,280),("ExactMatch Tier 1",42.4,191),("BroadMatch T3 T4",41.1,250),("PMax TalkTherapy T3 T4",37.3,259),("BroadMatch SC",31.8,275),("Geo Virginia",29.9,298),("BroadMatch NC",29.3,289),("ExactMatch Tier 2",29.3,228),("BroadMatch PA",28.5,359)]
chart(s,XL_CHART_TYPE.BAR_CLUSTERED,[f"{c[0]} (${c[1]:.0f}k)" for c in camps],[c[2] for c in camps],0.6,1.4,7.9,5.45,"Non-brand CPB, last 30 days (label: spend)",SEA,'"$"#,##0',"Chart CPB by campaign",vmax=400,vmin=0,reverse=True)
card(s,8.9,1.5,3.8,2.4); text(s,[[("Spend mix",{"bold":True})],"Non-brand Search 62%, $262 CPB","Non-brand PMax 34%, $250 CPB","Brand 4.5%, $92 CPB"],9.15,1.7,3.3,2.0,15)
card(s,8.9,4.2,3.8,2.4); text(s,[[("Best: ",{"bold":True}),("ExactMatch Tier 1 ($191) and Tier 1 Psych ($197)",{})],[("Weakest at scale: ",{"bold":True}),("BroadMatch PA ($359), Geo VA ($298)",{})]],9.15,4.4,3.3,2.0,15,space=10)
# 4
s=new(title="Targeting matches the spend calculator; names don't",notes="Checked every state and channel in the TT and NP Spending Recos tabs against enabled campaigns that spent in the last 7 days. The routing is right; the campaign names just don't track tiers, which makes tier-level reporting unreliable.")
card(s,0.6,1.5,5.9,5.1); text(s,"Matches the sheet",0.9,1.75,5.3,0.5,22,TEAL,bold=True,font=HEAD)
text(s,["Every state, every Google column: broad, PMax, exact, brand, psychiatry","No state on where the sheet says off, or the reverse","Brand targets the sheet's 27 states"],0.9,2.45,5.3,3.9,16,bullets=True,space=10)
card(s,6.85,1.5,5.9,5.1,ROSE); text(s,"Doesn't line up",7.15,1.75,5.3,0.5,22,CORAL,bold=True,font=HEAD)
text(s,["Demand Gen: sheet says ON for NC, SC, VA; the campaign is paused","ExactMatch Tier 1 includes IL and MI (Tier 2) and leaves out SC (Tier 1)","SC exact match runs in ExactMatch Tier 2","PMax TalkTherapy V2 is Tier 1 minus MA and PA, plus CT"],7.15,2.45,5.3,3.9,16,bullets=True,space=10)
# 5
s=new(title="$70k a month served outside our states (fixed)",notes="Six campaigns were set to Presence or interest: four BroadMatch campaigns and both PMax TalkTherapy campaigns. Biggest out-of-state users were in TN, NM, MD, AL and OH, mostly states the sheet has off. Change history showed no location-target edits in the window, so the leak was the setting. All enabled campaigns are now on Presence.")
oos=[("BroadMatch T3 T4",16.8),("PMax TalkTherapy V2",15.2),("PMax TalkTherapy T3 T4",11.1),("PMax Psychiatry*",7.4),("BroadMatch SC",7.2),("BroadMatch PA",5.7),("BroadMatch NC",3.5)]
chart(s,XL_CHART_TYPE.BAR_CLUSTERED,[o[0] for o in oos],[o[1] for o in oos],0.6,1.4,7.4,5.0,"Spend from users outside target states, last 30 days",CORAL,'"$"0.0"k"',"Chart out-of-state spend",vmin=0,vmax=20,reverse=True)
text(s,"*PMax Psychiatry was already on Presence; its leak comes from Google's location detection.",0.6,6.45,7.4,0.4,11,SLATE)
stat(s,8.5,1.5,4.2,"$313","Out-of-state CPB vs $230 in-state",CORAL); stat(s,8.5,3.3,4.2,"9%","Of spend ($70k of $776k)",CORAL)
card(s,8.5,5.1,4.2,1.5); text(s,[[("Fixed Nov 16: ",{"bold":True}),("6 campaigns moved to Presence. Re-check around Nov 30.",{})]],8.75,5.3,3.7,1.1,15)
# 6
s=new(title="Spend piles up near offices; efficiency doesn't change",notes="90-day non-brand distance report, which reconciles to total spend within 0.2%. Bidding pays nearly twice as much per click within 5 miles as at 35 to 40 miles, because those clicks convert better; CPB ends up flat at about $260. Open questions: are near-office bookings incremental, and are location assets driving the concentration? Questions are with the Google rep.")
dl=["<1","1-5","5-10","10-15","15-20","20-25","25-30","30-35","35-40","40+"]
chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,dl,[4.34,4.90,4.71,4.33,3.83,3.44,3.16,2.94,2.71,1.02],0.6,1.4,6.0,3.9,"CPC by miles from nearest office",TEAL,'"$"0.00',"Chart CPC by distance",vmin=0,vmax=6)
chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,dl,[271,256,261,257,268,245,225,273,253,266],6.75,1.4,6.0,3.9,"CPB by miles from nearest office",SEA,'"$"0',"Chart CPB by distance",vmin=0,vmax=350)
for i,(a,b) in enumerate([("71%","of spend within 10 miles of an office"),("45%","of spend in the 262 office cities (2% of cities)"),("100%","of campaigns have location assets: no control group")]):
    x=0.6+i*4.15; card(s,x,5.5,3.95,1.3); text(s,a,x+0.2,5.6,1.55,1.1,30,TEAL,bold=True,font=HEAD,anchor=MSO_ANCHOR.MIDDLE); text(s,b,x+1.8,5.6,2.0,1.1,14,anchor=MSO_ANCHOR.MIDDLE,space=0)
# 7
s=new(title="Campaigns optimize toward different goals",notes="Worth understanding before standardizing goals. ExactMatch Tier 1 runs about $44 per bidding conversion against a $36 target, with 84% of impression share lost to rank, so there is room if the target is raised.")
card(s,0.6,1.5,5.9,3.6); text(s,"Account goals (calls-heavy)",0.9,1.75,5.3,0.5,20,TEAL,bold=True,font=HEAD)
text(s,["ExactMatch Tier 1 and Tier 1 Psych","Mostly local click-to-calls (about 11k a month), phone calls, Event 1","Best Bookings* CPB: $191 and $197"],0.9,2.4,5.3,2.5,16,bullets=True,space=10)
card(s,6.85,1.5,5.9,3.6); text(s,"Custom goal: Event 1 + Event 4",7.15,1.75,5.3,0.5,20,TEAL,bold=True,font=HEAD)
text(s,["Most other Search and all PMax campaigns","Bids directly on bookings","CPB mostly $230 to $300"],7.15,2.4,5.3,2.5,16,bullets=True,space=10)
card(s,0.6,5.4,12.15,1.3,ROSE); text(s,[[("Watch-out: ",{"bold":True,"color":CORAL}),("a calls goal can buy cheap calls that don't book. Judge target changes on Bookings* CPB, not in-platform CPA. Event 4 is 71% of ExactMatch Tier 1's bookings, in line with other campaigns.",{})]],0.9,5.5,11.6,1.1,15,anchor=MSO_ANCHOR.MIDDLE)
# 8
s=new(title="Junk search terms are cheap; a few themes aren't",notes="The PMax junk is high-impression, low-cost traffic; negating it is about cleanliness and PMax learning, not budget. The themes table is account-wide (PMax + Search): long-tail terms that are small one by one. The 756-term Universal Keyword Negative list is attached to nothing and contains phrase 'therapy' and 'therapist', so don't attach it as is.")
table(s,[["Theme (90 days)","Spend","CPB"],["Other practices' names","$6.4k","$454"],["\"Kids\" searches","$4.2k","$644"],["Sex therapy","$2.7k","$596"],["\"In my area\"","$1.1k","No bookings"]],0.6,1.5,6.2,[3.4,1.3,1.5],"Table themes",15)
text(s,"PMax top 100 terms (drug and condition lookups): 25% of impressions but 1.7% of cost, booking at $181 CPB.",0.6,4.3,6.2,1.0,15,SLATE)
card(s,7.2,1.5,5.55,2.4); text(s,[[("Done (Nov 13)",{"bold":True,"color":TEAL})],"New list \"All campaigns (potential future test)\" on 89 of 90 campaigns: kid, kids, sex, plus sex-therapy phrases. Flagged for a future test, not a permanent cut."],7.45,1.7,5.05,2.0,15)
card(s,7.2,4.2,5.55,2.5); text(s,[[("Pending",{"bold":True,"color":TEAL})],"Informational phrases (side effects, vs, uses). Competitor names leaking into PMax. Keep bare drug names ($156 CPB). The account-level negative list is empty."],7.45,4.4,5.05,2.1,15)
# 9
s=new(title="About 40% of brand spend isn't brand demand",notes="thriveworks alone is about 40% of brand spend and 47% of brand bookings. Mixing generic 'thrive' terms into brand makes brand CPB look better and non-brand look worse. The old duplicate thriveworks exact in 'Brand - Thriveworks EM' should be paused so traffic goes to the new ad group. CTRs for the thrive terms are approximate.")
table(s,[["Keyword","Impr. share","CTR","What it matches"],["thriveworks (exact)","92%","36%","People looking for us"],["thrive counseling (exact)","18%","~6%","Other \"Thrive\" practices"],["thrive therapy (exact)","17%","~5%","Other \"Thrive\" practices"],["thriving counseling (broad)","10%","~4%","\"therapy near me\" and similar"],["thrive marriage counseling (broad)","12%","~5%","Generic marriage counseling"]],0.6,1.5,8.3,[3.1,1.4,0.9,2.9],"Table brand",14,0.6)
stat(s,9.2,1.5,3.55,"~$17k","on \"thrive\" terms per 30 days",CORAL)
card(s,9.2,3.3,3.55,3.4); text(s,[[("Recommendation",{"bold":True,"color":TEAL})],"Separate them, don't pause: they book at about $90 to $190.","Done Nov 13: thriveworks exact moved to its own ad group."],9.45,3.5,3.05,3.0,15,space=10)
# 10
s=new(title="ExactMatch Tier 1: 190 of 801 keywords do the work",notes="801 enabled keywords plus about 1,550 paused. Keep rule: 1,000+ impressions or 3+ Bookings* in 90 days keeps 190 keywords. In progress: Tom is breaking the top search terms out into their own ad groups.")
ch=chart(s,XL_CHART_TYPE.LINE_MARKERS,["25","50","100","150","200","300","400","801"],[45.7,56.7,69.6,77.6,83.1,90.7,95.3,100],0.6,1.4,6.6,5.3,"Cumulative share of 90-day spend, by top N keywords",TEAL,'0"%"',"Chart keyword concentration",vmax=110,vmin=0)
table(s,[["Keyword (90 days)","Spend","Bookings*"],["relationship counseling near me","$12.9k","2.0"],["couples counselor near me","$4.6k","0"],["best couples counseling near me","$3.7k","0.5"],["relationship counseling","$3.4k","2.0"]],7.55,1.5,5.2,[3.0,1.0,1.2],"Table couples keywords",14)
card(s,7.55,4.3,5.2,2.3); text(s,[[("$24.5k for 4.5 bookings. ",{"bold":True,"color":CORAL}),("Similar keywords book normally (couples therapy near me: 30). The 611-keyword tail books at about the same CPB, so trimming it is about structure, not savings.",{})]],7.8,4.5,4.7,1.9,15)
# 11
s=new(title="What's already changed",notes="All account changes were approved by Tom before they were made. Location targeting and negatives were changed through the API; the brand ad group and search-term breakouts were done by Tom in the UI.")
ln=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(1.55),Inches(1.75),Inches(1.55),Inches(6.4)); ln.line.color.rgb=H(SAGE); ln.line.width=Pt(2); ln.name="Timeline line"
for i,(d,a,b) in enumerate([("Nov 13","New shared negative list on all campaigns","kid, kids, sex, plus 5 sex-therapy phrases"),("Nov 13","thriveworks exact in its own ad group","Cleaner brand structure"),("Nov 16","6 campaigns switched to Presence","Stops about $70k a month of out-of-state serving"),("Nov 17","3 Tier 1 campaigns created, paused","Tier 1 rebuild plus office test"),("Ongoing","Top search terms broken out into ad groups","Concentrate budget on proven terms")]):
    y=1.5+i*1.0; o=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(1.4),Inches(y+0.17),Inches(0.3),Inches(0.3)); o.fill.solid(); o.fill.fore_color.rgb=H(SEA); o.line.color.rgb=H(WHITE); o.shadow.inherit=False; o.name=f"Dot {i+1}"
    text(s,d,0.3,y+0.17,1.0,0.35,14,SLATE,bold=True,align=PP_ALIGN.RIGHT); text(s,a,2.0,y+0.05,10.6,0.45,18,bold=True); text(s,b,2.0,y+0.5,10.6,0.4,14,SLATE)
# 12
s=new(title="Tier 1 rebuild: three campaigns plus an office test",notes="Campaign IDs: Phrase 24470038974, Broad 24470038980, Virtual 24470038992. All paused. Built: 9 Tier 1 states by Presence, Search only, English, ExactMatch Tier 1 ad schedule, same 12 shared negative lists. Budgets are placeholders. The county split and the bidding goal are still to be confirmed (see decisions). One gap: the account-level static location group can't be excluded on Virtual through the API; confirm with Google.")
for i,(n,a,b,c) in enumerate([("Phrase","City searches","121 phrase keywords in 27 city ad groups","Office counties, with location assets"),("Broad","Service searches near offices","157 broad keywords in 16 ad groups","91 office counties (75% of Tier 1 spend, $251 CPB)"),("Virtual","Same searches, away from offices","Same keywords as Broad","712 non-office counties (25%, $242 CPB), no location assets")]):
    x=0.6+i*4.1; card(s,x,1.5,3.9,3.9,MINT if i==2 else PALE)
    text(s,n,x+0.25,1.7,3.4,0.6,26,SEA if i==2 else TEAL,bold=True,font=HEAD); text(s,a,x+0.25,2.35,3.4,0.5,16,bold=True)
    text(s,[b,c],x+0.25,2.95,3.4,2.3,14,bullets=True,space=8)
card(s,0.6,5.65,12.15,1.05,ROSE); text(s,[[("Why counties: ",{"bold":True,"color":CORAL}),("Google can't exclude a radius. Near and far don't overlap, so the campaigns don't compete with each other. State campaigns keep running across both areas.",{})]],0.9,5.75,11.6,0.85,15,anchor=MSO_ANCHOR.MIDDLE)
# 13
s=new(title="Launch steps and how we'll judge it",notes="Launch follows the Paid Search Campaign Launch SOP. Each campaign needs a NICE pool number and a call-asset number, a CallRail pool keyed on utm_campaign = campaign ID, an EXT number, one shared swap-target ticket, mapping sheet rows and a workflow branch. The out-of-state share after the Presence fix is also checked around Nov 30.")
for i,(a,b,done) in enumerate([("Campaigns built (paused)","Nov 17",True),("NICE numbers requested (6)","Nov 17",True),("Mapping sheet rows","Next",False),("CallRail pools, EXT, swap ticket","1-2 business days",False),("Workflow + QA","After swaps",False),("Launch, then pause ExactMatch T1","About 2 weeks later",False)]):
    x=0.6+i*2.05; card(s,x,1.6,1.9,1.9,TEAL if done else PALE,name=f"Step {i+1}")
    text(s,str(i+1),x+0.15,1.72,1.6,0.45,20,WHITE if done else TEAL,bold=True,font=HEAD); text(s,a,x+0.15,2.2,1.6,0.85,13,WHITE if done else INK,bold=True,space=0); text(s,b,x+0.15,3.05,1.6,0.4,12,SAGE if done else SLATE)
text(s,"How we'll judge it (read at 2 and 4 weeks)",0.6,3.95,12.1,0.5,20,TEAL,bold=True,font=HEAD)
for i,(a,b) in enumerate([("Bookings* CPB","By campaign, and combined with the state campaigns"),("Near vs far","CPC, conversion rate and CPB with and without location assets"),("Coverage","IL and MI lose exact match when ExactMatch Tier 1 pauses")]):
    x=0.6+i*4.1; card(s,x,4.6,3.9,1.95); text(s,[[(a,{"bold":True})],b],x+0.25,4.8,3.4,1.6,15)
# 14
s=new(dark=True,notes="Items 1 and 2 block the final build of the Tier 1 campaigns. Item 3 sets their budgets and targets. The rest can follow.")
text(s,"Decisions we need from this group",0.8,0.5,11.7,1.0,36,WHITE,bold=True,font=HEAD,anchor=MSO_ANCHOR.MIDDLE,name="Title")
text(s,["Bidding goal for new campaigns: Event 1 + 4 everywhere, or keep account goals on Broad?","Office test unit: county split, or city level?","Current tCPA ceilings ($240/$205 vs $200/$250) and LTV:CAC (1.87 vs 1.99)","Brand \"thrive\" terms: separate ad group, or move to non-brand?","Demand Gen: turn on for NC, SC, VA, or update the sheet?","Align ExactMatch states with tiers (SC in, IL and MI out)?","Event 4 attribution by campaign (Diego / Anfernee)","Kids and sex therapy: minimum age and clinician coverage before any test"],0.8,1.7,11.8,5.2,18,WHITE,numbered=True,space=10)
prs.core_properties.title="Google Ads account review and plan"; prs.core_properties.author="Tom Roberts"
prs.save("google-ads-review-nov-2026.pptx"); print("saved")
