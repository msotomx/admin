from django.contrib import admin

# Register your models here.
from .models import Empresa, Categoria, TipoCliente, Almacen, Moneda
from .models import UnidadMedida, ClaveMovimiento, Proveedor, Producto
from .models import Cliente, Movimiento, DetalleMovimiento
from .models import Traspaso, DetalleTraspaso, Remision, DetalleRemision, SaldoInicial

admin.site.register(Empresa)
admin.site.register(Categoria)
admin.site.register(TipoCliente)
admin.site.register(Almacen)
admin.site.register(Moneda)
admin.site.register(UnidadMedida)
admin.site.register(ClaveMovimiento)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Movimiento)
admin.site.register(DetalleMovimiento)
admin.site.register(Traspaso)
admin.site.register(DetalleTraspaso)
admin.site.register(Remision)
admin.site.register(DetalleRemision)
admin.site.register(SaldoInicial)

#@admin.register(Producto)
#class ProductoAdmin(admin.ModelAdmin):
#    list_display = ('nombre','precio','categoria')
#    list_editable = ('precio','categoria')