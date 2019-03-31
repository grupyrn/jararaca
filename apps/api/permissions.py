from rest_framework import permissions

from .models import *


class IsOwnerOrSuperUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, Event):
            return obj.created_by == request.user

        return False
