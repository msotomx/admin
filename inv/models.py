from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    categoria = models.IntegerField(null=False, default=1)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre 

class UnidadMedida(models.Model):
    unidad_medida = models.CharField(max_length=20,blank=False)
    descripcion = models.CharField(max_length=30,blank=False)

    def __str__(self):
        return self.unidad_medida

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

    def __str__(self):
        return f"{self.nombre} ({self.clave})"

# 'E' entrada, 'S' salida, 'C' compras
class ClaveMovimiento(models.Model):   
    clave_movimiento = models.CharField(max_length=2,default='', blank=False, unique=True)
    nombre = models.CharField(max_length=30,null=True)
    tipo = models.CharField(max_length=1,default='E',blank=False)  # E o S 
    
    def __str__(self):
        return self.nombre 

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100,blank=False,default=" ")
    direccion = models.TextField(null=True,default="")
    contacto = models.CharField(max_length=100,default="")
    telefono1 = models.CharField(max_length=20,default="")
    telefono2 = models.CharField(max_length=20,default="")
    email = models.EmailField(blank=True,default="")
    plazo_credito = models.SmallIntegerField(default=0)
    comentarios = models.TextField(blank=True,default="")
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=12, default='',blank=False)
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
    unidad_de_medida = models.ForeignKey(UnidadMedida,on_delete=models.RESTRICT)
    descuento_venta = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    costo_reposicion = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    iva = models.DecimalField(max_digits=10,decimal_places=4)  # Tasa de IVA
    campo_libre_str = models.CharField(max_length=50,blank=True,default='')
    campo_libre_num = models.DecimalField(max_digits=10,decimal_places=4, default=0, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    referencia = models.CharField(max_length=8, blank=False,unique=True)
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
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    descuento = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    subtotal = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.referencia

class Traspaso(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    referencia = models.CharField(max_length=8, blank=False)
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

class Remision(models.Model):
    ESTADO_CHOICES = (
        ('C','Cotizacion'),  # no genera movimiento de Salida
        ('P','Pedido'),      # no genera movimiento de Salida
        ('R','Remisionado'), # si genera movimiento de Salida
        ('F','Facturado')    # la remision se ha facturado
    )

    numero_remision = models.CharField(max_length=6,blank=False,default="")
    numero_factura = models.CharField(max_length=20,blank=False,default="")
    clave_remision = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT)
    cliente = models.ForeignKey('cxc.Cliente',on_delete=models.RESTRICT)
    fecha_remision = models.DateField(blank=False)
    monto_total = models.DecimalField(default=0,decimal_places=2, max_digits=10,null=True)
    estado = models.CharField(max_length=1,default='R',choices=ESTADO_CHOICES)   # CON Esto, solo permite 0 o 1

    def __str__(self):
        return self.numero_remision

class DetalleRemision(models.Model):
    numero_remision = models.ForeignKey(Remision,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    cantidad = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    precio = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    descuento = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    def __str__(self):
        return self.producto.nombre

class SaldoInicial(models.Model):
    almacen = models.ForeignKey(Almacen,on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)
    existencia = models.DecimalField(decimal_places=2, max_digits=10, default=0,null=False)
    fecha = models.DateField(blank=False)
    
    def __str__(self):
        return self.producto.nombre
