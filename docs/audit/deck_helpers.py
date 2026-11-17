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

