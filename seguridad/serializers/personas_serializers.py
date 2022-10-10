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
    
    
class PersonasPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = '__all__'
        extra_kwargs = {
                'id_persona': {'required': True},
                'tipo_persona': {'required': True},
                'numero_documento': {'required': True},
                'pais_residencia': {'required': True},
                'departamento_residencia': {'required': True},
                'ubicacion_georeferenciada': {'required': True},
                'pais_nacimiento': {'required': True},
                'sexo': {'required': True},
                'email': {'required': True},
                'cod_pais_nacionalidad_empresa': {'required': True},
                'acepta_notificacion_sms': {'required': True},
                'acepta_notificacion_email': {'required': True},
                'acepta_tratamiento_datos': {'required': True},
            }


class ApoderadoPersonaSerializer(serializers.ModelSerializer):
    persona_poderdante = PersonasSerializer(read_only=True)
    persona_apoderada = PersonasSerializer(read_only=True)
    
    class Meta:
        model = ApoderadoPersona
        fields = '__all__'
        
        
class ApoderadoPersonaPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApoderadoPersona
        fields = '__all__'
        extra_kwargs = {
                'persona_poderdante': {'required': True},
                'id_proceso': {'required': True},
                'persona_apoderada': {'required': True},
                'fecha_inicio': {'required': True},
            }
        
        
class SucursalesEmpresasSerializer(serializers.ModelSerializer):
    id_empresa = PersonasSerializer(read_only=True)
    
    class Meta:
        model = SucursalesEmpresas
        fields = '__all__'
        

class SucursalesEmpresasPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SucursalesEmpresas
        fields = '__all__'
        extra_kwargs = {
                'id_empresa': {'required': True},
                'sucursal': {'required': True},
                'direccion': {'required': True},
                'direccion_sucursal_georeferenciada': {'required': True},
                'pais_sucursal_exterior': {'required': True},
                'direccion_correspondencias': {'required': True},
                'email_sucursal': {'required': True},
                'telefono_sucursal': {'required': True},
            }
        

class HistoricoEmailsSerializer(serializers.ModelSerializer):
    id_persona = PersonasSerializer(read_only=True)
    class Meta:
        model = HistoricoEmails
        fields = '__all__'
        

class HistoricoEmailsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoEmails
        fields = '__all__'
        extra_kwargs = {
                'id_persona': {'required': True},
                'email_notificacion': {'required': True},
            }
        
        
class HistoricoDireccionSerializer(serializers.ModelSerializer):
    id_persona = PersonasSerializer(read_only=True)
    
    class Meta:
        model = HistoricoDireccion
        fields = '__all__'
        
        
class HistoricoDireccionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoDireccion
        fields = '__all__'
        extra_kwargs = {
                'id_persona': {'required': True},
                'direccion': {'required': True},
                'tipo_direccion': {'required': True},
            }
        

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
        

class ClasesTerceroPersonapostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasesTerceroPersona
        fields = '__all__'
        extra_kwargs = {
                'id_persona': {'required': True},
                'id_clase_tercero': {'required': True},
            }