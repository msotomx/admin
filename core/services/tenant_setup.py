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

def crear_tenant_completo(request, nombre_comercial, username, password, contacto_nombre, contacto_telefono, contacto_email):
    # 1. Normalizar nombre
    slug = slugify(nombre_comercial)
    slug = re.sub(r'[^a-z0-9_]', '', slug.replace('-', '_'))
    db_name = f'empresa_{slug}'
    db_name = db_name[:30]

    fecha = localtime(now()).date()
    fecha_str = fecha.strftime('%Y%m%d')
    db_name = db_name + fecha_str

    if EmpresaDB.objects.filter(db_name=db_name).exists():
        raise Exception(f"Ya existe una empresa con nombre '{nombre_comercial}'.")

    # db_config.pop('CONN_HEALTH_CHECKS', None)  
    # 2. Configuración completa para Django y el backend MySQL
    db_config_migracion = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'TIME_ZONE': settings.TIME_ZONE,
        'CONN_HEALTH_CHECKS': False,
        'CONN_MAX_AGE': 600,
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
        'OPTIONS': {},
    }
        
    # 3. Registrar en settings y conexiones
    settings.DATABASES[db_name] = db_config_migracion
    connections.databases[db_name] = db_config_migracion

    # 4. Crear la base de datos
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    except Exception as e:
        raise Exception(f"❌ Error al crear la base de datos: {e}")

    # 5. Ejecutar migraciones
    try:
        call_command('migrate', database=db_name, verbosity=1)
    except Exception as e:
        raise Exception(f"❌ Error al ejecutar migraciones: {e}")

    # 6. Activar zona horaria y establecer conexión
    activate(settings.TIME_ZONE)
    # 7. Preparar copia limpia para conexión del hilo
    db_config_conexion = deepcopy(db_config_migracion)
    db_config_conexion['ALIAS'] = db_name
    
    # 8. Conectar el hilo a la base tenant
    set_current_tenant_connection(db_config_conexion)
    
    # Ahora, actualizar el settings para consultas
    settings.DATABASES[db_name] = db_config_conexion
    connections.databases[db_name] = db_config_conexion
    
    # 9. Registrar empresa en base default
    empresa_db = EmpresaDB.objects.create(
        nombre=nombre_comercial,
        slug=slug,
        db_name    = db_name,
        db_user    = config('TENANT_DB_USER'),
        db_password= config('TENANT_DB_PASSWORD'),
        db_host    = config('TENANT_DB_HOST'),
        db_port    = config('TENANT_DB_PORT'),   #'5432' en postgresSQL,
        activa = True,
        fecha_inicio     = localtime(now()).date(),
        fecha_renovacion = localtime(now()).date(),
        contacto_nombre  = contacto_nombre,
        contacto_telefono= contacto_telefono,
        contacto_email   = contacto_email,
    )
    
    # 10. Crear superusuario técnico en tenant
    User = get_user_model()
    if not User.objects.using(db_name).filter(email='admin@switchh.com').exists():
        User._default_manager.db_manager(db_name).create_superuser(
            username='admin',
            email='admin@switchh.com',
            password='Ad6527'
        )
    
    # 11. Cargar datos iniciales (catálogos, etc.)
    try:
        cargar_datos_iniciales(db_name)
    except Exception as e:
        raise Exception(f"Error al cargar datos iniciales: {e}")
    
    # 12. Crear empresa fiscal
    regimen_default = RegimenFiscal.objects.using(db_name).first()
    if not regimen_default:
        raise Exception("No se encontró ningún régimen fiscal en la base de datos.")

    try:
        Empresa.objects.using(db_name).create(
            nombre_comercial=nombre_comercial,
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
            regimen_fiscal=regimen_default,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise Exception(f"❌ Error al crear empresa fiscal: {e}")

    # 13. Crear usuario capturado en el formulario, en User default
    UserModel = get_user_model()
    if UserModel.objects.filter(username=username).exists():
        raise Exception(f"Ya existe un usuario registrado con username '{username}' ")

    usuario_global = UserModel._default_manager.db_manager('default').create_user(
        username=username,
        password=password,
        email=f'{username}@switchh.com'
    )

    # 14. Crear el PerfilUsuario del usuario capturado en el formulario
    from core.models import PerfilUsuario
    PerfilUsuario.objects.using('default').create(
        user=usuario_global,
        empresa=empresa_db,  # se refiere al objeto EmpresaDB creado en la BD default
        tipo_usuario = "1"
    )

    return empresa_db
