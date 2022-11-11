# Generated by Django 4.1.1 on 2022-11-11 20:19

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
            model_name='bodegas',
            name='id_responsable',
            field=models.ForeignKey(db_column='T056Id_Responsable', on_delete=django.db.models.deletion.CASCADE, to='seguridad.personas'),
        ),
        migrations.AlterUniqueTogether(
            name='unidadesorganizacionales',
            unique_together={('id_organigrama', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='subseriesdoc',
            unique_together={('id_ccd', 'codigo')},
        ),
        migrations.AlterUniqueTogether(
            name='nivelesorganigrama',
            unique_together={('id_organigrama', 'orden_nivel')},
        ),
    ]
