from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Moneda, Categoria, UnidadMedida, Almacen, ClaveMovimiento, Proveedor
from .forms import MonedaForm, CategoriaForm, UnidadMedidaForm, AlmacenForm, ClaveMovimientoForm
from .forms import ProveedorForm

# CRUD MONEDAS
class MonedaListView(ListView):
    model = Moneda
    template_name = 'inv/moneda_list.html'
    context_object_name = 'monedas'

class MonedaCreateView(CreateView):
    model = Moneda
    form_class = MonedaForm
    template_name = 'inv/moneda_form.html'
    success_url = reverse_lazy('inv:moneda_list')

class MonedaUpdateView(UpdateView):
    model = Moneda
    form_class = MonedaForm
    template_name = 'inv/moneda_form.html'
    success_url = reverse_lazy('inv:moneda_list')

class MonedaDeleteView(DeleteView):
    model = Moneda
    template_name = 'inv/moneda_confirm_delete.html'
    success_url = reverse_lazy('inv:moneda_list')

# CRUD CATEGORIA
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'inv/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inv/categoria_form.html'
    success_url = reverse_lazy('inv:categoria_list')

class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inv/categoria_form.html'
    success_url = reverse_lazy('inv:categoria_list')

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'inv/categoria_confirm_delete.html'
    success_url = reverse_lazy('inv:categoria_list')

# CRUD UNIDAD DE MEDIDA
class UnidadMedidaListView(ListView):
    model = UnidadMedida
    template_name = 'inv/unidadmedida_list.html'
    context_object_name = 'unidadesmedida'

class UnidadMedidaCreateView(CreateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'inv/unidadmedida_form.html'
    success_url = reverse_lazy('inv:unidadmedida_list')

class UnidadMedidaUpdateView(UpdateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'inv/unidadmedida_form.html'
    success_url = reverse_lazy('inv:unidadmedida_list')

class UnidadMedidaDeleteView(DeleteView):
    model = UnidadMedida
    template_name = 'inv/unidadmedida_confirm_delete.html'
    success_url = reverse_lazy('inv:unidadmedida_list')

# CRUD ALMACEN
class AlmacenListView(ListView):
    model = Almacen
    template_name = 'inv/almacen_list.html'
    context_object_name = 'almacenes'

class AlmacenCreateView(CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'inv/almacen_form.html'
    success_url = reverse_lazy('inv:almacen_list')

class AlmacenUpdateView(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'inv/almacen_form.html'
    success_url = reverse_lazy('inv:almacen_list')

class AlmacenDeleteView(DeleteView):
    model = Almacen
    template_name = 'inv/almacen_confirm_delete.html'
    success_url = reverse_lazy('inv:almacen_list')

# CRUD CLAVES MOV INVENTARIO
class ClavesMovListView(ListView):
    model = ClaveMovimiento
    template_name = 'inv/clavemovimiento_list.html'
    context_object_name = 'clavesmovimiento'

class ClavesMovCreateView(CreateView):
    model = ClaveMovimiento
    form_class = ClaveMovimientoForm
    template_name = 'inv/clavemovimiento_form.html'
    success_url = reverse_lazy('inv:clavemovimiento_list')

class ClavesMovUpdateView(UpdateView):
    model = ClaveMovimiento
    form_class = ClaveMovimientoForm
    template_name = 'inv/clavemovimiento_form.html'
    success_url = reverse_lazy('inv:clavemovimiento_list')

class ClavesMovDeleteView(DeleteView):
    model = ClaveMovimiento
    template_name = 'inv/clavemovimiento_confirm_delete.html'
    success_url = reverse_lazy('inv:clavemovimiento_list')

# CRUD PROVEEDOR
class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'inv/proveedor_list.html'
    context_object_name = 'proveedores'

class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'inv/proveedor_form.html'
    success_url = reverse_lazy('inv:proveedor_list')

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'inv/proveedor_form.html'
    success_url = reverse_lazy('inv:proveedor_list')

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'inv/proveedor_confirm_delete.html'
    success_url = reverse_lazy('inv:proveedor_list')
