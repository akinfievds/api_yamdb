from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == request.user.UserRole.ADMIN
                    or request.user.is_staff)
        return False
