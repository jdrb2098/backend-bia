from seguridad.choices.tipo_usuario_choices import tipo_usuario_CHOICES 
from rest_framework.permissions import BasePermission
from seguridad.models import UsuariosRol, PermisosModuloRol
from django.db.models import Q

class TipoUsuarioBase(BasePermission):
    
    def has_permission(self, request, view):
        tipo_usuario = "I"
        print(view)
        return request.user.tipo_usuario == tipo_usuario
    

class PermisoActualizarPersona(BasePermission):
   def has_permission(self, request, view):
    id_user = request.user.id_usuario
    user_roles = UsuariosRol.objects.filter(id_usuario=id_user)

    for rol in user_roles:
        id_rol=  rol.id_rol
        permisos_modulo_rol = PermisosModuloRol.objects.filter(Q(id_rol=id_rol) & Q(id_permiso_modulo=1))
        if permisos_modulo_rol:
            return True

    return False


class PermisoConsultarPersona(BasePermission):
   def has_permission(self, request, view):
    id_user = request.user.id_usuario
    user_roles = UsuariosRol.objects.filter(id_usuario=id_user)

    for rol in user_roles:
        
        permisos_modulo_rol = PermisosModuloRol.objects.filter(Q(id_rol=rol.id_rol) & Q(id_permiso_modulo=2))
        if permisos_modulo_rol:
            return True

    return False