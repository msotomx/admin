from django.urls import path
from . import views
from .views import MonedaListView, MonedaCreateView, MonedaUpdateView, MonedaDeleteView
from .views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from .views import UnidadMedidaListView, UnidadMedidaCreateView, UnidadMedidaUpdateView, UnidadMedidaDeleteView
from .views import AlmacenListView, AlmacenCreateView, AlmacenUpdateView, AlmacenDeleteView
from .views import ClavesMovListView, ClavesMovCreateView, ClavesMovUpdateView, ClavesMovDeleteView
from .views import ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView

app_name = 'inv'

urlpatterns = [
    # path('', views.index, name='index'),
    path('monedas/', MonedaListView.as_view(), name='moneda_list'),
    path('monedas/nueva/', MonedaCreateView.as_view(), name='moneda_create'),
    path('monedas/<int:pk>/editar/', MonedaUpdateView.as_view(), name='moneda_update'),
    path('monedas/<int:pk>/eliminar/', MonedaDeleteView.as_view(), name='moneda_delete'),
    path('categoria/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/nueva/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('unidadmedida/', UnidadMedidaListView.as_view(), name='unidadmedida_list'),
    path('unidadmedida/nueva/', UnidadMedidaCreateView.as_view(), name='unidadmedida_create'),
    path('unidadmedida/<int:pk>/editar/', UnidadMedidaUpdateView.as_view(), name='unidadmedida_update'),
    path('unidadmedida/<int:pk>/eliminar/', UnidadMedidaDeleteView.as_view(), name='unidadmedida_delete'),
    path('almacen/', AlmacenListView.as_view(), name='almacen_list'),
    path('almacen/nueva/', AlmacenCreateView.as_view(), name='almacen_create'),
    path('almacen/<int:pk>/editar/', AlmacenUpdateView.as_view(), name='almacen_update'),
    path('almacen/<int:pk>/eliminar/', AlmacenDeleteView.as_view(), name='almacen_delete'),
    path('clavemovimiento/', ClavesMovListView.as_view(), name='clavemovimiento_list'),
    path('clavemovimiento/nueva/', ClavesMovCreateView.as_view(), name='clavemovimiento_create'),
    path('clavemovimiento/<int:pk>/editar/', ClavesMovUpdateView.as_view(), name='clavemovimiento_update'),
    path('clavemovimiento/<int:pk>/eliminar/', ClavesMovDeleteView.as_view(), name='clavemovimiento_delete'),
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
]
