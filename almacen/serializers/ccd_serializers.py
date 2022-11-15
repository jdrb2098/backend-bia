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

class CCDSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuadrosClasificacionDocumental
        fields = '__all__'

class CCDPostSerializer(serializers.ModelSerializer):
    version = serializers.CharField(validators=[UniqueValidator(queryset=CuadrosClasificacionDocumental.objects.all(), message='La versión del Cuadro de Clasificación Documental debe ser único')])
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=CuadrosClasificacionDocumental.objects.all(), message='El nombre del Cuadro de Clasificación Documental debe ser único')])
    class Meta:
        model = CuadrosClasificacionDocumental
        fields = ['id_organigrama', 'version', 'nombre', 'ruta_soporte']
        extra_kwargs = {
            'id_organigrama': {'required': True},
            'version': {'required': True},
            'nombre': {'required': True}
        }

class CCDPutSerializer(serializers.ModelSerializer):
    version = serializers.CharField(validators=[UniqueValidator(queryset=CuadrosClasificacionDocumental.objects.all(), message='La versión del Cuadro de Clasificación Documental debe ser único')])
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=CuadrosClasificacionDocumental.objects.all(), message='El nombre del Cuadro de Clasificación Documental debe ser único')])
    class Meta:
        model = CuadrosClasificacionDocumental
        fields = ['version', 'nombre', 'ruta_soporte']
        extra_kwargs = {
            'version': {'required': True},
            'nombre': {'required': True}
        }


    
class SeriesDocPostSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(validators=[UniqueValidator(queryset=SeriesDoc.objects.all(), message='La serie documental debe ser unica')])
    codigo = serializers.IntegerField(validators=[UniqueValidator(queryset=SeriesDoc.objects.all(), message='El códiggo debe de ser único')])
  
    class Meta:
        model = SeriesDoc
        fields = '__all__'

class SeriesDocSerializer(serializers.ModelSerializer):
    id_ccd = CCDSerializer(read_only=True)
    
    class Meta:
        model = SeriesDoc
        fields = '__all__'

class SeriesSubseriesUnidadOrgSerializer(serializers.ModelSerializer):
    #id_unidad_organizacional = serializers.IntegerField()
    class Meta:
        model = SeriesSubseriesUnidadOrg
        fields = '__all__'        
