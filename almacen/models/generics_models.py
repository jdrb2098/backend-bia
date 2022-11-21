from django.db import models
from seguridad.choices.municipios_choices import municipios_CHOICES
from almacen.choices.magnitudes_choices import magnitudes_CHOICES
from seguridad.models import Personas
       
class Marcas(models.Model):
    id_marca = models.AutoField(primary_key=True, editable=False, db_column='T052IdMarca')
    nombre = models.CharField(max_length=50, db_column='T052nombre',unique=True)
    activo = models.BooleanField(default=True, db_column='T052activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T052itemYaUsado')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T052Marcas'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        
class PorcentajesIVA(models.Model):
    id_porcentaje_iva = models.AutoField(primary_key=True, editable=False, db_column='T053IdPorcentajeIVA')
    porcentaje = models.FloatField(db_column='T053porcentaje',unique=True)
    observacion = models.CharField(max_length=255, db_column='T053observacion')
    registro_precargado=models.BooleanField(default=False, db_column='T053registroPrecargado')
    activo = models.BooleanField(default=True, db_column='T053activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T053itemYaUsado')

    def __str__(self):
        return str(self.porcentaje)

    class Meta:
        db_table = 'T053PorcentajesIVA'
        verbose_name = 'Porcentaje IVA'
        verbose_name_plural = 'Porcentajes IVA'
        
class Magnitudes(models.Model):
    cod_magnitud = models.AutoField(primary_key=True, editable=False, db_column='T054IdMagnitud')
    nombre = models.CharField(max_length=50, db_column='T054nombre',unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T054Magnitudes'
        verbose_name = 'Magnitud'
        verbose_name_plural = 'Magnitudes'
        
class UnidadesMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True, editable=False, db_column='T055IdUnidadMedida')
    nombre = models.CharField(max_length=50, db_column='T055nombre',unique=True)
    abreviatura = models.CharField(max_length=5, db_column='T055abreviatura',unique=True)
    id_magnitud = models.PositiveSmallIntegerField(choices=magnitudes_CHOICES, db_column='T055Id_Magnitud')
    precargado = models.BooleanField(default=False, db_column='T055registroPrecargado')
    activo = models.BooleanField(default=True, db_column='T055activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T055itemYaUsado')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T055UnidadesMedida'
        verbose_name = 'Unidad medida'
        verbose_name_plural = 'Unidades medida'
        
class Bodegas(models.Model):
    id_bodega = models.AutoField(primary_key=True, editable=False, db_column='T056IdBodega')
    nombre = models.CharField(max_length=255, db_column='T056nombre',unique=True)
    cod_municipio = models.CharField(max_length=5, choices=municipios_CHOICES, null=True, blank=True, db_column='T056Cod_Municipio')
    direccion = models.CharField(max_length=255, null=True, blank=True, db_column='T056direccion')
    id_responsable = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T056Id_Responsable')
    es_principal = models.BooleanField(default=False, db_column='T056esPrincipal')
    activo = models.BooleanField(default=True, db_column='T056activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T056itemYaUsado')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T056Bodegas'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'