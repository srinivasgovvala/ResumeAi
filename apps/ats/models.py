from django.db import models
from django.conf import settings
import uuid


class JobDescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_descriptions')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} at {self.company}'


class ATSResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ats_results')
    resume = models.ForeignKey('resume.Resume', on_delete=models.CASCADE, related_name='ats_results', null=True, blank=True)
    job_description = models.ForeignKey(JobDescription, on_delete=models.SET_NULL, null=True, blank=True)

    overall_score = models.IntegerField(default=0)
    keyword_score = models.IntegerField(default=0)
    format_score = models.IntegerField(default=0)
    section_score = models.IntegerField(default=0)
    readability_score = models.IntegerField(default=0)

    matched_keywords = models.JSONField(default=list)
    missing_keywords = models.JSONField(default=list)
    section_analysis = models.JSONField(default=dict)
    formatting_issues = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)

    resume_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'ATS Result {self.overall_score}% - {self.user.email}'


class ATSConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ATS Configuration'

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, name, default=None):
        try:
            return cls.objects.get(name=name).value
        except cls.DoesNotExist:
            return default
