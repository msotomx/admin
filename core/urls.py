from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.urls import path, reverse_lazy
from . import views
from core.views import CustomLoginView
from django.urls import reverse_lazy
from core.views import sign_inicial_view, logOutUsuario
from core.views import setup_tenant
from core.views import MenuStaffView
from core.views import StaffEmpresaListView, exportar_empresas_excel
from core.views import StaffTimbresClienteListView, exportar_timbres_disponibles_excel
from core.views import StaffMovimientoTimbresListView, exportar_mov_timbres_excel
from core.views import StaffEmpresaRenovacionListView, exportar_empresas_renovacion_excel
from core.views import UsuarioListView, usuario_create
from core.views import CambiarPasswordView, CambiarPasswordDoneView
from core.views import usuarios_bulk_status
from core.views import EmpresaContactoListView, EmpresaContactoUpdateView
from core.views import EmpresaNumUsuariosListView, EmpresaNumUsuariosUpdateView

app_name = 'core'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logOutUsuario, name='logout'),
    # Página de recuperación de contraseña
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="core/password_reset.html",
            email_template_name="core/password_reset_email.txt",         # texto plano
            html_email_template_name="core/password_reset_email.html",   # HTML
            subject_template_name="core/password_reset_subject.txt",     # 1 línea
            from_email=settings.DEFAULT_FROM_EMAIL,
            success_url=reverse_lazy("core:password_reset_done"),
            extra_email_context={"site_name": "Switchh"},  # opcional
        ),
        name="password_reset",
    ),
    # Página después de enviar el enlace
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="core/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    # Página donde el usuario cambia su contraseña, el patrón incluye 'uidb64' y 'token'
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
        success_url=reverse_lazy('core:password_reset_complete')
        ),
        name='password_reset_confirm'
     ),
    # Página que confirma el restablecimiento de la contraseña
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="core/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path('empresa/inactiva/', views.empresa_inactiva, name='empresa_inactiva'),
    path('empresa/sin_empresa/', views.sin_empresa, name='sin_empresa'),
    path('registro/', sign_inicial_view, name='sign_inicial'),
    path('setup-tenant/', setup_tenant, name='setup_tenant'),
    path('menu-staff/', MenuStaffView.as_view(), name='menu_staff'),
    path('staff-empresas/', StaffEmpresaListView.as_view(), name='staff_empresa_list'),
    path('staff-empresas/exportar/', exportar_empresas_excel, name='exportar_empresas_excel'),
    path('staff-timbres-clientes/', StaffTimbresClienteListView.as_view(), name='staff_timbres_clientes'),
    path('staff-timbres-disponibles-exportar/', exportar_timbres_disponibles_excel, name='exportar_timbres_disponibles_excel'),
    path('staff-movimientos-timbres/', StaffMovimientoTimbresListView.as_view(), name='staff_movimiento_timbres'),
    path('staff-movimientos-exportar/', exportar_mov_timbres_excel, name='exportar_mov_timbres_excel'),
    path('staff-empresas-renovacion/', StaffEmpresaRenovacionListView.as_view(), name='staff_empresa_renovacion_list'),
    path('staff-empresas-renovacion-exportar/', exportar_empresas_renovacion_excel, name='exportar_empresas_renovacion_excel'),
    path("usuario/nuevo/", usuario_create, name="usuario_create"),
    path("usuarios/", UsuarioListView.as_view(), name="usuario_list"),
    path("password/change/", CambiarPasswordView.as_view(), name="password_change"),  # yo mismo
    path("usuarios/<int:user_id>/password/change/", CambiarPasswordView.as_view(), name="password_change_for_user"),  # el admin  cambia la contraseña
    path("password/change/done/", CambiarPasswordDoneView.as_view(), name="password_change_done"),
    path("usuarios/bulk-status/", usuarios_bulk_status, name="usuarios_bulk_status"),
    path("staff-empresas/contacto/", EmpresaContactoListView.as_view(), name="staff_empresa_contacto_list"),
    path("staff-empresas/<str:codigo_empresa>/editar-contacto/", EmpresaContactoUpdateView.as_view(), name="staff_empresa_contacto_update"),
    path("staff-empresas/num-usuarios/", EmpresaNumUsuariosListView.as_view(), name="staff_empresa_num_usuarios_list"),
    path("staff-empresas/<str:codigo_empresa>/editar-num-usuarios/", EmpresaNumUsuariosUpdateView.as_view(), name="staff_empresa_num_usuarios_update"),
]

