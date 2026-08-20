import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from .models import ChatSession, ChatMessage, AIUsageLog
from .openrouter import chat, improve_bullet_points, generate_summary, tailor_resume_suggestions
from apps.resume.models import Resume

logger = logging.getLogger('apps')


def check_rate_limit(user):
    from apps.accounts.models import AppSettings
    import datetime
    max_requests = int(AppSettings.get('AI_MAX_REQUESTS_PER_DAY') or settings.AI_MAX_REQUESTS_PER_DAY)
    today = timezone.now().date()
    if user.ai_requests_reset_date != today:
        user.ai_requests_today = 0
        user.ai_requests_reset_date = today
        user.save(update_fields=['ai_requests_today', 'ai_requests_reset_date'])
    return user.ai_requests_today < max_requests


def increment_usage(user, tokens=0, model='', action='chat'):
    user.ai_requests_today += 1
    user.save(update_fields=['ai_requests_today'])
    AIUsageLog.objects.create(user=user, action=action, tokens_used=tokens, model_used=model)


@login_required
def ai_page(request):
    sessions = ChatSession.objects.filter(user=request.user)
    resumes = Resume.objects.filter(user=request.user)
    active_session = sessions.first()
    messages_list = []
    if active_session:
        messages_list = list(active_session.messages.values('role', 'content', 'created_at'))
    return render(request, 'ai_assistant/chat.html', {
        'sessions': sessions,
        'active_session': active_session,
        'messages': messages_list,
        'resumes': resumes,
    })


@login_required
@require_POST
def send_message(request):
    if not check_rate_limit(request.user):
        return JsonResponse({'success': False, 'error': 'Daily AI request limit reached. Try again tomorrow.'}, status=429)
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')
        resume_id = data.get('resume_id')

        if not user_message:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty.'}, status=400)

        resume_context = None
        if resume_id:
            try:
                resume = Resume.objects.get(pk=resume_id, user=request.user)
                resume_context = {
                    'title': resume.title,
                    'full_name': resume.full_name,
                    'summary': resume.professional_summary,
                    'skills': resume.skills,
                    'experience': resume.experience,
                    'education': resume.education,
                }
            except Resume.DoesNotExist:
                pass

        if session_id:
            session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(
                user=request.user,
                title=user_message[:50],
            )

        history = list(session.messages.values('role', 'content'))

        ChatMessage.objects.create(session=session, role='user', content=user_message)

        response_text, tokens, model = chat(history, user_message, resume_context=resume_context)

        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=response_text,
            tokens_used=tokens,
            model_used=model,
        )

        increment_usage(request.user, tokens=tokens, model=model, action='chat')

        return JsonResponse({
            'success': True,
            'response': response_text,
            'session_id': str(session.id),
            'session_title': session.title,
        })
    except Exception as e:
        logger.error(f'AI chat error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def improve_bullets(request):
    if not check_rate_limit(request.user):
        return JsonResponse({'success': False, 'error': 'Daily AI limit reached.'}, status=429)
    try:
        data = json.loads(request.body)
        bullets = data.get('bullets', [])
        job_title = data.get('job_title', '')
        industry = data.get('industry', '')
        result, tokens, model = improve_bullet_points(bullets, job_title, industry)
        increment_usage(request.user, tokens=tokens, model=model, action='improve_bullets')
        return JsonResponse({'success': True, 'result': result})
    except Exception as e:
        logger.error(f'Improve bullets error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def generate_resume_summary(request):
    if not check_rate_limit(request.user):
        return JsonResponse({'success': False, 'error': 'Daily AI limit reached.'}, status=429)
    try:
        data = json.loads(request.body)
        resume_id = data.get('resume_id')
        job_title = data.get('job_title', '')
        jd_text = data.get('jd_text', '')
        resume = get_object_or_404(Resume, pk=resume_id, user=request.user)
        resume_data = {
            'full_name': resume.full_name,
            'skills': resume.skills,
            'experience': resume.experience,
        }
        result, tokens, model = generate_summary(resume_data, job_title, jd_text)
        increment_usage(request.user, tokens=tokens, model=model, action='generate_summary')
        return JsonResponse({'success': True, 'summary': result})
    except Exception as e:
        logger.error(f'Generate summary error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def tailor_resume(request):
    if not check_rate_limit(request.user):
        return JsonResponse({'success': False, 'error': 'Daily AI limit reached.'}, status=429)
    try:
        data = json.loads(request.body)
        resume_id = data.get('resume_id')
        jd_text = data.get('jd_text', '')
        resume = get_object_or_404(Resume, pk=resume_id, user=request.user)
        resume_data = {
            'professional_summary': resume.professional_summary,
            'skills': resume.skills,
            'experience': resume.experience,
        }
        result, tokens, model = tailor_resume_suggestions(resume_data, jd_text)
        increment_usage(request.user, tokens=tokens, model=model, action='tailor_resume')
        return JsonResponse({'success': True, 'suggestions': result})
    except Exception as e:
        logger.error(f'Tailor resume error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def session_history(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    messages = list(session.messages.values('role', 'content', 'created_at'))
    return JsonResponse({'success': True, 'messages': messages, 'title': session.title})


@login_required
@require_POST
def delete_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    session.delete()
    return JsonResponse({'success': True})
