from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Moneda, Categoria, UnidadMedida, Almacen, ClaveMovimiento, Proveedor
from .models import Producto, Movimiento, DetalleMovimiento
from .forms import MonedaForm, CategoriaForm, UnidadMedidaForm, AlmacenForm, ClaveMovimientoForm
from .forms import ProveedorForm, ProductoForm, MovimientoForm,  DetalleMovimientoFormSet

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

# CRUD PRODUCTO
class ProductoListView(ListView):
    model = Producto
    template_name = 'inv/producto_list.html'
    context_object_name = 'productos'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inv/producto_form.html'
    success_url = reverse_lazy('inv:producto_list')

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inv/producto_form.html'
    success_url = reverse_lazy('inv:producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'inv/producto_confirm_delete.html'
    success_url = reverse_lazy('inv:producto_list')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

# CRUD MOVIMIENTOS
class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'inv/movimiento_list.html'
    context_object_name = 'movimientos'

class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inv/movimiento_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = DetalleMovimientoFormSet(queryset=DetalleMovimiento.objects.none())  # Inicializa el formset vacío
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleMovimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Guardar el movimiento
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.move_s = movimiento.clave_movimiento.tipo
            movimiento.save()

            # Asociar los detalles con el movimiento y guardarlos
            formset.instance = movimiento
            formset.save()

            return redirect('inv:movimiento_list')  # Redirige a la lista de movimientos
        
        return render(request, self.template_name, {'form': form, 'formset': formset})

class MovimientoUpdateView(UpdateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inv/movimiento_form.html'
    success_url = reverse_lazy('inv:movimiento_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DetalleMovimientoFormSet(self.request.POST, instance=self.object, prefix='detalles')
        else:
            data['formset'] = DetalleMovimientoFormSet(instance=self.object, prefix='detalles')
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            # Añadir depuración de errores en formset
            print("Formset no es válido:", formset.errors)
            return self.form_invalid(form)

# DETALLE DE MOVIMIENTO
class MovimientoDetailView(DetailView):
    model = Movimiento
    template_name = 'inv/movimiento_detail.html'
    context_object_name = 'movimiento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleMovimiento.objects.filter(referencia=self.object)
        return context

class MovimientoDeleteView(DeleteView):
    model = Movimiento
    template_name = 'inv/movimiento_confirm_delete.html'
    success_url = reverse_lazy('inv:movimiento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context
