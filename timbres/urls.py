from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

from timbres.views import MovimientoTimbresGlobalListView
from timbres.views import EntradaTimbreCreateView
from timbres.views import MovimientoTimbresCreateView
from timbres.views import timbres_solicitar

app_name = 'timbres'

urlpatterns = [
    path('timbres_asignar/', MovimientoTimbresCreateView.as_view(), name='asignar_timbres'),
    path('movimientos/', MovimientoTimbresGlobalListView.as_view(), name='timbres_movimiento_list'),
    path('entradas/', EntradaTimbreCreateView.as_view(), name='timbres_entradas'),
    path('solicitar_timbres/', timbres_solicitar, name='timbres_solicitar'),
]

