from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Empresa(models.Model):
    empresa = models.OneToOneField(User,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=50, blank=True)
    num_empresa = models.CharField(max_length=8,blank=False, unique=True)   # es el ID en la BD del Servidor
    activa = models.BooleanField(default=False)
    directorio = models.CharField(max_length=30,blank=True)   # es la ubicacion dentro del servidor
    fecha_inicio = models.DateField()
    fecha_renovacion = models.DateField()   #default=date(2025, 9, 30)) 
    almacen_actual = models.IntegerField(null=False,default=1)
    almacen_facturacion = models.IntegerField(null=False,default=1)
    decimales_unidades = models.SmallIntegerField(null=False,default=2)
    decimales_importe = models.SmallIntegerField(null=False,default=2)
    cuenta_iva = models.CharField(max_length=24,blank=True)  #cuenta iva contabilidad
    clave_compras = models.CharField(max_length=2,blank=False,default='CO')
    clave_traspasos = models.CharField(max_length=2,blank=False,default='TR')
    clave_remision = models.CharField(max_length=2,blank=False,default='RE')
    iva = models.DecimalField(max_digits=9,decimal_places=2)   # iva en facturas
    retencion_iva = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de iva en facturas
    retencion_isr = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de isr en facturas
    ieps = models.DecimalField(max_digits=9,decimal_places=5)  # % de retencion de ieps en facturas
    ip = models.CharField(max_length=24,blank=False)  #direccion ip de la app en el servidor
    comentarios = models.TextField(blank=True)
    factor = models.DecimalField(max_digits=10,decimal_places=5) # campo extra

    def __str__(self):
        return self.nombre 
