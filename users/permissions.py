from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
    
        return request.user.is_authenticated and request.user.is_superuser
    
class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        
        return request.user.is_authenticated and request.user.user_type=="teacher"
    
class IsStudent(BasePermission):

    def has_permission(self, request, view):
        
        return request.user.us_authenticated and request.user.user_type=="student"
    
class IsTeacherorAdmin(BasePermission):

    def has_permission(self, request, view):
        
        return request.user.is_authenticated and (request.user.user_type == 'teacher' or request.user.is_superuser)