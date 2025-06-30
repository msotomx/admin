from functools import wraps
from django.core.exceptions import PermissionDenied
from core.models import EmpresaDB
from core.utils import set_current_tenant_connection

# ASEGURA QUE LA CONEXION ESTE ACTIVA, USO EN FUNCIONES
def tenant_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        db_config = request.session.get('tenant_db_config')
        if not db_config:
            raise PermissionDenied("⚠️ No se encontró configuración del tenant en la sesión.")

        try:
            set_current_tenant_connection(db_config)
            request.db_name = db_config['db_name']  # ojo se agrego 250629
        except Exception as e:
            raise PermissionDenied(f"💥 Error al conectar a la base tenant: {e}")

        return view_func(request, *args, **kwargs)
    return _wrapped_view
