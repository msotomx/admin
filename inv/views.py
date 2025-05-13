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
    ordering = ['-fecha_movimiento','-clave_movimiento', '-referencia']  # Orden descendente por fecha
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
            referencia_formateada = str(referencia).zfill(7)
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
class RemisionBaseView:
    def procesar_formset(self, formset, remision):
        detalles_dict = {}
        monto_total = 0

        for detalle_form in formset:
            if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                producto = detalle_form.cleaned_data['producto']
                cantidad = detalle_form.cleaned_data['cantidad']
                precio = detalle_form.cleaned_data['precio']
                descuento = detalle_form.cleaned_data.get('descuento', 0)

                subtotal = (cantidad * precio) - descuento

                if producto in detalles_dict:
                    detalles_dict[producto]['cantidad'] += cantidad
                    detalles_dict[producto]['descuento'] += descuento
                    detalles_dict[producto]['subtotal'] += subtotal
                else:
                    detalles_dict[producto] = {
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio': precio,
                        'descuento': descuento,
                        'subtotal': subtotal,
                    }

        remision.detalles.all().delete()

        for detalle in detalles_dict.values():
            DetalleRemision.objects.create(
                numero_remision=remision,
                producto=detalle['producto'],
                cantidad=detalle['cantidad'],
                precio=detalle['precio'],
                descuento=detalle['descuento'],
                subtotal=detalle['subtotal'],
            )
            monto_total += detalle['subtotal']

        remision.monto_total = monto_total
        remision.save()

class RemisionListView(ListView):
    model = Remision
    template_name = 'inv/remision_list.html'
    context_object_name = 'remisiones'
    ordering = ['-fecha_remision', '-clave_movimiento', '-numero_remision']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

from decimal import Decimal
class RemisionCreateView(RemisionBaseView, CreateView):
    model = Remision
    form_class = RemisionForm
    template_name = 'inv/remision_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = getattr(self.request.user, 'empresa', None)

        if empresa and empresa.almacen_actual:
            try:
                almacen = Almacen.objects.get(id=empresa.almacen_actual)
                initial['almacen'] = almacen.id
            except Almacen.DoesNotExist:
                print("No se encontró el almacén", empresa.almacen_actual)

        initial['fecha_remision'] = date.today()
        return initial

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        formset = DetalleRemisionFormSet(queryset=DetalleRemision.objects.none(), prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleRemisionFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.usuario = self.request.user
            self.object.numero_factura = '0'
            self.object.status = 'R'
            numero_remision = form.cleaned_data.get('numero_remision')

            if numero_remision:
                self.object.numero_remision = str(numero_remision).zfill(7)

            self.object.save()

            # Aquí se usa la lógica compartida
            self.procesar_formset(formset, self.object)

            return redirect('inv:remision_list')

        return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})
    
class RemisionUpdateView(RemisionBaseView, UpdateView):
    model = Remision
    form_class = RemisionForm
    template_name = 'inv/remision_form.html'
    success_url = reverse_lazy('inv:remision_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        formset = DetalleRemisionFormSet(instance=self.object,prefix='detalles')

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = DetalleRemisionFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.procesar_formset(formset, self.object)
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['numero_remision'].widget.attrs['readonly'] = True
        return form

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

def obtener_ultimo_numero_remision(request):
    clave = request.GET.get('clave')
    if clave:
        ultima = Remision.objects.filter(clave_movimiento=clave).order_by('-numero_remision').first()
        if ultima and ultima.numero_remision.isdigit():
            siguiente = str(int(ultima.numero_remision) + 1).zfill(7)
        else:
            siguiente = "0000001"
        return JsonResponse({'numero_remision': siguiente})
    return JsonResponse({'numero_remision': '0000001'})

def obtener_ultimo_movimiento(request):
    clave = request.GET.get('clave')
    if clave:
        ultima = Movimiento.objects.filter(clave_movimiento=clave).order_by('-referencia').first()
        if ultima and ultima.referencia.isdigit():
            siguiente = str(int(ultima.referencia) + 1).zfill(7)
        else:
            siguiente = "0000001"
        return JsonResponse({'referencia': siguiente})
    return JsonResponse({'referencia': '0000001'})

# CONSULTAS
# REMISIONES POR FECHA
from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

def remisiones_por_dia(request):
    almacenes = Almacen.objects.all()
    resultados = []
    total_general = 0
    almacen = None
    fecha_ini = fecha_fin = None

    if request.GET.get('almacen') and request.GET.get('fecha_ini') and request.GET.get('fecha_fin'):
        almacen_id = request.GET['almacen']
        fecha_ini = request.GET['fecha_ini']
        fecha_fin = request.GET['fecha_fin']

        almacen = Almacen.objects.get(id=almacen_id)

        resultados = DetalleRemision.objects.filter(
            numero_remision__almacen=almacen,
            numero_remision__fecha_remision__range=[fecha_ini, fecha_fin]
        ).select_related('producto', 'numero_remision').annotate(
            total=ExpressionWrapper(
                F('cantidad') * F('precio') - F('descuento'),
                output_field=DecimalField()
            )
        ).order_by('numero_remision__fecha_remision')

        total_general = resultados.aggregate(gran_total=Sum('total'))['gran_total'] or 0

    return render(request, 'inv/reportes/remisiones_por_dia.html', {
        'almacenes': almacenes,
        'resultados': resultados,
        'almacen_seleccionado': almacen,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
        'fecha_actual': date.today(),
        'total_general': total_general,
    })

from django.shortcuts import render
from django.utils.timezone import now
from cxc.models import Cliente

def remisiones_por_cliente(request):
    #clientes = Cliente.objects.all()
    total_general = 0
    cliente = None
    fecha_ini = fecha_fin = None

    cliente_id = request.GET.get('cliente_id')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    cliente = Cliente.objects.get(pk=cliente_id)
    
    remisiones = Remision.objects.filter(
    cliente_id=cliente_id,
    fecha_remision__range=[fecha_ini, fecha_fin]
    ).order_by('fecha_remision','numero_remision') 

    detalles = DetalleRemision.objects.filter(numero_remision__in=remisiones).select_related('producto','numero_remision')

    # Calcula el total general
    total_general = detalles.aggregate(total=Sum('subtotal'))['total'] or 0

    contexto = {
        'cliente': cliente,
        'remisiones': remisiones,
        'detalles': detalles,
        'total_general': total_general,
        'fecha_actual': now().date(),
    }

    return render(request, 'inv/reportes/remisiones_por_cliente.html', contexto)

def buscar_remisiones_por_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'inv/reportes/remisiones_buscar.html', {'clientes': clientes})
