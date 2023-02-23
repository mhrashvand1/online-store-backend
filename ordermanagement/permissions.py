from rest_framework.permissions import BasePermission


class OrderDeletePermission(BasePermission): 
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return obj.status != 'deleted'
        
        # Staffs can delete only orders with status paid.
        if user.is_staff:
            return obj.status == 'paid'
        
        return bool(obj.status == 'paid' and obj.user == user)
        
        