from django.contrib import admin
from .models import ATSResult, JobDescription, ATSConfig


@admin.register(ATSConfig)
class ATSConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated_at']
    search_fields = ['name']


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'user', 'created_at']
    search_fields = ['title', 'company', 'user__email']
    raw_id_fields = ['user']


@admin.register(ATSResult)
class ATSResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'overall_score', 'keyword_score', 'format_score', 'created_at']
    list_filter = ['overall_score']
    search_fields = ['user__email']
    raw_id_fields = ['user', 'resume']
    readonly_fields = ['created_at']
