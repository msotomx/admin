from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Moneda, Categoria, UnidadMedida, Almacen
from .models import ClaveMovimiento, Proveedor, Producto
from .models import Movimiento, DetalleMovimiento
from .models import Traspaso, DetalleTraspaso, Remision, DetalleRemision, SaldoInicial

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = ['nombre', 'clave', 'simbolo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'clave': forms.TextInput(attrs={'class': 'form-control'}),
            'simbolo': forms.TextInput(attrs={'class': 'form-control'}),
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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['campo_libre_str'].required = False
            self.fields['campo_libre_num'].required = False
        
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        exclude = ['usuario', 'move_s']  # Ocultamos move_s (se asignará en la vista)
        widgets = {
            'fecha_movimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = ['producto', 'cantidad', 'precio', 'descuento', 'subtotal']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['descuento'].initial = 0  # Valor inicial por defecto

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

# Inline formset
DetalleMovimientoFormSet = inlineformset_factory(
    parent_model=Movimiento,
    model=DetalleMovimiento,
    form=DetalleMovimientoForm,
    formset=DetalleMovimientoFormSet,
    fk_name='referencia',
    fields=['producto', 'cantidad', 'precio', 'descuento', 'subtotal'],
    extra=1,
    can_delete=True
)
