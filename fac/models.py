from django.db import models
from django.contrib.auth.models import User
from cxc.models import Cliente
from inv.models import Moneda, Producto, ClaveMovimiento
from decimal import Decimal

# Create your models here.

class FormaPago(models.Model):
    forma_pago = models.CharField(max_length=2)  # 01=Efectivo, 03=Transferencia, etc.
    nombre = models.CharField(max_length=40,blank=False)
    
    def __str__(self):
        return self.nombre

class MetodoPago(models.Model):
    metodo_pago = models.CharField(max_length=3)  # PUE o PPD
    nombre = models.CharField(max_length=40,blank=False)

    def __str__(self):
        return self.nombre

class TipoComprobante(models.Model):
    tipo_comprobante = models.CharField(max_length=1, choices=[('I', 'Ingreso'), ('E', 'Egreso'), ('T', 'Traslado')])
    nombre = models.CharField(max_length=30,blank=False)

    def __str__(self):
        return self.nombre

class UsoCfdi(models.Model):
    uso_cfdi = models.CharField(max_length=5)  # por ejemplo: G03
    nombre = models.CharField(max_length=106,blank=False)

    def __str__(self):
        return f'{self.uso_cfdi} | {self.nombre}'

class Exportacion(models.Model):
    exportacion = models.CharField(max_length=20,blank=False)
    nombre = models.CharField(max_length=30,blank=False)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    ESTATUS_CHOICES = (
        ('BORRADOR','Borrador'),  
        ('TIMBRADA','Timbrado'),      
        ('CANCELADA','Cancelado'), 
        ('ERROR','Error') 
            )
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    clave_remision = models.ForeignKey(ClaveMovimiento,on_delete=models.RESTRICT, blank=True)
    numero_remision = models.CharField(max_length=7,blank=False,default="")
    numero_factura = models.CharField(max_length=7,blank=False,default="")
    fecha_emision = models.DateField(blank=False)
    forma_pago = models.ForeignKey(FormaPago,on_delete=models.RESTRICT)
    metodo_pago = models.ForeignKey(MetodoPago,on_delete=models.RESTRICT)
    moneda = models.ForeignKey(Moneda,on_delete=models.RESTRICT)
    uso_cfdi = models.ForeignKey(UsoCfdi,on_delete=models.RESTRICT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    impuestos_trasladados = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos_retenidos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    serie_emisor = models.CharField(max_length=50,blank=False,default="")
    serie_sat = models.CharField(max_length=50,blank=False,default="")
    fecha_hora_certificacion = models.DateField(blank=False)
    lugar_expedicion = models.CharField(max_length=5,blank=False,default="")
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    tipo_comprobante = models.ForeignKey(TipoComprobante,on_delete=models.RESTRICT)
    exportacion = models.ForeignKey(Exportacion,on_delete=models.RESTRICT)
    condiciones_pago = models.CharField(max_length=1,default="1") # 1- CONTADO 2-CREDITO

    # Archivos generados
    xml = models.FileField(upload_to='cfdi/xml/', null=True, blank=True)
    pdf = models.FileField(upload_to='cfdi/pdf/', null=True, blank=True)

    # Información de timbrado
    uuid = models.CharField(max_length=40, blank=True)
    fecha_timbrado = models.DateTimeField(null=True, blank=True)
    sello_cfdi = models.TextField(blank=True)
    no_certificado_sat = models.CharField(max_length=21, blank=True)
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default='BORRADOR')  # o 'TIMBRADA', 'CANCELADA' 'ERROR'

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.numero_factura or ""} - {self.cliente.nombre}'

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    clave_prod_serv = models.CharField(max_length=10)  # Catálogo SAT (ej. 01010101)
    clave_unidad = models.CharField(max_length=5)      # SAT (ej. H87)
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=4)
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # impuestos
    tasa_iva = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))  # ej. 16.00
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    # Impuestos trasladados por concepto

    tasa_ieps = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    ieps = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    # Retenciones por concepto (si aplican)
    retencion_iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    retencion_isr = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))

    # información adicional
    objeto_imp = models.CharField(max_length=3, default='02')  # Obligatorio desde CFDI 4.0

    def calcular_importes(self):
        self.importe = self.cantidad * self.valor_unitario
        tasa = Decimal(self.tasa_iva) / Decimal(100)
        self.iva = (self.importe - self.descuento) * tasa

    def save(self, *args, **kwargs):
        self.calcular_importes()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.descripcion} ({self.cantidad})'
