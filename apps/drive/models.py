from django.db import models
from django.conf import settings
import uuid


class DriveFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='drive_files')
    resume = models.ForeignKey('resume.Resume', on_delete=models.SET_NULL, null=True, blank=True, related_name='drive_files')
    file_name = models.CharField(max_length=300)
    drive_file_id = models.CharField(max_length=200)
    drive_view_url = models.URLField(blank=True)
    drive_download_url = models.URLField(blank=True)
    mime_type = models.CharField(max_length=100, default='application/pdf')
    file_size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.file_name} - {self.user.email}'
