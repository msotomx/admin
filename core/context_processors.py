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

def site_messages(request):
    from core.models import SiteMessages
    obj = SiteMessages.objects.using("default").first()
    return {
        "MENSAJE_INICIO1": getattr(obj, "mensaje1", ""),
        "MENSAJE_INICIO2": getattr(obj, "mensaje2", ""),
        "MENSAJE_INICIO3": getattr(obj, "mensaje3", ""),
        "MENSAJE_INICIO4": getattr(obj, "mensaje4", ""),
        "MENSAJE_INICIO5": getattr(obj, "mensaje5", ""),
    }
