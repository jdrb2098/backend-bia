import datetime
import copy
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from seguridad.renderers.user_renderers import UserRender
from django.template.loader import render_to_string
from seguridad.utils import Util
from rest_framework import status
from django.db.models import Q
from seguridad.permissions.permissions_user import PermisoActualizarExterno, PermisoActualizarInterno
from seguridad.permissions.permissions_user_over_person import (
    PermisoActualizarPersona, 
    PermisoActualizarTipoDocumento, 
    PermisoBorrarEstadoCivil,
    PermisoBorrarTipoDocumento,
    PermisoConsultarEstadoCivil, 
    PermisoConsultarPersona,
    PermisoConsultarTipoDocumento,
    PermisoCrearEstadoCivil, 
    PermisoCrearPersona, 
    PermisoActualizarEstadoCivil,
    PermisoCrearTipoDocumento,)
from seguridad.models import (
    Personas,
    TipoDocumento,
    EstadoCivil,
    ApoderadoPersona,
    SucursalesEmpresas,
    HistoricoEmails,
    HistoricoDireccion,
    ClasesTercero,
    ClasesTerceroPersona,
    User,
    Modulos,
    Permisos,
    Auditorias
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
    PersonaNaturalInternoUpdateSerializer,
    PersonaNaturalExternoUpdateSerializer,
    PersonaNaturalUpdateUserPermissionsSerializer,
    PersonaJuridicaInternaUpdateSerializer,
    PersonaJuridicaExternaUpdateSerializer,
    PersonaJuridicaUpdateUserPermissionsSerializer,
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


class GetEstadoCivil(generics.ListAPIView):
    serializer_class = EstadoCivilSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarEstadoCivil]
    queryset = EstadoCivil.objects.all()


class GetEstadoCivilById(generics.RetrieveAPIView):
    serializer_class = EstadoCivilSerializer
    queryset = EstadoCivil.objects.all()


class DeleteEstadoCivil(generics.RetrieveDestroyAPIView):
    serializer_class = EstadoCivilSerializer
    permission_classes = [IsAuthenticated, PermisoBorrarEstadoCivil]
    queryset = EstadoCivil.objects.all()
    
    def delete(self, request, pk):
        estado_civil = EstadoCivil.objects.get(cod_estado_civil=pk)
        
        if estado_civil.precargado == False:
            persona = Personas.objects.filter(estado_civil=pk)
            if persona:
                return Response({'detail': 'Ya existe una persona con este estado civil, por ello no es eliminable'})   
            
            estado_civil.delete()    
            return Response({'detail': 'Este estado civil ha sido eliminado exitosamente'})
        else:
            return Response({'detail': 'No puedes eliminar un estado civil precargado'})


class RegisterEstadoCivil(generics.CreateAPIView):
    serializer_class = EstadoCivilPostSerializer
    permission_classes = [IsAuthenticated, PermisoCrearEstadoCivil]
    queryset = EstadoCivil.objects.all()   


class UpdateEstadoCivil(generics.RetrieveUpdateAPIView):
    serializer_class = EstadoCivilPostSerializer
    queryset = EstadoCivil.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarEstadoCivil]

    def put(self, request, pk):
        data = request.data
        estado_civil = EstadoCivil.objects.get(cod_estado_civil=pk)
        
        if estado_civil.precargado == False:
            personas = Personas.objects.filter(estado_civil=pk)
            if personas:
                return Response({'detail': 'Ya existe una persona con este estado civil, por ello no es actualizable'})
            
            estado_civil.cod_estado_civil = data['cod_estado_civil']
            estado_civil.nombre = data['nombre']
            estado_civil.save()

            serializer = self.serializer_class(estado_civil, many=False)
            return Response({'detail': 'Registro actualizado exitosamente', 'data': serializer.data})
        else:
            return Response({'detail': 'Este es un dato precargado en el sistema, no se puede actualizar'})


# Views for Tipo Documento


class GetTipoDocumento(generics.ListAPIView):
    serializer_class = TipoDocumentoSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarTipoDocumento]
    queryset = TipoDocumento.objects.all()


class GetTipoDocumentoById(generics.RetrieveAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()


class DeleteTipoDocumento(generics.RetrieveDestroyAPIView):
    serializer_class = TipoDocumentoSerializer
    permission_classes = [IsAuthenticated, PermisoBorrarTipoDocumento]
    queryset = TipoDocumento.objects.all()
    
    def delete(self, request, pk):
        tipo_documento = TipoDocumento.objects.get(cod_tipo_documento=pk)
        
        if tipo_documento.precargado == False:
            persona = Personas.objects.filter(tipo_documento=pk)
            if persona:
                return Response({'detail': 'Ya existe una persona con este estado civil, por ello no es eliminable'})   
            
            tipo_documento.delete()    
            return Response({'detail': 'Este estado civil ha sido eliminado exitosamente'})
        else:
            return Response({'detail': 'No puedes eliminar un estado civil precargado'})


class RegisterTipoDocumento(generics.CreateAPIView):
    serializer_class = TipoDocumentoPostSerializer
    permission_classes = [IsAuthenticated, PermisoCrearTipoDocumento]
    queryset = TipoDocumento.objects.all()


class UpdateTipoDocumento(generics.RetrieveUpdateAPIView):
    serializer_class = TipoDocumentoPostSerializer
    queryset = TipoDocumento.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarTipoDocumento]

    def put(self, request, pk):
        data = request.data
        tipo_documento = TipoDocumento.objects.get(cod_tipo_documento=pk)
        
        if tipo_documento.precargado == False:
            personas = Personas.objects.filter(tipo_documento=pk)
            if personas:
                return Response({'detail': 'Ya existe una persona con este tipo de documento, por ello no es actualizable'})
            
            tipo_documento.cod_tipo_documento = data['cod_tipo_documento']
            tipo_documento.nombre = data['nombre']
            tipo_documento.save()

            serializer = self.serializer_class(tipo_documento, many=False)
            return Response({'detail': 'Registro actualizado exitosamente', 'data': serializer.data})
        else:
            return Response({'detail': 'Este es un dato precargado en el sistema, no se puede actualizar'})
            

# Views for Personas

class GetPersonas(generics.ListAPIView):
    serializer_class = PersonasSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarPersona]
    queryset = Personas.objects.all()



@api_view(['GET'])
def getPersonaByEmail(pk):
    try:
        persona = Personas.objects.get(email=pk)
        serializer = PersonasSerializer(persona, many=False)
        return Response(serializer.data)
    except:
        return Response({"message": "No existe una persona con este email"})


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


class GetPersonaNatural(generics.ListAPIView):
    serializer_class=PersonaNaturalSerializer
    permission_classes=[IsAuthenticated, PermisoConsultarPersona]
    queryset=Personas.objects.filter(tipo_persona='N')       
    filter_backends=[filters.SearchFilter]
    search_fields=['primer_nombre','primer_apellido']


class GetPersonaJuridica(generics.ListAPIView):
    serializer_class=PersonaJuridicaSerializer
    queryset=Personas.objects.filter(tipo_persona='J')
    filter_backends=[filters.SearchFilter]
    search_fields=['razon_social','nombre_comercial']


class deletePersona(generics.DestroyAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()


class UpdatePersonaNaturalInternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaNaturalInternoUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarInterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)
            
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')
            
            try:
                #personita = Personas.objects.get(email_empresarial=email_principal)
                personita = Personas.objects.get(email=email_secundario)
                if personita: 
                    #Personas.objects.get(email_empresarial=email_principal)
                    return Response({'detail': 'Ya existe una persona con este email como opcion secundaria'})
            except:
                persona_serializada.save()
                persona = Personas.objects.get(email=email_principal)

                sms = 'Hola ' + persona.primer_nombre + ' ' + persona.primer_apellido + ' te informamos que ha sido exitosa la actualización de tus datos como PERSONA NATURAL'
                context = {'primer_nombre': persona.primer_nombre, 'primer_apellido': persona.primer_apellido}
                template = render_to_string(('email-update-personanatural-interna.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.primer_nombre
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
                try:
                    print(persona)
                    print(persona.primer_nombre)
                    print(persona.primer_apellido)
                    print(persona.email)
                    print(persona.telefono_celular)
                    print(persona.email_empresarial)
                    Util.send_email(data)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el email, verificar servicio'})
                try:
                    Util.send_sms(persona.telefono_celular, sms)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'})
                return Response({'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data})
        else:
            return Response({'detail': 'No se encontró ninguna persona'})


class UpdatePersonaNaturalExternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaNaturalExternoUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarExterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            #persona_serializada = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            persona_serializada.is_valid(raise_exception=True) 

            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')
           
            try:
                #personita = Personas.objects.get(email_empresarial=email_principal)
                personita = Personas.objects.get(email=email_secundario)
                if personita: 
                    #Personas.objects.get(email_empresarial=email_principal)
                    return Response({'detail': 'Ya existe una persona con este email como opcion secundaria'})
            except:
                persona_serializada.save()
                persona = Personas.objects.get(email=email_principal)

                sms = 'Hola ' + persona.primer_nombre + ' ' + persona.primer_apellido + ' te informamos que ha sido exitosa la actualización de tus datos como PERSONA NATURAL'
                context = {'primer_nombre': persona.primer_nombre, 'primer_apellido': persona.primer_apellido}
                template = render_to_string(('email-update-personanatural-externa.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.primer_nombre
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
                try:
                    Util.send_email(data)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el email, verificar servicio'})
                try:
                    Util.send_sms(persona.telefono_celular, sms)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'})
                return Response({'detail': 'Persona actualizada y notificada correctamente', 'data': data})
        else:
            return Response({'detail': 'No se encontró ninguna persona'})


class UpdatePersonaNaturalByUserWithPermissions(generics.RetrieveUpdateAPIView):
    http_method_names= ['patch']
    serializer_class = PersonaNaturalUpdateUserPermissionsSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarPersona]
    queryset = Personas.objects.all()
    
    def patch(self, request, pk):
        persona_por_actualizar = Personas.objects.get(id_persona=pk)
        
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)
            
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')

            try:
                #personita = Personas.objects.get(email_empresarial=email_principal)
                personita = Personas.objects.get(email=email_secundario)
                if personita: 
                    #Personas.objects.get(email_empresarial=email_principal)
                    return Response({'detail': 'Ya existe una persona con este email como opcion secundaria'})
            except:
                persona_serializada.save()
                persona = Personas.objects.get(email=email_principal)

                sms = 'Hola ' + persona.primer_nombre + ' ' + persona.primer_apellido + ' te informamos que ha sido exitosa la actualización de tus datos como PERSONA NATURAL'
                context = {'primer_nombre': persona.primer_nombre, 'primer_apellido': persona.primer_apellido}
                template= render_to_string(('email-update-personanatural-byuser-withpermissions.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.primer_nombre
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
                try:
                    Util.send_email(data)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el email, verificar servicio'})
                try:
                    Util.send_sms(persona.telefono_celular, sms)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'})
                return Response({'detail': 'Persona actualizada y notificada correctamente', 'data': data})
        else:
            return Response({'detail': 'No se encontró ninguna persona'})


class UpdatePersonaJuridicaInternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaJuridicaInternaUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarInterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)
            
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')

            try:
                #personita = Personas.objects.get(email_empresarial=email_principal)
                personita = Personas.objects.get(email=email_secundario)
                if personita: 
                    #Personas.objects.get(email_empresarial=email_principal)
                    return Response({'detail': 'Ya existe una persona con este email como opcion secundaria'})
            except:
                persona_serializada.save()
                persona = Personas.objects.get(email=email_principal)

                sms = 'Hola ' + persona.razon_social + ' te informamos que ha sido exitosa la actualización de tus datos como PERSONA JURIDICA'
                context = {'razon_social': persona.razon_social}
                template = render_to_string(('email-update-personajuridica-interno.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.razon_social
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email} 
                try:
                    Util.send_email(data)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el email, verificar servicio'})
                try:
                    Util.send_sms(persona.telefono_celular_empresa, sms)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'})
                return Response({'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data})
        else:
            return Response({'detail': 'No se encontró ninguna persona'})


class UpdatePersonaJuridicaExternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaJuridicaExternaUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarExterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)
            
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')
            
            try:
                #personita = Personas.objects.get(email_empresarial=email_principal)
                personita = Personas.objects.get(email=email_secundario)
                if personita: 
                    #Personas.objects.get(email_empresarial=email_principal)
                    return Response({'detail': 'Ya existe una persona con este email como opcion secundaria'})
            except:
                persona_serializada.save()
                persona = Personas.objects.get(email=email_principal)
                
                sms = 'Hola ' + persona.razon_social + ' te informamos que ha sido exitosa la actualización de tus datos como PERSONA JURIDICA'
                context = {'razon_social': persona.razon_social}
                template = render_to_string(('email-update-personajuridica-externo.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.razon_social
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email} 
                try:
                    Util.send_email(data)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el email, verificar servicio'})
                try:
                    Util.send_sms(persona.telefono_celular_empresa, sms)
                except:
                    return Response({'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'})
                return Response({'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data})
        else:
            return Response({'detail': 'No se encontró ninguna persona'})


class UpdatePersonaJuridicaByUserWithPermissions(generics.RetrieveUpdateAPIView):
    http_method_names= ['patch']
    serializer_class = PersonaJuridicaUpdateUserPermissionsSerializer
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
                Util.send_sms(persona.telefono_celular_empresa, sms)
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
    
    def delete(self,request,pk):
        sucursal=SucursalesEmpresas.objects.filter(id_sucursal_empresa=pk).first()
        if sucursal:
            sucursal.delete()
            usuario=request.user.id_usuario
            user = User.objects.get(id_usuario = usuario)
            modulo = Modulos.objects.get(id_modulo = 1)
            permiso = Permisos.objects.get(cod_permiso = 'BO')
            
            descripcion = "Sucursal:" + str(pk)+ "Sucursal:" + str(sucursal.sucursal)+ "."
            direccion=Util.get_client_ip(request)
            Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "TRSV", dirip=direccion, descripcion=descripcion)  
            #headers = self.get_success_headers(sucursal.data)
            return Response({'detail':'la sucursal empresa fue eliminada'})
        else:
            return Response({'detail':'No existe sucursal'})
            
class updateSucursalEmpresa(generics.RetrieveUpdateAPIView):
    serializer_class = SucursalesEmpresasPostSerializer
    queryset = SucursalesEmpresas.objects.all()
    permission_classes = [IsAuthenticated]
    
    def put(self, request,pk=None):
        print(request.user)
        sucursal = SucursalesEmpresas.objects.filter(id_sucursal_empresa= pk).first()
        previous_sucursal = copy.copy(sucursal)
        if sucursal:
            sucursal_serializer = self.serializer_class(sucursal, data=request.data)
            sucursal_serializer.is_valid(raise_exception=True)
            sucursal_serializer.save()
            usuario=request.user.id_usuario
            user = User.objects.get(id_usuario = usuario)
            modulo = Modulos.objects.get(id_modulo = 1)
            permiso = Permisos.objects.get(cod_permiso = 'AC')
            
            valores_actualizados = ""
            del previous_sucursal.__dict__["_state"]
            del previous_sucursal.__dict__["_django_version"]  
            for field, value in previous_sucursal.__dict__.items():
                    new_value = getattr(sucursal,field)
                    if value != new_value:
                        valores_actualizados += field + "_anterior:" + str(value) + ";" + field + "_nuevo:" + str(new_value) + ";"
                        
            descripcion = "Sucursal id:" + str(sucursal.id_sucursal_empresa)+ "Sucursal:" + str(sucursal.sucursal)+ "."
            direccion=Util.get_client_ip(request)
            Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "TRSV", dirip=direccion, descripcion=descripcion, valores_actualizados=valores_actualizados)  
            return Response({'detail':'la sucursal empresa actualizada'})
        else:
            return Response({'detail':'No existe sucursal'})

class registerSucursalEmpresa(generics.CreateAPIView):
    serializer_class = SucursalesEmpresasPostSerializer 
    queryset = SucursalesEmpresas.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializador=serializer.save()
        usuario = request.user.id_usuario
        user = User.objects.get(id_usuario = usuario)
        modulo = Modulos.objects.get(id_modulo = 1)
        permiso = Permisos.objects.get(cod_permiso = 'CR')
        
        currentdate = datetime.date.today()
        formatDate = currentdate.strftime("%d/%m/%y")
        
        
        descripcion = "Sucursal:" + str(serializador.pk)+  ";" + "fecha:" + formatDate + ";" + "observaciones:Registro de otra sucursal" + ";" + "NumeroSucursal:"+ str(serializador.numero_sucursal) + "Sucursal:" + str(serializador.sucursal)+"."
        direccion=Util.get_client_ip(request)
        Auditorias.objects.create(id_usuario = user, id_modulo = modulo, id_cod_permiso_accion = permiso, subsistema = "TRSV", dirip=direccion, descripcion=descripcion)  
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

        # descripcion = "idUsuario:" + str(serializer_response.pk) + ";" + "fecha:" + formatDate + ";" + "observaciones:Registro de otro usuario" + ";" + "nombreUsuario:"+ serializer_response.nombre_de_usuario + "."
        
# Views for Historico Emails
class getHistoricoEmails(generics.ListAPIView):
    serializer_class = HistoricoEmailsSerializer
    queryset = HistoricoEmails.objects.all()


# Views for Historico Direcciones
class GetHistoricoDirecciones(generics.ListAPIView):
    queryset = HistoricoDireccion.objects.all()
    serializer_class = HistoricoDireccionSerializer

    
"""    
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
