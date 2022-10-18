from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from seguridad.renderers.user_renderers import UserRender
from seguridad.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.sites.shortcuts import get_current_site
from seguridad.serializers.personas_serializers import PersonasSerializer
from seguridad.utils import Util
from django.contrib.auth.hashers import make_password
from rest_framework import status
import jwt
from django.conf import settings
from seguridad.serializers.user_serializers import EmailVerificationSerializer, ResetPasswordEmailRequestSerializer, UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterSerializer  ,LoginSerializer

from rest_framework.generics import RetrieveUpdateAPIView

from django.contrib.auth.hashers import make_password
from rest_framework import status
from seguridad.serializers.user_serializers import EmailVerificationSerializer ,UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterSerializer,LoginErroneoPostSerializers,LoginErroneoSerializers,LoginSerializers,LoginPostSerializers
from django.template.loader import render_to_string

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

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserByPersonDocument(request, pk):
    try:
        personas = Personas.objects.get(numero_documento=pk)
        if personas:
            try:
                user = User.objects.get(persona=personas.id_persona)
                serializer = UserSerializer(user, many=False)
                return Response(serializer.data)
            except:
                personas_serializer = PersonasSerializer(personas, many=False)
                return Response([personas_serializer.data, {'message': 'No existe ningún usuario asociado a esta persona', 'persona': True}])
    except:
        return Response({'message':'La persona asociada a este numero de documento no existe dentro del sistema','persona': False})


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

"""@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserAdmin(request, pk):
    user = User.objects.get(id_usuario=pk)

    data = request.data

    user.nombre_de_usuario= data['email']
    user.email = data['email']
    user.is_blocked = data['is_blocked']
    

    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)"""


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id_usuario=pk)
    userForDeletion.delete()
    return Response('User was deleted')


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        
        current_site=get_current_site(request).domain

        persona = Personas.objects.get(id_persona = request.data['persona'])

        relativeLink= reverse('verify')
        absurl= 'http://'+ current_site + relativeLink + "?token="+ str(token)
        sms = 'Hola '+ user.persona.primer_nombre + ' ' + user.persona.primer_apellido + ' utiliza el siguiente link para verificar tu usuario \n' + absurl
        context = {'primer_nombre': user.persona.primer_nombre, 'primer_apellido':  user.persona.primer_apellido, 'absurl': absurl}
        template = render_to_string(('email-verification.html'), context)
        data = {'template': template, 'email_subject': 'Verifica tu usuario', 'to_email': user.email}
        Util.send_email(data)
        Util.send_sms(persona.telefono_celular, sms)

        
        return Response(user_data, status=status.HTTP_201_CREATED)

class Verify(views.APIView):

    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id_usuario=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                context = {'primer_nombre': user.persona.primer_nombre, 'primer_apellido':  user.persona.primer_apellido}
                template = render_to_string(('email-verified.html'), context)
                data = {'template': template, 'email_subject': 'Verificación Exitosa', 'to_email': user.email}
                Util.send_email(data)
            return Response({'email': 'succesfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
 

class LoginUpdateApiViews(RetrieveUpdateAPIView):
    serializer_class=LoginPostSerializers
    queryset = Login.objects.all()
    
class LoginDestroyApiViews(generics.DestroyAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()
    
class LoginConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()

class LoginListApiViews(generics.ListAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()

class LoginRegisterApiViews(generics.CreateAPIView):
    queryset = Login.objects.all()
    serializer_class = LoginPostSerializers

#__________________LoginErroneo

class LoginErroneoUpdateApiViews(RetrieveUpdateAPIView):
    serializer_class=LoginErroneoPostSerializers
    queryset = LoginErroneo.objects.all()
    
class LoginErroneoDestroyApiViews(generics.DestroyAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()
    
class LoginErroneoConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()

class LoginErroneoListApiViews(generics.ListAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()

class LoginErroneoRegisterApiViews(generics.CreateAPIView):
    queryset = LoginErroneo.objects.all()
    serializer_class = LoginErroneoPostSerializers

class LoginApiView(generics.CreateAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        user = request.data
        exist = User.objects.filter(email=user['email']).first()
        try:
            if exist:
                login_exist = LoginErroneo.objects.filter(id_usuario=exist.id_usuario).first()
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                
                login = Login.objects.create(
                    id_usuario = exist,
                    dirip = 'test',
                    dispositivo_conexion = 'test'
                )
                
                LoginPostSerializers(login, many=False)
                
                if login_exist:
                    login_exist.contador = 0
                    login_exist.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response({'detail':'No existe el correo ingresado'})
        except:
            login_exist = LoginErroneo.objects.filter(id_usuario=exist.id_usuario).first()
            if login_exist:
                if login_exist.contador < 3:
                    login_exist.contador += 1
                    login_exist.save()
                    if login_exist.contador == 3:
                        exist.is_blocked = True
                        exist.save()
                        return Response({'detail':'Su usuario ha sido bloqueado'})
                    serializer = LoginErroneoPostSerializers(login_exist, many=False)
                    return Response({'detail':'La contraseña es invalida', 'login_erroneo': serializer.data})
                else:
                    return Response({'detail':'Su usuario está bloqueado, debe comunicarse con el administrador'})
            else:
                if exist.is_blocked:
                    return Response({'detail':'Su usuario está bloqueado, debe comunicarse con el administrador'})
                else:
                    login_error = LoginErroneo.objects.create(
                        id_usuario = exist,
                        dirip = 'test',
                        dispositivo_conexion = 'test',
                        contador = 1
                    )
                serializer = LoginErroneoPostSerializers(login_error, many=False)
                return Response({'detail':'La contraseña es invalida', 'login_erroneo': serializer.data})

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self,request):
        data = {'request': request,'data':request.data}
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response( {'success': 'te enviamos el link  para poder actualizar tu contraseña'},status=status.HTTP_200_OK)

class PasswordTokenCheckApi(generics.GenericAPIView):

    def get(self,request,uid64,token):
        pass