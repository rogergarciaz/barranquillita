# Django
from django import forms

# Models
from proveedores.models import Adquisicion

class AdquisicionForm(forms.ModelForm):

    class Meta:
        model = Adquisicion
        fields = (
            'descripcion', 'cantidad',
            'precio_compra', 'nota'
        )