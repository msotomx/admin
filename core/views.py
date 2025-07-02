# VIEWS - DE CORE

from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout    
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib import messages
from core.db_config import get_db_config_from_empresa
# Create your views here.
from core.models import PerfilUsuario, EmpresaDB, Empresa
from django.conf import settings

from core._thread_locals import get_current_tenant, set_current_tenant
from django.db import connections
from django.core.exceptions import PermissionDenied

def require_tenant_connection(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')

        # Si ya hay conexión activa, continuar
        if get_current_tenant():
            return view_func(request, *args, **kwargs)

        try:
            # Conexión y objetos desde base de datos DEFAULT
            perfil = PerfilUsuario.objects.using('default').select_related('empresa').get(user=request.user)
            empresaDB = perfil.empresa

            if not empresaDB:
                logout(request)
                return redirect('core:login')

            if not empresaDB.activa:
                messages.error(request, "La empresa está desactivada. Envíanos un mensaje a Switchh.")
                logout(request)
                return redirect('core:login')

            alias = empresaDB.db_name    
            set_current_tenant(alias)
            print(f"✅ EN REQUIERE TENANT-WRAPPER Conexión establecida con la base de datos {empresaDB.db_name}")

        except PerfilUsuario.DoesNotExist:
            logout(request)
            return redirect('core:login')

        except Exception as e:
            print(f"❌ EN REQUIERE TENANT-Error al establecer conexión tenant: {e}")
            logout(request)
            return redirect('core:login')

        return view_func(request, *args, **kwargs)

    return wrapper

@login_required
@require_tenant_connection
def inicio(request):
    empresaDB = request.user.perfilusuario.empresa

    if not empresaDB.activa:
        return render(request, 'core/empresa_inactiva.html', {'empresa': empresaDB})

    empresa_fiscal = Empresa.objects.using(empresaDB.db_name).first()
    
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
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()

        try:
            perfil = user.perfilusuario
            empresa = perfil.empresa

            if not empresa or not empresa.activa:
                form.add_error(None, "Empresa inactiva o no asignada.")
                return self.form_invalid(form)
            
            # 1️⃣ Realizamos el login primero (esto reinicia la sesión)
            login(self.request, user)
            
            # 2️⃣ Redirigimos a una nueva vista para hacer la configuración del tenant
            #     y la conexión a la base de datos
            self.request.session['empresa_id'] = empresa.id
            self.request.session['alias_tenant'] = empresa.db_name
            self.request.session['empresa_fiscal'] = None
            # Forzar que Django persista la sesión
            self.request.session.modified = True

            return redirect(reverse('core:setup_tenant'))  # redirige a una vista específica para el tenant

        except PerfilUsuario.DoesNotExist:
            form.add_error(None, "Usuario o empresa no encontrados.")
            return self.form_invalid(form)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.utils import set_current_tenant_connection

# se llama de Login
@login_required
def setup_tenant(request):
    # Validamos que la sesión contenga los valores necesarios
    empresa_id = request.session.get('empresa_id')
    alias_tenant = request.session.get('alias_tenant')

    if not empresa_id or not alias_tenant:
        print("❌ La sesión está incompleta. Redirigiendo al login...")
        return redirect('login')

    try:
        # Conexión a la BD principal
        empresa = EmpresaDB.objects.using('default').get(pk=empresa_id)
        db_name = empresa.db_name

        # Obtener empresa fiscal desde base de datos tenant
        empresa_fiscal = Empresa.objects.using(db_name).first()
        request.session['empresa_fiscal'] = empresa_fiscal.nombre_comercial
        set_current_tenant(
            alias=db_name,
            empresa_id=empresa.id,
            empresa_fiscal=empresa_fiscal.nombre_comercial
        )

        print("1-EN VIEWS SETUP_TENANT, empresa:", empresa)
        print("2-EN VIEWS SETUP_TENANT, empresa.db_name:", db_name)
        print("3-EN VIEWS SETUP_TENANT, empresa_id:", empresa_id)
        print("4-EN VIEWS SETUP_TENANT, alias_tenant:", alias_tenant)
        print("5-EN VIEWS SETUP_TENANT, empresa_fiscal:", empresa_fiscal.nombre_comercial)

        # Establecer conexión del tenant
        set_current_tenant_connection(db_name)

        print(f"✅ EN SETUP TENANT Conexión con el tenant {alias_tenant} configurada exitosamente")
        return redirect('core:inicio')

    except EmpresaDB.DoesNotExist:
        print(f"❌ EmpresaDB con ID {empresa_id} no encontrada")
        return redirect('core:login')

    except Exception as e:
        print(f"❌ Error general en setup_tenant: {e}")
        return redirect('core:login')

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

