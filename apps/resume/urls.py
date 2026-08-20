from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/create/', views.resume_create, name='resume_create'),
    path('resumes/<uuid:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('resumes/<uuid:pk>/save/', views.resume_save, name='resume_save'),
    path('resumes/<uuid:pk>/duplicate/', views.resume_duplicate, name='resume_duplicate'),
    path('resumes/<uuid:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('resumes/<uuid:pk>/preview/', views.resume_preview, name='resume_preview'),
    path('resumes/<uuid:pk>/download/', views.resume_download_pdf, name='resume_download'),
    path('resumes/<uuid:pk>/drive-upload/', views.resume_upload_drive, name='resume_upload_drive'),
    path('resumes/<uuid:pk>/ats-validate/', views.resume_ats_validate, name='resume_ats_validate'),
]
