from rest_framework import serializers
from seguridad.models import (
    Permisos, 
    PermisosModulo, 
    PermisosModuloRol,
)


class PermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = '__all__'
        

class PermisosModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisosModulo
        fields = '__all__'
    
class PermisosModuloRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermisosModuloRol
        fields = '__all__'