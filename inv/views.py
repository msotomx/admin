from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum, Q
from django.conf import settings

from .forms import CertificadoCSDForm
from core.models import CertificadoCSD
from core._thread_locals import get_current_tenant
from services.pac import registrar_emisor_pac
from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Moneda, Categoria, UnidadMedida, Almacen, ClaveMovimiento, Proveedor, Vendedor
from .models import Producto, Movimiento, DetalleMovimiento, Remision, DetalleRemision
from .models import Compra, DetalleCompra
from .models import SaldoInicial
from core.models import Empresa
from cxc.models import Cliente
from core.models import CertificadoCSD
from .forms import MonedaForm, CategoriaForm, UnidadMedidaForm, AlmacenForm, ClaveMovimientoForm
from .forms import ProveedorForm, ProductoForm, MovimientoForm,  DetalleMovimientoFormSet
from .forms import VendedorForm
from .forms import RemisionForm,  DetalleRemisionFormSet
from .forms import CompraForm,  DetalleCompraFormSet
from .forms import EmpresaForm, EmpresaLugarForm
from datetime import date
from django.http import JsonResponse
from django.db.models import Case, When, Value, F, DecimalField
from datetime import datetime
from django.utils.timezone import now, localtime
from core.db_router import get_current_tenant_connection
from core.mixins import TenantRequiredMixin
from django.contrib.auth.decorators import login_required
from core.decorators import tenant_required
from core._thread_locals import get_current_tenant, get_current_empresa_id, get_current_empresa_fiscal

# CRUD MONEDAS
class MonedaListView(TenantRequiredMixin,ListView):
    model = Moneda
    template_name = 'inv/moneda_list.html'
    context_object_name = 'monedas'

    def get_queryset(self):
        db_name= get_current_tenant()
        return Moneda.objects.using(db_name).all()
    
class MonedaCreateView(TenantRequiredMixin,CreateView):
    model = Moneda
    form_class = MonedaForm
    template_name = 'inv/moneda_form.html'
    success_url = reverse_lazy('inv:moneda_list')

    def form_valid(self, form):
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name = get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)
    
class MonedaUpdateView(TenantRequiredMixin,UpdateView):
    model = Moneda
    form_class = MonedaForm
    template_name = 'inv/moneda_form.html'
    success_url = reverse_lazy('inv:moneda_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Moneda.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)


class MonedaDeleteView(TenantRequiredMixin,DeleteView):
    model = Moneda
    template_name = 'inv/moneda_confirm_delete.html'
    success_url = reverse_lazy('inv:moneda_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Moneda.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD CATEGORIA
class CategoriaListView(TenantRequiredMixin,ListView):
    model = Categoria
    template_name = 'inv/categoria_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        db_name= get_current_tenant()
        return Categoria.objects.using(db_name).all()

class CategoriaCreateView(TenantRequiredMixin,CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inv/categoria_form.html'
    success_url = reverse_lazy('inv:categoria_list')

    def form_valid(self, form):
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class CategoriaUpdateView(TenantRequiredMixin,UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inv/categoria_form.html'
    success_url = reverse_lazy('inv:categoria_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Categoria.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class CategoriaDeleteView(TenantRequiredMixin,DeleteView):
    model = Categoria
    template_name = 'inv/categoria_confirm_delete.html'
    success_url = reverse_lazy('inv:categoria_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Categoria.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD UNIDAD DE MEDIDA
class UnidadMedidaListView(TenantRequiredMixin,ListView):
    model = UnidadMedida
    template_name = 'inv/unidadmedida_list.html'
    context_object_name = 'unidadesmedida'
    
    def get_queryset(self):
        db_name= get_current_tenant()
        return UnidadMedida.objects.using(db_name).all()

class UnidadMedidaCreateView(TenantRequiredMixin,CreateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'inv/unidadmedida_form.html'
    success_url = reverse_lazy('inv:unidadmedida_list')

    def form_valid(self, form):
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class UnidadMedidaUpdateView(TenantRequiredMixin,UpdateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'inv/unidadmedida_form.html'
    success_url = reverse_lazy('inv:unidadmedida_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return UnidadMedida.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class UnidadMedidaDeleteView(TenantRequiredMixin,DeleteView):
    model = UnidadMedida
    template_name = 'inv/unidadmedida_confirm_delete.html'
    success_url = reverse_lazy('inv:unidadmedida_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return UnidadMedida.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD ALMACEN
class AlmacenListView(TenantRequiredMixin,ListView):
    model = Almacen
    template_name = 'inv/almacen_list.html'
    context_object_name = 'almacenes'
    
    def get_queryset(self):
        db_name= get_current_tenant()
        return Almacen.objects.using(db_name).all()

class AlmacenCreateView(TenantRequiredMixin,CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'inv/almacen_form.html'
    success_url = reverse_lazy('inv:almacen_list')

    def form_valid(self, form):
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class AlmacenUpdateView(TenantRequiredMixin,UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'inv/almacen_form.html'
    success_url = reverse_lazy('inv:almacen_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Almacen.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class AlmacenDeleteView(TenantRequiredMixin,DeleteView):
    model = Almacen
    template_name = 'inv/almacen_confirm_delete.html'
    success_url = reverse_lazy('inv:almacen_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Almacen.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD CLAVES MOV INVENTARIO
class ClavesMovListView(TenantRequiredMixin,ListView):
    model = ClaveMovimiento
    template_name = 'inv/clavemovimiento_list.html'
    context_object_name = 'clavesmovimiento'
    ordering = ['nombre'] 

    def get_queryset(self):
        db_name= get_current_tenant()
        return ClaveMovimiento.objects.using(db_name).all()

class ClavesMovCreateView(TenantRequiredMixin,CreateView):
    model = ClaveMovimiento
    form_class = ClaveMovimientoForm
    template_name = 'inv/clavemovimiento_form.html'
    success_url = reverse_lazy('inv:clavemovimiento_list')

    def form_valid(self, form):
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class ClavesMovUpdateView(TenantRequiredMixin,UpdateView):
    model = ClaveMovimiento
    form_class = ClaveMovimientoForm
    template_name = 'inv/clavemovimiento_form.html'
    success_url = reverse_lazy('inv:clavemovimiento_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return ClaveMovimiento.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class ClavesMovDeleteView(TenantRequiredMixin,DeleteView):
    model = ClaveMovimiento
    template_name = 'inv/clavemovimiento_confirm_delete.html'
    success_url = reverse_lazy('inv:clavemovimiento_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return ClaveMovimiento.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD VENDEDOR
class VendedorListView(TenantRequiredMixin,ListView):
    model = Vendedor
    template_name = 'inv/vendedor_list.html'
    context_object_name = 'vendedores'

    def get_queryset(self):
        db_name= get_current_tenant()
        return Vendedor.objects.using(db_name).all()

class VendedorCreateView(TenantRequiredMixin,CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'inv/vendedor_form.html'
    success_url = reverse_lazy('inv:vendedor_list')

    def get_initial(self):
        initial = super().get_initial()

        initial['fecha_registro'] = date.today()
        return initial

    def form_valid(self, form):
        vendedor = form.cleaned_data['vendedor']
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.vendedor = str(vendedor).zfill(3)
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class VendedorUpdateView(TenantRequiredMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'inv/vendedor_form.html'
    success_url = reverse_lazy('inv:vendedor_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Vendedor.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class VendedorDeleteView(TenantRequiredMixin, DeleteView):
    model = Vendedor
    template_name = 'inv/vendedor_confirm_delete.html'
    success_url = reverse_lazy('inv:vendedor_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Vendedor.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD PROVEEDOR
class ProveedorListView(TenantRequiredMixin, ListView):
    model = Proveedor
    template_name = 'inv/proveedor_list.html'
    context_object_name = 'proveedores'

    def get_queryset(self):
        db_name= get_current_tenant()
        return Proveedor.objects.using(db_name).all()

class ProveedorCreateView(TenantRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'inv/proveedor_form.html'
    success_url = reverse_lazy('inv:proveedor_list')

    def form_valid(self, form):
        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class ProveedorUpdateView(TenantRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'inv/proveedor_form.html'
    success_url = reverse_lazy('inv:proveedor_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Proveedor.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class ProveedorDeleteView(TenantRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'inv/proveedor_confirm_delete.html'
    success_url = reverse_lazy('inv:proveedor_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Proveedor.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD PRODUCTO
class ProductoListView(TenantRequiredMixin, ListView):
    model = Producto
    template_name = 'inv/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        # Primero obtenemos todos los productos
        db_name= get_current_tenant()
        productos = Producto.objects.using(db_name).all()
        
        if query:
            # Aplicamos filtros si hay búsqueda
            productos = productos.filter(
                Q(nombre__icontains=query) |
                Q(sku__icontains=query)
            )
        
        # Finalmente, ordenamos en orden alfabetico por nombre
        return productos.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()  # para que se mantenga en el input
        return context

class ProductoCreateView(TenantRequiredMixin, CreateView):  
    model = Producto
    form_class = ProductoForm
    template_name = 'inv/producto_form.html'
    success_url = reverse_lazy('inv:producto_list')

    def get_initial(self):
        initial = super().get_initial()

        initial['fecha_registro'] = date.today()
        return initial

    def form_valid(self, form):
        sku = form.cleaned_data['sku']
        form.instance.sku = str(sku).zfill(6)

        # Accede al nombre de la base de datos del tenant desde la sesión
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Errores del form producto:", form.errors)
        return 

class ProductoUpdateView(TenantRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inv/producto_form.html'
    success_url = reverse_lazy('inv:producto_list')

    def get_queryset(self):
        db_name = get_current_tenant()
        return Producto.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class ProductoDeleteView(TenantRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inv/producto_confirm_delete.html'
    success_url = reverse_lazy('inv:producto_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Producto.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

# CRUD MOVIMIENTOS
class MovimientoListView(TenantRequiredMixin, ListView):
    model = Movimiento
    template_name = 'inv/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha_movimiento','-clave_movimiento', '-referencia']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página
 
class MovimientoCreateView(TenantRequiredMixin, CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inv/movimiento_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = self.empresa #  <==== Viene de TenantRequireMixin
        print("Empresa en MovimientoCreateView:",empresa)
        db_name= get_current_tenant()
        if empresa:
            # Verificar que el almacen_actual está asignado
            if empresa.almacen_actual:
                try:
                    # Buscar el Almacen usando el ID almacen_actual
                    almacen = Almacen.objects.using(db_name).get(id=empresa.almacen_actual)
                    # Asignar solo el id del almacen
                    initial['almacen'] = almacen.id
                except Almacen.DoesNotExist:
                    print("No se encontró el almacén", empresa.almacen_actual)
                    
            else:
                print("No se asignó almacen_actual")
            
        # Asignar la fecha de hoy
        initial['fecha_movimiento'] = date.today()

        return initial
    
    # este metodo pasa a MovimientoForm (en forms.py) el db_name en kwargs['db_name']
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['db_name'] = get_current_tenant()
        return kwargs

    def get_formset_kwargs(self):
        kwargs = {
            'queryset': DetalleMovimiento.objects.none(),
            'db_name': get_current_tenant()
        }
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        formset = DetalleMovimientoFormSet(**self.get_formset_kwargs())

        # Asignar el valor inicial de 'almacen'
        initial = self.get_initial()  # Llamamos a get_initial() para obtener los valores iniciales del formulario
        form.initial = initial  # Asignamos esos valores iniciales al formulario
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        db_name= get_current_tenant()
        form = self.get_form()
        formset = DetalleMovimientoFormSet(
            request.POST,
            **self.get_formset_kwargs()
        )

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        db_name= get_current_tenant()
        referencia = form.cleaned_data.get('referencia')
        if referencia:
            referencia_formateada = str(referencia).zfill(7)
            form.instance.referencia = referencia_formateada

        form.instance.usuario = self.request.user.username
        # Asignar move_s leyendo de la clave_movimiento
        clave_movimiento = form.cleaned_data.get('clave_movimiento')
        if clave_movimiento:
            form.instance.move_s = clave_movimiento.tipo 

        self.object = form.save(using=db_name)

        # Guardar el formset
        formset.instance = self.object
        formset.save(using=db_name)

        return redirect('inv:movimiento_list')

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})

class MovimientoUpdateView(TenantRequiredMixin, UpdateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inv/movimiento_form.html'
    success_url = reverse_lazy('inv:movimiento_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['referencia'].widget.attrs['readonly'] = True
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        db_name= get_current_tenant()
        if self.request.POST:
            data['formset'] = DetalleMovimientoFormSet(
                self.request.POST,
                instance=self.object,
                queryset=DetalleMovimiento.objects.using(db_name).filter(referencia=self.object),
                prefix='detalles'
            )
        else:
            data['formset'] = DetalleMovimientoFormSet(
                instance=self.object, 
                queryset=DetalleMovimiento.objects.using(db_name).filter(referencia=self.object),
                prefix='detalles'
        )
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        db_name = get_current_tenant()
        if formset.is_valid():
            self.object = form.save(using=db_name)
            formset.instance = self.object
            formset.save(using=db_name)
            return super().form_valid(form)
        else:
            # Añadir depuración de errores en formset
            return self.form_invalid(form)

# DETALLE DE MOVIMIENTO
class MovimientoDetailView(TenantRequiredMixin, DetailView):
    model = Movimiento
    template_name = 'inv/movimiento_detail.html'
    context_object_name = 'movimiento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_name = get_current_tenant()
        context['detalles'] = DetalleMovimiento.objects.using(db_name).filter(referencia=self.object)
        return context

class MovimientoDeleteView(TenantRequiredMixin, DeleteView):
    model = Movimiento
    template_name = 'inv/movimiento_confirm_delete.html'
    success_url = reverse_lazy('inv:movimiento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_name = get_current_tenant()
        context['detalles'] = self.object.detalles.using(db_name).all()
        return context

    def get_queryset(self):
        db_name = get_current_tenant()
        return Movimiento.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        self.object = self.get_object()

        # Eliminar detalles explícitamente
        self.object.detallemovimiento_set.using(db_name).all().delete()

        # Eliminar Encabezado - MOvimiento
        self.object.delete(using=db_name)

        return super().delete(request, *args, **kwargs)

@login_required
@tenant_required
def verificar_movimiento(request):
    clave_movimiento_id = request.GET.get('clave_movimiento')
    referencia = request.GET.get('referencia')

    try: 
        db_name = get_current_tenant()
        movimiento = Movimiento.objects.using(db_name).get(clave_movimiento_id=clave_movimiento_id, referencia=referencia)
        return JsonResponse({'existe': True, 'id': movimiento.id})
    except Movimiento.DoesNotExist:
        return JsonResponse({'existe': False})

@login_required
@tenant_required
def obtener_costo_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        db_name = get_current_tenant()
        producto = Producto.objects.using(db_name).get(pk=producto_id) 
        return JsonResponse({'costo_reposicion': str(producto.costo_reposicion)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@login_required
@tenant_required
def obtener_paridad_moneda(request):
    moneda_id = request.GET.get('moneda_id')
    try:
        db_name = get_current_tenant()
        moneda = Moneda.objects.using(db_name).get(pk=moneda_id)
        return JsonResponse({'paridad': str(moneda.paridad)})
    except Moneda.DoesNotExist:
        return JsonResponse({'error': 'Moneda no encontrada'}, status=404)

# CRUD REMISIONES ==================
from decimal import Decimal

class RemisionBaseView:
    def procesar_formset(self, formset, remision):
        monto_total = 0
        db_name = get_current_tenant()
        remision.detalles.using(db_name).all().delete()

        for detalle_form in formset:
            if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                cd = detalle_form.cleaned_data
                cantidad = cd['cantidad']
                precio = cd['precio']
                descuento = cd['descuento']
                subtotal = (cantidad * precio) - descuento

                DetalleRemision.objects.using(db_name).create(
                    numero_remision=remision,
                    producto=cd['producto'],
                    cantidad=cantidad,
                    precio=precio,
                    descuento=descuento,
                    subtotal=subtotal,
                    tasa_iva=cd.get('tasa_iva', Decimal('0.00')),
                    tasa_ieps=cd.get('tasa_ieps', Decimal('0.00')),
                    iva_producto=cd.get('iva_producto', Decimal('0.00')),
                    ieps_producto=cd.get('ieps_producto', Decimal('0.00')),
                    tasa_retencion_iva=cd.get('tasa_retencion_iva', Decimal('0.00')),
                    tasa_retencion_isr=cd.get('tasa_retencion_isr', Decimal('0.00')),
                    retencion_iva=cd.get('retencion_iva', Decimal('0.00')),
                    retencion_isr=cd.get('retencion_isr', Decimal('0.00')),
                )

                monto_total += subtotal

        remision.monto_total = monto_total
        remision.save(using=db_name)

class RemisionListView(TenantRequiredMixin, ListView):
    model = Remision
    template_name = 'inv/remision_list.html'
    context_object_name = 'remisiones'
    ordering = ['-fecha_remision', '-clave_movimiento', '-numero_remision']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

from decimal import Decimal
class RemisionCreateView(TenantRequiredMixin, RemisionBaseView, CreateView):
    model = Remision
    form_class = RemisionForm
    template_name = 'inv/remision_form.html'

    def get_initial(self):
        initial = super().get_initial()
        db_name = get_current_tenant()
        empresa = self.empresa

        if empresa and empresa.almacen_actual:
            try:
                almacen = Almacen.objects.using(db_name).get(id=empresa.almacen_actual)
                initial['almacen'] = almacen.id
            except Almacen.DoesNotExist:
                print("No se encontró el almacén", empresa.almacen_actual)

        initial['fecha_remision'] = date.today()
        return initial

    def get(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        form = self.form_class(initial=self.get_initial())
        formset = DetalleRemisionFormSet(
            queryset=DetalleRemision.objects.using(db_name).none(), 
            prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        db_name = get_current_tenant()
        form = self.form_class(request.POST or None, db_name=db_name)
        
        formset = DetalleRemisionFormSet(
            request.POST,
            queryset=DetalleRemision.objects.using(db_name).none(),
            prefix='detalles'
        )
        
        if form.is_valid() and formset.is_valid():
            db_name = get_current_tenant()
            self.object = form.save(commit=False)
            self.object.usuario = self.request.user.username
            self.object.numero_factura = '0'
            self.object.status = 'R'
            numero_remision = form.cleaned_data.get('numero_remision')

            if numero_remision:
                self.object.numero_remision = str(numero_remision).zfill(7)

            self.object.save(using=db_name)

            # Aquí se usa la lógica compartida
            self.procesar_formset(formset, self.object)

            # return redirect('inv:remision_list')
            return redirect('inv:remision_update', pk=self.object.pk)

        return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})
    
class RemisionUpdateView(TenantRequiredMixin, RemisionBaseView, UpdateView):
    model = Remision
    form_class = RemisionForm
    template_name = 'inv/remision_form.html'
    success_url = reverse_lazy('inv:remision_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        db_name = get_current_tenant()
        form = self.form_class(instance=self.object)
        formset = DetalleRemisionFormSet(
            instance=self.object,
            queryset=DetalleRemision.objects.using(db_name).filter(numero_remision=self.object),
            prefix='detalles'
        )

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        db_name = get_current_tenant()
        form = self.form_class(request.POST or None, db_name=db_name)
        formset = DetalleRemisionFormSet(
            request.POST,
            instance=self.object,
            queryset=DetalleRemision.objects.using(db_name).filter(numero_remision=self.object),
            prefix='detalles'
        )

        if form.is_valid() and formset.is_valid():
            self.object = form.save(using=db_name)
            self.procesar_formset(formset, self.object)
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['numero_remision'].widget.attrs['readonly'] = True
        return form

# DETALLE DE MOVIMIENTO DE REMISIONES
class RemisionDetailView(TenantRequiredMixin, DetailView):
    model = Remision
    template_name = 'inv/remision_detail.html'
    context_object_name = 'remision'

    def get_context_data(self, **kwargs):
        db_name = get_current_tenant()
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleRemision.objects.using(db_name).filter(numero_remision=self.object)
        return context

class RemisionDeleteView(TenantRequiredMixin, DeleteView):
    model = Remision
    template_name = 'inv/remision_confirm_delete.html'
    success_url = reverse_lazy('inv:remision_list')

    def get_context_data(self, **kwargs):
        db_name = get_current_tenant()
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.using(db_name).all()
        return context

    def get_queryset(self):
        db_name = get_current_tenant()
        return Remision.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        self.object = self.get_object()

        # Eliminar detalles explícitamente
        self.object.detalleremision_set.using(db_name).all().delete()

        # Eliminar Encabezado - MOvimiento
        self.object.delete(using=db_name)

        return super().delete(request, *args, **kwargs)

@login_required
@tenant_required
def verificar_remision(request):
    clave_movimiento_id = request.GET.get('clave_movimiento')
    numero_remision = request.GET.get('numero_remision')
    
    try:
        db_name = get_current_tenant()
        remision = Remision.objects.using(db_name).get(clave_movimiento_id=clave_movimiento_id, numero_remision=numero_remision)
        return JsonResponse({'existe': True, 'id': remision.id})
    except Remision.DoesNotExist:
        return JsonResponse({'existe': False})

@login_required
@tenant_required
def obtener_precio_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        db_name = get_current_tenant()
        producto = Producto.objects.using(db_name).get(pk=producto_id)
        aplica_iva = 0
        aplica_ieps = 0
        if producto.aplica_iva:
            aplica_iva = 1
        if producto.aplica_ieps:
            aplica_ieps = 1
        return JsonResponse({
            'precio1': str(producto.precio1),
            'aplica_iva': aplica_iva,
            'aplica_ieps': aplica_ieps,
            'clave_prod_serv': producto.clave_sat,
            'clave_unidad': producto.unidad_medida.unidad_medida,
            'descripcion' : producto.nombre,
            })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@login_required
@tenant_required
def obtener_ultimo_numero_remision(request):
    clave = request.GET.get('clave')
    if clave:
        db_name = get_current_tenant()
        ultima = Remision.objects.using(db_name).filter(clave_movimiento=clave).order_by('-numero_remision').first()
        if ultima and ultima.numero_remision.isdigit():
            siguiente = str(int(ultima.numero_remision) + 1).zfill(7)
        else:
            siguiente = "0000001"
        return JsonResponse({'numero_remision': siguiente})
    return JsonResponse({'numero_remision': '0000001'})

@login_required
@tenant_required
def obtener_ultimo_movimiento(request):
    clave = request.GET.get('clave')
    print("CLAVE:", clave)
    if clave:
        db_name = get_current_tenant()
        ultima = Movimiento.objects.using(db_name).filter(clave_movimiento=clave).order_by('-referencia').first()
        print("DENTRO DE IF DE OBTENER_ULTIMO_MOVIMIENTO")
        if ultima and ultima.referencia.isdigit():
            siguiente = str(int(ultima.referencia) + 1).zfill(7)
        else:

            siguiente = "0000001"
        return JsonResponse({'referencia': siguiente})
    return JsonResponse({'referencia': '0000001'})

@login_required
@tenant_required
def obtener_ultima_compra(request):
    clave = request.GET.get('clave')
    
    if clave:
        db_name = get_current_tenant()
        ultima = Compra.objects.using(db_name).filter(clave_movimiento=clave).order_by('-referencia').first()
        if ultima and ultima.referencia.isdigit():
            siguiente = str(int(ultima.referencia) + 1).zfill(7)
        else:
            siguiente = "0000001"
        return JsonResponse({'referencia': siguiente})
    return JsonResponse({'referencia': '0000001'})

@login_required
@tenant_required
def obtener_ultimo_vendedor(request):
    db_name = get_current_tenant()
    ultimo = Vendedor.objects.using(db_name).all().order_by('-vendedor').first()
    if ultimo:
        siguiente = str(int(ultimo.vendedor) + 1).zfill(3)
    else:
        siguiente = "001"
    return JsonResponse({'vendedor': siguiente})


# CONSULTAS
# REMISIONES POR FECHA
from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

@login_required
@tenant_required
def remisiones_por_dia(request):
    db_name = get_current_tenant()
    almacenes = Almacen.objects.using(db_name).all()
    resultados = []
    total_general = 0
    almacen = None
    fecha_ini = fecha_fin = None

    if request.GET.get('almacen') and request.GET.get('fecha_ini') and request.GET.get('fecha_fin'):
        almacen_id = request.GET['almacen']
        fecha_ini = request.GET['fecha_ini']
        fecha_fin = request.GET['fecha_fin']

        almacen = Almacen.objects.using(db_name).get(id=almacen_id)

        resultados = DetalleRemision.objects.using(db_name).filter(
            numero_remision__almacen=almacen,
            numero_remision__fecha_remision__range=[fecha_ini, fecha_fin]
        ).select_related('producto', 'numero_remision').annotate(
            total=ExpressionWrapper(
                F('cantidad') * F('precio') - F('descuento'),
                output_field=DecimalField()
            )
        ).order_by('numero_remision__fecha_remision', 'numero_remision__numero_remision', 'id')

        total_general = resultados.aggregate(gran_total=Sum('total'))['gran_total'] or 0

    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None
 
    return render(request, 'inv/reportes/remisiones_por_dia.html', {
        'almacenes': almacenes,
        'resultados': resultados,
        'almacen_seleccionado': almacen,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
        'fecha_actual': date.today(),
        'total_general': total_general,
    })

@login_required
@tenant_required
def buscar_remisiones_por_dia(request):
    db_name = get_current_tenant()
    almacenes = Almacen.objects.using(db_name).all()
    return render(request, 'inv/reportes/remisiones_por_dia_buscar.html', {'almacenes': almacenes})

@login_required
@tenant_required
def remisiones_por_cliente(request):
    total_general = 0
    cliente = None
    fecha_ini = fecha_fin = None

    cliente_id = request.GET.get('cliente_id')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')
    
    db_name = get_current_tenant()
    cliente = Cliente.objects.using(db_name).get(pk=cliente_id)
    
    remisiones = Remision.objects.using(db_name).filter(cliente_id=cliente_id,
        fecha_remision__range=[fecha_ini, fecha_fin]
        ).order_by('fecha_remision','numero_remision') 

    detalles = DetalleRemision.objects.using(db_name).filter(numero_remision__in=remisiones
                                              ).select_related('numero_remision','producto'
                                              ).order_by('numero_remision__fecha_remision', 'numero_remision__numero_remision', 'id')

    # Calcula el total general
    total_general = detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None
    
    contexto = {
        'cliente': cliente,
        'remisiones': remisiones,
        'detalles': detalles,
        'total_general': total_general,
        'fecha_actual': localtime(now()).date(),
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
    }

    return render(request, 'inv/reportes/remisiones_por_cliente.html', contexto)

@login_required
@tenant_required
def buscar_remisiones_por_cliente(request):
    db_name = get_current_tenant()
    clientes = Cliente.objects.using(db_name).all()
    return render(request, 'inv/reportes/remisiones_por_cliente_buscar.html', {'clientes': clientes})

@login_required
@tenant_required
def remisiones_por_producto(request):
    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    db_name = get_current_tenant()
    producto = Producto.objects.using(db_name).get(pk=producto_id)

    # saca las remisiones a partir del detalle
    remisiones = Remision.objects.using(db_name).filter(
        detalles__producto_id=producto_id,  # este detalles es el related_names definido en la Tabla DetalleRemision
        fecha_remision__range=[fecha_ini, fecha_fin]
    ).distinct().order_by('fecha_remision', 'numero_remision')
    
    detalles = DetalleRemision.objects.using(db_name).filter(
        numero_remision__in=remisiones,
        producto_id=producto_id
    ).select_related('numero_remision', 'producto'
    ).order_by('numero_remision__fecha_remision', 'numero_remision__numero_remision', 'id')
    
    total_general = detalles.aggregate(total=Sum('subtotal'))['total'] or 0

    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None

    contexto = {
        'producto': producto,
        'remisiones': remisiones,
        'resultados': detalles,
        'total_general': total_general,
        'fecha_actual': localtime(now()).date(),
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
    }

    return render(request, 'inv/reportes/remisiones_por_producto.html', contexto)

@login_required
@tenant_required
def buscar_remisiones_por_producto(request):
    db_name = get_current_tenant()
    productos = Producto.objects.using(db_name).all()

    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto_seleccionado = Producto.objects.using(db_name).filter(id=producto_id).first() if producto_id else None

    contexto = {
        'productos': productos,
        'producto_seleccionado': producto_seleccionado,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'inv/reportes/remisiones_por_producto_buscar.html', contexto)

# VISTAS PARA CONSULTA DE MOVIMIENTOS TOTALES POR PRODUCTO: MOVIMIENTOS Y REMISIONES
# SE UTILIZA EN LA OPCION DE CONSULTAR "MOVIMIENTOS POR PRODUCTO"
@login_required
@tenant_required
def buscar_movimientos_por_producto_totales(request):
    db_name = get_current_tenant()
    productos = Producto.objects.using(db_name).all()
    return render(request, 'inv/reportes/movimientos_por_producto_buscar.html', {
        'productos': productos
    })

from django.db.models import F, Value, CharField
from django.db.models.functions import Coalesce
# OPCION CONSULTAR "MOVIMIENTOS POR PRODUCTO"
@login_required
@tenant_required
def movimientos_por_producto_totales(request):
    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    db_name = get_current_tenant()
    producto = Producto.objects.using(db_name).get(pk=producto_id)

    # Movimientos
    movimientos = DetalleMovimiento.objects.using(db_name).filter(
        producto_id=producto_id,
        referencia__fecha_movimiento__range=[fecha_ini, fecha_fin]
    ).annotate(
        fecha=F('referencia__fecha_movimiento'),
        tipo=F('referencia__move_s'),
        clave=F('referencia__clave_movimiento__clave_movimiento'),
        nombre_mov=F('referencia__clave_movimiento__nombre'),
        ref=F('referencia__referencia'),
        cantidad_entrada=Case(
            When(referencia__move_s='E', then=F('cantidad')),
            default=Value(0),
            output_field=DecimalField()
        ),
        cantidad_salida=Case(
            When(referencia__move_s='S', then=F('cantidad')),
            default=Value(0),
            output_field=DecimalField()
        ),
        origen=Value('MOVIMIENTO', output_field=CharField())
    ).values('fecha', 'tipo', 'clave', 'nombre_mov', 'ref','cantidad_entrada', 'cantidad_salida', 'origen')

    # Compras
    compras = DetalleCompra.objects.using(db_name).filter(
        producto_id=producto_id,
        referencia__fecha_compra__range=[fecha_ini, fecha_fin]
    ).annotate(
        fecha=F('referencia__fecha_compra'),
        tipo=Value('E', output_field=CharField()),
        clave=F('referencia__clave_movimiento__clave_movimiento'),
        nombre_mov=F('referencia__clave_movimiento__nombre'),
        ref=F('referencia__referencia'),
        cantidad_entrada=F('cantidad'),
        cantidad_salida=Value(0, output_field=DecimalField()),
        origen=Value('COMPRA', output_field=CharField())
    ).values('fecha', 'tipo', 'clave', 'nombre_mov', 'ref','cantidad_entrada', 'cantidad_salida', 'origen')

    # Remisiones
    remisiones = DetalleRemision.objects.using(db_name).filter(
        producto_id=producto_id,
        numero_remision__fecha_remision__range=[fecha_ini, fecha_fin],
        numero_remision__status__in=['R', 'F']  # Solo remisiones válidas
    ).annotate(
        fecha=F('numero_remision__fecha_remision'),
        tipo=Value('S', output_field=CharField()),
        clave=F('numero_remision__clave_movimiento__clave_movimiento'),
        nombre_mov=F('numero_remision__clave_movimiento__nombre'),
        ref=F('numero_remision__numero_remision'),
        cantidad_entrada=Value(0, output_field=DecimalField()),
        cantidad_salida=F('cantidad'),
        origen=Value('REMISION', output_field=CharField())
    ).values('fecha', 'tipo', 'clave', 'nombre_mov', 'ref','cantidad_entrada', 'cantidad_salida', 'origen')

    # Unir y ordenar
    resultados = list(movimientos.union(compras).union(remisiones).order_by('fecha'))
    
    total_entrada = sum(item['cantidad_entrada'] for item in resultados)
    total_salida = sum(item['cantidad_salida'] for item in resultados)
    
    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None

    contexto = {
        'producto': producto,
        'resultados': resultados,
        'fecha_actual': localtime(now()).date(),
        'total_entrada': total_entrada,
        'total_salida': total_salida,
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
    }
    return render(request, 'inv/reportes/movimientos_por_producto.html', contexto)

# MOVIMIENTOS POR CLAVE DE MOVIMIENTO
@login_required
@tenant_required
def buscar_movimientos_por_clave(request):
    db_name = get_current_tenant()
    claves = ClaveMovimiento.objects.using(db_name).all()

    context = {
        'claves': claves,
    }
    return render(request, 'inv/reportes/movimientos_por_clave_buscar.html', context)

@login_required
@tenant_required
def movimientos_por_clave(request):
    clave_id = request.GET.get('clave')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    clave_seleccionado = None
    if clave_id:
        try:
            db_name = get_current_tenant()
            clave_seleccionado = ClaveMovimiento.objects.using(db_name).get(id=clave_id)
        except ClaveMovimiento.DoesNotExist:
            clave_seleccionado = None
    
    movimientos = DetalleMovimiento.objects.using(db_name).filter(
        referencia__clave_movimiento_id=clave_id,
        referencia__fecha_movimiento__range=[fecha_ini, fecha_fin]
    ).select_related('referencia', 'producto').annotate(
        fecha=F('referencia__fecha_movimiento'),
        clave=F('referencia__clave_movimiento__clave_movimiento'),
        nombre_mov=F('referencia__clave_movimiento__nombre'),
        move_s=F('referencia__move_s'),
        ref=F('referencia__referencia'),
        sku=F('producto__sku'),
        nombre_producto=F('producto__nombre'),
        cant=F('cantidad'),
    ).values('fecha', 'clave', 'nombre_mov', 'move_s', 'ref', 'sku', 'nombre_producto', 'cant')

    # COMPRAS
    compras = DetalleCompra.objects.using(db_name).filter(
        referencia__clave_movimiento_id=clave_id,
        referencia__fecha_compra__range=[fecha_ini, fecha_fin]
    ).select_related('referencia', 'producto').annotate(
        fecha=F('referencia__fecha_compra'),
        clave=F('referencia__clave_movimiento__clave_movimiento'),
        nombre_mov=F('referencia__clave_movimiento__nombre'),
        move_s=F('referencia__clave_movimiento__tipo'),
        ref=F('referencia__referencia'),
        sku=F('producto__sku'),
        nombre_producto=F('producto__nombre'),
        cant=F('cantidad'),
    ).values('fecha', 'clave', 'nombre_mov', 'move_s', 'ref', 'sku', 'nombre_producto', 'cant')

    # REMISIONES
    remisiones = DetalleRemision.objects.using(db_name).filter(
        numero_remision__clave_movimiento_id=clave_id,
        numero_remision__fecha_remision__range=[fecha_ini, fecha_fin]
    ).select_related('numero_remision', 'producto').annotate(
        fecha=F('numero_remision__fecha_remision'),
        clave=F('numero_remision__clave_movimiento__clave_movimiento'),
        nombre_mov=F('numero_remision__clave_movimiento__nombre'),
        move_s=F('numero_remision__clave_movimiento__tipo'),
        ref=F('numero_remision__numero_remision'),
        sku=F('producto__sku'),
        nombre_producto=F('producto__nombre'),
        cant=F('cantidad'),
    ).values('fecha', 'clave', 'nombre_mov', 'move_s', 'ref', 'sku', 'nombre_producto', 'cant')

    resultados = movimientos.union(compras).union(remisiones).order_by('fecha')

    # resultados = list(movimientos.union(compras).union(remisiones).order_by('fecha'))
    
    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None

    contexto = {
        'resultados': resultados,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
        'fecha_actual': localtime(now()).date(),
        'clave_seleccionado': clave_seleccionado,
    }
    return render(request, 'inv/reportes/movimientos_por_clave.html', contexto)

# FUNCION PARA LLAMAR A calcular_existencia_producto 
from .utils import calcular_existencia_producto
@login_required
@tenant_required
def api_existencia_producto(request):
    producto_id = request.GET.get('producto')
    almacen_id = request.GET.get('almacen')
    fecha_leida = request.GET.get('fecha')

    try:
        db_name = get_current_tenant()
        producto = Producto.objects.using(db_name).get(pk=producto_id)
        almacen = Almacen.objects.using(db_name).get(pk=almacen_id)
        fecha = datetime.strptime(fecha_leida, '%Y-%m-%d').date()

        existencia = calcular_existencia_producto(request,producto, almacen, fecha)
        
        return JsonResponse({'existencia': float(existencia)})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@tenant_required
def buscar_existencia_producto(request):
    db_name = get_current_tenant()
    productos = Producto.objects.using(db_name).all()
    almacenes = Almacen.objects.using(db_name).all()
    contexto = {
        'productos':productos,
        'almacenes':almacenes,
    }
    return render(request, 'inv/reportes/existencia_por_producto_buscar.html', contexto )

# Imprime los movimientos desde el saldo inicial 
from decimal import Decimal
from datetime import datetime
from django.db.models import F, Value, Case, When, DecimalField, CharField

@login_required
@tenant_required
def imprimir_existencia_producto(request):
    producto = None  
    saldo_inicial = Decimal('0.00')
    db_name = get_current_tenant()
    
    if request.method == 'GET':
        producto_id = request.GET.get('producto')
        almacen_id = request.GET.get('almacen')
        fecha_fin = request.GET.get('fecha_fin')

        if producto_id and almacen_id and fecha_fin:
            producto = Producto.objects.using(db_name).get(id=producto_id)
            almacen = Almacen.objects.using(db_name).get(id=almacen_id)
            fecha_leida = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

            saldo = (
                SaldoInicial.objects.using(db_name)
                .filter(producto=producto, almacen=almacen, fecha__lte=fecha_leida)
                .order_by('-fecha')
                .first()
            )

            if not saldo:
                saldo_inicial = Decimal('0.00')
                fecha_ini = '1900-01-01'
                fecha_saldo = None
            else:
                saldo_inicial = saldo.existencia
                fecha_ini = saldo.fecha
                fecha_saldo = saldo.fecha

            # Movimientos
            movimientos = DetalleMovimiento.objects.using(db_name).filter(
                referencia__almacen_id=almacen_id,
                producto_id=producto_id,
                referencia__fecha_movimiento__range=[fecha_ini, fecha_fin]
            ).annotate(
                fecha=F('referencia__fecha_movimiento'),
                tipo=F('referencia__move_s'),
                clave=F('referencia__clave_movimiento__clave_movimiento'),
                nombre_mov=F('referencia__clave_movimiento__nombre'),
                ref=F('referencia__referencia'),
                cantidad_entrada=Case(
                    When(referencia__move_s='E', then=F('cantidad')),
                    default=Value(0),
                    output_field=DecimalField()
                ),
                cantidad_salida=Case(
                    When(referencia__move_s='S', then=F('cantidad')),
                    default=Value(0),
                    output_field=DecimalField()
                ),
                origen=Value('MOVIMIENTO', output_field=CharField())
            ).values('fecha', 'tipo', 'clave', 'nombre_mov', 'ref', 'cantidad_entrada', 'cantidad_salida', 'origen')

            # Compras
            compras = DetalleCompra.objects.using(db_name).filter(
                referencia__almacen_id=almacen_id,
                producto_id=producto_id,
                referencia__fecha_compra__range=[fecha_ini, fecha_fin]
            ).annotate(
                fecha=F('referencia__fecha_compra'),
                tipo=Value('E', output_field=CharField()),
                clave=F('referencia__clave_movimiento__clave_movimiento'),
                nombre_mov=F('referencia__clave_movimiento__nombre'),
                ref=F('referencia__referencia'),
                cantidad_entrada=F('cantidad'),
                cantidad_salida=Value(0, output_field=DecimalField()),
                origen=Value('COMPRA', output_field=CharField())
            ).values('fecha', 'tipo', 'clave', 'nombre_mov', 'ref', 'cantidad_entrada', 'cantidad_salida', 'origen')

            # Remisiones
            remisiones = DetalleRemision.objects.using(db_name).filter(
                numero_remision__almacen_id=almacen_id,
                producto_id=producto_id,
                numero_remision__fecha_remision__range=[fecha_ini, fecha_fin],
                numero_remision__status__in=['R', 'F']
            ).annotate(
                fecha=F('numero_remision__fecha_remision'),
                tipo=Value('S', output_field=CharField()),
                clave=F('numero_remision__clave_movimiento__clave_movimiento'),
                nombre_mov=F('numero_remision__clave_movimiento__nombre'),
                ref=F('numero_remision__numero_remision'),
                cantidad_entrada=Value(0, output_field=DecimalField()),
                cantidad_salida=F('cantidad'),
                origen=Value('REMISION', output_field=CharField())
            ).values('fecha', 'tipo', 'clave', 'nombre_mov', 'ref', 'cantidad_entrada', 'cantidad_salida', 'origen')

            resultados = list(movimientos.union(compras).union(remisiones).order_by('fecha'))

            total_entrada = sum(item['cantidad_entrada'] for item in resultados)
            total_salida = sum(item['cantidad_salida'] for item in resultados)
            existencia = saldo_inicial + total_entrada - total_salida

            # Convertir fechas
            fecha_ini_dt = datetime.strptime(str(fecha_ini), '%Y-%m-%d').date()
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

            contexto = {
                'producto': producto,
                'resultados': resultados,
                'fecha_actual': localtime(now()).date(),
                'total_entrada': total_entrada,
                'total_salida': total_salida,
                'fecha_ini': fecha_ini_dt,
                'fecha_fin': fecha_fin_dt,
                'saldo_inicial': saldo_inicial,
                'existencia' : existencia,
                'fecha_saldo' : fecha_saldo,
            }
        else:
            contexto = {
                'producto': producto,
                'resultados': {},
                'fecha_actual': localtime(now()).date(),
                'total_entrada': 0,
                'total_salida': 0,
                'fecha_ini': None,
                'fecha_fin': None,
                'saldo_inicial': saldo_inicial,
                'existencia' : existencia,
                'fecha_saldo' : fecha_saldo,
            }

    return render(request, 'inv/reportes/existencia_por_producto.html', contexto)

# CRUD COMPRAS ==================
class CompraBaseView:
    def procesar_formset(self, formset, compra):
        detalles_dict = {}
        monto_total = 0
        
        db_name = get_current_tenant()

        for detalle_form in formset:
            if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                producto = detalle_form.cleaned_data['producto']
                cantidad = detalle_form.cleaned_data['cantidad']
                costo_unit = detalle_form.cleaned_data['costo_unit']
                descuento = detalle_form.cleaned_data.get('descuento', 0)

                subtotal = (cantidad * costo_unit) - descuento

                if producto in detalles_dict:
                    detalles_dict[producto]['cantidad'] += cantidad
                    detalles_dict[producto]['descuento'] += descuento
                    detalles_dict[producto]['subtotal'] += subtotal
                else:
                    detalles_dict[producto] = {
                        'producto': producto,
                        'cantidad': cantidad,
                        'costo_unit': costo_unit,
                        'descuento': descuento,
                        'subtotal': subtotal,
                    }

        compra.detalles.using(db_name).all().delete()

        for detalle in detalles_dict.values():
            DetalleCompra.objects.using(db_name).create(
                referencia=compra,
                producto=detalle['producto'],
                cantidad=detalle['cantidad'],
                costo_unit=detalle['costo_unit'],
                descuento=detalle['descuento'],
                subtotal=detalle['subtotal'],
            )
            # Actualizar el costo de reposición del producto
            producto = detalle['producto']
            producto.costo_reposicion = detalle['costo_unit']
            producto.save(using=db_name)

            monto_total += detalle['subtotal']

        compra.monto_total = monto_total
        compra.save(using=db_name) 

class CompraListView(TenantRequiredMixin, ListView):
    model = Compra
    template_name = 'inv/compra_list.html'
    context_object_name = 'compras'
    ordering = ['-fecha_compra', '-clave_movimiento', '-referencia']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

    def get_queryset(self):
        db_name = get_current_tenant()
        return Empresa.objects.using(db_name).all()

from decimal import Decimal
class CompraCreateView(TenantRequiredMixin, CompraBaseView, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'inv/compra_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = self.empresa
        
        db_name = get_current_tenant()

        if empresa and empresa.almacen_actual:
            try:
                almacen = Almacen.objects.using(db_name).get(id=empresa.almacen_actual)
                moneda = Moneda.objects.using(db_name).all()
                initial['almacen'] = almacen.id
            except Almacen.DoesNotExist:
                print("No se encontró el almacén", empresa.almacen_actual)
        
        if empresa.clave_compras:
            try:
                clave_compras = ClaveMovimiento.objects.using(db_name).get(clave_movimiento=empresa.clave_compras)
                initial['clave_movimiento'] = clave_compras.id
            except ClaveMovimiento.DoesNotExist:
                pass

        initial['fecha_compra'] = localtime(now()).date().isoformat()
        return initial

    def get(self, request, *args, **kwargs):
        db_name = get_current_tenant()

        form = self.form_class(initial=self.get_initial())
        formset = DetalleCompraFormSet(queryset=DetalleCompra.using(db_name).objects.none(), 
                    prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        form = self.form_class(request.POST or None, db_name=db_name)
        formset = DetalleCompraFormSet(
            request.POST,
            queryset=DetalleCompra.objects.using(db_name).none(),
            prefix='detalles'
        )

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.usuario = self.request.user.username
            self.object.pedido = ''
            self.object.fecha_pagada = '1900-01-01'
            self.object.descuento_pp = 0
            referencia = form.cleaned_data.get('referencia')

            if referencia:
                self.object.referencia = str(referencia).zfill(7)

            self.object.save(using=db_name)
            
            # Aquí se usa la lógica compartida
            self.procesar_formset(formset, self.object)

            return redirect('inv:compra_list')

        return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        print("Errores del form principal:", form.errors)
        print("Errores del formset:")
        for i, f in enumerate(formset):
            if f.errors:
                print(f"Errores en el formulario #{i}:", f.errors.as_data())

        return render(self.request, self.template_name, {'form': form, 'formset': formset})
    
class CompraUpdateView(TenantRequiredMixin, CompraBaseView, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'inv/compra_form.html'
    success_url = reverse_lazy('inv:compra_list')

    def get(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        formset = DetalleCompraFormSet(
            instance=self.object,
            queryset=DetalleCompra.objects.using(db_name).filter(referencia=self.object),
            prefix='detalles'
        )

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        self.object = self.get_object()
        form = self.form_class(request.POST or None, db_name=db_name)
        formset = DetalleCompraFormSet(
            request.POST,
            instance=self.object,
            queryset=DetalleCompra.objects.using(db_name).filter(referencia=self.object),
            prefix='detalles'
        )

        if form.is_valid() and formset.is_valid():
            self.object = form.save(using=db_name)
            self.procesar_formset(formset, self.object)
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['referencia'].widget.attrs['readonly'] = True
        return form

# DETALLE DE MOVIMIENTO DE COMPRAS
class CompraDetailView(TenantRequiredMixin, DetailView):
    model = Compra
    template_name = 'inv/compra_detail.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        db_name = get_current_tenant()
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleCompra.objects.using(db_name).filter(referencia=self.object)
        return context

class CompraDeleteView(TenantRequiredMixin, DeleteView):
    model = Compra
    template_name = 'inv/compra_confirm_delete.html'
    success_url = reverse_lazy('inv:compra_list')

    def get_context_data(self, **kwargs):
        db_name = get_current_tenant()
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.using(db_name).all()
        return context

    def get_queryset(self):
        db_name = get_current_tenant()
        return Compra.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        db_name = get_current_tenant()
        self.object = self.get_object()

        # Eliminar detalles explícitamente
        self.object.detallecompra_set.using(db_name).all().delete()

        # Eliminar Encabezado - MOvimiento
        self.object.delete(using=db_name)

        return super().delete(request, *args, **kwargs)

@login_required
@tenant_required
def verificar_compra(request):
    clave_movimiento_id = request.GET.get('clave_movimiento')
    referencia = request.GET.get('referencia')

    try:
        db_name = get_current_tenant()
        compra = Compra.objects.using(db_name).get(clave_movimiento_id=clave_movimiento_id, referencia=referencia)
        return JsonResponse({'existe': True, 'id': referencia.id})
    except Compra.DoesNotExist:
        return JsonResponse({'existe': False})

@login_required
@tenant_required
def obtener_dias_plazo(request):
    proveedor_id = request.GET.get('proveedor_id')
    try:
        db_name = get_current_tenant()
        proveedor = Proveedor.objects.using(db_name).get(pk=proveedor_id)
        return JsonResponse({'dias_plazo': str(proveedor.dias_plazo)})
    except Proveedor.DoesNotExist:
        return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

# CONSULTA DE COMPRAS POR DIA    
@login_required
@tenant_required
def compras_por_dia(request):
    db_name = get_current_tenant()
    almacenes = Almacen.objects.using(db_name).all()
    resultados = []
    total_general = 0
    almacen = None
    fecha_ini = fecha_fin = None

    if request.GET.get('almacen') and request.GET.get('fecha_ini') and request.GET.get('fecha_fin'):
        almacen_id = request.GET['almacen']
        fecha_ini = request.GET['fecha_ini']
        fecha_fin = request.GET['fecha_fin']

        almacen = Almacen.objects.using(db_name).get(id=almacen_id)

        resultados = DetalleCompra.objects.using(db_name).filter(
            referencia__almacen=almacen,
            referencia__fecha_compra__range=[fecha_ini, fecha_fin]
        ).select_related('producto', 'referencia').annotate(
            total=ExpressionWrapper(
                F('cantidad') * F('costo_unit') - F('descuento'),
                output_field=DecimalField()
            )
        ).order_by('referencia__fecha_compra', 'referencia__referencia', 'id')

        total_general = resultados.aggregate(gran_total=Sum('total'))['gran_total'] or 0

    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None
 
    return render(request, 'inv/reportes/compras_por_dia.html', {
        'almacenes': almacenes,
        'resultados': resultados,
        'almacen_seleccionado': almacen,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
        'fecha_actual': date.today(),
        'total_general': total_general,
    })

@login_required
@tenant_required
def buscar_compras_por_dia(request):
    db_name = get_current_tenant()
    almacenes = Almacen.objects.using(db_name).all()
    return render(request, 'inv/reportes/compras_por_dia_buscar.html', {'almacenes': almacenes})

#CONSULTAR COMPRAS POR PRODUCTO
@login_required
@tenant_required
def compras_por_producto(request):
    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    db_name = get_current_tenant()
    producto = Producto.objects.using(db_name).get(pk=producto_id)

    # saca las compras a partir del detalle
    compras = Compra.objects.using(db_name).filter(
        detalles__producto_id=producto_id,  # este detalles es el related_names definido en la Tabla DetalleCompra
        fecha_compra__range=[fecha_ini, fecha_fin]
    ).distinct().order_by('fecha_compra', 'referencia')
    
    detalles = DetalleCompra.objects.using(db_name).filter(
        referencia__in=compras,
        producto_id=producto_id
    ).select_related('referencia', 'producto'
    ).order_by('referencia__fecha_compra', 'referencia__referencia', 'id')
    
    total_general = detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    total_cantidad = detalles.aggregate(total_qty=Sum('cantidad'))['total_qty'] or 0

    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None

    contexto = {
        'producto': producto,
        'compras': compras,
        'resultados': detalles,
        'total_general': total_general,
        'total_cantidad': total_cantidad,
        'fecha_actual': localtime(now()).date(),
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
    }

    return render(request, 'inv/reportes/compras_por_producto.html', contexto)

@login_required
@tenant_required
def buscar_compras_por_producto(request):
    db_name = get_current_tenant()
    productos = Producto.objects.using(db_name).all()

    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto_seleccionado = Producto.objects.using(db_name).filter(id=producto_id).first() if producto_id else None

    contexto = {
        'productos': productos,
        'producto_seleccionado': producto_seleccionado,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'inv/reportes/compras_por_producto_buscar.html', contexto)

#CONSULTAR COMPRAS POR PROVEEDOR
@login_required
@tenant_required
def compras_por_proveedor(request):
    total_general = 0
    total_cantidad = 0
    proveedor = None
    fecha_ini = fecha_fin = None
    
    proveedor_id = request.GET.get('proveedor_id')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    db_name = get_current_tenant()
    proveedor = Proveedor.objects.using(db_name).get(pk=proveedor_id)
    
    compras = Compra.objects.using(db_name).filter(
        proveedor_id=proveedor_id,
        fecha_compra__range=[fecha_ini, fecha_fin]
        ).order_by('fecha_compra','referencia') 

    detalles = DetalleCompra.objects.using(db_name).filter(referencia__in=compras
                                              ).select_related('referencia','producto'
                                              ).order_by('referencia__fecha_compra', 'referencia__referencia', 'id')

    # Calcula el total general
    total_general = detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    total_cantidad = detalles.aggregate(total_qty=Sum('cantidad'))['total_qty'] or 0
    
    # pasa fechas de string a fecha
    fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d').date() if fecha_ini else None
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else None
    
    contexto = {
        'proveedor': proveedor,
        'compras': compras,
        'detalles': detalles,
        'total_general': total_general,
        'total_cantidad': total_cantidad,
        'fecha_actual': localtime(now()).date(),
        'fecha_ini' : fecha_ini,
        'fecha_fin' : fecha_fin,
    }

    return render(request, 'inv/reportes/compras_por_proveedor.html', contexto)

@login_required
@tenant_required
def buscar_compras_por_proveedor(request):
    db_name = get_current_tenant()
    proveedores = Proveedor.objects.using(db_name).all()
    return render(request, 'inv/reportes/compras_por_proveedor_buscar.html', {'proveedores': proveedores})

# CRUD INFORMACION GENERAL - SOLO LIST y UPDATE 
class EmpresaListView(TenantRequiredMixin, ListView):
    model = Empresa
    template_name = 'inv/empresa_list.html'
    context_object_name = 'empresas'

    def get_queryset(self):
        db_name = get_current_tenant()
        return Empresa.objects.using(db_name).all()

class EmpresaCreateView(TenantRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'inv/empresa_form.html'
    success_url = reverse_lazy('inv:empresa_list')

class EmpresaUpdateView(TenantRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'inv/empresa_form.html'
    success_url = reverse_lazy('inv:empresa_list')

    def get_queryset(self):
        db_name = get_current_tenant()
        return Empresa.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name = get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

# CRUD INFORMACION GENERAL - LUGAR DE EXPEDICION 
class EmpresaLugarListView(TenantRequiredMixin, ListView):
    model = Empresa
    template_name = 'inv/empresa_lugarexp_list.html'
    context_object_name = 'empresas'

    def get_queryset(self):
        db_name = get_current_tenant()
        return Empresa.objects.using(db_name).all()

class EmpresaLugarUpdateView(TenantRequiredMixin, UpdateView):
    model = Empresa
    form_class = EmpresaLugarForm
    template_name = 'inv/empresa_lugarexp_form.html'
    success_url = reverse_lazy('inv:empresa_lugarexp_list')

    def get_queryset(self):
        db_name = get_current_tenant()
        return Empresa.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name = get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

# REGISTRO DEL EMISOR DE CFDI
@login_required
@tenant_required
def registrar_emisor_view(request):
    return render(request, "inv/cfdi_registrar_emisor.html")

# VISTA PARA REGISTRA CSD Y ENVIAR AL PAC
# CSD - Certificado de Sello Digital

import base64
import requests

@login_required
@tenant_required
def registrar_csd_view(request):
    if request.method == "POST":
        rfc = request.POST.get("rfc")
        password = request.POST.get("password")
        cer_file = request.FILES.get("cer_archivo")
        key_file = request.FILES.get("key_archivo")

        client_id = settings.PAC_CLIENT_ID
        api_token = settings.PAC_API_TOKEN
        url = f"https://dev.techbythree.com/api/v1/compatibilidad/{client_id}/RegistraEmisor"

        try:
            # Codifica los archivos a base64
            base64_cer = base64.b64encode(cer_file.read()).decode('utf-8')
            base64_key = base64.b64encode(key_file.read()).decode('utf-8')

            # Construye el cuerpo JSON
            payload = {
                "RfcEmisor": rfc,
                "Base64Cer": base64_cer,
                "Base64Key": base64_key,
                "Contrasena": password
            }

            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                # Guarda los archivos localmente y registra en la base de datos
                db_name = get_current_tenant()
                empresa_fiscal = Empresa.objects.using(db_name).first()
                csd = CertificadoCSD.objects.using(db_name).create(
                    empresa=empresa_fiscal,
                    rfc=rfc,
                    cer_archivo=cer_file,
                    key_archivo=key_file,
                    password=password
                )
                messages.success(request, "Emisor registrado correctamente en el PAC.")
            else:
                messages.error(request, f"❌ Error {response.status_code}: {response.text}")

        except Exception as e:
            messages.error(request, f"❌ Excepción: {str(e)}")

        return redirect('inv:cfdi_registrar_emisor')

    return render(request, 'inv/cfdi_registrar_emisor.html')

@login_required
@tenant_required
def obtener_ultimo_producto(request):
    db_name = get_current_tenant()
    ultimo = Producto.objects.using(db_name).all().order_by('-sku').first()
    if ultimo:
        siguiente = str(int(ultimo.sku) + 1).zfill(6)
    else:
        siguiente = "000001"
    return JsonResponse({'producto': siguiente})

@login_required
@tenant_required
def imprimir_remision(request, pk):
    db_name = get_current_tenant()
    remision = get_object_or_404(Remision.objects.using(db_name), pk=pk)
    detalles = DetalleRemision.objects.using(db_name).filter(numero_remision=remision)

    total = 0
    for det in detalles:
        total = total + (det.cantidad * det.precio) - det.descuento

    return render(request, 'inv/remision_print.html', {
        'remision': remision,
        'detalles': detalles,
        'total': total,
    })

@login_required
@tenant_required
def imprimir_movimiento(request, pk):
    db_name = get_current_tenant()
    movimiento = get_object_or_404(Movimiento.objects.using(db_name), pk=pk)
    detalles = DetalleMovimiento.objects.using(db_name).filter(referencia=movimiento)
    total = 0
    for det in detalles:
        total = total + det.cantidad * det.costo_unit

    return render(request, 'inv/movimiento_print.html', {
        'movimiento': movimiento,
        'detalles': detalles,
        'total': total,
    })

@login_required
@tenant_required
def imprimir_compra(request, pk):
    db_name = get_current_tenant()
    compra = get_object_or_404(Compra.objects.using(db_name), pk=pk)
    detalles = DetalleCompra.objects.using(db_name).filter(referencia=compra)

    total = 0
    for det in detalles:
        total = total + (det.cantidad * det.costo_unit) - det.descuento

    return render(request, 'inv/compra_print.html', {
        'compra': compra,
        'detalles': detalles,
        'total': total,
    })
