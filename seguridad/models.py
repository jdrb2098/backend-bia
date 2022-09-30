from random import choices
from tkinter.tix import Tree
from turtle import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
paises_CHOICES = (
    ('AF', 'AFGHANISTAN'),
    ('AL', 'ALBANIA'),
    ('DZ', 'ALGERIA'),
    ('AS', 'AMERICAN SAMOA'),
    ('AD', 'ANDORRA'),
    ('AO', 'ANGOLA'),
    ('AI', 'ANGUILLA'),
    ('AQ', 'ANTARCTICA'),
    ('AG', 'ANTIGUA AND BARBUDA'),
    ('AR', 'ARGENTINA'),
    ('AM', 'ARMENIA'),
    ('AW', 'ARUBA'),
    ('AU', 'AUSTRALIA'),
    ('AT', 'AUSTRIA'),
    ('AZ', 'AZERBAIJAN'),
    ('BS', 'BAHAMAS'),
    ('BH', 'BAHRAIN'),
    ('BD', 'BANGLADESH'),
    ('BB', 'BARBADOS'),
    ('BY', 'BELARUS'),
    ('BE', 'BELGIUM'),
    ('BZ', 'BELIZE'),
    ('BJ', 'BENIN'),
    ('BM', 'BERMUDA'),
    ('BT', 'BHUTAN'),
    ('BO', 'BOLIVIA'),
    ('BA', 'BOSNIA AND HERZEGOVINA'),
    ('BW', 'BOTSWANA'),
    ('BV', 'BOUVET ISLAND'),
    ('BR', 'BRAZIL'),
    ('IO', 'BRITISH INDIAN OCEAN TERRITORY'),
    ('BN', 'BRUNEI DARUSSALAM'),
    ('BG', 'BULGARIA'),
    ('BF', 'BURKINA FASO'),
    ('BI', 'BURUNDI'),
    ('KH', 'CAMBODIA'),
    ('CM', 'CAMEROON'),
    ('CA', 'CANADA'),
    ('CV', 'CAPE VERDE'),
    ('KY', 'CAYMAN ISLANDS'),
    ('CF', 'CENTRAL AFRICAN REPUBLIC'),
    ('TD', 'CHAD'),
    ('CL', 'CHILE'),
    ('CN', 'CHINA'),
    ('CX', 'CHRISTMAS ISLAND'),
    ('CC', 'COCOS (KEELING) ISLANDS'),
    ('CO', 'COLOMBIA'),
    ('KM', 'COMOROS'),
    ('CG', 'CONGO'),
    ('CD', 'CONGO, THE DEMOCRATIC REPUBLIC OF'),
    ('CK', 'COOK ISLANDS'),
    ('CR', 'COSTA RICA'),
    ('CI', "CÃ”TE D'IVOIRE"),
    ('HR', 'CROATIA'),
    ('CU', 'CUBA'),
    ('CY', 'CYPRUS'),
    ('CZ', 'CZECH REPUBLIC'),
    ('DK', 'DENMARK'),
    ('DJ', 'DJIBOUTI'),
    ('DM', 'DOMINICA'),
    ('DO', 'DOMINICAN REPUBLIC'),
    ('EC', 'ECUADOR'),
    ('EG', 'EGYPT'),
    ('SV', 'EL SALVADOR'),
    ('GQ', 'EQUATORIAL GUINEA'),
    ('ER', 'ERITREA'),
    ('EE', 'ESTONIA'),
    ('ET', 'ETHIOPIA'),
    ('FK', 'FALKLAND ISLANDS (MALVINAS)'),
    ('FO', 'FAROE ISLANDS'),
    ('FJ', 'FIJI'),
    ('FI', 'FINLAND'),
    ('FR', 'FRANCE'),
    ('GF', 'FRENCH GUIANA'),
    ('PF', 'FRENCH POLYNESIA'),
    ('TF', 'FRENCH SOUTHERN TERRITORIES'),
    ('GA', 'GABON'),
    ('GM', 'GAMBIA'),
    ('GE', 'GEORGIA'),
    ('DE', 'GERMANY'),
    ('GH', 'GHANA'),
    ('GI', 'GIBRALTAR'),
    ('GR', 'GREECE'),
    ('GL', 'GREENLAND'),
    ('GD', 'GRENADA'),
    ('GP', 'GUADELOUPE'),
    ('GU', 'GUAM'),
    ('GT', 'GUATEMALA'),
    ('GN', 'GUINEA'),
    ('GW', 'GUINEA'),
    ('GY', 'GUYANA'),
    ('HT', 'HAITI'),
    ('HM', 'HEARD ISLAND AND MCDONALD ISLANDS'),
    ('HN', 'HONDURAS'),
    ('HK', 'HONG KONG'),
    ('HU', 'HUNGARY'),
    ('IS', 'ICELAND'),
    ('IN', 'INDIA'),
    ('ID', 'INDONESIA'),
    ('IR', 'IRAN, ISLAMIC REPUBLIC OF'),
    ('IQ', 'IRAQ'),
    ('IE', 'IRELAND'),
    ('IL', 'ISRAEL'),
    ('IT', 'ITALY'),
    ('JM', 'JAMAICA'),
    ('JP', 'JAPAN'),
    ('JO', 'JORDAN'),
    ('KZ', 'KAZAKHSTAN'),
    ('KE', 'KENYA'),
    ('KI', 'KIRIBATI'),
    ('KP', "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF"),
    ('KR', 'KOREA, REPUBLIC OF'),
    ('KW', 'KUWAIT'),
    ('KG', 'KYRGYZSTAN'),
    ('LA', "LAO PEOPLE'S DEMOCRATIC REPUBLIC"),
    ('LV', 'LATVIA'),
    ('LB', 'LEBANON'),
    ('LS', 'LESOTHO'),
    ('LR', 'LIBERIA'),
    ('LY', 'LIBYAN ARAB JAMAHIRIYA'),
    ('LI', 'LIECHTENSTEIN'),
    ('LT', 'LITHUANIA'),
    ('LU', 'LUXEMBOURG'),
    ('MO', 'MACAO'),
    ('MK', 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF'),
    ('MG', 'MADAGASCAR'),
    ('MW', 'MALAWI'),
    ('MY', 'MALAYSIA'),
    ('MV', 'MALDIVES'),
    ('ML', 'MALI'),
    ('MT', 'MALTA'),
    ('MH', 'MARSHALL ISLANDS'),
    ('MQ', 'MARTINIQUE'),
    ('MR', 'MAURITANIA'),
    ('MU', 'MAURITIUS'),
    ('YT', 'MAYOTTE'),
    ('MX', 'MEXICO'),
    ('FM', 'MICRONESIA, FEDERATED STATES OF'),
    ('MD', 'MOLDOVA, REPUBLIC OF'),
    ('MC', 'MONACO'),
    ('MN', 'MONGOLIA'),
    ('MS', 'MONTSERRAT'),
    ('MA', 'MOROCCO'),
    ('MZ', 'MOZAMBIQUE'),
    ('MM', 'MYANMAR'),
    ('NA', 'NAMIBIA'),
    ('NR', 'NAURU'),
    ('NP', 'NEPAL'),
    ('NL', 'NETHERLANDS'),
    ('AN', 'NETHERLANDS ANTILLES'),
    ('NC', 'NEW CALEDONIA'),
    ('NZ', 'NEW ZEALAND'),
    ('NI', 'NICARAGUA'),
    ('NE', 'NIGER'),
    ('NG', 'NIGERIA'),
    ('NU', 'NIUE'),
    ('NF', 'NORFOLK ISLAND'),
    ('MP', 'NORTHERN MARIANA ISLANDS'),
    ('NO', 'NORWAY'),
    ('OM', 'OMAN'),
    ('PK', 'PAKISTAN'),
    ('PW', 'PALAU'),
    ('PS', 'PALESTINIAN TERRITORY, OCCUPIED'),
    ('PA', 'PANAMA'),
    ('PG', 'PAPUA NEW GUINEA'),
    ('PY', 'PARAGUAY'),
    ('PE', 'PERU'),
    ('PH', 'PHILIPPINES'),
    ('PN', 'PITCAIRN'),
    ('PL', 'POLAND'),
    ('PT', 'PORTUGAL'),
    ('PR', 'PUERTO RICO'),
    ('QA', 'QATAR'),
    ('RE', 'RÃ‰UNION'),
    ('RO', 'ROMANIA'),
    ('RU', 'RUSSIAN FEDERATION'),
    ('RW', 'RWANDA'),
    ('SH', 'SAINT HELENA'),
    ('KN', 'SAINT KITTS AND NEVIS'),
    ('LC', 'SAINT LUCIA'),
    ('PM', 'SAINT PIERRE AND MIQUELON'),
    ('VC', 'SAINT VINCENT AND THE GRENADINES'),
    ('WS', 'SAMOA'),
    ('SM', 'SAN MARINO'),
    ('ST', 'SAO TOME AND PRINCIPE'),
    ('SA', 'SAUDI ARABIA'),
    ('SN', 'SENEGAL'),
    ('CS', 'SERBIA AND MONTENEGRO'),
    ('SC', 'SEYCHELLES'),
    ('SL', 'SIERRA LEONE'),
    ('SG', 'SINGAPORE'),
    ('SK', 'SLOVAKIA'),
    ('SI', 'SLOVENIA'),
    ('SB', 'SOLOMON ISLANDS'),
    ('SO', 'SOMALIA'),
    ('ZA', 'SOUTH AFRICA'),
    ('GS', 'SOUTH GEORGIA AND SOUTH SANDWICH ISLANDS'),
    ('ES', 'SPAIN'),
    ('LK', 'SRI LANKA'),
    ('SD', 'SUDAN'),
    ('SR', 'SURINAME'),
    ('SJ', 'SVALBARD AND JAN MAYEN'),
    ('SZ', 'SWAZILAND'),
    ('SE', 'SWEDEN'),
    ('CH', 'SWITZERLAND'),
    ('SY', 'SYRIAN ARAB REPUBLIC'),
    ('TW', 'TAIWAN, PROVINCE OF CHINA'),
    ('TJ', 'TAJIKISTAN'),
    ('TZ', 'TANZANIA, UNITED REPUBLIC OF'),
    ('TH', 'THAILAND'),
    ('TL', 'TIMOR'),
    ('TG', 'TOGO'),
    ('TK', 'TOKELAU'),
    ('TO', 'TONGA'),
    ('TT', 'TRINIDAD AND TOBAGO'),
    ('TN', 'TUNISIA'),
    ('TR', 'TURKEY'),
    ('TM', 'TURKMENISTAN'),
    ('TC', 'TURKS AND CAICOS ISLANDS'),
    ('TV', 'TUVALU'),
    ('UG', 'UGANDA'),
    ('UA', 'UKRAINE'),
    ('AE', 'UNITED ARAB EMIRATES'),
    ('GB', 'UNITED KINGDOM'),
    ('US', 'UNITED STATES'),
    ('UM', 'UNITED STATES MINOR OUTLYING ISLANDS'),
    ('UY', 'URUGUAY'),
    ('UZ', 'UZBEKISTAN'),
    ('VU', 'VANUATU'),
    ('VN', 'VIET NAM'),
    ('VG', 'VIRGIN ISLANDS, BRITISH'),
    ('VI', 'VIRGIN ISLANDS, U.S.'),
    ('WF', 'WALLIS AND FUTUNA'),
    ('EH', 'WESTERN SAHARA'),
    ('YE', 'YEMEN'),
    ('ZW', 'ZIMBABWE')
)
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
    pais = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T002Cod_Pais')
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


class Permisos(models.Model):
    
    class cod_permiso_CHOICES(models.TextChoices):
        crear = "CR", "Crear"
        borrar = "BO", "Borrar"
        actualizar= "CO","Consultar"
        ejecutar="EJ","Ejecutar"
        aprobar="AP","Aprobar"
        
    nombre_permiso = models.CharField(max_length=20, db_column='TznombrePermiso')
    cod_permiso = models.CharField(max_length=2,primary_key=True, editable=False,choices=cod_permiso_CHOICES.choices, db_column='TzCodPermiso')

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
    class subsistema_CHOICES(models.TextChoices):
        conservacion="CONS","Conservación"
        gestion_Documental="GEST","Gestión Documental"
        recurso_hidrico="RECU","Recurso Hídrico"
        tramites_servicio="TRAM","Trámites y servicios"
        seguimiento_planes="PLAN","Seguimiento a planes"
        recaudo="RECA","Recaudo"
        
    id_modulo=models.AutoField(primary_key=True, editable=False, db_column='TzIdModulo')
    nombre_modulo=models.CharField(max_length=70,db_column='TznombreModulo')
    subsistema=models.CharField(max_length=4,choices=subsistema_CHOICES.choices,db_column='Tzsubsistema')# Juan camilo textchoices 
    descripcion = models.CharField(max_length=255, db_column='Tzdescripcion')
    
    class Meta:
        db_table= 'TzModulos'
        verbose_name='Modulo'
        verbose_name_plural='Modulos'
        
    def __str__(self):
         return self.nombre_modulo

class PermisosModulo(models.Model):
    
    id_modulo=models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='TzIdModulo')
    cod_permiso=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCodPermiso') #juan Camilo Text Choices
  
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
    class Sexo(models.TextChoices):
        Hombre = "H", "Hombre"
        Mujer = "M", "Mujer"
        InterSexual = "I", "Intersexual"  
    class EstadoCivil(models.TextChoices):
        Casado = "C", "Casado"
        Soltero = "S", "soltero"
        UnionLibre = "U", "Unión Libre"
        Viudo = "V", "Viudo"
        Divorciado = "D", "Divorciado"
    class TiposDocumento(models.TextChoices):
        NUIP = "UN", "NUIP"
        CedulaExtrangeria = "CE", "Cédula Extrangeria"
        Pasaporte = "PA", "Pasaporte"
        PermisoEspecialDePermanencia = "PE", "Permiso Especial de Permanencia"
        RegistroCivil = "RC", "Registro Civil"
        TarjetaDeIdentidad = "TI", "Tarjeta de Identidad"
        CedulaDeCiudadania = "CC", "Cédula de Ciudadania"

    class TipoPersona(models.TextChoices):
        Natural = "N", "Natural"
        Juridica = "J", "Juridica"

    id_persona = models.AutoField(primary_key=True, editable=False, db_column='T010IdPersona')
    tipo_persona = models.CharField(choices=-TipoPersona.choices, db_column='T010tipoPersona')
    tipo_documento = models.CharField(choices=TiposDocumento.choices, db_column='T010Cod_TipoDocumento')
    numero_documento = models.CharField(max_length=20, unique=True, db_column='T010nroDocumento')
    digito_verificacion = models.CharField(max_length=1, null=True, blank=True, db_column='T010digitoVerificacion')
    primer_nombre = models.CharField(max_length=30, null=True, blank=True, db_column='T010primerNombre')
    segundo_nombre = models.CharField(max_length=30, null=True, blank=True, db_column='T010segundoNombre')
    primer_apellido = models.CharField(max_length=30, null=True, blank=True, db_column='T010primerApellido')
    segundo_apellido = models.CharField(max_length=30, null=True, blank=True, db_column='T010segundoApellido')
    nombre_comercial = models.CharField(max_length=200, null=True, blank=True, db_column='T010nombreComercial')
    razon_social = models.CharField(max_length=200, null=True, blank=True, db_column='T010razonSocial')
    pais_residencia = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T010codPaisResidencia')
    municipio_residencia = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True, related_name='municipio_residencia', db_column='T010Cod_MunicipioResidenciaNal')
    direccion_residencia = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirResidencia')
    direccion_residencia_ref = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirResidenciaReferencia')
    ubicacion_georeferenciada = models.CharField(max_length=50, db_column='T010ubicacionGeoreferenciada')
    direccion_laboral = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirLaboralNal')
    direccion_notificaciones = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirNotificacion')
    pais_nacimiento = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T010Cod_Pais_Nacimiento')
    fecha_nacimiento = models.DateField(blank=True,null=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, db_column='T010Cod_Sexo')
    estado_civil = models.CharField(choices=EstadoCivil.choices, null=True, blank=True, db_column='T010Cod_Estado_Civil')
    representante_legal = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True, db_column='T010Id_PersonaRepLegal')
    email = models.EmailField(max_length=255, unique=True, db_column='T010emailNotificación')
    email_empresarial = models.EmailField(max_length=255, null=True, blank=True, db_column='T010emailEmpresarial')
    telefono_fijo_residencial = models.CharField(max_length=15, null=True, blank=True, db_column='T010telFijoResidencial')
    telefono_celular = models.CharField(max_length=15, null=True, blank=True, db_column='T010telCelular')
    telefono_empresa = models.CharField(max_length=15, null=True, blank=True, db_column='T010telEmpresa')
    cod_municipio_laboral_nal = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, related_name='municipio_laboral', db_column='T010Cod_MunicipioLaboralNal')
    cod_municipio_notificacion_nal = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, related_name='municipio_notificacion', db_column='T010Cod_MunicipioNotificacionNal')
    telefono_celular_empresa = models.CharField(max_length=15, blank=True, null=True, db_column='T010telCelularEmpresa')
    telefono_empresa_2 =models.CharField(max_length=15, null=True, blank=True, db_column='T010telEmpresa2')
    cod_pais_nacionalidad_empresa = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T010Cod_PaisNacionalidadDeEmpresa')
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
    
    class tipo_direccion_CHOICES(models.TextChoices):
        Laboral = "L", "Laboral"
        Residencia = "J", "Residencia"
        Notificacion = "N","Notificacion"
        
    id_historico_direccion = models.AutoField(primary_key=True, editable=False, db_column='T015IdHistoDireccion')
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column = 'T015Id_Persona')    
    direccion = models.CharField(max_length=255, db_column='T015direccion')
    cod_municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T015Cod_MunicipioEnCol')
    cod_pais_exterior = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T015Cod_PaisEnElExterior')
    tipo_direccion = models.CharField(max_length=1, choices=tipo_direccion_CHOICES.choices,db_column='T015TipoDeDireccion')
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
        
class SucursalesEmpresas(models.Model):
    id_empresa = models.ForeignKey(Personas,on_delete=models.CASCADE,  db_column='T012IdEmpresa')#Es primary_key????
    numero_sucursal = models.AutoField(primary_key=True, editable=False, db_column='T012NroSucursal')
    sucursal = models.CharField(max_length=255, db_column='T012sucursal')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T012codMunicipio')
    direccion = models.CharField(max_length=255, db_column='T012direccion')
    direccion_sucursal_georeferenciada = models.CharField(max_length=50, db_column='T012ubicacionGeoreferenciada') ##Foreing_Key con tabla persoas??
    pais_sucursal_exterior = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T012cod_sucursal_exterior')
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
    
    class tipo_usuario_CHOICES(models.TextChoices):
        interno="I","Interno"
        externo="E","Externo"
        
    id_usuario = models.AutoField(primary_key=True, editable=False, db_column='TzIdUsuario')
    nombre_de_usuario = models.CharField(max_length=30, db_column='TznombreUsuario')
    persona = models.OneToOneField(Personas, on_delete=models.SET_NULL, null=True,db_column='TzId_Persona')
    is_active = models.BooleanField(max_length=1, default=False, db_column='Tzactivo')
    is_staff = models.BooleanField(default=False, db_column='Tzstaff')#Añadido por Juan
    is_superuser = models.BooleanField(default=False, db_column='TzsuperUser')  #Añadido por Juan
    is_blocked = models.BooleanField(max_length=1,default=False, db_column='Tzbloqueado')
    id_usuario_creador = models.ForeignKey('self', on_delete=models.SET_NULL,null=True, db_column="TzId_Usuario_Creador")
    created_at = models.DateTimeField(auto_now_add=True, db_column='TzfechaCreacion')
    activated_at = models.DateTimeField(null=True, db_column='TzfechaActivacionInicial')
    tipo_usuario = models.CharField(max_length=1, choices=tipo_usuario_CHOICES.choices, db_column='TztipoUsuario') #Juan Camilo Text Choices
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
    
    class subsistema_CHOICES(models.TextChoices):
        Almacen="ALMA","Almacen"
        Conservacion="CONS","Conservación"
        Gestion_Documental="GEST","Gestión Documental"
        Recurso_hidrico="RECU","Recurso Hídrico"
        tramites_servicios="TRAM","Trámites y servicios"
        Seguimiento_planes="PLAN","Seguimiento a planes"
        Recaudo="RECA","Recaudo"
        
    id_auditoria=models.AutoField(db_column='TzIdAuditoria',primary_key=True, editable=False)
    id_usuario=models.ForeignKey(User, on_delete=models.CASCADE, db_column='TzId_Usuario') ##No tiene definido tipo de relacion
    id_modulo=models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='TzId_Modulo')
    id_cod_operacion=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCod_Operacion')
    fecha_accion=models.DateField(db_column='TzfechaAccion')
    subsistema=models.CharField(max_length=4,choices=subsistema_CHOICES.choices, db_column='Tzsubsistema') #Juan camilo text choices
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
    class OperacionesSobreUsuario(models.TextChoices):
        Activar = "A", "Activar"
        Desactivar = "D", "Desactivar"
        Bloquear = "B", "Bloquear"
        Unlock = "U", "Unlock"

    id_historico = models.AutoField(primary_key=True, editable=False, db_column='T014IdHistorico')
    id_usuario_afectado = models.ForeignKey(User, on_delete=models.CASCADE, db_column='T014Id_Usuario_Afectado')
    cod_operacion = models.CharField(choices=OperacionesSobreUsuario.choices, db_column='T014Cod_Operacion')
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

