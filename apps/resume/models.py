from django.db import models
from django.conf import settings
import uuid


class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    best_for = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    is_ats_friendly = models.BooleanField(default=True)
    preview_image = models.URLField(blank=True)
    sort_order = models.IntegerField(default=0)
    styles = models.JSONField(default=dict, blank=True)
    pdf_config = models.JSONField(default=dict, blank=True)
    section_order_experienced = models.JSONField(default=list, blank=True)
    section_order_fresher = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Resume(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('complete', 'Complete'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    template_style = models.CharField(max_length=50, default='classic')
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Personal Info
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    professional_summary = models.TextField(blank=True)
    career_objective = models.TextField(blank=True)

    # Structured data stored as JSON
    experience = models.JSONField(default=list)
    internships = models.JSONField(default=list)
    education = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    publications = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    awards = models.JSONField(default=list)
    achievements = models.JSONField(default=list)
    volunteer_experience = models.JSONField(default=list)

    # Template customization (font, color, spacing overrides)
    resume_customization = models.JSONField(default=dict)

    # Drive
    drive_file_id = models.CharField(max_length=200, blank=True)
    drive_file_url = models.URLField(blank=True)
    last_drive_sync = models.DateTimeField(null=True, blank=True)

    # ATS Score cache
    last_ats_score = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.title} - {self.user.email}'
