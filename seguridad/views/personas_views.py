from asyncio import exceptions
import datetime
import copy
from signal import raise_signal
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
    PermisoCrearTipoDocumento
    )
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
    EstadoCivilPutSerializer,
    TipoDocumentoSerializer,
    TipoDocumentoPutSerializer,
    PersonasSerializer,
    PersonaNaturalSerializer,
    PersonaJuridicaSerializer,
    PersonaNaturalPostSerializer,
    PersonaJuridicaPostSerializer,
    PersonaNaturalPostByUserSerializer,
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
    HistoricoDireccionSerializer,
    ClasesTerceroSerializer,
    ClasesTerceroPersonaSerializer,
    ClasesTerceroPersonapostSerializer,
    GetPersonaJuridicaByRepresentanteLegalSerializer
)

# Views for Estado Civil


class GetEstadoCivil(generics.ListAPIView):
    serializer_class = EstadoCivilSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarEstadoCivil]
    queryset = EstadoCivil.objects.filter(activo=True)


class GetEstadoCivilById(generics.RetrieveAPIView):
    serializer_class = EstadoCivilSerializer
    queryset = EstadoCivil.objects.all()


class DeleteEstadoCivil(generics.RetrieveDestroyAPIView):
    serializer_class = EstadoCivilSerializer
    permission_classes = [IsAuthenticated, PermisoBorrarEstadoCivil]
    queryset = EstadoCivil.objects.all()
    
    def delete(self, request, pk):
        estado_civil = EstadoCivil.objects.filter(cod_estado_civil=pk).first()
        if estado_civil:
            pass 
            if estado_civil.precargado == False:
                if estado_civil.item_ya_usado == True:
                    return Response({'success': False,'detail': 'Este estado civil ya está siendo usado, por lo cúal no es eliminable'}, status=status.HTTP_403_FORBIDDEN)   
  
                estado_civil.delete()    
                return Response({'success': True, 'detail': 'Este estado civil ha sido eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'success': False, 'detail': 'No puedes eliminar un estado civil precargado'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success': False, 'detail':'No existe el estado civil'}, status=status.HTTP_404_NOT_FOUND)


class RegisterEstadoCivil(generics.CreateAPIView):
    serializer_class = EstadoCivilSerializer
    permission_classes = [IsAuthenticated, PermisoCrearEstadoCivil]
    queryset = EstadoCivil.objects.all()   


class UpdateEstadoCivil(generics.RetrieveUpdateAPIView):
    serializer_class = EstadoCivilPutSerializer
    queryset = EstadoCivil.objects.all()
    permission_classes = [IsAuthenticated, PermisoActualizarEstadoCivil]

    def put(self, request, pk):
        estado_civil = EstadoCivil.objects.filter(cod_estado_civil=pk).first()

        if estado_civil:
            if estado_civil.precargado == False:
                if estado_civil.item_ya_usado == True:
                    return Response({'success':False, 'detail': 'Este estado civil ya está siendo usado, por lo cúal no es actualizable'}, status=status.HTTP_403_FORBIDDEN)
    
                serializer = self.serializer_class(estado_civil, data=request.data, many=False)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'success': True,'detail': 'Registro actualizado exitosamente', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'detail': 'No puede actualizar un estado civil precargado'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success': False, 'detail': 'No existe un estado civil con estos parametros'}, status=status.HTTP_404_NOT_FOUND)


# Views for Tipo Documento


class GetTipoDocumento(generics.ListAPIView):
    serializer_class = TipoDocumentoSerializer
    # permission_classes = [IsAuthenticated, PermisoConsultarTipoDocumento]
    queryset = TipoDocumento.objects.filter(activo=True)


class GetTipoDocumentoById(generics.RetrieveAPIView):
    serializer_class = TipoDocumentoSerializer
    queryset = TipoDocumento.objects.all()


class DeleteTipoDocumento(generics.RetrieveDestroyAPIView):
    serializer_class = TipoDocumentoSerializer
    # permission_classes = [IsAuthenticated, PermisoBorrarTipoDocumento]
    queryset = TipoDocumento.objects.all()
    
    def delete(self, request, pk):
        tipo_documento = TipoDocumento.objects.filter(cod_tipo_documento=pk).first()
        if tipo_documento:
            if tipo_documento.precargado == False:
                if tipo_documento.item_ya_usado == True:
                    return Response({'success': False,'detail': 'Este tipo de documento ya está siendo usado, por lo cúal no es eliminable'}, status=status.HTTP_403_FORBIDDEN)   
                
                tipo_documento.delete()    
                return Response({'success': True,'detail': 'Este tipo de documento ha sido eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'success': False,'detail': 'No puedes eliminar un tipo de documento precargado'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success':False, 'detail': 'No se encontró ningún tipo de documento con estos parámetros'}, status=status.HTTP_404_NOT_FOUND)


class RegisterTipoDocumento(generics.CreateAPIView):
    serializer_class = TipoDocumentoSerializer
    # permission_classes = [IsAuthenticated, PermisoCrearTipoDocumento]
    queryset = TipoDocumento.objects.all()


class UpdateTipoDocumento(generics.RetrieveUpdateAPIView):
    serializer_class = TipoDocumentoPutSerializer
    queryset = TipoDocumento.objects.all()
    # permission_classes = [IsAuthenticated, PermisoActualizarTipoDocumento]

    def put(self, request, pk):
        tipo_documento = TipoDocumento.objects.filter(cod_tipo_documento=pk).first()
        if tipo_documento:
            if tipo_documento.precargado == False:
                if tipo_documento.item_ya_usado == True:
                    return Response({'success': False,'detail': 'Este tipo de documento ya está siendo usado, por lo cúal no es actualizable'}, status=status.HTTP_403_FORBIDDEN)
                
                serializer = self.serializer_class(tipo_documento, data=request.data, many=False)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'success': True,'detail': 'Registro actualizado exitosamente', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'detail': 'Este es un dato precargado en el sistema, no se puede actualizar'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'success': False, 'detail':'No se encontró ningún tipo de documento con estos parámetros'}, status=status.HTTP_404_NOT_FOUND)
            

# Views for Personas

class GetPersonas(generics.ListAPIView):
    serializer_class = PersonasSerializer
    permission_classes = [IsAuthenticated, PermisoConsultarPersona]
    queryset = Personas.objects.all()


@api_view(['GET'])
def getPersonaByEmail(request, pk):
    try:
        persona = Personas.objects.get(email=pk)
        serializer = PersonasSerializer(persona, many=False)
        return Response({'success': True, 'data': serializer.data,},  status=status.HTTP_200_OK)
    except:
        return Response({'success': False ,"message": "No existe una persona con este email"}, status=status.HTTP_404_NOT_FOUND)


class GetPersonasByTipoDocumentoAndNumeroDocumento(generics.GenericAPIView):
    serializer_class = PersonasSerializer
    
    def get(self, request, tipodocumento, numerodocumento):
        try:
            queryset = Personas.objects.get(Q(tipo_documento = tipodocumento) & Q(numero_documento=numerodocumento))  
            persona_serializer = self.serializer_class(queryset)
            return Response({'success': True,'data': persona_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, 'detail': 'No encontró ninguna persona con los parametros ingresados'}, status=status.HTTP_404_NOT_FOUND)


class GetPersonasByID(generics.GenericAPIView):
    serializer_class = PersonasSerializer
    queryset = Personas.objects.all()
    
    def get(self, request, pk):
        try:
            queryset = Personas.objects.get(id_persona=pk)  
            persona_serializer = self.serializer_class(queryset)
            return Response({'success': True,'data': persona_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False,'detail': 'No encontró ninguna persona con los parametros ingresados'}, status=status.HTTP_404_NOT_FOUND)


class GetPersonaNaturalByTipoDocumentoAndNumeroDocumento(generics.ListAPIView):
    serializer_class = PersonaNaturalSerializer

    def get(self, request, tipodocumento, numerodocumento):
        try:
            queryset = Personas.objects.get(Q(tipo_persona='N') & Q(tipo_documento=tipodocumento) & Q(numero_documento=numerodocumento))
            serializador = self.serializer_class(queryset)
            return Response({'success': True,'data': serializador.data}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False,'data': 'No encontró ninguna persona con los parametros ingresados'}, status=status.HTTP_404_NOT_FOUND)

class GetPersonaJuridicaByTipoDocumentoAndNumeroDocumento(generics.GenericAPIView):
    serializer_class = PersonaJuridicaSerializer
    
    def get(self, request, tipodocumento, numerodocumento):
        try:
            queryset = Personas.objects.get(Q(tipo_persona='J') & Q(tipo_documento = tipodocumento) & Q(numero_documento=numerodocumento))  
            persona_serializer = self.serializer_class(queryset)
            return Response({'success': True, 'data': persona_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, 'detail': 'No encontró ninguna persona con los parametros ingresados'}, status=status.HTTP_404_NOT_FOUND)


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
    
class GetPersonaJuridicaByRepresentanteLegal(generics.ListAPIView):
    serializer_class=GetPersonaJuridicaByRepresentanteLegalSerializer
    
    permission_classes=[IsAuthenticated]
    queryset = Personas.objects.all()
    
    def get(self,request):
        persona= request.user.persona
        representante_legal=Personas.objects.filter(representante_legal=persona)
        if representante_legal:
            persona_serializada = self.serializer_class(representante_legal,many=True)
            return Response({'detail':persona_serializada.data})
        return Response({'success':False,'detail':'No está asociado en ninguna empresa como representante legal'},status=status.HTTP_404_NOT_FOUND)
        
class UpdatePersonaNaturalInternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaNaturalInternoUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarInterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        previous_persona = copy.copy(persona_por_actualizar)
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)

            #Marcar estado civil como item ya usado
            estado_civil = persona_serializada.validated_data.get('estado_civil')
            if estado_civil:
                try:
                    estado_civil_instance = EstadoCivil.objects.get(cod_estado_civil=estado_civil.cod_estado_civil)
                    if estado_civil_instance.item_ya_usado == False:
                        estado_civil_instance.item_ya_usado = True
                        estado_civil_instance.save()
                        pass
                except:
                    return Response({'success': False, 'detail': 'No existe el estado civil que está ingresando'}, status=status.HTTP_400_BAD_REQUEST)
            
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')

            #Validación emails dns
            validate_email = Util.validate_dns(email_principal)
            if validate_email == False:
                return Response({'success': False, 'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            if email_secundario:
                validate_second_email = Util.validate_dns(email_secundario)
                if validate_second_email == False:
                    return Response({'success': False, 'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            #Validación emails entrantes vs existentes            
            persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
            if len(persona_email_validate):
                return Response({'success': False, 'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializador = persona_serializada.save()

                # auditoria actualizar persona
                usuario = request.user.id_usuario
                direccion=Util.get_client_ip(request)
                descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "PrimerNombre": str(serializador.primer_nombre), "PrimerApellido": str(serializador.primer_apellido)}
                valores_actualizados = {'current': persona_por_actualizar, 'previous': previous_persona}

                auditoria_data = {
                    "id_usuario" : usuario,
                    "id_modulo" : 1,
                    "cod_permiso": "AC",
                    "subsistema": 'TRSV',
                    "dirip": direccion,
                    "descripcion": descripcion, 
                    "valores_actualizados": valores_actualizados
                }
                Util.save_auditoria(auditoria_data)

                #Enviar SMS y Email
                persona = Personas.objects.get(email=email_principal)

                sms = 'Actualizacion exitosa de persona en Cormacarena.'
                context = {'primer_nombre': persona.primer_nombre, 'primer_apellido': persona.primer_apellido}
                template = render_to_string(('email-update-personanatural-interna.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.primer_nombre
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
                Util.send_email(data)
                try:
                    Util.send_sms(persona.telefono_celular, sms)
                except:
                    return Response({'success': True, 'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar servicio'}, status=status.HTTP_201_CREATED)
                
                return Response({'success':True, 'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'detail': 'No se encontró ninguna persona'}, status=status.HTTP_404_NOT_FOUND)


class UpdatePersonaNaturalExternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaNaturalExternoUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarExterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        previous_persona = copy.copy(persona_por_actualizar)
        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)

            #Marcar estado civil como item ya usado
            estado_civil = persona_serializada.validated_data.get('estado_civil')
            if estado_civil:
                try:
                    estado_civil_instance = EstadoCivil.objects.get(cod_estado_civil=estado_civil.cod_estado_civil)
                    if estado_civil_instance.item_ya_usado == False:
                        estado_civil_instance.item_ya_usado = True
                        estado_civil_instance.save()
                        pass
                except:
                    return Response({'success': False, 'detail': 'No existe el estado civil que está ingresando'}, status=status.HTTP_400_BAD_REQUEST) 

            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')
            
             #Validación emails dns
            validate_email = Util.validate_dns(email_principal)
            if validate_email == False:
                return Response({'success': False, 'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            if email_secundario:
                validate_second_email = Util.validate_dns(email_secundario)
                if validate_second_email == False:
                    return Response({'success': False, 'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validación emails entrantes vs existentes
            persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
            if len(persona_email_validate):
                return Response({'success': False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializador = persona_serializada.save()

                # auditoria actualizar persona
                usuario = request.user.id_usuario
                direccion=Util.get_client_ip(request)
                descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "PrimerNombre": str(serializador.primer_nombre), "PrimerApellido": str(serializador.primer_apellido)}
                valores_actualizados = {'current': persona_por_actualizar, 'previous': previous_persona}

                auditoria_data = {
                    "id_usuario" : usuario,
                    "id_modulo" : 1,
                    "cod_permiso": "AC",
                    "subsistema": 'TRSV',
                    "dirip": direccion,
                    "descripcion": descripcion, 
                    "valores_actualizados": valores_actualizados
                }
                Util.save_auditoria(auditoria_data)

                #Envio SMS y EMAIL
                persona = Personas.objects.get(email=email_principal)

                sms = 'Actualizacion exitosa de persona natural en Cormacarena.'
                context = {'primer_nombre': persona.primer_nombre, 'primer_apellido': persona.primer_apellido}
                template = render_to_string(('email-update-personanatural-externa.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.primer_nombre
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
                Util.send_email(data)
                try:
                    Util.send_sms(persona.telefono_celular, sms)
                except:
                    return Response({'success': True, 'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'}, status=status.HTTP_201_CREATED)
                return Response({'success': True, 'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False,'detail': 'No se encontró ninguna persona'}, status=status.HTTP_404_NOT_FOUND)


class UpdatePersonaNaturalByUserWithPermissions(generics.RetrieveUpdateAPIView):
    http_method_names= ['patch']
    serializer_class = PersonaNaturalUpdateUserPermissionsSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarPersona]
    queryset = Personas.objects.all()

    def patch(self, request, tipodocumento, numerodocumento):
        try: 
            persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipodocumento) & Q(numero_documento=numerodocumento) & Q(tipo_persona='N'))
            previous_persona = copy.copy(persona_por_actualizar)
            
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            try:    
                persona_serializada.is_valid(raise_exception=True)
                try:
                    #Marcar estado civil como item ya usado
                    estado_civil = persona_serializada.validated_data.get('estado_civil')
                    if estado_civil:
                        try:
                            estado_civil_instance = EstadoCivil.objects.get(cod_estado_civil=estado_civil.cod_estado_civil)
                            if estado_civil_instance.item_ya_usado == False:
                                estado_civil_instance.item_ya_usado = True
                                estado_civil_instance.save()
                                pass
                        except:
                            return Response({'success': False, 'detail': 'No existe el estado civil que está ingresando'}, status=status.HTTP_400_BAD_REQUEST) 

                    email_principal = persona_serializada.validated_data.get('email')
                    email_secundario = persona_serializada.validated_data.get('email_empresarial')

                    #Validación emails dns
                    validate_email = Util.validate_dns(email_principal)
                    if validate_email == False:
                        return Response({'success': False, 'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

                    if email_secundario:
                        validate_second_email = Util.validate_dns(email_secundario)
                        if validate_second_email == False:
                            return Response({'success': False, 'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    #Validación emails entrantes vs existentes
                    persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
                    if len(persona_email_validate):
                        return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        serializador = persona_serializada.save()
                        
                        # auditoria actualizar persona
                        usuario = request.user.id_usuario
                        direccion=Util.get_client_ip(request)
                        descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "PrimerNombre": str(serializador.primer_nombre), "PrimerApellido": str(serializador.primer_apellido)}
                        valores_actualizados = {'current': persona_por_actualizar, 'previous': previous_persona}

                        auditoria_data = {
                            "id_usuario" : usuario,
                            "id_modulo" : 1,
                            "cod_permiso": "AC",
                            "subsistema": 'TRSV',
                            "dirip": direccion,
                            "descripcion": descripcion, 
                            "valores_actualizados": valores_actualizados
                        }
                        Util.save_auditoria(auditoria_data)
                        
                        #SMS y EMAILS
                        persona = Personas.objects.get(email=email_principal)
                        
                        sms = 'Actualizacion exitosa de persona Natural en Cormacarena por administrador.'
                        context = {'primer_nombre': persona.primer_nombre, 'primer_apellido': persona.primer_apellido}
                        template= render_to_string(('email-update-personanatural-byuser-withpermissions.html'), context)
                        subject = 'Actualización de datos exitosa ' + persona.primer_nombre
                        data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
                        Util.send_email(data)
                        try:
                            Util.send_sms(persona.telefono_celular, sms)
                        except:
                            return Response({'success': True, 'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'}, status=status.HTTP_201_CREATED)
                        return Response({'success':True,'message': 'Persona actualizada y notificada exitosamente', 'data': persona_serializada.data}, status=status.HTTP_201_CREATED)
                except:
                    return Response({'success':False,'detail': 'No pudo obtener el email principal y secundario que está intentando añadir'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'success': False,'detail': 'Revisar parámetros de ingreso de información, el email debe ser único, debe tener telefono celular y ubicación georeferenciada'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'success':False,'detail': 'No existe ninguna persona con estos datos, por favor verificar'}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonaJuridicaInternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaJuridicaInternaUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarInterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        previous_persona = copy.copy(persona_por_actualizar)

        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)

                    
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')

            #Validación emails dns
            validate_email = Util.validate_dns(email_principal)
            if validate_email == False:
                return Response({'success':False,'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            if email_secundario:
                validate_second_email = Util.validate_dns(email_secundario)
                if validate_second_email == False:
                    return Response({'success':False,'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            #Verificación emails entrantes vs salientes
            persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
            if len(persona_email_validate):    
                return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializador = persona_serializada.save()

                # auditoria actualizar persona
                usuario = request.user.id_usuario
                direccion=Util.get_client_ip(request)
                descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "RazonSocial": str(serializador.razon_social), "NombreComercial": str(serializador.nombre_comercial)}
                valores_actualizados = {'current': persona_por_actualizar, 'previous': previous_persona}

                auditoria_data = {
                    "id_usuario" : usuario,
                    "id_modulo" : 1,
                    "cod_permiso": "AC",
                    "subsistema": 'TRSV',
                    "dirip": direccion,
                    "descripcion": descripcion, 
                    "valores_actualizados": valores_actualizados
                }
                Util.save_auditoria(auditoria_data)

                #Envío sms y email
                persona = Personas.objects.get(email=email_principal)

                sms = 'Actualizacion exitosa de persona Juridica en Cormacarena.'
                context = {'razon_social': persona.razon_social}
                template = render_to_string(('email-update-personajuridica-interno.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.razon_social
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email} 
                Util.send_email(data)
                try:
                    Util.send_sms(persona.telefono_celular_empresa, sms)
                except:
                    return Response({'success':True,'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'}, status=status.HTTP_201_CREATED)
                return Response({'success':True,'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success':False,'detail': 'No se encontró ninguna persona'}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonaJuridicaExternoBySelf(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaJuridicaExternaUpdateSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarExterno]
    queryset = Personas.objects.all()
    
    def patch(self, request):
        tipo_documento = self.request.user.persona.tipo_documento
        numero_documento = self.request.user.persona.numero_documento
        
        persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipo_documento) & Q(numero_documento=numero_documento))
        previous_persona = copy.copy(persona_por_actualizar)

        if persona_por_actualizar:
            persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
            persona_serializada.is_valid(raise_exception=True)
                    
            email_principal = persona_serializada.validated_data.get('email')
            email_secundario = persona_serializada.validated_data.get('email_empresarial')

            #Validación emails dns
            validate_email = Util.validate_dns(email_principal)
            if validate_email == False:
                return Response({'success':False,'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            if email_secundario:
                validate_second_email = Util.validate_dns(email_secundario)
                if validate_second_email == False:
                    return Response({'success':False,'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

            #Verificacion emails entrantes vs existentes
            persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
            if len(persona_email_validate):
                return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializador = persona_serializada.save()
                
                # auditoria actualizar persona
                usuario = request.user.id_usuario
                direccion=Util.get_client_ip(request)
                descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "RazonSocial": str(serializador.razon_social), "NombreComercial": str(serializador.nombre_comercial)}
                valores_actualizados = {'current': persona_por_actualizar, 'previous': previous_persona}

                auditoria_data = {
                    "id_usuario" : usuario,
                    "id_modulo" : 1,
                    "cod_permiso": "AC",
                    "subsistema": 'TRSV',
                    "dirip": direccion,
                    "descripcion": descripcion, 
                    "valores_actualizados": valores_actualizados
                }
                Util.save_auditoria(auditoria_data)

                #Envío sms y emails
                persona = Personas.objects.get(email=email_principal)
                
                sms = 'Actualizacion exitosa de persona Juridica en Cormacarena.'
                context = {'razon_social': persona.razon_social}
                template = render_to_string(('email-update-personajuridica-externo.html'), context)
                subject = 'Actualización de datos exitosa ' + persona.razon_social
                data = {'template': template, 'email_subject': subject, 'to_email': persona.email} 
                Util.send_email(data)
                try:
                    Util.send_sms(persona.telefono_celular_empresa, sms)
                except:
                    return Response({'success':True,'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'}, status=status.HTTP_201_CREATED)
                return Response({'success':True,'detail': 'Persona actualizada y notificada correctamente', 'data': persona_serializada.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success':False,'detail': 'No se encontró ninguna persona'}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePersonaJuridicaByUserWithPermissions(generics.RetrieveUpdateAPIView):
    http_method_names = ['patch']
    serializer_class = PersonaJuridicaUpdateUserPermissionsSerializer
    permission_classes = [IsAuthenticated, PermisoActualizarPersona]
    queryset = Personas.objects.all()

    def patch(self, request, tipodocumento, numerodocumento):
        try:
            persona_por_actualizar = Personas.objects.get(Q(tipo_documento=tipodocumento) & Q(numero_documento=numerodocumento) & Q(tipo_persona='J'))           
            previous_persona = copy.copy(persona_por_actualizar)
            try:
                persona_serializada = self.serializer_class(persona_por_actualizar, data=request.data, many=False)
                persona_serializada.is_valid(raise_exception=True)
                try:
                    email_principal = persona_serializada.validated_data.get('email')
                    email_secundario = persona_serializada.validated_data.get('email_empresarial')

                    #Validación emails dns
                    validate_email = Util.validate_dns(email_principal)
                    if validate_email == False:
                        return Response({'success':False,'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

                    if email_secundario:
                        validate_second_email = Util.validate_dns(email_secundario)
                        if validate_second_email == False:
                            return Response({'success':False,'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

                    #Verificacion emails entrantes vs existentes
                    persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
                    if len(persona_email_validate):
                        return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        serializador = persona_serializada.save()

                        # auditoria actualizar persona
                        usuario = request.user.id_usuario
                        direccion=Util.get_client_ip(request)
                        descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "RazonSocial": str(serializador.razon_social), "NombreComercial": str(serializador.nombre_comercial)}
                        valores_actualizados = {'current': persona_por_actualizar, 'previous': previous_persona}

                        auditoria_data = {
                            "id_usuario" : usuario,
                            "id_modulo" : 1,
                            "cod_permiso": "AC",
                            "subsistema": 'TRSV',
                            "dirip": direccion,
                            "descripcion": descripcion, 
                            "valores_actualizados": valores_actualizados
                        }
                        Util.save_auditoria(auditoria_data)    
                        
                        #SMS y EMAILS
                        persona = Personas.objects.get(email=email_principal)

                        sms = 'Hola ' + str(persona.razon_social) + ' te informamos que ha sido exitosa la actualización de tus datos como PERSONA JURIDICA'
                        context = {'razon_social': persona.razon_social}
                        template = render_to_string(('email-update-personajuridica-byuser-withpermissions.html'), context)
                        subject = 'Actualización de datos exitosa ' + str(persona.razon_social)
                        data = {'template': template, 'email_subject': subject, 'to_email': persona.email} 
                        Util.send_email(data)
                        try:
                            Util.send_sms(persona.telefono_celular_empresa, sms)
                        except:
                            return Response({'success':True,'detail': 'Se actualizó la persona pero no se pudo enviar el mensaje, verificar numero o servicio'}, status=status.HTTP_201_CREATED)
                        return Response({'success':True,'detail': 'Persona actualizada y notificada exitosamente', 'data': persona_serializada.data}, status=status.HTTP_201_CREATED)
                except:
                    return Response({'success':False,'detail': 'No pudo obtener el email principal y/o secundario'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'success':False,'detail': 'Revisar parámetros de ingreso de información, el email debe ser único y debe tener telefono celular empresa'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'success':False,'detail': 'No existe ninguna persona con estos datos, por favor verificar'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class RegisterPersonaNatural(generics.CreateAPIView):
    serializer_class = PersonaNaturalPostSerializer
    
    def post(self, request):
        persona = request.data
        serializer = self.serializer_class(data=persona)
        serializer.is_valid(raise_exception=True)

        #Marcar tipo de documento como item ya usado
        tipo_documento_usado = serializer.validated_data.get('tipo_documento')
        try:
            tipo_documento_instance = TipoDocumento.objects.get(cod_tipo_documento=tipo_documento_usado.cod_tipo_documento)
            if tipo_documento_instance.item_ya_usado == False:
                tipo_documento_instance.item_ya_usado = True
                tipo_documento_instance.save()
                pass
        except:
            return Response({'success': False, 'detail': 'No existe el tipo de documento que está ingresando'})

        #Validación de persona natural
        tipo_persona = serializer.validated_data.get('tipo_persona')
        if tipo_persona != 'N':
            return Response({'success':False,'detail':'El tipo de persona debe ser Natural'}, status=status.HTTP_400_BAD_REQUEST)

        #Validación de tipo documento
        tipo_documento = serializer.validated_data.get('tipo_documento')
        if tipo_documento.cod_tipo_documento == 'NU':
            return Response({'success':False,'detail':'El tipo de documento debe ser el de una persona natural'}, status=status.HTTP_400_BAD_REQUEST)

        email_principal = serializer.validated_data.get('email')
        email_secundario = serializer.validated_data.get('email_empresarial')

        #Validación emails dns
        validate_email = Util.validate_dns(email_principal)
        if validate_email == False:
            return Response({'success':False,'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

        if email_secundario:
            validate_second_email = Util.validate_dns(email_secundario)
            if validate_second_email == False:
                return Response({'success':False,'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

        # validacion de email entrante vs existente
        persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
        if len(persona_email_validate):
            return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializador = serializer.save()

            # auditoria crear persona
            descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "PrimerNombre": str(serializador.primer_nombre), "PrimerApellido": str(serializador.primer_apellido)}
            direccion=Util.get_client_ip(request)

            auditoria_data = {
                "id_modulo" : 9,
                "cod_permiso": "CR",
                "subsistema": 'TRSV',
                "dirip": direccion,
                "descripcion": descripcion, 
            }
            Util.save_auditoria(auditoria_data)
    
            # envio de emails y sms
            persona = Personas.objects.get(email = email_principal)
    
            sms = 'Registro exitoso como persona en Cormacarena. Continue aqui: ' + 'http://127.0.0.1:8000/api/personas/persona-natural/create/'  
            context = {'primer_nombre': persona.primer_nombre, 'primer_apellido':  persona.primer_apellido}
            template = render_to_string(('email-register-personanatural.html'), context)
            subject = 'Registro exitoso ' + persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':True,'detail': 'Se guardo la persona pero no se pudo enviar el sms, verificar numero'}, status=status.HTTP_201_CREATED)
            return Response({'success':True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)


class RegisterPersonaJuridica(generics.CreateAPIView):
    serializer_class = PersonaJuridicaPostSerializer

    def post(self, request):
        persona = request.data
        print(persona)
        serializer = self.serializer_class(data=persona)
        serializer.is_valid(raise_exception=True)

        #Marcar tipo de documento como item ya usado
        tipo_documento_usado = serializer.validated_data.get('tipo_documento')
        try:
            tipo_documento_instance = TipoDocumento.objects.get(cod_tipo_documento=tipo_documento_usado.cod_tipo_documento)
            if tipo_documento_instance.item_ya_usado == False:
                tipo_documento_instance.item_ya_usado = True
                tipo_documento_instance.save()
                pass
        except:
            return Response({'success': False, 'detail': 'No existe el tipo de documento que está ingresando'}, status=status.HTTP_400_BAD_REQUEST)


        #Validación de persona natural
        tipo_persona = serializer.validated_data.get('tipo_persona')
        if tipo_persona != 'J':
            return Response({'success':False,'detail':'El tipo de persona debe ser Juridica'}, status=status.HTTP_400_BAD_REQUEST)

        #Validación de tipo documento
        tipo_documento = serializer.validated_data.get('tipo_documento')
        if tipo_documento.cod_tipo_documento != 'NU':
            return Response({'success':False,'detail':'El tipo de documento debe ser el de una persona juridica'}, status=status.HTTP_400_BAD_REQUEST)
        
        email_principal = serializer.validated_data.get('email')
        email_secundario = serializer.validated_data.get('email_empresarial')

        #Validación emails dns
        validate_email = Util.validate_dns(email_principal)
        if validate_email == False:
            return Response({'success':False,'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

        if email_secundario:
            validate_second_email = Util.validate_dns(email_secundario)
            if validate_second_email == False:
                return Response({'success':False,'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

        #Verificación emails entrantes vs salientes
        persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
        if len(persona_email_validate):
            return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
        else: 
            serializador = serializer.save()
            
            # auditoria crear persona
            descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "RazonSocial": str(serializador.razon_social), "NombreComercial": str(serializador.nombre_comercial)}
            direccion=Util.get_client_ip(request)

            auditoria_data = {
                "id_modulo" : 9,
                "cod_permiso": "CR",
                "subsistema": 'TRSV',
                "dirip": direccion,
                "descripcion": descripcion, 
            }
            Util.save_auditoria(auditoria_data)

            #Envio SMS y EMAIL
            persona = Personas.objects.get(email=email_principal)

            sms = 'Registro exitoso como persona Juridica en Cormacarena. Continue aqui: ' + 'http://127.0.0.1:8000/api/personas/persona-natural/create/'
            context = {'razon_social': persona.razon_social, 'nombre_comercial':  persona.nombre_comercial}
            template = render_to_string(('email-register-personajuridica.html'), context)
            subject = 'Registro exitoso ' + persona.razon_social
            data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular_empresa, sms)
            except:
                return Response({'success':True,'detail':'Se guardo la persona pero no se pudo enviar el sms, verificar numero', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            
            return Response({'success':True, 'detail': serializer.data}, status=status.HTTP_201_CREATED)


class RegisterPersonaNaturalByUserInterno(generics.CreateAPIView):
    serializer_class = PersonaNaturalPostByUserSerializer
    # permission_classes = [IsAuthenticated, PermisoCrearPersona]
    
    def post(self, request):
        persona = request.data
        serializer = self.serializer_class(data=persona)
        serializer.is_valid(raise_exception=True)

        #Marcar tipo de documento como item ya usado
        tipo_documento_usado = serializer.validated_data.get('tipo_documento')
        try:
            tipo_documento_instance = TipoDocumento.objects.get(cod_tipo_documento=tipo_documento_usado.cod_tipo_documento)
            if tipo_documento_instance.item_ya_usado == False:
                tipo_documento_instance.item_ya_usado = True
                tipo_documento_instance.save()
                pass
        except:
            return Response({'success': False, 'detail': 'No existe el tipo de documento que está ingresando'}, status=status.HTTP_400_BAD_REQUEST)


        email_principal = serializer.validated_data.get('email')
        email_secundario = serializer.validated_data.get('email_empresarial')

        #Validación de persona natural
        tipo_persona = serializer.validated_data.get('tipo_persona')
        if tipo_persona != 'N':
            return Response({'success':False,'detail':'El tipo de persona debe ser Natural'}, status=status.HTTP_400_BAD_REQUEST)

        #Validación de tipo documento
        tipo_documento = serializer.validated_data.get('tipo_documento')
        if tipo_documento.cod_tipo_documento == 'NU':
            return Response({'success':False,'detail':'El tipo de documento debe ser el de una persona natural'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Validación emails dns
        validate_email = Util.validate_dns(email_principal)
        if validate_email == False:
            return Response({'success':False,'detail': 'Valide que el email principal ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

        if email_secundario:
            validate_second_email = Util.validate_dns(email_secundario)
            if validate_second_email == False:
                return Response({'success':False,'detail': 'Valide que el email secundario ingresado exista'}, status=status.HTTP_400_BAD_REQUEST)

        # validacion de email entrante vs existente
        persona_email_validate = Personas.objects.filter(Q(email_empresarial=email_principal) | Q(email=email_secundario))
        if len(persona_email_validate):
            return Response({'success':False,'detail': 'Ya existe una persona con este email asociado como email principal o secundario'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializador = serializer.save()
            
            # auditoria crear persona
            usuario = request.user.id_usuario
            descripcion = {"TipodeDocumentoID": str(serializador.tipo_documento), "NumeroDocumentoID": str(serializador.numero_documento), "PrimerNombre": str(serializador.primer_nombre), "PrimerApellido": str(serializador.primer_apellido)}
            direccion=Util.get_client_ip(request)

            auditoria_data = {
                "id_usuario" : usuario,
                "id_modulo" : 1,
                "cod_permiso": "CR",
                "subsistema": 'TRSV',
                "dirip": direccion,
                "descripcion": descripcion, 
            }
            Util.save_auditoria(auditoria_data)

            # envio de emails y sms
            persona = Personas.objects.get(email = email_principal)
    
            sms = 'Hola '+ persona.primer_nombre + ' ' + persona.primer_apellido + ' te informamos que has sido registrado como PERSONA NATURAL en el portal Bia Cormacarena \n Ahora puedes crear tu usuario, hazlo en el siguiente link' + 'url'  
            context = {'primer_nombre': persona.primer_nombre, 'primer_apellido':  persona.primer_apellido}
            template = render_to_string(('email-register-personanatural.html'), context)
            subject = 'Registro exitoso ' + persona.primer_nombre
            data = {'template': template, 'email_subject': subject, 'to_email': persona.email}
            Util.send_email(data)
            try:
                Util.send_sms(persona.telefono_celular, sms)
            except:
                return Response({'success':True,'detail': 'Se guardo la persona pero no se pudo enviar el sms, verificar numero'}, status=status.HTTP_201_CREATED)
            return Response({'success':True, 'detail': serializer.data, 'message': 'Se ejecutó todo exitosamente'}, status=status.HTTP_201_CREATED)

# Views for apoderados persona


"""class getApoderadosPersona(generics.ListAPIView):
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
    queryset = ApoderadoPersona.objects.all()"""


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
            persona_empresa=sucursal.id_persona_empresa
            sucursal.delete()
            persona=Personas.objects.get(id_persona=persona_empresa.id_persona)
            usuario = request.user.id_usuario
            dirip = Util.get_client_ip(request)
            descripcion ={ "nombre razón social": str(persona.razon_social),"sucursal" :str(sucursal.sucursal)}
            auditoria_data = {
                'id_usuario': usuario,
                'id_modulo': 1,
                'cod_permiso': 'BO',
                'subsistema': 'TRSV',
                'dirip': dirip,
                'descripcion': descripcion,
            }
            
            Util.save_auditoria(auditoria_data)

            return Response({'success':True,'detail':'la sucursal empresa fue eliminada'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'success':False,'detail':'No existe sucursal'}, status=status.HTTP_400_BAD_REQUEST)
            
class updateSucursalEmpresa(generics.RetrieveUpdateAPIView):
    serializer_class = SucursalesEmpresasPostSerializer
    queryset = SucursalesEmpresas.objects.all()
    permission_classes = [IsAuthenticated]
    
    def put(self, request,pk=None):
        sucursal = SucursalesEmpresas.objects.filter(id_sucursal_empresa= pk).first()
        previous_sucursal = copy.copy(sucursal)
        if sucursal:
            sucursal_serializer = self.serializer_class(sucursal, data=request.data)
            sucursal_serializer.is_valid(raise_exception=True)
            sucursal_serializer.save()
            
            usuario = request.user.id_usuario
            persona=Personas.objects.get(id_persona=request.data['id_persona_empresa'])
            dirip = Util.get_client_ip(request)
            descripcion ={ "nombre razón social": str(persona.razon_social),"sucursal" :str(sucursal.sucursal)}
            valores_actualizados={'current':sucursal, 'previous':previous_sucursal}

            auditoria_data = {
                'id_usuario': usuario,
                'id_modulo': 1,
                'cod_permiso': 'AC',
                'subsistema': 'TRSV',
                'dirip': dirip,
                'descripcion': descripcion,
                'valores_actualizados': valores_actualizados
            }
            
            Util.save_auditoria(auditoria_data)
            return Response({'success':True,'detail':'la sucursal empresa actualizada'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success':False,'detail':'No existe sucursal'}, status=status.HTTP_400_BAD_REQUEST)

class registerSucursalEmpresa(generics.CreateAPIView):
    serializer_class = SucursalesEmpresasPostSerializer 
    queryset = SucursalesEmpresas.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializador=serializer.save()
        usuario = request.user.id_usuario

        persona=Personas.objects.get(id_persona=request.data['id_persona_empresa'])
        dirip = Util.get_client_ip(request)
        descripcion ={ "nombre razón social": str(persona.razon_social),"sucursal" :str(serializador.sucursal)}


        auditoria_data = {
            'id_usuario': usuario,
            'id_modulo': 1,
            'cod_permiso': 'CR',
            'subsistema': 'TRSV',
            'dirip': dirip,
            'descripcion': descripcion,
        }
        
        Util.save_auditoria(auditoria_data)
        headers = self.get_success_headers(serializer.data)
        return Response({'success':True},serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

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
