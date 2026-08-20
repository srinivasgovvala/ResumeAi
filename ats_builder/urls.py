from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Custom auth views (signup/login/logout/profile/settings)
    path('accounts/', include('apps.accounts.urls')),
    # Allauth (Google OAuth callbacks, social account management)
    path('accounts/', include('allauth.urls')),
    # App sections
    path('dashboard/', include('apps.resume.urls')),
    path('ats/', include('apps.ats.urls')),
    path('ai/', include('apps.ai_assistant.urls')),
    path('drive/', include('apps.drive.urls')),
    # Landing page
    path('', include('apps.accounts.landing_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
