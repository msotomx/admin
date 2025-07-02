from django.db import models
from django.contrib.auth.models import User
from cxc.models import Cliente
from inv.models import Moneda, Producto, ClaveMovimiento
from core.models import Empresa
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
        ('Borrador','Borrador'),  
        ('Vigente','Vigente'),      
        ('Cancelada','Cancelado'), 
        ('Error','Error') 
            )
    usuario = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.RESTRICT)
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
    descuento_factura = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    iva_factura = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ieps_factura = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retencion_iva_factura = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retencion_isr_factura = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos_trasladados = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos_retenidos   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    serie_emisor = models.CharField(max_length=50,blank=False,default="")
    lugar_expedicion = models.CharField(max_length=5,blank=False,default="")
    tipo_cambio      = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    tipo_comprobante = models.ForeignKey(TipoComprobante,on_delete=models.RESTRICT)
    exportacion      = models.ForeignKey(Exportacion,on_delete=models.RESTRICT)
    condiciones_pago = models.CharField(max_length=30, default="1") # CONTADO, 30 DIAS, ETC

    # Archivos generados
    xml = models.FileField(upload_to='cfdi/xml/', null=True, blank=True)
    pdf = models.FileField(upload_to='cfdi/pdf/', null=True, blank=True)

    # Información de timbrado
    uuid = models.CharField(max_length=40, blank=True)
    fecha_timbrado = models.DateTimeField(null=True, blank=True)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    
    sello     = models.TextField(blank=True)
    sello_sat = models.TextField(blank=True)
    num_certificado=models.CharField(max_length=21, blank=True)
    rfc_certifico  =models.CharField(max_length=13, blank=True)

    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default="Borrador")  # o 'TIMBRADA', 'CANCELADA' 'ERROR'

    def __str__(self):
        return f'{self.numero_factura or ""} - {self.cliente.nombre}'

from decimal import Decimal, ROUND_HALF_UP
class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    clave_prod_serv = models.CharField(max_length=10)  # Catálogo SAT (ej. 01010101)
    clave_unidad = models.CharField(max_length=5)      # SAT (ej. H87)
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=4)
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    # impuestos,iva
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

    # información adicional
    objeto_impuesto = models.CharField(max_length=3, default='02')  # Obligatorio desde CFDI 4.0

    def calcular_importes(self):
        # importe neto:
        neto = (self.cantidad * self.valor_unitario) - self.descuento
        self.importe = neto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # tasas de: iva, ieps, retencion de iva, retencion de isr
        if not self.factura.empresa:
            raise ValueError("No hay empresa asignada a la factura de este detalle")

        tasa_iva  = Decimal('0.0')
        tasa_ieps = Decimal('0.0')
        if self.producto.aplica_iva:
             tasa_iva = (self.factura.empresa.tasa_iva) / Decimal('100')
        if self.producto.aplica_ieps:
             tasa_ieps = (self.factura.empresa.tasa_ieps) / Decimal('100')
        self.tasa_iva  = tasa_iva
        self.tasa_ieps = tasa_ieps

        tasa_retencion_iva = Decimal('0.0')
        tasa_retencion_isr = Decimal('0.0')
        if self.factura.cliente.aplica_retencion_iva:
            tasa_retencion_iva = (self.factura.empresa.tasa_retencion_iva) / Decimal('100')
        if self.factura.cliente.aplica_retencion_isr:
            tasa_retencion_isr = (self.factura.empresa.tasa_retencion_isr) / Decimal('100')
        
        self.tasa_retencion_iva = tasa_retencion_iva
        self.tasa_retencion_isr = tasa_retencion_isr

        # Calculo de iva
        iva = self.importe * tasa_iva
        self.iva_producto = iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # ieps
        ieps = self.importe * tasa_ieps
        self.ieps_producto = ieps.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # retencion_iva
        retencion_iva = iva * tasa_retencion_iva
        self.retencion_iva = retencion_iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # retencion_isr
        retencion_isr = self.importe * tasa_retencion_isr
        self.retencion_isr = retencion_isr.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def grabar(self, using=None):
        """
        Método único de mantenimiento:  
        calcula impuestos y luego hace save().
        """
        self.calcular_importes()
        super().save(using=using)

    def __str__(self):
        return f'{self.descripcion} ({self.cantidad})'
