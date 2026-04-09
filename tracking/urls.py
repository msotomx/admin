from django.urls import path
from .views import tracking_list, reporte_visitas_por_ciudad

app_name = "tracking"

urlpatterns = [
    path("visitas/", tracking_list, name="tracking_list"),
    path("reporte-ciudades/", reporte_visitas_por_ciudad, name="reporte_ciudades"),
]
