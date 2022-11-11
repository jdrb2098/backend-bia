from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.utils import Util
from almacen.serializers.ccd_serializers import (
    SubseriesDocSerializer,
    CCDPostSerializer,
    CCDSerializer
)
from almacen.models.ccd_models import (
    CuadrosClasificacionDocumental,
    SeriesDoc,
    SubseriesDoc,
    SeriesSubseriesUnidadOrg
)

class CreateCuadroClasificacionDocumental(generics.CreateAPIView):
    serializer_class = CCDPostSerializer
    queryset = CuadrosClasificacionDocumental.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'detail': 'Cuadro de Clasificación Documental creado exitosamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCuadroClasificacionDocumental(generics.ListAPIView):
    serializer_class = CCDSerializer  
    queryset = CuadrosClasificacionDocumental.objects.all()

    def get(self, request):
        consulta = request.query_params.get('pk')
        if consulta == None:
            ccds = CuadrosClasificacionDocumental.objects.all().values()
            if len(ccds) == 0:
                return Response({'Error' : 'Aún no hay Cuadros de Clasificación Documental registrados'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'cuadros de Clasificación Documental': ccds}, status=status.HTTP_200_OK) 
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=consulta).values()
        if len(ccd) == 0:
            return Response({'Error' : 'No se encontró el Cuadro de Clasificación Documental ingresado'}, status=status.HTTP_404_NOT_FOUND)
        series = SeriesDoc.objects.filter(id_ccd=int(consulta)).values()
        subseries = 'No hay ubseries '
        if len(series) == 0:
            series = 'No hay series registradas'
            subseries = 'No hay subseries registradas'
            datos_finales = {'Cuadro de Clasificación Documental' : ccd, 'Series' : series, 'Subseries' : subseries}
            return Response({'Cuadro de Clasificación Documental' : datos_finales}, status=status.HTTP_200_OK)
        subseries = SubseriesDoc.objects.filter(id_ccd=int(consulta)).values()
        if len(subseries) == 0:
            subseries = 'No hay subseries registradas'
            datos_finales = {'Cuadro de Clasificación Documental' : ccd, 'Series' : series, 'Subseries' : subseries}
            return Response({'Cuadro de Clasificación Documental' : datos_finales}, status=status.HTTP_200_OK)
        datos_finales = {'Cuadro de Clasificación Documental' : ccd, 'series' : series, 'Subseries' : subseries}
        return Response({'Cuadro de Clasificación Documental' : datos_finales}, status=status.HTTP_200_OK)


