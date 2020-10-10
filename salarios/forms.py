# Django
from django import forms

# Models
from salarios.models import Produccion, ProduccionInterna, Fijo


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ('area', 'descripcion', 'cantidad',
                  'precio_pagado', 'usuario', 'perfil', 'nota')


class ProductionInternaForm(forms.ModelForm):
    class Meta:
        model = ProduccionInterna
        fields = ('area', 'descripcion', 'cantidad',
                  'precio_pagado', 'usuario', 'perfil', 'nota')


class FijoForm(forms.ModelForm):
    class Meta:
        model = Fijo
        fields = ('area', 'precio_pagado', 'usuario', 'perfil', 'nota')
