from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Adquisicion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey('usuarios.Perfil', on_delete=models.CASCADE, default=None)
    nombre = models.ForeignKey('proveedores.Proveedor', on_delete=models.CASCADE, default=None)
    descripcion = models.ForeignKey('sueldos.Descripcion', on_delete=models.CASCADE, default=None)
    cantidad = models.FloatField(blank=False)
    precio_compra = models.PositiveIntegerField(blank=False)
    nota = models.CharField(max_length=100, blank=True)
    compra = models.PositiveIntegerField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    credito = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return '{} {} compro {} de {} el {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.cantidad,
            self.descripcion.nombre,
            self.creado.strftime('%Y-%m-%d')
        )

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    identificador = models.CharField(max_length=100, blank=False, default=None)
    celular = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    nota = models.CharField(max_length=100, blank=True)
    saldo = models.FloatField(blank=False, default=None)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.nombre)