from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Empresa
from core.models import PerfilUsuario  
from django.utils.deprecation import MiddlewareMixin
from core.db_config import get_db_config_from_empresa

EXEMPT_PATHS = [
    '/admin/',  # evita interferir con el admin
    '/core/login/',
    '/core/logout/',
    '/core/sin_empresa/',
    '/core/empresa_inactiva/',
]

class EmpresaActivaMiddleware22:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Permitir paso si es superusuario
        if hasattr(request, 'user') and request.user.is_superuser:
            return self.get_response(request)

        # 2. Permitir rutas exentas sin validación
        if any(request.path.startswith(path) for path in EXEMPT_PATHS):
            return self.get_response(request)

        # 3. Validar solo si el usuario está autenticado
        if request.user.is_authenticated:

            # Validación defensiva: evitar error si no hay perfil
            if not hasattr(request.user, 'perfilusuario'):
                return render(request, 'core/sin_empresa.html')

            try:
                perfil = request.user.perfilusuario
                empresa = perfil.empresa
            except PerfilUsuario.DoesNotExist:
                return render(request, 'core/sin_empresa.html')

            if empresa is None or not empresa.activa:
                return render(request, 'core/empresa_inactiva.html', {'empresa': empresa})

        return self.get_response(request)

# SELECCIONAR EL TENANT Y REGISTRAR LA CONEXION DINAMICA

from core.db_router import set_current_tenant_connection
from django.db import connections
from django.conf import settings
from core.models import EmpresaDB
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from core._thread_locals import set_current_tenant

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        empresa_id = request.session.get('empresa_id')
        alias = request.session.get('alias_tenant')
        empresa_fiscal = request.session.get('empresa_fiscal', 'Empresa desconocida')
        
        if not empresa_id or not alias:
            request.alias_tenant = None
            request.empresa_id = None
            request.empresa_empresa_fiscal = None
            set_current_tenant(None, None, None)
            return

        set_current_tenant(alias, empresa_id, empresa_fiscal)
        set_current_tenant_connection(alias)  # Cambiado de set_current_tenant a set_current_tenant_connection
        
        # (Opcional) Para acceso directo desde el request
        request.alias_tenant = alias
        request.empresa_id = empresa_id
        request.empresa_fiscal = empresa_fiscal

        print(f"🧵 EN TENANT_Middleware: alias={alias}, empresa_id={empresa_id}, empresa_fiscal={empresa_fiscal}")
