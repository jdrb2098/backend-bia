from rest_framework import serializers
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


class EstadoCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCivil
        fields = '__all__'
        

class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'
        
        
class PersonasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = '__all__'
        

class ApoderadoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApoderadoPersona
        fields = '__all__'
        
        
class SucursalesEmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SucursalesEmpresas
        fields = '__all__'
        

class HistoricoEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoEmails
        fields = '__all__'
        
        
class HistoricoDireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoDireccion
        fields = '__all__'
        

class ClasesTerceroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasesTercero
        fields = '__all__'
        
        
class ClasesTerceroPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasesTerceroPersona
        fields = '__all__'
        