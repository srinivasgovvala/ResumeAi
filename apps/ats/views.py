import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ATSResult, JobDescription, ATSConfig
from .engine import score_resume
from apps.resume.models import Resume

logger = logging.getLogger('apps')


def _extract_text_from_upload(f):
    """Extract plain text from an uploaded PDF or text file."""
    name = f.name.lower()
    content = f.read()
    if name.endswith('.pdf'):
        try:
            import io
            from reportlab.lib.pagesizes import letter  # noqa — just verify reportlab present
        except ImportError:
            pass
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                return '\n'.join(page.extract_text() or '' for page in pdf.pages)
        except ImportError:
            pass
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content))
            return '\n'.join(page.extract_text() or '' for page in reader.pages)
        except ImportError:
            pass
        try:
            import PyPDF2
            import io as _io
            reader = PyPDF2.PdfReader(_io.BytesIO(content))
            return '\n'.join(page.extract_text() or '' for page in reader.pages)
        except ImportError:
            raise ValueError('No PDF library available. Install pdfplumber: pip install pdfplumber')
    elif name.endswith('.txt'):
        return content.decode('utf-8', errors='ignore')
    else:
        raise ValueError('Only PDF and TXT files are supported for upload.')



@login_required
def ats_checker(request):
    resumes = Resume.objects.filter(user=request.user)
    job_descriptions = JobDescription.objects.filter(user=request.user)
    recent_results = ATSResult.objects.filter(user=request.user).select_related('resume', 'job_description')[:10]
    return render(request, 'ats/checker.html', {
        'resumes': resumes,
        'job_descriptions': job_descriptions,
        'recent_results': recent_results,
    })


@login_required
@require_POST
def run_ats_check(request):
    try:
        data = json.loads(request.body)
        resume_id = data.get('resume_id')
        jd_id = data.get('jd_id')
        jd_text = data.get('jd_text', '')

        resume = None
        resume_data = data.get('resume_data', {})

        if resume_id:
            resume = get_object_or_404(Resume, pk=resume_id, user=request.user)
            resume_data = {
                'full_name': resume.full_name,
                'email': resume.email,
                'phone': resume.phone,
                'location': resume.location,
                'linkedin_url': resume.linkedin_url,
                'professional_summary': resume.professional_summary,
                'experience': resume.experience,
                'education': resume.education,
                'skills': resume.skills,
                'certifications': resume.certifications,
                'projects': resume.projects,
            }

        jd = None
        if jd_id:
            jd = get_object_or_404(JobDescription, pk=jd_id, user=request.user)
            jd_text = jd.content

        result = score_resume(resume_data, jd_text)

        ats_result = ATSResult.objects.create(
            user=request.user,
            resume=resume,
            job_description=jd,
            overall_score=result['overall_score'],
            keyword_score=result['keyword_score'],
            format_score=result['format_score'],
            section_score=result['section_score'],
            readability_score=result['readability_score'],
            matched_keywords=result['matched_keywords'],
            missing_keywords=result['missing_keywords'],
            section_analysis=result['section_analysis'],
            formatting_issues=result['formatting_issues'],
            recommendations=result['recommendations'],
            resume_text=result['resume_text'],
        )

        if resume:
            resume.last_ats_score = result['overall_score']
            resume.save(update_fields=['last_ats_score'])

        return JsonResponse({'success': True, 'result_id': str(ats_result.id), 'result': result})
    except Exception as e:
        logger.error(f'ATS check error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def ats_result(request, pk):
    result = get_object_or_404(ATSResult, pk=pk, user=request.user)
    return render(request, 'ats/result.html', {'result': result})


@login_required
@require_POST
def save_job_description(request):
    try:
        data = json.loads(request.body)
        jd = JobDescription.objects.create(
            user=request.user,
            title=data.get('title', 'Job Description'),
            company=data.get('company', ''),
            content=data.get('content', ''),
        )
        return JsonResponse({'success': True, 'id': str(jd.id), 'title': jd.title})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def job_descriptions(request):
    jds = JobDescription.objects.filter(user=request.user)
    return render(request, 'ats/job_descriptions.html', {'job_descriptions': jds})


@login_required
@require_POST
def delete_job_description(request, pk):
    jd = get_object_or_404(JobDescription, pk=pk, user=request.user)
    jd.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def run_ats_check_upload(request):
    try:
        resume_file = request.FILES.get('resume_file')
        jd_text = request.POST.get('jd_text', '').strip()
        if not resume_file:
            return JsonResponse({'success': False, 'error': 'No file uploaded.'}, status=400)

        resume_text = _extract_text_from_upload(resume_file)
        if not resume_text.strip():
            return JsonResponse({'success': False, 'error': 'Could not extract text from the file.'}, status=400)

        resume_data = {'resume_text': resume_text}
        result = score_resume(resume_data, jd_text)

        ats_result = ATSResult.objects.create(
            user=request.user,
            overall_score=result['overall_score'],
            keyword_score=result['keyword_score'],
            format_score=result['format_score'],
            section_score=result['section_score'],
            readability_score=result['readability_score'],
            matched_keywords=result['matched_keywords'],
            missing_keywords=result['missing_keywords'],
            section_analysis=result['section_analysis'],
            formatting_issues=result['formatting_issues'],
            recommendations=result['recommendations'],
            resume_text=result['resume_text'],
        )

        return JsonResponse({'success': True, 'result_id': str(ats_result.id), 'result': result})
    except Exception as e:
        logger.error(f'ATS upload check error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
