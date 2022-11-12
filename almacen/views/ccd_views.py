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


class UpdateCuadroClasificacionDocumental(generics.RetrieveAPIView):
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

class CreateSubseriesDoc(generics.CreateAPIView):
    serializer_class = SubseriesDocSerializer
    queryset = SubseriesDoc.objects.all()
    
    def post(self, request, id_ccd):
        data = request.data
        subseries = SubseriesDoc.objects.filter(id_ccd=id_ccd)
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=id_ccd).first()
        if ccd:
            if not ccd.fecha_terminado:
                if data:
                    # ELIMINACION DE UNIDADES
                    subseries_eliminar = SubseriesDoc.objects.filter(id_ccd=id_ccd)
                    subseries_eliminar.delete()
                    
                    # VALIDAR QUE LOS CODIGOS SEAN UNICOS
                    codigos_list = [subserie['codigo'] for subserie in data]
                    if len(codigos_list) != len(set(codigos_list)):
                        return Response({'success':False, 'detail':'Debe validar que los códigos de las subseries sean únicos'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # VALIDAR QUE LOS NOMBRES SEAN UNICOS
                    nombres_list = [subserie['nombre'] for subserie in data]
                    if len(nombres_list) != len(set(nombres_list)):
                        return Response({'success':False, 'detail':'Debe validar que los nombres de las subseries sean únicos'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # VALIDAR QUE EL ID_CCD SEA EL MISMO
                    ccd_list = [subserie['id_ccd'] for subserie in data]
                    if len(set(ccd_list)) != 1:
                        return Response({'success':False, 'detail':'Debe validar que las subseries pertenezcan a un mismo CCD'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        ccd_existe = CuadrosClasificacionDocumental.objects.filter(id_ccd=ccd_list[0]).first()
                        if not ccd_existe:
                            return Response({'success':False, 'detail':'El CCD no existe'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # CREAR SUBSERIES
                    serializer = self.serializer_class(data=request.data, many=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    
                    return Response({'success':True, 'detail':'Se ha creado las subseries'}, status=status.HTTP_201_CREATED)
                else:
                    subseries.delete()

                    return Response({'success':False, 'detail':'Se han eliminado todas las subseries'})
            else:
                return Response({'success':False, 'detail':'El CCD ya está terminado, por lo cual no es posible realizar acciones sobre las subseries'})
        else:
            return Response({'success':False, 'detail':'El CCD no existe'})

class GetSubseries(generics.ListAPIView):
    serializer_class = SubseriesDocSerializer
    queryset = SubseriesDoc.objects.all()
    
    def get(self, request, id_ccd):
        ccd = CuadrosClasificacionDocumental.objects.filter(id_ccd=id_ccd).first()
        if ccd:
            subseries = SubseriesDoc.objects.filter(id_ccd=id_ccd)
            serializer = self.serializer_class(subseries, many=True)
            return Response({'success':True, 'detail':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False, 'detail':'Debe consultar por un CCD válido'}, status=status.HTTP_404_NOT_FOUND)