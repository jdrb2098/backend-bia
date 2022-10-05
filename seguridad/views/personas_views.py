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
def registerPersonas(request):
    data = request.data
    personas = Personas.objects.create(
        cod_tipo_documento=data['cod_tipo_documento'],
        nombre=data['nombre']
    )
    serializer = PersonasSerializer(personas, many=False)
    return Response(serializer.data)
