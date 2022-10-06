from rest_framework import serializers
from seguridad.models import Auditorias, Modulos
from seguridad.serializers.user_serializers import UserSerializer
from seguridad.serializers.permisos_serializers import PermisosSerializer


    
class ModulosSerializers(serializers.ModelSerializer):
    class Meta:
        model=Modulos
        fields='__all__'
        
class AuditoriasSerializers(serializers.ModelSerializer):
    id_modulo=ModulosSerializers(read_only=True)
    id_usuario=UserSerializer(read_only=True)
    id_cod_operacion=PermisosSerializer(read_only=True)

    class Meta:
        model=Auditorias
        fields= '__all__'

        







