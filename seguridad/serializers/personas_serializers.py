from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
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
    #tipoDocumento = serializers.SerializerMethodField(read_only=True)
        
    class Meta:
        model = Personas
        fields = '__all__'
        
    def get_tipoDocumento(self, instance):
        response = super().to_representation(instance)
        response['tipo_documento'] = TipoDocumentoSerializer(instance.tipo_documento).data
        return response
    
    def get_estadoCivil(self, instance):
        response = super().to_representation(instance)
        response['estado_civil'] = EstadoCivilSerializer(instance.estado_civil).data
        return response
           

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
        