from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from almacen.models.organigrama_models import (
    Organigramas,
    NivelesOrganigrama,
    UnidadesOrganizacionales,
    Cargos
)

class NivelesPostSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=50, min_length=2, validators=[UniqueValidator(queryset=NivelesOrganigrama.objects.all())])
    orden_nivel = serializers.IntegerField(validators=[UniqueValidator(queryset=NivelesOrganigrama.objects.all())])

    class Meta:
        model = NivelesOrganigrama
        fields = [
            'id_organigrama',
            'orden_nivel',
            'nombre'
        ]
        validators = [
           UniqueTogetherValidator(
               queryset=NivelesOrganigrama.objects.all(),
               fields = ['id_organigrama', 'orden_nivel']
           )
        ]
        validators = [
           UniqueTogetherValidator(
               queryset=NivelesOrganigrama.objects.all(),
               fields = ['id_organigrama', 'nombre']
           )
        ]


class NivelesUpdateSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=50, min_length=2, validators=[UniqueValidator(queryset=NivelesOrganigrama.objects.all())])
    orden_nivel = serializers.IntegerField(validators=[UniqueValidator(queryset=NivelesOrganigrama.objects.all())])

    class Meta:
        model = NivelesOrganigrama
        fields = '__all__'
        validators = [
           UniqueTogetherValidator(
               queryset=NivelesOrganigrama.objects.all(),
               fields = ['id_organigrama', 'orden_nivel']
           )
        ]
        validators = [
           UniqueTogetherValidator(
               queryset=NivelesOrganigrama.objects.all(),
               fields = ['id_organigrama', 'nombre']
           )
        ]

class UnidadesPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadesOrganizacionales
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=UnidadesOrganizacionales.objects.all(),
                fields=['id_organigrama', 'codigo'],
                message='El id organigrama y el código deben ser una pareja única'
            ),
            UniqueTogetherValidator(
                queryset=UnidadesOrganizacionales.objects.all(),
                fields=['id_organigrama', 'nombre'],
                message='El id organigrama y el nombre deben ser una pareja única'
            )
        ]
        extra_kwargs = {"cod_tipo_unidad": {"error_messages": {"required": "El campo de cod_tipo_unidad es requerido"}}}    

class OrganigramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organigramas
        fields = ['nombre','fecha_terminado','descripcion', 'fecha_puesta_produccion','fecha_retiro_produccion','justificacion_nueva_version','version','ruta_resolucion']
        read_only_fields = ['actual']

class OrganigramaActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organigramas
        fields = ['actual']