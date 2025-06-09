from django.shortcuts import render

# Create your views here.

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Empresa
from fac.models import Factura, DetalleFactura, TipoComprobante, Exportacion
from inv.models import Producto, Moneda, ClaveMovimiento
from cxc.models import Cliente
from fac.forms import FacturaForm, DetalleFacturaFormSet, DetalleFacturaForm
from django.utils.timezone import now, localtime
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.forms import modelformset_factory
from django.views.decorators.http import require_GET

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
        empresa = getattr(self.request.user, 'empresa', None)

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
                objeto_imp     = '02',
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
        factura.descuento            = descuento_total
        factura.iva_factura          = iva_total
        factura.ieps_factura         = ieps_total
        factura.retencion_iva_factura= retencion_iva_total
        factura.retencion_isr_factura= retencion_isr_total
        factura.impuestos_trasladados= iva_total + ieps_total
        factura.impuestos_retenidos  = retencion_iva_total + retencion_isr_total
        factura.total                = subtotal_total + iva_total + ieps_total \
                                        - retencion_iva_total - retencion_isr_total
        factura.fecha_creacion       = localtime(now()).date()
        factura.save()

class FacturaListView(ListView):
    model = Factura
    template_name = 'fac/factura_list.html'
    context_object_name = 'facturas'
    ordering = ['-fecha_emision', '-numero_factura']  # Orden descendente por fecha
    paginate_by = 10  # Número de movimientos por página

from decimal import Decimal
class FacturaCreateView(FacturaBaseView, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'fac/factura_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = getattr(self.request.user, 'empresa', None)
        
        if empresa.clave_remision:
            try:
                clave_remision = ClaveMovimiento.objects.get(clave_movimiento=empresa.clave_remision)
                initial['clave_remision'] = clave_remision.id

            except ClaveMovimiento.DoesNotExist:
                print("No se encontró la Clave de Remision", empresa.clave_remision)

        initial['numero_remision'] = '0000000'  
        initial['fecha_emision'] = localtime(now()).date()
        initial['fecha_creacion'] = localtime(now()).date()
        
        initial['serie_emisor'] = ''  

        initial['serie_sat'] = ''
        initial['fecha_hora_certificacion'] = ''
        initial['lugar_expedicion'] = ''
        initial['tipo_cambio'] = 1
        moneda_mxn = Moneda.objects.filter(clave="MXN").first()
        if moneda_mxn:
            initial['moneda'] = moneda_mxn.id

        tipo_comprobante = TipoComprobante.objects.filter(tipo_comprobante='I').first()
        initial['tipo_comprobante'] = tipo_comprobante.id
        initial['exportacion'] = Exportacion.objects.filter(exportacion='01').first()
        initial['condiciones_pago'] = '1'
        initial['xml'] = ''
        initial['pdf'] = ''

        # Información de timbrado
        initial['uuid'] = ''
        initial['fecha_timbrado'] = ''
        initial['sello_cfdi'] = ''
        initial['no_certificado_sat'] = ''
        initial['estatus'] = 'BORRADOR' # BORRADOR TIMBRADO CANCELADO
        initial['subtotal'] = 0
        initial['descuento'] = 0
        initial['total'] = 0
        return initial

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        formset = DetalleFacturaFormSet(queryset=DetalleFactura.objects.none(), prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleFacturaFormSet(request.POST, prefix='detalles')
        
        if form.is_valid() and formset.is_valid():
            return self.guardar_factura_y_detalles(form, formset)

        return self.form_invalid(form, formset)

    from django.db import transaction
    @transaction.atomic
    def guardar_factura_y_detalles(self, form, formset):
        factura = form.save(commit=False)

        # Asignaciones obligatorias
        factura.usuario = self.request.user
        factura.empresa = getattr(self.request.user, 'empresa', None)
        print("factura.empresa:", factura.empresa)

        # Asignar moneda MXN si no viene del formulario
        if not factura.moneda:
            moneda_mxn = Moneda.objects.filter(clave="MXN").first()
            if not moneda_mxn:
                form.add_error(None, "No se encontró la moneda MXN en la base de datos.")
                return self.form_invalid(form, formset)
            factura.moneda = moneda_mxn

        # Asegurar tipo de comprobante
        if not factura.tipo_comprobante:
            tipo_comp = TipoComprobante.objects.filter(tipo_comprobante='I').first()
            if not tipo_comp:
                form.add_error(None, "No se encontró el tipo de comprobante 'I'.")
                return self.form_invalid(form, formset)
            factura.tipo_comprobante = tipo_comp

        # Defaults si están vacíos
        factura.serie_emisor = factura.serie_emisor or '000'
        factura.serie_sat = factura.serie_sat or '000'
        factura.fecha_hora_certificacion = factura.fecha_hora_certificacion or now()
        factura.lugar_expedicion = factura.lugar_expedicion or '00000'
        factura.tipo_cambio = factura.tipo_cambio or Decimal('1.00')
        factura.exportacion = factura.exportacion or Exportacion.objects.filter(exportacion='01').first()
        factura.condiciones_pago = factura.condiciones_pago or '1'
        factura.estatus = factura.estatus or 'BORRADOR'
        factura.subtotal = factura.subtotal or Decimal('0.00')
        factura.descuento = factura.descuento or Decimal('0.00')
        factura.total = factura.total or Decimal('0.00')
        factura.iva_factura = factura.iva_factura or Decimal('0.00')
        factura.ieps_factura = factura.ieps_factura or Decimal('0.00')
        factura.retencion_iva_factura = factura.retencion_iva_factura or Decimal('0.00')
        factura.retencion_isr_factura = factura.retencion_isr_factura or Decimal('0.00')

        factura.save()
        # procesar detalles
        self.procesar_formset(formset, factura)
        
        return redirect('fac:factura_list')

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

class FacturaUpdateView(FacturaBaseView, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'fac/factura_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form    = self.get_form()
        formset = DetalleFacturaFormSet(instance=self.object, prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form    = self.get_form()
        formset = DetalleFacturaFormSet(request.POST, instance=self.object, prefix='detalles')

        print("→ POST recibido. form.is_valid():", form.is_valid())
        print("→ Errores form:", form.errors)
        print("→ formset.is_valid():", formset.is_valid())
        print("→ Errores formset:", formset.errors)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    @transaction.atomic
    def form_valid(self, form, formset):
        # Guarda la factura principal
        factura = form.save(commit=False)
        factura.empresa = self.request.user.empresa
        print("factura.empresa:", factura.empresa)

        factura.save()

        # Recalcula y graba los detalles usando tu lógica centralizada
        self.procesar_formset(formset, factura)

        return redirect('fac:factura_list')

    def form_invalid(self, form, formset):
        # Puedes reutilizar tu método de manejo de errores
        messages.error(self.request, "Hay errores en el formulario. Por favor revísalos.")
        print("Errores del form principal:", form.errors)
        print("Errores del formset:")
        for i, f in enumerate(formset):
            if f.errors:
                print(f"Errores en el formulario #{i}:", f.errors.as_data())

        return render(self.request, self.template_name, {'form': form, 'formset': formset})

# VER FACTURA CUANDO YA ESTA TIMBRADA 
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'fac/factura_detail.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleFactura.objects.filter(numero_remision=self.object)
        return context

from django.views.generic import DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Factura

class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'fac/factura_confirm_delete.html'
    success_url = reverse_lazy('fac:factura_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.estatus not in ['BORRADOR', 'ERROR']:
            messages.warning(request, "Solo se pueden eliminar facturas en estatus BORRADOR o ERROR.")
            return redirect('fac:factura_list')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Factura eliminada correctamente.")
        return super().delete(request, *args, **kwargs)

# FUNCION PARA VALIDAR SI UNA FACTURA YA EXISTE
def verificar_factura(request):
    numero_factura = request.GET.get('numero_factura')

    try:
        factura = Factura.objects.get(numero_factura=numero_factura)
        return JsonResponse({'existe': True, 'id': factura.id})
    except Factura.DoesNotExist:
        return JsonResponse({'existe': False})

def obtener_clave_prod_serv2(request):
    producto_id = request.GET.get('producto_id')
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'clave_prod_serv': producto.clave_sat})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def obtener_ultimo_numero_factura(request):
    ultima = Factura.objects.all().order_by('-numero_factura').first()
    if ultima and ultima.numero_factura.isdigit():
        siguiente = str(int(ultima.numero_factura) + 1).zfill(7)
    else:
        siguiente = "0000001"
    
    return JsonResponse({'numero_factura': siguiente})

# ESTA FUNCION SE UTILIZA EN GENERAR CFDI
@require_GET
def obtener_tasa_empresa(request):
    cliente_id = request.GET.get('cliente_id')
    # 1) Validar que se recibió cliente_id
    if not cliente_id or not cliente_id.isdigit():
        return JsonResponse({'error': 'Parámetro cliente_id inválido'}, status=400)

    # 2) Obtener la empresa asociada al usuario
    empresa = getattr(request.user, 'empresa', None)
    if not empresa:
        return JsonResponse({'error': 'Usuario sin empresa asignada'}, status=403)

    # 3) Extraer tasas de la empresa
    tasa_iva      = float(empresa.tasa_iva)
    tasa_ieps     = float(empresa.tasa_ieps)
    ret_iva       = float(empresa.tasa_retencion_iva)
    ret_isr       = float(empresa.tasa_retencion_isr)

    # 4) Ajustar según configuración del cliente
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
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
from django.utils import timezone
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

# Esta función toma el objeto Factura y construye el JSON que se enviará al PAC para timbrar.
def generar_json_cfdi(factura):
    cliente = factura.cliente
    detalles = factura.detalles.all()

    conceptos = []
    for detalle in detalles:
        conceptos.append({
            "clave_prod_serv": detalle.clave_prod_serv,
            "cantidad": float(detalle.cantidad),
            "clave_unidad": detalle.clave_unidad,
            "unidad": detalle.producto.unidad_medida.nombre,
            "descripcion": detalle.descripcion,
            "valor_unitario": float(detalle.valor_unitario),
            "importe": float(detalle.importe),
            "descuento": float(detalle.descuento),
            "objeto_imp": detalle.objeto_imp,
            "impuestos": {
                "traslados": [
                    {
                        "base": float(detalle.importe - detalle.descuento),
                        "impuesto": "002",  # IVA
                        "tipo_factor": "Tasa",
                        "tasa_o_cuota": float(detalle.tasa_iva) / 100,
                        "importe": float(detalle.iva),
                    }
                ]
            }
        })

    json_cfdi = {
        "receptor": {
            "rfc": cliente.rfc,
            "nombre": cliente.nombre,
            "domicilio": {
                "calle": cliente.calle,
                "no_exterior": cliente.numero_exterior,
                "no_interior": cliente.numero_interior,
                "colonia": cliente.colonia,
                "municipio": cliente.municipio,
                "estado": cliente.estado,
                "pais": "México",
                "codigo_postal": cliente.codigo_postal
            },
            "residencia_fiscal": "MX",
            "uso_cfdi": factura.uso_cfdi.clave,
            "regimen_fiscal_receptor": cliente.regimen_fiscal.clave if cliente.regimen_fiscal else "",
        },
        "informacion_global": {},
        "tipo_comprobante": factura.tipo_comprobante.clave,
        "exportacion": factura.exportacion.clave,
        "forma_pago": factura.forma_pago.clave,
        "metodo_pago": factura.metodo_pago.clave,
        "moneda": factura.moneda.clave,
        "tipo_cambio": float(factura.tipo_cambio),
        "lugar_expedicion": factura.lugar_expedicion,
        "subtotal": float(factura.subtotal),
        "descuento": float(factura.descuento),
        "total": float(factura.total),
        "conceptos": conceptos,
        "impuestos": {
            "traslados": [
                {
                    "impuesto": "002",
                    "tipo_factor": "Tasa",
                    "tasa_o_cuota": 0.16,
                    "importe": float(factura.impuestos_trasladados)
                }
            ]
        }
    }

    return json_cfdi

# Esta función obtiene la factura y llama a la función generar_json_cfdi
def generar_json_timbrado(factura_id):
    from .models import Factura  # Importación interna para evitar problemas circulares

    factura = Factura.objects.select_related(
        'cliente', 'forma_pago', 'moneda', 'metodo_pago',
        'uso_cfdi', 'tipo_comprobante', 'exportacion',
        'cliente__regimen_fiscal'
    ).prefetch_related('detalles__producto', 'detalles')

    factura = factura.get(pk=factura_id)

    return generar_json_cfdi(factura)

import os
from django.core.files.base import ContentFile

def guardar_archivos_factura(factura, xml_bytes, pdf_bytes, uuid=None):
    """
    Guarda los archivos XML y PDF en la factura y actualiza el estatus y fecha de timbrado.
    """
    # Nombres únicos para los archivos
    base_filename = f"{factura.numero_factura}_{factura.cliente.rfc}_{now().strftime('%Y%m%d%H%M%S')}"
    
    xml_filename = f"{base_filename}.xml"
    pdf_filename = f"{base_filename}.pdf"

    # Guardar archivos usando ContentFile
    factura.xml.save(xml_filename, ContentFile(xml_bytes), save=False)
    factura.pdf.save(pdf_filename, ContentFile(pdf_bytes), save=False)

    # Timbrado exitoso
    factura.estatus = "TIMBRADA"
    factura.fecha_timbrado = localtime(now())

    # Guardar UUID si viene del PAC
    if uuid:
        factura.uuid = uuid

    # Guardar cambios
    factura.save()

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

def timbrar_factura(factura_id):
    try:
        factura = Factura.objects.get(pk=factura_id)

        # 1. Generar JSON CFDI
        json_cfdi = generar_json_cfdi(factura)

        # 2. Preparar headers y endpoint del PAC
        url = "https://api.demo.pac.com.mx/v1/cfdi40/generar"  # Ajusta según tu PAC real
        headers = {
            "Authorization": f"Bearer {settings.PAC_TOKEN}",  # variable en settings
            "Content-Type": "application/json"
        }

        # 3. Enviar al PAC
        response = requests.post(url, json=json_cfdi, headers=headers)

        # 4. Procesar respuesta
        if response.status_code == 200:
            data = response.json()

            factura.uuid = data.get("uuid")
            factura.sello_cfdi = data.get("selloCFDI", "")
            factura.no_certificado_sat = data.get("noCertificadoSAT", "")
            factura.fecha_timbrado = localtime(now())
            factura.estatus = "TIMBRADA"

            # Guardar XML
            xml_content = data.get("cfdiXml")
            if xml_content:
                factura.xml.save(f'{factura.numero_factura}.xml', ContentFile(xml_content.encode('utf-8')), save=False)

            # Guardar PDF (si lo envía el PAC)
            pdf_base64 = data.get("pdf")
            if pdf_base64:
                import base64
                pdf_data = base64.b64decode(pdf_base64)
                factura.pdf.save(f'{factura.numero_factura}.pdf', ContentFile(pdf_data), save=False)

            factura.save()
            return {"success": True, "uuid": factura.uuid}

        else:
            factura.estatus = "ERROR"
            factura.save()
            return {"success": False, "error": response.text}

    except Factura.DoesNotExist:
        return {"success": False, "error": "Factura no encontrada"}

    except Exception as e:
        factura.estatus = "ERROR"
        factura.save()
        return {"success": False, "error": str(e)}
