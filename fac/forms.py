from django import forms
from fac.models import Factura, DetalleFactura, TipoComprobante, Exportacion
from inv.models import Moneda, Producto, ClaveMovimiento
from cxc.models import Cliente

from django.forms import inlineformset_factory
from django.utils.timezone import now, localtime
from django.forms.models import BaseInlineFormSet

class BaseDetalleFacturaFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # opcional, pero no estrictamente necesario si usamos _should_delete_form
        for form in self.forms:
            if not self.data.get(form.add_prefix('producto')):
                form.empty_permitted = True

    def _should_delete_form(self, form):
        """
        Si el form no trae 'producto' (es un extra sin completar),
        forzamos que se trate como borrado antes de validar.
        """
        # Nombre exacto del campo producto en este subform
        producto_name = form.add_prefix('producto')
        # Si no vino ningún valor para producto → lo borramos
        if not self.data.get(producto_name):
            return True
        # Si el usuario marcó DELETE, también borrarlo
        # (se asume que usas can_delete=True)
        delete_name = form.add_prefix('DELETE')
        if self.data.get(delete_name):
            return True
        return False

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        exclude = ['serie_emisor',
                   'lugar_expedicion', 'tipo_cambio',  
                   'xml', 'pdf', 'uuid', 'fecha_timbrado',
                   'sello_cfdi', 'no_certificado_sat', 'empresa', 'usuario']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        # Bootstrap y estilos para campos específicos
        for name in ['impuestos_trasladados', 'impuestos_retenidos', 'subtotal', 'estatus']:
            self.fields[name].widget.attrs.update({
                'readonly': True,
                'tabindex': '-1',
                'class': 'form-control form-control-sm text-end bg-light'
            })

        self.fields['cliente'].queryset = Cliente.objects.using('tenant').all().order_by('nombre')
        self.fields['clave_remision'].queryset = ClaveMovimiento.objects.using('tenant').filter(es_remision=True).order_by('nombre')

        # Ocultar campos
        self.fields['descuento_factura'].widget = forms.HiddenInput()
        self.fields['moneda'].widget = forms.HiddenInput()
        self.fields['tipo_comprobante'].widget = forms.HiddenInput()
        self.fields['exportacion'].widget = forms.HiddenInput()

        # Inicializar valores por defecto al crear una nueva factura
        if not self.instance.pk:
            self.fields['estatus'].initial = "Borrador"
            self.fields['condiciones_pago'].initial = "CONTADO"
            self.fields['descuento_factura'].initial = 0
            self.fields['moneda'].initial = Moneda.objects.filter(clave="MXN").first()
            self.fields['tipo_comprobante'].initial = TipoComprobante.objects.filter(tipo_comprobante='I').first()
            self.fields['exportacion'].initial = Exportacion.objects.filter(exportacion='01').first()
                                                                
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'clave_prod_serv', 'clave_unidad', 'descripcion',
                  'cantidad', 'valor_unitario', 'descuento', 'importe', 'objeto_impuesto',
                  'tasa_iva', 'iva_producto', 'tasa_ieps', 'ieps_producto', 'retencion_iva', 'retencion_isr',
                  'tasa_retencion_iva', 'tasa_retencion_isr'
                ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'].queryset = Producto.objects.using('tenant').all().order_by('nombre')
        self.fields['objeto_impuesto'].required = False
        
        # Bootstrap para todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

        self.fields['objeto_impuesto'].initial = '02'  # Por defecto, objeto de impuesto
        self.fields['objeto_impuesto'].widget = forms.HiddenInput()
        # Impuestos ocultos
        for tax_field in ['tasa_iva', 'iva_producto', 'tasa_ieps', 'ieps_producto', 
                          'tasa_retencion_iva', 'tasa_retencion_isr', 'retencion_iva', 'retencion_isr',
                          'clave_unidad','descripcion']:
            self.fields[tax_field].initial = 0
            self.fields[tax_field].widget = forms.HiddenInput()

        # Clave SAT readonly
        self.fields['clave_prod_serv'].widget.attrs.update({
            'readonly': True,
            'tabindex': '-1',
            'class': 'form-control form-control-sm bg-light'
        })
        self.fields['importe'].widget.attrs.update({
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
    formset=BaseDetalleFacturaFormSet,
    fields=['producto', 'cantidad', 'valor_unitario', 'descuento', 'importe',
            'tasa_iva', 'iva_producto', 'tasa_ieps', 'ieps_producto', 
            'tasa_retencion_iva', 'tasa_retencion_isr', 'retencion_iva', 'retencion_isr',
            'clave_unidad','descripcion', 'objeto_impuesto', 'clave_prod_serv', 'descripcion'
            ],
    extra=1,
    can_delete=True
)