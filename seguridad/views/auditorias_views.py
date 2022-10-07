from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from seguridad.models import Auditorias, Modulos
from seguridad.serializers.auditorias_serializers import AuditoriasSerializers,AuditoriasPostSerializers
from seguridad.serializers.permisos_serializers import  ModulosSerializers


@api_view(['GET'])
def consultarAuditoria(request, pk):
    auditoria = Auditorias.objects.get(id_auditoria=pk)
    if auditoria:
        auditoria_serializer = AuditoriasSerializers(auditoria)
        return Response(auditoria_serializer.data, status=status.HTTP_200_OK)
    return Response(auditoria_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def actualizarAuditoria(request, pk):
    auditoria = Auditorias.objects.get(id_auditoria=pk) 
    if auditoria:
        auditoria_serializer = AuditoriasPostSerializers(auditoria, data=request.data)
        if auditoria_serializer.is_valid():
            auditoria_serializer.save()
            return Response(auditoria_serializer.data, status=status.HTTP_200_OK)
        return Response(auditoria_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def eliminarAuditoria(request, pk):
    auditoria = Auditorias.objects.get(id_auditoria=pk)
    if auditoria:  
        auditoria.delete()  
        return Response({'message': 'eliminado correctamente'}, status=status.HTTP_200_OK)


@api_view(['GET'])  
def mostrarListaAuditoria(request):
    auditoria = Auditorias.objects.all()
    auditoria_serializers = AuditoriasSerializers(auditoria, many=True)
    return Response(auditoria_serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def enviarDatosAuditoria(request):
    auditoria_serializers = AuditoriasPostSerializers(data=request.data)
    if auditoria_serializers.is_valid():
        auditoria_serializers.save()
        return Response(auditoria_serializers.data, status=status.HTTP_200_OK)
    return Response(auditoria_serializers.errors)

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
