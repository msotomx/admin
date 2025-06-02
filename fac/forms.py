from django import forms
from fac.models import Factura, DetalleFactura
from django.forms import inlineformset_factory
from django.utils.timezone import now, localtime

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica clase Bootstrap a todos los campos
        for field in self.fields.values():
            self.fields['impuestos_trasladados'].widget.attrs.update({
                'readonly': True,
                'tabindex': '-1',
                'class': 'form-control form-control-sm text-end bg-light'
            })
            self.fields['impuestos_retenidos'].widget.attrs.update({
                'readonly': True,
                'tabindex': '-1',
                'class': 'form-control form-control-sm text-end bg-light'
            })
            self.fields['subtotal'].widget.attrs.update({
                'readonly': True,
                'tabindex': '-1',
                'class': 'form-control form-control-sm text-end bg-light'
            })

class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = [
            'producto',
            'clave_prod_serv',
            'cantidad',
            'valor_unitario',
            'descuento',
            'importe',
            'objeto_imp',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap para todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

        self.fields['objeto_imp'].initial = '02'  # Por defecto, objeto de impuesto

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        valor_unitario = cleaned_data.get('valor_unitario')

        if cantidad is not None and cantidad <= 0:
            self.add_error('cantidad', 'La cantidad debe ser mayor a cero.')

        if valor_unitario is not None and valor_unitario <= 0:
            self.add_error('valor_unitario', 'El valor unitario debe ser mayor a cero.')

DetalleFacturaFormSet = inlineformset_factory(
    Factura,
    DetalleFactura,
    form=DetalleFacturaForm,
    extra=1,
    can_delete=True
)