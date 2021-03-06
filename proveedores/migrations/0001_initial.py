# Generated by Django 3.0.8 on 2020-10-09 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sueldos', '0001_initial'),
        ('usuarios', '0004_perfil_modificado_por'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('identificador', models.CharField(default=None, max_length=100)),
                ('celular', models.CharField(blank=True, max_length=20)),
                ('direccion', models.CharField(blank=True, max_length=100)),
                ('ciudad', models.CharField(blank=True, max_length=100)),
                ('nota', models.CharField(blank=True, max_length=100)),
                ('saldo', models.FloatField(default=None)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('modificado_por', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Adquisicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('precio_compra', models.PositiveIntegerField()),
                ('nota', models.CharField(blank=True, max_length=100)),
                ('compra', models.PositiveIntegerField()),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('credito', models.BooleanField(default=False)),
                ('modificado_por', models.CharField(default=None, max_length=100)),
                ('descripcion', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sueldos.DescripcionInterna')),
                ('nombre', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='proveedores.Proveedor')),
                ('perfil', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='usuarios.Perfil')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
