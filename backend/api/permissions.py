from rest_framework import permissions


class IsAdministrador(permissions.BasePermission):
    """Permiso personalizado para usuarios administradores"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'ADMINISTRADOR'
        )


class IsAdministradorOrReadOnly(permissions.BasePermission):
    """Permite lectura a todos, escritura solo a administradores"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'ADMINISTRADOR'
        )

