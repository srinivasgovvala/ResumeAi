from django.urls import path
from . import views

urlpatterns = [
    path('', views.drive_files, name='drive_files'),
    path('list/', views.list_drive_files, name='list_drive_files'),
    path('delete/<str:file_id>/', views.delete_drive_file, name='delete_drive_file'),
]
