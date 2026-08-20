from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .utils import send_welcome_email

@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    # This signal is fired when a user successfully signs up via allauth (Google OAuth).
    # Since email verification is not required for social login in this app,
    # we can send the welcome email directly.
    # Note: If the user signed up via regular email, our view handles it manually
    # after they verify their OTP, but allauth also fires this for social accounts.
    
    # Check if they logged in via social account
    if user.is_google_user or kwargs.get('sociallogin'):
        # Send the welcome email
        send_welcome_email(user)
