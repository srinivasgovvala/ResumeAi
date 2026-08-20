import random
import datetime
import logging
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import EmailOTP

logger = logging.getLogger('apps')

def send_otp_email(email):
    """
    Generates a 6-digit OTP code, saves it to EmailOTP table,
    and sends a beautiful verification email.
    """
    otp_code = f'{random.randint(100000, 999999)}'
    expires_at = timezone.now() + datetime.timedelta(minutes=10)

    # Invalidate previous unverified OTPs for this email
    EmailOTP.objects.filter(email=email, is_verified=False).update(is_verified=True)

    EmailOTP.objects.create(
        email=email,
        otp_code=otp_code,
        expires_at=expires_at,
        is_verified=False,
        attempts=0,
    )

    subject = 'Your Verification Code — ResumeAi'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
    
    html_content = render_to_string('emails/otp.html', {'otp_code': otp_code})
    text_content = f"Verification Code\n\nHi there,\n\nThank you for using ResumeAi. To complete your request and securely verify your email address, please enter the following verification code:\n\n{otp_code}\n\nThis code will expire in 10 minutes for security purposes.\n\nIf you did not initiate this request, you do not need to take any action. Your account remains secure.\n\nBest regards,\nThe ResumeAi Team\n\n---\nThis email was sent by ResumeAi.\nIf you did not request this communication, please safely ignore it.\n\n© {timezone.now().year} ResumeAi. All rights reserved."

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        logger.error(f'Failed to send OTP email to {email}: {e}')

    return otp_code

def verify_otp_code(email, code):
    """
    Verifies the submitted 6-digit OTP code.
    Returns (success_bool, message_str).
    """
    code = (code or '').strip()
    if not code or len(code) != 6:
        return False, 'Please enter a valid 6-digit OTP code.'

    now = timezone.now()
    otp = EmailOTP.objects.filter(
        email=email,
        is_verified=False,
        expires_at__gte=now,
    ).first()

    if not otp:
        return False, 'OTP code has expired or is invalid. Please request a new code.'

    if otp.attempts >= 5:
        return False, 'Too many incorrect attempts. Please request a new OTP code.'

    if otp.otp_code == code:
        otp.is_verified = True
        otp.save(update_fields=['is_verified'])
        return True, 'Email verified successfully.'
    else:
        otp.attempts += 1
        otp.save(update_fields=['attempts'])
        remaining = 5 - otp.attempts
        return False, f'Incorrect OTP code. {remaining} attempt(s) remaining.'

def send_welcome_email(user):
    """
    Sends a beautiful HTML welcome email to the user after successful registration.
    """
    first_name = user.first_name or user.email.split('@')[0]
    subject = 'Welcome to ResumeAi'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')

    import os
    # On Vercel, VERCEL_URL is provided without protocol
    site_url = os.environ.get('SITE_URL')
    if not site_url:
        vercel_url = os.environ.get('VERCEL_URL')
        site_url = f"https://{vercel_url}" if vercel_url else "http://localhost:8000"

    dashboard_url = f"{site_url.rstrip('/')}/dashboard/"
    is_local = 'localhost' in dashboard_url or '127.0.0.1' in dashboard_url

    context = {
        'first_name': first_name,
        'dashboard_url': dashboard_url,
        'is_local': is_local
    }

    html_content = render_to_string('emails/welcome.html', context)

    # Make the plain text perfectly match the HTML structure to avoid spam filters
    text_content = f"Welcome to ResumeAi\n\nHi {first_name},\n\nThank you for creating an account with ResumeAi. Your registration is complete, and your workspace is fully set up.\n\nYou now have access to our complete suite of career tools designed to optimize your application process:\n\n- ATS-Optimized Builder: Create professional resumes using industry-standard layouts.\n- Score Checker: Analyze your resume against specific job descriptions.\n- AI Career Coach: Refine bullet points and generate tailored professional summaries.\n- Cloud Sync: Automatically back up your PDF exports to Google Drive.\n\n"

    if not is_local:
        text_content += f"Access Your Dashboard: {dashboard_url}\n\n"
    else:
        text_content += "Please return to your browser to access the dashboard.\n\n"

    text_content += f"If you require any assistance getting started, please reply directly to this email. Our support team is here to help.\n\nBest regards,\nThe ResumeAi Team\n\n---\nThis email was sent by ResumeAi.\nIf you did not request this communication, please safely ignore it.\n\n© {timezone.now().year} ResumeAi. All rights reserved."

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
    except Exception as e:
        logger.error(f'Failed to send welcome email to {user.email}: {e}')
