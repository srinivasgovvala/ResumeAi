"""
Generate ATS_Builder_Admin_Guide.pdf - Comprehensive Step-by-Step Admin Guide
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── Color Palette ────────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#1e3a5f')
BLUE      = colors.HexColor('#2563eb')
BLUE_LIGHT= colors.HexColor('#eff6ff')
SLATE     = colors.HexColor('#0f172a')
TEXT_DARK = colors.HexColor('#334155')
MUTED     = colors.HexColor('#64748b')
BORDER    = colors.HexColor('#e2e8f0')
CODE_BG   = colors.HexColor('#f8fafc')
GREEN     = colors.HexColor('#16a34a')
GREEN_BG  = colors.HexColor('#f0fdf4')
ORANGE    = colors.HexColor('#d97706')
ORANGE_BG = colors.HexColor('#fffbeb')
WHITE     = colors.white


def build_pdf(filename="ATS_Builder_Admin_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # ── Custom Paragraph Styles ──
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=WHITE,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#93c5fd'),
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=BLUE,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=12,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
        backColor=CODE_BG,
        borderColor=BORDER,
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    note_style = ParagraphStyle(
        'NoteText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#92400e'),
        backColor=ORANGE_BG,
        borderColor=colors.HexColor('#f59e0b'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=WHITE,
        alignment=TA_LEFT
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK,
        alignment=TA_LEFT
    )

    story = []

    # ── HEADER BANNER ──
    header_data = [
        [Paragraph("ATS Resume Builder — Admin Customization Guide", title_style)],
        [Spacer(1, 4)],
        [Paragraph("Step-by-Step Instructions: AI Provider/Keys, Resume Templates & App Control", subtitle_style)],
        [Spacer(1, 4)],
        [Paragraph("<b>Version:</b> 2.0 · <b>Date:</b> August 2026 · <b>Author:</b> DeepMind Agentic Coding", subtitle_style)]
    ]
    header_table = Table(header_data, colWidths=[520])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))

    # ── OVERVIEW ──
    story.append(Paragraph("1. Admin Panel Overview & Access", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=8))

    story.append(Paragraph(
        "The Django Admin Panel provides complete runtime management of your ATS Resume Builder system without requiring code changes or server redeployments. From the admin panel, you can configure AI providers and API keys, customize or add new ATS resume templates, manage user accounts, and adjust scoring weights.",
        body_style
    ))

    access_info = [
        [Paragraph("<b>Admin URL:</b>", table_cell_style), Paragraph("<code>http://127.0.0.1:8000/admin/</code> (Local) or <code>https://yourdomain/admin/</code> (Prod)", table_cell_style)],
        [Paragraph("<b>Superuser Login:</b>", table_cell_style), Paragraph("Email: <code>admin@admin.com</code> | Password: <code>admin123</code>", table_cell_style)],
        [Paragraph("<b>Create Superuser Command:</b>", table_cell_style), Paragraph("<code>python manage.py createsuperuser</code>", table_cell_style)],
    ]
    t_access = Table(access_info, colWidths=[130, 390])
    t_access.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_access)
    story.append(Spacer(1, 12))

    # ── PART 1: AI PROVIDER & API KEY ──
    story.append(Paragraph("2. Part 1 — Configuring AI Provider & API Keys", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=8))

    story.append(Paragraph(
        "You can switch AI providers, keys, models, and endpoints live directly from <b>Accounts $\\rightarrow$ App Settings</b> at <code>/admin/accounts/appsettings/</code>.",
        body_style
    ))

    story.append(Paragraph("Step-by-Step Setup:", h2_style))
    story.append(Paragraph("<b>Step 1:</b> Log in to Django Admin and navigate to <b>App Settings</b>.", bullet_style))
    story.append(Paragraph("<b>Step 2:</b> Locate the AI settings rows in the settings table:", bullet_style))

    ai_table_data = [
        [Paragraph("Setting Key", table_header_style), Paragraph("Description & Options", table_header_style), Paragraph("Example Values", table_header_style)],
        [Paragraph("<b>AI_PROVIDER</b>", table_cell_style), Paragraph("Choose provider endpoint architecture.<br/>Options: <code>openrouter</code>, <code>openai</code>, <code>anthropic</code>, <code>google</code>, <code>custom</code>", table_cell_style), Paragraph("<code>openrouter</code>", table_cell_style)],
        [Paragraph("<b>AI_API_KEY</b>", table_cell_style), Paragraph("API key for provider. Masked in admin list.", table_cell_style), Paragraph("<code>sk-or-v1-xxxx...</code><br/><code>sk-ant-xxxx...</code>", table_cell_style)],
        [Paragraph("<b>AI_MODEL</b>", table_cell_style), Paragraph("Model identifier passed to provider.", table_cell_style), Paragraph("<code>openai/gpt-4o-mini</code><br/><code>claude-3-5-sonnet-20241022</code><br/><code>gemini-1.5-flash</code>", table_cell_style)],
        [Paragraph("<b>AI_BASE_URL</b>", table_cell_style), Paragraph("API Base URL endpoint.", table_cell_style), Paragraph("<code>https://openrouter.ai/api/v1</code><br/><code>https://api.openai.com/v1</code><br/><code>https://api.anthropic.com/v1</code>", table_cell_style)],
        [Paragraph("<b>AI_ENABLED</b>", table_cell_style), Paragraph("Enable or disable AI features system-wide.", table_cell_style), Paragraph("<code>true</code> or <code>false</code>", table_cell_style)],
        [Paragraph("<b>AI_MAX_REQUESTS_PER_DAY</b>", table_cell_style), Paragraph("Per-user daily quota cap.", table_cell_style), Paragraph("<code>50</code>", table_cell_style)],
    ]
    t_ai = Table(ai_table_data, colWidths=[120, 260, 140])
    t_ai.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ai)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Provider Specific Examples:", h2_style))

    story.append(Paragraph("<b>Option A: OpenRouter (Default)</b>", bullet_style))
    story.append(Paragraph("AI_PROVIDER: <code>openrouter</code><br/>AI_API_KEY: <code>sk-or-v1-your-key</code><br/>AI_MODEL: <code>openai/gpt-4o-mini</code><br/>AI_BASE_URL: <code>https://openrouter.ai/api/v1</code>", code_style))

    story.append(Paragraph("<b>Option B: Direct OpenAI</b>", bullet_style))
    story.append(Paragraph("AI_PROVIDER: <code>openai</code><br/>AI_API_KEY: <code>sk-proj-your-openai-key</code><br/>AI_MODEL: <code>gpt-4o-mini</code> or <code>gpt-4o</code><br/>AI_BASE_URL: <code>https://api.openai.com/v1</code>", code_style))

    story.append(Paragraph("<b>Option C: Anthropic Claude</b>", bullet_style))
    story.append(Paragraph("AI_PROVIDER: <code>anthropic</code><br/>AI_API_KEY: <code>sk-ant-api03-your-key</code><br/>AI_MODEL: <code>claude-3-5-sonnet-20241022</code><br/>AI_BASE_URL: <code>https://api.anthropic.com/v1</code>", code_style))

    story.append(Paragraph("<b>Option D: Google Gemini</b>", bullet_style))
    story.append(Paragraph("AI_PROVIDER: <code>google</code><br/>AI_API_KEY: <code>AIzaSy-your-gemini-key</code><br/>AI_MODEL: <code>gemini-1.5-flash</code>", code_style))

    story.append(Paragraph("Note: Changes take effect immediately on save. No server restart required.", note_style))
    story.append(Spacer(1, 10))

    # ── PART 2: RESUME TEMPLATES ──
    story.append(PageBreak())
    story.append(Paragraph("3. Part 2 — Adding & Customizing Resume Templates", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=8))

    story.append(Paragraph(
        "You can manage existing templates or publish completely new templates from <b>Resume $\\rightarrow$ Resume Templates</b> at <code>/admin/resume/resumetemplate/</code>.",
        body_style
    ))

    story.append(Paragraph("Step-by-Step Instructions to Add a Template:", h2_style))
    story.append(Paragraph("<b>Step 1:</b> Click the <b>+ Add Resume Template</b> button at top right of the table.", bullet_style))
    story.append(Paragraph("<b>Step 2:</b> Fill in the Basic Information:", bullet_style))
    story.append(Paragraph("• <b>Name:</b> Display name (e.g., <i>Executive Slate</i>)<br/>"
                           "• <b>Slug:</b> Unique identifier slug (e.g., <i>executive_slate</i>)<br/>"
                           "• <b>Description:</b> One-line summary for user selection<br/>"
                           "• <b>Category:</b> <code>universal</code> | <code>modern</code> | <code>formal</code> | <code>technical</code> | <code>compact</code> | <code>entry</code><br/>"
                           "• <b>Best For:</b> Audience target text (e.g., <i>Senior Directors, VPs</i>)<br/>"
                           "• <b>Sort Order:</b> Integer grid position (e.g., <i>16</i>)<br/>"
                           "• <b>Is Active:</b> Check <code>[x] True</code>", body_style))

    story.append(Paragraph("<b>Step 3:</b> Configure Section Orders (JSON Arrays):", bullet_style))
    story.append(Paragraph("<code>section_order_experienced</code>: Defines section order for candidates with work history:", body_style))
    story.append(Paragraph("[\n  \"header\", \"summary\", \"experience\", \"education\", \"skills\",\n  \"projects\", \"certifications\", \"achievements\", \"languages\"\n]", code_style))

    story.append(Paragraph("<code>section_order_fresher</code>: Defines section order for students and entry-level candidates:", body_style))
    story.append(Paragraph("[\n  \"header\", \"objective\", \"education\", \"skills\", \"projects\",\n  \"internships\", \"certifications\", \"awards\", \"languages\"\n]", code_style))

    story.append(Paragraph("<b>Step 4:</b> Configure HTML/CSS Styles (JSON Object):", bullet_style))
    story.append(Paragraph("The <code>styles</code> JSON dict controls live preview styling in the builder and standalone preview:", body_style))
    sample_styles_json = """{
  "font_family": "Arial, Helvetica, sans-serif",
  "font_size": "10.5px",
  "line_height": "1.55",
  "name_size": "20px",
  "name_weight": "700",
  "name_color": "#0f172a",
  "accent_color": "#2563eb",
  "section_header_size": "10.5px",
  "section_header_weight": "700",
  "section_header_transform": "uppercase",
  "section_header_color": "#2563eb",
  "section_divider": "border-bottom: 1.5px solid #e2e8f0",
  "header_divider": "border-top: 2px solid #2563eb",
  "contact_color": "#475569",
  "body_color": "#1e293b",
  "muted_color": "#64748b",
  "margin": "0.7in",
  "page_margin_top": "0.65in"
}"""
    story.append(Paragraph(sample_styles_json.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("<b>Step 5:</b> Configure ReportLab PDF Parameters (JSON Object):", bullet_style))
    story.append(Paragraph("The <code>pdf_config</code> JSON dict controls ReportLab PDF generation margins, sizes, and colors:", body_style))
    sample_pdf_json = """{
  "name_size": 18,
  "name_color": "#0f172a",
  "accent": "#2563eb",
  "section_size": 10.5,
  "body_size": 9.5,
  "sub_size": 9,
  "left_margin": 0.7,
  "right_margin": 0.7,
  "top_margin": 0.65,
  "bottom_margin": 0.6,
  "section_rule_color": "#e2e8f0",
  "header_rule_color": "#2563eb",
  "header_rule_width": 2,
  "section_rule_width": 0.75
}"""
    story.append(Paragraph(sample_pdf_json.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("<b>Step 6:</b> Click <b>Save</b>. The new template immediately becomes selectable in the Builder Grid, Live Preview, and PDF export!", note_style))
    story.append(Spacer(1, 10))

    # ── PART 3: ATS SCORING CONFIG & MANAGEMENT ──
    story.append(Paragraph("4. Part 3 — Managing ATS Scoring & System Data", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=8))

    story.append(Paragraph(
        "You can tune the weights of the ATS scoring algorithm from <b>ATS $\\rightarrow$ ATS Configs</b> at <code>/admin/ats/atsconfig/</code>.",
        body_style
    ))

    ats_table_data = [
        [Paragraph("Config Key", table_header_style), Paragraph("Default Value", table_header_style), Paragraph("Description", table_header_style)],
        [Paragraph("<code>keyword_weight</code>", table_cell_style), Paragraph("<code>0.40</code> (40%)", table_cell_style), Paragraph("Weight given to job description keyword matching score", table_cell_style)],
        [Paragraph("<code>section_weight</code>", table_cell_style), Paragraph("<code>0.25</code> (25%)", table_cell_style), Paragraph("Weight given to section completeness check score", table_cell_style)],
        [Paragraph("<code>format_weight</code>", table_cell_style), Paragraph("<code>0.20</code> (20%)", table_cell_style), Paragraph("Weight given to ATS formatting and structure check score", table_cell_style)],
        [Paragraph("<code>readability_weight</code>", table_cell_style), Paragraph("<code>0.15</code> (15%)", table_cell_style), Paragraph("Weight given to text word count and readability score", table_cell_style)],
        [Paragraph("<code>min_skills_count</code>", table_cell_style), Paragraph("<code>8</code>", table_cell_style), Paragraph("Minimum recommended skills count threshold", table_cell_style)],
        [Paragraph("<code>min_word_count</code>", table_cell_style), Paragraph("<code>200</code>", table_cell_style), Paragraph("Minimum recommended resume total word count threshold", table_cell_style)],
    ]
    t_ats = Table(ats_table_data, colWidths=[130, 100, 290])
    t_ats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ats)
    story.append(Spacer(1, 10))

    # ── CLI COMMANDS REFERENCE ──
    story.append(Paragraph("5. Management CLI Commands Reference", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=8))

    cmd_data = [
        [Paragraph("Command", table_header_style), Paragraph("Purpose & Description", table_header_style)],
        [Paragraph("<code>python manage.py seed_data</code>", table_cell_style), Paragraph("Seeds or updates all 15 default templates and AI app settings into DB", table_cell_style)],
        [Paragraph("<code>python manage.py createsuperuser</code>", table_cell_style), Paragraph("Creates an administrative user account for login access", table_cell_style)],
        [Paragraph("<code>python manage.py check</code>", table_cell_style), Paragraph("Runs Django system integrity check", table_cell_style)],
        [Paragraph("<code>python manage.py runserver</code>", table_cell_style), Paragraph("Launches local development server at http://127.0.0.1:8000", table_cell_style)],
    ]
    t_cmd = Table(cmd_data, colWidths=[200, 320])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 14))

    # ── FOOTER SUMMARY ──
    story.append(Paragraph("Summary Verification Checklist:", h2_style))
    story.append(Paragraph("✓ <b>AI Settings:</b> Check <code>/admin/accounts/appsettings/</code> to set provider & API key.<br/>"
                           "✓ <b>Templates:</b> Check <code>/admin/resume/resumetemplate/</code> to edit/add templates.<br/>"
                           "✓ <b>ATS Config:</b> Check <code>/admin/ats/atsconfig/</code> to tune weights.<br/>"
                           "✓ <b>Users:</b> Check <code>/admin/accounts/user/</code> to view active accounts and usage.", note_style))

    doc.build(story)
    print(f"Successfully generated {filename}")


if __name__ == '__main__':
    build_pdf()
