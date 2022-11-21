from django.db import models
from seguridad.choices.municipios_choices import municipios_CHOICES
from almacen.choices.magnitudes_choices import magnitudes_CHOICES
from seguridad.models import Personas
from almacen.models.articulos_models import Articulos, EstadosArticulo

class ProgramacionMantenimientos(models.Model):
    id_programacion_mtto = models.AutoField(db_column='T069IdProgramacionMtto')
    id_articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, db_column='T069Id_Articulo')
    cod_tipo_mantenimiento = models.CharField(max_length=1, db_column='T069codTipoMantenimiento')
    fecha_generada = models.DateField(db_column='T069fechaGenerada')
    fecha_programada = models.DateField(db_column='T069fechaProgramada')
    motivo_mantenimiento = models.CharField(max_length=255, db_column='T069motivoMantenimiento')
    observaciones = models.CharField(max_length=255, db_column='T069observaciones', blank=True, Null=True)
    id_persona_solicita = models.ForeignKey(Personas, on_delete=models.SET_NULL, db_column='T069Id_PersonaSolicita', blank=True, Null=True)
    fecha_solicitud = models.DateField(db_column='T069fechaSolicitud', blank=True, Null=True)
    fecha_anulacion = models.DateTimeField(db_column='T069fechaAnulacion', blank=True, Null=True)
    justificacion_anulacion = models.CharField(max_length=255, db_column='T069justificacionAnulacion', blank=True, Null=True)
    id_persona_anula = models.ForeignKey(Personas, on_delete=models.SET_NULL, db_column='T069Id_PersonaAnula', blank=True, Null=True)
    ejecutado = models.BooleanField(db_column='T069ejecutado', default=False)
    
    def __str__(self):
        return str(self.id_hoja_de_vida)

    class Meta:
        db_table = 'T069ProgramacionMantenimientos'
        verbose_name = 'Programacion Mantenimientos'
        verbose_name_plural = 'Programaciones Mantenimientos'

class RegistroMantenimientos(models.Model):
    id_registro_mtto = models.AutoField(db_column='T070IdRegistroMtto')
    id_articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, db_column='T070d_Articulo')
    fecha_registrado = models.DateTimeField(db_column='T070fechaRegistrado')
    fecha_ejecutado = models.DateTimeField(db_column='T070fechaEjecutado')
    cod_tipo_mantenimiento = models.CharField(max_length=1, db_column='T070codTipoMantenimiento')
    acciones_realizadas = models.TextField(db_column='T070accionesRealizadas', blank=True, Null=True)
    dias_empleados = models.SmallIntegerField(db_column='T070diasEmpleados')
    observaciones = models.CharField(max_length=255, db_column='T070observaciones', blank=True, Null=True)
    cod_estado_anterior = models.ForeignKey(EstadosArticulo, db_column='T070codEstadoAnterior', on_delete=models.SET_NULL, blank=True, Null=True)
    fecha_estado_anterior = models.DateTimeField(db_column='T070fechaEstadoAnterior', blank=True, Null=True)
    cod_estado_final = models.ForeignKey(Articulos, db_column='T070Cod_EstadoFinal', on_delete=models.CASCADE)
    id_programacion_mtto = models.ForeignKey(ProgramacionMantenimientos, on_delete=models.SET_NULL, db_column='T070Id_ProgramacionMtto', blank=True, Null=True)
    valor_mantenimiento = models.IntegerField(db_column='T070valorMantenimiento', blank=True, Null=True)
    contrato_mantenimiento = models.CharField(max_length=20, db_column='T070contratoMantenimiento', blank=True, Null=True)
    id_persona_realiza = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T070Id_PersonaRealiza')
    id_persona_diligencia = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T070Id_PersonaDiligencia')
    ruta_documentos_soporte = models.CharField(max_length=255, db_column='T070rutaDocumentosSoporte', blank=True, Null=True)
    
    def __str__(self):
        return str(self.id_hoja_de_vida)

    class Meta:
        db_table = 'T070RegistroMantenimientos'
        verbose_name = 'Registro Mantenimientos'
        verbose_name_plural = 'Registros Mantenimientos'