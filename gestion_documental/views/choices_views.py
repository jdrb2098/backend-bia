from gestion_documental.choices.tipo_clasificacion_choices import tipo_clasificacion_CHOICES
from rest_framework.views import APIView
from rest_framework.response import Response

class TipoClasificacion(APIView):
    def get(self,request):
        choices = tipo_clasificacion_CHOICES
        return Response(choices)