from django.contrib import admin
from .models import Resume, ResumeTemplate


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'best_for', 'sort_order', 'is_active', 'is_ats_friendly', 'created_at']
    list_filter = ['is_active', 'is_ats_friendly', 'category']
    search_fields = ['name', 'slug', 'description', 'category', 'best_for']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']

    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'slug', 'description', 'category', 'best_for', 'sort_order', 'is_active', 'is_ats_friendly', 'preview_image')
        }),
        ('Section Orders (JSON Lists)', {
            'fields': ('section_order_experienced', 'section_order_fresher'),
            'description': 'JSON arrays defining section slugs order (e.g., ["header", "summary", "experience", "education", "skills", "projects", "certifications"])'
        }),
        ('CSS & UI Styles (JSON Dict)', {
            'fields': ('styles',),
            'description': 'JSON object defining HTML preview styles: font_family, font_size, line_height, accent_color, name_size, section_header_color, margin, etc.'
        }),
        ('PDF Configuration (JSON Dict)', {
            'fields': ('pdf_config',),
            'description': 'JSON object defining ReportLab PDF settings: name_size, accent, section_size, body_size, left_margin, right_margin, top_margin, etc.'
        }),
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'template_style', 'status', 'last_ats_score', 'created_at', 'updated_at']
    list_filter = ['status', 'template_style']
    search_fields = ['title', 'user__email', 'full_name']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']
