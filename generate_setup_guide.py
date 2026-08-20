"""
Run this script once to generate the PDF setup guide:
    python generate_setup_guide.py
Output: ATS_Builder_Setup_Guide.pdf (in the project root)
"""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import PageBreak

# ── Colour palette ────────────────────────────────────────────────────────────
BLUE      = colors.HexColor('#2563eb')
BLUE_DARK = colors.HexColor('#1e40af')
BLUE_SOFT = colors.HexColor('#eff6ff')
SLATE     = colors.HexColor('#1e293b')
GREY      = colors.HexColor('#64748b')
GREY_LT   = colors.HexColor('#f1f5f9')
GREEN     = colors.HexColor('#16a34a')
GREEN_LT  = colors.HexColor('#f0fdf4')
ORANGE    = colors.HexColor('#d97706')
ORANGE_LT = colors.HexColor('#fffbeb')
RED       = colors.HexColor('#dc2626')
RED_LT    = colors.HexColor('#fef2f2')
WHITE     = colors.white
BLACK     = colors.HexColor('#0f172a')

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s['cover_title'] = ParagraphStyle(
        'cover_title', fontSize=28, fontName='Helvetica-Bold',
        alignment=TA_CENTER, textColor=WHITE, spaceAfter=8, leading=34
    )
    s['cover_sub'] = ParagraphStyle(
        'cover_sub', fontSize=13, fontName='Helvetica',
        alignment=TA_CENTER, textColor=colors.HexColor('#bfdbfe'), spaceAfter=6
    )
    s['cover_note'] = ParagraphStyle(
        'cover_note', fontSize=10, fontName='Helvetica',
        alignment=TA_CENTER, textColor=colors.HexColor('#93c5fd')
    )

    s['h1'] = ParagraphStyle(
        'h1', fontSize=18, fontName='Helvetica-Bold',
        textColor=BLUE_DARK, spaceBefore=14, spaceAfter=6, leading=22
    )
    s['h2'] = ParagraphStyle(
        'h2', fontSize=13, fontName='Helvetica-Bold',
        textColor=SLATE, spaceBefore=12, spaceAfter=4, leading=16
    )
    s['h3'] = ParagraphStyle(
        'h3', fontSize=11, fontName='Helvetica-Bold',
        textColor=SLATE, spaceBefore=8, spaceAfter=3
    )

    s['body'] = ParagraphStyle(
        'body', fontSize=10, fontName='Helvetica',
        textColor=BLACK, leading=15, spaceAfter=4, alignment=TA_JUSTIFY
    )
    s['body_small'] = ParagraphStyle(
        'body_small', fontSize=9, fontName='Helvetica',
        textColor=GREY, leading=13, spaceAfter=3
    )

    s['step_num'] = ParagraphStyle(
        'step_num', fontSize=9, fontName='Helvetica-Bold',
        textColor=WHITE, alignment=TA_CENTER
    )
    s['step_label'] = ParagraphStyle(
        'step_label', fontSize=10, fontName='Helvetica-Bold',
        textColor=SLATE, spaceAfter=2
    )
    s['step_body'] = ParagraphStyle(
        'step_body', fontSize=9.5, fontName='Helvetica',
        textColor=BLACK, leading=14, spaceAfter=2
    )

    s['code'] = ParagraphStyle(
        'code', fontSize=9, fontName='Courier',
        textColor=colors.HexColor('#1e293b'),
        backColor=GREY_LT, leftIndent=8, rightIndent=8,
        spaceAfter=4, leading=14
    )
    s['code_key'] = ParagraphStyle(
        'code_key', fontSize=8.5, fontName='Courier-Bold',
        textColor=BLUE_DARK, backColor=GREY_LT,
        leftIndent=8, spaceAfter=2, leading=13
    )

    s['note'] = ParagraphStyle(
        'note', fontSize=9, fontName='Helvetica',
        textColor=colors.HexColor('#92400e'),
        leading=13
    )
    s['tip'] = ParagraphStyle(
        'tip', fontSize=9, fontName='Helvetica',
        textColor=colors.HexColor('#166534'),
        leading=13
    )
    s['warn'] = ParagraphStyle(
        'warn', fontSize=9, fontName='Helvetica',
        textColor=RED, leading=13
    )
    s['toc_item'] = ParagraphStyle(
        'toc_item', fontSize=10, fontName='Helvetica',
        textColor=SLATE, leading=16, leftIndent=12
    )
    s['toc_section'] = ParagraphStyle(
        'toc_section', fontSize=11, fontName='Helvetica-Bold',
        textColor=BLUE_DARK, leading=18, spaceBefore=4
    )
    return s


# ── Helpers ───────────────────────────────────────────────────────────────────
def hr(story, color=colors.HexColor('#e2e8f0'), thickness=0.8):
    story.append(HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=6, spaceBefore=2))


def info_box(story, s, text, bg=BLUE_SOFT, border=BLUE, style_key='note'):
    data = [[Paragraph(text, s[style_key])]]
    t = Table(data, colWidths=[455])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX',        (0, 0), (-1, -1), 0.8, border),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING',   (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 7),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [bg]),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))


def step_row(story, s, number, label, body_lines):
    """Renders a numbered step with a blue badge."""
    badge = Table([[Paragraph(str(number), s['step_num'])]], colWidths=[22], rowHeights=[22])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE),
        ('ROUNDEDCORNERS', [11]),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    content = [Paragraph(f'<b>{label}</b>', s['step_label'])]
    for line in body_lines:
        content.append(Paragraph(line, s['step_body']))

    from reportlab.platypus import KeepTogether
    row = Table([[badge, content]], colWidths=[30, 437])
    row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(KeepTogether(row))


def section_banner(story, s, title, subtitle=''):
    data = [[Paragraph(title, s['h1'])]]
    if subtitle:
        data[0].append(Paragraph(subtitle, s['body_small']))
    banner = Table([[Paragraph(title, s['h1'])]
                    if not subtitle else
                    [Paragraph(title + '<br/><font size=9 color="#64748b">' + subtitle + '</font>', s['h1'])]],
                   colWidths=[467])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_SOFT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, -1), 2, BLUE),
    ]))
    story.append(banner)
    story.append(Spacer(1, 8))


def code_block(story, s, lines):
    for line in lines:
        story.append(Paragraph(line, s['code']))
    story.append(Spacer(1, 4))


# ── Build document ────────────────────────────────────────────────────────────
def build_pdf():
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title='ATS Resume Builder — Setup Guide',
        author='ATS Resume Builder',
    )
    s = make_styles()
    story = []

    # ── COVER PAGE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 60))
    cover = Table(
        [[Paragraph('ATS Resume Builder', s['cover_title'])],
         [Paragraph('Complete Setup Guide', s['cover_sub'])],
         [Spacer(1, 6)],
         [Paragraph('Google OAuth 2.0 · OpenRouter AI · Django Configuration', s['cover_note'])],
         [Spacer(1, 20)],
         [Paragraph('Step-by-step instructions to get every API key and configure your app', s['cover_note'])]],
        colWidths=[467]
    )
    cover.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BLUE_DARK),
        ('LEFTPADDING', (0, 0), (-1, -1), 30),
        ('RIGHTPADDING', (0, 0), (-1, -1), 30),
        ('TOPPADDING', (0, 0), (-1, -1), 40),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
        ('ROUNDEDCORNERS', [8]),
    ]))
    story.append(cover)
    story.append(Spacer(1, 30))

    # Quick legend
    legend_data = [
        [Paragraph('📌  URL to visit', s['body_small']),
         Paragraph('⌨️  Value to type / paste', s['body_small']),
         Paragraph('⚠️  Important warning', s['body_small'])],
    ]
    legend = Table(legend_data, colWidths=[155, 155, 157])
    legend.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GREY_LT),
        ('BOX', (0, 0), (-1, -1), 0.5, GREY),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cbd5e1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(legend)
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ─────────────────────────────────────────────────────
    story.append(Paragraph('Table of Contents', s['h1']))
    hr(story, BLUE, 1.5)
    toc = [
        ('Part 1', 'Google OAuth 2.0 Credentials', 'Google Cloud Console → OAuth 2.0 Client ID'),
        ('Part 2', 'Enable Google Drive API',       'Add Drive scope to your OAuth consent screen'),
        ('Part 3', 'OpenRouter API Key',             'openrouter.ai → free account → API key'),
        ('Part 4', 'Configure .env File',            'Paste all keys into your local .env'),
        ('Part 5', 'Django Admin — Link OAuth App',  'Social Applications in /admin/'),
        ('Part 6', 'Test Everything',                'Checklist to verify each integration works'),
        ('Part 7', 'Vercel Production Deployment',   'Add secrets to Vercel dashboard'),
    ]
    for part, title, desc in toc:
        story.append(Paragraph(f'<b>{part}</b> — {title}', s['toc_section']))
        story.append(Paragraph(desc, s['toc_item']))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 1 — GOOGLE OAUTH CREDENTIALS
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 1: Google OAuth 2.0 Credentials',
                   'Get GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET')

    story.append(Paragraph(
        'Google OAuth lets users sign in with their Google account and grants access to Google Drive. '
        'You need two values: a Client ID and a Client Secret. Both come from Google Cloud Console.',
        s['body']
    ))
    story.append(Spacer(1, 8))

    info_box(story, s,
             '📌  Open your browser and go to:  https://console.cloud.google.com',
             bg=BLUE_SOFT, border=BLUE, style_key='note')

    # Steps
    steps_p1 = [
        (1, 'Create or select a project',
         ['Click the project dropdown at the top-left of the Google Cloud Console.',
          'Click <b>NEW PROJECT</b>, give it a name (e.g. "ATS Resume Builder"), then click <b>Create</b>.',
          'Wait for the project to be created, then select it from the dropdown.']),

        (2, 'Open the OAuth consent screen',
         ['In the left sidebar go to:  <b>APIs &amp; Services → OAuth consent screen</b>',
          'Choose <b>External</b> (allows any Google account to sign in) and click <b>Create</b>.']),

        (3, 'Fill in the App Information form',
         ['<b>App name:</b>  ATS Resume Builder',
          '<b>User support email:</b>  your email address',
          '<b>App logo:</b>  optional — skip for now',
          '<b>Developer contact information:</b>  your email address again',
          'Click <b>Save and Continue</b>.']),

        (4, 'Add OAuth Scopes',
         ['Click <b>Add or Remove Scopes</b>.',
          'Search for and select these three scopes:',
          '  ✓  .../auth/userinfo.email',
          '  ✓  .../auth/userinfo.profile',
          '  ✓  .../auth/drive.file',
          'Click <b>Update</b>, then <b>Save and Continue</b>.']),

        (5, 'Add Test Users (while app is in Testing mode)',
         ['Click <b>Add Users</b> and enter your own Gmail address.',
          'This lets you test login before publishing the app.',
          'Click <b>Save and Continue</b> → <b>Back to Dashboard</b>.']),

        (6, 'Create the OAuth 2.0 Client ID',
         ['Go to:  <b>APIs &amp; Services → Credentials</b>',
          'Click <b>+ Create Credentials</b> → choose <b>OAuth client ID</b>.',
          '<b>Application type:</b>  Web application',
          '<b>Name:</b>  ATS Resume Builder (or any name)']),

        (7, 'Add Authorised Redirect URIs',
         ['Scroll down to the <b>Authorised redirect URIs</b> section.',
          'Click <b>+ Add URI</b> and add the following (both are needed):',
          '  http://127.0.0.1:8000/accounts/google/login/callback/',
          '  http://localhost:8000/accounts/google/login/callback/',
          'For production, also add:',
          '  https://YOUR-APP.vercel.app/accounts/google/login/callback/',
          'Click <b>Create</b>.']),

        (8, 'Copy your credentials',
         ['A popup shows your <b>Client ID</b> and <b>Client Secret</b>.',
          'Click <b>Download JSON</b> to save a backup, OR',
          'Copy each value and paste them into your .env file (see Part 4).',
          '⚠️  Never share or commit these values to GitHub.']),
    ]

    for num, label, body in steps_p1:
        step_row(story, s, num, label, body)

    story.append(Spacer(1, 4))
    info_box(story, s,
             'Warning: If you see "Access blocked" during testing, '
             'make sure your Gmail address is added as a Test User in Step 5 and that the redirect URIs '
             'in Step 7 exactly match what your server is running on.',
             bg=ORANGE_LT, border=ORANGE, style_key='note')
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 2 — ENABLE GOOGLE DRIVE API
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 2: Enable Google Drive API',
                   'Required for saving resumes to Google Drive')

    story.append(Paragraph(
        'The Google Drive API must be explicitly enabled in your project before the OAuth '
        'drive.file scope will work. This is a one-time step per project.',
        s['body']
    ))
    story.append(Spacer(1, 6))

    steps_p2 = [
        (1, 'Open the API Library',
         ['In Google Cloud Console left sidebar go to:  <b>APIs &amp; Services → Library</b>']),

        (2, 'Search for Google Drive API',
         ['Type "Google Drive API" in the search box and press Enter.',
          'Click the <b>Google Drive API</b> result card.']),

        (3, 'Enable it',
         ['Click the blue <b>Enable</b> button.',
          'Wait a few seconds for it to activate.',
          'You will be taken to the API overview page — that means it worked.']),

        (4, 'Verify (optional)',
         ['Go to <b>APIs &amp; Services → Enabled APIs &amp; Services</b>.',
          '"Google Drive API" should appear in the list with status Enabled.']),
    ]

    for num, label, body in steps_p2:
        step_row(story, s, num, label, body)

    info_box(story, s,
             '✅  You do NOT need a separate service account for this project. '
             'The app uses each user\'s own Google account (via OAuth) to access their Drive. '
             'Files are stored in a folder called "ATS Resume Builder" in the user\'s Drive.',
             bg=GREEN_LT, border=GREEN, style_key='tip')
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 3 — OPENROUTER API KEY
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 3: OpenRouter API Key',
                   'Get OPENROUTER_API_KEY for the AI Career Assistant')

    story.append(Paragraph(
        'OpenRouter is a single API that gives access to many AI models (GPT-4o, Claude, Gemini, '
        'Llama, and more). The free tier includes credits to get started. '
        'Your key is kept server-side — it is never sent to the browser.',
        s['body']
    ))
    story.append(Spacer(1, 6))

    info_box(story, s,
             '📌  Open your browser and go to:  https://openrouter.ai',
             bg=BLUE_SOFT, border=BLUE, style_key='note')

    steps_p3 = [
        (1, 'Create a free account',
         ['Click <b>Sign Up</b> at the top-right.',
          'You can sign up with Google, GitHub, or email.',
          'Verify your email if prompted.']),

        (2, 'Go to the API Keys page',
         ['After logging in, click your avatar (top-right) → <b>Keys</b>.',
          'Or go directly to:  https://openrouter.ai/settings/keys']),

        (3, 'Create a new key',
         ['Click <b>Create Key</b>.',
          '<b>Name:</b>  ATS Resume Builder (or anything descriptive)',
          '<b>Credit limit:</b>  leave blank (unlimited from your balance) or set a monthly cap.',
          'Click <b>Create</b>.']),

        (4, 'Copy the key immediately',
         ['The key is shown only once — copy it now.',
          'It starts with:  sk-or-v1-...',
          'Paste it into your .env file (see Part 4).']),

        (5, 'Add credits (optional for free models)',
         ['Click <b>Credits</b> in the sidebar.',
          'Some models (e.g. meta-llama/llama-3.1-8b-instruct) are free with $0 balance.',
          'Add a small amount ($5) to unlock GPT-4o mini and other low-cost models.',
          'The default model in this app is <b>openai/gpt-4o-mini</b> (~$0.15 per 1M tokens).']),
    ]

    for num, label, body in steps_p3:
        step_row(story, s, num, label, body)

    info_box(story, s,
             '✅  Free alternative: set OPENROUTER_DEFAULT_MODEL=meta-llama/llama-3.1-8b-instruct '
             'in your .env. This model is free (rate-limited) and works well for resume tasks.',
             bg=GREEN_LT, border=GREEN, style_key='tip')
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 4 — CONFIGURE .env FILE
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 4: Configure Your .env File',
                   'Paste all keys into the local .env file')

    story.append(Paragraph(
        'The .env file lives in the root of your project (same folder as manage.py). '
        'It is listed in .gitignore so it is never committed to GitHub. '
        'Open it with any text editor and fill in all values.',
        s['body']
    ))
    story.append(Spacer(1, 6))

    info_box(story, s,
             '📌  File location:  C:\\Users\\srini\\Desktop\\projects\\New folder\\.env',
             bg=BLUE_SOFT, border=BLUE, style_key='note')

    story.append(Paragraph('<b>Complete .env template — fill every line:</b>', s['h3']))
    story.append(Spacer(1, 4))

    env_lines = [
        '# ── Django Core ───────────────────────────────────────────────',
        'SECRET_KEY=django-insecure-REPLACE-with-a-long-random-string',
        'DEBUG=True',
        'ALLOWED_HOSTS=localhost,127.0.0.1',
        '',
        '# ── Google OAuth (from Part 1) ────────────────────────────────',
        'GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com',
        'GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxx',
        '',
        '# ── OpenRouter AI (from Part 3) ───────────────────────────────',
        'OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'OPENROUTER_DEFAULT_MODEL=openai/gpt-4o-mini',
        '',
        '# ── Email (optional — console backend works for local dev) ────',
        'EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend',
        '',
        '# ── Production only (leave blank for local dev) ───────────────',
        '# DATABASE_URL=postgresql://user:pass@host:5432/dbname',
    ]
    for line in env_lines:
        if line.startswith('#'):
            story.append(Paragraph(line, s['code_key']))
        elif line == '':
            story.append(Spacer(1, 3))
        else:
            story.append(Paragraph(line, s['code']))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Generate a secure SECRET_KEY</b>', s['h3']))
    story.append(Paragraph('Run this command once in your terminal:', s['body']))
    code_block(story, s, [
        'venv\\Scripts\\activate',
        'python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"',
    ])
    story.append(Paragraph('Copy the output and paste it as the SECRET_KEY value.', s['body']))

    story.append(Spacer(1, 6))
    info_box(story, s,
             '⚠️  Never set DEBUG=True in production. '
             'Never commit .env to GitHub. '
             'The .gitignore in this project already excludes it.',
             bg=RED_LT, border=RED, style_key='warn')
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 5 — DJANGO ADMIN LINK
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 5: Django Admin — Link the OAuth App',
                   'Tell Django about your Google credentials via /admin/')

    story.append(Paragraph(
        'Django-allauth stores OAuth provider credentials in the database (not just env vars). '
        'The management command configure_google_oauth does this automatically, but you can '
        'also do it manually from the admin panel.',
        s['body']
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph('<b>Option A — Automatic (recommended)</b>', s['h3']))
    story.append(Paragraph(
        'After filling in .env, run these commands in your terminal:', s['body']))
    code_block(story, s, [
        'venv\\Scripts\\activate',
        'python manage.py migrate',
        'python manage.py seed_data',
        'python manage.py configure_site',
        'python manage.py configure_google_oauth',
        'python manage.py runserver',
    ])
    info_box(story, s,
             '✅  configure_google_oauth reads GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET from .env '
             'and creates the Social Application automatically. '
             'You will see "Google OAuth app created/updated" in the terminal.',
             bg=GREEN_LT, border=GREEN, style_key='tip')

    story.append(Spacer(1, 8))
    story.append(Paragraph('<b>Option B — Manual (via Admin panel)</b>', s['h3']))

    steps_p5 = [
        (1, 'Open Django Admin',
         ['Start the server:  python manage.py runserver',
          'Go to:  http://127.0.0.1:8000/admin/',
          'Log in with:  admin@admin.com  /  admin123']),

        (2, 'Go to Social Applications',
         ['In the left sidebar, find <b>Social Accounts → Social Applications</b>.',
          'Click <b>Add Social Application</b>.']),

        (3, 'Fill in the form',
         ['<b>Provider:</b>  Google',
          '<b>Name:</b>  Google OAuth',
          '<b>Client id:</b>  paste your GOOGLE_CLIENT_ID value',
          '<b>Secret key:</b>  paste your GOOGLE_CLIENT_SECRET value',
          '<b>Key:</b>  leave blank']),

        (4, 'Link to the Site',
         ['In the <b>Sites</b> section at the bottom, move "example.com" (or "127.0.0.1:8000")',
          'from "Available sites" to "Chosen sites" by double-clicking it.',
          'Click <b>Save</b>.']),
    ]

    for num, label, body in steps_p5:
        step_row(story, s, num, label, body)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 6 — TEST EVERYTHING
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 6: Test Everything',
                   'Verification checklist after setup')

    story.append(Paragraph(
        'Run through this checklist after completing Parts 1–5 to confirm everything is working.',
        s['body']
    ))
    story.append(Spacer(1, 6))

    checks = [
        ('Server starts cleanly',
         'python manage.py runserver — no errors, no warnings about missing settings'),
        ('Landing page loads',
         'http://127.0.0.1:8000/ → page renders with correct theme'),
        ('Email signup works',
         '/accounts/signup/ → fill form → should redirect to /dashboard/'),
        ('Email login works',
         '/accounts/login/ → email + password → redirects to /dashboard/'),
        ('Google button is visible',
         '/accounts/login/ → Google button appears (not the yellow warning banner)'),
        ('Google OAuth flow completes',
         'Click "Continue with Google" → Google asks for permission → redirects to /dashboard/'),
        ('Resume create works',
         '/dashboard/resumes/create/ → fill title → Create → builder page opens'),
        ('PDF download works',
         'In builder → Download PDF → file downloads (not a 500 error)'),
        ('ATS check works',
         '/ats/ → paste a job description + select resume → Run Check → score appears'),
        ('AI chat responds',
         '/ai/ → type a message → response appears (error if OPENROUTER_API_KEY is wrong/missing)'),
        ('Google Drive upload works',
         'In builder → Upload to Drive → success toast (only if signed in via Google)'),
        ('Admin panel accessible',
         'http://127.0.0.1:8000/admin/ → login → all models visible'),
    ]

    check_data = [[
        Paragraph('<b>#</b>', s['body_small']),
        Paragraph('<b>Check</b>', s['body_small']),
        Paragraph('<b>Expected result</b>', s['body_small']),
    ]]
    for i, (check, expected) in enumerate(checks, 1):
        check_data.append([
            Paragraph(str(i), s['body_small']),
            Paragraph(check, s['step_body']),
            Paragraph(expected, s['step_body']),
        ])

    check_table = Table(check_data, colWidths=[20, 175, 272])
    check_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GREY_LT]),
        ('BOX', (0, 0), (-1, -1), 0.5, GREY),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cbd5e1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(check_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph('<b>Common errors and fixes</b>', s['h3']))
    errors = [
        ('Error 400: invalid_request — Missing client_id',
         'GOOGLE_CLIENT_ID is empty in .env, or configure_google_oauth was not run.'),
        ('Error 403: Access denied',
         'Your Gmail is not added as a Test User in the OAuth consent screen (Step 5 of Part 1).'),
        ('Error 401 from OpenRouter',
         'OPENROUTER_API_KEY is wrong or missing in .env.'),
        ('Google button still shows warning banner',
         'Server was not restarted after editing .env. Stop and restart python manage.py runserver.'),
        ('Drive upload fails with "No Google credentials"',
         'User signed in via email, not Google. Drive requires Google OAuth login.'),
    ]
    err_data = [[
        Paragraph('<b>Error</b>', s['body_small']),
        Paragraph('<b>Fix</b>', s['body_small']),
    ]]
    for err, fix in errors:
        err_data.append([Paragraph(err, s['step_body']), Paragraph(fix, s['step_body'])])

    err_table = Table(err_data, colWidths=[220, 247])
    err_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), RED),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, RED_LT]),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#fca5a5')),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#fecaca')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(err_table)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # PART 7 — VERCEL PRODUCTION DEPLOYMENT
    # ═══════════════════════════════════════════════════════════════════════════
    section_banner(story, s, 'Part 7: Vercel Production Deployment',
                   'Add all secrets to Vercel dashboard — never hard-code them')

    story.append(Paragraph(
        'When deploying to Vercel, environment variables are set in the Vercel dashboard — '
        'not in .env (which stays local). Vercel injects them at build time and runtime.',
        s['body']
    ))
    story.append(Spacer(1, 6))

    steps_p7 = [
        (1, 'Create a PostgreSQL database',
         ['Recommended: Neon.tech (free tier — 512 MB)',
          'Sign up at https://neon.tech → New Project → copy the connection string.',
          'It looks like:  postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require']),

        (2, 'Push code to GitHub',
         ['git init',
          'git add .',
          'git commit -m "Initial commit"',
          'git remote add origin https://github.com/YOUR-USERNAME/ats-resume-builder.git',
          'git push -u origin main']),

        (3, 'Import project to Vercel',
         ['Go to https://vercel.com → New Project.',
          'Click Import on your GitHub repository.',
          '<b>Framework Preset:</b>  Other',
          '<b>Build Command:</b>  bash build_files.sh',
          '<b>Output Directory:</b>  staticfiles',
          'Do NOT deploy yet — add env vars first.']),

        (4, 'Add Environment Variables in Vercel',
         ['Click <b>Environment Variables</b> tab before deploying.',
          'Add each variable from the table below.']),

        (5, 'Update Google redirect URI',
         ['Back in Google Cloud Console → Credentials → your OAuth Client.',
          'Add a new Authorised Redirect URI:',
          '  https://YOUR-APP.vercel.app/accounts/google/login/callback/',
          'Click Save.']),

        (6, 'Deploy',
         ['Click <b>Deploy</b> in Vercel.',
          'Watch the build log — build_files.sh runs migrations, seeds data, configures OAuth.',
          'When finished, visit https://YOUR-APP.vercel.app']),

        (7, 'Update the Django Site domain',
         ['Go to https://YOUR-APP.vercel.app/admin/',
          'Log in → Sites → click "example.com" → change domain to YOUR-APP.vercel.app',
          'Click Save. This fixes allauth callback URLs in production.']),
    ]

    for num, label, body in steps_p7:
        step_row(story, s, num, label, body)

    story.append(Spacer(1, 8))
    story.append(Paragraph('<b>Vercel Environment Variables — complete list</b>', s['h3']))

    vercel_vars = [
        ('SECRET_KEY', 'Long random string — generate with Django command', 'Required'),
        ('DEBUG', 'False', 'Required'),
        ('ALLOWED_HOSTS', 'YOUR-APP.vercel.app', 'Required'),
        ('DATABASE_URL', 'postgresql://... from Neon.tech', 'Required'),
        ('GOOGLE_CLIENT_ID', 'From Google Cloud Console (Part 1)', 'For Google login'),
        ('GOOGLE_CLIENT_SECRET', 'From Google Cloud Console (Part 1)', 'For Google login'),
        ('OPENROUTER_API_KEY', 'sk-or-v1-... from openrouter.ai (Part 3)', 'For AI features'),
        ('OPENROUTER_DEFAULT_MODEL', 'openai/gpt-4o-mini', 'Optional'),
        ('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend', 'For email auth'),
        ('EMAIL_HOST', 'smtp.gmail.com', 'Optional'),
        ('EMAIL_HOST_USER', 'your-email@gmail.com', 'Optional'),
        ('EMAIL_HOST_PASSWORD', 'Gmail App Password', 'Optional'),
    ]

    vdata = [[
        Paragraph('<b>Variable</b>', s['body_small']),
        Paragraph('<b>Value</b>', s['body_small']),
        Paragraph('<b>Notes</b>', s['body_small']),
    ]]
    for var, val, note in vercel_vars:
        vdata.append([
            Paragraph(f'<font fontName="Courier" fontSize="8">{var}</font>', s['step_body']),
            Paragraph(val, s['step_body']),
            Paragraph(note, s['body_small']),
        ])

    vtable = Table(vdata, colWidths=[160, 175, 132])
    vtable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SLATE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, GREY_LT]),
        ('BOX', (0, 0), (-1, -1), 0.5, GREY),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cbd5e1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(vtable)
    story.append(Spacer(1, 12))

    info_box(story, s,
             '⚠️  Security reminder: Vercel encrypts environment variables at rest. '
             'Never put secrets in vercel.json or any file committed to GitHub. '
             'Rotate your keys if they are ever accidentally exposed.',
             bg=RED_LT, border=RED, style_key='warn')

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    hr(story, BLUE, 1)
    story.append(Paragraph(
        'ATS Resume Builder — Setup Guide  |  Generated 2026  |  '
        'Keep this document private — it describes your credential locations.',
        s['body_small']
    ))

    doc.build(story)
    return buf.getvalue()


if __name__ == '__main__':
    pdf_bytes = build_pdf()
    output_path = 'ATS_Builder_Setup_Guide.pdf'
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    print(f'PDF generated: {output_path}  ({len(pdf_bytes):,} bytes)')
