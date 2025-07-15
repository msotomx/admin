from django import forms
from .models import TipoCliente, Cliente, RegimenFiscal
from core._thread_locals import get_current_tenant
from django.db import connections

class TipoClienteForm(forms.ModelForm):
    class Meta:
        model = TipoCliente
        fields = ['tipo_cliente', 'nombre']
        widgets = {
            'tipo_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipocliente': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono2': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control form-control-sm'}),
            'direccion_entrega': forms.Textarea(attrs={'rows': 3, 'class': 'form-control form-control-sm'}),
            'comentarios': forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm'}),
        }
        
    def __init__(self, *args, **kwargs):
        db_name = kwargs.pop('db_name', None)
        super().__init__(*args, **kwargs)

        self.fields['tipo_cliente'].queryset = TipoCliente.objects.using('tenant')
        self.fields['regimen_fiscal'].queryset = RegimenFiscal.objects.using('tenant').order_by('nombre')
          
        self.fields['campo_libre_str'].required = False
        self.fields['campo_libre_num'].required = False
        self.fields['campo_libre_str'].initial = ''
        self.fields['campo_libre_num'].initial = 0
        
    def clean_cliente(self):
        cliente = self.cleaned_data['cliente']
        cliente_str = cliente.zfill(6)  # convierte a string y rellena con ceros
        return cliente_str
        

