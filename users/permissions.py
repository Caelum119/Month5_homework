from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModeratorPermission(BasePermission):
    

    def has_permission(self, request, view):
        if request.method == 'POST':
            return False  
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated and request.user.is_staff
        return False
