from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Moneda, Categoria, UnidadMedida, Almacen, ClaveMovimiento, Proveedor
from .models import Producto, Movimiento, DetalleMovimiento, Remision, DetalleRemision
from core.models import Empresa
from .forms import MonedaForm, CategoriaForm, UnidadMedidaForm, AlmacenForm, ClaveMovimientoForm
from .forms import ProveedorForm, ProductoForm, MovimientoForm,  DetalleMovimientoFormSet
from .forms import RemisionForm,  DetalleRemisionFormSet
from datetime import date
from django.http import JsonResponse

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
    ordering = ['-fecha_movimiento']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inv/movimiento_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = getattr(self.request.user, 'empresa', None)
        
        if empresa:
            # Verificar que el almacen_actual está asignado
            if empresa.almacen_actual:
                try:
                    # Buscar el Almacen usando el ID almacen_actual
                    almacen = Almacen.objects.get(id=empresa.almacen_actual)
                    # Asignar solo el id del almacen
                    initial['almacen'] = almacen.id
                except Almacen.DoesNotExist:
                    print("No se encontró el almacén", empresa.almacen_actual)
                    
            else:
                print("No se asignó almacen_actual")
            
        # Asignar la fecha de hoy
        initial['fecha_movimiento'] = date.today()

        return initial
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = DetalleMovimientoFormSet(queryset=DetalleMovimiento.objects.none())  # Inicializa el formset vacío

        # Asignar el valor inicial de 'almacen'
        initial = self.get_initial()  # Llamamos a get_initial() para obtener los valores iniciales del formulario
        form.initial = initial  # Asignamos esos valores iniciales al formulario
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleMovimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        referencia = form.cleaned_data.get('referencia')
        if referencia:
            referencia_formateada = str(referencia).zfill(8)
            form.instance.referencia = referencia_formateada

        form.instance.usuario = self.request.user
        # Asignar move_s leyendo de la clave_movimiento
        clave_movimiento = form.cleaned_data.get('clave_movimiento')
        if clave_movimiento:
            form.instance.move_s = clave_movimiento.tipo 

        self.object = form.save()

        # Guardar el formset
        formset.instance = self.object
        formset.save()

        return redirect('inv:movimiento_list')

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})

class MovimientoUpdateView(UpdateView):
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

def verificar_movimiento(request):
    clave_movimiento_id = request.GET.get('clave_movimiento')
    referencia = request.GET.get('referencia')

    try:
        movimiento = Movimiento.objects.get(clave_movimiento_id=clave_movimiento_id, referencia=referencia)
        return JsonResponse({'existe': True, 'id': movimiento.id})
    except Movimiento.DoesNotExist:
        return JsonResponse({'existe': False})

def obtener_costo_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'costo_reposicion': str(producto.costo_reposicion)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

# CRUD REMISIONES ==================
class RemisionListView(ListView):
    model = Remision
    template_name = 'inv/remision_list.html'
    context_object_name = 'remisiones'
    ordering = ['-fecha_remision', '-numero_remision']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

from decimal import Decimal
class RemisionCreateView(RemisionBaseView, CreateView):
    model = Remision 
    form_class = RemisionForm
    template_name = 'inv/remision_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = getattr(self.request.user, 'empresa', None)
        
        if empresa:
            # Verificar que el almacen_actual está asignado
            if empresa.almacen_actual:
                try:
                    # Buscar el Almacen usando el ID almacen_actual
                    almacen = Almacen.objects.get(id=empresa.almacen_actual)
                    # Asignar solo el id del almacen
                    initial['almacen'] = almacen.id
                except Almacen.DoesNotExist:
                    print("No se encontró el almacén", empresa.almacen_actual)
                    
            else:
                print("No se asignó almacen_actual")
            
        # Asignar la fecha de hoy
        initial['fecha_remision'] = date.today()

        return initial
    
    def get(self, request, *args, **kwargs):
        # Obtener los valores iniciales
        initial = self.get_initial()

        # Crear el formulario con los valores iniciales
        form = self.form_class(initial=initial)

        # Crear el formset vacío para el detalle
        formset = DetalleRemisionFormSet(queryset=DetalleRemision.objects.none(), prefix='detalles')
        
        # Renderizar la plantilla
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleRemisionFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
        
    def form_valid(self, form, formset):
        numero_remision = form.cleaned_data.get('numero_remision')
        if numero_remision:
            numero_remision_formateada = str(numero_remision).zfill(6)
            form.instance.numero_remision = numero_remision_formateada

        clave_movimiento = form.cleaned_data.get('clave_movimiento')
        form.instance.usuario = self.request.user
        form.instance.numero_factura = '0'
        form.instance.status = 'R'
        form.instance.monto_total = 0  # Se actualizará luego

        self.object = form.save()

        for i, form in enumerate(formset.forms):
            print(f"Form #{i}:")
            for field_name, field_value in form.cleaned_data.items():
                print(f"  {field_name}: {field_value}")


        # Consolidar productos duplicados
        # from collections import defaultdict
        detalles_consolidados = {}

        for form_detalle in formset:
            data = form_detalle.cleaned_data
            if not data or data.get('DELETE', False) or not data.get('producto'):
                continue

            producto = data['producto']
            producto_id = producto.id

            cantidad = Decimal(data.get('cantidad') or 0)
            precio = Decimal(data.get('precio') or 0)
            descuento = Decimal(data.get('descuento') or 0)
            subtotal = (cantidad * precio) - descuento

            if producto_id not in detalles_consolidados:
                detalles_consolidados[producto_id] = {
                    'producto': producto,
                    'cantidad': Decimal('0.00'),
                    'precio': precio,
                    'descuento': Decimal('0.00'),
                    'subtotal': Decimal('0.00'),
                }

            detalles_consolidados[producto_id]['cantidad'] += cantidad
            detalles_consolidados[producto_id]['descuento'] += descuento
            detalles_consolidados[producto_id]['subtotal'] += subtotal


        # Guardar los detalles consolidados
        for datos in detalles_consolidados.values():
            DetalleRemision.objects.create(
                numero_remision=self.object,
                producto=datos['producto'],
                cantidad=datos['cantidad'],
                precio=datos['precio'],
                descuento=datos['descuento'],
                subtotal=datos['subtotal'],
            )

        # Actualizar monto_total de la remisión
        self.object.monto_total = sum(d['subtotal'] for d in detalles_consolidados.values())
        self.object.save()

        return redirect('inv:remision_list')

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})

class RemisionUpdateView(UpdateView):
    model = Remision
    form_class = RemisionForm
    template_name = 'inv/remision_form.html'
    success_url = reverse_lazy('inv:remision_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DetalleRemisionFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = DetalleRemisionFormSet(instance=self.object)
        return data
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        formset = DetalleRemisionFormSet(queryset=self.object.detalles.all(), prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['numero_remision'].widget.attrs['readonly'] = True
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DetalleRemisionFormSet(self.request.POST, instance=self.object, prefix='detalles')
        else:
            data['formset'] = DetalleRemisionFormSet(instance=self.object, prefix='detalles')
        return data
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = DetalleRemisionFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            self.procesar_formset(formset, self.object)
            return redirect('remision_list')
        return self.form_invalid(form)
        
# DETALLE DE MOVIMIENTO DE REMISIONES
class RemisionDetailView(DetailView):
    model = Remision
    template_name = 'inv/remision_detail.html'
    context_object_name = 'remision'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleRemision.objects.filter(numero_remision=self.object)
        return context

class RemisionDeleteView(DeleteView):
    model = Remision
    template_name = 'inv/remision_confirm_delete.html'
    success_url = reverse_lazy('inv:remision_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context

def verificar_remision(request):
    clave_movimiento_id = request.GET.get('clave_movimiento')
    numero_remision = request.GET.get('numero_remision')

    try:
        remision = Remision.objects.get(clave_movimiento_id=clave_movimiento_id, numero_remision=numero_remision)
        return JsonResponse({'existe': True, 'id': remision.id})
    except Remision.DoesNotExist:
        return JsonResponse({'existe': False})

def obtener_precio_producto(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'precio1': str(producto.precio1)})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
