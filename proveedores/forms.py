# Django
from django import forms

# Models
from proveedores.models import Adquisicion

class AdquisicionForm(forms.ModelForm):

    class Meta:
        model = Adquisicion
        fields = (
            'descripcion', 'cantidad', 'credito',
            'precio_compra', 'nota'
        )