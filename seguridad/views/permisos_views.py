from email import message
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.models import Permisos, PermisosModulo, PermisosModuloRol

from django.contrib.auth.hashers import make_password
from rest_framework import status
from seguridad.serializers.permisos_serializers import PermisosSerializer, PermisosModuloSerializer, PermisosModuloRolSerializer  

 #----------------------------------------------------->Vistas tabla Permisos
@api_view(['PUT'])
def updatePermiso(request, pk):
    permiso = Permisos.objects.get(cod_permiso=pk)
    data = request.data
    permiso.nombre_permiso = data['nombre_permiso']
    permiso.save() 
    serializer = PermisosSerializer(permiso, many = False) 
    return Response(serializer.data)
        
@api_view(['GET'])
def listarPermisos(request):
    permisos = Permisos.objects.all()
    permiso_serializers = PermisosSerializer(permisos, many=True)
    return Response(permiso_serializers.data)

@api_view(['GET'])
def verPermiso(request,pk):
    permiso = Permisos.objects.get(cod_permiso=pk)
    permiso_serializer = PermisosSerializer(permiso)
    return Response(permiso_serializer.data)
 

@api_view(['POST'])
def insertarPermiso(request):
    data = request.data
    try:
       permiso = Permisos.objects.create(nombre_permiso = data['nombre_permiso']) 
       serializer = PermisosSerializer(permiso, many=False)
       return Response(serializer.data)
    except:
        message = {'Error' : 'No se pudo crear permiso'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def deletePermiso(request,pk):
    permiso = Permisos.objects.get(cod_permiso=pk)
    permiso.delete()
    return Response('Eliminado correctamente')
        

#----------------------------------------------------->Vistas tabla PermisosModulo
