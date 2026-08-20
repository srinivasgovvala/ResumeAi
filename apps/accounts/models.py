from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(blank=True)
    is_google_user = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    google_drive_token = models.JSONField(null=True, blank=True)
    google_drive_folder_id = models.CharField(max_length=200, blank=True)
    ai_requests_today = models.IntegerField(default=0)
    ai_requests_reset_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email.split('@')[0]


class EmailOTP(models.Model):
    email = models.EmailField(db_index=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email OTP'
        verbose_name_plural = 'Email OTPs'

    def __str__(self):
        return f'{self.email} - {self.otp_code}'


class AppSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_secret = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'App Setting'
        verbose_name_plural = 'App Settings'

    def __str__(self):
        return self.key

    @classmethod
    def get(cls, key, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default
