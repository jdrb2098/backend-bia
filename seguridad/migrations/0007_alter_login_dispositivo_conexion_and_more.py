# Generated by Django 4.1.1 on 2022-10-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seguridad", "0006_alter_login_dirip_alter_loginerroneo_dirip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="login",
            name="dispositivo_conexion",
            field=models.CharField(db_column="TzdispositivoConexion", max_length=100),
        ),
        migrations.AlterField(
            model_name="loginerroneo",
            name="dispositivo_conexion",
            field=models.CharField(db_column="TzdispositivoConexion", max_length=100),
        ),
    ]
