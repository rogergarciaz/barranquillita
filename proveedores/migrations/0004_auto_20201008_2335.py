# Generated by Django 3.0.8 on 2020-10-08 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0003_auto_20201008_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='adquisicion',
            name='modificado_por',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='modificado_por',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
