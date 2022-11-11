from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.utils import Util
from almacen.serializers.ccd_serializers import (
    SubseriesDocSerializer,
    CCDPostSerializer
)
from almacen.models.ccd_models import (
    CuadrosClasificacionDocumental,
    SeriesDoc,
    SubseriesDoc,
    SeriesSubseriesUnidadOrg
)

# class CrearCDD(generics.CreateAPIView):
#     serializer_class = CCDPostSerializer


