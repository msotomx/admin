from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import CustomLoginView
from django.urls import reverse_lazy
from .views import sign_inicial_view, logOutUsuario
from .views import setup_tenant

app_name = 'core'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logOutUsuario, name='logout'),
    # Página de recuperación de contraseña
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
             template_name='core/password_reset.html',
             email_template_name='core/password_reset_email.html',
             success_url=reverse_lazy('core:password_reset_done')),
             name='password_reset'
     ),
#    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), 
#         name='password_reset'),
    # Página después de enviar el enlace
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), 
         name='password_reset_done'),
    # Página donde el usuario cambia su contraseña, el patrón incluye 'uidb64' y 'token'
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
        success_url=reverse_lazy('core:password_reset_complete')
        ),
        name='password_reset_confirm'
     ),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), 
    #     name='password_reset_confirm'),
    # Página que confirma el restablecimiento de la contraseña
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    #path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), 
    #    name='password_reset_complete'),
    path('empresa/inactiva/', views.empresa_inactiva, name='empresa_inactiva'),
    path('empresa/sin_empresa/', views.sin_empresa, name='sin_empresa'),
    path('registro/', sign_inicial_view, name='sign_inicial'),
    path('setup-tenant/', setup_tenant, name='setup_tenant'),
]
