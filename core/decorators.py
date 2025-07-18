from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

# ASEGURA QUE LA CONEXION ESTE ACTIVA, USO EN FUNCIONES

from django.http import HttpResponseBadRequest
from core._thread_locals import get_current_tenant, get_current_empresa_id


def tenant_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Obtenemos el alias del tenant y el empresa_id de _thread_locals
        alias_tenant = get_current_tenant()
        empresa_id = get_current_empresa_id()

        if not alias_tenant or not empresa_id:
            return redirect('core:login')  # HttpResponseBadRequest("Sesión inválida o expirada")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
