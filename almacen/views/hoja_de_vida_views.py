from almacen.models.generics_models import Bodegas
from rest_framework import generics
from rest_framework.views import APIView
from almacen.serializers.hoja_de_vida_serializers import (
    SerializersHojaDeVidaComputadores, SerializersHojaDeVidaVehiculos, SerializersHojaDeVidaOtrosctivos
    )   
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class DeleteHojaDeVidaComputadores(generics.DestroyAPIView):
    serializer_class=SerializersHojaDeVidaComputadores
    queryset=Marcas.objects.all()