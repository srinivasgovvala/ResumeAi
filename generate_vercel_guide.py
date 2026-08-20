import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from reportlab.lib.units import inch

def create_guide():
    doc = SimpleDocTemplate(
        "ATS_Builder_Vercel_Deployment_Guide.pdf",
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor("#1a56db"),
        spaceAfter=15,
        alignment=1 # Center
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.HexColor("#4a5568"),
        spaceAfter=30,
        alignment=1
    )

    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor("#0d1b2e"),
        spaceBefore=20,
        spaceAfter=10
    )

    step_title_style = ParagraphStyle(
        'StepTitleStyle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor("#1a56db"),
        spaceBefore=15,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10,
        leading=16
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        textColor=colors.HexColor("#e2e8f0"),
        backColor=colors.HexColor("#1e293b"),
        borderPadding=(8, 10, 8, 10),
        spaceBefore=5,
        spaceAfter=15,
        leading=14
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor("#334155"),
        leftIndent=20,
        spaceAfter=5,
        bulletIndent=10,
        leading=16
    )

    story = []

    # Title
    story.append(Paragraph("Vercel Deployment Guide", title_style))
    story.append(Paragraph("The complete step-by-step guide to deploying ATS Resume Builder to production.", subtitle_style))

    story.append(Paragraph("Overview", heading_style))
    story.append(Paragraph("ATS Resume Builder is fully configured for serverless deployment on Vercel. Because Vercel functions are stateless and ephemeral, you cannot use the local SQLite database. You will need a cloud PostgreSQL database. This guide covers the end-to-step process.", normal_style))

    # Step 1
    story.append(Paragraph("Step 1: Set Up a Production Database", step_title_style))
    story.append(Paragraph("Vercel requires a hosted PostgreSQL database. We recommend <b>Neon.tech</b> or <b>Supabase</b> because they offer excellent free tiers.", normal_style))
    story.append(Paragraph("1. Go to <a href='https://neon.tech' color='#1a56db'>neon.tech</a> and create a free account.", bullet_style))
    story.append(Paragraph("2. Create a new project and database.", bullet_style))
    story.append(Paragraph("3. Copy the <b>Connection String</b>. It will look like this:", bullet_style))
    story.append(Paragraph("postgresql://user:password@ep-cool-snowflake-123.region.aws.neon.tech/neondb?sslmode=require", code_style))

    # Step 2
    story.append(Paragraph("Step 2: Push Your Code to GitHub", step_title_style))
    story.append(Paragraph("Vercel deploys directly from your GitHub repository. Your code is already pushed to GitHub!", normal_style))
    story.append(Paragraph("Your repository is located at: <b>https://github.com/srinivasgovvala/ResumeAi</b>", normal_style))

    # Step 3
    story.append(Paragraph("Step 3: Import Project into Vercel", step_title_style))
    story.append(Paragraph("1. Log in to <a href='https://vercel.com' color='#1a56db'>Vercel.com</a>.", bullet_style))
    story.append(Paragraph("2. Click <b>Add New</b> → <b>Project</b>.", bullet_style))
    story.append(Paragraph("3. Connect your GitHub account if you haven't already.", bullet_style))
    story.append(Paragraph("4. Find the <b>ResumeAi</b> repository and click <b>Import</b>.", bullet_style))

    # Step 4
    story.append(Paragraph("Step 4: Configure Vercel Build Settings", step_title_style))
    story.append(Paragraph("In the 'Configure Project' screen on Vercel, leave the 'Framework Preset' as <b>Other</b>. The project already includes a `vercel.json` and `build_files.sh` script, so Vercel will automatically detect how to build it.", normal_style))

    # Step 5
    story.append(PageBreak())
    story.append(Paragraph("Step 5: Add Environment Variables", step_title_style))
    story.append(Paragraph("Before clicking 'Deploy', open the <b>Environment Variables</b> dropdown and add the following keys. <b>This is the most critical step.</b>", normal_style))

    # Env Var Table
    data = [
        ['Key', 'Value Description'],
        ['DJANGO_SECRET_KEY', 'A strong, random password string (e.g., 50 random characters).'],
        ['DEBUG', 'False'],
        ['DATABASE_URL', 'Your PostgreSQL connection string from Neon.tech (Step 1).'],
        ['ALLOWED_HOSTS', '.vercel.app'],
        ['SITE_URL', 'Your expected Vercel URL (e.g., https://resumeai.vercel.app)'],
        ['OPENROUTER_API_KEY', 'Your OpenRouter API key.'],
        ['GOOGLE_CLIENT_ID', 'Your Google OAuth Client ID.'],
        ['GOOGLE_CLIENT_SECRET', 'Your Google OAuth Client Secret.'],
        ['EMAIL_HOST_USER', 'The email address you use for SMTP.'],
        ['EMAIL_HOST_PASSWORD', 'Your SMTP App Password.']
    ]

    t = Table(data, colWidths=[2.2 * inch, 4.3 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('FONTNAME', (0, 1), (0, -1), 'Courier-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor("#1a56db")),
        ('PADDING', (0, 1), (-1, -1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Step 6
    story.append(Paragraph("Step 6: Deploy!", step_title_style))
    story.append(Paragraph("1. Click the big <b>Deploy</b> button.", bullet_style))
    story.append(Paragraph("2. Vercel will install Python, run your migrations (`manage.py migrate`), configure your site, and deploy the application.", bullet_style))
    story.append(Paragraph("3. When it finishes, click <b>Continue to Dashboard</b>.", bullet_style))

    # Step 7
    story.append(Paragraph("Step 7: Final Google OAuth Fixes", step_title_style))
    story.append(Paragraph("Because your domain changed from `localhost` to a `.vercel.app` domain, you must update Google.", normal_style))
    story.append(Paragraph("1. Go to Google Cloud Console → Credentials → OAuth 2.0 Client IDs.", bullet_style))
    story.append(Paragraph("2. Add your new Vercel URL to <b>Authorized JavaScript origins</b> (e.g., `https://resumeai-yourname.vercel.app`).", bullet_style))
    story.append(Paragraph("3. Add the callback URL to <b>Authorized redirect URIs</b> (e.g., `https://resumeai-yourname.vercel.app/accounts/google/login/callback/`).", bullet_style))

    # Done
    story.append(Spacer(1, 30))
    story.append(Paragraph("Congratulations! Your App is Live.", heading_style))
    story.append(Paragraph("Your ATS Resume Builder is now fully deployed globally on Vercel's Edge Network.", normal_style))

    doc.build(story)
    print("PDF generated successfully: ATS_Builder_Vercel_Deployment_Guide.pdf")

if __name__ == "__main__":
    create_guide()