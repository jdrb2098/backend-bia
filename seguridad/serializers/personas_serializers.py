from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
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
        
        
class EstadoCivilPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCivil
        fields = [
            'cod_estado_civil', 
            'nombre'        
        ]
        extra_kwargs = {
            'cod_estado_civil': {'required': True},  
            'nombre': {'required': True}, 
        }


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'


class TipoDocumentoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = [
            'cod_tipo_documento',
            'nombre'
        ]
        extra_kwargs = {
            'cod_tipo_documento': {'required': True},
            'nombre': {'required': True}
        }


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
        

class PersonaNaturalSerializer(serializers.ModelSerializer):
    tipo_documento = TipoDocumentoSerializer(read_only=True)
    
    estado_civil = EstadoCivilSerializer(read_only=True)
          
    class Meta:
        model = Personas
        fields = [
            'id_persona', 
            # 'tipo_persona', 
            'tipo_documento', 
            'numero_documento', 
            'digito_verificacion', 
            'nombre_comercial', 
            'primer_nombre', 
            'segundo_nombre', 
            'primer_apellido', 
            'segundo_apellido', 
            'fecha_nacimiento', 
            'email', 
            'telefono_celular',
            'sexo',
            'estado_civil',
            'pais_nacimiento',
            'email_empresarial',
            'ubicacion_georeferenciada',
            'telefono_fijo_residencial',            
            'telefono_empresa',
            'pais_residencia',
            'departamento_residencia',
            'municipio_residencia',
            'direccion_residencia',
            'direccion_residencia_ref',
            'direccion_notificaciones',
            'cod_municipio_laboral_nal',
            'acepta_notificacion_sms',
            'acepta_notificacion_email',
            'acepta_tratamiento_datos'
        ]
        
         
    
class PersonaJuridicaSerializer(serializers.ModelSerializer):
    tipo_documento = TipoDocumentoSerializer(read_only=True)
           
    class Meta:
        model = Personas
        fields = [
            'id_persona', 
            'tipo_persona', 
            'tipo_documento', 
            'numero_documento', 
            'digito_verificacion', 
            'nombre_comercial',
            'razon_social', 
            'email', 
            'email_empresarial',
            'telefono_celular', 
            'direccion_notificaciones', 
            'direccion_residencia',
            'pais_residencia',
            'departamento_residencia', 
            'municipio_residencia',
            'cod_municipio_notificacion_nal',
            'ubicacion_georeferenciada',
            'telefono_celular_empresa',
            'telefono_empresa_2',
            'telefono_empresa',
            'acepta_notificacion_sms',
            'acepta_notificacion_email',
            'acepta_tratamiento_datos'
        ]
            
    
class PersonaNaturalPostSerializer(serializers.ModelSerializer):
    numero_documento = serializers.CharField(max_length=20, min_length=5)
    primer_nombre = serializers.CharField(max_length=30)
    primer_apellido = serializers.CharField(max_length=30)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Personas.objects.all())])
    telefono_celular = serializers.CharField(max_length=15, min_length=10)
    
    class Meta:
        model = Personas
        fields = [
            'id_persona', 
            'tipo_persona', 
            'tipo_documento', 
            'numero_documento', 
            'digito_verificacion', 
            'nombre_comercial', 
            'primer_nombre', 
            'segundo_nombre', 
            'primer_apellido', 
            'segundo_apellido', 
            'fecha_nacimiento', 
            'email', 
            'telefono_celular',
            'sexo',
            'estado_civil',
            'pais_nacimiento',
            'email_empresarial',
            'ubicacion_georeferenciada',
            'telefono_fijo_residencial',            
            'telefono_empresa',
            'pais_residencia',
            'departamento_residencia',
            'municipio_residencia',
            'direccion_residencia',
            'direccion_laboral',
            'direccion_residencia_ref',
            'direccion_notificaciones',
            'cod_municipio_laboral_nal',
            'acepta_notificacion_sms',
            'acepta_notificacion_email',
            'acepta_tratamiento_datos'
        ]
        
        validators = [
            UniqueTogetherValidator(
                queryset = Personas.objects.all(),
                fields = ['tipo_documento', 'numero_documento']
            )
        ]
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
    numero_documento = serializers.CharField(max_length=20, min_length=5)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Personas.objects.all())])
    razon_social = serializers.CharField(max_length=200)
    telefono_celular = serializers.CharField(max_length=15, min_length=10)
    direccion_notificaciones = serializers.CharField(max_length=255, min_length=5)

    class Meta:
        model = Personas
        fields = [
            'id_persona', 
            'tipo_persona', 
            'tipo_documento', 
            'numero_documento', 
            'digito_verificacion', 
            'nombre_comercial',
            'razon_social', 
            'email', 
            'email_empresarial',
            'direccion_notificaciones', 
            'direccion_residencia',
            'pais_residencia',
            'departamento_residencia', 
            'municipio_residencia',
            'cod_municipio_notificacion_nal',
            'ubicacion_georeferenciada',
            'telefono_celular',
            'telefono_celular_empresa',
            'telefono_empresa_2',
            'telefono_empresa',
            'acepta_notificacion_sms',
            'acepta_notificacion_email',
            'acepta_tratamiento_datos'
        ]
        validators = [
           UniqueTogetherValidator(
               queryset=Personas.objects.all(),
               fields = ['tipo_documento', 'numero_documento']
           )
        ]
        
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