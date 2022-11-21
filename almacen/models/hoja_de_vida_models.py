from django.db import models
from seguridad.choices.municipios_choices import municipios_CHOICES
from almacen.choices.magnitudes_choices import magnitudes_CHOICES
from seguridad.models import Personas
from almacen.models.articulos_models import Articulos

class VehiculosArrendados(models.Model):
    pass

class HojaDeVidaComputadores(models.Model):
    id_hoja_de_vida = models.AutoField(db_column='T065IdHojaDeVida')
    id_articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, db_column='T065Id_Articulo', unique=True)
    sistema_operativo = models.CharField(max_length=40, db_column='T065sistemaOperativo', blank=True, Null=True)
    suite_ofimatica = models.CharField(max_length=40, db_column='T065suiteOfimatica', blank=True, Null=True)
    antivirus = models.CharField(max_length=40, db_column='T065antivirus', blank=True, Null=True)
    otras_aplicaciones = models.CharField(max_length=255, db_column='T065otrasAplicaciones', blank=True, Null=True)
    color = models.CharField(max_length=20, db_column='T065color', blank=True, Null=True)
    tipo_de_equipo = models.CharField(max_length=20, db_column='T065tipoDeEquipo', blank=True, Null=True)
    tipo_almacenamiento = models.CharField(max_length=30, db_column='T065tipoAlmacenamiento', blank=True, Null=True)
    capacidad_almacenamiento = models.CharField(max_length=20, db_column='T065capacidadAlmacenamiento', blank=True, Null=True)
    procesador = models.CharField(max_length=20, db_column='T065procesador', blank=True, Null=True)
    memoria_ram = models.SmallIntegerField(db_column='T065memoriaRAM', blank=True, Null=True)
    observaciones_adicionales = models.CharField(max_length=255, db_column='T065observacionesAdicionales', blank=True, Null=True)
    otras_aplicaciones = models.CharField(max_length=255, db_column='T065otrasAplicaciones', blank=True, Null=True)
    ruta_imagen_foto = models.CharField(max_length=255, db_column='T065rutaImagenFoto', blank=True, Null=True)
    
    def __str__(self):
        return str(self.id_hoja_de_vida)

    class Meta:
        db_table = 'T065HojaDeVidaComputadores'
        verbose_name = 'Hoja de vida computadores'
        verbose_name_plural = 'Hojas de vida computadores'
    
class HojaDeVidaVehiculos(models.Model):
    id_hoja_de_vida = models.AutoField(db_column='T066IdHojaDeVida')
    id_articulo = models.ForeignKey(Articulos, on_delete=models.SET_NULL, db_column='T066Id_Articulo', unique=True, blank=True, Null=True)
    id_vehiculo_arrendado = models.ForeignKey(VehiculosArrendados, on_delete=models.SET_NULL, db_column='T066Id_VehiculoArrendado', unique=True, blank=True, Null=True)
    cod_tipo_vehiculo = models.CharField(max_length=1, db_column='T066codTipoVehiculo', blank=True, Null=True)
    tiene_platon = models.BooleanField(db_column='T066tienePlaton', blank=True, Null=True)
    capacidad_pasajeros = models.SmallIntegerField(db_column='T066capacidadPasajeros', blank=True, Null=True)
    color = models.CharField(max_length=20, db_column='T066color', blank=True, Null=True)
    linea = models.CharField(max_length=20, db_column='T066linea', blank=True, Null=True)
    tipo_combustible = models.CharField(max_length=3, db_column='T066tipoCombustible', blank=True, Null=True)
    es_arrendado = models.BooleanField(db_column='T066esArrendado', blank=True, Null=True)
    ultimo_kilometraje = models.IntegerField(db_column='T066ultimoKilometraje', blank=True, Null=True)
    fecha_ultimo_kilometraje = models.DateField(db_column='T066fechaUltimoKilometraje', blank=True, Null=True)
    fecha_adquisicion = models.DateField(db_column='T066fechaAdquisicion', blank=True, Null=True)
    fecha_vigencia_garantia = models.DateField(db_column='T066fechaVigenciaGarantia', blank=True, Null=True)
    numero_motor = models.CharField(max_length=40, db_column='T066numeroMotor', blank=True, Null=True)
    numero_chasis = models.CharField(max_length=40, db_column='T066numeroChasis', blank=True, Null=True)
    cilindraje = models.SmallIntegerField(db_column='T066cilindraje', blank=True, Null=True)
    transmision = models.CharField(max_length=20, db_column='T066transmision', blank=True, Null=True)
    dimesion_llantas = models.SmallIntegerField(db_column='T066dimensionLlantas', blank=True, Null=True)
    id_proveedor = models.ForeignKey(Personas, on_delete=models.SET_NULL, db_column='T066Id_Proveedor', blank=True, Null=True)
    capacidad_extintor = models.SmallIntegerField(db_column='T066capacidadExtintor', blank=True, Null=True)
    tarjeta_operacion = models.CharField(max_length=20, db_column='T066tarjetaOperacion', blank=True, Null=True)
    observaciones_adicionales = models.CharField(max_length=255, db_column='T066observacionesAdicionales', blank=True, Null=True)
    es_agendable = models.BooleanField(db_column='T066esAgendable', blank=True, Null=True)
    en_circulacion = models.BooleanField(db_column='T066enCirculacion', blank=True, Null=True)
    fecha_circulacion = models.DateField(db_column='T066fechaCirculacion', blank=True, Null=True)
    ruta_imagen_foto = models.CharField(max_length=255, db_column='T066rutaImagenFoto', blank=True, Null=True)
    
    def __str__(self):
        return str(self.id_hoja_de_vida)

    class Meta:
        db_table = 'T066HojaDeVidaVehiculos'
        verbose_name = 'Hoja de vida vehiculos'
        verbose_name_plural = 'Hojas de vida vehiculos'

class HojaDeVidaOtrosctivos(models.Model):
    id_hoja_de_vida = models.AutoField(db_column='T067IdHojaDeVida')
    id_articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, db_column='T067Id_Articulo', unique=True)
    caracteristicas_fisicas = models.TextField(db_column='T067caracteristicasFisicas', blank=True, Null=True)
    especificaciones_tecnicas = models.TextField(db_column='T067especificacionesTecnicas', blank=True, Null=True)
    observaciones_adicionales = models.CharField(max_length=255, db_column='T067observacionesAdicionales', blank=True, Null=True)
    ruta_imagen_foto = models.CharField(max_length=255, db_column='T067rutaImagenFoto', blank=True, Null=True)
    
    def __str__(self):
        return str(self.id_hoja_de_vida)

    class Meta:
        db_table = 'T065HojaDeVidaOtrosctivos'
        verbose_name = 'Hoja de vida otros activos'
        verbose_name_plural = 'Hojas de vida otros activos'

class DocumentosVehiculo(models.Model):
    id_documentos_vehiculos = models.AutoField(db_column='T068IdDocumentosVehiculos')
    id_articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, db_column='T068Id_Articulo')
    cod_tipo_documento = models.CharField(max_length=4, db_column='T068codTipoDocumento')
    nro_documento = models.CharField(max_length=20, db_column='T068nroDocumento')
    fecha_inicio_vigencia = models.DateField(db_column='T068fechaInicioVigencia')
    fecha_expiracion = models.DateField(db_column='T068fechaExpiracion')
    id_empresa_proveedora = models.ForeignKey(Personas, on_delete=models.SET_NULL, db_column='T068Id_EmpresaProveedora')
    
    def __str__(self):
        return str(self.id_hoja_de_vida)

    class Meta:
        db_table = 'T068DocumentosVehiculo'
        verbose_name = 'Documento Vehiculo'
        verbose_name_plural = 'Documentos Vehiculo'
        unique_together = ['id_articulo', 'cod_tipo_documento', 'nro_documento']