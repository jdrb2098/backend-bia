from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from almacen.models.generics_models import Marcas, EstadosArticulo,Bodegas

class SerializersMarca(serializers.ModelSerializer):
    class Meta:
        model=Marcas
        fields=('__all__')
        

class SerializersEstadosArticulo(serializers.ModelSerializer):
    class Meta:
        model=EstadosArticulo
        fields=('__all__')
        
class SerializerBodegas(serializers.ModelSerializer):
    class Meta:
        model=Bodegas
        fields=('__all__')
        