from rest_framework import permissions

from apps.classifieds.models import DRAFT


class DraftClassifiedPermission(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):
    return request.method in ['GET', 'POST', 'DELETE'] and obj.status == DRAFT


class PublishedClassifiedPermission(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):
    return request.method in ['GET', 'PUT', 'PATCH', 'DELETE'] and obj.status != DRAFT


class ClassifiedOwner(permissions.BasePermission):
    """
    Custom permission to allow only classified owners to perform CRUD operations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ClassifiedOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow classified owners to perform CRUD operations
    while allowing read-only access for others.
    """

    def has_permission(self, request, view):
        # Allow read-only access (GET, HEAD, OPTIONS) for all users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the classified object for other methods.
        return True  # Add your logic here to check if the user is the owner.

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS for all users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the classified object for other methods.
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admin users to perform CRUD operations
    while allowing read-only access for non-admin users.
    """

    def has_permission(self, request, view):
        # Allow read-only access (GET, HEAD, OPTIONS) for all users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an admin user.
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS for all users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an admin user.
        return request.user and request.user.is_staff
