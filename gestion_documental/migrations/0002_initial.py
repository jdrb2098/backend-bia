# Generated by Django 4.1.1 on 2022-11-25 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_documental', '0001_initial'),
        ('almacen', '0002_initial'),
        ('seguridad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipologiasdocumentales',
            name='id_persona_desactiva',
            field=models.ForeignKey(blank=True, db_column='T208Id_PersonaQueDesactiva', null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='tipologiasdocumentales',
            name='id_trd',
            field=models.ForeignKey(db_column='T208Id_TRD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tablaretenciondocumental'),
        ),
        migrations.AddField(
            model_name='tablascontrolacceso',
            name='id_CCD',
            field=models.ForeignKey(db_column='T216Id_CCD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.cuadrosclasificaciondocumental'),
        ),
        migrations.AddField(
            model_name='tablaretenciondocumental',
            name='id_ccd',
            field=models.ForeignKey(db_column='T212Id_CCD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.cuadrosclasificaciondocumental'),
        ),
        migrations.AddField(
            model_name='subseriesdoc',
            name='id_ccd',
            field=models.ForeignKey(db_column='T204Id_CCD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.cuadrosclasificaciondocumental'),
        ),
        migrations.AddField(
            model_name='seriessubsunidadorgtrdtipologias',
            name='id_serie_subserie_unidadorg_trd',
            field=models.ForeignKey(db_column='T211IdSerie_SubS_UnidadOrg_TRD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.seriessubsunidadorgtrd'),
        ),
        migrations.AddField(
            model_name='seriessubsunidadorgtrdtipologias',
            name='id_tipologia_doc',
            field=models.ForeignKey(db_column='T211IdTipologiaDoc_TRD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tipologiasdocumentales'),
        ),
        migrations.AddField(
            model_name='seriessubsunidadorgtrd',
            name='id_serie_subserie_doc',
            field=models.ForeignKey(db_column='T218Id_SerieSubserieDoc', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.seriessubseriesunidadorg'),
        ),
        migrations.AddField(
            model_name='seriessubsunidadorgtrd',
            name='id_trd',
            field=models.ForeignKey(db_column='T2018Id_TRD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tablaretenciondocumental'),
        ),
        migrations.AddField(
            model_name='seriessubseriesunidadorg',
            name='id_serie_doc',
            field=models.ForeignKey(db_column='T205Id_SerieDocCCD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.seriesdoc'),
        ),
        migrations.AddField(
            model_name='seriessubseriesunidadorg',
            name='id_sub_serie_doc',
            field=models.ForeignKey(blank=True, db_column='T205Id_SubserieDocCCD', null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_documental.subseriesdoc'),
        ),
        migrations.AddField(
            model_name='seriessubseriesunidadorg',
            name='id_unidad_organizacional',
            field=models.ForeignKey(db_column='T205Id_UnidadOrganizacional', on_delete=django.db.models.deletion.CASCADE, to='almacen.unidadesorganizacionales'),
        ),
        migrations.AddField(
            model_name='seriesdoc',
            name='id_ccd',
            field=models.ForeignKey(db_column='T203Id_CCD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.cuadrosclasificaciondocumental'),
        ),
        migrations.AddField(
            model_name='historicosseriesubseriesunidadorgtrd',
            name='id_persona_cambia',
            field=models.ForeignKey(blank=True, db_column='T219Id_PersonaCambia', null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='historicosseriesubseriesunidadorgtrd',
            name='id_serie_subs_unidadorg_trd',
            field=models.ForeignKey(db_column='T219IdSerie_SubS_UnidadOrg_TRD', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.seriessubsunidadorgtrd'),
        ),
        migrations.AddField(
            model_name='formatostiposmediotipodoc',
            name='id_formato_tipo_medio',
            field=models.ForeignKey(db_column='T217Id_Formato_TipoMedio', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.formatostiposmedio'),
        ),
        migrations.AddField(
            model_name='formatostiposmediotipodoc',
            name='id_tipologia_doc',
            field=models.ForeignKey(db_column='T217Id_TipologiaDoc', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tipologiasdocumentales'),
        ),
        migrations.AlterUniqueTogether(
            name='formatostiposmedio',
            unique_together={('cod_tipo_medio_doc', 'nombre')},
        ),
        migrations.AddField(
            model_name='cuadrosclasificaciondocumental',
            name='id_organigrama',
            field=models.ForeignKey(db_column='T206Id_Organigrama', on_delete=django.db.models.deletion.CASCADE, to='almacen.organigramas'),
        ),
        migrations.AddField(
            model_name='ccd_clasif_serie_subserie_tca',
            name='id_TCA',
            field=models.ForeignKey(db_column='T215Id_TCA', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.tablascontrolacceso'),
        ),
        migrations.AddField(
            model_name='ccd_clasif_serie_subserie_tca',
            name='id_permiso_GD',
            field=models.ForeignKey(db_column='T215Id_PermisoGd', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.permisosgd'),
        ),
        migrations.AddField(
            model_name='ccd_clasif_serie_subserie_tca',
            name='id_serie_subserie_doc',
            field=models.ForeignKey(db_column='T215Id_SerieSubserieDoc', on_delete=django.db.models.deletion.CASCADE, to='gestion_documental.seriessubseriesunidadorg'),
        ),
        migrations.AlterUniqueTogether(
            name='tipologiasdocumentales',
            unique_together={('id_trd', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='subseriesdoc',
            unique_together={('id_ccd', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='seriessubsunidadorgtrdtipologias',
            unique_together={('id_serie_subserie_unidadorg_trd', 'id_tipologia_doc')},
        ),
        migrations.AlterUniqueTogether(
            name='seriessubsunidadorgtrd',
            unique_together={('id_trd', 'id_serie_subserie_doc')},
        ),
        migrations.AlterUniqueTogether(
            name='ccd_clasif_serie_subserie_tca',
            unique_together={('id_TCA', 'id_serie_subserie_doc', 'id_permiso_GD')},
        ),
    ]
