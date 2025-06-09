from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum, Q
from django.conf import settings

from .forms import CertificadoCSDForm
from core.models import CertificadoCSD
from services.pac import registrar_emisor_pac
from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Moneda, Categoria, UnidadMedida, Almacen, ClaveMovimiento, Proveedor
from .models import Producto, Movimiento, DetalleMovimiento, Remision, DetalleRemision
from .models import Compra, DetalleCompra
from .models import SaldoInicial
from core.models import Empresa
from cxc.models import Cliente
from core.models import Empresa
from core.models import CertificadoCSD
from .forms import MonedaForm, CategoriaForm, UnidadMedidaForm, AlmacenForm, ClaveMovimientoForm
from .forms import ProveedorForm, ProductoForm, MovimientoForm,  DetalleMovimientoFormSet
from .forms import RemisionForm,  DetalleRemisionFormSet
from .forms import CompraForm,  DetalleCompraFormSet
from .forms import EmpresaForm, EmpresaLugarForm
from datetime import date
from django.http import JsonResponse
from django.db.models import Case, When, Value, F, DecimalField
from datetime import datetime
from django.utils.timezone import now, localtime

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
            })
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

def obtener_ultima_compra(request):
    clave = request.GET.get('clave')
    
    if clave:
        ultima = Compra.objects.filter(clave_movimiento=clave).order_by('-referencia').first()
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

def buscar_remisiones_por_dia(request):
    almacenes = Almacen.objects.all()
    return render(request, 'inv/reportes/remisiones_por_dia_buscar.html', {'almacenes': almacenes})


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

    detalles = DetalleRemision.objects.filter(numero_remision__in=remisiones
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

def buscar_remisiones_por_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'inv/reportes/remisiones_por_cliente_buscar.html', {'clientes': clientes})

def remisiones_por_producto(request):
    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto = Producto.objects.get(pk=producto_id)

    # saca las remisiones a partir del detalle
    remisiones = Remision.objects.filter(
        detalles__producto_id=producto_id,  # este detalles es el related_names definido en la Tabla DetalleRemision
        fecha_remision__range=[fecha_ini, fecha_fin]
    ).distinct().order_by('fecha_remision', 'numero_remision')
    
    detalles = DetalleRemision.objects.filter(
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

def buscar_remisiones_por_producto(request):
    productos = Producto.objects.all()

    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto_seleccionado = Producto.objects.filter(id=producto_id).first() if producto_id else None

    contexto = {
        'productos': productos,
        'producto_seleccionado': producto_seleccionado,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'inv/reportes/remisiones_por_producto_buscar.html', contexto)

# VISTAS PARA CONSULTA DE MOVIMIENTOS TOTALES POR PRODUCTO: MOVIMIENTOS Y REMISIONES
def buscar_movimientos_por_producto_totales(request):
    productos = Producto.objects.all()
    return render(request, 'inv/reportes/movimientos_por_producto_buscar.html', {
        'productos': productos
    })

from django.db.models import F, Value, CharField
from django.db.models.functions import Coalesce

def movimientos_por_producto_totales(request):
    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto = Producto.objects.get(pk=producto_id)

    # Movimientos
    movimientos = DetalleMovimiento.objects.filter(
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
    compras = DetalleCompra.objects.filter(
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
    remisiones = DetalleRemision.objects.filter(
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
def buscar_movimientos_por_clave(request):
    claves = ClaveMovimiento.objects.all()

    context = {
        'claves': claves,
    }
    return render(request, 'inv/reportes/movimientos_por_clave_buscar.html', context)

def movimientos_por_clave(request):
    clave_id = request.GET.get('clave')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    clave_seleccionado = None
    if clave_id:
        try:
            clave_seleccionado = ClaveMovimiento.objects.get(id=clave_id)
        except ClaveMovimiento.DoesNotExist:
            clave_seleccionado = None

    resultados = DetalleMovimiento.objects.filter(
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
    ).order_by('fecha', 'ref')

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

def api_existencia_producto(request):
    producto_id = request.GET.get('producto')
    almacen_id = request.GET.get('almacen')
    fecha_leida = request.GET.get('fecha')

    try:
        producto = Producto.objects.get(pk=producto_id)
        almacen = Almacen.objects.get(pk=almacen_id)
        fecha = datetime.strptime(fecha_leida, '%Y-%m-%d').date()

        existencia = calcular_existencia_producto(producto, almacen, fecha)
        
        return JsonResponse({'existencia': float(existencia)})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def buscar_existencia_producto(request):
    productos = Producto.objects.all()
    almacenes = Almacen.objects.all()
    contexto = {
        'productos':productos,
        'almacenes':almacenes,
    }
    return render(request, 'inv/reportes/existencia_por_producto_buscar.html', contexto )

# Imprime los movimientos desde el saldo inicial 
from decimal import Decimal
from datetime import datetime
from django.db.models import F, Value, Case, When, DecimalField, CharField

def imprimir_existencia_producto(request):
    producto = None  
    saldo_inicial = Decimal('0.00')

    if request.method == 'GET':
        producto_id = request.GET.get('producto')
        almacen_id = request.GET.get('almacen')
        fecha_fin = request.GET.get('fecha_fin')

        if producto_id and almacen_id and fecha_fin:
            producto = Producto.objects.get(id=producto_id)
            almacen = Almacen.objects.get(id=almacen_id)
            fecha_leida = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

            saldo = (
                SaldoInicial.objects
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
            movimientos = DetalleMovimiento.objects.filter(
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
            compras = DetalleCompra.objects.filter(
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
            remisiones = DetalleRemision.objects.filter(
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

        compra.detalles.all().delete()

        for detalle in detalles_dict.values():
            DetalleCompra.objects.create(
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
            producto.save()

            monto_total += detalle['subtotal']

        compra.monto_total = monto_total
        compra.save()

class CompraListView(ListView):
    model = Compra
    template_name = 'inv/compra_list.html'
    context_object_name = 'compras'
    ordering = ['-fecha_compra', '-clave_movimiento', '-referencia']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

from decimal import Decimal
class CompraCreateView(CompraBaseView, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'inv/compra_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = getattr(self.request.user, 'empresa', None)
        
        if empresa and empresa.almacen_actual:
            try:
                almacen = Almacen.objects.get(id=empresa.almacen_actual)
                moneda = Moneda.objects.all()
                initial['almacen'] = almacen.id
            except Almacen.DoesNotExist:
                print("No se encontró el almacén", empresa.almacen_actual)
        
        if empresa.clave_compras:
            try:
                clave_compras = ClaveMovimiento.objects.get(clave_movimiento=empresa.clave_compras)
                initial['clave_movimiento'] = clave_compras.id
            except ClaveMovimiento.DoesNotExist:
                pass

        initial['fecha_compra'] = localtime(now()).date().isoformat()
        return initial

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        formset = DetalleCompraFormSet(queryset=DetalleCompra.objects.none(), prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleCompraFormSet(request.POST, prefix='detalles')
        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.usuario = self.request.user
            self.object.pedido = ''
            self.object.fecha_pagada = '1900-01-01'
            self.object.descuento_pp = 0
            referencia = form.cleaned_data.get('referencia')

            if referencia:
                self.object.referencia = str(referencia).zfill(7)

            self.object.save()
            
            # Aquí se usa la lógica compartida
            self.procesar_formset(formset, self.object)

            return redirect('inv:compra_list')

        return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})
    
class CompraUpdateView(CompraBaseView, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'inv/compra_form.html'
    success_url = reverse_lazy('inv:compra_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        formset = DetalleCompraFormSet(instance=self.object,prefix='detalles')

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = DetalleCompraFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.procesar_formset(formset, self.object)
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['referencia'].widget.attrs['readonly'] = True
        return form

# DETALLE DE MOVIMIENTO DE COMPRAS
class CompraDetailView(DetailView):
    model = Compra
    template_name = 'inv/compra_detail.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleCompra.objects.filter(referencia=self.object)
        return context

class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'inv/compra_confirm_delete.html'
    success_url = reverse_lazy('inv:compra_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context

def verificar_compra(request):
    clave_movimiento_id = request.GET.get('clave_movimiento')
    referencia = request.GET.get('referencia')

    try:
        compra = Compra.objects.get(clave_movimiento_id=clave_movimiento_id, referencia=referencia)
        return JsonResponse({'existe': True, 'id': referencia.id})
    except Compra.DoesNotExist:
        return JsonResponse({'existe': False})

def obtener_dias_plazo(request):
    proveedor_id = request.GET.get('proveedor_id')
    try:
        proveedor = Proveedor.objects.get(pk=proveedor_id)
        return JsonResponse({'dias_plazo': str(proveedor.dias_plazo)})
    except Proveedor.DoesNotExist:
        return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

def obtener_dias_plazo(request):
    proveedor_id = request.GET.get('proveedor_id')
    try:
        proveedor = Proveedor.objects.get(pk=proveedor_id)
        return JsonResponse({'dias_credito': proveedor.plazo_credito})
    except Proveedor.DoesNotExist:
        return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

# CONSULTA DE COMPRAS POR DIA    
def compras_por_dia(request):
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

        resultados = DetalleCompra.objects.filter(
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

def buscar_compras_por_dia(request):
    almacenes = Almacen.objects.all()
    return render(request, 'inv/reportes/compras_por_dia_buscar.html', {'almacenes': almacenes})

#CONSULTAR COMPRAS POR PRODUCTO
def compras_por_producto(request):
    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto = Producto.objects.get(pk=producto_id)

    # saca las compras a partir del detalle
    compras = Compra.objects.filter(
        detalles__producto_id=producto_id,  # este detalles es el related_names definido en la Tabla DetalleCompra
        fecha_compra__range=[fecha_ini, fecha_fin]
    ).distinct().order_by('fecha_compra', 'referencia')
    
    detalles = DetalleCompra.objects.filter(
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

def buscar_compras_por_producto(request):
    productos = Producto.objects.all()

    producto_id = request.GET.get('producto')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    producto_seleccionado = Producto.objects.filter(id=producto_id).first() if producto_id else None

    contexto = {
        'productos': productos,
        'producto_seleccionado': producto_seleccionado,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'inv/reportes/compras_por_producto_buscar.html', contexto)

#CONSULTAR COMPRAS POR PROVEEDOR
def compras_por_proveedor(request):
    total_general = 0
    total_cantidad = 0
    proveedor = None
    fecha_ini = fecha_fin = None

    proveedor_id = request.GET.get('proveedor_id')
    fecha_ini = request.GET.get('fecha_ini')
    fecha_fin = request.GET.get('fecha_fin')

    proveedor = Proveedor.objects.get(pk=proveedor_id)
    
    compras = Compra.objects.filter(
    proveedor_id=proveedor_id,
    fecha_compra__range=[fecha_ini, fecha_fin]
    ).order_by('fecha_compra','referencia') 

    detalles = DetalleCompra.objects.filter(referencia__in=compras
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

def buscar_compras_por_proveedor(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'inv/reportes/compras_por_proveedor_buscar.html', {'proveedores': proveedores})

#def buscar_info_general(request):
#    empresa = Empresa.objects.filter(pk=empresa_id)
#    return render(request, 'inv/reportes/info_general_buscar.html', {'empresa': empresa})

# CRUD INFORMACION GENERAL - SOLO LIST y UPDATE 
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'inv/empresa_list.html'
    context_object_name = 'empresas'

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'inv/empresa_form.html'
    success_url = reverse_lazy('inv:empresa_list')

class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'inv/empresa_form.html'
    success_url = reverse_lazy('inv:empresa_list')

    def form_invalid(self, form):
        return super().form_invalid(form)

# CRUD INFORMACION GENERAL - LUGAR DE EXPEDICION 
class EmpresaLugarListView(ListView):
    model = Empresa
    template_name = 'inv/empresa_lugarexp_list.html'
    context_object_name = 'empresas'

class EmpresaLugarUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaLugarForm
    template_name = 'inv/empresa_lugarexp_form.html'
    success_url = reverse_lazy('inv:empresa_lugarexp_list')

    def form_invalid(self, form):
        return super().form_invalid(form)

# REGISTRO DEL EMISOR DE CFDI
def registrar_emisor_view(request):
    return render(request, "inv/cfdi_registrar_emisor.html")

# VISTA PARA REGISTRA CSD Y ENVIAR AL PAC
# CSD - Certificado de Sello Digital

import base64
import requests

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
                csd = CertificadoCSD.objects.create(
                    empresa=request.user,
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
