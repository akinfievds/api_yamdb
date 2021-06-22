from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == request.user.UserRole.ADMIN
            or request.user.is_staff
        )


class IsAuthorOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            # or request.user.is_superuser
            or request.user.role == request.user.UserRole.MODERATOR
            or request.user.role == request.user.UserRole.ADMIN
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == request.user.UserRole.ADMIN
            or request.user.is_staff
            or request.method in SAFE_METHODS
        )


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.user.role == request.user.UserRole.MODERATOR
            or request.user.role == request.user.UserRole.ADMIN
        )
