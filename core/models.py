from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Empresa(models.Model):
    empresa = models.OneToOneField(User,on_delete=models.RESTRICT)
    id_empresa = models.CharField(max_length=8,blank=False)   # es el ID en la BD del Servidor
    activa = models.BooleanField(default=False)
    directorio = models.CharField(max_length=8,blank=False)   # es la ubicacion dentro del servidor
    fecha_inicio = models.DateField()
    almacen_actual = models.IntegerField(null=False,default=1)
    almacen_facturacion = models.IntegerField(null=False,default=1)
    decimales_unidades = models.SmallIntegerField(null=False,default=2)
    decimales_importe = models.SmallIntegerField(null=False,default=2)
    cuenta_iva = models.CharField(max_length=24,null=True)  #cuenta iva contabilidad
    clave_compras = models.CharField(max_length=2,blank=False,default='CO')
    clave_traspasos = models.CharField(max_length=2,blank=False,default='TR')
    clave_remision = models.CharField(max_length=2,blank=False,default='RE')
    iva = models.DecimalField(max_digits=9,decimal_places=2)   # iva en facturas
    retencion_iva = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de iva en facturas
    retencion_isr = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de isr en facturas
    ieps = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de ieps en facturas
    ip = models.CharField(max_length=24,null=True)  #direccion ip de la app en el servidor

    def __str__(self):
        return self.id_empresa 
