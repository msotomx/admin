# ROUTER PERSONALIZADO PARA BASE DE DATOS
# Este DatabaseRouter se usará para decidir a qué base de datos se envían las operaciones de cada usuario.

from django.conf import settings
from threading import local
from copy import deepcopy
from django.db import connections

_thread_locals = local()

def set_current_tenant_connection(db_config):
    alias = db_config['ALIAS']
    db_config = deepcopy(db_config)
    db_config.pop('ALIAS')
    db_config["CONN_HEALTH_CHECKS"] = False

    # registrar la conexión en settings
    if alias not in settings.DATABASES:
        settings.DATABASES[alias] = db_config
        connections.databases[alias] = db_config
        print("Se establece conexion con la BD:", alias)

    _thread_locals.tenant_db_alias = alias

# aqui regresa el config de la base tenant
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
