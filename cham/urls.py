# cham/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index', views.Index, name='index'),
    path('hom/', views.Home, name='home'),
    path('abou/', views.About, name='about'),
    path('contac/', views.Contact, name='contact'),
    path('service/', views.Services, name='services'),
    path('breed/', views.Breeds, name='breeds'),

    
]