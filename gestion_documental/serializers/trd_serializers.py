from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from gestion_documental.models.trd_models import (
    TipologiasDocumentales,
    TablaRetencionDocumental
)

class TipologiasDocumentalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipologiasDocumentales
        fields = '__all__'
        validators = [
           UniqueTogetherValidator(
               queryset=TipologiasDocumentales.objects.all(),
               fields = ['id_trd', 'codigo'],
               message='El id_ccd y el codigo deben ser una pareja única'
           ),
           UniqueTogetherValidator(
               queryset=TipologiasDocumentales.objects.all(),
               fields = ['id_trd', 'nombre'],
               message='El id_ccd y nombre deben ser una pareja única'
           )
        ]


class TRDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TablaRetencionDocumental
        fields = '__all__'

class TRDPostSerializer(serializers.ModelSerializer):
    version = serializers.CharField(validators=[UniqueValidator(queryset=TablaRetencionDocumental.objects.all(), message='La versión de la Tabla de Retención Documental debe ser único')])
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=TablaRetencionDocumental.objects.all(), message='El nombre de la Tabla de Retención Documental debe ser único')])

    class Meta:
        model = TablaRetencionDocumental
        fields = [ 'id_ccd', 'version', 'nombre', 'ruta_soporte']
        extra_kwargs = {
            'id_ccd': {'required': True},
            'version': {'required': True},
            'nombre': {'required': True}
        }


class TRDPutSerializer(serializers.ModelSerializer):
    version = serializers.CharField(validators=[UniqueValidator(queryset=TablaRetencionDocumental.objects.all(), message='La versión de la Tabla de Retención Documental debe ser único')])
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=TablaRetencionDocumental.objects.all(), message='El nombre de la Tabla de Retención Documental debe ser único')])

    class Meta:
        model = TablaRetencionDocumental
        fields = ['version', 'nombre', 'ruta_soporte']
        extra_kwargs = {
            'version': {'required': True},
            'nombre': {'required': True}
        }


class TRDFinalizarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TablaRetencionDocumental
        fields = ['fecha_terminado']
        extra_kwargs = {
            'fecha_terminado': {'read_only': True}
        }
            