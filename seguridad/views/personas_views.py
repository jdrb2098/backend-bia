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


@api_view(['GET'])
def getEstadoCivil(request):
    estadoCivil = EstadoCivil.objects.all()
    serializer = EstadoCivilSerializer(estadoCivil, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getEstadoCivilById(request, pk):
    estadoCivil = EstadoCivil.objects.get(cod_estado_civil=pk)
    serializer = EstadoCivilSerializer(estadoCivil, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteEstadoCivil(request, pk):
    estadoCivilForDeletion = EstadoCivil.objects.get(cod_estado_civil=pk)
    estadoCivilForDeletion.delete()
    return Response('Estado Civil was deleted')


@api_view(['PUT'])  
def updateEstadoCivil(request,pk):
    estado_civil = EstadoCivil.objects.filter(cod_estado_civil=pk).first() ##consulta por id
    if estado_civil:  ## si existe auditoria
        estado_civil_serializer = EstadoCivilSerializer(estado_civil,data=request.data) ## envia al serializador la información actualizada
        if estado_civil_serializer.is_valid():
            estado_civil_serializer.save() #guarda nueva información
            return Response(estado_civil_serializer.data,status=status.HTTP_200_OK)
        return Response(estado_civil_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerEstadoCivil(request):
    estado_civil_serializers=EstadoCivilSerializer(data=request.data)
    if estado_civil_serializers.is_valid():
        estado_civil_serializers.save()
        return Response(estado_civil_serializers.data,status=status.HTTP_200_OK)
    return Response(estado_civil_serializers.errors)


# Views for Tipo Documento

@api_view(['GET'])
def getTipoDocumento(request):
    tipoDocumento = TipoDocumento.objects.all()
    serializer = TipoDocumentoSerializer(tipoDocumento, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTipoDocumentoById(request, pk):
    tipoDocumento = TipoDocumento.objects.get(cod_tipo_documento=pk)
    serializer = TipoDocumentoSerializer(tipoDocumento, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteTipoDocumento(request, pk):
    tipoDocumentoForDeletion = TipoDocumento.objects.get(cod_tipo_documento=pk)
    tipoDocumentoForDeletion.delete()
    return Response('Estado Civil was deleted')


@api_view(['PUT'])  
def updateTipoDocumento(request,pk):
    tipoDocumento = TipoDocumento.objects.filter(cod_tipo_documento=pk).first() ##consulta por id
    if tipoDocumento:  ## si existe auditoria
        tipo_documento_serializer = TipoDocumentoSerializer(tipoDocumento,data=request.data) ## envia al serializador la información actualizada
        if tipo_documento_serializer.is_valid():
            tipo_documento_serializer.save() #guarda nueva información
            return Response(tipo_documento_serializer.data,status=status.HTTP_200_OK)
        return Response(tipo_documento_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerTipoDocumento(request):
    tipo_documento_serializer = TipoDocumentoSerializer(data=request.data)
    if tipo_documento_serializer.is_valid():
        tipo_documento_serializer.save()
        return Response(tipo_documento_serializer.data,status=status.HTTP_200_OK)
    return Response(tipo_documento_serializer.errors)


# Views for Personas


@api_view(['GET'])
def getPersonas(request):
    personas = Personas.objects.all()
    serializer = PersonasSerializer(personas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPersonaById(request, pk):
    persona = Personas.objects.get(id_persona=pk)
    serializer = PersonasSerializer(persona, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deletePersona(request, pk):
    personaForDeletion = Personas.objects.get(id_persona=pk)
    personaForDeletion.delete()
    return Response('Persona was deleted')


@api_view(['PUT'])  
def updatePersona(request,pk):
    persona = Personas.objects.filter(id_persona=pk).first() ##consulta por id
    if persona:  ## si existe auditoria
        personas_serializer = PersonasPostSerializer(persona,data=request.data) ## envia al serializador la información actualizada
        if personas_serializer.is_valid():
            personas_serializer.save() #guarda nueva información
            return Response(personas_serializer.data,status=status.HTTP_200_OK)
        return Response(personas_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UpdatePersona(RetrieveUpdateAPIView):
    serializer_class = PersonasPostSerializer
    queryset = Personas.objects.all()

class RegisterPersona(generics.CreateAPIView):
    queryset = Personas.objects.all()
    serializer_class = PersonasPostSerializer

# Views for apoderados persona

@api_view(['GET'])
def getApoderadosPersona(request):
    apoderado_persona = ApoderadoPersona.objects.all()
    serializer = ApoderadoPersonaSerializer(apoderado_persona, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getApoderadoPersonaById(request, pk):
    apoderado_persona = ApoderadoPersona.objects.get(consecutivo_del_proceso=pk)
    serializer = ApoderadoPersonaSerializer(apoderado_persona, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteApoderadoPersona(request, pk):
    apoderadoForDeletion = ApoderadoPersona.objects.get(consecutivo_del_proceso=pk)
    apoderadoForDeletion.delete()
    return Response('Apoderado was deleted')


@api_view(['PUT'])  
def updateApoderadoPersona(request,pk):
    apoderado_persona = ApoderadoPersona.objects.filter(consecutivo_del_proceso=pk).first() ##consulta por id
    if apoderado_persona:  ## si existe auditoria
        apoderado_persona_serializer = ApoderadoPersonaPostSerializer(apoderado_persona ,data=request.data) ## envia al serializador la información actualizada
        if apoderado_persona_serializer.is_valid():
            apoderado_persona_serializer.save() #guarda nueva información
            return Response(apoderado_persona_serializer.data,status=status.HTTP_200_OK)
        return Response(apoderado_persona_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerApoderadoPersona(request):
    apoderado_persona_serializer = ApoderadoPersonaPostSerializer(data=request.data)
    if apoderado_persona_serializer.is_valid():
        apoderado_persona_serializer.save()
        return Response(apoderado_persona_serializer.data,status=status.HTTP_200_OK)
    return Response(apoderado_persona_serializer.errors)


# Views for Sucursales Empresas

@api_view(['GET'])
def getSucursalesEmpresas(request):
    sucursal_empresa = SucursalesEmpresas.objects.all()
    serializer = SucursalesEmpresasSerializer(sucursal_empresa, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSucursalEmpresaById(request, pk):
    sucursal_empresa = SucursalesEmpresas.objects.get(numero_sucursal=pk)
    serializer = SucursalesEmpresasSerializer(sucursal_empresa, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteSucursalEmpresa(request, pk):
    sucursal_empresa = SucursalesEmpresas.objects.get(numero_sucursal=pk)
    sucursal_empresa.delete()
    return Response('Sucursal was deleted')


@api_view(['PUT'])  
def updateSucursalEmpresa(request,pk):
    sucursal_empresa = SucursalesEmpresas.objects.filter(numero_sucursal=pk).first() ##consulta por id
    if sucursal_empresa:  ## si existe auditoria
        sucursal_empresa_serializer = SucursalesEmpresasSerializer(sucursal_empresa ,data=request.data) ## envia al serializador la información actualizada
        if sucursal_empresa_serializer.is_valid():
            sucursal_empresa_serializer.save() #guarda nueva información
            return Response(sucursal_empresa_serializer.data,status=status.HTTP_200_OK)
        return Response(sucursal_empresa_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerSucursalEmpresa(request):
    sucursal_empresa_serializer = SucursalesEmpresasPostSerializer(data=request.data)
    if sucursal_empresa_serializer.is_valid():
        sucursal_empresa_serializer.save()
        return Response(sucursal_empresa_serializer.data,status=status.HTTP_200_OK)
    return Response(sucursal_empresa_serializer.errors)


# Views for Historico Emails


@api_view(['GET'])
def getHistoricoEmails(request):
    historico_email = HistoricoEmails.objects.all()
    serializer = HistoricoEmailsSerializer(historico_email, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getHistoricoEmailById(request, pk):
    historico_email = HistoricoEmails.objects.get(id_histo_email=pk)
    serializer = HistoricoEmailsSerializer(historico_email, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteHistoricoEmail(request, pk):
    historico_email = HistoricoEmails.objects.get(id_histo_email=pk)
    historico_email.delete()
    return Response('Historico Email was deleted')


@api_view(['PUT'])  
def updateHistoricoEmail(request,pk):
    historico_email = HistoricoEmails.objects.filter(id_histo_email=pk).first() ##consulta por id
    if historico_email:  ## si existe auditoria
        historico_email_serializer = HistoricoEmailsSerializer(historico_email ,data=request.data) ## envia al serializador la información actualizada
        if historico_email_serializer.is_valid():
            historico_email_serializer.save() #guarda nueva información
            return Response(historico_email_serializer.data,status=status.HTTP_200_OK)
        return Response(historico_email_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerHistoricoEmail(request):
    historico_email_serializer = HistoricoEmailsPostSerializer(data=request.data)
    if historico_email_serializer.is_valid():
        historico_email_serializer.save()
        return Response(historico_email_serializer.data,status=status.HTTP_200_OK)
    return Response(historico_email_serializer.errors)


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


@api_view(['GET'])
def getClasesTercero(request):
    clases_terceros = ClasesTercero.objects.all()
    serializer = ClasesTerceroSerializer(clases_terceros, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getClaseTerceroById(request, pk):
    clase_tercero = ClasesTercero.objects.get(id_clase_tercero=pk)
    serializer = ClasesTerceroSerializer(clase_tercero, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteClaseTercero(request, pk):
    clase_tercero = ClasesTercero.objects.get(id_clase_tercero=pk)
    clase_tercero.delete()
    return Response('Clase Tercero was deleted')


@api_view(['PUT'])  
def updateClaseTercero(request,pk):
    clase_tercero = ClasesTercero.objects.filter(id_clase_tercero=pk).first() ##consulta por id
    if clase_tercero:  ## si existe auditoria
        clase_tercero_serializer = ClasesTerceroSerializer(clase_tercero ,data=request.data) ## envia al serializador la información actualizada
        if clase_tercero_serializer.is_valid():
            clase_tercero_serializer.save() #guarda nueva información
            return Response(clase_tercero_serializer.data,status=status.HTTP_200_OK)
        return Response(clase_tercero_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


"""@api_view(['POST'])
def registerClaseTercero(request):
    clase_tercero_serializer = ClasesTerceroSerializer(data=request.data)
    if clase_tercero_serializer.is_valid():
        clase_tercero_serializer.save()
        return Response(clase_tercero_serializer.data,status=status.HTTP_200_OK)
    return Response(clase_tercero_serializer.errors)"""

@api_view(['POST'])
def registerClaseTercero(request):
    data = request.data
    try:
        clase_tercero = ClasesTercero.objects.create(
            nombre=data['nombre']
        )
        
        serializer = ClasesTerceroSerializer(clase_tercero, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'Clase tercero no pudo ser añadido'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# Views for Clases Tercero Persona


@api_view(['GET'])
def getClasesTerceroPersonas(request):
    clases_terceros_personas = ClasesTerceroPersona.objects.all()
    serializer = ClasesTerceroPersonaSerializer(clases_terceros_personas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getClaseTerceroPersonaById(request, pk):
    clase_tercero_persona = ClasesTerceroPersona.objects.get(id_clase_tercero=pk)
    serializer = ClasesTerceroPersonaSerializer(clase_tercero_persona, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteClaseTerceroPersona(request, pk):
    clase_tercero_persona = ClasesTerceroPersona.objects.get(id_clase_tercero=pk)
    clase_tercero_persona.delete()
    return Response('Clase Tercero was deleted')


@api_view(['PUT'])  
def updateClaseTerceroPersona(request,pk):
    clase_tercero_persona = ClasesTerceroPersona.objects.filter(id_clase_tercero=pk).first() ##consulta por id
    if clase_tercero_persona:  ## si existe auditoria
        clase_tercero_persona_serializer = ClasesTerceroSerializer(clase_tercero_persona ,data=request.data) ## envia al serializador la información actualizada
        if clase_tercero_persona_serializer.is_valid():
            clase_tercero_persona_serializer.save() #guarda nueva información
            return Response(clase_tercero_persona_serializer.data,status=status.HTTP_200_OK)
        return Response(clase_tercero_persona_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registerClaseTerceroPersona(request):
    clase_tercero_persona_serializer = ClasesTerceroPersonapostSerializer(data=request.data)
    if clase_tercero_persona_serializer.is_valid():
        clase_tercero_persona_serializer.save()
        return Response(clase_tercero_persona_serializer.data,status=status.HTTP_200_OK)
    return Response(clase_tercero_persona_serializer.errors)

class PaisesChoices(APIView):
    def get(self,request):
        paises = {"paises": dict(paises_choices.paises_CHOICES)}
        departamentos = {"departamentos": dict(departamentos_choices.departamentos_CHOICES)}
        municipios = {"municipios": dict(municipios_choices.municipios_CHOICES)}
        response = [paises,departamentos,municipios]
        return Response(response)