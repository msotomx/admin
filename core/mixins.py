from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from core._thread_locals import get_current_tenant, get_current_empresa_id, get_current_empresa_fiscal
from core.db_router import set_current_tenant_connection
from django.contrib import messages

class TenantRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            # Obtener los valores desde _thread_locals directamente
            db_name = get_current_tenant()  # Obtiene el alias del tenant
            empresa_id = get_current_empresa_id()  # Obtiene la empresa_id desde _thread_locals
            empresa_fiscal = get_current_empresa_fiscal()  # Obtiene la empresa_fiscal desde _thread_locals
            # Validamos si el tenant y la empresa están correctamente asignados
            if not db_name or not empresa_id or not empresa_fiscal:
                messages.error(request, "Tu sesión ha expirado o es inválida.")
                logout(request)
                return redirect('core:login')

            # Establecemos estos valores en request para su uso posterior
            request.alias_tenant = 'tenant'
            request.empresa_id = empresa_id
            request.empresa_fiscal = empresa_fiscal

            # Verificamos si la conexión con el tenant ya está activa
            if db_name and empresa_id:
                set_current_tenant_connection(db_name)  # Esto configura la conexión a la base de datos del tenant
            else:
                return redirect('core:login')

        except Exception as e:
            # print(f"❌ Error en TenantRequiredMixin: {e}")
            # Si hay un error, redirigimos a la página de error o login
            return redirect('core:login')  # O redirigir a una página de error personalizada

        # Continuar con la ejecución si todo está correcto
        return super().dispatch(request, *args, **kwargs)
