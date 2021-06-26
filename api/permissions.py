from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == request.user.UserRole.ADMIN
                or request.user.is_staff
            )
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == request.user.UserRole.ADMIN
                or request.user.is_staff
            )
        )


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role == request.user.UserRole.MODERATOR
                or request.user.role == request.user.UserRole.ADMIN
            )
        )
