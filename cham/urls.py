# cham/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index, name='index'),
    path('home/', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('services/', views.Services, name='services'),
    path('breeds/', views.Breeds, name='breeds'),

    # Auth URLs
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]