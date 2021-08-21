"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check object and user are the same."""
        return request.user == obj


class IsSiteAdmin(BasePermission):
    """Allow CRUD access only to site admins."""

    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        return not request.user.is_client
