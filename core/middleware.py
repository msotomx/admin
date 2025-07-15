from django.shortcuts import redirect, render   
from django.urls import reverse
from core.models import Empresa
from core.models import PerfilUsuario  
from django.utils.deprecation import MiddlewareMixin
from core.db_config import get_db_config_from_empresa

# SELECCIONAR EL TENANT Y REGISTRAR LA CONEXION DINAMICA

from core.db_router import set_current_tenant_connection
from django.db import connections
from django.conf import settings
from core.models import EmpresaDB
from django.core.exceptions import PermissionDenied
from core._thread_locals import set_current_tenant
from core._thread_locals import get_current_tenant, get_current_empresa_id, get_current_empresa_fiscal

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("📦 SESSION CHECK EN MIDDLEWARE:")
        print("🔍 COOKIES:", request.COOKIES.get('sessionid'))
        path = request.path

        # Ignorar rutas especiales
        if path.startswith(('/.well-known/', '/favicon.ico', '/setup-tenant')):
            return

        # Ignorar peticiones no HTML
        accept_header = request.headers.get('Accept', '')
        if 'text/html' not in accept_header:
            print(f"⚠️ Ignorando petición no HTML: {path}")
            return

        # Asegurar que es desde localhost
        if not request.get_host().startswith('127.0.0.1'):
            print("🚫 Petición no permitida desde host:", request.get_host())
            return

        # Validar autenticación
        if not request.user.is_authenticated:
            print("⚠️ Usuario no autenticado")
            return

        # Leer datos de sesión
        empresa_id = request.session.get('empresa_id')
        empresa_fiscal = request.session.get('empresa_fiscal')
        print("EN MIDDLEWARE - empresa_id:", empresa_id)
        print("EN MIDDLEWARE - empresa_fiscal:", empresa_fiscal)
        if not empresa_id:
            print("❌ empresa_id no encontrado en sesión")
            set_current_tenant(None, None, None)
            return

        # Usar alias fijo para el tenant
        alias = 'tenant'
        print(f"🧪 EN MIDDLEWARE session_key: {request.session.session_key}")
        print(f"🧪 EN MIDDLEWARE session_data: {request.session.items()}")
        # Establecer conexión si no existe
        if alias not in connections.databases:
            try:
                db_config = get_db_config_from_empresa(empresa_id)
                connections.databases[alias] = db_config
                print(f"✅ EN MIDDLEWARE Conexión '{alias}' registrada exitosamente")
            except Exception as e:
                print(f"❌ Error registrando conexión tenant: {e}")
                return

        # Si no hay nombre fiscal, consultar
        if not empresa_fiscal:
            try:
                empresa = Empresa.objects.using(alias).first()
                empresa_fiscal = empresa.nombre_comercial if empresa else "Desconocida"
                request.session['empresa_fiscal'] = empresa_fiscal
                request.session.modified = True
            except Exception as e:
                print(f"⚠️ No se pudo obtener empresa fiscal: {e}")
                empresa_fiscal = "Desconocida"

        # Guardar en _thread_locals
        set_current_tenant(alias, empresa_id, empresa_fiscal)

        # Para uso directo en la request
        request.alias_tenant = alias
        request.empresa_id = empresa_id
        request.empresa_fiscal = empresa_fiscal

        print(f"🏢 Middleware listo: tenant='{alias}', empresa_id={empresa_id}, empresa_fiscal={empresa_fiscal}")

