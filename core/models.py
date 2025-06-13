from django.db import models
from django.contrib.auth.models import User
from datetime import date
from cxc.models import RegimenFiscal

# Create your models here.
class Empresa(models.Model):
    nombre_comercial = models.CharField(max_length=50, blank=True)
    num_empresa = models.CharField(max_length=8,blank=False, unique=True)   # es el ID en la BD del Servidor
    activa = models.BooleanField(default=False)
    directorio = models.CharField(max_length=30,blank=True)   # es la ubicacion dentro del servidor
    fecha_inicio = models.DateField()
    fecha_renovacion = models.DateField()
    almacen_actual = models.IntegerField(null=False,default=1)
    almacen_facturacion = models.IntegerField(null=False,default=1,blank=True)
    decimales_unidades = models.SmallIntegerField(null=False,default=2,blank=True)
    decimales_importe = models.SmallIntegerField(null=False,default=2,blank=True)
    cuenta_iva = models.CharField(max_length=24,blank=True)  #cuenta iva contabilidad
    clave_compras = models.CharField(max_length=2,blank=False,default='CO')
    clave_traspasos = models.CharField(max_length=2,blank=False,default='TR')
    clave_remision = models.CharField(max_length=2,blank=False,default='R1')
    tasa_iva = models.DecimalField(max_digits=9,decimal_places=2)   # tasa de iva en facturas
    tasa_ieps = models.DecimalField(max_digits=9,decimal_places=5)  # Tasa de IEPS
    tasa_retencion_iva = models.DecimalField(max_digits=9,decimal_places=5)  #Tasa de Retencion 16% = 16, 8% = 8 se usa al facturar
    tasa_retencion_isr = models.DecimalField(max_digits=9,decimal_places=5)  
    ip = models.CharField(max_length=24,blank=True)  #direccion ip de la app en el servidor
    comentarios = models.TextField(blank=True)
    factor = models.DecimalField(max_digits=10,decimal_places=5,blank=True) # campo extra
    #DATOS FISCALES
    nombre_fiscal = models.CharField(max_length=80, blank=True)
    rfc = models.CharField(max_length=13,blank=True)
    regimen_de_sociedad = models.CharField(max_length=25, blank=True)
    regimen_fiscal = models.ForeignKey(RegimenFiscal,on_delete=models.RESTRICT, default='1',blank=True,null=True)
    representante = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True,default="")
    calle = models.CharField(max_length=50, blank=True)
    numero_exterior = models.CharField(max_length=6, blank=True)
    numero_interior = models.CharField(max_length=6, blank=True)
    colonia = models.CharField(max_length=40, blank=True)
    codigo_postal = models.CharField(max_length=5, blank=True)
    localidad = models.CharField(max_length=30, blank=True)
    municipio = models.CharField(max_length=40, blank=True)
    estado = models.CharField(max_length=20, blank=True)
    pais = models.CharField(max_length=20, blank=True)
    ruta_xml = models.CharField(max_length=100, blank=True)
    pagina_web = models.CharField(max_length=50, blank=True)
    #LUGAR DE EXPEDICION
    calle_expedicion = models.CharField(max_length=50, blank=True)
    numero_exterior_expedicion = models.CharField(max_length=6, blank=True)
    numero_interior_expedicion = models.CharField(max_length=6, blank=True)
    colonia_expedicion = models.CharField(max_length=40, blank=True)
    codigo_postal_expedicion = models.CharField(max_length=5, blank=True)
    localidad_expedicion = models.CharField(max_length=30, blank=True)
    municipio_expedicion = models.CharField(max_length=40, blank=True)
    estado_expedicion = models.CharField(max_length=20, blank=True)
    pais_expedicion = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre_comercial

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.empresa.nombre_comercial}'

class CertificadoCSD(models.Model):
    empresa = models.OneToOneField(User, on_delete=models.CASCADE)
    rfc = models.CharField(max_length=13)
    cer_archivo = models.FileField(upload_to='csd/')
    key_archivo = models.FileField(upload_to='csd/')
    password = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CSD de {self.empresa.username} - {self.rfc}"
