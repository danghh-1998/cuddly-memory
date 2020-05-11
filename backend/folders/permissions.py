from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        return current_user.role == 1

    def has_object_permission(self, request, view, obj):
        current_user = request.user
        return obj.user == current_user


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        owner = obj.user
        access_users = [*list(owner.sub_users.all()), owner]
        return current_user in access_users
