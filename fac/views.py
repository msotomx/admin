from django.shortcuts import render

# Create your views here.

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from fac.models import Factura, DetalleFactura
from fac.forms import FacturaForm, DetalleFacturaFormSet
from inv.models import Producto
from django.utils.timezone import now, localtime
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView, UpdateView

# CRUD FACTURAS ==================
class FacturaBaseView:
    def procesar_formset(self, formset, factura):
        detalles_dict = {}
        monto_total = 0

        for detalle_form in formset:
            if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                producto = detalle_form.cleaned_data['producto']
                clave_prod_serv = detalle_form.cleaned_data['clave_prod_serv']
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
                        'clave_prod_serv' : clave_prod_serv,
                        'cantidad': cantidad,
                        'precio': precio,
                        'descuento': descuento,
                        'subtotal': subtotal,
                    }

        factura.detalles.all().delete()

        for detalle in detalles_dict.values():
            DetalleFactura.objects.create(
                numero_factura=factura,
                producto=detalle['producto'],
                clave_prod_serv=['clave_prod_serv'],
                cantidad=detalle['cantidad'],
                precio=detalle['precio'],
                descuento=detalle['descuento'],
                subtotal=detalle['subtotal'],
            )
            monto_total += detalle['subtotal']

        factura.total = monto_total
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

        initial['fecha_emision'] = localtime(now()).date()
        initial['fecha_creacion'] = localtime(now()).date()
        initial['serie_emisor'] = '021'  
        initial['serie_sat'] = '022'
        initial['fecha_hora_certificacion'] = '023'
        initial['lugar_expedicion'] = '024'
        initial['tipo_cambio'] = 1
        initial['tipo_comprobante'] = 'I'
        initial['exportacion'] = 1
        initial['xml'] = ''
        initial['pdf'] = ''

        # Información de timbrado
        initial['uuid'] = ''
        initial['fecha_timbrado'] = ''
        initial['sello_cfdi'] = ''
        initial['no_certificado_sat'] = ''
        initial['estatus'] = 'B' # BORRADOR TIMBRADO CANCELADO
        initial['fecha_creacion'] = localtime(now()).date()
        initial['subtotal'] = 0
        initial['descuento'] = 0
        initial['total'] = 0
        initial['moneda'] = 1
        return initial

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        formset = DetalleFacturaFormSet(queryset=DetalleFactura.objects.none(), prefix='detalles')
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleFacturaFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.usuario = self.request.user
            self.object.status = 'B'
            numero_factura = form.cleaned_data.get('numero_factura')

            if numero_factura:
                self.object.numero_factura = str(numero_factura).zfill(7)

            self.object.save()

            # Aquí se usa la lógica compartida
            self.procesar_formset(formset, self.object)

            return redirect('fac:factura_list')

        return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return render(self.request, self.template_name, {'form': form, 'formset': formset})
    

class FacturaUpdateView(FacturaBaseView, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'fac/factura_form.html'
    success_url = reverse_lazy('fac:factura_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        formset = DetalleFacturaFormSet(instance=self.object,prefix='detalles')

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = DetalleFacturaFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            self.procesar_formset(formset, self.object)
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'formset': formset})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['numero_factura'].widget.attrs['readonly'] = True
        return form

# DETALLE DE MOVIMIENTO DE REMISIONES
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'fac/factura_detail.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleFactura.objects.filter(numero_remision=self.object)
        return context

class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'fac/factura_confirm_delete.html'
    success_url = reverse_lazy('fac:factura_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all()
        return context

def verificar_factura(request):
    numero_factura = request.GET.get('numero_factura')

    try:
        factura = Factura.objects.get(numero_factura=numero_factura)
        return JsonResponse({'existe': True, 'id': factura.id})
    except Factura.DoesNotExist:
        return JsonResponse({'existe': False})

def obtener_clave_prod_serv(request):
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
