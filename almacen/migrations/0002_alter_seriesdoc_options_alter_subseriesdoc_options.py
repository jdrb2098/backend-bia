# Generated by Django 4.1.1 on 2022-11-17 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seriesdoc',
            options={'ordering': ['nombre'], 'verbose_name': 'Serie', 'verbose_name_plural': 'Series'},
        ),
        migrations.AlterModelOptions(
            name='subseriesdoc',
            options={'ordering': ['nombre'], 'verbose_name': 'Subserie', 'verbose_name_plural': 'Subseries'},
        ),
    ]
