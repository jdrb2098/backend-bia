from rest_framework import serializers
from seguridad.models import Auditorias
from seguridad.serializers.user_serializers import UserSerializer
from seguridad.serializers.permisos_serializers import PermisosSerializer, ModulosSerializers

class AuditoriasSerializers(serializers.ModelSerializer):
    id_modulo=ModulosSerializers(read_only=True)
    id_usuario=UserSerializer(read_only=True)
    id_cod_operacion=PermisosSerializer(read_only=True)

    class Meta:
        model=Auditorias
        fields= '__all__'

        







