from functools import wraps
from django.core.exceptions import PermissionDenied
from core.models import EmpresaDB
from core.utils import set_current_tenant_connection
from core.db_config import get_db_config_from_empresa

# ASEGURA QUE LA CONEXION ESTE ACTIVA, USO EN FUNCIONES
from functools import wraps
from django.http import HttpResponseBadRequest
from core.models import EmpresaDB  # Asegúrate que EmpresaDB usa 'default'

from functools import wraps
from django.http import HttpResponseBadRequest
from core._thread_locals import get_current_tenant, get_current_empresa_id

from functools import wraps
from django.http import HttpResponseBadRequest
from core._thread_locals import get_current_tenant, get_current_empresa_id

def tenant_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Obtenemos el alias del tenant y el empresa_id de _thread_locals
        alias_tenant = get_current_tenant()
        empresa_id = get_current_empresa_id()

        if not alias_tenant or not empresa_id:
            print("❌ No se encontró alias_tenant o empresa_id en _thread_locals")
            return HttpResponseBadRequest("Sesión inválida o expirada")

        print(f"En Tenant Required encontrado: empresa_id={empresa_id}, alias={alias_tenant}")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
