from email import message
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.models import Permisos, PermisosModulo, PermisosModuloRol

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
       permiso = Permisos.objects.create(cod_permiso = data['cod_permiso'], nombre_permiso = data['nombre_permiso']) 
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
@api_view(['GET'])
def listarPermisosModulo(request):
    permisos_modulo = PermisosModulo.objects.all()
    permisos_moodulo_serializer = PermisosModuloSerializer(permisos_modulo, many = True)
    return Response(permisos_moodulo_serializer.data)

@api_view(['GET'])
def verPermisosModulo(request, pk ):
    permiso_modulo = PermisosModulo.objects.get(cod_permiso = pk)
    permisos_modulo_serilizer = PermisosModuloSerializer(permiso_modulo)
    return Response(permisos_modulo_serilizer.data)

@api_view(['DELETE'])
def deletePermisosModulo(request,pk):
    permiso_modulo = PermisosModulo.objects.get(cod_permiso=pk)
    permiso_modulo.delete()
    return Response('Eliminado correctamente')

@api_view(['POST'])
def insertarPermisosModulo(request):
    data = request.data
    try: 
        permisos_modulo = PermisosModulo.objects.create(id_modulo = data['id_modulo'], cod_permiso = data['cod_permiso'])
        serializer = PermisosModuloSerializer(permisos_modulo, many=False)
        return Response(serializer.data)
    except:
        message = {'Error' : 'No se pudo crear permiso modulo'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    
#----------------------------------------------------->Vistas tabla PermisosModuloRol
@api_view(['GET'])
def listarPermisosModuloRol(request):
    permisos_modulo_rol = PermisosModuloRol.objects.all()
    permisos_moodulo_rol_serializer = PermisosModuloRolSerializer(permisos_modulo_rol, many = True)
    return Response(permisos_moodulo_rol_serializer.data)

@api_view(['GET'])
def verPermisosModuloRol(request, pk ):
    permiso_modulo_rol = PermisosModuloRol.objects.get(id_rol = pk)
    permisos_modulo_rol_serilizer = PermisosModuloRolSerializer(permiso_modulo_rol)
    return Response(permisos_modulo_rol_serilizer.data)

@api_view(['DELETE'])
def deletePermisosModuloRol(request,pk):
    permiso_modulo_rol = PermisosModuloRol.objects.get(id_rol=pk)
    permiso_modulo_rol.delete()
    return Response('Eliminado correctamente')

@api_view(['POST'])
def insertarPermisosModuloRol(request):
    data = request.data
    try: 
        permisos_modulo = PermisosModuloRol.objects.create(id_rol = data['id_rol'], id_modulo = data['id_modulo'], cod_permiso = data['cod_permiso'])
        serializer = PermisosModuloRolSerializer(permisos_modulo, many=False)
        return Response(serializer.data)
    except:
        message = {'Error' : 'No se pudo crear permiso modulo'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)