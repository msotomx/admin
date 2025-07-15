
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
    empresa_id = get_current_empresa_id()
    empresa_fiscal = get_current_empresa_fiscal()
    print("EN SET_CURRENT-TENANT-CONNECTION: empresa_id:", empresa_id)
    print("EN SET_CURRENT-TENANT-CONNECTION: alias:", alias)
    print("EN SET_CURRENT-TENANT-CONNECTION: empresa_fiscal:", empresa_fiscal)

    if not empresa_id:
        raise ValueError("No se puede establecer conexión sin empresa_id")

    db_config = get_db_config_from_empresa(empresa_id)

    if not db_config or 'NAME' not in db_config:
        raise ValueError(f"❌ Configuración inválida para el tenant '{alias}'")

    # Usamos alias fijo 'tenant'
    if 'tenant' not in connections.databases:
        connections.databases['tenant'] = db_config
        print(f"✅ Conexión con base tenant registrada como 'tenant'")
    else:
        print("ℹ️ Conexión 'tenant' ya registrada")

    # Si no está seteado, obtener el nombre comercial
    if not empresa_fiscal:
        empresa = Empresa.objects.using('tenant').first()
        empresa_fiscal = empresa.nombre_comercial if empresa else "Desconocida"

    # Guardar en _thread_locals
    set_current_tenant('tenant', empresa_id, empresa_fiscal)
    print(f"✅ EN SET_CURRENT_TENANT_CONNECTION: alias=tenant, empresa_id={empresa_id}, empresa_fiscal={empresa_fiscal}")
    
class TenantDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return 'default'
        return 'tenant'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return 'default'
        return 'tenant'
    
    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = getattr(obj1._state, 'db', None)
        db_obj2 = getattr(obj2._state, 'db', None)
        return db_obj1 == db_obj2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Solo migramos auth, admin, etc. en 'default'
        if app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return db == 'default'
        return db == 'tenant'