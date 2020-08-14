from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey('usuarios.Perfil', on_delete=models.CASCADE, default=None)
    cliente_id = models.ForeignKey('ventas.Cliente', on_delete=models.CASCADE, default=None)
    descripcion = models.ForeignKey('sueldos.Descripcion', on_delete=models.CASCADE)
    cantidad = models.FloatField(blank=False)
    precio_vendido = models.PositiveIntegerField(blank=False)
    nota = models.CharField(max_length=100, blank=True)
    venta = models.PositiveIntegerField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} vendio {} de {} el {}'.format(
            self.usuario.first_name,
            self.usuario.last_name,
            self.cantidad,
            self.descripcion.nombre,
            self.creado.strftime('%Y-%m-%d')
        )

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False)
    celular = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    nota = models.CharField(max_length=100, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'El cliente {} tiene el número {} y su direccion es {}'.format(
            self.nombre,
            self.celular,
            self.direccion
        )