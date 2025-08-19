from rest_framework import permissions

class DevicePermission(permissions.BasePermission):
    """
    Custom permission for device operations based on user roles.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin has full access
        if request.user.role == 'admin':
            return True
        
        # Engineers can read, create, update but not delete
        if request.user.role == 'engineer':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']
        
        # Viewers can only read
        if request.user.role == 'viewer':
            return request.method in ['GET']
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        
        if request.user.role == 'engineer':
            return request.method in ['GET', 'PUT', 'PATCH']
        
        if request.user.role == 'viewer':
            return request.method in ['GET']
        
        return False

class CommandPermission(permissions.BasePermission):
    """
    Permission for executing commands on devices.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Only admin and engineers can execute commands
        return request.user.role in ['admin', 'engineer']
