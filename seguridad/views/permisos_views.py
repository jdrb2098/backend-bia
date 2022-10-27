from calendar import c
from email import message
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.models import Permisos, PermisosModulo, PermisosModuloRol, Modulos, User, Auditorias, Roles
from rest_framework import status,viewsets,mixins
from rest_framework import status
from seguridad.serializers.permisos_serializers import PermisosSerializer, PermisosModuloSerializer, PermisosModuloPostSerializer, PermisosModuloRolPostSerializer, PermisosModuloRolSerializer, ModulosSerializers, PermisosModuloRolSerializerHyper
from rest_framework.generics import ListAPIView, CreateAPIView , RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView
from seguridad.utils import Util
import datetime

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

#====================================================>Vistas tabla PermisosModulo
# #----------------------------------------------------> Crear permisos por módulo
# class PermisosModulosViewSet(viewsets.ModelViewSet):
#     queryset = PermisosModulo.objects.all()
#     serializer_class = PermisosModuloPostSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         usuario = request.user.nombre_de_usuario
#         print(usuario)
#         user = User.objects.get(nombre_de_usuario = usuario)
#         print(user)
#         modulo = Modulos.objects.get(id_modulo = 2)
#         permiso = Permisos.objects.get(cod_permiso = 'CR')
#         direccion_ip = Util.get_client_ip(request)
#         descripcion = []
#         for i in request.data:
#                 descripcion.append( "Usuario" + ":" + usuario + ";" + "Permisos(es):" + "=>")
#             print(i)
#             descripcion.append( "Modulo" + ":" + i["id_modulo"] + ";" + "Permiso" + ":" + i["cod_permiso"] )

#         print(descripcion)
#         Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# #------------------------------------------------> Borrar un permiso de un modulo
# class DeletePermisoModulo(DestroyAPIView):
#     serializer_class = PermisosModuloPostSerializer
#     queryset = PermisosModulo.objects.all()

#     def delete(self, request, pk):

#         data = PermisosModulo.objects.get(id_permisos_modulo=pk)

#         if data:
#             data.delete()
#             usuario = request.user.id_usuario
#             user = User.objects.get(id_usuario = usuario)
#             modulo = Modulos.objects.get(id_modulo = 2)
#             permiso = Permisos.objects.get(cod_permiso = 'BO')
#             direccion_ip = Util.get_client_ip(request)
#             descripcion =   "Modulo:" + str(data.id_modulo.nombre_modulo) + ";" + "Permiso:" + str(data.cod_permiso.nombre_permiso) + "."
#             print(descripcion)
#             Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')

#             return Response({'detail':'El permiso fue eliminado del modulo'})
#         else:
#             return Response({'detail':'No existe el esa selección ingresada'})

#====================================================>Vistas tabla PermisosModuloRol
#----------------------------------------------------> Asignar un permiso de módulo a un rol
class PermisosModuloRolViewSet(viewsets.ModelViewSet):
    queryset = PermisosModuloRol.objects.all()
    serializer_class = PermisosModuloRolPostSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        usuario = request.user.nombre_de_usuario
        print(usuario)
        user = User.objects.get(nombre_de_usuario = usuario)
        print(user)
        modulo = Modulos.objects.get(id_modulo = 2)
        permiso = Permisos.objects.get(cod_permiso = 'CR')
        direccion_ip = Util.get_client_ip(request)
        currentdate = datetime.date.today()
        formatDate = currentdate.strftime("%d/%m/%y")
        descripcion = []
        cont = 0 
        for i in request.data: 
            # consulta_rol = Roles.objects.get(id_rol = i["id_rol"])
            # print(consulta_rol.nombre_rol)   
            
            # descripcion = "Sucursal:" + str(serializador.pk)+  ";" + "fecha:" + formatDate + ";" + "observaciones:Registro de otra sucursal" + ";" + "NumeroSucursal:"+ str(serializador.numero_sucursal) + "."
            
            consulta_permiso_modulo = PermisosModulo.objects.get(id_permisos_modulo = i["id_permiso_modulo"])
            consulta_rol = Roles.objects.get(id_rol = i["id_rol"])
            consulta_modulo = Modulos.objects.get(id_modulo = consulta_permiso_modulo.id_modulo.id_modulo)
            permiso = Permisos.objects.get(cod_permiso = consulta_permiso_modulo.cod_permiso.cod_permiso)
            if cont == 0:
                descripcion.append( "Permisos Modulo rol añadidos=>")
            descripcion.append( "Permiso" + ":" + str(permiso.nombre_permiso) + ";" + "Modulo" + ":" + str(consulta_modulo.nombre_modulo) + ";" + "Rol:" + str(consulta_rol.nombre_rol))

        print(descripcion)
        Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#------------------------------------------------> Borrar un permiso de un modulo rol
class DeletePermisoModuloRol(DestroyAPIView):
    serializer_class = PermisosModuloRolPostSerializer
    queryset = PermisosModuloRol.objects.all()

    def delete(self, request, pk):
        data = PermisosModuloRol.objects.get(id_permiso_modulo_rol=pk)
        if data:
            data.delete()
            usuario = request.user.id_usuario
            user = User.objects.get(id_usuario = usuario)
            modulo = Modulos.objects.get(id_modulo = 2)
            permiso = Permisos.objects.get(cod_permiso = 'BO')
            direccion_ip = Util.get_client_ip(request)
            consulta_rol = Roles.objects.get(id_rol = data.id_rol.id_rol)
            consulta_permiso_modulo = PermisosModulo.objects.get(id_permisos_modulo = data.id_permiso_modulo.id_permisos_modulo)
            consulta_modulo = Modulos.objects.get(id_modulo = consulta_permiso_modulo.id_modulo.id_modulo)
            descripcion =   "Permiso" + ":" + str(permiso.nombre_permiso) + ";" + "Modulo" + ":" + str(consulta_modulo.nombre_modulo) + ";" + "Rol:" + str(consulta_rol.nombre_rol) + "."
            print(descripcion)
            Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')

            return Response({'detail':'El permiso fue eliminado del modulo'})
        else:
            return Response({'detail':'No existe el esa selección ingresada'})


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
