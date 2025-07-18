from django.contrib import admin
from datetime import date
# Register your models here.
from .models import Empresa
from .models import PerfilUsuario
from .models import EmpresaDB

admin.site.register(Empresa)
admin.site.register(PerfilUsuario)
from django.contrib import admin
from .models import CertificadoCSD

@admin.register(CertificadoCSD)
class CertificadoCSDAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'fecha_registro')

@admin.register(EmpresaDB)
class EmpresaDBAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_inicio', 'fecha_renovacion', 'dias_restantes', 'estado_renovacion']

    def dias_restantes(self, obj):
        if obj.fecha_renovacion:
            return (obj.fecha_renovacion - date.today()).days
        return 'N/A'
    dias_restantes.short_description = 'Días restantes'

    def estado_renovacion(self, obj):
        if obj.fecha_renovacion and obj.fecha_renovacion < date.today():
            return 'VENCIDA'
        return 'VIGENTE'
    estado_renovacion.short_description = 'Estado'
