from django.urls import path
from . import views

app_name = "ayuda"

urlpatterns = [
    path("", views.ayuda_home, name="ayuda"),
    path("<slug:slug>/", views.articulo, name="articulo"),
]
