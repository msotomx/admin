from django import forms
from fac.models import Factura, DetalleFactura, TipoComprobante, Exportacion
from inv.models import Moneda

from django.forms import inlineformset_factory
from django.utils.timezone import now, localtime

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        exclude = ['serie_emisor', 'serie_sat', 'fecha_hora_certificacion', 
                   'lugar_expedicion', 'tipo_cambio',  
                   'descuento', 'xml', 'pdf', 'uuid', 'fecha_timbrado',
                   'sello_cfdi', 'no_certificado_sat', 'empresa']
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
            self.fields['estatus'].widget.attrs.update({
                'readonly': True,
                'tabindex': '-1',
                'class': 'form-control form-control-sm text-end bg-light'
            })

            self.fields['moneda'].initial = Moneda.objects.filter(clave="MXN").first()
            self.fields['moneda'].widget = forms.HiddenInput()  # el campo no es visible en el formulario
            self.fields['tipo_comprobante'].initial = TipoComprobante.objects.filter(tipo_comprobante='I').first()
            self.fields['tipo_comprobante'].widget = forms.HiddenInput()  # el campo no es visible en el formulario
            self.fields['exportacion'].initial = Exportacion.objects.filter(exportacion='01').first()
            self.fields['exportacion'].widget = forms.HiddenInput()  # el campo no es visible en el formulario
            self.fields['estatus'].initial = "BORRADOR"
            self.fields['condiciones_pago'].initial = "1"
            self.fields['condiciones_pago'].widget = forms.HiddenInput()  # el campo no es visible en el formulario
                                        
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'clave_prod_serv', 'clave_unidad', 'descripcion',
                  'cantidad', 'valor_unitario', 'descuento', 'importe', 'objeto_imp' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['clave_unidad'].required = False
        self.fields['descripcion'].required = False
        self.fields['objeto_imp'].required = False
        
        # Bootstrap para todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

        self.fields['objeto_imp'].initial = '02'  # Por defecto, objeto de impuesto
        self.fields['objeto_imp'].widget = forms.HiddenInput()
        self.fields['clave_prod_serv'].widget.attrs.update({
            'readonly': True,
            'tabindex': '-1',
            'class': 'form-control form-control-sm bg-light'
        })

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