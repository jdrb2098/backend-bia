from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework import serializers
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import encoding, http
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from seguridad.models import User, UsuariosRol, HistoricoActivacion,Login,LoginErroneo
from seguridad.models import User, UsuariosRol, HistoricoActivacion, PermisosModuloRol
from seguridad.serializers.personas_serializers import PersonasSerializer
from seguridad.serializers.permisos_serializers import PermisosModuloRolSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from seguridad.utils import Util

class HistoricoActivacionSerializers(serializers.ModelSerializer):
    class Meta:
        model= HistoricoActivacion
        fields = '__all__'

class UserRolesSerializer(serializers.ModelSerializer):
    permisos_rol = serializers.SerializerMethodField()
    
    class Meta:
        model = UsuariosRol
        fields = '__all__'

    def get_permisos_rol(self, obj):
        permisos_rol = PermisosModuloRol.objects.filter(id_rol=obj.id_rol)
        return PermisosModuloRolSerializer(permisos_rol, many=True).data
        
class UsuarioCreadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    id_usuario_creador = UsuarioCreadorSerializer(read_only=True)
    persona = PersonasSerializer(read_only=True)
    usuario_rol = UserRolesSerializer(read_only=True)
    

    class Meta:
        model = User
        fields = '__all__'

    def get_usuario_rol(self, obj):
        rol = obj.usuariosrol_set.all()
        serializer = UserRolesSerializer(rol, many=True)
        return serializer.data

    def get__id(self, obj):
        return obj.id_usuario

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_usuario_creador(self,obj):
        usuario_creador= obj.id_usuario_creador
        serializer = UsuarioCreadorSerializer(usuario_creador,many=True)
        return serializer.data
    
    def create(self, validated_data):
        usuario_creador = validated_data.pop('usuario_creador')
        user_instance = User.objects.create(**validated_data)
        for user in usuario_creador:
            User.objects.create(user=user_instance,**user)
        return user_instance
    
class UsuarioRolesLookSerializers(serializers.ModelSerializer):
    id_usuario = UserSerializer(read_only=True)
    class Meta:
        model=UsuariosRol
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length= 68, min_length = 6, write_only=True)
    class Meta:
        model = User
        fields = ["email", 'nombre_de_usuario', 'persona', 'password', 'id_usuario_creador', 'tipo_usuario', 'is_active', 'is_blocked']

    def validate(self, attrs):
        email= attrs.get('email', '')
        nombre_de_usuario=attrs.get('nombre_de_usuario', '')
        if not nombre_de_usuario.isalnum():
            raise serializers.ValidationError("El Nombre de usuario solo debe tener caracteres alfanumericos")
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

from seguridad.models import Login,LoginErroneo

class LoginSerializers(serializers.ModelSerializer):
    id_usuario=UserSerializer(read_only=True)
    class Meta:
        model=Login
        fields= '__all__'

class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password= serializers.CharField(max_length=68, min_length=6, write_only=True)
    nombre_de_usuario = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)
    class Meta:
        model=Login
        fields= ['email', 'password', 'nombre_de_usuario', 'tokens']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user= auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Credenciales invalidas intenta denuevo')
        
        if not user.is_active:
            raise AuthenticationFailed('Cuenta no verificada')
        if user.is_blocked:
            raise AuthenticationFailed('Tu cuenta ha sido bloqueada, contacta un Admin')

        return {'email': user.email, 'nombre_de_usuario': user.nombre_de_usuario, 'tokens': user.tokens()}
 
class LoginPostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Login
        fields= '__all__'
        extra_kwargs = {
                'id_login': {'required': True},
                'id_usuario': {'required': True},
                'dirip':  {'required': True},
                'dispositivo_conexion': {'required': True},
                'fecha_login': {'required': True},
            }
    
class LoginErroneoSerializers(serializers.ModelSerializer):
    id_usuario=UserSerializer(read_only=True)
    class Meta:
        model=LoginErroneo
        fields= '__all__'

class LoginErroneoPostSerializers(serializers.ModelSerializer):
    class Meta:
     model=LoginErroneo
     fields= '__all__'
     extra_kwargs = {
                'id_login_error': {'required': True},
                'id_usuario': {'required': True},
                'dirip':  {'required': True},
                'dispositivo_conexion': {'required': True},
                'fecha_login_error': {'required': True},
                'contador': {'required': True},  
            }
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        models = User
        fields = ['token']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        email = attrs['data'].get('email','')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = http.urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(request=attrs['data'].get('request')).domain
            relativeLink=reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            absurl='http://'+ current_site + relativeLink 
            context = {
                'primer_nombre': user.persona.primer_nombre,
                'primer_apellido':user.persona.primer_apellido,
                'absurl': absurl,
                }
            template = render_to_string(('email-resetpassword.html'), context)
            data = {'template': template, 'email_subject': 'Verifica tu usuario', 'to_email': user.email}
            Util.send_email(data)
        return super().validate(attrs)
        
