
import threading

_thread_locals = threading.local()

def set_current_tenant(alias, empresa_id=None, empresa_fiscal=None):
    _thread_locals.tenant_db_alias = alias
    _thread_locals.empresa_id = empresa_id
    _thread_locals.empresa_fiscal = empresa_fiscal

def get_current_tenant():
    return getattr(_thread_locals, 'tenant_db_alias', None)

def get_current_empresa_id():
    return getattr(_thread_locals, 'empresa_id', None)

def get_current_empresa_fiscal():
    return getattr(_thread_locals, 'empresa_fiscal', None)
