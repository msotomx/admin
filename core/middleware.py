from django.shortcuts import redirect, render   
from django.urls import reverse
from core.models import Empresa
from core.models import PerfilUsuario  
from django.utils.deprecation import MiddlewareMixin
from core.db_config import get_db_config_from_empresa
from core.db_router import set_current_tenant

from django.db import connections

def reconfigurar_conexion_tenant(alias, nueva_config):
    actual_name = connections.databases.get(alias, {}).get('NAME')

    if alias in connections:
        connections['tenant'].close()
        del connections['tenant']

    if actual_name != nueva_config['NAME']:
        if alias in connections:
            if connections[alias].connection is not None:
                connections[alias].close()
                del connections.databases[alias]
                
            # Esto es clave: eliminar también la conexión cachéada
            if alias in connections._connections:
                del connections._connections[alias]
        
        # Reasignar la configuración nueva
        connections.databases[alias] = nueva_config

        connections[alias].connect()
        # Forzar conexión para que se active
        try:
            Empresa.objects.using(alias).exists()
        except Exception as e:
            print(f"❌ Error al activar la conexión con alias '{alias}': {e}")

from django.db import connections
from django.utils.deprecation import MiddlewareMixin
from core.models import EmpresaDB  # o como se llame tu app

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        # Ignorar rutas especiales
        if path.startswith(('/.well-known/', '/favicon.ico', '/setup-tenant', '/logout')):
            return

        # Ignorar estáticos o extensiones conocidas
        if path.startswith('/static/') or path.endswith('.css') or path.endswith('.js'):
            return  # no procesar middleware

        # Ignorar peticiones no HTML
        accept_header = request.headers.get('Accept', '')
        if 'text/html' not in accept_header:
            return

        # Validar autenticación
        if not request.user.is_authenticated:
            return
        
        empresa_id = request.session.get('empresa_id')
        alias = 'tenant'
        
        if not empresa_id:
            return  # No hay sesión activa aún

        empresa = EmpresaDB.objects.using('default').filter(id=empresa_id).first()
        
        if not empresa:
            return

        db_name = empresa.db_name

        nueva_config = {
            "ENGINE": "django.db.backends.postgresql",
            'NAME': db_name,
            'USER': empresa.db_user,
            'PASSWORD': empresa.db_password,
            'HOST': empresa.db_host,
            'PORT': empresa.db_port,
            'TIME_ZONE': 'America/Mexico_City',
            'CONN_MAX_AGE': 600,
            'AUTOCOMMIT': True,
            'ATOMIC_REQUESTS': False,
            'CONN_HEALTH_CHECKS': False,
            'OPTIONS': {},
        }

        reconfigurar_conexion_tenant(alias, nueva_config)
        
        empresa_fiscal = None
        empresa_f = None
        try:
            empresa_fiscal = Empresa.objects.using('tenant').first()
            
            if empresa_fiscal.db_name == db_name:
                empresa_f = empresa_fiscal.nombre_comercial
            else:
                empresa_f = ""

        except Exception as e:
            print(f"❌ Error al conectar a la base de datos '{alias}': {e}")
        
        # Guardar en _thread_locals
        set_current_tenant(alias, empresa_id, empresa_f)
