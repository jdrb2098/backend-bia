from seguridad.choices.tipo_usuario_choices import tipo_usuario_CHOICES 
from rest_framework.permissions import BasePermission

class TipoUsuarioBase(BasePermission):
    
    def has_permission(self, request, view):
        tipo_usuario = "I"
        print(view)
        return request.user.tipo_usuario == tipo_usuario
    

class IsDeveloper(BasePermission):
   def has_permission(self, request, view):
      return request.user.is_developer and request.user.is_authenticated