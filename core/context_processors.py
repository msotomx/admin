from core._thread_locals import get_current_empresa_fiscal


def empresa_context(request):
    if request.user.is_authenticated:
        print("EN CONTEXT_PROCESSORS - usuario:", request.user.username)
        empresa_fiscal = None
        try:
            empresa_fiscal = get_current_empresa_fiscal()  # regresa Empresa.nombre_comercial de _thread_locals
            print("EN CONTEXT_PROCESSORS empresa_actual:", empresa_fiscal)
            return {'empresa_actual': empresa_fiscal}
        except Exception:
            print("EN CONTEXT_PROCESSORS-except")
            return {'empresa_actual': None}
        
    return {'empresa_actual': None}
