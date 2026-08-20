from django.urls import path
from . import views

urlpatterns = [
    path('', views.ats_checker, name='ats_checker'),
    path('check/', views.run_ats_check, name='run_ats_check'),
    path('check-upload/', views.run_ats_check_upload, name='run_ats_check_upload'),
    path('result/<uuid:pk>/', views.ats_result, name='ats_result'),
    path('job-descriptions/', views.job_descriptions, name='job_descriptions'),
    path('job-descriptions/save/', views.save_job_description, name='save_job_description'),
    path('job-descriptions/<uuid:pk>/delete/', views.delete_job_description, name='delete_job_description'),
]
