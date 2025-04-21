from django.urls import path
from . import views
from .views import MonedaListView, MonedaCreateView, MonedaUpdateView, MonedaDeleteView

app_name = 'inv'

urlpatterns = [
    # path('', views.index, name='index'),
    path('monedas/', MonedaListView.as_view(), name='moneda_list'),
    path('monedas/nueva/', MonedaCreateView.as_view(), name='moneda_create'),
    path('monedas/<int:pk>/editar/', MonedaUpdateView.as_view(), name='moneda_update'),
    path('monedas/<int:pk>/eliminar/', MonedaDeleteView.as_view(), name='moneda_delete'),
]
