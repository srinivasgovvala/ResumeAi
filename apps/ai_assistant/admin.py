from django.contrib import admin
from .models import ChatSession, ChatMessage, AIUsageLog


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    search_fields = ['user__email', 'title']
    raw_id_fields = ['user']


@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'tokens_used', 'model_used', 'created_at']
    list_filter = ['action', 'model_used']
    search_fields = ['user__email']
    raw_id_fields = ['user']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False
