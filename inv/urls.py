from django.urls import path
from . import views

app_name = 'inv'

urlpatterns = [
    path('', views.index, name='index'),
]
