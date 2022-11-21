from django.db import models
from seguridad.choices.municipios_choices import municipios_CHOICES
from almacen.choices.magnitudes_choices import magnitudes_CHOICES
from seguridad.models import Personas

class Articulos(models.Model):
    pass

class MetodosValoracionArticulos(models.Model):
    cod_metodo_valoracion = models.Autofield(db_column='T058CodMetodoValoracion')
    nombre = models.CharField(max_length=50, db_column='T058nombre', unique=True)
    descripcion = models.CharField(max_length=255, db_column='T058descripccion', blank=True, Null=True)
    
    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T058MetodosValoracionArticulos'
        verbose_name = 'Metodo valoracion articulo'
        verbose_name_plural = 'Metodos valoracion articulo'

class TiposDepreciacionActivos(models.Model):
    cod_tipo_depreciacion = models.Autofield(db_column='T059CodTipoDepreciacion')
    nombre = models.CharField(max_length=50, db_column='T059nombre', unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T059TiposDepreciacionActivos'
        verbose_name = 'Tipo Depreciacion Activos'
        verbose_name_plural = 'Tipos Depreciacion Activos'

class TiposActivo(models.Model):
    cod_tipo_activo = models.CharField(max_length=1, db_column='T060CodTipoActivo')
    nombre = models.CharField(max_length=15, db_column='T060nombre', unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T060TiposActivo'
        verbose_name = 'Tipo Activos'
        verbose_name_plural = 'Tipos Activos'
