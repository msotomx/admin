from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

from timbres.views import MovimientoTimbresGlobalListView, CompraTimbresGlobalCreateView, MovimientoTimbresCreateView

app_name = 'timbres'

urlpatterns = [
    path('timbres_asignar/', MovimientoTimbresCreateView.as_view(), name='asignar_timbres'),
    path('timbres/', MovimientoTimbresGlobalListView.as_view(), name='timbres_movimiento_list'),
    path('timbres/entradas/', CompraTimbresGlobalCreateView.as_view(), name='timbres_entradas_form'),
]

