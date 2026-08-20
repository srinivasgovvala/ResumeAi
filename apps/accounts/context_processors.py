from django.conf import settings


def google_oauth_configured(request):
    """Expose whether Google OAuth is properly configured to all templates."""
    configured = bool(
        getattr(settings, 'GOOGLE_CLIENT_ID', '') and
        getattr(settings, 'GOOGLE_CLIENT_SECRET', '')
    )
    return {'google_oauth_configured': configured}
