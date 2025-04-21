# VIEWS - DE CORE

from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import Empresa

# Create your views here.
@login_required
def inicio(request):
    try:
        empresa = Empresa.objects.get(empresa=request.user)
    except Empresa.DoesNotExist:
        return redirect(request, 'core:inicio.html')

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
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


@login_required
def empresa_detail(request):
    try:
        empresa = Empresa.objects.get(empresa=request.user)
    except Empresa.DoesNotExist:
        return render(request, 'core/sin_empresa.html')  # Crea un template para este caso
    
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
