# cham/views.py
from django.shortcuts import render, redirect

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

