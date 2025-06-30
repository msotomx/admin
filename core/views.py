# VIEWS - DE CORE

from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.urls import reverse
from core.utils import get_empresa_actual
from django.contrib import messages

# Create your views here.

from django.shortcuts import render, redirect
from core.models import PerfilUsuario, EmpresaDB, Empresa
from django.conf import settings

from core.db_router import get_current_tenant_connection
from core.db_router import set_current_tenant_connection
from core.utils import get_empresa_actual
from django.db import connections
from django.core.exceptions import PermissionDenied

def require_tenant_connection2(view_func):
    def wrapper(request, *args, **kwargs):
        if not get_current_tenant_connection():
            raise PermissionDenied("Conexión al tenant no activa")
        return view_func(request, *args, **kwargs)
    return wrapper

def require_tenant_connection(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        # Si ya hay conexión activa, continuar
        if get_current_tenant_connection():
            return view_func(request, *args, **kwargs)

        try:
            # Conexión y objetos desde base de datos DEFAULT
            perfil = PerfilUsuario.objects.using('default').select_related('empresa').get(user=request.user)
            empresaDB = perfil.empresa

            if not empresaDB:
                logout(request)
                return redirect('login')

            if not empresaDB.activa:
                messages.error(request, "La empresa está desactivada. Envíanos un mensaje a Switchh.")
                logout(request)
                return redirect('login')

            # Construcción del db_config (incluyendo CONN_HEALTH_CHECKS)
            db_config = {
                'ALIAS': empresaDB.db_name,
                'ENGINE': 'django.db.backends.mysql',
                'NAME': empresaDB.db_name,
                'USER': empresaDB.db_user,
                'PASSWORD': empresaDB.db_password,
                'HOST': empresaDB.db_host,
                'PORT': empresaDB.db_port,
                'TIME_ZONE': 'America/Mexico_City',
                'CONN_HEALTH_CHECKS': False,  # 👈 NO lo quites aquí
                'CONN_MAX_AGE': 600,
                'AUTOCOMMIT': True,
                'ATOMIC_REQUESTS': False,
                'OPTIONS': {},
            }

            set_current_tenant_connection(db_config)
            print(f"✅ EN WRAPPER Conexión establecida con la base de datos {empresaDB.db_name}")

        except PerfilUsuario.DoesNotExist:
            logout(request)
            return redirect('login')

        except Exception as e:
            print(f"❌ Error al establecer conexión tenant: {e}")
            logout(request)
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper

@login_required
@require_tenant_connection
def inicio(request):
    empresaDB = request.user.perfilusuario.empresa

    if not empresaDB.activa:
        return render(request, 'core/empresa_inactiva.html', {'empresa': empresaDB})

    empresa_fiscal = Empresa.objects.using(empresaDB.db_name).first()
    #empresa_fiscal = get_empresa_actual(request)
    if not empresa_fiscal:
        return render(request, 'core/empresa_no_configurada.html', {'empresa': empresaDB})

    return render(request, 'core/inicio.html', {
        'empresaDB': empresaDB,
        'empresa': empresa_fiscal,
        'usuario': request.user
    })

def logOutUsuario(request):
    
    logout(request)
    return render(request,'core/inicio.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from core.db_router import set_current_tenant_connection
from core.models import PerfilUsuario

@login_required
def empresa_detail(request):
    try:
        perfil = request.user.perfilusuario  # Base default
        empresa = perfil.empresa
    except PerfilUsuario.DoesNotExist:
        return render(request, 'core/sin_empresa.html')

    if not empresa.activa:
        return render(request, 'core/empresa_inactiva.html', {'empresa': empresa})

    if request.session.get('empresa_id') != empresa.id:
            request.session['empresa_id'] = empresa.id

    return render(request, 'core/empresa_detail.html', {'empresa': empresa})

def empresa_inactiva(request):
    return render(request, 'core/empresa_inactiva.html')

def sin_empresa(request):
    return render(request, 'core/sin_empresa.html')

from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nueva_empresa'] = self.request.GET.get('nueva_empresa') == '1'
        return context

    def form_valid(self, form):
        user = form.get_user()

        try:
            perfil = PerfilUsuario.objects.get(user=user)
            empresa = perfil.empresa
            if not empresa or not empresa.activa:
                return HttpResponse("Empresa inactiva o no asignada.")
            
            if not empresa.activa:
                # aún NO se ha hecho login → no pasa nada por hacer logout aquí
                return HttpResponse("Empresa inactiva.")

            db_config = {
                'ALIAS': empresa.db_name,
                'ENGINE': 'django.db.backends.mysql',
                'NAME': empresa.db_name,
                'USER': empresa.db_user,
                'PASSWORD': empresa.db_password,
                'HOST': empresa.db_host,
                'PORT': int(empresa.db_port),
                'TIME_ZONE': 'America/Mexico_City',
                'CONN_MAX_AGE': 600,
                'AUTOCOMMIT': True,
                'ATOMIC_REQUESTS': False,
                'CONN_HEALTH_CHECKS': False,
                'OPTIONS': {},
            }
            self.request.session['empresa_id'] = empresa.id
            self.request.session['alias_tenant'] = empresa.db_name  # 🔑 ahora sí
            self.request.session['db_config'] = db_config  # 🔑 nombre correcto
            print(f"✅ Login correcto: usuario={user.username}, empresa={empresa.nombre}")
            print("📦 DB Config:", db_config)

            set_current_tenant_connection(db_config)
            
        except PerfilUsuario.DoesNotExist:
            return HttpResponse("Usuario o empresa no encontrados.")

        # Ahora sí, llamar al login real
        return super().form_valid(form)

# FUNCION PARA SIGN INICIAL, AQUI SE CREA LA BD DEL CLIENTE, EL USUARIO INICIAL Y 
# SE AGREGA LA EMPRESA NUEVA EN LA LISTA DE EMPRESAS
from django.shortcuts import render, redirect
from core.services.tenant_setup import crear_tenant_completo

def sign_inicial_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_comercial')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contacto_nombre = request.POST.get('contacto_nombre')
        contacto_telefono = request.POST.get('contacto_telefono')
        contacto_email = request.POST.get('contacto_email')

        try:
            crear_tenant_completo(
                request, nombre, username, password,
                contacto_nombre, contacto_telefono, contacto_email
            )
            
            return redirect(f"{reverse('core:login')}?nueva_empresa=1")
        except Exception as e:
            return render(request, 'core/sign_inicial.html', {'error': str(e)})
        
        

    return render(request, 'core/sign_inicial.html')
