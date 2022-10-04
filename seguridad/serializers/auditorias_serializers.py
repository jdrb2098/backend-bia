from rest_framework import serializers
from seguridad.models import Auditorias, Modulos

class AuditoriasSerializers(serializers.ModelSerializer):
    class Meta:
        model=Auditorias
        field= '__all__'

class ModulosSerializers(serializers.ModelSerializer):
    class Meta:
        model=Modulos
        field='__all__'
        






