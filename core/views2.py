# VIEWS - DE CORE
# ANTES DE CAMBIOS A LOGIN 2025-07-19   9.19PM
from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
# Create your views here.
from core.models import PerfilUsuario, EmpresaDB, Empresa
from core._thread_locals import get_current_tenant, get_current_empresa_id, set_current_tenant
from django.db import connections
from django.core.exceptions import PermissionDenied

from functools import wraps

def require_tenant_connection(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('core:login')

        # Validamos que la sesión tenga la clave 'tenant'
        if not get_current_tenant() or not get_current_empresa_id():
            messages.error(request, "La sesión del tenant es inválida o ha expirado.")
            logout(request)
            return redirect('core:login')

        # Verificamos si 'tenant' está en la sesión
        if request.session.get('alias_tenant') != 'tenant':
            messages.error(request, "La sesión del tenant es inválida o ha expirado.")
            logout(request)
            return redirect('core:login')

        # Continuar con la vista original si todo es válido
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@require_tenant_connection
def inicio(request):
    print("ENTRANDO A  INICIO")
    try:
        # Leemos el perfil desde la base 'default'
        empresa_id = get_current_empresa_id()
        print("EN INICIO- empresa_id:",empresa_id)
        #perfil = PerfilUsuario.objects.using('default').select_related(None).get(user=request.user)
        empresaDB = EmpresaDB.objects.using('default').get(pk=empresa_id)

        if not empresaDB.activa:
            return render(request, 'core/empresa_inactiva.html', {'empresa': empresaDB})

        # Leemos la empresa fiscal desde la base del tenant (ya registrada)
        empresa_fiscal = Empresa.objects.using('tenant').first()

        if not empresa_fiscal:
            return render(request, 'core/empresa_no_configurada.html', {'empresa': empresaDB})
        
        return render(request, 'core/inicio.html')
    
    except PerfilUsuario.DoesNotExist:
        return redirect('core:login')
    
    except Exception as e:
        # print(f"❌ Error en inicio: {e}")
        return redirect('core:login')

from django.db import connections
def logOutUsuario(request):
    # Cierra y elimina la conexión del alias 'tenant'
    if 'tenant' in connections.databases:
        # Cierra la conexión si está abierta
        if hasattr(connections, 'tenant'):
            connections['tenant'].close()
        # Elimina el alias del diccionario de conexiones
        del connections.databases['tenant']

    # Borra también los datos de sesión relacionados
    request.session.pop('empresa_id', None)
    request.session.pop('empresa_fiscal', None)

    # Elimina el tenant actual en thread locals (si usas eso)
    set_current_tenant(None, None, None)

    # Realiza logout
    from django.contrib.auth import logout
    logout(request)

    # Redirige donde corresponda
    return redirect('core:login')  # o donde necesites

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from core.models import PerfilUsuario

def empresa_inactiva(request):
    return render(request, 'core/empresa_inactiva.html')

def sin_empresa(request):
    return render(request, 'core/sin_empresa.html')

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse
from core.models import PerfilUsuario

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()

        try:
            perfil = PerfilUsuario.objects.using('default').get(user=user)
            empresa = EmpresaDB.objects.using('default').get(pk=perfil.empresa_id)
            print("EN LOGIN - empresa.db_name:",empresa.db_name)
            print("EN LOGIN - empresa.id:",empresa.id)
            if not empresa or not empresa.activa:
                form.add_error(None, "Empresa inactiva o no asignada.")
                return self.form_invalid(form)

            login(self.request, user)  # 🔒 Esto reinicia la sesión
            update_session_auth_hash(self.request, user)

            # 🔁 Redirige con empresa.id como parámetro
            return redirect(reverse('core:setup_tenant') + f'?eid={empresa.id}')

        except PerfilUsuario.DoesNotExist:
            form.add_error(None, "Usuario o empresa no encontrados.")
            return self.form_invalid(form)

# se llama de Login
@login_required
def setup_tenant(request):
    empresa_id = request.GET.get('eid')
    if not empresa_id:
        # Sin empresa_id, redirigiendo a login.
        return redirect('core:login')

    try:
        # Leer empresa desde la base default
        empresa = EmpresaDB.objects.using('default').get(pk=empresa_id)
        
        # Asegurarse de que hay sesión activa
        if not request.session.session_key:
            request.session.create()

        request.session['empresa_id'] = empresa.id
        request.session['alias_tenant'] = 'tenant'
        request.session['empresa_fiscal'] = None
        request.session.modified = True

        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('core:inicio'))

    except Exception as e:
        # print(f"❌ Error en setup_tenant: {e}")
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
