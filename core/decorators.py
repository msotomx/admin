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

from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

def staff_required(redirect_url='/'):
    """
    Decorador para requerir que el usuario esté autenticado y sea staff.
    Si no es staff, redirige en lugar de devolver 403.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Redirige al login, conservando la URL original
                path = request.get_full_path()
                login_url = reverse('login')  # Cambia si tu login tiene otro nombre
                return redirect(f"{login_url}?{REDIRECT_FIELD_NAME}={path}")

            if not request.user.is_staff:
                # Redirige a otra página si no es staff
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
