# Generated by Django 3.0.8 on 2020-07-29 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0002_prestamo_perfil'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prestamo',
            old_name='cuotas_pagadas',
            new_name='cuotas_debidas',
        ),
    ]
