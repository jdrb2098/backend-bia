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


class SerializersPostMarca(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=Marcas.objects.all())])
    class Meta:
        model=Marcas
        fields=['nombre']
        extra_kwargs = {
            'nombre': {'required': True}, 
        }

class SerializersPutMarca(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=Marcas.objects.all())])
    class Meta:
        model=Marcas
        fields=['nombre', 'activo']
        extra_kwargs = {
            'nombre': {'required': True}, 
        }
        

class SerializersEstadosArticulo(serializers.ModelSerializer):
    class Meta:
        model=EstadosArticulo
        fields=('__all__')
        
class SerializerBodegas(serializers.ModelSerializer):
    id_responsable=PersonasSerializer(read_only=True)
    class Meta:
        model=Bodegas
        fields='__all__'

class SerializerPostBodegas(serializers.ModelSerializer):
    class Meta:
        model=Bodegas
        fields=['nombre', 'cod_municipio', 'direccion', 'id_responsable', 'es_principal']
        extra_kwargs = {
            'nombre': {'required': True},
            'id_responsable': {'required': True}
        }

class SerializerPutBodegas(serializers.ModelSerializer):
    class Meta:
        model=Bodegas
        fields=['nombre', 'cod_municipio', 'direccion', 'id_responsable', 'es_principal', 'activo']
        extra_kwargs = {
            'nombre': {'required': True},
            'id_responsable': {'required': True}
        }
        
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


class SerializerPostPorcentajesIVA(serializers.ModelSerializer):
    porcentaje = serializers.FloatField(validators=[UniqueValidator(queryset=PorcentajesIVA.objects.all())])
    class Meta:
        model=PorcentajesIVA
        fields=['porcentaje', 'observacion']
        extra_kwargs = {
            'porcentaje': {'required': True},
            'observacion': {'required': True}
        }


class SerializerPutPorcentajesIVA(serializers.ModelSerializer):
    porcentaje = serializers.FloatField(validators=[UniqueValidator(queryset=PorcentajesIVA.objects.all())])
    class Meta:
        model=PorcentajesIVA
        fields=['porcentaje', 'observacion', 'activo']
        extra_kwargs = {
            'porcentaje': {'required': True},
            'observacion': {'required': True},
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

class SerializersPostUnidadesMedida(serializers.ModelSerializer):
    nombre=serializers.CharField(validators=[UniqueValidator(queryset=UnidadesMedida.objects.all())])
    abreviatura=serializers.CharField(validators=[UniqueValidator(queryset=UnidadesMedida.objects.all())])

    class Meta:
        model=UnidadesMedida
        fields=['nombre', 'abreviatura', 'id_magnitud']
        extra_kwargs = {
            'nombre': {'required': True},
            'abreviatura': {'required': True},
            'id_magnitud': {'required': True}
        }


class SerializersPutUnidadesMedida(serializers.ModelSerializer):
    nombre=serializers.CharField(validators=[UniqueValidator(queryset=UnidadesMedida.objects.all())])
    abreviatura=serializers.CharField(validators=[UniqueValidator(queryset=UnidadesMedida.objects.all())])

    class Meta:
        model=UnidadesMedida
        fields=['nombre', 'abreviatura', 'id_magnitud', 'activo']
        extra_kwargs = {
            'nombre': {'required': True},
            'abreviatura': {'required': True},
            'id_magnitud': {'required': True}
        }
        
        