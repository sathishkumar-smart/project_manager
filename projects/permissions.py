from rest_framework import permissions
from .models import ProjectMember

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write methods, check ownership
        return obj.owner == request.user


class IsAssignedOrOwner(permissions.BasePermission):
    """
    Custom permission for tasks:
    Owner of project or assigned user can edit/view.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.project.owner == request.user or obj.assigned_to == request.user

        return obj.project.owner == request.user

class IsProjectMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, 'project', None) or getattr(obj, 'task', None).project
        return ProjectMember.objects.filter(project=project, user=request.user).exists()