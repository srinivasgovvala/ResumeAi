"""
ATS-friendly PDF generator using ReportLab Platypus.
Supports all 15 resume templates with pixel-perfect matching to the HTML preview (preview.html).
Matches font families, centered header, dot-separated contact info, 2-column flex layout (title left, date right),
categorized skills, project links, custom section order, and hidden section toggling.
"""
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from .template_engine import get_template_config, get_section_order, detect_fresher


def _hex(h):
    if not h:
        return colors.Color(0, 0, 0)
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return colors.Color(r / 255, g / 255, b / 255)


def _get_reportlab_fonts(font_family_str):
    """Map template CSS font_family string to ReportLab standard fonts."""
    s = (font_family_str or '').lower()
    if any(f in s for f in ['times', 'georgia', 'palatino', 'garamond', 'antiqua', 'serif']):
        return 'Times-Roman', 'Times-Bold'
    elif any(f in s for f in ['courier', 'console', 'monospace']):
        return 'Courier', 'Courier-Bold'
    else:
        return 'Helvetica', 'Helvetica-Bold'


def _make_styles(p, font_family='Arial'):
    """Build paragraph styles from PDF config p and font_family."""
    f_reg, f_bold = _get_reportlab_fonts(font_family)
    accent = _hex(p['accent'])
    body_c = _hex(p.get('body_color', '#1e293b'))
    muted_c = _hex(p.get('muted_color', '#64748b'))
    name_c = _hex(p['name_color'])

    name_style = ParagraphStyle(
        'Name', fontSize=p['name_size'], fontName=f_bold,
        alignment=TA_CENTER, spaceAfter=4, textColor=name_c, leading=p['name_size'] * 1.15
    )
    contact_style = ParagraphStyle(
        'Contact', fontSize=p['sub_size'], fontName=f_reg,
        alignment=TA_CENTER, spaceAfter=6, textColor=muted_c, leading=p['sub_size'] * 1.35
    )
    section_style = ParagraphStyle(
        'Section', fontSize=p['section_size'], fontName=f_bold,
        spaceBefore=8, spaceAfter=2, textColor=accent,
        leading=p['section_size'] * 1.2
    )
    body_style = ParagraphStyle(
        'Body', fontSize=p['body_size'], fontName=f_reg,
        leading=p['body_size'] * 1.45, spaceAfter=3, textColor=body_c
    )
    bullet_style = ParagraphStyle(
        'Bullet', fontSize=p['body_size'], fontName=f_reg,
        leading=p['body_size'] * 1.4, leftIndent=10, spaceAfter=1, textColor=body_c
    )
    job_title_style = ParagraphStyle(
        'JobTitle', fontSize=p['body_size'] + 0.5, fontName=f_bold,
        spaceAfter=1, textColor=body_c, leading=(p['body_size'] + 0.5) * 1.25
    )
    date_right_style = ParagraphStyle(
        'DateRight', fontSize=p['sub_size'], fontName=f_reg,
        alignment=TA_RIGHT, spaceAfter=1, textColor=muted_c, leading=p['sub_size'] * 1.25
    )
    sub_style = ParagraphStyle(
        'Sub', fontSize=p['sub_size'], fontName=f_reg,
        textColor=muted_c, spaceAfter=2, leading=p['sub_size'] * 1.3
    )
    return {
        'name': name_style, 'contact': contact_style, 'section': section_style,
        'body': body_style, 'bullet': bullet_style,
        'job_title': job_title_style, 'date_right': date_right_style, 'sub': sub_style,
        'accent': accent, 'muted': muted_c, 'f_bold': f_bold, 'f_reg': f_reg
    }


def _section_block(title, p_cfg, st):
    """Return [header paragraph, optional rule] for a section."""
    items = [Paragraph(title.upper(), st['section'])]
    if p_cfg.get('section_rule_width', 0) > 0:
        items.append(HRFlowable(
            width='100%',
            thickness=p_cfg['section_rule_width'],
            color=_hex(p_cfg['section_rule_color']),
            spaceAfter=4,
        ))
    else:
        items.append(Spacer(1, 4))
    return items


def _safe(v):
    if v is None:
        return ''
    return str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _flex_header_row(left_text, right_text, st, page_width):
    """Create a 2-column table: left_text on left, right_text right-aligned."""
    p_left = Paragraph(left_text, st['job_title'])
    p_right = Paragraph(right_text, st['date_right'])
    t = Table([[p_left, p_right]], colWidths=[page_width * 0.72, page_width * 0.28])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


def _render_experience_block(exp, st, page_width):
    rows = []
    title_line = _safe(exp.get('title', ''))
    company = _safe(exp.get('company', ''))
    location = _safe(exp.get('location', ''))
    start = _safe(exp.get('start_date', ''))
    end = _safe(exp.get('end_date', 'Present'))
    if exp.get('current'):
        end = 'Present'
    date_part = f'{start} – {end}' if (start or end) else ''

    rows.append(_flex_header_row(f'<b>{title_line}</b>', date_part, st, page_width))
    loc_part = f' &middot; {location}' if location else ''
    sub_line = f'{company}{loc_part}'
    rows.append(Paragraph(sub_line, st['sub']))

    bullets = exp.get('bullets', [])
    if isinstance(bullets, str):
        bullets = [b.strip() for b in bullets.split('\n') if b.strip()]
    for b in bullets:
        rows.append(Paragraph(f'&bull; {_safe(b)}', st['bullet']))
    rows.append(Spacer(1, 5))
    return rows


def _render_education_block(edu, st, page_width):
    rows = []
    degree = _safe(edu.get('degree', ''))
    field = _safe(edu.get('field', ''))
    school = _safe(edu.get('school', ''))
    location = _safe(edu.get('location', ''))
    grad = _safe(edu.get('graduation_year', ''))
    gpa = _safe(edu.get('gpa', ''))
    courses = _safe(edu.get('courses', ''))

    full_degree = f'{degree} in {field}' if field else degree
    rows.append(_flex_header_row(f'<b>{full_degree}</b>', grad, st, page_width))

    sub_parts = [school]
    if location:
        sub_parts.append(location)
    if gpa:
        sub_parts.append(f'GPA: {gpa}')
    rows.append(Paragraph(' &middot; '.join(sub_parts), st['sub']))

    if courses:
        rows.append(Paragraph(f'Relevant Courses: {courses}', st['sub']))
    rows.append(Spacer(1, 5))
    return rows


def generate_pdf(resume):
    style_key = getattr(resume, 'template_style', None) or 'classic'
    customization = getattr(resume, 'resume_customization', None) or {}
    cfg = get_template_config(style_key, customization)
    p = cfg['pdf']
    styles_cfg = cfg.get('styles', {})
    font_family = styles_cfg.get('font_family', 'Arial')
    st = _make_styles(p, font_family)

    is_fresher = detect_fresher(resume)

    # Custom section order & hidden sections support
    hidden_sections = set(customization.get('hidden_sections') or [])
    custom_order = customization.get('section_order')
    if custom_order and isinstance(custom_order, list):
        section_order = custom_order
    else:
        section_order = get_section_order(style_key, is_fresher)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=p['left_margin'] * inch,
        rightMargin=p['right_margin'] * inch,
        topMargin=p['top_margin'] * inch,
        bottomMargin=p['bottom_margin'] * inch,
    )
    page_width = letter[0] - (p['left_margin'] + p['right_margin']) * inch

    story = []
    accent_hex = p.get('accent', '#2563eb')

    # ── HEADER ── Name centered, contact info single line centered (matches preview.html)
    name = _safe(resume.full_name or resume.user.full_name)
    story.append(Paragraph(name, st['name']))

    contact_parts = []
    contact_hex = styles_cfg.get('contact_color', '#475569')

    def _url_link(url):
        if not url:
            return ''
        url_str = str(url).strip()
        disp = _safe(url_str.replace('https://', '').replace('http://', ''))
        href = url_str if url_str.startswith(('http://', 'https://')) else f'https://{url_str}'
        return f'<a href="{_safe(href)}" color="{contact_hex}"><u>{disp}</u></a>'

    if resume.email:
        email_clean = _safe(resume.email)
        contact_parts.append(f'<a href="mailto:{email_clean}" color="{contact_hex}"><u>{email_clean}</u></a>')
    if resume.phone:
        contact_parts.append(_safe(resume.phone))
    if resume.location:
        contact_parts.append(_safe(resume.location))
    if resume.linkedin_url:
        link = _url_link(resume.linkedin_url)
        if link:
            contact_parts.append(link)
    if resume.github_url:
        link = _url_link(resume.github_url)
        if link:
            contact_parts.append(link)
    if resume.portfolio_url:
        link = _url_link(resume.portfolio_url)
        if link:
            contact_parts.append(link)
    if resume.website_url:
        link = _url_link(resume.website_url)
        if link:
            contact_parts.append(link)

    if contact_parts:
        contact_html = ' &middot; '.join(contact_parts)
        story.append(Paragraph(contact_html, st['contact']))

    # Header divider line
    if p.get('header_rule_width', 0) > 0:
        story.append(HRFlowable(
            width='100%',
            thickness=p['header_rule_width'],
            color=_hex(p['header_rule_color']),
            spaceAfter=8,
        ))
    else:
        story.append(Spacer(1, 8))

    # ── SECTIONS (ordered by template/custom order) ─────────────────────────
    def add_section(title):
        story.extend(_section_block(title, p, st))

    for section_key in section_order:
        if section_key == 'header' or section_key in hidden_sections:
            continue

        elif section_key == 'summary':
            sum_text = resume.professional_summary or resume.career_objective
            if sum_text:
                title = 'Professional Summary' if resume.professional_summary else 'Career Objective'
                block = _section_block(title, p, st)
                block.append(Paragraph(_safe(sum_text), st['body']))
                story.append(KeepTogether(block))

        elif section_key == 'objective':
            obj_text = resume.career_objective or resume.professional_summary
            if obj_text:
                title = 'Career Objective' if resume.career_objective else 'Professional Summary'
                block = _section_block(title, p, st)
                block.append(Paragraph(_safe(obj_text), st['body']))
                story.append(KeepTogether(block))

        elif section_key == 'experience' and resume.experience:
            add_section('Work Experience')
            for exp in resume.experience:
                story.append(KeepTogether(_render_experience_block(exp, st, page_width)))

        elif section_key == 'internships' and resume.internships:
            add_section('Internships')
            for exp in resume.internships:
                story.append(KeepTogether(_render_experience_block(exp, st, page_width)))

        elif section_key == 'education' and resume.education:
            add_section('Education')
            for edu in resume.education:
                story.append(KeepTogether(_render_education_block(edu, st, page_width)))

        elif section_key == 'skills' and resume.skills:
            # Skills Summary - categorized or flat format
            block = _section_block('Skills Summary', p, st)
            skills_data = resume.skills
            if isinstance(skills_data, dict):
                skill_lines = []
                category_labels = [
                    ('languages', 'Languages'),
                    ('frameworks', 'Frameworks'),
                    ('cloud', 'Cloud/DevOps'),
                    ('tools', 'Tools'),
                    ('soft', 'Soft Skills')
                ]
                for cat_key, label in category_labels:
                    items = skills_data.get(cat_key, [])
                    if items:
                        if isinstance(items, list):
                            items_str = ", ".join(_safe(s) for s in items if s)
                        elif isinstance(items, str):
                            items_str = _safe(items)
                        else:
                            items_str = _safe(str(items))
                        if items_str:
                            skill_lines.append(f'<b>{label}:</b> {items_str}')
                if skill_lines:
                    skills_html = '<br/>'.join(skill_lines)
                    block.append(Paragraph(skills_html, st['body']))
            elif isinstance(skills_data, list) and len(skills_data) > 0:
                skills_html = " &middot; ".join(_safe(s) for s in skills_data if s)
                block.append(Paragraph(skills_html, st['body']))
            else:
                skills_text = _safe(str(skills_data)) if skills_data else ''
                if skills_text:
                    block.append(Paragraph(skills_text, st['body']))
            story.append(KeepTogether(block))

        elif section_key == 'projects' and resume.projects:
            add_section('Projects')
            for proj in resume.projects:
                rows = []
                pname = _safe(proj.get('name', ''))
                ptech = _safe(proj.get('technologies', ''))
                pdesc = proj.get('description', '')
                pbullets = proj.get('bullets', [])
                purl = _safe(proj.get('url', ''))
                pgithub = _safe(proj.get('github', ''))

                links = []
                if purl:
                    purl_href = purl if purl.startswith(('http://', 'https://')) else f'https://{purl}'
                    links.append(f'<a href="{_safe(purl_href)}" color="{accent_hex}"><u>Live</u></a>')
                if pgithub:
                    pgithub_href = pgithub if pgithub.startswith(('http://', 'https://')) else f'https://{pgithub}'
                    links.append(f'<a href="{_safe(pgithub_href)}" color="{accent_hex}"><u>Source Code</u></a>')

                left_title = f'<b>{pname}</b>'
                right_links = ' &middot; '.join(links) if links else ''
                rows.append(_flex_header_row(left_title, right_links, st, page_width))

                if ptech:
                    rows.append(Paragraph(ptech, st['sub']))

                lines = []
                if isinstance(pbullets, list) and len(pbullets) > 0:
                    lines = [str(b).strip().lstrip('•-* ').strip() for b in pbullets if b]
                elif pdesc:
                    if isinstance(pdesc, list):
                        lines = [str(b).strip().lstrip('•-* ').strip() for b in pdesc if b]
                    else:
                        lines = [l.strip().lstrip('•-* ').strip() for l in str(pdesc).split('\n') if l.strip()]

                for l in lines:
                    if l:
                        rows.append(Paragraph(f'&bull; {_safe(l)}', st['bullet']))
                rows.append(Spacer(1, 4))
                story.append(KeepTogether(rows))

        elif section_key == 'certifications' and resume.certifications:
            block = _section_block('Certifications', p, st)
            for cert in resume.certifications:
                if isinstance(cert, dict):
                    cname = _safe(cert.get('name', ''))
                    cissuer = _safe(cert.get('issuer', ''))
                    cyear = _safe(cert.get('year', '') or cert.get('date', ''))
                    curl = _safe(cert.get('url', ''))
                    line = cname
                    if cissuer:
                        line += f' &mdash; {cissuer}'
                    if cyear:
                        line += f' ({cyear})'
                    if curl:
                        line += f' <a href="{curl}" color="{accent_hex}"><u>[link]</u></a>'
                else:
                    line = _safe(str(cert))
                block.append(Paragraph(f'&bull; {line}', st['bullet']))
            story.append(KeepTogether(block))

        elif section_key == 'achievements' and resume.achievements:
            block = _section_block('Key Achievements', p, st)
            for ach in resume.achievements:
                if isinstance(ach, dict):
                    atitle = _safe(ach.get('title', ach.get('text', '')))
                    adesc = _safe(ach.get('description', ''))
                    line = f'<b>{atitle}</b>'
                    if adesc:
                        line += f' &mdash; {adesc}'
                else:
                    line = _safe(str(ach))
                block.append(Paragraph(f'&bull; {line}', st['bullet']))
            story.append(KeepTogether(block))

        elif section_key == 'publications' and resume.publications:
            add_section('Publications')
            for pub in resume.publications:
                if isinstance(pub, dict):
                    ptitle = _safe(pub.get('title', ''))
                    pauth = _safe(pub.get('authors', ''))
                    pvenue = _safe(pub.get('venue', ''))
                    pyear = _safe(pub.get('year', ''))
                    purl = _safe(pub.get('url', ''))
                    rows = []
                    rows.append(Paragraph(f'<b>{ptitle}</b>', st['job_title']))
                    sub_parts = [x for x in [pauth, pvenue, pyear] if x]
                    if sub_parts:
                        sub_text = ' &middot; '.join(sub_parts)
                        if purl:
                            sub_text += f' <a href="{purl}" color="{accent_hex}"><u>[Link]</u></a>'
                        rows.append(Paragraph(sub_text, st['sub']))
                    rows.append(Spacer(1, 4))
                    story.append(KeepTogether(rows))
                else:
                    story.append(Paragraph(f'&bull; {_safe(str(pub))}', st['bullet']))

        elif section_key == 'awards' and resume.awards:
            block = _section_block('Awards & Honors', p, st)
            awards_list = resume.awards
            if isinstance(awards_list, list):
                awards_text = ' &middot; '.join(
                    _safe(a.get('title', a.get('text', str(a))) if isinstance(a, dict) else str(a))
                    for a in awards_list if a
                )
            else:
                awards_text = _safe(str(awards_list))
            block.append(Paragraph(awards_text, st['body']))
            story.append(KeepTogether(block))

        elif section_key == 'languages' and resume.languages:
            block = _section_block('Languages', p, st)
            langs_list = resume.languages
            if isinstance(langs_list, list):
                langs_text = ' &middot; '.join(
                    _safe(l.get('name', str(l)) if isinstance(l, dict) else str(l))
                    for l in langs_list if l
                )
            else:
                langs_text = _safe(str(langs_list))
            block.append(Paragraph(langs_text, st['body']))
            story.append(KeepTogether(block))

        elif section_key == 'volunteer' and resume.volunteer_experience:
            add_section('Volunteer Experience')
            for vol in resume.volunteer_experience:
                if isinstance(vol, dict):
                    story.append(KeepTogether(_render_experience_block(vol, st, page_width)))
                else:
                    story.append(Paragraph(f'&bull; {_safe(str(vol))}', st['bullet']))

    doc.build(story)
    return buffer.getvalue()
