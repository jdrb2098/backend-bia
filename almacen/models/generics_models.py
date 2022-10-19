from django.db import models
from seguridad.models import Municipio

class EstadosArticulos(models.Model):
    cod_estado = models.AutoField(primary_key=True, editable=False, db_column='T051CodEstado')
    nombre = models.CharField(max_length=30, db_column='T051nombre')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T051EstadosArticulo'
        verbose_name = 'Estado artículo'
        verbose_name_plural = 'Estados artículos'
        
class Marcas(models.Model):
    id_marca = models.AutoField(primary_key=True, editable=False, db_column='T052IdMarca')
    nombre = models.CharField(max_length=30, db_column='T052nombre')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T052Marcas'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        
class PorcentajesIVA(models.Model):
    id_porcentaje_iva = models.AutoField(primary_key=True, editable=False, db_column='T053IdPorcentajeIVA')
    porcentaje = models.FloatField(db_column='T053porcentaje')
    observacion = models.CharField(max_length=100, db_column='T053observacion')

    def __str__(self):
        return str(self.porcentaje)

    class Meta:
        db_table = 'T053PorcentajesIVA'
        verbose_name = 'Porcentaje IVA'
        verbose_name_plural = 'Porcentajes IVA'
        
class Magnitudes(models.Model):
    cod_magnitud = models.AutoField(primary_key=True, editable=False, db_column='T054CodMagnitud')
    nombre = models.CharField(max_length=30, db_column='T054nombre')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T054Magnitudes'
        verbose_name = 'Magnitud'
        verbose_name_plural = 'Magnitudes'
        
class UnidadesMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True, editable=False, db_column='T055IdUnidadMedida')
    nombre = models.CharField(max_length=30, db_column='T055nombre')
    abreviatura = models.CharField(max_length=5, db_column='T055abreviatura')
    cod_magnitud = models.ForeignKey(Magnitudes, on_delete=models.CASCADE, db_column='T055Cod_Magnitud')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T055UnidadesMedida'
        verbose_name = 'Unidad medida'
        verbose_name_plural = 'Unidades medida'
        
class Bodegas(models.Model):
    id_bodega = models.AutoField(primary_key=True, editable=False, db_column='T056IdBodega')
    nombre = models.CharField(max_length=30, db_column='T056nombre')
    cod_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, db_column='T056Cod_Municipio')
    direccion = models.CharField(max_length=255, null=True, blank=True, db_column='T056direccion')
    id_responsable = models.IntegerField(db_column='T056Id_Responsable')
    es_principal = models.CharField(max_length=30, db_column='T056esPrincipal')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T056Bodegas'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'