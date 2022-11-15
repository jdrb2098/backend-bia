from django.db import models
from almacen.models.ccd_models import SeriesSubseriesUnidadOrg, CuadrosClasificacionDocumental
from gestion_documental.choices.trd_choices import disposicion_final_series_CHOICES
from gestion_documental.choices.tipo_clasificacion_choices import tipo_clasificacion_CHOICES
from gestion_documental.choices.tipos_soportes_doc_choices import tipos_soportes_doc_CHOICES


class TablaRetencionDocumental(models.Model):
    id_trd = models.AutoField(primary_key=True, editable=False, db_column='T212IdTRD')
    id_ccd = models.ForeignKey(CuadrosClasificacionDocumental, on_delete=models.CASCADE, db_column='T212Id_CCD')
    version = models.CharField(max_length=10, unique=True, db_column='T212version')
    nombre = models.CharField(max_length=50, unique=True, db_column='T212nombre')
    fecha_terminado = models.DateTimeField(null=True, blank=True, db_column='T212fechaTerminado')
    fecha_puesta_produccion = models.DateTimeField(null=True, blank=True, db_column='T212fechaPuestaEnProduccion')
    fecha_retiro_produccion = models.DateTimeField(null=True, blank=True, db_column='T212fechaRetiroDeProduccion')
    justificacion = models.CharField(max_length=255,null=True, blank=True, db_column='T212justificacionNuevaVersion')
    ruta_soporte = models.FileField(null=True, blank=True, db_column='T212rutaSoporte')
    actual = models.BooleanField(default=False, db_column='T212actual')
    
    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table = 'T212TablasRetencionDoc'
        verbose_name= 'Tabla de Retención Documental'
        verbose_name_plural = 'Tablas de Retención Documental'


class TiposSoportesDocumentos(models.Model):
    id_tipo_soporte_doc = models.AutoField(primary_key=True, editable=False, db_column='T209Cod_TipoSoporteDoc')
    nombre = models.CharField(max_length=10, choices=tipos_soportes_doc_CHOICES, db_column='T209nombre')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T209TiposSoporteDocumentos'
        verbose_name = 'Tipo Soporte Documento'
        verbose_name_plural = 'Tipos Soportes Documentos'


class FormatosTipoSoporte(models.Model):
    id_formato_tipo_soporte = models.AutoField(primary_key=True, editable=False, db_column='T210IdFormatoTipoSoporte')
    nombre = models.CharField(max_length=10, unique=True, db_column='T210nombre')
    id_tipo_soporte_doc=models.ForeignKey(TiposSoportesDocumentos, on_delete=models.CASCADE, db_column='T210Cod_TipoSoporteDoc')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T210FormatosTipoSoporte'
        verbose_name = 'Formato Tipo Soporte'
        verbose_name_plural = 'Formatos Tipos Soportes'

class DisposicionFinalSeries(models.Model):
    cod_disposicion_final = models.AutoField(editable=False, primary_key=True, db_column='T207CodDisposicionFinal')
    nombre = models.CharField(max_length=30, db_column='T207nombre')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T207DisposicionFinalSeries'
        verbose_name = 'Disposición Final Serie'
        verbose_name_plural = 'Disposición Final Series'


class TipologiasDocumentales(models.Model):
    id_tipologia_documental = models.AutoField(editable=False, primary_key=True, db_column='T208TipologiasDocumentales')
    nombre = models.CharField(max_length=10, db_column='T208nombre')
    codigo = models.PositiveSmallIntegerField(db_column='T208codigo')
    cod_tipo_soporte_doc = models.ForeignKey(TiposSoportesDocumentos, on_delete=models.CASCADE, db_column='T208Cod_TipoSoporteDoc')
    id_trd = models.ForeignKey(TablaRetencionDocumental, on_delete=models.CASCADE, db_column='T208Id_TRD')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T208TipologiasDocumentales'
        verbose_name = 'Tipologia Documental'
        verbose_name_plural = 'Tipologias Documentales'
        unique_together = ['id_trd', 'nombre']
        unique_together = ['id_trd', 'codigo']


class SeriesSubSeriesUnidadesTipologias(models.Model):
    id_serie_subserie_tipologia = models.AutoField(primary_key=True, editable=False, db_column='T211IdSerieSubserieTipologia')
    id_serie_subserie_doc = models.ForeignKey(SeriesSubseriesUnidadOrg, on_delete=models.CASCADE, db_column='T211Id_SerieSubserieDoc')
    cod_disposicion_final = models.CharField(max_length=20, choices=disposicion_final_series_CHOICES, db_column='T211Cod_DisposicionFinal')
    digitalizacion_dis_final = models.BooleanField(default=True, db_column='T211digitalizacionDispFinal')
    tiempo_retencion_ag = models.PositiveSmallIntegerField(db_column='T211tiempoRetencionAG')
    tiempo_retencion_ac = models.PositiveSmallIntegerField(db_column='T211tiempoRetencionAC')
    descripcion_procedimiento = models.TextField(max_length=500, db_column='T211descripcionProcedimiento')
    id_tipologia_documental = models.ForeignKey(TipologiasDocumentales, on_delete=models.CASCADE,db_column='T211Id_TipologiaDoc')

    def __str__(self):
        return str(self.id_serie_subserie_tipologia)

    class Meta:
        db_table = 'T211Series_Sub_UndOrg_Tipologias'
        verbose_name = 'Serie Subserie Unidad Tipologia'
        verbose_name = 'Series Subseries Unidades Tipologias'
        unique_together = ['id_serie_subserie_doc', 'id_tipologia_documental']
        

class TablasControAcceso(models.Model):
    id_TCA=models.AutoField(primary_key=True, editable=False, db_column='T216IdTCA')
    id_CCD=models.ForeignKey(CuadrosClasificacionDocumental,on_delete=models.CASCADE,db_column='T216Id_CCD')
    version=models.CharField(max_length=30,unique=True,db_column='T216version')
    nombre=models.CharField(max_length=200,unique=True,db_column='T216nombre')
    fecha_terminado=models.DateTimeField(blank=True,null=True,db_column='T216fechaTerminado')
    fecha_puesta_produccion=models.DateTimeField(blank=True,null=True,db_column='T216fechaPuestaEnProduccion')
    fecha_retiro_produccion=models.DateTimeField(blank=True,null=True,db_column='T216fechaRetiroDeProduccion')
    justificacion_nueva_version=models.CharField(max_length=500,blank=True,null=True,db_column='T216justificacionNuevaVersion')
    ruta_soporte=models.CharField(max_length=200,blank=True,null=True,db_column='T216rutaSoporte')
    actual=models.BooleanField(default=False,db_column='T216actual')
    
    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table='T216TablasControlAcceso'
        verbose_name='Tabla de control de acceso'
        verbose_name_plural='Tablas de control de acceso'
        
class ClasificacionSeriesSubDoc(models.Model):
    cod_clas_serie_doc=models.IntegerField(db_column='T214CodClasSerieDoc')
    tipo_clasificacion=models.CharField(max_length=20,choices=tipo_clasificacion_CHOICES,db_column='T214tipoClasificacion')
    
    def __str__(self):
        return str(self.cod_clas_serie_doc)
    
    class Meta:
        db_table='T214ClasificacionSeriesSubDoc'
        verbose_name='Clasificacion serie sub Doc '
        verbose_name_plural='Clasificaciones serie sub Doc'

class PermisosGD(models.Model):
    permisos_GD=models.AutoField(primary_key=True, editable=False,db_column='T213IdPermisosGD')
    tipo_permiso=models.CharField(db_column='T213tipoPermiso')
    
    def __str__(self):
        return str(self.permisos_GD)
    
    class Meta:
        db_table='T213PermisosGD'
        verbose_name='Permiso GD'
        verbose_name_plural='Permisos GD'
        
class CCD_Clasif_Cargos_UndCargo_Permisos(models.Model):
    id_serie_sub_serie_cargo_permiso_GD=models.AutoField(primary_key=True, editable=False, db_column='T215IdSerieSubserieCargoPermisoGD')
    id_serie_sub_serie_Doc=models.ForeignKey(SeriesSubseriesUnidadOrg,on_delete=models.CASCADE,db_column='T215Id_SerieSubserieDoc')
    cod_class_serie_Doc=models.ForeignKey(ClasificacionSeriesSubDoc,on_delete=models.CASCADE,db_column='T215Cod_ClasSerieDoc')
    id_cargo_persona=models.CharField(db_column='T215Id_CargoPersona')
    id_unidad_org_cargo=models.CharField('db_columnT215Id_UnidadOrgCargo') 
    id_permiso_GD=models.ForeignKey(PermisosGD,on_delete=models.CASCADE,db_column='T215Id_PermisoGD')
    id_TCA=models.ForeignKey(TablasControAcceso,on_delete=models.CASCADE,db_column='T215Id_TCA')       
    
    def __str__(self):
        return str(self.id_serie_sub_serie_cargo_permiso_GD)
    
    class Meta:
        db_table='T215CCD_Clasif_Cargos_UndCargo_Permisos'
        verbose_name='clasificación cargo unidad cargo y permisos'
        verbose_name_plural='clasificaciones cargos unidad cargo y permisos'                       
                                    