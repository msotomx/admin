from .models import Movimiento, DetalleMovimiento, Remision, DetalleRemision
from .models import SaldoInicial
from django.db.models import Sum, DecimalField
from decimal import Decimal


# CALCULA LA EXISTENCIA DEL PRODUCTO
# La existencia se calcula asi:
# existencia = saldo_inicial + entradas - salidas

# 1) saldo_inicial, se calcula asi: 
#   el el valor del campo Saldo_Inicial.existencia, esa existencia indica la existencia a la fecha Saldo_Inicial.fecha
#     si hay varios registros de ese producto, se toma el valor de SaldoInicial.existencia mas cercano a la fecha_leida

# 2) entradas = DetalleMovimiento
#   Se toman todos los movimientos de la tabla DetalleMovimiento, con:
#	Movimiento.move_s ='E'     
#	(Movimiento.fecha_movimiento >= SaldoInicial.fecha) and (Movimiento.fecha_movimiento<= fecha_leida)
     
# 3) salidas = DetalleMovimiento + DetalleRemisiones
#    Se toman todos los movimientos de la tabla DetalleMovimiento, con:
#  	   Movimiento.move_s ='S'     
#	   (Movimiento.fecha_movimiento >= SaldoInicial.fecha) and (Movimiento.fecha_movimiento<= fecha_leida)
#      mas
#      todos los movimientos de la tabla DetalleRemision, con:
#	   (Remision.fecha_remision >= SaldoInicial.fecha) and (Remision.fecha_remision <= fecha_leida)
#	   Remision.status = 'R' o 'F'

def calcular_existencia_producto(producto, almacen, fecha_leida):
    # 1. Buscar el saldo inicial más cercano antes de la fecha_leida
    saldo = (
        SaldoInicial.objects
        .filter(producto=producto, almacen=almacen, fecha__lte=fecha_leida)
        .order_by('-fecha')
        .first()
    )

    if not saldo:
        saldo_inicial = Decimal('0.00')
        fecha_saldo = '1900-01-01'  # si no hay saldo, se parte desde la fecha_base
        print("fecha saldo inicial", fecha_saldo)
    else:
        saldo_inicial = saldo.existencia
        fecha_saldo = saldo.fecha

    # 2. Calcular entradas
    entradas = (
        DetalleMovimiento.objects
        .filter(
            producto=producto,
            referencia__almacen=almacen,
            referencia__move_s='E',
            referencia__fecha_movimiento__range=(fecha_saldo, fecha_leida)
        )
        .aggregate(total=Sum('cantidad'))['total'] or Decimal('0.00')
    )

    # 3. Calcular salidas por movimientos
    salidas_mov = (
        DetalleMovimiento.objects
        .filter(
            producto=producto,
            referencia__almacen=almacen,
            referencia__move_s='S',
            referencia__fecha_movimiento__range=(fecha_saldo, fecha_leida)
        )
        .aggregate(total=Sum('cantidad'))['total'] or Decimal('0.00')
    )

    # 4. Calcular salidas por remisiones
    salidas_rem = (
        DetalleRemision.objects
        .filter(
            producto=producto,
            numero_remision__almacen=almacen,
            numero_remision__fecha_remision__range=(fecha_saldo, fecha_leida),
            numero_remision__status__in=['R', 'F']
        )
        .aggregate(total=Sum('cantidad'))['total'] or Decimal('0.00')
    )

    # 5. Cálculo final de existencia
    existencia = saldo_inicial + entradas - salidas_mov - salidas_rem

    return existencia
