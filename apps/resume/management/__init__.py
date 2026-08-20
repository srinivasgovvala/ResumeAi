import json
from django.core.management.base import BaseCommand
from apps.resume.models import ResumeTemplate


class Command(BaseCommand):
    help = 'Create initial data: resume templates, ATS config'

    def handle(self, *args, **kwargs):
        # Resume template
        ResumeTemplate.objects.get_or_create(
            slug='classic-1col',
            defaults={
                'name': 'Classic (1-Column)',
                'description': 'Traditional single-column ATS-friendly resume. Works for freshers and experienced candidates.',
                'is_active': True,
                'is_ats_friendly': True,
            }
        )
        self.stdout.write(self.style.SUCCESS('Initial data created.'))
