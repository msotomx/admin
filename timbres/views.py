from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from decimal import Decimal
from django.views.generic.edit import FormView
from django.utils.timezone import now, localtime
from django.views.generic import ListView, CreateView
from core.mixins import TenantRequiredMixin
from core.decorators import tenant_required
from timbres.forms import AsignarTimbresForm
from timbres.models import MovimientoTimbresGlobal

# Create your views here.

@login_required
@tenant_required
def obtener_ultima_referencia_timbres():
    ultima = MovimientoTimbresGlobal.objects.using('default').all().order_by('-referencia').first()
    if ultima and ultima.referencia.isdigit():
        siguiente = str(int(ultima.referencia) + 1).zfill(7)
    else:
        siguiente = "0000001"
    
    return siguiente

from django.db.models import Sum, F

class MovimientoTimbresGlobalListView(TenantRequiredMixin, ListView):
    model = MovimientoTimbresGlobal
    template_name = 'timbres/timbres_movimiento_list.html'
    context_object_name = 'movimientos'
    queryset = MovimientoTimbresGlobal.objects.using('default').order_by('-fecha')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entradas = MovimientoTimbresGlobal.objects.using('default').filter(tipo='E').aggregate(total=Sum('cantidad'))['total'] or 0
        salidas = MovimientoTimbresGlobal.objects.using('default').filter(tipo='S').aggregate(total=Sum('cantidad'))['total'] or 0
        disponibles = entradas - salidas

        context.update({
            'entradas': entradas,
            'salidas': salidas,
            'disponibles': disponibles
        })
        return context

# compra/entrada de timbres global
class CompraTimbresGlobalCreateView(TenantRequiredMixin, CreateView):
    model = MovimientoTimbresGlobal
    template_name = 'timbres/timbres_entradas_form.html'
    fields = ['referencia', 'cantidad', 'importe']

    def form_valid(self, form):
        print("[CompraTimbresGlobal]")
        form.instance.tipo = 'E'
        form.instance.fecha = localtime(now()).date()
        form.instance.precio_unit = form.instance.importe / form.instance.cantidad
        print("[CompraTimbresGlobal]- antes de save")

        print("Campos del formulario:")
        for field_name, value in form.cleaned_data.items():
            print(f"{field_name}: {value}")

        form.instance.save(using='default')
        
        # Redirige al lugar correspondiente después de guardar
        return redirect('timbres:timbres_movimiento_list')

    def get_success_url(self):
        return reverse_lazy('timbres:timbres_movimiento_list')

from decimal import Decimal
from django.utils.timezone import localtime, now
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class MovimientoTimbresCreateView(FormView):
    template_name = 'timbres/asignar_timbres.html'
    form_class = AsignarTimbresForm

    def form_valid(self, form):
        try:
            # Mostrar datos del formulario
            print("✅ Campos del formulario (cleaned_data):")
            for field_name, value in form.cleaned_data.items():
                print(f"{field_name}: {value}")

            # Crear instancia pero no guardar aún
            movimiento = form.save(commit=False)

            # Asignar valores adicionales
            movimiento.usuario = self.request.user.username
            movimiento.tipo = 'S'  # Asignación de timbres
            movimiento.fecha = localtime(now()).date()
            movimiento.precio_unit = Decimal('1.00')
            # movimiento.referencia = obtener_ultima_referencia_timbres()

            print("✅ Objeto preparado para guardar:", movimiento)

            # Guardar en la base de datos 'default'
            movimiento.save(using='default')
            messages.success(self.request, "Timbres asignados correctamente.")
            return redirect('timbres:timbres_movimiento_list')

        except Exception as e:
            logger.exception("❌ Error en form_valid:")
            print("❌ EXCEPCIÓN atrapada en form_valid:", str(e))
            messages.error(self.request, "Error inesperado al guardar los datos.")
            return self.form_invalid(form)  # Para que Django vuelva a renderizar con errores

    def form_invalid(self, form):
        print("❌ Errores del formulario:", form.errors)
        messages.error(self.request, "Ocurrió un error al asignar los timbres. Revisa los datos.")
        return super().form_invalid(form)
