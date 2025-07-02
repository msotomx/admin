# ROUTER PERSONALIZADO PARA BASE DE DATOS
# Este DatabaseRouter se usará para decidir a qué base de datos se envían las operaciones de cada usuario.

import threading
from threading import local
from django.conf import settings
from django.db import connections
from copy import deepcopy
from core.db_config import get_db_config_from_empresa
from core.models import EmpresaDB
from core._thread_locals import get_current_empresa_id, get_current_tenant, get_current_empresa_fiscal

# regresa el db_config, recibe empresaDB

_thread_locals = threading.local()
def set_current_tenant_connection(alias):
    """
    Establece la conexión con la base de datos correspondiente al alias del tenant.
    """
    # Verificar si la conexión ya existe, sino crearla
    empresa_id = get_current_empresa_id()  # regresa la empresa_id de _thread_locals
    empresa_fiscal = get_current_empresa_fiscal()

    print("EN SET_CURRENT_TENANT_CONNECTION - alias:", alias)
    if alias not in connections.databases:
        # Si no está registrada, debemos configurar la base de datos para este alias
        empresa = EmpresaDB.objects.using('default').get(id=empresa_id)  # Aquí obtenemos la empresa completa
        print(f"EN SET_CURRENT_TENANT_CONNECTION - Empresa: {empresa.nombre}")

        db_config = get_db_config_from_empresa(empresa)  # Obtener la configuración del tenant
        connections.databases[alias] = db_config
        print(f"Conexión con la base de datos {alias} registrada exitosamente.")
    else:
        print(f"La conexión con {alias} ya está registrada.")

    # Guardar datos activos en _thread_locals
    from core._thread_locals import set_current_tenant
    set_current_tenant(alias, empresa_id, empresa_fiscal)

# aqui regresa el alias de la base tenant
def get_current_tenant_connection():
    return getattr(_thread_locals, 'tenant_db_alias', None)

class TenantDatabaseRouter:
    GLOBAL_MODELS = [
        'auth.user',
        'core.perfilusuario',
        'core.empresadb',
        'core.contenttype',  # para ContentType
        'core.session',      # para sesiones manualmente
    ]

    def db_for_read(self, model, **hints):
        label = f"{model._meta.app_label}.{model._meta.model_name}"
        if label in self.GLOBAL_MODELS:
            return 'default'

        return get_current_tenant_connection() or 'default'
    
    def db_for_write(self, model, **hints):
        label = f"{model._meta.app_label}.{model._meta.model_name}"
        if label in self.GLOBAL_MODELS:
            return 'default'

        return get_current_tenant_connection() or 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        # Relación válida si ambos objetos usan la misma BD
        db1 = self.db_for_read(obj1)
        db2 = self.db_for_read(obj2)
        return db1 == db2

def allow_migrate(self, db, app_label, model_name=None, **hints):
    db_conf = get_current_tenant_connection()

    # Migrar globales en 'default' y también en base tenant si está activa
    if app_label in ['auth', 'contenttypes', 'admin', 'sessions']:
        return db == 'default' or (db_conf and db == db_conf['ALIAS'])

    # Migrar las demás apps solo en la base tenant activa
    return db_conf and db == db_conf['ALIAS']

