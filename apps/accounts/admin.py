from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, AppSettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'is_google_user', 'ai_requests_today', 'is_active', 'created_at']
    list_filter = ['is_google_user', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('ATS Builder', {'fields': ('is_google_user', 'avatar_url', 'google_drive_folder_id', 'ai_requests_today', 'ai_requests_reset_date')}),
    )


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'formatted_value', 'description', 'is_secret', 'updated_at']
    list_filter = ['is_secret']
    search_fields = ['key', 'description', 'value']
    ordering = ['key']

    def formatted_value(self, obj):
        if obj.is_secret and obj.value:
            masked = ('•' * 12) + obj.value[-4:] if len(obj.value) > 4 else '••••••••'
            return format_html('<code>{}</code>', masked)
        return format_html('<code>{}</code>', obj.value or '<empty>')
    formatted_value.short_description = 'Current Value'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.key == 'AI_PROVIDER':
            form.base_fields['value'].help_text = 'Provider options: openrouter | openai | anthropic | google | custom'
        elif obj and obj.key == 'AI_API_KEY':
            form.base_fields['value'].help_text = 'API Key for OpenRouter, OpenAI, Anthropic, or Google Gemini'
        elif obj and obj.key == 'AI_MODEL':
            form.base_fields['value'].help_text = 'Model name (e.g. openai/gpt-4o-mini, gpt-4o, claude-3-5-sonnet-20241022, gemini-1.5-flash)'
        elif obj and obj.key == 'AI_BASE_URL':
            form.base_fields['value'].help_text = 'Endpoint URL (e.g. https://openrouter.ai/api/v1, https://api.openai.com/v1, https://api.anthropic.com/v1)'
        return form
