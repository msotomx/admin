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
        print("EN TENANTREQUIRED-MIXIN")
        try:
            # Obtener los valores desde _thread_locals directamente
            db_name = get_current_tenant()  # Obtiene el alias del tenant
            empresa_id = get_current_empresa_id()  # Obtiene la empresa_id desde _thread_locals
            empresa_fiscal = get_current_empresa_fiscal()  # Obtiene la empresa_fiscal desde _thread_locals
            
            print("EN TENANTREQUIERED_MIXIN: get_current_tenant():", db_name)
            print("EN TENANTREQUIERED_MIXIN: get_current_empresa_id()", empresa_id)
            print("EN TENANTREQUIERED_MIXIN: get_current_empresa_fiscal():", empresa_fiscal)

            # Validamos si el tenant y la empresa están correctamente asignados
            if not db_name or not empresa_id or not empresa_fiscal:
                messages.error(request, "Tu sesión ha expirado o es inválida.")
                logout(request)
                return redirect('core:login')

            # Establecemos estos valores en request para su uso posterior
            request.alias_tenant = db_name
            request.empresa_id = empresa_id
            request.empresa_fiscal = empresa_fiscal

            # Establecer la conexión con la base de datos 'tenant' utilizando la función ya definida
            set_current_tenant_connection(db_name)  # Esto configura la conexión de la base de datos 'tenant'

        except Exception as e:
            print(f"❌ Error en TenantRequiredMixin: {e}")
            # Si hay un error, redirigimos a la página de error o login
            return redirect('core:login')  # O redirigir a una página de error personalizada

        # Continuar con la ejecución si todo está correcto
        return super().dispatch(request, *args, **kwargs)


from django.db import models
# esto permite accesar asi: monedas = Moneda.tenant.all(), por ejemplo
class TenantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('tenant')

class TenantModel(models.Model):
    objects = models.Manager()       # Acceso normal (default)
    tenant = TenantManager()         # Acceso usando 'tenant'

    class Meta:
        abstract = True
