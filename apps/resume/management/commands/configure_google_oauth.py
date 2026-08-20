import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Configure Google OAuth Social Application from environment variables'

    def handle(self, *args, **options):
        client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')

        if not client_id or not client_secret:
            self.stdout.write(self.style.WARNING(
                'GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set — skipping Google OAuth setup.'
            ))
            return

        try:
            from allauth.socialaccount.models import SocialApp
            from django.contrib.sites.models import Site

            site = Site.objects.get(id=1)
            app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': client_id,
                    'secret': client_secret,
                }
            )
            if not created:
                app.client_id = client_id
                app.secret = client_secret
                app.save()

            app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(
                f'Google OAuth app {"created" if created else "updated"} and linked to site.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to configure Google OAuth: {e}'))
