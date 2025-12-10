from rest_framework import permissions

class IsSalesOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.role == 'SALES' and request.method == 'POST':
            return True
            
        return request.user.role == 'ADMIN'
    
class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.user.role == 'ADMIN':
            return True
            
        if request.user.role == 'SALES':
            if request.method == 'DELETE':
                return False 
            return True 
            
        return False