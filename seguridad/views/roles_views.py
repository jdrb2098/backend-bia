from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from seguridad.models import Roles, User,UsuariosRol
from rest_framework import status,viewsets,mixins
from seguridad.serializers.roles_serializers import RolesSerializer, UsuarioRolesSerializers

from rest_framework.response import Response    


class UserRolViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin):

    #I took the liberty to change the model to queryset
    queryset = UsuariosRol.objects.all()
    serializer_class = UsuarioRolesSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

@api_view(['PUT'])
def updateRol(request, pk):
    rol = Roles.objects.get(id_rol=pk)
    
    data = request.data
    try:
        if (data['nombre_rol']) and (data['nombre_rol'] != ''):
            rol.nombre_rol = data['nombre_rol']
            
        if (data['descripcion_rol']) and (data['descripcion_rol'] != ''):
            rol.descripcion_rol = data['descripcion_rol']
            
        rol.save()
        
        serializer = RolesSerializer(rol, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'An error ocurred'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([AllowAny])
def deleteRol(request, pk):
    rolForDeletion = Roles.objects.get(id_rol=pk)
    rolForDeletion.delete()
    message = {'detail': "Rol was deleted"}
    return Response(message, status=status.HTTP_200_OK)