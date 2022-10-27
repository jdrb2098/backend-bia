from base64 import urlsafe_b64decode, urlsafe_b64encode
from email import message
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
            
            usuario = User.objects.get(id_usuario = request.user.id_usuario)
            modulo = Modulos.objects.get(id_modulo = 3)
            permiso = Permisos.objects.get(cod_permiso = 'AC')
            dirip = Util.get_client_ip(request)
            descripcion =   "idUsuario:" + str(user_loggedin) + ";" + "nombreUsuario:" + str(user.nombre_de_usuario) + "."
            valores_actualizados = ""
                
            del previous_user.__dict__["_state"]
            del previous_user.__dict__["_django_version"]
            
            for field, value in previous_user.__dict__.items():
                new_value = getattr(user,field)
                if value != new_value:
                    valores_actualizados += field + "_anterior:" + str(value) + ";" + field + "_nuevo:" + str(new_value) + ";"
            
            auditoria_user = Auditorias.objects.create(
                id_usuario = usuario,
                id_modulo = modulo,
                id_cod_permiso_accion = permiso,
                subsistema = "SEGU",
                dirip = dirip,
                descripcion = descripcion,
                valores_actualizados = valores_actualizados
            )
            auditoria_user.save()
            
            return Response({'success': True,'data': user_serializer.data})
        
        
class UpdateUserProfileExterno(generics.RetrieveUpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = UserPutSerializerExterno
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarExterno]
    
    def patch(self, request):
        user_loggedin = self.request.user.id_usuario
        user = User.objects.filter(id_usuario = self.request.user.id_usuario).first()
        previous_user = copy.copy(user)
        if user:
            user_serializer = self.serializer_class(user, data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            
            # AUDITORIA AL ACTUALIZAR USUARIO PROPIO
            
            usuario = User.objects.get(id_usuario = request.user.id_usuario)
            modulo = Modulos.objects.get(id_modulo = 4)
            permiso = Permisos.objects.get(cod_permiso = 'AC')
            dirip = Util.get_client_ip(request)
            descripcion =   "idUsuario:" + str(user_loggedin) + ";" + "nombreUsuario:" + str(user.nombre_de_usuario) + "."
            valores_actualizados = ""
                
            del previous_user.__dict__["_state"]
            del previous_user.__dict__["_django_version"]
            
            for field, value in previous_user.__dict__.items():
                new_value = getattr(user,field)
                if value != new_value:
                    valores_actualizados += field + "_anterior:" + str(value) + ";" + field + "_nuevo:" + str(new_value) + ";"
            
            auditoria_user = Auditorias.objects.create(
                id_usuario = usuario,
                id_modulo = modulo,
                id_cod_permiso_accion = permiso,
                subsistema = "SEGU",
                dirip = dirip,
                descripcion = descripcion,
                valores_actualizados = valores_actualizados
            )
            auditoria_user.save()
            
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
                
                # AUDITORIA AL ACTUALIZAR USUARIO
                
                usuario = User.objects.get(id_usuario = user_loggedin)
                modulo = Modulos.objects.get(id_modulo = 2)
                permiso = Permisos.objects.get(cod_permiso = 'AC')
                dirip = Util.get_client_ip(request)
                descripcion =   "idUsuario:" + str(user_loggedin) + ";" + "nombreUsuario:" + str(user.nombre_de_usuario) + "."
                valores_actualizados = ""
                
                del previous_user.__dict__["_state"]
                del previous_user.__dict__["_django_version"]
                
                for field, value in previous_user.__dict__.items():
                    new_value = getattr(user,field)
                    if value != new_value:
                        valores_actualizados += field + "_anterior:" + str(value) + ";" + field + "_nuevo:" + str(new_value) + ";"
                    
                auditoria_user = Auditorias.objects.create(
                    id_usuario = usuario,
                    id_modulo = modulo,
                    id_cod_permiso_accion = permiso,
                    subsistema = "SEGU",
                    dirip = dirip,
                    descripcion = descripcion,
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
            user = User.objects.get(persona=persona.id_persona)
            serializador = self.serializer_class(user)
            return Response({'Respuesta' : serializador.data})
        except:
            return Response({'data': 'Datos no validos'})
        
    
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
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer_response = serializer.save()
        
        user_data = serializer.data
        
        # AUDITORIA AL REGISTRAR USUARIO
        
        usuario = User.objects.get(id_usuario = request.user.id_usuario)
        modulo = Modulos.objects.get(id_modulo = 2)
        permiso = Permisos.objects.get(cod_permiso = 'CR')
        dirip = Util.get_client_ip(request)
        
        currentdate = datetime.date.today()
        formatDate = currentdate.strftime("%d/%m/%y")
        
        descripcion = "idUsuario:" + str(serializer_response.pk) + ";" + "fecha:" + formatDate + ";" + "observaciones:Registro de otro usuario" + ";" + "nombreUsuario:"+ serializer_response.nombre_de_usuario + "."
        
        auditoria_user = Auditorias.objects.create(
            id_usuario = usuario,
            id_modulo = modulo,
            id_cod_permiso_accion = permiso,
            subsistema = "SEGU",
            dirip = dirip,
            descripcion = descripcion
        )
        auditoria_user.save()
        
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        
        current_site=get_current_site(request).domain

        persona = Personas.objects.get(id_persona = request.data['persona'])

        relativeLink= reverse('verify')
        absurl= 'http://'+ current_site + relativeLink + "?token="+ str(token)
        
        short_url = Util.get_short_url(request, absurl)
        
        if user.persona.tipo_persona == 'N':
            sms = 'Hola '+ user.persona.primer_nombre + ' ' + user.persona.primer_apellido + ' utiliza el siguiente link para verificar tu usuario \n' + short_url
            context = {'primer_nombre': user.persona.primer_nombre, 'primer_apellido': user.persona.primer_apellido, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            try:
                Util.send_email(data)
            except:
                return Response({'success':False, 'message':'no se pudo enviar email de confirmacion'})
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
            return Response(user_data, status=status.HTTP_201_CREATED)

        else:
            sms = 'Hola '+ user.persona.razon_social + ' utiliza el siguiente link para verificar tu usuario \n' + short_url
            context = {'razon_social': user.persona.razon_social, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.razon_social
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            try:
                Util.send_email(data)
            except:
                return Response({'success':False, 'message':'no se pudo enviar email de confirmacion'})
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
            return Response(user_data, status=status.HTTP_201_CREATED)

class RegisterExternoView(generics.CreateAPIView):
    serializer_class = RegisterExternoSerializer
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
        
        short_url = Util.get_short_url(request, absurl)
        
        if user.persona.tipo_persona == 'N':
            sms = 'Hola '+ user.persona.primer_nombre + ' ' + user.persona.primer_apellido + ' utiliza el siguiente link para verificar tu usuario \n' + short_url
            context = {'primer_nombre': user.persona.primer_nombre, 'primer_apellido': user.persona.primer_apellido, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            try:
                Util.send_email(data)
            except:
                return Response({'success':False, 'message':'no se pudo enviar email de confirmacion'})
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':False, 'message':'no se pudo envias sms de confirmacion'})
            return Response(user_data, status=status.HTTP_201_CREATED)

        else:
            sms = 'Hola '+ user.persona.razon_social + ' utiliza el siguiente link para verificar tu usuario \n' + short_url
            context = {'razon_social': user.persona.razon_social, 'absurl': absurl}
            template = render_to_string(('email-verification.html'), context)
            subject = 'Verifica tu usuario ' + user.persona.razon_social
            data = {'template': template, 'email_subject': subject, 'to_email': user.email}
            try:
                Util.send_email(data)
            except:
                return Response({'success':False, 'message':'no se pudo enviar email de confirmacion'})
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
                    try:
                        Util.send_email(data)
                    except:
                        return Response({'detail': 'No se pudo enviar el email, verificar servicio'})
                else:
                    context = {'razon_social': user.persona.razon_social}
                    template = render_to_string(('email-verified.html'), context)
                    subject = 'Verificación exitosa ' + user.nombre_de_usuario
                    data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                    try:
                        Util.send_email(data)
                    except:
                        return Response({'detail': 'No se pudo enviar el email, verificar servicio'})
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
                                    sms = 'Hola ' + user.persona.primer_nombre + ' Tu usuario ha sido bloqueado ya que alcanzó el limite de intentos \
                                        para ingresar a Bia Cormacarena, desbloquealo enviando un correo a admin@admin.com'
                                    context = {'primer_nombre': user.persona.primer_nombre}
                                    template = render_to_string(('email-blocked-user.html'), context)
                                    subject = 'Bloqueo de cuenta ' + user.persona.primer_nombre
                                    email_data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                                    try:
                                        Util.send_email(email_data)
                                    except:
                                        return Response({'detail': 'Se bloqueó el usuario pero no pudo enviar el email, verificar servicio'})
                                    try:
                                        Util.send_sms(user.persona.telefono_celular, sms)
                                    except:
                                        return Response({'detail': 'Se bloqueó el usuario pero no pudo enviar el sms, verificar servicio o número'})
                                    return Response({'detail':'Su usuario ha sido bloqueado'})
                                else:
                                    sms = 'Hola ' + user.persona.razon_social + ' Tu usuario ha sido bloqueado ya que alcanzó el limite de intentos \
                                        para ingresar a Bia Cormacarena, desbloquealo enviando un correo a admin@admin.com'
                                    context = {'razon_social': user.persona.razon_social}
                                    template = render_to_string(('email-blocked-user.html'), context)
                                    subject = 'Bloqueo de cuenta ' + user.persona.razon_social
                                    email_data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                                    try:
                                        Util.send_email(email_data)
                                    except:
                                        return Response({'detail': 'Se bloqueó el usuario pero no pudo enviar el email, verificar servicio'})
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
                try:
                    Util.send_email(data)
                except:
                    return Response({'detail': 'error '})
            else:
                context = {
                'razon_social': user.persona.razon_social,
                'absurl': absurl,
                }
                template = render_to_string(('email-resetpassword.html'), context)
                subject = 'Actualiza tu contraseña ' + user.persona.razon_social
                data = {'template': template, 'email_subject': subject, 'to_email': user.email}
                try:
                    Util.send_email(data)
                except:
                    return Response({'detail': 'error '})
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
    