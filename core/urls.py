from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, empresa_detail

app_name = 'core'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('empresa/', views.empresa_detail, name='empresa_detail'),
    path('empresa/inactiva/', views.empresa_inactiva, name='empresa_inactiva'),
    path('empresa/sin_empresa/', views.sin_empresa, name='sin_empresa')
    #path('login',views.loginUsuario,name='loginUsuario'),
    #path('logout',views.logoutUsuario,name='logoutUsuario')
]
