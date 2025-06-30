from core.utils import get_empresa_actual

def empresa_context(request):
    if request.user.is_authenticated:
        print("EN EMPRESA-CONTEXT- usuario:", request.user.username)
        try:
            empresa = get_empresa_actual(request)   # regresa empresa fiscal
            print("EN EMPRESA_CONTEXT empresa.nombre_comercial:", empresa.nombre_comercial)
            return {'empresa_actual': empresa}
        except Exception:
            print("EN EMPRESA_CONTEXT-except")
            return {'empresa_actual': None}
        
    return {'empresa_actual': None}
