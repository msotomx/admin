# Create your views here.

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Empresa
from fac.models import Factura, DetalleFactura, TipoComprobante, Exportacion
from inv.models import Producto, Moneda, ClaveMovimiento, Remision, DetalleRemision
from cxc.models import Cliente, RegimenFiscal
from fac.forms import FacturaForm, DetalleFacturaFormSet, DetalleFacturaForm
from core.utils import get_empresa_actual
from django.utils.timezone import now, localtime
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.forms import modelformset_factory
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.http import JsonResponse
from core.mixins import TenantRequiredMixin
from django.contrib.auth.decorators import login_required
from core.decorators import tenant_required

# CRUD FACTURAS ==================
from decimal import Decimal
class FacturaBaseView:
    def procesar_formset(self, formset, factura):
        # Limpia detalles previos
        factura.detalles.all().delete()

        subtotal_total = Decimal('0')
        descuento_total = Decimal('0')
        iva_total = Decimal('0')
        ieps_total = Decimal('0')
        retencion_iva_total = Decimal('0')
        retencion_isr_total = Decimal('0')

        cliente = factura.cliente
        empresa = self.empresa

        for detalle_form in formset:
            cleaned = getattr(detalle_form, 'cleaned_data', {})
            # 1) Saltar si el form vino marcado para borrado
            if cleaned.get('DELETE', False):
                continue
            # 2) Saltar si no tiene un producto (sub-form vacío)
            producto = cleaned.get('producto')
            if not producto:
                continue
            # Extrae campos básicos
            producto        = detalle_form.cleaned_data['producto']
            clave_prod_serv = detalle_form.cleaned_data['clave_prod_serv']
            cantidad        = detalle_form.cleaned_data['cantidad']
            valor_unitario  = detalle_form.cleaned_data['valor_unitario']
            descuento       = detalle_form.cleaned_data.get('descuento') or Decimal('0')

            # Inicializa instancia sin guardar aún
            detalle = DetalleFactura(
                factura        = factura,
                producto       = producto,
                clave_prod_serv= clave_prod_serv,
                clave_unidad   = producto.unidad_medida.unidad_medida,
                descripcion    = producto.nombre,
                cantidad       = cantidad,
                valor_unitario = valor_unitario,
                descuento      = descuento,
                # (tasa_iva, iva, ieps, retenciones se calculan en  el metodo grabar)
                objeto_impuesto= '02',
            )
            detalle.grabar()

            # Acumula en totales
            subtotal_total         += detalle.importe
            descuento_total        += detalle.descuento
            iva_total              += detalle.iva_producto
            ieps_total             += detalle.ieps_producto
            retencion_iva_total    += detalle.retencion_iva
            retencion_isr_total    += detalle.retencion_isr

        # Actualiza campos de la factura
        factura.subtotal             = subtotal_total
        factura.descuento_factura    = descuento_total
        factura.iva_factura          = iva_total
        factura.ieps_factura         = ieps_total
        factura.retencion_iva_factura= retencion_iva_total
        factura.retencion_isr_factura= retencion_isr_total
        factura.impuestos_trasladados= iva_total + ieps_total
        factura.impuestos_retenidos  = retencion_iva_total + retencion_isr_total
        factura.total                = subtotal_total + iva_total + ieps_total \
                                        - retencion_iva_total - retencion_isr_total
        factura.fecha_creacion       = localtime(now()).date() 
        factura.save(
            using=self.db_name
        )

class FacturaListView(TenantRequiredMixin, ListView):
    model = Factura
    template_name = 'fac/factura_list.html'
    context_object_name = 'facturas'
    # ordering = ['- n u m e r o_factura']  # Orden descendente por numero_factura
    paginate_by = 10  # Número de movimientos por página
    
    # Este metodo se encarga de aplicar orden personalizado, 
    # usarlo cuando se realicen busquedas y que se quiera presentar el resultado en algun orden
    # en este caso en orden descendente por numero_factura
    # al usar este metodo ya no se ocupa la funcion en la vista, para la busqueda se requiere:
    #    1) este metodo 2) el url factura_list 3) en el template factura_list agregar el query-form
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        # Primero obtenemos todas las facturas
        facturas = Factura.objects.all()

        if query:
            # Aplicamos filtros si hay búsqueda
            facturas = facturas.filter(
                Q(cliente__nombre__icontains=query) |
                Q(cliente__rfc__icontains=query) |
                Q(numero_factura__icontains=query)
            )
        
        # Finalmente, ordenamos en orden descendente por numero_factura
        return facturas.order_by('-numero_factura')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()  # para que se mantenga en el input
        return context

from decimal import Decimal
class FacturaCreateView(TenantRequiredMixin, FacturaBaseView, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'fac/factura_form.html'

    def get_initial(self):
        initial = super().get_initial()
        
        empresa = self.empresa
        if empresa:
            initial['empresa'] = empresa
        
        if empresa.clave_remision:
            try:
                clave_remision = ClaveMovimiento.objects.using(self.db_name).get(clave_movimiento=empresa.clave_remision)
                initial['clave_remision'] = clave_remision.id

            except ClaveMovimiento.DoesNotExist:
                print("No se encontró la Clave de Remision", empresa.clave_remision)

        initial['numero_remision'] = '0000000'  
        initial['fecha_emision'] = localtime(now()).date()
        initial['fecha_creacion'] = localtime(now()).date()
        initial['serie_emisor'] = 'A'
        initial['lugar_expedicion'] = empresa.codigo_postal_expedicion
        initial['tipo_cambio'] = 1
        moneda_mxn = Moneda.objects.using(self.db_name).filter(clave="MXN").first()
        if moneda_mxn:
            initial['moneda'] = moneda_mxn.id

        tipo_comprobante = TipoComprobante.objects.using(self.db_name).filter(tipo_comprobante='I').first()
        initial['tipo_comprobante'] = tipo_comprobante
        initial['exportacion'] = Exportacion.objects.using(self.db_name).filter(exportacion='01').first()
        initial['condiciones_pago'] = 'CONTADO'
        initial['xml'] = ''
        initial['pdf'] = ''

        # Información de timbrado
        initial['uuid'] = ''
        initial['fecha_timbrado'] = ''
        initial['sello'] = ''
        initial['sello_sat'] = ''
        initial['num_certificado'] = ''
        initial['rfc_certifico'] = ''
        initial['estatus'] = 'Borrador'
        initial['subtotal'] = 0
        initial['descuento_factura'] = 0
        initial['total'] = 0
        return initial

    # get original
    #def get(self, request, *args, **kwargs):
    #    form = self.form_class(initial=self.get_initial())
    #    formset = DetalleFacturaFormSet(queryset=DetalleFactura.objects.using(self.db_name).none(), prefix='detalles')
    #    return render(request, self.template_name, {'form': form, 'formset': formset})

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, db_name=self.db_name)
        formset = DetalleFacturaFormSet(queryset=DetalleFactura.objects.using(self.db_name).none())  # Inicializa el formset vacío

        # Asignar el valor inicial de 'almacen'
        initial = self.get_initial()  # Llamamos a get_initial() para obtener los valores iniciales del formulario
        form.initial = initial  # Asignamos esos valores iniciales al formulario
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = getattr(self, 'object', None)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, db_name=self.db_name)
        formset = DetalleFacturaFormSet(
            request.POST,
            queryset=DetalleFactura.objects.using(self.db_name).none(),
            prefix='detalles'
        )
        
        if form.is_valid() and formset.is_valid():
            return self.guardar_factura_y_detalles(form, formset)

        return self.form_invalid(form, formset)

    from django.db import transaction
    @transaction.atomic
    def guardar_factura_y_detalles(self, form, formset):
        factura = form.save(commit=False)

        # Asignaciones obligatorias
        empresa = self.empresa

        factura.usuario = self.request.user.username
        factura.empresa = empresa  
        
        # Asignar moneda MXN si no viene del formulario
        if not factura.moneda:
            moneda_mxn = Moneda.objects.using(self.db_name).filter(clave="MXN").first()
            if not moneda_mxn:
                form.add_error(None, "No se encontró la moneda MXN en la base de datos.")
                return self.form_invalid(form, formset)
            factura.moneda = moneda_mxn

        # Asegurar tipo de comprobante
        if not factura.tipo_comprobante:
            tipo_comp = TipoComprobante.objects.using(self.db_name).filter(tipo_comprobante='I').first()
            if not tipo_comp:
                form.add_error(None, "No se encontró el tipo de comprobante 'I'")
                return self.form_invalid(form, formset)
            factura.tipo_comprobante = str(tipo_comp)[:1]

        # Defaults si están vacíos
        factura.serie_emisor = factura.serie_emisor or 'A'
        factura.lugar_expedicion = empresa.codigo_postal_expedicion or '00000'
        factura.tipo_cambio = factura.tipo_cambio or Decimal('1.00')
        factura.exportacion = factura.exportacion or Exportacion.objects.using(self.db_name).filter(exportacion='01').first()
        factura.condiciones_pago = factura.condiciones_pago or 'CONTADO'
        factura.estatus = factura.estatus or 'Borrador'
        factura.subtotal = factura.subtotal or Decimal('0.00')
        factura.descuento_factura = factura.descuento_factura or Decimal('0.00')
        factura.total = factura.total or Decimal('0.00')
        factura.iva_factura = factura.iva_factura or Decimal('0.00')
        factura.ieps_factura = factura.ieps_factura or Decimal('0.00')
        factura.retencion_iva_factura = factura.retencion_iva_factura or Decimal('0.00')
        factura.retencion_isr_factura = factura.retencion_isr_factura or Decimal('0.00')

        factura.save(
            using=self.db_name
        )

        # procesar detalles
        self.procesar_formset(formset, factura)
        
        #return redirect('fac:factura_list')
        return redirect('fac:factura_update', pk=factura.pk)
    
    def form_invalid(self, form, formset):
        print("Errores del form principal:", form.errors)
        print("Errores del formset:")
        for i, f in enumerate(formset):
            if f.errors:
                print(f"Errores en el formulario #{i}:", f.errors.as_data())
        
        messages.error(self.request, "Hay errores en el formulario. Por favor revísalos.")

        return render(self.request, self.template_name, {'form': form, 'formset': formset})
    
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.db import transaction
from .models import Factura, DetalleFactura
from .forms import FacturaForm, DetalleFacturaFormSet

class FacturaUpdateView(TenantRequiredMixin, FacturaBaseView, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'fac/factura_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        formset = DetalleFacturaFormSet(
            instance=self.object,
            queryset=DetalleRemision.objects.using(self.db_name).filter(factura=self.object),
            prefix='detalles'
        )
        
        if (self.object.estatus == "Vigente") or (self.object.estatus == "Cancelada"):
            for f in formset.forms:
                for field in f.fields.values():
                    field.disabled = True

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if (self.object.estatus == "Vigente") or (self.object.estatus == "Cancelada"):
            for field in form.fields.values():
                field.disabled = True  # Esto desactiva el campo
        return form
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST or None, db_name=self.db_name)
        formset = DetalleFacturaFormSet(
            request.POST,
            instance=self.object,
            queryset=DetalleFactura.objects.using(self.db_name).filter(factura=self.object),
            prefix='detalles'
        )
        
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    @transaction.atomic
    def form_valid(self, form, formset):
        # Guarda la factura principal
        factura = form.save(commit=False)
        
        empresa = self.empresa

        factura.save(
            using=self.db_name
        )


        # Recalcula y graba los detalles usando tu lógica centralizada
        self.procesar_formset(formset, factura)

        return redirect('fac:factura_list')

    def form_invalid(self, form, formset):
        messages.error(self.request, "Hay errores en el formulario. Por favor revísalos.")
        print("Errores del form principal:", form.errors)
        print("Errores del formset:")
        for i, f in enumerate(formset):
            if f.errors:
                print(f"Errores en el formulario #{i}:", f.errors.as_data())

        return render(self.request, self.template_name, {'form': form, 'formset': formset})

# VER FACTURA CUANDO YA ESTA TIMBRADA 
class FacturaDetailView(TenantRequiredMixin, DetailView):
    model = Factura
    template_name = 'fac/factura_detail.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleFactura.objects.using(self.db_name).filter(factura=self.object)
        return context

from django.views.generic import DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Factura

class FacturaDeleteView(TenantRequiredMixin, DeleteView):
    model = Factura
    template_name = 'fac/factura_confirm_delete.html'
    success_url = reverse_lazy('fac:factura_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.estatus not in ['Borrador', 'Error']:
            messages.warning(request, "Solo se pueden eliminar facturas en estatus BORRADOR o ERROR.")
            return redirect('fac:factura_list')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_name = self.request.session.get('db_config')['NAME']
        context['detalles'] = self.object.detalles.using(db_name).all()
        return context

    def get_queryset(self):
        db_name = self.request.session.get('db_config')['NAME']
        return Factura.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        db_name = self.request.session.get('db_config')['NAME']
        self.object = self.get_object()

        # Eliminar detalles explícitamente
        self.object.detallefactura_set.using(db_name).all().delete()

        # Eliminar Encabezado - MOvimiento
        self.object.delete(using=db_name)
        messages.success(request, "Factura eliminada correctamente.")
        return super().delete(request, *args, **kwargs)

# FUNCION PARA VALIDAR SI UNA FACTURA YA EXISTE
@login_required
@tenant_required
def verificar_factura(request):
    get_empresa_actual(request)
    numero_factura = request.GET.get('numero_factura')

    try:
        factura = Factura.objects.using(request.db_name).get(numero_factura=numero_factura)
        return JsonResponse({'existe': True, 'id': factura.id})
    except Factura.DoesNotExist:
        return JsonResponse({'existe': False})

@login_required
@tenant_required
def obtener_clave_prod_serv2(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.using(request.db_name).get(pk=producto_id)
        return JsonResponse({'clave_prod_serv': producto.clave_sat})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@login_required
@tenant_required
def obtener_ultimo_numero_factura(request):
    ultima = Factura.objects.using(request.db_name).all().order_by('-numero_factura').first()
    if ultima and ultima.numero_factura.isdigit():
        siguiente = str(int(ultima.numero_factura) + 1).zfill(7)
    else:
        siguiente = "0000001"
    
    return JsonResponse({'numero_factura': siguiente})

# ESTA FUNCION SE UTILIZA EN GENERAR CFDI
@login_required
@tenant_required
@require_GET
def obtener_tasa_empresa(request):
    cliente_id = request.GET.get('cliente_id')
    # 1) Validar que se recibió cliente_id
    if not cliente_id or not cliente_id.isdigit():
        return JsonResponse({'error': 'Parámetro cliente_id inválido'}, status=400)
 
    # 2) Obtener la empresa asociada al usuario
    empresa = get_empresa_actual(request)
    
    if not empresa:
        return JsonResponse({'error': 'Usuario sin empresa asignada'}, status=403)

    # 3) Extraer tasas de la empresa
    tasa_iva      = float(empresa.tasa_iva)
    tasa_ieps     = float(empresa.tasa_ieps)
    ret_iva       = float(empresa.tasa_retencion_iva)
    ret_isr       = float(empresa.tasa_retencion_isr)

    # 4) Ajustar según configuración del cliente
    try:
        cliente = Cliente.objects.using(request.db_name).get(pk=cliente_id)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    if not cliente.aplica_retencion_iva:
        ret_iva = 0.0
    if not cliente.aplica_retencion_isr:
        ret_isr = 0.0

    # 5) Devolver JSON con números (no Decimal) para que JS reciba Number
    return JsonResponse({
        'tasa_iva_empresa': tasa_iva,
        'tasa_ieps_empresa': tasa_ieps,
        'tasa_retencion_iva_empresa': ret_iva,
        'tasa_retencion_isr_empresa': ret_isr,
    })


# TIMBRADO DE CFDI
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import localtime, now

# Esta función toma el objeto Factura y construye el JSON que se enviará al PAC para timbrar.
@login_required
@tenant_required
def generar_json_cfdi(request,factura):
    cliente = factura.cliente
    emisor = factura.empresa
    detalles = factura.detalles.using(request.db_name).all()

    conceptos = []
    # Para acumular totales y agrupar traslados/retenciones
    # Usamos dicts: {(impuesto, tasa_o_cuota): {'base': Decimal, 'importe': Decimal}}
    traslados_agrup = {}
    retenciones_agrup = {}

    for detalle in detalles:
        # Determinar importe neto y descuento
        # Asumimos que det.importe ya es neto = (cantidad * valor_unitario) - descuento

        base = float(detalle.importe)  # es neto, ya incluye descuento
        descuento = detalle.descuento
        if detalle.descuento is None:
            descuento = float('0.0')

        # Tasas como proporción: ej. detalle.tasa_iva = Decimal('0.16') si aplica
        tasa_iva = getattr(detalle, 'tasa_iva', float('0')) or float('0')
        tasa_ieps = getattr(detalle, 'tasa_ieps', float('0')) or float('0')

        # Importes de impuesto en detalle (ya calculados en el modelo):
        iva_detalle = getattr(detalle, 'iva_producto', None)
        if iva_detalle is None:
            iva_detalle = (base * tasa_iva).quantize(Decimal('0.01'))
        ieps_detalle = getattr(detalle, 'ieps_producto', None)
        if ieps_detalle is None:
            ieps_detalle = (base * tasa_ieps).quantize(Decimal('0.01'))
        
        # Retenciones en detalle:
        # supongamos det.retencion_iva y det.retencion_isr ya calculados
        retencion_iva_detalle = getattr(detalle, 'retencion_iva', float('0')) or float('0')
        retencion_isr_detalle = getattr(detalle, 'retencion_isr', float('0')) or float('0')
        tasa_retencion_iva    = getattr(detalle, 'tasa_retencion_iva', float('0')) or float('0')
        tasa_retencion_isr    = getattr(detalle, 'tasa_retencion_isr', float('0')) or float('0')

        # Agrupar traslados: IVA
        if iva_detalle and tasa_iva > 0:
            key = ("002", float(tasa_iva))
            entry = traslados_agrup.setdefault(key, {'base': float('0'), 'importe': float('0')})
            entry['base'] += float(base)
            entry['importe'] += float(iva_detalle)
        # Agrupar traslados: IEPS 
        if ieps_detalle and tasa_ieps > 0:
            key = ("003", float(tasa_ieps))
            entry = traslados_agrup.setdefault(key, {'base': float('0'), 'importe': float('0')})
            entry['base'] += float(base)
            entry['importe'] += float(ieps_detalle)

        # Agrupar retenciones: ISR retención (código "001" o "002")
        if retencion_isr_detalle and retencion_isr_detalle > 0:
            key = ("001", None)
            entry = retenciones_agrup.setdefault(key, {'importe': float('0')})
            entry['importe'] += float(retencion_isr_detalle)
        # Agrupar retenciones: IVA retención
        if retencion_iva_detalle and retencion_iva_detalle > 0:
            key = ("002", None) 
            entry = retenciones_agrup.setdefault(key, {'importe': float('0')})
            entry['importe'] += float(retencion_iva_detalle)

        # Construir el concepto
        concepto = {
            "clave_prod_serv": detalle.clave_prod_serv,
            "descripcion": detalle.descripcion,
            "clave_unidad": detalle.clave_unidad,
            "unidad": detalle.producto.unidad_medida.descripcion if hasattr(detalle.producto.unidad_medida, 'descripcion') 
                       else detalle.clave_unidad,
            "valor_unitario": float(detalle.valor_unitario),
            "cantidad": float(detalle.cantidad),
            "importe": float(detalle.importe) + float(descuento),
            "subtotal": float(base),       # neto
            "numero_identificacion": detalle.producto.sku  if hasattr(detalle.producto.sku, 'sku') else "", 
            "objeto_impuesto": detalle.objeto_impuesto,
            "impuestos": {"traslados": [], "retenciones": []}
        }
    
        tc = str(factura.tipo_comprobante.tipo_comprobante)[:1]
        if tc in ['I', 'E', 'N'] and float(descuento) > 0:
            concepto["descuento"] = float(descuento)
        
        # Detalle traslados
        if iva_detalle and tasa_iva > 0:
            tasa_str = "{:.6f}".format(float(tasa_iva))  # tasa con 6 decimales
            concepto["impuestos"]["traslados"].append({
                "base": float(base),
                "impuesto": "002",
                "tipo_factor": "Tasa",
                "tasa_cuota": tasa_str,
                "importe": float(iva_detalle)
            })
        if ieps_detalle and tasa_ieps > 0:
            tasa_str = "{:.6f}".format(float(tasa_ieps))  # tasa con 6 decimales
            concepto["impuestos"]["traslados"].append({
                "base": float(base),
                "impuesto": "003",
                "tipo_factor": "Tasa",
                "tasa_cuota": tasa_str,
                "importe": float(ieps_detalle)
            })
        # Detalle retenciones
        if retencion_isr_detalle and retencion_isr_detalle > 0:
            tasa_str = "{:.6f}".format(float(tasa_retencion_isr))  # tasa con 6 decimales
            concepto["impuestos"]["retenciones"].append({
                "base": float(base),
                "impuesto": "001",
                "tipo_factor": "Tasa",
                "tasa_cuota": tasa_str,
                "importe": float(retencion_isr_detalle)
            })
        if retencion_iva_detalle and retencion_iva_detalle > 0:
            tasa_str = "{:.6f}".format(float(tasa_retencion_iva))  # tasa con 6 decimales
            concepto["impuestos"]["retenciones"].append({
                "base": float(iva_detalle),
                "impuesto": "002",
                "tipo_factor": "Tasa",
                "tasa_cuota": tasa_str,
                "importe": float(retencion_iva_detalle)
            })

        conceptos.append(concepto)

    # Construir lista de traslados a nivel factura
    traslados = []
    total_traslado = float('0')
    for (impuesto, tasa), vals in traslados_agrup.items():
        tasa_str = "{:.6f}".format(float(tasa))  # tasa con 6 decimales
        base = vals['base']
        importe = vals['importe']
        total_traslado += importe
        traslados.append({
            "base": float(base),
            "impuesto": impuesto,
            "tipo_factor": "Tasa",
            "tasa_cuota": tasa_str,
            "importe": float(importe)
        })

    # Construir lista de retenciones a nivel factura
    retenciones = []
    total_retencion = float('0')
    for (impuesto, _), vals in retenciones_agrup.items():
        importe = vals['importe']
        total_retencion += float(importe)
        # No se envía tasa_o_cuota en retenciones 
        retenciones.append({
            "impuesto": impuesto,
            "importe": float(importe)
        })

    # Montar el objeto impuestos para PAC
    impuestos = {}
    # Solo agregar impuestos trasladados si hay al menos una
    if traslados:
        impuestos["total_impuestos_trasladados"] = float(total_traslado)
        impuestos["traslados"] = traslados

    # Solo agregar retenciones si hay al menos una
    if retenciones:
        impuestos["total_impuestos_retenidos"] = float(total_retencion)
        impuestos["retenciones"] = retenciones


    # Información global: si no aplicas facturación global, déjalo vacío o elimínalo
    informacion_global = {}
    # Si no aplicas global, algunos PAC requieren omitir la clave:
    # No incluir "informacion_global" si no aplica:
    # json_cfdi.pop("informacion_global", None)

    # Fecha_emision: según spec, puede requerir hora. Ejemplo:
    fecha = localtime(now()).strftime("%Y-%m-%d %H:%M:%S")

    # "numero_cuenta": "6789",
    # "nombre_banco": "BBVA",
    receptor = {
        "rfc": cliente.rfc,
        "razon_social": cliente.nombre,
        "uso_cfdi": factura.uso_cfdi.uso_cfdi,
        "regimen_fiscal": cliente.regimen_fiscal.regimen_fiscal if cliente.regimen_fiscal else None,
        "codigo_postal": cliente.codigo_postal or "",
    }
    descuentoF = factura.descuento_factura
    if descuentoF is None:
        descuentoF = float('0.0')
    camposPDF = {
        "tipoComprobante": "Factura",
        "Comentarios": "Aqui van los comentarios de la factura",
        "calleEmisor": emisor.calle_expedicion,
        "noExteriorEmisor": emisor.numero_exterior_expedicion,
        "noInteriorEmisor": emisor.numero_interior_expedicion,
        "coloniaEmisor": emisor.colonia_expedicion,
        "codigoPostalEmisor": emisor.codigo_postal_expedicion,
        "localidadEmisor": emisor.localidad_expedicion,
        "municipioEmisor": emisor.municipio_expedicion,
        "estadoEmisor": emisor.estado_expedicion,
        "paisEmisor": emisor.pais_expedicion,
        "telefonoEmisor": emisor.telefono,
        "emailEmisor": emisor.email,
        "calleReceptor": cliente.calle,
        "noExteriorReceptor": cliente.numero_exterior,
        "noInteriorReceptor": cliente.numero_interior,
        "coloniaReceptor": cliente.colonia,
        "codigoPostalReceptor": cliente.codigo_postal,
        "localidadReceptor": cliente.ciudad,
        "municipioReceptor": cliente.municipio,
        "estadoReceptor": cliente.estado,
        "paisReceptor": "Mexico",
        
    }

    json_cfdi = {
        "fecha_emision": fecha,
        "serie": factura.serie_emisor,
        "folio": int(factura.numero_factura),
        "forma_pago": factura.forma_pago.forma_pago,
        "metodo_pago": factura.metodo_pago.metodo_pago,
        "condiciones_pago": getattr(factura, 'condiciones_pago', None) or "",
        "tipo_comprobante": tc,
        "moneda": factura.moneda.clave,
        "tipo_cambio": float(factura.tipo_cambio),
        "subtotal": float(factura.subtotal) + float(factura.descuento_factura),
        "total": float(factura.total),
        "lugar_expedicion": factura.lugar_expedicion,
        "observaciones": "observaciones de la factura vamos a ver que tantos caracteres acepta este campo de observaciones",
        "exportacion": factura.exportacion.exportacion,
        "respuesta_compatibilidad_terceros": False,
        # Emisor
        "emisor": {
            "rfc": emisor.rfc,
            "razon_social": emisor.nombre_fiscal,
            "regimen_fiscal": emisor.regimen_fiscal.regimen_fiscal,
            "codigo_postal": emisor.codigo_postal_expedicion,
        },
        # Receptor
        "receptor": receptor,
        # Conceptos e impuestos
        "conceptos": conceptos,
        "impuestos": impuestos,
        "camposPDF": camposPDF,
        # Solo incluir si aplica:
        # "informacion_global": informacion_global,
    }
    
    if tc in ['I', 'E', 'N'] and float(descuentoF) > 0:
        json_cfdi["descuento"] = float(descuentoF)

    # print("Data antes de serializar:", json_cfdi)
    return json_cfdi

from django.core.exceptions import ObjectDoesNotExist
# Esta función obtiene la factura y llama a la función generar_json_cfdi
@login_required
@tenant_required
def generar_json_timbrado22(request,factura_id):
    from .models import Factura  # Importación interna para evitar pro
    try:
        factura = (Factura.objects
            .using(request.db_name)  # ← base del tenant
            .select_related(
                'empresa', 'cliente__regimen_fiscal',
                'forma_pago', 'moneda', 'metodo_pago',
                'uso_cfdi', 'tipo_comprobante', 'exportacion'
            )
            .prefetch_related('detalles__producto__unidad_medida')
            .get(pk=factura_id))
    except Factura.DoesNotExist:
        raise ValueError(f"Factura con id {factura_id} no encontrada")
    
    if factura.estatus not in ['Borrador', 'Error']:
        raise ValueError(f"Estatus '{factura.estatus}' no válido para timbrar factura {factura_id}")

    return generar_json_cfdi(factura)

import os
from django.core.files.base import ContentFile
from django.utils.timezone import is_naive, make_aware
from django.utils import timezone
from datetime import datetime

import logging
logger = logging.getLogger(__name__)
@login_required
@tenant_required
def guardar_archivos_factura(request,factura, uuid=None, sello=None, sello_sat=None, 
                             num_certificado=None, rfc_certifico=None, 
                             fecha_timbrado=None, estatus=None):
    """
    Guarda la factura ya timbrada
    Parámetros:
        - factura: instancia de Factura ya existente.
        - xml y pdf en otra funcion 
        - uuid, sello... 
    """
    if not factura.pk:
        raise ValueError("La factura debe existir antes de guardar archivos")
    # convierte fecha_timbrado a aware
    
    if isinstance(fecha_timbrado, str):
        try:
            fecha_dt = datetime.strptime(fecha_timbrado, "%Y-%m-%d %H:%M:%S")
        except Exception:
            fecha_dt = timezone.now()
    elif isinstance(fecha_timbrado, datetime):
        fecha_dt = fecha_timbrado
    else:
        fecha_dt = timezone.now()  # fallback seguro

    # Si es naive, conviértelo a aware
    if timezone.is_naive(fecha_dt):
        fecha_dt = timezone.make_aware(fecha_dt, timezone.utc)  # Aseguramos que es UTC

    # Ahora, ajustamos la fecha a la zona horaria local (si corresponde)
    fecha_local = fecha_dt.astimezone(timezone.get_current_timezone())


    # Timbrado exitoso
    factura.estatus = estatus

    factura.fecha_timbrado = fecha_local

    # Guardar UUID si viene del PAC
    if uuid:
        factura.uuid = uuid
    if sello:
        factura.sello = sello
    if sello_sat:
        factura.sello_sat = sello_sat
    if num_certificado:
        factura.num_certificado = num_certificado
    if rfc_certifico:
        factura.rfc_certifico = rfc_certifico

    # Guardar cambios
    try:
        factura.save(
            using=request.db_name,  # 👈 fuerza guardado en la base tenant
            update_fields=['estatus', 'fecha_timbrado', 'uuid',
                        'sello','sello_sat','num_certificado','rfc_certifico']
        )
        success, mensaje = consultar_y_guardar_archivos(factura)
        if not success:
                return JsonResponse({'success': False, 'error': mensaje}, status=500)

    except Exception as e:
            logger.error(f"Error guardando factura tras timbrado {factura.pk}: {e}")
            raise

# Vamos a integrar la lógica completa para generar y enviar un CFDI al PAC en una función (timbrar_factura) que:
#1) Reciba un factura_id.
#2) Genere el JSON del CFDI a partir de los modelos (Factura, DetalleFactura, Cliente, etc.).
#3) Envíe el JSON al PAC vía requests.post().
#4) Procese la respuesta:
#    Si es exitosa, guarde UUID, XML, PDF, sello, fecha de timbrado, etc.
#    Si falla, registre el error.

import os
import requests
from django.utils.timezone import localtime, now
from django.core.files.base import ContentFile
from django.conf import settings
 
# UTILIZA generar_json_cfdi  --> Esta función construye el JSON a partir de la factura
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import base64

@login_required
@tenant_required
@require_POST
def timbrar_factura(request,factura_id):
    db_name = request.db_name  # ← viene del decorador tenant_required

    factura = get_object_or_404(
        Factura.objects.using(db_name),
        pk=factura_id,
        usuario=request.user.username
    )

    # 1) Verificar estatus de la factura
    if factura.estatus not in ['Borrador', 'Error']:
        return JsonResponse(
            {'success': False, 'error': 'Estatus no válido para timbrar'},
            status=400
        )
    if not factura.serie_emisor or not factura.numero_factura.isdigit():
        return JsonResponse({'success': False, 'error': 'Serie o folio inválido'}, status=400)

    # 2) Generar JSON CFDI
    try:
        # Genera el JSON del CFDI
        json_cfdi = generar_json_cfdi(request, factura)
        
        # Validación
        if validar_cfdi(json_cfdi):
            # Aquí iría el código para enviar al PAC
            print("CFDI validado correctamente, listo para enviarse.")
        else:
                        
            return JsonResponse({'success': False, 'error': 'Error al generar CFDI: validación fallida.'}, status=400)        
    
    except ValueError as e:
        print(f"Error de validación: {e}")
        return JsonResponse({'success': False, 'error': f'Error al generar JSON CFDI: {e}'}, status=500)

    # 3) Preparar llamada al PAC
    url = settings.PAC_URL
    if not url:
        return JsonResponse({'success': False, 'error': 'No está configurada la URL del PAC'}, status=500)
    
    headers = {
        "Authorization": f"Bearer {settings.PAC_API_TOKEN}",
        "X-CLIENT-ID": settings.PAC_CLIENT_ID,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    # 4) Enviar al PAC
    try:
        resp = requests.post(url, json=json_cfdi, headers=headers, timeout=30)
    except requests.RequestException as e:
        # Error de red, timeout, etc.
        factura.estatus = "Error"
        factura.save(using=request.db_name, update_fields=['estatus'])
        return JsonResponse({'success': False, 'error': f'Error al conectar con PAC: {e}'}, status=502)
    
    # 5) Procesar respuesta
    try:
        data = resp.json()
    except ValueError:
        data = None
    

    uuid = None
    if data and isinstance(data, dict):
        uuid = data.get("data", {}).get("timbre_fiscal", {}).get("uuid")
    
    if 200 <= resp.status_code < 300 and uuid:
        try:
            timbre = data["data"].get("timbre_fiscal", {})
            guardar_archivos_factura(
                request,
                factura,
                uuid            = timbre.get("uuid"),
                sello           = timbre.get("sello"),
                sello_sat       = timbre.get("sello_sat"),
                num_certificado = timbre.get("num_certificado_sat"),
                rfc_certifico   = timbre.get("rfc_certifico"),
                fecha_timbrado  = data["data"].get("fecha_timbrado"),
                estatus         = data["data"].get("estado"),
            )
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error al guardar archivos: {e}'}, status=500)

        return JsonResponse({'success': True, 'uuid': factura.uuid})

    else:
        # En caso de fallo del PAC: marcar ERROR y devolver detalle
        factura.estatus = "Error"
        factura.save(using=request.db_name, update_fields=['estatus'])
        # Obtener mensaje de error del PAC si viene en JSON
        err_msg = None
        if data and data.get("error"):
            err_msg = data.get("error")
        else:
            err_msg = resp.text
        return JsonResponse({'success': False, 'error': err_msg}, status=resp.status_code or 500)

from django.contrib import messages
@login_required
@tenant_required
def validar_cfdi(json_cfdi):
    # Validar emisor
    emisor = json_cfdi.get('emisor', {})
    if not emisor.get('rfc'):
        raise ValueError("Falta RFC del emisor.")
    
    if not emisor.get('razon_social'):
        raise ValueError("Falta la razón social del emisor.")
    if not emisor.get('regimen_fiscal'):
        raise ValueError("Falta el régimen fiscal del emisor.")

    # Validar receptor
    receptor = json_cfdi.get('receptor', {})
    if not receptor.get('rfc'):
        return False
        
    if not receptor.get('razon_social'):
        raise ValueError("Falta la razón social del receptor.")
    if not receptor.get('regimen_fiscal'):
        raise ValueError("Falta el régimen fiscal del receptor.")

    # Validar conceptos
    conceptos = json_cfdi.get('conceptos', [])
    if not conceptos:
        raise ValueError("Faltan los conceptos en el CFDI.")
    for i, concepto in enumerate(conceptos):
        if not concepto.get('clave_prod_serv'):
            raise ValueError(f"Falta la clave del producto o servicio en el concepto {i + 1}.")
        if not concepto.get('cantidad'):
            raise ValueError(f"Falta la cantidad en el concepto {i + 1}.")
        if not concepto.get('valor_unitario'):
            raise ValueError(f"Falta el valor unitario en el concepto {i + 1}.")

    # Validar impuestos (traslados y retenciones)
    impuestos = json_cfdi.get('impuestos', {})
    if (impuestos.get('total_impuestos_trasladados')) and (impuestos.get('traslados')):
        if not impuestos.get('total_impuestos_trasladados') == 0.0 and not impuestos.get('traslados'):
            raise ValueError("Faltan traslados en los impuestos.")
    if (impuestos.get('total_impuestos_retenidos')) and (impuestos.get('retenciones')):
        if not impuestos.get('total_impuestos_retenidos') == 0.0 and not impuestos.get('retenciones'):
            raise ValueError("Faltan retenciones en los impuestos.")

    # Validar totals
    if not json_cfdi.get('total'):
        raise ValueError("Falta el total del CFDI.")
    if not json_cfdi.get('subtotal'):
        raise ValueError("Falta el subtotal del CFDI.")

    # Validación de fechas
    if not json_cfdi.get('fecha_emision'):
        raise ValueError("Falta la fecha de emisión del CFDI.")

    return True  # Si todo está validado correctamente

#
# FUNCION PARA GUARDAR EL XML y PDF Y LO GUARDA EN FACTURA
#
import requests
import base64

@login_required
@tenant_required
def consultar_y_guardar_archivos(request, factura):
    uuid = factura.uuid
    if not uuid:
        return False, "UUID no disponible"

    base_url = "https://dev.techbythree.com/api/v1/facturacion/descargar"
    headers = {
        "Authorization": f"Bearer {settings.PAC_API_TOKEN}",
        "Accept": "application/json",
        "X-CLIENT-ID": settings.PAC_CLIENT_ID,
    }
    
    nombre_factura= f"FACTURA_{factura.cliente.rfc}_{factura.numero_factura}" if factura.cliente and factura.numero_factura else "factura-sin-datos"
    try:
        # 1. Descargar XML
        xml_url = f"{base_url}/{uuid}/xml"
        xml_resp = requests.get(xml_url, headers=headers)
        if xml_resp.status_code != 200:
            return False, f"Error consultando XML: {xml_resp.text}"
        xml_data = xml_resp.json()
        xml_str = xml_data.get("archivo")  # 🔄 clave corregida

        # 2. Descargar PDF
        pdf_url = f"{base_url}/{uuid}/pdf"
        pdf_resp = requests.get(pdf_url, headers=headers)
        if pdf_resp.status_code != 200:
            return False, f"Error consultando PDF: {pdf_resp.text}"
        pdf_data = pdf_resp.json()
        pdf_b64 = pdf_data.get("archivo") 

        if not xml_str or not pdf_b64:
            return False, "XML o PDF no disponibles en la respuesta"

        # Guardar en el modelo
        factura.xml.save(f"{nombre_factura}.xml", ContentFile(xml_str.encode('utf-8')), save=False)
        factura.pdf.save(f"{nombre_factura}.pdf", ContentFile(base64.b64decode(pdf_b64)), save=False)
        factura.save(using=request.db_name,update_fields=["xml", "pdf"])

        return True, "Archivos descargados y guardados correctamente"

    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

import os
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
# DESCARGA EL PDF


@login_required
@tenant_required
@xframe_options_exempt
def descargar_factura(request, factura_id, tipo):
    #    factura = get_object_or_404(Factura, id=factura_id)
    db_name = request.db_name  # ← viene del decorador tenant_required

    factura = get_object_or_404(
        Factura.objects.using(db_name),
        id=factura_id,
    )

    nombre_factura= f"FACTURA_{factura.cliente.rfc}_{factura.numero_factura}" if factura.cliente and factura.numero_factura else " "
    if tipo == 'xml':
        archivo = factura.xml
        content_type = 'application/xml'
        nombre = f"{nombre_factura}.xml"
    elif tipo == 'pdf':
        archivo = factura.pdf
        content_type = 'application/pdf'
        nombre = f"{nombre_factura}.pdf"

    else:
        raise Http404("Tipo de archivo no válido")

    if not archivo:
            return HttpResponse(status=204)  # No Content, sin error visible    
    
    response = HttpResponse(archivo, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{nombre}"'  # Para abrir en navegador
    return response



# Busca la remision y regresa los datos para cargarlos en factura_form.html
@login_required
@tenant_required
def cargar_remision(request):
    numero = request.GET.get('numero_remision')
    clave_id = request.GET.get('clave_movimiento')
    try:
        remision = Remision.objects.get(numero_remision=numero, clave_movimiento_id=clave_id)
    
        detalles = DetalleRemision.objects.filter(numero_remision=remision)

        data = {
            'cliente_id': remision.cliente.id,
            'detalles': []
        }
        i = 0
        for det in detalles:
            data['detalles'].append({
                'producto_id': det.producto.id,
                'cantidad': float(det.cantidad),
                'precio': float(det.precio),
                'descuento': float(det.descuento or 0),
                'importe': float(det.subtotal),
                'clave_prod_serv': det.producto.clave_sat,
                'clave_unidad' : det.producto.unidad_medida.unidad_medida,
                'nombre_producto': det.producto.nombre,
                'tasa_iva' : det.tasa_iva,
                'tasa_ieps' : det.tasa_ieps,
                'tasa_retencion_iva' : det.tasa_retencion_iva,
                'tasa_retencion_isr' : det.tasa_retencion_isr,
                'iva_producto': det.iva_producto,
                'ieps_producto': det.ieps_producto,
                'retencion_iva': det.retencion_iva,
                'retencion_isr': det.retencion_isr,
            })
            
        return JsonResponse(data)
    except Remision.DoesNotExist:
        return JsonResponse({'error': 'No se encontró la remisión'}, status=404)

import requests
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse
"""
En 2025, los MOTIVOS DE CANCELACION de CFDI (Comprobante Fiscal Digital por Internet) se clasifican
 en cuatro categorías principales, según el Servicio de Administración Tributaria (SAT): 
1. Comprobante emitido con errores con relación (01):
Se utiliza cuando la factura original contiene errores y se requiere emitir 
una nueva factura que la sustituya. Se debe indicar el folio fiscal de la nueva 
factura que reemplaza a la original.
2. Comprobante emitido con errores sin relación (02):
Se usa cuando la factura original tiene errores, pero no es necesario emitir una 
nueva factura que la sustituya. Por ejemplo, si la factura se duplicó por error.
3. No se llevó a cabo la operación (03):
Se aplica cuando la operación comercial que amparaba el CFDI no se realizó. 
Esto implica que el ingreso registrado en la factura debe eliminarse de la contabilidad.
4. Operación nominativa relacionada en factura global (04):
Se utiliza cuando una venta que inicialmente se incluyó en una factura global 
(a público en general) posteriormente se requiere facturar de manera individual 
para un cliente específico. En este caso, se cancela la parte correspondiente 
de la factura global y se emite un nuevo CFDI individual. 
"""
# CANCELAR FACTURA TIMBRADA
class CancelarFacturaView(TenantRequiredMixin, View):
    def post(self, request, pk):
        # factura = get_object_or_404(Factura, pk=pk)
        db_name = request.db_name  # ← viene del decorador tenant_required

        factura = get_object_or_404(
            Factura.objects.using(db_name),
            pk=pk,
        )

        if not factura.uuid:
            messages.error(request, "La factura no tiene UUID y no puede ser cancelada.")
            return redirect('fac:factura_list')

        url = f"https://dev.techbythree.com/api/v1/facturacion/cancelar/{factura.uuid}"
        payload = {
            "motivo": "02",
            "folio_sustitucion": ""
        }
        headers = {
            "Authorization": f"Bearer {settings.PAC_API_TOKEN}",
            "X-CLIENT-ID": settings.PAC_CLIENT_ID,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            resp = requests.delete(url, json=payload, headers=headers)
            if resp.status_code == 200:
                factura.estatus = 'Cancelada'
                factura.fecha_cancelacion = timezone.now()
                factura.save(
                    using=self.db_name
                )

                messages.success(request, f"Factura: {factura.numero_factura} cancelada correctamente.")
            else:
                messages.error(request, f"Error al cancelar factura: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(str(e))
            messages.error(request, f"Error de conexión con el PAC: {str(e)}")

        return redirect('fac:factura_list')
