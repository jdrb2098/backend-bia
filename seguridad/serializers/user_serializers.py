
from dataclasses import field
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from seguridad.models import User, UsuariosRol, HistoricoActivacion
from seguridad.serializers.personas_serializers import PersonasSerializer
from seguridad.serializers.roles_serializers import RolesSerializer

class HistoricoActivacionSerializers(serializers.ModelSerializer):
    class Meta:
        model= HistoricoActivacion
        fields = '__all__'

class UserRolesSerializer(serializers.ModelSerializer):
    id_rol = RolesSerializer(read_only=True)

    class Meta:
        model = UsuariosRol
        fields = '__all__'
        
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


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id_usuario', '_id', 'nombre_de_usuario', 'email', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
