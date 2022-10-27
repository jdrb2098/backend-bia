from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from seguridad.models import Roles, User,UsuariosRol, Auditorias, Permisos, Modulos
from rest_framework import status,viewsets,mixins
from seguridad.serializers.roles_serializers import RolesSerializer, UsuarioRolesSerializers
from seguridad.serializers.user_serializers import UsuarioRolesLookSerializers
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from seguridad.permissions.permissions_roles import PermisoActualizarRoles,PermisoBorrarRoles,PermisoConsultarRoles,PermisoCrearRoles
from rest_framework.response import Response    
from rest_framework.generics import ListAPIView, CreateAPIView , RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework import generics
from datetime import datetime
from seguridad.utils import Util
   
class GetRolesByUser(ListAPIView):
    serializer_class = UsuarioRolesLookSerializers
    def get_queryset(self):
        queryset = UsuariosRol.objects.all()
        query = self.request.query_params.get('keyword')
        if query == None:
            query = ''
        queryset = queryset.filter(
            Q(id_usuario = query)
        )
        return queryset
    
class GetUsersByRol(ListAPIView):
    serializer_class = UsuarioRolesLookSerializers
    def get_queryset(self):
        queryset = UsuariosRol.objects.all()
        query = self.request.query_params.get('keyword')
        if query == None:
            query = ''
        queryset = queryset.filter(
            Q(id_rol = query)
        )
        return queryset


class UserRolViewSet(viewsets.ModelViewSet):
    queryset = UsuariosRol.objects.all()
    serializer_class = UsuarioRolesSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        usuario = request.user.nombre_de_usuario
        user = User.objects.get(nombre_de_usuario = usuario)
        modulo = Modulos.objects.get(id_modulo = 5)
        permiso = Permisos.objects.get(cod_permiso = 'CR')
        direccion_ip = Util.get_client_ip(request)
        descripcion = []
        cont = 0
        for i in request.data:
            if cont == 0:
                descripcion.append( "Usuario" + ":" + usuario + ";" + "Rol:" + "=>")
            consulta_rol = Roles.objects.get(id_rol = i["id_rol"])
            print(consulta_rol.nombre_rol)
            descripcion.append( str(consulta_rol ) + ";")
            cont = cont + 1
            
        print(descripcion)
        Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')  
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GetRolById(RetrieveAPIView):
    serializer_class=RolesSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarRoles]
    queryset=Roles.objects.all()   
class GetRol(ListAPIView):
    serializer_class=RolesSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarRoles]
    queryset=Roles.objects.all()
class RegisterRol(CreateAPIView):
    serializer_class=RolesSerializer
    permission_classes = [IsAuthenticated, PermisoCrearRoles]
    queryset=Roles.objects.all()

#------------------------------------------------> Borrar un rol a un usuario
class DeleteUserRol(DestroyAPIView):
    serializer_class = UsuarioRolesSerializers
    queryset = UsuariosRol.objects.all()
    
    def delete(self, request, pk):
   
        id_usuarios_rol = UsuariosRol.objects.get(id_usuarios_rol=pk)
        
        if id_usuarios_rol:
            id_usuarios_rol.delete()
            usuario = request.user.id_usuario
            user = User.objects.get(id_usuario = usuario)
            modulo = Modulos.objects.get(id_modulo = 5)
            permiso = Permisos.objects.get(cod_permiso = 'BO')
            direccion_ip = Util.get_client_ip(request)
            descripcion =  "id_usuarios_rol:" + str(pk) + ";" + "id_Usuario:" + str(id_usuarios_rol.id_usuario.id_usuario) + ";" + "id_rol:" + str(id_usuarios_rol.id_rol.id_rol) + "."
            print(descripcion)
            Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')  
            
            return Response({'detail':'El rol fue eliminado'})
        else:
            return Response({'detail':'No existe el rol ingresado'})
            
#------------------------------------------------> Borrar un rol 
class DeleteRol(DestroyAPIView):
    serializer_class = RolesSerializer
    queryset = Roles.objects.all()
    
    def delete(self, request, pk):
        usuario_rol = UsuariosRol.objects.filter(id_rol=pk)
        
        if usuario_rol:
            return Response({'detail':'No puede eliminar el rol porque ya está asignado a un usuario'})
        else:
            rol = Roles.objects.filter(id_rol=pk)
            
            if rol:
                rol.delete()
                usuario = request.user.id_usuario
                user = User.objects.get(id_usuario = usuario)
                modulo = Modulos.objects.get(id_modulo = 5)
                permiso = Permisos.objects.get(cod_permiso = 'CR')
                direccion_ip = Util.get_client_ip(request)
                descripcion = "Borradito"
                print(rol)
                print(descripcion)
                Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "SEGU", dirip=direccion_ip, descripcion=descripcion, valores_actualizados='')  
                
                return Response({'detail':'El rol fue eliminado'})
            else:
                return Response({'detail':'No existe el rol ingresado'})
            
            
@api_view(['GET'])
def getRoles(request):
    roles = Roles.objects.all()
    serializer = RolesSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRolById(request, pk):
    rol = Roles.objects.get(id_rol=pk)
    serializer = RolesSerializer(rol, many=False)
    return Response(serializer.data)
    
@api_view(['POST'])
def registerRol(request):
    data = request.data
    try:
        rol = Roles.objects.create(
            nombre_rol = data['nombre_rol'],
            descripcion_rol = data['descripcion_rol']
        )
        
        serializer = RolesSerializer(rol, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        message = {'detail': 'An error ocurred'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


    

class UpdateRol(RetrieveUpdateAPIView):
    queryset=Roles.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarRoles]
    serializer_class=RolesSerializer

class DeleteRol(DestroyAPIView):
    serializer_class = RolesSerializer
    permission_classes = [IsAuthenticated, PermisoBorrarRoles]
    queryset = Roles.objects.all()
    
    
    def delete(self, request, pk):
        usuario_rol = UsuariosRol.objects.filter(id_rol=pk)
        
        if usuario_rol:
            return Response({'detail':'No puede eliminar el rol porque ya está asignado a un usuario'})
        else:
            rol = Roles.objects.filter(id_rol=pk)
            
            if rol:
                rol.delete()
                return Response({'detail':'El rol fue eliminado'})
            else:
                return Response({'detail':'No existe el rol ingresado'})

