from base64 import urlsafe_b64decode, urlsafe_b64encode
from email import message
from seguridad.serializers.roles_serializers import UsuarioRolesSerializers
from django.core import signing
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from seguridad.permissions.permissions_user import PermisoCrearUsuarios, PermisoActualizarUsuarios, PermisoActualizarInterno, PermisoActualizarExterno
from rest_framework.response import Response
from seguridad.renderers.user_renderers import UserRender
from seguridad.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from seguridad.serializers.personas_serializers import PersonasSerializer
from seguridad.utils import Util
from django.contrib.auth.hashers import make_password
from rest_framework import status
import jwt
from django.conf import settings
from seguridad.serializers.user_serializers import EmailVerificationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, UserPutAdminSerializer, UserPutSerializerExterno, UserPutSerializerInterno, UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterSerializer  ,LoginSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from seguridad.serializers.user_serializers import EmailVerificationSerializer ,UserSerializer, UserSerializerWithToken, UserRolesSerializer, RegisterSerializer, RegisterExternoSerializer, LoginErroneoPostSerializers,LoginErroneoSerializers,LoginSerializers,LoginPostSerializers
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import encoding, http
import datetime, copy

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


class UpdateUserProfileInterno(generics.RetrieveUpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = UserPutSerializerInterno
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarInterno]

    def patch(self, request):
        user_loggedin = self.request.user.id_usuario
        user = User.objects.filter(id_usuario = user_loggedin).first()
        previous_user = copy.copy(user)
        if user:
            user_serializer = self.serializer_class(user, data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            # AUDITORIA AL ACTUALIZAR USUARIO PROPIO

            dirip = Util.get_client_ip(request)
            descripcion = {'nombre_de_usuario': user.nombre_de_usuario}
            valores_actualizados = {'current': user, 'previous': previous_user}

            auditoria_data = {
                'id_usuario': user_loggedin,
                'id_modulo': 3,
                'cod_permiso': 'AC',
                'subsistema': 'SEGU',
                'dirip': dirip,
                'descripcion': descripcion,
                'valores_actualizados': valores_actualizados
            }

            Util.save_auditoria(auditoria_data)

            return Response({'success': True,'data': user_serializer.data})


class UpdateUserProfileExterno(generics.RetrieveUpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = UserPutSerializerExterno
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarExterno]

    def patch(self, request):
        user_loggedin = self.request.user.id_usuario
        user = User.objects.filter(id_usuario = user_loggedin).first()
        previous_user = copy.copy(user)
        if user:
            user_serializer = self.serializer_class(user, data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            # AUDITORIA AL ACTUALIZAR USUARIO PROPIO

            dirip = Util.get_client_ip(request)
            descripcion = {'nombre_de_usuario': user.nombre_de_usuario}
            valores_actualizados = {'current': user, 'previous': previous_user}

            auditoria_data = {
                'id_usuario': user_loggedin,
                'id_modulo': 4,
                'cod_permiso': 'AC',
                'subsistema': 'SEGU',
                'dirip': dirip,
                'descripcion': descripcion,
                'valores_actualizados': valores_actualizados
            }

            Util.save_auditoria(auditoria_data)

            return Response({'success': True,'data': user_serializer.data})


class UpdateUser(generics.RetrieveUpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = UserPutAdminSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarUsuarios]

    def patch(self, request, pk):
        user_loggedin = request.user.id_usuario
        if int(user_loggedin) != int(pk):
            user = User.objects.filter(id_usuario = pk).first()
            previous_user = copy.copy(user)
            if user:
                user_serializer = self.serializer_class(user, data=request.data)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
                
                roles = user_serializer.validated_data.get("roles")
                roles_actuales = UsuariosRol.objects.filter(id_usuario=pk).values('id_rol')
                roles_previous = copy.copy(roles_actuales)
                
                roles_asignados = {}
                
                # ASIGNAR ROLES NUEVOS A USUARIO
                for rol in roles:
                    rol_existe = UsuariosRol.objects.filter(id_usuario=pk, id_rol=rol["id_rol"])
                    if not rol_existe:
                        rol_instance = Roles.objects.filter(id_rol=rol["id_rol"]).first()
                        roles_asignados["nombre_rol_"+str(rol_instance.id_rol)] = rol_instance.nombre_rol
                        UsuariosRol.objects.create(
                            id_usuario = user,
                            id_rol = rol_instance
                        )
                
                # ELIMINAR ROLES A USUARIO
                
                roles_eliminados = {}
                
                roles_list = [rol['id_rol'] for rol in roles]
                
                roles_eliminar = UsuariosRol.objects.filter(id_usuario=pk).exclude(id_rol__in=roles_list)
                
                for rol in roles_eliminar:
                    roles_eliminados["nombre_rol_"+str(rol.id_rol.id_rol)] = rol.id_rol.nombre_rol
                
                roles_eliminar.delete()
                
                # AUDITORIA AL ACTUALIZAR USUARIO

                dirip = Util.get_client_ip(request)
                descripcion = {'nombre_de_usuario': user.nombre_de_usuario}
                valores_actualizados = {'current': user, 'previous': previous_user}
                
                auditoria_user = {
                    'id_usuario': user_loggedin,
                    'id_modulo': 2,
                    'cod_permiso': 'AC',
                    'subsistema': 'SEGU',
                    'dirip': dirip,
                    'descripcion': descripcion,
                    'valores_actualizados': valores_actualizados
                }
                
                Util.save_auditoria(auditoria_user)
                
                # AUDITORIA AL ACTUALIZAR ROLES
                
                usuario = User.objects.get(id_usuario=user_loggedin)
                modulo = Modulos.objects.get(id_modulo = 5)
                permiso = Permisos.objects.get(cod_permiso = 'AC')
                
                descripcion_roles = 'nombre_de_usuario:' + user.nombre_de_usuario
                
                if roles_previous:
                    for rol in roles_previous:
                        rol_previous = Roles.objects.filter(id_rol=rol['id_rol']).first()
                        descripcion_roles += '|' + 'nombre_rol:' + rol_previous.nombre_rol
                    descripcion_roles += '.'
                else:
                    descripcion_roles += '.'
                
                if roles_asignados:
                    valores_actualizados = 'Se agregó en el detalle el rol '
                    for field, value in roles_asignados.items():
                        valores_actualizados += '' if not valores_actualizados else '|'
                        valores_actualizados += field + ":" + str(value)
                        
                    valores_actualizados += '.'
                    
                    auditoria_user = Auditorias.objects.create(
                        id_usuario = usuario,
                        id_modulo = modulo,
                        id_cod_permiso_accion = permiso,
                        subsistema = 'SEGU',
                        dirip = dirip,
                        descripcion = descripcion_roles,
                        valores_actualizados = valores_actualizados
                    )
                    
                    auditoria_user.save()
                
                if roles_eliminados:
                    valores_actualizados = 'Se eliminó en el detalle el rol '
                    for field, value in roles_eliminados.items():
                        valores_actualizados += '' if not valores_actualizados else '|'
                        valores_actualizados += field + ":" + str(value)
                        
                    valores_actualizados += '.'
                    
                    auditoria_user = Auditorias.objects.create(
                        id_usuario = usuario,
                        id_modulo = modulo,
                        id_cod_permiso_accion = permiso,
                        subsistema = 'SEGU',
                        dirip = dirip,
                        descripcion = descripcion_roles,
                        valores_actualizados = valores_actualizados
                    )
                    
                    auditoria_user.save()
                
                return Response({'success': True,'data': user_serializer.data})
            else:
                return Response({'success': False,'detail': 'No se encontró el usuario'})
        else:
            return Response({'success': False,'detail': 'No puede realizar esa acción'})

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


class GetUserByPersonDocument(generics.ListAPIView):
    persona_serializer = PersonasSerializer
    serializer_class = UserSerializer
    def get(self, request, keyword1, keyword2):
        try:
            persona = Personas.objects.get(Q(tipo_documento = keyword1) & Q(numero_documento = keyword2))
            try:
                user = User.objects.get(persona=persona.id_persona)
                serializador = self.serializer_class(user)
                return Response({'Usuario' : serializador.data})
            except:
                serializador = PersonasSerializer(persona, many=False)
                return Response({'Persona': serializador.data})
        except:
            return Response({'data': 'No se encuentra persona con este numero de documento'})



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
@permission_classes([IsAdminUser,])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id_usuario=pk)
    userForDeletion.delete()
    return Response('User was deleted')


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)
    permission_classes = [IsAuthenticated, PermisoCrearUsuarios]

    def post(self, request):
        user_logeado = request.user.id_usuario
        data = request.data

        #CREAR USUARIO
        serializer = self.serializer_class(data=data, many=False)
        serializer.is_valid(raise_exception=True)
        nombre_usuario_creado = serializer.validated_data.get('nombre_de_usuario')
        serializer.save()
        usuario = User.objects.get(nombre_de_usuario=nombre_usuario_creado)

        #AUDITORIA CREAR USUARIO
        dirip = Util.get_client_ip(request)
        descripcion = {'nombre_de_usuario': usuario.nombre_de_usuario}
        auditoria_data = {
            'id_usuario': user_logeado,
            'id_modulo': 2,
            'cod_permiso': 'CR',
            'subsistema': 'SEGU',
            'dirip': dirip,
            'descripcion': descripcion
        }
        Util.save_auditoria(auditoria_data)

        #ASIGNACIÓN DE ROLES AL USUARIO
        roles = request.data['roles']
        for rol in roles:
            try:
                consulta_rol = Roles.objects.get(id_rol=rol)
                descripcion["Rol" + str(rol)] = str(consulta_rol.nombre_rol)
                if consulta_rol:
                    UsuariosRol.objects.create(
                        id_rol = consulta_rol,
                        id_usuario = usuario
                    )    

                    #Auditoria Asignación de Roles    
                    dirip = Util.get_client_ip(request)
                    auditoria_data = {
                        'id_usuario': user_logeado,
                        'id_modulo': 5,
                        'cod_permiso': 'CR',
                        'subsistema': 'SEGU',
                        'dirip': dirip,
                        'descripcion': descripcion,
                    }
                    Util.save_auditoria(auditoria_data)
                else:
                    return Response({'No se puede asignar este rol por que no existe'})
            except:
                return Response({'No se puede consultar por que no existe este rol'})
        
        #Data paraSMS y EMAIL
        user = User.objects.get(email=usuario.email)

        token = RefreshToken.for_user(user).access_token
        current_site=get_current_site(request).domain

        persona = Personas.objects.get(id_persona = request.data['persona'])

        relativeLink= reverse('verify')
        absurl= 'http://'+ current_site + relativeLink + "?token="+ str(token)
        short_url = Util.get_short_url(request, absurl)

        if user.persona.tipo_persona == 'N':
            sms = 'Verifica tu usuario de Cormarena-Bia aqui: ' + short_url
            context = {'primer_nombre': user.persona.primer_nombre, 'primer_apellido': user.persona.primer_apellido, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
            return Response({'detail': 'creado exitosamente', 'usuario': serializer.data, 'Roles': roles})

        else:
            sms = 'Verifica tu usuario de Cormarena-Bia aqui: ' + short_url
            context = {'razon_social': user.persona.razon_social, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.razon_social
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular_empresa, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
            return Response({'detail': 'creado exitosamente', 'usuario': serializer.data, 'Roles': roles})

class RegisterExternoView(generics.CreateAPIView):
    serializer_class = RegisterExternoSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer_response = serializer.save()
        user_data = serializer.data

        # AUDITORIA AL REGISTRAR USUARIO

        dirip = Util.get_client_ip(request)
        descripcion = {'nombre_de_usuario': request.data["nombre_de_usuario"]}

        auditoria_data = {
            'id_usuario': serializer_response.pk,
            'id_modulo': 10,
            'cod_permiso': 'CR',
            'subsistema': 'SEGU',
            'dirip': dirip,
            'descripcion': descripcion
        }

        Util.save_auditoria(auditoria_data)

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site=get_current_site(request).domain

        persona = Personas.objects.get(id_persona = request.data['persona'])

        relativeLink= reverse('verify')
        absurl= 'http://'+ current_site + relativeLink + "?token="+ str(token)

        short_url = Util.get_short_url(request, absurl)

        if user.persona.tipo_persona == 'N':
            sms = 'Verifica tu usuario de Cormarena-Bia aqui: ' + short_url
            context = {'primer_nombre': user.persona.primer_nombre, 'primer_apellido': user.persona.primer_apellido, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
            return Response(user_data, status=status.HTTP_201_CREATED)

        else:
            sms = 'Verifica tu usuario de Cormarena-Bia aqui: ' + short_url
            context = {'razon_social': user.persona.razon_social, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.razon_social
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
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
                if user.persona.tipo_persona == 'N':
                    context = {'primer_nombre': user.persona.primer_nombre}
                    template = render_to_string(('email-verified.html'), context)
                    subject = 'Verificación exitosa ' + user.nombre_de_usuario
                    data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                    Util.send_email(data)
                else:
                    context = {'razon_social': user.persona.razon_social}
                    template = render_to_string(('email-verified.html'), context)
                    subject = 'Verificación exitosa ' + user.nombre_de_usuario
                    data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                    Util.send_email(data)
            return Response({'email': 'succesfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'activation link expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()

class LoginListApiViews(generics.ListAPIView):
    serializer_class=LoginSerializers
    queryset = Login.objects.all()

#__________________LoginErroneo

class LoginErroneoConsultarApiViews(generics.RetrieveAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()

class LoginErroneoListApiViews(generics.ListAPIView):
    serializer_class=LoginErroneoSerializers
    queryset = LoginErroneo.objects.all()

class LoginApiView(generics.CreateAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        data = request.data
        user = User.objects.filter(email=data['email']).first()
        ip = Util.get_client_ip(request)
        device = Util.get_client_device(request)
        if user:
            if user.is_active:
                try:
                    login_error = LoginErroneo.objects.filter(id_usuario=user.id_usuario).last()
                    serializer = self.serializer_class(data=request.data)
                    serializer.is_valid(raise_exception=True)

                    login = Login.objects.create(
                        id_usuario = user,
                        dirip = str(ip),
                        dispositivo_conexion = device
                    )

                    LoginPostSerializers(login, many=False)

                    if login_error:
                        login_error.contador = 0
                        login_error.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                except:
                    login_error = LoginErroneo.objects.filter(id_usuario=user.id_usuario).first()
                    if login_error:
                        if login_error.contador < 3:
                            hour_difference = datetime.utcnow().replace(tzinfo=None) - login_error.fecha_login_error.replace(tzinfo=None)
                            hour_difference = (hour_difference.days * 24) + (hour_difference.seconds//3600)
                            if hour_difference < 24:
                                login_error.contador += 1
                                login_error.save()
                            else :
                                login_error.contador = 1
                                login_error.save()
                            if login_error.contador == 3:
                                user.is_blocked = True
                                user.save()

                                if user.persona.tipo_persona == 'N':
                                    sms = 'Usuario Cormacarena Bia bloqueado por limite de intentos, desbloquealo enviando un correo a admin@admin.com'
                                    context = {'primer_nombre': user.persona.primer_nombre}
                                    template = render_to_string(('email-blocked-user.html'), context)
                                    subject = 'Bloqueo de cuenta ' + user.persona.primer_nombre
                                    email_data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                                    Util.send_email(email_data)
                                    try:
                                        Util.send_sms(user.persona.telefono_celular, sms)
                                    except:
                                        return Response({'detail': 'Se bloqueó el usuario pero no pudo enviar el sms, verificar servicio o número'})
                                    return Response({'detail':'Su usuario ha sido bloqueado'})
                                else:
                                    sms = 'Usuario Cormacarena Bia bloqueado por limite de intentos, desbloquealo enviando un correo a admin@admin.com'
                                    context = {'razon_social': user.persona.razon_social}
                                    template = render_to_string(('email-blocked-user.html'), context)
                                    subject = 'Bloqueo de cuenta ' + user.persona.razon_social
                                    email_data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                                    Util.send_email(email_data)
                                    try:
                                        Util.send_sms(user.persona.telefono_celular, sms)
                                    except:
                                        return Response({'detail': 'Se bloqueó el usuario pero no pudo enviar el sms, verificar servicio o número'})
                                    return Response({'detail':'Su usuario ha sido bloqueado'})
                            serializer = LoginErroneoPostSerializers(login_error, many=False)
                            return Response({'success':False, 'detail':'La contraseña es invalida', 'login_erroneo': serializer.data})
                        else:
                            if user.is_blocked:
                                return Response({'success':False, 'detail':'Su usuario está bloqueado, debe comunicarse con el administrador'})
                            else:
                                login_error.contador = 1
                                login_error.save()

                                serializer = LoginErroneoPostSerializers(login_error, many=False)
                                return Response({'success':False, 'detail':'La contraseña es invalida', 'login_erroneo': serializer.data}, status=status.HTTP_200_OK)
                    else:
                        if user.is_blocked:
                            return Response({'success':False, 'detail':'Su usuario está bloqueado, debe comunicarse con el administrador'})
                        else:
                            login_error = LoginErroneo.objects.create(
                                id_usuario = user,
                                dirip = str(ip),
                                dispositivo_conexion = device,
                                contador = 1
                            )
                        serializer = LoginErroneoPostSerializers(login_error, many=False)
                        return Response({'detail':'La contraseña es invalida', 'login_erroneo': serializer.data})
            else:
                return Response({'detail': 'Usuario no verificado'})
        else:
            return Response({'detail':'No existe el correo ingresado'})

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 =signing.dumps({'user':str(user.id_usuario)})
            print(uidb64)
            token = PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(request=request).domain
            relativeLink=reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            absurl='http://'+ current_site + relativeLink
            if user.persona.tipo_persona == 'N':
                context = {
                'primer_nombre': user.persona.primer_nombre,
                'primer_apellido':user.persona.primer_apellido,
                'absurl': absurl,
                }
                template = render_to_string(('email-resetpassword.html'), context)
                subject = 'Actualiza tu contraseña ' + user.persona.primer_nombre
                data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                Util.send_email(data)
            else:
                context = {
                'razon_social': user.persona.razon_social,
                'absurl': absurl,
                }
                template = render_to_string(('email-resetpassword.html'), context)
                subject = 'Actualiza tu contraseña ' + user.persona.razon_social
                data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                Util.send_email(data)
        return Response( {'success': 'te enviamos el link  para poder actualizar tu contraseña'},status=status.HTTP_200_OK)

class PasswordTokenCheckApi(generics.GenericAPIView):
    serializer_class=UserSerializer
    def get(self,request,uidb64,token):
        try:
            id = int(signing.loads(uidb64)['user'])
            user = User.objects.get(id_usuario=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error': 'token invalido, solicita uno nuevo'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True, 'message':'Credenciales validas', 'uidb64':uidb64,'token':token}, status=status.HTTP_200_OK)
        except encoding.DjangoUnicodeDecodeError as identifier:

            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error':'aslkdjaslkdjaslk'})

class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Contraseña actualizada'},status=status.HTTP_200_OK)
