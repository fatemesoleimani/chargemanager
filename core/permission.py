from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and not request.user.is_superuser
        )
