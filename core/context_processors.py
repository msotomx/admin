from core._thread_locals import get_current_empresa_fiscal, set_current_tenant
from django.db import connections

def empresa_context(request):
    if request.user.is_authenticated:
        empresa_fiscal = None
        try:
            # Solo intentarlo si la conexión tenant aún existe
            if 'tenant' in connections.databases:
                empresa_fiscal = get_current_empresa_fiscal()
                return {'empresa_actual': empresa_fiscal}
        except Exception:
            pass
    else:
        set_current_tenant(None,None,None)
    return {'empresa_actual': None}
