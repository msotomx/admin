from django.db import models
from django.contrib.auth.models import User
from cxc.models import Cliente
from decimal import Decimal

class Categoria(models.Model):
    categoria = models.IntegerField(null=False, unique=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre 

class Vendedor(models.Model):
    vendedor = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20,blank=True)
    email = models.EmailField(blank=True)
    fecha_registro = models.DateField(blank=True)
        
    def __str__(self):
        return self.nombre 

class UnidadMedida(models.Model):
    unidad_medida = models.CharField(max_length=3,blank=False)
    descripcion = models.CharField(max_length=30,blank=False)

    def __str__(self):
        return f'{self.unidad_medida} | {self.descripcion}'

class Almacen(models.Model):
    almacen = models.IntegerField(null=False,unique=True)
    nombre = models.CharField(max_length=30,blank=False,default='')
    
    def __str__(self):
        return f"{self.almacen} - {self.nombre}"  # Para facilitar la visualización en admin

class Moneda(models.Model):
    nombre = models.CharField(max_length=30,blank=False,default=" ")
    clave = models.CharField(max_length=10, unique=True)
    simbolo = models.CharField(max_length=5, blank=True, null=True)
    activa = models.BooleanField(default=True)
    paridad = models.DecimalField(default=1,decimal_places=6, max_digits=12,null=False) 

    def __str__(self):
        return f"{self.nombre} ({self.clave})"

# 'E' entrada, 'S' salida, 'C' compras
class ClaveMovimiento(models.Model):   
    clave_movimiento = models.CharField(max_length=2,default='', blank=False, unique=True)
    nombre      = models.CharField(max_length=30,null=True)
    tipo        = models.CharField(max_length=1,default='',blank=False)  # E o S 
    es_remision = models.BooleanField(blank=True)   # True - clave para remisiones
    es_compra   = models.BooleanField(blank=True)   # True - clave para compras
    
    def __str__(self):
        return self.nombre 

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100,blank=False,default=" ")
    direccion = models.TextField(blank=True)
    contacto = models.CharField(max_length=100, blank=False)
    telefono1 = models.CharField(max_length=20, blank=True)
    telefono2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    plazo_credito = models.SmallIntegerField(default=0,null=True, blank=True)
    comentarios = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=12, default='',blank=False)
    clave_sat = models.CharField(max_length=8, default='',blank=False)
    categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200,blank=False)
    descripcion = models.TextField(null=True,blank=True)
    imagen = models.ImageField(upload_to='productos',blank=True)
    precio1 = models.DecimalField(max_digits=9,decimal_places=2)
    precio2 = models.DecimalField(max_digits=9,decimal_places=2, default=0)
    precio3 = models.DecimalField(max_digits=9,decimal_places=2, default=0)
    precio4 = models.DecimalField(max_digits=9,decimal_places=2, default=0)
    precio5 = models.DecimalField(max_digits=9,decimal_places=2, default=0)
    precio6 = models.DecimalField(max_digits=9,decimal_places=2, default=0)
    maximo  = models.IntegerField(default=0) 
    minimo  = models.IntegerField(default=0) 
    reorden = models.IntegerField(default=0) 
    fecha_registro = models.DateField()
    proveedor = models.ForeignKey(Proveedor,on_delete=models.RESTRICT)
    unidad_medida = models.ForeignKey(UnidadMedida,on_delete=models.RESTRICT)
    precio_promocion = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    costo_reposicion = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    aplica_iva  = models.BooleanField(blank=True)   # False - No se aplica, True - Se aplica al facturar
    aplica_ieps = models.BooleanField(blank=True)   # False - No se aplica, True - Se aplica al facturar
    tasa_ieps   = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0'))
    campo_libre_str = models.CharField(max_length=50,blank=True,default='')
    campo_libre_num = models.DecimalField(max_digits=10,decimal_places=4, default=0, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    usuario = models.CharField(max_length=40, blank=True)
    referencia = models.CharField(max_length=7, blank=False)
    move_s = models.CharField(max_length=1,blank=False)  # 'E' entrada 'S' salida
    clave_movimiento = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT)
    fecha_movimiento = models.DateField(blank=False)
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)

    def __str__(self):
        return self.referencia
    
class DetalleMovimiento(models.Model):
    referencia = models.ForeignKey(Movimiento,on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto,on_delete=models.PROTECT)
    cantidad = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    costo_unit = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    subtotal = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.referencia

class Cotizacion(models.Model):
    usuario = models.CharField(max_length=40, blank=True)
    numero_cotizacion = models.CharField(max_length=7,blank=False,default="")
    vendedor = models.ForeignKey(Vendedor,on_delete=models.RESTRICT)
    fecha_cotizacion = models.DateField(blank=False)
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return self.numero_cotizacion

class DetalleCotizacion(models.Model):
    numero_cotizacion = models.ForeignKey(Cotizacion,related_name='detalles',on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    descuento = models.DecimalField(null=True, decimal_places=2, max_digits=10, blank=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    def __str__(self):
        return self.producto.nombre


class Remision(models.Model):
    ESTADO_CHOICES = (
        ('C','COTIZACION'),  # no genera movimiento de Salida
        ('P','PEDIDO'),      # no genera movimiento de Salida
        ('R','REMISION'), # si genera movimiento de Salida
        ('F','FACTURADO'),    # la remision se ha facturado
        ('E','ELIMINADA')    # la remision se ha borrado
    )
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)
    usuario = models.CharField(max_length=40, blank=True)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.RESTRICT) 
    clave_movimiento = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT)
    numero_remision = models.CharField(max_length=7,blank=False,default="")
    numero_cotizacion = models.ForeignKey(Cotizacion,on_delete=models.RESTRICT, blank=True, null=True)
    fecha_remision = models.DateField(blank=False)
    numero_factura = models.CharField(max_length=20,blank=False,default="")
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    monto_total = models.DecimalField(default=0,decimal_places=2, max_digits=10,null=True)
    status = models.CharField(max_length=1,default='R',choices=ESTADO_CHOICES)   # CON Esto, solo permite 0 o 1

    def __str__(self):
        return self.numero_remision

class DetalleRemision(models.Model):
    numero_remision = models.ForeignKey(Remision,related_name='detalles',on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    descuento = models.DecimalField(null=True, decimal_places=2, max_digits=10, blank=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    # Iva por producto
    tasa_iva = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0'))  # ej. 16.00
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    # Ieps por producto

    tasa_ieps = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0'))
    ieps_producto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    # Retenciones por concepto
    tasa_retencion_iva = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0'))
    tasa_retencion_isr = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0'))

    retencion_iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    retencion_isr = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    def __str__(self):
        return self.producto.nombre

class Compra(models.Model):
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)
    usuario = models.CharField(max_length=40, blank=True)
    clave_movimiento = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT)
    referencia = models.CharField(max_length=7,blank=False,default="")
    pedido = models.CharField(max_length=7,blank=True,default="")
    fecha_compra = models.DateField(blank=False)
    fecha_vencimiento = models.DateField(blank=False)
    fecha_pagada = models.DateField(blank=False)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.RESTRICT)
    moneda = models.ForeignKey(Moneda,on_delete=models.RESTRICT)
    paridad = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    flete = models.DecimalField(default=0,decimal_places=2, max_digits=10,null=True)
    descuento_pp = models.DecimalField(default=1,decimal_places=2, max_digits=10,null=False)
    monto_total = models.DecimalField(default=0,decimal_places=2, max_digits=10,null=True)
    
    def __str__(self):
        return self.referencia

class DetalleCompra(models.Model):
    referencia = models.ForeignKey(Compra,related_name='detalles',on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    costo_unit = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    descuento = models.DecimalField(null=True, decimal_places=2, max_digits=10, blank=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    def __str__(self):
        return self.producto.nombre

class Traspaso(models.Model):
    usuario = models.CharField(max_length=40, blank=True)
    referencia = models.CharField(max_length=7, blank=False)
    fecha_traspaso = models.DateField(blank=False)
    alm1 = models.ForeignKey(Almacen,on_delete=models.RESTRICT, related_name='traspasos_salida')
    alm2 = models.ForeignKey(Almacen,on_delete=models.RESTRICT, related_name='traspasos_entrada')

    def __str__(self):
        return self.referencia

class DetalleTraspaso(models.Model):
    referencia = models.ForeignKey(Traspaso,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.referencia

class SaldoInicial(models.Model):
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    existencia = models.DecimalField(decimal_places=2, max_digits=10, default=0,null=False)
    fecha = models.DateField(blank=False)
    
    def __str__(self):
        return self.producto.nombre
