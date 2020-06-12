from rest_framework.permissions import BasePermission


class SuperAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.client == request.user.client

    def has_permission(self, request, view):
        return request.user.role == 2
