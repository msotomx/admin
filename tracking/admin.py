from django.contrib import admin

# Register your models here.
# Register your models here.
from django.contrib import admin
from .models import VisitaRegistro


@admin.register(VisitaRegistro)
class VisitaRegistroAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_hora",
        "ip",
        "ciudad",
        "pais",
        "es_bot",
        "path",
    )
    list_filter = (
        "es_bot",
        "pais",
        "ciudad",
        "fecha_hora",
    )
    search_fields = (
        "ip",
        "ciudad",
        "pais",
        "user_agent",
        "referrer",
    )

