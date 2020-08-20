# Django
from django import forms

# Models
from clientes.models import Compra

class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = (
            'nombre', 'descripcion', 'cantidad',
            'precio_vendido', 'nota'
        )
        # Acomodar el Form para el Template