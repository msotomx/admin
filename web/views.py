import os

from .models import Empresa, Categoria, TipoCliente, Almacen, Moneda
from .models import UnidadMedida, ClaveMovimiento, Proveedor, Producto
from .models import Cliente, Movimiento, DetalleMovimiento
from .models import Traspaso, DetalleTraspaso, Remision, DetalleRemision, SaldoInicial

from django.urls import reverse
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings
from django import template

register = template.Library()

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def productos(request):
    return render(request, 'web/productos.html')

def clientes(request):
    return render(request, 'web/clientes.html')

def index2(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()

    context = {
        'productos':listaProductos,
        'categorias':listaCategorias
    }
    return render(request,'index.html',context)
