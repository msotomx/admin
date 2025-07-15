from core._thread_locals import get_current_empresa_fiscal


def empresa_context(request):
    if request.user.is_authenticated:
        empresa_fiscal = None
        try:
            empresa_fiscal = get_current_empresa_fiscal()  # regresa Empresa.nombre_comercial de _thread_locals
            return {'empresa_actual': empresa_fiscal}
        except Exception:
            return {'empresa_actual': None}
        
    return {'empresa_actual': None}
