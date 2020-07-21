# Django
from django import forms

# Models
from salarios.models import Produccion

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ('area', 'descripcion', 'cantidad', 'precio_pagado', 'usuario', 'perfil', 'nota')