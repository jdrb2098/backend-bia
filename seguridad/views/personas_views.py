from django.shortcuts import render
from rest_framework import generics
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

from rest_framework import status
from seguridad.serializers.personas_serializers import (
    EstadoCivilSerializer,
    TipoDocumentoSerializer,
    PersonasSerializer,
    PersonasPostSerializer,
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


class updateEstadoCivil(generics.RetrieveUpdateAPIView):
    serializer_class = EstadoCivilSerializer
    queryset = EstadoCivil.objects.all()


class registerEstadoCivil(generics.CreateAPIView):
    serializer_class = EstadoCivilSerializer
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


class updateTipoDocumento(generics.RetrieveUpdateAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()


class registerTipoDocumento(generics.CreateAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()


# Views for Personas


class getPersonas(generics.ListAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class getPersonaById(generics.RetrieveAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class deletePersona(generics.DestroyAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class UpdatePersona(generics.RetrieveUpdateAPIView):
    serializer_class = PersonasPostSerializer
    queryset = Personas.objects.all()


class RegisterPersona(generics.CreateAPIView):
    serializer_class = PersonasPostSerializer
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

