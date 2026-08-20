from django.core.management.base import BaseCommand
from apps.resume.models import ResumeTemplate
from apps.resume.template_engine import TEMPLATES
from apps.ats.models import ATSConfig
from apps.accounts.models import AppSettings


class Command(BaseCommand):
    help = 'Seed initial data: templates, ATS config, app settings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding resume templates...')
        order = 1
        for slug, tpl in TEMPLATES.items():
            t, created = ResumeTemplate.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': tpl['name'],
                    'description': tpl.get('description', ''),
                    'category': tpl.get('category', 'universal'),
                    'best_for': tpl.get('best_for', ''),
                    'sort_order': order,
                    'is_active': True,
                    'is_ats_friendly': True,
                    'styles': tpl.get('styles', {}),
                    'pdf_config': tpl.get('pdf', {}),
                    'section_order_experienced': tpl.get('section_order_experienced', []),
                    'section_order_fresher': tpl.get('section_order_fresher', []),
                }
            )
            order += 1
            self.stdout.write(f'  {"created" if created else "updated"} — {t.name}')

        # ATS config
        self.stdout.write('Seeding ATS config...')
        configs = [
            ('keyword_weight',     0.40, 'Weight for keyword match score'),
            ('section_weight',     0.25, 'Weight for section presence score'),
            ('format_weight',      0.20, 'Weight for formatting score'),
            ('readability_weight', 0.15, 'Weight for readability score'),
            ('min_skills_count',   8,    'Minimum recommended skills count'),
            ('min_word_count',     200,  'Minimum resume word count'),
        ]
        for name, value, desc in configs:
            _, created = ATSConfig.objects.get_or_create(
                name=name,
                defaults={'value': value, 'description': desc}
            )
            self.stdout.write(f'  {"created" if created else "exists"} — {name}')

        # App settings
        self.stdout.write('Seeding app settings...')
        settings_defaults = [
            ('AI_PROVIDER',            'openrouter',          'AI Provider (openrouter, openai, anthropic, google, custom)', False),
            ('AI_API_KEY',             '',                    'API Key for AI Provider',                                    True),
            ('AI_MODEL',               'openai/gpt-4o-mini',  'AI Model name (e.g. openai/gpt-4o-mini, gpt-4o, claude-3-5-sonnet-20241022, gemini-1.5-flash)', False),
            ('AI_BASE_URL',            'https://openrouter.ai/api/v1', 'AI API Base URL endpoint',                           False),
            ('AI_ENABLED',             'true',                'Enable or disable AI features (true/false)',                 False),
            ('AI_MAX_REQUESTS_PER_DAY','50',                  'Max AI requests per user per day',                           False),
            ('RESUME_MAX_PER_USER',    '20',                  'Max resumes per user',                                       False),
            ('SITE_NAME',              'ATS Resume Builder',   'Application name shown in UI',                              False),
        ]
        for key, value, desc, is_secret in settings_defaults:
            _, created = AppSettings.objects.get_or_create(
                key=key,
                defaults={'value': value, 'description': desc, 'is_secret': is_secret}
            )
            self.stdout.write(f'  {"created" if created else "exists"} — {key}')

        self.stdout.write(self.style.SUCCESS('\nSeed data complete. 15 templates, ATS config, and AI provider settings ready.'))
