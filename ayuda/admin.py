from django.contrib import admin
from .models import ArticuloAyuda

@admin.register(ArticuloAyuda)
class ArticuloAyudaAdmin(admin.ModelAdmin):
    list_display = ("categoria", "titulo", "orden", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("titulo", "categoria", "contenido_html")
    prepopulated_fields = {"slug": ("titulo",)}
    ordering = ("categoria", "orden", "titulo")
