from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from almacen.models.ccd_models import (
    CuadrosClasificacionDocumental,
    SeriesDoc,
    SubseriesDoc,
    SeriesSubseriesUnidadOrg
)

class SubseriesDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubseriesDoc
        fields = '__all__'
        validators = [
           UniqueTogetherValidator(
               queryset=SubseriesDoc.objects.all(),
               fields = ['id_ccd', 'codigo'],
               message='El id_ccd y el codigo deben ser una pareja única'
           ),
           UniqueTogetherValidator(
               queryset=SubseriesDoc.objects.all(),
               fields = ['id_ccd', 'nombre'],
               message='El id_ccd y nombre deben ser una pareja única'
           )
        ]


class CCDPostSerializer(serializers.ModelSerializer):
    version = serializers.CharField(validator=[UniqueValidator(queryset=CuadrosClasificacionDocumental.objects.all(), message='La versión del Cuadro de Clasificación Documental debe ser único')])
    nombre = serializers.CharField(validator=[UniqueValidator(queryset=CuadrosClasificacionDocumental.objects.all(), message='El nombre del Cuadro de Clasificación Documental debe ser único')])
    class Meta:
        model = CuadrosClasificacionDocumental
        fields = ['id_organigrama', 'version', 'nombre', 'ruta_soporte']