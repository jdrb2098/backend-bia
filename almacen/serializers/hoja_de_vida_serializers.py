from almacen.models.generics_models import UnidadesMedida
from seguridad.serializers.personas_serializers import PersonasSerializer
from almacen.models.generics_models import Magnitudes
from rest_framework import serializers
from almacen.models.articulos_models import Articulos
from almacen.models.hoja_de_vida_models import HojaDeVidaComputadores, HojaDeVidaOtrosctivos, HojaDeVidaVehiculos, DocumentosVehiculo
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class SerializersHojaDeVidaVehiculos(serializers.ModelSerializer):
    class Meta:
        model=HojaDeVidaVehiculos
        fields=('__all__')