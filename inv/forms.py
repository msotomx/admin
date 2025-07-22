from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.timezone import now, localtime
from .models import Moneda, Categoria, UnidadMedida, Almacen
from .models import ClaveMovimiento, Proveedor, Producto, Vendedor
from .models import Movimiento, DetalleMovimiento
from .models import Traspaso, DetalleTraspaso, Remision, DetalleRemision, SaldoInicial
from .models import Compra, DetalleCompra, Cotizacion, DetalleCotizacion
from core.models import Empresa
from cxc.models import Cliente
from core.models import CertificadoCSD

from decimal import Decimal
from collections import defaultdict

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ['clave', 'nombre', 'simbolo', 'paridad', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'clave': forms.TextInput(attrs={'class': 'form-control'}),
            'simbolo': forms.TextInput(attrs={'class': 'form-control'}),
            'paridad': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UnidadMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = '__all__'
        widgets = {
            'unidadmedida': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = '__all__'
        widgets = {
            'almacen': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClaveMovimientoForm(forms.ModelForm):
    class Meta:
        model = ClaveMovimiento
        fields = '__all__'
        widgets = {
            'clavemovimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono2': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'plazocredito': forms.TextInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = '__all__'
        widgets = {
            'vendedor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }        

from django import forms
from django.db import transaction
from .models import Producto
#self.fields['fecha_registro'].initial = localtime(now()).date()

from django import forms

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'fecha_movimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # como el router maneja la conexion ya no es necesario db_name 
        super().__init__(*args, **kwargs)
        
        self.fields['fecha_registro'].initial = localtime(now()).date()
        self.fields['categoria'].queryset = Categoria.objects.using('tenant').order_by('nombre')
        self.fields['unidad_medida'].queryset = UnidadMedida.objects.using('tenant').order_by('unidad_medida')
        self.fields['proveedor'].queryset = Proveedor.objects.using('tenant').order_by('nombre')
        
# MOVIMIENTOS
from datetime import date
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        exclude = ['usuario', 'move_s']  # Ocultamos move_s (se asignará en la vista)
        widgets = {
            'fecha_movimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clave_movimiento'].queryset = ClaveMovimiento.objects.using('tenant').order_by('nombre')

class DetalleMovimientoForm(forms.ModelForm):  
    class Meta:
        model = DetalleMovimiento
        fields = ['producto', 'cantidad', 'costo_unit', 'subtotal']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'costo_unit': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.using('tenant').all().order_by('nombre')
        
# valida productos repetidos
# valida cantidad = 0
class DetalleMovimientoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        productos_vistos = set()

        for form in self.forms:
            if not form.cleaned_data or (self.can_delete and self._should_delete_form(form)):
                continue

            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad')

            if not producto:
                raise ValidationError('Debe seleccionar un producto en cada línea del detalle.')

            if cantidad is None or cantidad <= 0:
                raise ValidationError(f'La cantidad para el producto "{producto}" debe ser mayor a cero.')

            if producto in productos_vistos:
                raise ValidationError(f'El producto "{producto}" está duplicado en el detalle.')

            productos_vistos.add(producto)

DetalleMovimientoFormSet = inlineformset_factory(
    parent_model=Movimiento,
    model=DetalleMovimiento,
    form=DetalleMovimientoForm,
    formset=DetalleMovimientoFormSet,
    fk_name='referencia',
    fields=['producto', 'cantidad', 'costo_unit', 'subtotal'],
    extra=1,
    can_delete=True
)

# COTIZACIONES
from datetime import date
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = '__all__'
        widgets = {
            'fecha_cotizacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendedor'].queryset = Vendedor.objects.using('tenant').order_by('nombre')

class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.using('tenant').all().order_by('nombre')
        
# valida productos repetidos
# valida cantidad = 0
class DetalleCotizacionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        productos_vistos = set()

        for form in self.forms:
            if not form.cleaned_data or (self.can_delete and self._should_delete_form(form)):
                continue

            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad')

            if not producto:
                raise ValidationError('Debe seleccionar un producto en cada línea del detalle.')

            if cantidad is None or cantidad <= 0:
                raise ValidationError(f'La cantidad para el producto "{producto}" debe ser mayor a cero.')

            if producto in productos_vistos:
                raise ValidationError(f'El producto "{producto}" está duplicado en el detalle.')

            productos_vistos.add(producto)

DetalleCotizacionFormSet = inlineformset_factory(
    parent_model=Cotizacion,
    model=DetalleCotizacion,
    form=DetalleCotizacionForm,
    formset=DetalleCotizacionFormSet,
    fk_name='numero_cotizacion',
    fields=['producto', 'cantidad', 'precio', 'descuento', 'subtotal'],
    extra=1,
    can_delete=True
)


# REMISIONES
class RemisionForm(forms.ModelForm):
    class Meta:
        model = Remision
        fields = '__all__'  
        exclude = ['usuario', 'numero_factura', 'status', 'monto_total']
        widgets = {
            'fecha_remision': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        self.fields['cliente'].queryset = Cliente.objects.using('tenant').all().order_by('nombre')
        self.fields['clave_movimiento'].queryset = ClaveMovimiento.objects.using('tenant').filter(es_remision=True).order_by('nombre')
        self.fields['vendedor'].queryset = Vendedor.objects.using('tenant').all().order_by('nombre')

class DetalleRemisionForm(forms.ModelForm):
    class Meta:
        model = DetalleRemision
        fields = ['producto', 'cantidad', 'precio', 'descuento', 'subtotal',
                  'tasa_iva', 'iva_producto', 'tasa_ieps', 'ieps_producto',
                  'tasa_retencion_iva','tasa_retencion_isr',
                  'retencion_iva','retencion_isr'
                  ]

        widgets = {
            'producto'  : forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cantidad'  : forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'precio'    : forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'descuento' : forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'subtotal'  : forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'].queryset = Producto.objects.using('tenant').all().order_by('nombre')
               
        # Bootstrap para todos los campos
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

        # Impuestos ocultos
        for tax_field in ['tasa_iva', 'iva_producto', 'tasa_ieps', 'ieps_producto', 
                          'tasa_retencion_iva', 'tasa_retencion_isr', 'retencion_iva', 'retencion_isr']:
            self.fields[tax_field].initial = 0
            self.fields[tax_field].widget = forms.HiddenInput()

# valida productos repetidos
# valida cantidad = 0

class DetalleRemisionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        productos_vistos = defaultdict(Decimal)  # clave: producto_id, valor: cantidad acumulada
        descuentos_vistos = defaultdict(Decimal)  # clave: producto_id, valor: cantidad acumulada
        formularios_a_eliminar = []

        for form in self.forms:
            if form.cleaned_data.get('DELETE', False):
                formularios_a_eliminar.append(form)
                continue

            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad') or Decimal(0)
            descuento = form.cleaned_data.get('descuento') or Decimal(0)

            if not producto:
                continue  # O puedes lanzar ValidationError si es obligatorio

            productos_vistos[producto] += cantidad
            descuentos_vistos[producto] += descuento

        # Ahora recorremos otra vez para actualizar cantidades y marcar duplicados para eliminación
        productos_actualizados = set()
        for form in self.forms:
            if form in formularios_a_eliminar or not form.cleaned_data.get('producto'):
                continue

            producto = form.cleaned_data['producto']

            if producto in productos_actualizados:
                # Ya consolidamos esta línea, marcar para eliminación
                form.cleaned_data['DELETE'] = True
            else:
                cantidad_total = productos_vistos[producto]
                precio = form.cleaned_data.get('precio') or Decimal(0)
                descuento_total = descuentos_vistos[producto]
                #descuento = form.cleaned_data.get('descuento') or Decimal(0)
                #subtotal = (cantidad_total * precio) - descuento
                subtotal = (cantidad_total * precio) - descuento_total

                # Actualizamos los campos en cleaned_data
                form.cleaned_data['cantidad'] = cantidad_total
                form.cleaned_data['descuento'] = descuento_total
                form.cleaned_data['subtotal'] = subtotal

                # Y también en la instancia del modelo
                if hasattr(form, 'instance'):
                    form.instance.cantidad = cantidad_total
                    form.instance.descuento = descuento_total
                    form.instance.subtotal = subtotal

                productos_actualizados.add(producto)

# Inline formset
DetalleRemisionFormSet = inlineformset_factory(
    parent_model=Remision,
    model=DetalleRemision,
    form=DetalleRemisionForm,
    formset=DetalleRemisionFormSet,
    fk_name='numero_remision',
    fields=['producto', 'cantidad', 'precio', 'descuento', 'subtotal', 'tasa_iva','tasa_ieps',
            'iva_producto', 'ieps_producto','tasa_retencion_iva','tasa_retencion_isr',
            'retencion_iva','retencion_isr'],
    extra=1,
    can_delete=True
)

# COMPRAS
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        exclude = ['usuario', 'fecha_pagada', 'pedido', 'descuento_pp', 'monto_total']
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        self.fields['clave_movimiento'].queryset = ClaveMovimiento.objects.using('tenant').filter(es_compra=True).order_by('nombre')
        self.fields['proveedor'].queryset = Proveedor.objects.using('tenant').all().order_by('nombre')
        self.fields['fecha_vencimiento'].initial = localtime(now()).date()
        
        # Aplica clases a todos los campos visibles
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

        # Alinear a la derecha los campos numéricos
        campos_derecha = ['paridad', 'flete', 'monto_total']
        for nombre in campos_derecha:
            if nombre in self.fields:
                clases = self.fields[nombre].widget.attrs.get('class', '')
                self.fields[nombre].widget.attrs['class'] = f"{clases} text-end"

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'costo_unit', 'descuento', 'subtotal']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'costo_unit': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.using('tenant').all().order_by('nombre')

# valida cantidad = 0
class DetalleCompraFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        productos_vistos = defaultdict(Decimal)  # clave: producto_id, valor: cantidad acumulada
        descuentos_vistos = defaultdict(Decimal)  # clave: producto_id, valor: cantidad acumulada
        formularios_a_eliminar = []

        for form in self.forms:
            if form.cleaned_data.get('DELETE', False):
                formularios_a_eliminar.append(form)
                continue

            producto = form.cleaned_data.get('producto')
            cantidad = form.cleaned_data.get('cantidad') or Decimal(0)
            descuento = form.cleaned_data.get('descuento') or Decimal(0)

            if not producto:
                continue  # O puedes lanzar ValidationError si es obligatorio

            productos_vistos[producto] += cantidad
            descuentos_vistos[producto] += descuento

        # Ahora recorremos otra vez para actualizar cantidades y marcar duplicados para eliminación
        productos_actualizados = set()
        for form in self.forms:
            if form in formularios_a_eliminar or not form.cleaned_data.get('producto'):
                continue

            producto = form.cleaned_data['producto']

            if producto in productos_actualizados:
                # Ya consolidamos esta línea, marcar para eliminación
                form.cleaned_data['DELETE'] = True
            else:
                cantidad_total = productos_vistos[producto]
                costo_unit = form.cleaned_data.get('costo_unit') or Decimal(0)
                descuento_total = descuentos_vistos[producto]
                subtotal = (cantidad_total * costo_unit) - descuento_total

                # Actualizamos los campos en cleaned_data
                form.cleaned_data['cantidad'] = cantidad_total
                form.cleaned_data['descuento'] = descuento_total
                form.cleaned_data['subtotal'] = subtotal

                # Y también en la instancia del modelo
                if hasattr(form, 'instance'):
                    form.instance.cantidad = cantidad_total
                    form.instance.descuento = descuento_total
                    form.instance.subtotal = subtotal

                productos_actualizados.add(producto)

# Inline formset
DetalleCompraFormSet = inlineformset_factory(
    parent_model=Compra,
    model=DetalleCompra,
    form=DetalleCompraForm,
    formset=DetalleCompraFormSet,
    fk_name='referencia',
    fields=['producto', 'cantidad', 'costo_unit', 'descuento', 'subtotal'],
    extra=1,
    can_delete=True
)

# INFORMACION GENERAL EMPRESA
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ['empresa','num_empresa','fecha_inicio','fecha_renovacion','factor','activa','directorio',
                   'calle_expedicion','numero_exterior_expedicion','numero_interior_expedicion',
                   'colonia_expedicion','localidad_expedicion','municipio_expedicion','estado_expedicion',
                   'pais_expedicion', 'db_name']
        fields = '__all__'  # O puedes listar explícitamente los campos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'

class EmpresaLugarForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre_comercial', 'calle_expedicion', 'numero_exterior_expedicion',
                  'numero_interior_expedicion','colonia_expedicion','codigo_postal_expedicion',
                  'localidad_expedicion','municipio_expedicion','estado_expedicion','pais_expedicion', 'db_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-sm'            

class CertificadoCSDForm(forms.ModelForm):
    class Meta:
        model = CertificadoCSD
        fields = ['rfc', 'cer_archivo', 'key_archivo', 'password']
