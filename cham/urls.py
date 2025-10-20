from django.urls import path
from . import views

urlpatterns = [
    path('INDEX', views.Index, name='index'),
    path('home/', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('services/', views.Services, name='services'),
    path('breeds/', views.Breeds, name='breeds'),
]