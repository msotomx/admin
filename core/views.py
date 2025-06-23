# VIEWS - DE CORE

from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .models import Empresa, PerfilUsuario

# Create your views here.

from django.shortcuts import render
from .models import PerfilUsuario

@login_required
def inicio(request):
    try:
        perfil = request.user.perfilusuario
        empresa = perfil.empresa
    except PerfilUsuario.DoesNotExist:
        empresa = None

    if not empresa:
        return render(request, 'core/sin_empresa.html')

    if not empresa.activa:
        return render(request, 'core/empresa_inactiva.html', {'empresa': empresa})
     
    return render(request, 'core/inicio.html', {'empresa': empresa})

def logoutUsuario(request):
    logout(request)
    return render(request,'core/inicio.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                empresa = user.perfilusuario.empresa
                if not empresa.activa:
                    logout(request)
                    return render(request, 'core/empresa_inactiva.html', {'empresa': empresa})
            except:
                logout(request)
                return render(request, 'core/sin_empresa.html')

            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

@login_required
def empresa_detail(request):
    try:
        empresa = request.user.perfilusuario.empresa
    except PerfilUsuario.DoesNotExist:
        return render(request, 'core/sin_empresa.html')

    if not empresa.activa:
        return render(request, 'core/empresa_inactiva.html', {'empresa': empresa})

    return render(request, 'core/empresa_detail.html', {'empresa': empresa})

def empresa_inactiva(request):
    return render(request, 'core/empresa_inactiva.html')

def sin_empresa(request):
    return render(request, 'core/sin_empresa.html')

from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
