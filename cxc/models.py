from django.db import models
from django.contrib.auth.models import User

# TipoCliente del 01 al 06 para asignarle el precio que le corresponde 
class TipoCliente(models.Model):
    tipo_cliente = models.SmallIntegerField(unique=True, null=False)
    nombre = models.CharField(max_length=30,blank=True)
    
    def __str__(self):
        return self.nombre

class RegimenFiscal(models.Model):
    regimen_fiscal = models.CharField(max_length=3)  # 601 602  
    nombre = models.CharField(max_length=110,blank=False)
    
    def __str__(self):
        return f'{self.regimen_fiscal} | {self.nombre}'

# 'C' cargo, 'A' abono
class ClaveMovimientoCxC(models.Model):   
    clave_movimiento = models.SmallIntegerField(default=1, null=False)
    nombre = models.CharField(max_length=30,null=True)
    tipo = models.CharField(max_length=1,default='C',blank=False)  # (C)argo o (A)bono  
    
    def __str__(self):
        return self.nombre 

class Cliente(models.Model):
    cliente = models.CharField(max_length=6,blank=False,unique=True)
    tipo_cliente = models.ForeignKey(TipoCliente,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=100,blank=False)
    rfc = models.CharField(max_length=13,blank=True)
    calle = models.CharField(max_length=50,blank=True,default="")  # direccion fiscal
    numero_exterior = models.CharField(max_length=10,blank=True)
    numero_interior = models.CharField(max_length=10,blank=True)
    colonia = models.CharField(max_length=30,blank=True)
    codigo_postal = models.CharField(max_length=5,default="",blank=True)  #cp fiscal
    ciudad = models.CharField(max_length=100,blank=True,default="")       #ciudad fiscal
    municipio = models.CharField(max_length=100,blank=True,default="")       #fiscal para factura
    estado = models.CharField(max_length=30,blank=True,default="")       #fiscal para factura
    direccion_entrega = models.TextField(blank=True,default="")
    codigo_postal_entrega = models.CharField(max_length=5,default="",blank=True)
    ciudad_entrega = models.CharField(max_length=100, blank=True,default="")
    telefono1 = models.CharField(max_length=20, blank=True,default="")
    telefono2 = models.CharField(max_length=20, blank=True,default="")
    email = models.EmailField(blank=True,default="")
    plazo_credito = models.SmallIntegerField(default=0, null=True)
    limite_credito = models.BigIntegerField(default=0,null=True)
    cuenta_cnt = models.CharField(max_length=24, blank=True,default="")
    aplica_retencion_iva = models.BooleanField(blank=True)   # False - No se aplica, True - Se aplica al facturar
    aplica_retencion_isr = models.BooleanField(blank=True)   # False - No se aplica, True - Se aplica al facturar
    regimen_fiscal = models.ForeignKey(RegimenFiscal,on_delete=models.RESTRICT)
    campo_libre_str = models.CharField(max_length=50,blank=True,default="")  # contacto
    campo_libre_num = models.FloatField(null=True,default=0, blank=True) 
    comentarios = models.TextField(blank=True,default="")

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    clave_movimiento = models.ForeignKey(ClaveMovimientoCxC,on_delete=models.RESTRICT)
    referencia_cargo = models.CharField(max_length=8, blank=False)
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    concepto = models.CharField(max_length=50, blank=True)
    fecha_movimiento = models.DateField(blank=False)
    fecha_vencimiento = models.DateField(blank=False)
    fecha_pago = models.DateField(blank=True)
    saldada = models.BooleanField(default=False)
    almacen = models.ForeignKey('inv.Almacen',on_delete=models.RESTRICT)

    def __str__(self): 
        return self.referencia_cargo
    
class Abono(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.RESTRICT)
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    clave_movimiento = models.ForeignKey(ClaveMovimientoCxC,on_delete=models.RESTRICT)
    referencia = models.CharField(max_length=8, blank=False)
    almacen = models.ForeignKey('inv.Almacen',on_delete=models.RESTRICT)
    referencia_cargo = models.ForeignKey(Cargo,on_delete=models.RESTRICT)
    fecha_movimiento = models.DateField(blank=False)
    concepto = models.CharField(max_length=50, blank=True)
    importe = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    
    def __str__(self):
        return self.referencia

class SaldoInicialCxC(models.Model):
    almacen = models.ForeignKey('inv.Almacen',on_delete=models.RESTRICT)
    cliente = models.ForeignKey(Cliente,on_delete=models.RESTRICT)
    saldo = models.DecimalField(decimal_places=2, max_digits=10, default=0,null=False)
    fecha = models.DateField(blank=False)
    
    def __str__(self):
        return self.cliente.nombre
