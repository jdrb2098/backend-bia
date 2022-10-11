from seguridad.choices.paises_choices import paises_CHOICES
from seguridad.choices.departamentos_choices import departamentos_CHOICES
from seguridad.choices.municipios_choices import municipios_CHOICES
from seguridad.choices.sexo_choices import sexo_CHOICES
from seguridad.choices.auditorias_subsistemas_choices import auditorias_subsistemas_CHOICES
from seguridad.choices.cod_permiso_choices import cod_permiso_CHOICES
from seguridad.choices.modulos_subsistemas_choices import modulos_subsistemas_CHOICES
from seguridad.choices.opciones_usuario_choices import opciones_usuario_CHOICES
from seguridad.choices.tipo_direccion_choices import tipo_direccion_CHOICES
from seguridad.choices.tipo_documento_choices import tipo_documento_CHOICES
from seguridad.choices.tipo_persona_choices import tipo_persona_CHOICES
from seguridad.choices.tipo_usuario_choices import tipo_usuario_CHOICES
from rest_framework.views import APIView
from rest_framework.response import Response

class PaisesChoices(APIView):
    def get(self,request):
        choices = paises_CHOICES
        return Response(choices)

class DepartamentosChoices(APIView):
    def get(self,request):
        choices = departamentos_CHOICES
        return Response(choices)
    
class MunicipiosChoices(APIView):
    def get(self,request):
        choices = municipios_CHOICES
        return Response(choices)
    
class SexoChoices(APIView):
    def get(self,request):
        choices = sexo_CHOICES
        return Response(choices)

class AuditoriasSubsistemasChoices(APIView):
    def get(self,request):
        choices = auditorias_subsistemas_CHOICES
        return Response(choices)

class CodPermisoChoices(APIView):
    def get(self,request):
        choices = cod_permiso_CHOICES
        return Response(choices)
    
class ModulosSubsistemasChoices(APIView):
    def get(self,request):
        choices = modulos_subsistemas_CHOICES
        return Response(choices)
    
class OpcionesUsuarioChoices(APIView):
    def get(self,request):
        choices = opciones_usuario_CHOICES
        return Response(choices)

class TipoDireccionChoices(APIView):
    def get(self,request):
        choices = tipo_direccion_CHOICES
        return Response(choices)

class TipoDocumentoChoices(APIView):
    def get(self,request):
        choices = tipo_documento_CHOICES
        return Response(choices)
    
class TipoPersonaChoices(APIView):
    def get(self,request):
        choices = tipo_persona_CHOICES
        return Response(choices)
    
class TipoUsuarioChoices(APIView):
    def get(self,request):
        choices = tipo_usuario_CHOICES
        return Response(choices)