# Generated by Django 3.0.8 on 2020-10-08 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sueldos', '0007_descripcion_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='descripcion',
            name='modificado_por',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='sueldo',
            name='modificado_por',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
