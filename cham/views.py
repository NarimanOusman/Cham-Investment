from django.shortcuts import render

def Home(request):
    return render(request, 'home.html')

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Index(request):
    return render(request, 'index.html')

def Breeds(request):
    return render(request, 'breeds.html')

def Services(request):
    return render(request, 'services.html')