from django.shortcuts import redirect
from django.urls import reverse
from .models import Empresa

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
        # Si el usuario es superusuario, no aplicar la validación de empresa activa
        if request.user.is_superuser:
            return self.get_response(request)

        # Permitir rutas exentas sin validación
        if any(request.path.startswith(path) for path in EXEMPT_PATHS):
            return self.get_response(request)

        # Solo continuar si el usuario está autenticado
        if request.user.is_authenticated:
            try:
                empresa = Empresa.objects.get(empresa=request.user)
                if not empresa.activa:
                    # Si el usuario ya está en la página de empresa inactiva, no redirigir
                    if request.path != reverse('core:empresa_inactiva'):
                        return redirect('core:empresa_inactiva')
            except Empresa.DoesNotExist:
                # Si el usuario ya está en la página de sin_empresa, no redirigir
                if request.path != reverse('core:sin_empresa'):
                    return redirect('core:sin_empresa')

        return self.get_response(request)
