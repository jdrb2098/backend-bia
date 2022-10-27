from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from seguridad.models import Roles, User,UsuariosRol
from rest_framework import status,viewsets,mixins
from seguridad.serializers.roles_serializers import RolesSerializer, UsuarioRolesSerializers
from seguridad.serializers.user_serializers import UsuarioRolesLookSerializers
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from seguridad.permissions.permissions_roles import PermisoActualizarRoles,PermisoBorrarRoles,PermisoConsultarRoles,PermisoCrearRoles
from rest_framework.response import Response    
from rest_framework.generics import ListAPIView, CreateAPIView , RetrieveAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView


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
    #I took the liberty to change the model to queryset
    queryset = UsuariosRol.objects.all()
    serializer_class = UsuarioRolesSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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