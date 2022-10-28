from almacen.models.generics_models import Bodegas
from almacen.serializers.generics_serializers import SerializerBodegas
from rest_framework import generics
from almacen.serializers.generics_serializers import SerializersMarca, SerializersEstadosArticulo
from almacen.models.generics_models import Marcas, EstadosArticulo



#_______Marca
class RegisterMarca(generics.CreateAPIView):
    serializer_class=SerializersMarca
    queryset=Marcas.objects.all()
    
class UpdateMarca(generics.UpdateAPIView):
    serializer_class=SerializersMarca
    queryset=Marcas.objects.all()
    
class DeleteMarca(generics.DestroyAPIView):
    serializer_class=SerializersMarca
    queryset=Marcas.objects.all()

class GetMarcaById(generics.RetrieveAPIView):
    serializer_class=SerializersMarca
    queryset=Marcas.objects.all()

class GetMarcaList(generics.ListAPIView):
    serializer_class=SerializersMarca
    queryset=Marcas.objects.all()
    
    
# Estado Articulos  
class GetEstadosArticuloById(generics.RetrieveAPIView):
    serializer_class=SerializersEstadosArticulo
    queryset=EstadosArticulo.objects.all()

class GetEstadosArticuloList(generics.ListAPIView):
    serializer_class=SerializersEstadosArticulo
    queryset=EstadosArticulo.objects.all()

#Bodega

class RegisterBodega(generics.CreateAPIView):
    serializer_class=SerializerBodegas
    queryset=Bodegas.objects.all()
    
class UpdateBodega(generics.UpdateAPIView):
    serializer_class=SerializerBodegas
    queryset=Bodegas.objects.all()
    
class DeleteBodega(generics.DestroyAPIView):
    serializer_class=SerializerBodegas
    queryset=Bodegas.objects.all()

class GetBodegaById(generics.RetrieveAPIView):
    serializer_class=SerializerBodegas
    queryset=Bodegas.objects.all()

class GetBodegaList(generics.ListAPIView):
    serializer_class=SerializerBodegas
    queryset=Bodegas.objects.all()
