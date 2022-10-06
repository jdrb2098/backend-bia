from seguridad.serializers.roles_serializers import RolesSerializer
from rest_framework import serializers
from seguridad.models import (
    Permisos, 
    PermisosModulo, 
    PermisosModuloRol,
    Modulos
)

class ModulosSerializers(serializers.ModelSerializer):
    class Meta:
        model=Modulos
        fields='__all__'

class PermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = '__all__'
        
class PermisosModuloSerializer(serializers.ModelSerializer):
    id_modulo = ModulosSerializers(read_only=True)
    cod_permiso = PermisosSerializer(read_only=True)    
    class Meta:
        model = PermisosModulo
        fields = '__all__'
        
class PermisosModuloRolSerializer(serializers.ModelSerializer):
    cod_permiso = PermisosSerializer(read_only=True)
    id_rol = RolesSerializer(read_only=True)
    id_modulo = PermisosModuloSerializer(read_only=True)
    class Meta:
        model = PermisosModuloRol
        fields = '__all__'