from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Empresa
from core.models import PerfilUsuario
from django.utils.deprecation import MiddlewareMixin


EXEMPT_PATHS = [
    '/admin/',  # evita interferir con el admin
    '/core/login/',
    '/core/logout/',
    '/core/sin_empresa/',
    '/core/empresa_inactiva/',
]

class EmpresaActivaMiddleware:
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

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        empresa_id = request.session.get('empresa_id')
        db_config = request.session.get('db_config')
        alias = request.session.get('alias_tenant')

        print(f"🌀 TenantMiddleware: empresa_id = {empresa_id}")
        print(f"🌀 TenantMiddleware: alias tenant = {alias if alias else '❌'}")

        if empresa_id and db_config:
            try:
                db_alias = alias or 'default'
                connections.databases[db_alias] = db_config
                request.tenant_db = db_alias
                print(f"✅ Conexión configurada para alias: {db_alias}")
            except Exception as e:
                print(f"❌ Error configurando conexión tenant: {e}")
        else:
            print("⚠️ No se encontró empresa_id o db_config en la sesión")
