import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import DriveFile
from .service import DriveService

logger = logging.getLogger('apps')


@login_required
def drive_files(request):
    has_google_account = False
    has_token = False
    live_files = []
    drive_error = None

    try:
        from allauth.socialaccount.models import SocialToken, SocialAccount
        has_google_account = SocialAccount.objects.filter(
            user=request.user, provider='google'
        ).exists()
        has_token = SocialToken.objects.filter(
            account__user=request.user,
            account__provider='google',
        ).exists()
    except Exception:
        pass

    if has_token:
        try:
            service = DriveService(request.user)
            live_files = service.list_files()
        except Exception as e:
            logger.error(f'Drive list error on page load: {e}')
            drive_error = str(e)

    return render(request, 'drive/files.html', {
        'files': live_files,
        'has_google_account': has_google_account,
        'has_token': has_token,
        'drive_connected': has_token,
        'drive_error': drive_error,
    })


@login_required
def list_drive_files(request):
    try:
        service = DriveService(request.user)
        files = service.list_files()
        return JsonResponse({'success': True, 'files': files})
    except Exception as e:
        logger.error(f'Drive list error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def delete_drive_file(request, file_id):
    try:
        service = DriveService(request.user)
        service.delete_file(file_id)
        DriveFile.objects.filter(user=request.user, drive_file_id=file_id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f'Drive delete error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
