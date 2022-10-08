from sre_parse import State
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView
from seguridad.models import Auditorias, Modulos
from seguridad.serializers.auditorias_serializers import AuditoriasSerializers,AuditoriasPostSerializers
from seguridad.serializers.permisos_serializers import  ModulosSerializers


class UpdateApiViews(RetrieveUpdateAPIView):
    serializer_class=AuditoriasPostSerializers
    queryset = Auditorias.objects.all()
    
class DestroyApiViews(generics.DestroyAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()
    
class ConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()

class ListApiViews(generics.ListAPIView):
    serializer_class=AuditoriasSerializers
    queryset = Auditorias.objects.all()

class RegisterApiViews(generics.CreateAPIView):
    queryset = Auditorias.objects.all()
    serializer_class = AuditoriasPostSerializers
    
##___________________________________________________________________________##


@api_view(['GET'])
def consultarModulos(request, pk):
    modulo = Modulos.objects.get(id_modulo=pk)
    if modulo:
        modulo_serializer = ModulosSerializers(modulo)
        return Response(modulo_serializer.data, status=status.HTTP_200_OK)
    return Response(modulo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def actualizarModulo(request, pk):
    modulo = Modulos.objects.get(id_modulo=pk) 
    if modulo:
        modulo_serializer = ModulosSerializers(modulo, data=request.data)
        if modulo_serializer.is_valid():
            modulo_serializer.save()
            return Response(modulo_serializer.data, status=status.HTTP_200_OK)
        return Response(modulo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminarModulo(request, pk):
    modulo = Modulos.objects.get(id_modulo=pk) 
    if modulo: 
        modulo.delete()  
        return Response({'message': 'eliminado correctamente'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def mostrarListaModulo(request):
    modulo = Modulos.objects.all()
    modulo_serializers = ModulosSerializers(modulo, many=True)
    return Response(modulo_serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def enviarDatosModulo(request):
    modulo_serializers = ModulosSerializers(data=request.data)
    if modulo_serializers.is_valid():
        modulo_serializers.save()
        return Response(modulo_serializers.data, status=status.HTTP_200_OK)
    return Response(modulo_serializers.errors)


