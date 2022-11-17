# Generated by Django 4.1.1 on 2022-11-17 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClasificacionSeriesSubDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_clas_serie_doc', models.IntegerField(db_column='T214CodClasSerieDoc')),
                ('tipo_clasificacion', models.CharField(choices=[('P', 'Público'), ('C', 'Controlado'), ('R', 'Rerservado')], db_column='T214tipoClasificacion', max_length=20)),
            ],
            options={
                'verbose_name': 'Clasificacion serie sub Doc ',
                'verbose_name_plural': 'Clasificaciones serie sub Doc',
                'db_table': 'T214ClasificacionSeriesSubDoc',
            },
        ),
        migrations.CreateModel(
            name='DisposicionFinalSeries',
            fields=[
                ('cod_disposicion_final', models.AutoField(db_column='T207CodDisposicionFinal', editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(db_column='T207nombre', max_length=30)),
            ],
            options={
                'verbose_name': 'Disposición Final Serie',
                'verbose_name_plural': 'Disposición Final Series',
                'db_table': 'T207DisposicionFinalSeries',
            },
        ),
        migrations.CreateModel(
            name='PermisosGD',
            fields=[
                ('permisos_GD', models.AutoField(db_column='T213IdPermisosGD', editable=False, primary_key=True, serialize=False)),
                ('tipo_permiso', models.CharField(db_column='T213tipoPermiso', max_length=20)),
            ],
            options={
                'verbose_name': 'Permiso GD',
                'verbose_name_plural': 'Permisos GD',
                'db_table': 'T213PermisosGD',
            },
        ),
        migrations.CreateModel(
            name='TablaRetencionDocumental',
            fields=[
                ('id_trd', models.AutoField(db_column='T212IdTRD', editable=False, primary_key=True, serialize=False)),
                ('version', models.CharField(db_column='T212version', max_length=10, unique=True)),
                ('nombre', models.CharField(db_column='T212nombre', max_length=50, unique=True)),
                ('fecha_terminado', models.DateTimeField(blank=True, db_column='T212fechaTerminado', null=True)),
                ('fecha_puesta_produccion', models.DateTimeField(blank=True, db_column='T212fechaPuestaEnProduccion', null=True)),
                ('fecha_retiro_produccion', models.DateTimeField(blank=True, db_column='T212fechaRetiroDeProduccion', null=True)),
                ('justificacion', models.CharField(blank=True, db_column='T212justificacionNuevaVersion', max_length=255, null=True)),
                ('ruta_soporte', models.FileField(blank=True, db_column='T212rutaSoporte', null=True, upload_to='')),
                ('actual', models.BooleanField(db_column='T212actual', default=False)),
                ('id_ccd', models.ForeignKey(db_column='T212Id_CCD', on_delete=django.db.models.deletion.CASCADE, to='almacen.cuadrosclasificaciondocumental')),
            ],
            options={
                'verbose_name': 'Tabla de Retención Documental',
                'verbose_name_plural': 'Tablas de Retención Documental',
                'db_table': 'T212TablasRetencionDoc',
            },
        ),
        migrations.CreateModel(
            name='TiposSoportesDocumentos',
            fields=[
                ('id_tipo_soporte_doc', models.CharField(db_column='T209Cod_TipoSoporteDoc', editable=False, max_length=1, primary_key=True, serialize=False)),
                ('nombre', models.CharField(db_column='T209nombre', max_length=11)),
            ],
            options={
                'verbose_name': 'Tipo Soporte Documento',
                'verbose_name_plural': 'Tipos Soportes Documentos',
                'db_table': 'T209TiposSoporteDocumentos',
            },
        ),
        migrations.CreateModel(
            name='TipologiasDocumentales',
            fields=[
                ('id_tipologia_documental', models.AutoField(db_column='T208TipologiasDocumentales', editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(db_column='T208nombre', max_length=10)),
                ('codigo', models.PositiveSmallIntegerField(db_column='T208codigo')),
                ('cod_tipo_soporte_doc', models.CharField(choices=[('E', 'Electrónico'), ('F', 'Físico'), ('H', 'Híbrido')], db_column='T208Cod_TipoSoporteDoc', max_length=1)),
                ('id_trd', models.ForeignKey(db_column='T208Id_TRD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tablaretenciondocumental')),
            ],
            options={
                'verbose_name': 'Tipologia Documental',
                'verbose_name_plural': 'Tipologias Documentales',
                'db_table': 'T208TipologiasDocumentales',
                'ordering': ['nombre'],
                'unique_together': {('id_trd', 'codigo')},
            },
        ),
        migrations.CreateModel(
            name='TablasControAcceso',
            fields=[
                ('id_TCA', models.AutoField(db_column='T216IdTCA', editable=False, primary_key=True, serialize=False)),
                ('version', models.CharField(db_column='T216version', max_length=30, unique=True)),
                ('nombre', models.CharField(db_column='T216nombre', max_length=200, unique=True)),
                ('fecha_terminado', models.DateTimeField(blank=True, db_column='T216fechaTerminado', null=True)),
                ('fecha_puesta_produccion', models.DateTimeField(blank=True, db_column='T216fechaPuestaEnProduccion', null=True)),
                ('fecha_retiro_produccion', models.DateTimeField(blank=True, db_column='T216fechaRetiroDeProduccion', null=True)),
                ('justificacion_nueva_version', models.CharField(blank=True, db_column='T216justificacionNuevaVersion', max_length=500, null=True)),
                ('ruta_soporte', models.CharField(blank=True, db_column='T216rutaSoporte', max_length=200, null=True)),
                ('actual', models.BooleanField(db_column='T216actual', default=False)),
                ('id_CCD', models.ForeignKey(db_column='T216Id_CCD', on_delete=django.db.models.deletion.CASCADE, to='almacen.cuadrosclasificaciondocumental')),
            ],
            options={
                'verbose_name': 'Tabla de control de acceso',
                'verbose_name_plural': 'Tablas de control de acceso',
                'db_table': 'T216TablasControlAcceso',
            },
        ),
        migrations.CreateModel(
            name='FormatosTipoSoporte',
            fields=[
                ('id_formato_tipo_soporte', models.AutoField(db_column='T210IdFormatoTipoSoporte', editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(db_column='T210nombre', max_length=30, unique=True)),
                ('id_tipo_soporte_doc', models.ForeignKey(db_column='T210Cod_TipoSoporteDoc', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tipossoportesdocumentos')),
            ],
            options={
                'verbose_name': 'Formato Tipo Soporte',
                'verbose_name_plural': 'Formatos Tipos Soportes',
                'db_table': 'T210FormatosTipoSoporte',
            },
        ),
        migrations.CreateModel(
            name='CCD_Clasif_Cargos_UndCargo_Permisos',
            fields=[
                ('id_serie_sub_serie_cargo_permiso_GD', models.AutoField(db_column='T215IdSerieSubserieCargoPermisoGD', editable=False, primary_key=True, serialize=False)),
                ('id_cargo_persona', models.CharField(db_column='T215Id_CargoPersona', max_length=10)),
                ('id_unidad_org_cargo', models.CharField(db_column='T215Id_UnidadOrgCargo', max_length=10)),
                ('cod_class_serie_Doc', models.ForeignKey(db_column='T215Cod_ClasSerieDoc', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.clasificacionseriessubdoc')),
                ('id_TCA', models.ForeignKey(db_column='T215Id_TCA', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tablascontroacceso')),
                ('id_permiso_GD', models.ForeignKey(db_column='T215Id_PermisoGD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.permisosgd')),
                ('id_serie_sub_serie_Doc', models.ForeignKey(db_column='T215Id_SerieSubserieDoc', on_delete=django.db.models.deletion.CASCADE, to='almacen.seriessubseriesunidadorg')),
            ],
            options={
                'verbose_name': 'clasificación cargo unidad cargo y permisos',
                'verbose_name_plural': 'clasificaciones cargos unidad cargo y permisos',
                'db_table': 'T215CCD_Clasif_Cargos_UndCargo_Permisos',
            },
        ),
        migrations.CreateModel(
            name='SeriesSubSeriesUnidadesTipologias',
            fields=[
                ('id_serie_subserie_tipologia', models.AutoField(db_column='T211IdSerieSubserieTipologia', editable=False, primary_key=True, serialize=False)),
                ('cod_disposicion_final', models.CharField(choices=[('CT', 'Conservación Total'), ('E', 'Eliminación'), ('S', 'Selección')], db_column='T211Cod_DisposicionFinal', max_length=20)),
                ('digitalizacion_dis_final', models.BooleanField(db_column='T211digitalizacionDispFinal', default=True)),
                ('tiempo_retencion_ag', models.PositiveSmallIntegerField(db_column='T211tiempoRetencionAG')),
                ('tiempo_retencion_ac', models.PositiveSmallIntegerField(db_column='T211tiempoRetencionAC')),
                ('descripcion_procedimiento', models.TextField(db_column='T211descripcionProcedimiento', max_length=500)),
                ('id_serie_subserie_doc', models.ForeignKey(db_column='T211Id_SerieSubserieDoc', on_delete=django.db.models.deletion.CASCADE, to='almacen.seriessubseriesunidadorg')),
                ('id_tipologia_documental', models.ForeignKey(db_column='T211Id_TipologiaDoc', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tipologiasdocumentales')),
            ],
            options={
                'verbose_name': 'Series Subseries Unidades Tipologias',
                'db_table': 'T211Series_Sub_UndOrg_Tipologias',
                'unique_together': {('id_serie_subserie_doc', 'id_tipologia_documental')},
            },
        ),
    ]
