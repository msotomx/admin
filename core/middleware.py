from django.shortcuts import redirect
from django.urls import reverse
from core.models import Empresa
from core.models import PerfilUsuario
from django.utils.deprecation import MiddlewareMixin


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
                perfil = request.user.perfilusuario
                empresa = perfil.empresa
            except PerfilUsuario.DoesNotExist:
                return render(request, 'core/sin_empresa.html')

            if not empresa or not empresa.activa:
                return render(request, 'core/empresa_inactiva.html', {'empresa': empresa})

        return self.get_response(request)

