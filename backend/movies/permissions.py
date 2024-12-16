from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자만 편집/삭제할 수 있도록 하는 권한
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return obj.user == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    관리자만 영화 정보를 수정할 수 있도록 하는 권한
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return request.user and request.user.is_staff