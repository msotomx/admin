from django.urls import path
from . import views

app_name = 'fac'

urlpatterns = [
    path('', views.index, name='index'),
]