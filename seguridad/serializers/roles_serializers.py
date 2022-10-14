
from rest_framework import serializers
from seguridad.models import Roles,UsuariosRol





class RolesSerializer(serializers.ModelSerializer):
     class Meta:
         model = Roles
         fields = '__all__'
         
class UsuarioRolesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=UsuariosRol
        fields='__all__'


        
        
        
        
        
        
        
        