from django.db import models

# Create your models here.
class MovimientoTimbresGlobal(models.Model):
    referencia = models.CharField(max_length=7)
    codigo_empresa = models.CharField(max_length=7)
    usuario = models.CharField(max_length=20)
    tipo = models.CharField(max_length=1)
    fecha = models.DateField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unit = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.referencia} - {self.fecha.strftime('%Y-%m-%d')} - (+{self.cantidad})"

class TimbresCliente(models.Model):
    codigo_empresa = models.CharField(max_length=7)
    total_asignados = models.BigIntegerField(default=0)
    utilizados = models.BigIntegerField(default=0)
    fecha_asignacion = models.DateField(blank=False)

    @property
    def disponibles(self):
        return self.total_asignados - self.utilizados

    def __str__(self):
        return f"{self.codigo_empresa} - {self.disponibles} disponibles"

