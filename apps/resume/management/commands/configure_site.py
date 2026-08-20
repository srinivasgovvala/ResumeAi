import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Configure the django.contrib.sites Site for allauth'

    def add_arguments(self, parser):
        parser.add_argument('--domain', default=None)

    def handle(self, *args, **options):
        from django.contrib.sites.models import Site
        domain = options['domain'] or os.environ.get('SITE_DOMAIN', '127.0.0.1:8000')
        name = 'ATS Resume Builder'
        site, created = Site.objects.get_or_create(id=1, defaults={'domain': domain, 'name': name})
        if not created:
            site.domain = domain
            site.name = name
            site.save()
        self.stdout.write(self.style.SUCCESS(f'Site configured: {domain}'))
