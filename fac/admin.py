from django.contrib import admin

# Register your models here.
from .models import FormaPago, MetodoPago, TipoComprobante, UsoCfdi, Exportacion

admin.site.register(FormaPago)
admin.site.register(MetodoPago)
admin.site.register(TipoComprobante)
admin.site.register(UsoCfdi)
admin.site.register(Exportacion)
