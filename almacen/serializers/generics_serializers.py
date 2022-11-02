from almacen.models.generics_models import UnidadesMedida
from seguridad.serializers.personas_serializers import PersonasSerializer
from almacen.models.generics_models import Magnitudes
from rest_framework import serializers
from almacen.models.generics_models import Marcas, EstadosArticulo,Bodegas,PorcentajesIVA
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class SerializersMarca(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=Marcas.objects.all())])
    class Meta:
        model=Marcas
        fields=('__all__')
        

class SerializersEstadosArticulo(serializers.ModelSerializer):
    class Meta:
        model=EstadosArticulo
        fields=('__all__')
        
class SerializerBodegas(serializers.ModelSerializer):
    persona=PersonasSerializer(read_only=True)
    class Meta:
        model=Bodegas
        fields=('__all__')
        
class SerializerMagnitudes(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=Magnitudes.objects.all())])
    class Meta:
        model=Magnitudes
        fields=('__all__')
        
class SerializerPorcentajesIVA(serializers.ModelSerializer):
    porcentaje = serializers.FloatField(validators=[UniqueValidator(queryset=PorcentajesIVA.objects.all())])
    class Meta:
        model=PorcentajesIVA
        fields=('__all__')
        extra_kwargs = {
            'registro_precargado': {'read_only': True}
        }

class SerializersUnidadesMedida(serializers.ModelSerializer):
    nombre=serializers.CharField(validators=[UniqueValidator(queryset=UnidadesMedida.objects.all())])
    abreviatura=serializers.CharField(validators=[UniqueValidator(queryset=UnidadesMedida.objects.all())])

    class Meta:
        model=UnidadesMedida
        fields=('__all__')
        extra_kwargs = {
            'precargado': {'read_only': True}
        }
        
        