from django.urls import path
from .views import TipoClienteListView, TipoClienteCreateView, TipoClienteUpdateView, TipoClienteDeleteView
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView

app_name = 'cxc'

urlpatterns = [
    path('tipocliente/', TipoClienteListView.as_view(), name='tipocliente_list'),
    path('tipocliente/nuevo/', TipoClienteCreateView.as_view(), name='tipocliente_create'),
    path('tipocliente/editar/<int:pk>/', TipoClienteUpdateView.as_view(), name='tipocliente_update'),
    path('tipocliente/eliminar/<int:pk>/', TipoClienteDeleteView.as_view(), name='tipocliente_delete'),
    path('cliente/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),
]