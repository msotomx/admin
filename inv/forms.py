from django import forms
from .models import Moneda, Categoria, UnidadMedida, Almacen, Producto
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
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'subcategoria': forms.TextInput(attrs={'class': 'form-control'}),
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
