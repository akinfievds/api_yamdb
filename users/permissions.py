from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user == request.user.is_superuser
        )


class IsAllRolesOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user or
            obj.author == request.user.is_superuser or
            request.user.role == request.user.UserRole.MODERATOR or
            request.user.role == request.user.UserRole.ADMIN
        )
