# Generated by Django 4.1.1 on 2022-11-08 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0002_alter_nivelesorganigrama_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unidadesorganizacionales',
            old_name='unidades_organizacional',
            new_name='id_unidad_organizacional',
        ),
        migrations.AlterField(
            model_name='unidadesorganizacionales',
            name='cod_agrupacion_documental',
            field=models.CharField(blank=True, db_column='T019codAgrupacionDocumental', max_length=3, null=True),
        ),
    ]
