from django.shortcuts import render
from seguridad.choices import paises_choices, departamentos_choices, municipios_choices, sexo_choices
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics  import RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from seguridad.models import (
    Personas,
    TipoDocumento,
    EstadoCivil,
    ApoderadoPersona,
    SucursalesEmpresas,
    HistoricoEmails,
    HistoricoDireccion,
    ClasesTercero,
    ClasesTerceroPersona
)

from rest_framework import filters
from seguridad.serializers.personas_serializers import (
    EstadoCivilSerializer,
    EstadoCivilPostSerializer,
    TipoDocumentoSerializer,
    TipoDocumentoPostSerializer,
    PersonasSerializer,
    PersonaNaturalSerializer,
    PersonaJuridicaSerializer,
    PersonaNaturalPostSerializer,
    PersonaJuridicaPostSerializer,
    ApoderadoPersonaSerializer,
    ApoderadoPersonaPostSerializer,
    SucursalesEmpresasSerializer,
    SucursalesEmpresasPostSerializer,
    HistoricoEmailsSerializer,
    HistoricoEmailsPostSerializer,
    HistoricoDireccionSerializer,
    HistoricoDireccionPostSerializer,
    ClasesTerceroSerializer,
    ClasesTerceroPersonaSerializer,
    ClasesTerceroPersonapostSerializer
)

# Views for Estado Civil


class getEstadoCivil(generics.ListAPIView):
    serializer_class = EstadoCivilSerializer
    queryset = EstadoCivil.objects.all()


class getEstadoCivilById(generics.RetrieveAPIView):
    serializer_class = EstadoCivilSerializer
    queryset = EstadoCivil.objects.all()


class deleteEstadoCivil(generics.DestroyAPIView):
    serializer_class = EstadoCivilSerializer
    queryset = EstadoCivil.objects.all()
    
    def delete(self, request, pk):
        estado_civil = EstadoCivil.objects.get(cod_estado_civil=pk)
        if estado_civil.precargado == False:
            estado_civil.delete()
            return Response({'message' :'Eliminado Exitosamente'})
        else: 
            return Response({ 'message' : 'No puedes eliminar un estado civil precargado'})


class updateEstadoCivil(generics.RetrieveUpdateAPIView):
    serializer_class = EstadoCivilPostSerializer
    queryset = EstadoCivil.objects.all()
    
    
    def update(self, request, pk):
        estado_civil = EstadoCivil.objects.get(cod_estado_civil=pk)
        data = request.data
        if estado_civil.precargado == False:
            estado_civil.cod_estado_civil = data['cod_estado_civil']
            estado_civil.nombre = data['nombre']
            estado_civil.save()
            return Response({'message': 'Actualizado exitosamente'})
        else:
            return Response({'message': 'No puedes actualizar un estado civil precargado'})       


class registerEstadoCivil(generics.CreateAPIView):
    serializer_class = EstadoCivilPostSerializer
    queryset = EstadoCivil.objects.all()
    

# Views for Tipo Documento


class getTipoDocumento(generics.ListAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()


class getTipoDocumentoById(generics.RetrieveAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()


class deleteTipoDocumento(generics.DestroyAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()
    
    def delete(self, request, pk):
        tipo_documento = TipoDocumento.objects.get(cod_tipo_documento=pk)
        if tipo_documento.precargado == False:
            tipo_documento.delete()
            return Response({'message' :'Eliminado Exitosamente'})
        else: 
            return Response({ 'message' : 'No puedes eliminar un tipo de documento precargado'})
            
        
class updateTipoDocumento(generics.RetrieveUpdateAPIView):
    serializer_class = TipoDocumentoPostSerializer
    queryset = TipoDocumento.objects.all()

    def update(self, request, pk):
        tipo_documento = TipoDocumento.objects.get(cod_tipo_documento=pk)
        data = request.data
        if tipo_documento.precargado == False:
            tipo_documento.cod_tipo_documento = data['cod_tipo_documento']
            tipo_documento.nombre = data['nombre']
            tipo_documento.save()
            return Response({'message': 'Actualizado exitosamente'})
        else:
            return Response({'message': 'No puedes actualizar un tipo de documento precargado'})


class registerTipoDocumento(generics.CreateAPIView):
    serializer_class = TipoDocumentoPostSerializer
    queryset = TipoDocumento.objects.all()


# Views for Personas

class getPersonas(generics.ListAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class GetPersonaNatural(generics.ListAPIView):
    serializer_class=PersonaNaturalSerializer
    queryset=Personas.objects.filter(tipo_persona='N')       
    filter_backends=[filters.SearchFilter]
    search_fields=['primer_nombre','primer_apellido']
    
    
class GetPersonaJuridica(generics.ListAPIView):
    serializer_class=PersonaJuridicaSerializer
    queryset=Personas.objects.filter(tipo_persona='J')
    filter_backends=[filters.SearchFilter]
    search_fields=['razon_social','nombre_comercial']
    

@api_view(['GET'])
def getPersonaByDocument(request,pk):
    try:
        persona = Personas.objects.get(numero_documento=pk)
        serializer = PersonasSerializer(persona, many=False)
        return Response(serializer.data)
    except:
        return Response({"message": "No existe una persona con este documento"})    


@api_view(['GET'])
def getPersonaByEmail(request,pk):
    try:
        persona = Personas.objects.get(email=pk)
        serializer = PersonasSerializer(persona, many=False)
        return Response(serializer.data)
    except:
        return Response({"message": "No existe una persona con este email"})
    

class deletePersona(generics.DestroyAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class UpdatePersonaNatural(generics.RetrieveUpdateAPIView):
    serializer_class = PersonaNaturalPostSerializer
    queryset = Personas.objects.all()


class RegisterPersonaNatural(generics.CreateAPIView):
    serializer_class = PersonaNaturalPostSerializer
    queryset = Personas.objects.all()
    
    
class UpdatePersonaJuridica(generics.RetrieveUpdateAPIView):
    serializer_class = PersonaJuridicaPostSerializer
    queryset = Personas.objects.all()


class RegisterPersonaJuridica(generics.CreateAPIView):
    serializer_class = PersonaJuridicaPostSerializer
    queryset = Personas.objects.all()


# Views for apoderados persona


class getApoderadosPersona(generics.ListAPIView):
    serializer_class = ApoderadoPersonaSerializer
    queryset = ApoderadoPersona.objects.all()


class getApoderadoPersonaById(generics.RetrieveAPIView):
    serializer_class = ApoderadoPersonaSerializer
    queryset = ApoderadoPersona.objects.all()


class deleteApoderadoPersona(generics.DestroyAPIView):
    serializer_class = ApoderadoPersonaSerializer
    queryset = ApoderadoPersona.objects.all()


class updateApoderadoPersona(generics.RetrieveUpdateAPIView):
    serializer_class = ApoderadoPersonaPostSerializer
    queryset = ApoderadoPersona.objects.all()


class registerApoderadoPersona(generics.CreateAPIView):
    serializer_class = ApoderadoPersonaPostSerializer 
    queryset = ApoderadoPersona.objects.all()


# Views for Sucursales Empresas


class getSucursalesEmpresas(generics.ListAPIView):
    serializer_class = SucursalesEmpresasSerializer
    queryset = SucursalesEmpresas.objects.all()


class getSucursalEmpresaById(generics.RetrieveAPIView):
    serializer_class = SucursalesEmpresasSerializer
    queryset = SucursalesEmpresas.objects.all()


class deleteSucursalEmpresa(generics.DestroyAPIView):
    serializer_class = SucursalesEmpresasSerializer
    queryset = SucursalesEmpresas.objects.all()


class updateSucursalEmpresa(generics.RetrieveUpdateAPIView):
    serializer_class = SucursalesEmpresasPostSerializer
    queryset = SucursalesEmpresas.objects.all()


class registerSucursalEmpresa(generics.CreateAPIView):
    serializer_class = SucursalesEmpresasPostSerializer 
    queryset = SucursalesEmpresas.objects.all()
    
"""
# Views for Historico Emails


class getHistoricoEmails(generics.ListAPIView):
    serializer_class = HistoricoEmailsSerializer
    queryset = HistoricoEmails.objects.all()


class getHistoricoEmailById(generics.RetrieveAPIView):
    serializer_class = HistoricoEmailsSerializer
    queryset = HistoricoEmails.objects.all()


class deleteHistoricoEmail(generics.DestroyAPIView):
    serializer_class = HistoricoEmailsSerializer
    queryset = HistoricoEmails.objects.all()


class updateHistoricoEmail(generics.RetrieveUpdateAPIView):
    serializer_class = HistoricoEmailsPostSerializer
    queryset = HistoricoEmails.objects.all()


class registerHistoricoEmail(generics.CreateAPIView):
    serializer_class = HistoricoEmailsPostSerializer 
    queryset = HistoricoEmails.objects.all() 


# Views for Historico Direcciones


class GetHistoricoDirecciones(generics.ListAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionSerializer


class GetHistoricoDireccionById(generics.RetrieveAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionSerializer
    
    
class DeleteHistoricoDireccion(generics.DestroyAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionSerializer


class UpdateHistoricoDireccion(generics.RetrieveUpdateAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionPostSerializer


class RegisterHistoricoDireccion(generics.CreateAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionPostSerializer


# Views for Clases Tercero


class getClasesTercero(generics.ListAPIView):
    queryset = ClasesTercero.objects.all()
    serializer_class = ClasesTerceroSerializer


class getClaseTerceroById(generics.RetrieveAPIView):
    queryset = ClasesTercero.objects.all()
    serializer_class = ClasesTerceroSerializer


class deleteClaseTercero(generics.DestroyAPIView):
    queryset = ClasesTercero.objects.all()
    serializer_class = ClasesTerceroSerializer


class updateClaseTercero(generics.RetrieveUpdateAPIView):
    queryset = ClasesTercero.objects.all()
    serializer_class = ClasesTerceroSerializer


class registerClaseTercero(generics.CreateAPIView):
    queryset = ClasesTercero.objects.all()
    serializer_class = ClasesTerceroSerializer


# Views for Clases Tercero Persona


class getClasesTerceroPersonas(generics.ListAPIView):
    queryset = ClasesTerceroPersona.objects.all()
    serializer_class = ClasesTerceroPersonaSerializer


class getClaseTerceroPersonaById(generics.RetrieveAPIView):
    queryset = ClasesTerceroPersona.objects.all()
    serializer_class = ClasesTerceroPersonaSerializer


class deleteClaseTerceroPersona(generics.DestroyAPIView):
    queryset = ClasesTerceroPersona.objects.all()
    serializer_class = ClasesTerceroPersonaSerializer


class updateClaseTerceroPersona(generics.RetrieveUpdateAPIView):
    queryset = ClasesTerceroPersona.objects.all()
    serializer_class = ClasesTerceroPersonapostSerializer


class registerClaseTerceroPersona(generics.CreateAPIView):
    queryset = ClasesTerceroPersona.objects.all()
    serializer_class = ClasesTerceroPersonapostSerializer
"""
