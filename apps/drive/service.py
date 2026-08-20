import logging
from django.conf import settings

logger = logging.getLogger('apps')


class DriveService:
    def __init__(self, user):
        self.user = user
        self._service = None

    def _get_service(self):
        if self._service:
            return self._service

        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from allauth.socialaccount.models import SocialToken, SocialApp

            social_token = SocialToken.objects.filter(
                account__user=self.user,
                account__provider='google',
            ).select_related('app').first()

            if not social_token:
                raise ValueError('No Google account connected. Please sign in with Google to use Drive.')

            credentials = Credentials(
                token=social_token.token,
                refresh_token=social_token.token_secret,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
            )

            self._service = build('drive', 'v3', credentials=credentials)
            return self._service
        except ImportError:
            raise RuntimeError('Google API client library not installed.')

    def _ensure_folder(self):
        if self.user.google_drive_folder_id:
            return self.user.google_drive_folder_id

        service = self._get_service()
        file_metadata = {
            'name': 'ATS Resume Builder',
            'mimeType': 'application/vnd.google-apps.folder',
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
        self.user.google_drive_folder_id = folder_id
        self.user.save(update_fields=['google_drive_folder_id'])
        return folder_id

    def upload_resume(self, pdf_bytes, filename, resume=None):
        from googleapiclient.http import MediaInMemoryUpload
        from apps.drive.models import DriveFile

        service = self._get_service()
        folder_id = self._ensure_folder()

        media = MediaInMemoryUpload(pdf_bytes, mimetype='application/pdf', resumable=False)
        file_metadata = {
            'name': filename,
            'parents': [folder_id],
        }

        # Check if file already exists for this resume
        existing_file_id = None
        if resume and resume.drive_file_id:
            existing_file_id = resume.drive_file_id

        if existing_file_id:
            file = service.files().update(
                fileId=existing_file_id,
                media_body=media,
                fields='id,webViewLink,webContentLink,size',
            ).execute()
        else:
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink,webContentLink,size',
            ).execute()

        # Track in DB
        drive_file, _ = DriveFile.objects.update_or_create(
            user=self.user,
            resume=resume,
            defaults={
                'file_name': filename,
                'drive_file_id': file['id'],
                'drive_view_url': file.get('webViewLink', ''),
                'drive_download_url': file.get('webContentLink', ''),
                'file_size': int(file.get('size', 0)),
            }
        )

        return file

    def list_files(self):
        service = self._get_service()
        folder_id = self._ensure_folder()

        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields='files(id,name,webViewLink,modifiedTime,size,mimeType)',
            orderBy='modifiedTime desc',
        ).execute()

        return results.get('files', [])

    def delete_file(self, file_id):
        service = self._get_service()
        service.files().delete(fileId=file_id).execute()
