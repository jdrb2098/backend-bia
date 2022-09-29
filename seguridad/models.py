from tkinter.tix import Tree
from turtle import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
# Create your models here.
class Paises(models.Model):
    nombre = models.CharField(max_length=50, db_column='T003nombre')
    cod_pais = models.CharField(primary_key=True,max_length=2, db_column='T003CodPais')
    def __str__(self):
        return self.cod_pais
    class Meta:
        db_table = "T003Paises"
        verbose_name='Pais'
        verbose_name_plural='Paises'
        

class EstadoCivil (models.Model):
    nombre = models.CharField(max_length=20, db_column='T005nombre')
    cod_estado_civil = models.CharField(primary_key=True,max_length=1, db_column='T005CodEstadoCivil')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T005EstadoCivil'
        verbose_name='Estado civil'
        verbose_name_plural='Estado civil'

class Departamento (models.Model):
    nombre = models.CharField(max_length=30, db_column='T002nombre')
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE, db_column='T002Cod_Pais')
    cod_departamento = models.CharField(primary_key=True, max_length=2, db_column='T002CodDepartamento')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T002DepartamentosPais'
        verbose_name='Departamento'
        verbose_name_plural='Departamentos'



class Municipio (models.Model):
    nombre = models.CharField(max_length=30, db_column='T001nombre')
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='T001Cod_Departamentos')
    cod_municipio = models.CharField(primary_key=True, max_length=5, db_column = 'T001CodMunicipio')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T001MunicipiosDepartamento'
        verbose_name='Municipio'
        verbose_name_plural='Municipios'


class Sexo(models.Model):
    nombre = models.CharField(max_length=20, db_column='T004nombre')
    cod_sexo = models.CharField(primary_key=True,max_length=1, db_column='T004CodSexo')

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'T004Sexo'
        verbose_name='Sexo'
        verbose_name_plural='Sexo'

class Permisos(models.Model):
    nombre_permiso = models.CharField(max_length=20, db_column='TznombrePermiso')
    cod_permiso = models.AutoField(max_length=2,primary_key=True, editable=False, db_column='TzCodPermiso')

    def __str__(self):
        return self.nombre_permiso

    class Meta:
        db_table = "TzPermisos"
        verbose_name='Permiso'
        verbose_name_plural='Permisos'



class OperacionesSobreUsuario(models.Model):
    cod_operacion = models.AutoField(primary_key=True, editable=False, db_column='T008CodOperacion')
    nombre = models.CharField(max_length=20, db_column='T008nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T008OperacionesSobreUsusario'
        verbose_name='Operacion sobre usuario'
        verbose_name_plural='Operaciones sobre usuario'

class TiposDocumento(models.Model):
    cod_tipo_documento = models.AutoField(primary_key=True, editable=False, db_column='T006CodTipoDocumento')
    nombre = models.CharField(max_length=40, db_column='T006nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T006TiposDocumento'
        verbose_name='Tipo de documento'
        verbose_name_plural='Tipos de documento'

    
class Roles(models.Model):
    id_rol=models.AutoField(primary_key=True, editable=False, db_column='TzIdRol')
    nombre_rol=models.CharField(max_length=100, db_column='TznombreRol')
    descripcion_rol=models.CharField(max_length=255,db_column='TzdescripcionRol')
    
    class Meta:
        db_table= 'TzRoles'
        verbose_name='Rol'
        verbose_name_plural='Roles'
        
    def __str__(self):
         return self.nombre_rol
    
        
class Modulos(models.Model):
    id_modulo=models.AutoField(primary_key=True, editable=False, db_column='TzIdModulo')
    nombre_modulo=models.CharField(max_length=70,db_column='TznombreModulo')
    subsistema=models.CharField(max_length=4,db_column='Tzsubsistema')
    descripcion = models.CharField(max_length=255, db_column='Tzdescripcion')
    
    class Meta:
        db_table= 'TzModulos'
        verbose_name='Modulo'
        verbose_name_plural='Modulos'
        
    def __str__(self):
         return self.nombre_modulo

class PermisosModulo(models.Model):
    id_modulo=models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='TzIdModulo')
    cod_permiso=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCodPermiso')
  
    class Meta:
        db_table= 'TzPermisos_Modulo'
        verbose_name='Permiso de módulo'
        verbose_name_plural='Permisos de módulo'

class PermisosModuloRol(models.Model):
    id_rol=models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='TzIdRol')
    id_modulo=models.ForeignKey(PermisosModulo, on_delete=models.CASCADE, db_column='TzIdModulo')
    cod_permiso=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCodPermiso')
    
    class Meta:
        db_table= 'TzPermisos_Modulo_Rol'
        verbose_name='Permiso de modulo de rol'
        verbose_name_plural='Permisos de modulo de roles'
        
class Personas(models.Model):
    id_persona = models.AutoField(primary_key=True, editable=False, db_column='T010IdPersona')
    tipo_persona = models.CharField(max_length=1, db_column='T010tipoPersona')
    tipo_documento = models.ForeignKey(TiposDocumento, on_delete=models.CASCADE, db_column='T010Cod_TipoDocumento')
    numero_documento = models.CharField(max_length=20, unique=True, db_column='T010nroDocumento')
    digito_verificacion = models.CharField(max_length=1, null=True, blank=True, db_column='T010digitoVerificacion')
    primer_nombre = models.CharField(max_length=30, null=True, blank=True, db_column='T010primerNombre')
    segundo_nombre = models.CharField(max_length=30, null=True, blank=True, db_column='T010segundoNombre')
    primer_apellido = models.CharField(max_length=30, null=True, blank=True, db_column='T010primerApellido')
    segundo_apellido = models.CharField(max_length=30, null=True, blank=True, db_column='T010segundoApellido')
    nombre_comercial = models.CharField(max_length=200, null=True, blank=True, db_column='T010nombreComercial')
    razon_social = models.CharField(max_length=200, null=True, blank=True, db_column='T010razonSocial')
    pais_residencia = models.ForeignKey(Paises, on_delete=models.CASCADE, null=True, blank=True, db_column='T010codPaisResidencia')
    municipio_residencia = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True, related_name='municipio_residencia', db_column='T010Cod_MunicipioResidenciaNal')
    direccion_residencia = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirResidencia')
    direccion_residencia_ref = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirResidenciaReferencia')
    ubicacion_georeferenciada = models.CharField(max_length=50, db_column='T010ubicacionGeoreferenciada')
    direccion_laboral = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirLaboralNal')
    direccion_notificaciones = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirNotificacion')
    pais_nacimiento = models.ForeignKey(Paises, on_delete=models.SET_NULL, null=True, db_column='T010Cod_Pais_Nacimiento')
    fecha_nacimiento = models.DateField(blank=True,null=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.SET_NULL, blank=True, null=True, db_column='T010Cod_Sexo')
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.SET_NULL, null=True, blank=True, db_column='T010Cod_Estado_Civil')
    representate_legal = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,db_column='T010Id_PersonaRepLegal')
    email = models.EmailField(max_length=255, unique=True, db_column='T010emailNotificación')
    email_empresarial = models.EmailField(max_length=255, null=True, blank=True, db_column='T010emailEmpresarial')
    telefono_fijo_residencial = models.CharField(max_length=15, null=True, blank=True, db_column='T010telFijoResidencial')
    telefono_celular = models.CharField(max_length=15, null=True, blank=True, db_column='T010telCelular')
    telefono_empresa = models.CharField(max_length=15, null=True, blank=True, db_column='T010telEmpresa')
    cod_municipio_laboral_nal = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, related_name='municipio_laboral', db_column='T010Cod_MunicipioLaboralNal')
    cod_municipio_notificacion_nal = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, related_name='municipio_notificacion', db_column='T010Cod_MunicipioNotificacionNal')
    telefono_celular_empresa = models.CharField(max_length=15, blank=True, null=True, db_column='T010telCelularEmpresa')
    telefono_empresa_2 =models.CharField(max_lenth=15, null=True, blank=True, db_column='T010telEmpresa2')
    cod_pais_nacionalidad_empresa = models.ForeignKey(Paises, on_delete=models.SET_NULL, null=True, blank=True, db_column='T010Cod_PaisNacionalidadDeEmpresa')
    acepta_notificacion_sms = models.BooleanField(default=False, db_column='T010AceptaNotificacionSMS')
    acepta_notificacion_email = models.BooleanField(default=False, db_column='T010AceptaNotificacionEmail')
    acepta_tratamiento_datos = models.BooleanField(default=False, db_column='T010AceptaTratamientoDeDatos')
    
    def __str__(self):
        return str(self.id_persona)
    
    class Meta:
        db_table = 'T010Personas'
        verbose_name='Persona'
        verbose_name_plural='Personas'
        
class HistoricoDireccion(models.Model):
    tipo_direccion_CHOICES = (
        ('L', 'Laboral'),
        ('R', 'Residencia'),
        ('N', 'Notificación'),
    )
    id_historico_direccion = models.AutoField(primary_key=True, editable=False, db_column='T015IdHistoDireccion')
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column = 'T015Id_Persona')    
    direccion = models.CharField(max_length=255, db_column='T015direccion')
    cod_municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T015Cod_MunicipioEnCol')
    cod_pais_exterior = models.ForeignKey(Paises, on_delete=models.SET_NULL, blank=True, null=True, db_column='T015Cod_PaisEnElExterior')
    tipo_direccion = models.CharField(max_length=1, choices=tipo_direccion_CHOICES,db_column='T015TipoDeDireccion')
    fecha_cambio = models.DateTimeField(auto_now_add=True, db_column='T015fechaCambio')
        
    def __str__(self):
        return str(self.id_historico_direccion)

    class Meta:
        db_table = 'T015HistoricoDirecciones'
        verbose_name='Histórico de dirección '
        verbose_name_plural='Histórico de direcciones'
        
class ApoderadoPersona (models.Model):
    persona_poderdante = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T013IdPersonaPoderdante')
    id_proceso = models.CharField(max_length=50, db_column = 'T013IdProceso') #Pendiente por foreingKey de tabla procesos
    consecutivo_del_proceso = models.AutoField(primary_key=True, editable=False, db_column = 'T013ConsecDelProceso') #Pendiente por foreingKey de tabla procesos
    persona_apoderada = models.ForeignKey(Personas, on_delete=models.CASCADE,  related_name='persona_apoderada', db_column = 'T013IdPersonaApoderada')
    fecha_inicio = models.DateTimeField(db_column = 'T013fechaInicio')
    fecha_cierre = models.DateTimeField(db_column = 'T013fechaCierre', null=True, blank=True)
    
    def __str__(self):
        return str(self.persona_poderdante)

    class Meta:
        db_table = 'T013Apoderados_Persona'    
        verbose_name='Apoderado'
        verbose_name_plural='Apoderados'
           
class HistoricoEmails(models.Model):
    id_histo_email = models.AutoField(primary_key=True, db_column='T016IdHistoEmail')
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T016Id_Persona')
    email_notificacion = models.EmailField(max_length=100, db_column='T016emailDeNotificacion')
    fecha_cambio = models.DateTimeField(auto_now=True, db_column='T016fechaCambio')

    def __str__(self):
        return self.email_notificacion

    class Meta:
        db_table = 'T016HistoricoEmails'      
        verbose_name='Historico de email'
        verbose_name_plural='Históricos de email'
        
class SucursalesEmpresa(models.Model):
    id_empresa = models.ForeignKey(Personas,on_delete=models.CASCADE,  db_column='T012IdEmpresa')#Es primary_key????
    numero_sucursal = models.AutoField(primary_key=True, editable=False, db_column='T012NroSucursal')
    sucursal = models.CharField(max_length=255, db_column='T012sucursal')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T012codMunicipio')
    direccion = models.CharField(max_length=255, db_column='T012direccion')
    direccion_sucursal_georeferenciada = models.CharField(max_length=50, db_column='T012ubicacionGeoreferenciada') ##Foreing_Key con tabla persoas??
    pais_sucursal_exterior = models.ForeignKey(Paises, on_delete=models.SET_NULL, null=True, blank=True, db_column='T012cod_sucursal_exterior')
    direccion_correspondencias = models.CharField(max_length=50, db_column='T012direccionCorrespondencias')
    email_sucursal = models.EmailField(max_length=255, db_column='T012emailSucursal')
    telefono_sucursal = models.CharField(max_length=10, db_column='T012telContactoSucursal')
    es_principal = models.BooleanField(default=False, db_column='T012esPrincipal')
    
    def __str__(self):
        return self.sucursal
    
    class Meta:
        db_table = 'T012SucursalesEempresa'
        verbose_name='Sucursal'
        verbose_name_plural='Sucursales'
        
class User(AbstractBaseUser,PermissionsMixin):
    id_usuario: models.AutoField(primary_key=True, editable=False, db_column='TzIdUsuario')
    nombre_de_usuario = models.CharField(max_length=30, db_column='TznombreUsuario')
    persona = models.OneToOneField(Personas, on_delete=models.CASCADE,db_column='TzId_Persona')
    is_active = models.BooleanField(max_length=1, default=False, db_column='Tzactivo')
    is_staff = models.BooleanField(default=False, db_column='Tzstaff')#Añadido por Juan
    is_superuser = models.BooleanField(default=False, db_column='TzsuperUser')  #Añadido por Juan
    is_blocked = models.BooleanField(max_length=1,default=False, db_column='Tzbloqueado')
    id_usuario_creador = models.ForeignKey('self', on_delete=models.CASCADE, db_column="TzId_Usuario_Creador")
    created_at = models.DateTimeField(auto_now_add=True, db_column='TzfechaCreacion')
    activated_at = models.DateTimeField(null=True, db_column='TzfechaActivacionInicial')
    tipo_usuario = models.CharField(max_length=1, db_column='TztipoUsuario')
    email = models.EmailField( unique=True, db_column='TzemailUsuario') #Añadido por Juan
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    
    class Meta:
        db_table = 'TzUsuarios'
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'

class UsuariosRol(models.Model):
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True, db_column='TzIdRol')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='TzIdUsuario')

    class Meta:
        db_table='TzUsuarios_Rol'
        verbose_name='Rol de usuario'
        verbose_name_plural='Roles de usuario'

class Auditorias(models.Model):
    id_auditoria=models.AutoField(db_column='TzIdAuditoria',primary_key=True, editable=False)
    id_usuario=models.ForeignKey(User, on_delete=models.CASCADE, db_column='TzId_Usuario') ##No tiene definido tipo de relacion
    id_modulo=models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='TzId_Modulo')
    id_cod_operacion=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCod_Operacion')
    fecha_accion=models.DateField(db_column='TzfechaAccion')
    subsistema=models.CharField(max_length=4, db_column='Tzsubsistema')
    dirip=models.CharField(max_length=255,db_column='Tzdirip')
    descripcion=models.TextField(db_column='Tzdescripcion')
    valores_actualizados=models.CharField(max_length=255, null=True, blank=True, db_column='TzvaloresActualizado')
    
    class Meta: 
        db_table ='TzAuditorias'
        verbose_name='Auditoría'
        verbose_name_plural='Auditorías'
        
    def __str__(self):
         return str(self.id_auditoria)   
      
class HistoricoActivacion(models.Model):
    id_historico = models.AutoField(primary_key=True, editable=False, db_column='T014IdHistorico')
    id_usuario_afectado = models.ForeignKey(User, on_delete=models.CASCADE, db_column='T014Id_Usuario_Afectado')
    cod_operacion = models.ForeignKey(OperacionesSobreUsuario, on_delete=models.CASCADE, db_column='T014Cod_Operacion')
    fecha_operacion = models.DateTimeField(auto_now = True, db_column='T014fechaOperacion')
    justificacion = models.TextField( db_column='T014justificacion')
    usuario_operador = models.ForeignKey(User, related_name='usuarioOperador',on_delete=models.CASCADE, db_column='T014usuarioOperador')  #Añadido por Juan

    def __str__(self):
        return self.fecha_operacion

    class Meta:
        db_table = 'T014HistoricoActivacion'  
        verbose_name='Histórico de activación'
        verbose_name_plural='Histórico de activaciones'

class ClasesTercero(models.Model):
    id_clase_tercero = models.AutoField(primary_key=True, editable=False, db_column='T007IdClaseTercero')
    nombre = models.CharField(max_length=30, db_column='T007nombre')
    
    def __str__(self):
        return str(self.id_clase_tercero)

    class Meta:
        db_table='T007ClasesTercero'
        verbose_name='Clase tercero'
        verbose_name_plural='Clase terceros'

class ClasesTerceroPersona(models.Model):
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T011IdClaseTercero')
    id_clase_tercero = models.ForeignKey(ClasesTercero, on_delete=models.CASCADE, db_column='T011IdPersona')
    class Meta:
        db_table='T011ClasesTercero_Persona'
        verbose_name='Clase tercero persona'
        verbose_name_plural='Clase tercero personas'

