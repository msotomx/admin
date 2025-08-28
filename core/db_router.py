
# ROUTER PERSONALIZADO PARA BASE DE DATOS
# Este DatabaseRouter se usará para decidir a qué base de datos se envían las operaciones de cada usuario.

import threading
from threading import local
from django.conf import settings
from django.db import connections
from copy import deepcopy
from core.db_config import get_db_config_from_empresa
from core.models import EmpresaDB, Empresa
from core._thread_locals import get_current_empresa_id, get_current_tenant, get_current_empresa_fiscal
from core._thread_locals import set_current_tenant


_thread_locals = threading.local()
def set_current_tenant_connection(alias):
    """
    Establece la conexión con la base de datos correspondiente al alias del tenant.
    El alias debe ser 'tenant', no se debe modificar la base 'default'.
    """
    # Si no hay nombre fiscal, consultar
    empresa_id = get_current_empresa_id()
    empresa_fiscal = get_current_empresa_fiscal()

    if not empresa_id:
        raise ValueError("No se puede establecer conexión sin empresa_id")
    
    db_config = get_db_config_from_empresa(empresa_id)

    if not db_config or 'NAME' not in db_config:
        raise ValueError(f"❌ Configuración inválida para el tenant '{alias}'")

    # Usamos alias fijo 'tenant'
    if 'tenant' not in connections.databases:
        connections.databases['tenant'] = db_config
        # Ahora establece la conexión
        connections[alias].connect()
    else:
        if connections['tenant'].is_usable():
            pass
        else:
            pass

    # Si no está seteado, obtener el nombre comercial
    if not empresa_fiscal:
        empresa = Empresa.objects.using('tenant').first()
        empresa_fiscal = empresa.nombre_comercial if empresa else "Desconocida"
    
    # Guardar en _thread_locals
    set_current_tenant('tenant', empresa_id, empresa_fiscal)
    
class TenantDatabaseRouter:
    DEFAULT_MODELS = ['empresadb', 'perfilusuario', 'certificadocsd',
                      'movimientotimbresglobal','timbrescliente','sitemessages'] 
    DEFAULT_APPS = ['auth', 'contenttypes', 'sessions', 'admin','timbres']

    def db_for_read(self, model, **hints):
        if model._meta.model_name in [m.lower() for m in self.DEFAULT_MODELS]:
            return 'default'
        if model._meta.app_label in self.DEFAULT_APPS:
            return 'default'
        return 'tenant'

    def db_for_write(self, model, **hints):
        if model._meta.model_name in [m.lower() for m in self.DEFAULT_MODELS]:
            return 'default'
        if model._meta.app_label in self.DEFAULT_APPS:
            return 'default'
        return 'tenant'

    def allow_relation(self, obj1, obj2, **hints):
        # Permitir relaciones solo si están en la misma base de datos
        if obj1._state.db and obj2._state.db:
            return obj1._state.db == obj2._state.db
        return None  # Usa el comportamiento por defecto si no se puede determinar
        
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default':
            # Solo migramos auth, admin y core en la base default
            return app_label in ['auth', 'contenttypes', 'admin', 'sessions', 'core', 'cxc', 'inv', 'fac','timbres']
        else:
            # Permitir migrar aplicaciones de tenant en la base 'tenant'
            tenant_apps = ['core', 'cxc', 'inv', 'fac', 'auth', 'contenttypes', 'sessions', 'admin']
            return app_label in tenant_apps
    