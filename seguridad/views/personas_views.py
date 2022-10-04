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


