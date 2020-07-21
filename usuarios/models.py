from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    seguro = models.PositiveIntegerField()
    recordar = models.PositiveIntegerField()
    celular = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='usuarios/fotos', blank=True, null=True)
    nacimiento = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.username