from almacen.models.generics_models import UnidadesMedida
from seguridad.serializers.personas_serializers import PersonasSerializer
from almacen.models.generics_models import Magnitudes
from rest_framework import serializers
from almacen.models.generics_models import Marcas, EstadosArticulo,Bodegas,PorcentajesIVA
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator