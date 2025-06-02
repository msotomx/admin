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
from .views import CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView, CompraDetailView
from .views import EmpresaListView, EmpresaCreateView, EmpresaUpdateView
from .views import EmpresaLugarListView, EmpresaLugarUpdateView
from .views import verificar_movimiento, obtener_costo_producto
from .views import verificar_remision, obtener_precio_producto
from .views import verificar_compra, obtener_dias_plazo
from .views import obtener_ultimo_numero_remision, obtener_ultimo_movimiento, obtener_ultima_compra
from .views import remisiones_por_dia, buscar_remisiones_por_dia
from .views import remisiones_por_cliente, buscar_remisiones_por_cliente
from .views import remisiones_por_producto, buscar_remisiones_por_producto
from .views import movimientos_por_producto_totales, buscar_movimientos_por_producto_totales
from .views import movimientos_por_clave, buscar_movimientos_por_clave
from .views import api_existencia_producto
from .views import buscar_existencia_producto, imprimir_existencia_producto
from .views import compras_por_dia, buscar_compras_por_dia
from .views import compras_por_producto, buscar_compras_por_producto
from .views import compras_por_proveedor, buscar_compras_por_proveedor
from .views import registrar_emisor_view, registrar_csd_view

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
    #Compras
    path('compra/', CompraListView.as_view(), name='compra_list'),
    path('compra/nuevo/', CompraCreateView.as_view(), name='compra_create'),
    path('compra/editar/<int:pk>/', CompraUpdateView.as_view(), name='compra_update'),
    path('compra/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='compra_delete'),
    path('compra/<int:pk>/', CompraDetailView.as_view(), name='compra_detail'),
    path('verificar_compra/', verificar_compra, name='verificar_compra'),
    path('ajax/ultima_compra/', obtener_ultima_compra, name='ajax_ultima_compra'),
    path('obtener_dias_plazo/', obtener_dias_plazo, name='obtener_dias_plazo'),
    #Consultas y Reportes
    path('reportes/remisiones_por_dia/', remisiones_por_dia, name='remisiones_por_dia'),
    path('reportes/buscar_remisiones_dia/', buscar_remisiones_por_dia, name='buscar_remisiones_dia'),
    path('reportes/remisiones_por_cliente/', remisiones_por_cliente, name='remisiones_por_cliente'),
    path('reportes/buscar_remisiones_cliente/', buscar_remisiones_por_cliente, name='buscar_remisiones_cliente'),
    path('reportes/remisiones_por_producto/', remisiones_por_producto, name='remisiones_por_producto'),
    path('reportes/buscar_remisiones_producto/', buscar_remisiones_por_producto, name='buscar_remisiones_producto'),
    path('reportes/buscar_movimientos_producto/', buscar_movimientos_por_producto_totales, name='buscar_movimientos_producto'),
    path('reportes/movimientos_por_producto/', movimientos_por_producto_totales, name='movimientos_por_producto'),
    path('reportes/buscar_movimientos_clave/', buscar_movimientos_por_clave, name='buscar_movimientos_clave'),
    path('reportes/movimientos_por_clave/', movimientos_por_clave, name='movimientos_por_clave'),
    path('api/existencia_producto/', api_existencia_producto, name='api_existencia_producto'),

    path('reportes/buscar_existencia_producto/', buscar_existencia_producto, name='buscar_existencia_producto'),
    path('reportes/imprimir_existencia_producto/', imprimir_existencia_producto, name='imprimir_existencia_producto'),

    path('reportes/compras_por_dia/', compras_por_dia, name='compras_por_dia'),
    path('reportes/buscar_compras_dia/', buscar_compras_por_dia, name='buscar_compras_dia'),
    path('reportes/compras_por_producto/', compras_por_producto, name='compras_por_producto'),
    path('reportes/buscar_compras_producto/', buscar_compras_por_producto, name='buscar_compras_producto'),
    path('reportes/compras_por_proveedor/', compras_por_proveedor, name='compras_por_proveedor'),
    path('reportes/buscar_compras_proveedor/', buscar_compras_por_proveedor, name='buscar_compras_proveedor'),
 
    path('empresa/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/nuevo/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/editar/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_update'),
  
    path('empresa_lugarexp/', EmpresaLugarListView.as_view(), name='empresa_lugarexp_list'),
    path('empresa_lugarexp/editar/<int:pk>/', EmpresaLugarUpdateView.as_view(), name='empresa_lugarexp_update'),

    path('cfdi_registrar_emisor/', registrar_emisor_view, name='cfdi_registrar_emisor'),
    path('cfdi_registrar_csd/', registrar_csd_view, name='cfdi_registrar_csd'),
]