import json
import logging
import requests
from django.conf import settings
from apps.accounts.models import AppSettings

logger = logging.getLogger('apps')


def get_provider():
    # Admin configurable: openrouter | openai | anthropic | google | custom
    return (AppSettings.get('AI_PROVIDER') or 'openrouter').lower().strip()


def get_api_key():
    # Priority: AppSettings AI_API_KEY -> AppSettings OPENROUTER_API_KEY -> settings.OPENROUTER_API_KEY -> settings.OPENAI_API_KEY -> settings.ANTHROPIC_API_KEY
    key = AppSettings.get('AI_API_KEY') or AppSettings.get('OPENROUTER_API_KEY')
    if not key:
        key = getattr(settings, 'OPENROUTER_API_KEY', '') or getattr(settings, 'OPENAI_API_KEY', '') or getattr(settings, 'ANTHROPIC_API_KEY', '')
    return key


def get_model():
    model = AppSettings.get('AI_MODEL') or AppSettings.get('OPENROUTER_MODEL')
    if not model:
        model = getattr(settings, 'OPENROUTER_DEFAULT_MODEL', 'openai/gpt-4o-mini')
    return model


def get_base_url():
    url = AppSettings.get('AI_BASE_URL') or AppSettings.get('OPENROUTER_BASE_URL')
    if not url:
        provider = get_provider()
        if provider == 'openai':
            url = 'https://api.openai.com/v1'
        elif provider == 'anthropic':
            url = 'https://api.anthropic.com/v1'
        else:
            url = getattr(settings, 'OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    return url.rstrip('/')


def get_ai_enabled():
    val = AppSettings.get('AI_ENABLED', 'true')
    return str(val).lower() in ('true', '1', 'yes')


SYSTEM_PROMPT = """You are CareerAI, an expert career coach and resume specialist integrated into ATS Resume Builder.

Your capabilities:
- Analyze resumes and provide detailed, actionable feedback
- Improve bullet points to be more impactful and quantifiable
- Generate professional summaries tailored to specific roles
- Tailor resumes to specific job descriptions
- Suggest relevant skills and keywords for specific industries/roles
- Answer career-related questions with expert guidance
- Help with cover letters, interview prep, and salary negotiation advice

Guidelines:
- Be specific, actionable, and concise
- Use industry-specific language appropriate to the user's field
- When improving bullet points, always use strong action verbs and quantify results when possible
- Focus on ATS compatibility and recruiter preferences
- Format responses clearly with bullet points or numbered lists when listing multiple items
- Be encouraging but honest about areas needing improvement
"""


def chat(messages_history, user_message, resume_context=None, system_extra=None):
    """
    Send a chat message using the configured AI Provider and API key.
    Supports OpenRouter, OpenAI, Anthropic, Google Gemini, and custom OpenAI-compatible endpoints.
    """
    if not get_ai_enabled():
        raise ValueError('AI features are currently disabled. Please contact the administrator.')

    api_key = get_api_key()
    if not api_key:
        raise ValueError('AI API key not configured. Please contact the administrator.')

    provider = get_provider()
    model = get_model()
    base_url = get_base_url()

    system = SYSTEM_PROMPT
    if resume_context:
        system += f'\n\nCurrent resume context:\n{json.dumps(resume_context, indent=2)}'
    if system_extra:
        system += f'\n\n{system_extra}'

    # ── Anthropic Claude API ──
    if provider == 'anthropic':
        messages = []
        for msg in messages_history[-10:]:
            messages.append({'role': msg['role'], 'content': msg['content']})
        messages.append({'role': 'user', 'content': user_message})

        endpoint = f'{base_url}/messages' if not base_url.endswith('/messages') else base_url
        headers = {
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': model or 'claude-3-5-sonnet-20241022',
            'system': system,
            'messages': messages,
            'max_tokens': 1500,
        }
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            logger.error(f'Anthropic API error {response.status_code}: {response.text}')
            raise RuntimeError(f'AI service error ({provider}): {response.status_code}. Please try again.')
        data = response.json()
        content = data['content'][0]['text']
        usage = data.get('usage', {})
        tokens = usage.get('input_tokens', 0) + usage.get('output_tokens', 0)
        return content, tokens, model

    # ── Google Gemini API ──
    elif provider in ('google', 'gemini'):
        gemini_model = model or 'gemini-1.5-flash'
        endpoint = f'https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}'
        contents = [{'role': 'user', 'parts': [{'text': f'{system}\n\nUser Question: {user_message}'}]}]
        response = requests.post(endpoint, headers={'Content-Type': 'application/json'}, json={'contents': contents}, timeout=30)
        if response.status_code != 200:
            logger.error(f'Gemini API error {response.status_code}: {response.text}')
            raise RuntimeError(f'AI service error ({provider}): {response.status_code}. Please try again.')
        data = response.json()
        content = data['candidates'][0]['content']['parts'][0]['text']
        tokens = data.get('usageMetadata', {}).get('totalTokenCount', 0)
        return content, tokens, gemini_model

    # ── OpenRouter / OpenAI / Custom OpenAI-compatible API ──
    else:
        messages = [{'role': 'system', 'content': system}]
        for msg in messages_history[-10:]:
            messages.append({'role': msg['role'], 'content': msg['content']})
        messages.append({'role': 'user', 'content': user_message})

        endpoint = f'{base_url}/chat/completions' if not base_url.endswith('/chat/completions') else base_url
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        if provider == 'openrouter':
            headers['HTTP-Referer'] = 'https://atsbuilder.vercel.app'
            headers['X-Title'] = 'ATS Resume Builder'

        response = requests.post(
            endpoint,
            headers=headers,
            json={
                'model': model,
                'messages': messages,
                'max_tokens': 1500,
                'temperature': 0.7,
            },
            timeout=30,
        )

        if response.status_code != 200:
            logger.error(f'AI API error {response.status_code}: {response.text}')
            raise RuntimeError(f'AI service error ({provider}): {response.status_code}. Please try again.')

        data = response.json()
        content = data['choices'][0]['message']['content']
        tokens = data.get('usage', {}).get('total_tokens', 0)
        return content, tokens, model


def improve_bullet_points(bullets, job_title, industry=''):
    prompt = f"""Improve these resume bullet points for a {job_title} role{' in ' + industry if industry else ''}.

Original bullet points:
{chr(10).join(f'- {b}' for b in bullets)}

Rules:
1. Start each bullet with a strong action verb
2. Quantify achievements where possible (add placeholder numbers if needed, e.g., [X]%)
3. Keep each bullet to 1-2 lines
4. Focus on impact and results
5. Use industry-relevant keywords

Return ONLY the improved bullet points, one per line, starting with •"""

    content, tokens, model = chat([], prompt)
    return content, tokens, model


def generate_summary(resume_data, job_title='', job_description=''):
    resume_info = f"""
Name: {resume_data.get('full_name', '')}
Current/Target Role: {job_title}
Skills: {', '.join(resume_data.get('skills', [])[:15]) if isinstance(resume_data.get('skills', []), list) else resume_data.get('skills', '')}
Experience entries: {len(resume_data.get('experience', []))}
Latest role: {resume_data.get('experience', [{}])[0].get('title', '') if resume_data.get('experience') else ''}
"""

    prompt = f"""Write a powerful 3-4 sentence professional summary for this candidate:

{resume_info}

{"Job description context:\n" + job_description[:500] if job_description else ""}

Requirements:
- Start with years of experience or seniority level
- Highlight 2-3 core competencies
- Mention specific technical skills or tools if relevant
- End with value proposition or career goal
- ATS-optimized: no pronouns, keyword-rich
- 60-80 words total

Return ONLY the summary paragraph, no labels or quotes."""

    content, tokens, model = chat([], prompt)
    return content.strip(), tokens, model


def tailor_resume_suggestions(resume_data, job_description):
    prompt = f"""Analyze this resume against the job description and provide specific tailoring suggestions.

Resume Summary: {resume_data.get('professional_summary', '')[:300]}
Skills: {resume_data.get('skills', [])}
Experience Titles: {[e.get('title', '') for e in resume_data.get('experience', [])]}

Job Description (first 800 chars): {job_description[:800]}

Provide:
1. Top 5 keywords/phrases to add to resume
2. Skills to highlight or add
3. Specific bullet points to rewrite (give examples)
4. Summary improvements
5. Overall tailoring strategy

Format with clear headers and bullet points."""

    content, tokens, model = chat([], prompt)
    return content, tokens, model
