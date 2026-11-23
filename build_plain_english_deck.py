"""
Generates a 10-Slide Plain English, Nigeria-Context PowerPoint Presentation
with Embedded Speaker Notes for Olakunle Awotunbo's Master's Project Defence.
Miva Open University • Master of Information Technology (MIT 8313)
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

OUTPUT_FILE = "Olakunle_Awotunbo_MIT8313_Defence_Presentation_PlainEnglish.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Professional Color Palette
C_NAVY_DARK = RGBColor(10, 25, 47)       # #0A192F (Deep Academic Navy)
C_NAVY_PRIMARY = RGBColor(16, 42, 77)     # #102A4D (Header Navy)
C_BLUE_ACCENT = RGBColor(26, 75, 140)     # #1A4B8C (Sub-headers & links)
C_GOLD = RGBColor(184, 134, 11)           # #B8860B (Academic Gold)
C_GOLD_LIGHT = RGBColor(254, 243, 199)    # #FEF3C7 (Warm highlight)
C_EMERALD = RGBColor(22, 101, 52)         # #166534 (Success / Low Risk)
C_EMERALD_BG = RGBColor(240, 253, 244)    # #F0FDF4
C_CRIMSON = RGBColor(153, 27, 27)         # #991B1B (Fraud / High Risk)
C_CRIMSON_BG = RGBColor(254, 242, 242)    # #FEF2F2
C_AMBER = RGBColor(180, 83, 9)            # #B45309 (Medium Risk)
C_AMBER_BG = RGBColor(255, 251, 235)      # #FFFBEB
C_TEXT_DARK = RGBColor(30, 41, 59)        # #1E293B (Body Text)
C_TEXT_MUTED = RGBColor(71, 85, 105)      # #475569 (Captions & Notes)
C_BG_LIGHT = RGBColor(248, 250, 252)      # #F8FAFC (Card Background)
C_BORDER = RGBColor(226, 232, 240)        # #E2E8F0 (Card Border)
C_BORDER_DARK = RGBColor(203, 213, 225)   # #CBD5E1
C_WHITE = RGBColor(255, 255, 255)
C_TABLE_HEADER = RGBColor(16, 42, 77)
C_TABLE_ROW_ALT = RGBColor(241, 245, 249)

FONT_NAME = "Times New Roman"

def set_font(run, size=11, bold=False, italic=False, color=C_TEXT_DARK):
    """Enforce Times New Roman typography across all presentation runs."""
    run.font.name = FONT_NAME
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def add_header(slide, title_text, category_text="MIVA OPEN UNIVERSITY • MIT 8313 DEFENCE"):
    """Standardized academic defense slide header."""
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_GOLD
    top_line.line.fill.background()

    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.22), Inches(11.733), Inches(0.95))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    set_font(p_cat.runs[0] if p_cat.runs else p_cat.add_run(), size=9.5, bold=True, color=C_GOLD)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    set_font(p_title.runs[0] if p_title.runs else p_title.add_run(), size=20, bold=True, color=C_NAVY_PRIMARY)
    p_title.space_before = Pt(2)

def add_footer(slide, slide_num, total_slides=10):
    """Standardized academic defense slide footer."""
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = C_BORDER
    div.line.fill.background()

    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.07), Inches(11.733), Inches(0.32))
    tf = footer_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Candidate: Olakunle Oladeji Awotunbo (2025/B/MIT/1384)  |  Supervisor: Prof. Olushina Olawale Awe"
    set_font(r1, size=9, color=C_TEXT_MUTED)

    r2 = p.add_run()
    r2.text = f"                                                                               Slide {slide_num} of {total_slides}"
    set_font(r2, size=9, bold=True, color=C_NAVY_PRIMARY)

def add_card(slide, left, top, width, height, bg_color=C_BG_LIGHT, border_color=C_BORDER):
    """Create a structured rounded container card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_image_fitted(slide, img_path, left, top, max_width, max_height, caption=None):
    """Fit image maintaining aspect ratio with thin border and caption."""
    if not os.path.exists(img_path):
        return None
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size
    aspect = orig_w / orig_h
    target_aspect = max_width / max_height
    if aspect > target_aspect:
        w = max_width
        h = max_width / aspect
    else:
        h = max_height
        w = max_height * aspect
    offset_x = left + (max_width - w) / 2
    offset_y = top + (max_height - h) / 2

    border_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, offset_x - Inches(0.04), offset_y - Inches(0.04), w + Inches(0.08), h + Inches(0.08))
    border_box.fill.solid()
    border_box.fill.fore_color.rgb = C_WHITE
    border_box.line.color.rgb = C_BORDER_DARK
    border_box.line.width = Pt(1)

    pic = slide.shapes.add_picture(img_path, offset_x, offset_y, w, h)
    if caption:
        cap_box = slide.shapes.add_textbox(left, offset_y + h + Inches(0.06), max_width, Inches(0.35))
        tf = cap_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = caption
        set_font(r, size=9, italic=True, color=C_TEXT_MUTED)
    return pic

def set_speaker_note(slide, note_text):
    """Embed conversational, first-person speaker script into PowerPoint's Notes pane."""
    notes = slide.notes_slide
    tf = notes.notes_text_frame
    tf.text = note_text.strip()


# ==============================================================================
# SLIDE 1: Title Slide (Simple English & Nigerian Financial Context)
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)

hero1 = add_card(slide1, Inches(0.8), Inches(0.65), Inches(11.733), Inches(3.7), bg_color=C_NAVY_DARK, border_color=None)
hero_accent1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.08))
hero_accent1.fill.solid()
hero_accent1.fill.fore_color.rgb = C_GOLD
hero_accent1.line.fill.background()

tb_hero1 = slide1.shapes.add_textbox(Inches(1.1), Inches(0.9), Inches(11.133), Inches(3.2))
tf1 = tb_hero1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

p = tf1.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "DEPARTMENT OF INFORMATION TECHNOLOGY • SCHOOL OF COMPUTING\nMIVA OPEN UNIVERSITY ABUJA, NIGERIA"
set_font(r, size=11, bold=True, color=C_GOLD)

p = tf1.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(10)
r = p.add_run()
r.text = "FINAL MASTER'S DEGREE PROJECT DEFENCE • MIT 8313"
set_font(r, size=12, bold=True, color=RGBColor(203, 213, 225))

p = tf1.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(12)
r = p.add_run()
r.text = "DESIGN AND IMPLEMENTATION OF A FRAUD DETECTION SYSTEM\nFOR MOBILE MONEY TRANSACTIONS IN NIGERIA"
set_font(r, size=23, bold=True, color=C_WHITE)

p = tf1.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(10)
r = p.add_run()
r.text = "A Practical, Real-Time Machine Learning System Tailored for Nigerian Mobile Payment Switches (OPay, PalmPay, USSD & NIP)"
set_font(r, size=12.5, italic=True, color=RGBColor(226, 232, 240))

# Left Card: Candidate Details
add_card(slide1, Inches(0.8), Inches(4.55), Inches(5.75), Inches(2.35), bg_color=C_BG_LIGHT)
tb_cand1 = slide1.shapes.add_textbox(Inches(1.05), Inches(4.7), Inches(5.25), Inches(2.05))
tfc1 = tb_cand1.text_frame
tfc1.word_wrap = True
tfc1.margin_left = tfc1.margin_top = tfc1.margin_right = tfc1.margin_bottom = 0

p = tfc1.paragraphs[0]
r = p.add_run()
r.text = "CANDIDATE INFORMATION"
set_font(r, size=11, bold=True, color=C_GOLD)

items_cand1 = [
    ("Candidate Name", "Olakunle Oladeji Awotunbo"),
    ("Matriculation No.", "2025/B/MIT/1384"),
    ("Degree Program", "Master of Information Technology (MIT)"),
    ("Institutional Email", "o.awotunbo6129@miva.edu.ng"),
    ("Academic Session", "November 2026"),
]
for label, val in items_cand1:
    p = tfc1.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"•  {label}: "
    set_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = val
    set_font(r2, size=10.5, color=C_NAVY_PRIMARY if "Name" in label else C_TEXT_DARK)

# Right Card: Supervision Details
add_card(slide1, Inches(6.783), Inches(4.55), Inches(5.75), Inches(2.35), bg_color=C_BG_LIGHT)
tb_sup1 = slide1.shapes.add_textbox(Inches(7.033), Inches(4.7), Inches(5.25), Inches(2.05))
tfs1 = tb_sup1.text_frame
tfs1.word_wrap = True
tfs1.margin_left = tfs1.margin_top = tfs1.margin_right = tfs1.margin_bottom = 0

p = tfs1.paragraphs[0]
r = p.add_run()
r.text = "SUPERVISION & DEFENCE COMMITTEE"
set_font(r, size=11, bold=True, color=C_GOLD)

items_sup1 = [
    ("Project Supervisor", "Prof. Olushina Olawale Awe"),
    ("Internal Examiner", "Dr. Morolake Lawrence"),
    ("Department", "Department of Information Technology"),
    ("Faculty / School", "School of Computing, Miva Open University"),
    ("Defense Status", "Master's Project Oral Defence (MIT 8313)"),
]
for label, val in items_sup1:
    p = tfs1.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"•  {label}: "
    set_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = val
    set_font(r2, size=10.5, color=C_BLUE_ACCENT if "Supervisor" in label else C_TEXT_DARK)

set_speaker_note(slide1, """
Good morning, distinguished members of the panel, my esteemed project supervisor Professor Olushina Olawale Awe, internal examiner Dr. Morolake Lawrence, and everyone present today.

My name is Olakunle Oladeji Awotunbo, with matriculation number 2025/B/MIT/1384. Today, I am proud and honored to present my Master's project defence titled: 'Design and Implementation of a Fraud Detection System for Mobile Money Transactions in Nigeria'.

In this presentation, I am going to explain in simple, everyday English what motivated this study, how it improves on existing banking systems, and how I built a practical, lightning-fast machine learning system to protect everyday Nigerians from mobile money fraud. Thank you, and I look forward to your feedback.
""")


# ==============================================================================
# SLIDE 2: What Motivated This Study? The Nigerian Reality
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "WHAT MOTIVATED THIS STUDY? THE NIGERIAN REALITY", "MOTIVATION & PROBLEM CONTEXT")
add_footer(slide2, 2)

# Left Column: The Daily Nigerian Financial Reality
add_card(slide2, Inches(0.8), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb2_left = slide2.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(5.25), Inches(5.2))
tf2_l = tb2_left.text_frame
tf2_l.word_wrap = True
tf2_l.margin_left = tf2_l.margin_top = tf2_l.margin_right = tf2_l.margin_bottom = 0

p = tf2_l.paragraphs[0]
r = p.add_run()
r.text = "1. THE BOOM IN NIGERIAN MOBILE PAYMENTS"
set_font(r, size=12, bold=True, color=C_NAVY_PRIMARY)

points2_l1 = [
    ("Cashless Revolution", "Millions of Nigerians use fintech mobile apps like OPay, PalmPay, Moniepoint, Kuda, and commercial bank apps every day."),
    ("USSD for Everyone", "Millions more rely on telecom USSD banking (*737#, *901#, *894#) without smartphones or internet connection."),
    ("Agency Banking / POS", "Over 1.5 million POS agent kiosks operate across Nigerian street corners and rural markets, driving financial inclusion."),
]
for title, desc in points2_l1:
    p = tf2_l.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = f"• {title}: "
    set_font(r, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.8, color=C_TEXT_MUTED)

p = tf2_l.add_paragraph()
p.space_before = Pt(14)
r = p.add_run()
r.text = "2. THE DEVASTATING THREAT OF FRAUD"
set_font(r, size=12, bold=True, color=C_CRIMSON)

points2_l2 = [
    ("Massive Financial Losses", "NIBSS and FITC report that Nigerian banks and fintechs lose billions of Naira every single year to electronic fraud."),
    ("Stolen Phones & SIM-Swaps", "Criminals steal phones or illegally swap SIM cards to seize bank access before the victim can react."),
    ("Midnight Account Drains", "Fraudsters intentionally strike between 1:00 AM and 5:00 AM while the victim sleeps, draining every kobo to zero!"),
    ("Human Cost", "Traders, students, and families lose their life savings in minutes. This erodes trust in cashless policies and financial inclusion."),
]
for title, desc in points2_l2:
    p = tf2_l.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = f"• {title}: "
    set_font(r, size=10, bold=True, color=C_CRIMSON)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.8, color=C_TEXT_DARK)

# Right Column: Why Legacy Bank Systems Fail in Nigeria
add_card(slide2, Inches(6.783), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb2_right = slide2.shapes.add_textbox(Inches(7.033), Inches(1.45), Inches(5.25), Inches(5.2))
tf2_r = tb2_right.text_frame
tf2_r.word_wrap = True
tf2_r.margin_left = tf2_r.margin_top = tf2_r.margin_right = tf2_r.margin_bottom = 0

p = tf2_r.paragraphs[0]
r = p.add_run()
r.text = "3. WHY CURRENT BANK SYSTEMS FAIL US"
set_font(r, size=12, bold=True, color=C_AMBER)

points2_r = [
    ("Static Rules Are Too Dumb", "Legacy bank rules only check fixed numbers—like 'alert if transfer > ₦500,000'. But fraudsters know this! They split the stolen money into ₦49,000 transfers ('smurfing') to slip under the radar."),
    ("The Delay is Deadly", "By the time a human fraud analyst arrives at work at 8:00 AM or the victim reaches a bank branch to place a Post-No-Debit (PND), the stolen money has hopped through 4 mule accounts and been cashed out at a roadside POS."),
    ("High False Alarm Chaos", "Standard anomaly detection tools flag 1% to 2% of normal transactions. In Nigeria, that means falsely freezing 50,000 innocent citizens every day at supermarket checkout lines and filling stations!"),
    ("Black-Box Algorithms", "Complex AI models cannot explain why a transaction was declined. Under Central Bank of Nigeria (CBN) rules, banks cannot freeze customers' funds without giving a valid, transparent reason."),
]
for title, desc in points2_r:
    p = tf2_r.add_paragraph()
    p.space_before = Pt(8)
    r = p.add_run()
    r.text = f"• {title}: "
    set_font(r, size=10.2, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.8, color=C_TEXT_MUTED)

# Bottom Highlight Banner on Right
add_card(slide2, Inches(7.033), Inches(5.8), Inches(5.25), Inches(0.85), bg_color=C_GOLD_LIGHT, border_color=C_GOLD)
tb2_box = slide2.shapes.add_textbox(Inches(7.15), Inches(5.85), Inches(5.0), Inches(0.75))
tf2_b = tb2_box.text_frame
tf2_b.word_wrap = True
tf2_b.margin_left = tf2_b.margin_top = tf2_b.margin_right = tf2_b.margin_bottom = 0
p = tf2_b.paragraphs[0]
r = p.add_run()
r.text = "THE CORE RESEARCH MOTIVATION:\n"
set_font(r, size=9.5, bold=True, color=C_NAVY_PRIMARY)
r2 = p.add_run()
r2.text = "To build an automated, explainable, sub-50 millisecond fraud detection system that stops account liquidation before money leaves the Nigerian payment switch."
set_font(r2, size=9.5, italic=True, color=C_TEXT_DARK)

set_speaker_note(slide2, """
Distinguished examiners, to understand what motivated this study, let us look at our daily reality in Nigeria.

Today, Nigeria is experiencing a massive cashless revolution. We use OPay, PalmPay, Moniepoint, Kuda, bank mobile apps, and USSD codes like *737# and *901# every single day. Even in remote villages and bustling markets like Balogun or Bodija, there are POS agent kiosks everywhere.

However, this convenience has created an urgent, dangerous problem. According to NIBSS and FITC, Nigerian banks and fintechs lose billions of Naira to digital fraud every year. When someone’s phone is stolen in traffic, or when fraudsters perform an unauthorized SIM-swap, they don't wait. They attack between 1:00 AM and 5:00 AM while the victim is fast asleep. Within minutes, they drain every single kobo from the account.

Why can't our current bank systems stop this?
First, legacy systems rely on dumb, static rules like 'flag transactions above ₦500,000'. Fraudsters know this rule, so they split ₦500,000 into ten transfers of ₦49,000. It passes cleanly!
Second, by the time the victim wakes up at 7:00 AM and runs to the bank to report, the money has already jumped across three different fintech accounts and been cashed out at an early morning POS stand.
Third, existing machine learning systems produce too many false alarms, wrongfully freezing innocent Nigerians at checkout counters.

This terrible situation motivated me to build a system that detects the exact behavioral signature of account liquidations in real time, without blocking innocent customers.
""")


# ==============================================================================
# SLIDE 3: How This Study Improves Over Existing Studies & Bank Systems
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "HOW THIS STUDY IMPROVES OVER EXISTING STUDIES", "RESEARCH INNOVATION & COMPARATIVE ADVANTAGE")
add_footer(slide3, 3)

# 4 Comparative Cards Layout (2x2 Grid)
card_w = Inches(5.75)
card_h = Inches(2.65)

# Card 1: Behavioral Liquidation vs Static Rules
add_card(slide3, Inches(0.8), Inches(1.3), card_w, card_h, bg_color=C_BG_LIGHT)
tb3_1 = slide3.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(5.25), Inches(2.35))
tf3_1 = tb3_1.text_frame
tf3_1.word_wrap = True
tf3_1.margin_left = tf3_1.margin_top = tf3_1.margin_right = tf3_1.margin_bottom = 0

p = tf3_1.paragraphs[0]
r = p.add_run()
r.text = "1. BEHAVIORAL LIQUIDATION TRACKING (VS STATIC RULES)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

items3_1 = [
    ("Old Bank Systems", "Only inspect transfer amounts (e.g. amount > ₦500k). Completely blind to split transfers (smurfing ₦49k) and SIM-swap cash-outs."),
    ("Our Improvement", "We engineered smart mathematical indicators: isCompleteDrain and amountToBalanceRatio (Eq 3.1 & 3.2)."),
    ("Practical Benefit", "If a fraudster attempts to empty 99% to 100% of an account's balance to zero, our system catches it instantly—whether the transfer is ₦20,000 or ₦2,000,000!"),
]
for label, desc in items3_1:
    p = tf3_1.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"• {label}: "
    set_font(r1, size=9.8, bold=True, color=C_CRIMSON if "Old" in label else C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.5, color=C_TEXT_DARK)

# Card 2: Crushing the False Positive Crisis
add_card(slide3, Inches(6.783), Inches(1.3), card_w, card_h, bg_color=C_BG_LIGHT)
tb3_2 = slide3.shapes.add_textbox(Inches(7.033), Inches(1.45), Inches(5.25), Inches(2.35))
tf3_2 = tb3_2.text_frame
tf3_2.word_wrap = True
tf3_2.margin_left = tf3_2.margin_top = tf3_2.margin_right = tf3_2.margin_bottom = 0

p = tf3_2.paragraphs[0]
r = p.add_run()
r.text = "2. CRUSHING FALSE ALARMS (0.007% FALSE POSITIVE RATE)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

items3_2 = [
    ("Old Academic Studies", "Unsupervised models (Deep Autoencoders, Isolation Forests) suffer an FPR of 1.0% to 1.84%. In a 5M daily switch, that wrongfully blocks 50,000 innocent Nigerians daily!"),
    ("Our Improvement", "Trained Cost-Weighted XGBoost with rigorous cost-sensitive penalty (scale_pos_weight = 774.7) and Train-only SMOTE."),
    ("Practical Benefit", "Slashed the False Positive Rate to 0.007% (only 35 false alarms in 500,000 transactions) while still catching 91.80% of real fraud!"),
]
for label, desc in items3_2:
    p = tf3_2.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"• {label}: "
    set_font(r1, size=9.8, bold=True, color=C_CRIMSON if "Old" in label else C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.5, color=C_TEXT_DARK)

# Card 3: Explainable Decisions (No Black Box AI)
add_card(slide3, Inches(0.8), Inches(4.15), card_w, card_h, bg_color=C_BG_LIGHT)
tb3_3 = slide3.shapes.add_textbox(Inches(1.05), Inches(4.3), Inches(5.25), Inches(2.35))
tf3_3 = tb3_3.text_frame
tf3_3.word_wrap = True
tf3_3.margin_left = tf3_3.margin_top = tf3_3.margin_right = tf3_3.margin_bottom = 0

p = tf3_3.paragraphs[0]
r = p.add_run()
r.text = "3. EXPLAINABLE DECISIONS (COMPLIANT WITH CBN & NDPR)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

items3_3 = [
    ("Old AI Approaches", "Complex neural networks are 'black boxes'. Banks cannot explain why an account was frozen, violating CBN consumer rights."),
    ("Our Improvement", "Integrated TreeSHAP (SHapley Additive exPlanations) directly into the decision pipeline."),
    ("Practical Benefit", "Every alert produces a mathematical receipt showing exact reasons (e.g. 'Account balance emptied to 0 (+0.42 risk), Midnight transfer (+0.25 risk)'). Customer care can explain it clearly."),
]
for label, desc in items3_3:
    p = tf3_3.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"• {label}: "
    set_font(r1, size=9.8, bold=True, color=C_CRIMSON if "Old" in label else C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.5, color=C_TEXT_DARK)

# Card 4: Lightning Speed for USSD & NIP (14.2ms Latency)
add_card(slide3, Inches(6.783), Inches(4.15), card_w, card_h, bg_color=C_BG_LIGHT)
tb3_4 = slide3.shapes.add_textbox(Inches(7.033), Inches(4.3), Inches(5.25), Inches(2.35))
tf3_4 = tb3_4.text_frame
tf3_4.word_wrap = True
tf3_4.margin_left = tf3_4.margin_top = tf3_4.margin_right = tf3_4.margin_bottom = 0

p = tf3_4.paragraphs[0]
r = p.add_run()
r.text = "4. LIGHTNING SPEED FOR USSD & NIP (14.2 MILLISECONDS)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

items3_4 = [
    ("Old Studies", "Academic models only run offline in Python notebooks; too slow to survive the 50ms telecom switch timeout SLA."),
    ("Our Improvement", "Engineered and deployed a lightweight FastAPI REST microservice optimized for high-throughput inference."),
    ("Practical Benefit", "Tested in Postman with an average latency of 14.2 milliseconds per transaction—more than 3 times faster than the 50ms limit required by Nigerian telecom switches!"),
]
for label, desc in items3_4:
    p = tf3_4.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"• {label}: "
    set_font(r1, size=9.8, bold=True, color=C_CRIMSON if "Old" in label else C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.5, color=C_TEXT_DARK)

set_speaker_note(slide3, """
A very important question the examiners will ask is: 'What makes your study an improvement over existing work?'
This slide summarizes our four key improvements in plain English:

First: We replaced dumb static rules with behavioral liquidation tracking. Old systems look only at the transfer amount, like 'flag if greater than ₦500,000'. But fraudsters easily bypass this by splitting transfers into ₦49,000. Our system doesn't care whether you send ₦20,000 or ₦2 million; it calculates our smart equations `isCompleteDrain` and `amountToBalanceRatio`. If someone tries to empty 100% of an account to zero, it catches them immediately.

Second: We solved the false alarm crisis. Existing academic studies that use unsupervised anomaly models like Autoencoders have a false positive rate of 1% to 2%. In Nigeria, where switches process 5 million transactions daily, a 1% false positive rate means freezing 50,000 innocent Nigerians every single day! Our Cost-Weighted XGBoost model reduced this false positive rate to 0.007%—meaning only 35 false alarms in 500,000 transactions, while still catching 91.8% of actual fraud.

Third: We eliminated 'black-box AI'. Under Central Bank of Nigeria regulations and the Nigerian Data Protection Regulation (NDPR), a bank cannot just freeze a customer's money and say 'the AI did it'. Our system integrates TreeSHAP, producing an instant explainability receipt that tells customer support exactly why the transaction was blocked.

Fourth: Lightning speed. If an AI model takes 200 milliseconds to think, a USSD session on MTN or Airtel (*737#) will timeout and fail. Our FastAPI system processes transactions in just 14.2 milliseconds, well below the 50-millisecond telecom limit.
""")


# ==============================================================================
# SLIDE 4: Research Objectives & Design Science Methodology
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "RESEARCH OBJECTIVES & DESIGN SCIENCE METHODOLOGY", "METHODOLOGICAL FRAMEWORK")
add_footer(slide4, 4)

# Left Column: Research Objectives
add_card(slide4, Inches(0.8), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb4_l = slide4.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(5.25), Inches(5.2))
tf4_l = tb4_l.text_frame
tf4_l.word_wrap = True
tf4_l.margin_left = tf4_l.margin_top = tf4_l.margin_right = tf4_l.margin_bottom = 0

p = tf4_l.paragraphs[0]
r = p.add_run()
r.text = "FOUR CLEAR RESEARCH OBJECTIVES"
set_font(r, size=12, bold=True, color=C_NAVY_PRIMARY)

objectives = [
    ("Objective 1: Behavioral Feature Engineering", "Design and formulate domain-specific mathematical features (isCompleteDrain, amountToBalanceRatio, balanceDiscrepancy) that specifically mirror Nigerian SIM-swap and account draining tactics."),
    ("Objective 2: Multi-Paradigm Machine Learning Benchmark", "Train and rigorously evaluate 5 diverse machine learning models (XGBoost, LightGBM, Random Forest, Logistic Regression, Deep Autoencoder) under severe class imbalance (0.129% fraud)."),
    ("Objective 3: Leakage-Free Protocol & Cost Optimization", "Implement a 5-Fold Stratified Cross-Validation protocol with Train-only SMOTE and cost-sensitive weighting to minimize False Positives without missing real fraud."),
    ("Objective 4: Production Artifact Implementation", "Build, test, and deploy a complete, working software artifact: a 14.2ms FastAPI gateway, a live Streamlit surveillance dashboard, and TreeSHAP explainability for bank compliance."),
]
for title, desc in objectives:
    p = tf4_l.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"• {title}:\n  "
    set_font(r1, size=10, bold=True, color=C_BLUE_ACCENT)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.5, color=C_TEXT_DARK)

# Right Column: DSR Framework Visual
add_card(slide4, Inches(6.783), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb4_r = slide4.shapes.add_textbox(Inches(7.033), Inches(1.45), Inches(5.25), Inches(0.4))
tf4_r = tb4_r.text_frame
tf4_r.word_wrap = True
tf4_r.margin_left = tf4_r.margin_top = tf4_r.margin_right = tf4_r.margin_bottom = 0
p = tf4_r.paragraphs[0]
r = p.add_run()
r.text = "PEFFERS ET AL. DESIGN SCIENCE RESEARCH (DSR)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide4,
    "screenshots/Figure 3.1 - Design Science Research.jpeg",
    left=Inches(7.033),
    top=Inches(1.95),
    max_width=Inches(5.25),
    max_height=Inches(4.65),
    caption="Figure 3.1: Design Science Research (DSR) Six-Phase Methodological Framework"
)

set_speaker_note(slide4, """
To achieve these goals, I followed the established Design Science Research (DSR) methodology by Peffers and colleagues, illustrated on the right side of this slide. Design Science is ideal for a Master of Information Technology project because it doesn't just stop at writing theory—it requires designing, developing, and evaluating a real-world software artifact that solves a genuine human problem.

My research answered four clear objectives:
First, to formulate behavioral accounting equations that capture the exact ways fraudsters operate in Nigeria—especially draining accounts to zero.
Second, to benchmark five diverse machine learning models across supervised tree ensembles, linear baselines, and deep unsupervised autoencoders under an extreme 0.129% fraud imbalance.
Third, to train these models without any data leakage using a strict 5-Fold Stratified Cross-Validation protocol and Cost-Sensitive Weighting.
And fourth, to build and deploy a working, production-ready system consisting of a 14.2ms FastAPI gateway, a live Streamlit surveillance dashboard, and TreeSHAP explainability.
""")


# ==============================================================================
# SLIDE 5: System Architecture & Smart Accounting Equations
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "SYSTEM ARCHITECTURE & SMART ACCOUNTING EQUATIONS", "MATHEMATICAL FORMULATION & SYSTEM DESIGN")
add_footer(slide5, 5)

# Left Column: The 4 Accounting Equations Explained Simply
add_card(slide5, Inches(0.8), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb5_l = slide5.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(5.25), Inches(5.2))
tf5_l = tb5_l.text_frame
tf5_l.word_wrap = True
tf5_l.margin_left = tf5_l.margin_top = tf5_l.margin_right = tf5_l.margin_bottom = 0

p = tf5_l.paragraphs[0]
r = p.add_run()
r.text = "SMART ACCOUNTING EQUATIONS (PLAIN ENGLISH)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

equations = [
    ("Equation 3.1: Complete Account Drain", "isCompleteDrain = 1  if  (amount == oldBalanceOrig  and  newBalanceOrig == 0)\nMeaning: Catches when a thief steals a phone or swaps a SIM, sees the victim's balance, and immediately transfers everything so the balance becomes zero."),
    ("Equation 3.2: Amount to Balance Ratio", "amountToBalanceRatio = amount / (oldBalanceOrig + 1.0)\nMeaning: Normal people transfer 5% or 20% of their money for groceries or transport. Fraudsters transfer 95% to 100% of available funds in one single hit!"),
    ("Equation 3.3: Origin Balance Discrepancy", "diffOrig = (newBalanceOrig + amount) - oldBalanceOrig\nMeaning: Checks if the sender's account ledger balances out properly after the transfer, exposing artificial money movements."),
    ("Equation 3.4: Destination Balance Discrepancy", "diffDest = (newBalanceDest - amount) - oldBalanceDest\nMeaning: Checks if the receiver's balance matches what was sent, catching ghost or mule accounts created to launder stolen funds."),
]
for title, text in equations:
    p = tf5_l.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"• {title}:\n"
    set_font(r1, size=9.8, bold=True, color=C_GOLD)
    r2 = p.add_run()
    r2.text = text
    set_font(r2, size=9.2, color=C_TEXT_DARK)

# Right Column: System Architecture Visual
add_card(slide5, Inches(6.783), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb5_r = slide5.shapes.add_textbox(Inches(7.033), Inches(1.45), Inches(5.25), Inches(0.4))
tf5_r = tb5_r.text_frame
tf5_r.word_wrap = True
tf5_r.margin_left = tf5_r.margin_top = tf5_r.margin_right = tf5_r.margin_bottom = 0
p = tf5_r.paragraphs[0]
r = p.add_run()
r.text = "MULTI-TIER PRODUCTION SYSTEM ARCHITECTURE"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide5,
    "screenshots/Figure 3.2 - High-Level Multi-Tier.png",
    left=Inches(7.033),
    top=Inches(1.95),
    max_width=Inches(5.25),
    max_height=Inches(4.65),
    caption="Figure 3.2: High-Level Multi-Tier System Architecture (Client -> Gateway -> XGBoost -> SHAP)"
)

set_speaker_note(slide5, """
How does the system actually catch a fraudster? It starts with the domain-specific accounting equations I formulated in Chapter 3, shown on the left side of this slide.

Let's look at Equation 3.1: `isCompleteDrain`. When normal Nigerians use their bank app, they might send ₦5,000 for electricity, ₦10,000 for groceries, or ₦20,000 to family. But when a phone thief or SIM-swap criminal takes over your account, what do they do? They look at the balance, see ₦150,000, and immediately transfer all ₦150,000 out so the remaining balance is zero! Equation 3.1 detects this exact behavior. If the amount equals the old balance and leaves zero behind, it sets `isCompleteDrain = 1`.

Equation 3.2 computes the `amountToBalanceRatio`. Honest transactions represent a small fraction of a user's funds. A liquidation attempt tries to empty 100% of the funds.

Equations 3.3 and 3.4 check for balance discrepancies on both sender and receiver accounts. In normal banking, money deducted from the sender must equal money credited to the receiver. But when fraudsters route money through temporary mule accounts or cash out illicitly at POS terminals, these accounting balances show clear mathematical discrepancies.

On the right side of the slide is our multi-tier architecture: The incoming transaction hits our FastAPI gateway, the feature engineering pipeline calculates these equations in microseconds, passes the numbers to our trained XGBoost model, and outputs a risk score and a SHAP explanation—all in just 14.2 milliseconds!
""")


# ==============================================================================
# SLIDE 6: How the AI Was Trained: Clean Data Without Any Cheating
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "HOW THE AI WAS TRAINED: CLEAN DATA & INTEGRITY", "DATA PIPELINE & VALIDATION PROTOCOL")
add_footer(slide6, 6)

# Left Column: Data Pipeline & Integrity Principles
add_card(slide6, Inches(0.8), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb6_l = slide6.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(5.25), Inches(5.2))
tf6_l = tb6_l.text_frame
tf6_l.word_wrap = True
tf6_l.margin_left = tf6_l.margin_top = tf6_l.margin_right = tf6_l.margin_bottom = 0

p = tf6_l.paragraphs[0]
r = p.add_run()
r.text = "TRAINING ON 6.36 MILLION TRANSACTIONS"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

pipeline_points = [
    ("Massive Benchmark Scale", "Trained on 6,362,620 mobile money transactions from the PaySim dataset, simulating real-world African telecom mobile money networks."),
    ("Extreme Class Imbalance (0.129%)", "Only 8,213 transactions out of 6.36 million were fraudulent. Finding fraud is like finding one needle in a haystack of 1,000 items!"),
    ("80/20 Stratified Partitioning", "5,090,096 transactions used for training and cross-validation; 1,272,524 transactions locked away in a blind test set never seen during training."),
    ("5-Fold Stratified Cross-Validation", "The training set was divided into 5 equal folds, each keeping the exact 0.129% fraud ratio. Models trained on 4 folds and tested on the 5th, rotating 5 times."),
    ("Zero Data Leakage (Train-Only SMOTE)", "Synthetic oversampling (SMOTE) was applied ONLY inside each training fold. We never touched validation or test sets with synthetic data!"),
]
for title, desc in pipeline_points:
    p = tf6_l.add_paragraph()
    p.space_before = Pt(6)
    r1 = p.add_run()
    r1.text = f"• {title}:\n  "
    set_font(r1, size=9.8, bold=True, color=C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.2, color=C_TEXT_DARK)

# Right Column: Neural Architecture Visual
add_card(slide6, Inches(6.783), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb6_r = slide6.shapes.add_textbox(Inches(7.033), Inches(1.45), Inches(5.25), Inches(0.4))
tf6_r = tb6_r.text_frame
tf6_r.word_wrap = True
tf6_r.margin_left = tf6_r.margin_top = tf6_r.margin_right = tf6_r.margin_bottom = 0
p = tf6_r.paragraphs[0]
r = p.add_run()
r.text = "DEEP AUTOENCODER BENCHMARK ARCHITECTURE"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide6,
    "screenshots/Figure 4.1- Deep Autoencoder Neural Reconst Archi.png",
    left=Inches(7.033),
    top=Inches(1.95),
    max_width=Inches(5.25),
    max_height=Inches(4.65),
    caption="Figure 4.1: Deep Autoencoder Neural Reconstruction Architecture (10 -> 8 -> 4 -> 8 -> 10)"
)

set_speaker_note(slide6, """
A very common problem in machine learning research is what we call 'data leakage' or cheating—where the model accidentally peeks at the test data during training. I made sure our training process was completely honest, scientific, and leak-free.

We evaluated on a massive dataset of 6.36 million mobile money transactions. Out of these, only 8,213 were fraudulent—representing just 0.129%. That means out of every 1,000 transactions, over 998 are completely legitimate.

We partitioned the data using an 80/20 stratified split: over 5 million transactions were used for training, and 1.27 million transactions were locked away in a blind test set.

Inside the training data, we used a 5-Fold Stratified Cross-Validation protocol. This means the data was split into five equal parts, each preserving that exact 0.129% fraud ratio. The model trained on four parts and tested on the fifth part, rotating five times so every single record was evaluated without bias.

Most importantly, when we applied SMOTE to help the models learn the rare fraud patterns, we applied it *strictly inside each training fold*. We never touched the validation folds or the test set with synthetic data.

On the right side of the slide is the Deep Autoencoder neural network we also built and tested. It compresses transactions down to 4 bottleneck features and tries to reconstruct them, flagging reconstruction errors as fraud. This allowed us to fairly compare deep neural networks against tree-based algorithms.
""")


# ==============================================================================
# SLIDE 7: Live Demonstration: The Real-Time Surveillance Dashboard
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "LIVE DEMONSTRATION: REAL-TIME SURVEILLANCE DASHBOARD", "SYSTEM ARTIFACT & DEMONSTRATION")
add_footer(slide7, 7)

# Left Column: Features of the Surveillance System
add_card(slide7, Inches(0.8), Inches(1.28), Inches(4.3), Inches(5.55), bg_color=C_BG_LIGHT)
tb7_l = slide7.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(3.9), Inches(5.2))
tf7_l = tb7_l.text_frame
tf7_l.word_wrap = True
tf7_l.margin_left = tf7_l.margin_top = tf7_l.margin_right = tf7_l.margin_bottom = 0

p = tf7_l.paragraphs[0]
r = p.add_run()
r.text = "WHAT BANK ANALYSTS SEE LIVE"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

dashboard_features = [
    ("Real-Time Red Alert Banner", "When a midnight drain is detected, the top banner flashes: 'Verdict: HIGH RISK OF FRAUDULENT ACCOUNT LIQUIDATION / SIM-SWAP DRAIN. Action Executed: Switch Transaction INTERCEPTED & Origin Account Held'."),
    ("Calibrated Risk Score Dial", "Displays instantaneous fraud probability from 0.00 to 1.00."),
    ("3-Tier Action Policy", "• Low Risk (< 0.35): Green - Auto-approved instantly.\n• Medium Risk (0.35 - 0.75): Amber - Soft hold; requests SMS OTP or fingerprint.\n• High Risk (> 0.75): Red - Hard intercept; transaction blocked immediately."),
    ("Live Switch Feed", "Continuously updates incoming transactions across the payment network for fraud ops."),
]
for title, desc in dashboard_features:
    p = tf7_l.add_paragraph()
    p.space_before = Pt(6)
    r1 = p.add_run()
    r1.text = f"• {title}:\n"
    set_font(r1, size=9.8, bold=True, color=C_CRIMSON if "Red" in title else C_BLUE_ACCENT)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.2, color=C_TEXT_DARK)

# Right Column: Prominent Dashboard Screenshot
add_card(slide7, Inches(5.3), Inches(1.28), Inches(7.233), Inches(5.55), bg_color=C_BG_LIGHT)
tb7_r = slide7.shapes.add_textbox(Inches(5.5), Inches(1.45), Inches(6.8), Inches(0.4))
tf7_r = tb7_r.text_frame
tf7_r.word_wrap = True
tf7_r.margin_left = tf7_r.margin_top = tf7_r.margin_right = tf7_r.margin_bottom = 0
p = tf7_r.paragraphs[0]
r = p.add_run()
r.text = "OPERATIONAL STREAMLIT SURVEILLANCE DASHBOARD"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide7,
    "screenshots/Dashboard.png",
    left=Inches(5.45),
    top=Inches(1.95),
    max_width=Inches(6.933),
    max_height=Inches(4.65),
    caption="Figure 4.3: Real-Time Fraud Surveillance Dashboard showing Instant Transaction Interception"
)

set_speaker_note(slide7, """
Distinguished examiners, on this slide you can see the actual, working software artifact running live—our Real-Time Fraud Surveillance Dashboard, built using Streamlit.

Imagine you are a fraud analyst at NIBSS, Interswitch, OPay, or a commercial bank. When an attack happens, you cannot be searching through lines of code or log files. You need an immediate, actionable interface.

Look at the top of the screenshot on the right: when a midnight SIM-swap drain is attempted, the system immediately flashes a bright red banner: 'Verdict: HIGH RISK OF FRAUDULENT ACCOUNT LIQUIDATION / SIM-SWAP DRAIN. Action Executed: Switch Transaction INTERCEPTED & Origin Account Held'. The transfer is stopped before money leaves the switch!

Right below the banner, the analyst sees a calibrated risk score dial. We implemented a 3-tier automated response policy:
If the risk score is below 0.35, it is green—auto-approved with zero delay.
If the score is between 0.35 and 0.75, it is amber—the system pauses and asks the user for a second factor, like a fingerprint or SMS OTP.
If the score exceeds 0.75, it is a critical red alert—the transaction is intercepted and the account is protected.

Below this, the dashboard provides a live stream of all incoming transactions across the network, giving the fraud team total situational awareness.
""")


# ==============================================================================
# SLIDE 8: Explainable Decisions & Real-Time Speed (TreeSHAP & FastAPI)
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "EXPLAINABLE DECISIONS & SUB-50MS SWITCH LATENCY", "REGULATORY COMPLIANCE & PRODUCTION VIABILITY")
add_footer(slide8, 8)

# Left Column: TreeSHAP Explainability
add_card(slide8, Inches(0.8), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb8_l = slide8.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(5.25), Inches(0.4))
tf8_l = tb8_l.text_frame
tf8_l.word_wrap = True
tf8_l.margin_left = tf8_l.margin_top = tf8_l.margin_right = tf8_l.margin_bottom = 0
p = tf8_l.paragraphs[0]
r = p.add_run()
r.text = "1. TREESHAP EXPLAINABILITY (CBN / NDPR COMPLIANCE)"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide8,
    "screenshots/Figure 4.4 (TreeSHAP Waterfall Plot).png",
    left=Inches(1.05),
    top=Inches(1.9),
    max_width=Inches(5.25),
    max_height=Inches(3.3),
    caption="Figure 4.4: TreeSHAP Waterfall Plot showing Feature-Level Risk Attribution"
)

tb8_lb = slide8.shapes.add_textbox(Inches(1.05), Inches(5.45), Inches(5.25), Inches(1.3))
tf8_lb = tb8_lb.text_frame
tf8_lb.word_wrap = True
tf8_lb.margin_left = tf8_lb.margin_top = tf8_lb.margin_right = tf8_lb.margin_bottom = 0
p = tf8_lb.paragraphs[0]
r = p.add_run()
r.text = "Why This Matters in Nigeria:"
set_font(r, size=10, bold=True, color=C_GOLD)
p = tf8_lb.add_paragraph()
r = p.add_run()
r.text = "Under Central Bank of Nigeria (CBN) rules, banks cannot freeze funds without giving reasons. TreeSHAP provides an exact mathematical receipt showing that isCompleteDrain (+0.42) and amountToBalanceRatio (+0.31) caused the block."
set_font(r, size=9.2, color=C_TEXT_DARK)

# Right Column: FastAPI Production Latency
add_card(slide8, Inches(6.783), Inches(1.28), Inches(5.75), Inches(5.55), bg_color=C_BG_LIGHT)
tb8_r = slide8.shapes.add_textbox(Inches(7.033), Inches(1.45), Inches(5.25), Inches(0.4))
tf8_r = tb8_r.text_frame
tf8_r.word_wrap = True
tf8_r.margin_left = tf8_r.margin_top = tf8_r.margin_right = tf8_r.margin_bottom = 0
p = tf8_r.paragraphs[0]
r = p.add_run()
r.text = "2. REST API GATEWAY & SUB-50MS SWITCH LATENCY"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide8,
    "screenshots/Figure 4.6 (REST API Gateway Endpoint).png",
    left=Inches(7.033),
    top=Inches(1.9),
    max_width=Inches(5.25),
    max_height=Inches(3.3),
    caption="Figure 4.6: Postman REST API Latency Benchmark (14.2 ms Execution Time)"
)

tb8_rb = slide8.shapes.add_textbox(Inches(7.033), Inches(5.45), Inches(5.25), Inches(1.3))
tf8_rb = tb8_rb.text_frame
tf8_rb.word_wrap = True
tf8_rb.margin_left = tf8_rb.margin_top = tf8_rb.margin_right = tf8_rb.margin_bottom = 0
p = tf8_rb.paragraphs[0]
r = p.add_run()
r.text = "Why Speed Matters for USSD & NIP:"
set_font(r, size=10, bold=True, color=C_GOLD)
p = tf8_rb.add_paragraph()
r = p.add_run()
r.text = "Telecom USSD sessions (*737#) timeout after just a few seconds, and switches have a strict 50ms SLA. As verified in Postman, our FastAPI service responds in 14.2 milliseconds—over 3 times faster than required!"
set_font(r, size=9.2, color=C_TEXT_DARK)

set_speaker_note(slide8, """
Two critical questions that bank executives and examiners will ask are: First, can this system explain why it blocked someone? And second, is it fast enough for real-world telecom and banking switches?

On the left side of this slide is our TreeSHAP waterfall plot. In Nigeria, the CBN Consumer Protection Framework and NDPR regulations mandate that financial institutions cannot treat customers unfairly using unexplained algorithms. With TreeSHAP, our model produces an instant audit receipt. In this example, you can see that `isCompleteDrain` pushed the risk up by +0.42, and `amountToBalanceRatio` pushed it up by +0.31. When an affected customer calls customer care, the bank representative can explain exactly what happened: 'Your account was flagged because someone attempted to transfer 100% of your balance.'

On the right side is our latency verification tested via Postman on our FastAPI gateway. In Nigeria, USSD sessions on MTN or Airtel drop if a bank's server takes more than a few seconds, and the internal switch timeout limit is 50 milliseconds. As demonstrated in Figure 4.6, our system processes the payload, runs feature engineering, scores the model, and responds in just 14.2 milliseconds! That is more than three times faster than the maximum allowed switch latency.
""")


# ==============================================================================
# SLIDE 9: Benchmark Results: Why XGBoost Won Over Deep Learning
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "BENCHMARK RESULTS: WHY XGBOOST WON OVER DEEP LEARNING", "EMPIRICAL BENCHMARK & MODEL SELECTION")
add_footer(slide9, 9)

# Left Column: Comprehensive Performance Table
add_card(slide9, Inches(0.8), Inches(1.28), Inches(6.8), Inches(5.55), bg_color=C_BG_LIGHT)
tb9_l = slide9.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(6.4), Inches(0.4))
tf9_l = tb9_l.text_frame
tf9_l.word_wrap = True
tf9_l.margin_left = tf9_l.margin_top = tf9_l.margin_right = tf9_l.margin_bottom = 0
p = tf9_l.paragraphs[0]
r = p.add_run()
r.text = "EMPIRICAL PERFORMANCE ON 1,272,524 BLIND TEST TRANSACTIONS"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

# Table of Results
rows, cols = 6, 6
table_shape = slide9.shapes.add_table(rows, cols, Inches(1.0), Inches(1.9), Inches(6.4), Inches(2.2))
tbl = table_shape.table
tbl.columns[0].width = Inches(1.7)
tbl.columns[1].width = Inches(0.9)
tbl.columns[2].width = Inches(0.9)
tbl.columns[3].width = Inches(0.9)
tbl.columns[4].width = Inches(1.0)
tbl.columns[5].width = Inches(1.0)

headers9 = ["Algorithm", "PR-AUC", "ROC-AUC", "Recall", "Precision", "FPR (False Alarms)"]
for col_idx, h_text in enumerate(headers9):
    cell = tbl.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_TABLE_HEADER
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = h_text
    set_font(r, size=8.5, bold=True, color=C_WHITE)

data9 = [
    ("Cost-Weighted XGBoost", "0.9996", "0.9997", "91.80%", "96.53%", "0.007% (Best)"),
    ("LightGBM", "0.9994", "0.9995", "91.05%", "95.80%", "0.009%"),
    ("Random Forest", "0.9991", "0.9992", "89.41%", "94.12%", "0.012%"),
    ("Logistic Regression", "0.7240", "0.8120", "62.30%", "45.10%", "0.184%"),
    ("Deep Autoencoder", "0.8841", "0.9410", "84.15%", "11.20%", "0.960% (High Chaos)"),
]
for row_idx, row_vals in enumerate(data9, start=1):
    for col_idx, val in enumerate(row_vals):
        cell = tbl.cell(row_idx, col_idx)
        cell.fill.solid()
        if "XGBoost" in row_vals[0]:
            cell.fill.fore_color.rgb = C_EMERALD_BG
        elif row_idx % 2 == 0:
            cell.fill.fore_color.rgb = C_TABLE_ROW_ALT
        else:
            cell.fill.fore_color.rgb = C_WHITE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = val
        is_best = "XGBoost" in row_vals[0] or "Best" in val
        is_bad = "High Chaos" in val or "0.960%" in val
        set_font(r, size=8.5, bold=is_best, color=C_EMERALD if is_best else (C_CRIMSON if is_bad else C_TEXT_DARK))

# Summary text below table
tb9_lb = slide9.shapes.add_textbox(Inches(1.0), Inches(4.25), Inches(6.4), Inches(2.4))
tf9_lb = tb9_lb.text_frame
tf9_lb.word_wrap = True
tf9_lb.margin_left = tf9_lb.margin_top = tf9_lb.margin_right = tf9_lb.margin_bottom = 0
p = tf9_lb.paragraphs[0]
r = p.add_run()
r.text = "THE PRACTICAL NIGERIAN IMPACT:"
set_font(r, size=10.5, bold=True, color=C_NAVY_PRIMARY)

analysis_points = [
    ("Why Deep Autoencoder Failed", "The Autoencoder had a Precision of only 11.2% and an FPR of 0.960%. In a Nigerian switch processing 5 million transactions daily, that would falsely freeze 48,000 innocent Nigerians every single day!"),
    ("Why Cost-Weighted XGBoost Won", "XGBoost achieved 91.80% Recall, 96.53% Precision, and an FPR of just 0.007%. In that same 5-million switch, it triggers only 35 false alarms in 500,000 transactions, while stopping 92 out of 100 criminals!"),
]
for title, desc in analysis_points:
    p = tf9_lb.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"• {title}: "
    set_font(r1, size=9.5, bold=True, color=C_CRIMSON if "Failed" in title else C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.0, color=C_TEXT_DARK)

# Right Column: PR Curve Visual
add_card(slide9, Inches(7.8), Inches(1.28), Inches(4.733), Inches(5.55), bg_color=C_BG_LIGHT)
tb9_r = slide9.shapes.add_textbox(Inches(8.0), Inches(1.45), Inches(4.333), Inches(0.4))
tf9_r = tb9_r.text_frame
tf9_r.word_wrap = True
tf9_r.margin_left = tf9_r.margin_top = tf9_r.margin_right = tf9_r.margin_bottom = 0
p = tf9_r.paragraphs[0]
r = p.add_run()
r.text = "PRECISION-RECALL (PR) CURVE"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

add_image_fitted(
    slide9,
    "models/pr_comparison.png",
    left=Inches(7.95),
    top=Inches(1.95),
    max_width=Inches(4.433),
    max_height=Inches(4.65),
    caption="Figure 4.5: Precision-Recall Curve showing XGBoost Superiority over Deep Learning"
)

set_speaker_note(slide9, """
This slide presents the core experimental results of this research, evaluating our models on the blind test set of over 1.27 million transactions.

Look at the table on the left and the Precision-Recall curve on the right. In academic circles, many people assume that 'Deep Learning is always superior to traditional machine learning'. But in real-world tabular fraud detection, the empirical evidence proves the exact opposite.

Notice the Deep Autoencoder in the bottom row. While it achieved an 84.15% recall, its precision was only 11.2%, and its False Positive Rate was 0.960%. In a payment switch like Interswitch or NIBSS that processes 5 million transactions a day, a 0.96% false positive rate means wrongfully blocking 48,000 innocent Nigerians every day! Imagine 48,000 people stranded at fuel stations, supermarkets, and hospital pharmacies. That would destroy public trust in cashless banking.

In contrast, our Cost-Weighted XGBoost model achieved a near-perfect PR-AUC of 0.9996, a Recall of 91.80%, and a Precision of 96.53%. Most importantly, its False Positive Rate was just 0.007%. In that same 5-million transaction volume, it triggers only 35 false alarms per 500,000 transactions, while stopping over 91 out of every 100 fraudulent attempts. This makes XGBoost the undisputed operational winner for Nigerian payment switches.
""")


# ==============================================================================
# SLIDE 10: Conclusion, Practical Value for Nigeria & Future Work
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "CONCLUSION, PRACTICAL VALUE FOR NIGERIA & FUTURE WORK", "PROJECT SUMMARY & STRATEGIC RECOMMENDATIONS")
add_footer(slide10, 10)

# 3 Horizontal Cards Layout
col_w = Inches(3.75)
col_h = Inches(5.55)

# Card 1: What We Achieved for Nigeria
add_card(slide10, Inches(0.8), Inches(1.28), col_w, col_h, bg_color=C_BG_LIGHT)
tb10_1 = slide10.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(3.35), Inches(5.2))
tf10_1 = tb10_1.text_frame
tf10_1.word_wrap = True
tf10_1.margin_left = tf10_1.margin_top = tf10_1.margin_right = tf10_1.margin_bottom = 0

p = tf10_1.paragraphs[0]
r = p.add_run()
r.text = "1. PRACTICAL VALUE FOR NIGERIA"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

achievements_ng = [
    ("Defending Normal Citizens", "Stops devastating midnight SIM-swap drains and phone theft liquidations before the victim even wakes up."),
    ("Protecting Cashless Inclusion", "Restores public trust in mobile money apps (OPay, PalmPay) and USSD banking across unbanked and rural communities."),
    ("Preventing Switch Panic", "With an FPR of only 0.007%, banks no longer suffer false-alarm fatigue, and innocent users are not falsely blocked at POS kiosks."),
    ("Telecom Compliance", "14.2ms latency allows seamless integration into NIBSS NIP and telecom USSD sessions without timeout drops."),
]
for title, desc in achievements_ng:
    p = tf10_1.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"• {title}:\n  "
    set_font(r1, size=9.8, bold=True, color=C_EMERALD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.0, color=C_TEXT_DARK)

# Card 2: Academic & Technical Contributions
add_card(slide10, Inches(4.783), Inches(1.28), col_w, col_h, bg_color=C_BG_LIGHT)
tb10_2 = slide10.shapes.add_textbox(Inches(4.983), Inches(1.45), Inches(3.35), Inches(5.2))
tf10_2 = tb10_2.text_frame
tf10_2.word_wrap = True
tf10_2.margin_left = tf10_2.margin_top = tf10_2.margin_right = tf10_2.margin_bottom = 0

p = tf10_2.paragraphs[0]
r = p.add_run()
r.text = "2. TECHNICAL CONTRIBUTIONS"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

contributions_tech = [
    ("Domain Feature Engineering", "Formulated 4 novel behavioral accounting indicators (Eq 3.1 - 3.4) capturing liquidation signatures."),
    ("Empirical Benchmark Proof", "Proved on 1.27M test transactions that Cost-Weighted Trees significantly outperform Deep Autoencoders on tabular fraud."),
    ("Leakage-Free Validation", "Demonstrated that Train-only SMOTE inside 5-Fold Stratified CV prevents optimistic evaluation bias."),
    ("Full Production Artifact", "Built an end-to-end working pipeline: FastAPI + Streamlit Dashboard + TreeSHAP explainability."),
]
for title, desc in contributions_tech:
    p = tf10_2.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"• {title}:\n  "
    set_font(r1, size=9.8, bold=True, color=C_BLUE_ACCENT)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.0, color=C_TEXT_DARK)

# Card 3: Future Work & Recommendations
add_card(slide10, Inches(8.766), Inches(1.28), col_w, col_h, bg_color=C_BG_LIGHT)
tb10_3 = slide10.shapes.add_textbox(Inches(8.966), Inches(1.45), Inches(3.35), Inches(5.2))
tf10_3 = tb10_3.text_frame
tf10_3.word_wrap = True
tf10_3.margin_left = tf10_3.margin_top = tf10_3.margin_right = tf10_3.margin_bottom = 0

p = tf10_3.paragraphs[0]
r = p.add_run()
r.text = "3. FUTURE WORK & NEXT STEPS"
set_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

future_work = [
    ("Graph Neural Networks (GNN)", "Extend the model to analyze transaction graphs, mapping out syndicate mule rings and coordinated money laundering hops across multiple fintechs."),
    ("Federated Learning", "Enable multiple Nigerian commercial banks and fintechs to train a shared fraud AI collaboratively without sharing sensitive customer personal data."),
    ("NIBSS Centralized Pilot", "Deploy this model as a pilot microservice inside the NIBSS Instant Payment (NIP) switch for real-time inter-bank fraud scoring."),
]
for title, desc in future_work:
    p = tf10_3.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"• {title}:\n  "
    set_font(r1, size=9.8, bold=True, color=C_GOLD)
    r2 = p.add_run()
    r2.text = desc
    set_font(r2, size=9.0, color=C_TEXT_DARK)

set_speaker_note(slide10, """
In conclusion, distinguished members of the panel, this project is not just a theoretical academic exercise; it is a practical, production-ready solution to one of Nigeria's most painful financial challenges.

By engineering behavioral accounting indicators that spot the exact signature of midnight SIM-swaps and account liquidations, we demonstrated that intelligent feature engineering beats dumb static rules.

By benchmarking five machine learning paradigms on over 1.27 million blind test transactions, we solved the false positive crisis—slashing false alarms to just 0.007% and saving tens of thousands of innocent Nigerians from wrongful account blocks.

And by deploying this as a 14.2-millisecond FastAPI service with an interactive surveillance dashboard and TreeSHAP explainability, we delivered an artifact that complies with Central Bank of Nigeria regulations and fits seamlessly into real-world payment switches.

For future work, I recommend expanding this architecture using Graph Neural Networks to map out criminal syndicate mule rings, and deploying Federated Learning so Nigerian banks can collaborate on fraud defense without sharing private customer records.

Thank you very much for your time, patience, and kind attention. I now welcome your questions, observations, and recommendations.
""")

prs.save(OUTPUT_FILE)
print(f"Successfully generated {OUTPUT_FILE} with 10 slides and embedded speaker notes!")
