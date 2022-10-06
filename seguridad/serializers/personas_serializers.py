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


class RepresentanteLegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = '__all__'

class PersonasSerializer(serializers.ModelSerializer):
    tipo_documento = TipoDocumentoSerializer(read_only=True)
    estado_civil = EstadoCivilSerializer(read_only=True)
    representante_legal = RepresentanteLegalSerializer(read_only=True)
        
    class Meta:
        model = Personas
        fields = '__all__'
        
    def get_tipo_documento(self, obj):
        tipo_documento = obj.tipodocumento_set.all()
        serializer = TipoDocumentoSerializer(tipo_documento, many=True)
        return serializer.data
    
    def get_estado_civil(self, obj):
        estado_civil = obj.estadocivil_set.all()
        serializer = EstadoCivilSerializer(estado_civil, many=True)
        return serializer.data
    
    def get_representante_legal(self, obj):
        representante_legal = obj.representantelegal_set.all()
        serializer = RepresentanteLegalSerializer(representante_legal, many=True)
        return serializer.data
           

class ApoderadoPersonaSerializer(serializers.ModelSerializer):
    persona_poderdante = PersonasSerializer(read_only=True)
    persona_apoderada = PersonasSerializer(read_only=True)
    
    class Meta:
        model = ApoderadoPersona
        fields = '__all__'
        
        
class SucursalesEmpresasSerializer(serializers.ModelSerializer):
    id_empresa = PersonasSerializer(read_only=True)
    
    class Meta:
        model = SucursalesEmpresas
        fields = '__all__'
        

class HistoricoEmailsSerializer(serializers.ModelSerializer):
    id_persona = PersonasSerializer(read_only=True)
    class Meta:
        model = HistoricoEmails
        fields = '__all__'
        
        
class HistoricoDireccionSerializer(serializers.ModelSerializer):
    id_persona = PersonasSerializer(read_only=True)
    
    class Meta:
        model = HistoricoDireccion
        fields = '__all__'
        

class ClasesTerceroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasesTercero
        fields = '__all__'
        
        
class ClasesTerceroPersonaSerializer(serializers.ModelSerializer):
    id_clase_tercero = ClasesTerceroSerializer(read_only=True)
    id_persona = PersonasSerializer(read_only=True)
    class Meta:
        model = ClasesTerceroPersona
        fields = '__all__'
        