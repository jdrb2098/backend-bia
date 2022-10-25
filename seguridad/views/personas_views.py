from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from seguridad.permissions.permissions_persona import PermisoActualizarPersona, PermisoConsultarPersona
from rest_framework.generics  import RetrieveUpdateAPIView, ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from seguridad.renderers.user_renderers import UserRender
from django.template.loader import render_to_string
from seguridad.utils import Util
from rest_framework import status
from django.db.models import Q
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
            

class registerTipoDocumento(generics.CreateAPIView):
    serializer_class = TipoDocumentoPostSerializer
    queryset = TipoDocumento.objects.all()


# Views for Personas

class getPersonas(generics.ListAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class GetPersonaNatural(generics.ListAPIView):
    serializer_class=PersonaNaturalSerializer
    permission_classes=[IsAuthenticated,PermisoConsultarPersona]
    queryset=Personas.objects.filter(tipo_persona='N')       
    filter_backends=[filters.SearchFilter]
    search_fields=['primer_nombre','primer_apellido']


class GetPersonasByTipoDocumentoAndNumeroDocumento(generics.GenericAPIView):
    serializer_class = PersonasSerializer
    
    def get(self, request, tipodocumento, numerodocumento):
        try:
            queryset = Personas.objects.get(Q(tipo_documento = tipodocumento) & Q(numero_documento=numerodocumento))  
            persona_serializer = self.serializer_class(queryset)
            return Response({'data': persona_serializer.data})
        except:
            return Response({'detail': 'No encontró ninguna persona con los parametros ingresados'})


class GetPersonaNaturalByTipoDocumentoAndNumeroDocumento(generics.ListAPIView):
    serializer_class = PersonaNaturalSerializer

    def get(self, request, tipodocumento, numerodocumento):
        try:
            queryset = Personas.objects.get(Q(tipo_persona='N') & Q(tipo_documento=tipodocumento) & Q(numero_documento=numerodocumento))
            serializador = self.serializer_class(queryset)
            return Response({'data': serializador.data})
        except:
            return Response({'data': 'No encontró ninguna persona con los parametros ingresados'})

class GetPersonaJuridicaByTipoDocumentoAndNumeroDocumento(generics.GenericAPIView):
    serializer_class = PersonaJuridicaSerializer
    
    def get(self, request, tipodocumento, numerodocumento):
        try:
            queryset = Personas.objects.get(Q(tipo_persona='J') & Q(tipo_documento = tipodocumento) & Q(numero_documento=numerodocumento))  
            persona_serializer = self.serializer_class(queryset)
            return Response({'data': persona_serializer.data})
        except:
            return Response({'detail': 'No encontró ninguna persona con los parametros ingresados'})
        
class GetPersonaJuridica(generics.ListAPIView):
    serializer_class=PersonaJuridicaSerializer
    queryset=Personas.objects.filter(tipo_persona='J')
    filter_backends=[filters.SearchFilter]
    search_fields=['razon_social','nombre_comercial']


@api_view(['GET'])
def getPersonaByEmail(pk):
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
    permission_classes = [IsAuthenticated, PermisoActualizarPersona]
    queryset = Personas.objects.all()


class RegisterPersonaNatural(generics.CreateAPIView):
    serializer_class = PersonaNaturalPostSerializer
    
    def post(self, request):
        persona = request.data
        serializer = self.serializer_class(data=persona)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        try:
            Personas.objects.get(email_empresarial = email)
            return Response({'detail': 'Ya existe un pelao con este email como opción secundaria'})
        except:
            serializer.save()
            persona = Personas.objects.get(email = email)
    
            sms = 'Hola '+ persona.primer_nombre + ' ' + persona.primer_apellido + ' te informamos que has sido registrado como PERSONA NATURAL en el portal Bia Cormacarena \n Ahora puedes crear tu usuario, hazlo en el siguiente link' + 'url'  
            context = {'primer_nombre': persona.primer_nombre, 'primer_apellido':  persona.primer_apellido}
            template = render_to_string(('email-register-personanatural.html'), context)
            subject = 'Registro exitoso ' + persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
            try:
                Util.send_email(data)
            except:
                return Response({'detail': 'Se guardo la persona pero no se pudo enviar el email, verificar servicio'})
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'detail': 'Se guardo la persona pero no se pudo enviar el sms, verificar numero'})
            return Response({'status': status.HTTP_201_CREATED, 'detail': serializer.data})

class UpdatePersonaJuridica(generics.RetrieveUpdateAPIView):
    serializer_class = PersonaJuridicaPostSerializer
    queryset = Personas.objects.all()


class RegisterPersonaJuridica(generics.CreateAPIView):
    serializer_class = PersonaJuridicaPostSerializer

    def post(self, request):
        persona = request.data
        serializer = self.serializer_class(data=persona)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        try: 
            Personas.objects.get(email_empresarial=email)
            return Response({'detail': 'Ya existe un pelao con este email como opción secundaria'})
        except: 
            serializer.save() 
            persona = Personas.objects.get(email=email)

            sms = 'Hola '+ persona.razon_social  + ' te informamos que has sido registrado como PERSONA JURIDICA en el portal Bia Cormacarena \n Ahora puedes crear tu usuario, hazlo en el siguiente link' + 'url'  
            context = {'razon_social': persona.razon_social, 'nombre_comercial':  persona.nombre_comercial}
            template = render_to_string(('email-register-personajuridica.html'), context)
            subject = 'Registro exitoso ' + persona.razon_social
            data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
            try: 
                Util.send_email(data)
            except:
                return Response({'detail': 'Se guardo la persona pero no se pudo enviar el email, verificar servicio'})
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'detail':'Se guardo la persona pero no se pudo enviar el sms, verificar numero'})
            
            return Response({'status': status.HTTP_201_CREATED, 'detail': serializer.data})


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


# Views for Historico Direcciones


class GetHistoricoDirecciones(generics.ListAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionSerializer


class GetHistoricoDireccionById(generics.RetrieveAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionSerializer
    
    
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
