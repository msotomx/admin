from django.contrib import admin

# Register your models here.
from .models import Empresa
from .models import PerfilUsuario

admin.site.register(Empresa)
admin.site.register(PerfilUsuario)
from django.contrib import admin
from .models import CertificadoCSD

@admin.register(CertificadoCSD)
class CertificadoCSDAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'fecha_registro')
