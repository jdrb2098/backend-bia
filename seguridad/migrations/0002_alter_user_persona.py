# Generated by Django 4.1.1 on 2022-10-08 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='persona',
            field=models.OneToOneField(db_column='TzId_Persona', default=1, on_delete=django.db.models.deletion.CASCADE, to='seguridad.personas'),
            preserve_default=False,
        ),
    ]
