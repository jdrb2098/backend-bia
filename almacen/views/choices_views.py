from almacen.choices.agrupacion_documental_choices import agrupacion_documental_CHOICES
from almacen.choices.tipo_unidad_choices import tipo_unidad_CHOICES
from almacen.choices.estados_articulo_choices import estados_articulo_CHOICES
from almacen.choices.magnitudes_choices import magnitudes_CHOICES
from rest_framework.views import APIView
from rest_framework.response import Response

class AgrupacionDocumentalChoices(APIView):
    def get(self,request):
        choices = agrupacion_documental_CHOICES
        return Response(choices)

class TipoUnidadChoices(APIView):
    def get(self,request):
        choices = tipo_unidad_CHOICES
        return Response(choices)
    
class EstadosArticuloChoices(APIView):
    def get(self,request):
        choices = estados_articulo_CHOICES
        return Response(choices)

class MagnitudesChoices(APIView):
    def get(self,request):
        choices = magnitudes_CHOICES
        return Response(choices)