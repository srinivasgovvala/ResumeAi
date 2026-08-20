"""
ATS Scoring Engine
Scores resumes against job descriptions using keyword matching,
section analysis, formatting checks, and readability metrics.
Fully compatible with both Fresher (entry-level/student) and Experienced candidates.
"""
import re
import json
from collections import Counter


SECTION_KEYWORDS = {
    'contact': ['email', 'phone', 'linkedin', 'github', 'location', 'address'],
    'summary': ['summary', 'objective', 'profile', 'about', 'overview', 'career objective'],
    'experience': ['experience', 'work history', 'employment', 'career', 'work experience'],
    'internships': ['internship', 'internships', 'trainee', 'apprentice'],
    'education': ['education', 'academic', 'degree', 'university', 'college', 'school', 'gpa'],
    'skills': ['skills', 'technical skills', 'competencies', 'technologies', 'tools', 'languages', 'frameworks'],
    'projects': ['projects', 'portfolio', 'work samples', 'academic projects'],
    'certifications': ['certifications', 'certificates', 'licenses', 'credentials'],
    'awards': ['awards', 'honors', 'achievements', 'recognition'],
}

POWER_VERBS = [
    'achieved', 'built', 'created', 'designed', 'developed', 'drove', 'established',
    'generated', 'implemented', 'improved', 'increased', 'launched', 'led', 'managed',
    'optimized', 'reduced', 'spearheaded', 'streamlined', 'transformed', 'delivered',
    'executed', 'coordinated', 'collaborated', 'mentored', 'scaled', 'architected',
    'engineered', 'analyzed', 'programmed', 'authored', 'formulated', 'orchestrated'
]

WEAK_PHRASES = [
    'responsible for', 'helped with', 'assisted in', 'worked on', 'duties included',
    'tasks included', 'involved in',
]

FILLER_WORDS = ['very', 'really', 'quite', 'basically', 'just', 'actually']


def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return [w for w in text.split() if len(w) > 2]


def extract_phrases(text, n=2):
    words = tokenize(text)
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def detect_fresher_status(resume_data):
    """Determine if the candidate is a fresher/entry-level or experienced."""
    exp = resume_data.get('experience', [])
    if isinstance(exp, list) and len(exp) > 0:
        return False
    tpl = resume_data.get('template_style', '')
    if tpl == 'fresher':
        return True
    return True


def build_resume_text(resume_data):
    """Extract plain text from all resume fields including categorized skills & new sections."""
    if resume_data.get('resume_text'):
        return resume_data['resume_text']

    parts = []
    for field in ['full_name', 'email', 'phone', 'location', 'professional_summary', 'career_objective', 'website_url']:
        val = resume_data.get(field, '')
        if val:
            parts.append(str(val))

    # Experience
    for exp in resume_data.get('experience', []):
        if isinstance(exp, dict):
            parts.append(exp.get('title', ''))
            parts.append(exp.get('company', ''))
            parts.append(exp.get('location', ''))
            bullets = exp.get('bullets', [])
            if isinstance(bullets, list):
                parts.extend([str(b) for b in bullets if b])
            elif isinstance(bullets, str):
                parts.append(bullets)

    # Internships
    for intern in resume_data.get('internships', []):
        if isinstance(intern, dict):
            parts.append(intern.get('title', ''))
            parts.append(intern.get('company', ''))
            parts.append(intern.get('location', ''))
            bullets = intern.get('bullets', [])
            if isinstance(bullets, list):
                parts.extend([str(b) for b in bullets if b])
            elif isinstance(bullets, str):
                parts.append(bullets)

    # Education
    for edu in resume_data.get('education', []):
        if isinstance(edu, dict):
            parts.append(edu.get('degree', ''))
            parts.append(edu.get('school', ''))
            parts.append(edu.get('field', ''))
            parts.append(edu.get('courses', ''))
            parts.append(edu.get('gpa', ''))

    # Skills — handle both categorized dict and flat list
    skills = resume_data.get('skills', [])
    if isinstance(skills, dict):
        for cat_list in skills.values():
            if isinstance(cat_list, list):
                parts.extend([str(s) for s in cat_list if s])
            elif isinstance(cat_list, str):
                parts.append(cat_list)
    elif isinstance(skills, list):
        for s in skills:
            parts.append(str(s if isinstance(s, str) else s.get('name', '')))
    elif isinstance(skills, str):
        parts.append(skills)

    # Projects
    for proj in resume_data.get('projects', []):
        if isinstance(proj, dict):
            parts.append(proj.get('name', ''))
            parts.append(proj.get('description', ''))
            parts.append(proj.get('technologies', ''))

    # Certifications
    for cert in resume_data.get('certifications', []):
        if isinstance(cert, dict):
            parts.append(cert.get('name', ''))
            parts.append(cert.get('issuer', ''))
        else:
            parts.append(str(cert))

    # Achievements & Publications & Awards & Volunteer
    for ach in resume_data.get('achievements', []):
        parts.append(ach.get('title', str(ach)) if isinstance(ach, dict) else str(ach))
        if isinstance(ach, dict) and ach.get('description'):
            parts.append(ach['description'])

    for pub in resume_data.get('publications', []):
        parts.append(pub.get('title', str(pub)) if isinstance(pub, dict) else str(pub))

    for a in resume_data.get('awards', []):
        parts.append(a.get('title', str(a)) if isinstance(a, dict) else str(a))

    for vol in resume_data.get('volunteer_experience', []):
        if isinstance(vol, dict):
            parts.append(vol.get('title', ''))
            parts.append(vol.get('company', vol.get('organization', '')))

    return ' '.join(filter(None, parts))


def score_resume(resume_data, job_description_text):
    """
    Main scoring function.
    Supports both Fresher and Experienced candidate profiles automatically.
    """
    resume_text = build_resume_text(resume_data)
    is_fresher = detect_fresher_status(resume_data)

    keyword_result = score_keywords(resume_text, job_description_text)
    section_result = score_sections(resume_data, is_fresher)
    format_result = score_formatting(resume_data, resume_text, is_fresher)
    readability_result = score_readability(resume_text, resume_data, is_fresher)

    keyword_score = keyword_result['score']
    section_score = section_result['score']
    format_score = format_result['score']
    readability_score = readability_result['score']

    overall = int(
        keyword_score * 0.40 +
        section_score * 0.25 +
        format_score * 0.20 +
        readability_score * 0.15
    )

    recommendations = []
    recommendations.extend(keyword_result['recommendations'])
    recommendations.extend(section_result['recommendations'])
    recommendations.extend(format_result['recommendations'])
    recommendations.extend(readability_result['recommendations'])

    return {
        'overall_score': overall,
        'is_fresher': is_fresher,
        'keyword_score': keyword_score,
        'section_score': section_score,
        'format_score': format_score,
        'readability_score': readability_score,
        'matched_keywords': keyword_result['matched'],
        'missing_keywords': keyword_result['missing'],
        'section_analysis': section_result['analysis'],
        'formatting_issues': format_result['issues'],
        'recommendations': recommendations[:15],
        'resume_text': resume_text,
    }


def score_keywords(resume_text, jd_text):
    if not jd_text or not jd_text.strip():
        return {'score': 60, 'matched': [], 'missing': [], 'recommendations': [
            'Paste a job description to calculate keyword match score.'
        ]}

    resume_tokens = set(tokenize(resume_text))
    jd_tokens = tokenize(jd_text)

    stopwords = {
        'the', 'and', 'for', 'are', 'you', 'with', 'our', 'will', 'have',
        'this', 'from', 'that', 'they', 'etc', 'its', 'can', 'all', 'also',
        'looking', 'ideal', 'candidate', 'seeking', 'join', 'team', 'work',
        'strong', 'good', 'great', 'excellent', 'highly', 'must', 'should',
        'able', 'ability', 'include', 'including', 'such', 'related', 'field',
        'preferred', 'required', 'minimum', 'years', 'year', 'experience',
        'knowledge', 'understanding', 'skills', 'skill', 'role', 'position',
        'responsibilities', 'job', 'company', 'organization', 'team', 'member',
    }
    jd_word_freq = Counter(jd_tokens)
    important_words = [
        w for w, freq in jd_word_freq.most_common(60)
        if w not in stopwords and len(w) > 3
    ]

    matched = [w for w in important_words if w in resume_tokens]
    missing = [w for w in important_words if w not in resume_tokens]

    resume_phrases = set(extract_phrases(resume_text, 2))
    jd_bigrams = [p for p in extract_phrases(jd_text, 2) if len(p) > 5]
    bigram_freq = Counter(jd_bigrams)
    important_phrases = [p for p, f in bigram_freq.most_common(20) if f >= 1]
    matched_phrases = [p for p in important_phrases if p in resume_phrases]
    missing_phrases = [p for p in important_phrases[:10] if p not in resume_phrases]

    all_matched = list(dict.fromkeys(matched[:15] + matched_phrases[:5]))
    all_missing = list(dict.fromkeys(missing[:15] + missing_phrases[:5]))

    total_checked = len(important_words[:30])
    match_rate = len([w for w in important_words[:30] if w in resume_tokens]) / max(total_checked, 1)
    score = min(100, int(match_rate * 100))

    recommendations = []
    if all_missing[:5]:
        recommendations.append(f"Add missing job keywords: {', '.join(all_missing[:8])}.")
    if score < 50:
        recommendations.append('Low keyword match. Tailor your skills and experience to match terms in the job post.')
    elif score < 75:
        recommendations.append('Good keyword coverage. Include a few more tech terms from the job post for >85% score.')

    return {
        'score': score,
        'matched': all_matched,
        'missing': all_missing,
        'recommendations': recommendations,
    }


def score_sections(resume_data, is_fresher=False):
    analysis = {}
    score = 0
    recommendations = []

    raw_text = resume_data.get('resume_text', '').lower()
    is_raw = bool(raw_text and not resume_data.get('email') and not resume_data.get('experience'))

    def has_section(key):
        if not is_raw:
            if key == 'contact':
                return bool(resume_data.get('email') or resume_data.get('phone'))
            if key == 'summary':
                return bool((resume_data.get('professional_summary') or '').strip() or (resume_data.get('career_objective') or '').strip())
            if key == 'experience':
                return bool(resume_data.get('experience'))
            if key == 'internships':
                return bool(resume_data.get('internships'))
            if key == 'education':
                return bool(resume_data.get('education'))
            if key == 'skills':
                sk = resume_data.get('skills')
                if isinstance(sk, dict):
                    return any(bool(v) for v in sk.values())
                return bool(sk)
            if key == 'projects':
                return bool(resume_data.get('projects'))
            if key == 'certifications':
                return bool(resume_data.get('certifications'))
        kws = SECTION_KEYWORDS.get(key, [])
        return any(k in raw_text for k in kws)

    if is_fresher:
        # Fresher weighting: Education, Skills, Projects/Internships hold primary weight
        weights = {
            'contact': 20,
            'summary': 15,     # Objectives count
            'education': 25,   # High weight for freshers
            'skills': 20,      # High weight for freshers
            'practical': 20    # Combined Internships or Projects
        }
        has_contact = has_section('contact')
        has_sum = has_section('summary')
        has_edu = has_section('education')
        has_sk = has_section('skills')
        has_prac = has_section('internships') or has_section('projects') or has_section('experience')

        analysis['contact'] = {'present': has_contact, 'weight': 20}
        analysis['summary'] = {'present': has_sum, 'weight': 15}
        analysis['education'] = {'present': has_edu, 'weight': 25}
        analysis['skills'] = {'present': has_sk, 'weight': 20}
        analysis['practical_experience'] = {'present': has_prac, 'weight': 20}

        score = (20 if has_contact else 0) + (15 if has_sum else 0) + (25 if has_edu else 0) + (20 if has_sk else 0) + (20 if has_prac else 0)

        if not has_contact:
            recommendations.append('Add Contact details (email & phone).')
        if not has_sum:
            recommendations.append('Add a Career Objective or Professional Summary.')
        if not has_edu:
            recommendations.append('Add Education section — vital for freshers.')
        if not has_sk:
            recommendations.append('Add Skills section with technical & soft skills.')
        if not has_prac:
            recommendations.append('Add Academic/Personal Projects or Internships to demonstrate practical work.')

    else:
        # Experienced weighting: Experience holds highest weight
        weights = {
            'contact': 20, 'summary': 15, 'experience': 30,
            'education': 15, 'skills': 15, 'projects': 5
        }
        checks = {k: has_section(k) for k in weights.keys()}
        for section, present in checks.items():
            w = weights[section]
            analysis[section] = {'present': present, 'weight': w}
            if present:
                score += w
            else:
                if section in ('contact', 'experience', 'education', 'skills'):
                    recommendations.append(f'Add a {section.title()} section — required for experienced profiles.')
                else:
                    recommendations.append(f'Consider adding a {section.title()} section.')

    # Check bullet points across experience, internships, and projects
    if not is_raw:
        all_entries = resume_data.get('experience', []) + resume_data.get('internships', [])
        if all_entries:
            with_bullets = sum(1 for e in all_entries if isinstance(e, dict) and e.get('bullets'))
            if with_bullets == 0:
                recommendations.append('Add achievement-focused bullet points to your experience/internship entries.')

    return {'score': min(100, score), 'analysis': analysis, 'recommendations': recommendations}


def score_formatting(resume_data, resume_text, is_fresher=False):
    issues = []
    score = 100
    is_raw = bool(resume_data.get('resume_text') and not resume_data.get('email') and not resume_data.get('experience'))

    if not is_raw:
        if not resume_data.get('linkedin_url'):
            issues.append('Missing LinkedIn URL — adding one boosts recruiter response rate.')
            score -= 5
        if not resume_data.get('location'):
            issues.append('Missing location — add City, State or Country.')
            score -= 5

        exp = resume_data.get('experience', [])
        if exp and not is_fresher:
            for e in exp:
                if isinstance(e, dict) and not e.get('start_date'):
                    issues.append(f'Missing start date in experience: {e.get("title", "entry")}.')
                    score -= 3
                    break

        summary = (resume_data.get('professional_summary', '') or resume_data.get('career_objective', '')).strip()
        if summary and len(summary) < 40:
            issues.append('Summary/Objective is brief. Expand to 2–4 impactful sentences.')
            score -= 5
        elif summary and len(summary) > 600:
            issues.append('Summary/Objective is too long. Keep under 4 sentences.')
            score -= 5

    text_lower = resume_text.lower()
    weak_found = [p for p in WEAK_PHRASES if p in text_lower]
    if weak_found:
        issues.append(f'Replace weak phrase "{weak_found[0]}" with a strong action verb (e.g. Led, Built, Delivered).')
        score -= 8

    return {'score': max(0, score), 'issues': issues, 'recommendations': []}


def score_readability(resume_text, resume_data, is_fresher=False):
    recommendations = []
    score = 100

    words = resume_text.split()
    word_count = len(words)

    min_words = 180 if is_fresher else 300
    max_words = 700 if is_fresher else 1200

    if word_count < min_words:
        recommendations.append(f'Resume content is concise ({word_count} words). Aim for {min_words}+ words.')
        score -= 15
    elif word_count > max_words:
        recommendations.append(f'Resume is lengthy ({word_count} words). Keep to 1 page for freshers or 2 pages max.')
        score -= 10

    # Collect bullets from experience, internships, and projects
    all_bullets = []
    for entry in (resume_data.get('experience', []) + resume_data.get('internships', [])):
        if isinstance(entry, dict):
            bullets = entry.get('bullets', [])
            if isinstance(bullets, list):
                all_bullets.extend(bullets)
            elif isinstance(bullets, str):
                all_bullets.extend(bullets.split('\n'))

    for proj in resume_data.get('projects', []):
        if isinstance(proj, dict) and proj.get('description'):
            all_bullets.append(proj['description'])

    if all_bullets:
        verbs_used = sum(1 for b in all_bullets if isinstance(b, str) and any(b.strip().lower().startswith(v) for v in POWER_VERBS))
        verb_ratio = verbs_used / max(len(all_bullets), 1)
        if verb_ratio < 0.35:
            recommendations.append('Start bullet points with strong action verbs (e.g. Spearheaded, Built, Optimized).')
            score -= 10

    filler_count = sum(resume_text.lower().count(f) for f in FILLER_WORDS)
    if filler_count > 5:
        recommendations.append('Remove filler words (very, really, basically) for concise language.')
        score -= 5

    return {'score': max(0, score), 'recommendations': recommendations}
