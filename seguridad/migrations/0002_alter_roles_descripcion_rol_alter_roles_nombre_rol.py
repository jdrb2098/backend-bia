# Generated by Django 4.1.1 on 2022-10-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seguridad", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roles",
            name="descripcion_rol",
            field=models.CharField(db_column="Tzdescripcion", max_length=255),
        ),
        migrations.AlterField(
            model_name="roles",
            name="nombre_rol",
            field=models.CharField(db_column="Tznombre", max_length=100),
        ),
    ]
