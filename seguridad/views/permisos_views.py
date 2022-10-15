from calendar import c
from email import message
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.models import Permisos, PermisosModulo, PermisosModuloRol, Modulos

from rest_framework import status
from seguridad.serializers.permisos_serializers import PermisosSerializer, PermisosModuloSerializer, PermisosModuloPostSerializer, PermisosModuloRolPostSerializer, PermisosModuloRolSerializer, ModulosSerializers, PermisosModuloRolSerializerHyper
from rest_framework.generics import ListAPIView, CreateAPIView , RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView

 #----------------------------------------------------->Vistas tabla Permisos
class InsertarPermiso(CreateAPIView):
    serializer_class = PermisosSerializer

class UpdatePermiso(RetrieveUpdateAPIView):
    serializer_class = PermisosSerializer
    queryset = Permisos.objects.all()
           
class ListarPermisos(ListAPIView):
    serializer_class = PermisosSerializer
    def get_queryset(self):
        return Permisos.objects.all()
    
class DetailPermisos(RetrieveAPIView):
    serializer_class = PermisosSerializer
    queryset = Permisos.objects.filter()

class DeletePermiso(DestroyAPIView):
    serializer_class = PermisosSerializer
    queryset = Permisos.objects.all()

#----------------------------------------------------->Vistas tabla PermisosModulo
"""class InsertarPermisosModulo(CreateAPIView):
    serializer_class = PermisosModuloPostSerializer

class UpdatePermisoModulo(RetrieveUpdateAPIView):
    serializer_class = PermisosModuloPostSerializer
    queryset = PermisosModulo.objects.all()
           
class ListarPermisosModulo(ListAPIView):
    serializer_class = PermisosModuloSerializer
    def get_queryset(self):
        return PermisosModulo.objects.all()
    
class DetailPermisosModulo(RetrieveAPIView):
    serializer_class = PermisosModuloSerializer
    queryset = PermisosModulo.objects.filter()

class DeletePermisosModulo(DestroyAPIView):
    serializer_class = PermisosModuloPostSerializer
    queryset = PermisosModulo.objects.all()
    

#----------------------------------------------------->Vistas tabla PermisosModuloRol
class InsertarPermisosModuloRol(CreateAPIView):
    serializer_class = PermisosModuloRolPostSerializer

class UpdatePermisoModuloRol(RetrieveUpdateAPIView):
    serializer_class = PermisosModuloRolPostSerializer
    queryset = PermisosModuloRol.objects.all()
           
class ListarPermisosModuloRol(ListAPIView):
    serializer_class = PermisosModuloRolSerializer
    def get_queryset(self):
        return PermisosModuloRol.objects.all()
    
class DetailPermisosModuloRol(RetrieveAPIView):
    serializer_class = PermisosModuloRolSerializer
    queryset = PermisosModuloRol.objects.filter()

class DeletePermisosModuloRol(DestroyAPIView):
    serializer_class = PermisosModuloRolPostSerializer
    queryset = PermisosModuloRol.objects.all()"""
    
#----------------------------------------------------->Tabla Modulos

class InsertarModulo(CreateAPIView):
    serializer_class = ModulosSerializers

class UpdateModulo(RetrieveUpdateAPIView):
    serializer_class = ModulosSerializers
    queryset = Modulos.objects.all()
           
class ListarModulo(ListAPIView):
    serializer_class = ModulosSerializers
    def get_queryset(self):
        return Modulos.objects.all()
    
class DetailModulo(RetrieveAPIView):
    serializer_class = ModulosSerializers
    queryset = Modulos.objects.filter()

class DeleteModulo(DestroyAPIView):
    serializer_class = ModulosSerializers
    queryset = Modulos.objects.all()
