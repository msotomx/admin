# Objetivo del comando crear_empresa:
# 1-Recibe el nombre de la empresa.
# 2-Genera el slug y nombre de la base de datos (por ejemplo: empresa_ferreteria_la_paz).
# 3-Crea esa base de datos en PostgreSQL.
# 4-Ejecuta las migraciones en esa base.
# 5-Registra la nueva empresa en el modelo EmpresaDB (en la base default).
# 6-Crea una instancia inicial del modelo Empresa en la base del tenant.
#
# este es un comando manual, que se ejecuta desde la consola:
# python manage.py crear_empresa "Ferretería La Paz"
#
import subprocess
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils.text import slugify
from core.models import EmpresaDB
from core.db_router import set_current_tenant_connection
from core.models import Empresa  # modelo fiscal que vive dentro de cada tenant
from django.utils.timezone import now, localtime
from core.utils import cargar_datos_iniciales

class Command(BaseCommand):
    help = 'Crea una nueva empresa'

    def add_arguments(self, parser):
        parser.add_argument('nombre', type=str, help='Nombre comercial de la empresa')

    def handle(self, *args, **options):
        nombre = options['nombre']
        slug = slugify(nombre)
        db_name = f'empresa_{slug}'
        db_user = 'admin_user'
        db_password = 'admin_pass'
        db_host = 'localhost'
        db_port = '5432'

        # Verifica si ya existe en EmpresaDB
        if EmpresaDB.objects.filter(db_name=db_name).exists():
            self.stdout.write(self.style.WARNING(f'La empresa con DB {db_name} ya existe.'))
            return

        # Crear base de datos usando SQL
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE {db_name}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la base de datos: {e}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Base de datos {db_name} creada.'))

        # Ejecutar migraciones en la nueva base
        try:
            subprocess.run(
                ['python', 'manage.py', 'migrate', '--database', db_name],
                check=True
            )
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Error al ejecutar migraciones: {e}'))
            return

        # Registrar en EmpresaDB
        empresa_db = EmpresaDB.objects.create(
            nombre=nombre,
            slug=slug,
            db_name=db_name,
            activa=True
        )
        self.stdout.write(self.style.SUCCESS(f'Empresa registrada en EmpresaDB.'))

        # Configurar conexión activa
        set_current_tenant_connection({
            'ALIAS': db_name,
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': db_user,
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': db_port,
        })

        # Crear instancia del modelo Empresa en la base del tenant
        try:
            Empresa.objects.using(db_name).create(
                nombre_comercial=nombre,
                razon_social = nombre.upper(),
                fecha_inicio = localtime(now()).date(),
                fecha_renovacion = localtime(now()).date(),
                almacen_actual = 1,
                decimales_unidades = 2,
                decimales_importe = 2,
                clave_compras = 'CO',
                clave_traspasos = 'TR',
                clave_remision = 'R1',
                tasa_iva = 16,
                tasa_ieps = 6.45,
                tasa_retencion_iva = 10.6666,
                tasa_retencion_isr = 1.25
            )
            self.stdout.write(self.style.SUCCESS(f'Empresa creada dentro de la BD {db_name}.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear Empresa interna: {e}'))

        # Cargar catálogos y valores iniciales
        try:
            cargar_datos_iniciales(db_name)
            self.stdout.write(self.style.SUCCESS(f'Datos iniciales cargados en {db_name}.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al cargar datos iniciales: {e}'))
