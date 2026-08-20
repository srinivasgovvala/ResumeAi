from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.conf import settings
from .forms import EmailSignupForm, EmailLoginForm
from .utils import send_otp_email, verify_otp_code, send_welcome_email
from .models import EmailOTP
import logging

logger = logging.getLogger('apps')
User = get_user_model()


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/landing.html')


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_email_verified = False
            user.save()
            send_otp_email(user.email)
            request.session['pending_otp_email'] = user.email
            messages.info(request, f'Verification code sent to {user.email}. Please enter the OTP to complete registration.')
            return redirect('verify_otp')
    else:
        form = EmailSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


@csrf_protect
def verify_otp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    email = request.session.get('pending_otp_email') or request.GET.get('email')
    if not email:
        messages.warning(request, 'No pending email verification found. Please sign up.')
        return redirect('signup')

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        if not otp_code:
            digits = [request.POST.get(f'digit_{i}', '').strip() for i in range(1, 7)]
            otp_code = ''.join(digits)

        success, msg = verify_otp_code(email, otp_code)
        if success:
            try:
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.is_active = True
                user.save(update_fields=['is_email_verified', 'is_active'])
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session.pop('pending_otp_email', None)

                # Send welcome email to user
                send_welcome_email(user)

                messages.success(request, 'Welcome to Resume AI! Your email has been verified.')
                return redirect('dashboard')
            except User.DoesNotExist:
                messages.error(request, 'User account not found. Please sign up again.')
                return redirect('signup')
        else:
            messages.error(request, msg)

    return render(request, 'accounts/verify_otp.html', {
        'email': email,
    })


@csrf_protect
@require_POST
def resend_otp(request):
    email = request.session.get('pending_otp_email') or request.POST.get('email')
    if not email:
        messages.error(request, 'Session expired. Please sign up again.')
        return redirect('signup')

    last_otp = EmailOTP.objects.filter(email=email).order_by('-created_at').first()
    if last_otp and (timezone.now() - last_otp.created_at).total_seconds() < 60:
        remaining_sec = int(60 - (timezone.now() - last_otp.created_at).total_seconds())
        messages.warning(request, f'Please wait {remaining_sec} seconds before requesting another code.')
        return redirect('verify_otp')

    send_otp_email(email)
    messages.success(request, f'A new verification code has been sent to {email}.')
    return redirect('verify_otp')


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', '/dashboard/')
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = EmailLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def profile(request):
    return render(request, 'profile/profile.html', {'user': request.user})


@login_required
@require_POST
def update_profile(request):
    user = request.user
    user.first_name = request.POST.get('first_name', user.first_name)
    user.last_name = request.POST.get('last_name', user.last_name)
    user.save()
    messages.success(request, 'Profile updated.')
    return redirect('profile')


@login_required
def settings_view(request):
    return render(request, 'profile/settings.html', {'user': request.user})
