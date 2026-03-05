from django.contrib import admin
from datetime import date
# Register your models here.
from .models import Empresa
from .models import PerfilUsuario
from .models import EmpresaDB
from .models import SiteMessages

admin.site.register(Empresa)
admin.site.register(PerfilUsuario)

from .models import CertificadoCSD
from django.utils.html import format_html
from .models import ConfiguracionCotizacion


@admin.register(CertificadoCSD)
class CertificadoCSDAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'fecha_registro')

@admin.register(EmpresaDB)
class EmpresaDBAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_empresa','fecha_inicio', 'fecha_renovacion', 'dias_restantes', 'estado_renovacion']

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

@admin.register(SiteMessages)
class SiteMessagesAdmin(admin.ModelAdmin):
    list_display = ("mensaje1","mensaje2","mensaje3", "mensaje4", "mensaje5")


@admin.register(ConfiguracionCotizacion)
class ConfiguracionCotizacionAdmin(admin.ModelAdmin):
    list_display = ("empresa", "mostrar_logo", "mostrar_direccion", "mostrar_totales", "logo_preview")
    list_select_related = ("empresa",)
    search_fields = ("empresa__nombre", "encabezado_nombre")
    readonly_fields = ("logo_preview",)

    fieldsets = (
        ("Empresa", {
            "fields": ("empresa",),
        }),
        ("Visibilidad", {
            "fields": (
                ("mostrar_logo", "mostrar_direccion", "mostrar_telefonos"),
                ("mostrar_vendedor", "mostrar_comentarios", "mostrar_totales"),
            )
        }),
        ("Branding / Logo", {
            "fields": ("logo", "logo_alto_px", "logo_preview", "color_fondo_logo", "color_texto_header")
        }),
        ("Encabezado para Cotización", {
            "fields": (
                "encabezado_nombre",
                ("calle_cotizacion", "colonia_cotizacion"),
                ("codigo_postal_cotizacion", "ciudad_cotizacion"),
                ("tel_cotizacion", "email_cotizacion"),
                "sitio_web",
            )
        }),
        ("Estilos", {
            "fields": (
                ("titulo_documento",),
                ("color_fondo_label_cotizacion", "color_texto_label_cotizacion"),
                ("color_fondo_encabezado_detalle", "color_texto_encabezado_detalle"),
                ("color_borde_tabla",),
            )
        }),
        ("Textos / Pie", {
            "fields": ("leyenda_pie", "terminos_condiciones"),
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:90px;border:1px solid #ddd;padding:6px;border-radius:6px;">', obj.logo.url)
        return "—"
    logo_preview.short_description = "Vista previa"
