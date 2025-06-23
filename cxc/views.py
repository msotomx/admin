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

# CRUD TIPO DE CLIENTE
class TipoClienteListView(ListView):
    model = TipoCliente
    template_name = 'cxc/tipocliente_list.html'
    context_object_name = 'tiposcliente'

class TipoClienteCreateView(CreateView):
    model = TipoCliente
    form_class = TipoClienteForm
    template_name = 'cxc/tipocliente_form.html'
    success_url = reverse_lazy('cxc:tipocliente_list')

class TipoClienteUpdateView(UpdateView):
    model = TipoCliente
    form_class = TipoClienteForm
    template_name = 'cxc/tipocliente_form.html'
    success_url = reverse_lazy('cxc:tipocliente_list')

class TipoClienteDeleteView(DeleteView):
    model = TipoCliente
    template_name = 'cxc/tipocliente_confirm_delete.html'
    success_url = reverse_lazy('cxc:tipocliente_list')

# CRUD CLIENTE
class ClienteListView(ListView):
    model = Cliente
    template_name = 'cxc/cliente_list.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        # Primero obtenemos todas las facturas
        clientes = Cliente.objects.all()

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

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cxc/cliente_form.html'
    success_url = reverse_lazy('cxc:cliente_list')

    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']

        form.instance.cliente = str(cliente).zfill(6)
        return super().form_valid(form)

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cxc/cliente_form.html'
    success_url = reverse_lazy('cxc:cliente_list')

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'cxc/cliente_confirm_delete.html'
    success_url = reverse_lazy('cxc:cliente_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Cliente eliminado con éxito.")
        except RestrictedError:
            messages.error(request, "No se puede eliminar un cliente con movimientos.")
        except Exception as e:
            print("❌ Error inesperado al eliminar cliente:")
            print(traceback.format_exc())  # muestra traza completa
            messages.error(request, f"Error inesperado: {str(e)}")
        return redirect(self.success_url)

def obtener_ultimo_cliente(request):

    ultimo = Cliente.objects.all().order_by('-cliente').first()
    if ultimo:
        siguiente = str(int(ultimo.cliente) + 1).zfill(6)
    else:
        siguiente = "000001"
    return JsonResponse({'cliente': siguiente})
