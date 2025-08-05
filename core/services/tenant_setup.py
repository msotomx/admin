# core/services/tenant_setup.py
# CREAR EMPRESA modelo core.Empresa y usuario inicial
# Recibe como parametros: nombre_comercial, username, password
import re
from django.conf import settings
from django.db import connection, connections
from django.utils.timezone import activate, localtime, now
from django.utils.text import slugify
from django.core.management import call_command
from django.contrib.auth import get_user_model
from copy import deepcopy
from core.models import Empresa, EmpresaDB
from core.db_router import set_current_tenant_connection
from core.utils import cargar_datos_iniciales
from decouple import config
from cxc.models import RegimenFiscal
import traceback

def obtener_ultimo_codigo_empresa():
    ultimo = EmpresaDB.objects.using('default').all().order_by('-codigo_empresa').first()
    if ultimo and ultimo.codigo_empresa.isdigit():
        siguiente = str(int(ultimo.codigo_empresa) + 1).zfill(7)
    else:
        siguiente = "0000701"
    
    return siguiente


def crear_tenant_completo(request, nombre_comercial, username, password, contacto_nombre, contacto_telefono, contacto_email):
    # Paso 1: Normalizar nombre
    slug = slugify(nombre_comercial)
    slug = re.sub(r'[^a-z0-9_]', '', slug.replace('-', '_'))
    db_name = f'e_{slug}'
    db_name = db_name[:22]

    fecha = localtime(now()).date()
    fecha_str = fecha.strftime('%Y%m%d')
    db_name = db_name + fecha_str
    
    # Paso 2: Crear la base de datos físicamente
    if EmpresaDB.objects.using('default').filter(db_name=db_name).exists():
        raise Exception(f"Ya existe una empresa con nombre '{nombre_comercial}'.")

    try:
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE "{db_name}"')
    except Exception as e:
        raise Exception(f"❌ Error al crear la base de datos: {e}")
    
    # Paso 3: Registrar la configuración de la nueva base en runtime
    from django.conf import settings
    db_config_migracion = {
        'ALIAS': db_name,
        "ENGINE": "django.db.backends.postgresql",
        'NAME': db_name,
        'USER': config('TENANT_DB_USER'),
        'PASSWORD': config('TENANT_DB_PASSWORD'),
        'HOST': config('TENANT_DB_HOST'),
        'PORT': config('TENANT_DB_PORT'),   #'5432' en postgresSQL,
        'TIME_ZONE': settings.TIME_ZONE,
        'CONN_HEALTH_CHECKS': False,
        'CONN_MAX_AGE': 600,
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
        'OPTIONS': {},
    }
    
    # Paso 4. Registrar en settings y conexiones
    settings.DATABASES[db_name] = db_config_migracion
    connections.databases[db_name] = db_config_migracion
    # Limpiar conexión previa si existiera
    try:
        del connections[db_name]
    except (KeyError, AttributeError):
        pass

    # Paso 5: Ejecutar migraciones en la nueva base
    try:
        from django.apps import apps
        apps.get_app_configs()
        call_command('migrate', database=db_name, verbosity=1)

    except Exception as e:
        raise Exception(f"❌ Error al ejecutar migraciones: {e}")

    # Paso 6: Activar zona horaria y establecer conexión
    activate(settings.TIME_ZONE)
    
    # Paso 7: Registrar la empresa en la base default
    codigo_empresa = obtener_ultimo_codigo_empresa()
    empresa_db = EmpresaDB.objects.using('default').create(
        nombre=nombre_comercial,
        slug=slug,
        db_name    = db_name,
        db_user    = config('TENANT_DB_USER'),
        db_password= config('TENANT_DB_PASSWORD'),
        db_host    = config('TENANT_DB_HOST'),
        db_port    = config('TENANT_DB_PORT'),
        activa = True,
        fecha_inicio     = localtime(now()).date(),
        fecha_renovacion = localtime(now()).date(),
        contacto_nombre  = contacto_nombre,
        contacto_telefono= contacto_telefono,
        contacto_email   = contacto_email,
        codigo_empresa   = codigo_empresa,
    )

    # paso 8: Crear usuario capturado en el formulario, en User default
    UserModel = get_user_model()
    if UserModel.objects.using('default').filter(username=username).exists():
        raise Exception(f"Ya existe un usuario registrado con username '{username}' ")

    usuario_global = UserModel._default_manager.db_manager('default').create_user(
        username=username,
        password=password,
        email=f'{username}@switchh.com'
    )

    # Paso 9: Crear el PerfilUsuario del usuario capturado en el formulario
    from core.models import PerfilUsuario
    PerfilUsuario.objects.using('default').create(
        user=usuario_global,
        empresa=empresa_db,
        tipo_usuario = "1"
    )

    # Paso 10: Cargar datos iniciales (catálogos, etc.)
    try:
        cargar_datos_iniciales(db_name)
    except Exception as e:
        raise Exception(f"Error al cargar datos iniciales: {e}")

    # Paso 11: Crear empresa fiscal
    regimen_default = RegimenFiscal.objects.using(db_name).first()
    if not regimen_default:
        raise Exception("No se encontró ningún régimen fiscal en la base de datos.")
    try:
        Empresa.objects.using(db_name).create(
            nombre_comercial=nombre_comercial,
            codigo_empresa = codigo_empresa,
            db_name = db_name,
            nombre_fiscal=nombre_comercial.upper(),
            fecha_inicio=localtime(now()).date(),
            fecha_renovacion=localtime(now()).date(),
            almacen_actual=1,
            decimales_unidades=2,
            decimales_importe=2,
            clave_compras='CO',
            clave_traspasos='TR',
            clave_remision='R1',
            tasa_iva=16,
            tasa_ieps=6.45,
            tasa_retencion_iva=10.6666,
            tasa_retencion_isr=1.25,
            factor=0,
            activa=True,
            regimen_fiscal=regimen_default.regimen_fiscal,
        )
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"❌ Error al crear empresa fiscal: {e}")

    # Paso 12: Crear usuario administrador en la base del tenant
    User = get_user_model()
    if not User.objects.using(db_name).filter(email='admin@switchh.com').exists():
        User._default_manager.db_manager(db_name).create_superuser(
            username=config('TENANT_SUPER_USER'),
            email=config('TENANT_SUPER_EMAIL'),
            password=config('TENANT_SUPER_PASS'),
        )

    return nombre_comercial
