from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from core.utils import get_empresa_actual
from django.contrib.auth.mixins import LoginRequiredMixin
from core._thread_locals import get_current_tenant, get_current_empresa_id, get_current_empresa_fiscal

class TenantRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            # Obtener los valores desde _thread_locals directamente
            self.db_name = get_current_tenant()  # Obtiene el alias del tenant
            self.empresa_id = get_current_empresa_id()  # Obtiene la empresa_id desde _thread_locals
            self.empresa_fiscal = get_current_empresa_fiscal()  # Obtiene la empresa_fiscal desde _thread_locals

            # Validamos si el tenant y la empresa están correctamente asignados
            if not self.db_name or not self.empresa_id or not self.empresa_fiscal:
                raise Exception("Faltan datos del tenant o de la empresa en _thread_locals")

        except Exception as e:
            print(f"❌ Error en TenantRequiredMixin: {e}")
            return HttpResponse("No se pudo acceder a la empresa del tenant. Verifica tu sesión.", status=400)
        
        # Continuar con la ejecución si todo está correcto
        return super().dispatch(request, *args, **kwargs)
