from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == request.user.UserRole.ADMIN
                or request.user.is_staff
            )
        return False


class IsAllRolesOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or obj.author == request.user.is_superuser
            or request.user.role == request.user.UserRole.MODERATOR
            or request.user.role == request.user.UserRole.ADMIN
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.role == request.user.UserRole.ADMIN
            or request.user.is_staff
        )
