from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from core.utils import get_empresa_actual
from django.contrib.auth.mixins import LoginRequiredMixin

class TenantRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.empresa = get_empresa_actual(request)  # Debe conectar tenant y devolver Empresa
            self.db_name = request.session.get('alias_tenant')
        except Exception as e:
            print(f"❌ Error en TenantRequiredMixin: {e}")
            return HttpResponse("No se pudo acceder a la empresa del tenant. Verifica tu sesión.", status=400)
        
        return super().dispatch(request, *args, **kwargs)