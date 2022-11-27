"""
Admin rules for dashboard app
"""
from functools import update_wrapper
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Student, StudentMentorCard, StudentSession, MentorNotes

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


# Unregistrations of tables in Admin
admin.site.unregister(EmailAddress)
admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)


def admin_view(view, cacheable=False):
    """
    Dissallow non admins and courseadministrators to access admin.
    Found information on Stackoverflow to solve this.
    """
    def inner(request, *args, **kwargs):
        if not request.user.is_active and not request.user.is_staff:
            raise Http404()
        return view(request, *args, **kwargs)

    if not cacheable:
        inner = never_cache(inner)

    if not getattr(view, 'csrf_exempt', False):
        inner = csrf_protect(inner)

    return update_wrapper(inner, view)


class UserAdmin(BaseUserAdmin):
    """
    Class to display the UserAdmin options for create and change
    users as Admin
    """

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    list_display = ['email', 'admin', 'staff', 'created_on']
    list_filter = ['admin', 'staff']
    fieldsets = (
        ('User credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Type of user', {'fields': ('admin', 'staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Enter User credentials', {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}),
        ('Personal info', {'fields': ('name',)}),
        ('Type of User', {'fields': ('admin', 'staff',)}),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(StudentMentorCard)
admin.site.register(MentorNotes)
admin.site.register(Student)
admin.site.register(StudentSession)
