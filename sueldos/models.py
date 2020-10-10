from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Sueldo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey(
        'usuarios.Perfil', on_delete=models.CASCADE, default=None)
    nota = models.CharField(max_length=100, blank=True)
    sueldo = models.PositiveIntegerField(blank=False)
    valor = models.FloatField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    agregado = models.CharField(max_length=100, blank=False, default=None)
    modificado_por = models.CharField(
        max_length=100, blank=False, default=None)

    def __str__(self):
        return 'El sueldo el {} de {} {} es de {} pesos'.format(
            self.creado.strftime('%Y-%m-%d %H:%M'),
            self.usuario.first_name,
            self.usuario.last_name,
            self.valor
        )


# Clientes Ventas, Sellado, Exrusión
class Descripcion(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    precio_vendido = models.FloatField(blank=True, default=None)
    precio_pagado = models.FloatField(blank=True, default=None)
    precio_compra = models.FloatField(blank=True, default=None)
    cantidad = models.FloatField(blank=False, default=None)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    area = models.CharField(max_length=100, blank=False, default='Sellado')
    modificado_por = models.CharField(
        max_length=100, blank=False, default=None)

    def __str__(self):
        if self.cantidad > 0.0:
            return '{}'.format(self.nombre)
        elif self.cantidad <= 0.0:
            return 'No hay {}'.format(self.nombre)


# Proveedores Compras, Lavado, Aglutinado, Peletizado
class DescripcionInterna(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    precio_vendido = models.FloatField(blank=True, default=None)
    precio_pagado = models.FloatField(blank=True, default=None)
    precio_compra = models.FloatField(blank=True, default=None)
    cantidad = models.FloatField(blank=False, default=None)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    area = models.CharField(max_length=100, blank=False, default='Peletizado')
    modificado_por = models.CharField(
        max_length=100, blank=False, default=None)

    def __str__(self):
        if self.cantidad > 0.0:
            return '{}'.format(self.nombre)
        elif self.cantidad <= 0.0:
            return 'No hay {}'.format(self.nombre)
