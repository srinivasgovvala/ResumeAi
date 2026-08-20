from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_page, name='ai_assistant'),
    path('chat/', views.send_message, name='ai_send_message'),
    path('improve-bullets/', views.improve_bullets, name='ai_improve_bullets'),
    path('generate-summary/', views.generate_resume_summary, name='ai_generate_summary'),
    path('tailor-resume/', views.tailor_resume, name='ai_tailor_resume'),
    path('session/<uuid:pk>/', views.session_history, name='ai_session_history'),
    path('session/<uuid:pk>/delete/', views.delete_session, name='ai_delete_session'),
]
