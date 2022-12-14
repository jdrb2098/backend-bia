# Generated by Django 4.1.1 on 2022-11-25 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('almacen', '0001_initial'),
        ('seguridad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registromantenimientos',
            name='id_persona_diligencia',
            field=models.ForeignKey(db_column='T070Id_PersonaDiligencia', on_delete=django.db.models.deletion.CASCADE, related_name='id_persona_diligencia', to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='registromantenimientos',
            name='id_persona_realiza',
            field=models.ForeignKey(db_column='T070Id_PersonaRealiza', on_delete=django.db.models.deletion.CASCADE, related_name='id_persona_realiza', to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='registromantenimientos',
            name='id_programacion_mtto',
            field=models.ForeignKey(blank=True, db_column='T070Id_ProgramacionMtto', null=True, on_delete=django.db.models.deletion.SET_NULL, to='almacen.programacionmantenimientos'),
        ),
        migrations.AddField(
            model_name='programacionmantenimientos',
            name='id_articulo',
            field=models.ForeignKey(db_column='T069Id_Articulo', on_delete=django.db.models.deletion.CASCADE, to='almacen.articulos'),
        ),
        migrations.AddField(
            model_name='programacionmantenimientos',
            name='id_persona_anula',
            field=models.ForeignKey(blank=True, db_column='T069Id_PersonaAnula', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persona_anula', to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='programacionmantenimientos',
            name='id_persona_solicita',
            field=models.ForeignKey(blank=True, db_column='T069Id_PersonaSolicita', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persona_solicita', to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='nivelesorganigrama',
            name='id_organigrama',
            field=models.ForeignKey(db_column='T018Id_Organigrama', on_delete=django.db.models.deletion.CASCADE, to='almacen.organigramas'),
        ),
        migrations.AddField(
            model_name='hojadevidavehiculos',
            name='id_articulo',
            field=models.ForeignKey(blank=True, db_column='T066Id_Articulo', null=True, on_delete=django.db.models.deletion.SET_NULL, to='almacen.articulos'),
        ),
        migrations.AddField(
            model_name='hojadevidavehiculos',
            name='id_proveedor',
            field=models.ForeignKey(blank=True, db_column='T066Id_Proveedor', null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='hojadevidavehiculos',
            name='id_vehiculo_arrendado',
            field=models.ForeignKey(blank=True, db_column='T066Id_VehiculoArrendado', null=True, on_delete=django.db.models.deletion.SET_NULL, to='almacen.vehiculosarrendados'),
        ),
        migrations.AddField(
            model_name='hojadevidaotrosactivos',
            name='id_articulo',
            field=models.ForeignKey(db_column='T067Id_Articulo', on_delete=django.db.models.deletion.CASCADE, to='almacen.articulos'),
        ),
        migrations.AddField(
            model_name='hojadevidacomputadores',
            name='id_articulo',
            field=models.ForeignKey(db_column='T065Id_Articulo', on_delete=django.db.models.deletion.CASCADE, to='almacen.articulos'),
        ),
        migrations.AddField(
            model_name='documentosvehiculo',
            name='id_articulo',
            field=models.ForeignKey(db_column='T068Id_Articulo', on_delete=django.db.models.deletion.CASCADE, to='almacen.articulos'),
        ),
        migrations.AddField(
            model_name='documentosvehiculo',
            name='id_empresa_proveedora',
            field=models.ForeignKey(blank=True, db_column='T068Id_EmpresaProveedora', null=True, on_delete=django.db.models.deletion.SET_NULL, to='seguridad.personas'),
        ),
        migrations.AddField(
            model_name='bodegas',
            name='id_responsable',
            field=models.ForeignKey(db_column='T056Id_Responsable', on_delete=django.db.models.deletion.CASCADE, to='seguridad.personas'),
        ),
        migrations.AlterUniqueTogether(
            name='unidadesorganizacionales',
            unique_together={('id_organigrama', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='nivelesorganigrama',
            unique_together={('id_organigrama', 'orden_nivel')},
        ),
        migrations.AlterUniqueTogether(
            name='documentosvehiculo',
            unique_together={('id_articulo', 'cod_tipo_documento', 'nro_documento')},
        ),
    ]
