from almacen.models.generics_models import UnidadesMedida
from seguridad.serializers.personas_serializers import PersonasSerializer
from almacen.models.generics_models import Magnitudes
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from almacen.models.mantenimientos_models import (
    ProgramacionMantenimientos,
    RegistroMantenimientos
)
        
class SerializerProgramacionMantenimientos(serializers.ModelSerializer):
    class Meta:
        model=ProgramacionMantenimientos
        fields=('__all__')
        
class SerializerRegistroMantenimientos(serializers.ModelSerializer):
    class Meta:
        model=RegistroMantenimientos
        fields=('__all__')