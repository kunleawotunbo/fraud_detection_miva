"""
Builds the 10-Slide Final Master's Project Defence Presentation
Candidate: Olakunle Oladeji Awotunbo (2025/B/MIT/1384)
Degree: Master of Information Technology (MIT 8313)
Institution: Miva Open University, Abuja, Nigeria
Supervisor: Prof. Olushina Olawale Awe
Title: DESIGN AND IMPLEMENTATION OF A FRAUD DETECTION SYSTEM FOR MOBILE MONEY TRANSACTIONS IN NIGERIA
"""

import os
import sys
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

OUTPUT_PATH = "Olakunle_Awotunbo_MIT8313_Defence_Presentation.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Professional Academic Color Palette
C_NAVY_DARK = RGBColor(10, 25, 47)       # #0A192F
C_NAVY_PRIMARY = RGBColor(16, 42, 77)     # #102A4D
C_BLUE_ACCENT = RGBColor(26, 75, 140)     # #1A4B8C
C_GOLD = RGBColor(184, 134, 11)           # #B8860B
C_GOLD_LIGHT = RGBColor(254, 243, 199)    # #FEF3C7
C_EMERALD = RGBColor(22, 101, 52)         # #166534
C_EMERALD_BG = RGBColor(240, 253, 244)    # #F0FDF4
C_CRIMSON = RGBColor(153, 27, 27)         # #991B1B
C_CRIMSON_BG = RGBColor(254, 242, 242)    # #FEF2F2
C_TEXT_DARK = RGBColor(30, 41, 59)        # #1E293B
C_TEXT_MUTED = RGBColor(71, 85, 105)      # #475569
C_BG_LIGHT = RGBColor(248, 250, 252)      # #F8FAFC
C_BORDER = RGBColor(226, 232, 240)        # #E2E8F0
C_BORDER_DARK = RGBColor(203, 213, 225)   # #CBD5E1
C_WHITE = RGBColor(255, 255, 255)
C_TABLE_HEADER = RGBColor(16, 42, 77)
C_TABLE_ROW_ALT = RGBColor(241, 245, 249)

FONT_NAME = "Times New Roman"


def set_run_font(run, font_name=FONT_NAME, size=11, bold=False, italic=False, color=C_TEXT_DARK):
    """Utility to set font attributes on a text run."""
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color


def add_header(slide, title_text, category_text="MIVA OPEN UNIVERSITY • MIT 8313 FINAL PROJECT DEFENCE"):
    """Standardized academic defense slide header."""
    # Top Gold accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_GOLD
    top_line.line.fill.background()

    # Header text box
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.22), Inches(11.733), Inches(0.95))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    set_run_font(p_cat.runs[0] if p_cat.runs else p_cat.add_run(), size=9.5, bold=True, color=C_GOLD)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    set_run_font(p_title.runs[0] if p_title.runs else p_title.add_run(), size=20, bold=True, color=C_NAVY_PRIMARY)
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
    set_run_font(r1, size=9, color=C_TEXT_MUTED)

    r2 = p.add_run()
    r2.text = f"                                                                               Slide {slide_num} of {total_slides}"
    set_run_font(r2, size=9, bold=True, color=C_NAVY_PRIMARY)


def add_card(slide, left, top, width, height, bg_color=C_BG_LIGHT, border_color=C_BORDER):
    """Draws a subtle rounded rectangle container for content chunking."""
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
    """Adds an image keeping its aspect ratio within bounded container."""
    if not os.path.exists(img_path):
        print(f"Warning: Image {img_path} not found.")
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

    # Center within the box
    offset_x = left + (max_width - w) / 2
    offset_y = top + (max_height - h) / 2

    # Draw border shape behind picture
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
        set_run_font(r, size=9, italic=True, color=C_TEXT_MUTED)

    return pic


# ==============================================================================
# SLIDE 1: Title Slide (Formal Academic Defence Presentation)
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)

# Hero Background Card
hero = add_card(slide1, Inches(0.8), Inches(0.65), Inches(11.733), Inches(3.7), bg_color=C_NAVY_DARK, border_color=None)

# Top Gold Accent Band on Hero
hero_accent = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.08))
hero_accent.fill.solid()
hero_accent.fill.fore_color.rgb = C_GOLD
hero_accent.line.fill.background()

# Title text box
tb_hero = slide1.shapes.add_textbox(Inches(1.1), Inches(0.9), Inches(11.133), Inches(3.2))
tf1 = tb_hero.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

p_inst = tf1.paragraphs[0]
p_inst.alignment = PP_ALIGN.CENTER
r = p_inst.add_run()
r.text = "DEPARTMENT OF INFORMATION TECHNOLOGY • SCHOOL OF COMPUTING\nMIVA OPEN UNIVERSITY ABUJA, NIGERIA"
set_run_font(r, size=11, bold=True, color=C_GOLD)

p_deg = tf1.add_paragraph()
p_deg.alignment = PP_ALIGN.CENTER
p_deg.space_before = Pt(10)
r = p_deg.add_run()
r.text = "FINAL MASTER'S DEGREE PROJECT DEFENCE • MIT 8313"
set_run_font(r, size=12, bold=True, color=RGBColor(203, 213, 225))

p_t = tf1.add_paragraph()
p_t.alignment = PP_ALIGN.CENTER
p_t.space_before = Pt(12)
r = p_t.add_run()
r.text = "DESIGN AND IMPLEMENTATION OF A FRAUD DETECTION SYSTEM\nFOR MOBILE MONEY TRANSACTIONS IN NIGERIA"
set_run_font(r, size=23, bold=True, color=C_WHITE)

p_sub = tf1.add_paragraph()
p_sub.alignment = PP_ALIGN.CENTER
p_sub.space_before = Pt(10)
r = p_sub.add_run()
r.text = "An Explainable, Multi-Tier Anomaly Detection Architecture for High-Throughput Electronic Payment Rails"
set_run_font(r, size=12.5, italic=True, color=RGBColor(226, 232, 240))

# Bottom Left Card: Candidate Details
add_card(slide1, Inches(0.8), Inches(4.55), Inches(5.75), Inches(2.35), bg_color=C_BG_LIGHT)
tb_cand = slide1.shapes.add_textbox(Inches(1.05), Inches(4.7), Inches(5.25), Inches(2.05))
tfc = tb_cand.text_frame
tfc.word_wrap = True
tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0

p = tfc.paragraphs[0]
r = p.add_run()
r.text = "CANDIDATE INFORMATION"
set_run_font(r, size=11, bold=True, color=C_GOLD)

items_cand = [
    ("Candidate Name", "Olakunle Oladeji Awotunbo"),
    ("Matriculation No.", "2025/B/MIT/1384"),
    ("Degree Program", "Master of Information Technology (MIT)"),
    ("Institutional Email", "o.awotunbo6129@miva.edu.ng"),
    ("Academic Session", "November 2026"),
]
for label, val in items_cand:
    p = tfc.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"•  {label}: "
    set_run_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = val
    set_run_font(r2, size=10.5, color=C_NAVY_PRIMARY if "Name" in label else C_TEXT_DARK)

# Bottom Right Card: Supervision & Defense Details
add_card(slide1, Inches(6.783), Inches(4.55), Inches(5.75), Inches(2.35), bg_color=C_BG_LIGHT)
tb_sup = slide1.shapes.add_textbox(Inches(7.033), Inches(4.7), Inches(5.25), Inches(2.05))
tfs = tb_sup.text_frame
tfs.word_wrap = True
tfs.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0

p = tfs.paragraphs[0]
r = p.add_run()
r.text = "SUPERVISION & DEFENCE COMMITTEE"
set_run_font(r, size=11, bold=True, color=C_GOLD)

items_sup = [
    ("Project Supervisor", "Prof. Olushina Olawale Awe"),
    ("Supervisory Role", "Professor of Artificial Intelligence & Data Science"),
    ("Internal Examiner", "Dr. Morolake Lawrence"),
    ("Methodology", "Design Science Research (DSR Framework)"),
    ("Operational Rails", "NIBSS Instant Payments, USSD (*737#), Agency POS"),
]
for label, val in items_sup:
    p = tfs.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"•  {label}: "
    set_run_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = val
    set_run_font(r2, size=10.5, color=C_NAVY_PRIMARY if "Supervisor" in label else C_TEXT_DARK)

add_footer(slide1, 1)


# ==============================================================================
# SLIDE 2: Industry Context & Statement of the Problem
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Context, Vulnerability Landscape & Problem Statement", "CHAPTER 1: INTRODUCTION & PROBLEM FORMULATION")

# Left Column Card: Context & Threat Vectors
add_card(slide2, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s2_l = slide2.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(5.25), Inches(5.15))
tf2_l = tb_s2_l.text_frame
tf2_l.word_wrap = True
tf2_l.margin_left = tf2_l.margin_top = tf2_l.margin_right = tf2_l.margin_bottom = 0

p = tf2_l.paragraphs[0]
r = p.add_run()
r.text = "NIGERIAN MOBILE MONEY VULNERABILITIES"
set_run_font(r, size=12, bold=True, color=C_NAVY_PRIMARY)

bullet_ctx = [
    ("High-Throughput Financial Inclusion Rails:", "Mobile money processes trillions of Naira monthly across Nigeria via telecom-centric channels (USSD, mobile banking apps, and over 1.5 million agency POS terminals)."),
    ("SIM-Swap & Identity Hijacking Attacks:", "Syndicates intercept telecom authentication to execute total account drains, transferring entire ledger balances within seconds before subscribers can flag telco SIM-clones."),
    ("Nocturnal Velocity Spikes (1 AM – 5 AM):", "Exploiting off-peak clearing windows, fraudsters route illicit transfers through automated switches while legitimate account owners are asleep."),
    ("Multi-Hop Mule Structuring:", "Stolen balances are rapidly fragmented across freshly provisioned wallet networks and immediately liquidated at cash-in/cash-out (CICO) agent locations."),
    ("Financial Exclusion Fallout:", "Unmitigated fraud disproportionately victimizes unbanked and rural citizens, severely threatening Central Bank of Nigeria (CBN) cashless adoption initiatives."),
]
for title, text in bullet_ctx:
    p = tf2_l.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10.5, color=C_TEXT_DARK)

# Right Column Card: Identified Failure Modes
add_card(slide2, Inches(6.783), Inches(1.35), Inches(5.75), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s2_r = slide2.shapes.add_textbox(Inches(7.033), Inches(1.5), Inches(5.25), Inches(5.15))
tf2_r = tb_s2_r.text_frame
tf2_r.word_wrap = True
tf2_r.margin_left = tf2_r.margin_top = tf2_r.margin_right = tf2_r.margin_bottom = 0

p = tf2_r.paragraphs[0]
r = p.add_run()
r.text = "LIMITATIONS OF CONVENTIONAL SURVEILLANCE"
set_run_font(r, size=12, bold=True, color=C_CRIMSON)

bullet_lim = [
    ("Brittle Deterministic Rule Engines:", "Legacy switch rules (e.g. static flags on transfers > ₦500,000) fail against dynamic structuring and cannot adapt to evolving transactional behaviors."),
    ("The Extreme Imbalance Barrier (0.13% Fraud):", "Standard machine learning algorithms overwhelmed by 99.87% legitimate volume suffer severe minority class collapse, missing rare but catastrophic liquidation attacks."),
    ("The False Positive Rate (FPR) Crisis:", "Unsupervised anomaly detectors (Isolation Forests, Autoencoders) trigger excessive false alarms (> 1.5% FPR), halting tens of thousands of legitimate transactions and overwhelming fraud desks."),
    ("The 'Black-Box' Regulatory Dilemma:", "Complex deep learning ensembles lack interpretability, violating Central Bank of Nigeria (CBN) and NDPR mandates requiring transparent justifications for frozen consumer accounts."),
    ("USSD Network Latency Constraint:", "Switch scoring must execute in sub-50ms to prevent USSD telecom gateway session timeout drops during live mobile money clearance."),
]
for title, text in bullet_lim:
    p = tf2_r.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10.5, color=C_TEXT_DARK)

add_footer(slide2, 2)


# ==============================================================================
# SLIDE 3: Research Aim, Specific Objectives & Technical Scope
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Research Aim, Specific Objectives & Technical Scope", "CHAPTER 1: RESEARCH GOALS & TECHNICAL MANDATE")

# Top Aim Card
add_card(slide3, Inches(0.8), Inches(1.35), Inches(11.733), Inches(1.25), bg_color=C_NAVY_DARK, border_color=None)
tb_aim = slide3.shapes.add_textbox(Inches(1.05), Inches(1.45), Inches(11.233), Inches(1.05))
tf_aim = tb_aim.text_frame
tf_aim.word_wrap = True
tf_aim.margin_left = tf_aim.margin_top = tf_aim.margin_right = tf_aim.margin_bottom = 0

p = tf_aim.paragraphs[0]
r = p.add_run()
r.text = "RESEARCH AIM"
set_run_font(r, size=11, bold=True, color=C_GOLD)

p = tf_aim.add_paragraph()
p.space_before = Pt(4)
r = p.add_run()
r.text = "To design, implement, and benchmark an adaptive, explainable fraud surveillance system tailored to Nigerian mobile money transaction topologies, resolving the trade-off between minority class detection sensitivity, sub-15ms operational latency, and regulatory audit compliance."
set_run_font(r, size=12.5, bold=True, color=C_WHITE)

# 4 Specific Objectives in a 2x2 Grid
obj_data = [
    ("Objective 1: Domain Invariant Engineering",
     "Formulate mathematical ledger accounting indicators (Equations 3.1 – 3.4) capturing origin/destination discrepancies, complete account drainage, and capital liquidation ratios to detect illegal state transitions.",
     C_BLUE_ACCENT),
    ("Objective 2: Leakage-Free Imbalance Strategy",
     "Establish an isolated 5-fold Stratified Cross-Validation protocol with train-only SMOTE oversampling and cost-sensitive weighting, eliminating data leakage and ensuring robust generalization on 0.13% fraud.",
     C_NAVY_PRIMARY),
    ("Objective 3: Dual-Paradigm Algorithmic Benchmark",
     "Empirically compare supervised algorithms (Cost-Weighted XGBoost, LSTM) against unsupervised neural reconstruction models (PyTorch Deep Autoencoder, Isolation Forest) under identical stratified validation splits.",
     C_EMERALD),
    ("Objective 4: Production Deployment & XAI",
     "Develop an operational Streamlit executive surveillance dashboard with local TreeSHAP attribution and a containerized, sub-15ms FastAPI REST gateway meeting CBN and NDPR regulatory standards.",
     C_GOLD),
]

grid_positions = [
    (Inches(0.8), Inches(2.8), Inches(5.75), Inches(1.95)),
    (Inches(6.783), Inches(2.8), Inches(5.75), Inches(1.95)),
    (Inches(0.8), Inches(4.9), Inches(5.75), Inches(1.95)),
    (Inches(6.783), Inches(4.9), Inches(5.75), Inches(1.95)),
]

for (title, desc, col), (x, y, w, h) in zip(obj_data, grid_positions):
    add_card(slide3, x, y, w, h, bg_color=C_BG_LIGHT)
    tb = slide3.shapes.add_textbox(x + Inches(0.25), y + Inches(0.18), w - Inches(0.5), h - Inches(0.35))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    set_run_font(r, size=11.5, bold=True, color=col)

    p = tf.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run()
    r.text = desc
    set_run_font(r, size=10.5, color=C_TEXT_DARK)

add_footer(slide3, 3)


# ==============================================================================
# SLIDE 4: Research Methodology (Design Science Research Framework)
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Research Methodology: Design Science Research (DSR)", "CHAPTER 3: METHODOLOGICAL FRAMEWORK & DATA MODELING")

# Left Column Card: DSR Lifecycle & Data Engine
add_card(slide4, Inches(0.8), Inches(1.35), Inches(6.5), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s4 = slide4.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(6.0), Inches(5.2))
tf4 = tb_s4.text_frame
tf4.word_wrap = True
tf4.margin_left = tf4.margin_top = tf4.margin_right = tf4.margin_bottom = 0

p = tf4.paragraphs[0]
r = p.add_run()
r.text = "THE 6-STAGE DSR LIFECYCLE (Peffers et al. & Hevner et al.)"
set_run_font(r, size=11.5, bold=True, color=C_NAVY_PRIMARY)

dsr_steps = [
    ("1. Problem Identification:", "Documented escalating mobile money fraud in Nigeria, sub-50ms USSD latency caps, and the high false alarm rate of current unsupervised tools."),
    ("2. Objectives Definition:", "Targeted sub-15ms inference latency, PR-AUC > 0.95, FPR < 0.05%, and compliance with NDPR data protection mandates."),
    ("3. Artifact Design & Dev:", "Engineered mathematical ledger invariants (Eq 3.1–3.4), Cost-Weighted XGBoost, PyTorch Autoencoder, and TreeSHAP explainers."),
    ("4. Demonstration:", "Built an enterprise Streamlit dashboard (`app.py`) for live scoring and a containerized FastAPI REST scoring gateway (`api.py`)."),
    ("5. Empirical Evaluation:", "Conducted 5-fold Stratified Cross-Validation on 1,048,575 transactions, latency profiling, and formal unit testing (TC-01 to TC-06)."),
    ("6. Communication:", "Authored academic thesis, created open reproducible GitHub repository, and delivered technical defense presentation."),
]
for step, desc in dsr_steps:
    p = tf4.add_paragraph()
    p.space_before = Pt(5)
    r1 = p.add_run()
    r1.text = f"•  {step} "
    set_run_font(r1, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = desc
    set_run_font(r2, size=10, color=C_TEXT_DARK)

p_div = tf4.add_paragraph()
p_div.space_before = Pt(8)
r = p_div.add_run()
r.text = "SYNTHETIC NIGERIAN TRANSACTION DATASET ENGINE"
set_run_font(r, size=11.5, bold=True, color=C_GOLD)

p_dat = tf4.add_paragraph()
p_dat.space_before = Pt(4)
r = p_dat.add_run()
r.text = "Generated 1,048,575 records modeling authentic Nigerian mobile payment primitives (TRANSFER, CASH_OUT, PAYMENT, CASH_IN, DEBIT) at 0.13% true fraud prevalence, nocturnal velocity anomalies, and SIM-swap liquidation patterns."
set_run_font(r, size=10, color=C_TEXT_DARK)

# Right Column Card: DSR Diagram Image
add_card(slide4, Inches(7.5), Inches(1.35), Inches(5.033), Inches(5.5), bg_color=C_BG_LIGHT)
img_p1 = os.path.join("screenshots", "Figure 3.1 - Design Science Research.jpeg")
add_image_fitted(slide4, img_p1, Inches(7.7), Inches(1.5), Inches(4.633), Inches(4.8), 
                 caption="Figure 3.1: Design Science Research (DSR) Iteration Lifecycle applied to the Surveillance Engine")

add_footer(slide4, 4)


# ==============================================================================
# SLIDE 5: System Architecture & Mathematical Invariant Formulations
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "System Architecture & Mathematical Ledger Invariants", "CHAPTER 3: ARCHITECTURAL SPECIFICATION & FORMULATION")

# Left Column Card: Multi-Tier Pipeline & Equations
add_card(slide5, Inches(0.8), Inches(1.35), Inches(6.8), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s5 = slide5.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(6.3), Inches(5.2))
tf5 = tb_s5.text_frame
tf5.word_wrap = True
tf5.margin_left = tf5.margin_top = tf5.margin_right = tf5.margin_bottom = 0

p = tf5.paragraphs[0]
r = p.add_run()
r.text = "FOUR-TIER REAL-TIME SURVEILLANCE PIPELINE"
set_run_font(r, size=11.5, bold=True, color=C_NAVY_PRIMARY)

tiers = [
    ("Tier 1: Ingestion & Privacy:", "Receives raw payload, computes cryptographic SHA-256 salted account hashes, eliminating unmasked PII storage in compliance with NDPR."),
    ("Tier 2: Sanitization & Invariants:", "Imputes negative balances to 0.0 with audit warnings (TC-01) and extracts mathematical ledger invariants (Eq 3.1 – 3.4)."),
    ("Tier 3: Dual-Paradigm Inference:", "Computes posterior fraud probability via Cost-Weighted XGBoost with real-time TreeSHAP local feature attribution."),
    ("Tier 4: Regulatory Action Dispatch:", "Triages decisions into Low Risk (ALLOW), Suspicious Review (CHALLENGE), or Critical Block (INTERCEPT) under 15ms."),
]
for t_name, t_desc in tiers:
    p = tf5.add_paragraph()
    p.space_before = Pt(5)
    r1 = p.add_run()
    r1.text = f"•  {t_name} "
    set_run_font(r1, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = t_desc
    set_run_font(r2, size=10, color=C_TEXT_DARK)

p_eq_h = tf5.add_paragraph()
p_eq_h.space_before = Pt(8)
r = p_eq_h.add_run()
r.text = "MATHEMATICAL LEDGER INVARIANTS (CHAPTER 3.5)"
set_run_font(r, size=11.5, bold=True, color=C_GOLD)

eqs = [
    ("Eq 3.1: Origin Ledger Error", "errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig"),
    ("Eq 3.2: Destination Ledger Error", "errorBalanceDest = oldbalanceDest + amount - newbalanceDest"),
    ("Eq 3.3: Complete Account Drain", "isCompleteDrain = 1.0  if  (newbalanceOrig == 0 and amount > 0)  else  0.0"),
    ("Eq 3.4: Capital Liquidation Ratio", "amountToBalanceRatio = amount / (oldbalanceOrg + 1e-5)"),
]
for eq_name, formula in eqs:
    p = tf5.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"•  {eq_name}: "
    set_run_font(r1, size=9.5, bold=True, color=C_NAVY_PRIMARY)
    r2 = p.add_run()
    r2.text = formula
    set_run_font(r2, size=9.5, italic=True, color=C_CRIMSON if "Drain" in eq_name else C_TEXT_DARK)

# Right Column Card: Architecture Diagram
add_card(slide5, Inches(7.8), Inches(1.35), Inches(4.733), Inches(5.5), bg_color=C_BG_LIGHT)
img_p2 = os.path.join("screenshots", "Figure 3.2 - High-Level Multi-Tier.png")
add_image_fitted(slide5, img_p2, Inches(8.0), Inches(1.5), Inches(4.333), Inches(4.8),
                 caption="Figure 3.2: High-Level Multi-Tier System Architecture Diagram")

add_footer(slide5, 5)


# ==============================================================================
# SLIDE 6: Model Implementation & Class Imbalance Strategy
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Model Implementation & Imbalance Handling Strategy", "CHAPTER 4: ARTIFACT IMPLEMENTATION & PIPELINE ISOLATION")

# Left Column Card: Pipeline Isolation & SMOTE
add_card(slide6, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s6_l = slide6.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(5.25), Inches(5.15))
tf6_l = tb_s6_l.text_frame
tf6_l.word_wrap = True
tf6_l.margin_left = tf6_l.margin_top = tf6_l.margin_right = tf6_l.margin_bottom = 0

p = tf6_l.paragraphs[0]
r = p.add_run()
r.text = "HANDLING 0.13% CLASS ASYMMETRY WITHOUT LEAKAGE"
set_run_font(r, size=11.5, bold=True, color=C_NAVY_PRIMARY)

imb_points = [
    ("The Data Leakage Vulnerability:", "Resampling entire datasets prior to cross-validation introduces synthetic minority vectors into test sets, creating severe data leakage and artificially inflated performance."),
    ("Strict Cross-Validation Pipeline Isolation:", "In this study, SMOTE oversampling is strictly executed inside training folds only. Evaluation test folds remain 100% natural, unmanipulated, and leak-free (verified in TC-02)."),
    ("Cost-Sensitive Loss Weighting:", "Configured scale_pos_weight = N_neg / N_pos = 761.6 in the XGBoost objective function, penalizing false negatives 761 times more heavily to ensure high minority recall."),
    ("Categorical Primitive Preservation:", "Payment primitives (TRANSFER, CASH_OUT, PAYMENT, etc.) are one-hot encoded without dense dimensionality reduction to retain channel-specific fraud patterns."),
]
for title, text in imb_points:
    p = tf6_l.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10.5, color=C_TEXT_DARK)

# Right Column Card: Models Evaluated & Autoencoder Diagram
add_card(slide6, Inches(6.783), Inches(1.35), Inches(5.75), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s6_r = slide6.shapes.add_textbox(Inches(7.033), Inches(1.5), Inches(5.25), Inches(2.3))
tf6_r = tb_s6_r.text_frame
tf6_r.word_wrap = True
tf6_r.margin_left = tf6_r.margin_top = tf6_r.margin_right = tf6_r.margin_bottom = 0

p = tf6_r.paragraphs[0]
r = p.add_run()
r.text = "MODEL ARCHITECTURES IMPLEMENTED"
set_run_font(r, size=11.5, bold=True, color=C_GOLD)

models_eval = [
    ("1. Cost-Weighted XGBoost:", "100 estimators, max depth 6, histogram splitting (tree_method='hist') optimizing PR-AUC."),
    ("2. PyTorch Deep Autoencoder:", "10 -> 32 -> 16 -> 8 -> 16 -> 32 -> 10 symmetric manifold with BatchNorm1d and LeakyReLU(0.2)."),
    ("3. LSTM Sequence Tracker:", "2-layer recurrent network tracking temporal account state evolution across time steps."),
    ("4. Isolation Forest Baseline:", "100 trees parameterized to 0.13% contamination factor."),
]
for title, text in models_eval:
    p = tf6_r.add_paragraph()
    p.space_before = Pt(3)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10, color=C_TEXT_DARK)

img_ae = os.path.join("screenshots", "Figure 4.1- Deep Autoencoder Neural Reconst Archi.png")
add_image_fitted(slide6, img_ae, Inches(7.033), Inches(4.0), Inches(5.25), Inches(2.6),
                 caption="Figure 4.1: PyTorch Symmetric Deep Autoencoder Neural Reconstruction Architecture")

add_footer(slide6, 6)


# ==============================================================================
# SLIDE 7: Operational Demonstration: Executive Surveillance Dashboard
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Operational Demonstration: Streamlit Surveillance Console", "CHAPTER 4: EXECUTIVE INTERFACE & OPERATIONAL RUNTIME")

# Top Banner: Capabilities Summary
add_card(slide7, Inches(0.8), Inches(1.35), Inches(11.733), Inches(1.05), bg_color=C_BG_LIGHT)
tb_s7 = slide7.shapes.add_textbox(Inches(1.05), Inches(1.42), Inches(11.233), Inches(0.9))
tf7 = tb_s7.text_frame
tf7.word_wrap = True
tf7.margin_left = tf7.margin_top = tf7.margin_right = tf7.margin_bottom = 0

p = tf7.paragraphs[0]
r = p.add_run()
r.text = "EXECUTIVE DECISION SUPPORT & FRAUD TRIAGE ARCHITECTURE"
set_run_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

p = tf7.add_paragraph()
p.space_before = Pt(3)
r = p.add_run()
r.text = "• Three Operational Consoles: (1) Single Transaction Real-Time Inspector, (2) Batch Switch CSV Auditor (1,000+ tx/sec), (3) Algorithmic Benchmark Matrix.\n• Three Action Tiers: Low Risk (<0.30: ALLOW), Suspicious Review (0.30–0.70: CHALLENGE with Biometric OTP), Critical (>0.70: BLOCK & Account Held)."
set_run_font(r, size=10, color=C_TEXT_DARK)

# Main Dashboard Screenshot (Prominent display of Dashboard.png)
img_dash = os.path.join("screenshots", "Dashboard.png")
add_image_fitted(slide7, img_dash, Inches(0.8), Inches(2.55), Inches(11.733), Inches(4.25),
                 caption="Figure 4.2: Streamlit Executive Surveillance Dashboard — Real-time Transaction Scoring, Anomaly Audit, and USSD Latency Profiling")

add_footer(slide7, 7)


# ==============================================================================
# SLIDE 8: Regulatory Explainability & REST Gateway (TreeSHAP & FastAPI)
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Regulatory Explainability & Cloud REST Scoring Gateway", "CHAPTER 4: EXPLAINABLE AI & CLOUD MICROSERVICE RUNTIME")

# Left Column Card: TreeSHAP Explainability
add_card(slide8, Inches(0.8), Inches(1.35), Inches(5.75), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s8_l = slide8.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(5.25), Inches(2.1))
tf8_l = tb_s8_l.text_frame
tf8_l.word_wrap = True
tf8_l.margin_left = tf8_l.margin_top = tf8_l.margin_right = tf8_l.margin_bottom = 0

p = tf8_l.paragraphs[0]
r = p.add_run()
r.text = "LOCAL TREESHAP ATTRIBUTION (FIGURE 4.4)"
set_run_font(r, size=11.5, bold=True, color=C_NAVY_PRIMARY)

shap_points = [
    ("Solving the Black-Box Dilemma:", "Decomposes the model's log-odds margin into exact additive Shapley feature contributions (phi_i) for every scored transaction."),
    ("Fulfilling Regulatory Mandates:", "Directly complies with Central Bank of Nigeria (CBN) and NDPR mandates requiring auditable justifications for administrative account freezes."),
    ("Dominant Risk Drivers in Drains:", "SIM-swap liquidations exhibit heavy positive attribution on isCompleteDrain (+0.412), errorBalanceOrig (+0.334), and liquidation ratio (+0.185)."),
]
for title, text in shap_points:
    p = tf8_l.add_paragraph()
    p.space_before = Pt(3)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=9.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=9.5, color=C_TEXT_DARK)

img_shap = os.path.join("screenshots", "Figure 4.4 (TreeSHAP Waterfall Plot).png")
add_image_fitted(slide8, img_shap, Inches(1.05), Inches(3.75), Inches(5.25), Inches(2.9),
                 caption="Figure 4.4: TreeSHAP Local Feature Attribution Waterfall Plot for a Critical Block Verdict")

# Right Column Card: Cloud REST Gateway (FastAPI)
add_card(slide8, Inches(6.783), Inches(1.35), Inches(5.75), Inches(5.5), bg_color=C_BG_LIGHT)
tb_s8_r = slide8.shapes.add_textbox(Inches(7.033), Inches(1.5), Inches(5.25), Inches(2.1))
tf8_r = tb_s8_r.text_frame
tf8_r.word_wrap = True
tf8_r.margin_left = tf8_r.margin_top = tf8_r.margin_right = tf8_r.margin_bottom = 0

p = tf8_r.paragraphs[0]
r = p.add_run()
r.text = "ASYNCHRONOUS FASTAPI REST GATEWAY (FIGURE 4.6)"
set_run_font(r, size=11.5, bold=True, color=C_GOLD)

api_points = [
    ("High-Throughput Scoring Endpoint:", "Exposes POST /api/v1/score-transaction with asynchronous request pipelining and Pydantic V2 schema validation."),
    ("NDPR Salted SHA-256 Hashing:", "Pseudonymizes account identifiers on ingestion, guaranteeing that zero unmasked customer PII is logged in transaction histories."),
    ("Sub-15ms Latency Budget (USSD Proof):", "Profiled in Postman at 14.2 ms mean latency, comfortably clearing the strict < 50 ms USSD session drop timeout."),
]
for title, text in api_points:
    p = tf8_r.add_paragraph()
    p.space_before = Pt(3)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=9.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=9.5, color=C_TEXT_DARK)

img_api = os.path.join("screenshots", "Figure 4.6 (REST API Gateway Endpoint).png")
add_image_fitted(slide8, img_api, Inches(7.033), Inches(3.75), Inches(5.25), Inches(2.9),
                 caption="Figure 4.6: REST API Gateway Endpoint Latency Profiling in Postman (Sub-15ms Validation)")

add_footer(slide8, 8)


# ==============================================================================
# SLIDE 9: Empirical Benchmark Evaluation & Key Findings (Tables 5.2 & 5.3)
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Empirical Benchmark Results & Comparative Analysis", "CHAPTER 5: EVALUATION, BENCHMARK TABLES & DISCUSSION")

# Table Card Container
add_card(slide9, Inches(0.8), Inches(1.35), Inches(11.733), Inches(2.7), bg_color=C_WHITE)

# Insert Table 5.2 / 5.3
rows, cols = 5, 8
table_shape = slide9.shapes.add_table(rows, cols, Inches(0.9), Inches(1.45), Inches(11.533), Inches(2.45))
table = table_shape.table

# Set Column Widths
table.columns[0].width = Inches(2.533)  # Model Name
table.columns[1].width = Inches(1.25)   # PR-AUC
table.columns[2].width = Inches(1.25)   # ROC-AUC
table.columns[3].width = Inches(1.3)    # Precision
table.columns[4].width = Inches(1.3)    # Recall
table.columns[5].width = Inches(1.3)    # F1-Score
table.columns[6].width = Inches(1.2)    # FPR
table.columns[7].width = Inches(1.4)    # Latency

headers = ["Evaluated Model Architecture", "PR-AUC", "ROC-AUC", "Precision", "Recall", "F1-Score", "FPR (%)", "Mean Latency"]
data_table = [
    ["Cost-Weighted XGBoost (Proposed)", "0.9841", "0.9992", "94.12%", "91.80%", "0.9295", "0.007%", "14.2 ms"],
    ["LSTM Recurrent Sequence Model", "0.9120", "0.9785", "88.42%", "89.45%", "0.8893", "0.060%", "28.5 ms"],
    ["PyTorch Deep Autoencoder", "0.3862", "0.9410", "31.45%", "84.00%", "0.4574", "0.960%", "8.4 ms"],
    ["Isolation Forest (Unsupervised)", "0.2104", "0.8872", "18.24%", "78.18%", "0.2957", "1.840%", "2.1 ms"],
]

for col_idx, h_text in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_TABLE_HEADER
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
    r = p.add_run()
    r.text = h_text
    set_run_font(r, size=10, bold=True, color=C_WHITE)

for row_idx, row_data in enumerate(data_table):
    is_best = (row_idx == 0)
    for col_idx, val in enumerate(row_data):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        if is_best:
            cell.fill.fore_color.rgb = C_GOLD_LIGHT
        elif row_idx % 2 == 1:
            cell.fill.fore_color.rgb = C_TABLE_ROW_ALT
        else:
            cell.fill.fore_color.rgb = C_WHITE

        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
        r = p.add_run()
        r.text = val
        set_run_font(r, size=10, bold=is_best, color=C_CRIMSON if (is_best and col_idx in [1, 5, 6]) else C_TEXT_DARK)

# Bottom Analytical Discussion Cards (2 Cards)
add_card(slide9, Inches(0.8), Inches(4.2), Inches(6.8), Inches(2.65), bg_color=C_BG_LIGHT)
tb_disc = slide9.shapes.add_textbox(Inches(1.05), Inches(4.35), Inches(6.3), Inches(2.35))
tf_d = tb_disc.text_frame
tf_d.word_wrap = True
tf_d.margin_left = tf_d.margin_top = tf_d.margin_right = tf_d.margin_bottom = 0

p = tf_d.paragraphs[0]
r = p.add_run()
r.text = "KEY EMPIRICAL FINDINGS (TABLE 5.2 & 5.3 ANALYSIS)"
set_run_font(r, size=11, bold=True, color=C_NAVY_PRIMARY)

findings = [
    ("The False Positive Crisis in Unsupervised Learning:", "While the Deep Autoencoder attained 84.00% recall, its 0.960% FPR blocks ~9,600 legitimate transactions per million. Cost-Weighted XGBoost's 0.007% FPR cuts false alarms by >99%, preserving customer convenience."),
    ("Superiority of Cost-Weighted Gradient Tree Boosting:", "XGBoost decisively outperformed all baselines, achieving PR-AUC = 0.9841 and F1 = 0.9295, demonstrating that histogram-based decision trees capture non-linear tabular ledger interactions far better than neural manifolds."),
    ("Strict USSD Network Budget Compliance:", "At 14.2 ms mean inference latency, XGBoost operates at under 30% of the maximum 50 ms USSD session drop threshold, ensuring zero dropped payments."),
]
for title, text in findings:
    p = tf_d.add_paragraph()
    p.space_before = Pt(4)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=9.5, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=9.5, color=C_TEXT_DARK)

# PR Curve Thumbnail / Image Card
add_card(slide9, Inches(7.8), Inches(4.2), Inches(4.733), Inches(2.65), bg_color=C_BG_LIGHT)
img_pr = os.path.join("models", "pr_comparison.png")
add_image_fitted(slide9, img_pr, Inches(7.95), Inches(4.3), Inches(4.433), Inches(2.2),
                 caption="Figure 5.2: Precision-Recall (PR) Curve Benchmark on 0.13% Imbalanced Stream")

add_footer(slide9, 9)


# ==============================================================================
# SLIDE 10: Conclusion, Contributions & Recommendations
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Conclusions, Contributions & Future Work", "CHAPTER 6: SUMMARY, CONCLUSION & RECOMMENDATIONS")

# Three Equal Cards Layout
card_w = Inches(3.75)
card_gap = Inches(0.24)
card_top = Inches(1.35)
card_h = Inches(5.5)

# Card 1: Conclusions
c1_x = Inches(0.8)
add_card(slide10, c1_x, card_top, card_w, card_h, bg_color=C_BG_LIGHT)
tb1 = slide10.shapes.add_textbox(c1_x + Inches(0.25), card_top + Inches(0.2), card_w - Inches(0.5), card_h - Inches(0.4))
tf10_1 = tb1.text_frame
tf10_1.word_wrap = True
tf10_1.margin_left = tf10_1.margin_top = tf10_1.margin_right = tf10_1.margin_bottom = 0

p = tf10_1.paragraphs[0]
r = p.add_run()
r.text = "RESEARCH CONCLUSIONS"
set_run_font(r, size=11.5, bold=True, color=C_NAVY_PRIMARY)

concls = [
    ("Resolution of the Trilemma:", "Proved that domain-engineered accounting invariants coupled with cost-weighted gradient boosting resolve the trade-off between detection sensitivity, USSD latency constraints, and operational false positive rates."),
    ("Tabular Feature Supremacy:", "Demonstrated that explicit ledger discrepancies (Equations 3.1–3.4) provide stronger predictive signals than purely data-driven neural autoencoder reconstruction errors."),
    ("Regulatory Feasibility:", "Validated that machine learning can operate within strict CBN consumer protection guidelines when paired with local TreeSHAP explainability."),
]
for title, text in concls:
    p = tf10_1.add_paragraph()
    p.space_before = Pt(8)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10, color=C_TEXT_DARK)

# Card 2: Professional & Practical Contributions
c2_x = c1_x + card_w + card_gap
add_card(slide10, c2_x, card_top, card_w, card_h, bg_color=C_BG_LIGHT)
tb2 = slide10.shapes.add_textbox(c2_x + Inches(0.25), card_top + Inches(0.2), card_w - Inches(0.5), card_h - Inches(0.4))
tf10_2 = tb2.text_frame
tf10_2.word_wrap = True
tf10_2.margin_left = tf10_2.margin_top = tf10_2.margin_right = tf10_2.margin_bottom = 0

p = tf10_2.paragraphs[0]
r = p.add_run()
r.text = "PROFESSIONAL CONTRIBUTIONS"
set_run_font(r, size=11.5, bold=True, color=C_GOLD)

contribs = [
    ("Production FinTech Blueprint:", "Delivered a fully functional, containerized software stack (FastAPI, Streamlit, Docker) ready for enterprise deployment in Nigerian payment switches."),
    ("Regulatory XAI Framework:", "Created an auditable TreeSHAP feature attribution pipeline fulfilling Central Bank of Nigeria (CBN) and NDPR administrative hold requirements."),
    ("Standardized Accounting Invariants:", "Formulated open, mathematically verified mobile money accounting invariants (origin/dest balance errors, complete drain flags, liquidation ratios)."),
    ("Miva MIT Academic Benchmark:", "Established rigorous baseline metrics for financial fraud research within emerging Sub-Saharan African electronic payment ecosystems."),
]
for title, text in contribs:
    p = tf10_2.add_paragraph()
    p.space_before = Pt(6)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10, color=C_TEXT_DARK)

# Card 3: Actionable Future Recommendations
c3_x = c2_x + card_w + card_gap
add_card(slide10, c3_x, card_top, card_w, card_h, bg_color=C_BG_LIGHT)
tb3 = slide10.shapes.add_textbox(c3_x + Inches(0.25), card_top + Inches(0.2), card_w - Inches(0.5), card_h - Inches(0.4))
tf10_3 = tb3.text_frame
tf10_3.word_wrap = True
tf10_3.margin_left = tf10_3.margin_top = tf10_3.margin_right = tf10_3.margin_bottom = 0

p = tf10_3.paragraphs[0]
r = p.add_run()
r.text = "RECOMMENDATIONS FOR FUTURE WORK"
set_run_font(r, size=11.5, bold=True, color=C_EMERALD)

recomms = [
    ("Dynamic Graph Neural Networks (GNNs):", "Transition from isolated transaction scoring to graph-level modeling of multi-hop mule account topologies and syndicate ring structures."),
    ("Distributed Event Streaming (Kafka):", "Integrate the FastAPI scoring engine directly with Apache Kafka or Redpanda clusters for horizontal scaling across national payment switches."),
    ("Edge ONNX Model Quantization:", "Quantize gradient boosting and neural estimators into ONNX/TFLite for sub-5ms offline execution directly on agency banking Android POS hardware."),
    ("Continuous Drift Adaptation:", "Deploy online learning mechanisms to autonomously adapt feature weights as fraudsters alter transaction velocity and amounts."),
]
for title, text in recomms:
    p = tf10_3.add_paragraph()
    p.space_before = Pt(6)
    r1 = p.add_run()
    r1.text = f"•  {title} "
    set_run_font(r1, size=10, bold=True, color=C_TEXT_DARK)
    r2 = p.add_run()
    r2.text = text
    set_run_font(r2, size=10, color=C_TEXT_DARK)

add_footer(slide10, 10)


# Save presentation
prs.save(OUTPUT_PATH)
print(f"Successfully generated {OUTPUT_PATH} ({len(prs.slides)} slides)!")
