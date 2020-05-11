from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        return current_user.role == 0


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        return current_user == obj.user
