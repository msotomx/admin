from django import forms
from timbres.models import MovimientoTimbresGlobal

class AsignarTimbresForm(forms.ModelForm):
    class Meta:
        model = MovimientoTimbresGlobal
        fields = ['codigo_empresa','referencia','cantidad','importe']
        widgets = {
            'codigo_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'importe': forms.TextInput(attrs={'class': 'form-control'})
        }        
