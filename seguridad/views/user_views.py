from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from django.contrib.auth.hashers import make_password
from rest_framework import status
from seguridad.serializers.user_serializers import UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterSerializer  

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            nombre_de_usuario=data['nombre_de_usuario'],
            email=data['email'],
            password=make_password(data['password']),
            persona =data['persona'],
            id_usuario_creador = data['id_usuario_creador'],
            activated_at = data['activated_at'],
            tipo_usuario = data['tipo_usuario'] 
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'error'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.nombre_de_usuario = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)


@api_view(['GET'])
def roles(request):
    roles = UsuariosRol.objects.all()
    serializers = UserRolesSerializer(roles, many=True)
    return Response(serializers.data)

class GetUserRoles(generics.ListAPIView):
    queryset = UsuariosRol.objects.all()
    serializer_class = UserRolesSerializer

class DeleteUserRoles(generics.DestroyAPIView):
    queryset = UsuariosRol.objects.all()
    serializer_class = UserRolesSerializer

class UpdateUserRoles(generics.RetrieveUpdateAPIView):
    queryset = UsuariosRol.objects.all()
    serializer_class = UserRolesSerializer

class RegisterUserRoles(generics.CreateAPIView):
    queryset = UsuariosRol.objects.all()
    serializer_class = UserRolesSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id_usuario=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = User.objects.get(id_usuario=pk)

    data = request.data

    user.nombre_de_usuario= data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id_usuario=pk)
    userForDeletion.delete()
    return Response('User was deleted')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer