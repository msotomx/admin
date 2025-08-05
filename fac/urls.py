from django.urls import path
from fac.views import FacturaListView, FacturaCreateView, FacturaUpdateView, FacturaDeleteView, FacturaDetailView
from fac.views import verificar_factura, obtener_clave_prod_serv2, obtener_ultimo_numero_factura, obtener_tasa_empresa
from fac.views import timbrar_factura, descargar_factura, cargar_remision
from fac.views import CancelarFacturaView


app_name = 'fac'

urlpatterns = [
    path('factura/', FacturaListView.as_view(), name='factura_list'),
    path('factura/nueva/', FacturaCreateView.as_view(), name='factura_create'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_update'),
    path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_delete'),
    path('factura/<int:pk>/', FacturaDetailView.as_view(), name='factura_detail'),
    path('facturas/', FacturaListView.as_view(), name='factura_list'),
    path('ajax/cargar-remision/', cargar_remision, name='cargar_remision'),


    path('verificar-factura/', verificar_factura, name='verificar_factura'),
    path('obtener_clave_prod_serv/', obtener_clave_prod_serv2, name='obtener_clave_prod_serv'),
    path('ajax/numero-factura/', obtener_ultimo_numero_factura, name='ajax_numero_factura'), 
    path('obtener_tasa_empresa/', obtener_tasa_empresa, name='obtener_tasa_empresa'),
    path('factura/<int:factura_id>/timbrar/', timbrar_factura, name='timbrar_factura'),
    # PATH para cfdi
    path('factura/<int:factura_id>/descargar/<str:tipo>/', descargar_factura, name='descargar_factura'),
    path('factura/<int:pk>/cancelar/', CancelarFacturaView.as_view(), name='cancelar_factura'),
]



