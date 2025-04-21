# ADMIN DE INV
from django.contrib import admin

# Register your models here.

from .models import Categoria, UnidadMedida, Almacen, Moneda
from .models import ClaveMovimiento, Proveedor, Producto
from .models import Movimiento, DetalleMovimiento
from .models import Traspaso, DetalleTraspaso, Remision, DetalleRemision, SaldoInicial

admin.site.register(Categoria)
admin.site.register(UnidadMedida)
admin.site.register(Almacen)
admin.site.register(Moneda)
admin.site.register(ClaveMovimiento)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Movimiento)
admin.site.register(DetalleMovimiento)
admin.site.register(Traspaso)
admin.site.register(DetalleTraspaso)
admin.site.register(Remision)
admin.site.register(DetalleRemision)
admin.site.register(SaldoInicial)
