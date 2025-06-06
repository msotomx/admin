from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TipoCliente, Cliente, ClaveMovimientoCxC, Cargo, Abono, SaldoInicialCxC
from .forms import TipoClienteForm, ClienteForm

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
    ordering = ['nombre']  

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cxc/cliente_form.html'
    success_url = reverse_lazy('cxc:cliente_list')

    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']
        print("retencion_iva:",form.instance.retencion_iva)
        print("retencion_isr:",form.instance.retencion_isr)
        print("ieps:",form.instance.ieps)

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
