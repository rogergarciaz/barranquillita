from django import forms

class PerfilForm(forms.Form):
    celular = forms.CharField(max_length=20, required=True)
    foto = forms.ImageField(required=True)