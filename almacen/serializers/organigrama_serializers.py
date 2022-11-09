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
               queryset=Organigramas.objects.all(),
               fields = ['id_organigrama', 'orden_nivel']
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
               queryset=Organigramas.objects.all(),
               fields = ['id_organigrama', 'orden_nivel']
           )
        ]

class UnidadesPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadesOrganizacionales
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=UnidadesOrganizacionales.objects.all(),
                fields=['id_organigrama', 'nombre']
            )
        ]

class OrganigramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organigramas
        fields = '__all__'

class OrganigramaActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organigramas
        fields = ['actual']