# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['phone', 'address', 'city', 'postal_code']

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)