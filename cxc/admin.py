from django.contrib import admin
from django.contrib.auth.models import User

from .models import TipoCliente, ClaveMovimientoCxC, Cliente  
from .models import Cargo, Abono, SaldoInicialCxC

# Register your models here.

admin.site.register(TipoCliente)
admin.site.register(ClaveMovimientoCxC)
admin.site.register(Cliente)
admin.site.register(Cargo)
admin.site.register(Abono)
admin.site.register(SaldoInicialCxC)
