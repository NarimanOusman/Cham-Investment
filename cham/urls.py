from django.urls import path
from . import views

urlpatterns = [
    path('INDEX', views.Index, name='index'),
    path('hom/', views.Home, name='home'),
    path('abou/', views.About, name='about'),
    path('contac/', views.Contact, name='contact'),
    path('service/', views.Services, name='services'),
    path('breed/', views.Breeds, name='breeds'),
]