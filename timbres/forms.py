from django import forms
from .models import MovimientoTimbresGlobal
from django.utils.timezone import now, localtime

class EntradaTimbreForm(forms.ModelForm):
    class Meta:
        model = MovimientoTimbresGlobal
        fields = ['referencia', 'cantidad', 'importe']

class AsignarTimbresForm(forms.ModelForm):
    class Meta:
        model = MovimientoTimbresGlobal
        fields = ['codigo_empresa','referencia', 'cantidad', 'importe']
