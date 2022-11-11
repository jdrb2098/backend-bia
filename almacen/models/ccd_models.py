from django.db import models
from almacen.models.organigrama_models import Organigramas, UnidadesOrganizacionales


class CuadrosClasificacionDocumental(models.Model):
    id_ccd = models.AutoField(primary_key=True, editable=False, db_column='T206IdCCD')
    id_organigrama = models.ForeignKey(Organigramas, on_delete=models.CASCADE, db_column='T206Id_Organigrama')
    version = models.CharField(max_length=30, unique=True, db_column='T206version')
    nombre = models.CharField(max_length=200, unique=True, db_column='T206nombre')
    fecha_terminado = models.DateTimeField(null=True, blank=True, db_column='T206fechaTerminado')
    fecha_puesta_produccion = models.DateTimeField(null=True, blank=True, db_column='T206fechaPuestaProduccion')
    fecha_retiro_produccion = models.DateTimeField(null=True, blank=True, db_column='T206fechaRetiroProduccion')
    justificacion = models.CharField(max_length=255,null=True, blank=True, db_column='T206justificacionNuevaVersion')
    ruta_soporte = models.CharField(max_length=200,null=True, blank=True, db_column='T206rutaSoporte')
    actual = models.BooleanField(default=False, db_column='T206actual')
    
    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table = 'T206CuadrosClasificacionDoc'
        verbose_name= 'Cuadro Clasificacion Documental'
        verbose_name_plural = 'Cuadros Clasificacion Documental'


class SubseriesDoc(models.Model):
    id_subserie_doc = models.AutoField(primary_key=True, editable=False, db_column='T204IdSubserieDoc')
    nombre = models.CharField(max_length=200, db_column='T204nombre')
    codigo = models.PositiveBigIntegerField(db_column='T204codigo')
    id_ccd = models.ForeignKey(CuadrosClasificacionDocumental, on_delete=models.CASCADE, db_column='T204Id_CCD')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T204SubseriesDoc_CDD'
        verbose_name = 'Subserie'
        verbose_name_plural = 'Subseries'
        unique_together = ['id_ccd', 'nombre']
        unique_together = ['id_ccd', 'codigo']
    

class SeriesDoc(models.Model):
    id_serie_doc = models.AutoField(primary_key=True, editable=False, db_column='T203IdSerieDoc')
    nombre = models.CharField(max_length=200,db_column='T203nombre')
    codigo = models.PositiveBigIntegerField(db_column='T203codigo')
    id_ccd = models.ForeignKey(CuadrosClasificacionDocumental, on_delete=models.CASCADE, db_column='T203Id_CCD')

    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table = 'T203SeriesDoc_CCD'
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'
    
class SeriesSubseriesUnidadOrg(models.Model):
    id_serie_subserie_doc = models.AutoField(primary_key=True, editable=False, db_column='T205SerieSubserieDoc')
    id_unidad_organizacional = models.ForeignKey(UnidadesOrganizacionales, on_delete=models.CASCADE,db_column='T205Id_UnidadOrganizacional')
    id_serie_doc = models.ForeignKey(SeriesDoc,on_delete=models.CASCADE,db_column='T205Id_SerieDoc')
    id_sub_serie_doc = models.ForeignKey(SubseriesDoc, on_delete=models.SET_NULL, null=True, blank=True, db_column='T205Id_SubserieDoc')

    def __str__(self):
            return str(self.id_serie_subserie_doc)
        
    class Meta:
        db_table = 'T205Series_Subseries_UnidadOrg'
        verbose_name = 'Serie Subserie Unidad'
        verbose_name_plural = 'Series Subseries Unidades'