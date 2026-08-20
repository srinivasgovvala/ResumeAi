from django.contrib import admin
from .models import DriveFile


@admin.register(DriveFile)
class DriveFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'user', 'drive_file_id', 'file_size', 'created_at']
    search_fields = ['user__email', 'file_name']
    raw_id_fields = ['user', 'resume']
    readonly_fields = ['created_at', 'updated_at']
