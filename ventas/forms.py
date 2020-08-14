# Django
from django import forms

# Models
from ventas.models import Venta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = (
            'cliente_id', 'descripcion', 'cantidad',
            'precio_vendido', 'nota', 'usuario',
            'perfil', 'venta'
        )
