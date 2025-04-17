from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empresa(models.Model):
    empresa = models.OneToOneField(User,on_delete=models.RESTRICT)
    id_empresa = models.CharField(max_length=8,null=False)   # es el ID en la BD del Servidor
    directorio = models.CharField(max_length=8,null=False)   # es la ubicacion dentro del servidor
    fecha_inicio = models.DateField()
    almacen_actual = models.CharField(max_length=2,null=False,default='01')
    almacen_facturacion = models.CharField(max_length=2,null=False,default='01')
    decimales_unidades = models.SmallIntegerField(null=False,default='2')
    decimales_importe = models.SmallIntegerField(null=False,default='2')
    cuenta_iva = models.CharField(max_length=24,null=True)  #cuenta iva contabilidad
    clave_compras = models.CharField(max_length=2,null=False,default='CO')
    clave_traspasos = models.CharField(max_length=2,null=False,default='TR')
    clave_remision = models.CharField(max_length=2,null=False,default='RE')
    iva = models.DecimalField(max_digits=9,decimal_places=2)   # iva en facturas
    retencion_iva = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de iva en facturas
    retencion_isr = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de isr en facturas
    ieps = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de ieps en facturas
    ip = models.CharField(max_length=24,null=True)  #direccion ip de la app en el servidor

    def __str__(self):
        return self.nombre 
 
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_lenght=3)
    subcategoria = models.CharField(max_lenght=3)

    def __str__(self):
        return self.nombre 

# TipoCliente del 01 al 06 para asignarle el precio que le corresponde 
class TipoCliente(models.Model):
    tipo = models.CharField(max_length=2,default='01')
    nombre = models.CharField(max_length=30,null=True)
    
    def __str__(self):
        return self.nombre 

class Almacen(models.Model):
    clave = models.CharField(max_length=2,default='01')
    nombre = models.CharField(max_length=30,null=True)
    
    def __str__(self):
        return self.nombre 

class Moneda(models.Model):
    nombre = models.CharField(max_length=30,null=True)
    
    def __str__(self):
        return self.nombre
    
class UnidadMedida(models.Model):
    unidad_medida = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=30)

# 'E' entrada, 'S' salida, 'C' compras
class ClaveMovimiento(models.Model):   
    clave_movimiento = models.CharField(max_length=2,default='01')
    nombre = models.CharField(max_length=30,null=True)
    tipo = models.CharField(max_length=1,default='E')  # E o S 
    
    def __str__(self):
        return self.nombre 

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(null=True)
    contacto = models.CharField(max_length=100)
    telefono1 = models.CharField(max_length=13)
    telefono2 = models.CharField(max_length=13)
    email = models.EmailField(null=True)
    plazo_credito = models.SmallIntegerField(default=0)
    comentarios = models.TextField(null=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=12, default='')
    categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    subcategoria = models.CharField(max_length=3)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    precio1 = models.DecimalField(max_digits=9,decimal_places=2)
    precio2 = models.DecimalField(max_digits=9,decimal_places=2)
    precio3 = models.DecimalField(max_digits=9,decimal_places=2)
    precio4 = models.DecimalField(max_digits=9,decimal_places=2)
    precio5 = models.DecimalField(max_digits=9,decimal_places=2)
    precio6 = models.DecimalField(max_digits=9,decimal_places=2)
    maximo  = models.SmallIntegerField(default=0) 
    minimo  = models.SmallIntegerField(default=0) 
    reorden = models.SmallIntegerField(default=0) 
    fecha_registro = models.DateField()
    imagen = models.ImageField(upload_to='productos',blank=True)
    proveedor = models.ForeignKey(Proveedor,on_delete=models.RESTRICT)
    unidad_de_medida = models.ForeignKey(UnidadMedida,on_delete=models.RESTRICT)
    descuento_venta = models.DecimalField(default=0)
    costo_reposicion = models.DecimalField(max_length=15, default=0)
    iva = models.DecimalField(max_digits=10,decimal_places=4)  # Tasa de IVA
    campo_libre_str = models.CharField(max_length=50, null=True)
    campo_libre_real = models.FloatField(max_length=15, default=0)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    cliente = models.CharField(max_length=6,null=False)
    tipoCliente = models.ForeignKey(TipoCliente,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=100,null=False)
    rfc = models.CharField(max_length=13)
    telefono = models.CharField(max_length=12)
    direccion = models.TextField(null=True)  # direccion fiscal
    codigo_postal = models.CharField(max_length=5,default="00000")  #cp fiscal
    ciudad = models.CharField(max_length=100, null=True)       #ciudad fiscal
    direccion_entrega = models.TextField(null=True)
    codigo_postal_entrega = models.CharField(max_length=5,default="00000")
    ciudad_entrega = models.CharField(max_length=100, null=True)
    telefono1 = models.CharField(max_length=13, null=True)
    telefono2 = models.CharField(max_length=13, null=True)
    email = models.EmailField(null=True)
    plazo_credito = models.SmallIntegerField(default=0)
    limite_credito = models.BigIntegerField(max_digits=10,decimal_places=2,default=0)
    cuenta_cnt = models.CharField(max_length=24, null=True)
    retencion_iva = models.BooleanField(default='False')   # False - No se aplica, True - Se aplica al facturar
    retencion_isr = models.BooleanField(default='False')   # False - No se aplica, True - Se aplica al facturar
    ieps = models.BooleanField(default='False')            # False - No se aplica, True - Se aplica al facturar
    campo_libre_str = models.CharField(max_length=50, null=True)
    campo_libre_real = models.FloatField(max_length=15, default=0) 
    comentarios = models.TextField(null=True)

    def __str__(self):
        return self.rfc

class Movimiento(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    referencia = models.CharField(max_length=8, null=False)
    move_s = models.CharField(max_length=1, null=False)  # 'E' entrada 'S' salida
    clave_movimiento = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT)
    fecha_movimiento = models.DateField()
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)

    def __str__(self):
        return self.referencia
    
class DetalleMovimiento(models.Model):
    referencia = models.ForeignKey(Movimiento,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(max_length=10,null=True)
    precio = models.DecimalField(max_length=10,null=True)
    descuento = models.DecimalField(max_length=10,null=True)
    subtotal = models.DecimalField(max_length=10,null=True)

    def __str__(self):
        return self.referencia

class Traspaso(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    referencia = models.CharField(max_length=8, null=False)
    fecha_traspaso = models.DateField()
    alm1 = models.ForeignKey(Almacen,on_delete=models.RESTRICT)
    alm2 = models.ForeignKey(Almacen,on_delete=models.RESTRICT)

    def __str__(self):
        return self.referencia

class DetalleTraspaso(models.Model):
    referencia = ForeignKey(Traspaso,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(max_length=10,null=True)

    def __str__(self):
        return self.referencia

class Remision(models.Model):
        ESTADO_CHOICES = (
        ('C','Cotizacion'),  # no genera movimiento de Salida
        ('P','Pedido'),      # no genera movimiento de Salida
        ('R','Remisionado'), # si genera movimiento de Salida
        ('F','Facturado')    # la remision se ha facturado
    )

    numero_remision = models.CharField(max_length=6,null=False)
    numero_factura = models.CharField(max_length=20,null=True)
    clave_remision = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT)
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)   # ForeingKey - relacion de muchos a uno
    fecha_remision = models.DateField()
    monto_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    estado = models.CharField(max_length=1,default='R',choices=ESTADO_CHOICES)   # CON Esto, solo permite 0 o 1

    def __str__(self):
        return self.numero_pedido

class DetalleRemision(models.Model):
    numero_remision = models.ForeignKey(Remision,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_length=10,null=True)
    descuento = models.DecimalField(max_length=10,null=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(delf):
        return self.producto.nombre

class SaldoInicial(models.Model):
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    Existencia = models.DecimalField(decimal_places=4, default=0)
    fecha = models.DateField()
    
