import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.utils import timezone
from .models import Resume, ResumeTemplate
from apps.drive.service import DriveService

logger = logging.getLogger('apps')


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')[:6]
    total_resumes = Resume.objects.filter(user=request.user).count()
    from apps.ats.models import ATSResult
    latest_ats = ATSResult.objects.filter(user=request.user).first()
    from apps.ai_assistant.models import ChatSession
    recent_sessions = ChatSession.objects.filter(user=request.user)[:3]
    return render(request, 'dashboard/dashboard.html', {
        'resumes': resumes,
        'total_resumes': total_resumes,
        'latest_ats': latest_ats,
        'recent_sessions': recent_sessions,
    })


@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume/list.html', {'resumes': resumes})


@login_required
def resume_create(request):
    templates = ResumeTemplate.objects.filter(is_active=True)
    if request.method == 'POST':
        title = request.POST.get('title', 'My Resume')
        template_id = request.POST.get('template_id')
        template_style = request.POST.get('template_style', 'classic')
        resume = Resume.objects.create(
            user=request.user,
            title=title,
            template_id=template_id if template_id else None,
            template_style=template_style,
            full_name=request.user.full_name,
            email=request.user.email,
        )
        return redirect('resume_edit', pk=resume.pk)
    return render(request, 'resume/create.html', {'templates': templates})


@login_required
def resume_edit(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    templates = ResumeTemplate.objects.filter(is_active=True)

    from .template_engine import TEMPLATES as TPL_DEFS, get_template_config, detect_fresher
    tpl_config = get_template_config(resume.template_style, resume.resume_customization)
    is_fresher = detect_fresher(resume)

    resume_json = json.dumps({
        'id': str(resume.id),
        'title': resume.title,
        'template_style': resume.template_style,
        'resume_customization': resume.resume_customization or {},
        'section_order': resume.resume_customization.get('section_order', []) if resume.resume_customization else [],
        'hidden_sections': resume.resume_customization.get('hidden_sections', []) if resume.resume_customization else [],
        # Personal
        'full_name': resume.full_name,
        'email': resume.email,
        'phone': resume.phone,
        'location': resume.location,
        'linkedin_url': resume.linkedin_url,
        'github_url': resume.github_url,
        'portfolio_url': resume.portfolio_url,
        'website_url': resume.website_url,
        # Content
        'professional_summary': resume.professional_summary,
        'career_objective': resume.career_objective,
        'experience': resume.experience,
        'internships': resume.internships,
        'education': resume.education,
        'skills': resume.skills,
        'certifications': resume.certifications,
        'projects': resume.projects,
        'publications': resume.publications,
        'languages': resume.languages,
        'awards': resume.awards,
        'achievements': resume.achievements,
        'volunteer_experience': resume.volunteer_experience,
    })

    # Serialize template definitions for client-side preview engine
    tpl_defs_json = json.dumps({k: {
        'name': v['name'],
        'styles': v['styles'],
        'section_order_experienced': v['section_order_experienced'],
        'section_order_fresher': v['section_order_fresher'],
    } for k, v in TPL_DEFS.items()})

    return render(request, 'resume/builder.html', {
        'resume': resume,
        'resume_json': resume_json,
        'tpl_defs_json': tpl_defs_json,
        'templates': templates,
        'is_fresher': is_fresher,
        'tpl_config': tpl_config,
    })


@login_required
@require_POST
def resume_save(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)

        scalar_fields = [
            'title', 'full_name', 'email', 'phone', 'location',
            'linkedin_url', 'github_url', 'portfolio_url', 'website_url',
            'professional_summary', 'career_objective',
            'template_style', 'status',
        ]
        json_fields = [
            'experience', 'internships', 'education', 'skills',
            'certifications', 'projects', 'publications',
            'languages', 'awards', 'achievements', 'volunteer_experience',
        ]

        for field in scalar_fields:
            if field in data:
                setattr(resume, field, data[field])

        for field in json_fields:
            if field in data:
                setattr(resume, field, data[field])

        # Merge section_order and hidden_sections into resume_customization
        customization = resume.resume_customization or {}
        if 'resume_customization' in data:
            customization.update(data['resume_customization'])
        if 'section_order' in data:
            customization['section_order'] = data['section_order']
        if 'hidden_sections' in data:
            customization['hidden_sections'] = data['hidden_sections']
        resume.resume_customization = customization

        resume.save()
        return JsonResponse({'success': True, 'updated_at': resume.updated_at.isoformat()})
    except Exception as e:
        logger.error(f'Resume save error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def resume_duplicate(request, pk):
    original = get_object_or_404(Resume, pk=pk, user=request.user)
    original.pk = None
    original.id = None
    original.title = f'{original.title} (Copy)'
    original.drive_file_id = ''
    original.drive_file_url = ''
    original.save()
    return redirect('resume_edit', pk=original.pk)


@login_required
@require_POST
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.delete()
    return JsonResponse({'success': True})


@login_required
def resume_preview(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    from .template_engine import get_template_config, get_section_order, detect_fresher
    is_fresher = detect_fresher(resume)
    customization = resume.resume_customization or {}
    tpl_config = get_template_config(resume.template_style, customization)
    section_order = customization.get('section_order') or get_section_order(resume.template_style, is_fresher)
    hidden_sections = customization.get('hidden_sections', [])

    formatted_projects = []
    for proj in (resume.projects or []):
        if isinstance(proj, dict):
            p_copy = proj.copy()
            pdesc = proj.get('description', '')
            pbullets = proj.get('bullets', [])
            if isinstance(pbullets, list) and len(pbullets) > 0:
                p_copy['bullets'] = [str(b).strip().lstrip('•-* ').strip() for b in pbullets if b]
            elif pdesc:
                if isinstance(pdesc, list):
                    p_copy['bullets'] = [str(b).strip().lstrip('•-* ').strip() for b in pdesc if b]
                else:
                    p_copy['bullets'] = [l.strip().lstrip('•-* ').strip() for l in str(pdesc).split('\n') if l.strip()]
            formatted_projects.append(p_copy)

    return render(request, 'resume/preview.html', {
        'resume': resume,
        'formatted_projects': formatted_projects,
        'tpl_config': tpl_config,
        'section_order': section_order,
        'hidden_sections': hidden_sections,
        'is_fresher': is_fresher,
    })


@login_required
def resume_download_pdf(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    try:
        from .pdf_generator import generate_pdf
        pdf_bytes = generate_pdf(resume)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        safe_title = resume.title.replace(' ', '_')[:50]
        response['Content-Disposition'] = f'attachment; filename="{safe_title}.pdf"'
        return response
    except Exception as e:
        logger.error(f'PDF generation error: {e}')
        messages.error(request, 'Failed to generate PDF. Please try again.')
        return redirect('resume_edit', pk=pk)


@login_required
@require_POST
def resume_upload_drive(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    try:
        from .pdf_generator import generate_pdf
        pdf_bytes = generate_pdf(resume)
        service = DriveService(request.user)
        file_info = service.upload_resume(pdf_bytes, f'{resume.title}.pdf', resume)
        resume.drive_file_id = file_info['id']
        resume.drive_file_url = file_info.get('webViewLink', '')
        resume.last_drive_sync = timezone.now()
        resume.save()
        return JsonResponse({'success': True, 'url': resume.drive_file_url})
    except Exception as e:
        logger.error(f'Drive upload error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def resume_ats_validate(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    from .template_engine import validate_ats
    resume_data = {
        'full_name': resume.full_name,
        'email': resume.email,
        'phone': resume.phone,
        'linkedin_url': resume.linkedin_url,
        'professional_summary': resume.professional_summary,
        'career_objective': resume.career_objective,
        'experience': resume.experience,
        'internships': resume.internships,
        'education': resume.education,
        'skills': resume.skills,
        'projects': resume.projects,
        'certifications': resume.certifications,
    }
    warnings = validate_ats(resume_data)
    return JsonResponse({'success': True, 'warnings': warnings})
