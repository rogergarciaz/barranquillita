# Generated by Django 3.0.8 on 2020-09-03 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sueldos', '0003_sueldo_modificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='descripcion',
            name='cantidad',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='descripcion',
            name='precio_compra',
            field=models.PositiveIntegerField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='descripcion',
            name='precio_pagado',
            field=models.PositiveIntegerField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='descripcion',
            name='precio_vendido',
            field=models.PositiveIntegerField(blank=True, default=None),
        ),
    ]