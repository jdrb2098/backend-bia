# Generated by Django 4.1.1 on 2022-10-20 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0001_initial'),
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unidadesmedida',
            name='cod_magnitud',
        ),
        migrations.AddField(
            model_name='estadosarticulos',
            name='precargado',
            field=models.BooleanField(db_column='T051registroPrecargado', default=False),
        ),
        migrations.AddField(
            model_name='magnitudes',
            name='precargado',
            field=models.BooleanField(db_column='T054registroPrecargado', default=False),
        ),
        migrations.AddField(
            model_name='unidadesmedida',
            name='id_magnitud',
            field=models.ForeignKey(db_column='T055Id_Magnitud', default=1, on_delete=django.db.models.deletion.CASCADE, to='almacen.magnitudes'),
        ),
        migrations.AddField(
            model_name='unidadesmedida',
            name='precargado',
            field=models.BooleanField(db_column='T055registroPrecargado', default=False),
        ),
        migrations.AlterField(
            model_name='bodegas',
            name='es_principal',
            field=models.BooleanField(db_column='T056esPrincipal', default=False),
        ),
        migrations.AlterField(
            model_name='bodegas',
            name='id_responsable',
            field=models.ForeignKey(db_column='T056Id_Responsable', on_delete=django.db.models.deletion.CASCADE, to='seguridad.personas'),
        ),
        migrations.AlterField(
            model_name='bodegas',
            name='nombre',
            field=models.CharField(db_column='T056nombre', max_length=255),
        ),
        migrations.AlterField(
            model_name='estadosarticulos',
            name='cod_estado',
            field=models.CharField(db_column='T051Cod_Estado', max_length=1, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='estadosarticulos',
            name='nombre',
            field=models.CharField(db_column='T051nombre', max_length=50),
        ),
        migrations.AlterField(
            model_name='magnitudes',
            name='nombre',
            field=models.CharField(db_column='T054nombre', max_length=50),
        ),
        migrations.AlterField(
            model_name='marcas',
            name='nombre',
            field=models.CharField(db_column='T052nombre', max_length=75),
        ),
        migrations.AlterField(
            model_name='porcentajesiva',
            name='observacion',
            field=models.CharField(db_column='T053observacion', max_length=255),
        ),
        migrations.AlterField(
            model_name='unidadesmedida',
            name='abreviatura',
            field=models.CharField(db_column='T055abreviatura', max_length=1),
        ),
        migrations.AlterField(
            model_name='unidadesmedida',
            name='nombre',
            field=models.CharField(db_column='T055nombre', max_length=50),
        ),
    ]
