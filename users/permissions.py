from rest_framework import permissions


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.is_superuser


class HasObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj == request.user
