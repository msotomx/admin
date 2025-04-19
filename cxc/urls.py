from django.urls import path
from . import views

app_name = 'cxc'

urlpatterns = [
    path('', views.index, name='index'),
]