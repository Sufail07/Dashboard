from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role.name.lower() == "admin":
            return True
        return False



class RoleBasedPermission(BasePermission):
    permission_map = {}

    def has_permission(self, request, view):
        user = request.user
        
        if not user or not user.is_authenticated:
            return False

        if not user.role:
            return False

        if user.role.name == "Admin":
            return True
        
        action = self.permission_map.get(request.method)

        if not action:
            return False

        return getattr(user.role, action, False)
    
    
class DashboardPermission(RoleBasedPermission):
    permission_map = {
        "GET": "can_view_dashboard",
        "PUT": "can_edit_dashboard",
        "PATCH": "can_edit_dashboard",
        "POST": "can_create_dashboard",
        "DELETE": "can_delete_dashboard"
    }
    
class FinancialRecordPermission(RoleBasedPermission):
    permission_map = {
        "GET": "can_view_record",
        "POST": "can_create_record",
        "PUT": "can_edit_record",
        "PATCH": "can_edit_record",
        "DELETE": "can_delete_record",
    }

class SummaryPermission(RoleBasedPermission):
    permission_map = {
        "GET": "can_view_summary"
    }