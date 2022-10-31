from almacen.models.generics_models import UnidadesMedida
from almacen.serializers.generics_serializers import SerializersUnidadesMedida
from almacen.models.generics_models import Magnitudes
from almacen.models.generics_models import Bodegas
from almacen.serializers.generics_serializers import SerializerBodegas,SerializerMagnitudes
from rest_framework import generics
from almacen.serializers.generics_serializers import SerializersMarca, SerializersEstadosArticulo, SerializerPorcentajesIVA
from almacen.models.generics_models import Marcas, EstadosArticulo, PorcentajesIVA
from rest_framework.response import Response


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

#Magnitudes

class GetMagnitudesById(generics.RetrieveAPIView):
    serializer_class=SerializerMagnitudes
    queryset=Magnitudes.objects.all()

class GetMagnitudesList(generics.ListAPIView):
    serializer_class=SerializerMagnitudes
    queryset=Magnitudes.objects.all()

#Porcentajes IVA
class RegisterPorcentaje(generics.CreateAPIView):
    serializer_class=SerializerPorcentajesIVA
    queryset=PorcentajesIVA.objects.all()
    
class UpdatePorcentaje(generics.UpdateAPIView):
    serializer_class=SerializerPorcentajesIVA
    queryset=PorcentajesIVA.objects.all()
    
    def put(self, request, pk):
        try:
            data = request.data
            porcentaje = PorcentajesIVA.objects.get(id_porcentaje_iva=pk)
            
            if porcentaje.registro_precargado == False:
                porcentaje_serializer = self.serializer_class(porcentaje, data)
                porcentaje_serializer.is_valid(raise_exception=True)
                porcentaje_serializer.save()
                
                return Response({'success':True, 'data': porcentaje_serializer.data})
            else:
                return Response({'success':False, 'detail': 'No puedes actualizar un porcentaje precargado'})
        except:
            return Response({'success':False, 'detail': 'No existe el porcentaje'})
    
class DeletePorcentaje(generics.DestroyAPIView):
    serializer_class=SerializerPorcentajesIVA
    queryset=PorcentajesIVA.objects.all()
    
    def delete(self, request, pk):
        try:
            porcentaje = PorcentajesIVA.objects.get(id_porcentaje_iva=pk)
            
            if porcentaje.registro_precargado == False:
                porcentaje.delete()
                
                return Response({'success':True, 'detail': 'Se ha eliminado exitosamente'})
            else:
                return Response({'success':False, 'detail': 'No puedes eliminar un porcentaje precargado'})
        except:
            return Response({'success':False, 'detail': 'No existe el porcentaje'})

class GetPorcentajeById(generics.RetrieveAPIView):
    serializer_class=SerializerPorcentajesIVA
    queryset=PorcentajesIVA.objects.all()

class GetPorcentajeList(generics.ListAPIView):
    serializer_class=SerializerPorcentajesIVA
    queryset=PorcentajesIVA.objects.all()
    
#UnidadesMedida
class RegisterUnidadMedida(generics.CreateAPIView):
    serializer_class=SerializersUnidadesMedida
    queryset=UnidadesMedida.objects.all()
    
class UpdateUnidadMedida(generics.UpdateAPIView):
    serializer_class=SerializersUnidadesMedida
    queryset=UnidadesMedida.objects.all()
    
class DeleteUnidadMedida(generics.DestroyAPIView):
    serializer_class=SerializersUnidadesMedida
    queryset=UnidadesMedida.objects.all()

class GetUnidadMedidaById(generics.RetrieveAPIView):
    serializer_class=SerializersUnidadesMedida
    queryset=UnidadesMedida.objects.all()

class GetUnidadMedidaList(generics.ListAPIView):
    serializer_class=SerializersUnidadesMedida
    queryset=UnidadesMedida.objects.all()