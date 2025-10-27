# cham/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Re-register UserAdmin to ensure 'is_active' is editable
admin.site.unregister(User)
admin.site.register(User, UserAdmin)