# VIEWS - DE CORE

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Empresa

# Create your views here.

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

@login_required
def inicio(request):
    return render(request, 'core/inicio.html')    

"""  ===
from django.contrib.auth import login, logout, authenticate

def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    
    context = {
        'destino':paginaDestino
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        if usuarioAuth is not None:
            login(request,usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)
        
            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos Incorrectos'
            }

    return render(request,'login.html',context)

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html')

==== """
