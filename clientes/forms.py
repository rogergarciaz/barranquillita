# Django
from django import forms

# Models
from clientes.models import Compra


class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = (
            'descripcion', 'cantidad',
            'precio_vendido', 'nota'
        )
