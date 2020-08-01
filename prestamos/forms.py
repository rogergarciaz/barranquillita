# Django
from django import forms

# Models
from prestamos.models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('descripcion', 'cuotas', 'cuotas_debidas', 'valor', 'usuario', 'perfil')