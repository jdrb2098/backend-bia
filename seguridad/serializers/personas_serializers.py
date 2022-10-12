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
    
    
class PersonaNaturalPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = ['id_persona', 'tipo_persona', 'tipo_documento', 'numero_documento', 'digito_verificacion', 'nombre_comercial', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'fecha_nacimiento', 'email', 'telefono_celular',]
        extra_kwargs = {
                'id_persona': {'required': True},
                'tipo_persona': {'required': True},
                'tipo_documento': {'required': True},
                'numero_documento': {'required': True},
                'primer_nombre': {'required': True},
                'primer_apellido': {'required': True},
                'fecha_nacimiento': {'required': True},
                'email': {'required': True},
                'telefono_celular': {'required': True},
            }
        
        
class PersonaJuridicaPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personas
        fields = ['id_persona', 'tipo_persona', 'tipo_documento', 'numero_documento', 'digito_verificacion', 'razon_social', 'email', 'telefono_celular', 'direccion_notificaciones', 'departamento_residencia', 'municipio_residencia',]
        extra_kwargs = {
                'id_persona': {'required': True},
                'tipo_persona': {'required': True},
                'tipo_documento': {'required': True},
                'numero_documento': {'required': True},
                'razon_social': {'required': True},
                'email': {'required': True},
                'telefono_celular': {'required': True},
                'direccion_notificaciones': {'required': True},
                'departamento_residencia': {'required': True},
                'municipio_residencia': {'required': True},
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