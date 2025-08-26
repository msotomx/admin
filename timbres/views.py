from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from decimal import Decimal
from django.views.generic.edit import FormView
from decouple import config
from django.utils.timezone import now, localtime
from django.views.generic import ListView, CreateView
from core.mixins import TenantRequiredMixin
from core.decorators import tenant_required
from core.models import Empresa, EmpresaDB
from timbres.models import MovimientoTimbresGlobal, TimbresCliente
from timbres.forms import AsignarTimbresForm
from django.db.models import Q
from django.conf import settings

# Create your views here.

@login_required
@tenant_required
def obtener_ultima_referencia_timbres(request):
    ultima = MovimientoTimbresGlobal.objects.using('default').filter(tipo='S').order_by('-referencia').first()
    if ultima and ultima.referencia.isdigit():
        siguiente = str(int(ultima.referencia) + 1).zfill(7)
    else:
        siguiente = "0000001"
    
    return siguiente

# =====================
from django.db.models import Sum, F
from django.contrib.auth.mixins import LoginRequiredMixin
from core.decorators import staff_required

class MovimientoTimbresGlobalListView(LoginRequiredMixin,ListView):
    model = MovimientoTimbresGlobal
    template_name = 'timbres/timbres_movimiento_list.html'
    context_object_name = 'timbres'
    queryset = MovimientoTimbresGlobal.objects.using('default').order_by('-fecha')
    
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

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        # Primero obtenemos todas las facturas
        timbres = MovimientoTimbresGlobal.objects.using('default').all()

        if query:
            # Aplicamos filtros si hay búsqueda
            timbres = timbres.filter(
                Q(codigo_empresa__icontains=query)
            )
        
        # Finalmente, ordenamos en orden descendente por numero_factura
        return timbres.order_by('-fecha')

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.timezone import localtime, now
from timbres.forms import EntradaTimbreForm

class EntradaTimbreCreateView(LoginRequiredMixin,CreateView):
    model = MovimientoTimbresGlobal
    form_class = EntradaTimbreForm
    template_name = 'timbres/timbres_entradas_form.html'
    success_url = reverse_lazy('timbres:timbres_movimiento_list')

    def form_valid(self, form):

        try:
            obj = form.save(commit=False)
            obj.codigo_empresa = "0000000"
            obj.usuario = self.request.user.username
            user_autorizado = config('USER_TIMBRES')
            if obj.usuario == user_autorizado:

                obj.tipo = "E"
                obj.referencia = obj.referencia.zfill(7)
                obj.fecha = localtime(now()).date()
                if obj.cantidad and obj.importe:
                    obj.precio_unit = obj.importe / obj.cantidad
                else:
                    obj.precio_unit = 0

                obj.save(using='default')
                messages.success(self.request, "Compra Registrada Correctamente.")
            else:
                messages.error(self.request, "Usuario no autorizado para registrar timbres.")
                return redirect('timbres:timbres_movimiento_list')
                
        except Exception as e:
            print("ERROR EN FORM_VALID:", e)
            raise
    
        return redirect(self.success_url)

    def form_invalid(self, form):
        print("❌ Errores del formulario:", form.errors)

        return super().form_invalid(form)

# asignar timbres al cliente
# 1 - graba movimiento
# 2 - genera disponibles para el codigo_empresa

class MovimientoTimbresCreateView(LoginRequiredMixin,CreateView):
    model = MovimientoTimbresGlobal
    form_class = AsignarTimbresForm
    template_name = 'timbres/asignar_timbres.html'
    success_url = reverse_lazy('timbres:timbres_movimiento_list')

    def form_valid(self, form):
        try:
            # Crear instancia pero no guardar aún
            movimiento = form.save(commit=False)
            movimiento.codigo_empresa = movimiento.codigo_empresa.zfill(7)
            ee = EmpresaDB.objects.using('default').filter(codigo_empresa=movimiento.codigo_empresa).first()
            
            if ee:
                # Asignar valores adicionales
                movimiento.usuario = self.request.user.username

                user_autorizado = config('USER_TIMBRES')
                if movimiento.usuario == user_autorizado:
                    if movimiento.referencia == config('REF_TIMBRES'):
                        movimiento.tipo = 'S'
                        movimiento.fecha = localtime(now()).date()
                        if movimiento.cantidad and movimiento.importe:
                            movimiento.precio_unit = movimiento.importe / movimiento.cantidad
                        else:
                            movimiento.precio_unit = 0

                        movimiento.referencia = obtener_ultima_referencia_timbres(self.request)
                            
                        c_empresa = movimiento.codigo_empresa
                        cantidad = Decimal(movimiento.cantidad)

                        # Guardar en la base de datos 'default'
                        movimiento.save(using='default')

                        #
                        # Actualizar la Tabla TimbresCliente
                        # 
                        timbre, creado = TimbresCliente.objects.get_or_create(
                            codigo_empresa=c_empresa,
                            defaults={
                                'total_asignados': cantidad,
                                'fecha_asignacion': localtime(now()).date(),
                                'utilizados': 0
                            }
                        )
                        if not creado:   # el registro ya existe
                            timbre.total_asignados += cantidad
                            fecha_asignacion = localtime(now()).date()
                            timbre.save(using='default')

                        messages.success(self.request, "Timbres asignados correctamente.")
                        return redirect('timbres:timbres_movimiento_list')
                    else:
                        messages.error(self.request, "Referencia Inválida.")
                        return redirect('timbres:timbres_movimiento_list')
                else:
                    messages.error(self.request, "Usuario no autorizado para asignar timbres.")
                    return redirect('timbres:timbres_movimiento_list')
            else:
                messages.error(self.request, "Codigo de Empresa no Registrado.")
                return redirect('timbres:timbres_movimiento_list')


        except Exception as e:
            print("❌ EXCEPCIÓN atrapada en form_valid:", str(e))
            messages.error(self.request, "Error inesperado, no se guardaron timbres.")
            return self.form_invalid(form)  # Para que Django vuelva a renderizar con errores

    def form_invalid(self, form):
        print("❌ Errores del formulario:", form.errors)
        messages.error(self.request, "Ocurrió un error al asignar los timbres. Revisa los datos.")
        return super().form_invalid(form)

@login_required
def timbres_solicitar(request):
    empresa = Empresa.objects.using('tenant').first()
    
    timbres = TimbresCliente.objects.using('default').filter(codigo_empresa=empresa.codigo_empresa).first()
    if timbres:
        disponibles = timbres.total_asignados - timbres.utilizados
    else:
        disponibles = 0

    celular = settings.CELULAR
    contexto = {
        'codigo_empresa': empresa.codigo_empresa,
        'disponibles': disponibles,
        'celular': celular
    }

    return render(request, 'timbres/timbres_solicitar.html', contexto)

