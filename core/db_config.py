from core.models import EmpresaDB

def get_db_config_from_empresa(empresa_id):
    empresa = EmpresaDB.objects.using('default').get(pk=empresa_id)
    return {
        'ALIAS': empresa.db_name,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': empresa.db_name,
        'USER': empresa.db_user,
        'PASSWORD': empresa.db_password,
        'HOST': empresa.db_host,
        'PORT': int(empresa.db_port),
        'TIME_ZONE': 'America/Mexico_City',
        'CONN_MAX_AGE': 600,
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
        'CONN_HEALTH_CHECKS': False,
        'OPTIONS': {},
    }
