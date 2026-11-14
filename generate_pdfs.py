"""
Generate professional submission PDFs for Velcoris Industries:
1. docs/Velcoris_Industries_Assignment_Report.pdf
2. docs/Velcoris_Architecture_and_Dataflow.pdf
"""
import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#65716b"))
            # Header
            self.drawString(54, 11 * inch - 36, "VELCORIS INDUSTRIES — Digital Infrastructure Fellowship | Round 1")
            self.setStrokeColor(colors.HexColor("#dfe4dd"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            # Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * inch - 54, 36, page_text)
            self.drawString(54, 36, "Confidential — Candidate Assessment Document")
            self.line(54, 48, 8.5 * inch - 54, 48)
            self.restoreState()

def create_report_pdf():
    pdf_path = "docs/Velcoris_Industries_Assignment_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    cDark = colors.HexColor("#101a16")
    cAcid = colors.HexColor("#6b9b37")
    cGreen = colors.HexColor("#294d3d")
    cText = colors.HexColor("#1e2923")
    cMuted = colors.HexColor("#58645c")
    cBgHeader = colors.HexColor("#e9eee7")
    cBorder = colors.HexColor("#d5ded2")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=cDark,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=cGreen,
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=cDark,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=cGreen,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=cDark,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=cText,
        spaceAfter=8
    )
    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=cMuted,
        alignment=1,
        spaceAfter=14
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=cText
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=cDark
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=cDark
    )

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("VELCORIS INDUSTRIES", ParagraphStyle('Eyebrow', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=cAcid)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Digital Infrastructure & Backend-IT Fellowship", title_style))
    story.append(Paragraph("Round 1 — Test by Fire: Technical Assessment Report & Prototype Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=cAcid, spaceAfter=30))

    meta_data = [
        [Paragraph("<b>Organisation:</b>", table_cell_bold), Paragraph("Velcoris Industries (Greater Noida, UP)", table_cell)],
        [Paragraph("<b>Candidate:</b>", table_cell_bold), Paragraph("Shauriya Garg", table_cell)],
        [Paragraph("<b>Role:</b>", table_cell_bold), Paragraph("Digital Infrastructure & Backend-IT Fellowship", table_cell)],
        [Paragraph("<b>Assessment Round:</b>", table_cell_bold), Paragraph("Round 1 — Comprehensive Deliverable", table_cell)],
        [Paragraph("<b>Submission Date:</b>", table_cell_bold), Paragraph("14 November 2026", table_cell)],
        [Paragraph("<b>GitHub Repository:</b>", table_cell_bold), Paragraph("<font color='#184d21'><u>https://github.com/ShauriyaDeveloper1/Velcoris_Assignment</u></font>", table_cell)],
        [Paragraph("<b>Live Prototype:</b>", table_cell_bold), Paragraph("<font color='#184d21'><u>https://velcoris-assignment.vercel.app</u></font>", table_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[130, 370])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8faf6")),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 40))

    exec_summary_text = (
        "<b>Executive Brief:</b> This report presents an end-to-end evaluation and production-grade implementation "
        "for Velcoris Industries. It addresses both Task 1 (Corporate Website Analysis, Information Architecture redesign, "
        "and modern industrial prototype) and Task 2 (Backend & IT Infrastructure Analysis, enterprise email/automation strategy, "
        "and a functional Query Management System). All backend features, SQLite parameterised storage via python-dotenv, "
        "admin session gating, and CLI tools have been verified with empirical tests."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(PageBreak())

    # ================= TASK 1 =================
    story.append(Paragraph("Task 1 — Existing Website Analysis & Redesign", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=cBorder, spaceAfter=14))

    story.append(Paragraph("1.1 Publicly Observable Website Content & Architecture", h2_style))
    story.append(Paragraph(
        "Based on an analysis of the public web presence at velcorisindustries.com, Velcoris Industries positions itself as an "
        "Indian pioneer in industrial graphene manufacturing, focusing on Few-Layer Graphene (FLG) and Graphene Oxide (GO). "
        "The site communicates a 6-stage closed-loop conversion methodology, batch characterisation standards (Raman spectroscopy, "
        "XRD, particle-size distribution), leadership information, and sample request channels. This report respects public disclosures "
        "without making unverified private claims.",
        body_style
    ))

    story.append(Paragraph("1.2 Evaluation of Existing UX & Areas for Improvement", h2_style))
    ux_data = [
        [Paragraph("Dimension", table_header), Paragraph("Current Observation", table_header), Paragraph("Area for Improvement", table_header), Paragraph("Prototype Solution", table_header)],
        [
            Paragraph("<b>Positioning & Hierarchy</b>", table_cell_bold),
            Paragraph("High text density; materials distinctions compete with general vision.", table_cell),
            Paragraph("Industrial buyers need immediate clarity on material grades (FLG vs GO).", table_cell),
            Paragraph("Technical hero proposition + comparative material cards.", table_cell)
        ],
        [
            Paragraph("<b>Navigation & CTAs</b>", table_cell_bold),
            Paragraph("Excessive scrolling needed to find specific B2B conversion pathways.", table_cell),
            Paragraph("Direct high-contrast anchor navigation to Materials, Process, Contact.", table_cell),
            Paragraph("Sticky header with anchor links + distinct Admin Portal button.", table_cell)
        ],
        [
            Paragraph("<b>Enquiry Journey</b>", table_cell_bold),
            Paragraph("Generic contact form combines all inquiries into one unsegmented bucket.", table_cell),
            Paragraph("Segment sample requests, tech consultations, and partnerships upfront.", table_cell),
            Paragraph("Multi-intent enquiry select with live inline validation.", table_cell)
        ],
        [
            Paragraph("<b>Mobile Responsiveness</b>", table_cell_bold),
            Paragraph("Dense multi-column tables need fluid responsive behavior.", table_cell),
            Paragraph("Single-column stacking, accessible tap targets (48px+), mobile drawer.", table_cell),
            Paragraph("Responsive CSS breakpoints (1440px, 850px, 390px) + drawer toggle.", table_cell)
        ],
        [
            Paragraph("<b>Spam Defense</b>", table_cell_bold),
            Paragraph("Standard HTML forms vulnerable to automated scrapers.", table_cell),
            Paragraph("Prevent spam bots without hostile user CAPTCHA friction.", table_cell),
            Paragraph("Concealed honeypot field (aria-hidden) trapping bots silently.", table_cell)
        ]
    ]
    t_ux = Table(ux_data, colWidths=[80, 130, 140, 150])
    t_ux.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cBgHeader),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ux)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.3 Proposed Information Architecture & Design Benchmarks", h2_style))
    story.append(Paragraph(
        "The redesign adopts a 6-stage structured conversion funnel: (1) Value proposition hero, (2) Trust strip with core metrics, "
        "(3) Modular material cards for FLG and GO, (4) Repeatable 4-stage technical methodology, (5) Application landscape, and "
        "(6) Asynchronous multi-intent enquiry form. To anchor the visual identity, design principles were adopted from leading industrial peers:",
        body_style
    ))
    story.append(Paragraph("• <b>Hexcel Corporation (hexcel.com):</b> Rigorous data density, technical specification tags, and high-contrast carbon aesthetic.", body_style))
    story.append(Paragraph("• <b>Toray Advanced Composites (toraytac.com):</b> Purpose-driven B2B customer triage separating sample evaluation from commercial contracts.", body_style))
    story.append(Paragraph("• <b>BASF Advanced Materials (basf.com):</b> Process transparency and analytical quality gates to establish credibility before procurement.", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("1.4 Prototype Screenshots", h2_style))
    
    # Image 1
    if os.path.exists("docs/screenshots/01_homepage.png"):
        story.append(Image("docs/screenshots/01_homepage.png", width=6.8*inch, height=3.9*inch))
        story.append(Paragraph("Figure 1: Redesigned Velcoris Industries Homepage (Desktop 1440×900 View)", caption_style))

    # Image 2
    if os.path.exists("docs/screenshots/02_contact_form.png"):
        story.append(Image("docs/screenshots/02_contact_form.png", width=6.8*inch, height=3.9*inch))
        story.append(Paragraph("Figure 2: Structured Multi-Intent Contact & Enquiry Form Interface", caption_style))

    # Image 3
    if os.path.exists("docs/screenshots/03_enquiry_success.png"):
        story.append(Image("docs/screenshots/03_enquiry_success.png", width=6.8*inch, height=3.9*inch))
        story.append(Paragraph("Figure 3: Asynchronous Form Confirmation with Database Verification Notice", caption_style))

    story.append(PageBreak())

    # ================= TASK 2 =================
    story.append(Paragraph("Task 2 — Backend & IT Infrastructure Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=cBorder, spaceAfter=14))

    story.append(Paragraph("2.1 Existing Technical Setup: Evidence & Unknowns", h2_style))
    tech_data = [
        [Paragraph("Layer", table_header), Paragraph("Existing Velcoris Setup", table_header), Paragraph("Your Prototype", table_header), Paragraph("Target Recommendation", table_header)],
        [Paragraph("Backend", table_cell_bold), Paragraph("Unknown", table_cell), Paragraph("Flask", table_cell), Paragraph("Gunicorn/FastAPI containerised with CI/CD.", table_cell)],
        [Paragraph("Database", table_cell_bold), Paragraph("Unknown", table_cell), Paragraph("SQLite", table_cell), Paragraph("Managed PostgreSQL (AWS RDS / Neon) with WAL backups.", table_cell)],
        [Paragraph("Frontend", table_cell_bold), Paragraph("Publicly observed", table_cell), Paragraph("HTML/CSS/JavaScript", table_cell), Paragraph("Maintain zero-dependency vanilla JS and semantic HTML5.", table_cell)],
        [Paragraph("Web Server", table_cell_bold), Paragraph("Inferred (Reverse proxy)", table_cell), Paragraph("Vercel WSGI Serverless", table_cell), Paragraph("Cloudflare Edge CDN / WAF with TLS 1.3.", table_cell)],
        [Paragraph("Identity & Mail", table_cell_bold), Paragraph("Inferred (Domain MX)", table_cell), Paragraph("Session RBAC (.env)", table_cell), Paragraph("Google Workspace / M365 with hardware MFA.", table_cell)],
        [Paragraph("Automations", table_cell_bold), Paragraph("Unknown", table_cell), Paragraph("CLI & JSON endpoints", table_cell), Paragraph("n8n / Make webhook pipelines to CRM & Slack.", table_cell)],
    ]
    t_tech = Table(tech_data, colWidths=[75, 125, 120, 180])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cBgHeader),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.2 Enterprise Security Baseline", h2_style))
    story.append(Paragraph(
        "• <b>HTTP Security Headers:</b> X-Content-Type-Options: nosniff, X-Frame-Options: DENY, Referrer-Policy: strict-origin-when-cross-origin, "
        "and strict Content-Security-Policy (CSP) headers are actively enforced.<br/>"
        "• <b>SQL Injection Prevention:</b> All database interactions use parameterised queries with prepared statements.<br/>"
        "• <b>Secrets Isolation:</b> Zero hardcoded credentials; runtime configuration injected via python-dotenv.<br/>"
        "• <b>Bot Defense:</b> CSS-hidden honeypot silently swallows automated spam submissions.",
        body_style
    ))

    story.append(Paragraph("2.3 Query Management System & Database Access", h2_style))
    story.append(Paragraph(
        "The practical task was implemented end-to-end and supports dual access modes: (1) A session-authenticated Web Dashboard "
        "at /admin showing lifecycle statuses (New, In Progress, Responded, Closed) with inline update forms, and (2) A CLI script "
        "(view_enquiries.py) and Flask command (flask view-enquiries) allowing direct terminal data inspection.",
        body_style
    ))

    # Image 4
    if os.path.exists("docs/screenshots/04_admin_dashboard.png"):
        story.append(Image("docs/screenshots/04_admin_dashboard.png", width=6.8*inch, height=3.9*inch))
        story.append(Paragraph("Figure 4: Authenticated Admin Dashboard Showing Query Triage and Status Controls", caption_style))

    # Image 5
    if os.path.exists("docs/screenshots/05_sqlite_browse_data.png"):
        story.append(Image("docs/screenshots/05_sqlite_browse_data.png", width=6.8*inch, height=3.9*inch))
        story.append(Paragraph("Figure 5: DB Browser for SQLite Showing Persisted Enquiries in velcoris.db", caption_style))

    story.append(PageBreak())

    # ================= TESTING MATRIX =================
    story.append(Paragraph("2.4 Empirical Testing Results Matrix", h2_style))
    story.append(Paragraph(
        "The following matrix documents live tests executed against the application backend. All tests passed with verified evidence.",
        body_style
    ))

    test_data = [
        [Paragraph("ID", table_header), Paragraph("Test Scenario", table_header), Paragraph("Expected Result", table_header), Paragraph("Actual Verified Result", table_header), Paragraph("HTTP", table_header), Paragraph("Status", table_header)],
        [Paragraph("T1", table_cell_bold), Paragraph("Valid Form Submission", table_cell), Paragraph("Record saved to SQLite", table_cell), Paragraph("Inserted; confirmation returned", table_cell), Paragraph("201", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T2", table_cell_bold), Paragraph("Invalid Email Format", table_cell), Paragraph("HTTP 400 validation error", table_cell), Paragraph("Rejected: Enter valid email", table_cell), Paragraph("400", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T3", table_cell_bold), Paragraph("Short Name (<2 chars)", table_cell), Paragraph("HTTP 400 validation error", table_cell), Paragraph("Rejected: Name 2-100 chars", table_cell), Paragraph("400", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T4", table_cell_bold), Paragraph("Honeypot Bot Trap", table_cell), Paragraph("Silent drop; 0 DB rows", table_cell), Paragraph("Returns 201; no row inserted", table_cell), Paragraph("201", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T5", table_cell_bold), Paragraph("Unauth Admin Access", table_cell), Paragraph("Redirect to /admin/login", table_cell), Paragraph("Redirects to login page", table_cell), Paragraph("302", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T6", table_cell_bold), Paragraph("Admin Authentication", table_cell), Paragraph("Dashboard rendered", table_cell), Paragraph("Session valid; shows table", table_cell), Paragraph("302→200", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T7", table_cell_bold), Paragraph("Status Update Lifecycle", table_cell), Paragraph("Status persists in DB", table_cell), Paragraph("Updated in SQLite; badge reflects", table_cell), Paragraph("302→200", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T8", table_cell_bold), Paragraph("Healthcheck Endpoint", table_cell), Paragraph("JSON status: ok", table_cell), Paragraph("Returns {'status': 'ok'}", table_cell), Paragraph("200", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
        [Paragraph("T9", table_cell_bold), Paragraph("Standalone CLI Script", table_cell), Paragraph("Terminal dumps enquiries", table_cell), Paragraph("Outputs formatted records", table_cell), Paragraph("Exit 0", table_cell), Paragraph("<b>PASS</b>", table_cell_bold)],
    ]
    t_test = Table(test_data, colWidths=[24, 110, 110, 150, 50, 50])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cBgHeader),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 14))

    story.append(Paragraph("2.5 Enterprise Implementation Roadmap", h2_style))
    roadmap_data = [
        [Paragraph("Priority", table_header), Paragraph("Phase", table_header), Paragraph("Workstream", table_header), Paragraph("Timeline", table_header), Paragraph("Acceptance Criteria", table_header)],
        [Paragraph("P0", table_cell_bold), Paragraph("Discovery", table_cell), Paragraph("Audit DNS, register @velcorisindustries.com", table_cell), Paragraph("Weeks 1–2", table_cell), Paragraph("Signed-off asset inventory", table_cell)],
        [Paragraph("P0", table_cell_bold), Paragraph("Security", table_cell), Paragraph("Enforce hardware MFA, SPF/DKIM/DMARC", table_cell), Paragraph("Weeks 2–3", table_cell), Paragraph("Zero unauthenticated accounts", table_cell)],
        [Paragraph("P1", table_cell_bold), Paragraph("Backend", table_cell), Paragraph("Migrate SQLite to AWS RDS PostgreSQL", table_cell), Paragraph("Weeks 3–5", table_cell), Paragraph("Automated CI/CD & SSL A+", table_cell)],
        [Paragraph("P1", table_cell_bold), Paragraph("Website", table_cell), Paragraph("Deploy redesigned site with approved assets", table_cell), Paragraph("Weeks 4–6", table_cell), Paragraph("Sub-1.2s Core Web Vitals", table_cell)],
        [Paragraph("P2", table_cell_bold), Paragraph("Automation", table_cell), Paragraph("n8n workflow for enquiry triage & CRM sync", table_cell), Paragraph("Weeks 6–8", table_cell), Paragraph("Inquiries in CRM within 15s", table_cell)],
        [Paragraph("P2", table_cell_bold), Paragraph("Operations", table_cell), Paragraph("Centralised logging, error tracking (Sentry)", table_cell), Paragraph("Weeks 8–10", table_cell), Paragraph("Real-time monitoring dashboards", table_cell)],
    ]
    t_road = Table(roadmap_data, colWidths=[40, 70, 160, 70, 160])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cBgHeader),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Conclusion", h2_style))
    story.append(Paragraph(
        "This evaluation demonstrates that Velcoris Industries' digital infrastructure can be significantly modernized "
        "to mirror the precision of its advanced materials platform. The prototype is functional and suitable for technical "
        "evaluation. Additional security hardening, managed database integration and deployment validation are required "
        "before production use.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF generated successfully at:", pdf_path)

def create_architecture_pdf():
    pdf_path = "docs/Velcoris_Architecture_and_Dataflow.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    cDark = colors.HexColor("#101a16")
    cAcid = colors.HexColor("#6b9b37")
    cGreen = colors.HexColor("#294d3d")
    cText = colors.HexColor("#1e2923")
    cBorder = colors.HexColor("#d5ded2")
    cBgHeader = colors.HexColor("#e9eee7")

    title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=cDark, spaceAfter=6)
    subtitle_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=11, leading=15, textColor=cGreen, spaceAfter=16)
    h1_style = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=cDark, spaceBefore=12, spaceAfter=8, keepWithNext=True)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9, leading=13.5, textColor=cText, spaceAfter=6)
    table_cell = ParagraphStyle('TC', fontName='Helvetica', fontSize=8, leading=11, textColor=cText)
    table_cell_bold = ParagraphStyle('TCB', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=cDark)
    table_header = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=cDark)

    story = []

    story.append(Paragraph("VELCORIS INDUSTRIES", ParagraphStyle('EB', fontName='Helvetica-Bold', fontSize=10, textColor=cAcid)))
    story.append(Paragraph("Digital Infrastructure Architecture & Dataflow Specification", title_style))
    story.append(Paragraph("Candidate Assessment Submission · Technical Specification Document", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=cAcid, spaceAfter=16))

    story.append(Paragraph("1. End-to-End System Architecture", h1_style))
    arch_diagram = [
        [Paragraph("<b>Step</b>", table_header), Paragraph("Entity / Component", table_header), Paragraph("Protocol / Action", table_header), Paragraph("Technical Details", table_header)],
        [Paragraph("1", table_cell_bold), Paragraph("Client Browser", table_cell), Paragraph("HTTPS GET /", table_cell), Paragraph("Receives semantic HTML5 with inlined CSS & responsive layout", table_cell)],
        [Paragraph("2", table_cell_bold), Paragraph("Contact Form", table_cell), Paragraph("POST /api/enquiries", table_cell), Paragraph("Asynchronous fetch payload with honeypot & length validation", table_cell)],
        [Paragraph("3", table_cell_bold), Paragraph("Flask Backend", table_cell), Paragraph("Validation & Sanitization", table_cell), Paragraph("Validates name, RFC 5322 email regex, enum enquiry type", table_cell)],
        [Paragraph("4", table_cell_bold), Paragraph("SQLite Storage", table_cell), Paragraph("Parameterized INSERT", table_cell), Paragraph("Inserts into enquiries table; sets status='New', UTC timestamp", table_cell)],
        [Paragraph("5", table_cell_bold), Paragraph("Confirmation", table_cell), Paragraph("HTTP 201 JSON", table_cell), Paragraph("Returns message + Admin link; form resets instantly", table_cell)],
        [Paragraph("6", table_cell_bold), Paragraph("Administrator", table_cell), Paragraph("POST /admin/login", table_cell), Paragraph("Session-authenticated login using .env credentials", table_cell)],
        [Paragraph("7", table_cell_bold), Paragraph("Admin Portal", table_cell), Paragraph("GET /admin", table_cell), Paragraph("Displays enquiry counters, tabular data, and status controls", table_cell)],
        [Paragraph("8", table_cell_bold), Paragraph("Status Update", table_cell), Paragraph("POST /admin/.../status", table_cell), Paragraph("Updates status: New → In Progress → Responded → Closed", table_cell)],
        [Paragraph("9", table_cell_bold), Paragraph("CLI Inspection", table_cell), Paragraph("python view_enquiries.py", table_cell), Paragraph("Direct terminal extraction of SQLite records for audits", table_cell)],
    ]
    t_arch = Table(arch_diagram, colWidths=[24, 110, 130, 240])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cBgHeader),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 14))

    story.append(Paragraph("2. Database Schema Specification (enquiries table)", h1_style))
    schema_data = [
        [Paragraph("Column Name", table_header), Paragraph("Data Type", table_header), Paragraph("Constraints", table_header), Paragraph("Purpose / Description", table_header)],
        [Paragraph("id", table_cell_bold), Paragraph("INTEGER", table_cell), Paragraph("PRIMARY KEY AUTOINCREMENT", table_cell), Paragraph("Unique enquiry tracking identifier", table_cell)],
        [Paragraph("name", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("NOT NULL, length 2-100", table_cell), Paragraph("Full name of prospective client or researcher", table_cell)],
        [Paragraph("email", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("NOT NULL, valid RFC regex", table_cell), Paragraph("Work reply email address", table_cell)],
        [Paragraph("organisation", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("NULLABLE, max 120", table_cell), Paragraph("Institution, university, or corporate enterprise", table_cell)],
        [Paragraph("enquiry_type", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("CHECK IN (Sample, Tech, etc.)", table_cell), Paragraph("Triage intent category for sales routing", table_cell)],
        [Paragraph("subject", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("NOT NULL, length 3-140", table_cell), Paragraph("Brief summary of project or requirement", table_cell)],
        [Paragraph("message", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("NOT NULL, length 10-3000", table_cell), Paragraph("Detailed technical requirements or scope", table_cell)],
        [Paragraph("status", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("DEFAULT 'New' CHECK(status)", table_cell), Paragraph("New, In Progress, Responded, Closed", table_cell)],
        [Paragraph("created_at", table_cell_bold), Paragraph("TEXT", table_cell), Paragraph("DEFAULT (datetime('now'))", table_cell), Paragraph("ISO 8601 UTC timestamp of submission", table_cell)],
    ]
    t_sch = Table(schema_data, colWidths=[70, 70, 140, 220])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), cBgHeader),
        ('BOX', (0,0), (-1,-1), 1, cBorder),
        ('INNERGRID', (0,0), (-1,-1), 0.5, cBorder),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sch)
    story.append(Spacer(1, 14))

    story.append(Paragraph("3. Production Scaling Roadmap (AWS / PostgreSQL Architecture)", h1_style))
    story.append(Paragraph(
        "• <b>Edge:</b> Cloudflare WAF + DDoS mitigation with origin shielding.<br/>"
        "• <b>Compute:</b> Dockerized Flask API deployed on AWS ECS (Fargate) with auto-scaling.<br/>"
        "• <b>Database:</b> Managed PostgreSQL (AWS RDS Multi-AZ) with connection pooling (PgBouncer) and point-in-time recovery.<br/>"
        "• <b>Automation:</b> Event-driven webhook dispatches to n8n / Make for CRM lead synchronization and email alerts.<br/>"
        "• <b>Identity:</b> SSO & SAML integration via Microsoft Entra ID / Google Workspace with hardware MFA.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Architecture PDF generated successfully at:", pdf_path)

if __name__ == '__main__':
    create_report_pdf()
    create_architecture_pdf()
