from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == User.UserRole.ADMIN
                or request.user.is_staff
            )
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.role == User.UserRole.ADMIN
            )
        return request.method in SAFE_METHODS


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_staff
                or request.user.role == User.UserRole.MODERATOR
                or request.user.role == User.UserRole.ADMIN
            )
        return request.method in SAFE_METHODS
