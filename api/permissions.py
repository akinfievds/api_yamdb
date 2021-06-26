from rest_framework.permissions import SAFE_METHODS, BasePermission

from api.models import User


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
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_staff
                    or request.user.role == User.UserRole.ADMIN
                )
            )
        )


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.role == User.UserRole.ADMIN
                    or request.user.role == User.UserRole.MODERATOR
                )
            )
        )
