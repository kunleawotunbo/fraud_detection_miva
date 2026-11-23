"""
Generates a Professional PDF Defense Preparation Guide:
Miva Open University - School of Computing
Master of Information Technology (MIT 8313)
Candidate: Olakunle Oladeji Awotunbo (2025/B/MIT/1384)
Supervisor: Prof. Olushina Olawale Awe
Title: DESIGN AND IMPLEMENTATION OF A FRAUD DETECTION SYSTEM FOR MOBILE MONEY TRANSACTIONS IN NIGERIA
"""

import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas

PDF_FILENAME = "Olakunle_Awotunbo_MIT8313_Defence_QA_Guide.pdf"

# Color Palette
C_NAVY_DARK = HexColor("#0A192F")
C_NAVY_PRIMARY = HexColor("#102A4D")
C_BLUE_ACCENT = HexColor("#1E4B87")
C_NAVY_LIGHT = HexColor("#EBF3FC")
C_GOLD = HexColor("#B8860B")
C_GOLD_LIGHT = HexColor("#FEF9C3")
C_EMERALD = HexColor("#166534")
C_CRIMSON = HexColor("#991B1B")
C_TEXT_DARK = HexColor("#1E293B")
C_TEXT_MUTED = HexColor("#475569")
C_BG_CARD = HexColor("#F8FAFC")
C_BORDER = HexColor("#CBD5E1")
C_LINE = HexColor("#E2E8F0")


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' footers
    and professional running headers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setFillColor(C_TEXT_MUTED)

        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(
                54, 11 * inch - 36,
                "Miva Open University • MIT 8313 Final Project Defence Guide • Olakunle Oladeji Awotunbo (2025/B/MIT/1384)"
            )
            self.setStrokeColor(C_LINE)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer (All pages)
        self.setStrokeColor(C_LINE)
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * inch - 54, 45)

        self.drawString(
            54, 32,
            "Master of Information Technology (Artificial Intelligence)  |  Supervisor: Prof. Olushina Olawale Awe"
        )
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles using Times-Roman
    style_inst = ParagraphStyle(
        "InstHeader",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=10,
        leading=13,
        textColor=C_GOLD,
        alignment=TA_CENTER,
        spaceAfter=2
    )

    style_sub_inst = ParagraphStyle(
        "SubInstHeader",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9,
        leading=12,
        textColor=C_TEXT_MUTED,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    style_doc_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=15,
        leading=19,
        textColor=C_NAVY_PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    style_doc_sub = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=10.5,
        leading=14,
        textColor=C_TEXT_DARK,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    style_meta = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9,
        leading=13,
        textColor=C_TEXT_DARK
    )

    style_meta_b = ParagraphStyle(
        "MetaTextBold",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=9,
        leading=13,
        textColor=C_NAVY_PRIMARY
    )

    style_cat_title = ParagraphStyle(
        "CategoryTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12,
        leading=16,
        textColor=C_NAVY_PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_q_num = ParagraphStyle(
        "QNum",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=10.5,
        leading=14,
        textColor=C_NAVY_PRIMARY
    )

    style_intent = ParagraphStyle(
        "IntentText",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=9,
        leading=12.5,
        textColor=C_TEXT_MUTED
    )

    style_intent_b = ParagraphStyle(
        "IntentBold",
        parent=styles["Normal"],
        fontName="Times-BoldItalic",
        fontSize=9,
        leading=12.5,
        textColor=C_GOLD
    )

    style_body = ParagraphStyle(
        "AnswerBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=4
    )

    style_bullet = ParagraphStyle(
        "AnswerBullet",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXT_DARK,
        leftIndent=14,
        firstLineIndent=-10,
        alignment=TA_JUSTIFY,
        spaceAfter=3
    )

    style_tip = ParagraphStyle(
        "TipText",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9,
        leading=12.5,
        textColor=C_TEXT_DARK
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------------------
    story.append(Paragraph("MIVA OPEN UNIVERSITY ABUJA, NIGERIA", style_inst))
    story.append(Paragraph("SCHOOL OF COMPUTING • DEPARTMENT OF INFORMATION TECHNOLOGY", style_sub_inst))
    story.append(Paragraph("MASTER OF INFORMATION TECHNOLOGY (MIT 8313) • FINAL PROJECT DEFENCE", style_inst))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "COMPREHENSIVE ORAL EXAMINATION DEFENCE GUIDE", style_doc_title
    ))
    story.append(Paragraph(
        "Anticipated Committee Questions, Analytical Examiner Intents, and Authoritative Defence Responses",
        style_doc_sub
    ))

    # Metadata Table
    meta_data = [
        [
            Paragraph("<b>Candidate:</b> Olakunle Oladeji Awotunbo", style_meta),
            Paragraph("<b>Matriculation No.:</b> 2025/B/MIT/1384", style_meta),
        ],
        [
            Paragraph("<b>Programme:</b> Master of Information Technology (MIT)", style_meta),
            Paragraph("<b>Course Code:</b> MIT 8313 (Project)", style_meta),
        ],
        [
            Paragraph("<b>Project Supervisor:</b> Prof. Olushina Olawale Awe", style_meta),
            Paragraph("<b>Examination Session:</b> November 2026", style_meta),
        ],
        [
            Paragraph("<b>Project Title:</b> <i>Design and Implementation of a Fraud Detection System for Mobile Money Transactions in Nigeria</i>", style_meta),
            Paragraph("<b>Methodology:</b> Design Science Research (DSR)", style_meta)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 234])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.75, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_LINE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------------------
    # QA GENERATOR HELPER
    # -------------------------------------------------------------------------
    def format_qa(q_num_str, question_text, intent_text, answer_paragraphs):
        flowables = []

        # Question Header Table
        q_table = Table(
            [[Paragraph(f"<b>{q_num_str}:</b> {question_text}", style_q_num)]],
            colWidths=[504]
        )
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_NAVY_LIGHT),
            ('BOX', (0, 0), (-1, -1), 1, C_BLUE_ACCENT),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        flowables.append(q_table)
        flowables.append(Spacer(1, 4))

        # Intent Box Table
        intent_table = Table(
            [[
                Paragraph("<b>Examiner's Underlying Intent:</b>", style_intent_b),
                Paragraph(intent_text, style_intent)
            ]],
            colWidths=[150, 354]
        )
        intent_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_GOLD_LIGHT),
            ('BOX', (0, 0), (-1, -1), 0.5, C_GOLD),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        flowables.append(intent_table)
        flowables.append(Spacer(1, 6))

        # Answer Label
        p_ans_lbl = Paragraph("<b>Recommended Authoritative Response:</b>", style_meta_b)
        flowables.append(p_ans_lbl)
        flowables.append(Spacer(1, 3))

        # Answer Paragraphs
        for p_text in answer_paragraphs:
            if p_text.startswith("•"):
                flowables.append(Paragraph(p_text, style_bullet))
            else:
                flowables.append(Paragraph(p_text, style_body))

        flowables.append(Spacer(1, 10))
        return KeepTogether(flowables)

    # -------------------------------------------------------------------------
    # CATEGORY 1: RESEARCH METHODOLOGY & PROBLEM FORMULATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 1: METHODOLOGY & PROBLEM FORMULATION", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 1",
        "Why did you adopt the Design Science Research (DSR) methodology instead of standard experimental or survey-based approaches?",
        "Probing whether you understand the fundamental difference between descriptive behavioral science and applied IT artifact engineering.",
        [
            "Design Science Research (DSR), as formulated by Peffers et al. (2007) and Hevner et al. (2004), is specifically tailored for applied information technology disciplines where the research objective is to solve an identified operational problem through the creation, demonstration, and empirical evaluation of an innovative software artifact.",
            "Traditional survey or purely behavioral methodologies observe and describe existing phenomena without creating interventions. In contrast, DSR iteratively guides the artifact development lifecycle through six distinct, structured phases:",
            "•  <b>1. Problem Identification:</b> Documenting high mobile money fraud volumes, identity theft via SIM-swaps, and the sub-50ms latency limitations of Nigerian telecom USSD switches.",
            "•  <b>2. Objective Definition:</b> Formulating requirements for sub-15ms inference latency, PR-AUC > 0.95, and zero data leakage.",
            "•  <b>3. Artifact Design & Development:</b> Formulating domain accounting invariants (Equations 3.1–3.4), training Cost-Weighted XGBoost, and building a PyTorch Deep Autoencoder.",
            "•  <b>4. Demonstration:</b> Creating an operational executive Streamlit dashboard (app.py) and an asynchronous FastAPI gateway (api.py).",
            "•  <b>5. Empirical Evaluation:</b> Conducting rigorous 5-fold Stratified Cross-Validation on 1,048,575 transactions, latency profiling, and formal unit testing (TC-01 to TC-06).",
            "•  <b>6. Communication:</b> Delivering the master's thesis dissertation, publishing an open-source reproducible repository, and presenting this oral defense."
        ]
    ))

    story.append(format_qa(
        "Question 2",
        "Why did you utilize synthetic transaction data instead of real commercial records from a licensed Nigerian bank or mobile money operator?",
        "Testing awareness of legal data privacy frameworks (NDPR), corporate banking confidentiality, and whether your dataset realistically represents Nigerian payment rails.",
        [
            "Licensed Nigerian commercial banks, mobile money operators, and the Nigeria Inter-Bank Settlement System (NIBSS) are legally prohibited from sharing raw production financial transaction logs containing Personally Identifiable Information (PII) under Section 2.1 of the Nigeria Data Protection Regulation (NDPR) and Central Bank of Nigeria (CBN) data governance directives.",
            "To solve this while ensuring complete research reproducibility, and following established benchmark literature (such as the PaySim financial simulation methodology by Lopez-Rojas et al.), we engineered a dedicated synthetic Nigerian mobile money dataset engine (data_generator.py) generating 1,048,575 records.",
            "Crucially, the dataset is not arbitrarily random; it strictly mirrors the exact operational characteristics of the Nigerian payment ecosystem:",
            "•  <b>Authentic Payment Primitives:</b> Models genuine payment types (TRANSFER, CASH_OUT, PAYMENT, CASH_IN, and DEBIT).",
            "•  <b>Macroeconomic Asymmetry:</b> Enforces the realistic, real-world low fraud prevalence rate of 0.13% (1,363 fraudulent transactions among 1,048,575 total).",
            "•  <b>Nocturnal Velocity Spikes:</b> Models off-peak liquidation patterns where fraudsters execute transfers between 1:00 AM and 5:00 AM while legitimate account owners sleep.",
            "•  <b>SIM-Swap Liquidation Topologies:</b> Replicates total balance evacuations where entire origin ledgers are emptied to zero in a single transaction and routed to freshly opened mule accounts."
        ]
    ))

    # -------------------------------------------------------------------------
    # CATEGORY 2: DOMAIN FEATURE ENGINEERING & MATHEMATICAL INVARIANTS
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 2: DOMAIN FEATURE ENGINEERING & MATHEMATICAL INVARIANTS", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 3",
        "Explain the mathematical formulations in Equations 3.1 through 3.4. Why were raw transaction amounts alone insufficient for fraud surveillance?",
        "Evaluating whether you understand domain-specific financial state invariants versus relying blindly on raw data columns.",
        [
            "In mobile money networks, raw transaction amounts alone provide weak predictive signals because a legitimate business transfer of ₦350,000 looks identical to a fraudulent SIM-swap drain of ₦350,000. Fraud manifests not in the standalone amount, but in the mathematical relationship between the transacted amount and the pre- and post-balances of the transacting ledgers.",
            "To capture illegal state transitions, we formulated four domain accounting invariants in Chapter 3.5:",
            "•  <b>Equation 3.1 (Origin Balance Discrepancy):</b> errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig. Captures double-debit anomalies or unauthorized adjustments where the origin ledger does not balance mathematically.",
            "•  <b>Equation 3.2 (Destination Balance Discrepancy):</b> errorBalanceDest = oldbalanceDest + amount - newbalanceDest. Detects rapid mule account cash-outs where incoming funds are instantly liquidated rather than retained.",
            "•  <b>Equation 3.3 (Complete Account Drain Flag):</b> isCompleteDrain = 1.0 if (newbalanceOrig == 0.0 and amount > 0.0) else 0.0. In Nigerian telecommunications SIM-swap attacks, fraudsters do not take partial sums; they wipe the victim's account to exactly ₦0.00.",
            "•  <b>Equation 3.4 (Capital Liquidation Ratio):</b> amountToBalanceRatio = amount / (oldbalanceOrg + 1e-5). Measures the proportion of the account liquidated in a single stroke, where values >= 0.95 strongly correlate with account takeovers.",
            "Empirical TreeSHAP feature attribution (Chapter 5.4.4) demonstrates that these four domain features account for over 74% of the final fraud score attribution."
        ]
    ))

    # -------------------------------------------------------------------------
    # CATEGORY 3: CLASS IMBALANCE & PIPELINE INTEGRITY
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 3: CLASS IMBALANCE & PIPELINE INTEGRITY", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 4",
        "Your dataset features an extreme 0.13% class imbalance. How did you resolve this, and how did you guarantee zero synthetic data leakage?",
        "Probing the #1 research pitfall in fraud analytics: Did you erroneously apply SMOTE before splitting your train and validation sets?",
        [
            "Applying synthetic oversampling (like SMOTE) across an entire dataset prior to cross-validation splitting introduces catastrophic data leakage. Synthetic minority points generated from future test samples bleed into the training folds, artificially inflating model accuracy and failing in production.",
            "To eliminate this risk, we enforced two rigorous methodological safeguards in Chapter 4.2.3:",
            "•  <b>1. Strict Pipeline Isolation (Train-Only Resampling):</b> In our 5-fold Stratified Cross-Validation loop, SMOTE was embedded strictly inside the training split of each fold. Test folds remained 100% natural, unmanipulated, and completely isolated (verified in Test Case TC-02).",
            "•  <b>2. Algorithmic Cost-Sensitive Loss Weighting:</b> Rather than over-synthesizing massive data points, we parameterized XGBoost's objective function with scale_pos_weight = N_neg / N_pos = 761.6, reflecting the exact inverse of our 0.13% fraud prevalence.",
            "This configuration forces the gradient tree-splitting loss to penalize false negatives (missed fraud) 761 times more heavily than false positives, guaranteeing high sensitivity for rare SIM-swap attacks without distorting test fold validity."
        ]
    ))

    # -------------------------------------------------------------------------
    # CATEGORY 4: EVALUATION METRICS & BENCHMARK PERFORMANCE ANALYSIS
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 4: EVALUATION METRICS & BENCHMARK PERFORMANCE", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 5",
        "Why did you prioritize the Area Under the Precision-Recall Curve (PR-AUC) over the standard ROC-AUC metric in your evaluation?",
        "Testing whether you understand why ROC-AUC provides misleading results on severely imbalanced financial data.",
        [
            "On highly imbalanced datasets (such as 0.13% fraud prevalence), the standard Receiver Operating Characteristic curve (ROC-AUC) is mathematically deceptive. The False Positive Rate (FPR) formula is FP / (FP + TN). Because the legitimate majority class (TN) represents 99.87% of the data, the denominator is massive.",
            "Consequently, hundreds or thousands of false alarms cause only an imperceptible change in FPR, yielding artificially high ROC-AUC scores (> 0.94) even for poorly calibrated models.",
            "In contrast, the Precision-Recall curve (PR-AUC) evaluates Precision (TP / (TP + FP)) against Recall (TP / (TP + FN)). Precision directly incorporates False Positives against true fraud hits without being masked by millions of True Negatives.",
            "As proven in Table 5.2, while the Deep Autoencoder achieved an apparently strong ROC-AUC of 0.9410, its PR-AUC collapsed to 0.3862 due to excessive false alarms. Cost-Weighted XGBoost proved vastly superior, attaining a PR-AUC of 0.9841."
        ]
    ))

    story.append(format_qa(
        "Question 6",
        "The PyTorch Deep Autoencoder achieved an 84% recall. Why was it rejected for production deployment in favor of Cost-Weighted XGBoost?",
        "Evaluating your ability to connect raw machine learning metrics with commercial banking operations and customer retention.",
        [
            "While the PyTorch Deep Autoencoder achieved an 84.00% recall through out-of-distribution reconstruction loss, its False Positive Rate (FPR) was 0.960%.",
            "In an academic paper, 0.96% sounds negligible; however, in a live commercial Nigerian payment switch processing 10 million transactions daily, a 0.960% FPR means wrongfully intercepting and freezing approximately 96,000 legitimate customer transactions every single day.",
            "This causes catastrophic operational consequences:",
            "•  It paralyzes bank compliance desks under unmanageable manual investigation backlogs.",
            "•  It severely erodes consumer trust in cashless electronic payment rails.",
            "By contrast, Cost-Weighted XGBoost achieved a higher recall (91.80%), higher precision (94.12%), and reduced the False Positive Rate to 0.007%—eliminating over 99% of false alarms while executing in 14.2 milliseconds."
        ]
    ))

    # -------------------------------------------------------------------------
    # CATEGORY 5: REAL-WORLD FINTECH DEPLOYMENT & LATENCY CONSTRAINTS
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 5: FINTECH DEPLOYMENT & LATENCY CONSTRAINTS", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 7",
        "Why was sub-50ms inference latency established as a non-negotiable operational constraint for the system?",
        "Testing your technical understanding of the Nigerian telecommunications switching infrastructure and USSD protocol limits.",
        [
            "A vast proportion of financial inclusion transactions across Nigeria operate via Unstructured Supplementary Service Data (USSD) channels (such as *737#, *901#, *894#) and low-bandwidth 2G/3G mobile POS terminals in rural agency banking locations.",
            "Telecommunications signaling networks (such as MTN, Airtel, and Glo) enforce a rigid session timeout budget: if an integrated banking switch takes longer than 50 milliseconds to process and respond to an authorization request, the USSD session drops.",
            "A dropped session results in uncompleted transactions, double-debit customer disputes, and severe operational friction. Through histogram-based gradient tree traversal (tree_method='hist') and asynchronous FastAPI pipelining, our production model scores transactions in 14.2 ms (profiled in Postman, Figure 4.6), comfortably operating well under the 50ms cap."
        ]
    ))

    story.append(format_qa(
        "Question 8",
        "How does your containerized microservice architecture scale during peak festive velocity surges (e.g. Black Friday or Christmas)?",
        "Probing your software engineering and cloud deployment skills (FastAPI, Docker, stateless scaling).",
        [
            "Our architecture is deployed as a stateless containerized microservice using multi-stage Docker builds (Dockerfile and docker-compose.yml, Appendix D).",
            "Because the FastAPI scoring engine is entirely stateless—deserializing immutable model artifacts (xgboost_model.joblib, scaler.joblib, explainer.joblib) into memory at container startup—it exhibits zero inter-process dependencies.",
            "In production, the service can be horizontally autoscaled across Kubernetes pods or AWS Elastic Container Service (ECS) behind an NGINX or Application Load Balancer. As transaction throughput spikes from thousands to tens of thousands per second during peak clearing windows, additional container replicas spawn dynamically within seconds without downtime or database contention."
        ]
    ))

    # -------------------------------------------------------------------------
    # CATEGORY 6: REGULATION, EXPLAINABILITY (XAI) & DATA PROTECTION
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 6: REGULATION, EXPLAINABLE AI & DATA PROTECTION", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 9",
        "How does your system enforce compliance with the Nigeria Data Protection Regulation (NDPR 2019)?",
        "Assessing compliance with Nigerian legal statutes on privacy, data retention, and cryptographic hashing.",
        [
            "Compliance with the NDPR (2019) is enforced at the very first tier of our processing pipeline (security.py, Section 4.4):",
            "•  <b>Cryptographic Salted Pseudonymization:</b> Origin and destination account identifiers (nameOrig, nameDest) undergo irreversible salted SHA-256 cryptographic hashing immediately upon entry into the API gateway.",
            "•  <b>Zero PII Persistence:</b> Downstream feature extraction, gradient boosted scoring, and audit logging consume only 64-character hexadecimal hashes. No plain text account numbers, customer names, or phone numbers are ever stored in RAM or written to disk.",
            "•  <b>Stateless Clearance:</b> Once scored and returned to the payment switch, transaction payloads are purged from memory, fulfilling the NDPR's data minimization and storage limitation principles."
        ]
    ))

    story.append(format_qa(
        "Question 10",
        "If an aggrieved customer sues a bank for an automated account freeze, how does your system legally defend the interception decision?",
        "Probing your knowledge of Explainable AI (TreeSHAP) and Central Bank of Nigeria (CBN) Consumer Protection regulations.",
        [
            "Under the Central Bank of Nigeria Consumer Protection Framework, financial institutions must provide clear, auditable explanations when automated fraud systems freeze or restrict customer accounts. Black-box neural models that merely output an uninterpretable score cannot legally defend such administrative actions.",
            "To solve this, our system integrates TreeSHAP (shap.TreeExplainer, Section 4.2.6), which mathematically decomposes the model's log-odds margin into exact additive Shapley feature attributions (phi_i) based on cooperative game theory.",
            "When an interception occurs (Risk Score > 0.70), the system generates an auditable waterfall plot (Figure 4.4 in the thesis) providing conclusive legal proof:",
            "•  The origin account was 100% liquidated in a single transfer (isCompleteDrain contributed +41.2% to the risk probability).",
            "•  The ledger exhibited an accounting mismatch (errorBalanceOrig contributed +33.4%).",
            "•  The transaction occurred during nocturnal velocity hours (1:00 AM – 5:00 AM, contributing +18.5%).",
            "This provides compliance officers, bank legal counsel, and the CBN Ombudsman with an undeniable, mathematically grounded explanation."
        ]
    ))

    # -------------------------------------------------------------------------
    # CATEGORY 7: SYSTEM LIMITATIONS & FUTURE RESEARCH DIRECTIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 7: LIMITATIONS & FUTURE RESEARCH DIRECTIONS", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_NAVY_PRIMARY, spaceBefore=1, spaceAfter=8))

    story.append(format_qa(
        "Question 11",
        "What are the primary limitations of your research, and what actionable extensions do you recommend for future work?",
        "Testing academic self-awareness, intellectual maturity, and future research vision.",
        [
            "In fulfillment of academic rigor, we identified three key technical limitations and corresponding future research directions in Chapter 6.4:",
            "•  <b>1. From Isolated Transactions to Graph Topologies:</b> The current architecture evaluates transactions as independent, discrete records. However, modern Nigerian fraud syndicates utilize sophisticated, multi-hop mule account rings. Future research should implement <b>Dynamic Graph Neural Networks (GNNs)</b> to track money flows across multi-account graph structures.",
            "•  <b>2. Distributed Event Streaming Architecture:</b> While our FastAPI service is optimized for REST requests, integration with distributed event brokers like <b>Apache Kafka</b> or <b>Redpanda</b> would enable continuous stream processing directly at the national switch level.",
            "•  <b>3. Edge Model Quantization for Agency POS:</b> Rural agency banking locations in Nigeria often suffer intermittent cellular connectivity. Future work should quantize the trained XGBoost model into <b>ONNX or TensorFlow Lite</b> to enable sub-5ms offline edge scoring directly on Android POS hardware."
        ]
    ))

    # -------------------------------------------------------------------------
    # DEFENSE PROTOCOL CHECKLIST
    # -------------------------------------------------------------------------
    story.append(Paragraph("SECTION 8: CANDIDATE DEFENSE STRATEGY & ADVICE", style_cat_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceBefore=1, spaceAfter=8))

    tip_data = [
        [
            Paragraph("<b>1. Time Management:</b>", style_meta_b),
            Paragraph("Keep oral presentation to exactly 15 minutes. Spend 2 minutes on problem/context, 3 minutes on methodology, 4 minutes on architecture/invariants, 4 minutes on benchmarks, and 2 minutes on demo/conclusion.", style_tip)
        ],
        [
            Paragraph("<b>2. Cite Exact Numbers:</b>", style_meta_b),
            Paragraph("Always quote exact thesis metrics: PR-AUC of <b>0.9841</b>, F1-score of <b>0.9295</b>, FPR of <b>0.007%</b>, and mean latency of <b>14.2 ms</b> against the <b>50 ms USSD budget</b>.", style_tip)
        ],
        [
            Paragraph("<b>3. Emphasize DSR Artifact:</b>", style_meta_b),
            Paragraph("Remind examiners that as an applied MIT degree project, you did not just write equations—you built, tested, and containerized a fully functional software artifact (FastAPI, Streamlit, Docker).", style_tip)
        ],
        [
            Paragraph("<b>4. Defend Against SMOTE Leakage:</b>", style_meta_b),
            Paragraph("If asked about resampling, immediately state that SMOTE was applied <b>strictly inside the cross-validation training folds</b>, completely isolating test folds (validated in TC-02).", style_tip)
        ]
    ]
    tip_table = Table(tip_data, colWidths=[140, 364])
    tip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 1, C_GOLD),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tip_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {PDF_FILENAME}")


if __name__ == "__main__":
    build_pdf()
