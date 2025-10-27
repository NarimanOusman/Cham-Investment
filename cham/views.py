# cham/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.forms import SetPasswordForm
from django import forms

# Custom OTP storage (in production, use cache like Redis)
otp_storage = {}

def Index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

def Home(request):
    return render(request, 'home.html')

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Breeds(request):
    return render(request, 'breeds.html')

def Services(request):
    return render(request, 'services.html')

# Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
    class LoginForm(forms.Form):
        email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    context = {'login_form': LoginForm()}
    return render(request, 'login.html', context)

# Sign Up View
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            return redirect('home')
    class RegisterForm(forms.Form):
        username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label="Confirm Password")
    context = {'register_form': RegisterForm()}
    return render(request, 'signup.html', context)

# Logout View
def user_logout(request):
    logout(request)
    return redirect('index')

# Password Reset Request
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            code = str(random.randint(10000, 99999))
            otp_storage[email] = code
            send_mail(
                'Your Password Reset Code',
                f'Your 5-digit verification code is: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, "Code sent to your email.")
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
    class ResetForm(forms.Form):
        email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email for reset'}))
    return render(request, 'login.html', {'login_form': ResetForm()})

# OTP Verification
def verify_otp(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = None
        for k, v in otp_storage.items():
            if v == code:
                email = k
                break
        if email:
            request.session['reset_email'] = email
            del otp_storage[email]
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid code.")
    class OTPForm(forms.Form):
        code = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': '12345'}))
    return render(request, 'verify_otp.html', {'form': OTPForm()})

# Reset Password
def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('password_reset')
    user = User.objects.get(email=email)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['reset_email']
            messages.success(request, "Password updated. Please login.")
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'reset_password.html', {'form': form})