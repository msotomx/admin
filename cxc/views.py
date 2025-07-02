from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoCliente, Cliente, ClaveMovimientoCxC, Cargo, Abono, SaldoInicialCxC
from .forms import TipoClienteForm, ClienteForm
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.deletion import RestrictedError
from core.mixins import TenantRequiredMixin
from django.contrib.auth.decorators import login_required
from core.decorators import tenant_required
from core._thread_locals import get_current_tenant

# CRUD TIPO DE CLIENTE
class TipoClienteListView(TenantRequiredMixin, ListView):
    model = TipoCliente
    template_name = 'cxc/tipocliente_list.html'
    context_object_name = 'tiposcliente'

    def get_queryset(self):
        db_name= get_current_tenant()
        return TipoCliente.objects.using(db_name).all()

class TipoClienteCreateView(TenantRequiredMixin, CreateView):
    model = TipoCliente
    form_class = TipoClienteForm
    template_name = 'cxc/tipocliente_form.html'
    success_url = reverse_lazy('cxc:tipocliente_list')

    def form_valid(self, form):
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class TipoClienteUpdateView(TenantRequiredMixin, UpdateView):
    model = TipoCliente
    form_class = TipoClienteForm
    template_name = 'cxc/tipocliente_form.html'
    success_url = reverse_lazy('cxc:tipocliente_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return TipoCliente.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class TipoClienteDeleteView(TenantRequiredMixin, DeleteView):
    model = TipoCliente
    template_name = 'cxc/tipocliente_confirm_delete.html'
    success_url = reverse_lazy('cxc:tipocliente_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return TipoCliente.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()
        self.object.delete(using=db_name)
        return super().delete(request, *args, **kwargs)

# CRUD CLIENTE
class ClienteListView(TenantRequiredMixin, ListView):
    model = Cliente
    template_name = 'cxc/cliente_list.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        db_name= get_current_tenant()
        # Primero obtenemos todas las facturas
        clientes = Cliente.objects.using(db_name).all()

        if query:
            # Aplicamos filtros si hay búsqueda
            clientes = clientes.filter(
                Q(nombre__icontains=query) |
                Q(rfc__icontains=query) |
                Q(cliente__icontains=query)
            )
        
        # Finalmente, ordenamos en orden descendente por numero_factura
        return clientes.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()  # para que se mantenga en el input
        return context

class ClienteCreateView(TenantRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cxc/cliente_form.html'
    success_url = reverse_lazy('cxc:cliente_list')

    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']

        form.instance.cliente = str(cliente).zfill(6)
        db_name= get_current_tenant()
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant

        return super().form_valid(form)

class ClienteUpdateView(TenantRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cxc/cliente_form.html'
    success_url = reverse_lazy('cxc:cliente_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Cliente.objects.using(db_name).filter(id=self.kwargs['pk'])  # Filtramos por la ID de la moneda

    def form_valid(self, form):
        # Obtenemos el nombre de la base de datos del tenant
        db_name= get_current_tenant()
        
        # Guarda el objeto en la base de datos del tenant
        form.instance.save(using=db_name)  # Guarda en la base de datos del tenant
        
        # Redirige al lugar correspondiente después de guardar
        return super().form_valid(form)

class ClienteDeleteView(TenantRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cxc/cliente_confirm_delete.html'
    success_url = reverse_lazy('cxc:cliente_list')

    def get_queryset(self):
        db_name= get_current_tenant()
        return Cliente.objects.using(db_name).filter(id=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        # Elimina el objeto en la base del tenant
        self.object = self.get_object()
        db_name= get_current_tenant()

        try:
            self.object.delete(using=db_name)
            messages.success(request, "Cliente eliminado con éxito.")
        except RestrictedError:
            messages.error(request, "No se puede eliminar un cliente con movimientos.")
        except Exception as e:
            print("❌ Error inesperado al eliminar cliente:")
            messages.error(request, f"Error inesperado: {str(e)}")
        return redirect(self.success_url)

@login_required
@tenant_required
def obtener_ultimo_cliente(request):
    db_name= get_current_tenant()
    ultimo = Cliente.objects.using(db_name).all().order_by('-cliente').first()
    if ultimo:
        siguiente = str(int(ultimo.cliente) + 1).zfill(6)
    else:
        siguiente = "000001"
    return JsonResponse({'cliente': siguiente})
