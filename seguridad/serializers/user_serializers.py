
from dataclasses import field
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from seguridad.models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    roles = serializers.SerializerMethodField(read_only= True)

    class Meta:
        model = User
        fields = ['id_usuario', '_id', 'nombre_de_usuario', 'email', 'name', 'isAdmin', 'roles']

    def get__id(self, obj):
        return obj.id_usuario

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_roles(self, obj):
        return obj.roles

    def get_name(self, obj):
        name = obj.persona
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id_usuario', '_id', 'nombre_de_usuario', 'email', 'name', 'isAdmin', 'token', 'roles']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

