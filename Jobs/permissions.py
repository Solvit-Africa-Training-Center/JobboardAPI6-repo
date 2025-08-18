from rest_framework.permissions import BasePermission
from .models import User
from django.core.exceptions import ImproperlyConfigured

class RolePermission(BasePermission):
    '''Base permissions to check if a user has one of the allowed roles.
    Subclasses must define 'allowed_roles'.'''
    allowed_roles= []

    def has_permission(self, request, view):
        if self.allowed_roles is None:
            raise ImproperlyConfigured(
                f"{self.__class.__name__} must define 'allowed_roles"
            )
        return(
            request.user.is_authenticated and getattr(request.user, 'role', None) in self.allowed_roles
        )
    
# ROLE-BASED PERMISSIONS     
class IsAdmin(RolePermission):
    allowed_roles=[User.Role.ADMIN]

class IsRecruiter(RolePermission):
    allowed_roles=[User.Role.RECRUITER]
class IsCandidate(RolePermission):
    allowed_roles=[User.Role.CANDIDATE]

class IsAdminOrRecruiter(RolePermission):
    allowed_roles=[User.Role.RECRUITER, User.Role.ADMIN]

# OBJECT-LEVEL PERMISSION 

class IsOwnerorAdmin(BasePermission):
    """
    Object-level permission:
    - Admin can access everything
    - Owners can access only their own objects
    """
    owner_field= 'recruiter'
    #by default to check  ownership

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role== User.Role.ADMIN:
            return True
        owner=getattr(obj, self.owner_field, None)
        return owner==request.user
    
class ApplicationPermission(BasePermission):
    #Rolebased Permission for application

    def has_permission(self, request, view):
       if request.user.is_authenticated:
           return True
       return False
    def has_object_permission(self, request, view, obj):
        role=request.user.role
        if role== "admin":
            return True #full Access
        if role == 'candidate':
            return obj.candidate== request.user #only Owner applications
        if role== 'recruiter':
            return obj.recruiter == request.user #Applications to their own job
        return False



