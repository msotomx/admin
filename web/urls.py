from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('inicio', views.inicio,name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('clientes/', views.clientes, name='clientes')
    
    #path('empresa',views.abc_empresa,name='empresa'),
    #path('categoria',views.abc_categoria,name='categoria'),
    #path('loginUsuario',views.loginUsuario,name='loginUsuario'),
    #path('login',views.loginUsuario,name='loginUsuario'),
    #path('logout',views.logoutUsuario,name='logoutUsuario')
]
