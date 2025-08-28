from django.shortcuts import redirect, render   
from django.urls import reverse
from core.models import Empresa, EmpresaDB
from django.utils.deprecation import MiddlewareMixin
from core._thread_locals import set_current_tenant, clear_current_tenant
from django.db import connections

def reconfigurar_conexion_tenant(alias: str, nueva_config: dict, *, allow_default: bool = False) -> bool:
    """
    Actualiza la configuración del alias SOLO si cambió.
    Cierra la conexión existente y ACTUALIZA el settings_dict del wrapper,
    para que la próxima conexión use la DB correcta. No force ensure_connection.
    """
    if alias == "default" and not allow_default:
        return False

    cfg = nueva_config.copy()

    # Normaliza strings y PORT
    for k in ("ENGINE", "NAME", "USER", "PASSWORD", "HOST"):
        if k in cfg and isinstance(cfg[k], str):
            cfg[k] = cfg[k].strip()
    if "PORT" in cfg and cfg["PORT"] is not None:
        cfg["PORT"] = str(cfg["PORT"]).strip()

    # Obtén wrapper si ya existe; si no, será creado lazy más tarde
    wrapper = None
    try:
        wrapper = connections[alias]
    except Exception:
        wrapper = None

    # Compara contra la config ACTUAL efectiva (la del wrapper si existe)
    actual = (getattr(wrapper, "settings_dict", None)
              or connections.databases.get(alias))

    keys = ("ENGINE", "NAME", "USER", "PASSWORD", "HOST", "PORT")
    if actual and all(actual.get(k) == cfg.get(k) for k in keys):
        return False  # no-op

    # Actualiza el mapeo global
    connections.databases[alias] = cfg

    # Si ya hay wrapper, ciérralo y ACTUALIZA su settings_dict
    if wrapper is not None:
        try:
            if wrapper.connection is not None:
                wrapper.close()
        finally:
            # 🔑 Clave: que el wrapper use la nueva config al reconectar
            wrapper.settings_dict.update(cfg)

    # No llamamos ensure_connection: que conecte lazy cuando se use
    return True
    

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        clear_current_tenant()
        path = request.path
        # Ignorar rutas especiales
        if path.startswith(('/.well-known/', '/favicon.ico', '/setup-tenant', '/logout')):
            return

        # Ignorar estáticos o extensiones conocidas
        if path.startswith('/static/') or path.endswith('.css') or path.endswith('.js'):
            return  # no procesar middleware

        # Ignorar peticiones no HTML
        #accept_header = request.headers.get('Accept', '')
        #if 'text/html' not in accept_header:
        #    return

        # Validar autenticación
        if not request.user.is_authenticated:
            return
        
        empresa_id = request.session.get('empresa_id')
        alias = 'tenant'
        
        if not empresa_id:
            return  # No hay sesión activa aún

        empresadb = EmpresaDB.objects.using('default').filter(id=empresa_id).first()
        
        if not empresadb:
            return

        db_name = empresadb.db_name

        nueva_config = {
            "ENGINE": "django.db.backends.postgresql",
            'NAME': db_name,
            'USER': empresadb.db_user,
            'PASSWORD': empresadb.db_password,
            'HOST': empresadb.db_host,
            'PORT': empresadb.db_port,
            'TIME_ZONE': 'America/Mexico_City',
            'CONN_MAX_AGE': 600,
            'AUTOCOMMIT': True,
            'ATOMIC_REQUESTS': False,
            'CONN_HEALTH_CHECKS': False,
            'OPTIONS': {},
        }

        reconfigurar_conexion_tenant(alias, nueva_config)
        # print("→ tenant NAME ahora:", connections[alias].settings_dict.get("NAME"))

        empresa_fiscal = None
        empresa_f = None
        try:
            empresa_fiscal = Empresa.objects.using(alias).first()
            empresa_f = empresa_fiscal.nombre_comercial
        except Exception as e:
            print(f"❌ Error al conectar a la base de datos '{alias}': {e}")

        # Guardar en _thread_locals
        set_current_tenant(alias, empresa_id, empresa_f)

