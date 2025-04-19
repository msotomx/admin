from django.shortcuts import redirect
from django.urls import reverse
from .models import Empresa

class EmpresaActivaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                empresa = Empresa.objects.get(empresa=request.user)
                if not empresa.activa:
                    if request.path not in [
                        reverse('core:empresa_inactiva'),
                        reverse('logout'),
                    ]:
                        return redirect('core:empresa_inactiva')
            except Empresa.DoesNotExist:
                if request.path != reverse('core:sin_empresa'):
                    return redirect('core:sin_empresa')
        return self.get_response(request)
