"""
Admin rules for dashboard app
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

