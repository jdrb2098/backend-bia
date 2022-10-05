from django.shortcuts import render
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
    ApoderadoPersonaSerializer,
    SucursalesEmpresasSerializer,
    HistoricoEmailsSerializer,
    HistoricoDireccionSerializer,
    ClasesTerceroSerializer,
    ClasesTerceroPersonaSerializer
)

# Views for Estado Civil


@api_view(['POST'])
def registerEstadoCivil(request):
    data = request.data
    estadoCivil = EstadoCivil.objects.create(
        cod_estado_civil=data['cod_estado_civil'],
        nombre=data['nombre']
    )
    serializer = EstadoCivilSerializer(estadoCivil, many=False)
    return Response(serializer.data)


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


@api_view(['PUT'])
def updateEstadoCivil(request, pk):
    estadoCivil = EstadoCivil.objects.get(cod_estado_civil=pk)

    data = request.data

    estadoCivil.nombre = data['nombre']
    estadoCivil.save()

    serializer = EstadoCivilSerializer(estadoCivil, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteEstadoCivil(request, pk):
    estadoCivilForDeletion = EstadoCivil.objects.get(cod_estado_civil=pk)
    estadoCivilForDeletion.delete()
    return Response('Estado Civil was deleted')


# Views for Tipo Documento

@api_view(['POST'])
def registerTipoDocumento(request):
    data = request.data
    tipoDocumento = TipoDocumento.objects.create(
        cod_tipo_documento=data['cod_tipo_documento'],
        nombre=data['nombre']
    )
    serializer = TipoDocumentoSerializer(tipoDocumento, many=False)
    return Response(serializer.data)


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


@api_view(['PUT'])
def updateTipoDocumento(request, pk):
    tipoDocumento = TipoDocumento.objects.get(cod_tipo_documento=pk)

    data = request.data

    tipoDocumento.nombre = data['nombre']
    tipoDocumento.save()

    serializer = TipoDocumentoSerializer(tipoDocumento, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteTipoDocumento(request, pk):
    tipoDocumentoForDeletion = TipoDocumento.objects.get(cod_tipo_documento=pk)
    tipoDocumentoForDeletion.delete()
    return Response('Estado Civil was deleted')


# Views for Personas


@api_view(['POST'])
def registerPersona(request):
    data = request.data
    
    persona = Personas.objects.create(
        tipo_persona=data['tipo_persona'],
        numero_documento=data['numero_documento'],
        digito_verificacion=data['digito_verificacion'],
        primer_nombre=data['primer_nombre'],
        segundo_nombre=data['segundo_nombre'],
        primer_apellido=data['primer_apellido'],
        segundo_apellido=data['segundo_apellido'],
        nombre_comercial=data['nombre_comercial'],
        razon_social=data['razon_social'],
        pais_residencia=data['pais_residencia'],
        departamento_residencia=data['departamento_residencia'],
        municipio_residencia=data['municipio_residencia'],
        direccion_residencia=data['direccion_residencia'],
        direccion_residencia_ref=data['direccion_residencia_ref'],
        ubicacion_georeferenciada=data['ubicacion_georeferenciada'],
        direccion_laboral=data['direccion_laboral'],
        direccion_notificaciones=data['direccion_notificaciones'],
        pais_nacimiento=data['pais_nacimiento'],
        fecha_nacimiento=data['fecha_nacimiento'],
        sexo=data['sexo'],
        estado_civil=data['estado_civil'],
        representante_legal=data['representante_legal'],
        email=data['email'],
        email_empresarial=data['email_empresarial'],
        telefono_fijo_residencial=data['telefono_fijo_residencial'],
        telefono_celular=data['telefono_celular'],
        telefono_empresa=data['telefono_empresa'],
        cod_municipio_laboral_nal=data['cod_municipio_laboral_nal'],
        cod_municipio_notificacion_nal=data['cod_municipio_notificacion_nal'],
        telefono_celular_empresa=data['telefono_celular_empresa'],
        telefono_empresa_2=data['telefono_empresa_2'],
        cod_pais_nacionalidad_empresa=data['cod_pais_nacionalidad_empresa'],
        acepta_notificacion_sms=data['acepta_notificacion_sms'],
        acepta_notificacion_email=data['acepta_notificacion_email'],
        acepta_tratamiento_datos=data['acepta_tratamiento_datos']
    )
    serializer = PersonasSerializer(persona, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getPersonas(request):
    personas = Personas.objects.all()
    serializer = PersonasSerializer(personas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPersonaById(request, pk):
    personas = Personas.objects.get(id_persona=pk)
    serializer = PersonasSerializer(personas, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updatePersona(request, pk):
    persona = Personas.objects.get(id_persona=pk)

    data = request.data

    persona.tipo_persona = data['tipo_persona'],
    persona.tipo_documento = data['tipo_documento'],
    persona.numero_documento = data['numero_documento'],
    persona.digito_verificacion = data['digito_verificacion'],
    persona.primer_nombre = data['primer_nombre'],
    persona.segundo_nombre = data['segundo_nombre'],
    persona.primer_apellido = data['primer_apellido'],
    persona.segundo_apellido = data['segundo_apellido'],
    persona.nombre_comercial = data['nombre_comercial'],
    persona.razon_social = data['razon_social'],
    persona.pais_residencia = data['pais_residencia'],
    persona.departamento_residencia = data['departamento_residencia'],
    persona.municipio_residencia = data['municipio_residencia'],
    persona.direccion_residencia = data['direccion_residencia'],
    persona.direccion_residencia_ref = data['direccion_residencia_ref'],
    persona.ubicacion_georeferenciada = data['ubicacion_georeferenciada'],
    persona.direccion_laboral = data['direccion_laboral'],
    persona.direccion_notificaciones = data['direccion_notificaciones'],
    persona.pais_nacimiento = data['pais_nacimiento'],
    persona.fecha_nacimiento = data['fecha_nacimiento'],
    persona.sexo = data['sexo'],
    persona.estado_civil = data['estado_civil'],
    persona.representante_legal = data['representante_legal'],
    persona.email = data['email'],
    persona.email_empresarial = data['email_empresarial'],
    persona.telefono_fijo_residencial = data['telefono_fijo_residencial'],
    persona.telefono_celular = data['telefono_celular'],
    persona.telefono_empresa = data['telefono_empresa'],
    persona.cod_municipio_laboral_nal = data['cod_municipio_laboral_nal'],
    persona.cod_municipio_notificacion_nal = data['cod_municipio_notificacion_nal'],
    persona.telefono_celular_empresa = data['telefono_celular_empresa'],
    persona.telefono_empresa_2 = data['telefono_empresa_2'],
    persona.cod_pais_nacionalidad_empresa = data['cod_pais_nacionalidad_empresa'],
    persona.acepta_notificacion_sms = data['acepta_notificacion_sms'],
    persona.acepta_notificacion_email = data['acepta_notificacion_email'],
    persona.acepta_tratamiento_datos = data['acepta_tratamiento_datos']

    persona.save()

    serializer = PersonasSerializer(persona, many=False)
    return Response(serializer.data)
