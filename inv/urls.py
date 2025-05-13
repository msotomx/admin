from django.urls import path
#from . import views
from .views import MonedaListView, MonedaCreateView, MonedaUpdateView, MonedaDeleteView
from .views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from .views import UnidadMedidaListView, UnidadMedidaCreateView, UnidadMedidaUpdateView, UnidadMedidaDeleteView
from .views import AlmacenListView, AlmacenCreateView, AlmacenUpdateView, AlmacenDeleteView
from .views import ClavesMovListView, ClavesMovCreateView, ClavesMovUpdateView, ClavesMovDeleteView
from .views import ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from .views import MovimientoListView, MovimientoCreateView, MovimientoUpdateView, MovimientoDeleteView, MovimientoDetailView
from .views import RemisionListView, RemisionCreateView, RemisionUpdateView, RemisionDeleteView, RemisionDetailView
from .views import verificar_movimiento, obtener_costo_producto
from .views import verificar_remision, obtener_precio_producto
from .views import obtener_ultimo_numero_remision, obtener_ultimo_movimiento
from .views import remisiones_por_dia, remisiones_por_cliente, buscar_remisiones_por_cliente

app_name = 'inv'

urlpatterns = [
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
    path('almacen/editar/<int:pk>/', AlmacenUpdateView.as_view(), name='almacen_update'),
    path('almacen/eliminar/<int:pk>/', AlmacenDeleteView.as_view(), name='almacen_delete'),
    path('clavemovimiento/', ClavesMovListView.as_view(), name='clavemovimiento_list'),
    path('clavemovimiento/nueva/', ClavesMovCreateView.as_view(), name='clavemovimiento_create'),
    path('clavemovimiento/editar/<int:pk>/', ClavesMovUpdateView.as_view(), name='clavemovimiento_update'),
    path('clavemovimiento/eliminar/<int:pk>/', ClavesMovDeleteView.as_view(), name='clavemovimiento_delete'),
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
    path('producto/', ProductoListView.as_view(), name='producto_list'),
    path('producto/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('movimiento/', MovimientoListView.as_view(), name='movimiento_list'),
    path('movimiento/nuevo/', MovimientoCreateView.as_view(), name='movimiento_create'),
    path('movimiento/editar/<int:pk>/', MovimientoUpdateView.as_view(), name='movimiento_update'),
    path('movimiento/eliminar/<int:pk>/', MovimientoDeleteView.as_view(), name='movimiento_delete'),
    path('movimiento/<int:pk>/', MovimientoDetailView.as_view(), name='movimiento_detail'),
    path('verificar-movimiento/', verificar_movimiento, name='verificar_movimiento'),
    path('obtener_costo_producto/', obtener_costo_producto, name='obtener_costo_producto'),
    path('remision/', RemisionListView.as_view(), name='remision_list'),
    path('remision/nuevo/', RemisionCreateView.as_view(), name='remision_create'),
    path('remision/editar/<int:pk>/', RemisionUpdateView.as_view(), name='remision_update'),
    path('remision/eliminar/<int:pk>/', RemisionDeleteView.as_view(), name='remision_delete'),
    path('remision/<int:pk>/', RemisionDetailView.as_view(), name='remision_detail'),
    path('verificar-remision/', verificar_remision, name='verificar_remision'),
    path('obtener_precio_producto/', obtener_precio_producto, name='obtener_precio_producto'),
    path('ajax/numero-remision/', obtener_ultimo_numero_remision, name='ajax_numero_remision'),
    path('ajax/numero-movimiento/', obtener_ultimo_movimiento, name='ajax_numero_movimiento'),
    path('reportes/remisiones_por_dia/', remisiones_por_dia, name='remisiones_por_dia'),
    path('reportes/remisiones_por_cliente/', remisiones_por_cliente, name='remisiones_por_cliente'),
    path('reportes/buscar_remisiones_cliente/', buscar_remisiones_por_cliente, name='buscar_remisiones_cliente'),
]

