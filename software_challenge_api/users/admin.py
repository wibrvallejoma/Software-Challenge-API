"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from software_challenge_api.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
