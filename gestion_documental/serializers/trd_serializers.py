from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from gestion_documental.models.trd_models import (
    TipologiasDocumentales
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